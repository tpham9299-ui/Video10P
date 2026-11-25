import React from 'react';
import { useCurrentFrame } from 'remotion';
import type { DaoCuTrongCanh } from '../kieu_dai';

type DaoCuProps = {
  daoCu: DaoCuTrongCanh;
};

export const DaoCu: React.FC<DaoCuProps> = ({ daoCu }) => {
  const frame = useCurrentFrame();
  const mau = daoCu.mau ?? '#38BDF8';
  const tiLe = daoCu.tiLe ?? 1;

  const veBieuTuong = () => {
    switch (daoCu.loai) {
      case 'bang_den':
        return (
          <g>
            <rect
              x={-72}
              y={-48}
              width={144}
              height={96}
              rx={8}
              fill="#0F2922"
              stroke="#B45309"
              strokeWidth={6}
            />
            <line x1={-46} y1={-14} x2={34} y2={-14} stroke="#E2E8F0" strokeWidth={3} strokeLinecap="round" />
            <line x1={-46} y1={10} x2={48} y2={10} stroke={mau} strokeWidth={3} strokeLinecap="round" />
          </g>
        );
      case 'cuon_giay':
        return (
          <g>
            <rect x={-42} y={-50} width={84} height={100} rx={10} fill="#FEF3C7" stroke="#D97706" strokeWidth={4} />
            <ellipse cx={0} cy={-50} rx={42} ry={10} fill="#FDE68A" stroke="#D97706" strokeWidth={3} />
            <line x1={-24} y1={-16} x2={24} y2={-16} stroke="#92400E" strokeWidth={3} strokeLinecap="round" />
            <line x1={-24} y1={6} x2={18} y2={6} stroke="#92400E" strokeWidth={3} strokeLinecap="round" />
            <line x1={-24} y1={26} x2={22} y2={26} stroke="#92400E" strokeWidth={3} strokeLinecap="round" />
          </g>
        );
      case 'bong_den':
        return (
          <g>
            <circle cx={0} cy={-14} r={30} fill="#FEF08A" fillOpacity={0.22} stroke="#FACC15" strokeWidth={4} />
            <rect x={-12} y={16} width={24} height={16} rx={4} fill="#94A3B8" />
            <line x1={0} y1={-56} x2={0} y2={-66} stroke="#FACC15" strokeWidth={4} strokeLinecap="round" />
            <line x1={-40} y1={-34} x2={-50} y2={-40} stroke="#FACC15" strokeWidth={4} strokeLinecap="round" />
            <line x1={40} y1={-34} x2={50} y2={-40} stroke="#FACC15" strokeWidth={4} strokeLinecap="round" />
          </g>
        );
      case 'dong_ho_cat':
        return (
          <g>
            <line x1={-28} y1={-42} x2={28} y2={-42} stroke={mau} strokeWidth={5} strokeLinecap="round" />
            <line x1={-28} y1={42} x2={28} y2={42} stroke={mau} strokeWidth={5} strokeLinecap="round" />
            <polygon points="-24,-40 24,-40 0,0" fill="#38BDF8" fillOpacity={0.25} stroke={mau} strokeWidth={3} />
            <polygon points="-24,40 24,40 0,0" fill="#FACC15" fillOpacity={0.35} stroke={mau} strokeWidth={3} />
          </g>
        );
      case 'can_thang_bang':
        return (
          <g>
            <line x1={0} y1={-40} x2={0} y2={38} stroke={mau} strokeWidth={5} strokeLinecap="round" />
            <line x1={-26} y1={38} x2={26} y2={38} stroke={mau} strokeWidth={6} strokeLinecap="round" />
            <line x1={-52} y1={-28} x2={52} y2={-28} stroke={mau} strokeWidth={4} strokeLinecap="round" />
            <path d="M -64 4 Q -52 20 -40 4 Z" fill={mau} fillOpacity={0.35} stroke={mau} strokeWidth={2.5} />
            <path d="M 40 4 Q 52 20 64 4 Z" fill={mau} fillOpacity={0.35} stroke={mau} strokeWidth={2.5} />
            <line x1={-52} y1={-28} x2={-52} y2={4} stroke={mau} strokeWidth={2} />
            <line x1={52} y1={-28} x2={52} y2={4} stroke={mau} strokeWidth={2} />
          </g>
        );
      case 'thuoc_compa':
        return (
          <g>
            <line x1={0} y1={-42} x2={-28} y2={40} stroke={mau} strokeWidth={5} strokeLinecap="round" />
            <line x1={0} y1={-42} x2={28} y2={40} stroke={mau} strokeWidth={5} strokeLinecap="round" />
            <circle cx={0} cy={-42} r={8} fill="#0F172A" stroke={mau} strokeWidth={4} />
            <path d="M -18 14 Q 0 26 18 14" fill="none" stroke="#FACC15" strokeWidth={3} />
          </g>
        );
      case 'compa_co':
        return (
          <g>
            {/* Vong khac do phia sau */}
            <path d="M -38 14 A 44 44 0 0 0 38 14" fill="none" stroke="#FDE047" strokeWidth={3.5} strokeDasharray="4 3" />
            {/* Hai chan compa dong co */}
            <path d="M -4 -44 L -32 42 L -25 46 L 0 -36 Z" fill="#D97706" stroke="#78350F" strokeWidth={2.5} />
            <path d="M 4 -44 L 32 42 L 25 46 L 0 -36 Z" fill="#F59E0B" stroke="#78350F" strokeWidth={2.5} />
            {/* Mui kim & dau but chi */}
            <polygon points="-32,42 -25,46 -32,54" fill="#E2E8F0" stroke="#475569" strokeWidth={1.5} />
            <polygon points="32,42 25,46 32,54" fill="#1E293B" />
            {/* Thanh vit ngang */}
            <line x1={-22} y1={4} x2={22} y2={4} stroke="#FEF08A" strokeWidth={4} strokeLinecap="round" />
            <rect x={-5} y={-2} width={10} height={12} rx={2} fill="#92400E" stroke="#FEF08A" strokeWidth={1.8} />
            {/* Khop xoay dinh compa */}
            <rect x={-4} y={-62} width={8} height={14} rx={3} fill="#B45309" stroke="#78350F" strokeWidth={2} />
            <circle cx={0} cy={-42} r={11} fill="#FACC15" stroke="#78350F" strokeWidth={3} />
            <circle cx={0} cy={-42} r={4} fill="#451A03" />
          </g>
        );
      case 'ban_tinh_co':
        return (
          <g>
            {/* Khung go ngoai */}
            <rect x={-54} y={-38} width={108} height={76} rx={8} fill="#451A03" stroke="#B45309" strokeWidth={6} />
            {/* Thanh chia tren-duoi */}
            <line x1={-50} y1={-12} x2={50} y2={-12} stroke="#D97706" strokeWidth={5} />
            {/* 4 thanh doc + hat ban tinh tat dinh */}
            {[-30, -10, 10, 30].map((rx, idx) => (
              <g key={`bt-${idx}`}>
                <line x1={rx} y1={-34} x2={rx} y2={34} stroke="#FDE68A" strokeWidth={2.4} />
                {/* Hat phia tren */}
                <ellipse cx={rx} cy={idx % 2 === 0 ? -24 : -20} rx={7.5} ry={4.5} fill="#F59E0B" stroke="#78350F" strokeWidth={1.5} />
                {/* Hat phia duoi */}
                <ellipse cx={rx} cy={4 + (idx % 2) * 8} rx={7.5} ry={4.5} fill={mau} stroke="#0F172A" strokeWidth={1.5} />
                <ellipse cx={rx} cy={22} rx={7.5} ry={4.5} fill="#FACC15" stroke="#78350F" strokeWidth={1.5} />
              </g>
            ))}
          </g>
        );
      case 'khoi_da_dien':
        return (
          <g>
            {/* Khoi bat dien deu (Octahedron) voi cac mat sang toi & canh khuat net dut */}
            <polygon points="0,-48 -42,0 0,14" fill={mau} fillOpacity={0.38} stroke="#E0F2FE" strokeWidth={2.8} strokeLinejoin="round" />
            <polygon points="0,-48 42,0 0,14" fill={mau} fillOpacity={0.62} stroke="#E0F2FE" strokeWidth={2.8} strokeLinejoin="round" />
            <polygon points="0,48 -42,0 0,14" fill="#1E3A8A" fillOpacity={0.55} stroke="#7DD3FC" strokeWidth={2.8} strokeLinejoin="round" />
            <polygon points="0,48 42,0 0,14" fill="#0F172A" fillOpacity={0.55} stroke="#7DD3FC" strokeWidth={2.8} strokeLinejoin="round" />
            {/* Canh khuat phia sau */}
            <line x1={-42} y1={0} x2={0} y2={-14} stroke="#FEF08A" strokeOpacity={0.65} strokeWidth={2} strokeDasharray="4 4" />
            <line x1={42} y1={0} x2={0} y2={-14} stroke="#FEF08A" strokeOpacity={0.65} strokeWidth={2} strokeDasharray="4 4" />
            <line x1={0} y1={-48} x2={0} y2={48} stroke="#FEF08A" strokeOpacity={0.45} strokeWidth={1.8} strokeDasharray="5 4" />
            {/* Dinh phat sang */}
            {[
              [0, -48],
              [-42, 0],
              [42, 0],
              [0, 14],
              [0, 48],
            ].map(([vx, vy], vi) => (
              <circle key={`dd-${vi}`} cx={vx} cy={vy} r={4} fill="#FEF08A" stroke="#0F172A" strokeWidth={1.5} />
            ))}
          </g>
        );
      case 'kinh_thien_van':
        return (
          <g>
            {/* Chan de ba chan go */}
            <line x1={-2} y1={4} x2={-30} y2={48} stroke="#92400E" strokeWidth={5} strokeLinecap="round" />
            <line x1={-2} y1={4} x2={24} y2={48} stroke="#92400E" strokeWidth={5} strokeLinecap="round" />
            <line x1={-2} y1={4} x2={-2} y2={46} stroke="#78350F" strokeWidth={4} strokeLinecap="round" />
            {/* Thuoc do goc gan o khop */}
            <path d="M -22 10 A 22 22 0 0 0 18 10" fill="none" stroke="#FACC15" strokeWidth={2.5} />
            {/* Ong kinh thien van dong thau nghieng len troi */}
            <g transform="translate(-2, -6) rotate(-28)">
              <rect x={-46} y={-9} width={78} height={18} rx={4} fill="#D97706" stroke="#78350F" strokeWidth={2.8} />
              <rect x={28} y={-13} width={22} height={26} rx={4} fill="#F59E0B" stroke="#78350F" strokeWidth={2.8} />
              <ellipse cx={50} cy={0} rx={4.5} ry={12} fill="#7DD3FC" stroke="#1E3A8A" strokeWidth={2} />
              <rect x={-56} y={-6} width={12} height={12} rx={2} fill="#92400E" stroke="#451A03" strokeWidth={2} />
              {/* Dai dong trang tri */}
              <rect x={-10} y={-10} width={8} height={20} fill="#FEF08A" />
              <rect x={14} y={-10} width={6} height={20} fill="#FEF08A" />
            </g>
            <circle cx={-2} cy={4} r={7} fill="#FACC15" stroke="#78350F" strokeWidth={2.5} />
          </g>
        );
      case 'noi_em_be': {
        const lacNoi = Math.sin(frame * 0.08) * 3.5;
        return (
          <g transform={`rotate(${lacNoi.toFixed(2)}, 0, 38)`}>
            {/* Chan vong cung bap benh */}
            <path d="M -58 34 Q 0 54 58 34" fill="none" stroke="#92400E" strokeWidth={6} strokeLinecap="round" />
            <line x1={-34} y1={22} x2={-34} y2={40} stroke="#78350F" strokeWidth={5} />
            <line x1={34} y1={22} x2={34} y2={40} stroke="#78350F" strokeWidth={5} />
            {/* Than noi go nan */}
            <path d="M -52 -16 L 52 -16 L 44 26 L -44 26 Z" fill="#D97706" stroke="#78350F" strokeWidth={4} strokeLinejoin="round" />
            {[-30, -10, 10, 30].map((nx) => (
              <line key={`nan-${nx}`} x1={nx} y1={-14} x2={nx * 0.88} y2={24} stroke="#92400E" strokeWidth={3} />
            ))}
            {/* Chan men mem & dau em be nho xinh */}
            <path d="M -44 -16 Q 0 -30 44 -16 Z" fill="#FEF08A" stroke="#CA8A04" strokeWidth={2.5} />
            <circle cx={-16} cy={-24} r={11} fill="#FDE68A" stroke="#78350F" strokeWidth={2.5} />
            <path d="M -20 -25 Q -16 -22 -12 -25" fill="none" stroke="#78350F" strokeWidth={1.8} strokeLinecap="round" />
          </g>
        );
      }
      case 'noi_sup': {
        const uonKhoi = Math.sin(frame * 0.14) * 5;
        return (
          <g>
            {/* Hoi nong boc len tat dinh */}
            <path d={`M -16 -32 Q ${(-22 + uonKhoi).toFixed(1)} -48 -14 -64`} fill="none" stroke="#FFFFFF" strokeOpacity={0.72} strokeWidth={3.5} strokeLinecap="round" />
            <path d={`M 2 -36 Q ${(8 - uonKhoi).toFixed(1)} -54 0 -72`} fill="none" stroke="#FFFFFF" strokeOpacity={0.78} strokeWidth={3.8} strokeLinecap="round" />
            <path d={`M 18 -32 Q ${(24 + uonKhoi).toFixed(1)} -46 16 -62`} fill="none" stroke="#FFFFFF" strokeOpacity={0.68} strokeWidth={3.2} strokeLinecap="round" />
            {/* Quai noi 2 ben */}
            <path d="M -46 -10 Q -62 -10 -62 4 Q -62 16 -44 16" fill="none" stroke="#334155" strokeWidth={5} />
            <path d="M 46 -10 Q 62 -10 62 4 Q 62 16 44 16" fill="none" stroke="#334155" strokeWidth={5} />
            {/* Than noi sup */}
            <path d="M -46 -18 L 46 -18 L 42 28 Q 42 40 28 40 L -28 40 Q -42 40 -42 28 Z" fill="#475569" stroke="#1E293B" strokeWidth={4} />
            <ellipse cx={0} cy={-18} rx={46} ry={11} fill="#F59E0B" stroke="#1E293B" strokeWidth={3.5} />
            <circle cx={-14} cy={-18} r={5} fill="#FEF08A" />
            <circle cx={12} cy={-16} r={4} fill="#22C55E" />
          </g>
        );
      }
      case 'phong_bi_thu_tay':
        return (
          <g>
            <rect x={-56} y={-36} width={112} height={72} rx={8} fill="#FEF3C7" stroke="#92400E" strokeWidth={4} />
            <polyline points="-54,-34 0,8 54,-34" fill="none" stroke="#B45309" strokeWidth={3.5} strokeLinejoin="round" />
            <line x1={-52} y1={34} x2={-14} y2={2} stroke="#D97706" strokeWidth={2.4} />
            <line x1={52} y1={34} x2={14} y2={2} stroke="#D97706" strokeWidth={2.4} />
            {/* Dau sap do co dien */}
            <circle cx={0} cy={8} r={13} fill="#DC2626" stroke="#7F1D1D" strokeWidth={2.5} />
            <circle cx={0} cy={8} r={6} fill="none" stroke="#FCA5A5" strokeWidth={1.8} />
          </g>
        );
      case 'giuong_benh':
        return (
          <g>
            {/* Khung sat dau & cuoi giuong */}
            <path d="M -72 34 L -72 -32 Q -72 -44 -58 -44 L -50 -44 L -50 34" fill="none" stroke="#94A3B8" strokeWidth={6} strokeLinecap="round" />
            <path d="M 72 34 L 72 -18 Q 72 -28 60 -28 L 54 -28 L 54 34" fill="none" stroke="#94A3B8" strokeWidth={6} strokeLinecap="round" />
            {/* Nem trang & goi */}
            <rect x={-66} y={-8} width={132} height={24} rx={6} fill="#F8FAFC" stroke="#CBD5E1" strokeWidth={3} />
            <ellipse cx={-46} cy={-14} rx={18} ry={9} fill="#FFFFFF" stroke="#94A3B8" strokeWidth={2.5} />
            {/* Chan xanh benh vien */}
            <path d="M -28 -10 L 66 -10 L 66 18 L -28 18 Z" fill="#38BDF8" fillOpacity={0.85} stroke="#0369A1" strokeWidth={3} />
            {/* Khung gam & banh xe */}
            <rect x={-72} y={16} width={144} height={9} rx={3} fill="#64748B" />
            <circle cx={-60} cy={38} r={6} fill="#1E293B" />
            <circle cx={60} cy={38} r={6} fill="#1E293B" />
          </g>
        );
      case 'bien_so_xe': {
        const soXe = (daoCu.bienSoXe || daoCu.nhan || '1729').trim();
        const rongBien = Math.max(146, soXe.length * 20 + 44);
        return (
          <g>
            {/* The chu thich / khung treo gan xe (tranh cam giac bien so treo lo lung tren tuong) */}
            <rect
              x={-rongBien / 2 - 12}
              y={-56}
              width={rongBien + 24}
              height={102}
              rx={16}
              fill="#0F172A"
              fillOpacity={0.92}
              stroke="#FACC15"
              strokeWidth={3.5}
            />
            <rect
              x={-58}
              y={-68}
              width={116}
              height={24}
              rx={12}
              fill="#FACC15"
              stroke="#0F172A"
              strokeWidth={2.5}
            />
            <text
              x={0}
              y={-52}
              textAnchor="middle"
              fill="#0F172A"
              fontSize={12.5}
              fontWeight={900}
              fontFamily="Segoe UI, Arial, sans-serif"
            >
              BIỂN SỐ TAXI
            </text>
            <rect
              x={-rongBien / 2}
              y={-30}
              width={rongBien}
              height={62}
              rx={10}
              fill="#1E293B"
              stroke="#FEF08A"
              strokeWidth={4}
            />
            <rect
              x={-rongBien / 2 + 8}
              y={-22}
              width={rongBien - 16}
              height={46}
              rx={6}
              fill="#FEF08A"
            />
            <circle cx={-rongBien / 2 + 16} cy={1} r={3.5} fill="#64748B" />
            <circle cx={rongBien / 2 - 16} cy={1} r={3.5} fill="#64748B" />
            <text
              x={0}
              y={12}
              textAnchor="middle"
              fill="#0F172A"
              fontSize={32}
              fontWeight={900}
              fontFamily="Consolas, Segoe UI, monospace"
            >
              {soXe}
            </text>
          </g>
        );
      }
      case 'tach_tra_nong': {
        const khoiTra = Math.sin(frame * 0.16) * 4;
        return (
          <g>
            {/* Hoi tra nong */}
            <path d={`M -10 -24 Q ${(-15 + khoiTra).toFixed(1)} -40 -8 -54`} fill="none" stroke="#FFFFFF" strokeOpacity={0.78} strokeWidth={3} strokeLinecap="round" />
            <path d={`M 8 -26 Q ${(13 - khoiTra).toFixed(1)} -42 6 -58`} fill="none" stroke="#E2E8F0" strokeOpacity={0.72} strokeWidth={2.8} strokeLinecap="round" />
            {/* Dia lot */}
            <ellipse cx={0} cy={28} rx={44} ry={10} fill="#E2E8F0" stroke="#64748B" strokeWidth={3} />
            {/* Quai tach */}
            <path d="M 28 -8 Q 48 -8 48 6 Q 48 20 26 20" fill="none" stroke="#FFFFFF" strokeWidth={6} />
            <path d="M 28 -8 Q 48 -8 48 6 Q 48 20 26 20" fill="none" stroke="#475569" strokeWidth={2.5} />
            {/* Than tach su */}
            <path d="M -30 -16 L 30 -16 L 24 22 Q 20 30 0 30 Q -20 30 -24 22 Z" fill="#FFFFFF" stroke="#334155" strokeWidth={3.5} />
            <ellipse cx={0} cy={-16} rx={30} ry={7} fill="#B45309" stroke="#334155" strokeWidth={2.5} />
          </g>
        );
      }
      case 'tau_thuy': {
        const nhapNho = Math.sin(frame * 0.1) * 3;
        return (
          <g transform={`translate(0, ${nhapNho.toFixed(1)})`}>
            {/* Ong khoi tau vien duong */}
            <rect x={-26} y={-50} width={16} height={32} rx={3} fill="#DC2626" stroke="#1E293B" strokeWidth={2.5} />
            <rect x={-26} y={-50} width={16} height={8} fill="#1E293B" />
            <rect x={4} y={-46} width={16} height={28} rx={3} fill="#DC2626" stroke="#1E293B" strokeWidth={2.5} />
            <rect x={4} y={-46} width={16} height={8} fill="#1E293B" />
            {/* Tang cabin trang */}
            <rect x={-46} y={-20} width={88} height={22} rx={5} fill="#F8FAFC" stroke="#334155" strokeWidth={3} />
            {/* Than tau den + vien do */}
            <path d="M -68 2 L 76 2 L 58 30 L -54 30 Z" fill="#1E293B" stroke="#0F172A" strokeWidth={3} />
            <line x1={-60} y1={16} x2={68} y2={16} stroke="#EF4444" strokeWidth={5} />
            {/* Cua so tron man tau */}
            {[-36, -12, 12, 36].map((px) => (
              <circle key={`porthole-${px}`} cx={px} cy={-9} r={4} fill="#38BDF8" stroke="#1E293B" strokeWidth={1.5} />
            ))}
            {/* Dai song duoi mui tau */}
            <path d="M -78 34 Q -40 26 0 34 Q 40 42 82 34" fill="none" stroke="#BAE6FD" strokeWidth={4} strokeLinecap="round" />
          </g>
        );
      }
      case 'ban_hoc_den_dau': {
        const rungLua = Math.sin(frame * 0.28) * 2;
        return (
          <g>
            {/* Ban go co dien */}
            <rect x={-68} y={6} width={136} height={14} rx={4} fill="#B45309" stroke="#451A03" strokeWidth={3.5} />
            <rect x={-56} y={20} width={14} height={36} fill="#78350F" />
            <rect x={42} y={20} width={14} height={36} fill="#78350F" />
            {/* So ghi chep mo */}
            <polygon points="-46,6 -8,6 -4,-4 -42,-4" fill="#FEF3C7" stroke="#92400E" strokeWidth={2.2} />
            <polygon points="-8,6 30,6 34,-4 -4,-4" fill="#FFFBEB" stroke="#92400E" strokeWidth={2.2} />
            {/* Den dau dong thau ben phai ban (hao quang phang khong blur) */}
            <g transform="translate(42, -12)">
              <circle cx={0} cy={-16} r={26} fill="#FACC15" fillOpacity={0.2} />
              <ellipse cx={0} cy={14} rx={15} ry={6} fill="#D97706" stroke="#78350F" strokeWidth={2.5} />
              <path d="M -9 10 Q -12 -18 0 -24 Q 12 -18 9 10 Z" fill="#E0F2FE" fillOpacity={0.45} stroke="#94A3B8" strokeWidth={2} />
              <path d={`M 0 ${(-24 + rungLua).toFixed(1)} Q 6 -12 0 -4 Q -6 -12 0 ${(-24 + rungLua).toFixed(1)} Z`} fill="#F97316" />
              <circle cx={0} cy={-12} r={3.5} fill="#FEF08A" />
            </g>
          </g>
        );
      }
      case 'qua_dia_cau':
        return (
          <g>
            {/* Vong kinh tuyen dong thau */}
            <path d="M -38 -30 A 44 44 0 1 1 -38 30" fill="none" stroke="#D97706" strokeWidth={6} strokeLinecap="round" />
            {/* Qua cau xanh & luc dia */}
            <circle cx={0} cy={0} r={34} fill="#0EA5E9" stroke="#0C4A6E" strokeWidth={3.5} />
            <path d="M -18 -18 Q -4 -26 10 -12 Q 20 -4 8 8 Q -8 12 -18 -18 Z" fill="#22C55E" />
            <path d="M 8 10 Q 22 6 24 18 Q 14 26 2 22 Z" fill="#4ADE80" />
            <ellipse cx={0} cy={0} rx={34} ry={11} fill="none" stroke="#E0F2FE" strokeOpacity={0.45} strokeWidth={1.8} />
            <ellipse cx={0} cy={0} rx={14} ry={34} fill="none" stroke="#E0F2FE" strokeOpacity={0.45} strokeWidth={1.8} />
            {/* Chan de go */}
            <line x1={0} y1={42} x2={0} y2={52} stroke="#92400E" strokeWidth={7} />
            <rect x={-26} y={48} width={52} height={10} rx={5} fill="#78350F" stroke="#451A03" strokeWidth={2.5} />
          </g>
        );
      case 'dau_hoi_cham':
      default:
        return (
          <g>
            <circle cx={0} cy={0} r={34} fill="#0F172A" stroke={mau} strokeWidth={4} />
            <text
              x={0}
              y={14}
              textAnchor="middle"
              fill={mau}
              fontSize={44}
              fontWeight={800}
              fontFamily="Segoe UI, Arial, sans-serif"
            >
              ?
            </text>
          </g>
        );
    }
  };

  return (
    <g transform={`translate(${daoCu.x}, ${daoCu.y}) scale(${tiLe})`}>
      {veBieuTuong()}
      {daoCu.nhan && (
        <text
          x={0}
          y={72}
          textAnchor="middle"
          fill="#CBD5E1"
          fontSize={16}
          fontWeight={600}
          fontFamily="Segoe UI, Arial, sans-serif"
        >
          {daoCu.nhan}
        </text>
      )}
    </g>
  );
};
