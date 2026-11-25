import type {
  DoTuoiNhanVat,
  HuongNhanVat,
  LoaiHanhDong,
  TuTheNhanVat,
} from '../kieu_dai';
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
  /** Bien the do tuoi hinh the nhan vat (v2.0) */
  doTuoi?: DoTuoiNhanVat;
  /** Tu the boi canh cua nhan vat (v2.0) */
  tuThe?: TuTheNhanVat;
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

// Gioi han giai phau an toan cho goc xoay dau & truc co (do) — ngan dau bi lat nguoc hoac lech truc
export const GIOI_HAN_GOC_DAU_MIN = -18;
export const GIOI_HAN_GOC_DAU_MAX = 22;
export const GIOI_HAN_GOC_CO_MIN = -16;
export const GIOI_HAN_GOC_CO_MAX = 20;
export const GIOI_HAN_LECH_DAU_CO = 16;

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
  doTuoi: DoTuoiNhanVat = 'truong_thanh',
  tuThe: TuTheNhanVat = 'dung',
): KetQuaNoiBo {
  const dir = huong === 'trai' ? -1 : 1;
  const pGoc = tinhGocKhopDongTac(hanhDong, frame, dangNoi);
  const p = { ...pGoc };

  // Bien the ty le chieu dai xuong theo doTuoi (v2.0)
  const tiLeThan =
    doTuoi === 'so_sinh'
      ? 0.48
      : doTuoi === 'thieu_nien'
        ? 0.82
        : doTuoi === 'gia'
          ? 0.94
          : 1.0;
  const tiLeChi =
    doTuoi === 'so_sinh'
      ? 0.45
      : doTuoi === 'thieu_nien'
        ? 0.8
        : doTuoi === 'gia'
          ? 0.95
          : 1.0;

  if (doTuoi === 'gia') {
    p.gocThan = kepGiaTri(p.gocThan + 6, -10, 26);
    p.doCongThan -= 4.5;
  } else if (doTuoi === 'thieu_nien') {
    // Tre trung, nhun nang dong hon nhe
    p.offsetY += Math.sin(frame * 0.22) * 1.4;
  } else if (doTuoi === 'so_sinh') {
    // Em be nam gon trong noi, dung dua nhe
    p.offsetY = 18 + Math.sin(frame * 0.09) * 1.8;
    p.gocThan = Math.sin(frame * 0.09) * 3;
    p.gocDau = Math.sin(frame * 0.11) * 4;
    p.vaiPhaiGoc = 42 + Math.sin(frame * 0.24) * 14;
    p.khuyuPhaiGoc = 44 + Math.cos(frame * 0.24) * 10;
    p.vaiTraiGoc = -42 - Math.sin(frame * 0.24 + 0.6) * 14;
    p.khuyuTraiGoc = 42 + Math.cos(frame * 0.24 + 0.6) * 10;
    p.duiPhaiGoc = 22;
    p.goiPhaiGoc = -30;
    p.duiTraiGoc = -22;
    p.goiTraiGoc = -28;
    p.khoaMatDat = false;
  }

  // Dieu chinh khung xuong theo tuThe boi canh (v2.0)
  if (doTuoi !== 'so_sinh') {
    if (tuThe === 'ngoi_ban') {
      p.offsetY = 34 + Math.sin(frame * 0.11) * 1.1;
      p.duiPhaiGoc = 76;
      p.goiPhaiGoc = -76;
      p.duiTraiGoc = 66;
      p.goiTraiGoc = -70;
      p.gocThan = kepGiaTri(p.gocThan * 0.5 + 11, -6, 20);
      p.doCongThan = -6;
      if (hanhDong === 'dung_tho' || hanhDong === 'ngoi_doc_sach') {
        const viet = Math.sin(frame * 0.34);
        p.vaiPhaiGoc = 56 + viet * 5;
        p.khuyuPhaiGoc = 44 + Math.cos(frame * 0.34) * 6;
        p.vaiTraiGoc = 38;
        p.khuyuTraiGoc = 56;
        p.gocDau = kepGiaTri(12 + Math.sin(frame * 0.12) * 2.5, -18, 22);
      }
    } else if (tuThe === 'nam_giuong') {
      // Tua lung em ai len goi cao tren giuong, chan duoi thang duoi chan (giu ro mat & lip-sync)
      p.offsetY = 40 + Math.sin(frame * 0.08) * 1.4;
      p.gocThan = -14 + Math.sin(frame * 0.08) * 1.5;
      p.doCongThan = 5;
      p.duiPhaiGoc = 86;
      p.goiPhaiGoc = -14;
      p.duiTraiGoc = 78;
      p.goiTraiGoc = -18;
      p.khoaMatDat = false;
      if (hanhDong === 'dung_tho') {
        p.vaiPhaiGoc = 34 + Math.sin(frame * 0.09) * 3;
        p.khuyuPhaiGoc = 38;
        p.vaiTraiGoc = 18;
        p.khuyuTraiGoc = 42;
      }
    } else if (tuThe === 'om_em_be') {
      // Vong tay om ru em be diu dang truoc nguc
      const ru = Math.sin(frame * 0.12);
      p.gocThan = 4 + ru * 2.5;
      p.gocDau = kepGiaTri(10 + ru * 2.2, -18, 22);
      p.vaiPhaiGoc = 48 + ru * 4;
      p.khuyuPhaiGoc = 66 + ru * 3;
      p.vaiTraiGoc = 32 - ru * 3;
      p.khuyuTraiGoc = 72 - ru * 3;
    } else if (tuThe === 'mac_ao_khoac') {
      // Hoi co vai giu am mua dong nhung van giu nguyen dong tac chinh
      p.nhunVai += 1.6;
    }
  }

  const { squashX, squashY } = baoToanCoGian(p.squashY);

  const daiThanBase = DAI_THAN_GOC * tiLeThan;
  const daiCanhTayTren = DAI_CANH_TAY_TREN * tiLeChi;
  const daiCangTay = DAI_CANG_TAY * tiLeChi;
  const daiDui = DAI_DUI * tiLeChi;
  const daiCangChan = DAI_CANG_CHAN * tiLeChi;
  const hongYGoc = HONG_Y_GOC * tiLeChi;

  const chieuDaiThan = daiThanBase * squashY;

  // 1. Goc hong ban dau
  let hongX = p.offsetX * dir;
  let hongY = hongYGoc + p.offsetY;

  // 2. Giai chuoi chan FK: hong -> goi -> banChan
  const hongTam: Diem2D = { x: hongX, y: hongY };
  let goiPhai = buocFK(hongTam, p.duiPhaiGoc, daiDui, dir);
  let banChanPhai = buocFK(goiPhai, p.duiPhaiGoc + p.goiPhaiGoc, daiCangChan, dir);

  let goiTrai = buocFK(hongTam, p.duiTraiGoc, daiDui, dir);
  let banChanTrai = buocFK(goiTrai, p.duiTraiGoc + p.goiTraiGoc, daiCangChan, dir);

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

  // Khong bao gio cho ban chan xuyen xuong duoi san y = 0 (tru truong hop nam_giuong/so_sinh co san giuong/noi rieng)
  if (doTuoi !== 'so_sinh' && tuThe !== 'nam_giuong') {
    const chanPhaiKep = kepChanTrenMatDat(hong, goiPhai, banChanPhai, dir);
    goiPhai = chanPhaiKep.goi;
    banChanPhai = chanPhaiKep.banChan;

    const chanTraiKep = kepChanTrenMatDat(hong, goiTrai, banChanTrai, dir);
    goiTrai = chanTraiKep.goi;
    banChanTrai = chanTraiKep.banChan;
  }

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

  // 4. Dau giai theo FK tu co, kep cung gioi han goc xoay dau/co de khong bi lat nguoc hay lech truc
  const gocDauCoBan = kepGiaTri(
    p.gocDau,
    GIOI_HAN_GOC_DAU_MIN,
    GIOI_HAN_GOC_DAU_MAX,
  );
  const gocCoDauDo = kepGiaTri(
    p.gocThan * 0.45 + gocDauCoBan * 0.25,
    GIOI_HAN_GOC_CO_MIN,
    GIOI_HAN_GOC_CO_MAX,
  );
  const gocDauAnToan = kepGiaTri(
    gocDauCoBan,
    Math.max(GIOI_HAN_GOC_DAU_MIN, gocCoDauDo - GIOI_HAN_LECH_DAU_CO),
    Math.min(GIOI_HAN_GOC_DAU_MAX, gocCoDauDo + GIOI_HAN_LECH_DAU_CO),
  );
  const gocCoDauRad = gocCoDauDo * DO_SANG_RAD;
  const dau: Diem2D = {
    x: co.x + Math.sin(gocCoDauRad) * DAI_CO_DAU * dir,
    y: co.y - Math.cos(gocCoDauRad) * DAI_CO_DAU,
  };

  // 5. Chuoi canh tay FK: hong -> co -> vai -> khuyu -> banTay -> diemCamVat
  const rongVai = 10.5 * tiLeThan * squashX;
  const vaiPhai: Diem2D = {
    x: co.x + rongVai * dir,
    y: co.y + 6 * tiLeThan - p.nhunVai,
  };
  const vaiTrai: Diem2D = {
    x: co.x - rongVai * dir,
    y: co.y + 6 * tiLeThan - p.nhunVai,
  };

  const gocCanhTayPhai = p.gocThan * 0.35 + p.vaiPhaiGoc;
  const gocCangTayPhai = gocCanhTayPhai + p.khuyuPhaiGoc;
  const khuyuPhai = buocFK(vaiPhai, gocCanhTayPhai, daiCanhTayTren, dir);
  const banTayPhai = buocFK(khuyuPhai, gocCangTayPhai, daiCangTay, dir);

  const gocCanhTayTrai = p.gocThan * 0.35 + p.vaiTraiGoc;
  const gocCangTayTrai = gocCanhTayTrai + p.khuyuTraiGoc;
  const khuyuTrai = buocFK(vaiTrai, gocCanhTayTrai, daiCanhTayTren, dir);
  const banTayTrai = buocFK(khuyuTrai, gocCangTayTrai, daiCangTay, dir);

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
    gocDau: gocDauAnToan * dir,
    gocCangTayPhai: gocCangTayPhai * dir,
    doCaoNhay: Math.max(0, -p.nhayY),
    dichNgangNoiBo: p.dichNgangNoiBo,
    offsetX: hong.x,
    offsetY: hong.y - hongYGoc,
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
  const doTuoi = tuyChon?.doTuoi ?? 'truong_thanh';
  const tuThe = tuyChon?.tuThe ?? 'dung';
  const vanTocNgoaiX = Number.isFinite(tuyChon?.vanTocDiChuyenX)
    ? (tuyChon?.vanTocDiChuyenX ?? 0)
    : 0;

  const hienTai = giaiKhungXuongTaiFrame(hanhDong, f, huong, dangNoi, doTuoi, tuThe);
  const truoc1 = giaiKhungXuongTaiFrame(hanhDong, f - 1, huong, dangNoi, doTuoi, tuThe);
  const tre3 = giaiKhungXuongTaiFrame(hanhDong, f - 3, huong, dangNoi, doTuoi, tuThe);

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
    gocTre: kepGiaTri(tre3.gocDau - hienTai.gocDau, -14, 14),
    doRung: Math.sin((f - 3) * 0.22),
  };

  return {
    ...hienTai,
    vanTocThan,
    doTrePhuKien,
  };
}
