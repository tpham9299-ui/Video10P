import React from 'react';
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

export const CanhHanhDong: React.FC<Props> = ({
  canh,
  bangMau,
  banDoNhanVat,
}) => {
  return (
    <MayQuayDong camera={canh.camera} hieuUngTanCong={canh.hieuUngTanCong}>
      {/* Dai tieu de canh hanh dong */}
      <div
        style={{
          position: 'absolute',
          top: 72,
          left: 88,
          display: 'flex',
          alignItems: 'center',
          gap: 16,
        }}
      >
        <div
          style={{
            padding: '6px 16px',
            borderRadius: 8,
            backgroundColor: bangMau.canhBao,
            color: '#0F172A',
            fontSize: 18,
            fontWeight: 900,
            letterSpacing: 1.2,
          }}
        >
          ĐỐI ĐẦU
        </div>
        {canh.tieuDeNho && (
          <div
            style={{
              color: bangMau.chuChinh,
              fontSize: 36,
              fontWeight: 800,
            }}
          >
            {canh.tieuDeNho}
          </div>
        )}
      </div>

      <svg
        width={1920}
        height={1080}
        viewBox="0 0 1920 1080"
        style={{ position: 'absolute', inset: 0 }}
      >
        {/* Nen san dau co duong chan troi sac net */}
        <rect x={0} y={830} width={1920} height={250} fill="#020617" fillOpacity={0.45} />
        <line
          x1={80}
          y1={830}
          x2={1840}
          y2={830}
          stroke={bangMau.canhBao}
          strokeWidth={5}
          strokeLinecap="round"
        />

        {canh.daoCu?.map((dc, idx) => (
          <DaoCu key={`${dc.loai}-${idx}`} daoCu={dc} />
        ))}
        {canh.nhanVat.map((nv, idx) => {
          const tt = banDoNhanVat[nv.id];
          if (!tt) return null;
          return <NguoiQueDong key={`${nv.id}-${idx}`} thongTin={tt} trangThai={nv} tiLe={1.3} />;
        })}
        <HieuUngTanCong danhSach={canh.hieuUngTanCong} />
      </svg>
    </MayQuayDong>
  );
};
