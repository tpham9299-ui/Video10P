import { kepGiaTri } from '../xuong/duong_cong.ts';
import { bamTatDinh } from '../vfx/tat_dinh.ts';

export type KhauHinhMieng = 0 | 1 | 2 | 3;

export type KetQuaLipSync = {
  cuongDo: number;
  khauHinh: KhauHinhMieng;
  nguon: 'rms' | 'du_phong';
};

/** Nguong anh xa bien do RMS chuan hoa [0..1] sang 4 khau hinh mieng */
export const NGUONG_RMS_KHEP_MIENG = 0.08;
export const NGUONG_RMS_HE_NHE = 0.32;
export const NGUONG_RMS_MO_VUA = 0.62;

/**
 * Anh xa truc tiep bien do RMS [0..1] cua khung hinh hien tai vao 4 khau hinh:
 * - 0: im lang / duoi nguong thap -> khep mieng hoan toan
 * - 1: thap -> he nhe (mo nho)
 * - 2: trung binh -> mo vua (tron chu O)
 * - 3: cao -> mo rong
 */
export function chonKhauHinhTuBienDo(bienDo: number): KetQuaLipSync {
  const cuongDo = Number.isFinite(bienDo) ? kepGiaTri(bienDo, 0, 1) : 0;

  if (cuongDo < NGUONG_RMS_KHEP_MIENG) {
    return { cuongDo, khauHinh: 0, nguon: 'rms' };
  }
  if (cuongDo < NGUONG_RMS_HE_NHE) {
    return { cuongDo, khauHinh: 1, nguon: 'rms' };
  }
  if (cuongDo < NGUONG_RMS_MO_VUA) {
    return { cuongDo, khauHinh: 2, nguon: 'rms' };
  }
  return { cuongDo, khauHinh: 3, nguon: 'rms' };
}

/**
 * Co che du phong tat dinh 100% (dung bamTatDinh + 3 song sin + khoang ngat lay hoi)
 * khi canh chua co mang bien do RMS (vd: du_lieu/mau_pythagoras.json).
 */
export function tinhLipSyncDuPhong(frame: number, seedId: number): KetQuaLipSync {
  // Khoang ngat lay hoi dinh ky: moi 74 frame nghi lay hoi 8 frame
  const phaHoi = (((frame + (seedId % 37)) % 74) + 74) % 74;
  if (phaHoi >= 66) {
    return { cuongDo: 0, khauHinh: 0, nguon: 'du_phong' };
  }

  // Lam mem bien do ngay truoc/sau khi lay hoi
  const baoHoi =
    phaHoi < 3 ? phaHoi / 3 : phaHoi > 63 ? (66 - phaHoi) / 3 : 1;

  const nhieuNhe = (bamTatDinh(Math.floor(frame / 3) * 13 + seedId * 7) - 0.5) * 0.14;
  const song =
    0.46 * Math.sin(frame * 0.42 + (seedId % 19) * 0.31) +
    0.34 * Math.sin(frame * 0.73 + (seedId % 23) * 0.47 + 1.2) +
    0.2 * Math.sin(frame * 1.17 + (seedId % 29) * 0.23 + 2.5);

  const cuongDo = kepGiaTri(((song + 1) * 0.5 + nhieuNhe) * baoHoi, 0, 1);

  if (cuongDo < 0.22) {
    return { cuongDo, khauHinh: 0, nguon: 'du_phong' };
  }
  if (cuongDo < 0.48) {
    return { cuongDo, khauHinh: 1, nguon: 'du_phong' };
  }
  if (cuongDo < 0.72) {
    return { cuongDo, khauHinh: 2, nguon: 'du_phong' };
  }
  return { cuongDo, khauHinh: 3, nguon: 'du_phong' };
}

/**
 * Tinh khau hinh lip-sync cho khung hinh hien tai:
 * - Neu canh/nhan vat co mang bienDoAmThanh (RMS theo 30fps): bam sat bien do that.
 *   Khi vuot qua do dai audio (khoang nghi cuoi canh), tu dong tra ve khauHinh 0 (khep mieng).
 * - Neu khong co mang RMS: tu dong fallback ve tinhLipSyncDuPhong tat dinh 100%.
 */
export function tinhLipSyncChoFrame(
  frame: number,
  seedId: number,
  bienDoAmThanh?: readonly number[] | null,
): KetQuaLipSync {
  if (Array.isArray(bienDoAmThanh) && bienDoAmThanh.length > 0) {
    const chiSo = Math.floor(frame);
    if (chiSo < 0 || chiSo >= bienDoAmThanh.length) {
      return { cuongDo: 0, khauHinh: 0, nguon: 'rms' };
    }
    const giaTri = bienDoAmThanh[chiSo];
    if (typeof giaTri === 'number' && Number.isFinite(giaTri)) {
      return chonKhauHinhTuBienDo(giaTri);
    }
    return { cuongDo: 0, khauHinh: 0, nguon: 'rms' };
  }
  return tinhLipSyncDuPhong(frame, seedId);
}
