import React from 'react';
import { useCurrentFrame } from 'remotion';
import type { LoiBinhHaiHuoc } from '../kieu_dai';
import { kepGiaTri, noiSuy, springTatDinh } from '../xuong/duong_cong';

type KhungLoiBinhHaiHuocProps = {
  loiBinh?: LoiBinhHaiHuoc;
};

/**
 * The ghi chu hai huoc / pha vo buc tuong thu 4 cua nguoi dan chuyen o goc man hinh.
 * Bat ra bang lo xo springTatDinh, khong dung blur, vien sac net kieu hoat hinh.
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
  const loXo = springTatDinh(delta, 11, 215);
  const scale = kepGiaTri(loXo, 0, 1.25);
  const opacity = kepGiaTri(delta / 5, 0, 1);

  const benTrai = loiBinh.viTri === 'goc_trai';
  const gocDich = benTrai ? -2 : 2;
  const gocHienTai = noiSuy(benTrai ? -9 : 9, gocDich, kepGiaTri(loXo, 0, 1.12));

  return (
    <div
      style={{
        position: 'absolute',
        top: 76,
        left: benTrai ? 52 : undefined,
        right: benTrai ? undefined : 52,
        maxWidth: 430,
        opacity,
        transform: `rotate(${gocHienTai.toFixed(2)}deg) scale(${scale.toFixed(3)})`,
        transformOrigin: benTrai ? 'top left' : 'top right',
        pointerEvents: 'none',
        zIndex: 24,
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
