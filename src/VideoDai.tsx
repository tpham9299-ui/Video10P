import React, { useMemo } from 'react';
import {
  AbsoluteFill,
  Audio,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import type { Canh, DuLieuVideoDai, ThongTinNhanVat } from './kieu_dai';
import { layDuongDanSfxNeuCoSan } from './amthanh/sfx';
import { BoiCanhHoatHinh } from './boicanh/BoiCanhHoatHinh';
import { CanhMoDau } from './canh/CanhMoDau';
import { CanhKeChuyen } from './canh/CanhKeChuyen';
import { CanhDoiThoai } from './canh/CanhDoiThoai';
import { CanhHaiHuoc } from './canh/CanhHaiHuoc';
import { CanhGiaiThichToan } from './canh/CanhGiaiThichToan';
import { CanhDongThoiGian } from './canh/CanhDongThoiGian';
import { CanhKet } from './canh/CanhKet';

type CanhKemChuong = {
  canh: Canh;
  tenChuong: string;
  chuongId: string;
};

/** Phu de 16:9 de doc tren ca nen sang (troi xanh/giay kem) lan nen toi (troi dem) */
const PhuDeCanh: React.FC<{ canh: Canh; mauVien: string }> = ({
  canh,
  mauVien,
}) => {
  const frame = useCurrentFrame();
  const tong = Math.max(1, canh.denFrame - canh.tuFrame);
  const danhSachDong =
    canh.phuDe && canh.phuDe.length > 0 ? canh.phuDe : [canh.loiThoai];
  const chiSo = Math.min(
    danhSachDong.length - 1,
    Math.floor((frame / tong) * danhSachDong.length),
  );
  const noiDung = danhSachDong[chiSo];

  if (!noiDung) {
    return null;
  }

  return (
    <div
      style={{
        position: 'absolute',
        left: 140,
        right: 140,
        bottom: 36,
        display: 'flex',
        justifyContent: 'center',
        pointerEvents: 'none',
        zIndex: 30,
      }}
    >
      <div
        style={{
          padding: '14px 30px',
          borderRadius: 16,
          backgroundColor: 'rgba(15, 23, 42, 0.9)',
          border: `2.5px solid ${mauVien}`,
          color: '#FFFFFF',
          fontSize: 28,
          fontWeight: 700,
          lineHeight: 1.35,
          textAlign: 'center',
          maxWidth: 1520,
          fontFamily: 'Segoe UI, Arial, sans-serif',
        }}
      >
        {noiDung}
      </div>
    </div>
  );
};

export const VideoDai: React.FC<DuLieuVideoDai> = ({
  tieuDe,
  chuDe,
  bangMau,
  batSfx = false,
  batPhuDe = true,
  danhSachNhanVat,
  chuong,
}) => {
  const frameToanCuc = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const banDoNhanVat = useMemo(() => {
    const map: Record<string, ThongTinNhanVat> = {};
    for (const nv of danhSachNhanVat) {
      map[nv.id] = nv;
    }
    return map;
  }, [danhSachNhanVat]);

  const tatCaCanh = useMemo<CanhKemChuong[]>(() => {
    const ketQua: CanhKemChuong[] = [];
    for (const ch of chuong) {
      for (const c of ch.canh) {
        ketQua.push({
          canh: c,
          tenChuong: ch.tenChuong,
          chuongId: ch.id,
        });
      }
    }
    return ketQua;
  }, [chuong]);

  const thongKeChuong = useMemo(() => {
    return chuong.map((ch) => {
      const tu = ch.canh.length > 0 ? ch.canh[0].tuFrame : 0;
      const den =
        ch.canh.length > 0 ? ch.canh[ch.canh.length - 1].denFrame : tu;
      return {
        id: ch.id,
        tenChuong: ch.tenChuong,
        tuFrame: tu,
        denFrame: den,
      };
    });
  }, [chuong]);

  const veNoiDungCanh = (muc: CanhKemChuong) => {
    const { canh, tenChuong } = muc;
    switch (canh.boCuc) {
      case 'mo_dau':
        return (
          <CanhMoDau
            canh={canh}
            tieuDeVideo={tieuDe}
            chuDeVideo={chuDe}
            bangMau={bangMau}
            banDoNhanVat={banDoNhanVat}
          />
        );
      case 'ke_chuyen':
        return (
          <CanhKeChuyen
            canh={canh}
            tenChuong={tenChuong}
            bangMau={bangMau}
            banDoNhanVat={banDoNhanVat}
          />
        );
      case 'doi_thoai':
        return (
          <CanhDoiThoai
            canh={canh}
            bangMau={bangMau}
            banDoNhanVat={banDoNhanVat}
          />
        );
      case 'hai_huoc':
        return (
          <CanhHaiHuoc
            canh={canh}
            bangMau={bangMau}
            banDoNhanVat={banDoNhanVat}
          />
        );
      case 'giai_thich_toan':
        return (
          <CanhGiaiThichToan
            canh={canh}
            bangMau={bangMau}
            banDoNhanVat={banDoNhanVat}
          />
        );
      case 'dong_thoi_gian':
        return (
          <CanhDongThoiGian
            canh={canh}
            bangMau={bangMau}
            banDoNhanVat={banDoNhanVat}
          />
        );
      case 'ket_thuc':
      default:
        return (
          <CanhKet
            canh={canh}
            tieuDeVideo={tieuDe}
            bangMau={bangMau}
            banDoNhanVat={banDoNhanVat}
          />
        );
    }
  };

  return (
    <AbsoluteFill
      style={{
        backgroundColor: bangMau.nenChinh || '#0EA5E9',
        fontFamily: 'Segoe UI, Arial, sans-serif',
        overflow: 'hidden',
      }}
    >
      {/* Nen mac dinh du phong */}
      <BoiCanhHoatHinh loai="bo_bien_hy_lap" thoiTiet="nang_dep" />

      {/* Chuoi canh noi tiep bang Sequence */}
      {tatCaCanh.map((muc) => {
        const thoiLuongCanh = Math.max(1, muc.canh.denFrame - muc.canh.tuFrame);
        return (
          <Sequence
            key={muc.canh.id}
            from={muc.canh.tuFrame}
            durationInFrames={thoiLuongCanh}
            name={`${muc.canh.id} (${muc.canh.boCuc})`}
          >
            {veNoiDungCanh(muc)}

            {batPhuDe && (
              <PhuDeCanh
                canh={muc.canh}
                mauVien={bangMau.nhanManh || '#FACC15'}
              />
            )}

            {muc.canh.audioSrc && (
              <Audio src={staticFile(muc.canh.audioSrc)} />
            )}

            {batSfx &&
              muc.canh.hieuUngHoatHinh?.map((hu, idx) => {
                const duongDan = layDuongDanSfxNeuCoSan(hu.loai);
                if (!duongDan) {
                  return null;
                }
                return (
                  <Sequence
                    key={`sfx-${muc.canh.id}-${idx}`}
                    from={hu.tuFrame}
                    durationInFrames={Math.max(1, hu.thoiLuong)}
                  >
                    <Audio src={staticFile(duongDan)} />
                  </Sequence>
                );
              })}
          </Sequence>
        );
      })}

      {/* Thanh tien do chuong gon dep o mep tren */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: 38,
          backgroundColor: 'rgba(15, 23, 42, 0.86)',
          borderBottom: `2px solid ${bangMau.nhanManh || '#FACC15'}`,
          display: 'flex',
          alignItems: 'center',
          padding: '0 24px',
          gap: 12,
          boxSizing: 'border-box',
          zIndex: 40,
        }}
      >
        {thongKeChuong.map((ch) => {
          const doDai = Math.max(1, ch.denFrame - ch.tuFrame);
          const tiLeDoRong = (doDai / Math.max(1, durationInFrames)) * 100;
          const tienDoChuong = Math.max(
            0,
            Math.min(1, (frameToanCuc - ch.tuFrame) / doDai),
          );
          const dangPhat =
            frameToanCuc >= ch.tuFrame && frameToanCuc < ch.denFrame;

          return (
            <div
              key={ch.id}
              style={{
                width: `${tiLeDoRong}%`,
                display: 'flex',
                flexDirection: 'column',
                gap: 4,
              }}
            >
              <div
                style={{
                  fontSize: 13,
                  fontWeight: dangPhat ? 800 : 600,
                  color: dangPhat ? '#FEF08A' : '#CBD5E1',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                }}
              >
                {ch.tenChuong}
              </div>
              <div
                style={{
                  height: 4,
                  width: '100%',
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  borderRadius: 999,
                  overflow: 'hidden',
                }}
              >
                <div
                  style={{
                    height: '100%',
                    width: `${tienDoChuong * 100}%`,
                    backgroundColor: dangPhat ? '#FACC15' : '#94A3B8',
                  }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
