import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { DaoCu } from '../daocu/DaoCu';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngTanCong } from '../vfx/HieuUngTanCong';

type Props = {
  canh: Canh;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

const MOC_THOI_GIAN = [
  { nam: '~530 TCN', moTa: 'Trường phái Pythagoras' },
  { nam: '~500 TCN', moTa: 'Phát hiện số vô tỉ √2' },
  { nam: '~300 TCN', moTa: 'Euclid chuẩn hóa chứng minh' },
];

export const CanhDongThoiGian: React.FC<Props> = ({
  canh,
  bangMau,
  banDoNhanVat,
}) => {
  const frame = useCurrentFrame();
  const chieuDaiTruc = interpolate(frame, [0, 30], [0, 1440], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <MayQuayDong camera={canh.camera} hieuUngTanCong={canh.hieuUngTanCong}>
      <div
        style={{
          position: 'absolute',
          top: 76,
          left: 96,
          right: 96,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'baseline',
        }}
      >
        <div style={{ color: bangMau.chuChinh, fontSize: 44, fontWeight: 800 }}>
          {canh.tieuDeNho ?? 'Dòng thời gian lịch sử'}
        </div>
        {canh.namMoc && (
          <div style={{ color: bangMau.nhanManh, fontSize: 28, fontWeight: 800 }}>
            {canh.namMoc}
          </div>
        )}
      </div>

      <svg
        width={1920}
        height={1080}
        viewBox="0 0 1920 1080"
        style={{ position: 'absolute', inset: 0 }}
      >
        {/* Truc dong thoi gian */}
        <line
          x1={240}
          y1={360}
          x2={240 + chieuDaiTruc}
          y2={360}
          stroke={bangMau.nhanManh}
          strokeWidth={6}
          strokeLinecap="round"
        />

        {MOC_THOI_GIAN.map((moc, idx) => {
          const x = 360 + idx * 600;
          const noiBat = idx === 1;
          return (
            <g key={moc.nam} transform={`translate(${x}, 360)`}>
              <circle
                cx={0}
                cy={0}
                r={noiBat ? 22 : 15}
                fill={noiBat ? bangMau.canhBao : bangMau.nenPhu}
                stroke={noiBat ? '#FEF08A' : bangMau.nhanManh}
                strokeWidth={5}
              />
              <text
                x={0}
                y={-42}
                textAnchor="middle"
                fill={noiBat ? '#FEF08A' : bangMau.chuChinh}
                fontSize={28}
                fontWeight={800}
                fontFamily="Segoe UI, Arial, sans-serif"
              >
                {moc.nam}
              </text>
              <text
                x={0}
                y={54}
                textAnchor="middle"
                fill={bangMau.chuPhu}
                fontSize={22}
                fontWeight={600}
                fontFamily="Segoe UI, Arial, sans-serif"
              >
                {moc.moTa}
              </text>
            </g>
          );
        })}

        <line
          x1={140}
          y1={830}
          x2={1780}
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
