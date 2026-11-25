import type {
  AnhSangMoiTruong,
  LoaiBoiCanh,
  LoaiThoiTiet,
} from '../kieu_dai';
import { bamChuoiTatDinh } from '../vfx/tat_dinh.ts';
import type { KetQuaBienDoiCamera } from '../vfx/dao_dien_camera.ts';
import { easeInOutSine, kepGiaTri, noiSuy } from '../xuong/duong_cong.ts';
import { BOI_CANH_TRONG_NHA, BOI_CANH_VU_TRU } from './moi_truong_logic.ts';

export type BienDoiKenBurnsAI = {
  scale: number;
  tx: number;
  ty: number;
};

export type CauHinhKhongKhiAI = {
  loaiAnhSang: string;
  laTrongNha: boolean;
  laVuTru: boolean;
  coLuongNangXien: boolean;
  coBuiSang: boolean;
  coAnhNenNhapNhay: boolean;
  coSuongDem: boolean;
  coMayChimNgoaiTroi: boolean;
  coMua: boolean;
  coTuyet: boolean;
  coLaRoi: boolean;
  mauHatSang: string;
};

/**
 * Tinh chuyen dong may quay cham muot (Ken Burns + parallax nhe theo MayQuayDong)
 * cho anh nen minh hoa AI 16:9, dam bao 100% tat dinh va KHONG BAO GIO lo vien den.
 */
export function tinhKenBurnsNenAI(
  frame: number,
  thoiLuongCanh: number,
  seedStr: string,
  cam?: Pick<KetQuaBienDoiCamera, 'panX' | 'panY' | 'zoom'>,
  laKhungTranhDacTa = false,
): BienDoiKenBurnsAI {
  const f = Number.isFinite(frame) ? Math.max(0, frame) : 0;
  const tong = Math.max(1, Number.isFinite(thoiLuongCanh) ? thoiLuongCanh : 120);
  const tienDo = easeInOutSine(kepGiaTri(f / tong, 0, 1));
  const seed = bamChuoiTatDinh(seedStr || 'boi_canh_ai');
  const huongX = seed % 2 === 0 ? 1 : -1;
  const huongY = (seed >> 2) % 2 === 0 ? 1 : -1;
  const zoomVao = (seed >> 4) % 3 !== 0;

  const minScale = laKhungTranhDacTa ? 1.05 : 1.035;
  const maxScale = laKhungTranhDacTa ? 1.145 : 1.095;
  const scale = zoomVao
    ? noiSuy(minScale, maxScale, tienDo)
    : noiSuy(maxScale, minScale, tienDo);

  // Bien do Ken Burns cham muot + bu tru parallax nhe theo MayQuayDong (cho cam giac chieu sau 2.5D)
  const bienDoPanX = laKhungTranhDacTa ? 34 : 20;
  const bienDoPanY = laKhungTranhDacTa ? 16 : 9;
  const kbX = noiSuy(-bienDoPanX * huongX, bienDoPanX * huongX, tienDo);
  const kbY = noiSuy(-bienDoPanY * huongY, bienDoPanY * huongY, tienDo);

  const camPanX = Number.isFinite(cam?.panX) ? (cam?.panX ?? 0) : 0;
  const camPanY = Number.isFinite(cam?.panY) ? (cam?.panY ?? 0) : 0;
  const parallaxX = -kepGiaTri(camPanX, -180, 180) * 0.14;
  const parallaxY = -kepGiaTri(camPanY, -120, 120) * 0.08;

  // Khoa bien tuyet doi de mep anh 1920x1080 luon phu kin khung hinh
  const maxTx = Math.max(0, 960 * (scale - 1) - 2);
  const maxTy = Math.max(0, 540 * (scale - 1) - 2);

  return {
    scale: Number(scale.toFixed(4)),
    tx: Number(kepGiaTri(kbX + parallaxX, -maxTx, maxTx).toFixed(2)),
    ty: Number(kepGiaTri(kbY + parallaxY, -maxTy, maxTy).toFixed(2)),
  };
}

/**
 * Xac dinh cac lop khong khi song dong tat dinh phu len anh nen minh hoa AI
 * dua tren anhSangMoiTruong, thoiTiet, boiCanh va laKhungTranhDacTa.
 */
export function tinhLopKhongKhiNenAI(
  anhSang?: AnhSangMoiTruong,
  thoiTiet: LoaiThoiTiet = 'khong',
  boiCanh: LoaiBoiCanh = 'thu_vien_co_dien',
  laKhungTranhDacTa = false,
): CauHinhKhongKhiAI {
  const laTrongNha = BOI_CANH_TRONG_NHA.has(boiCanh);
  const laVuTru = BOI_CANH_VU_TRU.has(boiCanh);

  const loaiAnhSang = String(
    anhSang?.loaiAnhSang ||
      (thoiTiet === 'ban_dem'
        ? 'dem_lanh'
        : thoiTiet === 'hoang_hon'
          ? 'hoang_hon'
          : thoiTiet === 'nang_dep'
            ? 'nang_am'
            : 'trung_tinh'),
  ).toLowerCase();

  const coLuongNangXien =
    loaiAnhSang === 'nang_am' ||
    loaiAnhSang === 'hoang_hon' ||
    (thoiTiet === 'nang_dep' && loaiAnhSang !== 'dem_lanh');

  const coAnhNenNhapNhay = loaiAnhSang === 'anh_nen';
  const coSuongDem = loaiAnhSang === 'dem_lanh' || thoiTiet === 'ban_dem';
  const coBuiSang =
    coLuongNangXien ||
    coAnhNenNhapNhay ||
    coSuongDem ||
    laKhungTranhDacTa ||
    loaiAnhSang === 'trung_tinh';

  const coMayChimNgoaiTroi =
    !laTrongNha &&
    !laVuTru &&
    !laKhungTranhDacTa &&
    boiCanh !== 'phong_nen_hai_huoc' &&
    thoiTiet !== 'ban_dem';

  const coMua = thoiTiet === 'mua_nhe' && !laTrongNha && !laVuTru;
  const coTuyet = thoiTiet === 'tuyet_roi' && !laTrongNha && !laVuTru;
  const coLaRoi = thoiTiet === 'la_roi' && !laTrongNha && !laVuTru;

  const mauHatSang =
    loaiAnhSang === 'anh_nen'
      ? '#FDE68A'
      : loaiAnhSang === 'hoang_hon'
        ? '#FED7AA'
        : loaiAnhSang === 'dem_lanh'
          ? '#BAE6FD'
          : loaiAnhSang === 'nang_am'
            ? '#FEF9C3'
            : '#F8FAFC';

  return {
    loaiAnhSang,
    laTrongNha,
    laVuTru,
    coLuongNangXien,
    coBuiSang,
    coAnhNenNhapNhay,
    coSuongDem,
    coMayChimNgoaiTroi,
    coMua,
    coTuyet,
    coLaRoi,
    mauHatSang,
  };
}
