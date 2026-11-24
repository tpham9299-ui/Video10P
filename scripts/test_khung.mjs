import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { tinhKhungXuongCoBan } from '../src/xuong/he_xuong.ts';
import {
  easeInBack,
  easeInOutCubic,
  easeOutBack,
  springTatDinh,
} from '../src/xuong/duong_cong.ts';
import { bamTatDinh, bamChuoiTatDinh } from '../src/vfx/tat_dinh.ts';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const gocDuAn = path.resolve(__dirname, '..');

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
  `[OK] src/xuong/he_xuong.ts (FK): 14/14 hanh dong x frames [${MOC_FRAME_FK.join(', ')}] x 2 huong x dangNoi tat dinh 100%, du ${KHOP_XUONG_BAT_BUOC.length} khop, squash bao toan dien tich, khong NaN/Infinity.`,
);

// 4. Kiem tra bamTatDinh & bamChuoiTatDinh
if (bamTatDinh(42) !== bamTatDinh(42) || bamChuoiTatDinh('pythagoras') !== bamChuoiTatDinh('pythagoras')) {
  baoLoi('src/vfx/tat_dinh.ts khong tat dinh!');
} else {
  console.log('[OK] src/vfx/tat_dinh.ts: ham bam seed tat dinh 100%.');
}

// 5. Quet quy tac cam blur va Math.random() trong src/
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

console.log('\n[THANH CONG] Tat ca kiem tra khung v0.4 (Chuyen dong hoat hinh 2D FK + Parallax + Chuyen canh) deu xanh!');
