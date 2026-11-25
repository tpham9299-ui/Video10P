import type {
  AnhSangMoiTruong,
  DoTuoiNhanVat,
  LoaiCoRau,
  LoaiKieuToc,
  LoaiTrangPhuc,
  NhanVatTrongCanh,
  TamKhungNhanVat,
  ThongTinNhanVat,
  TuTheNhanVat,
} from '../kieu_dai';
import { kepGiaTri } from '../xuong/duong_cong.ts';

export const MAU_MUC_TRUYEN_TRANH = '#1A1A1A';

export type ThamSoAnhSangNhanVat = {
  coPhuMau: boolean;
  /** Lop phu mau phang do mo thap (0.08..0.22) dong bo tong am/lanh/toi voi nen tranh */
  mauPhu: string;
  doMoPhu: number;
  /** Lop phu lam toi nhe khi doToi cao (khong dung filter nang) */
  mauToi: string;
  doMoToi: number;
  /** Vien sang mong theo huong nguon sang (rim light SVG phang) */
  mauVienSang: string;
  doMoVienSang: number;
  /** Mau & do dam bong tiep dat duoi chan */
  mauBongDat: string;
  heSoBongDat: number;
};

export type HoaTrangHieuLuc = {
  trangPhuc: LoaiTrangPhuc;
  kieuToc: LoaiKieuToc | null;
  coRau: LoaiCoRau;
  mauAoChinh: string;
  mauAoBong: string;
  mauAoSang: string;
  mauQuanChinh: string;
  mauQuanBong: string;
  tamKhung: TamKhungNhanVat;
};

export type ThongSoBongTiepDat = {
  rx: number;
  ry: number;
  opacity: number;
  fill: string;
};

/** Tach ma mau hex #RRGGBB (hoac #RGB) thanh [r, g, b] an toan */
export function tachMauHex(hex: string | undefined, macDinh = '#2563EB'): [number, number, number] {
  const s = (hex || '').trim().replace(/^#/, '');
  if (/^[0-9a-fA-F]{6}$/.test(s)) {
    return [
      parseInt(s.slice(0, 2), 16),
      parseInt(s.slice(2, 4), 16),
      parseInt(s.slice(4, 6), 16),
    ];
  }
  if (/^[0-9a-fA-F]{3}$/.test(s)) {
    return [
      parseInt(s[0] + s[0], 16),
      parseInt(s[1] + s[1], 16),
      parseInt(s[2] + s[2], 16),
    ];
  }
  if (hex !== macDinh) {
    return tachMauHex(macDinh, '#2563EB');
  }
  return [37, 99, 235];
}

function ghepMauHex(r: number, g: number, b: number): string {
  const k = (n: number) =>
    Math.max(0, Math.min(255, Math.round(n)))
      .toString(16)
      .padStart(2, '0')
      .toUpperCase();
  return `#${k(r)}${k(g)}${k(b)}`;
}

/** Lam toi mau hex theo he so (0..1) de tao mang do bong 2 sac do SVG phang */
export function lamToiMauHex(hex: string | undefined, heSo = 0.24): string {
  const [r, g, b] = tachMauHex(hex);
  const f = kepGiaTri(1 - heSo, 0.15, 1);
  return ghepMauHex(r * f, g * f, b * f);
}

/** Lam sang mau hex theo he so (0..1) cho vien sang / ve ao */
export function lamSangMauHex(hex: string | undefined, heSo = 0.22): string {
  const [r, g, b] = tachMauHex(hex);
  const f = kepGiaTri(heSo, 0, 0.85);
  return ghepMauHex(r + (255 - r) * f, g + (255 - g) * f, b + (255 - b) * f);
}

/**
 * Tinh lop phu dong bo anh sang moi truong len nhan vat (SVG phang do mo 0.08..0.22,
 * TUYET DOI KHONG dung hieu ung lam mo CSS hay SVG nang).
 */
export function tinhThamSoAnhSangNhanVat(
  anhSang?: AnhSangMoiTruong,
): ThamSoAnhSangNhanVat {
  if (!anhSang) {
    return {
      coPhuMau: false,
      mauPhu: '#000000',
      doMoPhu: 0,
      mauToi: '#0F172A',
      doMoToi: 0,
      mauVienSang: '#FFFBEB',
      doMoVienSang: 0,
      mauBongDat: '#111827',
      heSoBongDat: 1,
    };
  }

  const doToi = kepGiaTri(
    Number.isFinite(anhSang.doToi) ? anhSang.doToi : 0.25,
    0,
    1,
  );
  const loai = String(anhSang.loaiAnhSang || 'trung_tinh').toLowerCase();
  const mauAmHopLe = /^#[0-9a-fA-F]{3}([0-9a-fA-F]{3})?$/.test(
    (anhSang.mauAm || '').trim(),
  )
    ? anhSang.mauAm.trim()
    : '#F4D99B';

  if (loai === 'anh_nen') {
    const doMoPhu = Number(kepGiaTri(0.14 + doToi * 0.08, 0.08, 0.22).toFixed(3));
    return {
      coPhuMau: true,
      mauPhu: mauAmHopLe,
      doMoPhu,
      mauToi: '#2A160B',
      doMoToi: Number(kepGiaTri(doToi * 0.16, 0.06, 0.16).toFixed(3)),
      mauVienSang: '#FDE68A',
      doMoVienSang: 0.42,
      mauBongDat: '#1E1108',
      heSoBongDat: 1.12,
    };
  }

  if (loai === 'dem_lanh') {
    const doMoPhu = Number(kepGiaTri(0.14 + doToi * 0.08, 0.08, 0.22).toFixed(3));
    return {
      coPhuMau: true,
      mauPhu: '#1E3A8A',
      doMoPhu,
      mauToi: '#0B132B',
      doMoToi: Number(kepGiaTri(doToi * 0.18, 0.08, 0.18).toFixed(3)),
      mauVienSang: '#93C5FD',
      doMoVienSang: 0.34,
      mauBongDat: '#070C1A',
      heSoBongDat: 1.16,
    };
  }

  if (loai === 'hoang_hon') {
    const doMoPhu = Number(kepGiaTri(0.12 + doToi * 0.1, 0.08, 0.22).toFixed(3));
    return {
      coPhuMau: true,
      mauPhu: mauAmHopLe,
      doMoPhu,
      mauToi: '#3B1810',
      doMoToi: Number(kepGiaTri(doToi * 0.12, 0.03, 0.12).toFixed(3)),
      mauVienSang: '#FDBA74',
      doMoVienSang: 0.4,
      mauBongDat: '#2A1410',
      heSoBongDat: 1.08,
    };
  }

  if (loai === 'nang_am') {
    const doMoPhu = Number(kepGiaTri(0.09 + (1 - doToi) * 0.05, 0.08, 0.18).toFixed(3));
    return {
      coPhuMau: true,
      mauPhu: mauAmHopLe,
      doMoPhu,
      mauToi: '#1F1B16',
      doMoToi: Number(kepGiaTri(doToi * 0.08, 0, 0.08).toFixed(3)),
      mauVienSang: '#FEF9C3',
      doMoVienSang: 0.36,
      mauBongDat: '#1C1917',
      heSoBongDat: 1.05,
    };
  }

  // trung_tinh
  const doMoPhu = Number(kepGiaTri(0.08 + doToi * 0.08, 0.08, 0.2).toFixed(3));
  return {
    coPhuMau: true,
    mauPhu: mauAmHopLe,
    doMoPhu,
    mauToi: '#0F172A',
    doMoToi: Number(kepGiaTri(doToi * 0.1, 0, 0.12).toFixed(3)),
    mauVienSang: '#F8FAFC',
    doMoVienSang: 0.24,
    mauBongDat: '#0F172A',
    heSoBongDat: 1.0,
  };
}

/**
 * Giai trang phuc, kieu toc, co rau & bang mau 2 sac do tu thongTin + trangThai.
 * Tuong thich nguoc 100% voi kich ban v1/v2 khong khai bao trangPhuc/kieuToc/coRau.
 */
export function giaiTrangPhucHieuLuc(
  thongTin: ThongTinNhanVat,
  trangThai: NhanVatTrongCanh,
): HoaTrangHieuLuc {
  const tuThe: TuTheNhanVat = trangThai.tuThe ?? 'dung';
  let trangPhuc: LoaiTrangPhuc | undefined =
    trangThai.trangPhuc ?? thongTin.trangPhuc;

  if (!trangPhuc) {
    if (tuThe === 'mac_ao_khoac') {
      trangPhuc = 'ao_len_mua_dong';
    } else if (thongTin.phuKien === 'vong_nguyet_que') {
      trangPhuc = 'ao_choang_hy_lap';
    } else if (thongTin.phuKien === 'ao_choang') {
      trangPhuc = 'ao_choang_hoc_gia';
    } else if (thongTin.phuKien === 'toc_gia_17') {
      trangPhuc = 'ao_vest_co_dien';
    } else if (thongTin.phuKien === 'mu_tham_tu') {
      trangPhuc = 'ao_vest_co_dien';
    } else {
      trangPhuc = 'thuong_dan';
    }
  }

  const mauAoChinh =
    trangThai.mauAo ?? thongTin.mauAo ?? thongTin.mauChuDao ?? '#2563EB';
  const mauAoBong = lamToiMauHex(mauAoChinh, 0.26);
  const mauAoSang = lamSangMauHex(mauAoChinh, 0.24);

  const mauQuanChinh =
    trangPhuc === 'ao_choang_hy_lap'
      ? '#EDE4D3'
      : trangPhuc === 'ao_co_an_do'
        ? '#F3E8D2'
        : trangPhuc === 'quan_phuc_co'
          ? '#1E293B'
          : '#334155';
  const mauQuanBong = lamToiMauHex(mauQuanChinh, 0.24);

  const kieuToc: LoaiKieuToc | null =
    trangThai.kieuToc ?? thongTin.kieuToc ?? null;
  const coRau: LoaiCoRau = trangThai.coRau ?? thongTin.coRau ?? 'khong';
  const tamKhung: TamKhungNhanVat = trangThai.tamKhung ?? 'toan_canh';

  return {
    trangPhuc,
    kieuToc,
    coRau,
    mauAoChinh,
    mauAoBong,
    mauAoSang,
    mauQuanChinh,
    mauQuanBong,
    tamKhung,
  };
}

/** Tinh he so phong & dich doc cho tamKhung (toan_canh | ban_than | can_mat) */
export function tinhTiLeTamKhung(
  tamKhung?: TamKhungNhanVat,
): { heSoTiLe: number; dichY: number } {
  switch (tamKhung) {
    case 'ban_than':
      return { heSoTiLe: 1.24, dichY: 42 };
    case 'can_mat':
      return { heSoTiLe: 1.52, dichY: 112 };
    case 'toan_canh':
    default:
      return { heSoTiLe: 1, dichY: 0 };
  }
}

/**
 * Tinh bong tiep dat (ground shadow) elip ban trong suot duoi chan nhan vat,
 * tu co gian muot khi nhay (doCaoBay) va khi buoc di (doRongBuocChan).
 */
export function tinhBongTiepDat(
  doCaoBay: number,
  doTuoi: DoTuoiNhanVat,
  tuThe: TuTheNhanVat,
  doRongBuocChan: number,
  anhSang?: AnhSangMoiTruong,
): ThongSoBongTiepDat {
  const bay = Math.max(0, Number.isFinite(doCaoBay) ? doCaoBay : 0);
  const buoc = kepGiaTri(
    Math.abs(Number.isFinite(doRongBuocChan) ? doRongBuocChan : 0),
    0,
    90,
  );
  const heSoBay = kepGiaTri(1 - bay / 125, 0.34, 1.06);
  const rxGoc =
    doTuoi === 'so_sinh'
      ? 58
      : tuThe === 'nam_giuong'
        ? 78
        : tuThe === 'ngoi_ban'
          ? 52
          : 44 + buoc * 0.24;
  const ryGoc =
    doTuoi === 'so_sinh' ? 11 : tuThe === 'nam_giuong' ? 12 : 10.5;
  const thamSoAs = tinhThamSoAnhSangNhanVat(anhSang);
  const opacity = kepGiaTri(
    0.29 * (1 - bay / 145) * thamSoAs.heSoBongDat,
    0.07,
    0.4,
  );

  return {
    rx: Number((rxGoc * heSoBay).toFixed(2)),
    ry: Number((ryGoc * heSoBay).toFixed(2)),
    opacity: Number(opacity.toFixed(3)),
    fill: thamSoAs.mauBongDat,
  };
}
