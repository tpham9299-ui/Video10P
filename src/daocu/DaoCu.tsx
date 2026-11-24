import React from 'react';
import type { DaoCuTrongCanh } from '../kieu_dai';

type DaoCuProps = {
  daoCu: DaoCuTrongCanh;
};

export const DaoCu: React.FC<DaoCuProps> = ({ daoCu }) => {
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
