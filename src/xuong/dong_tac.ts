import type { LoaiHanhDong } from '../kieu_dai';

export type NhomDongTac = 'dien_xuat' | 'di_chuyen' | 'hai_huoc';

export type ThongTinDongTac = {
  ma: LoaiHanhDong;
  tenHienThi: string;
  nhom: NhomDongTac;
  doDaiGoiY: number;
  moTa: string;
};

export const BANG_DONG_TAC: Record<LoaiHanhDong, ThongTinDongTac> = {
  dung_tho: {
    ma: 'dung_tho',
    tenHienThi: 'Đứng thở',
    nhom: 'dien_xuat',
    doDaiGoiY: 60,
    moTa: 'Tư thế đứng tự nhiên, nhún thở và đung đưa tay nhẹ.',
  },
  di_bo: {
    ma: 'di_bo',
    tenHienThi: 'Đi bộ',
    nhom: 'di_chuyen',
    doDaiGoiY: 75,
    moTa: 'Chu kỳ bước chân và đánh tay đối xứng kèm nhún hông nhẹ.',
  },
  chay_voi_va: {
    ma: 'chay_voi_va',
    tenHienThi: 'Chạy vội vã',
    nhom: 'di_chuyen',
    doDaiGoiY: 48,
    moTa: 'Nghiêng thân về trước, sải chân nhanh đầy năng lượng.',
  },
  ngoi_doc_sach: {
    ma: 'ngoi_doc_sach',
    tenHienThi: 'Ngồi đọc sách',
    nhom: 'dien_xuat',
    doDaiGoiY: 90,
    moTa: 'Ngồi gọn gàng, hai tay nâng cuộn giấy/sách chăm chú đọc.',
  },
  chi_tro_giai_thich: {
    ma: 'chi_tro_giai_thich',
    tenHienThi: 'Chỉ trỏ giải thích',
    nhom: 'dien_xuat',
    doDaiGoiY: 90,
    moTa: 'Vươn tay chỉ bảng hoặc nhấn mạnh luận điểm Toán học.',
  },
  nhin_len_troi: {
    ma: 'nhin_len_troi',
    tenHienThi: 'Nhìn lên trời',
    nhom: 'dien_xuat',
    doDaiGoiY: 75,
    moTa: 'Ngước nhìn bầu trời/chòm sao đầy trầm trồ và cảm hứng.',
  },
  gat_gu_dong_tinh: {
    ma: 'gat_gu_dong_tinh',
    tenHienThi: 'Gật gù đồng tình',
    nhom: 'dien_xuat',
    doDaiGoiY: 60,
    moTa: 'Gật đầu nhịp nhàng tỏ ý tán thành và thích thú.',
  },
  gai_dau_kho_hieu: {
    ma: 'gai_dau_kho_hieu',
    tenHienThi: 'Gãi đầu khó hiểu',
    nhom: 'hai_huoc',
    doDaiGoiY: 60,
    moTa: 'Đưa tay gãi đầu bối rối trước bài toán hóc búa.',
  },
  giat_minh_nhay_dung: {
    ma: 'giat_minh_nhay_dung',
    tenHienThi: 'Giật mình nhảy dựng',
    nhom: 'hai_huoc',
    doDaiGoiY: 42,
    moTa: 'Nhún nhẹ rồi bật nhảy dựng lên đầy bất ngờ rồi rơi xuống.',
  },
  bo_tay_can_loi: {
    ma: 'bo_tay_can_loi',
    tenHienThi: 'Bó tay cạn lời',
    nhom: 'hai_huoc',
    doDaiGoiY: 70,
    moTa: 'Đưa tay vỗ trán bất lực theo phong cách hài hoạt hình.',
  },
  khoanh_tay_tu_man: {
    ma: 'khoanh_tay_tu_man',
    tenHienThi: 'Khoanh tay tự mãn',
    nhom: 'hai_huoc',
    doDaiGoiY: 75,
    moTa: 'Khoanh tay trước ngực, ngửa nhẹ đầu đầy tự tin kiêu hãnh.',
  },
  ho_het_sung_suong: {
    ma: 'ho_het_sung_suong',
    tenHienThi: 'Hò hét sung sướng',
    nhom: 'hai_huoc',
    doDaiGoiY: 54,
    moTa: 'Nhảy cẫng giơ hai tay lên trời ăn mừng phát hiện mới.',
  },
  di_qua_di_lai: {
    ma: 'di_qua_di_lai',
    tenHienThi: 'Đi qua đi lại',
    nhom: 'di_chuyen',
    doDaiGoiY: 90,
    moTa: 'Chắp tay sau lưng đi qua đi lại suy tư tìm lời giải.',
  },
  sup_do_tuyet_vong: {
    ma: 'sup_do_tuyet_vong',
    tenHienThi: 'Sụp đổ tuyệt vọng',
    nhom: 'hai_huoc',
    doDaiGoiY: 75,
    moTa: 'Gục người xuống sàn kịch tính khi lý thuyết bị lung lay.',
  },
};
