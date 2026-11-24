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

export const CanhDoiThoai: React.FC<Props> = ({
  canh,
  bangMau,
  banDoNhanVat,
}) => {
  return (
    <MayQuayDong camera={canh.camera} hieuUngTanCong={canh.hieuUngTanCong}>
      <div
        style={{
          position: 'absolute',
          top: 76,
          left: 0,
          right: 0,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <div
          style={{
            padding: '6px 18px',
            borderRadius: 999,
            backgroundColor: bangMau.nenPhu,
            border: `2px solid ${bangMau.nhanManh}`,
            color: bangMau.nhanManh,
            fontSize: 18,
            fontWeight: 700,
            letterSpacing: 1.4,
          }}
        >
          TRANH LUẬN TOÁN HỌC
        </div>
        {canh.tieuDeNho && (
          <div
            style={{
              marginTop: 12,
              color: bangMau.chuChinh,
              fontSize: 42,
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
        {/* Vach phan cach trung tam */}
        <line
          x1={960}
          y1={230}
          x2={960}
          y2={810}
          stroke={bangMau.luoi}
          strokeWidth={2}
          strokeDasharray="10 10"
        />
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
          return <NguoiQueDong key={`${nv.id}-${idx}`} thongTin={tt} trangThai={nv} tiLe={1.25} />;
        })}
        <HieuUngTanCong danhSach={canh.hieuUngTanCong} />
      </svg>
    </MayQuayDong>
  );
};
