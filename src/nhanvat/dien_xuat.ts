import type {
  BieuCamTheoMoc,
  Canh,
  HuongNhanVat,
  LoaiBieuCam,
  LuotThoai,
  NhanVatTrongCanh,
} from '../kieu_dai';
import { kepGiaTri } from '../xuong/duong_cong.ts';

export type KetQuaHuongNhin = {
  huongHieuLuc: HuongNhanVat;
  nhinThangOngKinh: boolean;
  lechNhinX: number;
  lechNhinY: number;
};

export type TrangThaiNhanVatDaGiai = NhanVatTrongCanh & {
  /** Frame bat dau cua bong bong thoai hien tai de lo xo bat lai muot khi doi luot */
  frameBatDauThoai: number;
  /** Co nhin thang vao ong kinh / khan gia hay khong */
  nhinThangOngKinh: boolean;
  /** Huong anh mat bo sung tinh tu tuongTacVoi / nguoi dang noi */
  lechNhinX: number;
  lechNhinY: number;
};

/**
 * Tim luot thoai dang hoat dong tai frame cuc bo trong canh.
 */
export function timLuotThoaiTaiFrame(
  luotThoai: readonly LuotThoai[] | undefined,
  frame: number,
): LuotThoai | null {
  if (!luotThoai || luotThoai.length === 0) {
    return null;
  }
  const f = Number.isFinite(frame) ? frame : 0;
  for (const lt of luotThoai) {
    if (f >= lt.batDauFrame && f < lt.ketThucFrame) {
      return lt;
    }
  }
  return null;
}

/**
 * Giai bieu cam hien tai cua nhan vat tai frame tu bieuCamTheoMoc[] (ho tro ca tuFrame lan tienDo [0..1]).
 */
export function giaiBieuCamTheoMoc(
  bieuCamMacDinh: LoaiBieuCam,
  bieuCamTheoMoc: readonly BieuCamTheoMoc[] | undefined,
  frame: number,
  thoiLuongCanh: number,
): { bieuCam: LoaiBieuCam; mocFrameGanNhat: number } {
  if (!bieuCamTheoMoc || bieuCamTheoMoc.length === 0) {
    return { bieuCam: bieuCamMacDinh, mocFrameGanNhat: -1 };
  }

  const f = Number.isFinite(frame) ? frame : 0;
  const tong = Math.max(1, Number.isFinite(thoiLuongCanh) ? thoiLuongCanh : 60);

  const daChuanHoa = bieuCamTheoMoc
    .map((m) => ({
      mocFrame:
        typeof m.tuFrame === 'number' && Number.isFinite(m.tuFrame)
          ? m.tuFrame
          : Math.round(kepGiaTri(m.tienDo ?? 0, 0, 1) * tong),
      bieuCam: m.bieuCam,
    }))
    .sort((a, b) => a.mocFrame - b.mocFrame);

  let ketQua = bieuCamMacDinh;
  let mocGanNhat = -1;
  for (const item of daChuanHoa) {
    if (f >= item.mocFrame) {
      ketQua = item.bieuCam;
      mocGanNhat = item.mocFrame;
    }
  }

  return { bieuCam: ketQua, mocFrameGanNhat: mocGanNhat };
}

/**
 * Tinh huong quay mat va anh mat tuong tac cho nhan vat:
 * - Khi canh la tuong_tac_khan_gia, hanhDong="quay_nhin_khan_gia", hoac tuongTacVoi="khan_gia": nhin thang ong kinh.
 * - Khi co tuongTacVoi (ID nhan vat khac) hoac dang nghe nguoi khac noi trong doi thoai: tu dong quay mat/anh mat ve phia doi phuong.
 */
export function tinhHuongNhinTuongTac(
  nv: NhanVatTrongCanh,
  danhSachNhanVat: readonly NhanVatTrongCanh[],
  tuyChon?: {
    loaiCanh?: Canh['loaiCanh'];
    nguoiDangNoiId?: string | null;
  },
): KetQuaHuongNhin {
  const laTuongTacKhanGia =
    tuyChon?.loaiCanh === 'tuong_tac_khan_gia' ||
    nv.hanhDong === 'quay_nhin_khan_gia' ||
    nv.tuongTacVoi === 'khan_gia';

  if (laTuongTacKhanGia) {
    return {
      huongHieuLuc: nv.huong,
      nhinThangOngKinh: true,
      lechNhinX: 0,
      lechNhinY: 0,
    };
  }

  // Uu tien tuongTacVoi duoc khai bao; neu khong co va co nguoi khac dang noi trong canh, nhin ve nguoi dang noi
  const idMucTieu =
    nv.tuongTacVoi ??
    (tuyChon?.nguoiDangNoiId && tuyChon.nguoiDangNoiId !== nv.id
      ? tuyChon.nguoiDangNoiId
      : undefined);

  if (idMucTieu && idMucTieu !== nv.id) {
    const doiTuong = danhSachNhanVat.find((item) => item.id === idMucTieu);
    if (doiTuong) {
      const dx = doiTuong.x - nv.x;
      const dy = doiTuong.y - nv.y;
      const huongMoi: HuongNhanVat =
        Math.abs(dx) > 24 ? (dx < 0 ? 'trai' : 'phai') : nv.huong;
      const dirMoi = huongMoi === 'trai' ? -1 : 1;
      const khoangCach = Math.max(1, Math.hypot(dx, dy));
      // Anh mat huong mem ve phia mat doi phuong
      const lechNhinX = kepGiaTri(((dx / khoangCach) * dirMoi) * 1.4, -1.6, 1.8);
      const lechNhinY = kepGiaTri((dy / khoangCach) * 1.2, -1.1, 1.1);
      return {
        huongHieuLuc: huongMoi,
        nhinThangOngKinh: false,
        lechNhinX,
        lechNhinY,
      };
    }
  }

  return {
    huongHieuLuc: nv.huong,
    nhinThangOngKinh: false,
    lechNhinX: 0,
    lechNhinY: 0,
  };
}

/**
 * Giai trang thai dong cua tat ca nhan vat trong canh tai frame (ho tro day du luotThoai[], bieuCamTheoMoc[], tuongTacVoi, tuong_tac_khan_gia).
 * Giu tuong thich nguoc 100% khi canh khong dung luotThoai/bieuCamTheoMoc.
 */
export function giaiTrangThaiNhanVatTrongCanh(
  canh: Pick<Canh, 'nhanVat' | 'luotThoai' | 'loaiCanh'>,
  frame: number,
  thoiLuongCanh: number,
): TrangThaiNhanVatDaGiai[] {
  const ds = canh.nhanVat ?? [];
  const coLuotThoai = Boolean(canh.luotThoai && canh.luotThoai.length > 0);
  const luotHienTai = timLuotThoaiTaiFrame(canh.luotThoai, frame);
  const nguoiDangNoiId =
    luotHienTai?.nhanVatId ?? ds.find((n) => n.dangNoi)?.id ?? null;

  return ds.map((nv) => {
    const laNguoiNoiLuot = Boolean(
      luotHienTai && luotHienTai.nhanVatId === nv.id,
    );

    // 1. Giai bieu cam (bieuCamTheoMoc uu tien neu moc moi hon luot thoai, nguoc lai dung luotThoai.bieuCam -> nv.bieuCam)
    const { bieuCam: bieuCamMoc, mocFrameGanNhat } = giaiBieuCamTheoMoc(
      nv.bieuCam,
      nv.bieuCamTheoMoc,
      frame,
      thoiLuongCanh,
    );
    let bieuCamHieuLuc: LoaiBieuCam = bieuCamMoc;
    if (laNguoiNoiLuot && luotHienTai?.bieuCam) {
      if (mocFrameGanNhat < luotHienTai.batDauFrame) {
        bieuCamHieuLuc = luotHienTai.bieuCam;
      }
    }

    // 2. Giai hanh dong, dangNoi, bongBongThoai, bienDoAmThanh theo luotThoai[]
    const hanhDongHieuLuc =
      laNguoiNoiLuot && luotHienTai?.dongTac ? luotHienTai.dongTac : nv.hanhDong;
    const dangNoiHieuLuc = coLuotThoai ? laNguoiNoiLuot : Boolean(nv.dangNoi);
    const bongBongThoaiHieuLuc = coLuotThoai
      ? laNguoiNoiLuot
        ? luotHienTai?.noiDung
        : undefined
      : nv.bongBongThoai;
    const bienDoAmThanhHieuLuc =
      laNguoiNoiLuot && luotHienTai?.bienDoAmThanh
        ? luotHienTai.bienDoAmThanh
        : nv.bienDoAmThanh;
    const frameBatDauThoai =
      laNguoiNoiLuot && luotHienTai ? luotHienTai.batDauFrame : 0;

    // 3. Giai huong mat & anh mat tuong tac
    const huongNhin = tinhHuongNhinTuongTac(
      { ...nv, hanhDong: hanhDongHieuLuc },
      ds,
      {
        loaiCanh: canh.loaiCanh,
        nguoiDangNoiId,
      },
    );

    return {
      ...nv,
      huong: huongNhin.huongHieuLuc,
      hanhDong: hanhDongHieuLuc,
      bieuCam: bieuCamHieuLuc,
      dangNoi: dangNoiHieuLuc,
      bongBongThoai: bongBongThoaiHieuLuc,
      bienDoAmThanh: bienDoAmThanhHieuLuc,
      frameBatDauThoai,
      nhinThangOngKinh: huongNhin.nhinThangOngKinh,
      lechNhinX: huongNhin.lechNhinX,
      lechNhinY: huongNhin.lechNhinY,
    };
  });
}
