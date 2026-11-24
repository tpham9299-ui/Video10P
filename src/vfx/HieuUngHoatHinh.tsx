import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { HieuUngHoatHinhItem } from '../kieu_dai';
import { bamTatDinh } from './tat_dinh';

type HieuUngHoatHinhProps = {
  danhSach?: HieuUngHoatHinhItem[];
};

const veBongDenNaySo = (t: number, frame: number, mau: string) => {
  // Pop-in nay nhe trong 18% dau
  const pop = t < 0.18 ? 0.4 + (t / 0.18) * 0.72 : t < 0.28 ? 1.12 - ((t - 0.18) / 0.1) * 0.12 : 1;
  const fade = t > 0.85 ? (1 - t) / 0.15 : 1;
  const nhipTia = 1 + 0.12 * Math.sin(frame * 0.45);

  return (
    <g transform={`scale(${pop.toFixed(3)})`} opacity={fade}>
      {/* Vong sang khong blur */}
      <circle cx={0} cy={-10} r={44 * nhipTia} fill="#FEF08A" fillOpacity={0.28} />
      {/* 7 tia sang bat xung quanh */}
      {Array.from({ length: 7 }).map((_, i) => {
        const goc = -Math.PI * 1.15 + (i / 6) * Math.PI * 1.3;
        const r1 = 36;
        const r2 = 52 * nhipTia;
        return (
          <line
            key={`tia-bd-${i}`}
            x1={Math.cos(goc) * r1}
            y1={-10 + Math.sin(goc) * r1}
            x2={Math.cos(goc) * r2}
            y2={-10 + Math.sin(goc) * r2}
            stroke={mau}
            strokeWidth={4.5}
            strokeLinecap="round"
          />
        );
      })}
      {/* Bong den */}
      <path
        d="M -22 -12 A 24 24 0 1 1 22 -12 C 20 2 13 8 12 18 L -12 18 C -13 8 -20 2 -22 -12 Z"
        fill="#FEF08A"
        stroke="#1E293B"
        strokeWidth={3.2}
        strokeLinejoin="round"
      />
      {/* Day toc */}
      <path d="M -6 14 L -6 -4 L 0 2 L 6 -4 L 6 14" fill="none" stroke="#D97706" strokeWidth={2.6} strokeLinecap="round" strokeLinejoin="round" />
      {/* Dui den */}
      <rect x={-11} y={18} width={22} height={11} rx={3} fill="#94A3B8" stroke="#1E293B" strokeWidth={2.4} />
      <line x1={-9} y1={23} x2={9} y2={23} stroke="#475569" strokeWidth={2} />
    </g>
  );
};

const veGiotMoHoi = (t: number) => {
  const dy = t * 44;
  const pop = t < 0.14 ? t / 0.14 : 1;
  const fade = t > 0.85 ? (1 - t) / 0.15 : 1;
  return (
    <g transform={`translate(0, ${dy.toFixed(1)}) scale(${pop.toFixed(3)})`} opacity={fade}>
      <path
        d="M 0 -26 C 14 -6, 18 10, 14 20 C 10 29, -10 29, -14 20 C -18 10, -14 -6, 0 -26 Z"
        fill="#38BDF8"
        stroke="#0369A1"
        strokeWidth={3.2}
        strokeLinejoin="round"
      />
      <ellipse cx={-4} cy={6} rx={3.5} ry={7} fill="#E0F2FE" transform="rotate(-14, -4, 6)" />
      <circle cx={-3} cy={17} r={2.2} fill="#FFFFFF" />
    </g>
  );
};

const veDauChamHoi = (t: number, frame: number, mau: string) => {
  const fade = t > 0.85 ? (1 - t) / 0.15 : 1;
  const cacDau = [
    { dx: -28, dy: 6, rot: -16, s: 0.82, delay: 0.1 },
    { dx: 0, dy: -8, rot: 0, s: 1.15, delay: 0 },
    { dx: 30, dy: 8, rot: 16, s: 0.78, delay: 0.2 },
  ];
  return (
    <g opacity={fade}>
      {cacDau.map((d, idx) => {
        const localT = Math.max(0, Math.min(1, (t - d.delay) / 0.25));
        const nay = Math.sin(frame * 0.28 + idx) * 5;
        return (
          <g
            key={`q-${idx}`}
            transform={`translate(${d.dx}, ${(d.dy + nay).toFixed(1)}) rotate(${d.rot}) scale(${(d.s * localT).toFixed(3)})`}
          >
            <text
              x={0}
              y={14}
              textAnchor="middle"
              fill={mau}
              stroke="#1E293B"
              strokeWidth={3}
              paintOrder="stroke"
              fontSize={44}
              fontWeight={900}
              fontFamily="Segoe UI, Arial, sans-serif"
            >
              ?
            </text>
          </g>
        );
      })}
    </g>
  );
};

const veSocSetDanh = (t: number, frame: number) => {
  const fade = t > 0.82 ? (1 - t) / 0.18 : 1;
  const rung = Math.sin(frame * 1.4) * 3;
  return (
    <g transform={`translate(${rung.toFixed(1)}, 0)`} opacity={fade}>
      {/* Tia set vang phai & trai */}
      <polygon
        points="-58,-48 -24,-22 -36,-16 -8,14 -32,6 -22,22 -64,-10 -46,-16"
        fill="#FACC15"
        stroke="#1E293B"
        strokeWidth={3}
        strokeLinejoin="round"
      />
      <polygon
        points="58,-48 24,-22 36,-16 8,14 32,6 22,22 64,-10 46,-16"
        fill="#FB923C"
        stroke="#1E293B"
        strokeWidth={3}
        strokeLinejoin="round"
      />
      <polygon
        points="0,-78 14,-44 4,-44 16,-14 -12,-46 -2,-46"
        fill="#FEF08A"
        stroke="#1E293B"
        strokeWidth={3}
        strokeLinejoin="round"
      />
    </g>
  );
};

const veSaoLapLanh = (t: number, frame: number, mau: string, seed: number) => {
  const fade = t < 0.12 ? t / 0.12 : t > 0.85 ? (1 - t) / 0.15 : 1;
  const viTri = [
    { dx: 0, dy: 0, s: 1.05 },
    { dx: -42, dy: -22, s: 0.72 },
    { dx: 44, dy: -16, s: 0.68 },
    { dx: 26, dy: 30, s: 0.56 },
  ];

  return (
    <g opacity={fade}>
      {viTri.map((v, i) => {
        const pulse = 0.7 + 0.35 * Math.abs(Math.sin(frame * 0.22 + i * 1.4 + seed));
        const rot = (frame * 1.6 + i * 28) % 360;
        const sc = v.s * pulse;
        return (
          <g
            key={`star-${i}`}
            transform={`translate(${v.dx}, ${v.dy}) rotate(${rot.toFixed(1)}) scale(${sc.toFixed(3)})`}
          >
            <path
              d="M 0 -22 L 6 -6 L 22 0 L 6 6 L 0 22 L -6 6 L -22 0 L -6 -6 Z"
              fill={i % 2 === 0 ? mau : '#FFFFFF'}
              stroke="#B45309"
              strokeWidth={1.8}
              strokeLinejoin="round"
            />
          </g>
        );
      })}
    </g>
  );
};

const veKhoiChayTron = (t: number, seed: number) => {
  const fade = Math.max(0, 1 - t);
  return (
    <g opacity={fade * 0.9}>
      {Array.from({ length: 5 }).map((_, i) => {
        const dx = -t * (65 + i * 24) - bamTatDinh(seed + i * 13) * 18;
        const dy = -t * (16 + (i % 3) * 14) + (i % 2 === 0 ? 6 : -6);
        const r = (14 + (i % 3) * 7) * (0.65 + t * 0.75);
        return (
          <circle
            key={`khoi-${i}`}
            cx={dx}
            cy={dy}
            r={r}
            fill="#F8FAFC"
            stroke="#CBD5E1"
            strokeWidth={2.5}
          />
        );
      })}
    </g>
  );
};

const veCoLanImLang = (t: number) => {
  // Co lan ngang man hinh, xoay tron va nay nhe hai huoc
  const dx = interpolate(t, [0, 1], [-420, 520], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const bounceY = -Math.abs(Math.sin(t * Math.PI * 5)) * 26;
  const rot = t * 760;
  const fade = t < 0.08 ? t / 0.08 : t > 0.88 ? (1 - t) / 0.12 : 1;

  return (
    <g opacity={fade}>
      {/* Bui dat nho phia sau bui co */}
      <circle cx={dx - 44} cy={22} r={10} fill="#E7D3B1" fillOpacity={0.65} />
      <circle cx={dx - 68} cy={16} r={7} fill="#E7D3B1" fillOpacity={0.45} />
      {/* Bong co tren dat */}
      <ellipse cx={dx} cy={36} rx={30} ry={7} fill="#0F172A" fillOpacity={0.2} />

      {/* Bui co kho xoay tron */}
      <g transform={`translate(${dx.toFixed(1)}, ${bounceY.toFixed(1)}) rotate(${rot.toFixed(1)})`}>
        <circle cx={0} cy={0} r={34} fill="#D97706" fillOpacity={0.18} stroke="#92400E" strokeWidth={3.5} strokeDasharray="10 6" />
        <circle cx={0} cy={0} r={24} fill="none" stroke="#B45309" strokeWidth={3} strokeDasharray="8 5" />
        <path d="M -30 -8 Q -6 -22 28 -10" fill="none" stroke="#78350F" strokeWidth={3} strokeLinecap="round" />
        <path d="M -26 14 Q 4 -4 30 12" fill="none" stroke="#92400E" strokeWidth={3} strokeLinecap="round" />
        <path d="M -12 -30 Q 8 0 -10 30" fill="none" stroke="#78350F" strokeWidth={2.8} strokeLinecap="round" />
        <path d="M 14 -28 Q -6 4 16 28" fill="none" stroke="#B45309" strokeWidth={2.8} strokeLinecap="round" />
        <line x1={-36} y1={-4} x2={-24} y2={-12} stroke="#78350F" strokeWidth={2.6} strokeLinecap="round" />
        <line x1={26} y1={-22} x2={36} y2={-14} stroke="#78350F" strokeWidth={2.6} strokeLinecap="round" />
        <line x1={-20} y1={26} x2={-30} y2={20} stroke="#78350F" strokeWidth={2.6} strokeLinecap="round" />
      </g>
    </g>
  );
};

const veNhanChuHaiHuoc = (t: number, chu: string, mau: string) => {
  // Dong dau nghieng bat mat co nhip phong nhe
  const pop =
    t < 0.14
      ? interpolate(t, [0, 0.14], [1.65, 0.94], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
      : t < 0.24
        ? interpolate(t, [0.14, 0.24], [0.94, 1.03], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })
        : 1;
  const fade = t > 0.88 ? (1 - t) / 0.12 : 1;
  const rong = Math.max(190, Math.min(430, chu.length * 17 + 62));

  return (
    <g transform={`rotate(-7) scale(${pop.toFixed(3)})`} opacity={fade}>
      <rect
        x={-rong / 2 + 5}
        y={-30 + 5}
        width={rong}
        height={60}
        rx={14}
        fill="#1E293B"
      />
      <rect
        x={-rong / 2}
        y={-30}
        width={rong}
        height={60}
        rx={14}
        fill={mau}
        stroke="#1E293B"
        strokeWidth={4}
      />
      <rect
        x={-rong / 2 + 6}
        y={-24}
        width={rong - 12}
        height={48}
        rx={9}
        fill="none"
        stroke="#FFFFFF"
        strokeOpacity={0.55}
        strokeWidth={2}
        strokeDasharray="6 4"
      />
      <text
        x={0}
        y={9}
        textAnchor="middle"
        fill="#1E293B"
        fontSize={27}
        fontWeight={900}
        fontFamily="Segoe UI, Arial, sans-serif"
      >
        {chu}
      </text>
    </g>
  );
};

export const HieuUngHoatHinh: React.FC<HieuUngHoatHinhProps> = ({ danhSach }) => {
  const frame = useCurrentFrame();

  if (!danhSach || danhSach.length === 0) {
    return null;
  }

  return (
    <g pointerEvents="none">
      {danhSach.map((item, idx) => {
        const delta = frame - item.tuFrame;
        const thoiLuong = Math.max(1, item.thoiLuong);
        if (delta < 0 || delta > thoiLuong) {
          return null;
        }
        const t = delta / thoiLuong;
        const tiLe = item.tiLe ?? 1;
        const seed = (idx + 1) * 47;

        let noiDung: React.ReactNode = null;
        switch (item.loai) {
          case 'bong_den_nay_so':
            noiDung = veBongDenNaySo(t, frame, item.mau ?? '#F59E0B');
            break;
          case 'giot_mo_hoi':
            noiDung = veGiotMoHoi(t);
            break;
          case 'dau_cham_hoi':
            noiDung = veDauChamHoi(t, frame, item.mau ?? '#F97316');
            break;
          case 'soc_set_danh':
            noiDung = veSocSetDanh(t, frame);
            break;
          case 'sao_lap_lanh':
            noiDung = veSaoLapLanh(t, frame, item.mau ?? '#FACC15', seed);
            break;
          case 'khoi_chay_tron':
            noiDung = veKhoiChayTron(t, seed);
            break;
          case 'co_lan_im_lang':
            noiDung = veCoLanImLang(t);
            break;
          case 'nhan_chu_hai_huoc':
            noiDung = veNhanChuHaiHuoc(
              t,
              item.chuHienThi ?? 'Ủa khoan đã?!',
              item.mau ?? '#FDE047',
            );
            break;
        }

        return (
          <g
            key={`${item.loai}-${idx}`}
            transform={`translate(${item.x}, ${item.y}) scale(${tiLe})`}
          >
            {noiDung}
          </g>
        );
      })}
    </g>
  );
};
