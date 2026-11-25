import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import type { BangMau, CauHoiTuongTac } from '../kieu_dai';
import { kepGiaTri, springTatDinh } from '../xuong/duong_cong';
import { tinhTrangThaiCauHoiTuongTac } from './tuong_tac';

type LopCauHoiTuongTacProps = {
  cauHoi?: CauHoiTuongTac;
  bangMau: BangMau;
  thoiLuongCanh: number;
  /** Bo cuc 2 cot (nam gon ben phai ~65% man hinh de khong de nhan vat ben trai) hoac can giua */
  boCuc?: 'phai_hai_cot' | 'giua';
};

/**
 * Lop giao dien cau hoi tuong tac khan gia:
 * - The cau hoi bat ra bang springTatDinh
 * - Thanh dem nguoc 3 giay + dong ho so nhay nhip moi giay
 * - Hop dap an bung no sau khi het gio (khong dung blur, tat dinh 100%)
 */
export const LopCauHoiTuongTac: React.FC<LopCauHoiTuongTacProps> = ({
  cauHoi,
  bangMau,
  thoiLuongCanh,
  boCuc = 'phai_hai_cot',
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (!cauHoi || !cauHoi.cauHoi) {
    return null;
  }

  const tt = tinhTrangThaiCauHoiTuongTac(cauHoi, frame, thoiLuongCanh, fps);
  const scaleThe = kepGiaTri(springTatDinh(frame - 2, 11, 200), 0, 1.06);
  const scaleSoDem = tt.dangDemNguoc
    ? 1 + (1 - kepGiaTri(springTatDinh(tt.frameTrongGiayHienTai, 10, 260), 0, 1)) * 0.32
    : 1;
  const scaleDapAn = tt.daHienDapAn
    ? kepGiaTri(springTatDinh(tt.frameTuDapAn, 10, 210), 0, 1.06)
    : 0;

  const mauThanhDem =
    tt.tiLeConLai > 0.55
      ? '#38BDF8'
      : tt.tiLeConLai > 0.25
        ? '#FACC15'
        : '#FB7185';

  const laHaiCotPhai = boCuc === 'phai_hai_cot';

  return (
    <div
      style={{
        position: 'absolute',
        top: 76,
        bottom: 154,
        left: laHaiCotPhai ? 620 : 0,
        right: laHaiCotPhai ? 52 : 0,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: laHaiCotPhai ? 'center' : 'flex-start',
        alignItems: laHaiCotPhai ? 'stretch' : 'center',
        gap: 18,
        pointerEvents: 'none',
        zIndex: 25,
        fontFamily: 'Segoe UI, Arial, sans-serif',
        boxSizing: 'border-box',
      }}
    >
      {/* The cau hoi chinh */}
      <div
        style={{
          width: laHaiCotPhai ? '100%' : 1120,
          maxWidth: laHaiCotPhai ? '100%' : '88%',
          backgroundColor: 'rgba(15, 23, 42, 0.94)',
          border: `4px solid ${bangMau.nhanManh || '#FACC15'}`,
          borderRadius: 24,
          padding: '20px 28px',
          boxShadow: '10px 10px 0px rgba(15, 23, 42, 0.45)',
          transform: `scale(${scaleThe.toFixed(3)})`,
          transformOrigin: laHaiCotPhai ? 'center right' : 'top center',
          boxSizing: 'border-box',
        }}
      >
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            gap: 16,
            marginBottom: 12,
          }}
        >
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 10,
              padding: '5px 16px',
              borderRadius: 999,
              backgroundColor: '#FEF08A',
              color: '#0F172A',
              fontSize: 16,
              fontWeight: 900,
              letterSpacing: 0.9,
              textTransform: 'uppercase',
              border: '2.5px solid #1E293B',
            }}
          >
            <span>?</span>
            <span>Thử tài khán giả • {tt.tongGiayDemNguoc} giây</span>
          </div>

          {/* Dong ho dem nguoc so tron */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 12,
            }}
          >
            <div
              style={{
                color: tt.daHienDapAn ? '#4ADE80' : '#E2E8F0',
                fontSize: 18,
                fontWeight: 800,
              }}
            >
              {tt.daHienDapAn
                ? 'Hết giờ!'
                : tt.dangDocCauHoi
                  ? 'Chuẩn bị...'
                  : 'Đếm ngược'}
            </div>
            <div
              style={{
                width: 54,
                height: 54,
                borderRadius: 999,
                backgroundColor: tt.daHienDapAn ? '#22C55E' : mauThanhDem,
                border: '3.5px solid #FFFFFF',
                color: '#0F172A',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 28,
                fontWeight: 900,
                transform: `scale(${scaleSoDem.toFixed(3)})`,
              }}
            >
              {tt.daHienDapAn ? '✓' : tt.giayConLai}
            </div>
          </div>
        </div>

        {/* Noi dung cau hoi */}
        <div
          style={{
            color: '#FFFFFF',
            fontSize: 34,
            fontWeight: 900,
            lineHeight: 1.28,
            marginBottom: cauHoi.luaChon && cauHoi.luaChon.length > 0 ? 14 : 16,
          }}
        >
          {cauHoi.cauHoi}
        </div>

        {/* Cac phuong an goi y (neu co) */}
        {cauHoi.luaChon && cauHoi.luaChon.length > 0 && (
          <div
            style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: 12,
              marginBottom: 16,
            }}
          >
            {cauHoi.luaChon.map((lc, idx) => (
              <div
                key={`lc-${idx}`}
                style={{
                  padding: '8px 18px',
                  borderRadius: 12,
                  backgroundColor: 'rgba(30, 41, 59, 0.92)',
                  border: '2px solid rgba(254, 240, 138, 0.5)',
                  color: '#F8FAFC',
                  fontSize: 21,
                  fontWeight: 700,
                }}
              >
                {lc}
              </div>
            ))}
          </div>
        )}

        {/* Thanh tien do dem nguoc 3 giay */}
        <div
          style={{
            width: '100%',
            height: 16,
            borderRadius: 999,
            backgroundColor: 'rgba(255, 255, 255, 0.16)',
            border: '2px solid rgba(255, 255, 255, 0.3)',
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              height: '100%',
              width: `${(tt.tiLeConLai * 100).toFixed(2)}%`,
              backgroundColor: mauThanhDem,
              borderRadius: 999,
            }}
          />
        </div>
      </div>

      {/* Hop dap an bat ra sau khi het dem nguoc */}
      {tt.daHienDapAn && scaleDapAn > 0.02 && (
        <div
          style={{
            width: laHaiCotPhai ? '100%' : 980,
            maxWidth: laHaiCotPhai ? '100%' : '84%',
            backgroundColor: '#ECFDF5',
            border: '4px solid #059669',
            borderRadius: 22,
            padding: '18px 28px',
            boxShadow: '9px 9px 0px #064E3B',
            transform: `scale(${scaleDapAn.toFixed(3)})`,
            transformOrigin: laHaiCotPhai ? 'center right' : 'top center',
            boxSizing: 'border-box',
          }}
        >
          <div
            style={{
              display: 'inline-block',
              padding: '4px 14px',
              borderRadius: 999,
              backgroundColor: '#059669',
              color: '#FFFFFF',
              fontSize: 15,
              fontWeight: 900,
              letterSpacing: 1,
              textTransform: 'uppercase',
              marginBottom: 8,
            }}
          >
            Đáp án chính xác
          </div>
          <div
            style={{
              color: '#064E3B',
              fontSize: 32,
              fontWeight: 900,
              lineHeight: 1.25,
            }}
          >
            {cauHoi.dapAn}
          </div>
          {cauHoi.giaiThichNgan && (
            <div
              style={{
                marginTop: 8,
                color: '#1E293B',
                fontSize: 22,
                fontWeight: 700,
                lineHeight: 1.35,
              }}
            >
              {cauHoi.giaiThichNgan}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
