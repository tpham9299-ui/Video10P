import React, { useMemo } from 'react';
import {
  AbsoluteFill,
  Audio,
  getStaticFiles,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import type {
  Canh,
  DuLieuVideoDai,
  LoaiChuyenCanh,
  ThongTinNhanVat,
} from './kieu_dai';
import { layAmLuongSfx, layDuongDanSfxNeuCoSan } from './amthanh/sfx';
import { CanhMoDau } from './canh/CanhMoDau';
import { CanhKeChuyen } from './canh/CanhKeChuyen';
import { CanhDoiThoai } from './canh/CanhDoiThoai';
import { CanhHaiHuoc } from './canh/CanhHaiHuoc';
import { CanhGiaiThichToan } from './canh/CanhGiaiThichToan';
import { CanhDongThoiGian } from './canh/CanhDongThoiGian';
import { CanhKet } from './canh/CanhKet';
import { CanhTuongTacKhanGia } from './canh/CanhTuongTacKhanGia';
import { CanhChiaDoiManHinh } from './canh/CanhChiaDoiManHinh';
import { timLuotThoaiTaiFrame } from './nhanvat/dien_xuat';
import {
  chuanHoaKhungHinhLienMach,
  type CanhDaCanKhung,
} from './canh/dieu_phoi_canh';
import { easeInOutCubic, kepGiaTri, noiSuy } from './xuong/duong_cong';

/**
 * Lop chuyen canh hoat hinh toan man hinh (v0.4):
 * Hien thuc hoa du 3 kieu:
 * - mo_dan: mo dan dong-mo em ai
 * - quet_ngang: man quet ngang vien vang dong-mo nhanh gon
 * - vong_tron_hoat_hinh: Iris Wipe dong-mo hinh tron kinh dien phim hoat hinh
 */
const LopChuyenCanhCanh: React.FC<{
  chuyenCanhVao?: LoaiChuyenCanh;
  chuyenCanhRa?: LoaiChuyenCanh;
  thoiLuongCanh: number;
}> = ({ chuyenCanhVao, chuyenCanhRa, thoiLuongCanh }) => {
  const frame = useCurrentFrame();

  const veHieuUng = (
    loai: LoaiChuyenCanh,
    tienDoMo: number, // 0 = che kin hoan toan, 1 = mo ra hoan toan
    laPhaRa: boolean,
  ) => {
    const e = easeInOutCubic(kepGiaTri(tienDoMo, 0, 1));

    if (loai === 'mo_dan') {
      // Giu do mo toi da 0.62 de chuyen canh muot ma, khong tao khung den tuyet doi (gap frame)
      const op = (1 - e) * 0.62;
      if (op <= 0.005) return null;
      return (
        <div
          style={{
            position: 'absolute',
            inset: 0,
            backgroundColor: '#0F172A',
            opacity: op,
            pointerEvents: 'none',
            zIndex: 35,
          }}
        />
      );
    }

    if (loai === 'quet_ngang') {
      if (e >= 0.995) return null;
      // Pha vao: man quet di chuyen tu 0 -> 1980; pha ra: man quet truot tu -1980 -> 0
      const leftX = laPhaRa ? noiSuy(0, -1980, e) : noiSuy(0, 1980, e);
      return (
        <div
          style={{
            position: 'absolute',
            top: 0,
            bottom: 0,
            left: leftX,
            width: 1960,
            backgroundColor: '#1E293B',
            borderLeft: laPhaRa ? undefined : '16px solid #FACC15',
            borderRight: laPhaRa ? '16px solid #FACC15' : undefined,
            pointerEvents: 'none',
            zIndex: 35,
          }}
        />
      );
    }

    // vong_tron_hoat_hinh: Iris Wipe dong-mo hinh tron (ban kinh toi thieu > 0 tranh khung den chet)
    if (e >= 0.995) return null;
    const r = Math.max(48, noiSuy(48, 1320, e));
    const cx = 960;
    const cy = 540;
    const d = `M 0 0 H 1920 V 1080 H 0 Z M ${cx - r} ${cy} a ${r} ${r} 0 1 0 ${r * 2} 0 a ${r} ${r} 0 1 0 ${-r * 2} 0 Z`;

    return (
      <svg
        width={1920}
        height={1080}
        viewBox="0 0 1920 1080"
        style={{
          position: 'absolute',
          inset: 0,
          pointerEvents: 'none',
          zIndex: 35,
        }}
      >
        <path d={d} fill="#0F172A" fillRule="evenodd" />
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke="#FACC15"
          strokeWidth={7}
        />
      </svg>
    );
  };

  // Pha vao dau canh (bat dau tu (frame + 1) / (doDaiVao + 1) de khong dong cung 100% toi o frame 0)
  if (chuyenCanhVao) {
    const doDaiVao =
      chuyenCanhVao === 'vong_tron_hoat_hinh'
        ? 16
        : chuyenCanhVao === 'quet_ngang'
          ? 12
          : 10;
    if (frame < doDaiVao) {
      return veHieuUng(chuyenCanhVao, (frame + 1) / (doDaiVao + 1), false);
    }
  }

  // Pha dong o cuoi canh khi canh tiep theo co khai bao chuyenCanh
  if (chuyenCanhRa) {
    const doDaiRa =
      chuyenCanhRa === 'vong_tron_hoat_hinh'
        ? 12
        : chuyenCanhRa === 'quet_ngang'
          ? 10
          : 8;
    const conLai = thoiLuongCanh - 1 - frame;
    if (conLai >= 0 && conLai < doDaiRa) {
      return veHieuUng(chuyenCanhRa, (conLai + 1) / (doDaiRa + 1), true);
    }
  }

  return null;
};

/** Phu de 16:9 de doc tren ca nen sang (troi xanh/giay kem) lan nen toi (troi dem) */
const PhuDeCanh: React.FC<{
  canh: Canh;
  mauVien: string;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
}> = ({ canh, mauVien, banDoNhanVat }) => {
  const frame = useCurrentFrame();
  const tong = Math.max(1, canh.denFrame - canh.tuFrame);
  const luotHienTai = timLuotThoaiTaiFrame(canh.luotThoai, frame);

  let noiDung = '';
  if (luotHienTai && luotHienTai.noiDung) {
    const ten = banDoNhanVat[luotHienTai.nhanVatId]?.ten;
    noiDung = ten ? `${ten}: ${luotHienTai.noiDung}` : luotHienTai.noiDung;
  } else {
    const danhSachDong =
      canh.phuDe && canh.phuDe.length > 0 ? canh.phuDe : [canh.loiThoai];
    const chiSo = Math.min(
      danhSachDong.length - 1,
      Math.floor((frame / tong) * danhSachDong.length),
    );
    noiDung = danhSachDong[chiSo] ?? '';
  }

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
  batSfx = true,
  batPhuDe = true,
  danhSachNhanVat,
  chuong,
}) => {
  const frameToanCuc = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Danh sach file that dang co trong public/ de chan crash neu 1 file SFX bi xoa trong tuong lai
  const tapFilePublic = useMemo(() => {
    try {
      const files = getStaticFiles();
      return new Set(files.map((f) => f.name.replace(/^\/+/, '')));
    } catch {
      return null;
    }
  }, []);

  const banDoNhanVat = useMemo(() => {
    const map: Record<string, ThongTinNhanVat> = {};
    for (const nv of danhSachNhanVat) {
      map[nv.id] = nv;
    }
    return map;
  }, [danhSachNhanVat]);

  const { danhSachCanh: tatCaCanh, thongKeChuong, tongFrames } = useMemo(
    () => chuanHoaKhungHinhLienMach(chuong),
    [chuong],
  );

  const veNoiDungCanh = (muc: CanhDaCanKhung) => {
    const { canh, tenChuong, hienManHinhKetThuc } = muc;

    // Uu tien che do chia doi man hinh (gocQuay="chia_doi_man_hinh") va canh tuong tac khan gia v2.0
    if (!hienManHinhKetThuc && canh.mayQuay?.gocQuay === 'chia_doi_man_hinh') {
      return (
        <CanhChiaDoiManHinh
          canh={canh}
          bangMau={bangMau}
          banDoNhanVat={banDoNhanVat}
        />
      );
    }

    if (!hienManHinhKetThuc && canh.loaiCanh === 'tuong_tac_khan_gia') {
      return (
        <CanhTuongTacKhanGia
          canh={canh}
          bangMau={bangMau}
          banDoNhanVat={banDoNhanVat}
        />
      );
    }

    if (
      !hienManHinhKetThuc &&
      canh.loaiCanh === 'doi_thoai' &&
      canh.boCuc !== 'giai_thich_toan' &&
      canh.boCuc !== 'mo_dau'
    ) {
      return (
        <CanhDoiThoai
          canh={canh}
          bangMau={bangMau}
          banDoNhanVat={banDoNhanVat}
        />
      );
    }

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
        // Chi cho phep hien thi man hinh ket thuc / outro o canh cuoi cung cua hoi cuoi cung toan tap
        if (hienManHinhKetThuc) {
          return (
            <CanhKet
              canh={canh}
              tieuDeVideo={tieuDe}
              bangMau={bangMau}
              banDoNhanVat={banDoNhanVat}
              hienBannerKetThuc={true}
            />
          );
        }
        return (
          <CanhKeChuyen
            canh={canh}
            tenChuong={tenChuong}
            bangMau={bangMau}
            banDoNhanVat={banDoNhanVat}
          />
        );
      default:
        return (
          <CanhKeChuyen
            canh={canh}
            tenChuong={tenChuong}
            bangMau={bangMau}
            banDoNhanVat={banDoNhanVat}
          />
        );
    }
  };

  return (
    <AbsoluteFill
      style={{
        backgroundColor: bangMau.nenChinh || '#0F172A',
        fontFamily: 'Segoe UI, Arial, sans-serif',
        overflow: 'hidden',
      }}
    >
      {/* Chuoi canh noi tiep lien mach 100% tu frame 0 den frame cuoi (khong gap frame) */}
      {tatCaCanh.map((muc, idx) => {
        const laCuoi = idx === tatCaCanh.length - 1;
        const phanBuCuoi =
          laCuoi && tongFrames < durationInFrames
            ? durationInFrames - tongFrames
            : 0;
        const thoiLuongCanh = muc.thoiLuongCanh + phanBuCuoi;
        return (
          <Sequence
            key={`${muc.canh.id}-${idx}`}
            from={muc.tuFrameThuc}
            durationInFrames={thoiLuongCanh}
            name={`${muc.canh.id} (${muc.canh.boCuc})`}
          >
            {veNoiDungCanh(muc)}

            {batPhuDe && (
              <PhuDeCanh
                canh={muc.canh}
                mauVien={bangMau.nhanManh || '#FACC15'}
                banDoNhanVat={banDoNhanVat}
              />
            )}

            <LopChuyenCanhCanh
              chuyenCanhVao={muc.canh.chuyenCanh}
              chuyenCanhRa={muc.chuyenCanhTiepTheo}
              thoiLuongCanh={thoiLuongCanh}
            />

            {muc.canh.audioSrc && (
              <Audio src={staticFile(muc.canh.audioSrc)} />
            )}

            {batSfx &&
              muc.canh.hieuUngHoatHinh?.map((hu, idx) => {
                const duongDan = layDuongDanSfxNeuCoSan(hu.loai, tapFilePublic);
                if (!duongDan) {
                  return null;
                }
                return (
                  <Sequence
                    key={`sfx-${muc.canh.id}-${idx}`}
                    from={hu.tuFrame}
                    durationInFrames={Math.max(1, hu.thoiLuong)}
                  >
                    <Audio
                      src={staticFile(duongDan)}
                      volume={layAmLuongSfx(hu.loai)}
                    />
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
