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
import { LopCauHoiTuongTac } from './LopCauHoiTuongTac';
import { chiaDongMoTaTimeline, locMocThoiGianHopLe } from '../daocu/minh_hoa_hop_le';

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
  const moCuonGiay = interpolate(frame, [0, 14], [0.82, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Cuon giay da co mo ra chua duong thoi gian lich su (Clean Cinema v3.0, khong tran khung, khong cat tu)
  const lopHud = (
    <>
      <div
        style={{
          position: 'absolute',
          top: 68,
          left: 88,
          right: 88,
          borderRadius: 14,
          backgroundColor: '#FAF2DC',
          border: '4px solid #1A1A1A',
          boxShadow: '8px 8px 0px rgba(26, 26, 26, 0.38)',
          padding: '22px 46px 26px',
          boxSizing: 'border-box',
          pointerEvents: 'none',
          fontFamily: 'Segoe UI, Arial, sans-serif',
          transform: `scaleX(${moCuonGiay.toFixed(3)})`,
          transformOrigin: 'center center',
        }}
      >
        {/* Hai truc cuon go co dien hai ben cuon giay da */}
        <div
          style={{
            position: 'absolute',
            top: -10,
            bottom: -10,
            left: -14,
            width: 22,
            borderRadius: 10,
            backgroundColor: '#92400E',
            border: '3px solid #1A1A1A',
          }}
        />
        <div
          style={{
            position: 'absolute',
            top: -10,
            bottom: -10,
            right: -14,
            width: 22,
            borderRadius: 10,
            backgroundColor: '#92400E',
            border: '3px solid #1A1A1A',
          }}
        />
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
                    {(() => {
                      const boCucChu = chiaDongMoTaTimeline(moc.moTa, danhSachMoc.length);
                      return (
                        <div
                          style={{
                            color: '#334155',
                            fontSize: boCucChu.fontSize,
                            fontWeight: 700,
                            lineHeight: boCucChu.lineHeight,
                            maxWidth: 340,
                            wordBreak: 'normal',
                            overflowWrap: 'break-word',
                          }}
                        >
                          {boCucChu.dong.map((dong, di) => (
                            <div key={`m-d-${idx}-${di}`}>{dong}</div>
                          ))}
                        </div>
                      );
                    })()}
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
                tiLe={1.2}
                thoiLuongCanh={thoiLuong}
                bienDoAmThanh={canh.bienDoAmThanh}
              />
            );
          })}
          <HieuUngHoatHinh
            danhSach={canh.hieuUngHoatHinh}
            nhanVat={danhSachNhanVat}
            tiLeNhanVat={1.2}
          />
        </svg>
      </MayQuayDong>
    </div>
  );
};
