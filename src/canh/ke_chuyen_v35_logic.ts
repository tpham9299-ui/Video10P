import { easeInOutCubic, easeOutBack, kepGiaTri } from '../xuong/duong_cong';

export type Diem2D = {
  x: number;
  y: number;
};

export type TrangThaiHanhTrinh = {
  tienDo: number;
  viTri: Diem2D;
  gocHuongDeg: number;
  daDenNoi: boolean;
};

/**
 * Toa do tuyen duong cong Bezier bac 2 chuan tren khung 1920x1080 cho CanhBanDoHanhTrinh:
 * P0 (diemDi ben trai duoi) -> P1 (dinh cong giua) -> P2 (diemDen ben phai tren).
 */
export const TOA_DO_BAN_DO_MAC_DINH = {
  p0: { x: 360, y: 690 } as Diem2D,
  p1: { x: 960, y: 260 } as Diem2D,
  p2: { x: 1560, y: 420 } as Diem2D,
};

/** Tinh diem & goc tiep tuyen tat dinh 100% tren duong Bezier bac 2 theo frame */
export function tinhTrangThaiHanhTrinh(
  frame: number,
  thoiLuongCanh: number,
  p0: Diem2D = TOA_DO_BAN_DO_MAC_DINH.p0,
  p1: Diem2D = TOA_DO_BAN_DO_MAC_DINH.p1,
  p2: Diem2D = TOA_DO_BAN_DO_MAC_DINH.p2,
): TrangThaiHanhTrinh {
  const tong = Math.max(12, thoiLuongCanh);
  const fBatDau = Math.min(10, Math.floor(tong * 0.08));
  const fKetThuc = Math.max(fBatDau + 10, Math.floor(tong * 0.86));
  const rawT = kepGiaTri((frame - fBatDau) / Math.max(1, fKetThuc - fBatDau), 0, 1);
  const t = easeInOutCubic(rawT);

  const u = 1 - t;
  const x = u * u * p0.x + 2 * u * t * p1.x + t * t * p2.x;
  const y = u * u * p0.y + 2 * u * t * p1.y + t * t * p2.y;

  // Dao ham tiep tuyen de xoay nhe bieu tuong tau/thu theo huong di chuyen
  const dx = 2 * u * (p1.x - p0.x) + 2 * t * (p2.x - p1.x);
  const dy = 2 * u * (p1.y - p0.y) + 2 * t * (p2.y - p1.y);
  const gocRaw = (Math.atan2(dy, dx) * 180) / Math.PI;
  const gocHuongDeg = kepGiaTri(gocRaw, -32, 32);

  return {
    tienDo: Number(t.toFixed(4)),
    viTri: { x: Number(x.toFixed(2)), y: Number(y.toFixed(2)) },
    gocHuongDeg: Number(gocHuongDeg.toFixed(2)),
    daDenNoi: rawT >= 0.96,
  };
}

export type BienDoiBaoChiCo = {
  scale: number;
  xoayDeg: number;
  opacity: number;
  hienTieuDePhu: boolean;
};

/**
 * Hieu ung to bao giay co xoay phong vao man hinh tat dinh 100% (v3.5):
 * - 0..18 frame: xoay 1 vong (-360deg -> -2.2deg) & phong 0.16 -> 1.0 voi easeOutBack
 * - >18 frame: giu nghieng bao dien anh (-2.2deg) kem nhip zoom cham 1.0 -> 1.03
 */
export function tinhBienDoiBaoChiCo(
  frame: number,
  thoiLuongCanh: number,
): BienDoiBaoChiCo {
  const fVao = 18;
  const tong = Math.max(24, thoiLuongCanh);
  if (frame < fVao) {
    const p = kepGiaTri(frame / fVao, 0, 1);
    const e = easeOutBack(p);
    return {
      scale: Number((0.16 + 0.84 * e).toFixed(4)),
      xoayDeg: Number((-360 + 357.8 * kepGiaTri(p * 1.04, 0, 1)).toFixed(2)),
      opacity: Number(kepGiaTri(p * 1.4, 0, 1).toFixed(3)),
      hienTieuDePhu: false,
    };
  }
  const pSau = kepGiaTri((frame - fVao) / Math.max(1, tong - fVao), 0, 1);
  return {
    scale: Number((1.0 + pSau * 0.032).toFixed(4)),
    xoayDeg: Number((-2.2 + Math.sin((frame - fVao) * 0.04) * 0.5).toFixed(2)),
    opacity: 1,
    hienTieuDePhu: frame >= fVao + 4,
  };
}

export type TrangThaiPhanUngCam = {
  zoom: number;
  nhapTraTienDo: number;
  nhuongMayOffsetY: number;
  hienTemChu: boolean;
  temScale: number;
};

/** Tinh dong tac can mat cho CanhPhanUngCam (1.5-2.5s = 45-75 frame, tat dinh 100%) */
export function tinhTrangThaiPhanUngCam(
  frame: number,
  thoiLuongCanh: number,
): TrangThaiPhanUngCam {
  const tong = Math.max(20, thoiLuongCanh);
  const p = kepGiaTri(frame / tong, 0, 1);
  // Zoom nhe nhanh vao mat de tang nhip hai (1.92 -> 2.12)
  const zoom = 1.92 + easeInOutCubic(kepGiaTri(frame / 14, 0, 1)) * 0.14 + p * 0.06;
  // Nhip nang tach tra len mieng roi ha nhe
  const nhapTraTienDo = kepGiaTri(Math.sin(p * Math.PI), 0, 1);
  // Nhuong may len roi giu nguyen
  const nhuongMayOffsetY = -10 * easeOutBack(kepGiaTri((frame - 6) / 10, 0, 1));
  const hienTemChu = frame >= 8;
  const temScale = hienTemChu
    ? Number(kepGiaTri(easeOutBack(kepGiaTri((frame - 8) / 10, 0, 1)), 0.1, 1.15).toFixed(3))
    : 0;

  return {
    zoom: Number(zoom.toFixed(3)),
    nhapTraTienDo: Number(nhapTraTienDo.toFixed(3)),
    nhuongMayOffsetY: Number(nhuongMayOffsetY.toFixed(2)),
    hienTemChu,
    temScale,
  };
}

/**
 * Vung an toan chuan YouTube End-Screen (khung 1920x1080):
 * - 2 khung video 16:9 trai & phai dat o vung giua-tren (khong cham phu de day y>900, chua khoang giua cho Mascot)
 */
export const VUNG_END_SCREEN_YOUTUBE = {
  khungTrai: { x: 88, y: 318, width: 544, height: 306 },
  khungPhai: { x: 1288, y: 318, width: 544, height: 306 },
  vungMascotGiua: { x: 960, y: 830 },
} as const;
