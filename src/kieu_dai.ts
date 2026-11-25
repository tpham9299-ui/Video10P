export type LoaiBoCuc =
  | 'mo_dau'
  | 'ke_chuyen'
  | 'doi_thoai'
  | 'hai_huoc'
  | 'giai_thich_toan'
  | 'dong_thoi_gian'
  | 'ban_do_hanh_trinh'
  | 'bao_chi_co'
  | 'phan_ung_cam'
  | 'ket_thuc';

/** 4 sac thai nhac nen theo tung Hoi (v3.5) */
export type TamTrangNhac = 'vui_tuoi' | 'bi_an' | 'kich_tinh' | 'tram_lang';

/** 4 bieu tuong di chuyen tren CanhBanDoHanhTrinh (v3.5) */
export type PhuongTienHanhTrinh = 'tau_thuy' | 'thu_tay' | 'nguoi_di_bo' | 'xe_ngua';

export type BanDoHanhTrinhData = {
  diemDi: string;
  diemDen: string;
  phuongTien?: PhuongTienHanhTrinh;
  khoangCachNhan?: string;
  moTaHanhTrinh?: string;
  diemDungGiua?: string;
};

/** Du lieu cho CanhBaoChiCo (v3.5): to bao giay co xoay/phong ra man hinh */
export type BaoChiCoData = {
  tenToBao?: string;
  ngayPhatHanh?: string;
  tieuDeBao: string;
  tieuDePhu?: string;
  nhanAnhMinhHoa?: string;
  daoCuMinhHoa?: LoaiDaoCu;
  congThucMinhHoa?: string;
};

/** 4 kieu phan ung cam nhanh 1.5-2.5s cho CanhPhanUngCam (v3.5) */
export type KieuPhanUngCam = 'nhap_tra' | 'nhuong_may' | 'tron_mat' | 'can_loi';

export type PhanUngCamData = {
  nhanVatId?: string;
  kieuPhanUng?: KieuPhanUngCam;
  chuHieuUng?: string;
};

/** Cau hinh vung YouTube End-Screen 15 giay cuoi cua CanhKet (v3.5) */
export type CauHinhEndScreen = {
  khungTraiNhan?: string;
  khungPhaiNhan?: string;
  loiDanXemTiep?: string;
};

/** Cau hinh tuy chinh Mascot dan chuyen cua kenh (v3.5) */
export type CauHinhMascotKenh = Partial<ThongTinNhanVat> & {
  batMascot?: boolean;
};

export type LoaiBoiCanh =
  | 'bo_bien_hy_lap'
  | 'vuon_tao_dong_que'
  | 'pho_co_chau_au'
  | 'rung_nui_thien_nhien'
  | 'thu_vien_co_dien'
  | 'lop_hoc_bang_xanh'
  | 'bau_troi_dem_vu_tru'
  | 'phong_nen_hai_huoc'
  | 'quang_truong_hy_lap'
  | 'thu_vien_trung_co'
  | 'dai_thien_van_phuc_hung'
  | 'giang_duong_hien_dai'
  | 'nha_co_phong_sinh'
  | 'cang_bien_tau_thuy'
  | 'phong_tro_bep_lua'
  | 'phong_benh_vien'
  | 'duong_pho_xe_co'
  | 'giang_duong_dai_hoc'
  | 'san_truong_co_dien'
  | 'phong_thi_nghiem_co'
  | 'khong_gian_vu_tru_toan'
  | 'lang_que_an_do_a_dong';

/** 10 loai sinh vat & do vat moi truong song dong tat dinh (v2.0 Buoc 3) */
export type LoaiVatTheXungQuanh =
  | 'chim_hai_au'
  | 'chim_san_truong'
  | 'ca_gon_song'
  | 'buom_vuon'
  | 'hoi_khoi'
  | 'ngon_nen_den_dau'
  | 'la_vang_gio'
  | 'tuyet_cua_so'
  | 'xe_taxi_co'
  | 'dong_ho_qua_lac';

export type VatTheXungQuanh = {
  loai: LoaiVatTheXungQuanh;
  x?: number;
  y?: number;
  tiLe?: number;
  soLuong?: number;
  tocDo?: number;
  mau?: string;
  /** Bien so xe tuy chinh cho xe_taxi_co (vi du: "1729") */
  bienSoXe?: string;
};

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
  | 'sup_do_tuyet_vong'
  | 'trao_thu'
  | 'chi_bang_giang_bai'
  | 'quay_nhin_doi_thoai'
  | 'bat_tay'
  | 'giat_minh_bat_day'
  | 'quay_nhin_khan_gia';

/** 12 goc quay dao dien chuyen nghiep (v2.0 + 4 goc can mat & dao goc v3.0) */
export type GocQuayCamera =
  | 'toan_canh'
  | 'trung_canh'
  | 'can_mat'
  | 'focus_trai'
  | 'focus_phai'
  | 'zoom_dao_cu'
  | 'pan_ngang'
  | 'chia_doi_man_hinh'
  | 'can_mat_trai'
  | 'can_mat_phai'
  | 'can_mat_kich_tinh'
  | 'dao_goc_can_mat';

/** 4 kieu bong bong chat hoat hinh truyen tranh (v3.0) */
export type KieuBongBongChat = 'thuong' | 'quat_thao' | 'suy_nghi' | 'ca_khia';

/** Phan loai nhip/loai canh de dao dien & dien xuat tuong tac (v2.0) */
export type LoaiCanh =
  | 'ke_chuyen'
  | 'doi_thoai'
  | 'tuong_tac_khan_gia'
  | 'giang_toan'
  | 'chuyen_canh_lich_su';

/** 4 bien the do tuoi hinh the nhan vat (v2.0) */
export type DoTuoiNhanVat =
  | 'so_sinh'
  | 'thieu_nien'
  | 'truong_thanh'
  | 'gia';

/** 5 tu the boi canh cua nhan vat (v2.0) */
export type TuTheNhanVat =
  | 'dung'
  | 'ngoi_ban'
  | 'nam_giuong'
  | 'om_em_be'
  | 'mac_ao_khoac';

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
  | 'nhan_chu_hai_huoc'
  | 'mo_hoi_lon'
  | 'khoi_boc_tai'
  | 'mat_xoan_oc'
  | 'cham_hoi_nay'
  | 'tia_toc_do'
  | 'bong_den_y_tuong';

export type LoaiMinhHoaToan =
  | 'tam_giac_vuong'
  | 'truc_so_vo_ti'
  | 'do_thi_ham_so'
  | 'hinh_hoc_chung_minh'
  | 'chuoi_suy_luan'
  | 'tung_buoc'
  | 'so_do_anh_xa'
  | 'luoi_duong_cheo'
  | 'bieu_do_cot';

export type LoaiChuyenCanh = 'mo_dan' | 'quet_ngang' | 'vong_tron_hoat_hinh';

export type KieuCamera = 'tinh' | 'pan_nhe' | 'zoom_cham' | 'zoom_hai_huoc';

export type LoaiDaoCu =
  | 'bang_den'
  | 'cuon_giay'
  | 'bong_den'
  | 'dong_ho_cat'
  | 'can_thang_bang'
  | 'thuoc_compa'
  | 'dau_hoi_cham'
  | 'compa_co'
  | 'ban_tinh_co'
  | 'khoi_da_dien'
  | 'kinh_thien_van'
  | 'noi_em_be'
  | 'noi_sup'
  | 'phong_bi_thu_tay'
  | 'giuong_benh'
  | 'bien_so_xe'
  | 'tach_tra_nong'
  | 'tau_thuy'
  | 'ban_hoc_den_dau'
  | 'qua_dia_cau';

export type HuongNhanVat = 'trai' | 'phai';

/** Vai noi tuy chon de phan giong Edge TTS (tuong thich nguoc khi khong khai bao) */
export type VaiNoi = 'nguoi_dan' | 'nhan_vat' | 'binh_luan_hai';

export type BangMau = {
  nenChinh: string;
  nenPhu: string;
  luoi: string;
  chuChinh: string;
  chuPhu: string;
  nhanManh: string;
  canhBao: string;
};

/** 5 nhom anh sang moi truong phan tich tu nen AI (v3.0) */
export type LoaiAnhSangMoiTruong =
  | 'nang_am'
  | 'anh_nen'
  | 'dem_lanh'
  | 'trung_tinh'
  | 'hoang_hon';

/** Thong so anh sang moi truong de dong bo mau sac & do toi giua nen AI va nhan vat (v3.0) */
export type AnhSangMoiTruong = {
  /** Ma hex tong sang chu dao (vi du: "#F4D99B") */
  mauAm: string;
  /** Muc do toi cua moi truong trong [0..1] (0 = sang nhat, 1 = toi nhat) */
  doToi: number;
  /** Phan loai anh sang moi truong (nang_am | anh_nen | dem_lanh | trung_tinh | hoang_hon) */
  loaiAnhSang: LoaiAnhSangMoiTruong | string;
};

/** 7 bo trang phuc lich su / truyen tranh chi tiet 2 sac do cho nhan vat (v3.0) */
export type LoaiTrangPhuc =
  | 'ao_vest_co_dien'
  | 'ao_choang_hoc_gia'
  | 'ao_co_an_do'
  | 'ao_len_mua_dong'
  | 'ao_choang_hy_lap'
  | 'quan_phuc_co'
  | 'thuong_dan';

/** 7 kieu toc & mu dac trung nhan vat lich su (v3.0) */
export type LoaiKieuToc =
  | 'gon_gang'
  | 'xoan_co_dien'
  | 'toc_bac_dai'
  | 'khan_quan'
  | 'mu_rong_vanh'
  | 'mu_noi'
  | 'hoi_hoi';

/** 4 kieu rau dac trung nhan vat lich su (v3.0) */
export type LoaiCoRau = 'khong' | 'ria_mep' | 'rau_quai_non' | 'rau_bac_dai';

/** 3 tam khung hinh nhan vat (v3.0) */
export type TamKhungNhanVat = 'toan_canh' | 'ban_than' | 'can_mat';

export type ThongTinNhanVat = {
  id: string;
  ten: string;
  mauThan: string;
  mauChuDao: string;
  mauDa?: string;
  phuKien: LoaiPhuKien;
  /** Do tuoi mac dinh cua nhan vat (tuy chon, co the ghi de tung canh) */
  doTuoi?: DoTuoiNhanVat;
  /** Trang phuc mac dinh cua nhan vat (v3.0, tuy chon) */
  trangPhuc?: LoaiTrangPhuc;
  /** Kieu toc/mu mac dinh cua nhan vat (v3.0, tuy chon) */
  kieuToc?: LoaiKieuToc;
  /** Kieu rau mac dinh cua nhan vat (v3.0, tuy chon) */
  coRau?: LoaiCoRau;
  /** Mau ao chinh tuy chinh (v3.0, tuy chon - fallback mauChuDao) */
  mauAo?: string;
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

/** Cau hinh may quay dao dien v2.0 (tuong thich nguoc 100% voi camera cu) */
export type DiemTieuCu = {
  x: number;
  y: number;
};

export type CauHinhMayQuay = {
  gocQuay?: GocQuayCamera;
  /** Ti le phong dai (scale), vi du 1.0 - 1.7 */
  doPhong?: number;
  /** Toa do diem tieu cu tren khung 1920x1080 */
  diemTieuCu?: DiemTieuCu;
  /** Tu dong lia & zoom nhe (1.2x-1.45x) sang nhan vat dang noi / co bien do RMS */
  tuDongFocusNguoiNoi?: boolean;
  /** Tuy chon rung nhe kich tinh */
  rungNhe?: boolean;
};

/** Moc doi bieu cam nhieu lan trong 1 canh theo frame hoac tien do [0..1] */
export type BieuCamTheoMoc = {
  /** Frame cuc bo trong canh (uu tien neu khai bao) */
  tuFrame?: number;
  /** Tien do tuong doi trong canh [0..1] (dung khi khong khai bao tuFrame) */
  tienDo?: number;
  bieuCam: LoaiBieuCam;
};

/** Mot luot thoai trong canh doi thoai nhieu luot (v2.0 + kieuBongBong v3.0) */
export type LuotThoai = {
  nhanVatId: string;
  noiDung: string;
  bieuCam?: LoaiBieuCam;
  dongTac?: LoaiHanhDong;
  /** Kieu bong bong chat truyen tranh cho luot thoai (thuong | quat_thao | suy_nghi | ca_khia) */
  kieuBongBong?: KieuBongBongChat;
  batDauFrame: number;
  ketThucFrame: number;
  /** Mang bien do RMS tuy chon rieng cho luot thoai nay */
  bienDoAmThanh?: number[];
};

/** Cau hoi tuong tac khan gia co dong ho dem nguoc 3 giay + hop dap an (v2.0) */
export type CauHoiTuongTac = {
  cauHoi: string;
  /** Thoi gian dem nguoc (giay), mac dinh 3 giay */
  thoiGianDemNguocGiay?: number;
  /** Frame cuc bo bat dau dem nguoc (mac dinh tinh tu dong dau canh) */
  batDauDemNguocFrame?: number;
  /** Cac phuong an goi y tuy chon (trac nghiem) */
  luaChon?: string[];
  /** Dap an hien ra sau khi het dem nguoc */
  dapAn: string;
  /** Giai thich ngan gon kem dap an (tuy chon) */
  giaiThichNgan?: string;
  /** Frame cuc bo bat dau hien dap an (mac dinh = batDauDemNguocFrame + thoiGianDemNguocGiay * 30) */
  hienDapAnTuFrame?: number;
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
  /** Kieu bong bong chat truyen tranh (thuong | quat_thao | suy_nghi | ca_khia) (v3.0) */
  kieuBongBong?: KieuBongBongChat;
  diChuyenDenX?: number;
  tiLe?: number;
  /** Mang bien do RMS tuy chon rieng cho nhan vat (uu tien hon canh.bienDoAmThanh neu co) */
  bienDoAmThanh?: number[];
  /** Bien the do tuoi hinh the trong canh nay (ghi de ThongTinNhanVat.doTuoi) */
  doTuoi?: DoTuoiNhanVat;
  /** Tu the boi canh cua nhan vat (dung, ngoi_ban, nam_giuong, om_em_be, mac_ao_khoac) */
  tuThe?: TuTheNhanVat;
  /** Cho phep doi bieu cam nhieu lan trong 1 canh theo moc frame hoac tien do */
  bieuCamTheoMoc?: BieuCamTheoMoc[];
  /** ID nhan vat khac (hoac 'khan_gia') de quay mat/anh mat nhin ve phia doi tuong tuong tac */
  tuongTacVoi?: string;
  /** Trang phuc truyen tranh 2 sac do cua nhan vat trong canh nay (v3.0, ghi de ThongTinNhanVat) */
  trangPhuc?: LoaiTrangPhuc;
  /** Kieu toc/mu cua nhan vat trong canh nay (v3.0, ghi de ThongTinNhanVat) */
  kieuToc?: LoaiKieuToc;
  /** Kieu rau cua nhan vat trong canh nay (v3.0, ghi de ThongTinNhanVat) */
  coRau?: LoaiCoRau;
  /** Mau ao tuy chinh trong canh nay (v3.0, ghi de ThongTinNhanVat) */
  mauAo?: string;
  /** Tam khung hinh nhan vat trong canh (toan_canh | ban_than | can_mat) (v3.0) */
  tamKhung?: TamKhungNhanVat;
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
  /** Bien so xe tuy chinh cho dao cu bien_so_xe (vi du: "1729") */
  bienSoXe?: string;
};

export type KhungToaDoToan = {
  xMin?: number;
  xMax?: number;
  yMin?: number;
  yMax?: number;
  hienLuoi?: boolean;
  hienTruc?: boolean;
  nhanX?: string;
  nhanY?: string;
  mauTruc?: string;
  heToaDo?: 'toan' | 'svg';
};

export type LoaiHamDoThi = 'parabol' | 'sin' | 'cos' | 'bac_ba' | 'mu' | 'tuyen_tinh';

export type BuocVeToan =
  | {
      loai: 'diem';
      x: number;
      y: number;
      nhan?: string;
      mau?: string;
      banKinh?: number;
      tuFrame?: number;
      thoiLuong?: number;
    }
  | {
      loai: 'doan_thang';
      x1: number;
      y1: number;
      x2: number;
      y2: number;
      nhan?: string;
      mau?: string;
      doDay?: number;
      netDut?: boolean;
      muiTen?: boolean;
      tuFrame?: number;
      thoiLuong?: number;
    }
  | {
      loai: 'cung_tron';
      cx: number;
      cy: number;
      r: number;
      gocBatDau?: number;
      gocKetThuc?: number;
      nhan?: string;
      mau?: string;
      mauTo?: string;
      doDay?: number;
      tuFrame?: number;
      thoiLuong?: number;
    }
  | {
      loai: 'da_giac';
      diem: [number, number][];
      diemDich?: [number, number][];
      nhan?: string;
      mau?: string;
      mauTo?: string;
      doMoTo?: number;
      tuFrame?: number;
      thoiLuong?: number;
    }
  | {
      loai: 'truc_toa_do';
      xMin?: number;
      xMax?: number;
      yMin?: number;
      yMax?: number;
      hienLuoi?: boolean;
      nhanX?: string;
      nhanY?: string;
      mau?: string;
      tuFrame?: number;
      thoiLuong?: number;
    }
  | {
      loai: 'duong_cong';
      diem?: [number, number][];
      ham?: LoaiHamDoThi;
      heSoA?: number;
      heSoB?: number;
      heSoC?: number;
      xTu?: number;
      xDen?: number;
      nhan?: string;
      mau?: string;
      doDay?: number;
      tuFrame?: number;
      thoiLuong?: number;
    }
  | {
      loai: 'nhan_chu';
      x: number;
      y: number;
      noiDung: string;
      mau?: string;
      coChu?: number;
      tuFrame?: number;
      thoiLuong?: number;
    };

export type MinhHoaToanData = {
  loai: LoaiMinhHoaToan;
  tieuDe?: string;
  thamSo?: Record<string, number | string | number[] | string[]>;
  /** Cau hinh he toa do cho dang minh hoa "tung_buoc" */
  khungToaDo?: KhungToaDoToan;
  /** Danh sach doi tuong hinh hoc/do thi xuat hien tuan tu theo frame (cho loai="tung_buoc") */
  buocVe?: BuocVeToan[];
  /** Chu thich tong ket cuoi hinh minh hoa */
  chuThichCuoi?: string;
  /** Mau nhan manh tuy chinh tu JSON cho bieu do / diem nhan */
  mauNhanManh?: string;
};

export type BienTheThumbnail = 1 | 2 | 3;

export type PhuongAnThumbnail = {
  bien_the: BienTheThumbnail;
  /** Dong chu lon toi da 2-4 tu, tuong phan cao de doc ro tren dien thoai */
  tieuDeLon: string;
  /** The nhan ngan phia tren/goc (tuy chon) */
  nhanPhu?: string;
  /** 1 cong thuc KaTeX noi bat */
  congThucLatex?: string;
  /** Vat the/dao cu Toan hoc cot loi */
  daoCuNoiBat?: LoaiDaoCu;
  /** Boi canh nen tuy chon */
  boiCanh?: LoaiBoiCanh;
  thoiTiet?: LoaiThoiTiet;
  /** Nhan vat phong lon voi bieu cam tuong phan cao */
  nhanVat?: ThongTinNhanVat;
  bieuCam?: LoaiBieuCam;
  hanhDong?: LoaiHanhDong;
  vatCamTay?: LoaiVatCamTay;
  mauNhan?: string;
  mauNen?: string;
  /** Anh boi canh AI dep nhat cua tap de uu tien lam phong nen Thumbnail v3.5 */
  anhBoiCanh?: string | null;
  /** Thong so anh sang moi truong dong bo voi anhBoiCanh */
  anhSangMoiTruong?: AnhSangMoiTruong;
};

export type DuLieuThumbnail = PhuongAnThumbnail & {
  tieuDeVideo?: string;
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
  /** Dong mo ta rieng cho canh mo hoi (khong dung chung 1 cau cho nhieu hoi) */
  phuDeHoi?: string;
  namMoc?: string;
  loiThoai: string;
  /** Nhan vai noi tuy chon cho TTS da giong (nguoi_dan | nhan_vat | binh_luan_hai) */
  vaiNoi?: VaiNoi;
  /** Khoang nghi dau canh tuy chon (giay) de dong bo nhip punchline/phu de */
  nghiDauGiay?: number;
  phuDe?: string[];
  audioSrc?: string;
  /** Mang bien do am thanh RMS chuan hoa [0..1] theo tung frame 30fps (tuy chon, tuong thich nguoc) */
  bienDoAmThanh?: number[];
  camera?: CauHinhCamera;
  /** Cau hinh may quay dao dien v2.0 (8 goc quay + tuDongFocusNguoiNoi) */
  mayQuay?: CauHinhMayQuay;
  /** Phan loai canh v2.0 (ke_chuyen, doi_thoai, tuong_tac_khan_gia, giang_toan, chuyen_canh_lich_su) */
  loaiCanh?: LoaiCanh;
  /** Danh sach luot thoai nhieu nhan vat trong cung 1 canh (v2.0) */
  luotThoai?: LuotThoai[];
  /** Cau hoi tuong tac khan gia co dem nguoc 3 giay + dap an (v2.0) */
  cauHoiTuongTac?: CauHoiTuongTac;
  /** Danh sach sinh vat & do vat moi truong song dong tuy chinh trong canh (v2.0 Buoc 3) */
  vatTheXungQuanh?: VatTheXungQuanh[];
  /** Bien so xe tuy chinh cho xe taxi co trong canh (vi du: "1729") */
  bienSoXe?: string;
  /** Duong dan tuong doi trong public/ toi anh boi canh minh hoa AI (v3.0, null/undefined -> dung SVG) */
  anhBoiCanh?: string | null;
  /** Thong so anh sang moi truong phan tich tu anh nen AI de dong bo len nhan vat (v3.0) */
  anhSangMoiTruong?: AnhSangMoiTruong;
  /** Bat che do khung tranh dac ta can canh vat the/phong canh (khong ve nhan vat, chi Ken Burns + hat anh sang) (v3.0) */
  laKhungTranhDacTa?: boolean;
  /** Du lieu ban do hanh trinh co (v3.5) cho boCuc='ban_do_hanh_trinh' */
  banDoHanhTrinh?: BanDoHanhTrinhData;
  /** Du lieu to bao giay co giat gan (v3.5) cho boCuc='bao_chi_co' */
  baoChiCo?: BaoChiCoData;
  /** Du lieu canh cat nhanh phan ung cam 1.5-2.5s (v3.5) cho boCuc='phan_ung_cam' */
  phanUngCam?: PhanUngCamData;
  /** Danh dau ngat nhac nen 0.8s dot ngot truoc cau punchline hai (v3.5) */
  ngatNhacPunchline?: boolean;
  /** Cau hinh 2 o End-Screen YouTube cho canh ket_thuc (v3.5) */
  endScreen?: CauHinhEndScreen;
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
  /** Dong mo ta rieng biet cua hoi (hien thi khi mo hoi, cam dung chung 1 cau cho nhieu hoi) */
  phuDeHoi?: string;
  /** Sac thai nhac nen chu dao cua hoi (v3.5: vui_tuoi | bi_an | kich_tinh | tram_lang) */
  tamTrangNhac?: TamTrangNhac;
  /** Cau moc noi Open Loop cuoi hoi keo nguoi xem sang hoi tiep theo (v3.5) */
  openLoopCuoiHoi?: string;
  canh: Canh[];
};

export type DuLieuVideoDai = {
  tieuDe: string;
  chuDe: string;
  bangMau: BangMau;
  batSfx?: boolean;
  batPhuDe?: boolean;
  danhSachNhanVat: ThongTinNhanVat[];
  /** Ho so tuy chinh Mascot dan chuyen co dinh cua kenh (v3.5, tuy chon) */
  mascotKenh?: CauHinhMascotKenh;
  chuong: Chuong[];
  /** 3 phuong an goi y Thumbnail A/B (tuy chon, tuong thich nguoc 100%) */
  goiYThumbnail?: PhuongAnThumbnail[];
};

export const DANH_SACH_LOAI_BO_CUC: readonly LoaiBoCuc[] = [
  'mo_dau',
  'ke_chuyen',
  'doi_thoai',
  'hai_huoc',
  'giai_thich_toan',
  'dong_thoi_gian',
  'ban_do_hanh_trinh',
  'bao_chi_co',
  'phan_ung_cam',
  'ket_thuc',
] as const;

export const DANH_SACH_TAM_TRANG_NHAC: readonly TamTrangNhac[] = [
  'vui_tuoi',
  'bi_an',
  'kich_tinh',
  'tram_lang',
] as const;

export const DANH_SACH_PHUONG_TIEN_HANH_TRINH: readonly PhuongTienHanhTrinh[] = [
  'tau_thuy',
  'thu_tay',
  'nguoi_di_bo',
  'xe_ngua',
] as const;

export const DANH_SACH_KIEU_PHAN_UNG_CAM: readonly KieuPhanUngCam[] = [
  'nhap_tra',
  'nhuong_may',
  'tron_mat',
  'can_loi',
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
  'quang_truong_hy_lap',
  'thu_vien_trung_co',
  'dai_thien_van_phuc_hung',
  'giang_duong_hien_dai',
  'nha_co_phong_sinh',
  'cang_bien_tau_thuy',
  'phong_tro_bep_lua',
  'phong_benh_vien',
  'duong_pho_xe_co',
  'giang_duong_dai_hoc',
  'san_truong_co_dien',
  'phong_thi_nghiem_co',
  'khong_gian_vu_tru_toan',
  'lang_que_an_do_a_dong',
] as const;

export const DANH_SACH_LOAI_VAT_THE_XUNG_QUANH: readonly LoaiVatTheXungQuanh[] = [
  'chim_hai_au',
  'chim_san_truong',
  'ca_gon_song',
  'buom_vuon',
  'hoi_khoi',
  'ngon_nen_den_dau',
  'la_vang_gio',
  'tuyet_cua_so',
  'xe_taxi_co',
  'dong_ho_qua_lac',
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
  'trao_thu',
  'chi_bang_giang_bai',
  'quay_nhin_doi_thoai',
  'bat_tay',
  'giat_minh_bat_day',
  'quay_nhin_khan_gia',
] as const;

export const DANH_SACH_GOC_QUAY: readonly GocQuayCamera[] = [
  'toan_canh',
  'trung_canh',
  'can_mat',
  'focus_trai',
  'focus_phai',
  'zoom_dao_cu',
  'pan_ngang',
  'chia_doi_man_hinh',
  'can_mat_trai',
  'can_mat_phai',
  'can_mat_kich_tinh',
  'dao_goc_can_mat',
] as const;

export const DANH_SACH_KIEU_BONG_BONG: readonly KieuBongBongChat[] = [
  'thuong',
  'quat_thao',
  'suy_nghi',
  'ca_khia',
] as const;

export const DANH_SACH_LOAI_CANH: readonly LoaiCanh[] = [
  'ke_chuyen',
  'doi_thoai',
  'tuong_tac_khan_gia',
  'giang_toan',
  'chuyen_canh_lich_su',
] as const;

export const DANH_SACH_DO_TUOI: readonly DoTuoiNhanVat[] = [
  'so_sinh',
  'thieu_nien',
  'truong_thanh',
  'gia',
] as const;

export const DANH_SACH_TU_THE: readonly TuTheNhanVat[] = [
  'dung',
  'ngoi_ban',
  'nam_giuong',
  'om_em_be',
  'mac_ao_khoac',
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
  'mo_hoi_lon',
  'khoi_boc_tai',
  'mat_xoan_oc',
  'cham_hoi_nay',
  'tia_toc_do',
  'bong_den_y_tuong',
] as const;

export const DANH_SACH_LOAI_MINH_HOA_TOAN: readonly LoaiMinhHoaToan[] = [
  'tam_giac_vuong',
  'truc_so_vo_ti',
  'do_thi_ham_so',
  'hinh_hoc_chung_minh',
  'chuoi_suy_luan',
  'tung_buoc',
  'so_do_anh_xa',
  'luoi_duong_cheo',
  'bieu_do_cot',
] as const;

export const DANH_SACH_LOAI_DAO_CU: readonly LoaiDaoCu[] = [
  'bang_den',
  'cuon_giay',
  'bong_den',
  'dong_ho_cat',
  'can_thang_bang',
  'thuoc_compa',
  'dau_hoi_cham',
  'compa_co',
  'ban_tinh_co',
  'khoi_da_dien',
  'kinh_thien_van',
  'noi_em_be',
  'noi_sup',
  'phong_bi_thu_tay',
  'giuong_benh',
  'bien_so_xe',
  'tach_tra_nong',
  'tau_thuy',
  'ban_hoc_den_dau',
  'qua_dia_cau',
] as const;

export const DANH_SACH_VAI_NOI: readonly VaiNoi[] = [
  'nguoi_dan',
  'nhan_vat',
  'binh_luan_hai',
] as const;

export const DANH_SACH_TRANG_PHUC: readonly LoaiTrangPhuc[] = [
  'ao_vest_co_dien',
  'ao_choang_hoc_gia',
  'ao_co_an_do',
  'ao_len_mua_dong',
  'ao_choang_hy_lap',
  'quan_phuc_co',
  'thuong_dan',
] as const;

export const DANH_SACH_KIEU_TOC: readonly LoaiKieuToc[] = [
  'gon_gang',
  'xoan_co_dien',
  'toc_bac_dai',
  'khan_quan',
  'mu_rong_vanh',
  'mu_noi',
  'hoi_hoi',
] as const;

export const DANH_SACH_CO_RAU: readonly LoaiCoRau[] = [
  'khong',
  'ria_mep',
  'rau_quai_non',
  'rau_bac_dai',
] as const;

export const DANH_SACH_TAM_KHUNG: readonly TamKhungNhanVat[] = [
  'toan_canh',
  'ban_than',
  'can_mat',
] as const;

export const DANH_SACH_LOAI_ANH_SANG: readonly LoaiAnhSangMoiTruong[] = [
  'nang_am',
  'anh_nen',
  'dem_lanh',
  'trung_tinh',
  'hoang_hon',
] as const;
