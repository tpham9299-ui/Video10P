import type { HuongNhanVat, LoaiHanhDong } from '../kieu_dai';
import { tinhGocKhopDongTac } from './dong_tac.ts';
import { baoToanCoGian, kepGiaTri } from './duong_cong.ts';

export type Diem2D = {
  x: number;
  y: number;
};

export type DoTrePhuKien = {
  dx: number;
  dy: number;
  gocTre: number;
  doRung: number;
};

export type TuyChonKhungXuong = {
  dangNoi?: boolean;
  vanTocDiChuyenX?: number;
};

export type TuTheKhungXuong = {
  hong: Diem2D;
  diemUonThan: Diem2D;
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
  diemCamVat: Diem2D;
  gocDau: number;
  gocCangTayPhai: number;
  doCaoNhay: number;
  dichNgangNoiBo: number;
  offsetX: number;
  offsetY: number;
  squashX: number;
  squashY: number;
  vanTocThan: Diem2D;
  doTrePhuKien: DoTrePhuKien;
  coVetBui: boolean;
  huongNhinX: number;
  huongNhinY: number;
};

// Chieu dai cac doan xuong co dinh (px) de giu ty le hoat hinh nhat quan
const HONG_Y_GOC = -88;
const DAI_THAN_GOC = 72;
const DAI_CO_DAU = 28;
const DAI_CANH_TAY_TREN = 31;
const DAI_CANG_TAY = 29;
const DAI_DUI = 46;
const DAI_CANG_CHAN = 45;

const DO_SANG_RAD = Math.PI / 180;

/** Buoc FK: tu khop cha + goc theo huong nhin (0 = thang xuong, + = ve truoc/len) + do dai */
function buocFK(cha: Diem2D, gocDo: number, doDai: number, dir: number): Diem2D {
  const rad = gocDo * DO_SANG_RAD;
  return {
    x: cha.x + Math.sin(rad) * doDai * dir,
    y: cha.y + Math.cos(rad) * doDai,
  };
}

/**
 * Giai IK 2 xuong cuc nhe khi ban chan bi cham mat dat (y > 0) de khong bao gio xuyen san
 * ma van giu nguyen do dai dui & cang chan, dau goi gap tu nhien ve truoc.
 */
function kepChanTrenMatDat(
  hong: Diem2D,
  goi: Diem2D,
  banChan: Diem2D,
  dir: number,
): { goi: Diem2D; banChan: Diem2D } {
  if (banChan.y <= 0) {
    return { goi, banChan };
  }

  const chanKep: Diem2D = { x: banChan.x, y: 0 };
  const dx = chanKep.x - hong.x;
  const dy = chanKep.y - hong.y;
  const khoangCach = Math.hypot(dx, dy);
  const tongDai = DAI_DUI + DAI_CANG_CHAN;

  if (khoangCach < 1e-3 || khoangCach >= tongDai - 0.5) {
    const tiLe = khoangCach > 1e-3 ? DAI_DUI / khoangCach : 0.5;
    return {
      goi: {
        x: hong.x + dx * tiLe + 3 * dir,
        y: Math.min(0, hong.y + dy * tiLe),
      },
      banChan: chanKep,
    };
  }

  // Dinh ly cosin tim diem goi gap ve phia truoc (+dir)
  const cosGoc = kepGiaTri(
    (DAI_DUI * DAI_DUI + khoangCach * khoangCach - DAI_CANG_CHAN * DAI_CANG_CHAN) /
      (2 * DAI_DUI * khoangCach),
    -1,
    1,
  );
  const a = DAI_DUI * cosGoc;
  const h = Math.sqrt(Math.max(0, DAI_DUI * DAI_DUI - a * a));
  const ux = dx / khoangCach;
  const uy = dy / khoangCach;
  // Phap tuyen huong ve phia truoc (+dir) khi dy > 0
  const px = uy * dir;
  const py = -ux * dir;

  const goiMoi: Diem2D = {
    x: hong.x + ux * a + px * h,
    y: Math.min(0, hong.y + uy * a + py * h),
  };

  return { goi: goiMoi, banChan: chanKep };
}

type KetQuaNoiBo = Omit<TuTheKhungXuong, 'vanTocThan' | 'doTrePhuKien'>;

/** Giai khung xuong FK phan cap tai dung mot thoi diem frame */
function giaiKhungXuongTaiFrame(
  hanhDong: LoaiHanhDong,
  frame: number,
  huong: HuongNhanVat,
  dangNoi: boolean,
): KetQuaNoiBo {
  const dir = huong === 'trai' ? -1 : 1;
  const p = tinhGocKhopDongTac(hanhDong, frame, dangNoi);
  const { squashX, squashY } = baoToanCoGian(p.squashY);

  const chieuDaiThan = DAI_THAN_GOC * squashY;

  // 1. Goc hong ban dau
  let hongX = p.offsetX * dir;
  let hongY = HONG_Y_GOC + p.offsetY;

  // 2. Giai chuoi chan FK: hong -> goi -> banChan
  const hongTam: Diem2D = { x: hongX, y: hongY };
  let goiPhai = buocFK(hongTam, p.duiPhaiGoc, DAI_DUI, dir);
  let banChanPhai = buocFK(goiPhai, p.duiPhaiGoc + p.goiPhaiGoc, DAI_CANG_CHAN, dir);

  let goiTrai = buocFK(hongTam, p.duiTraiGoc, DAI_DUI, dir);
  let banChanTrai = buocFK(goiTrai, p.duiTraiGoc + p.goiTraiGoc, DAI_CANG_CHAN, dir);

  // Tu kep ban chan sat mat dat (y = 0) khi dung/di de khong bi troi truot hay lo lung
  if (p.khoaMatDat) {
    const chanThapNhatY = Math.max(banChanPhai.y, banChanTrai.y);
    const buTruY = -chanThapNhatY;
    // Cho phep dich nhe than de ban chan cham san y=0 nhung van giu tu the ngoi/quy
    const buTruGioiHan = kepGiaTri(buTruY, -28, 18);
    hongY += buTruGioiHan;
    goiPhai = { x: goiPhai.x, y: goiPhai.y + buTruGioiHan };
    banChanPhai = { x: banChanPhai.x, y: banChanPhai.y + buTruGioiHan };
    goiTrai = { x: goiTrai.x, y: goiTrai.y + buTruGioiHan };
    banChanTrai = { x: banChanTrai.x, y: banChanTrai.y + buTruGioiHan };
  }

  const hong: Diem2D = { x: hongX, y: hongY };

  // Khong bao gio cho ban chan xuyen xuong duoi san y = 0
  const chanPhaiKep = kepChanTrenMatDat(hong, goiPhai, banChanPhai, dir);
  goiPhai = chanPhaiKep.goi;
  banChanPhai = chanPhaiKep.banChan;

  const chanTraiKep = kepChanTrenMatDat(hong, goiTrai, banChanTrai, dir);
  goiTrai = chanTraiKep.goi;
  banChanTrai = chanTraiKep.banChan;

  // 3. Cot song cong Quadratic Bezier: hong -> diemUonThan -> co
  const radThan = p.gocThan * DO_SANG_RAD;
  const co: Diem2D = {
    x: hong.x + Math.sin(radThan) * chieuDaiThan * dir,
    y: hong.y - Math.cos(radThan) * chieuDaiThan,
  };

  const tx = co.x - hong.x;
  const ty = co.y - hong.y;
  const daiThanThuc = Math.max(1, Math.hypot(tx, ty));
  // Phap tuyen vuong goc truc than huong ve truoc (+dir)
  const phapX = (-ty / daiThanThuc) * dir;
  const phapY = (tx / daiThanThuc) * dir;

  const diemUonThan: Diem2D = {
    x: (hong.x + co.x) * 0.5 + phapX * p.doCongThan * squashX,
    y: (hong.y + co.y) * 0.5 + phapY * p.doCongThan * squashX,
  };

  // 4. Dau giai theo FK tu co, bam theo do nghieng cot song
  const gocCoDauRad = (p.gocThan * 0.55 + p.gocDau * 0.3) * DO_SANG_RAD;
  const dau: Diem2D = {
    x: co.x + Math.sin(gocCoDauRad) * DAI_CO_DAU * dir,
    y: co.y - Math.cos(gocCoDauRad) * DAI_CO_DAU,
  };

  // 5. Chuoi canh tay FK: hong -> co -> vai -> khuyu -> banTay -> diemCamVat
  const rongVai = 10.5 * squashX;
  const vaiPhai: Diem2D = {
    x: co.x + rongVai * dir,
    y: co.y + 6 - p.nhunVai,
  };
  const vaiTrai: Diem2D = {
    x: co.x - rongVai * dir,
    y: co.y + 6 - p.nhunVai,
  };

  const gocCanhTayPhai = p.gocThan * 0.35 + p.vaiPhaiGoc;
  const gocCangTayPhai = gocCanhTayPhai + p.khuyuPhaiGoc;
  const khuyuPhai = buocFK(vaiPhai, gocCanhTayPhai, DAI_CANH_TAY_TREN, dir);
  const banTayPhai = buocFK(khuyuPhai, gocCangTayPhai, DAI_CANG_TAY, dir);

  const gocCanhTayTrai = p.gocThan * 0.35 + p.vaiTraiGoc;
  const gocCangTayTrai = gocCanhTayTrai + p.khuyuTraiGoc;
  const khuyuTrai = buocFK(vaiTrai, gocCanhTayTrai, DAI_CANH_TAY_TREN, dir);
  const banTayTrai = buocFK(khuyuTrai, gocCangTayTrai, DAI_CANG_TAY, dir);

  const diemCamVat = buocFK(banTayPhai, gocCangTayPhai, 4.5, dir);

  return {
    hong,
    diemUonThan,
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
    diemCamVat,
    gocDau: p.gocDau * dir,
    gocCangTayPhai: gocCangTayPhai * dir,
    doCaoNhay: Math.max(0, -p.nhayY),
    dichNgangNoiBo: p.dichNgangNoiBo,
    offsetX: hong.x,
    offsetY: hong.y - HONG_Y_GOC,
    squashX,
    squashY,
    coVetBui: p.coVetBui,
    huongNhinX: p.huongNhinX,
    huongNhinY: p.huongNhinY,
  };
}

/**
 * Bo giai xuong khop FK mem phan cap theo goc khop + chuyen dong thu cap co do tre (v0.4).
 * He toa do cuc bo: (0, 0) la mat dat giua hai ban chan, truc Y am huong len tren.
 * Tat dinh 100% theo frameCucBo, khong bao gio tra ve NaN hoac Infinity.
 */
export function tinhKhungXuongCoBan(
  hanhDong: LoaiHanhDong,
  frameCucBo: number,
  huong: HuongNhanVat,
  tuyChon?: TuyChonKhungXuong,
): TuTheKhungXuong {
  const f = Number.isFinite(frameCucBo) ? frameCucBo : 0;
  const dangNoi = Boolean(tuyChon?.dangNoi);
  const vanTocNgoaiX = Number.isFinite(tuyChon?.vanTocDiChuyenX)
    ? (tuyChon?.vanTocDiChuyenX ?? 0)
    : 0;

  const hienTai = giaiKhungXuongTaiFrame(hanhDong, f, huong, dangNoi);
  const truoc1 = giaiKhungXuongTaiFrame(hanhDong, f - 1, huong, dangNoi);
  const tre3 = giaiKhungXuongTaiFrame(hanhDong, f - 3, huong, dangNoi);

  const vanTocThan: Diem2D = {
    x:
      hienTai.co.x +
      hienTai.dichNgangNoiBo -
      (truoc1.co.x + truoc1.dichNgangNoiBo) +
      vanTocNgoaiX,
    y: hienTai.co.y - truoc1.co.y,
  };

  // Do tre phu kien (frame - 3) + quan tinh di chuyen ngang
  const doTrePhuKien: DoTrePhuKien = {
    dx: kepGiaTri(
      tre3.co.x +
        tre3.dichNgangNoiBo -
        (hienTai.co.x + hienTai.dichNgangNoiBo) -
        vanTocNgoaiX * 3,
      -42,
      42,
    ),
    dy: kepGiaTri(tre3.co.y - hienTai.co.y, -32, 32),
    gocTre: kepGiaTri(tre3.gocDau - hienTai.gocDau, -24, 24),
    doRung: Math.sin((f - 3) * 0.22),
  };

  return {
    ...hienTai,
    vanTocThan,
    doTrePhuKien,
  };
}
