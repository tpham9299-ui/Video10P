import React from 'react';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngTanCong } from '../vfx/HieuUngTanCong';

type Props = {
  canh: Canh;
  tieuDeVideo: string;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

/**
 * Canh ket thuc: chua san 2 khung End Screen chuan ty le 16:9 cho YouTube.
 */
export const CanhKet: React.FC<Props> = ({
  canh,
  tieuDeVideo,
  bangMau,
  banDoNhanVat,
}) => {
  return (
    <MayQuayDong camera={canh.camera} hieuUngTanCong={canh.hieuUngTanCong}>
      <div
        style={{
          position: 'absolute',
          top: 84,
          left: 96,
          right: 96,
          textAlign: 'center',
        }}
      >
        <div
          style={{
            color: bangMau.nhanManh,
            fontSize: 22,
            fontWeight: 700,
            letterSpacing: 2,
          }}
        >
          CẢM ƠN ĐÃ THEO DÕI
        </div>
        <div
          style={{
            marginTop: 10,
            color: bangMau.chuChinh,
            fontSize: 52,
            fontWeight: 800,
          }}
        >
          {canh.tieuDeNho ?? tieuDeVideo}
        </div>
      </div>

      {/* 2 khung End Screen ty le 16:9 (512 x 288) */}
      <div
        style={{
          position: 'absolute',
          top: 280,
          left: 160,
          right: 160,
          display: 'flex',
          justifyContent: 'space-between',
          gap: 64,
        }}
      >
        {[1, 2].map((so) => (
          <div
            key={so}
            style={{
              width: 512,
              height: 288,
              borderRadius: 18,
              border: `3px dashed ${bangMau.nhanManh}`,
              backgroundColor: 'rgba(15, 23, 42, 0.72)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              color: bangMau.chuPhu,
            }}
          >
            <div style={{ fontSize: 24, fontWeight: 800, color: bangMau.chuChinh }}>
              End Screen 16:9 #{so}
            </div>
            <div style={{ fontSize: 18, marginTop: 8 }}>Vùng gắn video đề xuất</div>
          </div>
        ))}
      </div>

      <svg
        width={1920}
        height={1080}
        viewBox="0 0 1920 1080"
        style={{ position: 'absolute', inset: 0 }}
      >
        <line
          x1={220}
          y1={840}
          x2={1700}
          y2={840}
          stroke={bangMau.luoi}
          strokeWidth={4}
          strokeLinecap="round"
        />
        {canh.nhanVat.map((nv, idx) => {
          const tt = banDoNhanVat[nv.id];
          if (!tt) return null;
          return <NguoiQueDong key={`${nv.id}-${idx}`} thongTin={tt} trangThai={nv} tiLe={1.1} />;
        })}
        <HieuUngTanCong danhSach={canh.hieuUngTanCong} />
      </svg>
    </MayQuayDong>
  );
};
