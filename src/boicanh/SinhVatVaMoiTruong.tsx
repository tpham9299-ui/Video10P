import React from 'react';
import { useCurrentFrame } from 'remotion';
import type {
  LoaiBoiCanh,
  LoaiThoiTiet,
  VatTheXungQuanh,
} from '../kieu_dai';
import { bamTatDinh } from '../vfx/tat_dinh';
import {
  giaiDanhSachVatTheXungQuanh,
  layKhungCuaSoChoBoiCanh,
  tinhBuomBay,
  tinhGocQuaLac,
  tinhViTriTaxiCo,
} from './moi_truong_logic';

type SinhVatVaMoiTruongProps = {
  boiCanh: LoaiBoiCanh;
  thoiTiet?: LoaiThoiTiet;
  vatTheXungQuanh?: readonly VatTheXungQuanh[];
  bienSoXe?: string;
};

/** 1. Dan chim hai au bay luon o cang bien / bo bien */
const DanChimHaiAu: React.FC<{
  item: VatTheXungQuanh;
  frame: number;
  seedBase: number;
}> = ({ item, frame, seedBase }) => {
  const soLuong = Math.max(1, Math.min(7, item.soLuong ?? 4));
  const x0 = item.x ?? 300;
  const y0 = item.y ?? 185;
  const tocDo = item.tocDo ?? 1.35;
  const tiLe = item.tiLe ?? 1;
  const mau = item.mau ?? '#FFFFFF';

  return (
    <g pointerEvents="none">
      {Array.from({ length: soLuong }).map((_, i) => {
        const pha = i * 1.35 + seedBase * 0.4;
        const speed = tocDo * (0.85 + (i % 3) * 0.14);
        const x = (((x0 + i * 95 + frame * speed) % 2360) + 2360) % 2360 - 220;
        const vo = Math.sin(frame * 0.32 + pha);
        const y = y0 + (i % 3) * 34 + Math.sin(frame * 0.07 + pha) * 14 - vo * 3;
        const sc = tiLe * (0.72 + bamTatDinh(seedBase + i * 19) * 0.42);
        const giuaY = -7 + vo * 5;
        const mepY = vo * 11;
        return (
          <g
            key={`ha-${i}`}
            transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)}) scale(${sc.toFixed(2)})`}
          >
            <path
              d={`M -22 ${mepY.toFixed(1)} Q -10 ${giuaY.toFixed(1)} 0 0 Q 10 ${giuaY.toFixed(1)} 22 ${mepY.toFixed(1)}`}
              fill="none"
              stroke="#1E293B"
              strokeWidth={4.5}
              strokeLinecap="round"
            />
            <path
              d={`M -22 ${mepY.toFixed(1)} Q -10 ${giuaY.toFixed(1)} 0 0 Q 10 ${giuaY.toFixed(1)} 22 ${mepY.toFixed(1)}`}
              fill="none"
              stroke={mau}
              strokeWidth={2.8}
              strokeLinecap="round"
            />
          </g>
        );
      })}
    </g>
  );
};

/** 2. Dan chim bo cau / chim se bay & luon quanh san truong / pho co */
const DanChimSanTruong: React.FC<{
  item: VatTheXungQuanh;
  frame: number;
  seedBase: number;
}> = ({ item, frame, seedBase }) => {
  const soLuong = Math.max(1, Math.min(6, item.soLuong ?? 3));
  const x0 = item.x ?? 380;
  const y0 = item.y ?? 230;
  const tocDo = item.tocDo ?? 1.15;
  const tiLe = item.tiLe ?? 1;
  const mau = item.mau ?? '#475569';

  return (
    <g pointerEvents="none">
      {Array.from({ length: soLuong }).map((_, i) => {
        const pha = i * 1.6 + seedBase * 0.3;
        const x = (((x0 + i * 110 + frame * tocDo * (0.9 + (i % 2) * 0.2)) % 2320) + 2320) % 2320 - 200;
        const vo = Math.sin(frame * 0.38 + pha);
        const y = y0 + (i % 2) * 30 + Math.cos(frame * 0.08 + pha) * 12;
        const sc = tiLe * (0.68 + (i % 3) * 0.14);
        return (
          <g
            key={`cst-${i}`}
            transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)}) scale(${sc.toFixed(2)})`}
          >
            <ellipse cx={0} cy={1} rx={9} ry={4.5} fill={mau} />
            <circle cx={8} cy={-2} r={3.5} fill={mau} />
            <path
              d={`M -2 -1 Q -12 ${(-11 + vo * 12).toFixed(1)} -18 ${(vo * 10).toFixed(1)}`}
              fill="none"
              stroke="#E2E8F0"
              strokeWidth={3.2}
              strokeLinecap="round"
            />
            <path
              d={`M 2 -1 Q 10 ${(-10 + vo * 11).toFixed(1)} 14 ${(vo * 8).toFixed(1)}`}
              fill="none"
              stroke="#CBD5E1"
              strokeWidth={2.6}
              strokeLinecap="round"
            />
          </g>
        );
      })}
    </g>
  );
};

/** 3. Ca nhay & gon song lan toa tren mat nuoc */
const CaVaGonSong: React.FC<{
  item: VatTheXungQuanh;
  frame: number;
  seedBase: number;
}> = ({ item, frame, seedBase }) => {
  const soLuong = Math.max(1, Math.min(4, item.soLuong ?? 2));
  const x0 = item.x ?? 980;
  const y0 = item.y ?? 630;
  const mau = item.mau ?? '#E0F2FE';

  return (
    <g pointerEvents="none">
      {Array.from({ length: soLuong }).map((_, i) => {
        const chuKy = 120;
        const f = (frame + i * 47 + seedBase * 11) % chuKy;
        const cx = x0 + (i - (soLuong - 1) / 2) * 260;
        const cy = y0 + (i % 2) * 24;
        const tRip = (f % 60) / 60;
        const rx = 14 + tRip * 54;
        const ry = 4 + tRip * 13;
        const opRip = (1 - tRip) * 0.55;

        // Ca nhay vong cung nhanh trong 26 frame dau moi chu ky
        const dangNhay = f < 26;
        const tCa = f / 26;
        const caX = cx - 26 + tCa * 52;
        const caY = cy - Math.sin(tCa * Math.PI) * 34;
        const gocCa = -42 + tCa * 84;

        return (
          <g key={`cgs-${i}`}>
            <ellipse
              cx={cx}
              cy={cy}
              rx={rx.toFixed(1)}
              ry={ry.toFixed(1)}
              fill="none"
              stroke={mau}
              strokeOpacity={opRip.toFixed(2)}
              strokeWidth={2.4}
            />
            {dangNhay && (
              <g transform={`translate(${caX.toFixed(1)}, ${caY.toFixed(1)}) rotate(${gocCa.toFixed(1)})`}>
                <ellipse cx={0} cy={0} rx={11} ry={5} fill="#38BDF8" stroke="#0C4A6E" strokeWidth={1.8} />
                <polygon points="-10,0 -18,-6 -18,6" fill="#0284C7" />
                <circle cx={5} cy={-1} r={1.4} fill="#FFFFFF" />
              </g>
            )}
          </g>
        );
      })}
    </g>
  );
};

/** 4. Dan buom bay luon trong vuon / lang que / rung nui */
const DanBuomVuon: React.FC<{
  item: VatTheXungQuanh;
  frame: number;
  seedBase: number;
}> = ({ item, frame, seedBase }) => {
  const soLuong = Math.max(1, Math.min(5, item.soLuong ?? 3));
  const x0 = item.x ?? 560;
  const y0 = item.y ?? 610;
  const tiLe = item.tiLe ?? 1;
  const bangMauBuom = ['#FACC15', '#F472B6', '#38BDF8', '#FB923C', '#A78BFA'];

  return (
    <g pointerEvents="none">
      {Array.from({ length: soLuong }).map((_, i) => {
        const bx = x0 + i * 240;
        const by = y0 + (i % 2) * 35;
        const pos = tinhBuomBay(frame, bx, by, i + seedBase);
        const mauCanh = item.mau ?? bangMauBuom[i % bangMauBuom.length];
        return (
          <g
            key={`buom-${i}`}
            transform={`translate(${pos.x.toFixed(1)}, ${pos.y.toFixed(1)}) rotate(${pos.nghieng.toFixed(1)}) scale(${tiLe})`}
          >
            <g transform={`scale(${pos.coCanhX.toFixed(2)}, 1)`}>
              <ellipse cx={-7} cy={-4} rx={8} ry={6} fill={mauCanh} stroke="#1E293B" strokeWidth={1.3} />
              <ellipse cx={7} cy={-4} rx={8} ry={6} fill={mauCanh} stroke="#1E293B" strokeWidth={1.3} />
              <ellipse cx={-5} cy={4} rx={5.5} ry={4.2} fill="#FEF08A" stroke="#1E293B" strokeWidth={1.1} />
              <ellipse cx={5} cy={4} rx={5.5} ry={4.2} fill="#FEF08A" stroke="#1E293B" strokeWidth={1.1} />
            </g>
            <line x1={0} y1={-6} x2={0} y2={7} stroke="#1E293B" strokeWidth={2.2} strokeLinecap="round" />
          </g>
        );
      })}
    </g>
  );
};

/** 5. Hoi khoi / hoi nuoc boc len uon luon tu noi sup hoac tach tra nong */
const HoiKhoiBocLen: React.FC<{
  item: VatTheXungQuanh;
  frame: number;
  seedBase: number;
}> = ({ item, frame, seedBase }) => {
  const soLuong = Math.max(2, Math.min(5, item.soLuong ?? 3));
  const x0 = item.x ?? 1520;
  const y0 = item.y ?? 620;
  const tiLe = item.tiLe ?? 1;
  const mau = item.mau ?? '#FFFFFF';

  return (
    <g transform={`translate(${x0}, ${y0}) scale(${tiLe})`} pointerEvents="none">
      {Array.from({ length: soLuong }).map((_, i) => {
        const pha = ((frame * 0.02 + i / soLuong + seedBase * 0.13) % 1 + 1) % 1;
        const dxBase = (i - (soLuong - 1) / 2) * 18;
        const dy = -pha * 88;
        const uon1 = Math.sin(frame * 0.12 + i * 1.9) * 10;
        const uon2 = Math.cos(frame * 0.1 + i * 1.4) * 12;
        const op = Math.sin(pha * Math.PI) * 0.65;
        return (
          <path
            key={`khoi-${i}`}
            d={`M ${dxBase.toFixed(1)} ${dy.toFixed(1)} Q ${(dxBase + uon1).toFixed(1)} ${(dy - 22).toFixed(1)} ${(dxBase - uon2 * 0.5).toFixed(1)} ${(dy - 46).toFixed(1)} Q ${(dxBase + uon2).toFixed(1)} ${(dy - 68).toFixed(1)} ${(dxBase + uon1 * 0.4).toFixed(1)} ${(dy - 86).toFixed(1)}`}
            fill="none"
            stroke={mau}
            strokeOpacity={op.toFixed(2)}
            strokeWidth={4.5}
            strokeLinecap="round"
          />
        );
      })}
    </g>
  );
};

/** 6. Ngon nen / den dau rung nhe voi hao quang phang (khong blur) */
const NgonNenDenDau: React.FC<{
  item: VatTheXungQuanh;
  frame: number;
  seedBase: number;
}> = ({ item, frame, seedBase }) => {
  const x0 = item.x ?? 410;
  const y0 = item.y ?? 585;
  const tiLe = item.tiLe ?? 1;
  const rung = Math.sin(frame * 0.3 + seedBase) * 2.4 + Math.cos(frame * 0.52 + seedBase) * 1.2;
  const nhipSang = 1 + Math.sin(frame * 0.22 + seedBase) * 0.08;

  return (
    <g transform={`translate(${x0}, ${y0}) scale(${tiLe})`} pointerEvents="none">
      {/* Hao quang am phang 2 lop (khong blur) */}
      <circle cx={0} cy={-26} r={62 * nhipSang} fill="#FACC15" fillOpacity={0.12} />
      <circle cx={0} cy={-26} r={34 * nhipSang} fill="#FEF08A" fillOpacity={0.22} />
      {/* Chan de den dau dong */}
      <ellipse cx={0} cy={18} rx={22} ry={7} fill="#B45309" stroke="#78350F" strokeWidth={2.5} />
      <rect x={-11} y={-10} width={22} height={28} rx={5} fill="#FEF3C7" stroke="#D97706" strokeWidth={2.2} />
      {/* Ngon lua rung nhe */}
      <path
        d={`M 0 ${(-44 + rung * 0.7).toFixed(1)} Q ${(11 + rung * 0.5).toFixed(1)} -25 0 -13 Q ${(-11 + rung * 0.5).toFixed(1)} -25 0 ${(-44 + rung * 0.7).toFixed(1)} Z`}
        fill="#F97316"
      />
      <path
        d={`M 0 ${(-35 + rung * 0.4).toFixed(1)} Q 5 -24 0 -16 Q -5 -24 0 ${(-35 + rung * 0.4).toFixed(1)} Z`}
        fill="#FEF08A"
      />
    </g>
  );
};

/** 7. La vang roi theo gio nhe tat dinh */
const LaVangTheoGio: React.FC<{
  item: VatTheXungQuanh;
  frame: number;
  seedBase: number;
}> = ({ item, frame, seedBase }) => {
  const soLuong = Math.max(2, Math.min(12, item.soLuong ?? 6));
  const tocDo = item.tocDo ?? 1.8;

  return (
    <g pointerEvents="none">
      {Array.from({ length: soLuong }).map((_, i) => {
        const x0 = bamTatDinh(seedBase * 17 + i * 31 + 3) * 1920;
        const y0 = bamTatDinh(seedBase * 29 + i * 47 + 7) * 920;
        const y = ((y0 + frame * (tocDo + (i % 3) * 0.45)) % 980) - 40;
        const x = (((x0 + frame * 1.25 + Math.sin(frame * 0.06 + i * 1.4) * 52) % 2020) + 2020) % 2020 - 50;
        const rot = (frame * (2.2 + (i % 3) * 0.9) + i * 53) % 360;
        const mau = i % 3 === 0 ? '#F59E0B' : i % 3 === 1 ? '#EA580C' : '#EAB308';
        return (
          <g key={`lvg-${i}`} transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)}) rotate(${rot.toFixed(1)})`}>
            <path d="M -11 0 Q 0 -9 13 0 Q 0 9 -11 0 Z" fill={mau} stroke="#9A3412" strokeWidth={1.2} />
            <line x1={-9} y1={0} x2={9} y2={0} stroke="#FEF3C7" strokeWidth={1.1} />
          </g>
        );
      })}
    </g>
  );
};

/** 8. Tuyet / mua roi qua khung cua so (co clipPath cat gon 100% trong khung kinh, khong roi vao phong) */
const TuyetQuaCuaSo: React.FC<{
  item: VatTheXungQuanh;
  boiCanh: LoaiBoiCanh;
  frame: number;
  seedBase: number;
}> = ({ item, boiCanh, frame, seedBase }) => {
  const khung = layKhungCuaSoChoBoiCanh(boiCanh);
  if (!khung) {
    return null;
  }
  const x0 = khung.x;
  const y0 = khung.y;
  const w = khung.width;
  const h = khung.height;
  const soLuong = Math.max(6, Math.min(28, item.soLuong ?? 18));
  const mau = item.mau ?? '#FFFFFF';
  const clipId = `clip-tuyet-cs-${boiCanh}-${seedBase}`;

  return (
    <g pointerEvents="none">
      <defs>
        <clipPath id={clipId}>
          <rect x={x0} y={y0} width={w} height={h} rx={6} />
        </clipPath>
      </defs>
      <g clipPath={`url(#${clipId})`}>
        {Array.from({ length: soLuong }).map((_, i) => {
          const sx = x0 + bamTatDinh(seedBase * 13 + i * 29) * w;
          const sy0 = bamTatDinh(seedBase * 23 + i * 41) * h;
          const speed = 1.4 + (i % 4) * 0.55;
          const y = y0 + ((sy0 + frame * speed) % (h + 20)) - 10;
          const x = sx + Math.sin(frame * 0.06 + i * 1.3) * 14;
          const r = 2.6 + (i % 3) * 1.3;
          return <circle key={`tcs-${i}`} cx={x.toFixed(1)} cy={y.toFixed(1)} r={r} fill={mau} fillOpacity={0.86} />;
        })}
      </g>
    </g>
  );
};

/** 9. Chiec xe taxi co chau Au/Anh di qua pho (KHONG hardcode bien so 1729: chi hien bien so neu JSON truyen ro) */
const XeTaxiCo: React.FC<{
  item: VatTheXungQuanh;
  frame: number;
}> = ({ item, frame }) => {
  const tiLe = item.tiLe ?? 1;
  const y = item.y ?? 745;
  const tocDo = item.tocDo ?? 3.1;
  const { x, gocBanhXe, nhunXeY } = tinhViTriTaxiCo(frame, item.x ?? 340, tocDo);
  const bienSo = (item.bienSoXe || '').trim();
  const mauXe = item.mau ?? '#1E293B';

  return (
    <g
      transform={`translate(${x.toFixed(1)}, ${(y + nhunXeY).toFixed(1)}) scale(${tiLe})`}
      pointerEvents="none"
    >
      {/* Bong xe phang duoi banh */}
      <ellipse cx={0} cy={32} rx={138} ry={13} fill="#0F172A" fillOpacity={0.34} />
      {/* Luong den pha phang (khong blur) */}
      <polygon points="124,-10 245,-32 245,22 124,6" fill="#FEF08A" fillOpacity={0.18} />
      {/* Than xe taxi co dien */}
      <path
        d="M -126 16 L -126 -24 Q -120 -34 -96 -36 L -74 -84 Q -68 -96 -46 -96 L 34 -96 Q 54 -96 64 -80 L 82 -38 L 116 -32 Q 130 -28 130 -12 L 130 16 Z"
        fill={mauXe}
        stroke="#0F172A"
        strokeWidth={4}
        strokeLinejoin="round"
      />
      {/* Cua kinh khoang hanh khach */}
      <path d="M -64 -42 L -48 -84 L -6 -84 L -6 -42 Z" fill="#BAE6FD" stroke="#334155" strokeWidth={3} />
      <path d="M 4 -42 L 4 -84 L 44 -84 L 62 -42 Z" fill="#E0F2FE" stroke="#334155" strokeWidth={3} />
      {/* Den hieu TAXI tren noc xe */}
      <rect x={-20} y={-114} width={44} height={18} rx={5} fill="#FACC15" stroke="#0F172A" strokeWidth={2.5} />
      <text x={2} y={-101} textAnchor="middle" fill="#0F172A" fontSize={11} fontWeight={900} fontFamily="Segoe UI, Arial, sans-serif">
        TAXI
      </text>
      {/* Dai trang tri & bien so xe (chi hien so tuy chinh neu JSON truyen, nguoc lai de bien so tron trung tinh) */}
      <rect x={-118} y={-20} width={236} height={8} rx={3} fill="#F59E0B" />
      <g transform="translate(-4, -2)">
        <rect x={-46} y={-16} width={92} height={28} rx={5} fill="#FFFDF7" stroke="#0F172A" strokeWidth={3} />
        <rect x={-42} y={-12} width={84} height={20} rx={3} fill="#FEF08A" />
        {bienSo ? (
          <text
            x={0}
            y={4}
            textAnchor="middle"
            fill="#0F172A"
            fontSize={bienSo.length > 6 ? 13 : 16}
            fontWeight={900}
            fontFamily="Consolas, Segoe UI, monospace"
          >
            {bienSo}
          </text>
        ) : (
          <g>
            <rect x={-26} y={-4} width={52} height={4} rx={2} fill="#94A3B8" />
            <rect x={-18} y={3} width={36} height={3} rx={1.5} fill="#CBD5E1" />
          </g>
        )}
      </g>
      {/* Den pha & den hau */}
      <circle cx={126} cy={-8} r={8} fill="#FEF08A" stroke="#78350F" strokeWidth={2.2} />
      <rect x={-130} y={-16} width={8} height={14} rx={2} fill="#EF4444" />
      {/* 2 banh xe quay tat dinh theo toc do */}
      {[-74, 74].map((wx, wi) => (
        <g key={`bx-${wi}`} transform={`translate(${wx}, 18) rotate(${gocBanhXe.toFixed(1)})`}>
          <circle cx={0} cy={0} r={24} fill="#0F172A" stroke="#475569" strokeWidth={3} />
          <circle cx={0} cy={0} r={12} fill="#E2E8F0" stroke="#64748B" strokeWidth={2} />
          <line x1={-10} y1={0} x2={10} y2={0} stroke="#334155" strokeWidth={2.4} />
          <line x1={0} y1={-10} x2={0} y2={10} stroke="#334155" strokeWidth={2.4} />
          <circle cx={0} cy={0} r={3.5} fill="#0F172A" />
        </g>
      ))}
    </g>
  );
};

/** 10. Dong ho qua lac co dien tich tac tat dinh */
const DongHoQuaLac: React.FC<{
  item: VatTheXungQuanh;
  frame: number;
}> = ({ item, frame }) => {
  const x0 = item.x ?? 1625;
  const y0 = item.y ?? 255;
  const tiLe = item.tiLe ?? 1;
  const gocLac = tinhGocQuaLac(frame, 16);
  const gocPhut = (frame * 0.4) % 360;
  const gocGio = (35 + frame * 0.03) % 360;

  return (
    <g transform={`translate(${x0}, ${y0}) scale(${tiLe})`} pointerEvents="none">
      {/* Hop go dong ho qua lac */}
      <rect x={-44} y={-52} width={88} height={182} rx={14} fill="#78350F" stroke="#451A03" strokeWidth={5} />
      <rect x={-32} y={42} width={64} height={74} rx={6} fill="#291205" stroke="#B45309" strokeWidth={2.5} />
      {/* Con lac tich tac */}
      <g transform={`translate(0, 46) rotate(${gocLac.toFixed(2)})`}>
        <line x1={0} y1={0} x2={0} y2={52} stroke="#FDE68A" strokeWidth={3.5} />
        <circle cx={0} cy={56} r={12} fill="#FACC15" stroke="#92400E" strokeWidth={2.5} />
      </g>
      {/* Mat dong ho */}
      <circle cx={0} cy={-6} r={34} fill="#FFFBEB" stroke="#B45309" strokeWidth={5} />
      {[0, 3, 6, 9].map((h) => {
        const g = (h / 12) * Math.PI * 2 - Math.PI / 2;
        return <circle key={`dh-${h}`} cx={Math.cos(g) * 24} cy={-6 + Math.sin(g) * 24} r={2.4} fill="#1E293B" />;
      })}
      <line
        x1={0}
        y1={-6}
        x2={(Math.sin((gocGio * Math.PI) / 180) * 14).toFixed(1)}
        y2={(-6 - Math.cos((gocGio * Math.PI) / 180) * 14).toFixed(1)}
        stroke="#0F172A"
        strokeWidth={3.5}
        strokeLinecap="round"
      />
      <line
        x1={0}
        y1={-6}
        x2={(Math.sin((gocPhut * Math.PI) / 180) * 21).toFixed(1)}
        y2={(-6 - Math.cos((gocPhut * Math.PI) / 180) * 21).toFixed(1)}
        stroke="#DC2626"
        strokeWidth={2.4}
        strokeLinecap="round"
      />
      <circle cx={0} cy={-6} r={3.5} fill="#0F172A" />
    </g>
  );
};

/**
 * Lop the gioi song dong tat dinh (v2.0 Buoc 3):
 * Tu dong hien thi hoac nhan danh sach vatTheXungQuanh[] tu JSON,
 * giup moi boi canh co chieu sau va su song ma van 100% SVG phang, tat dinh theo frame.
 */
export const SinhVatVaMoiTruong: React.FC<SinhVatVaMoiTruongProps> = ({
  boiCanh,
  thoiTiet,
  vatTheXungQuanh,
  bienSoXe,
}) => {
  const frame = useCurrentFrame();
  const danhSach = giaiDanhSachVatTheXungQuanh(
    boiCanh,
    thoiTiet,
    vatTheXungQuanh,
    bienSoXe,
  );

  if (danhSach.length === 0) {
    return null;
  }

  return (
    <g pointerEvents="none">
      {danhSach.map((item, idx) => {
        const key = `svmt-${item.loai}-${idx}`;
        switch (item.loai) {
          case 'chim_hai_au':
            return <DanChimHaiAu key={key} item={item} frame={frame} seedBase={idx + 1} />;
          case 'chim_san_truong':
            return <DanChimSanTruong key={key} item={item} frame={frame} seedBase={idx + 7} />;
          case 'ca_gon_song':
            return <CaVaGonSong key={key} item={item} frame={frame} seedBase={idx + 13} />;
          case 'buom_vuon':
            return <DanBuomVuon key={key} item={item} frame={frame} seedBase={idx + 19} />;
          case 'hoi_khoi':
            return <HoiKhoiBocLen key={key} item={item} frame={frame} seedBase={idx + 23} />;
          case 'ngon_nen_den_dau':
            return <NgonNenDenDau key={key} item={item} frame={frame} seedBase={idx + 29} />;
          case 'la_vang_gio':
            return <LaVangTheoGio key={key} item={item} frame={frame} seedBase={idx + 31} />;
          case 'tuyet_cua_so':
            return <TuyetQuaCuaSo key={key} item={item} boiCanh={boiCanh} frame={frame} seedBase={idx + 37} />;
          case 'xe_taxi_co':
            return <XeTaxiCo key={key} item={item} frame={frame} />;
          case 'dong_ho_qua_lac':
            return <DongHoQuaLac key={key} item={item} frame={frame} />;
          default:
            return null;
        }
      })}
    </g>
  );
};
