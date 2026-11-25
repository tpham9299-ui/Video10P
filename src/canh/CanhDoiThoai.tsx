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
import { CanhChiaDoiManHinh } from './CanhChiaDoiManHinh';

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
  const frame = useCurrentFrame();

  if (canh.mayQuay?.gocQuay === 'chia_doi_man_hinh') {
    return (
      <CanhChiaDoiManHinh
        canh={canh}
        bangMau={bangMau}
        banDoNhanVat={banDoNhanVat}
      />
    );
  }

  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const danhSachNhanVat = giaiTrangThaiNhanVatTrongCanh(canh, frame, thoiLuong);
  const daoCuHienThi = locDaoCuKhongTrungLap(canh.daoCu, canh.nhanVat);

  // Clean Cinema UI (v3.0): go bo hop tieu de & GOC BINH LUAN co dinh de khung hinh doi thoai sach dep 100%
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
                  tiLe={1.28}
                  thoiLuongCanh={thoiLuong}
                  bienDoAmThanh={canh.bienDoAmThanh}
                  anhSangMoiTruong={canh.anhSangMoiTruong}
                />
              );
            })}
            <HieuUngHoatHinh
              danhSach={canh.hieuUngHoatHinh}
              nhanVat={danhSachNhanVat}
              tiLeNhanVat={1.28}
            />
          </svg>
        )}
      </MayQuayDong>
    </div>
  );
};
