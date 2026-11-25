import type { LoaiHanhDong } from '../kieu_dai';
import {
  baoToanCoGian,
  easeInBack,
  easeInOutCubic,
  easeOutBack,
  kepGiaTri,
  noiSuy,
  springTatDinh,
} from './duong_cong.ts';

export type NhomDongTac = 'dien_xuat' | 'di_chuyen' | 'hai_huoc';

export type ThongTinDongTac = {
  ma: LoaiHanhDong;
  tenHienThi: string;
  nhom: NhomDongTac;
  doDaiGoiY: number;
  moTa: string;
};

/**
 * Tap tham so goc khop & co gian FK cho tung frame.
 * Quy uoc goc (do, theo he toa do huong nhin cua nhan vat):
 * - gocThan: 0 = thang dung, duong = nghieng ve truoc, am = nga ve sau
 * - gocDau: duong = cui/gat xuong, am = ngua/nhin len
 * - vaiGoc / duiGoc: 0 = thang xuong dat, duong = dua ve truoc/len, am = dua ve sau
 * - khuyuGoc: duong = gap khuyu tu nhien ve truoc/len
 * - goiGoc: am = gap goi tu nhien ve sau
 */
export type ThongSoTuTheFK = {
  offsetX: number;
  offsetY: number;
  squashX: number;
  squashY: number;
  gocThan: number;
  doCongThan: number;
  gocDau: number;
  nhunVai: number;
  vaiPhaiGoc: number;
  khuyuPhaiGoc: number;
  vaiTraiGoc: number;
  khuyuTraiGoc: number;
  duiPhaiGoc: number;
  goiPhaiGoc: number;
  duiTraiGoc: number;
  goiTraiGoc: number;
  nhayY: number;
  dichNgangNoiBo: number;
  khoaMatDat: boolean;
  coVetBui: boolean;
  huongNhinX: number;
  huongNhinY: number;
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
    moTa: 'Chu kỳ 4 pha Contact-Down-Passing-Up, hông nhún 2 nhịp và tay đánh lệch pha.',
  },
  chay_voi_va: {
    ma: 'chay_voi_va',
    tenHienThi: 'Chạy vội vã',
    nhom: 'di_chuyen',
    doDaiGoiY: 48,
    moTa: 'Thân nghiêng về trước 18–22°, đạp chân cao kèm vệt bụi nhỏ dưới gót.',
  },
  ngoi_doc_sach: {
    ma: 'ngoi_doc_sach',
    tenHienThi: 'Ngồi đọc sách',
    nhom: 'dien_xuat',
    doDaiGoiY: 90,
    moTa: 'Ngồi gọn gàng, lưng cong nhẹ, hai tay nâng cuộn giấy/sách chăm chú đọc.',
  },
  chi_tro_giai_thich: {
    ma: 'chi_tro_giai_thich',
    tenHienThi: 'Chỉ trỏ giải thích',
    nhom: 'dien_xuat',
    doDaiGoiY: 90,
    moTa: 'Tay cầm que chỉ đưa nhịp nhàng hướng vào bảng và công thức đang sáng.',
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
    moTa: 'Gật đầu nhịp nhàng kèm lấy đà nhẹ tỏ ý tán thành thích thú.',
  },
  gai_dau_kho_hieu: {
    ma: 'gai_dau_kho_hieu',
    tenHienThi: 'Gãi đầu khó hiểu',
    nhom: 'hai_huoc',
    doDaiGoiY: 60,
    moTa: 'Lấy đà rồi đưa tay gãi đầu bối rối trước bài toán hóc búa.',
  },
  giat_minh_nhay_dung: {
    ma: 'giat_minh_nhay_dung',
    tenHienThi: 'Giật mình nhảy dựng',
    nhom: 'hai_huoc',
    doDaiGoiY: 48,
    moTa: 'Ép thấp lấy đà (squash) → bật vọt kéo dài → lơ lửng 4 frame → đáp đất nhún lò xo.',
  },
  bo_tay_can_loi: {
    ma: 'bo_tay_can_loi',
    tenHienThi: 'Bó tay cạn lời',
    nhom: 'hai_huoc',
    doDaiGoiY: 70,
    moTa: 'Hít sâu lấy đà rồi vỗ trán bất lực, vai sụp xuống đầy biểu cảm.',
  },
  khoanh_tay_tu_man: {
    ma: 'khoanh_tay_tu_man',
    tenHienThi: 'Khoanh tay tự mãn',
    nhom: 'hai_huoc',
    doDaiGoiY: 75,
    moTa: 'Khoanh tay bật lò xo trước ngực, ưỡn lưng ngửa đầu đầy kiêu hãnh.',
  },
  ho_het_sung_suong: {
    ma: 'ho_het_sung_suong',
    tenHienThi: 'Hò hét sung sướng',
    nhom: 'hai_huoc',
    doDaiGoiY: 54,
    moTa: 'Nhún lấy đà rồi nhảy cẫng ăn mừng giơ hai tay cao vẫy nhịp nhàng.',
  },
  di_qua_di_lai: {
    ma: 'di_qua_di_lai',
    tenHienThi: 'Đi qua đi lại',
    nhom: 'di_chuyen',
    doDaiGoiY: 90,
    moTa: 'Chắp tay sau lưng đi qua đi lại suy tư, bước chân đồng bộ vận tốc quay đầu.',
  },
  sup_do_tuyet_vong: {
    ma: 'sup_do_tuyet_vong',
    tenHienThi: 'Sụp đổ tuyệt vọng',
    nhom: 'hai_huoc',
    doDaiGoiY: 75,
    moTa: 'Giật nhẹ lấy đà rồi gục quỵ xuống sàn đàn hồi kịch tính.',
  },
  trao_thu: {
    ma: 'trao_thu',
    tenHienThi: 'Trao thư / cuộn giấy',
    nhom: 'dien_xuat',
    doDaiGoiY: 66,
    moTa: 'Cúi người lịch sự đưa hai tay trao bức thư hoặc tài liệu cho đối phương.',
  },
  chi_bang_giang_bai: {
    ma: 'chi_bang_giang_bai',
    tenHienThi: 'Chỉ bảng giảng bài',
    nhom: 'dien_xuat',
    doDaiGoiY: 90,
    moTa: 'Đứng cạnh bảng giảng bài sôi nổi, tay chỉ công thức nhịp nhàng và liếc nhìn người nghe.',
  },
  quay_nhin_doi_thoai: {
    ma: 'quay_nhin_doi_thoai',
    tenHienThi: 'Quay nhìn đối thoại',
    nhom: 'dien_xuat',
    doDaiGoiY: 72,
    moTa: 'Nghiêng người lắng nghe và trò chuyện tự nhiên, ánh mắt tập trung về phía người đối diện.',
  },
  bat_tay: {
    ma: 'bat_tay',
    tenHienThi: 'Bắt tay thân thiện',
    nhom: 'dien_xuat',
    doDaiGoiY: 60,
    moTa: 'Đưa tay phải về phía trước bắt tay nhịp nhàng đầy trân trọng.',
  },
  giat_minh_bat_day: {
    ma: 'giat_minh_bat_day',
    tenHienThi: 'Giật mình bật dậy',
    nhom: 'hai_huoc',
    doDaiGoiY: 54,
    moTa: 'Ép lấy đà ngắn rồi bật tung người lên đầy kinh ngạc trước khi ổn định lại.',
  },
  quay_nhin_khan_gia: {
    ma: 'quay_nhin_khan_gia',
    tenHienThi: 'Quay nhìn khán giả',
    nhom: 'dien_xuat',
    doDaiGoiY: 75,
    moTa: 'Xoay thẳng về phía ống kính, giơ tay chào và trò chuyện trực tiếp với khán giả.',
  },
};

/** Tu the dung trung tinh lam moc vao-the muot (8-12 frame) */
function taoTuTheTrungTinh(f: number): ThongSoTuTheFK {
  const tho = Math.sin(f * 0.11);
  const thoPhu = Math.sin(f * 0.055 + 0.8);
  const { squashX, squashY } = baoToanCoGian(1 + tho * 0.018);
  return {
    offsetX: thoPhu * 1.6,
    offsetY: tho * 1.4,
    squashX,
    squashY,
    gocThan: thoPhu * 1.6,
    doCongThan: 2 + tho * 1.8,
    gocDau: Math.sin(f * 0.08 + 0.5) * 2.2,
    nhunVai: tho * 1.1,
    vaiPhaiGoc: 15 + Math.sin(f * 0.12) * 3.5,
    khuyuPhaiGoc: 20 + Math.sin(f * 0.12 - 0.5) * 3,
    vaiTraiGoc: -16 - Math.sin(f * 0.12) * 3.2,
    khuyuTraiGoc: 16 + Math.cos(f * 0.12) * 2.5,
    duiPhaiGoc: 12,
    goiPhaiGoc: -12,
    duiTraiGoc: -11,
    goiTraiGoc: -8,
    nhayY: 0,
    dichNgangNoiBo: 0,
    khoaMatDat: true,
    coVetBui: false,
    huongNhinX: 0.6,
    huongNhinY: 0,
  };
}

/** Tron muot giua hai tu the FK theo he so alpha */
function tronTuTheFK(
  a: ThongSoTuTheFK,
  b: ThongSoTuTheFK,
  alpha: number,
): ThongSoTuTheFK {
  const sy = noiSuy(a.squashY, b.squashY, alpha);
  const { squashX, squashY } = baoToanCoGian(sy);
  return {
    offsetX: noiSuy(a.offsetX, b.offsetX, alpha),
    offsetY: noiSuy(a.offsetY, b.offsetY, alpha),
    squashX,
    squashY,
    gocThan: noiSuy(a.gocThan, b.gocThan, alpha),
    doCongThan: noiSuy(a.doCongThan, b.doCongThan, alpha),
    gocDau: noiSuy(a.gocDau, b.gocDau, alpha),
    nhunVai: noiSuy(a.nhunVai, b.nhunVai, alpha),
    vaiPhaiGoc: noiSuy(a.vaiPhaiGoc, b.vaiPhaiGoc, alpha),
    khuyuPhaiGoc: noiSuy(a.khuyuPhaiGoc, b.khuyuPhaiGoc, alpha),
    vaiTraiGoc: noiSuy(a.vaiTraiGoc, b.vaiTraiGoc, alpha),
    khuyuTraiGoc: noiSuy(a.khuyuTraiGoc, b.khuyuTraiGoc, alpha),
    duiPhaiGoc: noiSuy(a.duiPhaiGoc, b.duiPhaiGoc, alpha),
    goiPhaiGoc: noiSuy(a.goiPhaiGoc, b.goiPhaiGoc, alpha),
    duiTraiGoc: noiSuy(a.duiTraiGoc, b.duiTraiGoc, alpha),
    goiTraiGoc: noiSuy(a.goiTraiGoc, b.goiTraiGoc, alpha),
    nhayY: noiSuy(a.nhayY, b.nhayY, alpha),
    dichNgangNoiBo: noiSuy(a.dichNgangNoiBo, b.dichNgangNoiBo, alpha),
    khoaMatDat: alpha > 0.35 ? b.khoaMatDat : a.khoaMatDat,
    coVetBui: alpha > 0.35 ? b.coVetBui : a.coVetBui,
    huongNhinX: noiSuy(a.huongNhinX, b.huongNhinX, alpha),
    huongNhinY: noiSuy(a.huongNhinY, b.huongNhinY, alpha),
  };
}

/**
 * Chu ky buoc chan 4 pha kinh dien (Contact -> Down -> Passing -> Up).
 * Tra ve goc dui, goc goi cho mot chan tai pha p (radian).
 */
function tinhChanDiBo(pha: number, bienDo = 1): { dui: number; goi: number } {
  const s = Math.sin(pha);
  const c = Math.cos(pha);
  // Contact: s ~ +1, Down: s > 0 & c < 0, Passing: c ~ +1 (nhac goi len), Up: s ~ -1
  const dui = (s * 31 + 3) * bienDo;
  const nhacGoi = Math.max(0, c) * 46 + Math.max(0, -s) * 16;
  const chiuTai = Math.max(0, s * 0.5 - c * 0.5) * 14;
  const goi = (-8 - (nhacGoi + chiuTai) * bienDo);
  return { dui, goi };
}

/**
 * Tinh toan tham so goc khop FK cho 14 hanh dong dien xuat & hai huoc.
 * Tat dinh 100% theo frameCucBo, co pha vao-the muot 8-12 frame va lop cu chi khi dangNoi.
 */
export function tinhGocKhopDongTac(
  hanhDong: LoaiHanhDong,
  frameCucBo: number,
  dangNoi = false,
): ThongSoTuTheFK {
  const f = Number.isFinite(frameCucBo) ? frameCucBo : 0;
  const fDuong = Math.max(0, f);
  const trungTinh = taoTuTheTrungTinh(f);
  const tho = Math.sin(f * 0.12);

  // Pha vao-the muot mac dinh (10 frame)
  const vaoThe10 = easeInOutCubic(kepGiaTri(fDuong / 10, 0, 1));
  const vaoThe8 = easeInOutCubic(kepGiaTri(fDuong / 8, 0, 1));
  const vaoThe12 = easeInOutCubic(kepGiaTri(fDuong / 12, 0, 1));

  let ketQua: ThongSoTuTheFK = { ...trungTinh };

  switch (hanhDong) {
    case 'di_bo': {
      // Chu ky 4 pha: 24 frame / 2 buoc, hong nhun 2 lan moi chu ky
      const pha = f * ((Math.PI * 2) / 24);
      const bienDo = 0.25 + 0.75 * vaoThe8;
      const chanPhai = tinhChanDiBo(pha, bienDo);
      const chanTrai = tinhChanDiBo(pha + Math.PI, bienDo);

      // Hong nhun 2 lan moi chu ky (thap o Down, cao o Passing/Up)
      const nhun2Lan = -Math.cos(2 * pha) * 5.8 * bienDo;
      const { squashX, squashY } = baoToanCoGian(1 + Math.cos(2 * pha) * 0.032 * bienDo);

      // Tay danh lech pha nguoc chan, khuyu tay tre nhip ~0.55 rad cho mem mai
      const danhTayPhai = -Math.sin(pha) * 28 * bienDo;
      const danhTayTrai = Math.sin(pha) * 28 * bienDo;

      ketQua = {
        offsetX: Math.sin(pha) * 2.2 * bienDo,
        offsetY: nhun2Lan,
        squashX,
        squashY,
        gocThan: 6.5 * bienDo + Math.sin(2 * pha) * 1.8 * bienDo,
        doCongThan: -3.5 * bienDo + Math.cos(2 * pha) * 1.4,
        gocDau: -1.5 + Math.sin(2 * pha - 0.6) * 2.6 * bienDo,
        nhunVai: Math.cos(2 * pha) * 1.4,
        vaiPhaiGoc: 8 + danhTayPhai,
        khuyuPhaiGoc: 20 + Math.max(0, -Math.sin(pha - 0.55)) * 26 * bienDo,
        vaiTraiGoc: -6 + danhTayTrai,
        khuyuTraiGoc: 18 + Math.max(0, Math.sin(pha - 0.55)) * 24 * bienDo,
        duiPhaiGoc: chanPhai.dui,
        goiPhaiGoc: chanPhai.goi,
        duiTraiGoc: chanTrai.dui,
        goiTraiGoc: chanTrai.goi,
        nhayY: 0,
        dichNgangNoiBo: 0,
        khoaMatDat: true,
        coVetBui: false,
        huongNhinX: 1.4,
        huongNhinY: -0.2,
      };
      break;
    }

    case 'chay_voi_va': {
      // Than nghieng ve truoc 18-22 do, chan dap cao, co vet bui nho duoi got
      const pha = f * ((Math.PI * 2) / 14);
      const bienDo = 0.35 + 0.65 * vaoThe8;
      const nhayChay = -Math.max(0, Math.sin(2 * pha - 0.35)) * 14 * bienDo;
      const { squashX, squashY } = baoToanCoGian(1 - Math.sin(2 * pha) * 0.065 * bienDo);

      const tinhChanChay = (p: number) => {
        const s = Math.sin(p);
        const c = Math.cos(p);
        const dui = (s * 48 + 10) * bienDo;
        const goi = -18 - (Math.max(0, c) * 76 + Math.max(0, -s) * 38) * bienDo;
        return { dui, goi };
      };

      const chanPhai = tinhChanChay(pha);
      const chanTrai = tinhChanChay(pha + Math.PI);

      ketQua = {
        offsetX: 5 * bienDo,
        offsetY: nhayChay,
        squashX,
        squashY,
        gocThan: 18 + 2.2 * bienDo + Math.sin(2 * pha) * 1.8, // 18-22 do
        doCongThan: -8.5 * bienDo,
        gocDau: -6 + Math.sin(2 * pha - 0.5) * 3.5,
        nhunVai: 2.5 + Math.abs(Math.sin(pha)) * 2.5,
        vaiPhaiGoc: 12 - Math.sin(pha) * 52 * bienDo,
        khuyuPhaiGoc: 86 + Math.cos(pha) * 14 * bienDo,
        vaiTraiGoc: 4 + Math.sin(pha) * 52 * bienDo,
        khuyuTraiGoc: 82 - Math.cos(pha) * 14 * bienDo,
        duiPhaiGoc: chanPhai.dui,
        goiPhaiGoc: chanPhai.goi,
        duiTraiGoc: chanTrai.dui,
        goiTraiGoc: chanTrai.goi,
        nhayY: nhayChay,
        dichNgangNoiBo: 0,
        khoaMatDat: nhayChay >= -2,
        coVetBui: true,
        huongNhinX: 1.8,
        huongNhinY: -0.4,
      };
      break;
    }

    case 'ngoi_doc_sach': {
      const luotMat = Math.sin(f * 0.09);
      const gatDoc = Math.sin(f * 0.14) * 2.2;
      const mucTieu: ThongSoTuTheFK = {
        offsetX: -10,
        offsetY: 36 + tho * 1.1,
        ...baoToanCoGian(0.96 + tho * 0.015),
        gocThan: 11 + tho * 1.2,
        doCongThan: -10.5,
        gocDau: 15 + gatDoc,
        nhunVai: -1,
        vaiPhaiGoc: 44 + Math.sin(f * 0.08) * 3,
        khuyuPhaiGoc: 58 + Math.cos(f * 0.08) * 3,
        vaiTraiGoc: 32 + Math.sin(f * 0.08 + 0.4) * 2.5,
        khuyuTraiGoc: 60,
        duiPhaiGoc: 72,
        goiPhaiGoc: -72,
        duiTraiGoc: 60,
        goiTraiGoc: -64,
        nhayY: 0,
        dichNgangNoiBo: 0,
        khoaMatDat: true,
        coVetBui: false,
        huongNhinX: 0.7 + luotMat * 0.9,
        huongNhinY: 1.2,
      };
      ketQua = tronTuTheFK(trungTinh, mucTieu, vaoThe12);
      break;
    }

    case 'chi_tro_giai_thich': {
      // Tay cam que chi dua nhip nhang huong vao bang / cong thuc dang sang
      const vaoChi = easeOutBack(kepGiaTri(fDuong / 11, 0, 1), 1.35);
      const nhipChi = Math.sin(f * 0.19) * 9 + Math.sin(f * 0.43) * 3.5;
      const nhipKhuyu = Math.sin(f * 0.19 - 0.6) * 7;
      const liecBang = Math.sin(f * 0.075);

      const mucTieu: ThongSoTuTheFK = {
        offsetX: 4,
        offsetY: Math.sin(f * 0.19) * 1.6,
        ...baoToanCoGian(1.01 + Math.sin(f * 0.19) * 0.02),
        gocThan: 7.5 + Math.sin(f * 0.19) * 2.2,
        doCongThan: 4.5,
        gocDau: -2 + Math.sin(f * 0.15) * 4,
        nhunVai: 1.5 + Math.max(0, Math.sin(f * 0.19)) * 2.2,
        vaiPhaiGoc: 84 + nhipChi,
        khuyuPhaiGoc: 30 + nhipKhuyu,
        vaiTraiGoc: -28 + Math.cos(f * 0.16) * 6,
        khuyuTraiGoc: 56 + Math.sin(f * 0.16) * 8,
        duiPhaiGoc: 15,
        goiPhaiGoc: -14,
        duiTraiGoc: -14,
        goiTraiGoc: -10,
        nhayY: 0,
        dichNgangNoiBo: 0,
        khoaMatDat: true,
        coVetBui: false,
        huongNhinX: 1.2 + liecBang * 0.7,
        huongNhinY: -0.7 + Math.sin(f * 0.19) * 0.5,
      };
      ketQua = tronTuTheFK(trungTinh, mucTieu, vaoChi);
      break;
    }

    case 'nhin_len_troi': {
      const luong = Math.sin(f * 0.1);
      const mucTieu: ThongSoTuTheFK = {
        offsetX: -4,
        offsetY: tho * 1.4,
        ...baoToanCoGian(1.02 + tho * 0.02),
        gocThan: -9 + luong * 1.8,
        doCongThan: 9.5,
        gocDau: -20 + luong * 3,
        nhunVai: 1.2,
        vaiPhaiGoc: 112 + Math.sin(f * 0.13) * 6,
        khuyuPhaiGoc: 30 + Math.cos(f * 0.13) * 5,
        vaiTraiGoc: -22,
        khuyuTraiGoc: 24 + luong * 4,
        duiPhaiGoc: 13,
        goiPhaiGoc: -11,
        duiTraiGoc: -14,
        goiTraiGoc: -9,
        nhayY: 0,
        dichNgangNoiBo: 0,
        khoaMatDat: true,
        coVetBui: false,
        huongNhinX: 0.8,
        huongNhinY: -1.8,
      };
      ketQua = tronTuTheFK(trungTinh, mucTieu, vaoThe12);
      break;
    }

    case 'gat_gu_dong_tinh': {
      // Gat dau co lay da len truoc khi gat xuong nhip nhang
      const phaGat = f * 0.24;
      const gat = Math.sin(phaGat) + 0.25 * Math.sin(phaGat * 2 - 0.5);
      const mucTieu: ThongSoTuTheFK = {
        offsetX: 2,
        offsetY: Math.max(0, gat) * 3.2,
        ...baoToanCoGian(1 - gat * 0.028),
        gocThan: 4 + gat * 4.5,
        doCongThan: 2 - gat * 3.5,
        gocDau: 6 + gat * 13,
        nhunVai: -gat * 1.5,
        vaiPhaiGoc: 38 + gat * 10,
        khuyuPhaiGoc: 46 + gat * 12,
        vaiTraiGoc: -18,
        khuyuTraiGoc: 22,
        duiPhaiGoc: 13,
        goiPhaiGoc: -13 - Math.max(0, gat) * 4,
        duiTraiGoc: -12,
        goiTraiGoc: -10,
        nhayY: 0,
        dichNgangNoiBo: 0,
        khoaMatDat: true,
        coVetBui: false,
        huongNhinX: 1.0,
        huongNhinY: gat * 0.6,
      };
      ketQua = tronTuTheFK(trungTinh, mucTieu, vaoThe10);
      break;
    }

    case 'gai_dau_kho_hieu': {
      // Lay da (0..6) -> dua tay len gai dau co vuot da (6..16) -> gai lien tuc
      const layDa = fDuong < 6 ? easeInBack(fDuong / 6, 1.4) : 1;
      const vaoGai = fDuong < 6 ? 0 : easeOutBack(kepGiaTri((fDuong - 6) / 10, 0, 1), 1.6);
      const nhipGai = fDuong >= 12 ? Math.sin((f - 12) * 0.45) : 0;

      const mucTieu: ThongSoTuTheFK = {
        offsetX: -4 + Math.sin(f * 0.08) * 2,
        offsetY: fDuong < 6 ? layDa * 4 : tho * 1.3,
        ...baoToanCoGian(fDuong < 6 ? 0.96 : 1 + tho * 0.015),
        gocThan: -6 + nhipGai * 1.5,
        doCongThan: -6.5,
        gocDau: -10 + nhipGai * 3.2,
        nhunVai: 3.5 + nhipGai * 1.2,
        vaiPhaiGoc: 126 + nhipGai * 5,
        khuyuPhaiGoc: 112 + nhipGai * 10,
        vaiTraiGoc: -34,
        khuyuTraiGoc: 76,
        duiPhaiGoc: 14,
        goiPhaiGoc: -13,
        duiTraiGoc: -14,
        goiTraiGoc: -10,
        nhayY: 0,
        dichNgangNoiBo: 0,
        khoaMatDat: true,
        coVetBui: false,
        huongNhinX: -0.6 + Math.sin(f * 0.09) * 0.9,
        huongNhinY: -1.1,
      };
      ketQua = tronTuTheFK(trungTinh, mucTieu, kepGiaTri(vaoGai, 0, 1.12));
      if (fDuong < 6) {
        const { squashX, squashY } = baoToanCoGian(1 - (fDuong / 6) * 0.06);
        ketQua.squashX = squashX;
        ketQua.squashY = squashY;
        ketQua.offsetY += (fDuong / 6) * 4.5;
      }
      break;
    }

    case 'giat_minh_nhay_dung': {
      // Chu ky 48 frame:
      // 0..7: lay da ep thap (squashY -> 0.78)
      // 7..16: bat vot keo dai (squashY -> 1.22)
      // 16..20: lo lung 4 frame tren dinh
      // 20..28: roi xuong
      // 28..48: dap dat nhun dan hoi (springTatDinh)
      const c = ((f % 48) + 48) % 48;
      if (c < 7) {
        const t = c / 7;
        const ep = easeInOutCubic(t);
        const { squashX, squashY } = baoToanCoGian(noiSuy(1, 0.78, ep));
        ketQua = {
          ...trungTinh,
          offsetY: ep * 20,
          squashX,
          squashY,
          gocThan: ep * 12,
          doCongThan: -12 * ep,
          gocDau: -6 * ep,
          nhunVai: -4 * ep,
          vaiPhaiGoc: noiSuy(16, -24, ep),
          khuyuPhaiGoc: noiSuy(20, 68, ep),
          vaiTraiGoc: noiSuy(-16, -34, ep),
          khuyuTraiGoc: noiSuy(16, 62, ep),
          duiPhaiGoc: noiSuy(12, 34, ep),
          goiPhaiGoc: noiSuy(-12, -56, ep),
          duiTraiGoc: noiSuy(-11, 20, ep),
          goiTraiGoc: noiSuy(-8, -50, ep),
          nhayY: 0,
          khoaMatDat: true,
          coVetBui: false,
          huongNhinX: 0.4,
          huongNhinY: -0.6,
        };
      } else if (c < 16) {
        const t = (c - 7) / 9;
        const len = 1 - Math.pow(1 - t, 2.2);
        const nhayY = -len * 74;
        const sy = t < 0.45 ? noiSuy(0.84, 1.22, t / 0.45) : noiSuy(1.22, 1.06, (t - 0.45) / 0.55);
        const { squashX, squashY } = baoToanCoGian(sy);
        ketQua = {
          ...trungTinh,
          offsetY: nhayY,
          squashX,
          squashY,
          gocThan: -7 * len,
          doCongThan: 10 * len,
          gocDau: -12 * len,
          nhunVai: 6 * len,
          vaiPhaiGoc: noiSuy(20, 152, len),
          khuyuPhaiGoc: noiSuy(50, 14, len),
          vaiTraiGoc: noiSuy(-20, -148, len),
          khuyuTraiGoc: noiSuy(45, -14, len),
          duiPhaiGoc: noiSuy(28, 32, len),
          goiPhaiGoc: noiSuy(-48, -22, len),
          duiTraiGoc: noiSuy(-18, -32, len),
          goiTraiGoc: noiSuy(-40, -18, len),
          nhayY,
          khoaMatDat: false,
          coVetBui: c < 11,
          huongNhinX: 0.5,
          huongNhinY: -0.5,
        };
      } else if (c < 20) {
        // Lo lung 4 frame tren dinh (c = 16, 17, 18, 19)
        const rungKhong = Math.sin((c - 16) * 2.1);
        const nhayY = -74 - Math.sin(((c - 16) / 4) * Math.PI) * 4;
        const { squashX, squashY } = baoToanCoGian(1.04);
        ketQua = {
          ...trungTinh,
          offsetY: nhayY,
          squashX,
          squashY,
          gocThan: -6 + rungKhong * 2,
          doCongThan: 8,
          gocDau: -11 + rungKhong * 3,
          nhunVai: 6,
          vaiPhaiGoc: 150 + rungKhong * 8,
          khuyuPhaiGoc: 18,
          vaiTraiGoc: -146 - rungKhong * 8,
          khuyuTraiGoc: -16,
          duiPhaiGoc: 34 + rungKhong * 6,
          goiPhaiGoc: -34,
          duiTraiGoc: -34 - rungKhong * 6,
          goiTraiGoc: -30,
          nhayY,
          khoaMatDat: false,
          coVetBui: false,
          huongNhinX: 0.5,
          huongNhinY: 0.4,
        };
      } else if (c < 28) {
        // Roi xuong co keo dai nhe
        const t = (c - 20) / 8;
        const roi = t * t;
        const nhayY = -74 * (1 - roi);
        const { squashX, squashY } = baoToanCoGian(noiSuy(1.04, 1.14, t));
        ketQua = {
          ...trungTinh,
          offsetY: nhayY,
          squashX,
          squashY,
          gocThan: noiSuy(-6, 6, roi),
          doCongThan: noiSuy(6, -4, roi),
          gocDau: noiSuy(-10, 4, roi),
          nhunVai: noiSuy(5, 2, roi),
          vaiPhaiGoc: noiSuy(146, 78, roi),
          khuyuPhaiGoc: noiSuy(20, 36, roi),
          vaiTraiGoc: noiSuy(-142, -72, roi),
          khuyuTraiGoc: noiSuy(-18, 28, roi),
          duiPhaiGoc: noiSuy(30, 18, roi),
          goiPhaiGoc: noiSuy(-30, -18, roi),
          duiTraiGoc: noiSuy(-30, -16, roi),
          goiTraiGoc: noiSuy(-26, -16, roi),
          nhayY,
          khoaMatDat: false,
          coVetBui: false,
          huongNhinX: 0.6,
          huongNhinY: 0.8,
        };
      } else {
        // Dap dat nhun dan hoi bang springTatDinh
        const fDap = c - 28;
        const sp = springTatDinh(fDap, 9, 210);
        // sp di tu 0 -> ~1.22 -> 1 => khi fDap nho nen nen xuong roi nay len ve 1
        const nen = 1 - sp; // 1 -> -0.22 -> 0
        const { squashX, squashY } = baoToanCoGian(1 - nen * 0.2);
        ketQua = {
          ...trungTinh,
          offsetY: nen * 16,
          squashX,
          squashY,
          gocThan: nen * 10,
          doCongThan: -nen * 9,
          gocDau: nen * 8,
          nhunVai: -nen * 4,
          vaiPhaiGoc: noiSuy(68, 18, sp),
          khuyuPhaiGoc: noiSuy(46, 22, sp),
          vaiTraiGoc: noiSuy(-64, -18, sp),
          khuyuTraiGoc: noiSuy(38, 18, sp),
          duiPhaiGoc: noiSuy(28, 12, sp),
          goiPhaiGoc: noiSuy(-44, -12, sp),
          duiTraiGoc: noiSuy(-22, -11, sp),
          goiTraiGoc: noiSuy(-36, -8, sp),
          nhayY: 0,
          khoaMatDat: true,
          coVetBui: fDap < 6,
          huongNhinX: 0.6,
          huongNhinY: 0,
        };
      }
      break;
    }

    case 'bo_tay_can_loi': {
      // Lay da (0..7: hit sau, vai nang nhe) -> vo tran + sup vai bang springTatDinh
      const sp = springTatDinh(Math.max(0, fDuong - 6), 11, 175);
      const thoDai = fDuong > 18 ? Math.sin((f - 18) * 0.14) : 0;

      if (fDuong < 7) {
        const t = easeInOutCubic(fDuong / 7);
        const { squashX, squashY } = baoToanCoGian(1 + t * 0.05);
        ketQua = {
          ...trungTinh,
          offsetY: -t * 3,
          squashX,
          squashY,
          gocThan: -4 * t,
          doCongThan: 4 * t,
          gocDau: -6 * t,
          nhunVai: 4.5 * t,
          vaiPhaiGoc: noiSuy(16, 48, t),
          khuyuPhaiGoc: noiSuy(20, 62, t),
          vaiTraiGoc: -16,
          khuyuTraiGoc: 18,
          huongNhinX: 0.4,
          huongNhinY: -0.3,
        };
      } else {
        const mucTieu: ThongSoTuTheFK = {
          offsetX: -4,
          offsetY: 4 + thoDai * 1.8,
          ...baoToanCoGian(0.95 - thoDai * 0.02),
          gocThan: -4 + thoDai * 1.4,
          doCongThan: -9.5 - thoDai * 1.8,
          gocDau: 11 + thoDai * 2.5,
          nhunVai: -4.5 - thoDai * 1.2,
          vaiPhaiGoc: 94 + thoDai * 2,
          khuyuPhaiGoc: 118 - thoDai * 2,
          vaiTraiGoc: -14,
          khuyuTraiGoc: 8,
          duiPhaiGoc: 13,
          goiPhaiGoc: -14,
          duiTraiGoc: -13,
          goiTraiGoc: -11,
          nhayY: 0,
          dichNgangNoiBo: 0,
          khoaMatDat: true,
          coVetBui: false,
          huongNhinX: 0.2,
          huongNhinY: 0.6,
        };
        ketQua = tronTuTheFK(trungTinh, mucTieu, kepGiaTri(sp, 0, 1.15));
      }
      break;
    }

    case 'khoanh_tay_tu_man': {
      // Lay da (0..6: mo tay nhe, nhun) -> bat khoanh tay truoc nguc + uon nguc springTatDinh
      const sp = springTatDinh(Math.max(0, fDuong - 5), 10, 210);
      const nhipTuMan = Math.sin(f * 0.14);

      if (fDuong < 6) {
        const t = easeInBack(fDuong / 6, 1.2);
        const { squashX, squashY } = baoToanCoGian(1 - Math.abs(t) * 0.04);
        ketQua = {
          ...trungTinh,
          offsetY: 3 * (fDuong / 6),
          squashX,
          squashY,
          gocThan: 3 * (fDuong / 6),
          vaiPhaiGoc: noiSuy(15, 36, fDuong / 6),
          khuyuPhaiGoc: 18,
          vaiTraiGoc: noiSuy(-16, -34, fDuong / 6),
          khuyuTraiGoc: 16,
        };
      } else {
        const mucTieu: ThongSoTuTheFK = {
          offsetX: -3,
          offsetY: -2 + nhipTuMan * 1.6,
          ...baoToanCoGian(1.03 + nhipTuMan * 0.02),
          gocThan: -9.5 + nhipTuMan * 1.5,
          doCongThan: 10.5 + nhipTuMan * 1.4,
          gocDau: -13 + nhipTuMan * 2.2,
          nhunVai: 2.2,
          vaiPhaiGoc: 32,
          khuyuPhaiGoc: -124,
          vaiTraiGoc: -32,
          khuyuTraiGoc: 122,
          duiPhaiGoc: 16,
          goiPhaiGoc: -11,
          duiTraiGoc: -16,
          goiTraiGoc: -10,
          nhayY: 0,
          dichNgangNoiBo: 0,
          khoaMatDat: true,
          coVetBui: false,
          huongNhinX: 0.9,
          huongNhinY: -0.5,
        };
        ketQua = tronTuTheFK(trungTinh, mucTieu, kepGiaTri(sp, 0, 1.15));
      }
      break;
    }

    case 'ho_het_sung_suong': {
      // Lay da (0..5) -> nhay cang an mung lien mach (5..18) -> dap dat nhun lo xo (18..26)
      // Giu gocThan va gocDau thang truc, vui tuoi, tuyet doi khong ngua/lat nguoc dau khi bat nhay
      const c = ((f % 26) + 26) % 26;
      if (c < 5) {
        const t = easeInOutCubic(c / 5);
        const { squashX, squashY } = baoToanCoGian(noiSuy(1, 0.86, t));
        ketQua = {
          ...trungTinh,
          offsetY: t * 10,
          squashX,
          squashY,
          gocThan: 4.5 * t,
          doCongThan: -3.5 * t,
          gocDau: noiSuy(-4, -2, t),
          nhunVai: -1.8 * t,
          vaiPhaiGoc: noiSuy(132, 114, t),
          khuyuPhaiGoc: noiSuy(18, 36, t),
          vaiTraiGoc: noiSuy(-132, -114, t),
          khuyuTraiGoc: noiSuy(-18, -36, t),
          duiPhaiGoc: 22 * t + 10,
          goiPhaiGoc: -34 * t - 10,
          duiTraiGoc: -16,
          goiTraiGoc: -30 * t - 8,
          nhayY: 0,
          khoaMatDat: true,
          coVetBui: false,
          huongNhinX: 0.6,
          huongNhinY: -0.7,
        };
      } else if (c < 18) {
        const t = (c - 5) / 13;
        const arc = Math.sin(t * Math.PI);
        const nhayY = -arc * 38;
        const { squashX, squashY } = baoToanCoGian(1 + arc * 0.13);
        const vay = Math.sin(f * 0.5) * 10;
        ketQua = {
          ...trungTinh,
          offsetY: nhayY,
          squashX,
          squashY,
          gocThan: -3.5 * arc,
          doCongThan: 6.5 * arc,
          gocDau: -6 - arc * 4,
          nhunVai: 3.5,
          vaiPhaiGoc: 138 + vay * 0.5,
          khuyuPhaiGoc: 14 + vay * 0.7,
          vaiTraiGoc: -138 - vay * 0.5,
          khuyuTraiGoc: -14 - vay * 0.7,
          duiPhaiGoc: 16 + arc * 12,
          goiPhaiGoc: -16 - arc * 15,
          duiTraiGoc: -16 - arc * 12,
          goiTraiGoc: -16 - arc * 13,
          nhayY,
          khoaMatDat: false,
          coVetBui: false,
          huongNhinX: 0.6,
          huongNhinY: -0.9,
        };
      } else {
        const sp = springTatDinh(c - 18, 10, 220);
        const nen = 1 - sp;
        const { squashX, squashY } = baoToanCoGian(1 - nen * 0.12);
        ketQua = {
          ...trungTinh,
          offsetY: nen * 9,
          squashX,
          squashY,
          gocThan: nen * 4,
          doCongThan: 3 - nen * 6,
          gocDau: -5 + nen * 3,
          nhunVai: 1.8,
          vaiPhaiGoc: 134,
          khuyuPhaiGoc: 18,
          vaiTraiGoc: -134,
          khuyuTraiGoc: -18,
          duiPhaiGoc: 14 + nen * 9,
          goiPhaiGoc: -14 - nen * 18,
          duiTraiGoc: -14 - nen * 6,
          goiTraiGoc: -12 - nen * 16,
          nhayY: 0,
          khoaMatDat: true,
          coVetBui: false,
          huongNhinX: 0.6,
          huongNhinY: -0.7,
        };
      }
      break;
    }

    case 'di_qua_di_lai': {
      // Di qua di lai suy tu, tay chap sau lung, bien do buoc tu giam o 2 dau quay
      const phaDi = f * 0.055;
      const dichNgangNoiBo = Math.sin(phaDi) * 58 * vaoThe10;
      const heSoTocDo = kepGiaTri(Math.abs(Math.cos(phaDi)) * 1.15, 0.2, 1) * vaoThe10;
      const phaBuoc = f * ((Math.PI * 2) / 24);
      const chanPhai = tinhChanDiBo(phaBuoc, heSoTocDo * 0.82);
      const chanTrai = tinhChanDiBo(phaBuoc + Math.PI, heSoTocDo * 0.82);
      const nhun = -Math.cos(2 * phaBuoc) * 4.2 * heSoTocDo;
      const { squashX, squashY } = baoToanCoGian(1 + Math.cos(2 * phaBuoc) * 0.022 * heSoTocDo);

      ketQua = {
        offsetX: 0,
        offsetY: nhun,
        squashX,
        squashY,
        gocThan: 8.5,
        doCongThan: -7.5,
        gocDau: 10 + Math.sin(f * 0.14) * 3,
        nhunVai: -1.5,
        vaiPhaiGoc: -28,
        khuyuPhaiGoc: -32,
        vaiTraiGoc: -32,
        khuyuTraiGoc: -28,
        duiPhaiGoc: chanPhai.dui,
        goiPhaiGoc: chanPhai.goi,
        duiTraiGoc: chanTrai.dui,
        goiTraiGoc: chanTrai.goi,
        nhayY: 0,
        dichNgangNoiBo,
        khoaMatDat: true,
        coVetBui: false,
        huongNhinX: 0.7,
        huongNhinY: 1.0,
      };
      break;
    }

    case 'sup_do_tuyet_vong': {
      // Lay da giat nhe (0..7) -> guc xuong san kich tinh (7..19) -> nay dan hoi + run nhe
      const run = fDuong > 20 ? Math.sin((f - 20) * 0.55) * 1.6 : 0;
      if (fDuong < 7) {
        const t = easeInOutCubic(fDuong / 7);
        const { squashX, squashY } = baoToanCoGian(1 + t * 0.08);
        ketQua = {
          ...trungTinh,
          offsetY: -t * 5,
          squashX,
          squashY,
          gocThan: -8 * t,
          doCongThan: 6 * t,
          gocDau: -10 * t,
          nhunVai: 5 * t,
          vaiPhaiGoc: noiSuy(15, 76, t),
          khuyuPhaiGoc: 36,
          vaiTraiGoc: noiSuy(-16, -64, t),
          khuyuTraiGoc: 32,
        };
      } else {
        const fGuc = fDuong - 7;
        const sp = springTatDinh(fGuc, 11, 160);
        const mucTieu: ThongSoTuTheFK = {
          offsetX: -16,
          offsetY: 50 + Math.abs(run) * 0.6,
          ...baoToanCoGian(0.88 + Math.sin(f * 0.16) * 0.02),
          gocThan: 46 + run * 0.8,
          doCongThan: -15,
          gocDau: 28 + run * 1.2,
          nhunVai: -4,
          vaiPhaiGoc: 24,
          khuyuPhaiGoc: 16,
          vaiTraiGoc: 8,
          khuyuTraiGoc: 14,
          duiPhaiGoc: -12,
          goiPhaiGoc: -84,
          duiTraiGoc: -24,
          goiTraiGoc: -78,
          nhayY: 0,
          dichNgangNoiBo: 0,
          khoaMatDat: true,
          coVetBui: fGuc >= 6 && fGuc <= 12,
          huongNhinX: 0.4,
          huongNhinY: 1.5,
        };
        ketQua = tronTuTheFK(trungTinh, mucTieu, kepGiaTri(sp, 0, 1.12));
      }
      break;
    }

    case 'trao_thu': {
      // Lay da nhe -> dua hai tay ve truoc trao thu/cuon giay lich su
      const sp = springTatDinh(fDuong, 12, 185);
      const nhipTrao = Math.sin(f * 0.14);
      const mucTieu: ThongSoTuTheFK = {
        offsetX: 8,
        offsetY: 2 + tho * 1.1,
        ...baoToanCoGian(1.0 + tho * 0.016),
        gocThan: 10 + nhipTrao * 1.6,
        doCongThan: -4.5,
        gocDau: 5 + nhipTrao * 2.2,
        nhunVai: 1.5,
        vaiPhaiGoc: 64 + nhipTrao * 5,
        khuyuPhaiGoc: 28 + Math.cos(f * 0.14) * 4,
        vaiTraiGoc: 52 + nhipTrao * 4,
        khuyuTraiGoc: 34 + Math.cos(f * 0.14) * 3,
        duiPhaiGoc: 16,
        goiPhaiGoc: -15,
        duiTraiGoc: -13,
        goiTraiGoc: -11,
        nhayY: 0,
        dichNgangNoiBo: 0,
        khoaMatDat: true,
        coVetBui: false,
        huongNhinX: 1.6,
        huongNhinY: 0.2,
      };
      ketQua = tronTuTheFK(trungTinh, mucTieu, kepGiaTri(sp, 0, 1.08));
      break;
    }

    case 'chi_bang_giang_bai': {
      // Giang bai soi noi: tay phai chi len cao theo nhip, tay trai mo rong dien giai, mat luoc giua bang & nguoi nghe
      const vao = easeOutBack(kepGiaTri(fDuong / 12, 0, 1), 1.3);
      const nhipChi = Math.sin(f * 0.21) * 11 + Math.cos(f * 0.42) * 3.5;
      const liec = Math.sin(f * 0.085);
      const mucTieu: ThongSoTuTheFK = {
        offsetX: 5,
        offsetY: Math.sin(f * 0.21) * 1.8,
        ...baoToanCoGian(1.02 + Math.sin(f * 0.21) * 0.022),
        gocThan: 6 + Math.sin(f * 0.21) * 2.2,
        doCongThan: 5.2,
        gocDau: -4 + liec * 4.5,
        nhunVai: 2.2 + Math.max(0, Math.sin(f * 0.21)) * 2.0,
        vaiPhaiGoc: 108 + nhipChi,
        khuyuPhaiGoc: 24 + Math.sin(f * 0.21 - 0.5) * 8,
        vaiTraiGoc: 32 + Math.cos(f * 0.17) * 9,
        khuyuTraiGoc: 52 + Math.sin(f * 0.17) * 8,
        duiPhaiGoc: 15,
        goiPhaiGoc: -14,
        duiTraiGoc: -14,
        goiTraiGoc: -11,
        nhayY: 0,
        dichNgangNoiBo: 0,
        khoaMatDat: true,
        coVetBui: false,
        huongNhinX: 1.3 + liec * 0.6,
        huongNhinY: -0.9 + Math.sin(f * 0.21) * 0.4,
      };
      ketQua = tronTuTheFK(trungTinh, mucTieu, kepGiaTri(vao, 0, 1.08));
      break;
    }

    case 'quay_nhin_doi_thoai': {
      // Tu the doi thoai tu nhien: nghieng nhe ve doi phuong, gat nhe & cu chi tay mem mai
      const nhipTroChuyen = Math.sin(f * 0.17);
      const mucTieu: ThongSoTuTheFK = {
        offsetX: 3,
        offsetY: tho * 1.3,
        ...baoToanCoGian(1.0 + tho * 0.018),
        gocThan: 5 + nhipTroChuyen * 2.0,
        doCongThan: 3.2,
        gocDau: 2 + Math.sin(f * 0.19) * 4.5,
        nhunVai: 1.2 + Math.max(0, nhipTroChuyen) * 1.4,
        vaiPhaiGoc: 42 + nhipTroChuyen * 10,
        khuyuPhaiGoc: 48 + Math.cos(f * 0.17) * 9,
        vaiTraiGoc: 20 - nhipTroChuyen * 6,
        khuyuTraiGoc: 44 + Math.sin(f * 0.15) * 6,
        duiPhaiGoc: 13,
        goiPhaiGoc: -12,
        duiTraiGoc: -12,
        goiTraiGoc: -10,
        nhayY: 0,
        dichNgangNoiBo: 0,
        khoaMatDat: true,
        coVetBui: false,
        huongNhinX: 1.8,
        huongNhinY: -0.1,
      };
      ketQua = tronTuTheFK(trungTinh, mucTieu, vaoThe10);
      break;
    }

    case 'bat_tay': {
      // Dua tay phai ve truoc bat tay nhip nhang (lac len xuong 2-3 nhip/giay)
      const sp = springTatDinh(fDuong, 11, 195);
      const lacTay = fDuong >= 6 ? Math.sin((f - 6) * 0.38) : 0;
      const mucTieu: ThongSoTuTheFK = {
        offsetX: 9,
        offsetY: 1.5 + Math.abs(lacTay) * 1.6,
        ...baoToanCoGian(1.0 - Math.abs(lacTay) * 0.02),
        gocThan: 9 + lacTay * 2.2,
        doCongThan: -2.5,
        gocDau: 3 + lacTay * 3.5,
        nhunVai: 1.8 + lacTay * 1.5,
        vaiPhaiGoc: 68 + lacTay * 11,
        khuyuPhaiGoc: 22 - lacTay * 7,
        vaiTraiGoc: -18,
        khuyuTraiGoc: 24,
        duiPhaiGoc: 17,
        goiPhaiGoc: -15,
        duiTraiGoc: -14,
        goiTraiGoc: -11,
        nhayY: 0,
        dichNgangNoiBo: 0,
        khoaMatDat: true,
        coVetBui: false,
        huongNhinX: 1.7,
        huongNhinY: 0,
      };
      ketQua = tronTuTheFK(trungTinh, mucTieu, kepGiaTri(sp, 0, 1.08));
      break;
    }

    case 'giat_minh_bat_day': {
      // Lay da ngan (0..6) -> bat day manh bang springTatDinh (6..22) -> tho doc tinh tao
      if (fDuong < 6) {
        const t = easeInOutCubic(fDuong / 6);
        const { squashX, squashY } = baoToanCoGian(noiSuy(1, 0.82, t));
        ketQua = {
          ...trungTinh,
          offsetY: t * 18,
          squashX,
          squashY,
          gocThan: t * 11,
          doCongThan: -10 * t,
          gocDau: 4 * t,
          nhunVai: -3 * t,
          vaiPhaiGoc: noiSuy(16, -22, t),
          khuyuPhaiGoc: noiSuy(20, 62, t),
          vaiTraiGoc: noiSuy(-16, -26, t),
          khuyuTraiGoc: noiSuy(18, 56, t),
          duiPhaiGoc: noiSuy(12, 32, t),
          goiPhaiGoc: noiSuy(-12, -52, t),
          duiTraiGoc: noiSuy(-11, 18, t),
          goiTraiGoc: noiSuy(-8, -46, t),
          nhayY: 0,
          khoaMatDat: true,
          coVetBui: false,
          huongNhinX: 0.4,
          huongNhinY: -0.4,
        };
      } else {
        const fBat = fDuong - 6;
        const sp = springTatDinh(fBat, 9, 225);
        const batNhay = fBat < 14 ? -Math.sin((fBat / 14) * Math.PI) * 28 : 0;
        const sy =
          fBat < 8
            ? noiSuy(0.86, 1.18, fBat / 8)
            : noiSuy(1.18, 1.02 + Math.sin(f * 0.24) * 0.02, kepGiaTri((fBat - 8) / 14, 0, 1));
        const { squashX, squashY } = baoToanCoGian(sy);
        const rung = Math.sin(f * 0.34) * Math.exp(-fBat / 24);
        ketQua = {
          ...trungTinh,
          offsetX: -4 * kepGiaTri(sp, 0, 1),
          offsetY: batNhay + tho * 1.4,
          squashX,
          squashY,
          gocThan: -7 * kepGiaTri(sp, 0, 1.1) + rung * 3,
          doCongThan: 8 * kepGiaTri(sp, 0, 1),
          gocDau: -8 * kepGiaTri(sp, 0, 1) + rung * 3,
          nhunVai: 5.5 * kepGiaTri(sp, 0, 1),
          vaiPhaiGoc: noiSuy(-10, 118, kepGiaTri(sp, 0, 1.12)) + rung * 10,
          khuyuPhaiGoc: noiSuy(54, 32, kepGiaTri(sp, 0, 1)),
          vaiTraiGoc: noiSuy(-18, -112, kepGiaTri(sp, 0, 1.12)) - rung * 10,
          khuyuTraiGoc: noiSuy(48, 28, kepGiaTri(sp, 0, 1)),
          duiPhaiGoc: 18,
          goiPhaiGoc: -16,
          duiTraiGoc: -18,
          goiTraiGoc: -14,
          nhayY: batNhay,
          dichNgangNoiBo: 0,
          khoaMatDat: batNhay >= -2,
          coVetBui: fBat < 7,
          huongNhinX: 0.9,
          huongNhinY: -0.5,
        };
      }
      break;
    }

    case 'quay_nhin_khan_gia': {
      // Xoay thang ve phia ong kinh, tay phai vay chao / gioi thieu tuong tac voi khan gia
      const vao = easeOutBack(kepGiaTri(fDuong / 12, 0, 1), 1.35);
      const vay = Math.sin(f * 0.28) * 14;
      const mucTieu: ThongSoTuTheFK = {
        offsetX: 0,
        offsetY: Math.sin(f * 0.14) * 1.5,
        ...baoToanCoGian(1.02 + Math.sin(f * 0.14) * 0.018),
        gocThan: -2 + Math.sin(f * 0.14) * 1.4,
        doCongThan: 4,
        gocDau: Math.sin(f * 0.16) * 3.5,
        nhunVai: 1.8,
        vaiPhaiGoc: 124 + vay * 0.6,
        khuyuPhaiGoc: 36 + vay * 0.8,
        vaiTraiGoc: 24 + Math.cos(f * 0.16) * 5,
        khuyuTraiGoc: 48 + Math.sin(f * 0.16) * 5,
        duiPhaiGoc: 13,
        goiPhaiGoc: -12,
        duiTraiGoc: -13,
        goiTraiGoc: -11,
        nhayY: 0,
        dichNgangNoiBo: 0,
        khoaMatDat: true,
        coVetBui: false,
        huongNhinX: 0,
        huongNhinY: 0,
      };
      ketQua = tronTuTheFK(trungTinh, mucTieu, kepGiaTri(vao, 0, 1.08));
      break;
    }

    case 'dung_tho':
    default:
      ketQua = trungTinh;
      break;
  }

  // Lop cu chi khi dang noi (dangNoi = true): cong them nhip vung tay, gat nhe dau, nhun vai
  if (dangNoi) {
    const heSoNoi =
      hanhDong === 'sup_do_tuyet_vong' || hanhDong === 'ho_het_sung_suong'
        ? 0.25
        : hanhDong === 'giat_minh_nhay_dung' && !ketQua.khoaMatDat
          ? 0.2
          : hanhDong === 'khoanh_tay_tu_man'
            ? 0.35
            : 1;

    const nhipNoi =
      Math.sin(f * 0.26) * 0.65 + Math.sin(f * 0.47 + 0.9) * 0.35;
    const nhipTay = Math.sin(f * 0.22 + 0.4) * 0.7 + Math.cos(f * 0.39) * 0.3;

    ketQua.gocDau += nhipNoi * 4.2 * heSoNoi;
    ketQua.nhunVai += Math.abs(Math.sin(f * 0.28)) * 2.4 * heSoNoi;
    ketQua.gocThan += Math.sin(f * 0.18) * 1.6 * heSoNoi;
    ketQua.doCongThan += Math.sin(f * 0.24) * 1.8 * heSoNoi;

    // Vung tay bieu cam nhe khi ke chuyen (tranh pha tu the khoanh tay / chap sau lung / an mung)
    if (
      hanhDong !== 'khoanh_tay_tu_man' &&
      hanhDong !== 'di_qua_di_lai' &&
      hanhDong !== 'ho_het_sung_suong' &&
      hanhDong !== 'bat_tay' &&
      hanhDong !== 'trao_thu'
    ) {
      ketQua.vaiPhaiGoc += nhipTay * 11 * heSoNoi;
      ketQua.khuyuPhaiGoc += Math.sin(f * 0.22 - 0.5) * 12 * heSoNoi;
      ketQua.vaiTraiGoc += Math.cos(f * 0.2) * 5.5 * heSoNoi;
    }
  }

  // Kep cung goc xoay dau an toan (dac biet chat hon voi dong tac nhay an mung / nhay dung / giat minh)
  if (
    hanhDong === 'ho_het_sung_suong' ||
    hanhDong === 'giat_minh_nhay_dung' ||
    hanhDong === 'giat_minh_bat_day'
  ) {
    ketQua.gocDau = kepGiaTri(ketQua.gocDau, -12, 12);
    ketQua.gocThan = kepGiaTri(ketQua.gocThan, -10, 14);
  } else {
    ketQua.gocDau = kepGiaTri(ketQua.gocDau, -18, 22);
  }

  return ketQua;
}
