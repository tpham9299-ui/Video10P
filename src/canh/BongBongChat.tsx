import React from 'react';
import { useCurrentFrame } from 'remotion';
import type { KieuBongBongChat } from '../kieu_dai';
import { kepGiaTri, springTatDinh } from '../xuong/duong_cong';
import { MAU_MUC_TRUYEN_TRANH } from '../nhanvat/hoa_trang_va_anh_sang';
import { tinhBoCucBongBongChat } from './bong_bong_logic';

export type BongBongChatProps = {
  noiDung: string;
  kieu?: KieuBongBongChat;
  frameBatDau?: number;
  nhanVatWorldX: number;
  nhanVatWorldY: number;
  tiLeNhanVat: number;
  dauLocalX: number;
  dauLocalY: number;
  dir: number;
  banKinhDau?: number;
};

/** Tao duong vien rang cua kich tinh cho bong bong quat_thao (tat dinh 100%) */
function taoDuongRangCua(w: number, h: number): string {
  const rx = w / 2;
  const ry = h / 2;
  const soDinh = 18;
  const pts: string[] = [];
  for (let i = 0; i < soDinh * 2; i++) {
    const goc = (i / (soDinh * 2)) * Math.PI * 2;
    const laDinhNgoai = i % 2 === 0;
    const heSo = laDinhNgoai ? 1.13 : 0.97;
    const px = Math.cos(goc) * rx * heSo;
    const py = Math.sin(goc) * ry * heSo;
    pts.push(`${i === 0 ? 'M' : 'L'} ${px.toFixed(1)} ${py.toFixed(1)}`);
  }
  return `${pts.join(' ')} Z`;
}

/** Tao duong vien dam may cho bong bong suy_nghi (tat dinh 100%) */
function taoDuongDamMay(w: number, h: number): string {
  const hw = w / 2;
  const hh = h / 2;
  const d = [
    `M ${(-hw + 18).toFixed(1)} ${(-hh + 2).toFixed(1)}`,
    `Q ${(-hw * 0.45).toFixed(1)} ${(-hh - 14).toFixed(1)} 0 ${(-hh - 4).toFixed(1)}`,
    `Q ${(hw * 0.45).toFixed(1)} ${(-hh - 14).toFixed(1)} ${(hw - 18).toFixed(1)} ${(-hh + 2).toFixed(1)}`,
    `Q ${(hw + 14).toFixed(1)} ${(-hh * 0.25).toFixed(1)} ${(hw + 4).toFixed(1)} ${(hh * 0.1).toFixed(1)}`,
    `Q ${(hw + 14).toFixed(1)} ${(hh * 0.55).toFixed(1)} ${(hw - 18).toFixed(1)} ${(hh - 2).toFixed(1)}`,
    `Q ${(hw * 0.45).toFixed(1)} ${(hh + 13).toFixed(1)} 0 ${(hh + 4).toFixed(1)}`,
    `Q ${(-hw * 0.45).toFixed(1)} ${(hh + 13).toFixed(1)} ${(-hw + 18).toFixed(1)} ${(hh - 2).toFixed(1)}`,
    `Q ${(-hw - 14).toFixed(1)} ${(hh * 0.55).toFixed(1)} ${(-hw - 4).toFixed(1)} ${(hh * 0.1).toFixed(1)}`,
    `Q ${(-hw - 14).toFixed(1)} ${(-hh * 0.25).toFixed(1)} ${(-hw + 18).toFixed(1)} ${(-hh + 2).toFixed(1)} Z`,
  ];
  return d.join(' ');
}

/**
 * Bong bong chat hoat hinh ve net muc #1A1A1A dong bo truyen tranh chau Au (v3.0):
 * - Bat nay lo xo springTatDinh canh mieng nhan vat voi duoi tro dung huong
 * - Ho tro du 4 kieu: thuong | quat_thao (rang cua cam do rung nhe) | suy_nghi (dam may 3 cham tron) | ca_khia (net dut tinh nghich)
 * - Tu tranh tran mep 1920x1080 va tuyet doi khong che mat nhan vat
 */
export const BongBongChat: React.FC<BongBongChatProps> = ({
  noiDung,
  kieu = 'thuong',
  frameBatDau = 0,
  nhanVatWorldX,
  nhanVatWorldY,
  tiLeNhanVat,
  dauLocalX,
  dauLocalY,
  dir,
  banKinhDau = 26,
}) => {
  const frame = useCurrentFrame();
  if (!noiDung || !noiDung.trim()) {
    return null;
  }

  const bc = tinhBoCucBongBongChat({
    noiDung,
    kieu,
    nhanVatWorldX,
    nhanVatWorldY,
    tiLeNhanVat,
    dauLocalX,
    dauLocalY,
    dir,
    banKinhDau,
  });

  if (bc.dong.length === 0) {
    return null;
  }

  const loXo = springTatDinh(frame - frameBatDau - 1, 10.5, 230);
  const scale = kepGiaTri(loXo, 0, 1.14);
  if (scale <= 0.01) {
    return null;
  }

  const rungX = kieu === 'quat_thao' ? Math.sin(frame * 1.9) * 2.2 : 0;
  const rungY =
    kieu === 'quat_thao'
      ? Math.cos(frame * 2.3) * 1.8
      : Math.sin(frame * 0.1) * 1.8;
  const nghieng = kieu === 'ca_khia' ? (dir > 0 ? -1.8 : 1.8) : 0;

  const hw = bc.width / 2;
  const hh = bc.height / 2;

  // Diem goc duoi bong bong gan nhat voi mieng nhan vat
  const gocDuoiX =
    bc.viTriTuongDoi === 'ben_phai'
      ? -hw + 4
      : bc.viTriTuongDoi === 'ben_trai'
        ? hw - 4
        : kepGiaTri(bc.duoiTargetX, -hw + 28, hw - 28);
  const gocDuoiY =
    bc.viTriTuongDoi === 'phia_tren'
      ? hh - 2
      : kepGiaTri(bc.duoiTargetY * 0.35, -hh + 18, hh - 16);

  const muiX =
    bc.viTriTuongDoi === 'ben_phai'
      ? -hw - 19
      : bc.viTriTuongDoi === 'ben_trai'
        ? hw + 19
        : gocDuoiX + (bc.duoiTargetX - gocDuoiX) * 0.35;
  const muiY =
    bc.viTriTuongDoi === 'phia_tren'
      ? hh + 18
      : gocDuoiY + 12;

  const veDuoiHoacCham = () => {
    if (kieu === 'suy_nghi') {
      // 3 cham tron nho dan ve phia dau/mieng nhan vat
      return (
        <g>
          {[0.25, 0.55, 0.85].map((t, i) => {
            const cx = gocDuoiX + (muiX - gocDuoiX) * t;
            const cy = gocDuoiY + (muiY - gocDuoiY) * t;
            const r = 6.2 - i * 1.6;
            return (
              <circle
                key={`cham-sn-${i}`}
                cx={cx.toFixed(1)}
                cy={cy.toFixed(1)}
                r={r.toFixed(1)}
                fill="#F8FAFC"
                stroke={MAU_MUC_TRUYEN_TRANH}
                strokeWidth={2.4}
              />
            );
          })}
        </g>
      );
    }

    const baseOffset = bc.viTriTuongDoi === 'phia_tren' ? { x1: -10, y1: 0, x2: 10, y2: 0 } : { x1: 0, y1: -9, x2: 0, y2: 9 };
    const mauNen =
      kieu === 'quat_thao'
        ? '#FFF7ED'
        : kieu === 'ca_khia'
          ? '#FEFCE8'
          : '#FFFDF7';
    const mauVien = kieu === 'quat_thao' ? '#DC2626' : MAU_MUC_TRUYEN_TRANH;

    return (
      <g>
        <polygon
          points={`${(gocDuoiX + baseOffset.x1).toFixed(1)},${(gocDuoiY + baseOffset.y1).toFixed(1)} ${(gocDuoiX + baseOffset.x2).toFixed(1)},${(gocDuoiY + baseOffset.y2).toFixed(1)} ${muiX.toFixed(1)},${muiY.toFixed(1)}`}
          fill={mauNen}
          stroke={mauVien}
          strokeWidth={2.8}
          strokeLinejoin="round"
        />
        <line
          x1={(gocDuoiX + baseOffset.x1 * 0.8).toFixed(1)}
          y1={(gocDuoiY + baseOffset.y1 * 0.8).toFixed(1)}
          x2={(gocDuoiX + baseOffset.x2 * 0.8).toFixed(1)}
          y2={(gocDuoiY + baseOffset.y2 * 0.8).toFixed(1)}
          stroke={mauNen}
          strokeWidth={4.5}
        />
      </g>
    );
  };

  const veKhung = () => {
    if (kieu === 'quat_thao') {
      const dRang = taoDuongRangCua(bc.width, bc.height);
      return (
        <g>
          <path d={dRang} transform="translate(4, 4)" fill="#7C2D12" fillOpacity={0.28} />
          <path d={dRang} fill="#FFF7ED" stroke="#DC2626" strokeWidth={4.2} strokeLinejoin="round" />
          <path d={dRang} transform="scale(0.955)" fill="none" stroke="#F97316" strokeWidth={2} strokeLinejoin="round" />
        </g>
      );
    }

    if (kieu === 'suy_nghi') {
      const dMay = taoDuongDamMay(bc.width, bc.height);
      return (
        <g>
          <path d={dMay} transform="translate(3, 4)" fill="#1A1A1A" fillOpacity={0.14} />
          <path d={dMay} fill="#F8FAFC" stroke={MAU_MUC_TRUYEN_TRANH} strokeWidth={3} strokeLinejoin="round" />
        </g>
      );
    }

    if (kieu === 'ca_khia') {
      return (
        <g>
          <rect
            x={-hw + 4}
            y={-hh + 4}
            width={bc.width}
            height={bc.height}
            rx={18}
            fill="#1A1A1A"
            fillOpacity={0.18}
          />
          <rect
            x={-hw}
            y={-hh}
            width={bc.width}
            height={bc.height}
            rx={18}
            fill="#FEFCE8"
            stroke={MAU_MUC_TRUYEN_TRANH}
            strokeWidth={3.2}
            strokeDasharray="9 5"
          />
          {/* Tia chop nho tinh nghich o goc */}
          <path
            d={`M ${(hw - 14).toFixed(1)} ${(-hh - 8).toFixed(1)} L ${(hw - 8).toFixed(1)} ${(-hh - 2).toFixed(1)} M ${(hw - 4).toFixed(1)} ${(-hh - 11).toFixed(1)} L ${(hw - 2).toFixed(1)} ${(-hh - 4).toFixed(1)}`}
            stroke="#EA580C"
            strokeWidth={2.6}
            strokeLinecap="round"
          />
        </g>
      );
    }

    // thuong: bong bong giay kem vien muc den sac net
    return (
      <g>
        <rect
          x={-hw + 3.5}
          y={-hh + 4}
          width={bc.width}
          height={bc.height}
          rx={18}
          fill="#1A1A1A"
          fillOpacity={0.16}
        />
        <rect
          x={-hw}
          y={-hh}
          width={bc.width}
          height={bc.height}
          rx={18}
          fill="#FFFDF7"
          stroke={MAU_MUC_TRUYEN_TRANH}
          strokeWidth={3.2}
        />
      </g>
    );
  };

  const mauChu = kieu === 'quat_thao' ? '#9A3412' : '#111827';

  return (
    <g
      transform={`translate(${(bc.localX + rungX).toFixed(1)}, ${(bc.localY + rungY).toFixed(1)}) rotate(${nghieng.toFixed(1)}) scale(${scale.toFixed(3)})`}
    >
      {veDuoiHoacCham()}
      {veKhung()}
      {/* Lap lai luoi che mep duoi de duoi noi lien mach vao khung */}
      {kieu !== 'suy_nghi' && kieu !== 'quat_thao' && (
        <rect
          x={-hw + 2}
          y={-hh + 2}
          width={bc.width - 4}
          height={bc.height - 4}
          rx={16}
          fill={kieu === 'ca_khia' ? '#FEFCE8' : '#FFFDF7'}
        />
      )}
      {bc.dong.map((dong, idx) => {
        const yDong =
          -hh +
          bc.paddingY +
          bc.fontSize * 0.85 +
          idx * bc.lineHeight;
        return (
          <text
            key={`bb-dong-${idx}`}
            x={0}
            y={yDong.toFixed(1)}
            textAnchor="middle"
            fill={mauChu}
            fontSize={bc.fontSize}
            fontWeight={kieu === 'quat_thao' ? 900 : 700}
            fontFamily="Segoe UI, Arial, sans-serif"
          >
            {dong}
          </text>
        );
      })}
    </g>
  );
};
