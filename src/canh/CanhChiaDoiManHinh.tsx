import React from 'react';
import { useCurrentFrame } from 'remotion';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { BoiCanhHoatHinh } from '../boicanh/BoiCanhHoatHinh';
import { locDaoCuKhongTrungLap } from '../boicanh/moi_truong_logic';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import {
  giaiTrangThaiNhanVatTrongCanh,
  type TrangThaiNhanVatDaGiai,
} from '../nhanvat/dien_xuat';
import { DaoCu } from '../daocu/DaoCu';
import { HieuUngHoatHinh } from '../vfx/HieuUngHoatHinh';
import { LopCauHoiTuongTac } from './LopCauHoiTuongTac';
import { chiaNhomNhanVatChiaDoi } from './tuong_tac';
import { kepGiaTri, noiSuy, springTatDinh } from '../xuong/duong_cong';

type Props = {
  canh: Canh;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

/**
 * Canh chia doi man hinh (gocQuay = "chia_doi_man_hinh"):
 * - Chia khung 1920x1080 thanh 2 nua trai/phai sac net voi duong ke phan tach kieu truyen tranh
 * - Moi ben tu can giua nhan vat cua minh va phong nhe (1.08x) + sang vien khi den luot noi
 */
export const CanhChiaDoiManHinh: React.FC<Props> = ({
  canh,
  bangMau,
  banDoNhanVat,
}) => {
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const tatCaNhanVat = giaiTrangThaiNhanVatTrongCanh(canh, frame, thoiLuong);
  const { benTrai, benPhai } = chiaNhomNhanVatChiaDoi(tatCaNhanVat);

  const traiDangNoi = benTrai.some((nv) => Boolean(nv.dangNoi));
  const phaiDangNoi = benPhai.some((nv) => Boolean(nv.dangNoi));
  const batTuDongFocus = Boolean(canh.mayQuay?.tuDongFocusNguoiNoi);

  const vaoKhung = kepGiaTri(springTatDinh(frame, 13, 190), 0, 1);
  const zoomTrai =
    batTuDongFocus && traiDangNoi && !phaiDangNoi ? noiSuy(1, 1.08, vaoKhung) : 1;
  const zoomPhai =
    batTuDongFocus && phaiDangNoi && !traiDangNoi ? noiSuy(1, 1.08, vaoKhung) : 1;

  const daoCuHopLe = locDaoCuKhongTrungLap(canh.daoCu, canh.nhanVat);

  const veNuaManHinh = (
    nhom: TrangThaiNhanVatDaGiai[],
    laBenTrai: boolean,
    zoomNua: number,
    dangNoiBenNay: boolean,
  ) => {
    const daoCuNua = daoCuHopLe.filter((dc) =>
      laBenTrai ? dc.x < 960 : dc.x >= 960,
    );
    const hieuUngNua = (canh.hieuUngHoatHinh ?? []).filter((hu) =>
      laBenTrai ? hu.x < 960 : hu.x >= 960,
    );

    // Can lai toa do nhan vat vao giua nua khung 960px cho bo cuc can doi
    const dichKhungX = laBenTrai ? 0 : -960;

    return (
      <div
        style={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: laBenTrai ? 0 : 960,
          width: 960,
          overflow: 'hidden',
          boxSizing: 'border-box',
          border:
            batTuDongFocus && dangNoiBenNay
              ? `6px solid ${bangMau.nhanManh || '#FACC15'}`
              : '0px solid transparent',
        }}
      >
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: dichKhungX,
            width: 1920,
            height: 1080,
            transformOrigin: laBenTrai ? '480px 540px' : '1440px 540px',
            transform: `translate3d(0px, 0px, 0) scale(${zoomNua.toFixed(4)})`,
          }}
        >
          <BoiCanhHoatHinh
            loai={canh.boiCanh}
            thoiTiet={canh.thoiTiet}
            vatTheXungQuanh={canh.vatTheXungQuanh}
            bienSoXe={canh.bienSoXe}
            nhanVat={canh.nhanVat}
            daoCu={daoCuHopLe}
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
            {daoCuNua.map((dc, idx) => (
              <DaoCu key={`dc-${laBenTrai ? 'L' : 'R'}-${idx}`} daoCu={dc} />
            ))}
            {nhom.map((nv, idx) => {
              const tt = banDoNhanVat[nv.id];
              if (!tt) return null;
              // Neu 1 nhan vat tren nua nay, can gon quanh tam nua man hinh (480 / 1440)
              const xCan =
                nhom.length === 1
                  ? laBenTrai
                    ? kepGiaTri(nv.x, 340, 620)
                    : kepGiaTri(nv.x, 1300, 1580)
                  : nv.x;
              return (
                <NguoiQueDong
                  key={`${nv.id}-${idx}`}
                  thongTin={tt}
                  trangThai={{ ...nv, x: xCan }}
                  tiLe={1.34}
                  thoiLuongCanh={thoiLuong}
                  bienDoAmThanh={canh.bienDoAmThanh}
                  anhSangMoiTruong={canh.anhSangMoiTruong}
                />
              );
            })}
            <HieuUngHoatHinh
              danhSach={hieuUngNua}
              nhanVat={nhom}
              tiLeNhanVat={1.34}
            />
          </svg>
        </div>
      </div>
    );
  };

  return (
    <div style={{ position: 'absolute', inset: 0, overflow: 'hidden' }}>
      {veNuaManHinh(benTrai, true, zoomTrai, traiDangNoi)}
      {veNuaManHinh(benPhai, false, zoomPhai, phaiDangNoi)}

      {/* Thanh chia doi man hinh sac net o giua (x = 960) */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: 954,
          width: 12,
          backgroundColor: '#0F172A',
          borderLeft: `3px solid ${bangMau.nhanManh || '#FACC15'}`,
          borderRight: `3px solid ${bangMau.nhanManh || '#FACC15'}`,
          boxSizing: 'border-box',
          pointerEvents: 'none',
          zIndex: 18,
          transform: `scaleY(${vaoKhung.toFixed(3)})`,
          transformOrigin: 'center center',
        }}
      />

      {canh.cauHoiTuongTac && (
        <LopCauHoiTuongTac
          cauHoi={canh.cauHoiTuongTac}
          bangMau={bangMau}
          thoiLuongCanh={thoiLuong}
        />
      )}
    </div>
  );
};
