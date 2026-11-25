import type {
  CauHinhCamera,
  CauHinhMayQuay,
  DaoCuTrongCanh,
  GocQuayCamera,
  LuotThoai,
  NhanVatTrongCanh,
} from '../kieu_dai';
import {
  easeInOutCubic,
  easeInOutSine,
  easeOutBack,
  kepGiaTri,
  noiSuy,
  springTatDinh,
} from '../xuong/duong_cong.ts';

export type KetQuaBienDoiCamera = {
  zoom: number;
  panX: number;
  panY: number;
  rot: number;
  gocQuayHieuLuc?: GocQuayCamera;
  nhanVatDangFocus?: string | null;
  laChiaDoiManHinh?: boolean;
};

export const CAMERA_MAC_DINH: KetQuaBienDoiCamera = {
  zoom: 1,
  panX: 0,
  panY: 0,
  rot: 0,
  gocQuayHieuLuc: 'toan_canh',
  nhanVatDangFocus: null,
  laChiaDoiManHinh: false,
};

const KHUNG_RONG = 1920;
const KHUNG_CAO = 1080;
const TAM_X = KHUNG_RONG / 2;
const TAM_Y = KHUNG_CAO / 2;
const THOI_LUONG_CHUYEN_FOCUS = 16;
const NGUONG_RMS_NOI = 0.075;

/** Tinh vi tri thuc cua nhan vat tai frame (ho tro diChuyenDenX tat dinh) */
export function tinhViTriNhanVatTaiFrame(
  nv: NhanVatTrongCanh,
  frame: number,
  thoiLuongCanh: number,
): { x: number; y: number } {
  if (typeof nv.diChuyenDenX === 'number') {
    const t = easeInOutSine(
      kepGiaTri(frame / Math.max(1, thoiLuongCanh), 0, 1),
    );
    return {
      x: noiSuy(nv.x, nv.diChuyenDenX, t),
      y: nv.y,
    };
  }
  return { x: nv.x, y: nv.y };
}

/**
 * Tinh panX, panY an toan sao cho khung hinh 1920x1080 sau khi scale khong bao gio lo vien den.
 * Voi transformOrigin: center center va transform: translate3d(panX, panY, 0) scale(zoom),
 * gioi han bien tuyet doi la |panX| <= 960 * (zoom - 1) va |panY| <= 540 * (zoom - 1).
 */
export function tinhPanAnToan(
  tamX: number,
  tamY: number,
  zoom: number,
  heSoBam = 0.9,
): { panX: number; panY: number } {
  const z = Math.max(1, Number.isFinite(zoom) ? zoom : 1);
  const maxPanX = Math.max(0, TAM_X * (z - 1));
  const maxPanY = Math.max(0, TAM_Y * (z - 1));
  const rawX = (TAM_X - tamX) * z * heSoBam;
  const rawY = (TAM_Y - tamY) * z * heSoBam;
  return {
    panX: kepGiaTri(rawX, -maxPanX, maxPanX),
    panY: kepGiaTri(rawY, -maxPanY, maxPanY),
  };
}

/** Tinh trung binh bien do RMS trong cua so truot [frame - 10 .. frame] tat dinh 100% */
function tinhNangLuongRmsCuaSo(
  rms: readonly number[] | undefined,
  frame: number,
  cuaSo = 10,
): number {
  if (!rms || rms.length === 0) {
    return 0;
  }
  const fCuoi = Math.min(rms.length - 1, Math.floor(frame));
  if (fCuoi < 0) {
    return 0;
  }
  const fDau = Math.max(0, fCuoi - cuaSo);
  let tong = 0;
  let dem = 0;
  for (let i = fDau; i <= fCuoi; i++) {
    const v = rms[i];
    if (typeof v === 'number' && Number.isFinite(v) && v >= 0) {
      tong += v;
      dem++;
    }
  }
  return dem > 0 ? tong / dem : 0;
}

/** Xac dinh nhanh ID nhan vat dang noi tai frame (uu tien luotThoai -> RMS rieng -> dangNoi) */
export function xacDinhNguoiDangNoiTaiFrame(
  frame: number,
  nhanVat?: readonly NhanVatTrongCanh[],
  luotThoai?: readonly LuotThoai[],
): string | null {
  if (luotThoai && luotThoai.length > 0) {
    for (const lt of luotThoai) {
      if (frame >= lt.batDauFrame && frame < lt.ketThucFrame) {
        return lt.nhanVatId;
      }
    }
    return null;
  }

  if (nhanVat && nhanVat.length > 0) {
    let idRmsMax: string | null = null;
    let rmsMax = NGUONG_RMS_NOI;
    for (const nv of nhanVat) {
      const e = tinhNangLuongRmsCuaSo(nv.bienDoAmThanh, frame, 10);
      if (e > rmsMax) {
        rmsMax = e;
        idRmsMax = nv.id;
      }
    }
    if (idRmsMax) {
      return idRmsMax;
    }

    const nvNoi = nhanVat.find((nv) => Boolean(nv.dangNoi));
    if (nvNoi) {
      return nvNoi.id;
    }
  }

  return null;
}

/** Tinh goc quay co so (truoc khi ap dung tuDongFocusNguoiNoi) cho du 8 kieu gocQuay v2.0 */
function tinhGocQuayCoSo(
  gocQuay: GocQuayCamera,
  f: number,
  tong: number,
  mayQuay: CauHinhMayQuay,
  nhanVat?: readonly NhanVatTrongCanh[],
  daoCu?: readonly DaoCuTrongCanh[],
): { zoom: number; panX: number; panY: number; rot: number } {
  const tienDo = kepGiaTri(f / tong, 0, 1);
  const vaoMuot = easeInOutCubic(kepGiaTri(f / 18, 0, 1));
  const coDiem = mayQuay.diemTieuCu;
  const dsNv = nhanVat ?? [];

  const timTamNhanVat = (): { x: number; y: number } => {
    if (coDiem) return coDiem;
    if (dsNv.length === 0) return { x: TAM_X, y: TAM_Y };
    let sx = 0;
    let sy = 0;
    for (const nv of dsNv) {
      const p = tinhViTriNhanVatTaiFrame(nv, f, tong);
      sx += p.x;
      sy += p.y - 135;
    }
    return { x: sx / dsNv.length, y: sy / dsNv.length };
  };

  switch (gocQuay) {
    case 'toan_canh': {
      const zoomDich = kepGiaTri(mayQuay.doPhong ?? 1.03, 1.0, 1.25);
      const zoom = noiSuy(1, zoomDich, easeInOutSine(tienDo));
      const tam = coDiem ?? { x: TAM_X, y: TAM_Y };
      const { panX, panY } = tinhPanAnToan(tam.x, tam.y, zoom, 0.5);
      return { zoom, panX, panY, rot: 0 };
    }

    case 'trung_canh': {
      const zoomGoc = kepGiaTri(mayQuay.doPhong ?? 1.2, 1.05, 1.6);
      const zoom = noiSuy(1.04, zoomGoc, vaoMuot) + easeInOutSine(tienDo) * 0.03;
      const tam = timTamNhanVat();
      const { panX, panY } = tinhPanAnToan(tam.x, tam.y, zoom, 0.85);
      return { zoom, panX, panY, rot: 0 };
    }

    case 'can_mat': {
      const zoomGoc = kepGiaTri(mayQuay.doPhong ?? 1.58, 1.25, 2.0);
      const loXo = kepGiaTri(springTatDinh(f, 14, 170), 0, 1.08);
      const zoom = noiSuy(1.06, zoomGoc, loXo);
      let tam = coDiem;
      if (!tam) {
        const nvChinh = dsNv.find((nv) => nv.dangNoi) ?? dsNv[0];
        if (nvChinh) {
          const p = tinhViTriNhanVatTaiFrame(nvChinh, f, tong);
          tam = { x: p.x, y: p.y - 165 };
        } else {
          tam = { x: TAM_X, y: TAM_Y - 60 };
        }
      }
      const { panX, panY } = tinhPanAnToan(tam.x, tam.y, zoom, 0.95);
      return { zoom, panX, panY, rot: 0 };
    }

    case 'focus_trai': {
      const zoomGoc = kepGiaTri(mayQuay.doPhong ?? 1.34, 1.12, 1.75);
      const zoom = noiSuy(1.05, zoomGoc, vaoMuot) + easeInOutSine(tienDo) * 0.025;
      let tam = coDiem;
      if (!tam) {
        const traiNhat =
          dsNv.length > 0
            ? [...dsNv].sort((a, b) => a.x - b.x)[0]
            : undefined;
        if (traiNhat) {
          const p = tinhViTriNhanVatTaiFrame(traiNhat, f, tong);
          tam = { x: p.x, y: p.y - 140 };
        } else {
          tam = { x: 520, y: 540 };
        }
      }
      const { panX, panY } = tinhPanAnToan(tam.x, tam.y, zoom, 0.92);
      return { zoom, panX, panY, rot: 0 };
    }

    case 'focus_phai': {
      const zoomGoc = kepGiaTri(mayQuay.doPhong ?? 1.34, 1.12, 1.75);
      const zoom = noiSuy(1.05, zoomGoc, vaoMuot) + easeInOutSine(tienDo) * 0.025;
      let tam = coDiem;
      if (!tam) {
        const phaiNhat =
          dsNv.length > 0
            ? [...dsNv].sort((a, b) => b.x - a.x)[0]
            : undefined;
        if (phaiNhat) {
          const p = tinhViTriNhanVatTaiFrame(phaiNhat, f, tong);
          tam = { x: p.x, y: p.y - 140 };
        } else {
          tam = { x: 1400, y: 540 };
        }
      }
      const { panX, panY } = tinhPanAnToan(tam.x, tam.y, zoom, 0.92);
      return { zoom, panX, panY, rot: 0 };
    }

    case 'zoom_dao_cu': {
      const zoomGoc = kepGiaTri(mayQuay.doPhong ?? 1.44, 1.15, 1.85);
      const tienDoZoom = easeInOutCubic(kepGiaTri(f / 22, 0, 1));
      const zoom = noiSuy(1.02, zoomGoc, tienDoZoom) + Math.sin(tienDo * Math.PI) * 0.02;
      let tam = coDiem;
      if (!tam) {
        if (daoCu && daoCu.length > 0) {
          tam = { x: daoCu[0].x, y: daoCu[0].y };
        } else {
          tam = { x: TAM_X, y: TAM_Y - 30 };
        }
      }
      const { panX, panY } = tinhPanAnToan(tam.x, tam.y, zoom, 0.92);
      return { zoom, panX, panY, rot: 0 };
    }

    case 'pan_ngang': {
      const zoom = kepGiaTri(mayQuay.doPhong ?? 1.16, 1.12, 1.45);
      const maxPanX = Math.max(24, TAM_X * (zoom - 1) * 0.88);
      const panTheoPhai = !coDiem || coDiem.x >= TAM_X;
      const e = easeInOutSine(tienDo);
      const panX = panTheoPhai
        ? noiSuy(maxPanX, -maxPanX, e)
        : noiSuy(-maxPanX, maxPanX, e);
      const panY = coDiem
        ? tinhPanAnToan(coDiem.x, coDiem.y, zoom, 0.45).panY
        : Math.sin(e * Math.PI) * -6;
      return { zoom, panX, panY, rot: 0 };
    }

    case 'chia_doi_man_hinh':
    default:
      return { zoom: 1, panX: 0, panY: 0, rot: 0 };
  }
}

/**
 * Tinh bien doi camera tat dinh 100% theo frame (v2.0 + tuong thich nguoc 100% voi camera cu):
 * - Neu truyen mayQuay (v2.0): ho tro du 8 gocQuay + doPhong + diemTieuCu + tuDongFocusNguoiNoi (1.2x-1.45x).
 * - Neu chi truyen camera (v0.4): giu nguyen toan bo hanh vi tinh / pan_nhe / zoom_cham / zoom_hai_huoc.
 */
export function tinhBienDoiCamera(
  frame: number,
  thoiLuongCanh: number,
  camera?: CauHinhCamera,
  nhanVat?: NhanVatTrongCanh[],
  mayQuay?: CauHinhMayQuay,
  luotThoai?: readonly LuotThoai[],
  daoCu?: readonly DaoCuTrongCanh[],
): KetQuaBienDoiCamera {
  const f = Number.isFinite(frame) ? frame : 0;
  const tong = Math.max(1, Number.isFinite(thoiLuongCanh) ? thoiLuongCanh : 60);

  // Che do dao dien v2.0 khi co khai bao mayQuay
  if (mayQuay) {
    const gocQuay: GocQuayCamera = mayQuay.gocQuay ?? 'toan_canh';
    const nguoiDangNoi = xacDinhNguoiDangNoiTaiFrame(f, nhanVat, luotThoai);

    if (gocQuay === 'chia_doi_man_hinh') {
      return {
        zoom: 1,
        panX: 0,
        panY: 0,
        rot: 0,
        gocQuayHieuLuc: 'chia_doi_man_hinh',
        nhanVatDangFocus: nguoiDangNoi,
        laChiaDoiManHinh: true,
      };
    }

    const coSo = tinhGocQuayCoSo(gocQuay, f, tong, mayQuay, nhanVat, daoCu);
    let { zoom, panX, panY, rot } = coSo;

    // Tu dong lia & zoom nhe (1.2x - 1.45x) sang nhan vat dang noi / co bien do RMS, tra may muot khi doi nguoi
    if (mayQuay.tuDongFocusNguoiNoi && nhanVat && nhanVat.length > 0) {
      const zoomFocus = kepGiaTri(mayQuay.doPhong ?? 1.32, 1.2, 1.45);

      const tinhMucTieuFocus = (nvId: string | null) => {
        if (!nvId) {
          return { zoom: coSo.zoom, panX: coSo.panX, panY: coSo.panY };
        }
        const nv = nhanVat.find((item) => item.id === nvId);
        if (!nv) {
          return { zoom: coSo.zoom, panX: coSo.panX, panY: coSo.panY };
        }
        const pos = tinhViTriNhanVatTaiFrame(nv, f, tong);
        const { panX: px, panY: py } = tinhPanAnToan(
          pos.x,
          pos.y - 145,
          zoomFocus,
          0.9,
        );
        return { zoom: zoomFocus, panX: px, panY: py };
      };

      if (luotThoai && luotThoai.length > 0) {
        const danhSachSapXep = [...luotThoai].sort(
          (a, b) => a.batDauFrame - b.batDauFrame,
        );
        const idxHienTai = danhSachSapXep.findIndex(
          (lt) => f >= lt.batDauFrame && f < lt.ketThucFrame,
        );

        if (idxHienTai >= 0) {
          const luotCur = danhSachSapXep[idxHienTai];
          const luotTruoc = idxHienTai > 0 ? danhSachSapXep[idxHienTai - 1] : null;
          const ganLuotTruoc =
            luotTruoc !== null &&
            luotCur.batDauFrame - luotTruoc.ketThucFrame <= 24;
          const diemXuatPhat = ganLuotTruoc
            ? tinhMucTieuFocus(luotTruoc.nhanVatId)
            : { zoom: coSo.zoom, panX: coSo.panX, panY: coSo.panY };
          const diemDich = tinhMucTieuFocus(luotCur.nhanVatId);
          const tChuyen = easeInOutCubic(
            kepGiaTri((f - luotCur.batDauFrame) / THOI_LUONG_CHUYEN_FOCUS, 0, 1),
          );
          zoom = noiSuy(diemXuatPhat.zoom, diemDich.zoom, tChuyen);
          panX = noiSuy(diemXuatPhat.panX, diemDich.panX, tChuyen);
          panY = noiSuy(diemXuatPhat.panY, diemDich.panY, tChuyen);
        } else {
          // Khoang lang giua cac luot hoac sau luot cuoi: tra may muot ve khung co so
          let luotVuaXong: LuotThoai | null = null;
          for (const lt of danhSachSapXep) {
            if (lt.ketThucFrame <= f) {
              luotVuaXong = lt;
            }
          }
          if (
            luotVuaXong &&
            f - luotVuaXong.ketThucFrame < THOI_LUONG_CHUYEN_FOCUS
          ) {
            const diemCu = tinhMucTieuFocus(luotVuaXong.nhanVatId);
            const tTra = easeInOutCubic(
              kepGiaTri(
                (f - luotVuaXong.ketThucFrame) / THOI_LUONG_CHUYEN_FOCUS,
                0,
                1,
              ),
            );
            zoom = noiSuy(diemCu.zoom, coSo.zoom, tTra);
            panX = noiSuy(diemCu.panX, coSo.panX, tTra);
            panY = noiSuy(diemCu.panY, coSo.panY, tTra);
          }
        }
      } else {
        // Ho tro focus tu dong theo bien do RMS rieng cua nhan vat (khong giat nho cua so truot)
        let nvRmsMax: NhanVatTrongCanh | null = null;
        let eMax = 0;
        for (const nv of nhanVat) {
          const e = tinhNangLuongRmsCuaSo(nv.bienDoAmThanh, f, 12);
          if (e > eMax) {
            eMax = e;
            nvRmsMax = nv;
          }
        }

        if (nvRmsMax && eMax > 0.05) {
          const mucTieu = tinhMucTieuFocus(nvRmsMax.id);
          const trongSo = easeInOutCubic(
            kepGiaTri((eMax - 0.05) / 0.16, 0, 1),
          );
          zoom = noiSuy(coSo.zoom, mucTieu.zoom, trongSo);
          panX = noiSuy(coSo.panX, mucTieu.panX, trongSo);
          panY = noiSuy(coSo.panY, mucTieu.panY, trongSo);
        } else if (nguoiDangNoi) {
          const mucTieu = tinhMucTieuFocus(nguoiDangNoi);
          const tVao = easeInOutCubic(
            kepGiaTri(f / THOI_LUONG_CHUYEN_FOCUS, 0, 1),
          );
          zoom = noiSuy(coSo.zoom, mucTieu.zoom, tVao);
          panX = noiSuy(coSo.panX, mucTieu.panX, tVao);
          panY = noiSuy(coSo.panY, mucTieu.panY, tVao);
        }
      }
    }

    if (mayQuay.rungNhe || camera?.rungNhe) {
      panX += Math.sin(f * 2.15) * 4.2;
      panY += Math.cos(f * 2.75) * 3.2;
      rot += Math.sin(f * 1.8) * 0.35;
    }

    return {
      zoom,
      panX,
      panY,
      rot,
      gocQuayHieuLuc: gocQuay,
      nhanVatDangFocus: nguoiDangNoi,
      laChiaDoiManHinh: false,
    };
  }

  // Che do tuong thich nguoc 100% voi CauHinhCamera (v0.4)
  const kieu = camera?.kieu ?? 'tinh';

  let zoom = camera?.zoom ?? 1;
  let panX = camera?.panX ?? 0;
  let panY = camera?.panY ?? 0;
  let rot = 0;

  let tamX = camera?.mucTieuX ?? TAM_X;
  let tamY = camera?.mucTieuY ?? TAM_Y;
  if (camera?.theoDoiNhanVat && nhanVat && nhanVat.length > 0) {
    const nv = nhanVat.find((item) => item.id === camera.theoDoiNhanVat);
    if (nv) {
      const pos = tinhViTriNhanVatTaiFrame(nv, f, tong);
      tamX = pos.x;
      tamY = pos.y - 135;
    }
  } else if (
    kieu === 'zoom_hai_huoc' &&
    camera?.mucTieuX === undefined &&
    nhanVat &&
    nhanVat.length > 0
  ) {
    tamX = nhanVat[0].x;
    tamY = nhanVat[0].y - 135;
  }

  switch (kieu) {
    case 'pan_nhe': {
      const tienDo = easeInOutSine(kepGiaTri(f / tong, 0, 1));
      zoom = Math.max(1.06, camera?.zoom ?? 1.07);
      panX += noiSuy(-38, 38, tienDo);
      panY += Math.sin(tienDo * Math.PI) * -4;
      break;
    }

    case 'zoom_cham': {
      const tienDo = easeInOutCubic(kepGiaTri(f / tong, 0, 1));
      const zoomDich = camera?.zoom ?? 1.09;
      zoom = noiSuy(1, zoomDich, tienDo);
      panX += (TAM_X - tamX) * (zoom - 1) * 0.45;
      panY += (TAM_Y - tamY) * (zoom - 1) * 0.45;
      break;
    }

    case 'zoom_hai_huoc': {
      const zoomMucTieu = camera?.zoom ?? 1.46;
      const t = kepGiaTri(f / 13, 0, 1);
      const back = easeOutBack(t, 1.85);
      zoom = 1 + (zoomMucTieu - 1) * back;
      panX += (TAM_X - tamX) * (zoom - 1) * 0.85;
      panY += (TAM_Y - tamY) * (zoom - 1) * 0.85;
      if (f >= 4 && f <= 16) {
        const suyGiam = 1 - (f - 4) / 12;
        rot = Math.sin((f - 4) * 1.6) * 1.35 * suyGiam;
      }
      break;
    }

    case 'tinh':
    default:
      if (camera?.theoDoiNhanVat) {
        panX += (TAM_X - tamX) * 0.2;
        panY += (TAM_Y - tamY) * 0.14;
      }
      break;
  }

  if (camera?.rungNhe) {
    panX += Math.sin(f * 2.15) * 4.2;
    panY += Math.cos(f * 2.75) * 3.2;
    rot += Math.sin(f * 1.8) * 0.35;
  }

  return {
    zoom,
    panX,
    panY,
    rot,
    gocQuayHieuLuc: 'toan_canh',
    nhanVatDangFocus: camera?.theoDoiNhanVat ?? null,
    laChiaDoiManHinh: false,
  };
}
