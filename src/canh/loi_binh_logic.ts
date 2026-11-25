import type { LoaiBoCuc, LoaiCanh, LoiBinhHaiHuoc } from '../kieu_dai';

/**
 * Cam hien thi hop "GOC BINH LUAN" tren cac canh co bo cuc giang_toan hoac dong_thoi_gian
 * de tuyet doi khong de chu len bang Toan hoac thanh moc thoi gian.
 */
export function coHienKhungLoiBinh(
  boCuc?: LoaiBoCuc,
  loaiCanh?: LoaiCanh,
  loiBinh?: LoiBinhHaiHuoc,
): boolean {
  if (!loiBinh || !loiBinh.noiDung || !loiBinh.noiDung.trim()) {
    return false;
  }
  if (
    boCuc === 'giai_thich_toan' ||
    boCuc === 'dong_thoi_gian' ||
    loaiCanh === 'giang_toan'
  ) {
    return false;
  }
  return true;
}
