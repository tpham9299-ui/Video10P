export type LoaiBoCuc =
  | 'mo_dau'
  | 'ke_chuyen'
  | 'doi_thoai'
  | 'hanh_dong'
  | 'giai_thich_toan'
  | 'dong_thoi_gian'
  | 'ket_thuc';

export type LoaiHanhDong =
  | 'dung_tho'
  | 'giang_bai'
  | 'chi_bang'
  | 'suy_nghi_gai_dau'
  | 'soc_lui_lai'
  | 'an_mung_nhay'
  | 'chay_nuoc_rut'
  | 'luot_nhanh_dash'
  | 'nhay_xoay_dap_dat'
  | 'dam_cuong_luc'
  | 'chem_kiem_toan'
  | 'ban_tia_nang_luong'
  | 'do_don_khien'
  | 'bi_danh_vang';

export type LoaiVuKhiToan =
  | 'khong'
  | 'kiem_can2'
  | 'luoi_hai_tich_phan'
  | 'gay_pi'
  | 'khien_so_nguyen'
  | 'tia_vo_cuc';

export type LoaiBieuCam =
  | 'binh_thuong'
  | 'vui'
  | 'ngac_nhien'
  | 'tuc_gian'
  | 'hoang_mang'
  | 'tinh_quai'
  | 'tram_tu';

export type LoaiPhuKien =
  | 'khong'
  | 'vong_nguyet_que'
  | 'toc_gia_17'
  | 'kinh_tron'
  | 'ao_choang'
  | 'khan_choang_bay';

export type LoaiHieuUngTanCong =
  | 'vet_chem'
  | 'song_xung_kich'
  | 'tia_lua_va_cham'
  | 'tia_laser_toan'
  | 'nem_ky_hieu'
  | 'duong_toc_do'
  | 'bui_dat';

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
  mauNangLuong: string;
  phuKien: LoaiPhuKien;
};

export type CauHinhCamera = {
  zoom?: number;
  panX?: number;
  panY?: number;
  theoDoiNhanVat?: string;
};

export type NhanVatTrongCanh = {
  id: string;
  x: number;
  y: number;
  huong: HuongNhanVat;
  hanhDong: LoaiHanhDong;
  vuKhiToan?: LoaiVuKhiToan;
  bieuCam: LoaiBieuCam;
  dangNoi?: boolean;
  bongBongThoai?: string;
  frameRaDon?: number;
};

export type HieuUngTanCongData = {
  loai: LoaiHieuUngTanCong;
  tuX: number;
  tuY: number;
  denX?: number;
  denY?: number;
  mau?: string;
  tuFrame: number;
  thoiLuong: number;
  kyHieuToan?: string;
  hitstopFrames?: number;
  impactFrame?: boolean;
  cuongDoRung?: number;
};

export type DaoCuTrongCanh = {
  loai: LoaiDaoCu;
  x: number;
  y: number;
  tiLe?: number;
  nhan?: string;
  mau?: string;
};

export type CongThucLatexItem = {
  latex: string;
  nhan?: string;
  tuFrame?: number;
  noiBat?: boolean;
};

export type Canh = {
  id: string;
  boCuc: LoaiBoCuc;
  tuFrame: number;
  denFrame: number;
  tieuDeNho?: string;
  namMoc?: string;
  loiThoai: string;
  phuDe?: string[];
  audioSrc?: string;
  camera?: CauHinhCamera;
  nhanVat: NhanVatTrongCanh[];
  hieuUngTanCong?: HieuUngTanCongData[];
  daoCu?: DaoCuTrongCanh[];
  congThucLatex?: CongThucLatexItem[];
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
  'hanh_dong',
  'giai_thich_toan',
  'dong_thoi_gian',
  'ket_thuc',
] as const;

export const DANH_SACH_LOAI_HANH_DONG: readonly LoaiHanhDong[] = [
  'dung_tho',
  'giang_bai',
  'chi_bang',
  'suy_nghi_gai_dau',
  'soc_lui_lai',
  'an_mung_nhay',
  'chay_nuoc_rut',
  'luot_nhanh_dash',
  'nhay_xoay_dap_dat',
  'dam_cuong_luc',
  'chem_kiem_toan',
  'ban_tia_nang_luong',
  'do_don_khien',
  'bi_danh_vang',
] as const;
