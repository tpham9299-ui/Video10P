import React, { createContext, useContext } from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import type {
  CauHinhCamera,
  LoaiChuyenCanh,
  NhanVatTrongCanh,
} from '../kieu_dai';
import {
  easeInOutCubic,
  easeInOutSine,
  easeOutBack,
  kepGiaTri,
  noiSuy,
} from '../xuong/duong_cong';

export type KetQuaBienDoiCamera = {
  zoom: number;
  panX: number;
  panY: number;
  rot: number;
};

const CAMERA_MAC_DINH: KetQuaBienDoiCamera = {
  zoom: 1,
  panX: 0,
  panY: 0,
  rot: 0,
};

/** Context chia se bien doi camera cho he thong Parallax 3 lop trong BoiCanhHoatHinh */
export const CameraParallaxContext =
  createContext<KetQuaBienDoiCamera>(CAMERA_MAC_DINH);

export function useCameraParallax(): KetQuaBienDoiCamera {
  return useContext(CameraParallaxContext);
}

/**
 * Tinh bien doi camera tat dinh 100% theo frame (v0.4):
 * - tinh: giu khung on dinh
 * - pan_nhe: luot ngang em ai voi easeInOutSine
 * - zoom_cham: Ken Burns phong cham muot voi easeInOutCubic
 * - zoom_hai_huoc: giat gon vao nhan vat bang easeOutBack co vuot da & hoi nhe
 */
export function tinhBienDoiCamera(
  frame: number,
  thoiLuongCanh: number,
  camera?: CauHinhCamera,
  nhanVat?: NhanVatTrongCanh[],
): KetQuaBienDoiCamera {
  const f = Number.isFinite(frame) ? frame : 0;
  const tong = Math.max(1, Number.isFinite(thoiLuongCanh) ? thoiLuongCanh : 60);
  const kieu = camera?.kieu ?? 'tinh';

  let zoom = camera?.zoom ?? 1;
  let panX = camera?.panX ?? 0;
  let panY = camera?.panY ?? 0;
  let rot = 0;

  let tamX = camera?.mucTieuX ?? 960;
  let tamY = camera?.mucTieuY ?? 540;
  if (camera?.theoDoiNhanVat && nhanVat && nhanVat.length > 0) {
    const nv = nhanVat.find((item) => item.id === camera.theoDoiNhanVat);
    if (nv) {
      tamX = nv.x;
      tamY = nv.y - 135;
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
      panX += (960 - tamX) * (zoom - 1) * 0.45;
      panY += (540 - tamY) * (zoom - 1) * 0.45;
      break;
    }

    case 'zoom_hai_huoc': {
      // Giat gon vao nhan vat bang easeOutBack trong 13 frame dau (vuot da roi hoi em)
      const zoomMucTieu = camera?.zoom ?? 1.46;
      const t = kepGiaTri(f / 13, 0, 1);
      const back = easeOutBack(t, 1.85);
      zoom = 1 + (zoomMucTieu - 1) * back;
      panX += (960 - tamX) * (zoom - 1) * 0.85;
      panY += (540 - tamY) * (zoom - 1) * 0.85;
      if (f >= 4 && f <= 16) {
        const suyGiam = 1 - (f - 4) / 12;
        rot = Math.sin((f - 4) * 1.6) * 1.35 * suyGiam;
      }
      break;
    }

    case 'tinh':
    default:
      if (camera?.theoDoiNhanVat) {
        panX += (960 - tamX) * 0.2;
        panY += (540 - tamY) * 0.14;
      }
      break;
  }

  if (camera?.rungNhe) {
    panX += Math.sin(f * 2.15) * 4.2;
    panY += Math.cos(f * 2.75) * 3.2;
    rot += Math.sin(f * 1.8) * 0.35;
  }

  return { zoom, panX, panY, rot };
}

type MayQuayDongProps = {
  camera?: CauHinhCamera;
  /** Giu lai prop tuong thich nguoc; VideoDai.tsx dam nhiem lop chuyen canh toan man hinh */
  chuyenCanh?: LoaiChuyenCanh;
  nhanVat?: NhanVatTrongCanh[];
  thoiLuongCanh?: number;
  children: React.ReactNode;
};

export const MayQuayDong: React.FC<MayQuayDongProps> = ({
  camera,
  nhanVat,
  thoiLuongCanh,
  children,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const tong = Math.max(1, thoiLuongCanh ?? durationInFrames);

  const bienDoi = tinhBienDoiCamera(frame, tong, camera, nhanVat);

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        overflow: 'hidden',
      }}
    >
      <CameraParallaxContext.Provider value={bienDoi}>
        <div
          style={{
            width: '100%',
            height: '100%',
            transformOrigin: 'center center',
            transform: `translate(${bienDoi.panX.toFixed(2)}px, ${bienDoi.panY.toFixed(2)}px) scale(${bienDoi.zoom.toFixed(4)}) rotate(${bienDoi.rot.toFixed(3)}deg)`,
          }}
        >
          {children}
        </div>
      </CameraParallaxContext.Provider>
    </div>
  );
};
