import type {
  LoaiBoiCanh,
  LoaiThoiTiet,
  VatTheXungQuanh,
} from '../kieu_dai';

/**
 * Tu dong chon bo sinh vat & do vat moi truong song dong phu hop voi tung boi canh
 * khi canh chua khai bao rieng vatTheXungQuanh[] trong JSON.
 */
export function layVatTheMacDinhChoBoiCanh(
  loai: LoaiBoiCanh,
  thoiTiet?: LoaiThoiTiet,
  bienSoXe?: string,
): VatTheXungQuanh[] {
  const bienSo = (bienSoXe || '').trim() || '1729';
  switch (loai) {
    case 'cang_bien_tau_thuy':
      return [
        { loai: 'chim_hai_au', x: 320, y: 185, soLuong: 4, tocDo: 1.35 },
        { loai: 'ca_gon_song', x: 980, y: 635, soLuong: 3 },
      ];
    case 'bo_bien_hy_lap':
      return [
        { loai: 'chim_hai_au', x: 640, y: 200, soLuong: 3, tocDo: 1.2 },
        { loai: 'ca_gon_song', x: 1120, y: 625, soLuong: 2 },
      ];
    case 'vuon_tao_dong_que':
      return [
        { loai: 'buom_vuon', x: 520, y: 610, soLuong: 3 },
        { loai: 'chim_san_truong', x: 260, y: 210, soLuong: 2, tocDo: 1.1 },
      ];
    case 'rung_nui_thien_nhien':
      return [
        { loai: 'buom_vuon', x: 680, y: 620, soLuong: 3 },
        { loai: 'la_vang_gio', x: 0, y: 0, soLuong: 6 },
      ];
    case 'san_truong_co_dien':
      return [
        { loai: 'chim_san_truong', x: 420, y: 245, soLuong: 4, tocDo: 1.15 },
        { loai: 'la_vang_gio', x: 0, y: 0, soLuong: 5 },
      ];
    case 'lang_que_an_do_a_dong':
      return [
        { loai: 'buom_vuon', x: 600, y: 640, soLuong: 3 },
        { loai: 'chim_san_truong', x: 350, y: 190, soLuong: 3, tocDo: 1.1 },
      ];
    case 'duong_pho_xe_co':
      return [
        { loai: 'xe_taxi_co', x: 340, y: 745, tocDo: 3.1, bienSoXe: bienSo },
        { loai: 'chim_san_truong', x: 240, y: 205, soLuong: 3, tocDo: 1.15 },
      ];
    case 'pho_co_chau_au':
      return [
        { loai: 'chim_san_truong', x: 420, y: 200, soLuong: 3, tocDo: 1.1 },
        { loai: 'ca_gon_song', x: 960, y: 640, soLuong: 2 },
      ];
    case 'phong_tro_bep_lua':
      return [
        { loai: 'hoi_khoi', x: 1525, y: 618, soLuong: 3, tiLe: 1.05 },
        { loai: 'ngon_nen_den_dau', x: 410, y: 585, tiLe: 0.95 },
      ];
    case 'nha_co_phong_sinh':
      return [
        { loai: 'ngon_nen_den_dau', x: 355, y: 560, tiLe: 1.0 },
        { loai: 'dong_ho_qua_lac', x: 1625, y: 255, tiLe: 0.95 },
      ];
    case 'phong_benh_vien':
      return [
        {
          loai: 'tuyet_cua_so',
          x: 685,
          y: 120,
          soLuong: 18,
          mau: thoiTiet === 'mua_nhe' ? '#BAE6FD' : '#FFFFFF',
        },
        { loai: 'dong_ho_qua_lac', x: 270, y: 235, tiLe: 0.85 },
      ];
    case 'phong_thi_nghiem_co':
      return [
        { loai: 'ngon_nen_den_dau', x: 1510, y: 575, tiLe: 0.95 },
        { loai: 'dong_ho_qua_lac', x: 265, y: 235, tiLe: 0.9 },
      ];
    case 'thu_vien_co_dien':
    case 'thu_vien_trung_co':
      return [{ loai: 'ngon_nen_den_dau', x: 1560, y: 640, tiLe: 0.85 }];
    case 'giang_duong_dai_hoc':
      return [{ loai: 'dong_ho_qua_lac', x: 1685, y: 220, tiLe: 0.88 }];
    case 'quang_truong_hy_lap':
      return [{ loai: 'chim_san_truong', x: 520, y: 210, soLuong: 3, tocDo: 1.15 }];
    default:
      return [];
  }
}

/**
 * Giai danh sach vat the moi truong hien thi: uu tien vatTheXungQuanh[] tu JSON,
 * neu khong khai bao thi gan tu dong theo boiCanh. Luon truyen bienSoXe neu co.
 */
export function giaiDanhSachVatTheXungQuanh(
  loai: LoaiBoiCanh,
  thoiTiet?: LoaiThoiTiet,
  vatTheXungQuanh?: readonly VatTheXungQuanh[],
  bienSoXe?: string,
): VatTheXungQuanh[] {
  const nguon =
    Array.isArray(vatTheXungQuanh) && vatTheXungQuanh.length > 0
      ? vatTheXungQuanh
      : layVatTheMacDinhChoBoiCanh(loai, thoiTiet, bienSoXe);

  return nguon.map((item) => {
    if (item.loai === 'xe_taxi_co') {
      const bs = (item.bienSoXe || bienSoXe || '1729').trim().slice(0, 12);
      return { ...item, bienSoXe: bs || '1729' };
    }
    return item;
  });
}

/** Tinh vi tri X tat dinh cua xe taxi co chay lap ngang duong */
export function tinhViTriTaxiCo(
  frame: number,
  xBatDau = 260,
  tocDo = 3.1,
): { x: number; gocBanhXe: number; nhunXeY: number } {
  const chuKy = 2560;
  const x = (((xBatDau + frame * tocDo) % chuKy) + chuKy) % chuKy - 320;
  const gocBanhXe = (frame * tocDo * 3.8) % 360;
  const nhunXeY = Math.sin(frame * 0.45) * 1.4;
  return { x, gocBanhXe, nhunXeY };
}

/** Tinh goc lac con lac dong ho tat dinh (do) */
export function tinhGocQuaLac(frame: number, bienDoDo = 16): number {
  return Math.sin(frame * 0.14) * bienDoDo;
}

/** Tinh toa do va goc vo canh tat dinh cua buom bay trong vuon */
export function tinhBuomBay(
  frame: number,
  xGoc: number,
  yGoc: number,
  chiSo: number,
): { x: number; y: number; coCanhX: number; nghieng: number } {
  const pha = chiSo * 2.1;
  const t = frame * 0.045 + pha;
  const x = xGoc + Math.sin(t) * 125 + Math.cos(t * 0.5) * 45;
  const y = yGoc + Math.sin(t * 2) * 38 + Math.cos(t * 1.3) * 16;
  const coCanhX = 0.3 + 0.7 * Math.abs(Math.sin(frame * 0.42 + pha));
  const nghieng = Math.cos(t) * 14;
  return { x, y, coCanhX, nghieng };
}
