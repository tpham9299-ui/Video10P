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
  banDoNhanVat,
}) => {
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const danhSachNhanVat = giaiTrangThaiNhanVatTrongCanh(canh, frame, thoiLuong);
  // The mo man giay da hien 2.8s dau (84 frame) roi truot/mo bien mat sach se (Clean Cinema UI v3.0)
  const doMoVao = interpolate(frame, [2, 16], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const doMoRa = interpolate(frame, [68, 84], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const doMoTieuDe = doMoVao * doMoRa;
  const dichTieuDeY =
    frame < 68
      ? interpolate(frame, [2, 16], [-24, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        })
      : interpolate(frame, [68, 84], [0, -28], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
  const daoCuHienThi = locDaoCuKhongTrungLap(canh.daoCu, canh.nhanVat);

  const lopHud =
    doMoTieuDe > 0.01 ? (
      <div
        style={{
          position: 'absolute',
          top: 48,
          left: 60,
          right: 60,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          opacity: doMoTieuDe,
          transform: `translateY(${dichTieuDeY.toFixed(1)}px)`,
          pointerEvents: 'none',
        }}
      >
        {canh.namMoc && (
          <div
            style={{
              padding: '5px 20px',
              borderRadius: 999,
              border: '2.5px solid #1A1A1A',
              backgroundColor: '#FDE68A',
              color: '#1A1A1A',
              fontSize: 18,
              fontWeight: 900,
              letterSpacing: 1.4,
              marginBottom: 10,
              boxShadow: '3px 3px 0px #1A1A1A',
            }}
          >
            {canh.namMoc}
          </div>
        )}

        <div
          style={{
            position: 'relative',
            padding: '16px 40px',
            borderRadius: 16,
            backgroundColor: '#FAF3E0',
            border: '3.5px solid #1A1A1A',
            boxShadow: '7px 7px 0px rgba(26, 26, 26, 0.42)',
            maxWidth: 1320,
            textAlign: 'center',
          }}
        >
          <div
            style={{
              position: 'absolute',
              inset: 6,
              borderRadius: 10,
              border: '1.5px solid #B45309',
              pointerEvents: 'none',
            }}
          />
          <h1
            style={{
              margin: 0,
              color: '#1A1A1A',
              fontSize: 48,
              fontWeight: 900,
              lineHeight: 1.15,
            }}
          >
            {canh.tieuDeNho ?? tieuDeVideo}
          </h1>
          <p
            style={{
              margin: '8px 0 0',
              color: '#78350F',
              fontSize: 22,
              fontWeight: 700,
            }}
          >
            {canh.phuDeHoi ?? chuDeVideo}
          </p>
        </div>
      </div>
    ) : undefined;

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
        anhSangMoiTruong={canh.anhSangMoiTruong}
        hud={lopHud}
      >
        <BoiCanhHoatHinh
          loai={canh.boiCanh}
          thoiTiet={canh.thoiTiet}
          vatTheXungQuanh={canh.vatTheXungQuanh}
          bienSoXe={canh.bienSoXe}
          nhanVat={canh.nhanVat}
          daoCu={daoCuHienThi}
          anhBoiCanh={canh.anhBoiCanh}
          anhSangMoiTruong={canh.anhSangMoiTruong}
          laKhungTranhDacTa={canh.laKhungTranhDacTa}
          thoiLuongCanh={thoiLuong}
        />

        {!canh.laKhungTranhDacTa && (
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
                  anhSangMoiTruong={canh.anhSangMoiTruong}
                />
              );
            })}
            <HieuUngHoatHinh
              danhSach={canh.hieuUngHoatHinh}
              nhanVat={danhSachNhanVat}
              tiLeNhanVat={1.2}
            />
          </svg>
        )}
      </MayQuayDong>
    </div>
  );
};
