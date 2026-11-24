import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { DaoCu } from '../daocu/DaoCu';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngTanCong } from '../vfx/HieuUngTanCong';

type Props = {
  canh: Canh;
  tieuDeVideo: string;
  chuDeVideo: string;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

export const CanhMoDau: React.FC<Props> = ({
  canh,
  tieuDeVideo,
  chuDeVideo,
  bangMau,
  banDoNhanVat,
}) => {
  const frame = useCurrentFrame();
  const doMoTieuDe = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const dichTieuDeY = interpolate(frame, [0, 18], [28, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <MayQuayDong camera={canh.camera} hieuUngTanCong={canh.hieuUngTanCong}>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          paddingTop: 105,
          opacity: doMoTieuDe,
          transform: `translateY(${dichTieuDeY}px)`,
        }}
      >
        {canh.namMoc && (
          <div
            style={{
              padding: '8px 24px',
              borderRadius: 999,
              border: `2px solid ${bangMau.nhanManh}`,
              backgroundColor: bangMau.nenPhu,
              color: bangMau.nhanManh,
              fontSize: 22,
              fontWeight: 700,
              letterSpacing: 2,
              marginBottom: 18,
            }}
          >
            {canh.namMoc}
          </div>
        )}
        <h1
          style={{
            margin: 0,
            color: bangMau.chuChinh,
            fontSize: 68,
            fontWeight: 800,
            textAlign: 'center',
            maxWidth: 1480,
            lineHeight: 1.15,
          }}
        >
          {canh.tieuDeNho ?? tieuDeVideo}
        </h1>
        <p
          style={{
            margin: '16px 0 0',
            color: bangMau.chuPhu,
            fontSize: 28,
            fontWeight: 500,
            textAlign: 'center',
          }}
        >
          {chuDeVideo}
        </p>
      </div>

      <svg
        width={1920}
        height={1080}
        viewBox="0 0 1920 1080"
        style={{ position: 'absolute', inset: 0 }}
      >
        <line
          x1={160}
          y1={830}
          x2={1760}
          y2={830}
          stroke={bangMau.luoi}
          strokeWidth={4}
          strokeLinecap="round"
        />
        {canh.daoCu?.map((dc, idx) => (
          <DaoCu key={`${dc.loai}-${idx}`} daoCu={dc} />
        ))}
        {canh.nhanVat.map((nv, idx) => {
          const tt = banDoNhanVat[nv.id];
          if (!tt) return null;
          return <NguoiQueDong key={`${nv.id}-${idx}`} thongTin={tt} trangThai={nv} tiLe={1.15} />;
        })}
        <HieuUngTanCong danhSach={canh.hieuUngTanCong} />
      </svg>
    </MayQuayDong>
  );
};
