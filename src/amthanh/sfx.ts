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
};

/**
 * Danh sach file SFX that da dat trong public/sfx/.
 * Mac dinh rong de tuyet doi khong render <Audio> khi chua co file mp3 that.
 */
export const DANH_SACH_SFX_CO_SAN: readonly TenFileSfx[] = [];

export function layDuongDanSfxNeuCoSan(loai: LoaiHieuUngHoatHinh): string | null {
  const tenFile = BAN_DO_SFX_HIEU_UNG[loai];
  if (!DANH_SACH_SFX_CO_SAN.includes(tenFile)) {
    return null;
  }
  return `sfx/${tenFile}`;
}
