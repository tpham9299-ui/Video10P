import type {
  DaoCuTrongCanh,
  LoaiBoiCanh,
  LoaiThoiTiet,
  NhanVatTrongCanh,
  VatTheXungQuanh,
} from '../kieu_dai';

export type KhungCuaSo = {
  x: number;
  y: number;
  width: number;
  height: number;
};

/** Danh sach boi canh phong kin (trong nha) de chan la roi/mua/tuyet/chim/taxi lot vao phong */
export const BOI_CANH_TRONG_NHA: ReadonlySet<LoaiBoiCanh> = new Set<LoaiBoiCanh>([
  'thu_vien_co_dien',
  'lop_hoc_bang_xanh',
  'thu_vien_trung_co',
  'dai_thien_van_phuc_hung',
  'giang_duong_hien_dai',
  'nha_co_phong_sinh',
  'phong_tro_bep_lua',
  'phong_benh_vien',
  'giang_duong_dai_hoc',
  'phong_thi_nghiem_co',
  'phong_nen_hai_huoc',
]);

/** Danh sach boi canh vu tru (cam ngon_nen_den_dau lo lung, cam la roi/tuyet/chim) */
export const BOI_CANH_VU_TRU: ReadonlySet<LoaiBoiCanh> = new Set<LoaiBoiCanh>([
  'khong_gian_vu_tru_toan',
  'bau_troi_dem_vu_tru',
]);

const VAT_THE_NGOAI_TROI_CAM_TRONG_NHA = new Set<VatTheXungQuanh['loai']>([
  'la_vang_gio',
  'chim_hai_au',
  'chim_san_truong',
  'ca_gon_song',
  'buom_vuon',
  'xe_taxi_co',
]);

const VAT_THE_CAM_TRONG_VU_TRU = new Set<VatTheXungQuanh['loai']>([
  'ngon_nen_den_dau',
  'la_vang_gio',
  'chim_hai_au',
  'chim_san_truong',
  'ca_gon_song',
  'buom_vuon',
  'xe_taxi_co',
  'tuyet_cua_so',
  'hoi_khoi',
]);

/** Toa do khung kinh cua so chinh xac theo tung boi canh trong nha de clipPath tuyet/mua khong lot vao phong */
export function layKhungCuaSoChoBoiCanh(loai: LoaiBoiCanh): KhungCuaSo | null {
  switch (loai) {
    case 'phong_benh_vien':
      return { x: 685, y: 120, width: 550, height: 410 };
    case 'phong_tro_bep_lua':
      return { x: 776, y: 141, width: 368, height: 263 };
    case 'nha_co_phong_sinh':
      return { x: 687, y: 137, width: 526, height: 346 };
    case 'thu_vien_co_dien':
      return { x: 698, y: 103, width: 524, height: 524 };
    case 'phong_thi_nghiem_co':
      return { x: 772, y: 195, width: 376, height: 335 };
    default:
      return null;
  }
}

/**
 * Kiem tra canh nha_co_phong_sinh co thuc su co em be so sinh hoac dao cu noi_em_be hay khong.
 * Chi hien noi em be khi canh co doTuoi="so_sinh" hoac dao cu noi_em_be (khong ve noi thua cho canh nguoi lon/gia).
 */
export function coHienNoiTrongPhongSinh(
  nhanVat?: readonly NhanVatTrongCanh[],
  daoCu?: readonly DaoCuTrongCanh[],
): boolean {
  return Boolean(
    nhanVat?.some((nv) => nv.doTuoi === 'so_sinh') ||
      daoCu?.some((dc) => dc.loai === 'noi_em_be'),
  );
}

/**
 * Kiem tra co can an noi em be ve san trong nen nha_co_phong_sinh hay khong:
 * bo noi thua tren nen khi canh da co nhan vat so_sinh hoac dao cu noi_em_be.
 */
export function coAnNoiNenPhongSinh(
  nhanVat?: readonly NhanVatTrongCanh[],
  daoCu?: readonly DaoCuTrongCanh[],
): boolean {
  return coHienNoiTrongPhongSinh(nhanVat, daoCu);
}

/**
 * Kiem tra vat the moi truong co hop le voi loai phong / boi canh hay khong.
 * - Cam la_vang_gio (va sinh vat ngoai troi) trong giang_duong_dai_hoc hay bat ky phong kin nao.
 * - Cam ngon_nen_den_dau troi lo lung trong khong_gian_vu_tru_toan.
 * - Chi cho phep tuyet_cua_so o phong co khung cua so.
 */
export function locVatTheHopLeTheoBoiCanh(
  loai: LoaiBoiCanh,
  danhSach: readonly VatTheXungQuanh[],
): VatTheXungQuanh[] {
  const laTrongNha = BOI_CANH_TRONG_NHA.has(loai);
  const laVuTru = BOI_CANH_VU_TRU.has(loai);
  const cuaSo = layKhungCuaSoChoBoiCanh(loai);

  return danhSach.filter((item) => {
    if (laTrongNha && VAT_THE_NGOAI_TROI_CAM_TRONG_NHA.has(item.loai)) {
      return false;
    }
    if (laVuTru && VAT_THE_CAM_TRONG_VU_TRU.has(item.loai)) {
      return false;
    }
    if (item.loai === 'tuyet_cua_so' && !cuaSo) {
      return false;
    }
    return true;
  });
}

/**
 * Kiem tra co can an giuong benh ve san trong nen phong_benh_vien hay khong:
 * an giuong nen khi canh co nhan vat tuThe="nam_giuong" hoac dao cu giuong_benh.
 */
export function coAnGiuongBenhNen(
  nhanVat?: readonly NhanVatTrongCanh[],
  daoCu?: readonly DaoCuTrongCanh[],
): boolean {
  return Boolean(
    nhanVat?.some((nv) => nv.tuThe === 'nam_giuong') ||
      daoCu?.some((dc) => dc.loai === 'giuong_benh'),
  );
}

/**
 * Loc bo dao cu trung lap voi nhan vat:
 * - Bo dao cu noi_em_be khi da co nhan vat doTuoi="so_sinh" (da ve em be trong noi)
 * - Bo dao cu giuong_benh khi da co nhan vat tuThe="nam_giuong" (chi giu duy nhat 1 giuong co nhan vat nam)
 */
export function locDaoCuKhongTrungLap(
  daoCu?: readonly DaoCuTrongCanh[],
  nhanVat?: readonly NhanVatTrongCanh[],
): DaoCuTrongCanh[] {
  if (!daoCu || daoCu.length === 0) {
    return [];
  }
  const coSoSinh = Boolean(nhanVat?.some((nv) => nv.doTuoi === 'so_sinh'));
  const coNamGiuong = Boolean(nhanVat?.some((nv) => nv.tuThe === 'nam_giuong'));
  return daoCu.filter((dc) => {
    if (coSoSinh && dc.loai === 'noi_em_be') return false;
    if (coNamGiuong && dc.loai === 'giuong_benh') return false;
    return true;
  });
}

/**
 * Tu dong chon bo sinh vat & do vat moi truong song dong phu hop voi tung boi canh
 * khi canh chua khai bao rieng vatTheXungQuanh[] trong JSON.
 */
export function layVatTheMacDinhChoBoiCanh(
  loai: LoaiBoiCanh,
  thoiTiet?: LoaiThoiTiet,
  bienSoXe?: string,
): VatTheXungQuanh[] {
  const bienSo = (bienSoXe || '').trim();
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
        {
          loai: 'xe_taxi_co',
          x: 340,
          y: 745,
          tocDo: 3.1,
          ...(bienSo ? { bienSoXe: bienSo } : {}),
        },
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
 * neu khong khai bao thi gan tu dong theo boiCanh.
 * - Loc bo vat the lech boi canh (la_vang_gio trong phong kin, ngon_nen_den_dau trong vu tru...).
 * - Khong hardcode bien so "1729": chi gan bienSoXe neu JSON truyen ro.
 * - Tu dong khoa toa do tuyet_cua_so vao dung khung kinh cua so cua phong.
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

  const daLoc = locVatTheHopLeTheoBoiCanh(loai, nguon);
  const khungCuaSo = layKhungCuaSoChoBoiCanh(loai);

  return daLoc.map((item) => {
    if (item.loai === 'xe_taxi_co') {
      const bs = (item.bienSoXe || bienSoXe || '').trim().slice(0, 12);
      return bs ? { ...item, bienSoXe: bs } : { ...item, bienSoXe: undefined };
    }
    if (item.loai === 'tuyet_cua_so' && khungCuaSo) {
      return {
        ...item,
        x: khungCuaSo.x,
        y: khungCuaSo.y,
      };
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
