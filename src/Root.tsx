import React from 'react';
import { Composition, Still, type CalculateMetadataFunction } from 'remotion';
import type { DuLieuVideoDai } from './kieu_dai';
import { VideoDai } from './VideoDai';
import { THUMBNAIL_MAC_DINH, ThumbnailToanHoc } from './Thumbnail';
import { chuanHoaKhungHinhLienMach } from './canh/dieu_phoi_canh';
import mauPythagoras from '../du_lieu/mau_pythagoras.json';

const duLieuMau = mauPythagoras as DuLieuVideoDai;

function tinhTongFrames(duLieu: DuLieuVideoDai): number {
  const { tongFrames } = chuanHoaKhungHinhLienMach(duLieu.chuong ?? []);
  return Math.max(30, tongFrames);
}

const tinhMetadata: CalculateMetadataFunction<DuLieuVideoDai> = ({ props }) => {
  return {
    durationInFrames: tinhTongFrames(props),
  };
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
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
      <Still
        id="ThumbnailToanHoc"
        component={ThumbnailToanHoc}
        width={1280}
        height={720}
        defaultProps={THUMBNAIL_MAC_DINH}
      />
    </>
  );
};
