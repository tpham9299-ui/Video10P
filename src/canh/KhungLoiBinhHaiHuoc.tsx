import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { LoiBinhHaiHuoc } from '../kieu_dai';

type KhungLoiBinhHaiHuocProps = {
  loiBinh?: LoiBinhHaiHuoc;
};

/**
 * The ghi chu hai huoc / pha vo buc tuong thu 4 cua nguoi dan chuyen o goc man hinh.
 * Khong dung blur, dung vien sac net va bong cung kieu truyen tranh hoat hinh.
 */
export const KhungLoiBinhHaiHuoc: React.FC<KhungLoiBinhHaiHuocProps> = ({
  loiBinh,
}) => {
  const frame = useCurrentFrame();

  if (!loiBinh || !loiBinh.noiDung) {
    return null;
  }

  const tuFrame = loiBinh.tuFrame ?? 10;
  if (frame < tuFrame) {
    return null;
  }

  const delta = frame - tuFrame;
  const scale =
    delta < 8
      ? interpolate(delta, [0, 8], [0.65, 1.04], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        })
      : delta < 13
        ? interpolate(delta, [8, 13], [1.04, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          })
        : 1;

  const opacity = interpolate(delta, [0, 6], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const benTrai = loiBinh.viTri === 'goc_trai';

  return (
    <div
      style={{
        position: 'absolute',
        top: 64,
        left: benTrai ? 52 : undefined,
        right: benTrai ? undefined : 52,
        maxWidth: 430,
        opacity,
        transform: `rotate(${benTrai ? -2 : 2}deg) scale(${scale.toFixed(3)})`,
        transformOrigin: benTrai ? 'top left' : 'top right',
        pointerEvents: 'none',
        zIndex: 20,
      }}
    >
      <div
        style={{
          backgroundColor: '#FFFBEB',
          border: '3.5px solid #1E293B',
          borderRadius: 18,
          padding: '14px 20px',
          boxShadow: '7px 7px 0px #1E293B',
          fontFamily: 'Segoe UI, Arial, sans-serif',
        }}
      >
        <div
          style={{
            display: 'inline-block',
            padding: '3px 10px',
            borderRadius: 999,
            backgroundColor: '#F59E0B',
            color: '#1E293B',
            fontSize: 13,
            fontWeight: 900,
            letterSpacing: 0.7,
            marginBottom: 8,
            textTransform: 'uppercase',
          }}
        >
          Góc bình luận
        </div>
        <div
          style={{
            color: '#0F172A',
            fontSize: 21,
            fontWeight: 700,
            lineHeight: 1.35,
          }}
        >
          {loiBinh.noiDung}
        </div>
      </div>
    </div>
  );
};
