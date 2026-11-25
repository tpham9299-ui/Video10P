import React from 'react';
import { useCurrentFrame } from 'remotion';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { BoiCanhHoatHinh } from '../boicanh/BoiCanhHoatHinh';
import { locDaoCuKhongTrungLap } from '../boicanh/moi_truong_logic';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import {
  giaiTrangThaiNhanVatTrongCanh,
  timLuotThoaiTaiFrame,
} from '../nhanvat/dien_xuat';
import { DaoCu } from '../daocu/DaoCu';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngHoatHinh } from '../vfx/HieuUngHoatHinh';
import { KhungLoiBinhHaiHuoc } from './KhungLoiBinhHaiHuoc';
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
  const luotDangNoi = timLuotThoaiTaiFrame(canh.luotThoai, frame);
  const tongLuot = canh.luotThoai?.length ?? 0;
  const chiSoLuot =
    luotDangNoi && canh.luotThoai ? canh.luotThoai.indexOf(luotDangNoi) : -1;
  const tenNguoiDangNoi = luotDangNoi
    ? banDoNhanVat[luotDangNoi.nhanVatId]?.ten ?? luotDangNoi.nhanVatId
    : null;
  const daoCuHienThi = locDaoCuKhongTrungLap(canh.daoCu, canh.nhanVat);

  const lopHud = (
    <>
      {canh.tieuDeNho && (
        <div
          style={{
            position: 'absolute',
            top: 76,
            left: 0,
            right: 0,
            display: 'flex',
            justifyContent: 'center',
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              padding: '8px 26px',
              borderRadius: 16,
              backgroundColor: 'rgba(15, 23, 42, 0.88)',
              border: `2.5px solid ${bangMau.nhanManh}`,
              color: '#FFFFFF',
              fontSize: 30,
              fontWeight: 800,
              boxShadow: '4px 4px 0px rgba(15, 23, 42, 0.35)',
            }}
          >
            {canh.tieuDeNho}
          </div>
        </div>
      )}

      {/* Nhan hien luot doi thoai khi canh co nhieu luot thoai */}
      {tongLuot > 1 && tenNguoiDangNoi && chiSoLuot >= 0 && (
        <div
          style={{
            position: 'absolute',
            top: 76,
            left: 52,
            pointerEvents: 'none',
            zIndex: 18,
          }}
        >
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 10,
              padding: '6px 16px',
              borderRadius: 999,
              backgroundColor: 'rgba(15, 23, 42, 0.9)',
              border: `2.5px solid ${bangMau.nhanManh || '#FACC15'}`,
              color: '#FEF08A',
              fontSize: 17,
              fontWeight: 800,
              boxShadow: '4px 4px 0px rgba(15, 23, 42, 0.35)',
            }}
          >
            <span>{tenNguoiDangNoi}</span>
            <span style={{ color: '#94A3B8' }}>•</span>
            <span style={{ color: '#FFFFFF' }}>
              {chiSoLuot + 1}/{tongLuot}
            </span>
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
                tiLe={1.28}
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
