import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { BoiCanhHoatHinh } from '../boicanh/BoiCanhHoatHinh';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { giaiTrangThaiNhanVatTrongCanh } from '../nhanvat/dien_xuat';
import { DaoCu } from '../daocu/DaoCu';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngHoatHinh } from '../vfx/HieuUngHoatHinh';
import { KhungLoiBinhHaiHuoc } from './KhungLoiBinhHaiHuoc';
import { LopCauHoiTuongTac } from './LopCauHoiTuongTac';
import { locMocThoiGianHopLe } from '../daocu/minh_hoa_hop_le';

type Props = {
  canh: Canh;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

export const CanhDongThoiGian: React.FC<Props> = ({
  canh,
  bangMau,
  banDoNhanVat,
}) => {
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const danhSachNhanVat = giaiTrangThaiNhanVatTrongCanh(canh, frame, thoiLuong);
  const danhSachMoc = locMocThoiGianHopLe(canh.mocThoiGian);

  const chieuDaiTruc = interpolate(frame, [0, 26], [0, 1440], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ position: 'absolute', inset: 0 }}>
      <MayQuayDong
        camera={canh.camera}
        mayQuay={canh.mayQuay}
        luotThoai={canh.luotThoai}
        daoCu={canh.daoCu}
        chuyenCanh={canh.chuyenCanh}
        nhanVat={canh.nhanVat}
        thoiLuongCanh={thoiLuong}
      >
        <BoiCanhHoatHinh
          loai={canh.boiCanh}
          thoiTiet={canh.thoiTiet}
          vatTheXungQuanh={canh.vatTheXungQuanh}
          bienSoXe={canh.bienSoXe}
        />

        {/* Bang dong thoi gian sac net o nua tren */}
        <svg
          width={1920}
          height={1080}
          viewBox="0 0 1920 1080"
          style={{ position: 'absolute', inset: 0 }}
        >
          <rect
            x={140}
            y={150}
            width={1640}
            height={330}
            rx={26}
            fill="#FFFDF7"
            fillOpacity={0.93}
            stroke="#1E293B"
            strokeWidth={4}
          />

          <text
            x={190}
            y={210}
            fill="#0F172A"
            fontSize={34}
            fontWeight={900}
            fontFamily="Segoe UI, Arial, sans-serif"
          >
            {canh.tieuDeNho ?? 'Dòng thời gian lịch sử Toán học'}
          </text>

          {canh.namMoc && (
            <text
              x={1730}
              y={210}
              textAnchor="end"
              fill="#B45309"
              fontSize={26}
              fontWeight={800}
              fontFamily="Segoe UI, Arial, sans-serif"
            >
              {canh.namMoc}
            </text>
          )}

          {/* Truc ngang & cac moc thoi gian (khung trong sach neu thieu mocThoiGian trong JSON) */}
          {danhSachMoc.length > 0 && (
            <>
              <line
                x1={240}
                y1={335}
                x2={240 + chieuDaiTruc}
                y2={335}
                stroke={bangMau.nhanManh || '#F59E0B'}
                strokeWidth={8}
                strokeLinecap="round"
              />

              {danhSachMoc.map((moc, idx) => {
                const x =
                  danhSachMoc.length === 1
                    ? 960
                    : 380 + idx * (1160 / (danhSachMoc.length - 1));
                const noiBat = Boolean(moc.noiBat);
                return (
                  <g key={`${moc.nam}-${idx}`} transform={`translate(${x}, 335)`}>
                    <circle
                      cx={0}
                      cy={0}
                      r={noiBat ? 22 : 16}
                      fill={noiBat ? '#EF4444' : '#0EA5E9'}
                      stroke="#1E293B"
                      strokeWidth={4}
                    />
                    <text
                      x={0}
                      y={-36}
                      textAnchor="middle"
                      fill={noiBat ? '#B91C1C' : '#0F172A'}
                      fontSize={26}
                      fontWeight={900}
                      fontFamily="Segoe UI, Arial, sans-serif"
                    >
                      {moc.nam}
                    </text>
                    <text
                      x={0}
                      y={52}
                      textAnchor="middle"
                      fill="#334155"
                      fontSize={20}
                      fontWeight={700}
                      fontFamily="Segoe UI, Arial, sans-serif"
                    >
                      {moc.moTa}
                    </text>
                  </g>
                );
              })}
            </>
          )}

          {canh.daoCu?.map((dc, idx) => (
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

      {canh.cauHoiTuongTac && (
        <LopCauHoiTuongTac
          cauHoi={canh.cauHoiTuongTac}
          bangMau={bangMau}
          thoiLuongCanh={thoiLuong}
        />
      )}

      <KhungLoiBinhHaiHuoc loiBinh={canh.loiBinhHaiHuoc} />
    </div>
  );
};
