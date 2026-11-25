import React from 'react';
import { useCurrentFrame } from 'remotion';
import type {
  AnhSangMoiTruong,
  DaoCuTrongCanh,
  LoaiBoiCanh,
  LoaiThoiTiet,
  NhanVatTrongCanh,
  VatTheXungQuanh,
} from '../kieu_dai';
import { bamTatDinh } from '../vfx/tat_dinh';
import { useCameraParallax } from '../vfx/MayQuayDong';
import { kepGiaTri } from '../xuong/duong_cong';
import {
  BOI_CANH_TRONG_NHA,
  BOI_CANH_VU_TRU,
  coAnGiuongBenhNen,
  layKhungCuaSoChoBoiCanh,
} from './moi_truong_logic';
import {
  CangBienTauThuy,
  DuongPhoXeCo,
  GiangDuongDaiHoc,
  KhongGianVuTruToan,
  LangQueAnDoADong,
  NhaCoPhongSinh,
  PhongBenhVien,
  PhongThiNghiemCo,
  PhongTroBepLua,
  SanTruongCoDien,
} from './BoiCanhMoi';
import { NenMinhHoaAI } from './NenMinhHoaAI';
import { SinhVatVaMoiTruong } from './SinhVatVaMoiTruong';

type BoiCanhHoatHinhProps = {
  loai: LoaiBoiCanh;
  thoiTiet?: LoaiThoiTiet;
  vatTheXungQuanh?: readonly VatTheXungQuanh[];
  bienSoXe?: string;
  /** Danh sach nhan vat trong canh de tu dong khu trung lap do vat nen (noi em be / giuong benh) */
  nhanVat?: readonly NhanVatTrongCanh[];
  /** Danh sach dao cu trong canh de tu dong khu trung lap do vat nen */
  daoCu?: readonly DaoCuTrongCanh[];
  anNoiNen?: boolean;
  anGiuongBenhNen?: boolean;
  /** Duong dan tuong doi trong public/ toi anh minh hoa AI (v3.0); neu co se dung NenMinhHoaAI */
  anhBoiCanh?: string | null;
  /** Thong so anh sang moi truong tu Pillow de dong bo hieu ung khong khi (v3.0) */
  anhSangMoiTruong?: AnhSangMoiTruong;
  /** Khung tranh dac ta can canh vat the/phong canh (v3.0) */
  laKhungTranhDacTa?: boolean;
  /** Thoi luong canh (frame) de tinh Ken Burns muot cho NenMinhHoaAI */
  thoiLuongCanh?: number;
};

export type ParallaxOffset = {
  // Dich chuyen tuong doi ben trong MayQuayDong (da di chuyen 1.0x):
  // Lop 1 (troi 0.2x) bu tru -0.8 * pan; Lop 2 (nui/den/nha 0.5x) bu tru -0.5 * pan; Lop 3 (cay/san 1.0x) = 0
  lop1X: number;
  lop1Y: number;
  lop2X: number;
  lop2Y: number;
  lop3X: number;
  lop3Y: number;
};

function tinhParallax(panX: number, panY: number): ParallaxOffset {
  const px = kepGiaTri(panX, -180, 180);
  const py = kepGiaTri(panY, -120, 120);
  return {
    lop1X: -px * 0.8,
    lop1Y: -py * 0.5,
    lop2X: -px * 0.5,
    lop2Y: -py * 0.3,
    lop3X: 0,
    lop3Y: 0,
  };
}

/** Cum may trang bong benh troi tat dinh theo frame */
export const CumMay: React.FC<{
  xGoc: number;
  y: number;
  tiLe: number;
  tocDo: number;
  frame: number;
  mau?: string;
  doMo?: number;
}> = ({ xGoc, y, tiLe, tocDo, frame, mau = '#FFFFFF', doMo = 0.92 }) => {
  const x = ((xGoc + frame * tocDo) % 2480) - 280;
  return (
    <g transform={`translate(${x.toFixed(1)}, ${y}) scale(${tiLe})`} opacity={doMo}>
      <circle cx={-38} cy={10} r={24} fill={mau} />
      <circle cx={-10} cy={-6} r={34} fill={mau} />
      <circle cx={26} cy={2} r={28} fill={mau} />
      <circle cx={52} cy={14} r={20} fill={mau} />
      <rect x={-46} y={10} width={104} height={24} rx={12} fill={mau} />
    </g>
  );
};

/** Canh chim bay xa vo canh mem 2 doan tat dinh */
export const ChimBay: React.FC<{
  xGoc: number;
  yGoc: number;
  tocDo: number;
  tiLe: number;
  frame: number;
  pha: number;
  mau?: string;
}> = ({ xGoc, yGoc, tocDo, tiLe, frame, pha, mau = '#334155' }) => {
  const x = ((xGoc + frame * tocDo) % 2340) - 200;
  const nhipVo = Math.sin(frame * 0.34 + pha);
  const y = yGoc + Math.sin(frame * 0.08 + pha) * 10 - nhipVo * 2.5;
  const canhGiuaY = -6 + nhipVo * 4.5;
  const dauCanhY = nhipVo * 9.5;
  return (
    <path
      d={`M -18 ${dauCanhY.toFixed(1)} Q -9 ${canhGiuaY.toFixed(1)} 0 0 Q 9 ${canhGiuaY.toFixed(1)} 18 ${dauCanhY.toFixed(1)}`}
      transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)}) scale(${tiLe})`}
      fill="none"
      stroke={mau}
      strokeWidth={2.7}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  );
};

/** Dai song nuoc cuon lien mach bang duong cong sin muot */
export const DaiSongCuon: React.FC<{
  y: number;
  bienDo: number;
  buocSong: number;
  tocDo: number;
  frame: number;
  mau: string;
  doMo: number;
  doDay?: number;
}> = ({ y, bienDo, buocSong, tocDo, frame, mau, doMo, doDay = 3.2 }) => {
  const dichX = -(((frame * tocDo) % buocSong) + buocSong) % buocSong;
  const soChuKy = Math.ceil(2520 / buocSong) + 2;
  const doan: string[] = [];
  const xBatDau = -260 + dichX;
  doan.push(`M ${xBatDau.toFixed(1)} ${y}`);
  for (let i = 0; i < soChuKy; i++) {
    const x0 = xBatDau + i * buocSong;
    const x1 = x0 + buocSong * 0.25;
    const x2 = x0 + buocSong * 0.5;
    const x3 = x0 + buocSong * 0.75;
    const x4 = x0 + buocSong;
    doan.push(
      `Q ${x1.toFixed(1)} ${(y - bienDo).toFixed(1)} ${x2.toFixed(1)} ${y} Q ${x3.toFixed(1)} ${(y + bienDo).toFixed(1)} ${x4.toFixed(1)} ${y}`,
    );
  }
  return (
    <path
      d={doan.join(' ')}
      fill="none"
      stroke={mau}
      strokeOpacity={doMo}
      strokeWidth={doDay}
      strokeLinecap="round"
    />
  );
};

/** Nen tinh (React.memo) cho BoBienHyLap: giam re-render SVG nang tren CI */
const BoBienHyLapDenTinh = React.memo(() => (
  <g>
    {/* Vach da trang ben trai + hang cot Doric */}
    <path d="M -220 360 Q 170 340 360 390 Q 520 430 610 560 L -220 580 Z" fill="#F1F5F9" />
    <path d="M -220 420 Q 190 400 350 450 L 490 580 L -220 580 Z" fill="#E2E8F0" />
    {/* Mai den & 4 cot da co dai tren doi */}
    <g transform="translate(88, 226)">
      <polygon points="-14,48 164,-12 342,48" fill="#F8FAFC" stroke="#CBD5E1" strokeWidth={4} strokeLinejoin="round" />
      <rect x={-4} y={48} width={336} height={18} fill="#E2E8F0" stroke="#CBD5E1" strokeWidth={2} />
      {[24, 108, 192, 276].map((cx) => (
        <g key={`cot-${cx}`}>
          <rect x={cx - 6} y={66} width={36} height={10} rx={2} fill="#F1F5F9" stroke="#CBD5E1" strokeWidth={2} />
          <rect x={cx} y={76} width={24} height={148} fill="#F8FAFC" stroke="#CBD5E1" strokeWidth={2} />
          <line x1={cx + 8} y1={78} x2={cx + 8} y2={222} stroke="#E2E8F0" strokeWidth={2} />
          <line x1={cx + 16} y1={78} x2={cx + 16} y2={222} stroke="#E2E8F0" strokeWidth={2} />
        </g>
      ))}
      <rect x={-12} y={224} width={352} height={18} fill="#E2E8F0" />
    </g>
  </g>
));

const BoBienHyLapSanTinh = React.memo(() => (
  <g>
    <path d="M -180 710 Q 520 676 1080 698 Q 1560 716 2100 688 L 2100 1180 L -180 1180 Z" fill="url(#hyLapSan)" />
    <path d="M -180 738 Q 640 710 1280 732 Q 1620 742 2100 722" fill="none" stroke="#D6B98C" strokeWidth={5} />
    {[180, 460, 780, 1120, 1460, 1740].map((gx, i) => (
      <ellipse key={`da-${i}`} cx={gx} cy={835 + (i % 2) * 34} rx={58} ry={13} fill="#D6B98C" fillOpacity={0.38} />
    ))}
  </g>
));

/** 1. Bo bien Hy Lap co dai: mat troi ben trai (~30% be ngang), parallax 3 lop, song cuon & tan o-liu lech pha */
const BoBienHyLap: React.FC<{
  frame: number;
  laHoangHon: boolean;
  px: ParallaxOffset;
}> = ({ frame, laHoangHon, px }) => {
  const troiTren = laHoangHon ? '#EA580C' : '#0EA5E9';
  const troiGiua = laHoangHon ? '#FB923C' : '#38BDF8';
  const troiDuoi = laHoangHon ? '#FDE68A' : '#E0F2FE';
  const bienTren = laHoangHon ? '#0369A1' : '#0284C7';
  const bienDuoi = laHoangHon ? '#1E3A8A' : '#0EA5E9';
  const matTroiMau = laHoangHon ? '#FEF08A' : '#FFFBEB';

  // Tan cay o-liu dung dua lech pha giua cac cum la
  const duaLa1 = Math.sin(frame * 0.06) * 5.2;
  const duaLa2 = Math.sin(frame * 0.072 + 1.25) * 4.4;
  const duaLa3 = Math.sin(frame * 0.055 + 2.4) * 5.6;
  const duaLaY = Math.cos(frame * 0.058) * 2.2;

  const thuyenX = 1140 + ((frame * 0.65) % 480);
  const thuyenY = 548 + Math.sin(frame * 0.1) * 4;
  const thuyenLac = Math.sin(frame * 0.1 + 0.5) * 2.2;

  // Mat troi nam ben trai (~30% cua 1920 = 576) de KHONG bi the GOC BINH LUAN goc phai che khuat
  const matTroiX = laHoangHon ? 560 : 576;
  const matTroiY = laHoangHon ? 405 : 185;

  return (
    <g>
      <defs>
        <linearGradient id="hyLapTroi" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={troiTren} />
          <stop offset="55%" stopColor={troiGiua} />
          <stop offset="100%" stopColor={troiDuoi} />
        </linearGradient>
        <linearGradient id="hyLapBien" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={bienTren} />
          <stop offset="100%" stopColor={bienDuoi} />
        </linearGradient>
        <linearGradient id="hyLapSan" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#FEF3C7" />
          <stop offset="100%" stopColor="#E7D3B1" />
        </linearGradient>
      </defs>

      {/* LOP 1 (Parallax 0.2x): Bau troi, mat troi ben trai (~30%), may & hai au */}
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <rect x={-260} y={-120} width={2440} height={740} fill="url(#hyLapTroi)" />

        {/* Mat troi am ap ben trai (~30% be ngang, khong blur) */}
        <g transform={`translate(${matTroiX}, ${matTroiY})`}>
          <circle cx={0} cy={0} r={148 + Math.sin(frame * 0.05) * 4} fill={matTroiMau} fillOpacity={0.14} />
          <circle cx={0} cy={0} r={100} fill={matTroiMau} fillOpacity={0.24} />
          <circle cx={0} cy={0} r={62} fill={matTroiMau} />
        </g>

        <CumMay xGoc={160} y={135} tiLe={1.35} tocDo={0.42} frame={frame} mau={laHoangHon ? '#FFEDD5' : '#FFFFFF'} doMo={0.9} />
        <CumMay xGoc={840} y={100} tiLe={1.1} tocDo={0.28} frame={frame} mau={laHoangHon ? '#FED7AA' : '#FFFFFF'} doMo={0.85} />
        <CumMay xGoc={1420} y={195} tiLe={0.95} tocDo={0.35} frame={frame} mau={laHoangHon ? '#FFEDD5' : '#FFFFFF'} doMo={0.8} />

        <ChimBay xGoc={420} yGoc={215} tocDo={1.35} tiLe={1.0} frame={frame} pha={0.4} mau={laHoangHon ? '#7C2D12' : '#0C4A6E'} />
        <ChimBay xGoc={478} yGoc={188} tocDo={1.25} tiLe={0.82} frame={frame} pha={1.9} mau={laHoangHon ? '#7C2D12' : '#0C4A6E'} />
        <ChimBay xGoc={1080} yGoc={238} tocDo={1.1} tiLe={0.76} frame={frame} pha={3.1} mau={laHoangHon ? '#7C2D12' : '#0C4A6E'} />
      </g>

      {/* LOP 2 (Parallax 0.5x): Bien Dia Trung Hai song cuon muot, dao xa, canh buom & den Hy Lap */}
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        <rect x={-260} y={530} width={2440} height={260} fill="url(#hyLapBien)" />

        {/* Anh nang phan chieu nhe tren mat bien duoi mat troi ben trai */}
        {[0, 1, 2, 3].map((i) => {
          const rx = 56 - i * 9 + Math.sin(frame * 0.1 + i) * 6;
          return (
            <ellipse
              key={`phan-chieu-${i}`}
              cx={matTroiX + Math.sin(frame * 0.08 + i * 1.4) * 8}
              cy={555 + i * 32}
              rx={rx}
              ry={4.5}
              fill={matTroiMau}
              fillOpacity={0.35 - i * 0.06}
            />
          );
        })}

        {/* Dao nui xa chan troi */}
        <path d="M 880 532 Q 1030 462 1190 508 Q 1340 475 1480 532 Z" fill={laHoangHon ? '#9A3412' : '#38BDF8'} fillOpacity={0.45} />
        <path d="M 1520 532 Q 1680 468 1860 512 L 2140 532 Z" fill={laHoangHon ? '#7C2D12' : '#0284C7'} fillOpacity={0.4} />

        {/* 3 dai song nuoc cuon muot lech toc do */}
        <DaiSongCuon y={564} bienDo={5} buocSong={180} tocDo={1.0} frame={frame} mau="#E0F2FE" doMo={0.45} doDay={3} />
        <DaiSongCuon y={606} bienDo={6.5} buocSong={210} tocDo={1.45} frame={frame} mau="#BAE6FD" doMo={0.5} doDay={3.5} />
        <DaiSongCuon y={652} bienDo={7.5} buocSong={240} tocDo={1.9} frame={frame} mau="#E0F2FE" doMo={0.42} doDay={4} />

        {/* Canh buom Hy Lap xa bobbing theo song */}
        <g transform={`translate(${thuyenX.toFixed(1)}, ${thuyenY.toFixed(1)}) rotate(${thuyenLac.toFixed(1)})`}>
          <path d="M -38 8 Q 0 22 42 8 L 30 20 L -28 20 Z" fill="#92400E" />
          <line x1={2} y1={10} x2={2} y2={-64} stroke="#78350F" strokeWidth={4} />
          <path d="M 4 -58 Q 42 -26 32 4 L 4 4 Z" fill="#FFFBEB" stroke="#E2E8F0" strokeWidth={2} />
          <path d="M -1 -48 Q -24 -20 -18 4 L -1 4 Z" fill="#FEF3C7" stroke="#E2E8F0" strokeWidth={1.5} />
        </g>

        <BoBienHyLapDenTinh />
      </g>

      {/* LOP 3 (Parallax 1.0x): San da vang am tien canh & cay o-liu tan la dung dua lech pha */}
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <BoBienHyLapSanTinh />

        {/* Bui co xanh ven bo da lac nhe */}
        <g>
          <ellipse cx={220 + duaLa2 * 0.25} cy={726} rx={78} ry={28} fill="#65A30D" />
          <ellipse cx={275 + duaLa1 * 0.2} cy={732} rx={56} ry={22} fill="#84CC16" />
          <ellipse cx={1670 + duaLa3 * 0.25} cy={712} rx={88} ry={30} fill="#4D7C0F" />
          <ellipse cx={1735 + duaLa2 * 0.2} cy={720} rx={68} ry={24} fill="#65A30D" />
        </g>

        {/* Cay o-liu co thu ben phai tien canh voi 3 cum tan la dung dua lech pha */}
        <g transform="translate(1780, 742)">
          <path d="M -24 20 Q -36 -110 -12 -220 Q 8 -260 44 -310 L 66 -294 Q 24 -220 18 -120 Q 16 -40 28 20 Z" fill="#78350F" />
          <path d="M -12 -180 Q -92 -236 -146 -272" fill="none" stroke="#78350F" strokeWidth={18} strokeLinecap="round" />

          <g transform={`translate(${duaLa1.toFixed(1)}, ${(duaLaY * 0.5).toFixed(1)})`}>
            <ellipse cx={-125} cy={-292} rx={115} ry={58} fill="#4D7C0F" />
            <circle cx={-120} cy={-278} r={6} fill="#365314" />
          </g>
          <g transform={`translate(${duaLa2.toFixed(1)}, ${(-duaLaY * 0.4).toFixed(1)})`}>
            <ellipse cx={-40} cy={-338} rx={128} ry={66} fill="#65A30D" />
            <circle cx={-56} cy={-315} r={6} fill="#365314" />
          </g>
          <g transform={`translate(${duaLa3.toFixed(1)}, ${(duaLaY * 0.6).toFixed(1)})`}>
            <ellipse cx={55} cy={-305} rx={108} ry={56} fill="#84CC16" />
            <ellipse cx={-72} cy={-268} rx={88} ry={44} fill="#84CC16" fillOpacity={0.85} />
            <circle cx={24} cy={-290} r={6} fill="#365314" />
          </g>
        </g>
      </g>
    </g>
  );
};

/** 2. Vuon tao dong que: parallax 3 lop, dan chim bay, tan cay tao dung dua lech pha & qua tao roi */
const VuonTaoDongQue: React.FC<{ frame: number; px: ParallaxOffset }> = ({
  frame,
  px,
}) => {
  const dua1 = Math.sin(frame * 0.065) * 4.8;
  const dua2 = Math.sin(frame * 0.078 + 1.3) * 4.2;
  const dua3 = Math.sin(frame * 0.058 + 2.5) * 5.2;

  const chuKyRoi = frame % 150;
  let taoX = 1455;
  let taoY = 472;
  if (chuKyRoi < 35) {
    taoX = 1455 + Math.sin(chuKyRoi * 0.9) * 4;
  } else if (chuKyRoi < 75) {
    const t = (chuKyRoi - 35) / 40;
    taoY = 472 + t * t * 265;
  } else {
    taoY = 737;
  }

  return (
    <g>
      <defs>
        <linearGradient id="vuonTroi" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#38BDF8" />
          <stop offset="65%" stopColor="#BAE6FD" />
          <stop offset="100%" stopColor="#FEF9C3" />
        </linearGradient>
        <linearGradient id="vuonCo" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#4ADE80" />
          <stop offset="100%" stopColor="#16A34A" />
        </linearGradient>
      </defs>

      {/* LOP 1 (Parallax 0.2x): Troi, tia nang, may & chim bay */}
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <rect x={-260} y={-120} width={2440} height={760} fill="url(#vuonTroi)" />
        <polygon points="150,-80 440,-80 760,720 420,720" fill="#FEF08A" fillOpacity={0.14} />
        <polygon points="540,-80 760,-80 1090,720 820,720" fill="#FEF08A" fillOpacity={0.1} />

        <CumMay xGoc={120} y={120} tiLe={1.3} tocDo={0.38} frame={frame} />
        <CumMay xGoc={780} y={90} tiLe={1.15} tocDo={0.28} frame={frame} />
        <CumMay xGoc={1380} y={150} tiLe={1.0} tocDo={0.34} frame={frame} />

        <ChimBay xGoc={310} yGoc={195} tocDo={1.2} tiLe={0.85} frame={frame} pha={0.7} mau="#0F172A" />
        <ChimBay xGoc={360} yGoc={172} tocDo={1.15} tiLe={0.72} frame={frame} pha={2.1} mau="#0F172A" />
      </g>

      {/* LOP 2 (Parallax 0.5x): Doi co nhieu tang & hang rao go */}
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        <path d="M -220 560 Q 340 430 720 510 Q 1120 580 1560 470 Q 1780 430 2140 480 L 2140 780 L -220 780 Z" fill="#86EFAC" />
        <path d="M -220 610 Q 480 510 960 585 Q 1440 650 2140 545 L 2140 820 L -220 820 Z" fill="#4ADE80" />

        <g transform="translate(0, 610)">
          <rect x={-40} y={32} width={1260} height={11} rx={4} fill="#B45309" />
          <rect x={-40} y={66} width={1260} height={11} rx={4} fill="#92400E" />
          {Array.from({ length: 14 }).map((_, i) => (
            <rect key={`rao-${i}`} x={-20 + i * 94} y={12} width={18} height={92} rx={4} fill="#D97706" stroke="#78350F" strokeWidth={2} />
          ))}
        </g>
      </g>

      {/* LOP 3 (Parallax 1.0x): Tham co, cay tao lon tan la lech pha & qua tao roi */}
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <path d="M -180 700 Q 540 676 1120 704 Q 1560 720 2100 694 L 2100 1180 L -180 1180 Z" fill="url(#vuonCo)" />
        <path d="M 180 1120 Q 540 870 960 780 Q 1280 730 1520 725 L 1590 732 Q 1280 760 1040 825 Q 720 920 520 1120 Z" fill="#E7D3B1" fillOpacity={0.75} />

        <g transform="translate(1540, 748)">
          <path d="M -42 18 Q -32 -140 -26 -290 L 28 -290 Q 22 -140 46 18 Z" fill="#78350F" />
          <path d="M -18 -240 Q -110 -300 -150 -340" fill="none" stroke="#78350F" strokeWidth={22} strokeLinecap="round" />

          <g transform={`translate(${dua1.toFixed(1)}, 0)`}>
            <circle cx={-125} cy={-355} r={108} fill="#15803D" />
            <circle cx={-55} cy={-315} r={96} fill="#22C55E" />
          </g>
          <g transform={`translate(${dua2.toFixed(1)}, 0)`}>
            <circle cx={0} cy={-410} r={136} fill="#16A34A" />
          </g>
          <g transform={`translate(${dua3.toFixed(1)}, 0)`}>
            <circle cx={120} cy={-355} r={112} fill="#22C55E" />
            <circle cx={68} cy={-312} r={92} fill="#4ADE80" fillOpacity={0.75} />
          </g>

          <g transform={`translate(${dua2.toFixed(1)}, 0)`}>
            {[
              [-145, -340],
              [-45, -420],
              [42, -370],
              [115, -330],
              [-25, -310],
            ].map(([ax, ay], idx) => (
              <g key={`tao-${idx}`} transform={`translate(${ax}, ${ay})`}>
                <circle cx={0} cy={0} r={14} fill="#EF4444" stroke="#991B1B" strokeWidth={2} />
                <ellipse cx={-4} cy={-4} rx={4} ry={2.5} fill="#FCA5A5" />
                <line x1={0} y1={-14} x2={2} y2={-21} stroke="#78350F" strokeWidth={2.5} />
              </g>
            ))}
          </g>
        </g>

        <g transform={`translate(${taoX.toFixed(1)}, ${taoY.toFixed(1)})`}>
          <circle cx={0} cy={0} r={15} fill="#DC2626" stroke="#7F1D1D" strokeWidth={2.2} />
          <ellipse cx={-4} cy={-4} rx={4.5} ry={2.6} fill="#FCA5A5" />
          <path d="M 0 -15 Q 7 -24 14 -20 Q 8 -14 0 -15 Z" fill="#22C55E" />
        </g>

        {[210, 390, 680, 1180, 1740].map((fx, i) => (
          <g key={`hoa-${i}`} transform={`translate(${fx + Math.sin(frame * 0.08 + i) * 2}, ${825 + (i % 3) * 32})`}>
            <circle cx={0} cy={0} r={6} fill={i % 2 === 0 ? '#FEF08A' : '#F472B6'} />
            <circle cx={0} cy={0} r={2.5} fill="#FFFFFF" />
          </g>
        ))}
      </g>
    </g>
  );
};

/** 3. Pho co chau Au: parallax 3 lop, song cuon, cau da vong, day nha mai nhon & den duong co */
const PhoCoChauAu: React.FC<{ frame: number; px: ParallaxOffset }> = ({
  frame,
  px,
}) => {
  const nhaMau = [
    { x: 40, w: 190, h: 320, mau: '#FDE68A', mai: '#B45309' },
    { x: 220, w: 170, h: 270, mau: '#FED7AA', mai: '#9A3412' },
    { x: 380, w: 205, h: 350, mau: '#E0E7FF', mai: '#4338CA' },
    { x: 1320, w: 195, h: 330, mau: '#FECDD3', mai: '#9F1239' },
    { x: 1505, w: 185, h: 280, mau: '#FEF3C7', mai: '#B45309' },
    { x: 1680, w: 210, h: 345, mau: '#D1FAE5', mai: '#047857' },
  ];

  return (
    <g>
      <defs>
        <linearGradient id="phoTroi" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#60A5FA" />
          <stop offset="65%" stopColor="#BFDBFE" />
          <stop offset="100%" stopColor="#FEF3C7" />
        </linearGradient>
        <linearGradient id="phoSong" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#38BDF8" />
          <stop offset="100%" stopColor="#0284C7" />
        </linearGradient>
      </defs>

      {/* LOP 1 (0.2x): Troi, may & chim */}
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <rect x={-260} y={-120} width={2440} height={740} fill="url(#phoTroi)" />
        <CumMay xGoc={320} y={115} tiLe={1.15} tocDo={0.32} frame={frame} />
        <CumMay xGoc={1060} y={140} tiLe={1.0} tocDo={0.26} frame={frame} />
        <ChimBay xGoc={640} yGoc={190} tocDo={1.25} tiLe={0.8} frame={frame} pha={1.1} mau="#1E293B" />
      </g>

      {/* LOP 2 (0.5x): Dong song cuon muot, cau da & day nha */}
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        <rect x={-260} y={560} width={2440} height={195} fill="url(#phoSong)" />
        <DaiSongCuon y={605} bienDo={4} buocSong={150} tocDo={1.1} frame={frame} mau="#E0F2FE" doMo={0.48} doDay={3} />
        <DaiSongCuon y={648} bienDo={5} buocSong={180} tocDo={1.4} frame={frame} mau="#BAE6FD" doMo={0.44} doDay={3.2} />

        <g transform="translate(560, 495)">
          <path
            d="M 0 110 L 0 28 Q 400 -24 800 28 L 800 110 L 710 110 A 90 66 0 0 0 530 110 L 490 110 A 90 66 0 0 0 310 110 L 270 110 A 90 66 0 0 0 90 110 Z"
            fill="#CBD5E1"
            stroke="#64748B"
            strokeWidth={4}
          />
          <path d="M 0 28 Q 400 -24 800 28" fill="none" stroke="#94A3B8" strokeWidth={10} />
        </g>

        {nhaMau.map((n, idx) => {
          const topY = 635 - n.h;
          return (
            <g key={`nha-${idx}`}>
              <rect x={n.x} y={topY} width={n.w} height={n.h} fill={n.mau} stroke="#475569" strokeWidth={3} />
              <polygon
                points={`${n.x - 14},${topY} ${n.x + n.w / 2},${topY - 92} ${n.x + n.w + 14},${topY}`}
                fill={n.mai}
                stroke="#1E293B"
                strokeWidth={3}
                strokeLinejoin="round"
              />
              {[0, 1, 2].map((r) =>
                [0, 1].map((c) => (
                  <rect
                    key={`cs-${idx}-${r}-${c}`}
                    x={n.x + 28 + c * (n.w - 92)}
                    y={topY + 34 + r * 72}
                    width={36}
                    height={46}
                    rx={4}
                    fill="#FEF9C3"
                    stroke="#64748B"
                    strokeWidth={2.5}
                  />
                )),
              )}
            </g>
          );
        })}
      </g>

      {/* LOP 3 (1.0x): Duong lat da & den duong co */}
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <rect x={-180} y={695} width={2280} height={460} fill="#94A3B8" />
        <rect x={-180} y={688} width={2280} height={18} fill="#CBD5E1" stroke="#64748B" strokeWidth={2} />
        {Array.from({ length: 16 }).map((_, i) => (
          <rect
            key={`gach-${i}`}
            x={40 + i * 120 + (i % 2) * 24}
            y={748 + (i % 3) * 42}
            width={76}
            height={22}
            rx={8}
            fill="#64748B"
            fillOpacity={0.32}
          />
        ))}

        {[290, 1630].map((lx) => (
          <g key={`den-${lx}`} transform={`translate(${lx}, 696)`}>
            <rect x={-7} y={-255} width={14} height={255} fill="#1E293B" />
            <path d="M -18 0 L 18 0 L 12 -32 L -12 -32 Z" fill="#334155" />
            <circle cx={0} cy={-268} r={44} fill="#FEF08A" fillOpacity={0.18 + 0.05 * Math.sin(frame * 0.14)} />
            <polygon points="-18,-252 18,-252 24,-284 -24,-284" fill="#FEF08A" stroke="#1E293B" strokeWidth={3} />
            <polygon points="-26,-284 26,-284 0,-304" fill="#1E293B" />
          </g>
        ))}
      </g>
    </g>
  );
};

/** 4. Rung nui thien nhien: parallax 3 lop, dan chim vo canh, thong dung dua lech pha & suoi uon luon */
const RungNuiThienNhien: React.FC<{ frame: number; px: ParallaxOffset }> = ({
  frame,
  px,
}) => {
  const veThong = (x: number, y: number, tiLe: number, mau: string, idx: number) => {
    const dua1 = Math.sin(frame * 0.055 + idx * 1.1) * 3.8;
    const dua2 = Math.sin(frame * 0.055 + idx * 1.1 - 0.6) * 2.4;
    const dua3 = Math.sin(frame * 0.055 + idx * 1.1 - 1.2) * 1.4;
    return (
      <g key={`thong-${idx}`} transform={`translate(${x}, ${y}) scale(${tiLe})`}>
        <rect x={-7} y={-28} width={14} height={36} fill="#5C3A21" />
        <polygon points={`${dua1.toFixed(1)},-125 -42,-58 42,-58`} fill={mau} />
        <polygon points={`${dua2.toFixed(1)},-92 -52,-26 52,-26`} fill={mau} />
        <polygon points={`${dua3.toFixed(1)},-56 -60,2 60,2`} fill={mau} />
      </g>
    );
  };

  return (
    <g>
      <defs>
        <linearGradient id="nuiTroi" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#0284C7" />
          <stop offset="55%" stopColor="#7DD3FC" />
          <stop offset="100%" stopColor="#E0F2FE" />
        </linearGradient>
        <linearGradient id="nuiCo" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#22C55E" />
          <stop offset="100%" stopColor="#14532D" />
        </linearGradient>
      </defs>

      {/* LOP 1 (0.2x): Bau troi, may & dan chim bay */}
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <rect x={-260} y={-120} width={2440} height={740} fill="url(#nuiTroi)" />
        <CumMay xGoc={220} y={110} tiLe={1.25} tocDo={0.3} frame={frame} />
        <CumMay xGoc={1120} y={145} tiLe={1.1} tocDo={0.22} frame={frame} />
        {[0, 1, 2, 3, 4].map((i) => (
          <ChimBay
            key={`chim-nui-${i}`}
            xGoc={320 + i * 52}
            yGoc={210 + (i % 2) * 26}
            tocDo={1.45}
            tiLe={0.85 - i * 0.06}
            frame={frame}
            pha={i * 0.9}
            mau="#0F172A"
          />
        ))}
      </g>

      {/* LOP 2 (0.5x): Day nui tuyet & rung thong trung canh */}
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        <polygon points="-220,560 280,260 590,480 920,210 1280,450 1620,235 2140,440 2140,700 -220,700" fill="#64748B" fillOpacity={0.55} />
        <polygon points="920,210 854,282 900,268 925,294 958,268 986,282" fill="#F8FAFC" />
        <polygon points="1620,235 1564,296 1605,284 1628,308 1660,285 1684,298" fill="#F8FAFC" />

        <path d="M -220 600 Q 320 430 680 540 Q 1080 620 1480 465 Q 1740 410 2140 515 L 2140 780 L -220 780 Z" fill="#15803D" />
        <path d="M -220 655 Q 480 565 960 635 Q 1460 700 2140 605 L 2140 840 L -220 840 Z" fill="#16A34A" />

        {[120, 260, 410, 1460, 1610, 1770].map((tx, idx) =>
          veThong(tx, 645 + (idx % 2) * 22, 1.15 + (idx % 3) * 0.14, '#14532D', idx),
        )}
      </g>

      {/* LOP 3 (1.0x): Tham co, suoi chay lap lanh & thong tien canh */}
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <path d="M -180 702 Q 620 680 1260 708 Q 1640 722 2100 698 L 2100 1180 L -180 1180 Z" fill="url(#nuiCo)" />

        <path
          d="M 1020 696 Q 940 770 1120 845 Q 1260 910 1040 1120 L 1220 1120 Q 1410 920 1220 830 Q 1040 755 1095 696 Z"
          fill="#38BDF8"
          stroke="#BAE6FD"
          strokeWidth={4}
        />
        {[0, 1, 2, 3, 4].map((i) => {
          const py = 720 + ((i * 68 + frame * 1.6) % 340);
          const pxSuoi = 1120 + Math.sin(py * 0.025) * 65;
          return (
            <path
              key={`suoi-${i}`}
              d={`M ${pxSuoi - 22} ${py} Q ${pxSuoi} ${py - 4} ${pxSuoi + 22} ${py}`}
              fill="none"
              stroke="#FFFFFF"
              strokeOpacity={0.72}
              strokeWidth={3}
              strokeLinecap="round"
            />
          );
        })}

        {veThong(76, 770, 1.55, '#0F3D22', 10)}
        {veThong(1845, 765, 1.5, '#0F3D22', 11)}
      </g>
    </g>
  );
};

/** Nen tinh (React.memo) cho ThuVienCoDien: ke sach nhieu chi tiet khong re-render moi frame */
const KeSachThuVienCoDienTinh = React.memo(() => {
  const mauSach = ['#DC2626', '#2563EB', '#15803D', '#D97706', '#7C3AED', '#0F766E'];
  const veKeSach = (x0: number) => (
    <g key={`ke-${x0}`}>
      <rect x={x0} y={90} width={420} height={630} rx={8} fill="#451A03" stroke="#78350F" strokeWidth={6} />
      {[0, 1, 2, 3].map((tang) => {
        const y = 118 + tang * 145;
        return (
          <g key={`tang-${x0}-${tang}`}>
            <rect x={x0 + 16} y={y} width={388} height={118} fill="#291205" />
            {Array.from({ length: 12 }).map((_, bi) => {
              const bw = 24 + Math.floor(bamTatDinh(x0 + tang * 17 + bi * 13) * 12);
              const bh = 74 + Math.floor(bamTatDinh(x0 + tang * 23 + bi * 7) * 36);
              const bx = x0 + 22 + bi * 31;
              const mau = mauSach[(tang * 5 + bi) % mauSach.length];
              return (
                <rect
                  key={`sach-${bi}`}
                  x={bx}
                  y={y + 118 - bh}
                  width={Math.min(bw, 29)}
                  height={bh}
                  rx={3}
                  fill={mau}
                  stroke="#1C1917"
                  strokeWidth={1.6}
                />
              );
            })}
            <rect x={x0 + 10} y={y + 118} width={400} height={14} fill="#78350F" />
          </g>
        );
      })}
    </g>
  );
  return (
    <g>
      {veKeSach(120)}
      {veKeSach(1380)}
    </g>
  );
});

/** 5. Thu vien co dien: parallax 3 lop (troi ngoai cua so 0.2x, gia sach 0.5x, san & ban go 1.0x) */
const ThuVienCoDien: React.FC<{ frame: number; px: ParallaxOffset }> = ({
  frame,
  px,
}) => {
  const ngonNen = Math.sin(frame * 0.28) * 3;

  return (
    <g>
      <defs>
        <linearGradient id="tvTuong" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#78350F" />
          <stop offset="100%" stopColor="#451A03" />
        </linearGradient>
        <linearGradient id="tvCuaSo" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#38BDF8" />
          <stop offset="100%" stopColor="#FEF3C7" />
        </linearGradient>
      </defs>

      {/* LOP 1 + 2 (Parallax nhe): Tuong go, cua so vom troi may & 2 gia sach */}
      <g transform={`translate(${(px.lop2X * 0.65).toFixed(1)}, ${(px.lop2Y * 0.5).toFixed(1)})`}>
        <rect x={-240} y={-120} width={2400} height={880} fill="url(#tvTuong)" />
        <g transform="translate(690, 95)">
          <path d="M 0 540 L 0 210 A 270 210 0 0 1 540 210 L 540 540 Z" fill="url(#tvCuaSo)" stroke="#92400E" strokeWidth={16} />
          <clipPath id="clipCuaSoTv">
            <path d="M 8 532 L 8 210 A 262 202 0 0 1 532 210 L 532 532 Z" />
          </clipPath>
          <g clipPath="url(#clipCuaSoTv)" transform={`translate(${(px.lop1X * 0.35).toFixed(1)}, 0)`}>
            <CumMay xGoc={60} y={145} tiLe={0.78} tocDo={0.35} frame={frame} />
            <CumMay xGoc={320} y={240} tiLe={0.65} tocDo={0.25} frame={frame} />
          </g>
          <line x1={270} y1={10} x2={270} y2={540} stroke="#92400E" strokeWidth={10} />
          <line x1={8} y1={240} x2={532} y2={240} stroke="#92400E" strokeWidth={10} />
          <line x1={8} y1={390} x2={532} y2={390} stroke="#92400E" strokeWidth={10} />
        </g>

        <KeSachThuVienCoDienTinh />
      </g>

      {/* LOP 3 (1.0x): San go & ban lam viec */}
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <rect x={-180} y={712} width={2280} height={450} fill="#92400E" />
        <rect x={-180} y={712} width={2280} height={14} fill="#B45309" />
        {[780, 855, 935, 1020].map((ly) => (
          <line key={`san-${ly}`} x1={-180} y1={ly} x2={2100} y2={ly} stroke="#78350F" strokeWidth={3} />
        ))}

        <g transform="translate(1485, 675)">
          <rect x={-165} y={18} width={330} height={24} rx={6} fill="#B45309" stroke="#451A03" strokeWidth={4} />
          <rect x={-135} y={42} width={22} height={115} fill="#78350F" />
          <rect x={113} y={42} width={22} height={115} fill="#78350F" />
          <g transform="translate(-75, -36)">
            <circle cx={0} cy={0} r={34} fill="#38BDF8" stroke="#1E3A8A" strokeWidth={3} />
            <path d="M -18 -14 Q -4 -20 12 -8 Q 18 6 2 16 Q -14 14 -18 -14 Z" fill="#4ADE80" />
            <path d="M -42 0 A 42 42 0 0 0 42 0" fill="none" stroke="#D97706" strokeWidth={5} />
            <line x1={0} y1={42} x2={0} y2={54} stroke="#D97706" strokeWidth={6} />
            <rect x={-24} y={50} width={48} height={8} rx={4} fill="#B45309" />
          </g>
          <g transform="translate(76, -10)">
            <rect x={-10} y={-24} width={20} height={50} rx={4} fill="#FEF3C7" stroke="#D97706" strokeWidth={2} />
            <circle cx={0} cy={-44} r={44 + ngonNen * 1.4} fill="#FACC15" fillOpacity={0.16} />
            <circle cx={0} cy={-44} r={24 + ngonNen * 0.8} fill="#FDE047" fillOpacity={0.28} />
            <path
              d={`M 0 ${(-62 + ngonNen).toFixed(1)} Q 11 -44 0 -32 Q -11 -44 0 ${(-62 + ngonNen).toFixed(1)} Z`}
              fill="#F97316"
            />
            <path
              d={`M 0 ${(-54 + ngonNen * 0.6).toFixed(1)} Q 5 -43 0 -35 Q -5 -43 0 ${(-54 + ngonNen * 0.6).toFixed(1)} Z`}
              fill="#FEF08A"
            />
          </g>
        </g>
      </g>
    </g>
  );
};

/** Nen tinh (React.memo) cho LopHocBangXanh & ThuVienTrungCo & QuangTruongHyLap */
const LopHocBangXanhNenTinh = React.memo(() => (
  <g>
    <rect x={-200} y={-100} width={2320} height={860} fill="url(#lopTuong)" />
    <rect x={-200} y={645} width={2320} height={100} fill="#E7D3B1" />
    <rect x={-200} y={638} width={2320} height={14} fill="#C29B61" />
    <polygon points="0,40 240,40 520,745 0,745" fill="#FEF08A" fillOpacity={0.18} />
    <rect x={545} y={76} width={1320} height={588} rx={16} fill="#14532D" stroke="#92400E" strokeWidth={16} />
    <rect x={562} y={93} width={1286} height={554} rx={8} fill="#114226" />
    <rect x={530} y={658} width={1350} height={22} rx={6} fill="#B45309" stroke="#78350F" strokeWidth={3} />
    <rect x={630} y={646} width={44} height={12} rx={4} fill="#F8FAFC" />
    <rect x={686} y={646} width={36} height={12} rx={4} fill="#FEF08A" />
    <rect x={734} y={646} width={36} height={12} rx={4} fill="#7DD3FC" />
    <rect x={1690} y={636} width={78} height={22} rx={5} fill="#78350F" />
    <rect x={1696} y={630} width={66} height={10} rx={3} fill="#D97706" />
    <g transform="translate(155, 165)">
      <circle cx={0} cy={0} r={54} fill="#FFFFFF" stroke="#92400E" strokeWidth={7} />
      {[0, 3, 6, 9].map((h) => {
        const g = (h / 12) * Math.PI * 2 - Math.PI / 2;
        return <circle key={`gio-${h}`} cx={Math.cos(g) * 40} cy={Math.sin(g) * 40} r={3.5} fill="#334155" />;
      })}
      <line x1={0} y1={0} x2={0} y2={-28} stroke="#1E293B" strokeWidth={4} strokeLinecap="round" />
      <line x1={0} y1={0} x2={22} y2={8} stroke="#DC2626" strokeWidth={3} strokeLinecap="round" />
      <circle cx={0} cy={0} r={4.5} fill="#1E293B" />
    </g>
    <g transform="translate(340, 128) rotate(8)" opacity={0.85}>
      <polygon points="0,0 130,0 0,92" fill="#FDE68A" stroke="#B45309" strokeWidth={4} strokeLinejoin="round" />
      <polygon points="18,16 82,16 18,62" fill="#FEFCE8" stroke="#B45309" strokeWidth={2.5} strokeLinejoin="round" />
    </g>
  </g>
));

/** 6. Lop hoc bang xanh: sang sua am ap, bang xanh lon vien go, toi uu doc cong thuc Toan */
const LopHocBangXanh: React.FC<{ frame: number; px: ParallaxOffset }> = ({
  frame,
  px,
}) => {
  const buiNang = Math.sin(frame * 0.08) * 6;
  return (
    <g>
      <defs>
        <linearGradient id="lopTuong" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#FEFCE8" />
          <stop offset="100%" stopColor="#FEF3C7" />
        </linearGradient>
        <linearGradient id="lopSan" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#D97706" />
          <stop offset="100%" stopColor="#92400E" />
        </linearGradient>
      </defs>

      <g transform={`translate(${(px.lop2X * 0.4).toFixed(1)}, ${(px.lop2Y * 0.35).toFixed(1)})`}>
        <LopHocBangXanhNenTinh />
        <circle cx={190 + buiNang} cy={220} r={4} fill="#FFFFFF" fillOpacity={0.65} />
        <circle cx={270 - buiNang} cy={350} r={3} fill="#FFFFFF" fillOpacity={0.55} />
      </g>

      <rect x={-180} y={745} width={2280} height={420} fill="url(#lopSan)" />
      {[815, 895, 980].map((sy) => (
        <line key={`lsan-${sy}`} x1={-180} y1={sy} x2={2100} y2={sy} stroke="#78350F" strokeOpacity={0.45} strokeWidth={3} />
      ))}
    </g>
  );
};

/** 7. Bau troi dem vu tru: parallax 3 lop (sao xa 0.2x, chom sao & trang 0.5x, doi dem 1.0x) */
const BauTroiDemVuTru: React.FC<{ frame: number; px: ParallaxOffset }> = ({
  frame,
  px,
}) => {
  const chomSao = [
    [240, 220],
    [390, 165],
    [540, 240],
    [690, 185],
    [830, 265],
  ];
  const chomSao2 = [
    [1180, 190],
    [1320, 140],
    [1460, 225],
    [1365, 315],
  ];

  const phaSaoBang = frame % 110;
  const hienSaoBang = phaSaoBang >= 18 && phaSaoBang <= 44;
  const tSb = (phaSaoBang - 18) / 26;
  const sbX = 1520 - tSb * 760;
  const sbY = 95 + tSb * 260;

  return (
    <g>
      <defs>
        <linearGradient id="demTroi" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#0B1120" />
          <stop offset="55%" stopColor="#1E1B4B" />
          <stop offset="100%" stopColor="#312E81" />
        </linearGradient>
      </defs>

      {/* LOP 1 (0.2x): Nen dem & 48 ngoi sao */}
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <rect x={-260} y={-120} width={2440} height={1320} fill="url(#demTroi)" />
        {Array.from({ length: 48 }).map((_, i) => {
          const sx = -100 + bamTatDinh(i * 19 + 3) * 2120;
          const sy = 40 + bamTatDinh(i * 31 + 7) * 620;
          const r = 1.6 + bamTatDinh(i * 11 + 5) * 2.6;
          const op = 0.45 + 0.55 * Math.abs(Math.sin(frame * 0.08 + i * 1.3));
          return <circle key={`sao-${i}`} cx={sx} cy={sy} r={r} fill="#FEF9C3" fillOpacity={op} />;
        })}
      </g>

      {/* LOP 2 (0.5x): Chom sao, mat trang & sao bang */}
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        <polyline
          points={chomSao.map(([x, y]) => `${x},${y}`).join(' ')}
          fill="none"
          stroke="#7DD3FC"
          strokeOpacity={0.48}
          strokeWidth={2.5}
          strokeDasharray="8 6"
        />
        {chomSao.map(([x, y], i) => (
          <g key={`cs1-${i}`}>
            <circle cx={x} cy={y} r={9} fill="#38BDF8" fillOpacity={0.25} />
            <circle cx={x} cy={y} r={4} fill="#FFFFFF" />
          </g>
        ))}

        <polygon
          points={chomSao2.map(([x, y]) => `${x},${y}`).join(' ')}
          fill="#A78BFA"
          fillOpacity={0.08}
          stroke="#C4B5FD"
          strokeOpacity={0.5}
          strokeWidth={2.5}
        />
        {chomSao2.map(([x, y], i) => (
          <circle key={`cs2-${i}`} cx={x} cy={y} r={4.2} fill="#FEF08A" />
        ))}

        <g transform="translate(1660, 195)">
          <circle cx={0} cy={0} r={96} fill="#FEF08A" fillOpacity={0.12} />
          <path d="M 24 -56 A 62 62 0 1 0 24 56 A 48 48 0 1 1 24 -56 Z" fill="#FEF08A" />
        </g>

        {hienSaoBang && (
          <g opacity={Math.sin(tSb * Math.PI)}>
            <line x1={sbX} y1={sbY} x2={sbX + 165} y2={sbY - 56} stroke="#FEF08A" strokeWidth={4} strokeLinecap="round" />
            <line x1={sbX} y1={sbY} x2={sbX + 95} y2={sbY - 32} stroke="#FFFFFF" strokeWidth={2.5} strokeLinecap="round" />
            <circle cx={sbX} cy={sbY} r={5} fill="#FFFFFF" />
          </g>
        )}
      </g>

      {/* LOP 3 (1.0x): Doi dem tien canh */}
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <path d="M -180 740 Q 480 650 960 720 Q 1480 780 2100 690 L 2100 1180 L -180 1180 Z" fill="#1E293B" />
        <path d="M -180 800 Q 520 740 1080 785 Q 1540 820 2100 760 L 2100 1180 L -180 1180 Z" fill="#0F172A" />
      </g>
    </g>
  );
};

/** 8. Phong nen hai huoc: pastel/giay kraft toi gian kem sunburst & parallax nhe */
const PhongNenHaiHuoc: React.FC<{ frame: number; px: ParallaxOffset }> = ({
  frame,
  px,
}) => {
  const xoay = frame * 0.35;
  return (
    <g>
      <defs>
        <radialGradient id="haiNen" cx="50%" cy="50%" r="72%">
          <stop offset="0%" stopColor="#FFFBEB" />
          <stop offset="68%" stopColor="#FEF3C7" />
          <stop offset="100%" stopColor="#FDE68A" />
        </radialGradient>
      </defs>

      <rect x={-260} y={-140} width={2440} height={1360} fill="url(#haiNen)" />

      <g transform={`translate(${(960 + px.lop2X * 0.6).toFixed(1)}, ${(540 + px.lop2Y * 0.6).toFixed(1)}) rotate(${xoay.toFixed(2)})`} opacity={0.28}>
        {Array.from({ length: 18 }).map((_, i) => {
          const a1 = (i / 18) * Math.PI * 2;
          const a2 = ((i + 0.45) / 18) * Math.PI * 2;
          const r = 1450;
          return (
            <polygon
              key={`tia-${i}`}
              points={`0,0 ${(Math.cos(a1) * r).toFixed(1)},${(Math.sin(a1) * r).toFixed(1)} ${(Math.cos(a2) * r).toFixed(1)},${(Math.sin(a2) * r).toFixed(1)}`}
              fill="#F59E0B"
            />
          );
        })}
      </g>

      <g transform={`translate(${(px.lop2X * 0.35).toFixed(1)}, ${(px.lop2Y * 0.35).toFixed(1)})`}>
        {[
          [110, 140],
          [165, 110],
          [1810, 140],
          [1755, 110],
          [120, 910],
          [1800, 910],
        ].map(([dx, dy], idx) => (
          <circle key={`dot-${idx}`} cx={dx} cy={dy} r={12 + (idx % 2) * 5} fill="#FB923C" fillOpacity={0.28} />
        ))}
      </g>

      <ellipse cx={960} cy={805} rx={680} ry={62} fill="#F59E0B" fillOpacity={0.14} />
      <line x1={260} y1={805} x2={1660} y2={805} stroke="#D97706" strokeOpacity={0.35} strokeWidth={4} strokeDasharray="16 14" strokeLinecap="round" />
    </g>
  );
};

/** 9. Quang truong & Den Hy Lap co dai (Agora / Acropolis): parallax 3 lop (0.2x / 0.5x / 1.0x) */
const QuangTruongHyLap: React.FC<{ frame: number; px: ParallaxOffset }> = ({
  frame,
  px,
}) => {
  const duaLa = Math.sin(frame * 0.065) * 4.5;
  return (
    <g>
      <defs>
        <linearGradient id="agoraTroi" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#0284C7" />
          <stop offset="55%" stopColor="#7DD3FC" />
          <stop offset="100%" stopColor="#FEF3C7" />
        </linearGradient>
        <linearGradient id="agoraSan" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#F5E6CA" />
          <stop offset="100%" stopColor="#D6BE96" />
        </linearGradient>
      </defs>

      {/* LOP 1 (0.2x): Troi xanh Dia Trung Hai, mat troi trai, may & chim */}
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <rect x={-260} y={-120} width={2440} height={740} fill="url(#agoraTroi)" />
        <g transform="translate(520, 175)">
          <circle cx={0} cy={0} r={130 + Math.sin(frame * 0.05) * 4} fill="#FEF08A" fillOpacity={0.16} />
          <circle cx={0} cy={0} r={82} fill="#FEF9C3" fillOpacity={0.28} />
          <circle cx={0} cy={0} r={52} fill="#FFFBEB" />
        </g>
        <CumMay xGoc={140} y={135} tiLe={1.25} tocDo={0.35} frame={frame} />
        <CumMay xGoc={960} y={96} tiLe={1.08} tocDo={0.25} frame={frame} />
        <ChimBay xGoc={380} yGoc={215} tocDo={1.3} tiLe={0.88} frame={frame} pha={0.6} mau="#0C4A6E" />
        <ChimBay xGoc={435} yGoc={190} tocDo={1.22} tiLe={0.75} frame={frame} pha={1.9} mau="#0C4A6E" />
      </g>

      {/* LOP 2 (0.5x): Doi Acropolis, den Parthenon hung vi & hang cay bach */}
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        <path d="M -220 560 Q 320 420 760 470 Q 1240 510 1620 430 Q 1860 390 2140 470 L 2140 760 L -220 760 Z" fill="#CBD5E1" />
        <path d="M -220 605 Q 480 510 1040 555 Q 1520 590 2140 520 L 2140 780 L -220 780 Z" fill="#94A3B8" fillOpacity={0.55} />

        {/* Den Parthenon trung tam lech phai */}
        <g transform="translate(860, 235)">
          <polygon points="-24,62 290,-18 604,62" fill="#F8FAFC" stroke="#94A3B8" strokeWidth={5} strokeLinejoin="round" />
          <polygon points="36,52 290,4 544,52" fill="#E2E8F0" />
          <rect x={-12} y={62} width={604} height={24} fill="#E2E8F0" stroke="#94A3B8" strokeWidth={3} />
          {[22, 114, 206, 298, 390, 482].map((cx) => (
            <g key={`ag-cot-${cx}`}>
              <rect x={cx - 8} y={86} width={44} height={12} rx={2} fill="#F1F5F9" stroke="#94A3B8" strokeWidth={2} />
              <rect x={cx} y={98} width={28} height={206} fill="#FFFDF7" stroke="#CBD5E1" strokeWidth={2.5} />
              <line x1={cx + 9} y1={100} x2={cx + 9} y2={302} stroke="#E2E8F0" strokeWidth={2} />
              <line x1={cx + 19} y1={100} x2={cx + 19} y2={302} stroke="#E2E8F0" strokeWidth={2} />
            </g>
          ))}
          <rect x={-26} y={304} width={632} height={18} fill="#E2E8F0" stroke="#94A3B8" strokeWidth={2} />
          <rect x={-42} y={322} width={664} height={20} fill="#CBD5E1" stroke="#94A3B8" strokeWidth={2} />
        </g>

        {/* Hang cay bach Dia Trung Hai */}
        {[170, 255, 620, 1610, 1715].map((tx, idx) => (
          <g key={`bach-${idx}`} transform={`translate(${tx}, 580)`}>
            <rect x={-6} y={-20} width={12} height={36} fill="#78350F" />
            <ellipse cx={duaLa * 0.25} cy={-95} rx={24} ry={82} fill={idx % 2 === 0 ? '#15803D' : '#166534'} />
          </g>
        ))}
      </g>

      {/* LOP 3 (1.0x): Quang truong lat da cam thach, hang cot tien canh trai & chau cay o-liu */}
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <rect x={-180} y={678} width={2280} height={480} fill="url(#agoraSan)" />
        <rect x={-180} y={670} width={2280} height={18} fill="#FFFBEB" stroke="#C2A378" strokeWidth={3} />
        {[745, 825, 915, 1010].map((ly) => (
          <line key={`ag-l-${ly}`} x1={-180} y1={ly} x2={2100} y2={ly} stroke="#C2A378" strokeOpacity={0.5} strokeWidth={2.5} />
        ))}
        {[-60, 220, 520, 820, 1120, 1420, 1720, 1980].map((gx, i) => (
          <line key={`ag-v-${i}`} x1={gx} y1={688} x2={gx - 120 + i * 32} y2={1120} stroke="#C2A378" strokeOpacity={0.35} strokeWidth={2.5} />
        ))}

        {/* Cot da tien canh trai */}
        <g transform="translate(82, 220)">
          <rect x={-14} y={0} width={92} height={24} rx={4} fill="#F1F5F9" stroke="#94A3B8" strokeWidth={3} />
          <rect x={0} y={24} width={64} height={476} fill="#FFFDF7" stroke="#CBD5E1" strokeWidth={3} />
          <line x1={20} y1={28} x2={20} y2={494} stroke="#E2E8F0" strokeWidth={3} />
          <line x1={44} y1={28} x2={44} y2={494} stroke="#E2E8F0" strokeWidth={3} />
          <rect x={-16} y={498} width={96} height={28} rx={4} fill="#E2E8F0" stroke="#94A3B8" strokeWidth={3} />
        </g>

        {/* Chau gom co & nhanh o-liu ben phai */}
        <g transform="translate(1785, 720)">
          <path d="M -38 0 L 38 0 L 52 -58 L -52 -58 Z" fill="#C2410C" stroke="#7C2D12" strokeWidth={3.5} />
          <rect x={-58} y={-70} width={116} height={14} rx={5} fill="#EA580C" stroke="#7C2D12" strokeWidth={3} />
          <g transform={`translate(${duaLa.toFixed(1)}, 0)`}>
            <ellipse cx={-28} cy={-112} rx={46} ry={34} fill="#4D7C0F" />
            <ellipse cx={26} cy={-118} rx={48} ry={36} fill="#65A30D" />
            <ellipse cx={0} cy={-148} rx={44} ry={32} fill="#84CC16" />
          </g>
        </g>
      </g>
    </g>
  );
};

/** 10. Thu vien Trung Co (Scriptorium / Gothic): parallax 3 lop (troi cua so kinh mau 0.2x, vom da & gia cuon giay 0.5x, san da & buc doc sach 1.0x) */
const ThuVienTrungCo: React.FC<{ frame: number; px: ParallaxOffset }> = ({
  frame,
  px,
}) => {
  const rungNen = Math.sin(frame * 0.26) * 2.5;
  return (
    <g>
      <defs>
        <linearGradient id="tcTuong" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#334155" />
          <stop offset="100%" stopColor="#1E293B" />
        </linearGradient>
        <linearGradient id="tcKinh" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#38BDF8" />
          <stop offset="50%" stopColor="#A855F7" />
          <stop offset="100%" stopColor="#F59E0B" />
        </linearGradient>
      </defs>

      {/* LOP 1 (0.2x): Bau troi & tia sang sau cua so kinh mau Gothic */}
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <rect x={-260} y={-120} width={2440} height={880} fill="url(#tcTuong)" />
        {[680, 960, 1240].map((wx, wi) => (
          <g key={`tc-win-${wi}`} transform={`translate(${wx}, 115)`}>
            <path d="M -85 430 L -85 120 Q -85 20 0 -20 Q 85 20 85 120 L 85 430 Z" fill="url(#tcKinh)" fillOpacity={0.82} stroke="#0F172A" strokeWidth={10} />
            <circle cx={0} cy={78} r={34} fill="#FEF08A" fillOpacity={0.55} stroke="#1E293B" strokeWidth={5} />
            <line x1={0} y1={-10} x2={0} y2={430} stroke="#1E293B" strokeWidth={6} />
            <line x1={-82} y1={190} x2={82} y2={190} stroke="#1E293B" strokeWidth={6} />
            <line x1={-82} y1={310} x2={82} y2={310} stroke="#1E293B" strokeWidth={6} />
          </g>
        ))}
      </g>

      {/* LOP 2 (0.5x): Vom da Gothic, ke cuon giay da & den chum nen sat */}
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        {/* 2 ke cuon giay da ben trai va phai */}
        {[90, 1460].map((kx) => (
          <g key={`tc-ke-${kx}`}>
            <rect x={kx} y={130} width={360} height={585} rx={8} fill="#3F1D0B" stroke="#78350F" strokeWidth={7} />
            {[0, 1, 2, 3].map((tang) => {
              const ty = 158 + tang * 135;
              return (
                <g key={`tc-t-${kx}-${tang}`}>
                  <rect x={kx + 18} y={ty} width={324} height={106} fill="#231006" />
                  {Array.from({ length: 8 }).map((_, si) => {
                    const laCuon = bamTatDinh(kx + tang * 19 + si * 11) > 0.45;
                    const sx = kx + 28 + si * 39;
                    return laCuon ? (
                      <g key={`sc-${si}`} transform={`translate(${sx + 14}, ${ty + 54})`}>
                        <rect x={-12} y={-36} width={24} height={74} rx={6} fill="#FEF3C7" stroke="#B45309" strokeWidth={2} />
                        <line x1={-12} y1={0} x2={12} y2={0} stroke="#DC2626" strokeWidth={4} />
                      </g>
                    ) : (
                      <rect
                        key={`bk-${si}`}
                        x={sx}
                        y={ty + 18}
                        width={28}
                        height={88}
                        rx={3}
                        fill={si % 2 === 0 ? '#7C2D12' : '#1E3A8A'}
                        stroke="#F59E0B"
                        strokeWidth={1.6}
                      />
                    );
                  })}
                  <rect x={kx + 10} y={ty + 106} width={340} height={12} fill="#78350F" />
                </g>
              );
            })}
          </g>
        ))}

        {/* Den chum sat ren treo giua tran nha */}
        <g transform="translate(960, 118)">
          <line x1={0} y1={-140} x2={0} y2={48} stroke="#0F172A" strokeWidth={8} />
          <ellipse cx={0} cy={52} rx={155} ry={18} fill="none" stroke="#1E293B" strokeWidth={10} />
          {[-130, -45, 45, 130].map((nx, ni) => (
            <g key={`tc-nen-${ni}`} transform={`translate(${nx}, 42)`}>
              <rect x={-7} y={-24} width={14} height={28} rx={3} fill="#FEF3C7" />
              <circle cx={0} cy={-38} r={28 + rungNen * 1.2} fill="#FACC15" fillOpacity={0.18} />
              <path d={`M 0 ${(-50 + rungNen).toFixed(1)} Q 8 -36 0 -26 Q -8 -36 0 ${(-50 + rungNen).toFixed(1)} Z`} fill="#F97316" />
              <circle cx={0} cy={-36} r={4} fill="#FEF08A" />
            </g>
          ))}
        </g>
      </g>

      {/* LOP 3 (1.0x): San da xam & buc go doc ban thao */}
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <rect x={-180} y={712} width={2280} height={450} fill="#475569" />
        <rect x={-180} y={706} width={2280} height={14} fill="#64748B" />
        {[780, 860, 950, 1040].map((sy) => (
          <line key={`tc-s-${sy}`} x1={-180} y1={sy} x2={2100} y2={sy} stroke="#334155" strokeWidth={3} />
        ))}
        {/* Buc go Scriptorium ben phai */}
        <g transform="translate(1590, 742)">
          <rect x={-16} y={-140} width={32} height={140} fill="#78350F" stroke="#451A03" strokeWidth={3} />
          <rect x={-64} y={-12} width={128} height={18} rx={4} fill="#451A03" />
          <polygon points="-78,-154 78,-188 86,-168 -70,-134" fill="#B45309" stroke="#451A03" strokeWidth={4} />
          <polygon points="-58,-156 58,-182 64,-168 -52,-142" fill="#FEF3C7" stroke="#D97706" strokeWidth={2} />
        </g>
      </g>
    </g>
  );
};

/** 11. Dai thien van Phuc Hung: parallax 3 lop (sao troi 0.2x, vom dong & tinh cau xoay 0.5x, san da & kinh thien van lon 1.0x) */
const DaiThienVanPhucHung: React.FC<{ frame: number; px: ParallaxOffset }> = ({
  frame,
  px,
}) => {
  const gocTinhCau = (frame * 0.65) % 360;
  return (
    <g>
      <defs>
        <linearGradient id="dtvTroi" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#020617" />
          <stop offset="60%" stopColor="#1E1B4B" />
          <stop offset="100%" stopColor="#312E81" />
        </linearGradient>
        <linearGradient id="dtvVom" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#451A03" />
          <stop offset="100%" stopColor="#291205" />
        </linearGradient>
      </defs>

      {/* LOP 1 (0.2x): Bau troi sao lap lanh & trang khuyet qua khe mai vom */}
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <rect x={-260} y={-120} width={2440} height={920} fill="url(#dtvTroi)" />
        {Array.from({ length: 42 }).map((_, i) => {
          const sx = 220 + bamTatDinh(i * 23 + 5) * 1480;
          const sy = 45 + bamTatDinh(i * 37 + 11) * 520;
          const r = 1.6 + bamTatDinh(i * 13 + 3) * 2.8;
          const op = 0.4 + 0.6 * Math.abs(Math.sin(frame * 0.09 + i * 1.1));
          return <circle key={`dtv-s-${i}`} cx={sx} cy={sy} r={r} fill="#FEF9C3" fillOpacity={op} />;
        })}
        <g transform="translate(620, 175)">
          <circle cx={0} cy={0} r={78} fill="#FEF08A" fillOpacity={0.14} />
          <path d="M 18 -44 A 48 48 0 1 0 18 44 A 36 36 0 1 1 18 -44 Z" fill="#FEF08A" />
        </g>
      </g>

      {/* LOP 2 (0.5x): Khung mai vom dai thien van, ban do tinh cau & qua cau hon thien xoay */}
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        {/* Tuong mai vom trai va phai mo khe o giua */}
        <path d="M -260 -120 L 660 -120 Q 430 140 360 720 L -260 720 Z" fill="url(#dtvVom)" stroke="#B45309" strokeWidth={10} />
        <path d="M 2180 -120 L 1260 -120 Q 1490 140 1560 720 L 2180 720 Z" fill="url(#dtvVom)" stroke="#B45309" strokeWidth={10} />

        {/* Ban do sao Phuc Hung treo tuong trai */}
        <g transform="translate(175, 360)">
          <rect x={-110} y={-135} width={220} height={270} rx={8} fill="#FEF3C7" stroke="#92400E" strokeWidth={8} />
          <circle cx={0} cy={0} r={74} fill="none" stroke="#B45309" strokeWidth={3} />
          <circle cx={0} cy={0} r={44} fill="none" stroke="#D97706" strokeWidth={2} strokeDasharray="5 4" />
          <line x1={-78} y1={0} x2={78} y2={0} stroke="#92400E" strokeWidth={2} />
          <line x1={0} y1={-78} x2={0} y2={78} stroke="#92400E" strokeWidth={2} />
        </g>

        {/* Qua cau hon thien (Armillary Sphere) xoay nhe ben phai */}
        <g transform="translate(1720, 420)">
          <rect x={-48} y={110} width={96} height={18} rx={5} fill="#92400E" />
          <line x1={0} y1={80} x2={0} y2={112} stroke="#D97706" strokeWidth={10} />
          <g transform={`rotate(${gocTinhCau.toFixed(1)})`}>
            <circle cx={0} cy={0} r={78} fill="none" stroke="#FACC15" strokeWidth={6} />
            <ellipse cx={0} cy={0} rx={78} ry={28} fill="none" stroke="#F59E0B" strokeWidth={4} />
            <ellipse cx={0} cy={0} rx={28} ry={78} fill="none" stroke="#FEF08A" strokeWidth={4} />
            <circle cx={0} cy={0} r={14} fill="#38BDF8" stroke="#FEF08A" strokeWidth={3} />
          </g>
        </g>
      </g>

      {/* LOP 3 (1.0x): San da dai thien van, lan can da & kinh thien van dong lon */}
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <rect x={-180} y={700} width={2280} height={460} fill="#1E293B" />
        <rect x={-180} y={692} width={2280} height={18} fill="#475569" stroke="#94A3B8" strokeWidth={2} />
        {/* Kinh thien van Phuc Hung co lon o tien canh phai */}
        <g transform="translate(1545, 705)">
          <line x1={0} y1={-125} x2={-78} y2={35} stroke="#78350F" strokeWidth={14} strokeLinecap="round" />
          <line x1={0} y1={-125} x2={68} y2={35} stroke="#78350F" strokeWidth={14} strokeLinecap="round" />
          <g transform="translate(0, -140) rotate(-32)">
            <rect x={-130} y={-22} width={220} height={44} rx={8} fill="#D97706" stroke="#78350F" strokeWidth={5} />
            <rect x={85} y={-30} width={58} height={60} rx={8} fill="#F59E0B" stroke="#78350F" strokeWidth={5} />
            <ellipse cx={144} cy={0} rx={8} ry={28} fill="#7DD3FC" stroke="#1E3A8A" strokeWidth={3} />
            <rect x={-20} y={-24} width={18} height={48} fill="#FEF08A" />
          </g>
          <circle cx={0} cy={-125} r={18} fill="#FACC15" stroke="#78350F" strokeWidth={5} />
        </g>
      </g>
    </g>
  );
};

/** 12. Giang duong / phong thi nghiem hien dai: parallax 3 lop (thanh pho ngoai cua kinh 0.2x, tuong & man hinh do thi 0.5x, san go & buc giang 1.0x) */
const GiangDuongHienDai: React.FC<{ frame: number; px: ParallaxOffset }> = ({
  frame,
  px,
}) => {
  // Song sin nhe tren man hinh hien thi toan hoc
  const diemSong = Array.from({ length: 28 })
    .map((_, i) => {
      const x = 670 + i * 21;
      const y = 315 + Math.sin(i * 0.45 + frame * 0.08) * 48;
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(' ');

  return (
    <g>
      <defs>
        <linearGradient id="gdTroi" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#38BDF8" />
          <stop offset="100%" stopColor="#E0F2FE" />
        </linearGradient>
        <linearGradient id="gdTuong" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#F8FAFC" />
          <stop offset="100%" stopColor="#E2E8F0" />
        </linearGradient>
      </defs>

      {/* LOP 1 (0.2x): Bau troi & duong chan troi thanh pho ngoai cua kinh lon */}
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <rect x={-260} y={-120} width={2440} height={820} fill="url(#gdTroi)" />
        <CumMay xGoc={140} y={135} tiLe={0.95} tocDo={0.28} frame={frame} />
        <CumMay xGoc={1480} y={160} tiLe={1.05} tocDo={0.32} frame={frame} />
        {[
          [40, 290, 95],
          [145, 220, 110],
          [265, 260, 85],
          [1540, 230, 105],
          [1660, 190, 120],
          [1795, 270, 95],
        ].map(([bx, by, bw], bi) => (
          <rect key={`gd-b-${bi}`} x={bx} y={by} width={bw} height={420} fill="#94A3B8" fillOpacity={0.55} />
        ))}
      </g>

      {/* LOP 2 (0.5x): Tuong op go tieu am, khung kinh hai ben & man hinh/bang kinh hien dai giua */}
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        {/* Tuong trung tam va khung cua so kinh 2 ben */}
        <rect x={410} y={-60} width={1100} height={780} fill="url(#gdTuong)" stroke="#CBD5E1" strokeWidth={6} />
        {/* Khung nhom cua kinh trai & phai */}
        <line x1={180} y1={-60} x2={180} y2={720} stroke="#CBD5E1" strokeWidth={10} />
        <line x1={1740} y1={-60} x2={1740} y2={720} stroke="#CBD5E1" strokeWidth={10} />
        <line x1={-180} y1={420} x2={410} y2={420} stroke="#CBD5E1" strokeWidth={8} />
        <line x1={1510} y1={420} x2={2100} y2={420} stroke="#CBD5E1" strokeWidth={8} />

        {/* Thanh nan go tieu am hien dai */}
        {Array.from({ length: 6 }).map((_, i) => (
          <g key={`gd-nan-${i}`}>
            <rect x={434 + i * 24} y={70} width={12} height={580} rx={3} fill="#D97706" fillOpacity={0.45} />
            <rect x={1354 + i * 24} y={70} width={12} height={580} rx={3} fill="#D97706" fillOpacity={0.45} />
          </g>
        ))}

        {/* Bang kinh / man hinh hien dai trung tam */}
        <rect x={600} y={108} width={720} height={420} rx={18} fill="#0F172A" stroke="#38BDF8" strokeWidth={6} />
        {[1, 2, 3, 4].map((gi) => (
          <line key={`gd-gl-${gi}`} x1={624} y1={108 + gi * 84} x2={1296} y2={108 + gi * 84} stroke="#38BDF8" strokeOpacity={0.14} strokeWidth={1.5} />
        ))}
        <polyline points={diemSong} fill="none" stroke="#38BDF8" strokeWidth={5} strokeLinecap="round" />
        {/* Den LED thanh tren tran */}
        <rect x={680} y={24} width={560} height={14} rx={7} fill="#FFFFFF" stroke="#BAE6FD" strokeWidth={3} />
      </g>

      {/* LOP 3 (1.0x): San go sang & buc giang phong thi nghiem */}
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <rect x={-180} y={705} width={2280} height={455} fill="#CBD5E1" />
        <rect x={-180} y={700} width={2280} height={14} fill="#94A3B8" />
        <rect x={280} y={714} width={1360} height={42} rx={6} fill="#B45309" stroke="#78350F" strokeWidth={3} />
        {/* Buc giang ben phai */}
        <g transform="translate(1585, 718)">
          <rect x={-62} y={-142} width={124} height={142} rx={8} fill="#1E293B" stroke="#38BDF8" strokeWidth={4} />
          <polygon points="-76,-142 76,-156 80,-138 -72,-126" fill="#334155" stroke="#94A3B8" strokeWidth={3} />
          <rect x={-26} y={-92} width={52} height={10} rx={4} fill="#38BDF8" />
        </g>
      </g>
    </g>
  );
};

/** Lop phu thoi tiet tat dinh 100% theo frame (khong blur, khong Math.random; rang buoc trong nha vs ngoai troi) */
const LopThoiTiet: React.FC<{
  thoiTiet?: LoaiThoiTiet;
  boiCanh: LoaiBoiCanh;
  frame: number;
}> = ({ thoiTiet, boiCanh, frame }) => {
  if (!thoiTiet || thoiTiet === 'khong') {
    return null;
  }

  const laTrongNha = BOI_CANH_TRONG_NHA.has(boiCanh);
  const laVuTru = BOI_CANH_VU_TRU.has(boiCanh);
  const cuaSo = layKhungCuaSoChoBoiCanh(boiCanh);

  if (laVuTru && (thoiTiet === 'la_roi' || thoiTiet === 'mua_nhe' || thoiTiet === 'tuyet_roi')) {
    return null;
  }
  if (laTrongNha && thoiTiet === 'la_roi') {
    return null;
  }

  switch (thoiTiet) {
    case 'nang_dep':
      return (
        <g pointerEvents="none">
          <polygon points="320,0 640,0 1060,1080 680,1080" fill="#FEF08A" fillOpacity={0.1} />
          <polygon points="690,0 920,0 1320,1080 1050,1080" fill="#FEF9C3" fillOpacity={0.08} />
          {Array.from({ length: 14 }).map((_, i) => {
            const x = 180 + bamTatDinh(i * 23 + 11) * 1560 + Math.sin(frame * 0.04 + i) * 24;
            const y = ((bamTatDinh(i * 37 + 5) * 900 - frame * 0.45) % 900 + 900) % 900;
            const op = 0.28 + 0.32 * Math.abs(Math.sin(frame * 0.06 + i));
            return <circle key={`nang-${i}`} cx={x} cy={y} r={3.5 + (i % 3)} fill="#FEF9C3" fillOpacity={op} />;
          })}
        </g>
      );

    case 'hoang_hon':
      return (
        <g pointerEvents="none">
          <rect x={-180} y={-120} width={2280} height={1320} fill="#F97316" fillOpacity={0.13} />
          <polygon points="240,0 820,0 1460,1080 860,1080" fill="#FDE68A" fillOpacity={0.09} />
        </g>
      );

    case 'ban_dem':
      return (
        <g pointerEvents="none">
          <rect x={-180} y={-120} width={2280} height={1320} fill="#0F172A" fillOpacity={0.14} />
          {!laTrongNha &&
            Array.from({ length: 10 }).map((_, i) => {
              const fx = 140 + bamTatDinh(i * 41 + 9) * 1640 + Math.sin(frame * 0.05 + i) * 22;
              const fy = 520 + bamTatDinh(i * 17 + 3) * 360 + Math.cos(frame * 0.06 + i) * 16;
              const op = 0.25 + 0.65 * Math.abs(Math.sin(frame * 0.1 + i * 1.4));
              return (
                <g key={`domdom-${i}`} opacity={op}>
                  <circle cx={fx} cy={fy} r={8} fill="#FDE047" fillOpacity={0.28} />
                  <circle cx={fx} cy={fy} r={3} fill="#FEF9C3" />
                </g>
              );
            })}
        </g>
      );

    case 'mua_nhe': {
      if (laTrongNha) {
        if (!cuaSo) return null;
        const clipId = `clip-mua-cs-${boiCanh}`;
        return (
          <g pointerEvents="none">
            <defs>
              <clipPath id={clipId}>
                <rect x={cuaSo.x} y={cuaSo.y} width={cuaSo.width} height={cuaSo.height} rx={6} />
              </clipPath>
            </defs>
            <g clipPath={`url(#${clipId})`}>
              {Array.from({ length: 24 }).map((_, i) => {
                const speed = 14 + (i % 4) * 3;
                const x0 = cuaSo.x + bamTatDinh(i * 29 + 1) * (cuaSo.width + 60);
                const y0 = bamTatDinh(i * 53 + 7) * cuaSo.height;
                const y = cuaSo.y + ((y0 + frame * speed) % (cuaSo.height + 30)) - 20;
                const x = x0 - ((frame * speed * 0.18) % 60);
                return (
                  <line
                    key={`mua-cs-${i}`}
                    x1={x}
                    y1={y}
                    x2={x - 7}
                    y2={y + 24}
                    stroke="#E0F2FE"
                    strokeOpacity={0.62}
                    strokeWidth={2}
                    strokeLinecap="round"
                  />
                );
              })}
            </g>
          </g>
        );
      }
      return (
        <g pointerEvents="none">
          <rect x={-180} y={-120} width={2280} height={1320} fill="#0F172A" fillOpacity={0.12} />
          {Array.from({ length: 44 }).map((_, i) => {
            const speed = 18 + (i % 4) * 4;
            const x0 = bamTatDinh(i * 29 + 1) * 2100;
            const y0 = bamTatDinh(i * 53 + 7) * 1160;
            const y = ((y0 + frame * speed) % 1140) - 40;
            const x = (((x0 - frame * speed * 0.22) % 2040) + 2040) % 2040 - 60;
            return (
              <line
                key={`mua-${i}`}
                x1={x}
                y1={y}
                x2={x - 9}
                y2={y + 34}
                stroke="#E0F2FE"
                strokeOpacity={0.58}
                strokeWidth={2.2}
                strokeLinecap="round"
              />
            );
          })}
        </g>
      );
    }

    case 'la_roi':
      return (
        <g pointerEvents="none">
          {Array.from({ length: 18 }).map((_, i) => {
            const x0 = bamTatDinh(i * 31 + 3) * 1920;
            const y0 = bamTatDinh(i * 47 + 11) * 1080;
            const speed = 2.4 + (i % 4) * 0.7;
            const y = ((y0 + frame * speed) % 1140) - 30;
            const x = (((x0 + Math.sin(frame * 0.07 + i) * 58 + frame * 1.1) % 2020) + 2020) % 2020 - 50;
            const rot = (frame * (2.5 + (i % 3)) + i * 47) % 360;
            const mauLa = i % 3 === 0 ? '#F59E0B' : i % 3 === 1 ? '#EA580C' : '#EAB308';
            return (
              <g key={`la-${i}`} transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)}) rotate(${rot.toFixed(1)})`}>
                <path d="M -12 0 Q 0 -10 14 0 Q 0 10 -12 0 Z" fill={mauLa} stroke="#9A3412" strokeWidth={1.2} />
                <line x1={-10} y1={0} x2={10} y2={0} stroke="#FEF3C7" strokeWidth={1.2} />
              </g>
            );
          })}
        </g>
      );

    case 'tuyet_roi': {
      if (laTrongNha) {
        if (!cuaSo) return null;
        const clipId = `clip-tuyet-tt-${boiCanh}`;
        return (
          <g pointerEvents="none">
            <defs>
              <clipPath id={clipId}>
                <rect x={cuaSo.x} y={cuaSo.y} width={cuaSo.width} height={cuaSo.height} rx={6} />
              </clipPath>
            </defs>
            <g clipPath={`url(#${clipId})`}>
              {Array.from({ length: 20 }).map((_, i) => {
                const sx = cuaSo.x + bamTatDinh(i * 19 + 5) * cuaSo.width;
                const sy0 = bamTatDinh(i * 43 + 9) * cuaSo.height;
                const speed = 1.4 + (i % 4) * 0.5;
                const y = cuaSo.y + ((sy0 + frame * speed) % (cuaSo.height + 16)) - 8;
                const x = sx + Math.sin(frame * 0.05 + i * 1.7) * 14;
                const r = 2.6 + (i % 3) * 1.4;
                return <circle key={`tuyet-cs-${i}`} cx={x} cy={y} r={r} fill="#FFFFFF" fillOpacity={0.85} />;
              })}
            </g>
          </g>
        );
      }
      return (
        <g pointerEvents="none">
          {Array.from({ length: 36 }).map((_, i) => {
            const x0 = bamTatDinh(i * 19 + 5) * 1920;
            const y0 = bamTatDinh(i * 43 + 9) * 1080;
            const speed = 1.6 + (i % 4) * 0.55;
            const y = ((y0 + frame * speed) % 1120) - 20;
            const x = (((x0 + Math.sin(frame * 0.05 + i * 1.7) * 32) % 1960) + 1960) % 1960 - 20;
            const r = 3.2 + (i % 3) * 2;
            return <circle key={`tuyet-${i}`} cx={x} cy={y} r={r} fill="#FFFFFF" fillOpacity={0.82} />;
          })}
        </g>
      );
    }

    default:
      return null;
  }
};

export const BoiCanhHoatHinh: React.FC<BoiCanhHoatHinhProps> = ({
  loai,
  thoiTiet = 'khong',
  vatTheXungQuanh,
  bienSoXe,
  nhanVat,
  daoCu,
  anNoiNen: anNoiNenProp,
  anGiuongBenhNen: anGiuongBenhNenProp,
  anhBoiCanh,
  anhSangMoiTruong,
  laKhungTranhDacTa = false,
  thoiLuongCanh,
}) => {
  const frame = useCurrentFrame();
  const cam = useCameraParallax();

  // Khi canh co anhBoiCanh (minh hoa AI v3.0): render NenMinhHoaAI + lop khong khi song dong
  const duongDanAnhAi = typeof anhBoiCanh === 'string' ? anhBoiCanh.trim() : '';
  if (duongDanAnhAi.length > 0) {
    return (
      <NenMinhHoaAI
        anhBoiCanh={duongDanAnhAi}
        loaiBoiCanh={loai}
        thoiTiet={thoiTiet}
        anhSangMoiTruong={anhSangMoiTruong}
        vatTheXungQuanh={vatTheXungQuanh}
        bienSoXe={bienSoXe}
        laKhungTranhDacTa={laKhungTranhDacTa}
        thoiLuongCanh={thoiLuongCanh}
      />
    );
  }

  const px = tinhParallax(cam.panX, cam.panY);
  const anNoiNen = anNoiNenProp ?? true;
  const anGiuongBenhNen =
    anGiuongBenhNenProp ?? coAnGiuongBenhNen(nhanVat, daoCu);

  const veBoiCanh = () => {
    switch (loai) {
      case 'bo_bien_hy_lap':
        return <BoBienHyLap frame={frame} laHoangHon={thoiTiet === 'hoang_hon'} px={px} />;
      case 'vuon_tao_dong_que':
        return <VuonTaoDongQue frame={frame} px={px} />;
      case 'pho_co_chau_au':
        return <PhoCoChauAu frame={frame} px={px} />;
      case 'rung_nui_thien_nhien':
        return <RungNuiThienNhien frame={frame} px={px} />;
      case 'thu_vien_co_dien':
        return <ThuVienCoDien frame={frame} px={px} />;
      case 'lop_hoc_bang_xanh':
        return <LopHocBangXanh frame={frame} px={px} />;
      case 'bau_troi_dem_vu_tru':
        return <BauTroiDemVuTru frame={frame} px={px} />;
      case 'quang_truong_hy_lap':
        return <QuangTruongHyLap frame={frame} px={px} />;
      case 'thu_vien_trung_co':
        return <ThuVienTrungCo frame={frame} px={px} />;
      case 'dai_thien_van_phuc_hung':
        return <DaiThienVanPhucHung frame={frame} px={px} />;
      case 'giang_duong_hien_dai':
        return <GiangDuongHienDai frame={frame} px={px} />;
      case 'nha_co_phong_sinh':
        return <NhaCoPhongSinh frame={frame} px={px} anNoiNen={anNoiNen} />;
      case 'cang_bien_tau_thuy':
        return <CangBienTauThuy frame={frame} px={px} laHoangHon={thoiTiet === 'hoang_hon'} />;
      case 'phong_tro_bep_lua':
        return <PhongTroBepLua frame={frame} px={px} />;
      case 'phong_benh_vien':
        return <PhongBenhVien frame={frame} px={px} anGiuongBenhNen={anGiuongBenhNen} />;
      case 'duong_pho_xe_co':
        return <DuongPhoXeCo frame={frame} px={px} laHoangHon={thoiTiet === 'hoang_hon'} />;
      case 'giang_duong_dai_hoc':
        return <GiangDuongDaiHoc frame={frame} px={px} />;
      case 'san_truong_co_dien':
        return <SanTruongCoDien frame={frame} px={px} laHoangHon={thoiTiet === 'hoang_hon'} />;
      case 'phong_thi_nghiem_co':
        return <PhongThiNghiemCo frame={frame} px={px} />;
      case 'khong_gian_vu_tru_toan':
        return <KhongGianVuTruToan frame={frame} px={px} />;
      case 'lang_que_an_do_a_dong':
        return <LangQueAnDoADong frame={frame} px={px} laHoangHon={thoiTiet === 'hoang_hon'} />;
      case 'phong_nen_hai_huoc':
      default:
        return <PhongNenHaiHuoc frame={frame} px={px} />;
    }
  };

  return (
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
      {veBoiCanh()}
      <SinhVatVaMoiTruong
        boiCanh={loai}
        thoiTiet={thoiTiet}
        vatTheXungQuanh={vatTheXungQuanh}
        bienSoXe={bienSoXe}
      />
      <LopThoiTiet thoiTiet={thoiTiet} boiCanh={loai} frame={frame} />
    </svg>
  );
};
