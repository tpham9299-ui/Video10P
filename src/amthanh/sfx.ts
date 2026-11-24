import type { LoaiHieuUngTanCong } from '../kieu_dai';

export type TenFileSfx =
  | 'whoosh.mp3'
  | 'impact.mp3'
  | 'clash.mp3'
  | 'laser.mp3'
  | 'dash.mp3'
  | 'powerup.mp3';

export const BAN_DO_SFX_HIEU_UNG: Record<LoaiHieuUngTanCong, TenFileSfx> = {
  vet_chem: 'whoosh.mp3',
  song_xung_kich: 'impact.mp3',
  tia_lua_va_cham: 'clash.mp3',
  tia_laser_toan: 'laser.mp3',
  nem_ky_hieu: 'powerup.mp3',
  duong_toc_do: 'dash.mp3',
  bui_dat: 'impact.mp3',
};

/**
 * Danh sach file SFX that da dat trong public/sfx/.
 * Mac dinh rong de tuyet doi khong render <Audio> khi chua co file mp3 that.
 */
export const DANH_SACH_SFX_CO_SAN: readonly TenFileSfx[] = [];

export function layDuongDanSfxNeuCoSan(loai: LoaiHieuUngTanCong): string | null {
  const tenFile = BAN_DO_SFX_HIEU_UNG[loai];
  if (!DANH_SACH_SFX_CO_SAN.includes(tenFile)) {
    return null;
  }
  return `sfx/${tenFile}`;
}
