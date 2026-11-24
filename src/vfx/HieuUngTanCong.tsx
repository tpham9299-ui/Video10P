import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { HieuUngTanCongData } from '../kieu_dai';

// TODO(v0.2): nang cap xuong khop & VFX

type HieuUngTanCongProps = {
  danhSach?: HieuUngTanCongData[];
};

/**
 * Component giu cho (v0.1): hien thi vi tri, duong noi va ten hieu ung dung khoang frame
 * de kiem chung timing truoc khi nang cap he thong VFX day du o v0.2.
 */
export const HieuUngTanCong: React.FC<HieuUngTanCongProps> = ({ danhSach }) => {
  const frame = useCurrentFrame();

  if (!danhSach || danhSach.length === 0) {
    return null;
  }

  return (
    <g>
      {danhSach.map((item, idx) => {
        const ketThuc = item.tuFrame + item.thoiLuong;
        if (frame < item.tuFrame || frame > ketThuc) {
          return null;
        }

        const tienDo = interpolate(
          frame,
          [item.tuFrame, ketThuc],
          [0, 1],
          { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' },
        );
        const mau = item.mau ?? '#38BDF8';
        const banKinh = 28 + tienDo * 76;
        const doMo = 1 - tienDo * 0.7;
        const coDich =
          typeof item.denX === 'number' && typeof item.denY === 'number';
        const denX = coDich ? (item.denX as number) : item.tuX;
        const denY = coDich ? (item.denY as number) : item.tuY;
        const tamX = (item.tuX + denX) / 2;
        const tamY = (item.tuY + denY) / 2;

        return (
          <g key={`${item.loai}-${idx}`} opacity={doMo}>
            {/* Vong tron bao vi tri hieu ung */}
            <circle
              cx={item.tuX}
              cy={item.tuY}
              r={banKinh}
              fill="none"
              stroke={mau}
              strokeWidth={4}
              strokeDasharray="10 6"
            />

            {/* Duong gach noi tu -> den neu co toa do dich */}
            {coDich && (
              <>
                <line
                  x1={item.tuX}
                  y1={item.tuY}
                  x2={denX}
                  y2={denY}
                  stroke={mau}
                  strokeWidth={5}
                  strokeDasharray="14 8"
                  strokeLinecap="round"
                />
                <circle
                  cx={denX}
                  cy={denY}
                  r={18 + tienDo * 32}
                  fill="none"
                  stroke={mau}
                  strokeWidth={3}
                />
              </>
            )}

            {/* The ten hieu ung kiem chung timing */}
            <g transform={`translate(${tamX}, ${tamY - 42})`}>
              <rect
                x={-110}
                y={-22}
                width={220}
                height={34}
                rx={10}
                fill="#0F172A"
                fillOpacity={0.92}
                stroke={mau}
                strokeWidth={2}
              />
              <text
                x={0}
                y={0}
                textAnchor="middle"
                fill={mau}
                fontSize={15}
                fontWeight={700}
                fontFamily="Consolas, monospace"
              >
                {item.loai}
                {item.kyHieuToan ? ` [${item.kyHieuToan}]` : ''}
              </text>
            </g>
          </g>
        );
      })}
    </g>
  );
};
