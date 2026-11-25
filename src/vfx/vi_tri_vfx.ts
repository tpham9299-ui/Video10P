import type { HieuUngHoatHinhItem, NhanVatTrongCanh } from '../kieu_dai';
import { kepGiaTri } from '../xuong/duong_cong.ts';

/**
 * Uoc tinh chinh xac toa do Y tam dau nhan vat tren khung 1920x1080 theo doTuoi, tuThe & tiLe.
 */
export function tinhDauNhanVatY(
  nv: Pick<NhanVatTrongCanh, 'y' | 'tiLe' | 'doTuoi' | 'tuThe'>,
  tiLeCanh = 1.25,
): number {
  const tiLeTong = Math.max(0.4, (nv.tiLe ?? 1) * tiLeCanh);
  let headLocalY = -170;
  if (nv.doTuoi === 'so_sinh') {
    headLocalY = -62;
  } else if (nv.tuThe === 'ngoi_ban') {
    headLocalY = -136;
  } else if (nv.tuThe === 'nam_giuong') {
    headLocalY = -130;
  } else if (nv.doTuoi === 'thieu_nien') {
    headLocalY = -142;
  } else if (nv.doTuoi === 'gia') {
    headLocalY = -162;
  }
  return nv.y + headLocalY * tiLeTong;
}

function timNhanVatNeoGanNhat(
  item: HieuUngHoatHinhItem,
  ds: readonly NhanVatTrongCanh[],
): NhanVatTrongCanh {
  let nvMucTieu = ds[0];
  let diemTot = Infinity;
  for (const nv of ds) {
    const dist = Math.abs(nv.x - item.x) - (nv.dangNoi ? 90 : 0);
    if (dist < diemTot) {
      diemTot = dist;
      nvMucTieu = nv;
    }
  }
  return nvMucTieu;
}

/**
 * Tinh toa do hien thi an toan cho cac VFX hoat hinh:
 * - bong_den_nay_so / bong_den_y_tuong: luon noi o phia tren dau nhan vat (headY - 75), KHONG bao gio moc giua nguc/bung.
 * - mo_hoi_lon: ben thai duong phia sau/ben dau nhan vat (headY - 10).
 * - khoi_boc_tai / mat_xoan_oc / tia_toc_do: neo chuan quanh tam dau (headY - 4).
 * - cham_hoi_nay: nay phia tren dau nhan vat (headY - 72).
 * - nhan_chu_hai_huoc ("Ua khoan da?!"): tu dong day ra khoi vung mat/than nhan vat (dac biet khi ngoi ban).
 */
export function tinhToaDoHieuUngAnToan(
  item: HieuUngHoatHinhItem,
  nhanVat?: readonly NhanVatTrongCanh[],
  tiLeCanh = 1.25,
): { x: number; y: number } {
  const ds = nhanVat ?? [];
  if (ds.length === 0) {
    return { x: item.x, y: item.y };
  }

  if (item.loai === 'bong_den_nay_so' || item.loai === 'bong_den_y_tuong') {
    const nvMucTieu = timNhanVatNeoGanNhat(item, ds);
    const headY = tinhDauNhanVatY(nvMucTieu, tiLeCanh);
    return {
      x: kepGiaTri(nvMucTieu.x, 120, 1800),
      y: kepGiaTri(Math.round(headY - 75), 115, 680),
    };
  }

  if (item.loai === 'cham_hoi_nay') {
    const nvMucTieu = timNhanVatNeoGanNhat(item, ds);
    const headY = tinhDauNhanVatY(nvMucTieu, tiLeCanh);
    return {
      x: kepGiaTri(nvMucTieu.x, 120, 1800),
      y: kepGiaTri(Math.round(headY - 72), 110, 680),
    };
  }

  if (item.loai === 'mo_hoi_lon') {
    const nvMucTieu = timNhanVatNeoGanNhat(item, ds);
    const headY = tinhDauNhanVatY(nvMucTieu, tiLeCanh);
    const dir = nvMucTieu.huong === 'trai' ? -1 : 1;
    const tiLeTong = Math.max(0.5, (nvMucTieu.tiLe ?? 1) * tiLeCanh);
    return {
      x: kepGiaTri(Math.round(nvMucTieu.x - 32 * dir * tiLeTong), 90, 1830),
      y: kepGiaTri(Math.round(headY - 12), 110, 720),
    };
  }

  if (
    item.loai === 'khoi_boc_tai' ||
    item.loai === 'mat_xoan_oc' ||
    item.loai === 'tia_toc_do'
  ) {
    const nvMucTieu = timNhanVatNeoGanNhat(item, ds);
    const headY = tinhDauNhanVatY(nvMucTieu, tiLeCanh);
    return {
      x: kepGiaTri(nvMucTieu.x, 120, 1800),
      y: kepGiaTri(Math.round(headY - 4), 110, 720),
    };
  }

  if (item.loai === 'nhan_chu_hai_huoc') {
    const chu = item.chuHienThi ?? 'Ủa khoan đã?!';
    const tiLe = item.tiLe ?? 1;
    const nuaRong = (Math.max(190, Math.min(430, chu.length * 17 + 62)) / 2) * tiLe;
    const nuaCao = 34 * tiLe;

    let x = item.x;
    let y = item.y;

    for (const nv of ds) {
      const tiLeTong = Math.max(0.5, (nv.tiLe ?? 1) * tiLeCanh);
      const headY = tinhDauNhanVatY(nv, tiLeCanh);
      const nvLeft = nv.x - (nv.tuThe === 'ngoi_ban' ? 125 : 90) * tiLeTong;
      const nvRight = nv.x + (nv.tuThe === 'ngoi_ban' ? 125 : 90) * tiLeTong;
      const nvTop = headY - 46;
      const nvBottom = nv.y + 18;

      const chongNgang = x + nuaRong > nvLeft && x - nuaRong < nvRight;
      const chongDoc = y + nuaCao > nvTop && y - nuaCao < nvBottom;

      if (chongNgang && chongDoc) {
        // Uu tien day len phia tren dau nhan vat (cach dinh dau an toan)
        const yTrenDau = Math.round(headY - 105 - nuaCao * 0.4);
        if (yTrenDau >= 125) {
          y = yTrenDau;
        } else {
          // Neu khong du khong gian tren dau -> day sang khoang trong ngang ben trai/phai
          const benPhaiX = nvRight + nuaRong + 32;
          const benTraiX = nvLeft - nuaRong - 32;
          if (benPhaiX + nuaRong <= 1860) {
            x = benPhaiX;
          } else if (benTraiX - nuaRong >= 60) {
            x = benTraiX;
          } else {
            y = 125;
          }
        }
      }
    }

    return {
      x: kepGiaTri(x, nuaRong + 40, 1880 - nuaRong),
      y: kepGiaTri(y, 118, 860),
    };
  }

  return { x: item.x, y: item.y };
}
