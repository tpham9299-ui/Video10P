import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { DaoCu } from '../daocu/DaoCu';
import { CongThucMath } from '../daocu/CongThucMath';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngTanCong } from '../vfx/HieuUngTanCong';

type Props = {
  canh: Canh;
  tenChuong: string;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

export const CanhKeChuyen: React.FC<Props> = ({
  canh,
  tenChuong,
  bangMau,
  banDoNhanVat,
}) => {
  const frame = useCurrentFrame();
  const doMo = interpolate(frame, [0, 12], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <MayQuayDong camera={canh.camera} hieuUngTanCong={canh.hieuUngTanCong}>
      <div
        style={{
          position: 'absolute',
          top: 72,
          left: 88,
          right: 88,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          opacity: doMo,
        }}
      >
        <div>
          <div
            style={{
              color: bangMau.nhanManh,
              fontSize: 20,
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: 1.5,
            }}
          >
            {tenChuong}
          </div>
          {canh.tieuDeNho && (
            <div
              style={{
                color: bangMau.chuChinh,
                fontSize: 40,
                fontWeight: 800,
                marginTop: 6,
              }}
            >
              {canh.tieuDeNho}
            </div>
          )}
        </div>
        {canh.namMoc && (
          <div
            style={{
              padding: '8px 20px',
              borderRadius: 12,
              backgroundColor: bangMau.nenPhu,
              border: `2px solid ${bangMau.luoi}`,
              color: bangMau.chuChinh,
              fontSize: 24,
              fontWeight: 700,
            }}
          >
            {canh.namMoc}
          </div>
        )}
      </div>

      {canh.congThucLatex && canh.congThucLatex.length > 0 && (
        <div
          style={{
            position: 'absolute',
            top: 205,
            left: '50%',
            transform: 'translateX(-50%)',
            padding: '16px 32px',
            borderRadius: 16,
            backgroundColor: bangMau.nenPhu,
            border: `2px solid ${bangMau.nhanManh}`,
          }}
        >
          <CongThucMath latex={canh.congThucLatex[0].latex} fontSize={36} mau={bangMau.chuChinh} />
        </div>
      )}

      <svg
        width={1920}
        height={1080}
        viewBox="0 0 1920 1080"
        style={{ position: 'absolute', inset: 0 }}
      >
        <line
          x1={120}
          y1={830}
          x2={1800}
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
          return <NguoiQueDong key={`${nv.id}-${idx}`} thongTin={tt} trangThai={nv} tiLe={1.2} />;
        })}
        <HieuUngTanCong danhSach={canh.hieuUngTanCong} />
      </svg>
    </MayQuayDong>
  );
};
