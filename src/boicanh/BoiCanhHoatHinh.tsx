import React from 'react';
import { useCurrentFrame } from 'remotion';
import type { LoaiBoiCanh, LoaiThoiTiet } from '../kieu_dai';
import { bamTatDinh } from '../vfx/tat_dinh';

type BoiCanhHoatHinhProps = {
  loai: LoaiBoiCanh;
  thoiTiet?: LoaiThoiTiet;
};

/** Cum may trang bong benh troi tat dinh theo frame */
const CumMay: React.FC<{
  xGoc: number;
  y: number;
  tiLe: number;
  tocDo: number;
  frame: number;
  mau?: string;
  doMo?: number;
}> = ({ xGoc, y, tiLe, tocDo, frame, mau = '#FFFFFF', doMo = 0.92 }) => {
  const x = ((xGoc + frame * tocDo) % 2280) - 180;
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

/** Canh chim bay xa vo canh tat dinh */
const ChimBay: React.FC<{
  xGoc: number;
  yGoc: number;
  tocDo: number;
  tiLe: number;
  frame: number;
  pha: number;
  mau?: string;
}> = ({ xGoc, yGoc, tocDo, tiLe, frame, pha, mau = '#334155' }) => {
  const x = ((xGoc + frame * tocDo) % 2140) - 110;
  const y = yGoc + Math.sin(frame * 0.08 + pha) * 10;
  const canhY = Math.sin(frame * 0.34 + pha) * 7;
  return (
    <path
      d={`M -16 ${canhY.toFixed(1)} Q -8 ${(-7 + canhY * 0.4).toFixed(1)} 0 0 Q 8 ${(-7 + canhY * 0.4).toFixed(1)} 16 ${canhY.toFixed(1)}`}
      transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)}) scale(${tiLe})`}
      fill="none"
      stroke={mau}
      strokeWidth={2.6}
      strokeLinecap="round"
    />
  );
};

/** 1. Bo bien Hy Lap co dai: troi trong/hoang hon, vach da trang, cot da, cay o-liu, bien song & canh buom */
const BoBienHyLap: React.FC<{ frame: number; laHoangHon: boolean }> = ({
  frame,
  laHoangHon,
}) => {
  const troiTren = laHoangHon ? '#EA580C' : '#0EA5E9';
  const troiGiua = laHoangHon ? '#FB923C' : '#38BDF8';
  const troiDuoi = laHoangHon ? '#FDE68A' : '#E0F2FE';
  const bienTren = laHoangHon ? '#0369A1' : '#0284C7';
  const bienDuoi = laHoangHon ? '#1E3A8A' : '#0EA5E9';
  const matTroiMau = laHoangHon ? '#FEF08A' : '#FFFBEB';

  const duaLa = Math.sin(frame * 0.06) * 4.5;
  const duaLa2 = Math.cos(frame * 0.055) * 3.5;
  const thuyenX = 1180 + ((frame * 0.65) % 420);
  const thuyenY = 548 + Math.sin(frame * 0.1) * 3.5;

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

      {/* Lop 1: Bau troi, mat troi, may troi & hai au */}
      <rect x={0} y={0} width={1920} height={600} fill="url(#hyLapTroi)" />

      {/* Mat troi am ap (vong hao quang trong suot, khong blur) */}
      <g transform={`translate(${laHoangHon ? 1480 : 1540}, ${laHoangHon ? 430 : 180})`}>
        <circle cx={0} cy={0} r={145} fill={matTroiMau} fillOpacity={0.14} />
        <circle cx={0} cy={0} r={98} fill={matTroiMau} fillOpacity={0.24} />
        <circle cx={0} cy={0} r={62} fill={matTroiMau} />
      </g>

      <CumMay xGoc={160} y={135} tiLe={1.35} tocDo={0.42} frame={frame} mau={laHoangHon ? '#FFEDD5' : '#FFFFFF'} doMo={0.9} />
      <CumMay xGoc={840} y={100} tiLe={1.1} tocDo={0.28} frame={frame} mau={laHoangHon ? '#FED7AA' : '#FFFFFF'} doMo={0.85} />
      <CumMay xGoc={1420} y={195} tiLe={0.95} tocDo={0.35} frame={frame} mau={laHoangHon ? '#FFEDD5' : '#FFFFFF'} doMo={0.8} />

      <ChimBay xGoc={420} yGoc={210} tocDo={1.3} tiLe={1.0} frame={frame} pha={0.4} mau={laHoangHon ? '#7C2D12' : '#0C4A6E'} />
      <ChimBay xGoc={470} yGoc={185} tocDo={1.2} tiLe={0.82} frame={frame} pha={1.9} mau={laHoangHon ? '#7C2D12' : '#0C4A6E'} />
      <ChimBay xGoc={1120} yGoc={240} tocDo={1.05} tiLe={0.75} frame={frame} pha={3.1} mau={laHoangHon ? '#7C2D12' : '#0C4A6E'} />

      {/* Lop 2: Bien Dia Trung Hai, dao xa, canh buom & vach da trang co dien */}
      <rect x={0} y={530} width={1920} height={240} fill="url(#hyLapBien)" />

      {/* Dao nui xa chan troi */}
      <path d="M 880 532 Q 1030 462 1190 508 Q 1340 475 1480 532 Z" fill={laHoangHon ? '#9A3412' : '#38BDF8'} fillOpacity={0.45} />
      <path d="M 1520 532 Q 1680 468 1860 512 L 1920 532 Z" fill={laHoangHon ? '#7C2D12' : '#0284C7'} fillOpacity={0.4} />

      {/* Song nuoc gon nhe ngang mat bien */}
      {[0, 1, 2, 3, 4, 5, 6, 7].map((i) => {
        const wx = ((i * 270 + frame * (0.9 + (i % 3) * 0.25)) % 2100) - 90;
        const wy = 562 + (i % 4) * 34;
        return (
          <path
            key={`song-${i}`}
            d={`M ${wx} ${wy} Q ${wx + 32} ${wy - 6} ${wx + 64} ${wy} Q ${wx + 96} ${wy + 6} ${wx + 128} ${wy}`}
            fill="none"
            stroke="#E0F2FE"
            strokeOpacity={0.55}
            strokeWidth={3.5}
            strokeLinecap="round"
          />
        );
      })}

      {/* Canh buom Hy Lap xa */}
      <g transform={`translate(${thuyenX.toFixed(1)}, ${thuyenY.toFixed(1)})`}>
        <path d="M -38 8 Q 0 22 42 8 L 30 20 L -28 20 Z" fill="#92400E" />
        <line x1={2} y1={10} x2={2} y2={-64} stroke="#78350F" strokeWidth={4} />
        <path d="M 4 -58 Q 42 -26 32 4 L 4 4 Z" fill="#FFFBEB" stroke="#E2E8F0" strokeWidth={2} />
        <path d="M -1 -48 Q -24 -20 -18 4 L -1 4 Z" fill="#FEF3C7" stroke="#E2E8F0" strokeWidth={1.5} />
      </g>

      {/* Vach da trang ben trai + hang cot Doric */}
      <path d="M 0 360 Q 170 340 360 390 Q 520 430 610 560 L 0 580 Z" fill="#F1F5F9" />
      <path d="M 0 420 Q 190 400 350 450 L 490 580 L 0 580 Z" fill="#E2E8F0" />

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

      {/* Lop 3: San da vang am tien canh & cay o-liu dung dua */}
      <path d="M 0 710 Q 520 676 1080 698 Q 1560 716 1920 688 L 1920 1080 L 0 1080 Z" fill="url(#hyLapSan)" />
      {/* Gach da lat duong co */}
      <path d="M 0 738 Q 640 710 1280 732 Q 1620 742 1920 722" fill="none" stroke="#D6B98C" strokeWidth={5} />
      {[180, 460, 780, 1120, 1460, 1740].map((gx, i) => (
        <ellipse key={`da-${i}`} cx={gx} cy={835 + (i % 2) * 34} rx={58} ry={13} fill="#D6B98C" fillOpacity={0.38} />
      ))}

      {/* Bui co xanh ven bo da */}
      <g>
        <ellipse cx={220} cy={726} rx={78} ry={28} fill="#65A30D" />
        <ellipse cx={275} cy={732} rx={56} ry={22} fill="#84CC16" />
        <ellipse cx={1670} cy={712} rx={88} ry={30} fill="#4D7C0F" />
        <ellipse cx={1735} cy={720} rx={68} ry={24} fill="#65A30D" />
      </g>

      {/* Cay o-liu co thu ben phai tien canh co la dung dua theo sin */}
      <g transform="translate(1780, 742)">
        <path d="M -24 20 Q -36 -110 -12 -220 Q 8 -260 44 -310 L 66 -294 Q 24 -220 18 -120 Q 16 -40 28 20 Z" fill="#78350F" />
        <path d="M -12 -180 Q -92 -236 -146 -272" fill="none" stroke="#78350F" strokeWidth={18} strokeLinecap="round" />
        <g transform={`translate(${duaLa.toFixed(1)}, ${(duaLa2 * 0.4).toFixed(1)})`}>
          <ellipse cx={-125} cy={-292} rx={115} ry={58} fill="#4D7C0F" />
          <ellipse cx={-40} cy={-338} rx={128} ry={66} fill="#65A30D" />
          <ellipse cx={55} cy={-305} rx={108} ry={56} fill="#84CC16" />
          <ellipse cx={-72} cy={-268} rx={88} ry={44} fill="#84CC16" fillOpacity={0.85} />
          {/* Qua o-liu nho */}
          <circle cx={-120} cy={-278} r={6} fill="#365314" />
          <circle cx={-56} cy={-315} r={6} fill="#365314" />
          <circle cx={24} cy={-290} r={6} fill="#365314" />
        </g>
      </g>
    </g>
  );
};

/** 2. Vuon tao dong que: doi co xanh nhieu tang, cay tao co qua lac/roi, hang rao go, may trang & tia nang */
const VuonTaoDongQue: React.FC<{ frame: number }> = ({ frame }) => {
  const duaCanh = Math.sin(frame * 0.065) * 4;
  // 1 qua tao lac nhe roi roi xuong theo chu ky 150 frame
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

      {/* Lop 1: Troi xanh + tia nang nghieng + may bong benh */}
      <rect x={0} y={0} width={1920} height={620} fill="url(#vuonTroi)" />
      <polygon points="150,0 440,0 760,720 420,720" fill="#FEF08A" fillOpacity={0.14} />
      <polygon points="540,0 760,0 1090,720 820,720" fill="#FEF08A" fillOpacity={0.1} />

      <CumMay xGoc={120} y={120} tiLe={1.3} tocDo={0.38} frame={frame} />
      <CumMay xGoc={780} y={90} tiLe={1.15} tocDo={0.28} frame={frame} />
      <CumMay xGoc={1380} y={150} tiLe={1.0} tocDo={0.34} frame={frame} />

      {/* Lop 2: Doi co nhieu tang + ngoi nha go xa */}
      <path d="M 0 560 Q 340 430 720 510 Q 1120 580 1560 470 Q 1780 430 1920 480 L 1920 760 L 0 760 Z" fill="#86EFAC" />
      <path d="M 0 610 Q 480 510 960 585 Q 1440 650 1920 545 L 1920 800 L 0 800 Z" fill="#4ADE80" />

      {/* Hang rao go dong que */}
      <g transform="translate(0, 610)">
        <rect x={40} y={32} width={1180} height={11} rx={4} fill="#B45309" />
        <rect x={40} y={66} width={1180} height={11} rx={4} fill="#92400E" />
        {Array.from({ length: 13 }).map((_, i) => (
          <rect key={`rao-${i}`} x={66 + i * 94} y={12} width={18} height={92} rx={4} fill="#D97706" stroke="#78350F" strokeWidth={2} />
        ))}
      </g>

      {/* Lop 3: Tham co tien canh & cay tao lon */}
      <path d="M 0 700 Q 540 676 1120 704 Q 1560 720 1920 694 L 1920 1080 L 0 1080 Z" fill="url(#vuonCo)" />
      {/* Con duong dat nho uon luon */}
      <path d="M 180 1080 Q 540 870 960 780 Q 1280 730 1520 725 L 1590 732 Q 1280 760 1040 825 Q 720 920 520 1080 Z" fill="#E7D3B1" fillOpacity={0.75} />

      {/* Cay tao lon ben phai */}
      <g transform="translate(1540, 748)">
        <path d="M -42 18 Q -32 -140 -26 -290 L 28 -290 Q 22 -140 46 18 Z" fill="#78350F" />
        <path d="M -18 -240 Q -110 -300 -150 -340" fill="none" stroke="#78350F" strokeWidth={22} strokeLinecap="round" />
        <g transform={`translate(${duaCanh.toFixed(1)}, 0)`}>
          <circle cx={-125} cy={-355} r={108} fill="#15803D" />
          <circle cx={0} cy={-410} r={136} fill="#16A34A" />
          <circle cx={120} cy={-355} r={112} fill="#22C55E" />
          <circle cx={-55} cy={-315} r={96} fill="#22C55E" />
          <circle cx={68} cy={-312} r={92} fill="#4ADE80" fillOpacity={0.75} />

          {/* Cac qua tao do tren cay */}
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

      {/* Qua tao dang lac va roi xuong dat */}
      <g transform={`translate(${taoX.toFixed(1)}, ${taoY.toFixed(1)})`}>
        <circle cx={0} cy={0} r={15} fill="#DC2626" stroke="#7F1D1D" strokeWidth={2.2} />
        <ellipse cx={-4} cy={-4} rx={4.5} ry={2.6} fill="#FCA5A5" />
        <path d="M 0 -15 Q 7 -24 14 -20 Q 8 -14 0 -15 Z" fill="#22C55E" />
      </g>

      {/* Hoa dai nho tren co */}
      {[210, 390, 680, 1180, 1740].map((fx, i) => (
        <g key={`hoa-${i}`} transform={`translate(${fx}, ${825 + (i % 3) * 32})`}>
          <circle cx={0} cy={0} r={6} fill={i % 2 === 0 ? '#FEF08A' : '#F472B6'} />
          <circle cx={0} cy={0} r={2.5} fill="#FFFFFF" />
        </g>
      ))}
    </g>
  );
};

/** 3. Pho co chau Au: duong lat da, day nha mai nhon am ap, cau da bac qua song, den duong co */
const PhoCoChauAu: React.FC<{ frame: number }> = ({ frame }) => {
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

      {/* Lop 1: Bau troi & may */}
      <rect x={0} y={0} width={1920} height={600} fill="url(#phoTroi)" />
      <CumMay xGoc={320} y={115} tiLe={1.15} tocDo={0.32} frame={frame} />
      <CumMay xGoc={1060} y={140} tiLe={1.0} tocDo={0.26} frame={frame} />

      {/* Lop 2: Dong song + cau da vong + day nha mai nhon chau Au */}
      <rect x={0} y={560} width={1920} height={175} fill="url(#phoSong)" />
      {[0, 1, 2, 3, 4, 5].map((i) => {
        const sx = 620 + ((i * 120 + frame * 0.7) % 680);
        const sy = 595 + (i % 3) * 32;
        return (
          <line
            key={`ph-song-${i}`}
            x1={sx}
            y1={sy}
            x2={sx + 56}
            y2={sy}
            stroke="#E0F2FE"
            strokeOpacity={0.55}
            strokeWidth={3.5}
            strokeLinecap="round"
          />
        );
      })}

      {/* Cau da 3 nhip o giua khung hinh */}
      <g transform="translate(560, 495)">
        <path
          d="M 0 110 L 0 28 Q 400 -24 800 28 L 800 110 L 710 110 A 90 66 0 0 0 530 110 L 490 110 A 90 66 0 0 0 310 110 L 270 110 A 90 66 0 0 0 90 110 Z"
          fill="#CBD5E1"
          stroke="#64748B"
          strokeWidth={4}
        />
        <path d="M 0 28 Q 400 -24 800 28" fill="none" stroke="#94A3B8" strokeWidth={10} />
      </g>

      {/* Day nha mai nhon hai ben bo song */}
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

      {/* Lop 3: Duong lat da bo song + den duong co */}
      <rect x={0} y={695} width={1920} height={385} fill="#94A3B8" />
      <rect x={0} y={688} width={1920} height={18} fill="#CBD5E1" stroke="#64748B" strokeWidth={2} />
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

      {/* Hai cot den duong co dien */}
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
  );
};

/** 4. Rung nui thien nhien: day nui trung diep, rung thong nhieu lop, suoi nho uon luon & dan chim bay */
const RungNuiThienNhien: React.FC<{ frame: number }> = ({ frame }) => {
  const veThong = (x: number, y: number, tiLe: number, mau: string, idx: number) => {
    const dua = Math.sin(frame * 0.05 + idx) * 2.5;
    return (
      <g key={`thong-${idx}`} transform={`translate(${x}, ${y}) scale(${tiLe})`}>
        <rect x={-7} y={-28} width={14} height={36} fill="#5C3A21" />
        <polygon points={`${dua},-125 -42,-58 42,-58`} fill={mau} />
        <polygon points={`${dua * 0.7},-92 -52,-26 52,-26`} fill={mau} />
        <polygon points={`${dua * 0.4},-56 -60,2 60,2`} fill={mau} />
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

      {/* Lop 1: Bau troi + may + dan chim bay ngang */}
      <rect x={0} y={0} width={1920} height={600} fill="url(#nuiTroi)" />
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

      {/* Lop 2: Day nui trung diep 3 tang chieu sau khi quyen */}
      <polygon points="0,560 280,260 590,480 920,210 1280,450 1620,235 1920,440 1920,680 0,680" fill="#64748B" fillOpacity={0.55} />
      {/* Dinh tuyet trang tren nui xa */}
      <polygon points="920,210 854,282 900,268 925,294 958,268 986,282" fill="#F8FAFC" />
      <polygon points="1620,235 1564,296 1605,284 1628,308 1660,285 1684,298" fill="#F8FAFC" />

      <path d="M 0 600 Q 320 430 680 540 Q 1080 620 1480 465 Q 1740 410 1920 515 L 1920 760 L 0 760 Z" fill="#15803D" />
      <path d="M 0 655 Q 480 565 960 635 Q 1460 700 1920 605 L 1920 820 L 0 820 Z" fill="#16A34A" />

      {/* Rung thong lop giua */}
      {[120, 260, 410, 1460, 1610, 1770].map((tx, idx) =>
        veThong(tx, 645 + (idx % 2) * 22, 1.15 + (idx % 3) * 0.14, '#14532D', idx),
      )}

      {/* Lop 3: Tham co & dong suoi nho uon luon */}
      <path d="M 0 702 Q 620 680 1260 708 Q 1640 722 1920 698 L 1920 1080 L 0 1080 Z" fill="url(#nuiCo)" />

      {/* Suoi nuoc uon luon lap lanh */}
      <path
        d="M 1020 696 Q 940 770 1120 845 Q 1260 910 1040 1080 L 1220 1080 Q 1410 920 1220 830 Q 1040 755 1095 696 Z"
        fill="#38BDF8"
        stroke="#BAE6FD"
        strokeWidth={4}
      />
      {[0, 1, 2, 3].map((i) => {
        const py = 740 + ((i * 75 + frame * 1.4) % 300);
        const px = 1120 + Math.sin(py * 0.025) * 65;
        return (
          <line key={`suoi-${i}`} x1={px - 18} y1={py} x2={px + 18} y2={py} stroke="#FFFFFF" strokeOpacity={0.7} strokeWidth={3} strokeLinecap="round" />
        );
      })}

      {/* Hai cay thong tien canh mep man hinh */}
      {veThong(76, 770, 1.55, '#0F3D22', 10)}
      {veThong(1845, 765, 1.5, '#0F3D22', 11)}
    </g>
  );
};

/** 5. Thu vien co dien: phong go am cung, cua so vom lon nhin ra troi, gia sach, ban go, qua dia cau & nen */
const ThuVienCoDien: React.FC<{ frame: number }> = ({ frame }) => {
  const ngonNen = Math.sin(frame * 0.28) * 3;
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

      {/* Lop 1: Tuong go + cua so vom lon nhin ra troi may */}
      <rect x={0} y={0} width={1920} height={740} fill="url(#tvTuong)" />
      <g transform="translate(690, 95)">
        <path d="M 0 540 L 0 210 A 270 210 0 0 1 540 210 L 540 540 Z" fill="url(#tvCuaSo)" stroke="#92400E" strokeWidth={16} />
        <clipPath id="clipCuaSoTv">
          <path d="M 8 532 L 8 210 A 262 202 0 0 1 532 210 L 532 532 Z" />
        </clipPath>
        <g clipPath="url(#clipCuaSoTv)">
          <CumMay xGoc={60} y={145} tiLe={0.78} tocDo={0.35} frame={frame} />
          <CumMay xGoc={320} y={240} tiLe={0.65} tocDo={0.25} frame={frame} />
        </g>
        {/* Song cua so co dien */}
        <line x1={270} y1={10} x2={270} y2={540} stroke="#92400E" strokeWidth={10} />
        <line x1={8} y1={240} x2={532} y2={240} stroke="#92400E" strokeWidth={10} />
        <line x1={8} y1={390} x2={532} y2={390} stroke="#92400E" strokeWidth={10} />
      </g>

      {/* Lop 2: Hai gia sach lon hai ben */}
      {veKeSach(120)}
      {veKeSach(1380)}

      {/* Lop 3: San go am + ban lam viec co qua dia cau & nen chap chon */}
      <rect x={0} y={712} width={1920} height={368} fill="#92400E" />
      <rect x={0} y={712} width={1920} height={14} fill="#B45309" />
      {[780, 855, 935, 1020].map((ly) => (
        <line key={`san-${ly}`} x1={0} y1={ly} x2={1920} y2={ly} stroke="#78350F" strokeWidth={3} />
      ))}

      {/* Ban go goc phai + qua dia cau + cay nen */}
      <g transform="translate(1485, 675)">
        <rect x={-165} y={18} width={330} height={24} rx={6} fill="#B45309" stroke="#451A03" strokeWidth={4} />
        <rect x={-135} y={42} width={22} height={115} fill="#78350F" />
        <rect x={113} y={42} width={22} height={115} fill="#78350F" />
        {/* Qua dia cau */}
        <g transform="translate(-75, -36)">
          <circle cx={0} cy={0} r={34} fill="#38BDF8" stroke="#1E3A8A" strokeWidth={3} />
          <path d="M -18 -14 Q -4 -20 12 -8 Q 18 6 2 16 Q -14 14 -18 -14 Z" fill="#4ADE80" />
          <path d="M -42 0 A 42 42 0 0 0 42 0" fill="none" stroke="#D97706" strokeWidth={5} />
          <line x1={0} y1={42} x2={0} y2={54} stroke="#D97706" strokeWidth={6} />
          <rect x={-24} y={50} width={48} height={8} rx={4} fill="#B45309" />
        </g>
        {/* Cay nen chap chon khong blur */}
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
  );
};

/** 6. Lop hoc bang xanh: sang sua am ap, bang xanh lon vien go, ke phan, thuoc go, toi uu doc cong thuc Toan */
const LopHocBangXanh: React.FC<{ frame: number }> = ({ frame }) => {
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

      {/* Lop 1: Tuong kem am ap + lam go chan tuong */}
      <rect x={0} y={0} width={1920} height={745} fill="url(#lopTuong)" />
      <rect x={0} y={645} width={1920} height={100} fill="#E7D3B1" />
      <rect x={0} y={638} width={1920} height={14} fill="#C29B61" />

      {/* Tia nang nhe chieu tu cua so ben trai */}
      <polygon points="0,40 240,40 520,745 0,745" fill="#FEF08A" fillOpacity={0.18} />
      <circle cx={190 + buiNang} cy={220} r={4} fill="#FFFFFF" fillOpacity={0.65} />
      <circle cx={270 - buiNang} cy={350} r={3} fill="#FFFFFF" fillOpacity={0.55} />

      {/* Lop 2: Khung bang xanh lon nen tang + ke phan + thuoc eke go trang tri */}
      <rect x={545} y={76} width={1320} height={588} rx={16} fill="#14532D" stroke="#92400E" strokeWidth={16} />
      <rect x={562} y={93} width={1286} height={554} rx={8} fill="#114226" />
      {/* Ke phan & cac vien phan mau */}
      <rect x={530} y={658} width={1350} height={22} rx={6} fill="#B45309" stroke="#78350F" strokeWidth={3} />
      <rect x={630} y={646} width={44} height={12} rx={4} fill="#F8FAFC" />
      <rect x={686} y={646} width={36} height={12} rx={4} fill="#FEF08A" />
      <rect x={734} y={646} width={36} height={12} rx={4} fill="#7DD3FC" />
      {/* Gie lau bang */}
      <rect x={1690} y={636} width={78} height={22} rx={5} fill="#78350F" />
      <rect x={1696} y={630} width={66} height={10} rx={3} fill="#D97706" />

      {/* Dong ho treo tuong goc trai tren */}
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

      {/* Thuoc eke go treo trang tri goc trai */}
      <g transform="translate(340, 128) rotate(8)" opacity={0.85}>
        <polygon points="0,0 130,0 0,92" fill="#FDE68A" stroke="#B45309" strokeWidth={4} strokeLinejoin="round" />
        <polygon points="18,16 82,16 18,62" fill="#FEFCE8" stroke="#B45309" strokeWidth={2.5} strokeLinejoin="round" />
      </g>

      {/* Lop 3: San go lop hoc sach se */}
      <rect x={0} y={745} width={1920} height={335} fill="url(#lopSan)" />
      {[815, 895, 980].map((sy) => (
        <line key={`lsan-${sy}`} x1={0} y1={sy} x2={1920} y2={sy} stroke="#78350F" strokeOpacity={0.45} strokeWidth={3} />
      ))}
    </g>
  );
};

/** 7. Bau troi dem vu tru: chom sao noi net hinh hoc, trang luoi liem, sao bang theo chu ky */
const BauTroiDemVuTru: React.FC<{ frame: number }> = ({ frame }) => {
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

  // Sao bang bay qua moi 110 frame
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

      {/* Lop 1: Bau troi dem sau + 48 ngoi sao nhap nhay tat dinh */}
      <rect x={0} y={0} width={1920} height={1080} fill="url(#demTroi)" />
      {Array.from({ length: 48 }).map((_, i) => {
        const sx = 40 + bamTatDinh(i * 19 + 3) * 1840;
        const sy = 40 + bamTatDinh(i * 31 + 7) * 620;
        const r = 1.6 + bamTatDinh(i * 11 + 5) * 2.6;
        const op = 0.45 + 0.55 * Math.abs(Math.sin(frame * 0.08 + i * 1.3));
        return <circle key={`sao-${i}`} cx={sx} cy={sy} r={r} fill="#FEF9C3" fillOpacity={op} />;
      })}

      {/* Lop 2: Chom sao hinh hoc noi net + trang luoi liem + sao bang */}
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

      {/* Mat trang luoi liem */}
      <g transform="translate(1660, 195)">
        <circle cx={0} cy={0} r={96} fill="#FEF08A" fillOpacity={0.12} />
        <path
          d="M 24 -56 A 62 62 0 1 0 24 56 A 48 48 0 1 1 24 -56 Z"
          fill="#FEF08A"
        />
      </g>

      {/* Sao bang chu ky */}
      {hienSaoBang && (
        <g opacity={Math.sin(tSb * Math.PI)}>
          <line x1={sbX} y1={sbY} x2={sbX + 165} y2={sbY - 56} stroke="#FEF08A" strokeWidth={4} strokeLinecap="round" />
          <line x1={sbX} y1={sbY} x2={sbX + 95} y2={sbY - 32} stroke="#FFFFFF" strokeWidth={2.5} strokeLinecap="round" />
          <circle cx={sbX} cy={sbY} r={5} fill="#FFFFFF" />
        </g>
      )}

      {/* Lop 3: Doi dem tien canh */}
      <path d="M 0 740 Q 480 650 960 720 Q 1480 780 1920 690 L 1920 1080 L 0 1080 Z" fill="#1E293B" />
      <path d="M 0 800 Q 520 740 1080 785 Q 1540 820 1920 760 L 1920 1080 L 0 1080 Z" fill="#0F172A" />
    </g>
  );
};

/** 8. Phong nen hai huoc: pastel/giay kraft toi gian kem duong tia vui nhon o goc */
const PhongNenHaiHuoc: React.FC<{ frame: number }> = ({ frame }) => {
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

      {/* Lop 1: Nen giay kem pastel am ap */}
      <rect x={0} y={0} width={1920} height={1080} fill="url(#haiNen)" />

      {/* Lop 2: Duong tia sunburst xoay cham vui nhon */}
      <g transform={`translate(960, 540) rotate(${xoay.toFixed(2)})`} opacity={0.28}>
        {Array.from({ length: 18 }).map((_, i) => {
          const a1 = (i / 18) * Math.PI * 2;
          const a2 = ((i + 0.45) / 18) * Math.PI * 2;
          const r = 1350;
          return (
            <polygon
              key={`tia-${i}`}
              points={`0,0 ${(Math.cos(a1) * r).toFixed(1)},${(Math.sin(a1) * r).toFixed(1)} ${(Math.cos(a2) * r).toFixed(1)},${(Math.sin(a2) * r).toFixed(1)}`}
              fill="#F59E0B"
            />
          );
        })}
      </g>

      {/* Cham bi comic nhe o 4 goc */}
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

      {/* Lop 3: Vung san dung toi gian cho nhan vat */}
      <ellipse cx={960} cy={805} rx={680} ry={62} fill="#F59E0B" fillOpacity={0.14} />
      <line x1={260} y1={805} x2={1660} y2={805} stroke="#D97706" strokeOpacity={0.35} strokeWidth={4} strokeDasharray="16 14" strokeLinecap="round" />
    </g>
  );
};

/** Lop phu thoi tiet tat dinh 100% theo frame (khong blur, khong Math.random) */
const LopThoiTiet: React.FC<{ thoiTiet?: LoaiThoiTiet; frame: number }> = ({
  thoiTiet,
  frame,
}) => {
  if (!thoiTiet || thoiTiet === 'khong') {
    return null;
  }

  switch (thoiTiet) {
    case 'nang_dep':
      return (
        <g pointerEvents="none">
          <polygon points="1220,0 1560,0 1120,1080 780,1080" fill="#FEF08A" fillOpacity={0.11} />
          <polygon points="1590,0 1840,0 1440,1080 1210,1080" fill="#FEF9C3" fillOpacity={0.09} />
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
          <rect x={0} y={0} width={1920} height={1080} fill="#F97316" fillOpacity={0.13} />
          <polygon points="1300,0 1920,0 1920,420 960,1080 620,1080" fill="#FDE68A" fillOpacity={0.09} />
        </g>
      );

    case 'ban_dem':
      return (
        <g pointerEvents="none">
          <rect x={0} y={0} width={1920} height={1080} fill="#0F172A" fillOpacity={0.14} />
          {Array.from({ length: 10 }).map((_, i) => {
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

    case 'mua_nhe':
      return (
        <g pointerEvents="none">
          <rect x={0} y={0} width={1920} height={1080} fill="#0F172A" fillOpacity={0.12} />
          {Array.from({ length: 44 }).map((_, i) => {
            const speed = 18 + (i % 4) * 4;
            const x0 = bamTatDinh(i * 29 + 1) * 2100;
            const y0 = bamTatDinh(i * 53 + 7) * 1160;
            const y = (y0 + frame * speed) % 1140 - 40;
            const x = ((x0 - frame * speed * 0.22) % 2040 + 2040) % 2040 - 60;
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

    case 'la_roi':
      return (
        <g pointerEvents="none">
          {Array.from({ length: 18 }).map((_, i) => {
            const x0 = bamTatDinh(i * 31 + 3) * 1920;
            const y0 = bamTatDinh(i * 47 + 11) * 1080;
            const speed = 2.4 + (i % 4) * 0.7;
            const y = (y0 + frame * speed) % 1140 - 30;
            const x = ((x0 + Math.sin(frame * 0.07 + i) * 58 + frame * 1.1) % 2020 + 2020) % 2020 - 50;
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

    case 'tuyet_roi':
      return (
        <g pointerEvents="none">
          {Array.from({ length: 36 }).map((_, i) => {
            const x0 = bamTatDinh(i * 19 + 5) * 1920;
            const y0 = bamTatDinh(i * 43 + 9) * 1080;
            const speed = 1.6 + (i % 4) * 0.55;
            const y = (y0 + frame * speed) % 1120 - 20;
            const x = ((x0 + Math.sin(frame * 0.05 + i * 1.7) * 32) % 1960 + 1960) % 1960 - 20;
            const r = 3.2 + (i % 3) * 2;
            return (
              <circle
                key={`tuyet-${i}`}
                cx={x}
                cy={y}
                r={r}
                fill="#FFFFFF"
                fillOpacity={0.82}
              />
            );
          })}
        </g>
      );

    default:
      return null;
  }
};

export const BoiCanhHoatHinh: React.FC<BoiCanhHoatHinhProps> = ({
  loai,
  thoiTiet = 'khong',
}) => {
  const frame = useCurrentFrame();

  const veBoiCanh = () => {
    switch (loai) {
      case 'bo_bien_hy_lap':
        return <BoBienHyLap frame={frame} laHoangHon={thoiTiet === 'hoang_hon'} />;
      case 'vuon_tao_dong_que':
        return <VuonTaoDongQue frame={frame} />;
      case 'pho_co_chau_au':
        return <PhoCoChauAu frame={frame} />;
      case 'rung_nui_thien_nhien':
        return <RungNuiThienNhien frame={frame} />;
      case 'thu_vien_co_dien':
        return <ThuVienCoDien frame={frame} />;
      case 'lop_hoc_bang_xanh':
        return <LopHocBangXanh frame={frame} />;
      case 'bau_troi_dem_vu_tru':
        return <BauTroiDemVuTru frame={frame} />;
      case 'phong_nen_hai_huoc':
      default:
        return <PhongNenHaiHuoc frame={frame} />;
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
      <LopThoiTiet thoiTiet={thoiTiet} frame={frame} />
    </svg>
  );
};
