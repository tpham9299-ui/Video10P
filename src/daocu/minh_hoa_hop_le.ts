import type { MinhHoaToanData, MocThoiGianItem } from '../kieu_dai';

const HAM_DO_THI_HOP_LE = new Set([
  'parabol',
  'sin',
  'cos',
  'bac_ba',
  'mu',
  'tuyen_tinh',
]);

/**
 * Trich xuat danh sach buoc suy luan hop le (buoc1, buoc2, ...) tu thamSo JSON.
 * TUYET DOI KHONG fallback ve noi dung hardcode cua bat ky tap phim cu the nao.
 */
export function layDanhSachBuocSuyLuan(
  thamSo?: Record<string, number | string | number[] | string[]>,
): string[] {
  if (!thamSo || typeof thamSo !== 'object') {
    return [];
  }
  const mangBuoc = thamSo.buoc;
  if (Array.isArray(mangBuoc)) {
    const sach = mangBuoc
      .filter((v): v is string => typeof v === 'string' && v.trim().length > 0)
      .map((v) => v.trim());
    if (sach.length > 0) {
      return sach;
    }
  }
  const buocList: string[] = [];
  for (let i = 1; i <= 8; i++) {
    const val = thamSo[`buoc${i}`];
    if (typeof val === 'string' && val.trim().length > 0) {
      buocList.push(val.trim());
    }
  }
  return buocList;
}

/**
 * Loc danh sach moc thoi gian hop le tu JSON cua tap phim.
 * TUYET DOI KHONG fallback ve moc lich su hardcode.
 */
export function locMocThoiGianHopLe(
  mocThoiGian?: readonly MocThoiGianItem[],
): MocThoiGianItem[] {
  if (!Array.isArray(mocThoiGian)) {
    return [];
  }
  return mocThoiGian.filter(
    (m) =>
      Boolean(m) &&
      ((typeof m.nam === 'string' && m.nam.trim().length > 0) ||
        (typeof m.moTa === 'string' && m.moTa.trim().length > 0)),
  );
}

/**
 * Chia dong & tu co co chu cho mo ta moc thoi gian (CanhDongThoiGian):
 * - Giu gon toi da 3-4 dong tuy so moc (3..5 moc)
 * - TUYET DOI KHONG cat cut giua tu (nhu "...Leopol", "...một sự công")
 */
export function chiaDongMoTaTimeline(
  moTa: string,
  soMoc: number,
): { dong: string[]; fontSize: number; lineHeight: number } {
  const sach = String(moTa || '').replace(/\s+/g, ' ').trim();
  if (!sach) {
    return { dong: [], fontSize: 18, lineHeight: 1.3 };
  }

  const cot = Math.max(1, Math.min(6, Math.round(soMoc) || 3));
  // Chon co chu va so ky tu/dong phu hop be ngang cot tren man hinh 1920px (bang rong ~1650px)
  let fontSize = cot <= 3 ? 19 : cot === 4 ? 17 : 15;
  let maxKyTuDong = cot <= 3 ? 34 : cot === 4 ? 26 : 22;

  const bocDong = (chuoi: string, limit: number): string[] => {
    const cacTu = chuoi.split(' ');
    const kq: string[] = [];
    let hienTai = '';
    for (const tu of cacTu) {
      if (!hienTai) {
        hienTai = tu;
      } else if (hienTai.length + 1 + tu.length <= limit) {
        hienTai = `${hienTai} ${tu}`;
      } else {
        kq.push(hienTai);
        hienTai = tu;
      }
    }
    if (hienTai) {
      kq.push(hienTai);
    }
    return kq;
  };

  let dong = bocDong(sach, maxKyTuDong);
  // Neu > 4 dong, giam co chu nhe va tang be rong ky tu/dong de van nam gon <= 4 dong ma KHONG cat giua tu
  while (dong.length > 4 && fontSize > 12.5) {
    fontSize = Math.round((fontSize - 1.2) * 10) / 10;
    maxKyTuDong += 4;
    dong = bocDong(sach, maxKyTuDong);
  }

  return {
    dong,
    fontSize,
    lineHeight: fontSize <= 15 ? 1.24 : 1.3,
  };
}

/**
 * Kiem tra xem minhHoaToan co du du lieu tham so tu JSON de render dung noi dung tap phim hay khong.
 * Neu thieu du lieu -> tra ve false de render khung trong sach.
 */
export function coDuLieuMinhHoaHopLe(
  data?: MinhHoaToanData | null,
): boolean {
  if (!data || typeof data !== 'object') {
    return false;
  }
  const ts = data.thamSo;

  switch (data.loai) {
    case 'tam_giac_vuong': {
      const a = ts?.canhA;
      const b = ts?.canhB;
      return (
        typeof a === 'number' &&
        Number.isFinite(a) &&
        a > 0 &&
        typeof b === 'number' &&
        Number.isFinite(b) &&
        b > 0
      );
    }

    case 'truc_so_vo_ti': {
      const g = ts?.giaTri;
      const nhan = ts?.nhan;
      return (
        typeof g === 'number' &&
        Number.isFinite(g) &&
        typeof nhan === 'string' &&
        nhan.trim().length > 0
      );
    }

    case 'do_thi_ham_so': {
      const ham = ts?.ham;
      return typeof ham === 'string' && HAM_DO_THI_HOP_LE.has(ham.trim());
    }

    case 'hinh_hoc_chung_minh': {
      const a = ts?.canhA;
      const b = ts?.canhB;
      return (
        typeof a === 'number' &&
        Number.isFinite(a) &&
        a > 0 &&
        typeof b === 'number' &&
        Number.isFinite(b) &&
        b > 0
      );
    }

    case 'chuoi_suy_luan':
      return layDanhSachBuocSuyLuan(ts).length > 0;

    case 'tung_buoc':
      return Array.isArray(data.buocVe) && data.buocVe.length > 0;

    case 'so_do_anh_xa': {
      const trai = ts?.cotTrai;
      const phai = ts?.cotPhai;
      return (
        Array.isArray(trai) &&
        trai.length >= 2 &&
        Array.isArray(phai) &&
        phai.length >= 2
      );
    }

    case 'luoi_duong_cheo': {
      const hang = ts?.hang;
      return Array.isArray(hang) && hang.length >= 2;
    }

    case 'bieu_do_cot': {
      const nhan = ts?.nhan;
      const giaTri = ts?.giaTri;
      return (
        Array.isArray(nhan) &&
        nhan.length >= 2 &&
        Array.isArray(giaTri) &&
        giaTri.length >= 2
      );
    }

    default:
      return false;
  }
}
