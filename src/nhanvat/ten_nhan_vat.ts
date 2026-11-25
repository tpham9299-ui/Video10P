export type ThongSoHopTen = {
  text: string;
  fontSize: number;
  width: number;
  height: number;
};

const KY_TU_HEP = new Set(
  "ilIjtfr1.,:;!|'íìỉĩịÍÌỈĨỊ()[]",
);

const KY_TU_RONG = new Set(
  'WMmwGOQDHNUBRAKĐÔƠƯĂÂÀÁẢÃẠÈÉẺẼẸÒÓỎÕỌÙÚỦŨỤ',
);

/**
 * Uoc luong do rong chuoi ten nhan vat tat dinh 100% (khong dung DOM API)
 * de hop nhan ten tu co gian theo do dai chuoi, khong bao gio bi cat chu
 * (vi du: "Srinivasa Ramanujan", "Muhammad ibn Musa al-Khwarizmi").
 */
export function tinhThongSoHopTen(ten: string): ThongSoHopTen {
  const sach = (ten || '').trim();
  const fontSize = sach.length > 28 ? 14.5 : 16;
  const height = 28;

  if (!sach) {
    return { text: '', fontSize, width: 0, height };
  }

  let tongRongChu = 0;
  for (const ch of sach) {
    if (ch === ' ') {
      tongRongChu += fontSize * 0.36;
    } else if (KY_TU_HEP.has(ch)) {
      tongRongChu += fontSize * 0.44;
    } else if (KY_TU_RONG.has(ch)) {
      tongRongChu += fontSize * 0.8;
    } else if (ch === ch.toUpperCase() && ch !== ch.toLowerCase()) {
      tongRongChu += fontSize * 0.72;
    } else {
      tongRongChu += fontSize * 0.64;
    }
  }

  // Cong bien an toan 8% + padding ngang 40px (20px moi ben) de chu luon thoang & khong bao gio cham vien
  const width = Math.max(112, Math.ceil(tongRongChu * 1.08 + 40));

  return {
    text: sach,
    fontSize,
    width,
    height,
  };
}

/**
 * Tu dong xuong dong cho bong bong thoai theo ranh gioi tu, mo rong so dong vua du
 * de hien thi tron ven loi thoai ngan/trung binh, TUYET DOI KHONG cat cut bang dau "...".
 */
export function chiaDongBongBong(
  noiDung: string,
  kyTuToiDaMoiDong = 32,
): string[] {
  const sach = (noiDung || '').trim().replace(/\s+/g, ' ');
  if (!sach) {
    return [];
  }
  if (sach.length <= kyTuToiDaMoiDong) {
    return [sach];
  }

  const gioiHan =
    sach.length > 100 ? 38 : sach.length > 64 ? 34 : kyTuToiDaMoiDong;
  const cacTu = sach.split(' ');
  const ketQua: string[] = [];
  let dongHienTai = '';

  for (const tu of cacTu) {
    if (!dongHienTai) {
      dongHienTai = tu;
    } else if (dongHienTai.length + 1 + tu.length <= gioiHan) {
      dongHienTai = `${dongHienTai} ${tu}`;
    } else {
      ketQua.push(dongHienTai);
      dongHienTai = tu;
    }
  }
  if (dongHienTai) {
    ketQua.push(dongHienTai);
  }
  return ketQua;
}
