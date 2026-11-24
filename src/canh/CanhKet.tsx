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
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

export const CanhKet: React.FC<Props> = ({
  canh,
  tieuDeVideo,
  bangMau,
  banDoNhanVat,
}) => {
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const doMo = interpolate(frame, [0, 18], [0, 1], {
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
            top: 96,
            left: 0,
            right: 0,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            opacity: doMo,
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              padding: '22px 46px',
              borderRadius: 24,
              backgroundColor: 'rgba(15, 23, 42, 0.86)',
              border: `3.5px solid ${bangMau.nhanManh}`,
              textAlign: 'center',
              maxWidth: 1320,
              boxShadow: '8px 8px 0px rgba(15, 23, 42, 0.45)',
            }}
          >
            <div
              style={{
                color: bangMau.nhanManh,
                fontSize: 21,
                fontWeight: 900,
                letterSpacing: 1.8,
                marginBottom: 10,
                textTransform: 'uppercase',
              }}
            >
              Cảm ơn bạn đã theo dõi!
            </div>
            <div
              style={{
                color: '#FFFFFF',
                fontSize: 50,
                fontWeight: 900,
                lineHeight: 1.2,
              }}
            >
              {canh.tieuDeNho ?? tieuDeVideo}
            </div>
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
