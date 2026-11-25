import React from 'react';
import { Img, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import type {
  AnhSangMoiTruong,
  LoaiBoiCanh,
  LoaiThoiTiet,
  VatTheXungQuanh,
} from '../kieu_dai';
import { bamTatDinh } from '../vfx/tat_dinh';
import { useCameraParallax } from '../vfx/MayQuayDong';
import { SinhVatVaMoiTruong } from './SinhVatVaMoiTruong';
import { tinhKenBurnsNenAI, tinhLopKhongKhiNenAI } from './nen_ai_logic';

type NenMinhHoaAIProps = {
  anhBoiCanh: string;
  loaiBoiCanh: LoaiBoiCanh;
  thoiTiet?: LoaiThoiTiet;
  anhSangMoiTruong?: AnhSangMoiTruong;
  vatTheXungQuanh?: readonly VatTheXungQuanh[];
  bienSoXe?: string;
  laKhungTranhDacTa?: boolean;
  thoiLuongCanh?: number;
};

/**
 * Nen minh hoa AI 2.5D (v3.0):
 * - Render anh minh hoa AI qua <Img src={staticFile(anhBoiCanh)} /> voi chuyen dong Ken Burns + parallax nhe tat dinh
 * - Phu lop khong khi song dong 100% tat dinh theo loaiAnhSang & thoiTiet (KHONG blur, KHONG ngau nhien):
 *   luong nang xien (nang_am/hoang_hon), bui sang troi, anh nen nhap nhay (radialGradient phang),
 *   mua/tuyet/la roi ngoai troi, may/chim bay nhe o nen troi va vatTheXungQuanh.
 */
export const NenMinhHoaAI: React.FC<NenMinhHoaAIProps> = ({
  anhBoiCanh,
  loaiBoiCanh,
  thoiTiet = 'khong',
  anhSangMoiTruong,
  vatTheXungQuanh,
  bienSoXe,
  laKhungTranhDacTa = false,
  thoiLuongCanh,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const cam = useCameraParallax();
  const tongFrame = Math.max(1, thoiLuongCanh ?? durationInFrames);

  const kb = tinhKenBurnsNenAI(
    frame,
    tongFrame,
    `${anhBoiCanh}|${loaiBoiCanh}`,
    cam,
    laKhungTranhDacTa,
  );
  const khongKhi = tinhLopKhongKhiNenAI(
    anhSangMoiTruong,
    thoiTiet,
    loaiBoiCanh,
    laKhungTranhDacTa,
  );

  // Nhip tho anh sang tu nhien tat dinh
  const nhipNang = 0.88 + Math.sin(frame * 0.045) * 0.12;
  const nhipNen =
    0.84 + Math.sin(frame * 0.24) * 0.1 + Math.cos(frame * 0.37) * 0.06;
  const idPrefix = anhBoiCanh.replace(/[^a-zA-Z0-9]/g, '_').slice(-24) || 'ai';

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        overflow: 'hidden',
        pointerEvents: 'none',
        backgroundColor: '#1E1B18',
      }}
    >
      {/* Lop anh minh hoa AI 16:9 voi Ken Burns cham muot + parallax nhe */}
      <Img
        src={staticFile(anhBoiCanh)}
        style={{
          position: 'absolute',
          inset: 0,
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          transformOrigin: 'center center',
          transform: `translate3d(${kb.tx}px, ${kb.ty}px, 0) scale(${kb.scale})`,
        }}
      />

      {/* Lop khong khi song dong tat dinh (100% vector SVG phang, KHONG blur) */}
      <svg
        width={1920}
        height={1080}
        viewBox="0 0 1920 1080"
        style={{
          position: 'absolute',
          inset: 0,
          pointerEvents: 'none',
        }}
      >
        <defs>
          <linearGradient id={`nang-${idPrefix}`} x1="0" y1="0" x2="0.4" y2="1">
            <stop
              offset="0%"
              stopColor={khongKhi.loaiAnhSang === 'hoang_hon' ? '#FDBA74' : '#FEF9C3'}
              stopOpacity={0.28 * nhipNang}
            />
            <stop
              offset="68%"
              stopColor={khongKhi.loaiAnhSang === 'hoang_hon' ? '#FB923C' : '#FDE68A'}
              stopOpacity={0.08 * nhipNang}
            />
            <stop offset="100%" stopColor="#FEF08A" stopOpacity={0} />
          </linearGradient>

          <radialGradient id={`nen-${idPrefix}`} cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#FEF08A" stopOpacity={0.34 * nhipNen} />
            <stop offset="45%" stopColor="#F59E0B" stopOpacity={0.14 * nhipNen} />
            <stop offset="100%" stopColor="#F59E0B" stopOpacity={0} />
          </radialGradient>

          <radialGradient id={`dem-${idPrefix}`} cx="50%" cy="28%" r="72%">
            <stop offset="0%" stopColor="#38BDF8" stopOpacity={0.08} />
            <stop offset="100%" stopColor="#0B1120" stopOpacity={0.28} />
          </radialGradient>
        </defs>

        {/* 1. Luong nang xien nhe cho nang_am & hoang_hon */}
        {khongKhi.coLuongNangXien && (
          <g>
            <polygon
              points="120,-40 460,-40 940,1080 510,1080"
              fill={`url(#nang-${idPrefix})`}
            />
            <polygon
              points="640,-40 880,-40 1320,1080 1020,1080"
              fill={`url(#nang-${idPrefix})`}
              opacity={0.78}
            />
            <polygon
              points="1210,-40 1410,-40 1790,1080 1560,1080"
              fill={`url(#nang-${idPrefix})`}
              opacity={0.55}
            />
          </g>
        )}

        {/* 2. Anh lua / nen nhap nhay bang radialGradient phang cho anh_nen */}
        {khongKhi.coAnhNenNhapNhay && (
          <g>
            <circle
              cx={laKhungTranhDacTa ? 1120 : 420}
              cy={laKhungTranhDacTa ? 440 : 520}
              r={380 * nhipNen}
              fill={`url(#nen-${idPrefix})`}
            />
            <circle
              cx={laKhungTranhDacTa ? 760 : 1490}
              cy={laKhungTranhDacTa ? 540 : 490}
              r={290 * (1.85 - nhipNen)}
              fill={`url(#nen-${idPrefix})`}
              opacity={0.72}
            />
          </g>
        )}

        {/* 3. Khong khi dem lanh + sao lap lanh nhe phan troi */}
        {khongKhi.coSuongDem && (
          <g>
            <rect x={0} y={0} width={1920} height={1080} fill={`url(#dem-${idPrefix})`} />
            {!khongKhi.laTrongNha &&
              !laKhungTranhDacTa &&
              Array.from({ length: 18 }).map((_, i) => {
                const sx = 80 + bamTatDinh(i * 37 + 13) * 1760;
                const sy = 50 + bamTatDinh(i * 53 + 7) * 320;
                const lapLanh = 0.25 + 0.55 * Math.abs(Math.sin(frame * 0.08 + i * 1.3));
                const r = 1.6 + (i % 3) * 0.9;
                return (
                  <circle
                    key={`sao-ai-${i}`}
                    cx={sx.toFixed(1)}
                    cy={sy.toFixed(1)}
                    r={r}
                    fill="#E0F2FE"
                    fillOpacity={lapLanh}
                  />
                );
              })}
          </g>
        )}

        {/* 4. May mong & chim bay nhe o phan troi ngoai troi */}
        {khongKhi.coMayChimNgoaiTroi && (
          <g opacity={0.62}>
            {[0, 1].map((i) => {
              const cx = (((240 + i * 980 + frame * (0.35 + i * 0.14)) % 2320) - 200);
              const cy = 115 + i * 54;
              return (
                <g key={`may-ai-${i}`} transform={`translate(${cx.toFixed(1)}, ${cy}) scale(${1.05 - i * 0.18})`} opacity={0.38}>
                  <circle cx={-34} cy={8} r={20} fill="#FFFFFF" />
                  <circle cx={-6} cy={-5} r={28} fill="#FFFFFF" />
                  <circle cx={24} cy={3} r={22} fill="#FFFFFF" />
                  <rect x={-38} y={8} width={76} height={18} rx={9} fill="#FFFFFF" />
                </g>
              );
            })}
            {[0, 1, 2].map((i) => {
              const x = ((360 + i * 210 + frame * (1.15 + i * 0.16)) % 2260) - 160;
              const nhipVo = Math.sin(frame * 0.32 + i * 1.4);
              const y = 148 + i * 28 + Math.sin(frame * 0.07 + i) * 9;
              const dauCanhY = nhipVo * 7.5;
              return (
                <path
                  key={`chim-ai-${i}`}
                  d={`M -14 ${dauCanhY.toFixed(1)} Q -7 ${(-4 + nhipVo * 3.5).toFixed(1)} 0 0 Q 7 ${(-4 + nhipVo * 3.5).toFixed(1)} 14 ${dauCanhY.toFixed(1)}`}
                  transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)}) scale(${(0.82 - i * 0.08).toFixed(2)})`}
                  fill="none"
                  stroke={khongKhi.loaiAnhSang === 'hoang_hon' ? '#7C2D12' : '#1E293B'}
                  strokeOpacity={0.55}
                  strokeWidth={2.2}
                  strokeLinecap="round"
                />
              );
            })}
          </g>
        )}

        {/* 5. Bui sang troi lo lung tat dinh 100% tao chieu sau 2.5D */}
        {khongKhi.coBuiSang && (
          <g>
            {Array.from({ length: laKhungTranhDacTa ? 28 : 20 }).map((_, i) => {
              const x0 = bamTatDinh(i * 41 + 9) * 1920;
              const y0 = bamTatDinh(i * 67 + 19) * 960;
              const tocDoY = 0.35 + (i % 4) * 0.22;
              const y = (((y0 - frame * tocDoY) % 1020) + 1020) % 1020 + 20;
              const x = x0 + Math.sin(frame * 0.032 + i * 1.7) * 28;
              const r = 1.8 + (i % 3) * 1.15;
              const op =
                (laKhungTranhDacTa ? 0.36 : 0.28) *
                (0.5 + 0.5 * Math.sin(frame * 0.07 + i * 2.1));
              return (
                <circle
                  key={`bui-ai-${i}`}
                  cx={x.toFixed(1)}
                  cy={y.toFixed(1)}
                  r={r.toFixed(1)}
                  fill={khongKhi.mauHatSang}
                  fillOpacity={op.toFixed(3)}
                />
              );
            })}
          </g>
        )}

        {/* 6. Sinh vat / do vat xung quanh (tat tren khung tranh dac ta can canh vat the) */}
        {!laKhungTranhDacTa &&
          vatTheXungQuanh &&
          vatTheXungQuanh.length > 0 && (
            <SinhVatVaMoiTruong
              boiCanh={loaiBoiCanh}
              thoiTiet={thoiTiet}
              vatTheXungQuanh={vatTheXungQuanh}
              bienSoXe={bienSoXe}
            />
          )}

        {/* 7. Mua / tuyet / la roi ngoai troi tat dinh */}
        {khongKhi.coMua && (
          <g>
            {Array.from({ length: 38 }).map((_, i) => {
              const speed = 18 + (i % 4) * 4;
              const x0 = bamTatDinh(i * 29 + 1) * 2100;
              const y0 = bamTatDinh(i * 53 + 7) * 1160;
              const y = ((y0 + frame * speed) % 1140) - 40;
              const x = (((x0 - frame * speed * 0.22) % 2040) + 2040) % 2040 - 60;
              return (
                <line
                  key={`mua-ai-${i}`}
                  x1={x.toFixed(1)}
                  y1={y.toFixed(1)}
                  x2={(x - 9).toFixed(1)}
                  y2={(y + 32).toFixed(1)}
                  stroke="#E0F2FE"
                  strokeOpacity={0.54}
                  strokeWidth={2}
                  strokeLinecap="round"
                />
              );
            })}
          </g>
        )}

        {khongKhi.coTuyet && (
          <g>
            {Array.from({ length: 32 }).map((_, i) => {
              const x0 = bamTatDinh(i * 19 + 5) * 1920;
              const y0 = bamTatDinh(i * 43 + 9) * 1080;
              const speed = 1.5 + (i % 4) * 0.55;
              const y = ((y0 + frame * speed) % 1120) - 20;
              const x = (((x0 + Math.sin(frame * 0.05 + i * 1.7) * 30) % 1960) + 1960) % 1960 - 20;
              const r = 2.8 + (i % 3) * 1.7;
              return (
                <circle
                  key={`tuyet-ai-${i}`}
                  cx={x.toFixed(1)}
                  cy={y.toFixed(1)}
                  r={r}
                  fill="#FFFFFF"
                  fillOpacity={0.78}
                />
              );
            })}
          </g>
        )}

        {khongKhi.coLaRoi && (
          <g>
            {Array.from({ length: 14 }).map((_, i) => {
              const x0 = bamTatDinh(i * 31 + 3) * 1920;
              const y0 = bamTatDinh(i * 47 + 11) * 1080;
              const speed = 2.2 + (i % 4) * 0.65;
              const y = ((y0 + frame * speed) % 1140) - 30;
              const x = (((x0 + Math.sin(frame * 0.07 + i) * 52 + frame * 1.05) % 2020) + 2020) % 2020 - 50;
              const rot = (frame * (2.4 + (i % 3)) + i * 47) % 360;
              const mauLa = i % 3 === 0 ? '#F59E0B' : i % 3 === 1 ? '#EA580C' : '#EAB308';
              return (
                <g key={`la-ai-${i}`} transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)}) rotate(${rot.toFixed(1)})`}>
                  <path d="M -11 0 Q 0 -9 13 0 Q 0 9 -11 0 Z" fill={mauLa} stroke="#9A3412" strokeWidth={1.2} />
                </g>
              );
            })}
          </g>
        )}
      </svg>
    </div>
  );
};
