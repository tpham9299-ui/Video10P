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
import { LopCauHoiTuongTac } from './LopCauHoiTuongTac';

type Props = {
  canh: Canh;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

/**
 * Canh hai huoc Clean Cinema (v3.0): nhan manh bieu cam, bong bong chat & 6 hieu ung hai thi giac (khong GOC BINH LUAN).
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

  const lopHud = canh.cauHoiTuongTac ? (
    <LopCauHoiTuongTac
      cauHoi={canh.cauHoiTuongTac}
      bangMau={bangMau}
      thoiLuongCanh={thoiLuong}
    />
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
                  tiLe={1.45}
                  thoiLuongCanh={thoiLuong}
                  bienDoAmThanh={canh.bienDoAmThanh}
                  anhSangMoiTruong={canh.anhSangMoiTruong}
                />
              );
            })}
            <HieuUngHoatHinh
              danhSach={canh.hieuUngHoatHinh}
              nhanVat={danhSachNhanVat}
              tiLeNhanVat={1.45}
            />
          </svg>
        )}
      </MayQuayDong>
    </div>
  );
};
