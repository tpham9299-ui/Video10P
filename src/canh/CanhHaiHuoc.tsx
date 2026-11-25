import React from 'react';
import { useCurrentFrame } from 'remotion';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { BoiCanhHoatHinh } from '../boicanh/BoiCanhHoatHinh';
import { locDaoCuKhongTrungLap } from '../boicanh/moi_truong_logic';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { giaiTrangThaiNhanVatTrongCanh } from '../nhanvat/dien_xuat';
import { DaoCu } from '../daocu/DaoCu';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngHoatHinh } from '../vfx/HieuUngHoatHinh';
import { KhungLoiBinhHaiHuoc } from './KhungLoiBinhHaiHuoc';
import { LopCauHoiTuongTac } from './LopCauHoiTuongTac';

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
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const danhSachNhanVat = giaiTrangThaiNhanVatTrongCanh(canh, frame, thoiLuong);
  const daoCuHienThi = locDaoCuKhongTrungLap(canh.daoCu, canh.nhanVat);

  const lopHud = (
    <>
      {/* The nhan nhip hai goc trai tren (ghim co dinh ngoai camera zoom, >= 76px) */}
      {canh.tieuDeNho && (
        <div
          style={{
            position: 'absolute',
            top: 76,
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

      {canh.cauHoiTuongTac && (
        <LopCauHoiTuongTac
          cauHoi={canh.cauHoiTuongTac}
          bangMau={bangMau}
          thoiLuongCanh={thoiLuong}
        />
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
                tiLe={1.45}
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
