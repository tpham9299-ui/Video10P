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
  tenChuong: string;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

export const CanhKeChuyen: React.FC<Props> = ({
  canh,
  tenChuong,
  bangMau,
  banDoNhanVat,
}) => {
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const danhSachNhanVat = giaiTrangThaiNhanVatTrongCanh(canh, frame, thoiLuong);
  const daoCuHienThi = locDaoCuKhongTrungLap(canh.daoCu, canh.nhanVat);

  const lopHud = (
    <>
      {/* The chuong & tieu de nho o goc trai tren (cach mep tren >= 76px, tach khoi zoom camera) */}
      <div
        style={{
          position: 'absolute',
          top: 76,
          left: 52,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-start',
          gap: 8,
          pointerEvents: 'none',
        }}
      >
        <div
          style={{
            padding: '5px 16px',
            borderRadius: 999,
            backgroundColor: '#FEF08A',
            border: '2.5px solid #1E293B',
            color: '#1E293B',
            fontSize: 16,
            fontWeight: 900,
            letterSpacing: 0.6,
            boxShadow: '3px 3px 0px #1E293B',
          }}
        >
          {tenChuong}
          {canh.namMoc ? ` • ${canh.namMoc}` : ''}
        </div>
        {canh.tieuDeNho && (
          <div
            style={{
              padding: '8px 20px',
              borderRadius: 14,
              backgroundColor: 'rgba(15, 23, 42, 0.86)',
              border: `2.5px solid ${bangMau.nhanManh}`,
              color: '#FFFFFF',
              fontSize: 30,
              fontWeight: 800,
            }}
          >
            {canh.tieuDeNho}
          </div>
        )}
      </div>

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
                tiLe={1.25}
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
