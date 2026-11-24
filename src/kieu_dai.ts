export type LoaiBoCuc =
  | 'mo_dau'
  | 'ke_chuyen'
  | 'doi_thoai'
  | 'hai_huoc'
  | 'giai_thich_toan'
  | 'dong_thoi_gian'
  | 'ket_thuc';

export type LoaiBoiCanh =
  | 'bo_bien_hy_lap'
  | 'vuon_tao_dong_que'
  | 'pho_co_chau_au'
  | 'rung_nui_thien_nhien'
  | 'thu_vien_co_dien'
  | 'lop_hoc_bang_xanh'
  | 'bau_troi_dem_vu_tru'
  | 'phong_nen_hai_huoc';

export type LoaiThoiTiet =
  | 'khong'
  | 'nang_dep'
  | 'hoang_hon'
  | 'ban_dem'
  | 'mua_nhe'
  | 'la_roi'
  | 'tuyet_roi';

export type LoaiHanhDong =
  | 'dung_tho'
  | 'di_bo'
  | 'chay_voi_va'
  | 'ngoi_doc_sach'
  | 'chi_tro_giai_thich'
  | 'nhin_len_troi'
  | 'gat_gu_dong_tinh'
  | 'gai_dau_kho_hieu'
  | 'giat_minh_nhay_dung'
  | 'bo_tay_can_loi'
  | 'khoanh_tay_tu_man'
  | 'ho_het_sung_suong'
  | 'di_qua_di_lai'
  | 'sup_do_tuyet_vong';

export type LoaiBieuCam =
  | 'binh_thuong'
  | 'vui_tuoi'
  | 'ngac_nhien'
  | 'tuc_gian'
  | 'hoang_mang'
  | 'tinh_quai'
  | 'tram_tu'
  | 'can_loi_mat_do'
  | 'tu_man';

export type LoaiPhuKien =
  | 'khong'
  | 'vong_nguyet_que'
  | 'toc_gia_17'
  | 'kinh_tron'
  | 'mu_noi_phap'
  | 'ao_choang'
  | 'khan_choang'
  | 'mu_tham_tu';

export type LoaiVatCamTay =
  | 'khong'
  | 'cuon_giay'
  | 'qua_tao'
  | 'kinh_lup'
  | 'but_long_ngong'
  | 'que_chi_bang'
  | 'den_long'
  | 'ly_ca_phe';

export type LoaiHieuUngHoatHinh =
  | 'bong_den_nay_so'
  | 'giot_mo_hoi'
  | 'dau_cham_hoi'
  | 'soc_set_danh'
  | 'sao_lap_lanh'
  | 'khoi_chay_tron'
  | 'co_lan_im_lang'
  | 'nhan_chu_hai_huoc';

export type LoaiMinhHoaToan =
  | 'tam_giac_vuong'
  | 'truc_so_vo_ti'
  | 'do_thi_ham_so'
  | 'hinh_hoc_chung_minh'
  | 'chuoi_suy_luan';

export type LoaiChuyenCanh = 'mo_dan' | 'quet_ngang' | 'vong_tron_hoat_hinh';

export type KieuCamera = 'tinh' | 'pan_nhe' | 'zoom_cham' | 'zoom_hai_huoc';

export type LoaiDaoCu =
  | 'bang_den'
  | 'cuon_giay'
  | 'bong_den'
  | 'dong_ho_cat'
  | 'can_thang_bang'
  | 'thuoc_compa'
  | 'dau_hoi_cham';

export type HuongNhanVat = 'trai' | 'phai';

export type BangMau = {
  nenChinh: string;
  nenPhu: string;
  luoi: string;
  chuChinh: string;
  chuPhu: string;
  nhanManh: string;
  canhBao: string;
};

export type ThongTinNhanVat = {
  id: string;
  ten: string;
  mauThan: string;
  mauChuDao: string;
  mauDa?: string;
  phuKien: LoaiPhuKien;
};

export type CauHinhCamera = {
  kieu?: KieuCamera;
  zoom?: number;
  panX?: number;
  panY?: number;
  rungNhe?: boolean;
  mucTieuX?: number;
  mucTieuY?: number;
  theoDoiNhanVat?: string;
};

export type NhanVatTrongCanh = {
  id: string;
  x: number;
  y: number;
  huong: HuongNhanVat;
  hanhDong: LoaiHanhDong;
  vatCamTay?: LoaiVatCamTay;
  bieuCam: LoaiBieuCam;
  dangNoi?: boolean;
  bongBongThoai?: string;
  diChuyenDenX?: number;
  tiLe?: number;
};

export type HieuUngHoatHinhItem = {
  loai: LoaiHieuUngHoatHinh;
  x: number;
  y: number;
  tuFrame: number;
  thoiLuong: number;
  chuHienThi?: string;
  mau?: string;
  tiLe?: number;
};

export type LoiBinhHaiHuoc = {
  noiDung: string;
  viTri?: 'goc_phai' | 'goc_trai';
  tuFrame?: number;
};

export type DaoCuTrongCanh = {
  loai: LoaiDaoCu;
  x: number;
  y: number;
  tiLe?: number;
  nhan?: string;
  mau?: string;
};

export type MinhHoaToanData = {
  loai: LoaiMinhHoaToan;
  tieuDe?: string;
  thamSo?: Record<string, number | string | number[]>;
};

export type CongThucLatexItem = {
  latex: string;
  nhan?: string;
  tuFrame?: number;
  noiBat?: boolean;
};

export type MocThoiGianItem = {
  nam: string;
  moTa: string;
  noiBat?: boolean;
};

export type Canh = {
  id: string;
  boCuc: LoaiBoCuc;
  boiCanh: LoaiBoiCanh;
  thoiTiet?: LoaiThoiTiet;
  chuyenCanh?: LoaiChuyenCanh;
  tuFrame: number;
  denFrame: number;
  tieuDeNho?: string;
  namMoc?: string;
  loiThoai: string;
  phuDe?: string[];
  audioSrc?: string;
  camera?: CauHinhCamera;
  nhanVat: NhanVatTrongCanh[];
  hieuUngHoatHinh?: HieuUngHoatHinhItem[];
  loiBinhHaiHuoc?: LoiBinhHaiHuoc;
  daoCu?: DaoCuTrongCanh[];
  minhHoaToan?: MinhHoaToanData;
  congThucLatex?: CongThucLatexItem[];
  mocThoiGian?: MocThoiGianItem[];
};

export type Chuong = {
  id: string;
  tenChuong: string;
  canh: Canh[];
};

export type DuLieuVideoDai = {
  tieuDe: string;
  chuDe: string;
  bangMau: BangMau;
  batSfx?: boolean;
  batPhuDe?: boolean;
  danhSachNhanVat: ThongTinNhanVat[];
  chuong: Chuong[];
};

export const DANH_SACH_LOAI_BO_CUC: readonly LoaiBoCuc[] = [
  'mo_dau',
  'ke_chuyen',
  'doi_thoai',
  'hai_huoc',
  'giai_thich_toan',
  'dong_thoi_gian',
  'ket_thuc',
] as const;

export const DANH_SACH_LOAI_BOI_CANH: readonly LoaiBoiCanh[] = [
  'bo_bien_hy_lap',
  'vuon_tao_dong_que',
  'pho_co_chau_au',
  'rung_nui_thien_nhien',
  'thu_vien_co_dien',
  'lop_hoc_bang_xanh',
  'bau_troi_dem_vu_tru',
  'phong_nen_hai_huoc',
] as const;

export const DANH_SACH_LOAI_THOI_TIET: readonly LoaiThoiTiet[] = [
  'khong',
  'nang_dep',
  'hoang_hon',
  'ban_dem',
  'mua_nhe',
  'la_roi',
  'tuyet_roi',
] as const;

export const DANH_SACH_LOAI_HANH_DONG: readonly LoaiHanhDong[] = [
  'dung_tho',
  'di_bo',
  'chay_voi_va',
  'ngoi_doc_sach',
  'chi_tro_giai_thich',
  'nhin_len_troi',
  'gat_gu_dong_tinh',
  'gai_dau_kho_hieu',
  'giat_minh_nhay_dung',
  'bo_tay_can_loi',
  'khoanh_tay_tu_man',
  'ho_het_sung_suong',
  'di_qua_di_lai',
  'sup_do_tuyet_vong',
] as const;

export const DANH_SACH_LOAI_BIEU_CAM: readonly LoaiBieuCam[] = [
  'binh_thuong',
  'vui_tuoi',
  'ngac_nhien',
  'tuc_gian',
  'hoang_mang',
  'tinh_quai',
  'tram_tu',
  'can_loi_mat_do',
  'tu_man',
] as const;

export const DANH_SACH_LOAI_PHU_KIEN: readonly LoaiPhuKien[] = [
  'khong',
  'vong_nguyet_que',
  'toc_gia_17',
  'kinh_tron',
  'mu_noi_phap',
  'ao_choang',
  'khan_choang',
  'mu_tham_tu',
] as const;

export const DANH_SACH_LOAI_VAT_CAM_TAY: readonly LoaiVatCamTay[] = [
  'khong',
  'cuon_giay',
  'qua_tao',
  'kinh_lup',
  'but_long_ngong',
  'que_chi_bang',
  'den_long',
  'ly_ca_phe',
] as const;

export const DANH_SACH_LOAI_HIEU_UNG_HOAT_HINH: readonly LoaiHieuUngHoatHinh[] = [
  'bong_den_nay_so',
  'giot_mo_hoi',
  'dau_cham_hoi',
  'soc_set_danh',
  'sao_lap_lanh',
  'khoi_chay_tron',
  'co_lan_im_lang',
  'nhan_chu_hai_huoc',
] as const;

export const DANH_SACH_LOAI_MINH_HOA_TOAN: readonly LoaiMinhHoaToan[] = [
  'tam_giac_vuong',
  'truc_so_vo_ti',
  'do_thi_ham_so',
  'hinh_hoc_chung_minh',
  'chuoi_suy_luan',
] as const;
