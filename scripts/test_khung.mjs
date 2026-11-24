import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const gocDuAn = path.resolve(__dirname, '..');

const LOAI_BO_CUC_BAT_BUOC = [
  'mo_dau',
  'ke_chuyen',
  'doi_thoai',
  'hanh_dong',
  'giai_thich_toan',
  'dong_thoi_gian',
  'ket_thuc',
];

const KHOP_XUONG_BAT_BUOC = [
  'hong',
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
  'diemCamVuKhi',
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
  const tapNhanVat = new Set(
    (duLieu.danhSachNhanVat ?? []).map((nv) => nv.id),
  );
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

  let frameTruoc = 0;
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
      baoLoi(`Canh ${c.id}: bi chong de frame (tuFrame=${c.tuFrame} < ${frameTruoc})`);
    }
    if (i > 0 && c.tuFrame !== frameTruoc) {
      baoLoi(`Canh ${c.id}: khong noi tiep sat frame truoc (${frameTruoc} -> ${c.tuFrame})`);
    }
    frameTruoc = c.denFrame;

    for (const nv of c.nhanVat ?? []) {
      if (!tapNhanVat.has(nv.id)) {
        baoLoi(`Canh ${c.id}: nhanVat.id "${nv.id}" khong ton tai trong danhSachNhanVat`);
      }
    }
  }

  const tongFrames = frameTruoc;
  const thoiLuongGiay = (tongFrames / 30).toFixed(2);
  console.log(
    `[OK] mau_pythagoras.json: ${tatCaCanh.length} canh, ${tapBoCuc.size}/7 boCuc, tong ${tongFrames} frames (${thoiLuongGiay}s @ 30fps).`,
  );
}

// 2. Kiem tra cau truc src/xuong/he_xuong.ts
const duongDanXuong = path.join(gocDuAn, 'src', 'xuong', 'he_xuong.ts');
if (!fs.existsSync(duongDanXuong)) {
  baoLoi('Khong tim thay src/xuong/he_xuong.ts');
} else {
  const noiDungXuong = fs.readFileSync(duongDanXuong, 'utf8');
  if (!noiDungXuong.includes('export type TuTheKhungXuong')) {
    baoLoi('src/xuong/he_xuong.ts thieu export type TuTheKhungXuong');
  }
  if (!noiDungXuong.includes('export function tinhKhungXuongCoBan')) {
    baoLoi('src/xuong/he_xuong.ts thieu export function tinhKhungXuongCoBan');
  }
  for (const khop of KHOP_XUONG_BAT_BUOC) {
    if (!noiDungXuong.includes(`${khop}:`)) {
      baoLoi(`src/xuong/he_xuong.ts thieu khop "${khop}" trong TuTheKhungXuong`);
    }
  }
  console.log(
    `[OK] src/xuong/he_xuong.ts: hop le (${KHOP_XUONG_BAT_BUOC.length} khop + tinhKhungXuongCoBan).`,
  );
}

// 3. Quet quy tac cam blur va Math.random() trong src/
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

console.log('\n[THANH CONG] Tat ca kiem tra khung v0.1 deu xanh!');
