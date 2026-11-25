import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { build as esbuildBuild } from 'esbuild';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const gocDuAn = path.resolve(__dirname, '..');

/**
 * Bien dich tam cac module TypeScript thuan bang esbuild (co san trong node_modules cua Remotion)
 * de test_khung.mjs chay muot 100% tren ca Node 20 lan Node 22+ khong phu thuoc strip-types.
 */
async function napCacModuleTs() {
  const thuMucTam = fs.mkdtempSync(path.join(os.tmpdir(), 'video10p-test-khung-'));
  const tepBundle = path.join(thuMucTam, 'bundle.mjs');
  const donDep = () => {
    try {
      fs.rmSync(thuMucTam, { recursive: true, force: true });
    } catch {
      // bo qua loi don dep tam
    }
  };
  process.once('exit', donDep);

  const maNguonTongHop = `
export {
  GIOI_HAN_GOC_DAU_MAX,
  GIOI_HAN_GOC_DAU_MIN,
  tinhKhungXuongCoBan,
} from './src/xuong/he_xuong.ts';
export {
  chiaDongMoTaTimeline,
  coDuLieuMinhHoaHopLe,
  layDanhSachBuocSuyLuan,
  locMocThoiGianHopLe,
} from './src/daocu/minh_hoa_hop_le.ts';
export {
  chuanHoaKhungHinhLienMach,
  kiemTraKhungHinhLienMach,
} from './src/canh/dieu_phoi_canh.ts';
export { chiaDongBongBong, tinhThongSoHopTen } from './src/nhanvat/ten_nhan_vat.ts';
export {
  easeInBack,
  easeInOutCubic,
  easeOutBack,
  springTatDinh,
} from './src/xuong/duong_cong.ts';
export { bamTatDinh, bamChuoiTatDinh } from './src/vfx/tat_dinh.ts';
export {
  BAN_DO_SFX_HIEU_UNG,
  DANH_SACH_SFX_CO_SAN,
  layAmLuongSfx,
  layDuongDanSfxNeuCoSan,
} from './src/amthanh/sfx.ts';
export {
  chonKhauHinhTuBienDo,
  tinhLipSyncChoFrame,
  tinhLipSyncDuPhong,
} from './src/nhanvat/lip_sync.ts';
export {
  DANH_SACH_CO_RAU,
  DANH_SACH_DO_TUOI,
  DANH_SACH_GOC_QUAY,
  DANH_SACH_KIEU_BONG_BONG,
  DANH_SACH_KIEU_PHAN_UNG_CAM,
  DANH_SACH_KIEU_TOC,
  DANH_SACH_LOAI_ANH_SANG,
  DANH_SACH_LOAI_BOI_CANH,
  DANH_SACH_LOAI_BO_CUC,
  DANH_SACH_LOAI_CANH,
  DANH_SACH_LOAI_DAO_CU,
  DANH_SACH_LOAI_HANH_DONG,
  DANH_SACH_LOAI_HIEU_UNG_HOAT_HINH,
  DANH_SACH_LOAI_MINH_HOA_TOAN,
  DANH_SACH_LOAI_VAT_THE_XUNG_QUANH,
  DANH_SACH_PHUONG_TIEN_HANH_TRINH,
  DANH_SACH_TAM_KHUNG,
  DANH_SACH_TAM_TRANG_NHAC,
  DANH_SACH_TRANG_PHUC,
  DANH_SACH_TU_THE,
} from './src/kieu_dai.ts';
export {
  TOA_DO_BAN_DO_MAC_DINH,
  VUNG_END_SCREEN_YOUTUBE,
  tinhBienDoiBaoChiCo,
  tinhTrangThaiHanhTrinh,
  tinhTrangThaiPhanUngCam,
} from './src/canh/ke_chuyen_v35_logic.ts';
export {
  ID_MASCOT_KENH,
  MASCOT_KENH_MAC_DINH,
  layHoSoMascotKenh,
} from './src/nhanvat/mascot_kenh.ts';
export { tinhBoCucBongBongChat } from './src/canh/bong_bong_logic.ts';
export {
  THOI_LUONG_THE_TEN_HOI_GIAY,
  coAnPhuDeTrungBongBong,
  tinhTrangThaiTheTenHoi,
} from './src/canh/phu_de_logic.ts';
export {
  MAU_MUC_TRUYEN_TRANH,
  giaiTrangPhucHieuLuc,
  lamSangMauHex,
  lamToiMauHex,
  tinhBongTiepDat,
  tinhThamSoAnhSangNhanVat,
  tinhTiLeTamKhung,
} from './src/nhanvat/hoa_trang_va_anh_sang.ts';
export {
  tinhKenBurnsNenAI,
  tinhLopKhongKhiNenAI,
} from './src/boicanh/nen_ai_logic.ts';
export {
  coAnGiuongBenhNen,
  coAnNoiNenPhongSinh,
  coHienNoiTrongPhongSinh,
  giaiDanhSachVatTheXungQuanh,
  layKhungCuaSoChoBoiCanh,
  layVatTheMacDinhChoBoiCanh,
  locDaoCuKhongTrungLap,
  locVatTheHopLeTheoBoiCanh,
  tinhBuomBay,
  tinhGocQuaLac,
  tinhViTriTaxiCo,
} from './src/boicanh/moi_truong_logic.ts';
export {
  tinhBienDoiCamera,
  xacDinhNguoiDangNoiTaiFrame,
} from './src/vfx/dao_dien_camera.ts';
export {
  giaiBieuCamTheoMoc,
  giaiTrangThaiNhanVatTrongCanh,
  khuTrungLapNhanVatTrongCanh,
  tinhHuongNhinTuongTac,
} from './src/nhanvat/dien_xuat.ts';
export {
  chiaNhomNhanVatChiaDoi,
  tinhTrangThaiCauHoiTuongTac,
} from './src/canh/tuong_tac.ts';
export {
  tinhDauNhanVatY,
  tinhToaDoHieuUngAnToan,
} from './src/vfx/vi_tri_vfx.ts';
export { coHienKhungLoiBinh } from './src/canh/loi_binh_logic.ts';
`;

  await esbuildBuild({
    stdin: {
      contents: maNguonTongHop,
      resolveDir: gocDuAn,
      loader: 'ts',
    },
    bundle: true,
    format: 'esm',
    platform: 'node',
    target: 'node20',
    packages: 'external',
    outfile: tepBundle,
    logLevel: 'silent',
  });

  return import(pathToFileURL(tepBundle).href);
}

const {
  GIOI_HAN_GOC_DAU_MAX,
  GIOI_HAN_GOC_DAU_MIN,
  tinhKhungXuongCoBan,
  chiaDongMoTaTimeline,
  coDuLieuMinhHoaHopLe,
  layDanhSachBuocSuyLuan,
  locMocThoiGianHopLe,
  chuanHoaKhungHinhLienMach,
  kiemTraKhungHinhLienMach,
  chiaDongBongBong,
  tinhThongSoHopTen,
  easeInBack,
  easeInOutCubic,
  easeOutBack,
  springTatDinh,
  bamTatDinh,
  bamChuoiTatDinh,
  BAN_DO_SFX_HIEU_UNG,
  DANH_SACH_SFX_CO_SAN,
  layAmLuongSfx,
  layDuongDanSfxNeuCoSan,
  chonKhauHinhTuBienDo,
  tinhLipSyncChoFrame,
  tinhLipSyncDuPhong,
  DANH_SACH_CO_RAU,
  DANH_SACH_DO_TUOI,
  DANH_SACH_GOC_QUAY,
  DANH_SACH_KIEU_BONG_BONG,
  DANH_SACH_KIEU_PHAN_UNG_CAM,
  DANH_SACH_KIEU_TOC,
  DANH_SACH_LOAI_ANH_SANG,
  DANH_SACH_LOAI_BOI_CANH,
  DANH_SACH_LOAI_BO_CUC,
  DANH_SACH_LOAI_CANH,
  DANH_SACH_LOAI_DAO_CU,
  DANH_SACH_LOAI_HANH_DONG,
  DANH_SACH_LOAI_HIEU_UNG_HOAT_HINH,
  DANH_SACH_LOAI_MINH_HOA_TOAN,
  DANH_SACH_LOAI_VAT_THE_XUNG_QUANH,
  DANH_SACH_PHUONG_TIEN_HANH_TRINH,
  DANH_SACH_TAM_KHUNG,
  DANH_SACH_TAM_TRANG_NHAC,
  DANH_SACH_TRANG_PHUC,
  DANH_SACH_TU_THE,
  TOA_DO_BAN_DO_MAC_DINH,
  VUNG_END_SCREEN_YOUTUBE,
  tinhBienDoiBaoChiCo,
  tinhTrangThaiHanhTrinh,
  tinhTrangThaiPhanUngCam,
  ID_MASCOT_KENH,
  MASCOT_KENH_MAC_DINH,
  layHoSoMascotKenh,
  tinhBoCucBongBongChat,
  THOI_LUONG_THE_TEN_HOI_GIAY,
  coAnPhuDeTrungBongBong,
  tinhTrangThaiTheTenHoi,
  MAU_MUC_TRUYEN_TRANH,
  giaiTrangPhucHieuLuc,
  lamSangMauHex,
  lamToiMauHex,
  tinhBongTiepDat,
  tinhThamSoAnhSangNhanVat,
  tinhTiLeTamKhung,
  tinhKenBurnsNenAI,
  tinhLopKhongKhiNenAI,
  coAnGiuongBenhNen,
  coAnNoiNenPhongSinh,
  coHienNoiTrongPhongSinh,
  giaiDanhSachVatTheXungQuanh,
  layKhungCuaSoChoBoiCanh,
  layVatTheMacDinhChoBoiCanh,
  locDaoCuKhongTrungLap,
  locVatTheHopLeTheoBoiCanh,
  tinhBuomBay,
  tinhGocQuaLac,
  tinhViTriTaxiCo,
  tinhBienDoiCamera,
  xacDinhNguoiDangNoiTaiFrame,
  giaiBieuCamTheoMoc,
  giaiTrangThaiNhanVatTrongCanh,
  khuTrungLapNhanVatTrongCanh,
  tinhHuongNhinTuongTac,
  chiaNhomNhanVatChiaDoi,
  tinhTrangThaiCauHoiTuongTac,
  tinhDauNhanVatY,
  tinhToaDoHieuUngAnToan,
  coHienKhungLoiBinh,
} = await napCacModuleTs();

const LOAI_BO_CUC_BAT_BUOC = [
  'mo_dau',
  'ke_chuyen',
  'doi_thoai',
  'hai_huoc',
  'giai_thich_toan',
  'dong_thoi_gian',
  'ket_thuc',
];

const LOAI_BOI_CANH_HOP_LE = new Set([
  'bo_bien_hy_lap',
  'vuon_tao_dong_que',
  'pho_co_chau_au',
  'rung_nui_thien_nhien',
  'thu_vien_co_dien',
  'lop_hoc_bang_xanh',
  'bau_troi_dem_vu_tru',
  'phong_nen_hai_huoc',
  'quang_truong_hy_lap',
  'thu_vien_trung_co',
  'dai_thien_van_phuc_hung',
  'giang_duong_hien_dai',
  'nha_co_phong_sinh',
  'cang_bien_tau_thuy',
  'phong_tro_bep_lua',
  'phong_benh_vien',
  'duong_pho_xe_co',
  'giang_duong_dai_hoc',
  'san_truong_co_dien',
  'phong_thi_nghiem_co',
  'khong_gian_vu_tru_toan',
  'lang_que_an_do_a_dong',
]);

const LOAI_THOI_TIET_HOP_LE = new Set([
  'khong',
  'nang_dep',
  'hoang_hon',
  'ban_dem',
  'mua_nhe',
  'la_roi',
  'tuyet_roi',
]);

const LOAI_HANH_DONG_HOP_LE = [
  'dung_tho',
  'di_bo',
  'chay_voi_va',
  'ngoi_doc_sach',
  'chi_tro_giai_thich',
  'nhin_len_troi',
  'gat_gu_dong_tinh',
  'gai_dau_kho_hieu',
  'giat_minh_nhay_dung',
  'bo_tay_can_loi',
  'khoanh_tay_tu_man',
  'ho_het_sung_suong',
  'di_qua_di_lai',
  'sup_do_tuyet_vong',
  'trao_thu',
  'chi_bang_giang_bai',
  'quay_nhin_doi_thoai',
  'bat_tay',
  'giat_minh_bat_day',
  'quay_nhin_khan_gia',
];

const LOAI_BIEU_CAM_HOP_LE = new Set([
  'binh_thuong',
  'vui_tuoi',
  'ngac_nhien',
  'tuc_gian',
  'hoang_mang',
  'tinh_quai',
  'tram_tu',
  'can_loi_mat_do',
  'tu_man',
]);

const LOAI_PHU_KIEN_HOP_LE = new Set([
  'khong',
  'vong_nguyet_que',
  'toc_gia_17',
  'kinh_tron',
  'mu_noi_phap',
  'ao_choang',
  'khan_choang',
  'mu_tham_tu',
]);

const LOAI_VAT_CAM_TAY_HOP_LE = new Set([
  'khong',
  'cuon_giay',
  'qua_tao',
  'kinh_lup',
  'but_long_ngong',
  'que_chi_bang',
  'den_long',
  'ly_ca_phe',
]);

const LOAI_HIEU_UNG_HOP_LE = new Set([
  'bong_den_nay_so',
  'giot_mo_hoi',
  'dau_cham_hoi',
  'soc_set_danh',
  'sao_lap_lanh',
  'khoi_chay_tron',
  'co_lan_im_lang',
  'nhan_chu_hai_huoc',
]);

const LOAI_MINH_HOA_TOAN_HOP_LE = new Set([
  'tam_giac_vuong',
  'truc_so_vo_ti',
  'do_thi_ham_so',
  'hinh_hoc_chung_minh',
  'chuoi_suy_luan',
  'tung_buoc',
]);

const LOAI_DAO_CU_HOP_LE = new Set([
  'bang_den',
  'cuon_giay',
  'bong_den',
  'dong_ho_cat',
  'can_thang_bang',
  'thuoc_compa',
  'dau_hoi_cham',
  'compa_co',
  'ban_tinh_co',
  'khoi_da_dien',
  'kinh_thien_van',
  'noi_em_be',
  'noi_sup',
  'phong_bi_thu_tay',
  'giuong_benh',
  'bien_so_xe',
  'tach_tra_nong',
  'tau_thuy',
  'ban_hoc_den_dau',
  'qua_dia_cau',
]);

const LOAI_VAI_NOI_HOP_LE = new Set([
  'nguoi_dan',
  'nhan_vat',
  'binh_luan_hai',
]);

const KHOP_XUONG_BAT_BUOC = [
  'hong',
  'diemUonThan',
  'co',
  'dau',
  'vaiTrai',
  'khuyuTrai',
  'banTayTrai',
  'vaiPhai',
  'khuyuPhai',
  'banTayPhai',
  'goiTrai',
  'banChanTrai',
  'goiPhai',
  'banChanPhai',
  'diemCamVat',
];

const loi = [];

function baoLoi(thongBao) {
  loi.push(thongBao);
}

// 1. Kiem tra du_lieu/mau_pythagoras.json
const duongDanMau = path.join(gocDuAn, 'du_lieu', 'mau_pythagoras.json');
if (!fs.existsSync(duongDanMau)) {
  baoLoi('Khong tim thay du_lieu/mau_pythagoras.json');
} else {
  const duLieu = JSON.parse(fs.readFileSync(duongDanMau, 'utf8'));
  const tapNhanVat = new Set();

  for (const nv of duLieu.danhSachNhanVat ?? []) {
    tapNhanVat.add(nv.id);
    if (!LOAI_PHU_KIEN_HOP_LE.has(nv.phuKien)) {
      baoLoi(`Nhan vat ${nv.id}: phuKien "${nv.phuKien}" khong hop le`);
    }
  }

  const tatCaCanh = [];
  for (const ch of duLieu.chuong ?? []) {
    for (const c of ch.canh ?? []) {
      tatCaCanh.push(c);
    }
  }

  if (tatCaCanh.length === 0) {
    baoLoi('Khong co canh nao trong mau_pythagoras.json');
  }

  const tapBoCuc = new Set(tatCaCanh.map((c) => c.boCuc));
  for (const bc of LOAI_BO_CUC_BAT_BUOC) {
    if (!tapBoCuc.has(bc)) {
      baoLoi(`Thieu boCuc bat buoc trong mau_pythagoras.json: ${bc}`);
    }
  }

  const tapHanhDongHopLe = new Set(LOAI_HANH_DONG_HOP_LE);
  let frameTruoc = 0;
  let soCanhCoMinhHoa = 0;
  let soHieuUng = 0;
  let soLoiBinh = 0;

  for (let i = 0; i < tatCaCanh.length; i++) {
    const c = tatCaCanh[i];
    if (typeof c.tuFrame !== 'number' || typeof c.denFrame !== 'number') {
      baoLoi(`Canh ${c.id}: tuFrame/denFrame khong phai so`);
      continue;
    }
    if (c.tuFrame >= c.denFrame) {
      baoLoi(`Canh ${c.id}: tuFrame (${c.tuFrame}) >= denFrame (${c.denFrame})`);
    }
    if (c.tuFrame < frameTruoc) {
      baoLoi(`Canh ${c.id}: bi chong de frame (${c.tuFrame} < ${frameTruoc})`);
    }
    if (i > 0 && c.tuFrame !== frameTruoc) {
      baoLoi(`Canh ${c.id}: khong noi tiep sat frame truoc (${frameTruoc} -> ${c.tuFrame})`);
    }
    frameTruoc = c.denFrame;

    if (!LOAI_BOI_CANH_HOP_LE.has(c.boiCanh)) {
      baoLoi(`Canh ${c.id}: boiCanh "${c.boiCanh}" khong hop le`);
    }
    if (c.thoiTiet !== undefined && !LOAI_THOI_TIET_HOP_LE.has(c.thoiTiet)) {
      baoLoi(`Canh ${c.id}: thoiTiet "${c.thoiTiet}" khong hop le`);
    }

    if (c.minhHoaToan !== undefined) {
      if (!LOAI_MINH_HOA_TOAN_HOP_LE.has(c.minhHoaToan.loai)) {
        baoLoi(`Canh ${c.id}: minhHoaToan.loai "${c.minhHoaToan.loai}" khong hop le`);
      } else {
        soCanhCoMinhHoa++;
      }
    }

    if (c.loiBinhHaiHuoc?.noiDung) {
      soLoiBinh++;
    }

    for (const hu of c.hieuUngHoatHinh ?? []) {
      if (!LOAI_HIEU_UNG_HOP_LE.has(hu.loai)) {
        baoLoi(`Canh ${c.id}: hieuUngHoatHinh.loai "${hu.loai}" khong hop le`);
      } else {
        soHieuUng++;
      }
    }

    if (c.vaiNoi !== undefined && !LOAI_VAI_NOI_HOP_LE.has(c.vaiNoi)) {
      baoLoi(`Canh ${c.id}: vaiNoi "${c.vaiNoi}" khong hop le`);
    }

    if (c.bienDoAmThanh !== undefined) {
      if (
        !Array.isArray(c.bienDoAmThanh) ||
        c.bienDoAmThanh.some((v) => typeof v !== 'number' || !Number.isFinite(v) || v < 0 || v > 1)
      ) {
        baoLoi(`Canh ${c.id}: bienDoAmThanh khong hop le (phai la mang so trong [0, 1])`);
      }
    }

    for (const nv of c.nhanVat ?? []) {
      if (!tapNhanVat.has(nv.id)) {
        baoLoi(`Canh ${c.id}: nhanVat.id "${nv.id}" khong ton tai trong danhSachNhanVat`);
      }
      if (!tapHanhDongHopLe.has(nv.hanhDong)) {
        baoLoi(`Canh ${c.id}: hanhDong "${nv.hanhDong}" khong hop le`);
      }
      if (!LOAI_BIEU_CAM_HOP_LE.has(nv.bieuCam)) {
        baoLoi(`Canh ${c.id}: bieuCam "${nv.bieuCam}" khong hop le`);
      }
      if (nv.vatCamTay !== undefined && !LOAI_VAT_CAM_TAY_HOP_LE.has(nv.vatCamTay)) {
        baoLoi(`Canh ${c.id}: vatCamTay "${nv.vatCamTay}" khong hop le`);
      }
    }
  }

  if (soCanhCoMinhHoa < 1) {
    baoLoi('mau_pythagoras.json: can it nhat 1 canh co minhHoaToan');
  }
  if (soHieuUng < 3) {
    baoLoi('mau_pythagoras.json: can it nhat 3 hieuUngHoatHinh');
  }
  if (soLoiBinh < 1) {
    baoLoi('mau_pythagoras.json: can it nhat 1 canh co loiBinhHaiHuoc');
  }

  const tongFrames = frameTruoc;
  console.log(
    `[OK] mau_pythagoras.json: ${tatCaCanh.length} canh, ${tapBoCuc.size}/7 boCuc, ${soHieuUng} hieuUng, ${soLoiBinh} loiBinh, ${soCanhCoMinhHoa} minhHoaToan, tong ${tongFrames} frames (${(tongFrames / 30).toFixed(2)}s @ 30fps).`,
  );
}

// 2. Kiem tra bo duong cong & lo xo vat ly tat dinh (src/xuong/duong_cong.ts)
for (const t of [0, 0.25, 0.5, 0.75, 1]) {
  const c1 = easeInOutCubic(t);
  const c2 = easeOutBack(t);
  const c3 = easeInBack(t);
  if (!Number.isFinite(c1) || !Number.isFinite(c2) || !Number.isFinite(c3)) {
    baoLoi(`duong_cong.ts tra ve gia tri khong huu han tai t=${t}`);
  }
}
for (const fr of [-5, 0, 5, 10, 20, 60]) {
  const s1 = springTatDinh(fr, 11, 200);
  const s2 = springTatDinh(fr, 11, 200);
  if (!Number.isFinite(s1) || s1 !== s2) {
    baoLoi(`springTatDinh(${fr}) khong hop le hoac khong tat dinh`);
  }
}
if (springTatDinh(0) !== 0 || Math.abs(springTatDinh(90, 12, 180) - 1) > 0.02) {
  baoLoi('springTatDinh khong hoi tu dung tu 0 -> 1');
} else {
  console.log('[OK] src/xuong/duong_cong.ts: easeInOutCubic, easeOutBack, easeInBack & springTatDinh tat dinh 100%.');
}

// 3. Kiem tra bo giai FK cho du 14 LoaiHanhDong tai cac moc frame (0, 15, 45, 90)
const MOC_FRAME_FK = [0, 15, 45, 90];
for (const hd of LOAI_HANH_DONG_HOP_LE) {
  for (const frame of MOC_FRAME_FK) {
    for (const huong of ['phai', 'trai']) {
      for (const dangNoi of [false, true]) {
        const kq1 = tinhKhungXuongCoBan(hd, frame, huong, { dangNoi });
        const kq2 = tinhKhungXuongCoBan(hd, frame, huong, { dangNoi });
        if (JSON.stringify(kq1) !== JSON.stringify(kq2)) {
          baoLoi(`tinhKhungXuongCoBan("${hd}", ${frame}, "${huong}", dangNoi=${dangNoi}) khong tat dinh!`);
          break;
        }
        for (const khop of KHOP_XUONG_BAT_BUOC) {
          const diem = kq1[khop];
          if (!diem || !Number.isFinite(diem.x) || !Number.isFinite(diem.y)) {
            baoLoi(`tinhKhungXuongCoBan("${hd}", ${frame}): khop "${khop}" bi NaN/Infinity/thieu`);
            break;
          }
        }
        const cacSoKiemTra = [
          kq1.offsetX,
          kq1.offsetY,
          kq1.squashX,
          kq1.squashY,
          kq1.gocDau,
          kq1.doCaoNhay,
          kq1.dichNgangNoiBo,
          kq1.vanTocThan?.x,
          kq1.vanTocThan?.y,
          kq1.doTrePhuKien?.dx,
          kq1.doTrePhuKien?.dy,
          kq1.doTrePhuKien?.gocTre,
          kq1.doTrePhuKien?.doRung,
        ];
        if (cacSoKiemTra.some((v) => typeof v !== 'number' || !Number.isFinite(v))) {
          baoLoi(`tinhKhungXuongCoBan("${hd}", ${frame}): truong FK/thu cap co NaN hoac Infinity`);
        }
        if (
          kq1.squashX < 0.7 ||
          kq1.squashX > 1.45 ||
          kq1.squashY < 0.7 ||
          kq1.squashY > 1.45 ||
          Math.abs(kq1.squashX * kq1.squashY - 1) > 0.02
        ) {
          baoLoi(
            `tinhKhungXuongCoBan("${hd}", ${frame}): squash khong hop le (squashX=${kq1.squashX}, squashY=${kq1.squashY})`,
          );
        }
      }
    }
  }
}
console.log(
  `[OK] src/xuong/he_xuong.ts (FK): ${LOAI_HANH_DONG_HOP_LE.length}/${LOAI_HANH_DONG_HOP_LE.length} hanh dong x frames [${MOC_FRAME_FK.join(', ')}] x 2 huong x dangNoi tat dinh 100%, du ${KHOP_XUONG_BAT_BUOC.length} khop, squash bao toan dien tich, khong NaN/Infinity.`,
);

// 4. Kiem tra bamTatDinh & bamChuoiTatDinh
if (bamTatDinh(42) !== bamTatDinh(42) || bamChuoiTatDinh('pythagoras') !== bamChuoiTatDinh('pythagoras')) {
  baoLoi('src/vfx/tat_dinh.ts khong tat dinh!');
} else {
  console.log('[OK] src/vfx/tat_dinh.ts: ham bam seed tat dinh 100%.');
}

// 4b. Kiem tra he thong SFX hoat hinh (DANH_SACH_SFX_CO_SAN + file that + an toan khi thieu file)
const SFX_BAT_BUOC = ['pop.mp3', 'ding.mp3', 'boing.mp3', 'crickets.mp3', 'whoosh.mp3', 'dramatic.mp3'];
for (const ten of SFX_BAT_BUOC) {
  if (!DANH_SACH_SFX_CO_SAN.includes(ten)) {
    baoLoi(`DANH_SACH_SFX_CO_SAN thieu file SFX bat buoc: ${ten}`);
  }
  const duongDanThat = path.join(gocDuAn, 'public', 'sfx', ten);
  if (!fs.existsSync(duongDanThat) || fs.statSync(duongDanThat).size === 0) {
    baoLoi(`Thieu file am thanh that public/sfx/${ten}`);
  }
}
const duongDanBgm = path.join(gocDuAn, 'public', 'bgm', 'nhac_nen_nhe.mp3');
if (!fs.existsSync(duongDanBgm) || fs.statSync(duongDanBgm).size === 0) {
  baoLoi('Thieu file nhac nen mau public/bgm/nhac_nen_nhe.mp3');
}
for (const loai of LOAI_HIEU_UNG_HOP_LE) {
  const sfxPath = layDuongDanSfxNeuCoSan(loai);
  const expected = `sfx/${BAN_DO_SFX_HIEU_UNG[loai]}`;
  if (sfxPath !== expected) {
    baoLoi(`layDuongDanSfxNeuCoSan("${loai}") tra ve "${sfxPath}", mong doi "${expected}"`);
  }
  const vol = layAmLuongSfx(loai);
  if (typeof vol !== 'number' || !Number.isFinite(vol) || vol <= 0 || vol > 1) {
    baoLoi(`layAmLuongSfx("${loai}") khong hop le: ${vol}`);
  }
}
// Mo phong truong hop file bi xoa: chi con pop.mp3 -> ding.mp3 phai tra ve null an toan
const tapChiConPop = new Set(['sfx/pop.mp3']);
if (
  layDuongDanSfxNeuCoSan('giot_mo_hoi', tapChiConPop) !== 'sfx/pop.mp3' ||
  layDuongDanSfxNeuCoSan('bong_den_nay_so', tapChiConPop) !== null
) {
  baoLoi('layDuongDanSfxNeuCoSan khong chan an toan khi file SFX bi thieu trong public/sfx/');
} else {
  console.log(
    `[OK] src/amthanh/sfx.ts: du ${DANH_SACH_SFX_CO_SAN.length}/6 SFX that + nhac nen public/bgm/nhac_nen_nhe.mp3 + chan an toan khi thieu file.`,
  );
}

// 4c. Kiem tra logic Lip-sync bam bien do RMS & fallback tat dinh khi thieu RMS
const testRmsCases = [
  { val: 0.0, kyVong: 0 },
  { val: 0.05, kyVong: 0 },
  { val: 0.2, kyVong: 1 },
  { val: 0.45, kyVong: 2 },
  { val: 0.85, kyVong: 3 },
  { val: Number.NaN, kyVong: 0 },
];
for (const tc of testRmsCases) {
  const kq = chonKhauHinhTuBienDo(tc.val);
  if (kq.khauHinh !== tc.kyVong || kq.nguon !== 'rms') {
    baoLoi(`chonKhauHinhTuBienDo(${tc.val}) tra ve khauHinh=${kq.khauHinh}, mong doi ${tc.kyVong}`);
  }
}
const mangRmsMau = [0.0, 0.22, 0.5, 0.88, 0.02];
const kqRmsSeq = [0, 1, 2, 3, 4, 9].map((fr) => tinhLipSyncChoFrame(fr, 77, mangRmsMau));
if (
  kqRmsSeq[0].khauHinh !== 0 ||
  kqRmsSeq[1].khauHinh !== 1 ||
  kqRmsSeq[2].khauHinh !== 2 ||
  kqRmsSeq[3].khauHinh !== 3 ||
  kqRmsSeq[4].khauHinh !== 0 ||
  kqRmsSeq[5].khauHinh !== 0 ||
  kqRmsSeq.some((x) => x.nguon !== 'rms')
) {
  baoLoi(`tinhLipSyncChoFrame voi mang RMS tra ve sai: ${JSON.stringify(kqRmsSeq)}`);
}
// Kiem tra fallback tat dinh khi thieu RMS (mau_pythagoras.json)
const fb1 = tinhLipSyncChoFrame(18, 42, undefined);
const fb2 = tinhLipSyncChoFrame(18, 42, []);
const fbDirect = tinhLipSyncDuPhong(18, 42);
if (
  fb1.nguon !== 'du_phong' ||
  JSON.stringify(fb1) !== JSON.stringify(fb2) ||
  JSON.stringify(fb1) !== JSON.stringify(fbDirect)
) {
  baoLoi('tinhLipSyncChoFrame fallback khi thieu RMS khong khop tinhLipSyncDuPhong hoac khong tat dinh');
} else {
  console.log('[OK] src/nhanvat/lip_sync.ts: anh xa 4 khau hinh RMS + khep mieng khi im lang + fallback tat dinh 100%.');
}

// 4d. Kiem tra v0.8: 12 boi canh Parallax, 11 dao cu Toan hoc, MinhHoaToan "tung_buoc" & Still ThumbnailToanHoc
const BOI_CANH_MOI_V08 = [
  'quang_truong_hy_lap',
  'thu_vien_trung_co',
  'dai_thien_van_phuc_hung',
  'giang_duong_hien_dai',
];
const DAO_CU_MOI_V08 = ['compa_co', 'ban_tinh_co', 'khoi_da_dien', 'kinh_thien_van'];

if (DANH_SACH_LOAI_BOI_CANH.length < 12) {
  baoLoi(`DANH_SACH_LOAI_BOI_CANH phai co it nhat 12 boi canh, hien co ${DANH_SACH_LOAI_BOI_CANH.length}`);
}
for (const bc of BOI_CANH_MOI_V08) {
  if (!DANH_SACH_LOAI_BOI_CANH.includes(bc)) {
    baoLoi(`DANH_SACH_LOAI_BOI_CANH thieu boi canh moi v0.8: ${bc}`);
  }
}
if (DANH_SACH_LOAI_DAO_CU.length < 11) {
  baoLoi(`DANH_SACH_LOAI_DAO_CU phai co it nhat 11 dao cu, hien co ${DANH_SACH_LOAI_DAO_CU.length}`);
}
for (const dc of DAO_CU_MOI_V08) {
  if (!DANH_SACH_LOAI_DAO_CU.includes(dc) || !LOAI_DAO_CU_HOP_LE.has(dc)) {
    baoLoi(`DANH_SACH_LOAI_DAO_CU thieu dao cu moi v0.8: ${dc}`);
  }
}
if (!DANH_SACH_LOAI_MINH_HOA_TOAN.includes('tung_buoc')) {
  baoLoi('DANH_SACH_LOAI_MINH_HOA_TOAN thieu dang "tung_buoc"');
}

const srcBoiCanh = fs.readFileSync(path.join(gocDuAn, 'src', 'boicanh', 'BoiCanhHoatHinh.tsx'), 'utf8');
for (const bc of DANH_SACH_LOAI_BOI_CANH) {
  if (!srcBoiCanh.includes(`case '${bc}'`)) {
    baoLoi(`BoiCanhHoatHinh.tsx thieu nhanh switch cho boi canh "${bc}"`);
  }
}

const srcDaoCu = fs.readFileSync(path.join(gocDuAn, 'src', 'daocu', 'DaoCu.tsx'), 'utf8');
for (const dc of DANH_SACH_LOAI_DAO_CU) {
  if (!srcDaoCu.includes(`case '${dc}'`)) {
    baoLoi(`DaoCu.tsx thieu nhanh switch cho dao cu "${dc}"`);
  }
}

const srcMinhHoa = fs.readFileSync(path.join(gocDuAn, 'src', 'daocu', 'MinhHoaToan.tsx'), 'utf8');
for (const dsl of ['tung_buoc', 'truc_toa_do', 'duong_cong', 'da_giac', 'cung_tron', 'doan_thang', 'diem', 'nhan_chu']) {
  if (!srcMinhHoa.includes(`'${dsl}'`)) {
    baoLoi(`MinhHoaToan.tsx thieu ho tro mini-DSL "${dsl}"`);
  }
}

const pathThumbnail = path.join(gocDuAn, 'src', 'Thumbnail.tsx');
const srcRoot = fs.readFileSync(path.join(gocDuAn, 'src', 'Root.tsx'), 'utf8');
if (!fs.existsSync(pathThumbnail)) {
  baoLoi('Thieu tep src/Thumbnail.tsx');
} else {
  const srcThumb = fs.readFileSync(pathThumbnail, 'utf8');
  if (!srcThumb.includes('ThumbnailToanHoc') || !srcThumb.includes('bienThe === 1') || !srcThumb.includes('bienThe === 2')) {
    baoLoi('src/Thumbnail.tsx thieu component ThumbnailToanHoc hoac chua du 3 bien the A/B');
  }
}
if (!srcRoot.includes('id="ThumbnailToanHoc"') || !srcRoot.includes('<Still')) {
  baoLoi('src/Root.tsx chua dang ky <Still id="ThumbnailToanHoc" ... />');
}
console.log(
  `[OK] v0.8 Assets & Schema: ${DANH_SACH_LOAI_BOI_CANH.length} boi canh Parallax, ${DANH_SACH_LOAI_DAO_CU.length} dao cu Toan, MinhHoaToan mini-DSL "tung_buoc" & Still ThumbnailToanHoc.`,
);

// 5. Kiem tra v2.0 Buoc 1: Khong hardcode Pythagoras, khong outro hoi giua, khong gap frame, hop ten tu co gian & goc dau/co an toan
// 5a. Quet hardcode Pythagoras trong src/canh/, src/daocu/MinhHoaToan.tsx va src/VideoDai.tsx
const HARDCODE_PYTHAGORAS_CAM = [
  { ten: 'MOC_MAC_DINH', regex: /\bMOC_MAC_DINH\b/ },
  { ten: 'BUOC_VE_MAC_DINH', regex: /\bBUOC_VE_MAC_DINH\b/ },
  { ten: 'moc ~530 TCN', regex: /~530\s*TCN/i },
  { ten: 'moc ~500 TCN', regex: /~500\s*TCN/i },
  { ten: 'Pythagoras fallback', regex: /Pythagoras/i },
  { ten: 'Hippasus fallback', regex: /Hippasus/i },
  { ten: 'chung minh √2 = p/q fallback', regex: /Giả sử √2 = p\/q/i },
  { ten: 'ket luan √2 vo ti fallback', regex: /Mâu thuẫn! ⇒ √2 vô tỉ/i },
  { ten: 'gia tri √2 ≈ 1.4142 fallback', regex: /√2\s*≈\s*1\.4142/i },
  { ten: 'do thi mac dinh y = f(x)', regex: /y\s*=\s*f\(x\)\s*•\s*Đạo hàm & Diện tích ∫/i },
  { ten: 'hinh hoc chung minh a^2+b^2=c^2 hardcode', regex: /\(a \+ b\)² = 4·\(½ab\) \+ c²/i },
  { ten: 'nen mac dinh bo_bien_hy_lap trong VideoDai', regex: /<BoiCanhHoatHinh\s+loai="bo_bien_hy_lap"/ },
];

const fileQuetHardcode = [
  path.join(gocDuAn, 'src', 'VideoDai.tsx'),
  path.join(gocDuAn, 'src', 'daocu', 'MinhHoaToan.tsx'),
  path.join(gocDuAn, 'src', 'daocu', 'minh_hoa_hop_le.ts'),
  ...fs
    .readdirSync(path.join(gocDuAn, 'src', 'canh'))
    .filter((f) => /\.(ts|tsx)$/.test(f))
    .map((f) => path.join(gocDuAn, 'src', 'canh', f)),
];

for (const filePath of fileQuetHardcode) {
  const noiDung = fs.readFileSync(filePath, 'utf8');
  for (const qt of HARDCODE_PYTHAGORAS_CAM) {
    if (qt.regex.test(noiDung)) {
      baoLoi(`Phat hien du lieu hardcode Pythagoras/mac dinh "${qt.ten}" tai ${path.relative(gocDuAn, filePath)}`);
    }
  }
}

// Kiem tra coDuLieuMinhHoaHopLe & locMocThoiGianHopLe khi thieu du lieu vs co du lieu hop le
if (
  coDuLieuMinhHoaHopLe({ loai: 'chuoi_suy_luan' }) !== false ||
  coDuLieuMinhHoaHopLe({ loai: 'do_thi_ham_so' }) !== false ||
  coDuLieuMinhHoaHopLe({ loai: 'tam_giac_vuong' }) !== false ||
  coDuLieuMinhHoaHopLe({ loai: 'truc_so_vo_ti' }) !== false ||
  coDuLieuMinhHoaHopLe({ loai: 'hinh_hoc_chung_minh' }) !== false ||
  coDuLieuMinhHoaHopLe({ loai: 'tung_buoc', buocVe: [] }) !== false ||
  layDanhSachBuocSuyLuan(undefined).length !== 0 ||
  locMocThoiGianHopLe(undefined).length !== 0
) {
  baoLoi('minh_hoa_hop_le.ts phai tra ve false/rong khi thieu du lieu JSON (khong duoc fallback Pythagoras)');
}
if (
  coDuLieuMinhHoaHopLe({
    loai: 'tam_giac_vuong',
    thamSo: { canhA: 1, canhB: 1, nhanCanhHuyen: '√2' },
  }) !== true ||
  coDuLieuMinhHoaHopLe({
    loai: 'chuoi_suy_luan',
    thamSo: { buoc1: '1729 = 1^3 + 12^3', buoc2: '1729 = 9^3 + 10^3' },
  }) !== true ||
  coDuLieuMinhHoaHopLe({
    loai: 'do_thi_ham_so',
    thamSo: { ham: 'sin', chuThich: 'y = sin(x)' },
  }) !== true ||
  locMocThoiGianHopLe([{ nam: '1913', moTa: 'Ramanujan gui thu cho Hardy' }]).length !== 1
) {
  baoLoi('minh_hoa_hop_le.ts khong nhan dien dung du lieu JSON hop le');
}

// 5b. Kiem tra outro banner chi bat o canh cuoi cung cua hoi cuoi cung toan tap & phat hien gap frame
const chuongTestOutroVaGap = [
  {
    id: 'chuong_1',
    tenChuong: '1. Hoi 1',
    canh: [
      { id: 'c1', boCuc: 'mo_dau', boiCanh: 'thu_vien_co_dien', tuFrame: 0, denFrame: 90, loiThoai: 'a', nhanVat: [] },
      { id: 'c2', boCuc: 'ket_thuc', boiCanh: 'thu_vien_co_dien', tuFrame: 90, denFrame: 180, loiThoai: 'b', nhanVat: [] },
    ],
  },
  {
    id: 'chuong_3',
    tenChuong: '3. Hoi 3',
    canh: [
      { id: 'c3', boCuc: 'ket_thuc', boiCanh: 'lop_hoc_bang_xanh', tuFrame: 185, denFrame: 270, loiThoai: 'c', nhanVat: [] },
    ],
  },
  {
    id: 'chuong_6',
    tenChuong: '6. Hoi 6',
    canh: [
      { id: 'c4', boCuc: 'ket_thuc', boiCanh: 'bau_troi_dem_vu_tru', tuFrame: 270, denFrame: 360, loiThoai: 'd', nhanVat: [] },
    ],
  },
];
const loiGapPhatHien = kiemTraKhungHinhLienMach(chuongTestOutroVaGap);
if (!loiGapPhatHien.some((m) => m.includes('gap frame'))) {
  baoLoi('kiemTraKhungHinhLienMach khong phat hien duoc gap frame (180 -> 185)');
}
const daCan = chuanHoaKhungHinhLienMach(chuongTestOutroVaGap);
if (
  daCan.danhSachCanh[0].tuFrameThuc !== 0 ||
  daCan.danhSachCanh[1].tuFrameThuc !== 90 ||
  daCan.danhSachCanh[2].tuFrameThuc !== 180 ||
  daCan.danhSachCanh[3].tuFrameThuc !== 265 ||
  daCan.tongFrames !== 355
) {
  baoLoi('chuanHoaKhungHinhLienMach khong noi tiep lien mach tu frame 0 den frame cuoi');
}
if (
  daCan.danhSachCanh[1].hienManHinhKetThuc !== false ||
  daCan.danhSachCanh[2].hienManHinhKetThuc !== false ||
  daCan.danhSachCanh[3].hienManHinhKetThuc !== true
) {
  baoLoi('hienManHinhKetThuc phai = false o hoi giua (Hoi 1, Hoi 3) va chi = true o canh cuoi cung toan tap');
}
// Xac minh CanhKet.tsx khong mac dinh bat banner neu hienBannerKetThuc=false
const srcCanhKet = fs.readFileSync(path.join(gocDuAn, 'src', 'canh', 'CanhKet.tsx'), 'utf8');
if (!srcCanhKet.includes('hienBannerKetThuc = false')) {
  baoLoi('CanhKet.tsx phai mac dinh hienBannerKetThuc = false de chan banner outro o hoi giua');
}

// 5c. Kiem tra hop nhan ten nhan vat tu co gian (vi du "Srinivasa Ramanujan")
const hopTenNgan = tinhThongSoHopTen('Gauss');
const hopTenDai = tinhThongSoHopTen('Srinivasa Ramanujan');
const hopTenRatDai = tinhThongSoHopTen('Muhammad ibn Musa al-Khwarizmi');
if (hopTenNgan.width < 112 || hopTenDai.width < 210 || hopTenRatDai.width <= hopTenDai.width) {
  baoLoi(
    `tinhThongSoHopTen khong tu co gian dung theo do dai ten (Gauss=${hopTenNgan.width}, Ramanujan=${hopTenDai.width}, Khwarizmi=${hopTenRatDai.width})`,
  );
}

// 5d. Kiem tra gioi han goc xoay dau/co cua dong tac nhay an mung (ho_het_sung_suong) & tat ca 20 dong tac
for (const hd of ['ho_het_sung_suong', 'giat_minh_nhay_dung', 'giat_minh_bat_day']) {
  for (let f = 0; f <= 120; f++) {
    for (const huong of ['phai', 'trai']) {
      for (const dangNoi of [false, true]) {
        const kq = tinhKhungXuongCoBan(hd, f, huong, { dangNoi });
        if (Math.abs(kq.gocDau) > 12.5) {
          baoLoi(`Dong tac nhay "${hd}" frame=${f}: |gocDau|=${Math.abs(kq.gocDau)} vuot gioi han an toan 12°`);
          break;
        }
        if (kq.co.y - kq.dau.y < 24) {
          baoLoi(`Dong tac nhay "${hd}" frame=${f}: dau bi ha thap/lat nguoc (co.y - dau.y = ${(kq.co.y - kq.dau.y).toFixed(1)})`);
          break;
        }
        if (Math.abs(kq.dau.x - kq.co.x) > 10.5) {
          baoLoi(`Dong tac nhay "${hd}" frame=${f}: dau bi lech truc co (|dau.x - co.x| = ${Math.abs(kq.dau.x - kq.co.x).toFixed(1)})`);
          break;
        }
      }
    }
  }
}
for (const hd of LOAI_HANH_DONG_HOP_LE) {
  for (const frame of MOC_FRAME_FK) {
    for (const huong of ['phai', 'trai']) {
      for (const dangNoi of [false, true]) {
        const kq = tinhKhungXuongCoBan(hd, frame, huong, { dangNoi });
        const maxChoPhep = Math.max(Math.abs(GIOI_HAN_GOC_DAU_MIN), Math.abs(GIOI_HAN_GOC_DAU_MAX));
        if (Math.abs(kq.gocDau) > maxChoPhep + 0.01) {
          baoLoi(`Hanh dong "${hd}" frame=${frame}: |gocDau|=${Math.abs(kq.gocDau)} vuot gioi han ${maxChoPhep}°`);
        }
        if (kq.co.y - kq.dau.y < 23) {
          baoLoi(`Hanh dong "${hd}" frame=${frame}: dau bi lat nguoc hoac sap truc co`);
        }
      }
    }
  }
}
console.log(
  `[OK] v2.0 Buoc 1 Guard: sach 100% hardcode Pythagoras, chan outro hoi giua, khong gap frame, hop ten tu co gian (Ramanujan=${hopTenDai.width}px), goc dau/co an toan tren ${LOAI_HANH_DONG_HOP_LE.length} dong tac.`,
);

// 5e. Kiem tra v2.0 Buoc 2: Hop dong du lieu mo rong, 8 goc quay + tuDongFocusNguoiNoi, 4 doTuoi, 5 tuThe, 6 dong tac moi, bieuCamTheoMoc, tuongTacVoi, tuong_tac_khan_gia & chia_doi_man_hinh
const GOC_QUAY_BAT_BUOC = [
  'toan_canh',
  'trung_canh',
  'can_mat',
  'focus_trai',
  'focus_phai',
  'zoom_dao_cu',
  'pan_ngang',
  'chia_doi_man_hinh',
];
const LOAI_CANH_BAT_BUOC = [
  'ke_chuyen',
  'doi_thoai',
  'tuong_tac_khan_gia',
  'giang_toan',
  'chuyen_canh_lich_su',
];
const DO_TUOI_BAT_BUOC = ['so_sinh', 'thieu_nien', 'truong_thanh', 'gia'];
const TU_THE_BAT_BUOC = ['dung', 'ngoi_ban', 'nam_giuong', 'om_em_be', 'mac_ao_khoac'];
const DONG_TAC_MOI_V20 = [
  'trao_thu',
  'chi_bang_giang_bai',
  'quay_nhin_doi_thoai',
  'bat_tay',
  'giat_minh_bat_day',
  'quay_nhin_khan_gia',
];

for (const gq of GOC_QUAY_BAT_BUOC) {
  if (!DANH_SACH_GOC_QUAY.includes(gq)) {
    baoLoi(`DANH_SACH_GOC_QUAY thieu goc quay "${gq}"`);
  }
}
for (const lc of LOAI_CANH_BAT_BUOC) {
  if (!DANH_SACH_LOAI_CANH.includes(lc)) {
    baoLoi(`DANH_SACH_LOAI_CANH thieu loai canh "${lc}"`);
  }
}
for (const dt of DO_TUOI_BAT_BUOC) {
  if (!DANH_SACH_DO_TUOI.includes(dt)) {
    baoLoi(`DANH_SACH_DO_TUOI thieu do tuoi "${dt}"`);
  }
}
for (const tt of TU_THE_BAT_BUOC) {
  if (!DANH_SACH_TU_THE.includes(tt)) {
    baoLoi(`DANH_SACH_TU_THE thieu tu the "${tt}"`);
  }
}
for (const hd of DONG_TAC_MOI_V20) {
  if (!DANH_SACH_LOAI_HANH_DONG.includes(hd)) {
    baoLoi(`DANH_SACH_LOAI_HANH_DONG thieu dong tac tuong tac moi "${hd}"`);
  }
}

// Kiem tra 8 goc quay & tuDongFocusNguoiNoi trong src/vfx/dao_dien_camera.ts
const nvMauDoiThoai = [
  {
    id: 'nv_trai',
    x: 480,
    y: 790,
    huong: 'phai',
    hanhDong: 'quay_nhin_doi_thoai',
    bieuCam: 'binh_thuong',
    tuongTacVoi: 'nv_phai',
    bieuCamTheoMoc: [
      { tuFrame: 0, bieuCam: 'tram_tu' },
      { tuFrame: 45, bieuCam: 'ngac_nhien' },
      { tienDo: 0.75, bieuCam: 'vui_tuoi' },
    ],
  },
  {
    id: 'nv_phai',
    x: 1440,
    y: 790,
    huong: 'trai',
    hanhDong: 'trao_thu',
    bieuCam: 'vui_tuoi',
    tuongTacVoi: 'nv_trai',
  },
];
const luotThoaiMau = [
  {
    nhanVatId: 'nv_trai',
    noiDung: 'Thư này chứa công thức rất kỳ lạ!',
    bieuCam: 'ngac_nhien',
    dongTac: 'trao_thu',
    batDauFrame: 0,
    ketThucFrame: 60,
  },
  {
    nhanVatId: 'nv_phai',
    noiDung: 'Để tôi xem ngay, thật khó tin!',
    bieuCam: 'vui_tuoi',
    dongTac: 'bat_tay',
    batDauFrame: 60,
    ketThucFrame: 120,
  },
];
const daoCuMau = [{ loai: 'bang_den', x: 1280, y: 420 }];

for (const gq of GOC_QUAY_BAT_BUOC) {
  for (const f of [0, 15, 45, 90]) {
    const cam1 = tinhBienDoiCamera(
      f,
      120,
      undefined,
      nvMauDoiThoai,
      { gocQuay: gq },
      luotThoaiMau,
      daoCuMau,
    );
    const cam2 = tinhBienDoiCamera(
      f,
      120,
      undefined,
      nvMauDoiThoai,
      { gocQuay: gq },
      luotThoaiMau,
      daoCuMau,
    );
    if (JSON.stringify(cam1) !== JSON.stringify(cam2)) {
      baoLoi(`tinhBienDoiCamera gocQuay="${gq}" frame=${f} khong tat dinh`);
      break;
    }
    if (
      !Number.isFinite(cam1.zoom) ||
      !Number.isFinite(cam1.panX) ||
      !Number.isFinite(cam1.panY) ||
      !Number.isFinite(cam1.rot)
    ) {
      baoLoi(`tinhBienDoiCamera gocQuay="${gq}" frame=${f} tra ve NaN/Infinity`);
      break;
    }
    const maxPanX = 960 * Math.max(0, cam1.zoom - 1) + 0.5;
    const maxPanY = 540 * Math.max(0, cam1.zoom - 1) + 0.5;
    if (Math.abs(cam1.panX) > maxPanX || Math.abs(cam1.panY) > maxPanY) {
      baoLoi(`tinhBienDoiCamera gocQuay="${gq}" frame=${f} vuot bien khung (lo vien den)`);
      break;
    }
  }
}

const camFocusTrai = tinhBienDoiCamera(30, 120, undefined, nvMauDoiThoai, { gocQuay: 'focus_trai' });
const camFocusPhai = tinhBienDoiCamera(30, 120, undefined, nvMauDoiThoai, { gocQuay: 'focus_phai' });
const camCanMat = tinhBienDoiCamera(30, 120, undefined, nvMauDoiThoai, { gocQuay: 'can_mat' });
const camToanCanh = tinhBienDoiCamera(30, 120, undefined, nvMauDoiThoai, { gocQuay: 'toan_canh' });
const camPan0 = tinhBienDoiCamera(0, 120, undefined, nvMauDoiThoai, { gocQuay: 'pan_ngang' });
const camPan120 = tinhBienDoiCamera(120, 120, undefined, nvMauDoiThoai, { gocQuay: 'pan_ngang' });
const camChiaDoi = tinhBienDoiCamera(30, 120, undefined, nvMauDoiThoai, { gocQuay: 'chia_doi_man_hinh' });

if (!(camFocusTrai.panX > 0 && camFocusPhai.panX < 0)) {
  baoLoi(`focus_trai (${camFocusTrai.panX}) phai > 0 va focus_phai (${camFocusPhai.panX}) phai < 0`);
}
if (!(camCanMat.zoom > camToanCanh.zoom + 0.3)) {
  baoLoi(`can_mat zoom (${camCanMat.zoom}) phai lon hon toan_canh (${camToanCanh.zoom})`);
}
if (Math.abs(camPan120.panX - camPan0.panX) < 40) {
  baoLoi(`pan_ngang khong dich chuyen ngang du ro (${camPan0.panX} -> ${camPan120.panX})`);
}
if (!camChiaDoi.laChiaDoiManHinh) {
  baoLoi('chia_doi_man_hinh phai dat laChiaDoiManHinh = true');
}

// Kiem tra tuDongFocusNguoiNoi lia & zoom 1.2x-1.45x theo luotThoai[] & RMS
const camNoiTrai = tinhBienDoiCamera(
  30,
  120,
  undefined,
  nvMauDoiThoai,
  { gocQuay: 'toan_canh', tuDongFocusNguoiNoi: true },
  luotThoaiMau,
);
const camNoiPhai = tinhBienDoiCamera(
  90,
  120,
  undefined,
  nvMauDoiThoai,
  { gocQuay: 'toan_canh', tuDongFocusNguoiNoi: true },
  luotThoaiMau,
);
if (
  camNoiTrai.zoom < 1.2 ||
  camNoiTrai.zoom > 1.45 ||
  camNoiTrai.panX <= 0 ||
  camNoiPhai.zoom < 1.2 ||
  camNoiPhai.zoom > 1.45 ||
  camNoiPhai.panX >= 0
) {
  baoLoi(
    `tuDongFocusNguoiNoi khong lia & zoom dung trong [1.2, 1.45] (trai=${JSON.stringify(camNoiTrai)}, phai=${JSON.stringify(camNoiPhai)})`,
  );
}
// Kiem tra tuDongFocusNguoiNoi theo RMS rieng tung nhan vat
const nvRmsTest = [
  { ...nvMauDoiThoai[0], bienDoAmThanh: Array(40).fill(0.01) },
  { ...nvMauDoiThoai[1], bienDoAmThanh: Array(40).fill(0.55) },
];
if (xacDinhNguoiDangNoiTaiFrame(20, nvRmsTest) !== 'nv_phai') {
  baoLoi('xacDinhNguoiDangNoiTaiFrame khong phat hien dung nhan vat co RMS hoat dong');
}
const camRms = tinhBienDoiCamera(20, 40, undefined, nvRmsTest, {
  gocQuay: 'toan_canh',
  tuDongFocusNguoiNoi: true,
});
if (camRms.panX >= 0 || camRms.zoom < 1.2) {
  baoLoi('tuDongFocusNguoiNoi khong lia sang nhan vat co bien do RMS cao');
}

// Xac minh MayQuayDong.tsx dung translate3d + scale
const srcMayQuay = fs.readFileSync(path.join(gocDuAn, 'src', 'vfx', 'MayQuayDong.tsx'), 'utf8');
if (!srcMayQuay.includes('translate3d(') || !srcMayQuay.includes('scale(')) {
  baoLoi('src/vfx/MayQuayDong.tsx phai su dung transform: translate3d / scale');
}

// Kiem tra 4 doTuoi x 5 tuThe trong he_xuong.ts & NguoiQueDong.tsx
for (const dt of DO_TUOI_BAT_BUOC) {
  for (const tt of TU_THE_BAT_BUOC) {
    const kq = tinhKhungXuongCoBan('dung_tho', 20, 'phai', {
      dangNoi: true,
      doTuoi: dt,
      tuThe: tt,
    });
    for (const khop of KHOP_XUONG_BAT_BUOC) {
      if (!kq[khop] || !Number.isFinite(kq[khop].x) || !Number.isFinite(kq[khop].y)) {
        baoLoi(`tinhKhungXuongCoBan doTuoi="${dt}" tuThe="${tt}": khop "${khop}" khong hop le`);
        break;
      }
    }
    if (Math.abs(kq.squashX * kq.squashY - 1) > 0.02) {
      baoLoi(`tinhKhungXuongCoBan doTuoi="${dt}" tuThe="${tt}": squash khong bao toan dien tich`);
    }
  }
}
const srcNguoiQue = fs.readFileSync(path.join(gocDuAn, 'src', 'nhanvat', 'NguoiQueDong.tsx'), 'utf8');
for (const token of ['so_sinh', 'thieu_nien', 'gia', 'ngoi_ban', 'nam_giuong', 'om_em_be', 'mac_ao_khoac', 'nhinThangOngKinh']) {
  if (!srcNguoiQue.includes(token)) {
    baoLoi(`src/nhanvat/NguoiQueDong.tsx thieu xu ly "${token}"`);
  }
}

// Kiem tra bieuCamTheoMoc, giaiTrangThaiNhanVatTrongCanh, tuongTacVoi & tuong_tac_khan_gia
const bc0 = giaiBieuCamTheoMoc('binh_thuong', nvMauDoiThoai[0].bieuCamTheoMoc, 10, 120).bieuCam;
const bc50 = giaiBieuCamTheoMoc('binh_thuong', nvMauDoiThoai[0].bieuCamTheoMoc, 50, 120).bieuCam;
const bc95 = giaiBieuCamTheoMoc('binh_thuong', nvMauDoiThoai[0].bieuCamTheoMoc, 95, 120).bieuCam;
if (bc0 !== 'tram_tu' || bc50 !== 'ngac_nhien' || bc95 !== 'vui_tuoi') {
  baoLoi(`giaiBieuCamTheoMoc sai moc bieu cam (f10=${bc0}, f50=${bc50}, f95=${bc95})`);
}

const dsGiaiLuot1 = giaiTrangThaiNhanVatTrongCanh(
  { nhanVat: nvMauDoiThoai, luotThoai: luotThoaiMau, loaiCanh: 'doi_thoai' },
  25,
  120,
);
const dsGiaiLuot2 = giaiTrangThaiNhanVatTrongCanh(
  { nhanVat: nvMauDoiThoai, luotThoai: luotThoaiMau, loaiCanh: 'doi_thoai' },
  80,
  120,
);
if (
  dsGiaiLuot1[0].dangNoi !== true ||
  dsGiaiLuot1[1].dangNoi !== false ||
  dsGiaiLuot1[0].hanhDong !== 'trao_thu' ||
  dsGiaiLuot2[0].dangNoi !== false ||
  dsGiaiLuot2[1].dangNoi !== true ||
  dsGiaiLuot2[1].hanhDong !== 'bat_tay'
) {
  baoLoi('giaiTrangThaiNhanVatTrongCanh khong chuyen luot thoai/dongTac dung giua cac nhan vat');
}

const nhinKhanGia = tinhHuongNhinTuongTac(nvMauDoiThoai[0], nvMauDoiThoai, {
  loaiCanh: 'tuong_tac_khan_gia',
});
if (!nhinKhanGia.nhinThangOngKinh) {
  baoLoi('Canh loaiCanh="tuong_tac_khan_gia" phai bat nhinThangOngKinh = true');
}

// Kiem tra dong ho dem nguoc 3 giay + hop dap an & chia doi man hinh (src/canh/tuong_tac.ts)
const cauHoiMau = {
  cauHoi: 'Số 1729 đặc biệt ở điểm nào?',
  thoiGianDemNguocGiay: 3,
  batDauDemNguocFrame: 15,
  dapAn: 'Số nhỏ nhất viết được thành tổng 2 lập phương theo 2 cách!',
};
const ttTruoc = tinhTrangThaiCauHoiTuongTac(cauHoiMau, 5, 180, 30);
const ttGiay3 = tinhTrangThaiCauHoiTuongTac(cauHoiMau, 20, 180, 30);
const ttGiay1 = tinhTrangThaiCauHoiTuongTac(cauHoiMau, 95, 180, 30);
const ttDapAn = tinhTrangThaiCauHoiTuongTac(cauHoiMau, 110, 180, 30);
if (
  !ttTruoc.dangDocCauHoi ||
  !ttGiay3.dangDemNguoc ||
  ttGiay3.giayConLai !== 3 ||
  ttGiay1.giayConLai !== 1 ||
  !ttDapAn.daHienDapAn ||
  ttDapAn.giayConLai !== 0
) {
  baoLoi('tinhTrangThaiCauHoiTuongTac tinh sai trang thai dem nguoc 3 giay / hien dap an');
}

const nhomChiaDoi = chiaNhomNhanVatChiaDoi(nvMauDoiThoai);
if (nhomChiaDoi.benTrai.length !== 1 || nhomChiaDoi.benPhai.length !== 1) {
  baoLoi('chiaNhomNhanVatChiaDoi khong tach dung 2 nhan vat sang 2 nua man hinh');
}

for (const tepCanh of ['CanhTuongTacKhanGia.tsx', 'LopCauHoiTuongTac.tsx', 'CanhChiaDoiManHinh.tsx']) {
  if (!fs.existsSync(path.join(gocDuAn, 'src', 'canh', tepCanh))) {
    baoLoi(`Thieu tep canh moi v2.0: src/canh/${tepCanh}`);
  }
}

console.log(
  `[OK] v2.0 Buoc 2: 8 gocQuay + tuDongFocusNguoiNoi (1.2x-1.45x), 4 doTuoi x 5 tuThe, 6 dong tac tuong tac moi (tong ${LOAI_HANH_DONG_HOP_LE.length}), bieuCamTheoMoc, luotThoai[], dem nguoc 3s + dap an & chia_doi_man_hinh pass 100%.`,
);

// 5f. Kiem tra v2.0 Buoc 3: 22 boi canh (10 moi + 12 cu), 20 dao cu (9 ke chuyen moi), SinhVatVaMoiTruong & React.memo
const BOI_CANH_MOI_V20 = [
  'nha_co_phong_sinh',
  'cang_bien_tau_thuy',
  'phong_tro_bep_lua',
  'phong_benh_vien',
  'duong_pho_xe_co',
  'giang_duong_dai_hoc',
  'san_truong_co_dien',
  'phong_thi_nghiem_co',
  'khong_gian_vu_tru_toan',
  'lang_que_an_do_a_dong',
];
const DAO_CU_MOI_V20 = [
  'noi_em_be',
  'noi_sup',
  'phong_bi_thu_tay',
  'giuong_benh',
  'bien_so_xe',
  'tach_tra_nong',
  'tau_thuy',
  'ban_hoc_den_dau',
  'qua_dia_cau',
];

if (DANH_SACH_LOAI_BOI_CANH.length < 22) {
  baoLoi(`DANH_SACH_LOAI_BOI_CANH phai co it nhat 22 boi canh, hien co ${DANH_SACH_LOAI_BOI_CANH.length}`);
}
for (const bc of BOI_CANH_MOI_V20) {
  if (!DANH_SACH_LOAI_BOI_CANH.includes(bc)) {
    baoLoi(`DANH_SACH_LOAI_BOI_CANH thieu boi canh moi v2.0: ${bc}`);
  }
  if (!srcBoiCanh.includes(`case '${bc}'`)) {
    baoLoi(`BoiCanhHoatHinh.tsx thieu nhanh switch cho boi canh moi "${bc}"`);
  }
}

const pathBoiCanhMoi = path.join(gocDuAn, 'src', 'boicanh', 'BoiCanhMoi.tsx');
const pathSinhVat = path.join(gocDuAn, 'src', 'boicanh', 'SinhVatVaMoiTruong.tsx');
if (!fs.existsSync(pathBoiCanhMoi) || !fs.existsSync(pathSinhVat)) {
  baoLoi('Thieu tep src/boicanh/BoiCanhMoi.tsx hoac src/boicanh/SinhVatVaMoiTruong.tsx');
} else {
  const srcBoiCanhMoi = fs.readFileSync(pathBoiCanhMoi, 'utf8');
  const srcSinhVat = fs.readFileSync(pathSinhVat, 'utf8');
  if (!srcBoiCanhMoi.includes('React.memo') || !srcBoiCanh.includes('React.memo')) {
    baoLoi('Phai dung React.memo cho cac lop nen tinh trong BoiCanhHoatHinh.tsx va BoiCanhMoi.tsx');
  }
  for (const vt of DANH_SACH_LOAI_VAT_THE_XUNG_QUANH) {
    if (!srcSinhVat.includes(`case '${vt}'`)) {
      baoLoi(`SinhVatVaMoiTruong.tsx thieu nhanh switch cho vat the "${vt}"`);
    }
  }
}

if (DANH_SACH_LOAI_DAO_CU.length < 20) {
  baoLoi(`DANH_SACH_LOAI_DAO_CU phai co it nhat 20 dao cu, hien co ${DANH_SACH_LOAI_DAO_CU.length}`);
}
for (const dc of DAO_CU_MOI_V20) {
  if (!DANH_SACH_LOAI_DAO_CU.includes(dc) || !srcDaoCu.includes(`case '${dc}'`)) {
    baoLoi(`DaoCu.tsx hoac kieu_dai.ts thieu dao cu ke chuyen moi "${dc}"`);
  }
}

// Kiem tra tinh tat dinh cua lop sinh vat & do vat moi truong (taxi 1729, qua lac, buom)
const vtPhoTaxi = giaiDanhSachVatTheXungQuanh('duong_pho_xe_co', 'nang_dep', undefined, '1729');
const taxiItem = vtPhoTaxi.find((v) => v.loai === 'xe_taxi_co');
if (!taxiItem || taxiItem.bienSoXe !== '1729') {
  baoLoi('giaiDanhSachVatTheXungQuanh cho duong_pho_xe_co phai co xe_taxi_co voi bienSoXe="1729"');
}
const vtBenhVien = layVatTheMacDinhChoBoiCanh('phong_benh_vien', 'tuyet_roi');
if (!vtBenhVien.some((v) => v.loai === 'tuyet_cua_so')) {
  baoLoi('phong_benh_vien phai tu dong gan tuyet_cua_so');
}
if (
  JSON.stringify(tinhViTriTaxiCo(45, 340, 3.1)) !== JSON.stringify(tinhViTriTaxiCo(45, 340, 3.1)) ||
  tinhGocQuaLac(30) !== tinhGocQuaLac(30) ||
  JSON.stringify(tinhBuomBay(24, 520, 610, 2)) !== JSON.stringify(tinhBuomBay(24, 520, 610, 2))
) {
  baoLoi('Ham chuyen dong trong moi_truong_logic.ts khong tat dinh');
}
// Kiem tra MinhHoaToan nhan mang buoc[] tu JSON
if (
  layDanhSachBuocSuyLuan({ buoc: ['1729 = 1³ + 12³', '1729 = 9³ + 10³'] }).length !== 2 ||
  coDuLieuMinhHoaHopLe({
    loai: 'chuoi_suy_luan',
    thamSo: { buoc: ['1729 = 1³ + 12³', '1729 = 9³ + 10³'] },
    mauNhanManh: '#38BDF8',
  }) !== true
) {
  baoLoi('minh_hoa_hop_le.ts khong ho tro danh sach buoc[] tu JSON');
}
console.log(
  `[OK] v2.0 Buoc 3: ${DANH_SACH_LOAI_BOI_CANH.length} boi canh Parallax (10 moi + React.memo), ${DANH_SACH_LOAI_DAO_CU.length} dao cu (9 ke chuyen moi), ${DANH_SACH_LOAI_VAT_THE_XUNG_QUANH.length} sinh vat/do vat moi truong tat dinh & MinhHoaToan tham so hoa JSON pass 100%.`,
);

// 5g. Kiem tra 6 loi bo cuc / hien thi da sua: HUD ngoai camera, khu trung lap noi/giuong, bong bong thoai khong cat ..., 2 cot tuong tac, giang toan zoom 1.0x & chuyen canh slide phu kin
const cauThoaiTrungBinh =
  'Không đâu Hardy! Đó là số nhỏ nhất bằng tổng hai lập phương theo hai cách khác nhau!';
const cacDongBongBong = chiaDongBongBong(cauThoaiTrungBinh);
if (
  cacDongBongBong.length < 2 ||
  cacDongBongBong.join(' ') !== cauThoaiTrungBinh ||
  cacDongBongBong.some((d) => d.includes('…') || d.includes('...'))
) {
  baoLoi(
    `chiaDongBongBong phai giu tron ven loi thoai va KHONG cat bang ... (nhan: ${JSON.stringify(cacDongBongBong)})`,
  );
}
if (
  coAnNoiNenPhongSinh([{ id: 'r', x: 960, y: 788, huong: 'phai', doTuoi: 'so_sinh', hanhDong: 'dung_tho', bieuCam: 'vui_tuoi' }], []) !== true ||
  coAnNoiNenPhongSinh([], [{ loai: 'noi_em_be', x: 1200, y: 760 }]) !== true ||
  coAnNoiNenPhongSinh([], []) !== false ||
  coAnGiuongBenhNen([{ id: 'r', x: 1280, y: 785, huong: 'trai', tuThe: 'nam_giuong', hanhDong: 'dung_tho', bieuCam: 'vui_tuoi' }], []) !== true ||
  coAnGiuongBenhNen([], []) !== false ||
  locDaoCuKhongTrungLap(
    [{ loai: 'giuong_benh', x: 1300, y: 770 }, { loai: 'tach_tra_nong', x: 1060, y: 675 }],
    [{ id: 'r', x: 1280, y: 785, huong: 'trai', tuThe: 'nam_giuong', hanhDong: 'dung_tho', bieuCam: 'vui_tuoi' }],
  ).length !== 1
) {
  baoLoi('Logic khu trung lap noi em be / giuong benh hoat dong chua dung');
}
if (!srcMayQuay.includes('HUD_TOP_SAFE = 76') || !srcMayQuay.includes('HUD_BOTTOM_SAFE = 150')) {
  baoLoi('MayQuayDong.tsx phai khai bao HUD_TOP_SAFE = 76 va HUD_BOTTOM_SAFE = 150 tach khoi transform');
}
const srcGiangToan = fs.readFileSync(path.join(gocDuAn, 'src', 'canh', 'CanhGiaiThichToan.tsx'), 'utf8');
if (!srcGiangToan.includes('doPhong: 1')) {
  baoLoi('CanhGiaiThichToan.tsx phai khoa zoom camera o 1.0x (doPhong: 1)');
}
console.log(
  '[OK] Kiem dinh 6 sua loi hien thi: HUD ngoai zoom (>=76px/150px), khu trung lap noi/giuong, bong bong thoai tron ven khong "...", tuong tac 2 cot, giang Toan zoom 1.0x & chuyen canh phu kin.',
);

// 5h. Kiem dinh nang cap v2.5 Buoc 1 (6 nhom sua loi sau dot chay that tap Georg Cantor)
// 1. xe_taxi_co KHONG hardcode bien so "1729" khi JSON khong truyen bienSoXe
const vtPhoKhongBienSo = giaiDanhSachVatTheXungQuanh('duong_pho_xe_co', 'nang_dep', undefined, undefined);
const taxiMacDinh = vtPhoKhongBienSo.find((v) => v.loai === 'xe_taxi_co');
if (!taxiMacDinh || taxiMacDinh.bienSoXe !== undefined) {
  baoLoi(`xe_taxi_co KHONG duoc hardcode bienSoXe khi khong truyen (nhan: ${JSON.stringify(taxiMacDinh)})`);
}
const srcSinhVatV25 = fs.readFileSync(path.join(gocDuAn, 'src', 'boicanh', 'SinhVatVaMoiTruong.tsx'), 'utf8');
if (srcSinhVatV25.includes("'1729'") || srcSinhVatV25.includes('"1729"')) {
  baoLoi('SinhVatVaMoiTruong.tsx KHONG duoc hardcode bien so "1729"');
}
if (!srcSinhVatV25.includes('clipPath')) {
  baoLoi('SinhVatVaMoiTruong.tsx phai dung SVG clipPath de chan tuyet_cua_so roi trong phong');
}

// 2. Rang buoc moi truong theo phong kin / vu tru & khung cua so tuyet
const locGiangDuong = locVatTheHopLeTheoBoiCanh('giang_duong_dai_hoc', [
  { loai: 'la_vang_gio', soLuong: 6 },
  { loai: 'dong_ho_qua_lac', x: 1680, y: 220 },
]);
if (locGiangDuong.some((v) => v.loai === 'la_vang_gio') || locGiangDuong.length !== 1) {
  baoLoi('locVatTheHopLeTheoBoiCanh phai cam la_vang_gio trong giang_duong_dai_hoc');
}
const locVuTru = locVatTheHopLeTheoBoiCanh('khong_gian_vu_tru_toan', [
  { loai: 'ngon_nen_den_dau', x: 400, y: 500 },
  { loai: 'la_vang_gio', soLuong: 4 },
]);
if (locVuTru.length !== 0) {
  baoLoi('locVatTheHopLeTheoBoiCanh phai cam ngon_nen_den_dau va la_vang_gio trong khong_gian_vu_tru_toan');
}
const cuaSoBepLua = layKhungCuaSoChoBoiCanh('phong_tro_bep_lua');
const cuaSoBenhVien = layKhungCuaSoChoBoiCanh('phong_benh_vien');
if (!cuaSoBepLua || !cuaSoBenhVien) {
  baoLoi('layKhungCuaSoChoBoiCanh phai tra ve khung cua so cho phong_tro_bep_lua va phong_benh_vien');
}
if (
  coHienNoiTrongPhongSinh([{ id: 'c', x: 760, y: 810, huong: 'phai', doTuoi: 'gia', hanhDong: 'dung_tho', bieuCam: 'vui_tuoi' }], []) !== false ||
  coHienNoiTrongPhongSinh([{ id: 'c', x: 760, y: 810, huong: 'phai', doTuoi: 'so_sinh', hanhDong: 'dung_tho', bieuCam: 'vui_tuoi' }], []) !== true
) {
  baoLoi('coHienNoiTrongPhongSinh chi duoc tra ve true khi co so_sinh hoac dao cu noi_em_be');
}

// 3. Cam "GOC BINH LUAN" tren giang_toan / dong_thoi_gian + timeline khong cat giua tu + 3 loai MinhHoaToan moi
const loiBinhMau = { noiDung: 'Bình luận vui', viTri: 'goc_phai' };
if (
  coHienKhungLoiBinh('giai_thich_toan', 'giang_toan', loiBinhMau) !== false ||
  coHienKhungLoiBinh('dong_thoi_gian', 'chuyen_canh_lich_su', loiBinhMau) !== false ||
  coHienKhungLoiBinh('ke_chuyen', 'giang_toan', loiBinhMau) !== false ||
  coHienKhungLoiBinh('ke_chuyen', 'ke_chuyen', loiBinhMau) !== true
) {
  baoLoi('coHienKhungLoiBinh phai chan tren giai_thich_toan, dong_thoi_gian va loaiCanh=giang_toan');
}
const srcTimelineV25 = fs.readFileSync(path.join(gocDuAn, 'src', 'canh', 'CanhDongThoiGian.tsx'), 'utf8');
if (srcTimelineV25.includes('KhungLoiBinhHaiHuoc') || srcGiangToan.includes('KhungLoiBinhHaiHuoc')) {
  baoLoi('CanhDongThoiGian.tsx va CanhGiaiThichToan.tsx KHONG duoc render KhungLoiBinhHaiHuoc');
}
const moTaTimelineDai = 'Cuộc tranh luận nảy lửa với Leopold Kronecker về nền tảng tập hợp vô hạn kéo dài nhiều năm';
const wrapTimeline = chiaDongMoTaTimeline(moTaTimelineDai, 4);
if (
  wrapTimeline.dong.length > 4 ||
  wrapTimeline.dong.join(' ') !== moTaTimelineDai
) {
  baoLoi(`chiaDongMoTaTimeline phai gon <= 4 dong va giu nguyen tung tu (nhan: ${JSON.stringify(wrapTimeline)})`);
}
for (const loaiMhMoi of ['so_do_anh_xa', 'luoi_duong_cheo', 'bieu_do_cot']) {
  if (!DANH_SACH_LOAI_MINH_HOA_TOAN.includes(loaiMhMoi)) {
    baoLoi(`DANH_SACH_LOAI_MINH_HOA_TOAN thieu loai truc quan moi: ${loaiMhMoi}`);
  }
}
if (
  !coDuLieuMinhHoaHopLe({
    loai: 'so_do_anh_xa',
    thamSo: { cotTrai: ['1', '2', '3'], cotPhai: ['2', '4', '6'] },
    mauNhanManh: '#FACC15',
  }) ||
  !coDuLieuMinhHoaHopLe({
    loai: 'luoi_duong_cheo',
    thamSo: { hang: ['0.141...', '0.333...', '0.718...'] },
    mauNhanManh: '#FACC15',
  }) ||
  !coDuLieuMinhHoaHopLe({
    loai: 'bieu_do_cot',
    thamSo: { nhan: ['N', 'R'], giaTri: [20, 95] },
    mauNhanManh: '#FACC15',
  })
) {
  baoLoi('coDuLieuMinhHoaHopLe phai chap nhan so_do_anh_xa, luoi_duong_cheo va bieu_do_cot');
}
const srcMinhHoaV25 = fs.readFileSync(path.join(gocDuAn, 'src', 'daocu', 'MinhHoaToan.tsx'), 'utf8');
for (const tenComp of ['SoDoAnhXaSvg', 'LuoiDuongCheoSvg', 'BieuDoCotSvg']) {
  if (!srcMinhHoaV25.includes(tenComp)) {
    baoLoi(`MinhHoaToan.tsx thieu component truc quan ${tenComp}`);
  }
}

// 4. VFX bong_den tren dau (headY - 75), "Ua khoan da?!" khong de nguoi ngoi ban, khu trung nhanVatId, tuong tac >= 2.5s dap an
const nvNgoiBan = {
  id: 'cantor',
  x: 780,
  y: 805,
  huong: 'phai',
  tuThe: 'ngoi_ban',
  hanhDong: 'ngoi_doc_sach',
  bieuCam: 'tram_tu',
  dangNoi: true,
};
const headYCantor = tinhDauNhanVatY(nvNgoiBan, 1.25);
const posBongDen = tinhToaDoHieuUngAnToan(
  { loai: 'bong_den_nay_so', x: 780, y: 740, tuFrame: 10 },
  [nvNgoiBan],
  1.25,
);
if (Math.abs(posBongDen.y - Math.round(headYCantor - 75)) > 2 || posBongDen.y >= headYCantor) {
  baoLoi(`bong_den_nay_so phai o phia tren dau (headY - 75 = ${Math.round(headYCantor - 75)}), nhan y=${posBongDen.y}`);
}
const posUaKhoanDa = tinhToaDoHieuUngAnToan(
  { loai: 'nhan_chu_hai_huoc', x: 780, y: 720, tuFrame: 10, chuHienThi: 'Ủa khoan đã?!' },
  [nvNgoiBan],
  1.25,
);
if (posUaKhoanDa.y > headYCantor - 40 && Math.abs(posUaKhoanDa.x - nvNgoiBan.x) < 160) {
  baoLoi(`nhan_chu_hai_huoc ("Ua khoan da?!") khong duoc de len than/mat nhan vat ngoi ban (nhan: ${JSON.stringify(posUaKhoanDa)})`);
}
const dsKhongTrung = khuTrungLapNhanVatTrongCanh([
  nvNgoiBan,
  { ...nvNgoiBan, x: 1200 },
  { ...nvNgoiBan, id: 'kronecker', x: 1280 },
]);
if (dsKhongTrung.length !== 2 || dsKhongTrung[0].id !== 'cantor' || dsKhongTrung[1].id !== 'kronecker') {
  baoLoi('khuTrungLapNhanVatTrongCanh phai loai bo cung 1 nhanVatId xuat hien 2 lan trong 1 canh');
}
const ttChat = tinhTrangThaiCauHoiTuongTac(
  {
    cauHoi: 'Tập nào lớn hơn?',
    thoiGianDemNguocGiay: 3,
    batDauDemNguocFrame: 30,
    hienDapAnTuFrame: 145, // co tinh dat qua sat cuoi canh 160 frame
    dapAn: 'Tập số thực R lớn hơn!',
  },
  150,
  160,
  30,
);
if (160 - ttChat.hienDapAnTuFrame < 75 || !ttChat.daHienDapAn) {
  baoLoi(`tuong_tac_khan_gia phai giu du it nhat 2.5s (75 frame) hien "DAP AN CHINH XAC" cuoi canh (hienDapAnTuFrame=${ttChat.hienDapAnTuFrame}/160)`);
}
console.log(
  '[OK] v2.5 Buoc 1: taxi khong hardcode 1729, clipPath cua so tuyet, cam la/nen lech boi canh, cam Goc Binh Luan tren Toan/Timeline, Timeline tu co khong cat tu, 3 so do Toan moi, VFX bong den headY-75, chong nhan doi nhan vat & dap an >=2.5s pass 100%.',
);

// 5i. Kiem dinh nang cap v3.0 Buoc 2: Kien truc Lai 2.5D (Trang phuc 2 sac do, 7 kieuToc, 4 coRau, bong tiep dat, dong bo anhSangMoiTruong, NenMinhHoaAI + Ken Burns)
const TRANG_PHUC_BAT_BUOC = [
  'ao_vest_co_dien',
  'ao_choang_hoc_gia',
  'ao_co_an_do',
  'ao_len_mua_dong',
  'ao_choang_hy_lap',
  'quan_phuc_co',
  'thuong_dan',
];
const KIEU_TOC_BAT_BUOC = [
  'gon_gang',
  'xoan_co_dien',
  'toc_bac_dai',
  'khan_quan',
  'mu_rong_vanh',
  'mu_noi',
  'hoi_hoi',
];
const CO_RAU_BAT_BUOC = ['khong', 'ria_mep', 'rau_quai_non', 'rau_bac_dai'];
const TAM_KHUNG_BAT_BUOC = ['toan_canh', 'ban_than', 'can_mat'];
const ANH_SANG_BAT_BUOC = ['nang_am', 'anh_nen', 'dem_lanh', 'trung_tinh', 'hoang_hon'];

for (const tp of TRANG_PHUC_BAT_BUOC) {
  if (!DANH_SACH_TRANG_PHUC.includes(tp)) {
    baoLoi(`DANH_SACH_TRANG_PHUC thieu "${tp}"`);
  }
}
for (const kt of KIEU_TOC_BAT_BUOC) {
  if (!DANH_SACH_KIEU_TOC.includes(kt)) {
    baoLoi(`DANH_SACH_KIEU_TOC thieu "${kt}"`);
  }
}
for (const cr of CO_RAU_BAT_BUOC) {
  if (!DANH_SACH_CO_RAU.includes(cr)) {
    baoLoi(`DANH_SACH_CO_RAU thieu "${cr}"`);
  }
}
for (const tk of TAM_KHUNG_BAT_BUOC) {
  if (!DANH_SACH_TAM_KHUNG.includes(tk)) {
    baoLoi(`DANH_SACH_TAM_KHUNG thieu "${tk}"`);
  }
}
for (const asLoai of ANH_SANG_BAT_BUOC) {
  if (!DANH_SACH_LOAI_ANH_SANG.includes(asLoai)) {
    baoLoi(`DANH_SACH_LOAI_ANH_SANG thieu "${asLoai}"`);
  }
}
if (MAU_MUC_TRUYEN_TRANH !== '#1A1A1A') {
  baoLoi(`MAU_MUC_TRUYEN_TRANH phai la #1A1A1A (nhan: ${MAU_MUC_TRUYEN_TRANH})`);
}

// Kiem tra giaiTrangPhucHieuLuc (tuong thich nguoc + 2 sac do cel-shading)
const htHyLap = giaiTrangPhucHieuLuc(
  { id: 'pyth', ten: 'Pythagoras', mauThan: '#1E293B', mauChuDao: '#2563EB', phuKien: 'vong_nguyet_que' },
  { id: 'pyth', x: 700, y: 810, huong: 'phai', hanhDong: 'dung_tho', bieuCam: 'binh_thuong' },
);
const htAnDo = giaiTrangPhucHieuLuc(
  { id: 'ram', ten: 'Ramanujan', mauThan: '#1E293B', mauChuDao: '#2563EB', phuKien: 'khong', trangPhuc: 'ao_co_an_do', kieuToc: 'gon_gang', coRau: 'ria_mep', mauAo: '#D97706' },
  { id: 'ram', x: 700, y: 810, huong: 'phai', hanhDong: 'dung_tho', bieuCam: 'vui_tuoi', tamKhung: 'ban_than' },
);
if (
  htHyLap.trangPhuc !== 'ao_choang_hy_lap' ||
  htAnDo.trangPhuc !== 'ao_co_an_do' ||
  htAnDo.kieuToc !== 'gon_gang' ||
  htAnDo.coRau !== 'ria_mep' ||
  htAnDo.mauAoChinh !== '#D97706' ||
  htAnDo.mauAoBong === htAnDo.mauAoChinh ||
  lamToiMauHex('#2563EB') === '#2563EB' ||
  lamSangMauHex('#2563EB') === '#2563EB'
) {
  baoLoi('giaiTrangPhucHieuLuc hoac ham cel-shading 2 sac do hoat dong chua dung');
}

// Kiem tra dong bo anhSangMoiTruong (do mo 0.08..0.22, khong filter nang)
const asTrong = tinhThamSoAnhSangNhanVat(undefined);
if (asTrong.coPhuMau !== false || asTrong.doMoPhu !== 0) {
  baoLoi('tinhThamSoAnhSangNhanVat(undefined) phai tra ve coPhuMau=false, doMoPhu=0');
}
for (const loaiAs of ANH_SANG_BAT_BUOC) {
  const ts = tinhThamSoAnhSangNhanVat({ mauAm: '#E8A24A', doToi: 0.6, loaiAnhSang: loaiAs });
  if (!ts.coPhuMau || ts.doMoPhu < 0.08 || ts.doMoPhu > 0.22 || !Number.isFinite(ts.doMoToi)) {
    baoLoi(`tinhThamSoAnhSangNhanVat("${loaiAs}") doMoPhu=${ts.doMoPhu} nam ngoai [0.08..0.22]`);
  }
}

// Kiem tra bong tiep dat (co gian theo nhay & buoc di) va tamKhung
const bongDung = tinhBongTiepDat(0, 'truong_thanh', 'dung', 10);
const bongBuoc = tinhBongTiepDat(0, 'truong_thanh', 'dung', 60);
const bongNhay = tinhBongTiepDat(85, 'truong_thanh', 'dung', 10);
if (!(bongBuoc.rx > bongDung.rx && bongNhay.rx < bongDung.rx && bongNhay.opacity < bongDung.opacity)) {
  baoLoi('tinhBongTiepDat khong co gian dung khi buoc di / bat nhay');
}
const tkToan = tinhTiLeTamKhung('toan_canh');
const tkBan = tinhTiLeTamKhung('ban_than');
const tkCan = tinhTiLeTamKhung('can_mat');
if (!(tkToan.heSoTiLe === 1 && tkBan.heSoTiLe > tkToan.heSoTiLe && tkCan.heSoTiLe > tkBan.heSoTiLe)) {
  baoLoi('tinhTiLeTamKhung khong tang dan theo toan_canh < ban_than < can_mat');
}

// Kiem tra NenMinhHoaAI: Ken Burns tat dinh, khong lo vien den & lop khong khi dung theo loaiAnhSang
for (const dacTa of [false, true]) {
  for (const fr of [0, 30, 90, 180]) {
    const kb1 = tinhKenBurnsNenAI(fr, 180, 'boi_canh/demo/bc_01.jpg', { panX: 45, panY: -20, zoom: 1.2 }, dacTa);
    const kb2 = tinhKenBurnsNenAI(fr, 180, 'boi_canh/demo/bc_01.jpg', { panX: 45, panY: -20, zoom: 1.2 }, dacTa);
    if (JSON.stringify(kb1) !== JSON.stringify(kb2)) {
      baoLoi(`tinhKenBurnsNenAI(frame=${fr}, dacTa=${dacTa}) khong tat dinh`);
      break;
    }
    const maxTx = 960 * (kb1.scale - 1) + 0.1;
    const maxTy = 540 * (kb1.scale - 1) + 0.1;
    if (!Number.isFinite(kb1.scale) || Math.abs(kb1.tx) > maxTx || Math.abs(kb1.ty) > maxTy) {
      baoLoi(`tinhKenBurnsNenAI(frame=${fr}, dacTa=${dacTa}) vuot bien khung (lo vien den): ${JSON.stringify(kb1)}`);
      break;
    }
  }
}
const kkNang = tinhLopKhongKhiNenAI({ mauAm: '#F4D99B', doToi: 0.2, loaiAnhSang: 'nang_am' }, 'nang_dep', 'bo_bien_hy_lap', false);
const kkNen = tinhLopKhongKhiNenAI({ mauAm: '#E8A24A', doToi: 0.72, loaiAnhSang: 'anh_nen' }, 'khong', 'thu_vien_co_dien', false);
const kkDem = tinhLopKhongKhiNenAI({ mauAm: '#3B5284', doToi: 0.8, loaiAnhSang: 'dem_lanh' }, 'ban_dem', 'bau_troi_dem_vu_tru', false);
const kkDacTa = tinhLopKhongKhiNenAI({ mauAm: '#F4D99B', doToi: 0.3, loaiAnhSang: 'nang_am' }, 'nang_dep', 'bo_bien_hy_lap', true);
if (
  !kkNang.coLuongNangXien ||
  !kkNang.coMayChimNgoaiTroi ||
  !kkNen.coAnhNenNhapNhay ||
  kkNen.coMayChimNgoaiTroi ||
  !kkDem.coSuongDem ||
  kkDacTa.coMayChimNgoaiTroi ||
  !kkDacTa.coBuiSang
) {
  baoLoi('tinhLopKhongKhiNenAI bat/tat lop khong khi chua khop loaiAnhSang/boiCanh/laKhungTranhDacTa');
}

// Kiem tra file NenMinhHoaAI.tsx, TrangPhucVaToc.tsx & tich hop trong BoiCanhHoatHinh.tsx
const pathNenAI = path.join(gocDuAn, 'src', 'boicanh', 'NenMinhHoaAI.tsx');
const pathTrangPhuc = path.join(gocDuAn, 'src', 'nhanvat', 'TrangPhucVaToc.tsx');
if (!fs.existsSync(pathNenAI) || !fs.existsSync(pathTrangPhuc)) {
  baoLoi('Thieu tep v3.0: src/boicanh/NenMinhHoaAI.tsx hoac src/nhanvat/TrangPhucVaToc.tsx');
} else {
  const srcNenAI = fs.readFileSync(pathNenAI, 'utf8');
  const srcTrangPhuc = fs.readFileSync(pathTrangPhuc, 'utf8');
  if (!srcNenAI.includes('<Img') || !srcNenAI.includes('staticFile(') || !srcNenAI.includes('radialGradient')) {
    baoLoi('NenMinhHoaAI.tsx phai dung <Img src={staticFile(...)} /> va radialGradient phang');
  }
  if (!srcBoiCanh.includes('NenMinhHoaAI') || !srcBoiCanh.includes('anhBoiCanh')) {
    baoLoi('BoiCanhHoatHinh.tsx chua tich hop NenMinhHoaAI khi canh co anhBoiCanh');
  }
  for (const tp of TRANG_PHUC_BAT_BUOC) {
    if (!srcTrangPhuc.includes(`case '${tp}'`)) {
      baoLoi(`TrangPhucVaToc.tsx thieu nhanh ve trang phuc "${tp}"`);
    }
  }
  for (const kt of KIEU_TOC_BAT_BUOC) {
    if (!srcTrangPhuc.includes(`case '${kt}'`)) {
      baoLoi(`TrangPhucVaToc.tsx thieu nhanh ve kieu toc "${kt}"`);
    }
  }
  for (const cr of CO_RAU_BAT_BUOC.filter((x) => x !== 'khong')) {
    if (!srcTrangPhuc.includes(`case '${cr}'`)) {
      baoLoi(`TrangPhucVaToc.tsx thieu nhanh ve rau "${cr}"`);
    }
  }
}
console.log(
  `[OK] v3.0 Buoc 2 (Lai 2.5D): ${TRANG_PHUC_BAT_BUOC.length} trangPhuc 2 sac do, ${KIEU_TOC_BAT_BUOC.length} kieuToc, ${CO_RAU_BAT_BUOC.length} coRau, bong tiep dat, dong bo anhSangMoiTruong (0.08-0.22), NenMinhHoaAI Ken Burns + khong khi tat dinh pass 100%.`,
);

// 5j. Kiem dinh nang cap v3.0 Buoc 3: Clean Cinema UI, 4 goc can mat & Shot-Reverse-Shot, BongBongChat 4 kieu & 6 VFX hai neo quanh dau
// 1. Clean Cinema UI: bo thanh tien do co dinh, bo hop GOC BINH LUAN co dinh, TheTenHoi 2.8s & phu de tu an khi trung bong bong
const srcVideoDaiV3 = fs.readFileSync(path.join(gocDuAn, 'src', 'VideoDai.tsx'), 'utf8');
const srcLoiBinhV3 = fs.readFileSync(path.join(gocDuAn, 'src', 'canh', 'KhungLoiBinhHaiHuoc.tsx'), 'utf8');
if (srcVideoDaiV3.includes('Thanh tien do chuong') || !srcVideoDaiV3.includes('<TheTenHoi') || !srcVideoDaiV3.includes('coAnPhuDeTrungBongBong')) {
  baoLoi('VideoDai.tsx phai go thanh tien do co dinh, gan TheTenHoi 2.8s va tu an phu de trung bong bong');
}
if (srcLoiBinhV3.includes('Góc bình luận')) {
  baoLoi('KhungLoiBinhHaiHuoc.tsx phai go bo hop "Góc bình luận" co dinh o goc phai');
}
const thHoi0 = tinhTrangThaiTheTenHoi(0, 30);
const thHoiGiua = tinhTrangThaiTheTenHoi(40, 30);
const thHoiHet = tinhTrangThaiTheTenHoi(Math.round(THOI_LUONG_THE_TEN_HOI_GIAY * 30), 30);
if (!thHoi0.dangHien || thHoiGiua.opacity !== 1 || thHoiHet.dangHien !== false || thHoiHet.opacity !== 0) {
  baoLoi(`tinhTrangThaiTheTenHoi sai moc 2.8s (f40=${JSON.stringify(thHoiGiua)}, f84=${JSON.stringify(thHoiHet)})`);
}
const anTrungLuot = coAnPhuDeTrungBongBong(
  { nhanVat: nvMauDoiThoai, luotThoai: luotThoaiMau },
  20,
  'Hardy: Thư này chứa công thức rất kỳ lạ!',
);
const hienDanChuyen = coAnPhuDeTrungBongBong(
  { nhanVat: nvMauDoiThoai },
  20,
  'Năm 1913, một bức thư chín trang vượt đại dương đến Cambridge.',
);
if (anTrungLuot !== true || hienDanChuyen !== false) {
  baoLoi('coAnPhuDeTrungBongBong phai an phu de trung bong bong va giu nguyen loi dan chuyen');
}

// 2. 4 goc quay can mat & Shot-Reverse-Shot (dao_goc_can_mat)
const GOC_CAN_MAT_V30 = ['can_mat_trai', 'can_mat_phai', 'can_mat_kich_tinh', 'dao_goc_can_mat'];
for (const gq of GOC_CAN_MAT_V30) {
  if (!DANH_SACH_GOC_QUAY.includes(gq)) {
    baoLoi(`DANH_SACH_GOC_QUAY thieu goc quay v3.0 "${gq}"`);
  }
  for (const f of [0, 20, 45, 90]) {
    const cam = tinhBienDoiCamera(f, 120, undefined, nvMauDoiThoai, { gocQuay: gq }, luotThoaiMau);
    const maxPanX = 960 * Math.max(0, cam.zoom - 1) + 0.5;
    const maxPanY = 540 * Math.max(0, cam.zoom - 1) + 0.5;
    if (!Number.isFinite(cam.zoom) || Math.abs(cam.panX) > maxPanX || Math.abs(cam.panY) > maxPanY) {
      baoLoi(`Goc quay v3.0 "${gq}" frame=${f} vuot bien khung (lo vien den): ${JSON.stringify(cam)}`);
      break;
    }
  }
}
const camCmTrai = tinhBienDoiCamera(40, 120, undefined, nvMauDoiThoai, { gocQuay: 'can_mat_trai' });
const camCmPhai = tinhBienDoiCamera(40, 120, undefined, nvMauDoiThoai, { gocQuay: 'can_mat_phai' });
const camKichTinh = tinhBienDoiCamera(14, 120, undefined, nvMauDoiThoai, { gocQuay: 'can_mat_kich_tinh' });
const camDaoA = tinhBienDoiCamera(30, 120, undefined, nvMauDoiThoai, { gocQuay: 'dao_goc_can_mat' }, luotThoaiMau);
const camDaoB = tinhBienDoiCamera(90, 120, undefined, nvMauDoiThoai, { gocQuay: 'dao_goc_can_mat' }, luotThoaiMau);
if (
  camCmTrai.zoom < 1.85 ||
  camCmTrai.zoom > 2.15 ||
  camCmTrai.panX <= 0 ||
  camCmPhai.zoom < 1.85 ||
  camCmPhai.zoom > 2.15 ||
  camCmPhai.panX >= 0
) {
  baoLoi(`can_mat_trai/phai khong dat zoom 1.85x-2.1x & khoa 1/3 (trai=${JSON.stringify(camCmTrai)}, phai=${JSON.stringify(camCmPhai)})`);
}
if (camKichTinh.zoom < 2.05 || !camKichTinh.hienTiaTocDo) {
  baoLoi(`can_mat_kich_tinh phai zoom ~2.2x va bat hienTiaTocDo=true (nhan: ${JSON.stringify(camKichTinh)})`);
}
if (!(camDaoA.zoom >= 1.85 && camDaoB.zoom >= 1.85 && camDaoA.panX > 0 && camDaoB.panX < 0)) {
  baoLoi(`dao_goc_can_mat phai tu dong dao can mat A (panX>0) <-> B (panX<0) theo luotThoai[] (A=${JSON.stringify(camDaoA)}, B=${JSON.stringify(camDaoB)})`);
}

// 3. BongBongChat 4 kieu + tranh tran mep 1920x1080 & tranh che mat
const KIEU_BB_BAT_BUOC = ['thuong', 'quat_thao', 'suy_nghi', 'ca_khia'];
for (const kb of KIEU_BB_BAT_BUOC) {
  if (!DANH_SACH_KIEU_BONG_BONG.includes(kb)) {
    baoLoi(`DANH_SACH_KIEU_BONG_BONG thieu "${kb}"`);
  }
}
const pathBongBong = path.join(gocDuAn, 'src', 'canh', 'BongBongChat.tsx');
if (!fs.existsSync(pathBongBong)) {
  baoLoi('Thieu tep src/canh/BongBongChat.tsx');
} else {
  const srcBb = fs.readFileSync(pathBongBong, 'utf8');
  for (const kb of KIEU_BB_BAT_BUOC) {
    if (!srcBb.includes(kb)) {
      baoLoi(`BongBongChat.tsx thieu kieu "${kb}"`);
    }
  }
}
for (const wx of [120, 960, 1820]) {
  const bc = tinhBoCucBongBongChat({
    noiDung: 'Khoan đã, tại sao tập số thực lại lớn hơn tập số tự nhiên?!',
    kieu: 'quat_thao',
    nhanVatWorldX: wx,
    nhanVatWorldY: 800,
    tiLeNhanVat: 1.25,
    dauLocalX: 0,
    dauLocalY: -170,
    dir: wx > 1000 ? 1 : -1,
  });
  const nuaR = (bc.width / 2) * 1.25;
  if (bc.worldX - nuaR < 25 || bc.worldX + nuaR > 1895) {
    baoLoi(`tinhBoCucBongBongChat bi tran mep man hinh tai wx=${wx}: ${JSON.stringify(bc)}`);
  }
}

// 4. 6 hieu ung hai thi giac moi & neo chuan quanh dau (KHONG moc o bung)
const VFX_HAI_V30 = [
  'mo_hoi_lon',
  'khoi_boc_tai',
  'mat_xoan_oc',
  'cham_hoi_nay',
  'tia_toc_do',
  'bong_den_y_tuong',
];
const srcHieuUngV3 = fs.readFileSync(path.join(gocDuAn, 'src', 'vfx', 'HieuUngHoatHinh.tsx'), 'utf8');
const headYTest = tinhDauNhanVatY(nvMauDoiThoai[0], 1.25);
for (const loaiVfx of VFX_HAI_V30) {
  if (!DANH_SACH_LOAI_HIEU_UNG_HOAT_HINH.includes(loaiVfx)) {
    baoLoi(`DANH_SACH_LOAI_HIEU_UNG_HOAT_HINH thieu "${loaiVfx}"`);
  }
  if (!srcHieuUngV3.includes(`case '${loaiVfx}'`)) {
    baoLoi(`HieuUngHoatHinh.tsx thieu nhanh ve "${loaiVfx}"`);
  }
  if (!layDuongDanSfxNeuCoSan(loaiVfx)) {
    baoLoi(`BAN_DO_SFX_HIEU_UNG thieu anh xa cho "${loaiVfx}"`);
  }
  // Co tinh truyen y=760 (vung bung/chan) -> tinhToaDoHieuUngAnToan phai keo len quanh dau!
  const posVfx = tinhToaDoHieuUngAnToan(
    { loai: loaiVfx, x: nvMauDoiThoai[0].x, y: 760, tuFrame: 5, thoiLuong: 40 },
    nvMauDoiThoai,
    1.25,
  );
  if (posVfx.y > headYTest + 10) {
    baoLoi(`VFX hai "${loaiVfx}" bi moc thap o bung (y=${posVfx.y} > headY=${Math.round(headYTest)})`);
  }
}
console.log(
  '[OK] v3.0 Buoc 3 (Clean Cinema UI): bo thanh tien do & GOC BINH LUAN, TheTenHoi 2.8s, phu de vien manh tu an trung bong bong, 4 goc can mat & dao_goc_can_mat, BongBongChat 4 kieu & 6 VFX hai neo quanh dau pass 100%.',
);

// 5c. Kiem dinh v3.5: 4 nhac nen da cam xuc, 3 khung hinh ke chuyen moi, Mascot kenh, End-Screen 15s & Thumbnail anh AI
for (const bgmMood of ['vui_tuoi', 'bi_an', 'kich_tinh', 'tram_lang']) {
  if (!DANH_SACH_TAM_TRANG_NHAC.includes(bgmMood)) {
    baoLoi(`DANH_SACH_TAM_TRANG_NHAC thieu "${bgmMood}"`);
  }
  const bgmFile = path.join(gocDuAn, 'public', 'bgm', `${bgmMood}.mp3`);
  if (!fs.existsSync(bgmFile) || fs.statSync(bgmFile).size < 1024) {
    baoLoi(`Thieu file nhac nen v3.5 public/bgm/${bgmMood}.mp3`);
  }
}

for (const bcMoi of ['ban_do_hanh_trinh', 'bao_chi_co', 'phan_ung_cam']) {
  if (!DANH_SACH_LOAI_BO_CUC.includes(bcMoi)) {
    baoLoi(`DANH_SACH_LOAI_BO_CUC thieu boCuc v3.5 "${bcMoi}"`);
  }
}
for (const fileCanhMoi of ['CanhBanDoHanhTrinh.tsx', 'CanhBaoChiCo.tsx', 'CanhPhanUngCam.tsx']) {
  if (!fs.existsSync(path.join(gocDuAn, 'src', 'canh', fileCanhMoi))) {
    baoLoi(`Thieu component v3.5 src/canh/${fileCanhMoi}`);
  }
}
if (DANH_SACH_PHUONG_TIEN_HANH_TRINH.length !== 4 || DANH_SACH_KIEU_PHAN_UNG_CAM.length !== 4) {
  baoLoi('Enum PHUONG_TIEN_HANH_TRINH va KIEU_PHAN_UNG_CAM phai co du 4 gia tri');
}

// Kiem tra toan hoc tat dinh cua 3 canh moi
const ht0 = tinhTrangThaiHanhTrinh(0, 120);
const htMid = tinhTrangThaiHanhTrinh(60, 120);
const htEnd = tinhTrangThaiHanhTrinh(115, 120);
if (
  ht0.tienDo !== 0 ||
  !(htMid.tienDo > 0.3 && htMid.tienDo < 0.7) ||
  htEnd.tienDo !== 1 ||
  !htEnd.daDenNoi ||
  Math.abs(ht0.viTri.x - TOA_DO_BAN_DO_MAC_DINH.p0.x) > 1 ||
  Math.abs(htEnd.viTri.x - TOA_DO_BAN_DO_MAC_DINH.p2.x) > 1
) {
  baoLoi(`tinhTrangThaiHanhTrinh sai quy dao Bezier: f0=${JSON.stringify(ht0)}, f115=${JSON.stringify(htEnd)}`);
}

const bao0 = tinhBienDoiBaoChiCo(0, 90);
const bao30 = tinhBienDoiBaoChiCo(30, 90);
if (bao0.scale >= 0.5 || bao0.xoayDeg >= -180 || bao30.scale < 1.0 || !bao30.hienTieuDePhu) {
  baoLoi(`tinhBienDoiBaoChiCo sai hieu ung xoay phong: f0=${JSON.stringify(bao0)}, f30=${JSON.stringify(bao30)}`);
}

const pu10 = tinhTrangThaiPhanUngCam(10, 60);
const pu30 = tinhTrangThaiPhanUngCam(30, 60);
if (pu10.zoom < 1.9 || !pu10.hienTemChu || pu30.nhapTraTienDo <= 0.8) {
  baoLoi(`tinhTrangThaiPhanUngCam sai trang thai can mat: f10=${JSON.stringify(pu10)}, f30=${JSON.stringify(pu30)}`);
}

// Kiem tra Mascot kenh, End-Screen 2 khung & Thumbnail uu tien anhBoiCanh AI
const mascotDefault = layHoSoMascotKenh();
const mascotCustom = layHoSoMascotKenh({ ten: 'Thầy Beta', mauAo: '#16A34A' });
const mascotTat = layHoSoMascotKenh({ batMascot: false });
if (
  !mascotDefault ||
  mascotDefault.id !== ID_MASCOT_KENH ||
  mascotDefault.ten !== MASCOT_KENH_MAC_DINH.ten ||
  mascotCustom?.ten !== 'Thầy Beta' ||
  mascotCustom?.mauAo !== '#16A34A' ||
  mascotTat !== null
) {
  baoLoi('layHoSoMascotKenh khong dung hop dong tuy chinh/tat Mascot');
}
const { khungTrai, khungPhai, vungMascotGiua } = VUNG_END_SCREEN_YOUTUBE;
if (
  khungTrai.x + khungTrai.width >= vungMascotGiua.x - 200 ||
  khungPhai.x <= vungMascotGiua.x + 200 ||
  khungTrai.y + khungTrai.height > 850
) {
  baoLoi('VUNG_END_SCREEN_YOUTUBE bi de len vung Mascot giua hoac vung phu de day');
}
const srcCanhKetV35 = fs.readFileSync(path.join(gocDuAn, 'src', 'canh', 'CanhKet.tsx'), 'utf8');
const srcThumbV35 = fs.readFileSync(path.join(gocDuAn, 'src', 'Thumbnail.tsx'), 'utf8');
if (!srcCanhKetV35.includes('VUNG_END_SCREEN_YOUTUBE') || !srcCanhKetV35.includes('khungTrai')) {
  baoLoi('CanhKet.tsx phai hien thi 2 khung YouTube End-Screen 15s cuoi');
}
if (!srcThumbV35.includes('anhBoiCanh') || !srcThumbV35.includes('staticFile(')) {
  baoLoi('Thumbnail.tsx phai uu tien anhBoiCanh AI lam phong nen khi co');
}
console.log(
  '[OK] v3.5 Ke Chuyen Dien Anh: 4 nhac nen da cam xuc, 3 canh moi (BanDo/BaoChi/PhanUngCam), Mascot kenh, End-Screen 2 khung & Thumbnail anh AI pass 100%.',
);

// 6. Quet quy tac cam blur va Math.random() trong src/
const quyTacCam = [
  { ten: 'backdrop-filter: blur', regex: /backdrop-?filter\s*[:=][^;\n]*blur/i },
  { ten: 'filter: blur', regex: /\bfilter\s*[:=][^;\n]*blur/i },
  { ten: 'SVG <filter>', regex: /<filter\b/i },
  { ten: 'Math.random()', regex: /Math\.random\s*\(/ },
];

function quetThuMuc(thuMuc) {
  for (const entry of fs.readdirSync(thuMuc, { withFileTypes: true })) {
    const dayDu = path.join(thuMuc, entry.name);
    if (entry.isDirectory()) {
      quetThuMuc(dayDu);
    } else if (/\.(ts|tsx|js|mjs|css)$/.test(entry.name)) {
      const text = fs.readFileSync(dayDu, 'utf8');
      for (const qt of quyTacCam) {
        if (qt.regex.test(text)) {
          baoLoi(`Vi pham quy tac cam "${qt.ten}" tai ${path.relative(gocDuAn, dayDu)}`);
        }
      }
    }
  }
}

quetThuMuc(path.join(gocDuAn, 'src'));
console.log('[OK] Quet quy tac cam (blur / Math.random): sach 100%.');

if (loi.length > 0) {
  console.error('\n[THAT BAI] Phat hien loi kiem tra khung:');
  for (const l of loi) {
    console.error(`  - ${l}`);
  }
  process.exit(1);
}

console.log('\n[THANH CONG] Tat ca kiem tra khung v2.0 (Buoc 1 + Buoc 2: 8 gocQuay, tuDongFocusNguoiNoi, 4 doTuoi, 5 tuThe, 20 hanhDong FK, luotThoai, tuongTacKhanGia 3s, chiaDoiManHinh, Parallax, SFX, Lip-sync RMS & Quy tac cam) deu xanh!');
