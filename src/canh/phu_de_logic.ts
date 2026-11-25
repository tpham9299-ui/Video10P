import type { Canh } from '../kieu_dai';
import { timLuotThoaiTaiFrame } from '../nhanvat/dien_xuat.ts';
import { easeInOutCubic, kepGiaTri } from '../xuong/duong_cong.ts';

/** Thoi luong hien thi the ten Hoi o dau moi chuong: 2.8 giay (84 frame @ 30fps) */
export const THOI_LUONG_THE_TEN_HOI_GIAY = 2.8;

export type TrangThaiTheTenHoi = {
  dangHien: boolean;
  opacity: number;
  dichY: number;
};

/**
 * Tinh trang thai truot/mo bien mat hoan toan cua the ten Hoi trong 2.8s dau moi hoi.
 * Sau 2.8s (84 frame @ 30fps): dangHien=false, opacity=0 -> nhuong 100% khung hinh cho hoat hinh.
 */
export function tinhTrangThaiTheTenHoi(
  frameTrongHoi: number,
  fps = 30,
): TrangThaiTheTenHoi {
  const f = Number.isFinite(frameTrongHoi) ? frameTrongHoi : -1;
  const tongFrames = Math.round(THOI_LUONG_THE_TEN_HOI_GIAY * Math.max(1, fps));
  if (f < 0 || f >= tongFrames) {
    return { dangHien: false, opacity: 0, dichY: -36 };
  }

  const vaoFrames = 14;
  const raFrames = 16;

  if (f < vaoFrames) {
    const e = easeInOutCubic(kepGiaTri(f / vaoFrames, 0, 1));
    return {
      dangHien: true,
      opacity: Number(e.toFixed(3)),
      dichY: Number(((1 - e) * -28).toFixed(2)),
    };
  }

  if (f >= tongFrames - raFrames) {
    const e = easeInOutCubic(
      kepGiaTri((tongFrames - f) / raFrames, 0, 1),
    );
    return {
      dangHien: e > 0.01,
      opacity: Number(e.toFixed(3)),
      dichY: Number(((1 - e) * -32).toFixed(2)),
    };
  }

  return { dangHien: true, opacity: 1, dichY: 0 };
}

function chuanHoaSoSanhThoai(s: string): string {
  return (s || '')
    .trim()
    .toLowerCase()
    .replace(/\s+/g, ' ')
    .replace(/[“”"'.,!?;:…-]+/g, '');
}

/**
 * Kiem tra dong phu de day man hinh co trung lap voi cau thoai ngan dang hien tren
 * bong bong chat cua nhan vat hay khong -> tu an phu de trung lap de khung hinh sach dep
 * (file .srt van duoc xuat day du boi chuanbi_dai.py).
 */
export function coAnPhuDeTrungBongBong(
  canh: Pick<Canh, 'nhanVat' | 'luotThoai' | 'laKhungTranhDacTa'>,
  frameCucBo: number,
  noiDungPhuDe: string,
): boolean {
  if (canh.laKhungTranhDacTa) {
    return false;
  }
  const pdSach = chuanHoaSoSanhThoai(noiDungPhuDe);
  if (!pdSach) {
    return true;
  }

  const dsNv = canh.nhanVat ?? [];
  if (dsNv.length === 0) {
    return false;
  }

  // 1. Truong hop canh co luotThoai[]: luot dang noi duoc hien truc tiep tren bong bong chat cua nhan vat do
  const luot = timLuotThoaiTaiFrame(canh.luotThoai, frameCucBo);
  if (luot && luot.noiDung && dsNv.some((nv) => nv.id === luot.nhanVatId)) {
    const ndLuot = chuanHoaSoSanhThoai(luot.noiDung);
    if (ndLuot.length > 0 && ndLuot.length <= 140) {
      if (pdSach === ndLuot || pdSach.endsWith(ndLuot) || ndLuot.includes(pdSach)) {
        return true;
      }
    }
  }

  // 2. Truong hop nhan vat co bongBongThoai ngan trung noi dung dang hien o phu de
  for (const nv of dsNv) {
    if (!nv.bongBongThoai) continue;
    const ndBb = chuanHoaSoSanhThoai(nv.bongBongThoai);
    if (ndBb.length > 0 && ndBb.length <= 140) {
      if (pdSach === ndBb || ndBb.includes(pdSach) || pdSach.includes(ndBb)) {
        return true;
      }
    }
  }

  return false;
}
