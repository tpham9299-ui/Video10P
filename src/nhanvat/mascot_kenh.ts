import type { CauHinhMascotKenh, ThongTinNhanVat } from '../kieu_dai';

export const ID_MASCOT_KENH = 'mascot_pi';

/**
 * Ho so nhan vat dan chuyen co dinh (Mascot kenh v3.5):
 * De dang tuy chinh ten, trang phuc, kieu toc, mau ao trong du_lieu_render.json (`mascotKenh`)
 * hoac bien moi truong `.env` (MASCOT_TEN, MASCOT_TRANG_PHUC, MASCOT_KIEU_TOC, MASCOT_MAU_AO).
 * Xuat hien o 15s Cold Open mo man, canh tuong tac do khan gia va 15s End-Screen cuoi video.
 */
export const MASCOT_KENH_MAC_DINH: ThongTinNhanVat = {
  id: ID_MASCOT_KENH,
  ten: 'Giáo Sư Pi',
  mauThan: '#1A1A1A',
  mauChuDao: '#0284C7',
  mauDa: '#FFFDF7',
  phuKien: 'kinh_tron',
  doTuoi: 'truong_thanh',
  trangPhuc: 'ao_choang_hoc_gia',
  kieuToc: 'mu_noi',
  coRau: 'khong',
  mauAo: '#0284C7',
};

/** Hop nhat cau hinh tuy chinh cua nguoi dung voi ho so Mascot mac dinh */
export function layHoSoMascotKenh(
  cauHinh?: CauHinhMascotKenh,
): ThongTinNhanVat | null {
  if (cauHinh?.batMascot === false) {
    return null;
  }
  if (!cauHinh) {
    return { ...MASCOT_KENH_MAC_DINH };
  }
  const mauAo = cauHinh.mauAo || cauHinh.mauChuDao || MASCOT_KENH_MAC_DINH.mauAo;
  return {
    ...MASCOT_KENH_MAC_DINH,
    ...cauHinh,
    id: (cauHinh.id || MASCOT_KENH_MAC_DINH.id).trim() || ID_MASCOT_KENH,
    ten: (cauHinh.ten || MASCOT_KENH_MAC_DINH.ten).trim() || MASCOT_KENH_MAC_DINH.ten,
    mauChuDao: cauHinh.mauChuDao || mauAo || MASCOT_KENH_MAC_DINH.mauChuDao,
    mauAo,
  };
}
