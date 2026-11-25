import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import { tinhTrangThaiTheTenHoi } from './phu_de_logic';
import { MAU_MUC_TRUYEN_TRANH } from '../nhanvat/hoa_trang_va_anh_sang';

type TheTenHoiProps = {
  tenChuong: string;
  phuDeHoi?: string;
  chiSoHoi: number;
};

/**
 * The ten Hoi trang nha (phong cach giay da / vien muc co dien #1A1A1A):
 * chi hien trong 2.8 giay dau moi Hoi roi truot/mo bien mat hoan toan
 * de nhuong 100% khung hinh cho hoat hinh (Clean Cinema UI v3.0, khong blur).
 */
export const TheTenHoi: React.FC<TheTenHoiProps> = ({
  tenChuong,
  phuDeHoi,
  chiSoHoi,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const trangThai = tinhTrangThaiTheTenHoi(frame, fps);

  if (!trangThai.dangHien || trangThai.opacity <= 0.01) {
    return null;
  }

  return (
    <div
      style={{
        position: 'absolute',
        top: 36,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        pointerEvents: 'none',
        zIndex: 38,
        opacity: trangThai.opacity,
        transform: `translate3d(0, ${trangThai.dichY}px, 0)`,
      }}
    >
      <div
        style={{
          position: 'relative',
          padding: '12px 34px 13px',
          borderRadius: 12,
          backgroundColor: '#FAF3E0',
          border: `3px solid ${MAU_MUC_TRUYEN_TRANH}`,
          boxShadow: '5px 5px 0px rgba(26, 26, 26, 0.42)',
          textAlign: 'center',
          maxWidth: 1120,
          fontFamily: 'Georgia, "Times New Roman", serif',
        }}
      >
        {/* Vien trang tri trong phong cach giay da co dien */}
        <div
          style={{
            position: 'absolute',
            inset: 5,
            borderRadius: 7,
            border: '1.5px solid #B45309',
            pointerEvents: 'none',
          }}
        />
        <div
          style={{
            display: 'inline-block',
            fontSize: 13,
            fontWeight: 800,
            letterSpacing: 2.2,
            textTransform: 'uppercase',
            color: '#92400E',
            fontFamily: 'Segoe UI, Arial, sans-serif',
            marginBottom: 3,
          }}
        >
          Hồi {chiSoHoi + 1}
        </div>
        <div
          style={{
            fontSize: 28,
            fontWeight: 900,
            color: '#1A1A1A',
            lineHeight: 1.2,
            fontFamily: 'Segoe UI, Arial, sans-serif',
          }}
        >
          {tenChuong}
        </div>
        {phuDeHoi && (
          <div
            style={{
              marginTop: 4,
              fontSize: 16,
              fontWeight: 600,
              color: '#57534E',
              fontFamily: 'Segoe UI, Arial, sans-serif',
            }}
          >
            {phuDeHoi}
          </div>
        )}
      </div>
    </div>
  );
};
