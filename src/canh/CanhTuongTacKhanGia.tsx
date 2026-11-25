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
 * Canh tuong tac khan gia (v2.0):
 * - Chia 2 vung ro rang: nhan vat dung lech sang trai ~22% man hinh (x ~ 420px),
 *   hop cau hoi dem nguoc & hop "DAP AN CHINH XAC" nam gon ben phai ~65% man hinh (x = 620..1868px)
 * - Khoa camera o 1.0x de hop dap an tuyet doi KHONG de len mat hay than nhan vat
 */
export const CanhTuongTacKhanGia: React.FC<Props> = ({
  canh,
  bangMau,
  banDoNhanVat,
}) => {
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const danhSachGoc = giaiTrangThaiNhanVatTrongCanh(
    { ...canh, loaiCanh: 'tuong_tac_khan_gia' },
    frame,
    thoiLuong,
  );
  const daoCuHienThi = locDaoCuKhongTrungLap(canh.daoCu, canh.nhanVat);

  // Dat nhan vat vao vung trai (~22% cua 1920 = 422px) de tach biet hoan toan voi vung cau hoi ben phai (65%)
  const danhSachNhanVat = danhSachGoc.map((nv, idx) => {
    const xTrai =
      danhSachGoc.length === 1
        ? 420
        : 270 + idx * (220 / Math.max(1, danhSachGoc.length - 1));
    return {
      ...nv,
      x: xTrai,
      diChuyenDenX: undefined,
      y: Math.min(nv.y, 792),
      huong: 'phai' as const,
    };
  });

  const lopHud = (
    <LopCauHoiTuongTac
      cauHoi={canh.cauHoiTuongTac}
      bangMau={bangMau}
      thoiLuongCanh={thoiLuong}
      boCuc="phai_hai_cot"
    />
  );

  return (
    <div style={{ position: 'absolute', inset: 0 }}>
      <MayQuayDong
        camera={{ kieu: 'tinh', zoom: 1, panX: 0, panY: 0 }}
        mayQuay={{ gocQuay: 'toan_canh', doPhong: 1 }}
        luotThoai={canh.luotThoai}
        daoCu={daoCuHienThi}
        chuyenCanh={canh.chuyenCanh}
        nhanVat={danhSachNhanVat}
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
          thoiLuongCanh={thoiLuong}
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
                tiLe={1.32}
                thoiLuongCanh={thoiLuong}
                bienDoAmThanh={canh.bienDoAmThanh}
                nhinThangOngKinh={true}
              />
            );
          })}
          <HieuUngHoatHinh
            danhSach={canh.hieuUngHoatHinh}
            nhanVat={danhSachNhanVat}
            tiLeNhanVat={1.32}
          />
        </svg>
      </MayQuayDong>
    </div>
  );
};
