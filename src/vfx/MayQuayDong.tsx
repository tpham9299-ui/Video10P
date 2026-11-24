import React from 'react';
import type { CauHinhCamera, HieuUngTanCongData } from '../kieu_dai';

// TODO(v0.2): nang cap xuong khop & VFX

type MayQuayDongProps = {
  camera?: CauHinhCamera;
  hieuUngTanCong?: HieuUngTanCongData[];
  children: React.ReactNode;
};

/**
 * Khung may quay dong (v0.1): ap dung translate + scale co ban.
 * Chua san prop hieuUngTanCong de v0.2 gan cameraShake va impactFrame.
 */
export const MayQuayDong: React.FC<MayQuayDongProps> = ({
  camera,
  hieuUngTanCong: _hieuUngTanCong,
  children,
}) => {
  const zoom = camera?.zoom ?? 1;
  const panX = camera?.panX ?? 0;
  const panY = camera?.panY ?? 0;

  // TODO(v0.2): nang cap xuong khop & VFX (bo sung cameraShake & impactFrame tu _hieuUngTanCong)
  const shakeX = 0;
  const shakeY = 0;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          width: '100%',
          height: '100%',
          transformOrigin: 'center center',
          transform: `translate(${panX + shakeX}px, ${panY + shakeY}px) scale(${zoom})`,
        }}
      >
        {children}
      </div>
    </div>
  );
};
