import type { HuongNhanVat, LoaiHanhDong } from '../kieu_dai';

export type Diem2D = {
  x: number;
  y: number;
};

export type TuTheKhungXuong = {
  hong: Diem2D;
  co: Diem2D;
  dau: Diem2D;
  vaiTrai: Diem2D;
  khuyuTrai: Diem2D;
  banTayTrai: Diem2D;
  vaiPhai: Diem2D;
  khuyuPhai: Diem2D;
  banTayPhai: Diem2D;
  goiTrai: Diem2D;
  banChanTrai: Diem2D;
  goiPhai: Diem2D;
  banChanPhai: Diem2D;
  diemCamVat: Diem2D;
  gocDau: number;
  doCaoNhay: number;
  dichNgangNoiBo: number;
};

/**
 * Tinh khung xuong nguoi que dien xuat hoat hinh (v0.2).
 * He toa do cuc bo: (0, 0) la mat dat giua hai ban chan, truc Y am huong len tren.
 * Tat dinh 100% theo frameCucBo, khong bao gio tra ve NaN.
 */
export function tinhKhungXuongCoBan(
  hanhDong: LoaiHanhDong,
  frameCucBo: number,
  huong: HuongNhanVat,
): TuTheKhungXuong {
  const f = Number.isFinite(frameCucBo) ? frameCucBo : 0;
  const dir = huong === 'trai' ? -1 : 1;

  const nhipTho = Math.sin(f * 0.13) * 2.6;
  const lacTay = Math.sin(f * 0.16) * 5;

  let hongY = -88 + nhipTho * 0.45;
  let hongX = 0;
  let nghiengThanX = 0;
  let chieuDaiThan = 72;
  let nhayY = 0;
  let gocDau = 0;
  let dichNgangNoiBo = 0;

  let tayTruocDX = 26 * dir;
  let tayTruocDY = 24;
  let taySauDX = -22 * dir;
  let taySauDY = 26;
  let khuyuTruocLechX = -4 * dir;
  let khuyuTruocLechY = 12;
  let khuyuSauLechX = 4 * dir;
  let khuyuSauLechY = 12;

  let chanPhaiX = 18 * dir;
  let chanPhaiY = 0;
  let chanTraiX = -18 * dir;
  let chanTraiY = 0;
  let goiPhaiLechX = 5 * dir;
  let goiTraiLechX = -5 * dir;

  switch (hanhDong) {
    case 'di_bo': {
      const pha = f * 0.24;
      const buoc = Math.sin(pha);
      const nhun = Math.abs(Math.sin(pha)) * 6;
      hongY = -88 - nhun;
      nghiengThanX = 5 * dir;
      chanPhaiX = (6 + buoc * 26) * dir;
      chanTraiX = (-6 - buoc * 26) * dir;
      chanPhaiY = Math.min(0, -Math.cos(pha) * 10);
      chanTraiY = Math.min(0, Math.cos(pha) * 10);
      tayTruocDX = (18 - buoc * 22) * dir;
      tayTruocDY = 24 - Math.abs(buoc) * 4;
      taySauDX = (-18 + buoc * 22) * dir;
      taySauDY = 24 - Math.abs(buoc) * 4;
      break;
    }

    case 'chay_voi_va': {
      const pha = f * 0.44;
      const buoc = Math.sin(pha);
      const nhun = Math.abs(Math.sin(pha)) * 12;
      hongY = -86 - nhun;
      nhayY = -nhun * 0.6;
      nghiengThanX = 16 * dir;
      chanPhaiX = (8 + buoc * 36) * dir;
      chanTraiX = (-8 - buoc * 36) * dir;
      chanPhaiY = Math.min(0, -Math.cos(pha) * 18);
      chanTraiY = Math.min(0, Math.cos(pha) * 18);
      goiPhaiLechX = 12 * dir;
      goiTraiLechX = 6 * dir;
      tayTruocDX = (24 - buoc * 28) * dir;
      tayTruocDY = 8;
      taySauDX = (-24 + buoc * 28) * dir;
      taySauDY = 10;
      gocDau = 6 * dir;
      break;
    }

    case 'ngoi_doc_sach': {
      hongY = -50 + nhipTho * 0.3;
      hongX = -10 * dir;
      nghiengThanX = 8 * dir;
      chieuDaiThan = 66;
      chanPhaiX = 28 * dir;
      chanTraiX = 14 * dir;
      goiPhaiLechX = 24 * dir;
      goiTraiLechX = 18 * dir;
      tayTruocDX = 34 * dir;
      tayTruocDY = 10 + Math.sin(f * 0.1) * 2;
      taySauDX = 22 * dir;
      taySauDY = 12 + Math.sin(f * 0.1) * 2;
      gocDau = 14 * dir;
      break;
    }

    case 'chi_tro_giai_thich': {
      nghiengThanX = 6 * dir;
      tayTruocDX = 56 * dir;
      tayTruocDY = -18 + Math.sin(f * 0.22) * 7;
      khuyuTruocLechY = 6;
      taySauDX = -18 * dir;
      taySauDY = 20 + Math.cos(f * 0.18) * 4;
      gocDau = Math.sin(f * 0.16) * 3 * dir;
      break;
    }

    case 'nhin_len_troi': {
      nghiengThanX = -6 * dir;
      tayTruocDX = 38 * dir;
      tayTruocDY = -34 + Math.sin(f * 0.14) * 4;
      taySauDX = -20 * dir;
      taySauDY = 24;
      gocDau = -18 * dir;
      break;
    }

    case 'gat_gu_dong_tinh': {
      const gat = Math.sin(f * 0.26);
      gocDau = (6 + gat * 10) * dir;
      nghiengThanX = (2 + gat * 3) * dir;
      tayTruocDX = 30 * dir;
      tayTruocDY = 4 + gat * 6;
      taySauDX = -18 * dir;
      taySauDY = 24;
      break;
    }

    case 'gai_dau_kho_hieu': {
      const gai = Math.sin(f * 0.38) * 3;
      nghiengThanX = -5 * dir;
      gocDau = -8 * dir;
      tayTruocDX = (6 + gai) * dir;
      tayTruocDY = -40;
      khuyuTruocLechX = 22 * dir;
      khuyuTruocLechY = -8;
      taySauDX = -14 * dir;
      taySauDY = 32;
      khuyuSauLechX = -16 * dir;
      break;
    }

    case 'giat_minh_nhay_dung': {
      // 3 pha hai huoc: nhun (0..6) -> bat nhay cao (6..24) -> roi xuong dat (24..42)
      const c = ((f % 42) + 42) % 42;
      if (c < 6) {
        const t = c / 6;
        hongY = -88 + t * 18;
        chieuDaiThan = 72 - t * 6;
        tayTruocDX = 22 * dir;
        tayTruocDY = 14;
        taySauDX = -22 * dir;
        taySauDY = 14;
      } else if (c < 26) {
        const t = (c - 6) / 20;
        const arc = Math.sin(t * Math.PI);
        nhayY = -arc * 68;
        hongY = -88 + nhayY;
        tayTruocDX = 42 * dir;
        tayTruocDY = -36 - arc * 12;
        taySauDX = -42 * dir;
        taySauDY = -32 - arc * 12;
        chanPhaiX = (22 + arc * 14) * dir;
        chanTraiX = (-22 - arc * 14) * dir;
        chanPhaiY = nhayY * 0.72;
        chanTraiY = nhayY * 0.72;
        gocDau = -6 * dir;
      } else {
        const t = (c - 26) / 16;
        const settle = Math.sin(t * Math.PI) * 10;
        hongY = -88 + settle;
        tayTruocDX = 30 * dir;
        tayTruocDY = -6;
        taySauDX = -28 * dir;
        taySauDY = -4;
      }
      break;
    }

    case 'bo_tay_can_loi': {
      // Dua tay len vo tran, vai hoi xiu xuong kieu can loi
      nghiengThanX = -4 * dir;
      hongY = -86 + nhipTho * 0.3;
      gocDau = 8 * dir;
      tayTruocDX = 10 * dir;
      tayTruocDY = -26;
      khuyuTruocLechX = 20 * dir;
      khuyuTruocLechY = 4;
      taySauDX = -16 * dir;
      taySauDY = 34;
      khuyuSauLechX = -10 * dir;
      break;
    }

    case 'khoanh_tay_tu_man': {
      // Khoanh tay truoc nguc, uon nguc, ngua nhe dau tu man
      nghiengThanX = -7 * dir;
      gocDau = -12 * dir;
      tayTruocDX = -6 * dir;
      tayTruocDY = 20;
      khuyuTruocLechX = 20 * dir;
      khuyuTruocLechY = 18;
      taySauDX = 16 * dir;
      taySauDY = 22;
      khuyuSauLechX = -18 * dir;
      khuyuSauLechY = 18;
      chanPhaiX = 20 * dir;
      chanTraiX = -20 * dir;
      break;
    }

    case 'ho_het_sung_suong': {
      const arc = Math.abs(Math.sin(f * 0.24));
      nhayY = -arc * 32;
      hongY = -88 + nhayY;
      tayTruocDX = 36 * dir;
      tayTruocDY = -48 - arc * 6;
      taySauDX = -36 * dir;
      taySauDY = -48 - arc * 6;
      khuyuTruocLechY = 4;
      khuyuSauLechY = 4;
      chanPhaiY = nhayY * 0.55;
      chanTraiY = nhayY * 0.55;
      gocDau = -8 * dir;
      break;
    }

    case 'di_qua_di_lai': {
      const phaDi = f * 0.055;
      dichNgangNoiBo = Math.sin(phaDi) * 58;
      const buoc = Math.sin(f * 0.24);
      const nhun = Math.abs(buoc) * 5;
      hongY = -88 - nhun;
      nghiengThanX = 4 * dir;
      chanPhaiX = (5 + buoc * 22) * dir;
      chanTraiX = (-5 - buoc * 22) * dir;
      chanPhaiY = Math.min(0, -Math.cos(f * 0.24) * 8);
      chanTraiY = Math.min(0, Math.cos(f * 0.24) * 8);
      // Tay chap sau lung suy tu khi di qua di lai
      tayTruocDX = -14 * dir;
      tayTruocDY = 32;
      taySauDX = -18 * dir;
      taySauDY = 34;
      gocDau = 8 * dir;
      break;
    }

    case 'sup_do_tuyet_vong': {
      // Guc nguoi xuong san hai huoc (quy goi, tay chong dat, dau cui ru)
      hongY = -36;
      hongX = -18 * dir;
      nghiengThanX = 34 * dir;
      chieuDaiThan = 52;
      chanPhaiX = -26 * dir;
      chanTraiX = -42 * dir;
      goiPhaiLechX = 12 * dir;
      goiTraiLechX = 6 * dir;
      tayTruocDX = 26 * dir;
      tayTruocDY = 48;
      taySauDX = 10 * dir;
      taySauDY = 50;
      khuyuTruocLechX = 4 * dir;
      khuyuTruocLechY = 8;
      gocDau = 28 * dir;
      break;
    }

    case 'dung_tho':
    default:
      tayTruocDY = 24 + lacTay * 0.35;
      taySauDY = 26 - lacTay * 0.35;
      break;
  }

  const hong: Diem2D = { x: hongX, y: hongY };
  const co: Diem2D = {
    x: hong.x + nghiengThanX,
    y: hong.y - chieuDaiThan + nhipTho * 0.5,
  };
  const dau: Diem2D = {
    x: co.x + 2 * dir + (hanhDong === 'sup_do_tuyet_vong' ? 12 * dir : 0),
    y: co.y - 28 + (hanhDong === 'sup_do_tuyet_vong' ? 10 : 0),
  };

  const vaiPhai: Diem2D = { x: co.x + 11 * dir, y: co.y + 6 };
  const banTayPhai: Diem2D = {
    x: vaiPhai.x + tayTruocDX,
    y: vaiPhai.y + tayTruocDY,
  };
  const khuyuPhai: Diem2D = {
    x: (vaiPhai.x + banTayPhai.x) / 2 + khuyuTruocLechX,
    y: (vaiPhai.y + banTayPhai.y) / 2 + khuyuTruocLechY,
  };

  const vaiTrai: Diem2D = { x: co.x - 11 * dir, y: co.y + 6 };
  const banTayTrai: Diem2D = {
    x: vaiTrai.x + taySauDX,
    y: vaiTrai.y + taySauDY,
  };
  const khuyuTrai: Diem2D = {
    x: (vaiTrai.x + banTayTrai.x) / 2 + khuyuSauLechX,
    y: (vaiTrai.y + banTayTrai.y) / 2 + khuyuSauLechY,
  };

  const banChanPhai: Diem2D = { x: chanPhaiX, y: chanPhaiY };
  const goiPhai: Diem2D = {
    x: (hong.x + banChanPhai.x) / 2 + goiPhaiLechX,
    y: (hong.y + banChanPhai.y) / 2 - 4,
  };

  const banChanTrai: Diem2D = { x: chanTraiX, y: chanTraiY };
  const goiTrai: Diem2D = {
    x: (hong.x + banChanTrai.x) / 2 + goiTraiLechX,
    y: (hong.y + banChanTrai.y) / 2 - 4,
  };

  const diemCamVat: Diem2D = {
    x: banTayPhai.x + 3 * dir,
    y: banTayPhai.y - 2,
  };

  return {
    hong,
    co,
    dau,
    vaiTrai,
    khuyuTrai,
    banTayTrai,
    vaiPhai,
    khuyuPhai,
    banTayPhai,
    goiTrai,
    banChanTrai,
    goiPhai,
    banChanPhai,
    diemCamVat,
    gocDau,
    doCaoNhay: Math.max(0, -nhayY),
    dichNgangNoiBo,
  };
}
