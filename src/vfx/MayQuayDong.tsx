import React, { createContext, useContext } from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import type {
  AnhSangMoiTruong,
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

/** Context chia se bien doi camera cho he thong Parallax 3 lop trong BoiCanhHoatHinh & NenMinhHoaAI */
export const CameraParallaxContext =
  createContext<KetQuaBienDoiCamera>(CAMERA_MAC_DINH);

export function useCameraParallax(): KetQuaBienDoiCamera {
  return useContext(CameraParallaxContext);
}

/** Context chia se anhSangMoiTruong cua canh cho nhan vat tu dong dong bo anh sang (v3.0) */
export const AnhSangCanhContext = createContext<AnhSangMoiTruong | undefined>(
  undefined,
);

export function useAnhSangMoiTruong(): AnhSangMoiTruong | undefined {
  return useContext(AnhSangCanhContext);
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
  /** Anh sang moi truong cua canh de truyen xuong nhan vat dong bo tong mau (v3.0) */
  anhSangMoiTruong?: AnhSangMoiTruong;
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
  anhSangMoiTruong,
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
      <AnhSangCanhContext.Provider value={anhSangMoiTruong}>
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
      </AnhSangCanhContext.Provider>

      {/* Vien tia toc do SVG phang cho goc quay can_mat_kich_tinh (tat dinh 100%, khong blur) */}
      {bienDoi.hienTiaTocDo && (
        <svg
          width={1920}
          height={1080}
          viewBox="0 0 1920 1080"
          style={{
            position: 'absolute',
            inset: 0,
            pointerEvents: 'none',
            zIndex: 15,
          }}
        >
          {Array.from({ length: 36 }).map((_, i) => {
            const goc = (i / 36) * Math.PI * 2 + (frame % 3) * 0.015;
            const rNgoai = 1220;
            const rTrong = 660 + ((i * 37 + frame * 11) % 130);
            const lech = 0.024 + (i % 3) * 0.008;
            const x1 = 960 + Math.cos(goc - lech) * rNgoai;
            const y1 = 540 + Math.sin(goc - lech) * rNgoai;
            const x2 = 960 + Math.cos(goc + lech) * rNgoai;
            const y2 = 540 + Math.sin(goc + lech) * rNgoai;
            const xt = 960 + Math.cos(goc) * rTrong;
            const yt = 540 + Math.sin(goc) * rTrong;
            return (
              <polygon
                key={`speed-border-${i}`}
                points={`${x1.toFixed(1)},${y1.toFixed(1)} ${x2.toFixed(1)},${y2.toFixed(1)} ${xt.toFixed(1)},${yt.toFixed(1)}`}
                fill={i % 3 === 0 ? '#FEF08A' : '#1A1A1A'}
                fillOpacity={i % 3 === 0 ? 0.32 : 0.42}
              />
            );
          })}
        </svg>
      )}

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
