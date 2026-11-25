import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import type {
  BienTheThumbnail,
  DuLieuThumbnail,
  LoaiBieuCam,
  LoaiBoiCanh,
  LoaiDaoCu,
  LoaiHanhDong,
  LoaiVatCamTay,
  NhanVatTrongCanh,
  ThongTinNhanVat,
} from './kieu_dai';
import { BoiCanhHoatHinh } from './boicanh/BoiCanhHoatHinh';
import { NguoiQueDong } from './nhanvat/NguoiQueDong';
import { CongThucMath } from './daocu/CongThucMath';
import { DaoCu } from './daocu/DaoCu';
import { bamTatDinh } from './vfx/tat_dinh';

export const THUMBNAIL_MAC_DINH: DuLieuThumbnail = {
  bien_the: 1,
  tieuDeLon: 'CON SỐ BỊ CẤM!',
  nhanPhu: 'BÍ MẬT TOÁN HỌC',
  congThucLatex: '\\sqrt{2} \\notin \\mathbb{Q}',
  daoCuNoiBat: 'compa_co',
  boiCanh: 'quang_truong_hy_lap',
  thoiTiet: 'nang_dep',
  nhanVat: {
    id: 'pythagoras',
    ten: 'Pythagoras',
    mauThan: '#0F172A',
    mauChuDao: '#EA580C',
    mauDa: '#FFFDF7',
    phuKien: 'vong_nguyet_que',
  },
  bieuCam: 'ngac_nhien',
  hanhDong: 'giat_minh_nhay_dung',
  vatCamTay: 'cuon_giay',
  mauNhan: '#FACC15',
  mauNen: '#0F172A',
  tieuDeVideo: 'Số Vô Tỉ √2 Và Bí Mật Trường Phái Pythagoras',
};

const NHAN_VAT_DU_PHONG: ThongTinNhanVat = {
  id: 'nha_toan_hoc',
  ten: 'Nhà Toán Học',
  mauThan: '#0F172A',
  mauChuDao: '#2563EB',
  mauDa: '#FFFDF7',
  phuKien: 'kinh_tron',
};

/** Rut gon dong chu lon toi da 4 tu de doc ro tren man hinh dien thoai */
export function chuanHoaTieuDeThumbnail(vanBan: string): string {
  const tu = (vanBan || '').trim().split(/\s+/).filter(Boolean);
  if (tu.length === 0) return 'BÍ ẨN TOÁN HỌC';
  return tu.slice(0, 4).join(' ').toUpperCase();
}

/** Ve tia sunburst tat dinh 100% (khong blur, khong Math.random) */
const TiaSunburst: React.FC<{
  cx: number;
  cy: number;
  soTia: number;
  mau: string;
  doMo: number;
}> = ({ cx, cy, soTia, mau, doMo }) => {
  const banKinh = 1480;
  return (
    <g transform={`translate(${cx}, ${cy})`} opacity={doMo}>
      {Array.from({ length: soTia }).map((_, i) => {
        const a1 = (i / soTia) * Math.PI * 2;
        const a2 = ((i + 0.45) / soTia) * Math.PI * 2;
        return (
          <polygon
            key={`tb-tia-${i}`}
            points={`0,0 ${(Math.cos(a1) * banKinh).toFixed(1)},${(Math.sin(a1) * banKinh).toFixed(1)} ${(Math.cos(a2) * banKinh).toFixed(1)},${(Math.sin(a2) * banKinh).toFixed(1)}`}
            fill={mau}
          />
        );
      })}
    </g>
  );
};

/** Ve cac ngoi sao/cham trang tri tat dinh quanh khu vuc trung tam */
const HatNhanManhTatDinh: React.FC<{ seed: number; mau: string }> = ({ seed, mau }) => {
  return (
    <g pointerEvents="none">
      {Array.from({ length: 12 }).map((_, i) => {
        const x = 60 + bamTatDinh(seed * 17 + i * 29) * 1160;
        const y = 55 + bamTatDinh(seed * 31 + i * 19) * 610;
        const r = 4 + bamTatDinh(seed * 13 + i * 7) * 6;
        return (
          <g key={`hat-${i}`} transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)})`}>
            <polygon
              points={`0,${-r * 1.7} ${r * 0.55},${-r * 0.55} ${r * 1.7},0 ${r * 0.55},${r * 0.55} 0,${r * 1.7} ${-r * 0.55},${r * 0.55} ${-r * 1.7},0 ${-r * 0.55},${-r * 0.55}`}
              fill={mau}
              fillOpacity={0.78}
            />
          </g>
        );
      })}
    </g>
  );
};

/** Vien chu tuong phan cao khong dung blur, doc ro o kich thuoc dien thoai */
const ChuLonNoiBat: React.FC<{
  text: string;
  fontSize?: number;
  mauChu?: string;
  mauNenBadge?: string;
  mauVienBadge?: string;
  canLe?: 'left' | 'center' | 'right';
}> = ({
  text,
  fontSize = 86,
  mauChu = '#FEF08A',
  mauNenBadge = '#0F172A',
  mauVienBadge = '#FACC15',
  canLe = 'left',
}) => {
  return (
    <div
      style={{
        display: 'inline-block',
        backgroundColor: mauNenBadge,
        border: `6px solid ${mauVienBadge}`,
        borderRadius: 22,
        padding: '14px 28px',
        boxShadow: '0 10px 0 #020617',
        textAlign: canLe,
        maxWidth: '100%',
        boxSizing: 'border-box',
      }}
    >
      <div
        style={{
          color: mauChu,
          fontSize,
          fontWeight: 900,
          lineHeight: 1.04,
          letterSpacing: -1,
          fontFamily: '"Segoe UI", Arial, sans-serif',
          WebkitTextStroke: '3px #020617',
          textShadow: '4px 5px 0 #020617',
          wordBreak: 'break-word',
        }}
      >
        {text}
      </div>
    </div>
  );
};

/**
 * Composition Still 1280x720 tu xuat 3 bien the Thumbnail A/B cho YouTube Test & Compare:
 * - bien_the = 1: Kinh dien doi lap — Nhan vat lon ben trai, Chu lon + Bang KaTeX & DaoCu ben phai
 * - bien_the = 2: Chia doi cheo kich tinh — Chu lon & Cong thuc tren nen toi ben trai, Nhan vat & DaoCu ben phai
 * - bien_the = 3: Tam diem bang xanh — Cong thuc KaTeX khong lo tren bang xanh + Nhan vat can mat goc phai duoi
 */
export const ThumbnailToanHoc: React.FC<DuLieuThumbnail> = (props) => {
  const bienThe: BienTheThumbnail =
    props.bien_the === 2 || props.bien_the === 3 ? props.bien_the : 1;
  const tieuDeLon = chuanHoaTieuDeThumbnail(props.tieuDeLon || 'BÍ ẨN TOÁN HỌC');
  const nhanPhu = (props.nhanPhu || 'LỊCH SỬ TOÁN HỌC').trim().toUpperCase();
  const congThucLatex = (props.congThucLatex || 'a^2 + b^2 = c^2').trim();
  const daoCuNoiBat: LoaiDaoCu = props.daoCuNoiBat ?? 'compa_co';
  const boiCanh: LoaiBoiCanh = props.boiCanh ?? 'quang_truong_hy_lap';
  const nhanVat: ThongTinNhanVat = props.nhanVat ?? NHAN_VAT_DU_PHONG;
  const bieuCam: LoaiBieuCam =
    props.bieuCam ?? (bienThe === 1 ? 'ngac_nhien' : bienThe === 2 ? 'hoang_mang' : 'tinh_quai');
  const hanhDong: LoaiHanhDong =
    props.hanhDong ??
    (bienThe === 1
      ? 'giat_minh_nhay_dung'
      : bienThe === 2
        ? 'ho_het_sung_suong'
        : 'chi_tro_giai_thich');
  const vatCamTay: LoaiVatCamTay = props.vatCamTay ?? 'cuon_giay';
  const mauNhan = props.mauNhan ?? '#FACC15';
  const mauNen = props.mauNen ?? '#0F172A';
  const anhBoiCanhAI = typeof props.anhBoiCanh === 'string' && props.anhBoiCanh.trim().length > 0
    ? props.anhBoiCanh.trim()
    : null;

  /** Phong nen uu tien anh minh hoa AI cua tap (v3.5), fallback BoiCanhHoatHinh SVG (KHONG blur) */
  const renderNenThumbnail = () => {
    if (anhBoiCanhAI) {
      return (
        <Img
          src={staticFile(anhBoiCanhAI)}
          style={{
            position: 'absolute',
            inset: 0,
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
        />
      );
    }
    return (
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: 1920,
          height: 1080,
          transform: 'scale(0.666667)',
          transformOrigin: 'top left',
        }}
      >
        <BoiCanhHoatHinh loai={boiCanh} thoiTiet={props.thoiTiet ?? 'nang_dep'} />
      </div>
    );
  };

  const taoTrangThaiNhanVat = (
    x: number,
    y: number,
    huong: 'trai' | 'phai',
    tiLe: number,
  ): NhanVatTrongCanh => ({
    id: nhanVat.id,
    x,
    y,
    huong,
    hanhDong,
    bieuCam,
    vatCamTay,
    dangNoi: false,
    tiLe,
  });

  // =========================================================================
  // BIEN THE 1: Nhan vat phong lon ben trai | Chu lon + Bang KaTeX ben phai
  // =========================================================================
  if (bienThe === 1) {
    const trangThaiNv = taoTrangThaiNhanVat(295, 755, 'phai', 2.75);
    return (
      <AbsoluteFill style={{ width: 1280, height: 720, overflow: 'hidden', backgroundColor: mauNen }}>
        {/* Nen uu tien anh minh hoa AI cua tap (v3.5), fallback BoiCanhHoatHinh SVG */}
        {renderNenThumbnail()}

        {/* Lop phu tuong phan & tia sunburst (khong blur) */}
        <svg width={1280} height={720} viewBox="0 0 1280 720" style={{ position: 'absolute', inset: 0 }}>
          <rect x={0} y={0} width={1280} height={720} fill="#0F172A" fillOpacity={0.38} />
          <TiaSunburst cx={310} cy={360} soTia={16} mau={mauNhan} doMo={0.22} />
          {/* Vong tron hao quang sau nhan vat */}
          <circle cx={305} cy={395} r={255} fill="#FFFBEB" fillOpacity={0.92} stroke={mauNhan} strokeWidth={12} />
          <circle cx={305} cy={395} r={274} fill="none" stroke="#0F172A" strokeWidth={6} />
          <HatNhanManhTatDinh seed={101} mau="#FEF08A" />

          {/* Nhan vat phong lon voi bieu cam tuong phan cao */}
          <NguoiQueDong thongTin={nhanVat} trangThai={trangThaiNv} tiLe={1} thoiLuongCanh={90} />

          {/* Dao cu Toan hoc goc phai duoi */}
          <g transform="translate(1168, 596)">
            <circle cx={0} cy={0} r={76} fill="#0F172A" stroke={mauNhan} strokeWidth={6} />
            <DaoCu daoCu={{ loai: daoCuNoiBat, x: 0, y: 0, tiLe: 0.9, mau: mauNhan }} />
          </g>
        </svg>

        {/* Khoi chu lon + bang cong thuc KaTeX ben phai */}
        <div
          style={{
            position: 'absolute',
            top: 44,
            left: 590,
            right: 42,
            bottom: 44,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            gap: 18,
          }}
        >
          {/* Nhan phu tuong phan cao */}
          <div
            style={{
              backgroundColor: '#DC2626',
              color: '#FFFFFF',
              fontSize: 28,
              fontWeight: 900,
              letterSpacing: 1.5,
              padding: '8px 22px',
              borderRadius: 12,
              border: '4px solid #FFFFFF',
              boxShadow: '0 6px 0 #0F172A',
              fontFamily: '"Segoe UI", Arial, sans-serif',
            }}
          >
            {nhanPhu}
          </div>

          {/* Tieu de 2-4 tu sieu ro */}
          <ChuLonNoiBat
            text={tieuDeLon}
            fontSize={tieuDeLon.length > 15 ? 70 : 84}
            mauChu="#FEF08A"
            mauNenBadge="#0F172A"
            mauVienBadge={mauNhan}
          />

          {/* The cong thuc KaTeX noi bat (chua khoang trong cho huy hieu dao cu goc phai duoi) */}
          <div
            style={{
              width: '74%',
              backgroundColor: '#114226',
              border: '8px solid #B45309',
              borderRadius: 22,
              padding: '22px 24px',
              boxShadow: '0 10px 0 #020617',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              minHeight: 158,
              boxSizing: 'border-box',
            }}
          >
            <CongThucMath latex={congThucLatex} fontSize={58} mau="#FEF9C3" />
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // =========================================================================
  // BIEN THE 2: Chia doi cheo kich tinh — Chu + KaTeX ben trai | Nhan vat phai
  // =========================================================================
  if (bienThe === 2) {
    const trangThaiNv = taoTrangThaiNhanVat(965, 760, 'trai', 2.8);
    return (
      <AbsoluteFill style={{ width: 1280, height: 720, overflow: 'hidden', backgroundColor: '#0B1120' }}>
        {/* Neu tap co anh nen AI (v3.5), hien thi phia sau lop chia cheo tuong phan cao */}
        {anhBoiCanhAI && renderNenThumbnail()}

        {/* Nen cheo chia 2 mang mau tuong phan manh */}
        <svg width={1280} height={720} viewBox="0 0 1280 720" style={{ position: 'absolute', inset: 0 }}>
          <rect x={0} y={0} width={1280} height={720} fill="#0F172A" fillOpacity={anhBoiCanhAI ? 0.56 : 1} />
          <polygon points="735,0 1280,0 1280,720 630,720" fill="#F59E0B" fillOpacity={anhBoiCanhAI ? 0.72 : 1} />
          <TiaSunburst cx={980} cy={360} soTia={14} mau="#FEF08A" doMo={0.35} />
          {/* Duong chia cheo sac net */}
          <line x1={735} y1={0} x2={630} y2={720} stroke="#FFFFFF" strokeWidth={14} />
          <line x1={735} y1={0} x2={630} y2={720} stroke="#0F172A" strokeWidth={5} />

          {/* Vong tron nen trang sau nhan vat ben phai */}
          <circle cx={965} cy={385} r={240} fill="#FFFDF7" stroke="#0F172A" strokeWidth={10} />
          <HatNhanManhTatDinh seed={202} mau="#FFFFFF" />

          {/* Nhan vat lon quay sang trai chi vao cong thuc */}
          <NguoiQueDong thongTin={nhanVat} trangThai={trangThaiNv} tiLe={1} thoiLuongCanh={90} />

          {/* Dao cu Toan hoc goc tren phai */}
          <g transform="translate(1168, 118)">
            <circle cx={0} cy={0} r={74} fill="#0F172A" stroke="#FEF08A" strokeWidth={5} />
            <DaoCu daoCu={{ loai: daoCuNoiBat, x: 0, y: 0, tiLe: 0.85, mau: '#FEF08A' }} />
          </g>
        </svg>

        {/* Khoi chu + KaTeX ben trai */}
        <div
          style={{
            position: 'absolute',
            top: 48,
            left: 44,
            width: 625,
            bottom: 48,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            gap: 18,
          }}
        >
          <div
            style={{
              backgroundColor: mauNhan,
              color: '#0F172A',
              fontSize: 27,
              fontWeight: 900,
              letterSpacing: 1.2,
              padding: '8px 22px',
              borderRadius: 999,
              border: '4px solid #FFFFFF',
              boxShadow: '0 6px 0 #020617',
              fontFamily: '"Segoe UI", Arial, sans-serif',
            }}
          >
            {nhanPhu}
          </div>

          <ChuLonNoiBat
            text={tieuDeLon}
            fontSize={tieuDeLon.length > 15 ? 72 : 88}
            mauChu="#FFFFFF"
            mauNenBadge="#DC2626"
            mauVienBadge="#FEF08A"
          />

          <div
            style={{
              width: '100%',
              backgroundColor: '#1E293B',
              border: `6px solid ${mauNhan}`,
              borderRadius: 20,
              padding: '20px 24px',
              boxShadow: '0 10px 0 #020617',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              minHeight: 162,
              boxSizing: 'border-box',
            }}
          >
            <CongThucMath latex={congThucLatex} fontSize={56} mau="#FEF08A" />
          </div>
        </div>
      </AbsoluteFill>
    );
  }

  // =========================================================================
  // BIEN THE 3: Tam diem bang xanh khong lo + Nhan vat can mat goc duoi phai
  // =========================================================================
  const trangThaiNv3 = taoTrangThaiNhanVat(1035, 800, 'trai', 3.0);
  return (
    <AbsoluteFill style={{ width: 1280, height: 720, overflow: 'hidden', backgroundColor: '#114226' }}>
      {/* Neu tap co anh nen AI (v3.5), hien thi phia sau lop bang xanh ban trong suot (khong blur) */}
      {anhBoiCanhAI && renderNenThumbnail()}

      {/* Khung bang xanh lop hoc vien go co dien + luoi ke o nhe */}
      <svg width={1280} height={720} viewBox="0 0 1280 720" style={{ position: 'absolute', inset: 0 }}>
        <rect x={0} y={0} width={1280} height={720} fill="#114226" fillOpacity={anhBoiCanhAI ? 0.68 : 1} />
        {/* Luoi o ly bang xanh nhe */}
        {Array.from({ length: 16 }).map((_, i) => (
          <line
            key={`gx-${i}`}
            x1={i * 80}
            y1={0}
            x2={i * 80}
            y2={720}
            stroke="#FFFFFF"
            strokeOpacity={0.07}
            strokeWidth={2}
          />
        ))}
        {Array.from({ length: 9 }).map((_, i) => (
          <line
            key={`gy-${i}`}
            x1={0}
            y1={i * 80}
            x2={1280}
            y2={i * 80}
            stroke="#FFFFFF"
            strokeOpacity={0.07}
            strokeWidth={2}
          />
        ))}
        {/* Khung go bao quanh man hinh */}
        <rect
          x={14}
          y={14}
          width={1252}
          height={692}
          rx={24}
          fill="none"
          stroke="#B45309"
          strokeWidth={24}
        />
        <rect
          x={26}
          y={26}
          width={1228}
          height={668}
          rx={14}
          fill="none"
          stroke="#FDE68A"
          strokeOpacity={0.35}
          strokeWidth={4}
        />

        {/* Dao cu Toan hoc goc tren trai */}
        <g transform="translate(128, 134)">
          <circle cx={0} cy={0} r={76} fill="#092B19" stroke={mauNhan} strokeWidth={5} />
          <DaoCu daoCu={{ loai: daoCuNoiBat, x: 0, y: 0, tiLe: 0.9, mau: '#FEF08A' }} />
        </g>

        {/* Vong tron noi bat phia sau nhan vat goc phai duoi */}
        <circle cx={1040} cy={475} r={220} fill="#FEF3C7" stroke={mauNhan} strokeWidth={10} />
        <HatNhanManhTatDinh seed={303} mau="#FEF08A" />

        {/* Nhan vat can mat bieu cam manh */}
        <NguoiQueDong thongTin={nhanVat} trangThai={trangThaiNv3} tiLe={1} thoiLuongCanh={90} />
      </svg>

      {/* Nhan goc tren phai */}
      <div
        style={{
          position: 'absolute',
          top: 44,
          right: 52,
          backgroundColor: '#FACC15',
          color: '#0F172A',
          fontSize: 26,
          fontWeight: 900,
          padding: '8px 22px',
          borderRadius: 12,
          border: '4px solid #0F172A',
          boxShadow: '0 6px 0 #020617',
          fontFamily: '"Segoe UI", Arial, sans-serif',
        }}
      >
        {nhanPhu}
      </div>

      {/* Cong thuc KaTeX khong lo o phia tren trung tam-trai */}
      <div
        style={{
          position: 'absolute',
          top: 94,
          left: 228,
          width: 680,
          minHeight: 240,
          backgroundColor: 'rgba(9, 43, 25, 0.9)',
          border: '6px dashed #FEF08A',
          borderRadius: 24,
          padding: '24px 30px',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          boxSizing: 'border-box',
        }}
      >
        <CongThucMath latex={congThucLatex} fontSize={74} mau="#FEF9C3" />
      </div>

      {/* Dong chu lon 2-4 tu noi bat goc duoi trai */}
      <div
        style={{
          position: 'absolute',
          left: 56,
          bottom: 58,
          maxWidth: 740,
        }}
      >
        <ChuLonNoiBat
          text={tieuDeLon}
          fontSize={tieuDeLon.length > 15 ? 74 : 92}
          mauChu="#0F172A"
          mauNenBadge="#FACC15"
          mauVienBadge="#FFFFFF"
        />
      </div>
    </AbsoluteFill>
  );
};
