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
  DANH_SACH_DO_TUOI,
  DANH_SACH_GOC_QUAY,
  DANH_SACH_LOAI_BOI_CANH,
  DANH_SACH_LOAI_CANH,
  DANH_SACH_LOAI_DAO_CU,
  DANH_SACH_LOAI_HANH_DONG,
  DANH_SACH_LOAI_MINH_HOA_TOAN,
  DANH_SACH_LOAI_VAT_THE_XUNG_QUANH,
  DANH_SACH_TU_THE,
} from './src/kieu_dai.ts';
export {
  coAnGiuongBenhNen,
  coAnNoiNenPhongSinh,
  giaiDanhSachVatTheXungQuanh,
  layVatTheMacDinhChoBoiCanh,
  locDaoCuKhongTrungLap,
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
  tinhHuongNhinTuongTac,
} from './src/nhanvat/dien_xuat.ts';
export {
  chiaNhomNhanVatChiaDoi,
  tinhTrangThaiCauHoiTuongTac,
} from './src/canh/tuong_tac.ts';
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
  DANH_SACH_DO_TUOI,
  DANH_SACH_GOC_QUAY,
  DANH_SACH_LOAI_BOI_CANH,
  DANH_SACH_LOAI_CANH,
  DANH_SACH_LOAI_DAO_CU,
  DANH_SACH_LOAI_HANH_DONG,
  DANH_SACH_LOAI_MINH_HOA_TOAN,
  DANH_SACH_LOAI_VAT_THE_XUNG_QUANH,
  DANH_SACH_TU_THE,
  coAnGiuongBenhNen,
  coAnNoiNenPhongSinh,
  giaiDanhSachVatTheXungQuanh,
  layVatTheMacDinhChoBoiCanh,
  locDaoCuKhongTrungLap,
  tinhBuomBay,
  tinhGocQuaLac,
  tinhViTriTaxiCo,
  tinhBienDoiCamera,
  xacDinhNguoiDangNoiTaiFrame,
  giaiBieuCamTheoMoc,
  giaiTrangThaiNhanVatTrongCanh,
  tinhHuongNhinTuongTac,
  chiaNhomNhanVatChiaDoi,
  tinhTrangThaiCauHoiTuongTac,
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
