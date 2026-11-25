import type { KieuBongBongChat } from '../kieu_dai';
import { chiaDongBongBong } from '../nhanvat/ten_nhan_vat.ts';
import { kepGiaTri } from '../xuong/duong_cong.ts';

export type BoCucBongBongChat = {
  dong: string[];
  width: number;
  height: number;
  fontSize: number;
  lineHeight: number;
  paddingY: number;
  /** Toa do tam bong bong trong he toa do cuc bo cua nhan vat */
  localX: number;
  localY: number;
  /** Toa do tam bong bong trong he toa do the gioi 1920x1080 (da tranh tran mep & tranh che mat) */
  worldX: number;
  worldY: number;
  /** Toa do mui duoi chi ve mieng nhan vat (cuc bo theo tam bong bong) */
  duoiTargetX: number;
  duoiTargetY: number;
  /** Huong dat bong bong so voi dau: ben_trai | ben_phai | phia_tren */
  viTriTuongDoi: 'ben_trai' | 'ben_phai' | 'phia_tren';
  kieu: KieuBongBongChat;
};

/**
 * Tinh kich thuoc & vi tri an toan cho BongBongChat:
 * - Dat canh mieng nhan vat theo huong nhin (dir), tu dong lat sang phia con lai hoac len tren dau
 *   de KHONG bao gio che khuon mat va KHONG bao gio tran ra ngoai mep khung 1920x1080.
 */
export function tinhBoCucBongBongChat(thamSo: {
  noiDung: string;
  kieu?: KieuBongBongChat;
  /** Toa do goc nhan vat tren 1920x1080 */
  nhanVatWorldX: number;
  nhanVatWorldY: number;
  tiLeNhanVat: number;
  /** Toa do cuc bo tam dau & mieng nhan vat */
  dauLocalX: number;
  dauLocalY: number;
  dir: number;
  banKinhDau?: number;
}): BoCucBongBongChat {
  const kieu: KieuBongBongChat = thamSo.kieu ?? 'thuong';
  const dong = chiaDongBongBong(thamSo.noiDung);
  const tiLe = Math.max(0.25, Number.isFinite(thamSo.tiLeNhanVat) ? thamSo.tiLeNhanVat : 1);
  const banKinhDau = thamSo.banKinhDau ?? 26;

  const fontSize = dong.length >= 4 ? 15.5 : 17.5;
  const lineHeight = dong.length >= 4 ? 21 : 23.5;
  const paddingY = kieu === 'quat_thao' ? 18 : 15;
  const doDaiMax = dong.reduce((m, s) => Math.max(m, s.length), 0);
  const width = Math.max(
    188,
    Math.min(430, Math.ceil(doDaiMax * fontSize * 0.58 + (kieu === 'quat_thao' ? 62 : 48))),
  );
  const height = Math.max(54, dong.length * lineHeight + paddingY * 2);

  // Toa do tam dau & mieng trong he toa do the gioi 1920x1080
  const dauWorldX = thamSo.nhanVatWorldX + thamSo.dauLocalX * tiLe;
  const dauWorldY = thamSo.nhanVatWorldY + thamSo.dauLocalY * tiLe;
  const miengWorldX = dauWorldX + 10 * thamSo.dir * tiLe;
  const miengWorldY = dauWorldY + 8 * tiLe;

  const nuaRongW = (width / 2) * tiLe;
  const nuaCaoW = (height / 2) * tiLe;
  const lechNgangTuMat = (banKinhDau + 22) * tiLe + nuaRongW;
  const caoCanhMiengY = dauWorldY - 22 * tiLe;

  const mepTrai = 34 + nuaRongW;
  const mepPhai = 1886 - nuaRongW;
  const mepTren = 56 + nuaCaoW;
  const mepDuoi = 900 - nuaCaoW;

  // Thu dat phia truoc mieng (theo huong nhin dir) -> neu tran mep thi lat sang phia doi dien -> cuoi cung len phia tren dau
  const ungVienTruocX = dauWorldX + thamSo.dir * lechNgangTuMat;
  const ungVienSauX = dauWorldX - thamSo.dir * lechNgangTuMat;

  let worldX: number;
  let worldY: number;
  let viTriTuongDoi: 'ben_trai' | 'ben_phai' | 'phia_tren';

  const hopLeX = (x: number) => x >= mepTrai && x <= mepPhai;

  if (hopLeX(ungVienTruocX)) {
    worldX = ungVienTruocX;
    worldY = kepGiaTri(caoCanhMiengY, mepTren, mepDuoi);
    viTriTuongDoi = thamSo.dir > 0 ? 'ben_phai' : 'ben_trai';
  } else if (hopLeX(ungVienSauX)) {
    worldX = ungVienSauX;
    worldY = kepGiaTri(caoCanhMiengY, mepTren, mepDuoi);
    viTriTuongDoi = thamSo.dir > 0 ? 'ben_trai' : 'ben_phai';
  } else {
    worldX = kepGiaTri(dauWorldX + 18 * thamSo.dir * tiLe, mepTrai, mepPhai);
    worldY = kepGiaTri(
      dauWorldY - (banKinhDau + 28) * tiLe - nuaCaoW,
      mepTren,
      mepDuoi,
    );
    viTriTuongDoi = 'phia_tren';
  }

  // Kiem tra chong lan khuon mat lan cuoi: neu van cham hop dau thi day len phia tren dau
  const vungMatR = (banKinhDau + 14) * tiLe;
  const chongX = Math.abs(worldX - dauWorldX) < nuaRongW + vungMatR - 6;
  const chongY = Math.abs(worldY - dauWorldY) < nuaCaoW + vungMatR - 6;
  if (chongX && chongY) {
    worldY = kepGiaTri(
      dauWorldY - vungMatR - nuaCaoW - 10,
      mepTren,
      mepDuoi,
    );
    viTriTuongDoi = 'phia_tren';
  }

  const localX = (worldX - thamSo.nhanVatWorldX) / tiLe;
  const localY = (worldY - thamSo.nhanVatWorldY) / tiLe;

  const duoiTargetX = kepGiaTri((miengWorldX - worldX) / tiLe, -width / 2 - 48, width / 2 + 48);
  const duoiTargetY = kepGiaTri((miengWorldY - worldY) / tiLe, -height / 2 - 42, height / 2 + 54);

  return {
    dong,
    width,
    height,
    fontSize,
    lineHeight,
    paddingY,
    localX: Number(localX.toFixed(1)),
    localY: Number(localY.toFixed(1)),
    worldX: Number(worldX.toFixed(1)),
    worldY: Number(worldY.toFixed(1)),
    duoiTargetX: Number(duoiTargetX.toFixed(1)),
    duoiTargetY: Number(duoiTargetY.toFixed(1)),
    viTriTuongDoi,
    kieu,
  };
}
