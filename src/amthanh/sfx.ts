import type { LoaiHieuUngHoatHinh } from '../kieu_dai';

export type TenFileSfx =
  | 'pop.mp3'
  | 'ding.mp3'
  | 'boing.mp3'
  | 'crickets.mp3'
  | 'whoosh.mp3'
  | 'dramatic.mp3';

export const BAN_DO_SFX_HIEU_UNG: Record<LoaiHieuUngHoatHinh, TenFileSfx> = {
  bong_den_nay_so: 'ding.mp3',
  giot_mo_hoi: 'pop.mp3',
  dau_cham_hoi: 'boing.mp3',
  soc_set_danh: 'dramatic.mp3',
  sao_lap_lanh: 'ding.mp3',
  khoi_chay_tron: 'whoosh.mp3',
  co_lan_im_lang: 'crickets.mp3',
  nhan_chu_hai_huoc: 'pop.mp3',
  mo_hoi_lon: 'pop.mp3',
  khoi_boc_tai: 'whoosh.mp3',
  mat_xoan_oc: 'boing.mp3',
  cham_hoi_nay: 'boing.mp3',
  tia_toc_do: 'dramatic.mp3',
  bong_den_y_tuong: 'ding.mp3',
};

/** Am luong mac dinh (0..1) vua phai cho tung loai SFX de khong lan giong ke */
export const AM_LUONG_SFX_THEO_LOAI: Record<LoaiHieuUngHoatHinh, number> = {
  bong_den_nay_so: 0.55,
  giot_mo_hoi: 0.5,
  dau_cham_hoi: 0.52,
  soc_set_danh: 0.58,
  sao_lap_lanh: 0.42,
  khoi_chay_tron: 0.48,
  co_lan_im_lang: 0.45,
  nhan_chu_hai_huoc: 0.5,
  mo_hoi_lon: 0.48,
  khoi_boc_tai: 0.5,
  mat_xoan_oc: 0.46,
  cham_hoi_nay: 0.5,
  tia_toc_do: 0.56,
  bong_den_y_tuong: 0.55,
};

/**
 * Danh sach 6 file SFX hoat hinh da co san trong public/sfx/.
 * Co the thay the bang file .mp3 that cung ten ma khong can sua code.
 */
export const DANH_SACH_SFX_CO_SAN: readonly TenFileSfx[] = [
  'pop.mp3',
  'ding.mp3',
  'boing.mp3',
  'crickets.mp3',
  'whoosh.mp3',
  'dramatic.mp3',
] as const;

export function layAmLuongSfx(loai: LoaiHieuUngHoatHinh): number {
  return AM_LUONG_SFX_THEO_LOAI[loai] ?? 0.5;
}

/**
 * Tra ve duong dan tuong doi trong public/ (vd: 'sfx/pop.mp3') neu SFX duoc bat va co san.
 * Khi truyen `tapFilePublicThucTe` (lay tu `getStaticFiles()` cua Remotion),
 * ham se kiem tra them su ton tai thuc te cua file de tuyet doi khong crash neu file bi xoa/thieu.
 */
export function layDuongDanSfxNeuCoSan(
  loai: LoaiHieuUngHoatHinh,
  tapFilePublicThucTe?: ReadonlySet<string> | null,
): string | null {
  const tenFile = BAN_DO_SFX_HIEU_UNG[loai];
  if (!tenFile || !DANH_SACH_SFX_CO_SAN.includes(tenFile)) {
    return null;
  }
  const duongDan = `sfx/${tenFile}`;
  if (tapFilePublicThucTe && tapFilePublicThucTe.size > 0) {
    if (!tapFilePublicThucTe.has(duongDan)) {
      return null;
    }
  }
  return duongDan;
}
