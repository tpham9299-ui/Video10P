import React, { createContext, useContext } from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import type {
  CauHinhCamera,
  CauHinhMayQuay,
  DaoCuTrongCanh,
  LoaiChuyenCanh,
  LuotThoai,
  NhanVatTrongCanh,
} from '../kieu_dai';
import {
  CAMERA_MAC_DINH,
  tinhBienDoiCamera,
  type KetQuaBienDoiCamera,
} from './dao_dien_camera';

export { tinhBienDoiCamera, type KetQuaBienDoiCamera };

/** Vung an toan HUD co dinh ngoai transform zoom/pan: tranh de thanh tien do chuong (tren) & phu de (duoi) */
export const HUD_TOP_SAFE = 76;
export const HUD_BOTTOM_SAFE = 150;

/** Context chia se bien doi camera cho he thong Parallax 3 lop trong BoiCanhHoatHinh */
export const CameraParallaxContext =
  createContext<KetQuaBienDoiCamera>(CAMERA_MAC_DINH);

export function useCameraParallax(): KetQuaBienDoiCamera {
  return useContext(CameraParallaxContext);
}

type MayQuayDongProps = {
  camera?: CauHinhCamera;
  /** Cau hinh dao dien may quay v2.0 (8 goc quay + tuDongFocusNguoiNoi) */
  mayQuay?: CauHinhMayQuay;
  /** Danh sach luot thoai de tu dong lia may sang nguoi dang noi */
  luotThoai?: readonly LuotThoai[];
  /** Danh sach dao cu de ho tro gocQuay="zoom_dao_cu" */
  daoCu?: readonly DaoCuTrongCanh[];
  /** Giu lai prop tuong thich nguoc; VideoDai.tsx dam nhiem lop chuyen canh toan man hinh */
  chuyenCanh?: LoaiChuyenCanh;
  nhanVat?: NhanVatTrongCanh[];
  thoiLuongCanh?: number;
  /** Lop HUD (tieu de canh, the chuong, bong bong binh luan, cau hoi...) tach biet 100% ngoai transform zoom/pan */
  hud?: React.ReactNode;
  children: React.ReactNode;
};

export const MayQuayDong: React.FC<MayQuayDongProps> = ({
  camera,
  mayQuay,
  luotThoai,
  daoCu,
  nhanVat,
  thoiLuongCanh,
  hud,
  children,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const tong = Math.max(1, thoiLuongCanh ?? durationInFrames);

  const bienDoi = tinhBienDoiCamera(
    frame,
    tong,
    camera,
    nhanVat,
    mayQuay,
    luotThoai,
    daoCu,
  );

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
            transform: `translate3d(${bienDoi.panX.toFixed(2)}px, ${bienDoi.panY.toFixed(2)}px, 0) scale(${bienDoi.zoom.toFixed(4)}) rotate(${bienDoi.rot.toFixed(3)}deg)`,
          }}
        >
          {children}
        </div>
      </CameraParallaxContext.Provider>

      {/* Lop HUD co dinh ngoai transform zoom/pan, dam bao vung an toan tren >= 76px va duoi >= 150px */}
      {hud && (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            paddingTop: HUD_TOP_SAFE,
            paddingBottom: HUD_BOTTOM_SAFE,
            boxSizing: 'border-box',
            pointerEvents: 'none',
            zIndex: 20,
          }}
        >
          {hud}
        </div>
      )}
    </div>
  );
};
