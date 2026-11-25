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
  const daoCuHienThi = locDaoCuKhongTrungLap(canh.daoCu, canh.nhanVat);

  const tienDoTruc = interpolate(frame, [0, 28], [0, 100], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Tach bang dong thoi gian ra NGOAI transform zoom/pan cua MayQuayDong (>= 76px tu mep tren)
  const lopHud = (
    <>
      <div
        style={{
          position: 'absolute',
          top: 76,
          left: 96,
          right: 96,
          borderRadius: 24,
          backgroundColor: 'rgba(255, 253, 247, 0.95)',
          border: '4px solid #1E293B',
          boxShadow: '8px 8px 0px rgba(15, 23, 42, 0.35)',
          padding: '20px 36px 26px',
          boxSizing: 'border-box',
          pointerEvents: 'none',
          fontFamily: 'Segoe UI, Arial, sans-serif',
        }}
      >
        {/* Tieu de & khoang thoi gian */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: 22,
            gap: 16,
          }}
        >
          <div style={{ color: '#0F172A', fontSize: 32, fontWeight: 900 }}>
            {canh.tieuDeNho ?? 'Dòng thời gian lịch sử Toán học'}
          </div>
          {canh.namMoc && (
            <div
              style={{
                padding: '6px 18px',
                borderRadius: 999,
                backgroundColor: '#FEF3C7',
                border: '2.5px solid #B45309',
                color: '#B45309',
                fontSize: 22,
                fontWeight: 900,
                flexShrink: 0,
              }}
            >
              {canh.namMoc}
            </div>
          )}
        </div>

        {/* Thanh moc thoi gian ngang + cac diem cot moc (khung trong sach neu thieu mocThoiGian trong JSON) */}
        {danhSachMoc.length > 0 && (
          <div style={{ position: 'relative', paddingTop: 6 }}>
            {/* Duong ray nen + thanh tien do vang chay tu trai sang phai */}
            <div
              style={{
                position: 'absolute',
                top: 52,
                left: 60,
                right: 60,
                height: 8,
                borderRadius: 999,
                backgroundColor: '#E2E8F0',
                overflow: 'hidden',
              }}
            >
              <div
                style={{
                  width: `${tienDoTruc.toFixed(1)}%`,
                  height: '100%',
                  backgroundColor: bangMau.nhanManh || '#F59E0B',
                  borderRadius: 999,
                }}
              />
            </div>

            {/* Cac cot moc chia deu & tu xuong dong gon dep */}
            <div
              style={{
                position: 'relative',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'flex-start',
                gap: 16,
              }}
            >
              {danhSachMoc.map((moc, idx) => {
                const noiBat = Boolean(moc.noiBat);
                const mocBatDau = idx * 7;
                const opMoc = interpolate(frame, [mocBatDau, mocBatDau + 10], [0, 1], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                });
                return (
                  <div
                    key={`${moc.nam}-${idx}`}
                    style={{
                      flex: '1 1 0',
                      display: 'flex',
                      flexDirection: 'column',
                      alignItems: 'center',
                      textAlign: 'center',
                      opacity: opMoc,
                    }}
                  >
                    <div
                      style={{
                        color: noiBat ? '#B91C1C' : '#0F172A',
                        fontSize: 25,
                        fontWeight: 900,
                        lineHeight: 1.15,
                        marginBottom: 8,
                      }}
                    >
                      {moc.nam}
                    </div>
                    <div
                      style={{
                        width: noiBat ? 34 : 26,
                        height: noiBat ? 34 : 26,
                        marginTop: noiBat ? 0 : 4,
                        marginBottom: noiBat ? 10 : 14,
                        borderRadius: 999,
                        backgroundColor: noiBat ? '#EF4444' : '#0EA5E9',
                        border: '4px solid #1E293B',
                        boxSizing: 'border-box',
                      }}
                    />
                    <div
                      style={{
                        color: '#334155',
                        fontSize: 19,
                        fontWeight: 700,
                        lineHeight: 1.3,
                        maxWidth: 340,
                        wordBreak: 'break-word',
                      }}
                    >
                      {moc.moTa}
                    </div>
                  </div>
                );
              })}
            </div>
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
                tiLe={1.2}
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
