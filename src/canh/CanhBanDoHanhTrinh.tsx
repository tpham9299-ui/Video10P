import React from 'react';
import { useCurrentFrame } from 'remotion';
import type { BangMau, Canh, PhuongTienHanhTrinh } from '../kieu_dai';
import {
  TOA_DO_BAN_DO_MAC_DINH,
  tinhTrangThaiHanhTrinh,
} from './ke_chuyen_v35_logic';

type Props = {
  canh: Canh;
  bangMau: BangMau;
};

const BieuTuongPhuongTien: React.FC<{ loai: PhuongTienHanhTrinh; frame: number }> = ({
  loai,
  frame,
}) => {
  const nhip = Math.sin(frame * 0.25) * 3.5;

  if (loai === 'thu_tay') {
    return (
      <g transform={`translate(0, ${nhip.toFixed(1)})`}>
        <rect
          x={-34}
          y={-22}
          width={68}
          height={44}
          rx={6}
          fill="#FFFBEB"
          stroke="#1A1A1A"
          strokeWidth={3.5}
        />
        <polyline
          points="-32,-20 0,6 32,-20"
          fill="none"
          stroke="#1A1A1A"
          strokeWidth={3}
          strokeLinejoin="round"
        />
        <circle cx={0} cy={4} r={8} fill="#DC2626" stroke="#1A1A1A" strokeWidth={2.2} />
      </g>
    );
  }

  if (loai === 'nguoi_di_bo') {
    const buoc = Math.sin(frame * 0.35) * 9;
    return (
      <g transform={`translate(0, ${(-Math.abs(nhip) * 0.7).toFixed(1)})`}>
        <circle cx={0} cy={-26} r={13} fill="#FEF3C7" stroke="#1A1A1A" strokeWidth={3.5} />
        <line x1={0} y1={-13} x2={0} y2={12} stroke="#1A1A1A" strokeWidth={4.5} strokeLinecap="round" />
        <line x1={0} y1={-4} x2={16} y2={4 + buoc * 0.4} stroke="#1A1A1A" strokeWidth={3.5} strokeLinecap="round" />
        <line x1={0} y1={-4} x2={-14} y2={6 - buoc * 0.4} stroke="#1A1A1A" strokeWidth={3.5} strokeLinecap="round" />
        <line x1={0} y1={12} x2={12 + buoc} y2={30} stroke="#1A1A1A" strokeWidth={4} strokeLinecap="round" />
        <line x1={0} y1={12} x2={-12 - buoc} y2={30} stroke="#1A1A1A" strokeWidth={4} strokeLinecap="round" />
        {/* Gay hanh trinh */}
        <line x1={18} y1={-16} x2={22} y2={30} stroke="#92400E" strokeWidth={3} strokeLinecap="round" />
      </g>
    );
  }

  if (loai === 'xe_ngua') {
    return (
      <g transform={`translate(0, ${(Math.sin(frame * 0.4) * 2).toFixed(1)})`}>
        <rect x={-34} y={-20} width={52} height={30} rx={8} fill="#B45309" stroke="#1A1A1A" strokeWidth={3.5} />
        <rect x={-22} y={-12} width={16} height={14} rx={3} fill="#FEF08A" stroke="#1A1A1A" strokeWidth={2} />
        <circle cx={-20} cy={14} r={11} fill="#78350F" stroke="#1A1A1A" strokeWidth={3} />
        <circle cx={6} cy={14} r={11} fill="#78350F" stroke="#1A1A1A" strokeWidth={3} />
        <path d="M 18 -4 L 38 -12 L 42 4 L 20 8 Z" fill="#92400E" stroke="#1A1A1A" strokeWidth={3} />
      </g>
    );
  }

  // Mac dinh: tau_thuy buom co dien
  return (
    <g transform={`translate(0, ${nhip.toFixed(1)})`}>
      {/* Than tau go */}
      <path
        d="M -38 8 L 40 8 L 28 24 L -26 24 Z"
        fill="#92400E"
        stroke="#1A1A1A"
        strokeWidth={3.5}
        strokeLinejoin="round"
      />
      {/* Cot buom & 2 canh buom */}
      <line x1={-2} y1={8} x2={-2} y2={-34} stroke="#1A1A1A" strokeWidth={3.5} />
      <path
        d="M -2 -32 L 30 -6 L -2 2 Z"
        fill="#FFFBEB"
        stroke="#1A1A1A"
        strokeWidth={3}
        strokeLinejoin="round"
      />
      <path
        d="M -4 -26 L -26 -2 L -4 2 Z"
        fill="#FEF3C7"
        stroke="#1A1A1A"
        strokeWidth={3}
        strokeLinejoin="round"
      />
      <polygon points="-2,-34 12,-29 -2,-24" fill="#DC2626" stroke="#1A1A1A" strokeWidth={2} />
    </g>
  );
};

/**
 * CanhBanDoHanhTrinh (v3.5):
 * - Nen ban do giay da co voi hoa la ban, kinh/vi tuyen va vung dat-bien phang 2 sac do (tat dinh 100%)
 * - Duong net dut chay dan theo frame noi diemDi -> diemDen kem bieu tuong tau/thu/nguoi di chuyen muot.
 */
export const CanhBanDoHanhTrinh: React.FC<Props> = ({ canh }) => {
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const data = canh.banDoHanhTrinh;

  const diemDi = (data?.diemDi || 'Điểm Khởi Hành').trim();
  const diemDen = (data?.diemDen || 'Điểm Đích').trim();
  const phuongTien: PhuongTienHanhTrinh = data?.phuongTien ?? 'tau_thuy';
  const khoangCachNhan = (data?.khoangCachNhan || canh.namMoc || '').trim();
  const moTaHanhTrinh = (data?.moTaHanhTrinh || canh.tieuDeNho || '').trim();
  const diemDungGiua = (data?.diemDungGiua || '').trim();

  const { p0, p1, p2 } = TOA_DO_BAN_DO_MAC_DINH;
  const trangThai = tinhTrangThaiHanhTrinh(frame, thoiLuong, p0, p1, p2);
  const pathD = `M ${p0.x} ${p0.y} Q ${p1.x} ${p1.y} ${p2.x} ${p2.y}`;
  const chieuDaiUocLuong = 1420;
  const dashOffset = chieuDaiUocLuong * (1 - trangThai.tienDo);
  const pulseDich = trangThai.daDenNoi ? 1 + Math.sin(frame * 0.35) * 0.14 : 1;

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundColor: '#EBD9B4',
        overflow: 'hidden',
      }}
    >
      <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: 'absolute', inset: 0 }}>
        {/* Nen dai duong co & vien giay da */}
        <rect x={0} y={0} width={1920} height={1080} fill="#DFC896" />
        <rect x={36} y={36} width={1848} height={1008} rx={24} fill="#ECDAB2" stroke="#1A1A1A" strokeWidth={5} />
        <rect x={54} y={54} width={1812} height={972} rx={16} fill="none" stroke="#854D0E" strokeWidth={2.5} strokeDasharray="14 8" />

        {/* Luoi kinh do / vi do co dien */}
        {[240, 480, 720, 960, 1200, 1440, 1680].map((gx) => (
          <line key={`mx-${gx}`} x1={gx} y1={56} x2={gx} y2={1024} stroke="#92400E" strokeOpacity={0.14} strokeWidth={1.6} />
        ))}
        {[220, 400, 580, 760, 940].map((gy) => (
          <line key={`my-${gy}`} x1={56} y1={gy} x2={1864} y2={gy} stroke="#92400E" strokeOpacity={0.14} strokeWidth={1.6} />
        ))}

        {/* 2 mang luc dia cach dieu phang 2 sac do o 2 dau hanh trinh */}
        <path
          d="M 56 500 C 210 470, 470 520, 560 660 C 610 750, 510 920, 420 1024 L 56 1024 Z"
          fill="#D4B47A"
          stroke="#78350F"
          strokeWidth={3.5}
        />
        <path
          d="M 56 540 C 190 520, 410 560, 495 680 C 540 760, 460 900, 370 1024 L 56 1024 Z"
          fill="#C9A364"
          fillOpacity={0.42}
        />
        <path
          d="M 1340 56 L 1864 56 L 1864 650 C 1740 620, 1520 630, 1410 530 C 1310 430, 1260 210, 1340 56 Z"
          fill="#D4B47A"
          stroke="#78350F"
          strokeWidth={3.5}
        />
        <path
          d="M 1400 56 L 1864 56 L 1864 590 C 1740 560, 1550 570, 1460 485 C 1380 410, 1340 200, 1400 56 Z"
          fill="#C9A364"
          fillOpacity={0.42}
        />

        {/* Song bien cach dieu tat dinh */}
        {[
          [720, 620],
          [860, 740],
          [1040, 660],
          [1160, 800],
          [820, 500],
          [1120, 540],
        ].map(([wx, wy], i) => (
          <path
            key={`wave-${i}`}
            d={`M ${wx} ${wy} Q ${wx + 24} ${wy - 10} ${wx + 48} ${wy} Q ${wx + 72} ${wy + 10} ${wx + 96} ${wy}`}
            fill="none"
            stroke="#78350F"
            strokeOpacity={0.28}
            strokeWidth={3}
            strokeLinecap="round"
          />
        ))}

        {/* Hoa la ban co dien goc duoi phai */}
        <g transform="translate(1700, 845)">
          <circle cx={0} cy={0} r={78} fill="#F8EED6" stroke="#1A1A1A" strokeWidth={3.5} />
          <circle cx={0} cy={0} r={66} fill="none" stroke="#92400E" strokeWidth={2} strokeDasharray="6 4" />
          <polygon points="0,-58 14,-12 0,-4 -14,-12" fill="#DC2626" stroke="#1A1A1A" strokeWidth={2} />
          <polygon points="0,58 14,12 0,4 -14,12" fill="#1E293B" stroke="#1A1A1A" strokeWidth={2} />
          <polygon points="58,0 12,14 4,0 12,-14" fill="#B45309" stroke="#1A1A1A" strokeWidth={2} />
          <polygon points="-58,0 -12,14 -4,0 -12,-14" fill="#FDE68A" stroke="#1A1A1A" strokeWidth={2} />
          <circle cx={0} cy={0} r={8} fill="#FAF3E0" stroke="#1A1A1A" strokeWidth={2.5} />
          <text x={0} y={-62} textAnchor="middle" fill="#1A1A1A" fontSize={18} fontWeight={900}>N</text>
        </g>

        {/* Duong mo du kien phia duoi */}
        <path
          d={pathD}
          fill="none"
          stroke="#78350F"
          strokeOpacity={0.22}
          strokeWidth={7}
          strokeDasharray="16 14"
          strokeLinecap="round"
        />

        {/* Duong net dut do chay dan theo frame bang mask pathLength */}
        <path
          d={pathD}
          fill="none"
          stroke="#B91C1C"
          strokeWidth={8}
          strokeLinecap="round"
          strokeDasharray={`${chieuDaiUocLuong} ${chieuDaiUocLuong}`}
          strokeDashoffset={dashOffset}
        />
        <path
          d={pathD}
          fill="none"
          stroke="#FEF08A"
          strokeWidth={3.5}
          strokeDasharray="18 16"
          strokeLinecap="round"
          strokeDashoffset={dashOffset}
        />

        {/* Moc diemDi */}
        <g transform={`translate(${p0.x}, ${p0.y})`}>
          <circle cx={0} cy={0} r={22} fill="#1D4ED8" stroke="#1A1A1A" strokeWidth={4} />
          <circle cx={0} cy={0} r={8} fill="#FFFFFF" />
        </g>

        {/* Moc diemDungGiua (tuy chon) */}
        {diemDungGiua && (
          <g transform={`translate(${p1.x}, ${(p1.y + 160).toFixed(0)})`}>
            <circle cx={0} cy={0} r={11} fill="#F59E0B" stroke="#1A1A1A" strokeWidth={3} />
            <text
              x={0}
              y={34}
              textAnchor="middle"
              fill="#78350F"
              fontSize={22}
              fontWeight={800}
            >
              {diemDungGiua}
            </text>
          </g>
        )}

        {/* Moc diemDen (bung sang khi phuong tien toi noi) */}
        <g transform={`translate(${p2.x}, ${p2.y}) scale(${pulseDich.toFixed(3)})`}>
          <circle cx={0} cy={0} r={34} fill="#FACC15" fillOpacity={trangThai.daDenNoi ? 0.45 : 0.18} />
          <circle cx={0} cy={0} r={22} fill="#DC2626" stroke="#1A1A1A" strokeWidth={4} />
          <polygon points="0,-10 3.5,-3 11,-3 5,2 7,9 0,5 -7,9 -5,2 -11,-3 -3.5,-3" fill="#FEF08A" />
        </g>

        {/* Bieu tuong phuong tien di chuyen muot doc theo duong cong */}
        <g
          transform={`translate(${trangThai.viTri.x}, ${trangThai.viTri.y - 16}) rotate(${(trangThai.gocHuongDeg * 0.45).toFixed(1)}) scale(1.25)`}
        >
          <BieuTuongPhuongTien loai={phuongTien} frame={frame} />
        </g>
      </svg>

      {/* The nhan tieu de hanh trinh phia tren */}
      {(moTaHanhTrinh || khoangCachNhan) && (
        <div
          style={{
            position: 'absolute',
            top: 72,
            left: 90,
            right: 90,
            display: 'flex',
            justifyContent: 'center',
            pointerEvents: 'none',
          }}
        >
          <div
            style={{
              backgroundColor: '#FAF3E0',
              border: '3.5px solid #1A1A1A',
              borderRadius: 16,
              padding: '12px 34px',
              boxShadow: '6px 6px 0px rgba(26, 26, 26, 0.38)',
              textAlign: 'center',
            }}
          >
            {khoangCachNhan && (
              <div
                style={{
                  fontSize: 19,
                  fontWeight: 900,
                  color: '#B91C1C',
                  letterSpacing: 1.5,
                  textTransform: 'uppercase',
                  marginBottom: moTaHanhTrinh ? 4 : 0,
                }}
              >
                {khoangCachNhan}
              </div>
            )}
            {moTaHanhTrinh && (
              <div style={{ fontSize: 34, fontWeight: 900, color: '#1A1A1A', lineHeight: 1.2 }}>
                {moTaHanhTrinh}
              </div>
            )}
          </div>
        </div>
      )}

      {/* The ten diemDi */}
      <div
        style={{
          position: 'absolute',
          left: p0.x - 165,
          top: p0.y + 38,
          width: 330,
          textAlign: 'center',
          pointerEvents: 'none',
        }}
      >
        <div
          style={{
            display: 'inline-block',
            backgroundColor: '#1E3A8A',
            color: '#FFFFFF',
            border: '3.5px solid #1A1A1A',
            borderRadius: 14,
            padding: '10px 22px',
            fontSize: 28,
            fontWeight: 900,
            boxShadow: '5px 5px 0px #1A1A1A',
          }}
        >
          {diemDi}
        </div>
      </div>

      {/* The ten diemDen */}
      <div
        style={{
          position: 'absolute',
          left: p2.x - 180,
          top: p2.y + 42,
          width: 360,
          textAlign: 'center',
          pointerEvents: 'none',
        }}
      >
        <div
          style={{
            display: 'inline-block',
            backgroundColor: '#B91C1C',
            color: '#FEF08A',
            border: '3.5px solid #1A1A1A',
            borderRadius: 14,
            padding: '10px 24px',
            fontSize: 30,
            fontWeight: 900,
            boxShadow: '5px 5px 0px #1A1A1A',
          }}
        >
          {diemDen}
        </div>
      </div>
    </div>
  );
};
