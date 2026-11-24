import type { LoaiHanhDong } from '../kieu_dai';

// TODO(v0.2): nang cap xuong khop & VFX

export type ThongTinDongTac = {
  ma: LoaiHanhDong;
  tenHienThi: string;
  doDaiGoiY: number;
  laDonTanCong: boolean;
  moTa: string;
};

export const BANG_DONG_TAC: Record<LoaiHanhDong, ThongTinDongTac> = {
  dung_tho: {
    ma: 'dung_tho',
    tenHienThi: 'Đứng thở',
    doDaiGoiY: 60,
    laDonTanCong: false,
    moTa: 'Tư thế nghỉ cơ bản, nhún thở nhẹ theo chu kỳ.',
  },
  giang_bai: {
    ma: 'giang_bai',
    tenHienThi: 'Giảng bài',
    doDaiGoiY: 75,
    laDonTanCong: false,
    moTa: 'Đưa tay thuyết trình nhấn mạnh luận điểm.',
  },
  chi_bang: {
    ma: 'chi_bang',
    tenHienThi: 'Chỉ bảng',
    doDaiGoiY: 75,
    laDonTanCong: false,
    moTa: 'Vươn tay chỉ về phía công thức trên bảng đen.',
  },
  suy_nghi_gai_dau: {
    ma: 'suy_nghi_gai_dau',
    tenHienThi: 'Suy nghĩ gãi đầu',
    doDaiGoiY: 60,
    laDonTanCong: false,
    moTa: 'Đưa tay lên đầu suy tư trước nghịch lý toán học.',
  },
  soc_lui_lai: {
    ma: 'soc_lui_lai',
    tenHienThi: 'Sốc lùi lại',
    doDaiGoiY: 45,
    laDonTanCong: false,
    moTa: 'Ngả thân về sau vì bất ngờ trước phát hiện mới.',
  },
  an_mung_nhay: {
    ma: 'an_mung_nhay',
    tenHienThi: 'Ăn mừng nhảy',
    doDaiGoiY: 45,
    laDonTanCong: false,
    moTa: 'Bật nhảy giơ hai tay mừng chứng minh thành công.',
  },
  chay_nuoc_rut: {
    ma: 'chay_nuoc_rut',
    tenHienThi: 'Chạy nước rút',
    doDaiGoiY: 45,
    laDonTanCong: false,
    moTa: 'Nghiêng thân về trước, sải chân di chuyển nhanh.',
  },
  luot_nhanh_dash: {
    ma: 'luot_nhanh_dash',
    tenHienThi: 'Lướt nhanh (Dash)',
    doDaiGoiY: 24,
    laDonTanCong: false,
    moTa: 'Lao vụt về phía trước tạo đà tiếp cận đối thủ.',
  },
  nhay_xoay_dap_dat: {
    ma: 'nhay_xoay_dap_dat',
    tenHienThi: 'Nhảy xoay đáp đất',
    doDaiGoiY: 36,
    laDonTanCong: true,
    moTa: 'Bật cao xoay người rồi giáng lực xuống mặt đất.',
  },
  dam_cuong_luc: {
    ma: 'dam_cuong_luc',
    tenHienThi: 'Đấm cường lực',
    doDaiGoiY: 30,
    laDonTanCong: true,
    moTa: 'Thu tay tích lực và tung cú đấm mạnh về trước.',
  },
  chem_kiem_toan: {
    ma: 'chem_kiem_toan',
    tenHienThi: 'Chém kiếm Toán',
    doDaiGoiY: 32,
    laDonTanCong: true,
    moTa: 'Vung vũ khí toán học tạo đường chém sắc nét.',
  },
  ban_tia_nang_luong: {
    ma: 'ban_tia_nang_luong',
    tenHienThi: 'Bắn tia năng lượng',
    doDaiGoiY: 40,
    laDonTanCong: true,
    moTa: 'Đưa hai tay phóng tia năng lượng công thức.',
  },
  do_don_khien: {
    ma: 'do_don_khien',
    tenHienThi: 'Đỡ đòn khiên',
    doDaiGoiY: 36,
    laDonTanCong: false,
    moTa: 'Nâng khiên số nguyên chắn trước thân chống đỡ.',
  },
  bi_danh_vang: {
    ma: 'bi_danh_vang',
    tenHienThi: 'Bị đánh văng',
    doDaiGoiY: 30,
    laDonTanCong: false,
    moTa: 'Bật ngược ra sau khi trúng đòn phản chứng.',
  },
};
