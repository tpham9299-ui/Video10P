import React from 'react';
import { bamTatDinh } from '../vfx/tat_dinh';
import {
  CumMay,
  DaiSongCuon,
  type ParallaxOffset,
} from './BoiCanhHoatHinh';

type BoiCanhMoiProps = {
  frame: number;
  px: ParallaxOffset;
  laHoangHon?: boolean;
};

// =============================================================================
// 13. NHA CO PHONG SINH (nha truyen thong, anh den am, khung cua so, noi em be)
// =============================================================================
const NhaCoPhongSinhLop1Tinh = React.memo(() => (
  <g>
    <rect x={-260} y={-120} width={2440} height={840} fill="#78350F" />
    {/* Cua so go nhin ra vuon & bau troi am ap */}
    <rect x={680} y={130} width={540} height={360} rx={12} fill="#BAE6FD" stroke="#451A03" strokeWidth={14} />
    <path d="M 686 410 Q 820 355 960 390 Q 1100 345 1214 395 L 1214 484 L 686 484 Z" fill="#4ADE80" />
    <ellipse cx={800} cy={385} rx={75} ry={48} fill="#16A34A" />
    <ellipse cx={1115} cy={380} rx={82} ry={52} fill="#15803D" />
    {/* Song cua so go */}
    <line x1={950} y1={130} x2={950} y2={490} stroke="#451A03" strokeWidth={10} />
    <line x1={680} y1={310} x2={1220} y2={310} stroke="#451A03" strokeWidth={10} />
  </g>
));

const NhaCoPhongSinhLop2Tinh = React.memo(() => (
  <g>
    {/* Tuong go op am ap 2 ben cua so */}
    <rect x={-220} y={-80} width={900} height={810} fill="#92400E" />
    <rect x={1220} y={-80} width={920} height={810} fill="#92400E" />
    <rect x={680} y={-80} width={540} height={210} fill="#92400E" />
    <rect x={680} y={490} width={540} height={240} fill="#92400E" />
    {/* Vien go trang tri & rem cua vai kem */}
    <rect x={654} y={114} width={592} height={20} rx={6} fill="#451A03" />
    <path d="M 672 134 Q 724 270 678 498 L 656 498 L 656 134 Z" fill="#FEF3C7" stroke="#D97706" strokeWidth={3} />
    <path d="M 1228 134 Q 1176 270 1222 498 L 1244 498 L 1244 134 Z" fill="#FEF3C7" stroke="#D97706" strokeWidth={3} />
    {/* Tu go truyen thong & tranh treo tuong ben trai */}
    <rect x={145} y={175} width={220} height={160} rx={8} fill="#FEF3C7" stroke="#451A03" strokeWidth={8} />
    <path d="M 165 305 Q 230 245 280 285 Q 320 250 350 305 Z" fill="#B45309" fillOpacity={0.45} />
    <circle cx={295} cy={225} r={22} fill="#F59E0B" fillOpacity={0.65} />
    <rect x={120} y={500} width={330} height={218} rx={10} fill="#78350F" stroke="#451A03" strokeWidth={6} />
    <line x1={285} y1={504} x2={285} y2={714} stroke="#451A03" strokeWidth={4} />
    <circle cx={265} cy={610} r={6} fill="#FACC15" />
    <circle cx={305} cy={610} r={6} fill="#FACC15" />
    {/* Luong anh sang am phang tu den tran (khong blur) */}
    <polygon points="860,62 1060,62 1360,720 560,720" fill="#FEF08A" fillOpacity={0.1} />
  </g>
));

const NhaCoPhongSinhLop3Tinh = React.memo(() => (
  <g>
    <rect x={-180} y={712} width={2280} height={450} fill="#B45309" />
    <rect x={-180} y={704} width={2280} height={14} fill="#D97706" />
    {[775, 845, 920, 1005].map((sy) => (
      <line key={`nc-s-${sy}`} x1={-180} y1={sy} x2={2100} y2={sy} stroke="#78350F" strokeWidth={3} />
    ))}
    {/* Tham tron det tay am ap giua phong */}
    <ellipse cx={960} cy={830} rx={440} ry={66} fill="#FEF3C7" fillOpacity={0.85} stroke="#D97706" strokeWidth={6} />
    <ellipse cx={960} cy={830} rx={360} ry={48} fill="none" stroke="#EA580C" strokeOpacity={0.45} strokeWidth={4} strokeDasharray="14 10" />
  </g>
));

export const NhaCoPhongSinh: React.FC<BoiCanhMoiProps> = ({ frame, px }) => {
  const lacNoi = Math.sin(frame * 0.085) * 4.2;
  const nhipDen = 1 + Math.sin(frame * 0.16) * 0.06;
  return (
    <g>
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <NhaCoPhongSinhLop1Tinh />
        <CumMay xGoc={740} y={205} tiLe={0.55} tocDo={0.22} frame={frame} />
      </g>
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        <NhaCoPhongSinhLop2Tinh />
        {/* Den long treo tran phat sang am phang */}
        <g transform="translate(960, 48)">
          <line x1={0} y1={-90} x2={0} y2={0} stroke="#451A03" strokeWidth={6} />
          <circle cx={0} cy={22} r={74 * nhipDen} fill="#FACC15" fillOpacity={0.14} />
          <path d="M -56 16 Q 0 -18 56 16 Z" fill="#F59E0B" stroke="#78350F" strokeWidth={4} />
          <circle cx={0} cy={22} r={16} fill="#FEF08A" />
        </g>
      </g>
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <NhaCoPhongSinhLop3Tinh />
        {/* Noi em be bap benh em ai ben phai */}
        <g transform={`translate(1485, 735) rotate(${lacNoi.toFixed(2)}, 0, 52)`}>
          <path d="M -98 46 Q 0 78 98 46" fill="none" stroke="#78350F" strokeWidth={9} strokeLinecap="round" />
          <line x1={-56} y1={24} x2={-56} y2={56} stroke="#78350F" strokeWidth={7} />
          <line x1={56} y1={24} x2={56} y2={56} stroke="#78350F" strokeWidth={7} />
          <path d="M -88 -26 L 88 -26 L 74 36 L -74 36 Z" fill="#D97706" stroke="#451A03" strokeWidth={5} strokeLinejoin="round" />
          {[-50, -18, 18, 50].map((nx) => (
            <line key={`nc-n-${nx}`} x1={nx} y1={-22} x2={nx * 0.85} y2={32} stroke="#92400E" strokeWidth={4} />
          ))}
          <path d="M -72 -26 Q 0 -48 72 -26 Z" fill="#FEF08A" stroke="#CA8A04" strokeWidth={3} />
          <circle cx={-28} cy={-38} r={16} fill="#FDE68A" stroke="#78350F" strokeWidth={3} />
          <path d="M -34 -39 Q -28 -35 -22 -39" fill="none" stroke="#78350F" strokeWidth={2.2} strokeLinecap="round" />
        </g>
      </g>
    </g>
  );
};

// =============================================================================
// 14. CANG BIEN TAU THUY (ben cang, tau thuy vien duong, song nuoc, cot den/cau cang)
// =============================================================================
const CangBienLop1Tinh = React.memo<{ laHoangHon: boolean }>(({ laHoangHon }) => (
  <g>
    <defs>
      <linearGradient id="cbTroi" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor={laHoangHon ? '#EA580C' : '#0284C7'} />
        <stop offset="55%" stopColor={laHoangHon ? '#FB923C' : '#38BDF8'} />
        <stop offset="100%" stopColor={laHoangHon ? '#FDE68A' : '#E0F2FE'} />
      </linearGradient>
    </defs>
    <rect x={-260} y={-120} width={2440} height={720} fill="url(#cbTroi)" />
    <g transform="translate(460, 195)">
      <circle cx={0} cy={0} r={118} fill="#FEF08A" fillOpacity={0.18} />
      <circle cx={0} cy={0} r={62} fill="#FFFBEB" />
    </g>
  </g>
));

const CangBienLop2Tinh = React.memo(() => (
  <g>
    <defs>
      <linearGradient id="cbBien" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#0369A1" />
        <stop offset="100%" stopColor="#0C4A6E" />
      </linearGradient>
    </defs>
    {/* Ngon hai dang & bo de chan song xa ben trai */}
    <path d="M -220 520 L 340 520 L 390 560 L -220 560 Z" fill="#64748B" />
    <g transform="translate(215, 360)">
      <polygon points="-22,160 -12,0 12,0 22,160" fill="#F8FAFC" stroke="#334155" strokeWidth={3} />
      <rect x={-16} y={40} width={32} height={24} fill="#DC2626" />
      <rect x={-19} y={96} width={38} height={24} fill="#DC2626" />
      <rect x={-18} y={-24} width={36} height={24} rx={4} fill="#FEF08A" stroke="#1E293B" strokeWidth={3} />
      <polygon points="-22,-24 22,-24 0,-46" fill="#DC2626" />
    </g>
    <rect x={-260} y={530} width={2440} height={280} fill="url(#cbBien)" />
  </g>
));

const CangBienLop3Tinh = React.memo(() => (
  <g>
    {/* Cau cang go & cot neo tau tien canh */}
    <rect x={-180} y={705} width={2280} height={450} fill="#78350F" />
    <rect x={-180} y={695} width={2280} height={20} fill="#B45309" stroke="#451A03" strokeWidth={3} />
    {[760, 825, 895, 975].map((y) => (
      <line key={`cb-pl-${y}`} x1={-180} y1={y} x2={2100} y2={y} stroke="#451A03" strokeWidth={3.5} />
    ))}
    {/* Cot neo tau (bollards) & day thung */}
    {[320, 940, 1580].map((bx) => (
      <g key={`bollard-${bx}`} transform={`translate(${bx}, 712)`}>
        <rect x={-20} y={-34} width={40} height={38} rx={6} fill="#334155" stroke="#0F172A" strokeWidth={3} />
        <rect x={-28} y={-44} width={56} height={14} rx={5} fill="#475569" stroke="#0F172A" strokeWidth={3} />
      </g>
    ))}
    {/* 2 cot den cang ben trai va phai */}
    {[160, 1760].map((lx) => (
      <g key={`cb-den-${lx}`} transform={`translate(${lx}, 702)`}>
        <rect x={-8} y={-320} width={16} height={320} fill="#1E293B" />
        <path d="M -20 0 L 20 0 L 14 -36 L -14 -36 Z" fill="#334155" />
        <rect x={-22} y={-352} width={44} height={36} rx={6} fill="#FEF08A" stroke="#1E293B" strokeWidth={3.5} />
        <polygon points="-28,-352 28,-352 0,-376" fill="#0F172A" />
      </g>
    ))}
  </g>
));

export const CangBienTauThuy: React.FC<BoiCanhMoiProps> = ({ frame, px, laHoangHon = false }) => {
  const tauY = 472 + Math.sin(frame * 0.08) * 5;
  const tauLac = Math.sin(frame * 0.08 + 0.6) * 1.4;
  return (
    <g>
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <CangBienLop1Tinh laHoangHon={laHoangHon} />
        <CumMay xGoc={180} y={115} tiLe={1.25} tocDo={0.36} frame={frame} />
        <CumMay xGoc={1120} y={145} tiLe={1.05} tocDo={0.28} frame={frame} />
      </g>
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        <CangBienLop2Tinh />
        {/* Tau thuy vien duong lon bobbing + cum khoi bay len */}
        <g transform={`translate(1180, ${tauY.toFixed(1)}) rotate(${tauLac.toFixed(2)})`}>
          {[0, 1, 2].map((ki) => {
            const p = ((frame * 0.018 + ki / 3) % 1 + 1) % 1;
            return (
              <circle
                key={`tau-k-${ki}`}
                cx={-60 - p * 115}
                cy={-160 - p * 85}
                r={16 + p * 26}
                fill="#E2E8F0"
                fillOpacity={((1 - p) * 0.55).toFixed(2)}
              />
            );
          })}
          {/* 2 ong khoi do-den */}
          <rect x={-95} y={-155} width={44} height={74} rx={5} fill="#DC2626" stroke="#1E293B" strokeWidth={4} />
          <rect x={-95} y={-155} width={44} height={18} fill="#1E293B" />
          <rect x={15} y={-145} width={44} height={64} rx={5} fill="#DC2626" stroke="#1E293B" strokeWidth={4} />
          <rect x={15} y={-145} width={44} height={18} fill="#1E293B" />
          {/* Tang cabin trang */}
          <rect x={-215} y={-84} width={420} height={62} rx={10} fill="#F8FAFC" stroke="#334155" strokeWidth={4} />
          <rect x={-165} y={-114} width={290} height={32} rx={6} fill="#FFFFFF" stroke="#475569" strokeWidth={3.5} />
          {/* Than tau lon */}
          <path d="M -310 -22 L 340 -22 L 285 78 L -265 78 Z" fill="#1E293B" stroke="#0F172A" strokeWidth={4} />
          <line x1={-292} y1={24} x2={316} y2={24} stroke="#EF4444" strokeWidth={10} />
          {[-180, -120, -60, 0, 60, 120, 180].map((pxC) => (
            <circle key={`ct-${pxC}`} cx={pxC} cy={-54} r={9} fill="#38BDF8" stroke="#1E293B" strokeWidth={2.5} />
          ))}
        </g>
        <DaiSongCuon y={568} bienDo={5} buocSong={170} tocDo={1.1} frame={frame} mau="#E0F2FE" doMo={0.45} doDay={3} />
        <DaiSongCuon y={618} bienDo={6.5} buocSong={200} tocDo={1.55} frame={frame} mau="#BAE6FD" doMo={0.48} doDay={3.5} />
        <DaiSongCuon y={672} bienDo={7.5} buocSong={230} tocDo={1.95} frame={frame} mau="#E0F2FE" doMo={0.42} doDay={4} />
      </g>
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <CangBienLop3Tinh />
      </g>
    </g>
  );
};

// =============================================================================
// 15. PHONG TRO BEP LUA (phong nho, ban go, bep nau an noi sup, gia sach nho)
// =============================================================================
const PhongTroLop1Tinh = React.memo(() => (
  <g>
    <rect x={-260} y={-120} width={2440} height={860} fill="#7C2D12" />
    {/* Cua so nho nhin ra troi chieu */}
    <rect x={770} y={135} width={380} height={275} rx={8} fill="#7DD3FC" stroke="#451A03" strokeWidth={12} />
    <rect x={776} y={295} width={368} height={110} fill="#FDE68A" fillOpacity={0.5} />
    <line x1={960} y1={135} x2={960} y2={410} stroke="#451A03" strokeWidth={8} />
    <line x1={770} y1={270} x2={1150} y2={270} stroke="#451A03" strokeWidth={8} />
  </g>
));

const PhongTroLop2Tinh = React.memo(() => (
  <g>
    {/* Tuong gach/vua am & gia sach nho ben trai */}
    <rect x={-220} y={-80} width={990} height={810} fill="#9A3412" fillOpacity={0.62} />
    <rect x={1150} y={-80} width={990} height={810} fill="#9A3412" fillOpacity={0.62} />
    {/* Gia sach nho treo tuong */}
    <g transform="translate(150, 155)">
      <rect x={0} y={0} width={320} height={255} rx={8} fill="#451A03" stroke="#78350F" strokeWidth={6} />
      {[0, 1].map((tang) => (
        <g key={`pt-t-${tang}`} transform={`translate(16, ${24 + tang * 116})`}>
          <rect x={0} y={0} width={288} height={92} fill="#291205" />
          {[0, 1, 2, 3, 4, 5, 6, 7].map((bi) => (
            <rect
              key={`pt-b-${bi}`}
              x={10 + bi * 34}
              y={14 + (bi % 3) * 8}
              width={24}
              height={78 - (bi % 3) * 8}
              rx={3}
              fill={['#DC2626', '#2563EB', '#15803D', '#D97706'][bi % 4]}
              stroke="#1C1917"
              strokeWidth={1.5}
            />
          ))}
        </g>
      ))}
    </g>
    {/* Ban go nho hoc bai ben trai */}
    <g transform="translate(360, 625)">
      <rect x={-175} y={0} width={350} height={20} rx={5} fill="#B45309" stroke="#451A03" strokeWidth={4} />
      <rect x={-148} y={20} width={18} height={95} fill="#78350F" />
      <rect x={130} y={20} width={18} height={95} fill="#78350F" />
      {/* Cuon so tay mo tren ban */}
      <rect x={-110} y={-14} width={96} height={14} rx={3} fill="#FEF3C7" stroke="#92400E" strokeWidth={2.5} />
    </g>
  </g>
));

const PhongTroLop3Tinh = React.memo(() => (
  <g>
    <rect x={-180} y={718} width={2280} height={445} fill="#5C3A21" />
    <rect x={-180} y={710} width={2280} height={14} fill="#78350F" />
    {/* Bep nau an gach cu + noi sup ben phai */}
    <g transform="translate(1525, 685)">
      <rect x={-145} y={-35} width={290} height={140} rx={10} fill="#78350F" stroke="#451A03" strokeWidth={5} />
      <path d="M -68 105 L -68 35 A 68 58 0 0 1 68 35 L 68 105 Z" fill="#1C1917" stroke="#451A03" strokeWidth={4} />
      {/* Noi sup dat tren bep */}
      <path d="M -56 -88 L 56 -88 L 50 -36 L -50 -36 Z" fill="#334155" stroke="#0F172A" strokeWidth={4} />
      <ellipse cx={0} cy={-88} rx={56} ry={12} fill="#F59E0B" stroke="#0F172A" strokeWidth={3.5} />
    </g>
  </g>
));

export const PhongTroBepLua: React.FC<BoiCanhMoiProps> = ({ frame, px }) => {
  const lua = Math.sin(frame * 0.34) * 5;
  return (
    <g>
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <PhongTroLop1Tinh />
        <CumMay xGoc={840} y={190} tiLe={0.48} tocDo={0.18} frame={frame} />
      </g>
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        <PhongTroLop2Tinh />
      </g>
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <PhongTroLop3Tinh />
        {/* Ngon lua bep chay bap bung (khong blur) */}
        <g transform="translate(1525, 765)">
          <circle cx={0} cy={-18} r={54 + lua * 0.8} fill="#F97316" fillOpacity={0.18} />
          <path d={`M -34 20 Q -18 ${(-32 + lua).toFixed(1)} 0 -8 Q 18 ${(-42 - lua).toFixed(1)} 34 20 Z`} fill="#EA580C" />
          <path d={`M -20 20 Q 0 ${(-24 + lua * 0.6).toFixed(1)} 20 20 Z`} fill="#FACC15" />
        </g>
      </g>
    </g>
  );
};

// =============================================================================
// 16. PHONG BENH VIEN (giuong benh, tu dau giuong, cua so lon nhin ra tuyet/mua)
// =============================================================================
const PhongBenhVienLop1Tinh = React.memo(() => (
  <g>
    <defs>
      <linearGradient id="bvTroi" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#64748B" />
        <stop offset="100%" stopColor="#CBD5E1" />
      </linearGradient>
    </defs>
    {/* Khung canh tuyet/mua lanh gia ben ngoai cua so lon */}
    <rect x={650} y={95} width={620} height={460} fill="url(#bvTroi)" />
    <path d="M 650 450 Q 820 400 980 435 Q 1120 410 1270 445 L 1270 555 L 650 555 Z" fill="#F1F5F9" />
    {[760, 860, 1110, 1190].map((tx, i) => (
      <polygon key={`bv-c-${i}`} points={`${tx},355 ${tx - 34},450 ${tx + 34},450`} fill="#475569" />
    ))}
  </g>
));

const PhongBenhVienLop2Tinh = React.memo(() => (
  <g>
    {/* Tuong benh vien tong xanh bac ha / kem diu mat, chua o cua so o giua */}
    <path
      d="M -240 -100 H 2160 V 740 H -240 Z M 685 120 H 1235 V 530 H 685 Z"
      fill="#E2E8F0"
      fillRule="evenodd"
    />
    <rect x={-240} y={560} width={2400} height={180} fill="#CBD5E1" />
    <rect x={-240} y={554} width={2400} height={12} fill="#94A3B8" />
    {/* Khung cua so benh vien */}
    <rect x={685} y={120} width={550} height={410} rx={8} fill="none" stroke="#64748B" strokeWidth={14} />
    <line x1={960} y1={120} x2={960} y2={530} stroke="#64748B" strokeWidth={10} />
    <line x1={685} y1={325} x2={1235} y2={325} stroke="#64748B" strokeWidth={10} />
    {/* Bang theo doi benh an & khung anh nho */}
    <rect x={1440} y={185} width={190} height={240} rx={10} fill="#F8FAFC" stroke="#94A3B8" strokeWidth={6} />
    <polyline points="1465,305 1500,305 1518,260 1536,340 1554,285 1575,305 1605,305" fill="none" stroke="#0EA5E9" strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" />
  </g>
));

const PhongBenhVienLop3Tinh = React.memo(() => (
  <g>
    <rect x={-180} y={718} width={2280} height={445} fill="#CBD5E1" />
    <rect x={-180} y={712} width={2280} height={12} fill="#94A3B8" />
    {/* Giuong benh co dien ben phai */}
    <g transform="translate(1480, 742)">
      <path d="M -210 38 L -210 -128 Q -210 -150 -184 -150 L -162 -150 L -162 38" fill="none" stroke="#64748B" strokeWidth={12} strokeLinecap="round" />
      <path d="M 210 38 L 210 -78 Q 210 -98 186 -98 L 166 -98 L 166 38" fill="none" stroke="#64748B" strokeWidth={12} strokeLinecap="round" />
      <rect x={-196} y={-52} width={392} height={46} rx={10} fill="#FFFFFF" stroke="#94A3B8" strokeWidth={4} />
      <ellipse cx={-135} cy={-66} rx={48} ry={20} fill="#F8FAFC" stroke="#CBD5E1" strokeWidth={3} />
      <rect x={-95} y={-56} width={290} height={54} rx={8} fill="#38BDF8" fillOpacity={0.85} stroke="#0369A1" strokeWidth={4} />
      <rect x={-206} y={-4} width={412} height={16} rx={4} fill="#475569" />
    </g>
    {/* Tu dau giuong + lo thuoc & tach tra */}
    <g transform="translate(1150, 710)">
      <rect x={-56} y={-105} width={112} height={120} rx={8} fill="#F8FAFC" stroke="#64748B" strokeWidth={5} />
      <line x1={-46} y1={-48} x2={46} y2={-48} stroke="#94A3B8" strokeWidth={4} />
      <circle cx={0} cy={-76} r={5} fill="#64748B" />
      <circle cx={0} cy={-18} r={5} fill="#64748B" />
      <rect x={-28} y={-135} width={18} height={30} rx={4} fill="#38BDF8" stroke="#0369A1" strokeWidth={2.5} />
      <rect x={8} y={-126} width={24} height={21} rx={4} fill="#FEF3C7" stroke="#92400E" strokeWidth={2.5} />
    </g>
  </g>
));

export const PhongBenhVien: React.FC<BoiCanhMoiProps> = ({ px }) => (
  <g>
    <g transform={`translate(${(px.lop1X * 0.4).toFixed(1)}, ${(px.lop1Y * 0.3).toFixed(1)})`}>
      <PhongBenhVienLop1Tinh />
    </g>
    <g transform={`translate(${(px.lop2X * 0.5).toFixed(1)}, ${(px.lop2Y * 0.4).toFixed(1)})`}>
      <PhongBenhVienLop2Tinh />
    </g>
    <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
      <PhongBenhVienLop3Tinh />
    </g>
  </g>
);

// =============================================================================
// 17. DUONG PHO XE CO (pho co chau Au/Anh, den duong, xe taxi co, hang gach)
// =============================================================================
const DuongPhoXeCoLop1Tinh = React.memo<{ laHoangHon: boolean }>(({ laHoangHon }) => (
  <g>
    <defs>
      <linearGradient id="dpTroi" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor={laHoangHon ? '#9A3412' : '#475569'} />
        <stop offset="55%" stopColor={laHoangHon ? '#F97316' : '#94A3B8'} />
        <stop offset="100%" stopColor={laHoangHon ? '#FDE68A' : '#E2E8F0'} />
      </linearGradient>
    </defs>
    <rect x={-260} y={-120} width={2440} height={740} fill="url(#dpTroi)" />
  </g>
));

const DuongPhoXeCoLop2Tinh = React.memo(() => {
  const nhaGach = [
    { x: -80, w: 260, h: 430, mau: '#9A3412', mai: '#334155' },
    { x: 175, w: 245, h: 375, mau: '#B45309', mai: '#1E293B' },
    { x: 415, w: 280, h: 450, mau: '#7C2D12', mai: '#334155' },
    { x: 690, w: 255, h: 390, mau: '#92400E', mai: '#1E293B' },
    { x: 940, w: 290, h: 445, mau: '#9A3412', mai: '#334155' },
    { x: 1225, w: 260, h: 385, mau: '#78350F', mai: '#1E293B' },
    { x: 1480, w: 275, h: 435, mau: '#B45309', mai: '#334155' },
    { x: 1750, w: 280, h: 405, mau: '#7C2D12', mai: '#1E293B' },
  ];
  return (
    <g>
      {nhaGach.map((n, idx) => {
        const ty = 670 - n.h;
        return (
          <g key={`dp-n-${idx}`}>
            <rect x={n.x} y={ty} width={n.w} height={n.h} fill={n.mau} stroke="#451A03" strokeWidth={3.5} />
            <rect x={n.x - 8} y={ty - 22} width={n.w + 16} height={26} fill={n.mai} />
            {/* Ong khoi gach kieu Anh */}
            <rect x={n.x + 34} y={ty - 64} width={34} height={44} fill="#78350F" stroke="#1E293B" strokeWidth={2.5} />
            {[0, 1, 2].map((r) =>
              [0, 1, 2].map((c) => (
                <rect
                  key={`dp-w-${idx}-${r}-${c}`}
                  x={n.x + 28 + c * 74}
                  y={ty + 42 + r * 92}
                  width={44}
                  height={56}
                  rx={4}
                  fill={(idx + r + c) % 3 === 0 ? '#FEF08A' : '#CBD5E1'}
                  stroke="#1E293B"
                  strokeWidth={2.5}
                />
              )),
            )}
          </g>
        );
      })}
    </g>
  );
});

const DuongPhoXeCoLop3Tinh = React.memo(() => (
  <g>
    {/* Via he & mat duong lat gach co */}
    <rect x={-180} y={668} width={2280} height={68} fill="#CBD5E1" stroke="#64748B" strokeWidth={3} />
    <rect x={-180} y={736} width={2280} height={425} fill="#475569" />
    <line x1={-180} y1={850} x2={2100} y2={850} stroke="#FACC15" strokeWidth={7} strokeDasharray="48 34" />
    {Array.from({ length: 18 }).map((_, i) => (
      <rect
        key={`dp-g-${i}`}
        x={20 + i * 112 + (i % 2) * 18}
        y={762 + (i % 3) * 58}
        width={64}
        height={18}
        rx={6}
        fill="#334155"
        fillOpacity={0.45}
      />
    ))}
    {/* 3 cot den duong sat co kieu London */}
    {[220, 960, 1700].map((lx) => (
      <g key={`dp-l-${lx}`} transform={`translate(${lx}, 682)`}>
        <rect x={-7} y={-285} width={14} height={285} fill="#0F172A" />
        <path d="M -18 0 L 18 0 L 12 -34 L -12 -34 Z" fill="#1E293B" />
        <polygon points="-20,-282 20,-282 26,-318 -26,-318" fill="#FEF08A" stroke="#0F172A" strokeWidth={3.5} />
        <polygon points="-28,-318 28,-318 0,-340" fill="#0F172A" />
      </g>
    ))}
  </g>
));

export const DuongPhoXeCo: React.FC<BoiCanhMoiProps> = ({ frame, px, laHoangHon = false }) => {
  const sangDen = 0.16 + 0.04 * Math.sin(frame * 0.12);
  return (
    <g>
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <DuongPhoXeCoLop1Tinh laHoangHon={laHoangHon} />
        <CumMay xGoc={220} y={110} tiLe={1.15} tocDo={0.28} frame={frame} mau="#F1F5F9" doMo={0.8} />
        <CumMay xGoc={1160} y={135} tiLe={1.0} tocDo={0.22} frame={frame} mau="#E2E8F0" doMo={0.75} />
      </g>
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        <DuongPhoXeCoLop2Tinh />
      </g>
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <DuongPhoXeCoLop3Tinh />
        {[220, 960, 1700].map((lx) => (
          <circle key={`dp-g-${lx}`} cx={lx} cy={382} r={54} fill="#FEF08A" fillOpacity={sangDen} />
        ))}
      </g>
    </g>
  );
};

// =============================================================================
// 18. GIANG DUONG DAI HOC (bang den lon, buc giang, day ghe sinh vien, cua vom)
// =============================================================================
const GiangDuongDaiHocLop1Tinh = React.memo(() => (
  <g>
    <rect x={-260} y={-120} width={2440} height={860} fill="#3F2E21" />
    {/* 2 cua so vom lon hai ben nhin ra troi sang */}
    {[175, 1745].map((wx) => (
      <g key={`gddh-w-${wx}`} transform={`translate(${wx}, 105)`}>
        <path d="M -92 470 L -92 125 A 92 92 0 0 1 92 125 L 92 470 Z" fill="#BAE6FD" stroke="#78350F" strokeWidth={12} />
        <line x1={0} y1={34} x2={0} y2={470} stroke="#78350F" strokeWidth={8} />
        <line x1={-90} y1={210} x2={90} y2={210} stroke="#78350F" strokeWidth={8} />
        <line x1={-90} y1={345} x2={90} y2={345} stroke="#78350F" strokeWidth={8} />
      </g>
    ))}
  </g>
));

const GiangDuongDaiHocLop2Tinh = React.memo(() => (
  <g>
    {/* Tuong op go co dien dai hoc & bang den doi co lon */}
    <rect x={310} y={-60} width={1300} height={780} fill="#5C3A21" stroke="#451A03" strokeWidth={6} />
    <rect x={370} y={92} width={1180} height={470} rx={12} fill="#0F2922" stroke="#92400E" strokeWidth={16} />
    <rect x={390} y={112} width={1140} height={430} rx={6} fill="#11382C" />
    <line x1={960} y1={112} x2={960} y2={542} stroke="#92400E" strokeWidth={6} strokeOpacity={0.6} />
    {/* Khay phan go */}
    <rect x={356} y={556} width={1208} height={22} rx={5} fill="#B45309" stroke="#451A03" strokeWidth={3} />
    {/* Luong nang xien tu cua vom (phang khong blur) */}
    <polygon points="85,180 265,180 560,720 180,720" fill="#FEF9C3" fillOpacity={0.11} />
  </g>
));

const GiangDuongDaiHocLop3Tinh = React.memo(() => (
  <g>
    {/* San go & buc giang + hang ghe sinh vien phia duoi */}
    <rect x={-180} y={715} width={2280} height={445} fill="#78350F" />
    <rect x={-180} y={708} width={2280} height={14} fill="#B45309" />
    {/* Buc giang giao su ben phai */}
    <g transform="translate(1545, 728)">
      <rect x={-72} y={-148} width={144} height={148} rx={6} fill="#92400E" stroke="#451A03" strokeWidth={5} />
      <polygon points="-86,-148 86,-168 90,-148 -82,-130" fill="#B45309" stroke="#451A03" strokeWidth={4} />
    </g>
    {/* Day ghe sinh vien bac thang o mep duoi tien canh */}
    <g transform="translate(0, 960)">
      <rect x={80} y={0} width={1760} height={32} rx={6} fill="#451A03" stroke="#291205" strokeWidth={4} />
      {[210, 490, 770, 1050, 1330, 1610].map((gx) => (
        <rect key={`sv-g-${gx}`} x={gx} y={-24} width={130} height={24} rx={6} fill="#78350F" stroke="#451A03" strokeWidth={3} />
      ))}
    </g>
  </g>
));

export const GiangDuongDaiHoc: React.FC<BoiCanhMoiProps> = ({ frame, px }) => {
  const hatBui = Math.sin(frame * 0.06) * 8;
  return (
    <g>
      <g transform={`translate(${(px.lop1X * 0.4).toFixed(1)}, ${(px.lop1Y * 0.3).toFixed(1)})`}>
        <GiangDuongDaiHocLop1Tinh />
      </g>
      <g transform={`translate(${(px.lop2X * 0.5).toFixed(1)}, ${(px.lop2Y * 0.4).toFixed(1)})`}>
        <GiangDuongDaiHocLop2Tinh />
        <circle cx={290 + hatBui} cy={310} r={3.5} fill="#FEF9C3" fillOpacity={0.55} />
        <circle cx={380 - hatBui} cy={430} r={3} fill="#FEF9C3" fillOpacity={0.48} />
      </g>
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <GiangDuongDaiHocLop3Tinh />
      </g>
    </g>
  );
};

// =============================================================================
// 19. SAN TRUONG CO DIEN (kien truc vom da kieu Cambridge, thap dong ho, hoang hon/ban ngay)
// =============================================================================
const SanTruongLop1Tinh = React.memo<{ laHoangHon: boolean }>(({ laHoangHon }) => (
  <g>
    <defs>
      <linearGradient id="stTroi" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor={laHoangHon ? '#C2410C' : '#0284C7'} />
        <stop offset="55%" stopColor={laHoangHon ? '#FB923C' : '#7DD3FC'} />
        <stop offset="100%" stopColor={laHoangHon ? '#FDE68A' : '#FEF3C7'} />
      </linearGradient>
    </defs>
    <rect x={-260} y={-120} width={2440} height={740} fill="url(#stTroi)" />
    <circle cx={460} cy={laHoangHon ? 360 : 185} r={58} fill="#FFFBEB" />
    <circle cx={460} cy={laHoangHon ? 360 : 185} r={108} fill="#FEF08A" fillOpacity={0.2} />
  </g>
));

const SanTruongLop2Tinh = React.memo(() => (
  <g>
    {/* Day nha hoc vien da vang co dien kieu Cambridge */}
    <rect x={-180} y={330} width={2280} height={360} fill="#E7D3B1" stroke="#A88B62" strokeWidth={4} />
    <polygon points="-200,330 200,250 1720,250 2120,330" fill="#64748B" stroke="#334155" strokeWidth={4} />
    {/* Hang vom da Gothic dac trung */}
    {[110, 320, 530, 1280, 1490, 1700].map((ax) => (
      <g key={`cam-v-${ax}`} transform={`translate(${ax}, 450)`}>
        <path d="M -68 238 L -68 62 Q -68 0 0 -18 Q 68 0 68 62 L 68 238 Z" fill="#475569" stroke="#A88B62" strokeWidth={6} />
        <path d="M -52 238 L -52 72 Q -52 22 0 6 Q 52 22 52 72 L 52 238 Z" fill="#334155" />
      </g>
    ))}
    {/* Thap dong ho trung tam hung vi */}
    <g transform="translate(910, 115)">
      <rect x={-125} y={110} width={250} height={470} fill="#D6BE96" stroke="#8C7352" strokeWidth={5} />
      <polygon points="-145,112 0,-42 145,112" fill="#475569" stroke="#1E293B" strokeWidth={4} strokeLinejoin="round" />
      <rect x={-14} y={-82} width={28} height={46} fill="#334155" />
      <circle cx={0} cy={-94} r={10} fill="#FACC15" />
      {/* Cua cong lon duoi chan thap */}
      <path d="M -78 576 L -78 415 Q -78 345 0 322 Q 78 345 78 415 L 78 576 Z" fill="#1E293B" stroke="#8C7352" strokeWidth={8} />
    </g>
  </g>
));

const SanTruongLop3Tinh = React.memo(() => (
  <g>
    {/* San da & tham co xanh cat tia vuong vuc kieu Dai hoc Anh */}
    <rect x={-180} y={688} width={2280} height={470} fill="#CBD5E1" />
    <rect x={-180} y={680} width={2280} height={16} fill="#E2E8F0" stroke="#94A3B8" strokeWidth={2.5} />
    <polygon points="80,730 740,730 620,960 -60,960" fill="#22C55E" stroke="#15803D" strokeWidth={4} />
    <polygon points="1180,730 1840,730 1980,960 1300,960" fill="#22C55E" stroke="#15803D" strokeWidth={4} />
    {[760, 840, 930, 1020].map((ly) => (
      <line key={`st-l-${ly}`} x1={650} y1={ly} x2={1270} y2={ly} stroke="#94A3B8" strokeOpacity={0.55} strokeWidth={3} />
    ))}
  </g>
));

export const SanTruongCoDien: React.FC<BoiCanhMoiProps> = ({ frame, px, laHoangHon = false }) => {
  const gocKimPhut = (frame * 0.45) % 360;
  return (
    <g>
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <SanTruongLop1Tinh laHoangHon={laHoangHon} />
        <CumMay xGoc={180} y={115} tiLe={1.2} tocDo={0.32} frame={frame} mau={laHoangHon ? '#FFEDD5' : '#FFFFFF'} />
        <CumMay xGoc={1240} y={135} tiLe={1.0} tocDo={0.24} frame={frame} mau={laHoangHon ? '#FED7AA' : '#FFFFFF'} />
      </g>
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        <SanTruongLop2Tinh />
        {/* Mat dong ho co kim quay tren thap */}
        <g transform="translate(910, 315)">
          <circle cx={0} cy={0} r={58} fill="#FFFBEB" stroke="#92400E" strokeWidth={8} />
          <line x1={0} y1={0} x2={0} y2={-30} stroke="#0F172A" strokeWidth={5} strokeLinecap="round" />
          <line
            x1={0}
            y1={0}
            x2={(Math.sin((gocKimPhut * Math.PI) / 180) * 40).toFixed(1)}
            y2={(-Math.cos((gocKimPhut * Math.PI) / 180) * 40).toFixed(1)}
            stroke="#DC2626"
            strokeWidth={3.5}
            strokeLinecap="round"
          />
          <circle cx={0} cy={0} r={6} fill="#0F172A" />
        </g>
      </g>
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <SanTruongLop3Tinh />
      </g>
    </g>
  );
};

// =============================================================================
// 20. PHONG THI NGHIEM CO (ban thi nghiem, dung cu do dac, kinh lup, so ghi chep)
// =============================================================================
const PhongThiNghiemLop1Tinh = React.memo(() => (
  <g>
    <rect x={-260} y={-120} width={2440} height={860} fill="#1E293B" />
    {/* Cua so vom cao phia sau */}
    <path d="M 760 540 L 760 190 A 200 175 0 0 1 1160 190 L 1160 540 Z" fill="#0F172A" stroke="#64748B" strokeWidth={12} />
    <path d="M 772 530 L 772 195 A 188 164 0 0 1 1148 195 L 1148 530 Z" fill="#38BDF8" fillOpacity={0.28} />
    <line x1={960} y1={32} x2={960} y2={536} stroke="#64748B" strokeWidth={8} />
    <line x1={768} y1={265} x2={1152} y2={265} stroke="#64748B" strokeWidth={8} />
  </g>
));

const PhongThiNghiemLop2Tinh = React.memo(() => (
  <g>
    {/* Ke go dung lo thuy tinh, thuoc do goc, ban ve ky thuat */}
    {[130, 1400].map((kx, ki) => (
      <g key={`ptn-k-${ki}`} transform={`translate(${kx}, 145)`}>
        <rect x={0} y={0} width={380} height={510} rx={10} fill="#334155" stroke="#475569" strokeWidth={6} />
        {[0, 1, 2].map((r) => (
          <g key={`ptn-r-${r}`} transform={`translate(22, ${28 + r * 156})`}>
            <rect x={0} y={0} width={336} height={124} fill="#1E293B" />
            {/* Binh thuy tinh & dung cu do dac */}
            <path d="M 38 118 L 58 46 L 78 46 L 98 118 Z" fill="#38BDF8" fillOpacity={0.45} stroke="#BAE6FD" strokeWidth={3} />
            <rect x={140} y={56} width={34} height={62} rx={6} fill="#FACC15" fillOpacity={0.4} stroke="#FEF08A" strokeWidth={3} />
            <circle cx={245} cy={88} r={28} fill="#4ADE80" fillOpacity={0.35} stroke="#86EFAC" strokeWidth={3} />
            <rect x={-6} y={120} width={348} height={12} fill="#78350F" />
          </g>
        ))}
      </g>
    ))}
    {/* Bang ve so do hinh hoc treo tuong */}
    <rect x={545} y={140} width={185} height={240} rx={6} fill="#FEF3C7" stroke="#92400E" strokeWidth={6} />
    <circle cx={638} cy={240} r={54} fill="none" stroke="#B45309" strokeWidth={3} />
    <polygon points="638,186 688,284 588,284" fill="none" stroke="#1E3A8A" strokeWidth={3} />
  </g>
));

const PhongThiNghiemLop3Tinh = React.memo(() => (
  <g>
    <rect x={-180} y={718} width={2280} height={445} fill="#475569" />
    <rect x={-180} y={710} width={2280} height={14} fill="#64748B" />
    {/* Ban thi nghiem lon co so ghi chep & kinh lup ben phai */}
    <g transform="translate(1480, 685)">
      <rect x={-210} y={0} width={420} height={26} rx={6} fill="#78350F" stroke="#451A03" strokeWidth={4} />
      <rect x={-182} y={26} width={24} height={120} fill="#451A03" />
      <rect x={158} y={26} width={24} height={120} fill="#451A03" />
      {/* So ghi chep mo */}
      <polygon points="-145,0 -55,0 -48,-18 -138,-18" fill="#FEF3C7" stroke="#92400E" strokeWidth={3} />
      <polygon points="-55,0 35,0 42,-18 -48,-18" fill="#FFFBEB" stroke="#92400E" strokeWidth={3} />
      {/* Kinh lup dat tren ban */}
      <g transform="translate(95, -24) rotate(-25)">
        <line x1={0} y1={0} x2={34} y2={26} stroke="#78350F" strokeWidth={9} strokeLinecap="round" />
        <circle cx={-16} cy={-12} r={24} fill="#BAE6FD" fillOpacity={0.55} stroke="#CBD5E1" strokeWidth={5} />
      </g>
    </g>
  </g>
));

export const PhongThiNghiemCo: React.FC<BoiCanhMoiProps> = ({ frame, px }) => {
  const bot = ((frame * 0.8) % 44);
  return (
    <g>
      <g transform={`translate(${(px.lop1X * 0.4).toFixed(1)}, ${(px.lop1Y * 0.3).toFixed(1)})`}>
        <PhongThiNghiemLop1Tinh />
      </g>
      <g transform={`translate(${(px.lop2X * 0.5).toFixed(1)}, ${(px.lop2Y * 0.4).toFixed(1)})`}>
        <PhongThiNghiemLop2Tinh />
        {/* Bot khi soi nhe trong binh thi nghiem */}
        <circle cx={218} cy={274 - bot} r={4} fill="#E0F2FE" fillOpacity={0.75} />
        <circle cx={1488} cy={430 - ((bot + 18) % 44)} r={3.5} fill="#FEF08A" fillOpacity={0.75} />
      </g>
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <PhongThiNghiemLop3Tinh />
      </g>
    </g>
  );
};

// =============================================================================
// 21. KHONG GIAN VU TRU TOAN (hinh hoc truu tuong, lo den/quy dao phat sang SVG phang khong blur)
// =============================================================================
const VuTruToanLop1Tinh = React.memo(() => (
  <g>
    <defs>
      <radialGradient id="vttNen" cx="50%" cy="42%" r="68%">
        <stop offset="0%" stopColor="#1E1B4B" />
        <stop offset="55%" stopColor="#0F172A" />
        <stop offset="100%" stopColor="#020617" />
      </radialGradient>
    </defs>
    <rect x={-260} y={-140} width={2440} height={1360} fill="url(#vttNen)" />
    {/* Luoi khong-thoi gian phang */}
    {Array.from({ length: 14 }).map((_, i) => (
      <line key={`vtt-gx-${i}`} x1={-120 + i * 165} y1={-120} x2={-120 + i * 165} y2={1160} stroke="#38BDF8" strokeOpacity={0.08} strokeWidth={1.5} />
    ))}
    {Array.from({ length: 9 }).map((_, i) => (
      <line key={`vtt-gy-${i}`} x1={-220} y1={i * 135} x2={2140} y2={i * 135} stroke="#38BDF8" strokeOpacity={0.08} strokeWidth={1.5} />
    ))}
  </g>
));

const VuTruToanLop3Tinh = React.memo(() => (
  <g>
    {/* Luoi phoi canh mat phang vu tru o phan san */}
    <path d="M -180 760 L 2100 760 L 2100 1180 L -180 1180 Z" fill="#0B1120" fillOpacity={0.78} />
    {[760, 815, 885, 975].map((y) => (
      <line key={`vtt-fh-${y}`} x1={-180} y1={y} x2={2100} y2={y} stroke="#818CF8" strokeOpacity={0.32} strokeWidth={2} />
    ))}
    {[-200, 120, 440, 760, 960, 1160, 1480, 1800, 2120].map((x, idx) => (
      <line key={`vtt-fv-${idx}`} x1={960 + (x - 960) * 0.45} y1={760} x2={x} y2={1140} stroke="#818CF8" strokeOpacity={0.28} strokeWidth={2} />
    ))}
  </g>
));

export const KhongGianVuTruToan: React.FC<BoiCanhMoiProps> = ({ frame, px }) => {
  const xoay1 = (frame * 0.55) % 360;
  const xoay2 = (-frame * 0.38) % 360;
  const nhipLoDen = 1 + Math.sin(frame * 0.09) * 0.04;

  return (
    <g>
      {/* LOP 1 (0.2x): Nen vu tru luoi & sao lap lanh */}
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <VuTruToanLop1Tinh />
        {Array.from({ length: 36 }).map((_, i) => {
          const sx = -80 + bamTatDinh(i * 29 + 7) * 2080;
          const sy = 30 + bamTatDinh(i * 41 + 3) * 680;
          const r = 1.5 + bamTatDinh(i * 13 + 5) * 2.5;
          const op = 0.4 + 0.55 * Math.abs(Math.sin(frame * 0.08 + i * 1.1));
          return <circle key={`vtt-s-${i}`} cx={sx} cy={sy} r={r} fill="#E0F2FE" fillOpacity={op} />;
        })}
      </g>

      {/* LOP 2 (0.5x): Lo den / dia boi tu phat sang phang (khong blur) & quy dao hinh hoc xoay */}
      <g transform={`translate(${(960 + px.lop2X).toFixed(1)}, ${(380 + px.lop2Y).toFixed(1)})`}>
        {/* Cac vong hao quang dong tam phang (thay cho blur) */}
        <circle cx={0} cy={0} r={240 * nhipLoDen} fill="#6366F1" fillOpacity={0.09} />
        <circle cx={0} cy={0} r={175 * nhipLoDen} fill="#38BDF8" fillOpacity={0.14} />
        <circle cx={0} cy={0} r={124} fill="#F59E0B" fillOpacity={0.22} />
        {/* Quy dao elip phat sang nghieng xoay */}
        <g transform={`rotate(${(18 + xoay1 * 0.15).toFixed(1)})`}>
          <ellipse cx={0} cy={0} rx={360} ry={96} fill="none" stroke="#FACC15" strokeWidth={5} strokeOpacity={0.78} />
          <ellipse cx={0} cy={0} rx={310} ry={76} fill="none" stroke="#F97316" strokeWidth={3.5} strokeOpacity={0.65} />
          <circle
            cx={(Math.cos((xoay1 * Math.PI) / 180) * 360).toFixed(1)}
            cy={(Math.sin((xoay1 * Math.PI) / 180) * 96).toFixed(1)}
            r={11}
            fill="#FEF08A"
          />
        </g>
        <g transform={`rotate(${(-26 + xoay2 * 0.15).toFixed(1)})`}>
          <ellipse cx={0} cy={0} rx={295} ry={115} fill="none" stroke="#38BDF8" strokeWidth={3.5} strokeDasharray="14 10" strokeOpacity={0.68} />
          <circle
            cx={(Math.cos((xoay2 * Math.PI) / 180) * 295).toFixed(1)}
            cy={(Math.sin((xoay2 * Math.PI) / 180) * 115).toFixed(1)}
            r={9}
            fill="#7DD3FC"
          />
        </g>
        {/* Chan troi su kien trung tam */}
        <circle cx={0} cy={0} r={88} fill="#020617" stroke="#FEF08A" strokeWidth={5} />
        <circle cx={0} cy={0} r={98} fill="none" stroke="#F97316" strokeWidth={2.5} strokeOpacity={0.75} />
      </g>

      {/* LOP 3 (1.0x): Luoi mat phang & khoi da dien hinh hoc lo lung */}
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <VuTruToanLop3Tinh />
        {/* 2 khoi da dien lo lung phat sang hai ben */}
        <g transform={`translate(245, ${(460 + Math.sin(frame * 0.07) * 16).toFixed(1)}) rotate(${(xoay1 * 0.35).toFixed(1)})`}>
          <polygon points="0,-54 -46,0 0,54 46,0" fill="#38BDF8" fillOpacity={0.22} stroke="#7DD3FC" strokeWidth={3} />
          <line x1={-46} y1={0} x2={46} y2={0} stroke="#BAE6FD" strokeWidth={2} />
          <line x1={0} y1={-54} x2={0} y2={54} stroke="#BAE6FD" strokeWidth={2} />
        </g>
        <g transform={`translate(1675, ${(440 + Math.cos(frame * 0.065) * 18).toFixed(1)}) rotate(${(xoay2 * 0.35).toFixed(1)})`}>
          <polygon points="0,-58 50,-28 50,28 0,58 -50,28 -50,-28" fill="#A855F7" fillOpacity={0.22} stroke="#E9D5FF" strokeWidth={3} />
          <polygon points="0,-58 50,28 -50,28" fill="none" stroke="#FEF08A" strokeWidth={2.2} />
        </g>
      </g>
    </g>
  );
};

// =============================================================================
// 22. LANG QUE AN DO / A DONG (nha mai ngoi, san da, cay co/tre, nang am)
// =============================================================================
const LangQueLop1Tinh = React.memo<{ laHoangHon: boolean }>(({ laHoangHon }) => (
  <g>
    <defs>
      <linearGradient id="lqTroi" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor={laHoangHon ? '#EA580C' : '#0EA5E9'} />
        <stop offset="50%" stopColor={laHoangHon ? '#FB923C' : '#7DD3FC'} />
        <stop offset="100%" stopColor="#FEF3C7" />
      </linearGradient>
    </defs>
    <rect x={-260} y={-120} width={2440} height={740} fill="url(#lqTroi)" />
    <g transform="translate(520, 175)">
      <circle cx={0} cy={0} r={135} fill="#FEF08A" fillOpacity={0.18} />
      <circle cx={0} cy={0} r={86} fill="#FDE68A" fillOpacity={0.28} />
      <circle cx={0} cy={0} r={54} fill="#FFFBEB" />
    </g>
  </g>
));

const LangQueLop2Tinh = React.memo(() => (
  <g>
    {/* Doi xa xanh & ngoi den / nha mai ngoi truyen thong An Do - A Dong */}
    <path d="M -220 560 Q 340 440 820 510 Q 1340 570 1760 465 Q 1960 440 2140 490 L 2140 760 L -220 760 Z" fill="#86EFAC" />
    {/* Day nha mai ngoi dat nung am ap */}
    <g transform="translate(260, 410)">
      <rect x={0} y={96} width={380} height={195} fill="#FEF3C7" stroke="#B45309" strokeWidth={4} />
      <polygon points="-28,98 190,-6 408,98" fill="#C2410C" stroke="#7C2D12" strokeWidth={4} strokeLinejoin="round" />
      {[40, 110, 180, 250, 320].map((mx) => (
        <line key={`lq-ng-${mx}`} x1={mx} y1={96} x2={190} y2={2} stroke="#9A3412" strokeOpacity={0.45} strokeWidth={3} />
      ))}
      {/* Hien nha cot go & cua vom truyen thong */}
      <path d="M 145 290 L 145 182 Q 190 144 235 182 L 235 290 Z" fill="#78350F" stroke="#451A03" strokeWidth={4} />
      <rect x={36} y={168} width={68} height={68} rx={6} fill="#92400E" stroke="#451A03" strokeWidth={3} />
      <rect x={276} y={168} width={68} height={68} rx={6} fill="#92400E" stroke="#451A03" strokeWidth={3} />
    </g>
    {/* Nha mai ngoi thu hai ben phai */}
    <g transform="translate(1220, 445)">
      <rect x={0} y={84} width={330} height={175} fill="#FFEDD5" stroke="#B45309" strokeWidth={4} />
      <polygon points="-24,86 165,-8 354,86" fill="#EA580C" stroke="#7C2D12" strokeWidth={4} strokeLinejoin="round" />
      <path d="M 122 258 L 122 162 Q 165 130 208 162 L 208 258 Z" fill="#78350F" stroke="#451A03" strokeWidth={4} />
    </g>
  </g>
));

const LangQueLop3Tinh = React.memo(() => (
  <g>
    {/* San da vang am & tuong rao thap + chum dat nung */}
    <rect x={-180} y={698} width={2280} height={460} fill="#E7D3B1" />
    <rect x={-180} y={690} width={2280} height={16} fill="#F5E6CA" stroke="#C2A378" strokeWidth={3} />
    {[770, 855, 950].map((sy) => (
      <line key={`lq-s-${sy}`} x1={-180} y1={sy} x2={2100} y2={sy} stroke="#C2A378" strokeOpacity={0.55} strokeWidth={2.5} />
    ))}
    {/* Chum nuoc dat nung goc trai */}
    <g transform="translate(215, 725)">
      <ellipse cx={0} cy={0} rx={36} ry={30} fill="#C2410C" stroke="#7C2D12" strokeWidth={3.5} />
      <ellipse cx={0} cy={-28} rx={20} ry={7} fill="#EA580C" stroke="#7C2D12" strokeWidth={3} />
    </g>
  </g>
));

export const LangQueAnDoADong: React.FC<BoiCanhMoiProps> = ({ frame, px, laHoangHon = false }) => {
  const duaCo = Math.sin(frame * 0.06) * 5.5;
  const duaTre = Math.sin(frame * 0.075 + 1.1) * 4.5;
  return (
    <g>
      <g transform={`translate(${px.lop1X.toFixed(1)}, ${px.lop1Y.toFixed(1)})`}>
        <LangQueLop1Tinh laHoangHon={laHoangHon} />
        <CumMay xGoc={140} y={120} tiLe={1.2} tocDo={0.34} frame={frame} />
        <CumMay xGoc={1080} y={140} tiLe={1.0} tocDo={0.26} frame={frame} />
      </g>
      <g transform={`translate(${px.lop2X.toFixed(1)}, ${px.lop2Y.toFixed(1)})`}>
        <LangQueLop2Tinh />
        {/* Cum cay tre dung dua nhe phia sau ben trai */}
        <g transform="translate(120, 680)">
          {[-28, 0, 26].map((tx, ti) => (
            <g key={`tre-${ti}`}>
              <path
                d={`M ${tx} 10 Q ${(tx + duaTre * 0.5).toFixed(1)} -180 ${(tx + duaTre * 1.4).toFixed(1)} -350`}
                fill="none"
                stroke="#15803D"
                strokeWidth={11}
                strokeLinecap="round"
              />
              <ellipse cx={tx + duaTre * 1.4 - 24} cy={-315} rx={36} ry={12} fill="#22C55E" transform={`rotate(-18, ${tx}, -315)`} />
              <ellipse cx={tx + duaTre * 1.4 + 26} cy={-275} rx={38} ry={12} fill="#4ADE80" transform={`rotate(16, ${tx}, -275)`} />
            </g>
          ))}
        </g>
      </g>
      <g transform={`translate(${px.lop3X.toFixed(1)}, ${px.lop3Y.toFixed(1)})`}>
        <LangQueLop3Tinh />
        {/* Cay co / dua tien canh phai dung dua theo gio */}
        <g transform="translate(1785, 745)">
          <path d="M -22 20 Q -48 -140 -14 -330 L 14 -330 Q -12 -140 24 20 Z" fill="#92400E" />
          <g transform={`translate(${duaCo.toFixed(1)}, -330)`}>
            <path d="M 0 0 Q -110 -55 -185 18 Q -95 -12 0 12 Z" fill="#15803D" />
            <path d="M 0 0 Q -95 -95 -145 -80 Q -65 -55 0 4 Z" fill="#16A34A" />
            <path d="M 0 0 Q 95 -88 160 -42 Q 80 -36 0 6 Z" fill="#22C55E" />
            <path d="M 0 0 Q 110 -24 175 44 Q 90 4 0 14 Z" fill="#16A34A" />
            <circle cx={-12} cy={14} r={12} fill="#78350F" />
            <circle cx={10} cy={18} r={11} fill="#92400E" />
          </g>
        </g>
      </g>
    </g>
  );
};
