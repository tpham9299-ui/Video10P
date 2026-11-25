import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { BangMau, Canh, NhanVatTrongCanh, ThongTinNhanVat } from '../kieu_dai';
import { BoiCanhHoatHinh } from '../boicanh/BoiCanhHoatHinh';
import { locDaoCuKhongTrungLap } from '../boicanh/moi_truong_logic';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { giaiTrangThaiNhanVatTrongCanh } from '../nhanvat/dien_xuat';
import { DaoCu } from '../daocu/DaoCu';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngHoatHinh } from '../vfx/HieuUngHoatHinh';
import { VUNG_END_SCREEN_YOUTUBE } from './ke_chuyen_v35_logic';

type Props = {
  canh: Canh;
  tieuDeVideo: string;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
  /** Ho so Mascot kenh xuat hien giua 2 khung End-Screen 15s cuoi (v3.5) */
  mascot?: ThongTinNhanVat | null;
  /** Chi bat banner & khung End-Screen YouTube o canh cuoi cung cua hoi cuoi cung toan tap */
  hienBannerKetThuc?: boolean;
};

/**
 * CanhKet (v3.5):
 * - Giu nguyen tuong thich nguoc khi hienBannerKetThuc=false
 * - Khi hienBannerKetThuc=true (15s cuoi toan tap): chua san 2 khung vien 16:9 dung vung chuan
 *   YouTube End-Screen (goc trai & phai), dat Mascot o giua ra hieu moi khan gia xem tap tiep theo.
 * - Tat dinh 100%, khong dung hieu ung mo hay ngau nhien.
 */
export const CanhKet: React.FC<Props> = ({
  canh,
  tieuDeVideo,
  bangMau,
  banDoNhanVat,
  mascot,
  hienBannerKetThuc = false,
}) => {
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const danhSachGoc = giaiTrangThaiNhanVatTrongCanh(canh, frame, thoiLuong);
  const doMo = interpolate(frame, [0, 18], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const daoCuHienThi = locDaoCuKhongTrungLap(canh.daoCu, canh.nhanVat);

  const nhipMuiTen = Math.sin(frame * 0.16) * 8;
  const { khungTrai, khungPhai, vungMascotGiua } = VUNG_END_SCREEN_YOUTUBE;
  const nhanTrai = (canh.endScreen?.khungTraiNhan || 'TẬP TOÁN HỌC LIÊN QUAN').trim();
  const nhanPhai = (canh.endScreen?.khungPhaiNhan || 'DANH SÁCH PHÁT ĐỀ XUẤT').trim();
  const loiDanXemTiep = (
    canh.endScreen?.loiDanXemTiep ||
    'Bấm chọn 1 câu chuyện Toán học hấp dẫn ở hai bên để xem tiếp nhé!'
  ).trim();

  // O che do End-Screen: uu tien Mascot dung giua khung hinh (x=960) de khong bi 2 khung End-Screen che mat
  const danhSachNhanVat: NhanVatTrongCanh[] = (() => {
    if (!hienBannerKetThuc) {
      return danhSachGoc;
    }
    const coMascotTrongCanh = mascot && danhSachGoc.some((nv) => nv.id === mascot.id);
    if (mascot && !coMascotTrongCanh) {
      return [
        {
          id: mascot.id,
          x: vungMascotGiua.x,
          y: vungMascotGiua.y,
          huong: 'phai',
          hanhDong: 'quay_nhin_khan_gia',
          bieuCam: 'vui_tuoi',
          vatCamTay: 'cuon_giay',
          dangNoi: true,
        },
      ];
    }
    if (danhSachGoc.length > 0) {
      return [
        {
          ...danhSachGoc[0],
          x: vungMascotGiua.x,
          y: vungMascotGiua.y,
          diChuyenDenX: undefined,
          hanhDong: 'quay_nhin_khan_gia',
        },
      ];
    }
    return danhSachGoc;
  })();

  const banDoHieuLuc: Record<string, ThongTinNhanVat> = mascot
    ? { ...banDoNhanVat, [mascot.id]: mascot }
    : banDoNhanVat;

  const lopHud = (
    <>
      {(hienBannerKetThuc || canh.tieuDeNho) && (
        <div
          style={{
            position: 'absolute',
            top: 42,
            left: 72,
            right: 72,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            opacity: doMo,
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              padding: '16px 40px',
              borderRadius: 20,
              backgroundColor: 'rgba(15, 23, 42, 0.92)',
              border: `3.5px solid ${bangMau.nhanManh}`,
              textAlign: 'center',
              maxWidth: 1360,
              boxShadow: '7px 7px 0px rgba(15, 23, 42, 0.5)',
            }}
          >
            {hienBannerKetThuc && (
              <div
                style={{
                  color: bangMau.nhanManh,
                  fontSize: 19,
                  fontWeight: 900,
                  letterSpacing: 1.8,
                  marginBottom: 6,
                  textTransform: 'uppercase',
                }}
              >
                Cảm ơn bạn đã theo dõi!
              </div>
            )}
            <div
              style={{
                color: '#FFFFFF',
                fontSize: 40,
                fontWeight: 900,
                lineHeight: 1.18,
              }}
            >
              {canh.tieuDeNho ?? tieuDeVideo}
            </div>
            {hienBannerKetThuc && (
              <div
                style={{
                  marginTop: 8,
                  color: '#FEF08A',
                  fontSize: 22,
                  fontWeight: 700,
                }}
              >
                {loiDanXemTiep}
              </div>
            )}
          </div>
        </div>
      )}

      {/* 2 khung vien chuan YouTube End-Screen (trai & phai 16:9) — KHONG blur */}
      {hienBannerKetThuc && (
        <div style={{ position: 'absolute', inset: 0, opacity: doMo, pointerEvents: 'none' }}>
          {/* Khung End-Screen ben trai */}
          <div
            style={{
              position: 'absolute',
              left: khungTrai.x,
              top: khungTrai.y,
              width: khungTrai.width,
              height: khungTrai.height,
              borderRadius: 20,
              border: `5px solid ${bangMau.nhanManh}`,
              backgroundColor: 'rgba(15, 23, 42, 0.52)',
              boxShadow: '8px 8px 0px rgba(15, 23, 42, 0.55)',
              boxSizing: 'border-box',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              padding: 18,
            }}
          >
            <div
              style={{
                alignSelf: 'flex-start',
                backgroundColor: bangMau.nhanManh,
                color: '#1A1A1A',
                border: '2.5px solid #1A1A1A',
                borderRadius: 10,
                padding: '5px 14px',
                fontSize: 18,
                fontWeight: 900,
                letterSpacing: 0.8,
              }}
            >
              {nhanTrai}
            </div>
            <div
              style={{
                alignSelf: 'center',
                color: '#FEF9C3',
                fontSize: 22,
                fontWeight: 800,
                border: '2.5px dashed rgba(254, 240, 138, 0.65)',
                borderRadius: 12,
                padding: '10px 20px',
              }}
            >
              ▶ Vùng Video Đề Xuất (YouTube)
            </div>
          </div>

          {/* Khung End-Screen ben phai */}
          <div
            style={{
              position: 'absolute',
              left: khungPhai.x,
              top: khungPhai.y,
              width: khungPhai.width,
              height: khungPhai.height,
              borderRadius: 20,
              border: `5px solid ${bangMau.nhanManh}`,
              backgroundColor: 'rgba(15, 23, 42, 0.52)',
              boxShadow: '8px 8px 0px rgba(15, 23, 42, 0.55)',
              boxSizing: 'border-box',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              padding: 18,
            }}
          >
            <div
              style={{
                alignSelf: 'flex-end',
                backgroundColor: '#38BDF8',
                color: '#0F172A',
                border: '2.5px solid #1A1A1A',
                borderRadius: 10,
                padding: '5px 14px',
                fontSize: 18,
                fontWeight: 900,
                letterSpacing: 0.8,
              }}
            >
              {nhanPhai}
            </div>
            <div
              style={{
                alignSelf: 'center',
                color: '#E0F2FE',
                fontSize: 22,
                fontWeight: 800,
                border: '2.5px dashed rgba(186, 230, 253, 0.65)',
                borderRadius: 12,
                padding: '10px 20px',
              }}
            >
              ▶ Vùng Danh Sách Phát (YouTube)
            </div>
          </div>

          {/* 2 mui ten dan huong nhe tu Mascot o giua sang 2 khung End-Screen */}
          <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: 'absolute', inset: 0 }}>
            <g transform={`translate(${(685 - nhipMuiTen).toFixed(1)}, 470)`}>
              <polygon points="48,-20 0,0 48,20 38,0" fill={bangMau.nhanManh} stroke="#1A1A1A" strokeWidth={3} />
            </g>
            <g transform={`translate(${(1187 + nhipMuiTen).toFixed(1)}, 470)`}>
              <polygon points="0,-20 48,0 0,20 10,0" fill="#38BDF8" stroke="#1A1A1A" strokeWidth={3} />
            </g>
          </svg>
        </div>
      )}
    </>
  );

  return (
    <div style={{ position: 'absolute', inset: 0 }}>
      <MayQuayDong
        camera={hienBannerKetThuc ? { kieu: 'tinh', zoom: 1, panX: 0, panY: 0 } : canh.camera}
        mayQuay={hienBannerKetThuc ? { gocQuay: 'toan_canh', doPhong: 1 } : canh.mayQuay}
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
          nhanVat={danhSachNhanVat}
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
              const tt = banDoHieuLuc[nv.id];
              if (!tt) return null;
              return (
                <NguoiQueDong
                  key={`${nv.id}-${idx}`}
                  thongTin={tt}
                  trangThai={nv}
                  tiLe={1.25}
                  thoiLuongCanh={thoiLuong}
                  bienDoAmThanh={canh.bienDoAmThanh}
                  nhinThangOngKinh={hienBannerKetThuc}
                  anhSangMoiTruong={canh.anhSangMoiTruong}
                />
              );
            })}
            <HieuUngHoatHinh
              danhSach={canh.hieuUngHoatHinh}
              nhanVat={danhSachNhanVat}
              tiLeNhanVat={1.25}
            />
          </svg>
        )}
      </MayQuayDong>
    </div>
  );
};
