import type { CauHoiTuongTac, NhanVatTrongCanh } from '../kieu_dai';
import { kepGiaTri } from '../xuong/duong_cong.ts';

export const FPS_MAC_DINH = 30;
export const THOI_GIAN_DEM_NGUOC_MAC_DINH_GIAY = 3;

export type TrangThaiCauHoiTuongTac = {
  /** Frame bat dau dem nguoc cuc bo trong canh */
  batDauDemNguocFrame: number;
  /** Frame ket thuc dem nguoc / bat dau hien dap an */
  hienDapAnTuFrame: number;
  /** Tong so giay dem nguoc (mac dinh 3) */
  tongGiayDemNguoc: number;
  /** Dang o giai doan truoc khi bat dau dem nguoc (doc cau hoi) */
  dangDocCauHoi: boolean;
  /** Dang trong giai doan dong ho dem nguoc */
  dangDemNguoc: boolean;
  /** Da het gio va hien hop dap an */
  daHienDapAn: boolean;
  /** So giay con lai (3 -> 2 -> 1 -> 0) */
  giayConLai: number;
  /** Tien do con lai cua thanh dem nguoc [1 -> 0] */
  tiLeConLai: number;
  /** So frame da troi qua ke tu khi hien dap an */
  frameTuDapAn: number;
  /** Frame cuc bo trong giay hien tai (0..29) de bat lo xo nhip giay */
  frameTrongGiayHienTai: number;
};

/**
 * Tinh trang thai tat dinh 100% cua dong ho dem nguoc 3 giay + hop dap an cho canh tuong tac khan gia.
 */
export function tinhTrangThaiCauHoiTuongTac(
  cauHoi: CauHoiTuongTac,
  frame: number,
  thoiLuongCanh: number,
  fps = FPS_MAC_DINH,
): TrangThaiCauHoiTuongTac {
  const f = Number.isFinite(frame) ? frame : 0;
  const tong = Math.max(1, Number.isFinite(thoiLuongCanh) ? thoiLuongCanh : 150);
  const fpsHopLe = Math.max(1, Number.isFinite(fps) ? fps : FPS_MAC_DINH);

  const tongGiayDemNguoc = Math.max(
    1,
    Math.round(
      cauHoi.thoiGianDemNguocGiay ?? THOI_GIAN_DEM_NGUOC_MAC_DINH_GIAY,
    ),
  );
  const soFrameDemNguoc = tongGiayDemNguoc * fpsHopLe;

  const batDauDemNguocFrame =
    typeof cauHoi.batDauDemNguocFrame === 'number' &&
    Number.isFinite(cauHoi.batDauDemNguocFrame)
      ? Math.max(0, Math.round(cauHoi.batDauDemNguocFrame))
      : Math.min(24, Math.max(0, Math.floor((tong - soFrameDemNguoc) * 0.25)));

  const hienDapAnTuFrame =
    typeof cauHoi.hienDapAnTuFrame === 'number' &&
    Number.isFinite(cauHoi.hienDapAnTuFrame)
      ? Math.max(batDauDemNguocFrame + 1, Math.round(cauHoi.hienDapAnTuFrame))
      : batDauDemNguocFrame + soFrameDemNguoc;

  const doDaiDemThuc = Math.max(1, hienDapAnTuFrame - batDauDemNguocFrame);
  const dangDocCauHoi = f < batDauDemNguocFrame;
  const daHienDapAn = f >= hienDapAnTuFrame;
  const dangDemNguoc = !dangDocCauHoi && !daHienDapAn;

  let tiLeConLai = 1;
  let giayConLai = tongGiayDemNguoc;
  let frameTrongGiayHienTai = 0;

  if (daHienDapAn) {
    tiLeConLai = 0;
    giayConLai = 0;
  } else if (dangDemNguoc) {
    const daDem = f - batDauDemNguocFrame;
    tiLeConLai = kepGiaTri(1 - daDem / doDaiDemThuc, 0, 1);
    giayConLai = Math.max(
      1,
      Math.ceil((hienDapAnTuFrame - f) / (doDaiDemThuc / tongGiayDemNguoc)),
    );
    const frameMoiGiay = doDaiDemThuc / tongGiayDemNguoc;
    frameTrongGiayHienTai = daDem % frameMoiGiay;
  }

  return {
    batDauDemNguocFrame,
    hienDapAnTuFrame,
    tongGiayDemNguoc,
    dangDocCauHoi,
    dangDemNguoc,
    daHienDapAn,
    giayConLai,
    tiLeConLai,
    frameTuDapAn: daHienDapAn ? f - hienDapAnTuFrame : 0,
    frameTrongGiayHienTai,
  };
}

/**
 * Chia danh sach nhan vat sang khung trai va khung phai cho che do chia_doi_man_hinh.
 * Dam bao khi co 2 nhan vat luon tach ro moi ben 1 nguoi; khi >2 thi phan theo x < 960 vs x >= 960.
 */
export function chiaNhomNhanVatChiaDoi<T extends NhanVatTrongCanh>(
  danhSach: readonly T[],
): { benTrai: T[]; benPhai: T[] } {
  if (danhSach.length === 0) {
    return { benTrai: [], benPhai: [] };
  }
  if (danhSach.length === 1) {
    return { benTrai: [danhSach[0]], benPhai: [] };
  }
  if (danhSach.length === 2) {
    const sapXep = [...danhSach].sort((a, b) => a.x - b.x);
    return { benTrai: [sapXep[0]], benPhai: [sapXep[1]] };
  }

  const benTrai: T[] = [];
  const benPhai: T[] = [];
  for (const nv of danhSach) {
    if (nv.x < 960) {
      benTrai.push(nv);
    } else {
      benPhai.push(nv);
    }
  }
  if (benTrai.length === 0 && benPhai.length > 1) {
    benTrai.push(benPhai.shift()!);
  } else if (benPhai.length === 0 && benTrai.length > 1) {
    benPhai.push(benTrai.pop()!);
  }
  return { benTrai, benPhai };
}
