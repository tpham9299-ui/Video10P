import React from 'react';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { BoiCanhHoatHinh } from '../boicanh/BoiCanhHoatHinh';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { DaoCu } from '../daocu/DaoCu';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngHoatHinh } from '../vfx/HieuUngHoatHinh';
import { KhungLoiBinhHaiHuoc } from './KhungLoiBinhHaiHuoc';

type Props = {
  canh: Canh;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

/**
 * Canh hai huoc: toi uu nhip zoom_hai_huoc, mat do can loi, giot mo hoi, co lan & nhan chu comic.
 */
export const CanhHaiHuoc: React.FC<Props> = ({
  canh,
  bangMau,
  banDoNhanVat,
}) => {
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);

  return (
    <div style={{ position: 'absolute', inset: 0 }}>
      <MayQuayDong
        camera={canh.camera}
        chuyenCanh={canh.chuyenCanh}
        nhanVat={canh.nhanVat}
        thoiLuongCanh={thoiLuong}
      >
        <BoiCanhHoatHinh loai={canh.boiCanh} thoiTiet={canh.thoiTiet} />

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
                tiLe={1.45}
                thoiLuongCanh={thoiLuong}
              />
            );
          })}
          <HieuUngHoatHinh danhSach={canh.hieuUngHoatHinh} />
        </svg>
      </MayQuayDong>

      {/* The nhan nhip hai goc trai tren (ghim co dinh ngoai camera zoom) */}
      {canh.tieuDeNho && (
        <div
          style={{
            position: 'absolute',
            top: 62,
            left: 52,
            transform: 'rotate(-2deg)',
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              padding: '9px 22px',
              borderRadius: 14,
              backgroundColor: bangMau.canhBao || '#FB923C',
              border: '3.5px solid #1E293B',
              boxShadow: '6px 6px 0px #1E293B',
              color: '#1E293B',
              fontSize: 26,
              fontWeight: 900,
              letterSpacing: 0.4,
            }}
          >
            {canh.tieuDeNho}
          </div>
        </div>
      )}

      <KhungLoiBinhHaiHuoc loiBinh={canh.loiBinhHaiHuoc} />
    </div>
  );
};
