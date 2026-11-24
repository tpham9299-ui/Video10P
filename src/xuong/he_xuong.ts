import type { HuongNhanVat, LoaiHanhDong } from '../kieu_dai';

// TODO(v0.2): nang cap xuong khop & VFX

export type Diem2D = {
  x: number;
  y: number;
};

export type TuTheKhungXuong = {
  hong: Diem2D;
  co: Diem2D;
  dau: Diem2D;
  vaiTrai: Diem2D;
  khuyuTrai: Diem2D;
  banTayTrai: Diem2D;
  vaiPhai: Diem2D;
  khuyuPhai: Diem2D;
  banTayPhai: Diem2D;
  goiTrai: Diem2D;
  banChanTrai: Diem2D;
  goiPhai: Diem2D;
  banChanPhai: Diem2D;
  diemCamVuKhi: Diem2D;
};

/**
 * Tinh khung xuong nguoi que giu cho (v0.1).
 * He toa do cuc bo: (0, 0) la mat dat giua hai ban chan, truc Y am huong len tren.
 * Tat dinh 100% theo frameCucBo, khong bao gio tra ve NaN.
 */
export function tinhKhungXuongCoBan(
  hanhDong: LoaiHanhDong,
  frameCucBo: number,
  huong: HuongNhanVat,
): TuTheKhungXuong {
  const f = Number.isFinite(frameCucBo) ? frameCucBo : 0;
  const dir = huong === 'trai' ? -1 : 1;

  const nhipTho = Math.sin(f * 0.14) * 3;
  const lacTay = Math.sin(f * 0.18) * 6;

  let nhayY = 0;
  let nghiengThanX = 0;
  let tayTruocDX = 26 * dir;
  let tayTruocDY = 14;
  let taySauDX = -22 * dir;
  let taySauDY = 20;
  let buocChan = 0;

  switch (hanhDong) {
    case 'giang_bai':
      tayTruocDX = 42 * dir;
      tayTruocDY = -8 + Math.sin(f * 0.25) * 8;
      break;
    case 'chi_bang':
      tayTruocDX = 54 * dir;
      tayTruocDY = -24 + Math.sin(f * 0.12) * 3;
      break;
    case 'suy_nghi_gai_dau':
      tayTruocDX = 14 * dir;
      tayTruocDY = -38 + Math.sin(f * 0.2) * 2;
      nghiengThanX = -4 * dir;
      break;
    case 'soc_lui_lai':
      nghiengThanX = -16 * dir;
      tayTruocDX = 28 * dir;
      tayTruocDY = -14;
      taySauDX = -32 * dir;
      taySauDY = -10;
      break;
    case 'an_mung_nhay':
      nhayY = -Math.abs(Math.sin(f * 0.25)) * 22;
      tayTruocDX = 30 * dir;
      tayTruocDY = -42;
      taySauDX = -30 * dir;
      taySauDY = -42;
      break;
    case 'chay_nuoc_rut':
      nghiengThanX = 14 * dir;
      buocChan = Math.sin(f * 0.45) * 18;
      tayTruocDX = (28 + Math.sin(f * 0.45) * 14) * dir;
      tayTruocDY = 4;
      taySauDX = (-26 - Math.sin(f * 0.45) * 14) * dir;
      taySauDY = 8;
      break;
    case 'luot_nhanh_dash':
      nghiengThanX = 24 * dir;
      nhayY = -6;
      tayTruocDX = 36 * dir;
      tayTruocDY = 6;
      taySauDX = -42 * dir;
      taySauDY = 10;
      break;
    case 'nhay_xoay_dap_dat':
      nhayY = -Math.abs(Math.sin(f * 0.22)) * 34;
      tayTruocDX = 44 * dir;
      tayTruocDY = -20;
      break;
    case 'dam_cuong_luc':
      nghiengThanX = 16 * dir;
      tayTruocDX = 60 * dir;
      tayTruocDY = -4 + Math.sin(f * 0.3) * 4;
      taySauDX = -18 * dir;
      taySauDY = 14;
      break;
    case 'chem_kiem_toan':
      nghiengThanX = 14 * dir;
      tayTruocDX = 56 * dir;
      tayTruocDY = -16 + Math.sin(f * 0.35) * 14;
      taySauDX = -26 * dir;
      taySauDY = 16;
      break;
    case 'ban_tia_nang_luong':
      nghiengThanX = 10 * dir;
      tayTruocDX = 58 * dir;
      tayTruocDY = -10;
      taySauDX = 36 * dir;
      taySauDY = -6;
      break;
    case 'do_don_khien':
      nghiengThanX = -8 * dir;
      tayTruocDX = 40 * dir;
      tayTruocDY = -12;
      taySauDX = -18 * dir;
      taySauDY = 12;
      break;
    case 'bi_danh_vang':
      nghiengThanX = -24 * dir;
      nhayY = -12;
      tayTruocDX = 22 * dir;
      tayTruocDY = -26;
      taySauDX = -34 * dir;
      taySauDY = -18;
      break;
    case 'dung_tho':
    default:
      tayTruocDY = 16 + lacTay * 0.35;
      taySauDY = 18 - lacTay * 0.35;
      break;
  }

  const hong: Diem2D = { x: 0, y: -86 + nhipTho * 0.5 + nhayY };
  const co: Diem2D = { x: nghiengThanX, y: -158 + nhipTho + nhayY };
  const dau: Diem2D = { x: nghiengThanX + 2 * dir, y: -186 + nhipTho + nhayY };

  const vaiPhai: Diem2D = { x: co.x + 12 * dir, y: co.y + 6 };
  const banTayPhai: Diem2D = {
    x: vaiPhai.x + tayTruocDX,
    y: vaiPhai.y + tayTruocDY,
  };
  const khuyuPhai: Diem2D = {
    x: (vaiPhai.x + banTayPhai.x) / 2 - 4 * dir,
    y: (vaiPhai.y + banTayPhai.y) / 2 + 10,
  };

  const vaiTrai: Diem2D = { x: co.x - 12 * dir, y: co.y + 6 };
  const banTayTrai: Diem2D = {
    x: vaiTrai.x + taySauDX,
    y: vaiTrai.y + taySauDY,
  };
  const khuyuTrai: Diem2D = {
    x: (vaiTrai.x + banTayTrai.x) / 2 - 4 * dir,
    y: (vaiTrai.y + banTayTrai.y) / 2 + 10,
  };

  const banChanPhai: Diem2D = {
    x: (20 + buocChan) * dir,
    y: nhayY * 0.4,
  };
  const goiPhai: Diem2D = {
    x: (hong.x + banChanPhai.x) / 2 + 6 * dir,
    y: (hong.y + banChanPhai.y) / 2 - 4,
  };

  const banChanTrai: Diem2D = {
    x: (-20 - buocChan) * dir,
    y: nhayY * 0.4,
  };
  const goiTrai: Diem2D = {
    x: (hong.x + banChanTrai.x) / 2 - 4 * dir,
    y: (hong.y + banChanTrai.y) / 2 - 4,
  };

  const diemCamVuKhi: Diem2D = {
    x: banTayPhai.x + 4 * dir,
    y: banTayPhai.y - 2,
  };

  return {
    hong,
    co,
    dau,
    vaiTrai,
    khuyuTrai,
    banTayTrai,
    vaiPhai,
    khuyuPhai,
    banTayPhai,
    goiTrai,
    banChanTrai,
    goiPhai,
    banChanPhai,
    diemCamVuKhi,
  };
}
