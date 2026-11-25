import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type {
  BuocVeToan,
  KhungToaDoToan,
  LoaiHamDoThi,
  MinhHoaToanData,
} from '../kieu_dai';
import {
  coDuLieuMinhHoaHopLe,
  layDanhSachBuocSuyLuan,
} from './minh_hoa_hop_le';

type MinhHoaToanProps = {
  data: MinhHoaToanData;
  mauNhanManh?: string;
};

function laySoTuyChon(
  thamSo: Record<string, number | string | number[] | string[]> | undefined,
  khoa: string,
): number | null {
  const val = thamSo?.[khoa];
  return typeof val === 'number' && Number.isFinite(val) ? val : null;
}

function layChuoiTuyChon(
  thamSo: Record<string, number | string | number[] | string[]> | undefined,
  khoa: string,
): string | null {
  const val = thamSo?.[khoa];
  return typeof val === 'string' && val.trim().length > 0 ? val.trim() : null;
}

function lamMuotTienDo(t: number): number {
  const c = Math.max(0, Math.min(1, t));
  return 1 - Math.pow(1 - c, 3);
}

const KhungTrongSachSvg: React.FC = () => (
  <svg width="100%" height="100%" viewBox="0 0 500 490" />
);

/**
 * 1. Tam giac vuong kem 3 hinh vuong dung tren 3 canh (du lieu lay 100% tu thamSo JSON).
 */
const TamGiacVuongSvg: React.FC<{
  frame: number;
  thamSo?: Record<string, number | string | number[] | string[]>;
}> = ({ frame, thamSo }) => {
  const canhA = laySoTuyChon(thamSo, 'canhA');
  const canhB = laySoTuyChon(thamSo, 'canhB');
  if (canhA === null || canhB === null || canhA <= 0 || canhB <= 0) {
    return <KhungTrongSachSvg />;
  }
  const nhanHuyen = layChuoiTuyChon(thamSo, 'nhanCanhHuyen') ?? 'c';
  const dienTichC = Math.round((canhA * canhA + canhB * canhB) * 100) / 100;

  const tTamGiac = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const tVuongCanh = interpolate(frame, [16, 42], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const tVuongHuyen = interpolate(frame, [38, 68], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const nhipHuyen = 0.8 + 0.2 * Math.sin(frame * 0.16);

  const s = 142;
  const bx = 186;
  const by = 332;
  const ax = bx;
  const ay = by - s;
  const cx = bx + s;
  const cy = by;

  const d1x = ax + s;
  const d1y = ay - s;
  const d2x = cx + s;
  const d2y = cy - s;

  return (
    <svg width="100%" height="100%" viewBox="0 28 500 492">
      {/* Hinh vuong tren canh AB */}
      <g opacity={tVuongCanh}>
        <rect
          x={bx - s * tVuongCanh}
          y={ay}
          width={s * tVuongCanh}
          height={s}
          fill="#38BDF8"
          fillOpacity={0.22}
          stroke="#7DD3FC"
          strokeWidth={3}
        />
        <text
          x={bx - s * 0.5}
          y={ay + s * 0.5 + 8}
          textAnchor="middle"
          fill="#E0F2FE"
          fontSize={23}
          fontWeight={800}
          fontFamily="Georgia, Cambria, serif"
        >
          {canhA}² = {canhA * canhA}
        </text>
      </g>

      {/* Hinh vuong tren canh BC */}
      <g opacity={tVuongCanh}>
        <rect
          x={bx}
          y={by}
          width={s}
          height={s * tVuongCanh}
          fill="#4ADE80"
          fillOpacity={0.22}
          stroke="#86EFAC"
          strokeWidth={3}
        />
        <text
          x={bx + s * 0.5}
          y={by + s * 0.5 + 8}
          textAnchor="middle"
          fill="#DCFCE7"
          fontSize={23}
          fontWeight={800}
          fontFamily="Georgia, Cambria, serif"
        >
          {canhB}² = {canhB * canhB}
        </text>
      </g>

      {/* Hinh vuong tren canh huyen AC */}
      <g opacity={tVuongHuyen}>
        <polygon
          points={`${ax},${ay} ${cx},${cy} ${cx + (d2x - cx) * tVuongHuyen},${cy + (d2y - cy) * tVuongHuyen} ${ax + (d1x - ax) * tVuongHuyen},${ay + (d1y - ay) * tVuongHuyen}`}
          fill="#FACC15"
          fillOpacity={0.24 * nhipHuyen}
          stroke="#FEF08A"
          strokeWidth={3.2}
        />
        <line
          x1={(ax + d2x) / 2}
          y1={(ay + d2y) / 2}
          x2={cx}
          y2={cy}
          stroke="#FEF08A"
          strokeOpacity={0.35}
          strokeDasharray="6 6"
          strokeWidth={2}
        />
        <text
          x={(ax + cx + d1x + d2x) / 4}
          y={(ay + cy + d1y + d2y) / 4 + 4}
          textAnchor="middle"
          fill="#FEF9C3"
          fontSize={26}
          fontWeight={900}
          fontFamily="Georgia, Cambria, serif"
        >
          S = {dienTichC}
        </text>
      </g>

      {/* Tam giac vuong trung tam */}
      <g opacity={tTamGiac}>
        <polygon
          points={`${ax},${ay} ${bx},${by} ${cx},${cy}`}
          fill="#0B2E1B"
          fillOpacity={0.85}
          stroke="#FFFFFF"
          strokeWidth={3.8}
          strokeLinejoin="round"
        />
        <polyline
          points={`${bx},${by - 20} ${bx + 20},${by - 20} ${bx + 20},${by}`}
          fill="none"
          stroke="#7DD3FC"
          strokeWidth={2.8}
        />
        <line
          x1={ax}
          y1={ay}
          x2={cx}
          y2={cy}
          stroke="#FACC15"
          strokeWidth={11}
          strokeOpacity={0.28 * nhipHuyen}
          strokeLinecap="round"
        />
        <line
          x1={ax}
          y1={ay}
          x2={cx}
          y2={cy}
          stroke="#FEF08A"
          strokeWidth={4.8}
          strokeLinecap="round"
        />

        <text x={bx + 16} y={(ay + by) / 2 + 8} textAnchor="start" fill="#BAE6FD" fontSize={24} fontWeight={800}>
          {canhA}
        </text>
        <text x={(bx + cx) / 2} y={by - 10} textAnchor="middle" fill="#BBF7D0" fontSize={24} fontWeight={800}>
          {canhB}
        </text>
        <g transform={`translate(${(ax + cx) / 2 + 30}, ${(ay + cy) / 2 - 22})`}>
          <rect x={-32} y={-23} width={64} height={34} rx={9} fill="#14532D" stroke="#FEF08A" strokeWidth={2.6} />
          <text x={0} y={2} textAnchor="middle" fill="#FEF9C3" fontSize={23} fontWeight={900} fontFamily="Georgia, Cambria, serif">
            {nhanHuyen}
          </text>
        </g>
      </g>

      <text
        x={250}
        y={506}
        textAnchor="middle"
        fill="#FEFCE8"
        fontSize={21}
        fontWeight={800}
        fontFamily="Segoe UI, Arial, sans-serif"
      >
        {canhA}² + {canhB}² = ({nhanHuyen})² = {dienTichC}
      </text>
    </svg>
  );
};

/** 2. Truc so thuc / vo ti: phong dai quanh giaTri duoc cung cap trong thamSo JSON */
const TrucSoVoTiSvg: React.FC<{
  frame: number;
  thamSo?: Record<string, number | string | number[] | string[]>;
}> = ({ frame, thamSo }) => {
  const giaTri = laySoTuyChon(thamSo, 'giaTri');
  const nhan = layChuoiTuyChon(thamSo, 'nhan');
  if (giaTri === null || nhan === null) {
    return <KhungTrongSachSvg />;
  }

  const tZoom = interpolate(frame, [10, 50], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const nhip = 0.78 + 0.22 * Math.sin(frame * 0.2);

  const minTruc = laySoTuyChon(thamSo, 'min') ?? Math.floor(giaTri) - 1;
  const maxTruc = laySoTuyChon(thamSo, 'max') ?? Math.ceil(giaTri) + 1;
  const spanTruc = Math.max(0.5, maxTruc - minTruc);
  const mapX = (v: number) => 50 + ((v - minTruc) / spanTruc) * 400;
  const xMucTieu = mapX(giaTri);

  const banKinhZoom = Math.max(0.02, laySoTuyChon(thamSo, 'banKinhZoom') ?? 0.08);
  const zoomMin = giaTri - banKinhZoom;
  const zoomMax = giaTri + banKinhZoom;
  const mapZoomX = (v: number) =>
    60 + ((v - zoomMin) / Math.max(0.001, zoomMax - zoomMin)) * 380;
  const xZoomMucTieu = mapZoomX(giaTri);

  const mocChinh = Array.from({ length: 5 }).map(
    (_, i) => Math.round((minTruc + (i / 4) * spanTruc) * 100) / 100,
  );
  const mocZoom = Array.from({ length: 5 }).map((_, i) => {
    const val = zoomMin + (i / 4) * (zoomMax - zoomMin);
    return { val, label: val.toFixed(2) };
  });
  const tieuDeZoom =
    layChuoiTuyChon(thamSo, 'tieuDeZoom') ??
    `PHÓNG ĐẠI LÂN CẬN (${zoomMin.toFixed(2)} → ${zoomMax.toFixed(2)})`;
  const nhanZoom = layChuoiTuyChon(thamSo, 'nhanZoom') ?? nhan;

  return (
    <svg width="100%" height="100%" viewBox="0 0 500 490">
      <line x1={38} y1={130} x2={462} y2={130} stroke="#FFFFFF" strokeWidth={4} strokeLinecap="round" />
      {mocChinh.map((v, idx) => {
        const px = mapX(v);
        return (
          <g key={`tick-${idx}`}>
            <line x1={px} y1={118} x2={px} y2={142} stroke="#BBF7D0" strokeWidth={3} />
            <text x={px} y={168} textAnchor="middle" fill="#FEFCE8" fontSize={19} fontWeight={700}>
              {v}
            </text>
          </g>
        );
      })}

      <circle cx={xMucTieu} cy={130} r={22} fill="#FACC15" fillOpacity={0.2} stroke="#FEF08A" strokeWidth={2.8} strokeDasharray="5 4" />
      <circle cx={xMucTieu} cy={130} r={7.5} fill="#FEF08A" />
      <text x={xMucTieu} y={95} textAnchor="middle" fill="#FEF08A" fontSize={22} fontWeight={900}>
        {nhan}
      </text>

      <g opacity={tZoom}>
        <line x1={xMucTieu - 18} y1={148} x2={52} y2={240} stroke="#7DD3FC" strokeOpacity={0.65} strokeWidth={2.2} strokeDasharray="6 6" />
        <line x1={xMucTieu + 18} y1={148} x2={448} y2={240} stroke="#7DD3FC" strokeOpacity={0.65} strokeWidth={2.2} strokeDasharray="6 6" />

        <rect x={36} y={240} width={428} height={190} rx={16} fill="#092B19" stroke="#7DD3FC" strokeWidth={3} />
        <text x={250} y={272} textAnchor="middle" fill="#BAE6FD" fontSize={18} fontWeight={800}>
          {tieuDeZoom}
        </text>

        <line x1={60} y1={340} x2={440} y2={340} stroke="#FFFFFF" strokeWidth={4} strokeLinecap="round" />

        {mocZoom.map((mz, idx) => {
          const px = mapZoomX(mz.val);
          return (
            <g key={`mz-${idx}`}>
              <line x1={px} y1={326} x2={px} y2={354} stroke="#7DD3FC" strokeWidth={3} />
              <circle cx={px} cy={340} r={5} fill="#7DD3FC" />
              <text x={px} y={384} textAnchor="middle" fill="#E0F2FE" fontSize={16} fontWeight={700}>
                {mz.label}
              </text>
            </g>
          );
        })}

        <circle cx={xZoomMucTieu} cy={340} r={16 * nhip} fill="#FACC15" fillOpacity={0.28} />
        <circle cx={xZoomMucTieu} cy={340} r={8} fill="#FEF08A" stroke="#14532D" strokeWidth={2} />
        <text x={xZoomMucTieu} y={310} textAnchor="middle" fill="#FEF08A" fontSize={20} fontWeight={900}>
          {nhanZoom}
        </text>
      </g>
    </svg>
  );
};

/** 3. Do thi ham so: chi render khi JSON khai bao ro thamSo.ham, khong hardcode tieu de mac dinh */
const DoThiHamSoSvg: React.FC<{
  frame: number;
  thamSo?: Record<string, number | string | number[] | string[]>;
  mauNhanManh?: string;
}> = ({ frame, thamSo, mauNhanManh = '#FEF08A' }) => {
  const ham = layChuoiTuyChon(thamSo, 'ham');
  if (!ham) {
    return <KhungTrongSachSvg />;
  }

  const chuThich =
    layChuoiTuyChon(thamSo, 'chuThich') ?? layChuoiTuyChon(thamSo, 'nhan');
  const nhanX = layChuoiTuyChon(thamSo, 'nhanX') ?? 'x';
  const nhanY = layChuoiTuyChon(thamSo, 'nhanY') ?? 'y';
  const mauDuong = layChuoiTuyChon(thamSo, 'mauDuong') ?? '#7DD3FC';
  const mauDiemNhan = layChuoiTuyChon(thamSo, 'mauNhanManh') ?? mauNhanManh;
  const tVe = lamMuotTienDo(
    interpolate(frame, [0, 42], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }),
  );

  const ox = 76;
  const oy = 385;
  const w = 370;
  const h = 290;

  const evalF = (u: number): number => {
    switch (ham) {
      case 'sin':
        return 0.5 + 0.36 * Math.sin(u * Math.PI * 1.5);
      case 'cos':
        return 0.5 + 0.36 * Math.cos(u * Math.PI * 1.5);
      case 'bac_ba':
        return 0.5 + 0.42 * Math.pow(u * 2 - 1, 3);
      case 'mu':
        return 0.08 + 0.8 * ((Math.exp(2.2 * u) - 1) / (Math.exp(2.2) - 1));
      case 'tuyen_tinh':
        return 0.15 + 0.7 * u;
      case 'parabol':
        return 0.12 + 0.78 * u * u;
      default:
        return 0.5;
    }
  };
  const evalDf = (u: number): number => {
    const eps = 0.005;
    return (evalF(Math.min(1, u + eps)) - evalF(Math.max(0, u - eps))) / (2 * eps);
  };

  const toPt = (u: number) => ({ x: ox + u * w, y: oy - evalF(u) * h });

  const soDiem = 36;
  const maxIdx = Math.max(2, Math.floor(soDiem * tVe));
  const duongCong = Array.from({ length: maxIdx + 1 })
    .map((_, i) => {
      const p = toPt(i / soDiem);
      return `${p.x.toFixed(1)},${p.y.toFixed(1)}`;
    })
    .join(' ');

  const soCot = 8;
  const uStart = 0.15;
  const du = 0.7 / soCot;

  const uTan = 0.3 + 0.45 * (0.5 + 0.5 * Math.sin(frame * 0.045));
  const pTan = toPt(uTan);
  const slope = evalDf(uTan);
  const dxTan = 92;
  const dyTan = -(slope * (h / w)) * dxTan;

  return (
    <svg width="100%" height="100%" viewBox="0 0 500 490">
      {[1, 2, 3, 4].map((i) => (
        <g key={`grid-${i}`}>
          <line x1={ox + i * 85} y1={75} x2={ox + i * 85} y2={oy} stroke="#FFFFFF" strokeOpacity={0.18} strokeWidth={1.5} />
          <line x1={ox} y1={oy - i * 68} x2={ox + w} y2={oy - i * 68} stroke="#FFFFFF" strokeOpacity={0.18} strokeWidth={1.5} />
        </g>
      ))}

      {Array.from({ length: soCot }).map((_, i) => {
        const u0 = uStart + i * du;
        if (u0 > tVe) return null;
        const p = toPt(u0 + du * 0.5);
        return (
          <rect
            key={`cot-${i}`}
            x={ox + u0 * w}
            y={p.y}
            width={du * w - 3}
            height={oy - p.y}
            fill="#38BDF8"
            fillOpacity={0.28}
            stroke="#7DD3FC"
            strokeWidth={1.6}
          />
        );
      })}

      <line x1={54} y1={oy} x2={462} y2={oy} stroke="#FFFFFF" strokeWidth={3.5} />
      <line x1={ox} y1={410} x2={ox} y2={62} stroke="#FFFFFF" strokeWidth={3.5} />
      <text x={456} y={oy + 26} textAnchor="end" fill="#FEFCE8" fontSize={20} fontWeight={700}>{nhanX}</text>
      <text x={ox - 24} y={76} textAnchor="end" fill="#FEFCE8" fontSize={20} fontWeight={700}>{nhanY}</text>

      <polyline points={duongCong} fill="none" stroke={mauDuong} strokeWidth={4.5} strokeLinecap="round" />

      {tVe > 0.7 && (
        <g>
          <line
            x1={pTan.x - dxTan}
            y1={pTan.y - dyTan}
            x2={pTan.x + dxTan}
            y2={pTan.y + dyTan}
            stroke={mauDiemNhan}
            strokeWidth={3.4}
            strokeDasharray="8 5"
          />
          <circle cx={pTan.x} cy={pTan.y} r={11} fill={mauDiemNhan} fillOpacity={0.32} />
          <circle cx={pTan.x} cy={pTan.y} r={5.5} fill={mauDiemNhan} />
        </g>
      )}

      {chuThich && (
        <text x={250} y={456} textAnchor="middle" fill="#FEF9C3" fontSize={19} fontWeight={700}>
          {chuThich}
        </text>
      )}
    </svg>
  );
};

/** 4. Hinh hoc chung minh: chi render khi JSON cung cap thamSo.canhA va thamSo.canhB hop le */
const HinhHocChungMinhSvg: React.FC<{
  frame: number;
  thamSo?: Record<string, number | string | number[] | string[]>;
}> = ({ frame, thamSo }) => {
  const canhA = laySoTuyChon(thamSo, 'canhA');
  const canhB = laySoTuyChon(thamSo, 'canhB');
  if (canhA === null || canhB === null || canhA <= 0 || canhB <= 0) {
    return <KhungTrongSachSvg />;
  }

  const t = interpolate(frame, [0, 45], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const L = 310;
  const tiLeA = Math.max(0.2, Math.min(0.8, canhA / (canhA + canhB)));
  const x0 = 95;
  const y0 = 75;
  const a = Math.round(L * tiLeA);
  const b = L - a;
  const nhanA = layChuoiTuyChon(thamSo, 'nhanA') ?? String(canhA);
  const nhanB = layChuoiTuyChon(thamSo, 'nhanB') ?? String(canhB);
  const nhanTam = layChuoiTuyChon(thamSo, 'nhanTam') ?? 'S';
  const chuThich = layChuoiTuyChon(thamSo, 'chuThich');

  const tamGiacs = [
    `${x0},${y0} ${x0 + a},${y0} ${x0},${y0 + b}`,
    `${x0 + a},${y0} ${x0 + L},${y0} ${x0 + L},${y0 + a}`,
    `${x0 + L},${y0 + a} ${x0 + L},${y0 + L} ${x0 + b},${y0 + L}`,
    `${x0 + b},${y0 + L} ${x0},${y0 + L} ${x0},${y0 + b}`,
  ];

  return (
    <svg width="100%" height="100%" viewBox="0 0 500 490">
      <rect x={x0} y={y0} width={L} height={L} fill="#092B19" stroke="#FFFFFF" strokeWidth={3.5} />

      {tamGiacs.map((pts, idx) => {
        const op = interpolate(t, [idx * 0.16, idx * 0.16 + 0.35], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        return (
          <polygon
            key={`tg-${idx}`}
            points={pts}
            fill="#38BDF8"
            fillOpacity={0.3 * op}
            stroke="#7DD3FC"
            strokeWidth={2.6}
            opacity={op}
          />
        );
      })}

      <polygon
        points={`${x0 + a},${y0} ${x0 + L},${y0 + a} ${x0 + b},${y0 + L} ${x0},${y0 + b}`}
        fill="#FACC15"
        fillOpacity={0.28 * t}
        stroke="#FEF08A"
        strokeWidth={3.5}
        opacity={t}
      />
      <text
        x={x0 + L / 2}
        y={y0 + L / 2 + 12}
        textAnchor="middle"
        fill="#FEF9C3"
        fontSize={38}
        fontWeight={900}
        fontFamily="Georgia, Cambria, serif"
        opacity={t}
      >
        {nhanTam}
      </text>

      <text x={x0 + a / 2} y={y0 - 12} textAnchor="middle" fill="#BAE6FD" fontSize={20} fontWeight={800}>
        {nhanA}
      </text>
      <text x={x0 + a + b / 2} y={y0 - 12} textAnchor="middle" fill="#86EFAC" fontSize={20} fontWeight={800}>
        {nhanB}
      </text>
      {chuThich && (
        <text x={250} y={452} textAnchor="middle" fill="#FEFCE8" fontSize={20} fontWeight={700}>
          {chuThich}
        </text>
      )}
    </svg>
  );
};

/** 5. Chuoi suy luan tung buoc: chi render dung cac buoc tu thamSo JSON, khong fallback hardcode */
const ChuoiSuyLuanSvg: React.FC<{
  frame: number;
  thamSo?: Record<string, number | string | number[] | string[]>;
  mauNhanManh?: string;
}> = ({ frame, thamSo, mauNhanManh = '#FEF08A' }) => {
  const cacBuoc = layDanhSachBuocSuyLuan(thamSo);
  if (cacBuoc.length === 0) {
    return <KhungTrongSachSvg />;
  }
  const mauCuoi = layChuoiTuyChon(thamSo, 'mauNhanManh') ?? mauNhanManh;

  const soBuoc = cacBuoc.length;
  const chieuCaoO = soBuoc <= 4 ? 72 : Math.max(48, Math.floor(330 / soBuoc));
  const khoangCach = soBuoc <= 4 ? 40 : Math.max(20, Math.floor((430 - soBuoc * chieuCaoO) / Math.max(1, soBuoc - 1)));
  const buocY = chieuCaoO + khoangCach;
  const tongChieuCao = (soBuoc - 1) * buocY + chieuCaoO;
  const startY = Math.max(20, Math.round((490 - tongChieuCao) / 2));

  return (
    <svg width="100%" height="100%" viewBox="0 0 500 490">
      {cacBuoc.map((text, idx) => {
        const startF = idx * 18;
        const op = interpolate(frame, [startF, startF + 12], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        const y = startY + idx * buocY;
        const laCuoi = idx === soBuoc - 1;
        const dangActive = frame >= startF && (laCuoi || frame < (idx + 1) * 18);
        const mauVien = laCuoi ? mauCuoi : dangActive ? '#7DD3FC' : '#86EFAC';

        return (
          <g key={`sl-${idx}`} opacity={op}>
            <rect
              x={34}
              y={y}
              width={432}
              height={chieuCaoO}
              rx={14}
              fill={laCuoi ? '#713F12' : '#092B19'}
              stroke={mauVien}
              strokeWidth={dangActive ? 3.5 : 2.2}
            />
            <text
              x={250}
              y={y + chieuCaoO / 2 + 7}
              textAnchor="middle"
              fill={laCuoi ? '#FEF9C3' : '#FFFFFF'}
              fontSize={text.length > 36 ? 17 : 20}
              fontWeight={laCuoi ? 900 : 700}
              fontFamily="Segoe UI, Arial, sans-serif"
            >
              {text}
            </text>

            {!laCuoi && (
              <g>
                <line x1={250} y1={y + chieuCaoO} x2={250} y2={y + buocY - 6} stroke="#FEF08A" strokeWidth={3.5} />
                <polygon
                  points={`240,${y + buocY - 14} 260,${y + buocY - 14} 250,${y + buocY}`}
                  fill="#FEF08A"
                />
              </g>
            )}
          </g>
        );
      })}
    </svg>
  );
};

/** Ham danh gia gia tri do thi tat dinh cho mini-DSL "tung_buoc" */
function tinhGiaTriHam(
  ham: LoaiHamDoThi,
  x: number,
  a: number,
  b: number,
  c: number,
): number {
  switch (ham) {
    case 'sin':
      return a * Math.sin(b * x + c);
    case 'cos':
      return a * Math.cos(b * x + c);
    case 'bac_ba':
      return a * x * x * x + b * x + c;
    case 'mu':
      return a * Math.exp(Math.max(-4, Math.min(4, b * x))) + c;
    case 'tuyen_tinh':
      return a * x + b;
    case 'parabol':
    default:
      return a * x * x + b * x + c;
  }
}

/** 6. Minh hoa tham so hoa tung buoc (mini-DSL JSON): chi render khi buocVe co du lieu hop le */
const MinhHoaTungBuocSvg: React.FC<{
  frame: number;
  buocVe?: BuocVeToan[];
  khungToaDo?: KhungToaDoToan;
  chuThichCuoi?: string;
}> = ({ frame, buocVe, khungToaDo, chuThichCuoi }) => {
  if (!Array.isArray(buocVe) || buocVe.length === 0) {
    return <KhungTrongSachSvg />;
  }
  const danhSachBuoc = buocVe;

  // Tim cau hinh truc_toa_do neu co trong danh sach buoc
  const buocTruc = danhSachBuoc.find(
    (b): b is Extract<BuocVeToan, { loai: 'truc_toa_do' }> => b.loai === 'truc_toa_do',
  );

  // Tu dong nhan dien he toa do 'toan' (y huong len) hay 'svg' (0..500, 0..490)
  let dungToaDoToan = khungToaDo?.heToaDo === 'toan' || Boolean(khungToaDo) || Boolean(buocTruc);
  if (khungToaDo?.heToaDo === 'svg') {
    dungToaDoToan = false;
  } else if (!dungToaDoToan) {
    let maxAbs = 0;
    for (const b of danhSachBuoc) {
      if (b.loai === 'diem' || b.loai === 'nhan_chu') {
        maxAbs = Math.max(maxAbs, Math.abs(b.x), Math.abs(b.y));
      } else if (b.loai === 'doan_thang') {
        maxAbs = Math.max(maxAbs, Math.abs(b.x1), Math.abs(b.y1), Math.abs(b.x2), Math.abs(b.y2));
      } else if (b.loai === 'cung_tron') {
        maxAbs = Math.max(maxAbs, Math.abs(b.cx), Math.abs(b.cy), Math.abs(b.r));
      } else if (b.loai === 'da_giac') {
        for (const [px, py] of b.diem) {
          maxAbs = Math.max(maxAbs, Math.abs(px), Math.abs(py));
        }
      } else if (b.loai === 'duong_cong') {
        dungToaDoToan = true;
      }
    }
    if (!dungToaDoToan && maxAbs <= 20) {
      dungToaDoToan = true;
    }
  }

  const xMin = khungToaDo?.xMin ?? buocTruc?.xMin ?? -5;
  const xMax = khungToaDo?.xMax ?? buocTruc?.xMax ?? 5;
  const yMin = khungToaDo?.yMin ?? buocTruc?.yMin ?? -4;
  const yMax = khungToaDo?.yMax ?? buocTruc?.yMax ?? 4;
  const spanX = Math.max(0.001, xMax - xMin);
  const spanY = Math.max(0.001, yMax - yMin);

  // Vung ve an toan trong viewBox 500x490 (chua cho chu thich cuoi o y=462)
  const padL = 52;
  const padR = 456;
  const padT = 48;
  const padB = 420;
  const plotW = padR - padL;
  const plotH = padB - padT;

  const toSvg = (x: number, y: number): { x: number; y: number } => {
    if (!dungToaDoToan) {
      return { x, y };
    }
    return {
      x: padL + ((x - xMin) / spanX) * plotW,
      y: padB - ((y - yMin) / spanY) * plotH,
    };
  };

  const toRadiusSvg = (r: number): { rx: number; ry: number } => {
    if (!dungToaDoToan) {
      return { rx: Math.abs(r), ry: Math.abs(r) };
    }
    return {
      rx: (Math.abs(r) / spanX) * plotW,
      ry: (Math.abs(r) / spanY) * plotH,
    };
  };

  const veTrucToaDo = (
    cfg: {
      xMin?: number;
      xMax?: number;
      yMin?: number;
      yMax?: number;
      hienLuoi?: boolean;
      nhanX?: string;
      nhanY?: string;
      mau?: string;
    },
    op: number,
    key: string,
  ) => {
    const mauTruc = cfg.mau ?? '#E2E8F0';
    const x0 = Math.max(padL, Math.min(padR, toSvg(0, 0).x));
    const y0 = Math.max(padT, Math.min(padB, toSvg(0, 0).y));
    const hienLuoi = cfg.hienLuoi !== false;
    const soDuong = 5;

    return (
      <g key={key} opacity={op}>
        {hienLuoi &&
          Array.from({ length: soDuong + 1 }).map((_, gi) => {
            const gx = padL + (gi / soDuong) * plotW;
            const gy = padT + (gi / soDuong) * plotH;
            return (
              <g key={`${key}-g-${gi}`}>
                <line x1={gx} y1={padT} x2={gx} y2={padB} stroke="#FFFFFF" strokeOpacity={0.14} strokeWidth={1.2} />
                <line x1={padL} y1={gy} x2={padR} y2={gy} stroke="#FFFFFF" strokeOpacity={0.14} strokeWidth={1.2} />
              </g>
            );
          })}
        <line x1={padL - 8} y1={y0} x2={padR + 14} y2={y0} stroke={mauTruc} strokeWidth={3} />
        <polygon points={`${padR + 18},${y0} ${padR + 6},${y0 - 6} ${padR + 6},${y0 + 6}`} fill={mauTruc} />
        <line x1={x0} y1={padB + 10} x2={x0} y2={padT - 14} stroke={mauTruc} strokeWidth={3} />
        <polygon points={`${x0},${padT - 18} ${x0 - 6},${padT - 6} ${x0 + 6},${padT - 6}`} fill={mauTruc} />
        <text x={padR + 14} y={y0 + 22} textAnchor="end" fill="#FEFCE8" fontSize={18} fontWeight={800}>
          {cfg.nhanX ?? 'x'}
        </text>
        <text x={x0 - 16} y={padT - 2} textAnchor="end" fill="#FEFCE8" fontSize={18} fontWeight={800}>
          {cfg.nhanY ?? 'y'}
        </text>
      </g>
    );
  };

  return (
    <svg width="100%" height="100%" viewBox="0 0 500 490">
      {/* Neu khai bao khungToaDo.hienTruc ma khong co buoc truc_toa_do rieng */}
      {dungToaDoToan &&
        !buocTruc &&
        khungToaDo?.hienTruc &&
        veTrucToaDo(
          { ...khungToaDo, mau: khungToaDo.mauTruc },
          lamMuotTienDo(
            interpolate(frame, [0, 14], [0, 1], {
              extrapolateLeft: 'clamp',
              extrapolateRight: 'clamp',
            }),
          ),
          'khung-truc-auto',
        )}

      {danhSachBuoc.map((buoc, idx) => {
        const tuF = buoc.tuFrame ?? idx * 16;
        const dur = Math.max(4, buoc.thoiLuong ?? 22);
        const t = lamMuotTienDo(
          interpolate(frame, [tuF, tuF + dur], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp',
          }),
        );
        if (t <= 0.001) return null;

        switch (buoc.loai) {
          case 'truc_toa_do':
            return veTrucToaDo(buoc, t, `tb-${idx}`);

          case 'da_giac': {
            if (!buoc.diem || buoc.diem.length < 3) return null;
            const coBienHinh =
              Array.isArray(buoc.diemDich) && buoc.diemDich.length === buoc.diem.length;
            const tMorph = coBienHinh
              ? interpolate(frame, [tuF + Math.round(dur * 0.45), tuF + dur + 18], [0, 1], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                })
              : 0;
            const cacDiemSvg = buoc.diem.map(([x, y], pi) => {
              const mx = coBienHinh ? x + (buoc.diemDich![pi][0] - x) * tMorph : x;
              const my = coBienHinh ? y + (buoc.diemDich![pi][1] - y) * tMorph : y;
              return toSvg(mx, my);
            });
            const ptsStr = cacDiemSvg.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');
            const cx = cacDiemSvg.reduce((s, p) => s + p.x, 0) / cacDiemSvg.length;
            const cy = cacDiemSvg.reduce((s, p) => s + p.y, 0) / cacDiemSvg.length;
            const mauVien = buoc.mau ?? '#7DD3FC';
            const mauTo = buoc.mauTo ?? mauVien;
            const doMoTo = buoc.doMoTo ?? 0.25;
            return (
              <g key={`tb-${idx}`} opacity={t}>
                <polygon
                  points={ptsStr}
                  fill={mauTo}
                  fillOpacity={doMoTo}
                  stroke={mauVien}
                  strokeWidth={3}
                  strokeLinejoin="round"
                />
                {buoc.nhan && (
                  <text
                    x={cx}
                    y={cy + 6}
                    textAnchor="middle"
                    fill="#FEF9C3"
                    fontSize={20}
                    fontWeight={800}
                    fontFamily="Georgia, Cambria, serif"
                  >
                    {buoc.nhan}
                  </text>
                )}
              </g>
            );
          }

          case 'duong_cong': {
            const mau = buoc.mau ?? '#7DD3FC';
            const doDay = buoc.doDay ?? 4;
            let dsDiemToan: [number, number][] = [];
            if (buoc.diem && buoc.diem.length >= 2) {
              dsDiemToan = buoc.diem;
            } else {
              const ham: LoaiHamDoThi = buoc.ham ?? 'parabol';
              const a = buoc.heSoA ?? (ham === 'parabol' ? 0.35 : 1);
              const b = buoc.heSoB ?? (ham === 'sin' || ham === 'cos' ? 1 : 0);
              const c = buoc.heSoC ?? 0;
              const x1 = buoc.xTu ?? xMin;
              const x2 = buoc.xDen ?? xMax;
              const soMau = 44;
              for (let k = 0; k <= soMau; k++) {
                const xv = x1 + (k / soMau) * (x2 - x1);
                const yv = tinhGiaTriHam(ham, xv, a, b, c);
                dsDiemToan.push([xv, yv]);
              }
            }
            const soDiemVe = Math.max(2, Math.floor(dsDiemToan.length * t));
            const diemSvg = dsDiemToan.slice(0, soDiemVe).map(([px, py]) => toSvg(px, py));
            const ptsStr = diemSvg.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');
            const diemCuoi = diemSvg[diemSvg.length - 1];
            return (
              <g key={`tb-${idx}`}>
                <polyline
                  points={ptsStr}
                  fill="none"
                  stroke={mau}
                  strokeWidth={doDay}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                {diemCuoi && <circle cx={diemCuoi.x} cy={diemCuoi.y} r={5.5} fill="#FEF08A" />}
                {buoc.nhan && diemCuoi && t > 0.6 && (
                  <text
                    x={Math.min(440, Math.max(60, diemCuoi.x - 10))}
                    y={Math.max(36, diemCuoi.y - 14)}
                    textAnchor="middle"
                    fill="#FEF08A"
                    fontSize={18}
                    fontWeight={800}
                  >
                    {buoc.nhan}
                  </text>
                )}
              </g>
            );
          }

          case 'cung_tron': {
            const tam = toSvg(buoc.cx, buoc.cy);
            const { rx, ry } = toRadiusSvg(buoc.r);
            const mau = buoc.mau ?? '#FACC15';
            const g1 = buoc.gocBatDau ?? 0;
            const g2 = buoc.gocKetThuc ?? 360;
            const gocHienTai = g1 + (g2 - g1) * t;
            const lechGoc = Math.abs(gocHienTai - g1);
            if (lechGoc < 0.5) return null;

            if (lechGoc >= 359.5) {
              return (
                <g key={`tb-${idx}`}>
                  <ellipse
                    cx={tam.x}
                    cy={tam.y}
                    rx={rx}
                    ry={ry}
                    fill={buoc.mauTo ?? 'none'}
                    fillOpacity={buoc.mauTo ? 0.2 : 0}
                    stroke={mau}
                    strokeWidth={buoc.doDay ?? 3.2}
                  />
                  {buoc.nhan && (
                    <text x={tam.x + rx * 0.55} y={tam.y - ry * 0.55} fill="#FEF9C3" fontSize={18} fontWeight={800}>
                      {buoc.nhan}
                    </text>
                  )}
                </g>
              );
            }

            const rad1 = (g1 * Math.PI) / 180;
            const rad2 = (gocHienTai * Math.PI) / 180;
            // Trong he toa do toan hoc y huong len -> dung -sin
            const dauY = dungToaDoToan ? -1 : 1;
            const sx = tam.x + Math.cos(rad1) * rx;
            const sy = tam.y + dauY * Math.sin(rad1) * ry;
            const ex = tam.x + Math.cos(rad2) * rx;
            const ey = tam.y + dauY * Math.sin(rad2) * ry;
            const largeArc = lechGoc > 180 ? 1 : 0;
            const sweep = dungToaDoToan ? (g2 >= g1 ? 0 : 1) : g2 >= g1 ? 1 : 0;
            const dCung = `M ${sx.toFixed(1)} ${sy.toFixed(1)} A ${rx.toFixed(1)} ${ry.toFixed(1)} 0 ${largeArc} ${sweep} ${ex.toFixed(1)} ${ey.toFixed(1)}`;
            const radMid = ((g1 + gocHienTai) / 2) * (Math.PI / 180);
            const lx = tam.x + Math.cos(radMid) * (rx + 18);
            const ly = tam.y + dauY * Math.sin(radMid) * (ry + 18);

            return (
              <g key={`tb-${idx}`}>
                {buoc.mauTo && (
                  <path
                    d={`M ${tam.x.toFixed(1)} ${tam.y.toFixed(1)} L ${sx.toFixed(1)} ${sy.toFixed(1)} A ${rx.toFixed(1)} ${ry.toFixed(1)} 0 ${largeArc} ${sweep} ${ex.toFixed(1)} ${ey.toFixed(1)} Z`}
                    fill={buoc.mauTo}
                    fillOpacity={0.22}
                  />
                )}
                <path
                  d={dCung}
                  fill="none"
                  stroke={mau}
                  strokeWidth={buoc.doDay ?? 3.4}
                  strokeLinecap="round"
                />
                {buoc.nhan && t > 0.5 && (
                  <text x={lx} y={ly + 5} textAnchor="middle" fill="#FEF9C3" fontSize={18} fontWeight={800}>
                    {buoc.nhan}
                  </text>
                )}
              </g>
            );
          }

          case 'doan_thang': {
            const p1 = toSvg(buoc.x1, buoc.y1);
            const p2 = toSvg(buoc.x2, buoc.y2);
            const curX = p1.x + (p2.x - p1.x) * t;
            const curY = p1.y + (p2.y - p1.y) * t;
            const mau = buoc.mau ?? '#FFFFFF';
            const goc = Math.atan2(p2.y - p1.y, p2.x - p1.x);
            const midX = (p1.x + p2.x) / 2;
            const midY = (p1.y + p2.y) / 2;
            return (
              <g key={`tb-${idx}`}>
                <line
                  x1={p1.x}
                  y1={p1.y}
                  x2={curX}
                  y2={curY}
                  stroke={mau}
                  strokeWidth={buoc.doDay ?? 3.6}
                  strokeDasharray={buoc.netDut ? '8 6' : undefined}
                  strokeLinecap="round"
                />
                {buoc.muiTen && t > 0.35 && (
                  <polygon
                    points={`${curX.toFixed(1)},${curY.toFixed(1)} ${(curX - 13 * Math.cos(goc - 0.42)).toFixed(1)},${(curY - 13 * Math.sin(goc - 0.42)).toFixed(1)} ${(curX - 13 * Math.cos(goc + 0.42)).toFixed(1)},${(curY - 13 * Math.sin(goc + 0.42)).toFixed(1)}`}
                    fill={mau}
                  />
                )}
                {buoc.nhan && t > 0.55 && (
                  <text
                    x={midX - Math.sin(goc) * 18}
                    y={midY + Math.cos(goc) * 18 + 5}
                    textAnchor="middle"
                    fill="#FEF9C3"
                    fontSize={20}
                    fontWeight={800}
                  >
                    {buoc.nhan}
                  </text>
                )}
              </g>
            );
          }

          case 'diem': {
            const p = toSvg(buoc.x, buoc.y);
            const mau = buoc.mau ?? '#FEF08A';
            const r = (buoc.banKinh ?? 6.5) * (0.4 + 0.6 * t);
            return (
              <g key={`tb-${idx}`} opacity={t}>
                <circle cx={p.x} cy={p.y} r={r * 2.1} fill={mau} fillOpacity={0.22} />
                <circle cx={p.x} cy={p.y} r={r} fill={mau} stroke="#092B19" strokeWidth={2} />
                {buoc.nhan && (
                  <text
                    x={p.x + 12}
                    y={p.y - 10}
                    fill="#FFFFFF"
                    fontSize={19}
                    fontWeight={800}
                    fontFamily="Segoe UI, Arial, sans-serif"
                  >
                    {buoc.nhan}
                  </text>
                )}
              </g>
            );
          }

          case 'nhan_chu': {
            const p = toSvg(buoc.x, buoc.y);
            return (
              <text
                key={`tb-${idx}`}
                x={p.x}
                y={p.y}
                textAnchor="middle"
                fill={buoc.mau ?? '#FEF9C3'}
                fontSize={buoc.coChu ?? 20}
                fontWeight={800}
                opacity={t}
                fontFamily="Segoe UI, Arial, sans-serif"
              >
                {buoc.noiDung}
              </text>
            );
          }

          default:
            return null;
        }
      })}

      {chuThichCuoi && (
        <text
          x={250}
          y={466}
          textAnchor="middle"
          fill="#FEFCE8"
          fontSize={19}
          fontWeight={800}
          fontFamily="Segoe UI, Arial, sans-serif"
        >
          {chuThichCuoi}
        </text>
      )}
    </svg>
  );
};

export const MinhHoaToan: React.FC<MinhHoaToanProps> = ({
  data,
  mauNhanManh = '#FDE047',
}) => {
  const frame = useCurrentFrame();

  const mauHighlight = data.mauNhanManh || mauNhanManh;

  const veHinh = () => {
    if (!coDuLieuMinhHoaHopLe(data)) {
      return <KhungTrongSachSvg />;
    }
    switch (data.loai) {
      case 'tam_giac_vuong':
        return <TamGiacVuongSvg frame={frame} thamSo={data.thamSo} />;
      case 'truc_so_vo_ti':
        return <TrucSoVoTiSvg frame={frame} thamSo={data.thamSo} />;
      case 'do_thi_ham_so':
        return <DoThiHamSoSvg frame={frame} thamSo={data.thamSo} mauNhanManh={mauHighlight} />;
      case 'hinh_hoc_chung_minh':
        return <HinhHocChungMinhSvg frame={frame} thamSo={data.thamSo} />;
      case 'tung_buoc':
        return (
          <MinhHoaTungBuocSvg
            frame={frame}
            buocVe={data.buocVe}
            khungToaDo={data.khungToaDo}
            chuThichCuoi={data.chuThichCuoi}
          />
        );
      case 'chuoi_suy_luan':
        return <ChuoiSuyLuanSvg frame={frame} thamSo={data.thamSo} mauNhanManh={mauHighlight} />;
      default:
        return <KhungTrongSachSvg />;
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        borderRadius: 16,
        backgroundColor: 'rgba(9, 43, 25, 0.85)',
        border: `2.5px solid ${mauHighlight}`,
        padding: '12px 14px 8px',
        boxSizing: 'border-box',
      }}
    >
      {data.tieuDe && (
        <div
          style={{
            color: '#FEF08A',
            fontSize: 20,
            fontWeight: 800,
            textAlign: 'center',
            marginBottom: 4,
            letterSpacing: 0.3,
          }}
        >
          {data.tieuDe}
        </div>
      )}
      <div style={{ flex: 1, minHeight: 0 }}>{veHinh()}</div>
    </div>
  );
};
