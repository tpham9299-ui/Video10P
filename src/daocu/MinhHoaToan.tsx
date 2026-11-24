import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { MinhHoaToanData } from '../kieu_dai';

type MinhHoaToanProps = {
  data: MinhHoaToanData;
  mauNhanManh?: string;
};

function laySo(
  thamSo: Record<string, number | string | number[]> | undefined,
  khoa: string,
  macDinh: number,
): number {
  const val = thamSo?.[khoa];
  return typeof val === 'number' && Number.isFinite(val) ? val : macDinh;
}

function layChuoi(
  thamSo: Record<string, number | string | number[]> | undefined,
  khoa: string,
  macDinh: string,
): string {
  const val = thamSo?.[khoa];
  return typeof val === 'string' && val.length > 0 ? val : macDinh;
}

/**
 * 1. Tam giac vuong 1 - 1 - √2 kem 3 hinh vuong dung tren 3 canh (tong mau phan sang tren bang xanh).
 */
const TamGiacVuongSvg: React.FC<{
  frame: number;
  thamSo?: Record<string, number | string | number[]>;
}> = ({ frame, thamSo }) => {
  const canhA = laySo(thamSo, 'canhA', 1);
  const canhB = laySo(thamSo, 'canhB', 1);
  const nhanHuyen = layChuoi(thamSo, 'nhanCanhHuyen', '√2');
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

/** 2. Truc so vo ti: phong dai khe giua cac phan so huu ti quanh √2 */
const TrucSoVoTiSvg: React.FC<{
  frame: number;
  thamSo?: Record<string, number | string | number[]>;
}> = ({ frame, thamSo }) => {
  const giaTri = laySo(thamSo, 'giaTri', Math.SQRT2);
  const nhan = layChuoi(thamSo, 'nhan', '√2 ≈ 1.4142...');
  const tZoom = interpolate(frame, [10, 50], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const nhip = 0.78 + 0.22 * Math.sin(frame * 0.2);

  const mapX = (v: number) => 50 + (v / 2) * 400;
  const xMucTieu = mapX(giaTri);
  const mapZoomX = (v: number) => 60 + ((v - 1.35) / 0.15) * 380;
  const xZoomMucTieu = mapZoomX(giaTri);

  const cacPhanSo = [
    { val: 1.4, label: '7/5' },
    { val: 17 / 12, label: '17/12' },
    { val: 41 / 29, label: '41/29' },
    { val: 3 / 2, label: '3/2' },
  ];

  return (
    <svg width="100%" height="100%" viewBox="0 0 500 490">
      <line x1={38} y1={130} x2={462} y2={130} stroke="#FFFFFF" strokeWidth={4} strokeLinecap="round" />
      {[0, 0.5, 1, 1.5, 2].map((v) => {
        const px = mapX(v);
        return (
          <g key={`tick-${v}`}>
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
          PHÓNG ĐẠI KHE SỐ HỮU TỈ (1.35 → 1.50)
        </text>

        <line x1={60} y1={340} x2={440} y2={340} stroke="#FFFFFF" strokeWidth={4} strokeLinecap="round" />

        {cacPhanSo.map((ps) => {
          const px = mapZoomX(ps.val);
          return (
            <g key={ps.label}>
              <line x1={px} y1={326} x2={px} y2={354} stroke="#7DD3FC" strokeWidth={3} />
              <circle cx={px} cy={340} r={5} fill="#7DD3FC" />
              <text x={px} y={384} textAnchor="middle" fill="#E0F2FE" fontSize={17} fontWeight={700}>
                {ps.label}
              </text>
            </g>
          );
        })}

        <circle cx={xZoomMucTieu} cy={340} r={16 * nhip} fill="#FACC15" fillOpacity={0.28} />
        <circle cx={xZoomMucTieu} cy={340} r={8} fill="#FEF08A" stroke="#14532D" strokeWidth={2} />
        <text x={xZoomMucTieu} y={310} textAnchor="middle" fill="#FEF08A" fontSize={20} fontWeight={900}>
          ∉ ℚ
        </text>
      </g>
    </svg>
  );
};

/** 3. Do thi ham so: duong cong + dien tich tich phan + tiep tuyen chuyen dong */
const DoThiHamSoSvg: React.FC<{
  frame: number;
  thamSo?: Record<string, number | string | number[]>;
}> = ({ frame, thamSo }) => {
  const ham = layChuoi(thamSo, 'ham', 'parabol');
  const tVe = interpolate(frame, [0, 42], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const ox = 76;
  const oy = 385;
  const w = 370;
  const h = 290;

  const evalF = (u: number) =>
    ham === 'sin' ? 0.5 + 0.36 * Math.sin(u * Math.PI * 1.5) : 0.12 + 0.78 * u * u;
  const evalDf = (u: number) =>
    ham === 'sin' ? 0.36 * Math.PI * 1.5 * Math.cos(u * Math.PI * 1.5) : 1.56 * u;

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
      <text x={456} y={oy + 26} fill="#FEFCE8" fontSize={20} fontWeight={700}>x</text>
      <text x={ox - 24} y={76} fill="#FEFCE8" fontSize={20} fontWeight={700}>y</text>

      <polyline points={duongCong} fill="none" stroke="#7DD3FC" strokeWidth={4.5} strokeLinecap="round" />

      {tVe > 0.7 && (
        <g>
          <line
            x1={pTan.x - dxTan}
            y1={pTan.y - dyTan}
            x2={pTan.x + dxTan}
            y2={pTan.y + dyTan}
            stroke="#FEF08A"
            strokeWidth={3.4}
            strokeDasharray="8 5"
          />
          <circle cx={pTan.x} cy={pTan.y} r={11} fill="#FACC15" fillOpacity={0.32} />
          <circle cx={pTan.x} cy={pTan.y} r={5.5} fill="#FEF08A" />
        </g>
      )}

      <text x={250} y={456} textAnchor="middle" fill="#FEF9C3" fontSize={19} fontWeight={700}>
        {ham === 'sin' ? 'y = sin(x) • Tiếp tuyến & Tích phân' : 'y = f(x) • Đạo hàm & Diện tích ∫'}
      </text>
    </svg>
  );
};

/** 4. Hinh hoc chung minh: ghep hinh vuong (a+b)^2 */
const HinhHocChungMinhSvg: React.FC<{ frame: number }> = ({ frame }) => {
  const t = interpolate(frame, [0, 45], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const x0 = 95;
  const y0 = 75;
  const a = 110;
  const b = 200;
  const L = a + b;

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
        c²
      </text>

      <text x={x0 + a / 2} y={y0 - 12} textAnchor="middle" fill="#BAE6FD" fontSize={20} fontWeight={800}>a</text>
      <text x={x0 + a + b / 2} y={y0 - 12} textAnchor="middle" fill="#86EFAC" fontSize={20} fontWeight={800}>b</text>
      <text x={250} y={452} textAnchor="middle" fill="#FEFCE8" fontSize={20} fontWeight={700}>
        (a + b)² = 4·(½ab) + c² ⇒ a² + b² = c²
      </text>
    </svg>
  );
};

/** 5. Chuoi suy luan tung buoc */
const ChuoiSuyLuanSvg: React.FC<{
  frame: number;
  thamSo?: Record<string, number | string | number[]>;
}> = ({ frame, thamSo }) => {
  const cacBuoc = [
    layChuoi(thamSo, 'buoc1', '1. Giả sử √2 = p/q (tối giản)'),
    layChuoi(thamSo, 'buoc2', '2. Suy ra p² = 2q² ⇒ p chẵn'),
    layChuoi(thamSo, 'buoc3', '3. Thay p = 2k ⇒ q² = 2k² ⇒ q chẵn'),
    layChuoi(thamSo, 'buoc4', '4. Mâu thuẫn! ⇒ √2 vô tỉ'),
  ];

  return (
    <svg width="100%" height="100%" viewBox="0 0 500 490">
      {cacBuoc.map((text, idx) => {
        const startF = idx * 18;
        const op = interpolate(frame, [startF, startF + 12], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });
        const y = 34 + idx * 112;
        const laCuoi = idx === cacBuoc.length - 1;
        const dangActive = frame >= startF && (laCuoi || frame < (idx + 1) * 18);
        const mauVien = laCuoi ? '#FEF08A' : dangActive ? '#7DD3FC' : '#86EFAC';

        return (
          <g key={`sl-${idx}`} opacity={op}>
            <rect
              x={34}
              y={y}
              width={432}
              height={72}
              rx={14}
              fill={laCuoi ? '#713F12' : '#092B19'}
              stroke={mauVien}
              strokeWidth={dangActive ? 3.5 : 2.2}
            />
            <text
              x={250}
              y={y + 43}
              textAnchor="middle"
              fill={laCuoi ? '#FEF9C3' : '#FFFFFF'}
              fontSize={20}
              fontWeight={laCuoi ? 900 : 700}
              fontFamily="Segoe UI, Arial, sans-serif"
            >
              {text}
            </text>

            {!laCuoi && (
              <g>
                <line x1={250} y1={y + 72} x2={250} y2={y + 106} stroke="#FEF08A" strokeWidth={3.5} />
                <polygon points={`240,${y + 98} 260,${y + 98} 250,${y + 112}`} fill="#FEF08A" />
              </g>
            )}
          </g>
        );
      })}
    </svg>
  );
};

export const MinhHoaToan: React.FC<MinhHoaToanProps> = ({
  data,
  mauNhanManh = '#FDE047',
}) => {
  const frame = useCurrentFrame();

  const veHinh = () => {
    switch (data.loai) {
      case 'tam_giac_vuong':
        return <TamGiacVuongSvg frame={frame} thamSo={data.thamSo} />;
      case 'truc_so_vo_ti':
        return <TrucSoVoTiSvg frame={frame} thamSo={data.thamSo} />;
      case 'do_thi_ham_so':
        return <DoThiHamSoSvg frame={frame} thamSo={data.thamSo} />;
      case 'hinh_hoc_chung_minh':
        return <HinhHocChungMinhSvg frame={frame} />;
      case 'chuoi_suy_luan':
      default:
        return <ChuoiSuyLuanSvg frame={frame} thamSo={data.thamSo} />;
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
        border: `2.5px solid ${mauNhanManh}`,
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
