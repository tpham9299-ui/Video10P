import type { Canh, Chuong, LoaiChuyenCanh } from '../kieu_dai';

export type CanhDaCanKhung = {
  canh: Canh;
  tenChuong: string;
  phuDeHoi?: string;
  chuongId: string;
  chiSoChuong: number;
  tuFrameThuc: number;
  denFrameThuc: number;
  thoiLuongCanh: number;
  laCanhCuoiToanTap: boolean;
  /** Chi bat man hinh ket thuc / outro o canh cuoi cung cua hoi cuoi cung toan tap */
  hienManHinhKetThuc: boolean;
  chuyenCanhTiepTheo?: LoaiChuyenCanh;
};

export type ThongKeChuongLienMach = {
  id: string;
  tenChuong: string;
  tuFrame: number;
  denFrame: number;
};

export type KetQuaCanKhungLienMach = {
  danhSachCanh: CanhDaCanKhung[];
  thongKeChuong: ThongKeChuongLienMach[];
  tongFrames: number;
};

/**
 * Chuan hoa chuoi Sequence noi tiep lien mach tu frame 0 den frame cuoi (khong gap frame, khong chong de).
 * Dong thoi chi cho phep bat man hinh ket thuc / outro (hienManHinhKetThuc=true) tai dung canh cuoi cung
 * cua hoi cuoi cung toan tap.
 */
export function chuanHoaKhungHinhLienMach(
  chuong: readonly Chuong[],
): KetQuaCanKhungLienMach {
  const tam: Array<{
    canh: Canh;
    tenChuong: string;
    phuDeHoi?: string;
    chuongId: string;
    chiSoChuong: number;
  }> = [];

  for (let ci = 0; ci < chuong.length; ci++) {
    const ch = chuong[ci];
    for (const c of ch.canh ?? []) {
      tam.push({
        canh: c,
        tenChuong: ch.tenChuong,
        phuDeHoi: c.phuDeHoi ?? ch.phuDeHoi,
        chuongId: ch.id,
        chiSoChuong: ci,
      });
    }
  }

  let conTro = 0;
  const danhSachCanh: CanhDaCanKhung[] = tam.map((item, idx) => {
    const rawDur = Number.isFinite(item.canh.denFrame - item.canh.tuFrame)
      ? Math.round(item.canh.denFrame - item.canh.tuFrame)
      : 1;
    const thoiLuongCanh = Math.max(1, rawDur);
    const tuFrameThuc = conTro;
    const denFrameThuc = conTro + thoiLuongCanh;
    conTro = denFrameThuc;

    const laCanhCuoiToanTap = idx === tam.length - 1;
    return {
      ...item,
      tuFrameThuc,
      denFrameThuc,
      thoiLuongCanh,
      laCanhCuoiToanTap,
      hienManHinhKetThuc: laCanhCuoiToanTap && item.canh.boCuc === 'ket_thuc',
      chuyenCanhTiepTheo: tam[idx + 1]?.canh.chuyenCanh,
    };
  });

  const phamViTheoChuong = new Map<number, { tu: number; den: number }>();
  for (const muc of danhSachCanh) {
    const cur = phamViTheoChuong.get(muc.chiSoChuong);
    if (!cur) {
      phamViTheoChuong.set(muc.chiSoChuong, {
        tu: muc.tuFrameThuc,
        den: muc.denFrameThuc,
      });
    } else {
      cur.den = muc.denFrameThuc;
    }
  }

  const thongKeChuong: ThongKeChuongLienMach[] = chuong.map((ch, ci) => {
    const pv = phamViTheoChuong.get(ci);
    return {
      id: ch.id,
      tenChuong: ch.tenChuong,
      tuFrame: pv ? pv.tu : 0,
      denFrame: pv ? pv.den : 0,
    };
  });

  return {
    danhSachCanh,
    thongKeChuong,
    tongFrames: conTro,
  };
}

/**
 * Kiem dinh du lieu JSON goc xem co bat ky gap frame, chong de frame hoac tuFrame dau != 0 hay khong.
 */
export function kiemTraKhungHinhLienMach(chuong: readonly Chuong[]): string[] {
  const loi: string[] = [];
  const tatCa: Canh[] = [];
  for (const ch of chuong ?? []) {
    for (const c of ch.canh ?? []) {
      tatCa.push(c);
    }
  }

  if (tatCa.length === 0) {
    loi.push('Khong co canh nao trong danh sach chuong.');
    return loi;
  }

  let frameTruoc = 0;
  for (let i = 0; i < tatCa.length; i++) {
    const c = tatCa[i];
    if (
      typeof c.tuFrame !== 'number' ||
      typeof c.denFrame !== 'number' ||
      !Number.isInteger(c.tuFrame) ||
      !Number.isInteger(c.denFrame)
    ) {
      loi.push(`Canh ${c.id}: tuFrame/denFrame phai la so nguyen.`);
      continue;
    }
    if (c.denFrame <= c.tuFrame) {
      loi.push(`Canh ${c.id}: denFrame (${c.denFrame}) phai lon hon tuFrame (${c.tuFrame}).`);
    }
    if (i === 0 && c.tuFrame !== 0) {
      loi.push(`Canh dau tien ${c.id} phai bat dau tu frame 0 (hien tai: ${c.tuFrame}).`);
    } else if (i > 0 && c.tuFrame > frameTruoc) {
      loi.push(`Phat hien gap frame giua canh truoc (${frameTruoc}) va ${c.id} (${c.tuFrame}).`);
    } else if (i > 0 && c.tuFrame < frameTruoc) {
      loi.push(`Phat hien chong de frame tai ${c.id} (${c.tuFrame} < ${frameTruoc}).`);
    }
    frameTruoc = c.denFrame;
  }

  return loi;
}
