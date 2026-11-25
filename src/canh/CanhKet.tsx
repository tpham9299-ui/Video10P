import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { BoiCanhHoatHinh } from '../boicanh/BoiCanhHoatHinh';
import { locDaoCuKhongTrungLap } from '../boicanh/moi_truong_logic';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { giaiTrangThaiNhanVatTrongCanh } from '../nhanvat/dien_xuat';
import { DaoCu } from '../daocu/DaoCu';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngHoatHinh } from '../vfx/HieuUngHoatHinh';
import { KhungLoiBinhHaiHuoc } from './KhungLoiBinhHaiHuoc';

type Props = {
  canh: Canh;
  tieuDeVideo: string;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
  /** Chi bat banner "Cảm ơn bạn đã theo dõi!" o canh cuoi cung cua hoi cuoi cung toan tap */
  hienBannerKetThuc?: boolean;
};

export const CanhKet: React.FC<Props> = ({
  canh,
  tieuDeVideo,
  bangMau,
  banDoNhanVat,
  hienBannerKetThuc = false,
}) => {
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const danhSachNhanVat = giaiTrangThaiNhanVatTrongCanh(canh, frame, thoiLuong);
  const doMo = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const daoCuHienThi = locDaoCuKhongTrungLap(canh.daoCu, canh.nhanVat);

  const lopHud = (
    <>
      {(hienBannerKetThuc || canh.tieuDeNho) && (
        <div
          style={{
            position: 'absolute',
            top: 84,
            left: 60,
            right: 60,
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
              backgroundColor: 'rgba(15, 23, 42, 0.88)',
              border: `3.5px solid ${bangMau.nhanManh}`,
              textAlign: 'center',
              maxWidth: 1320,
              boxShadow: '8px 8px 0px rgba(15, 23, 42, 0.45)',
            }}
          >
            {hienBannerKetThuc && (
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
            )}
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
      )}

      <KhungLoiBinhHaiHuoc loiBinh={canh.loiBinhHaiHuoc} />
    </>
  );

  return (
    <div style={{ position: 'absolute', inset: 0 }}>
      <MayQuayDong
        camera={canh.camera}
        mayQuay={canh.mayQuay}
        luotThoai={canh.luotThoai}
        daoCu={daoCuHienThi}
        chuyenCanh={canh.chuyenCanh}
        nhanVat={canh.nhanVat}
        thoiLuongCanh={thoiLuong}
        hud={lopHud}
      >
        <BoiCanhHoatHinh
          loai={canh.boiCanh}
          thoiTiet={canh.thoiTiet}
          vatTheXungQuanh={canh.vatTheXungQuanh}
          bienSoXe={canh.bienSoXe}
          nhanVat={canh.nhanVat}
          daoCu={daoCuHienThi}
        />

        <svg
          width={1920}
          height={1080}
          viewBox="0 0 1920 1080"
          style={{ position: 'absolute', inset: 0 }}
        >
          {daoCuHienThi.map((dc, idx) => (
            <DaoCu key={`${dc.loai}-${idx}`} daoCu={dc} />
          ))}
          {danhSachNhanVat.map((nv, idx) => {
            const tt = banDoNhanVat[nv.id];
            if (!tt) return null;
            return (
              <NguoiQueDong
                key={`${nv.id}-${idx}`}
                thongTin={tt}
                trangThai={nv}
                tiLe={1.2}
                thoiLuongCanh={thoiLuong}
                bienDoAmThanh={canh.bienDoAmThanh}
              />
            );
          })}
          <HieuUngHoatHinh danhSach={canh.hieuUngHoatHinh} />
        </svg>
      </MayQuayDong>
    </div>
  );
};
