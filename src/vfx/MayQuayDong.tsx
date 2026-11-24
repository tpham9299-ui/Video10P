import React from 'react';
import { interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import type {
  CauHinhCamera,
  LoaiChuyenCanh,
  NhanVatTrongCanh,
} from '../kieu_dai';

export type KetQuaBienDoiCamera = {
  zoom: number;
  panX: number;
  panY: number;
  rot: number;
};

/**
 * Tinh bien doi camera tat dinh 100% theo frame:
 * - tinh: giu khung on dinh
 * - pan_nhe: luot ngang ngam phong canh dien anh
 * - zoom_cham: hieu ung Ken Burns phong cham em ai
 * - zoom_hai_huoc: phong nhanh cuc gat vao nhan vat de tao nhip gay cuoi
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

  // Tim tam muc tieu neu theoDoiNhanVat hoac zoom_hai_huoc
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
      const tienDo = Math.max(0, Math.min(1, f / tong));
      zoom = Math.max(1.06, camera?.zoom ?? 1.06);
      panX += interpolate(tienDo, [0, 1], [-32, 32], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      });
      break;
    }

    case 'zoom_cham': {
      const tienDo = Math.max(0, Math.min(1, f / tong));
      const zoomDich = camera?.zoom ?? 1.09;
      zoom = interpolate(tienDo, [0, 1], [1, zoomDich], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      });
      panX += (960 - tamX) * (zoom - 1) * 0.45;
      panY += (540 - tamY) * (zoom - 1) * 0.45;
      break;
    }

    case 'zoom_hai_huoc': {
      // Phong nhanh cuc gat trong 10 frame dau kem nay nhe o frame 9..13
      const zoomMucTieu = camera?.zoom ?? 1.48;
      if (f <= 10) {
        const t = f / 10;
        const easeOut = 1 - Math.pow(1 - t, 3);
        zoom = 1 + (zoomMucTieu + 0.06 - 1) * easeOut;
      } else if (f <= 15) {
        const t = (f - 10) / 5;
        zoom = zoomMucTieu + 0.06 * (1 - t);
      } else {
        zoom = zoomMucTieu;
      }
      panX += (960 - tamX) * (zoom - 1) * 0.85;
      panY += (540 - tamY) * (zoom - 1) * 0.85;
      if (f >= 6 && f <= 14) {
        rot = Math.sin(f * 1.9) * 1.1;
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

/** Lop chuyen canh vao (mo_dan, quet_ngang, vong_tron_hoat_hinh - khong blur) */
const LopChuyenCanh: React.FC<{ loai?: LoaiChuyenCanh; frame: number }> = ({
  loai,
  frame,
}) => {
  if (!loai) {
    return null;
  }

  if (loai === 'mo_dan') {
    if (frame > 10) return null;
    const op = interpolate(frame, [0, 10], [1, 0], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    return (
      <div
        style={{
          position: 'absolute',
          inset: 0,
          backgroundColor: '#0F172A',
          opacity: op,
          pointerEvents: 'none',
        }}
      />
    );
  }

  if (loai === 'quet_ngang') {
    if (frame > 14) return null;
    const x = interpolate(frame, [0, 14], [0, 1980], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    return (
      <div
        style={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: x,
          width: 1960,
          backgroundColor: '#1E293B',
          borderLeft: '14px solid #FACC15',
          pointerEvents: 'none',
        }}
      />
    );
  }

  // vong_tron_hoat_hinh (Iris Wipe kieu phim hoat hinh kinh dien)
  if (frame > 18) return null;
  const r = interpolate(frame, [0, 18], [18, 1280], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const cx = 960;
  const cy = 540;
  const d = `M 0 0 H 1920 V 1080 H 0 Z M ${cx - r} ${cy} a ${r} ${r} 0 1 0 ${r * 2} 0 a ${r} ${r} 0 1 0 ${-r * 2} 0 Z`;

  return (
    <svg
      width={1920}
      height={1080}
      viewBox="0 0 1920 1080"
      style={{ position: 'absolute', inset: 0, pointerEvents: 'none' }}
    >
      <path d={d} fill="#0F172A" fillRule="evenodd" />
      <circle cx={cx} cy={cy} r={r} fill="none" stroke="#FACC15" strokeWidth={6} />
    </svg>
  );
};

type MayQuayDongProps = {
  camera?: CauHinhCamera;
  chuyenCanh?: LoaiChuyenCanh;
  nhanVat?: NhanVatTrongCanh[];
  thoiLuongCanh?: number;
  children: React.ReactNode;
};

export const MayQuayDong: React.FC<MayQuayDongProps> = ({
  camera,
  chuyenCanh,
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

      <LopChuyenCanh loai={chuyenCanh} frame={frame} />
    </div>
  );
};
