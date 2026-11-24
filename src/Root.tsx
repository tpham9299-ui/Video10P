import React from 'react';
import { Composition, type CalculateMetadataFunction } from 'remotion';
import type { DuLieuVideoDai } from './kieu_dai';
import { VideoDai } from './VideoDai';
import mauPythagoras from '../du_lieu/mau_pythagoras.json';

const duLieuMau = mauPythagoras as DuLieuVideoDai;

function tinhTongFrames(duLieu: DuLieuVideoDai): number {
  let maxFrame = 0;
  for (const ch of duLieu.chuong) {
    for (const c of ch.canh) {
      if (c.denFrame > maxFrame) {
        maxFrame = c.denFrame;
      }
    }
  }
  return Math.max(30, maxFrame);
}

const tinhMetadata: CalculateMetadataFunction<DuLieuVideoDai> = ({ props }) => {
  return {
    durationInFrames: tinhTongFrames(props),
  };
};

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="VideoDaiNguoiQue"
      component={VideoDai}
      width={1920}
      height={1080}
      fps={30}
      durationInFrames={tinhTongFrames(duLieuMau)}
      defaultProps={duLieuMau}
      calculateMetadata={tinhMetadata}
    />
  );
};
