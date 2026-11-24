import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { BoiCanhHoatHinh } from '../boicanh/BoiCanhHoatHinh';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { DaoCu } from '../daocu/DaoCu';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngHoatHinh } from '../vfx/HieuUngHoatHinh';
import { KhungLoiBinhHaiHuoc } from './KhungLoiBinhHaiHuoc';

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
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const doMoTieuDe = interpolate(frame, [4, 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const dichTieuDeY = interpolate(frame, [4, 20], [26, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ position: 'absolute', inset: 0 }}>
      <MayQuayDong
        camera={canh.camera}
        chuyenCanh={canh.chuyenCanh}
        nhanVat={canh.nhanVat}
        thoiLuongCanh={thoiLuong}
      >
        <BoiCanhHoatHinh loai={canh.boiCanh} thoiTiet={canh.thoiTiet} />

        <div
          style={{
            position: 'absolute',
            top: 86,
            left: 0,
            right: 0,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            opacity: doMoTieuDe,
            transform: `translateY(${dichTieuDeY}px)`,
            pointerEvents: 'none',
          }}
        >
          {canh.namMoc && (
            <div
              style={{
                padding: '7px 24px',
                borderRadius: 999,
                border: '3px solid #1E293B',
                backgroundColor: '#FEF08A',
                color: '#1E293B',
                fontSize: 21,
                fontWeight: 900,
                letterSpacing: 1.5,
                marginBottom: 16,
                boxShadow: '4px 4px 0px #1E293B',
              }}
            >
              {canh.namMoc}
            </div>
          )}

          <div
            style={{
              padding: '20px 44px',
              borderRadius: 24,
              backgroundColor: 'rgba(15, 23, 42, 0.86)',
              border: `3.5px solid ${bangMau.nhanManh}`,
              boxShadow: '8px 8px 0px rgba(15, 23, 42, 0.4)',
              maxWidth: 1380,
              textAlign: 'center',
            }}
          >
            <h1
              style={{
                margin: 0,
                color: '#FFFFFF',
                fontSize: 60,
                fontWeight: 900,
                lineHeight: 1.15,
              }}
            >
              {canh.tieuDeNho ?? tieuDeVideo}
            </h1>
            <p
              style={{
                margin: '12px 0 0',
                color: '#FEF08A',
                fontSize: 26,
                fontWeight: 700,
              }}
            >
              {chuDeVideo}
            </p>
          </div>
        </div>

        <svg
          width={1920}
          height={1080}
          viewBox="0 0 1920 1080"
          style={{ position: 'absolute', inset: 0 }}
        >
          {canh.daoCu?.map((dc, idx) => (
            <DaoCu key={`${dc.loai}-${idx}`} daoCu={dc} />
          ))}
          {canh.nhanVat.map((nv, idx) => {
            const tt = banDoNhanVat[nv.id];
            if (!tt) return null;
            return (
              <NguoiQueDong
                key={`${nv.id}-${idx}`}
                thongTin={tt}
                trangThai={nv}
                tiLe={1.2}
                thoiLuongCanh={thoiLuong}
              />
            );
          })}
          <HieuUngHoatHinh danhSach={canh.hieuUngHoatHinh} />
        </svg>
      </MayQuayDong>

      <KhungLoiBinhHaiHuoc loiBinh={canh.loiBinhHaiHuoc} />
    </div>
  );
};
