import React, { useMemo } from 'react';
import {
  AbsoluteFill,
  Audio,
  Freeze,
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
 * Khung chuyen canh noi tiep phu kin 100% khung hinh (khong lo nen toi trong khi truot slide):
 * - quet_ngang: dung nen noi cua canh truoc (Freeze o frame cuoi) + quet mo canh moi tu trai sang phai voi vach vang mem
 * - mo_dan: cross-fade muot phu kin 100% khung hinh (co nen canh truoc o duoi)
 * - vong_tron_hoat_hinh: Iris Wipe hinh tron kinh dien (co nen canh truoc o duoi neu co)
 */
const KhungChuyenCanhNoiTiep: React.FC<{
  chuyenCanhVao?: LoaiChuyenCanh;
  noiDungMoi: React.ReactNode;
  noiDungTruoc?: React.ReactNode;
  frameCuoiCanhTruoc?: number;
}> = ({
  chuyenCanhVao,
  noiDungMoi,
  noiDungTruoc,
  frameCuoiCanhTruoc = 0,
}) => {
  const frame = useCurrentFrame();

  if (!chuyenCanhVao) {
    return <>{noiDungMoi}</>;
  }

  const doDaiVao =
    chuyenCanhVao === 'vong_tron_hoat_hinh'
      ? 16
      : chuyenCanhVao === 'quet_ngang'
        ? 14
        : 12;

  if (frame >= doDaiVao) {
    return <>{noiDungMoi}</>;
  }

  const e = easeInOutCubic(kepGiaTri((frame + 1) / (doDaiVao + 1), 0, 1));
  const coNenNoi = Boolean(noiDungTruoc);

  if (chuyenCanhVao === 'quet_ngang') {
    if (coNenNoi) {
      // Nen noi tu canh truoc phu kin 100% phan chua quet + canh moi phu kin 100% ben trai (tach stacking context)
      const phanTramChePhai = Math.max(0, (1 - e) * 100);
      const viTriThanhVang = e * 1920;
      return (
        <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', isolation: 'isolate' }}>
          <div style={{ position: 'absolute', inset: 0, zIndex: 1, isolation: 'isolate' }}>
            <Freeze frame={Math.max(0, frameCuoiCanhTruoc)}>
              {noiDungTruoc}
            </Freeze>
          </div>
          <div
            style={{
              position: 'absolute',
              inset: 0,
              zIndex: 2,
              isolation: 'isolate',
              clipPath: `inset(0 ${phanTramChePhai.toFixed(2)}% 0 0)`,
            }}
          >
            {noiDungMoi}
          </div>
          {e > 0.02 && e < 0.98 && (
            <div
              style={{
                position: 'absolute',
                top: 0,
                bottom: 0,
                left: viTriThanhVang - 5,
                width: 10,
                backgroundColor: '#FACC15',
                boxShadow: '0 0 0 2px rgba(15, 23, 42, 0.45)',
                pointerEvents: 'none',
                zIndex: 28,
              }}
            />
          )}
        </div>
      );
    }

    // Khong co canh truoc (canh dau tien): fade muot phu kin 100% khung hinh, khong de ho nen toi
    const op = kepGiaTri(0.35 + e * 0.65, 0, 1);
    return (
      <div style={{ position: 'absolute', inset: 0, opacity: op }}>
        {noiDungMoi}
      </div>
    );
  }

  if (chuyenCanhVao === 'mo_dan') {
    if (coNenNoi) {
      return (
        <div style={{ position: 'absolute', inset: 0, overflow: 'hidden', isolation: 'isolate' }}>
          <div style={{ position: 'absolute', inset: 0, zIndex: 1, isolation: 'isolate' }}>
            <Freeze frame={Math.max(0, frameCuoiCanhTruoc)}>
              {noiDungTruoc}
            </Freeze>
          </div>
          <div style={{ position: 'absolute', inset: 0, zIndex: 2, isolation: 'isolate', opacity: e }}>
            {noiDungMoi}
          </div>
        </div>
      );
    }
    return (
      <div
        style={{
          position: 'absolute',
          inset: 0,
          opacity: kepGiaTri(0.35 + e * 0.65, 0, 1),
        }}
      >
        {noiDungMoi}
      </div>
    );
  }

  // vong_tron_hoat_hinh: Iris Wipe hinh tron kinh dien (phu kin 100% khung hinh)
  const r = Math.max(48, noiSuy(48, 1320, e));
  const cx = 960;
  const cy = 540;
  const d = `M 0 0 H 1920 V 1080 H 0 Z M ${cx - r} ${cy} a ${r} ${r} 0 1 0 ${r * 2} 0 a ${r} ${r} 0 1 0 ${-r * 2} 0 Z`;

  return (
    <div style={{ position: 'absolute', inset: 0, overflow: 'hidden' }}>
      {noiDungMoi}
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
        <path d={d} fill="#0F172A" fillOpacity={coNenNoi ? 0.88 : 0.92} fillRule="evenodd" />
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke="#FACC15"
          strokeWidth={7}
        />
      </svg>
    </div>
  );
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
        left: 120,
        right: 120,
        bottom: 24,
        maxHeight: 120,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'flex-end',
        pointerEvents: 'none',
        zIndex: 30,
      }}
    >
      <div
        style={{
          padding: '11px 28px',
          borderRadius: 16,
          backgroundColor: 'rgba(15, 23, 42, 0.92)',
          border: `2.5px solid ${mauVien}`,
          color: '#FFFFFF',
          fontSize: 26,
          fontWeight: 700,
          lineHeight: 1.32,
          textAlign: 'center',
          maxWidth: 1540,
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

    // Uu tien bo cuc giang Toan va dong thoi gian de khong bi che khuat bang/thanh moc thoi gian
    if (
      !hienManHinhKetThuc &&
      (canh.boCuc === 'giai_thich_toan' || canh.loaiCanh === 'giang_toan')
    ) {
      return (
        <CanhGiaiThichToan
          canh={canh}
          bangMau={bangMau}
          banDoNhanVat={banDoNhanVat}
        />
      );
    }

    if (!hienManHinhKetThuc && canh.boCuc === 'dong_thoi_gian') {
      return (
        <CanhDongThoiGian
          canh={canh}
          bangMau={bangMau}
          banDoNhanVat={banDoNhanVat}
        />
      );
    }

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
        const mucTruoc = idx > 0 ? tatCaCanh[idx - 1] : undefined;
        return (
          <Sequence
            key={`${muc.canh.id}-${idx}`}
            from={muc.tuFrameThuc}
            durationInFrames={thoiLuongCanh}
            name={`${muc.canh.id} (${muc.canh.boCuc})`}
          >
            <KhungChuyenCanhNoiTiep
              chuyenCanhVao={muc.canh.chuyenCanh}
              noiDungMoi={veNoiDungCanh(muc)}
              noiDungTruoc={mucTruoc ? veNoiDungCanh(mucTruoc) : undefined}
              frameCuoiCanhTruoc={
                mucTruoc ? Math.max(0, mucTruoc.thoiLuongCanh - 1) : 0
              }
            />

            {batPhuDe && (
              <PhuDeCanh
                canh={muc.canh}
                mauVien={bangMau.nhanManh || '#FACC15'}
                banDoNhanVat={banDoNhanVat}
              />
            )}

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
