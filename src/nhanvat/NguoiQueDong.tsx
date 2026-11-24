import React from 'react';
import { interpolate, useCurrentFrame, useVideoConfig } from 'remotion';
import type {
  LoaiBieuCam,
  LoaiPhuKien,
  LoaiVatCamTay,
  NhanVatTrongCanh,
  ThongTinNhanVat,
} from '../kieu_dai';
import { tinhKhungXuongCoBan } from '../xuong/he_xuong';
import { bamChuoiTatDinh } from '../vfx/tat_dinh';

type NguoiQueDongProps = {
  thongTin: ThongTinNhanVat;
  trangThai: NhanVatTrongCanh;
  tiLe?: number;
  thoiLuongCanh?: number;
};

/** Ve khuon mat hoat hinh voi 9 bieu cam ro net + tu dong nhay mat tat dinh */
const veBieuCam = (
  bieuCam: LoaiBieuCam,
  dir: number,
  mauNet: string,
  dangNoi: boolean,
  frame: number,
  seedId: number,
) => {
  const matTraiX = 3 * dir;
  const matPhaiX = 12.5 * dir;
  const matY = -4;
  const miengX = 7.5 * dir;
  const miengY = 8;

  // Tu dong nhay mat tat dinh: moi 95 frame chop mat trong 4 frame
  const phaNhay = (frame + (seedId % 53)) % 95;
  const dangNhayMat = phaNhay >= 91 && bieuCam !== 'can_loi_mat_do' && bieuCam !== 'ngac_nhien';

  const moMieng = dangNoi ? Math.abs(Math.sin(frame * 0.58)) * 4.5 + 1.6 : 0;

  return (
    <g>
      {/* Ma hong duyen dang cho bieu cam vui tuoi / tu man */}
      {(bieuCam === 'vui_tuoi' || bieuCam === 'tu_man') && (
        <>
          <ellipse cx={matTraiX - 4 * dir} cy={matY + 8} rx={4.2} ry={2.4} fill="#FB7185" fillOpacity={0.38} />
          <ellipse cx={matPhaiX + 4 * dir} cy={matY + 8} rx={4.2} ry={2.4} fill="#FB7185" fillOpacity={0.38} />
        </>
      )}

      {/* Long may theo bieu cam */}
      {bieuCam === 'tuc_gian' && (
        <>
          <line x1={matTraiX - 4} y1={matY - 8} x2={matTraiX + 4.5} y2={matY - 4.5} stroke={mauNet} strokeWidth={2.6} strokeLinecap="round" />
          <line x1={matPhaiX - 4.5} y1={matY - 4.5} x2={matPhaiX + 4} y2={matY - 8} stroke={mauNet} strokeWidth={2.6} strokeLinecap="round" />
        </>
      )}
      {bieuCam === 'ngac_nhien' && (
        <>
          <path d={`M ${matTraiX - 4} ${matY - 9} Q ${matTraiX} ${matY - 12} ${matTraiX + 4} ${matY - 9}`} fill="none" stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
          <path d={`M ${matPhaiX - 4} ${matY - 9} Q ${matPhaiX} ${matY - 12} ${matPhaiX + 4} ${matY - 9}`} fill="none" stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
        </>
      )}
      {bieuCam === 'hoang_mang' && (
        <>
          <line x1={matTraiX - 4.5} y1={matY - 6} x2={matTraiX + 4} y2={matY - 9.5} stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
          <line x1={matPhaiX - 4} y1={matY - 9.5} x2={matPhaiX + 4.5} y2={matY - 6} stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
        </>
      )}
      {bieuCam === 'tinh_quai' && (
        <>
          <line x1={matTraiX - 4} y1={matY - 9} x2={matTraiX + 4} y2={matY - 6} stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
          <path d={`M ${matPhaiX - 4} ${matY - 9} Q ${matPhaiX} ${matY - 12} ${matPhaiX + 4} ${matY - 8}`} fill="none" stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
        </>
      )}
      {bieuCam === 'tram_tu' && (
        <>
          <line x1={matTraiX - 4} y1={matY - 7} x2={matTraiX + 4} y2={matY - 7} stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
          <line x1={matPhaiX - 4} y1={matY - 8.5} x2={matPhaiX + 4} y2={matY - 6.5} stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
        </>
      )}
      {bieuCam === 'tu_man' && (
        <>
          <path d={`M ${matTraiX - 4} ${matY - 8} Q ${matTraiX} ${matY - 11.5} ${matTraiX + 4} ${matY - 8}`} fill="none" stroke={mauNet} strokeWidth={2.4} strokeLinecap="round" />
          <line x1={matPhaiX - 4} y1={matY - 7} x2={matPhaiX + 4} y2={matY - 9.5} stroke={mauNet} strokeWidth={2.4} strokeLinecap="round" />
        </>
      )}

      {/* Doi mat: nhay mat / can_loi_mat_do (— —) / bieu cam dac trung */}
      {bieuCam === 'can_loi_mat_do' ? (
        <>
          <line x1={matTraiX - 3.2} y1={matY} x2={matTraiX + 3.2} y2={matY} stroke={mauNet} strokeWidth={3} strokeLinecap="round" />
          <line x1={matPhaiX - 3.2} y1={matY} x2={matPhaiX + 3.2} y2={matY} stroke={mauNet} strokeWidth={3} strokeLinecap="round" />
        </>
      ) : dangNhayMat ? (
        <>
          <path d={`M ${matTraiX - 3.8} ${matY} Q ${matTraiX} ${matY + 2.5} ${matTraiX + 3.8} ${matY}`} fill="none" stroke={mauNet} strokeWidth={2.5} strokeLinecap="round" />
          <path d={`M ${matPhaiX - 3.8} ${matY} Q ${matPhaiX} ${matY + 2.5} ${matPhaiX + 3.8} ${matY}`} fill="none" stroke={mauNet} strokeWidth={2.5} strokeLinecap="round" />
        </>
      ) : bieuCam === 'vui_tuoi' ? (
        <>
          <path d={`M ${matTraiX - 3.6} ${matY + 1} Q ${matTraiX} ${matY - 4.2} ${matTraiX + 3.6} ${matY + 1}`} fill="none" stroke={mauNet} strokeWidth={2.8} strokeLinecap="round" />
          <path d={`M ${matPhaiX - 3.6} ${matY + 1} Q ${matPhaiX} ${matY - 4.2} ${matPhaiX + 3.6} ${matY + 1}`} fill="none" stroke={mauNet} strokeWidth={2.8} strokeLinecap="round" />
        </>
      ) : bieuCam === 'ngac_nhien' || bieuCam === 'hoang_mang' ? (
        <>
          <circle cx={matTraiX} cy={matY} r={4.2} fill="#FFFFFF" stroke={mauNet} strokeWidth={2.2} />
          <circle cx={matPhaiX} cy={matY} r={4.2} fill="#FFFFFF" stroke={mauNet} strokeWidth={2.2} />
          <circle cx={matTraiX + 0.5 * dir} cy={matY} r={1.6} fill={mauNet} />
          <circle cx={matPhaiX + 0.5 * dir} cy={matY} r={1.6} fill={mauNet} />
        </>
      ) : bieuCam === 'tu_man' ? (
        <>
          {/* Mat nua khep tu man */}
          <circle cx={matTraiX} cy={matY + 1} r={2.6} fill={mauNet} />
          <circle cx={matPhaiX} cy={matY + 1} r={2.6} fill={mauNet} />
          <line x1={matTraiX - 4} y1={matY - 1.5} x2={matTraiX + 4} y2={matY - 1.5} stroke={mauNet} strokeWidth={2.5} strokeLinecap="round" />
          <line x1={matPhaiX - 4} y1={matY - 1.5} x2={matPhaiX + 4} y2={matY - 1.5} stroke={mauNet} strokeWidth={2.5} strokeLinecap="round" />
        </>
      ) : (
        <>
          <circle cx={matTraiX} cy={matY} r={3.1} fill={mauNet} />
          <circle cx={matPhaiX} cy={matY} r={3.1} fill={mauNet} />
          <circle cx={matTraiX - 0.9} cy={matY - 1} r={1} fill="#FFFFFF" />
          <circle cx={matPhaiX - 0.9} cy={matY - 1} r={1} fill="#FFFFFF" />
        </>
      )}

      {/* Mieng: mo/khep nhip nhang khi dangNoi, hoac theo 9 bieu cam */}
      {dangNoi ? (
        <g>
          <ellipse cx={miengX} cy={miengY} rx={5.2} ry={moMieng} fill="#991B1B" stroke={mauNet} strokeWidth={2} />
          {moMieng > 3 && <ellipse cx={miengX} cy={miengY + 1.5} rx={3} ry={1.4} fill="#FB7185" />}
        </g>
      ) : bieuCam === 'vui_tuoi' ? (
        <path
          d={`M ${miengX - 6.5} ${miengY - 1.5} Q ${miengX} ${miengY + 7.5} ${miengX + 6.5} ${miengY - 1.5} Z`}
          fill="#DC2626"
          stroke={mauNet}
          strokeWidth={2}
          strokeLinejoin="round"
        />
      ) : bieuCam === 'tu_man' || bieuCam === 'tinh_quai' ? (
        <path
          d={`M ${miengX - 5.5} ${miengY + 1} Q ${miengX + 1 * dir} ${miengY + 4.5} ${miengX + 6.5 * dir} ${miengY - 2.5}`}
          fill="none"
          stroke={mauNet}
          strokeWidth={2.6}
          strokeLinecap="round"
        />
      ) : bieuCam === 'ngac_nhien' ? (
        <ellipse cx={miengX} cy={miengY + 1} rx={4} ry={5} fill="#991B1B" stroke={mauNet} strokeWidth={2.2} />
      ) : bieuCam === 'tuc_gian' ? (
        <path
          d={`M ${miengX - 6} ${miengY + 3.5} Q ${miengX} ${miengY - 3} ${miengX + 6} ${miengY + 3.5}`}
          fill="none"
          stroke={mauNet}
          strokeWidth={2.6}
          strokeLinecap="round"
        />
      ) : bieuCam === 'hoang_mang' ? (
        <path
          d={`M ${miengX - 6} ${miengY + 1} Q ${miengX - 3} ${miengY - 2} ${miengX} ${miengY + 1} Q ${miengX + 3} ${miengY + 4} ${miengX + 6} ${miengY + 1}`}
          fill="none"
          stroke={mauNet}
          strokeWidth={2.4}
          strokeLinecap="round"
        />
      ) : bieuCam === 'can_loi_mat_do' ? (
        <line x1={miengX - 4.5} y1={miengY + 1} x2={miengX + 4.5} y2={miengY + 1} stroke={mauNet} strokeWidth={2.6} strokeLinecap="round" />
      ) : bieuCam === 'tram_tu' ? (
        <line x1={miengX - 4} y1={miengY} x2={miengX + 4} y2={miengY - 0.8} stroke={mauNet} strokeWidth={2.4} strokeLinecap="round" />
      ) : (
        <path
          d={`M ${miengX - 5} ${miengY - 0.5} Q ${miengX} ${miengY + 4} ${miengX + 5} ${miengY - 0.5}`}
          fill="none"
          stroke={mauNet}
          strokeWidth={2.4}
          strokeLinecap="round"
        />
      )}
    </g>
  );
};

/** 8 phu kien nhan vat sac net */
const vePhuKien = (
  phuKien: LoaiPhuKien,
  dauX: number,
  dauY: number,
  coX: number,
  coY: number,
  dir: number,
  mauChuDao: string,
  frame: number,
) => {
  const nhipBay = Math.sin(frame * 0.16) * 5;
  const nhipBay2 = Math.cos(frame * 0.14) * 4;

  switch (phuKien) {
    case 'vong_nguyet_que':
      return (
        <g transform={`translate(${dauX}, ${dauY - 20})`}>
          <path d="M -22 5 Q 0 -9 22 5" fill="none" stroke="#B45309" strokeWidth={3.2} strokeLinecap="round" />
          {[-18, -11, -4, 4, 11, 18].map((lx, idx) => {
            const goc = idx < 3 ? -32 + idx * 10 : 32 - (5 - idx) * 10;
            const ly = Math.abs(lx) * 0.18 - 2;
            return (
              <ellipse
                key={`la-${lx}`}
                cx={lx}
                cy={ly}
                rx={6.4}
                ry={3.2}
                fill="#22C55E"
                stroke="#14532D"
                strokeWidth={1.2}
                transform={`rotate(${goc}, ${lx}, ${ly})`}
              />
            );
          })}
          <circle cx={0} cy={-4} r={3.5} fill="#FACC15" stroke="#854D0E" strokeWidth={1.2} />
        </g>
      );

    case 'toc_gia_17':
      return (
        <g transform={`translate(${dauX}, ${dauY})`}>
          <path
            d="M -26 14 Q -32 -12 -18 -26 Q 0 -33 18 -26 Q 32 -12 26 14 Q 20 22 15 14 Q 21 -6 14 -16 Q 0 -22 -14 -16 Q -21 -6 -15 14 Q -20 22 -26 14 Z"
            fill="#F1F5F9"
            stroke="#64748B"
            strokeWidth={2.2}
          />
          <circle cx={-23} cy={-3} r={7} fill="#FFFFFF" stroke="#94A3B8" strokeWidth={1.6} />
          <circle cx={-23} cy={8} r={6.5} fill="#E2E8F0" stroke="#94A3B8" strokeWidth={1.6} />
          <circle cx={23} cy={-3} r={7} fill="#FFFFFF" stroke="#94A3B8" strokeWidth={1.6} />
          <circle cx={23} cy={8} r={6.5} fill="#E2E8F0" stroke="#94A3B8" strokeWidth={1.6} />
        </g>
      );

    case 'kinh_tron':
      return (
        <g transform={`translate(${dauX}, ${dauY})`}>
          <circle cx={3 * dir} cy={-4} r={6.4} fill="#E0F2FE" fillOpacity={0.35} stroke="#1E293B" strokeWidth={2.3} />
          <circle cx={14.8 * dir} cy={-4} r={6.4} fill="#E0F2FE" fillOpacity={0.35} stroke="#1E293B" strokeWidth={2.3} />
          <line x1={8.8 * dir} y1={-4} x2={9.4 * dir} y2={-4} stroke="#1E293B" strokeWidth={2.2} />
          <line x1={-3.2 * dir} y1={-4} x2={-19 * dir} y2={-6} stroke="#334155" strokeWidth={2} />
          <line x1={1 * dir} y1={-7} x2={4.5 * dir} y2={-3.5} stroke="#FFFFFF" strokeWidth={1.6} strokeLinecap="round" />
          <line x1={12.8 * dir} y1={-7} x2={16.3 * dir} y2={-3.5} stroke="#FFFFFF" strokeWidth={1.6} strokeLinecap="round" />
        </g>
      );

    case 'mu_noi_phap':
      return (
        <g transform={`translate(${dauX - 2 * dir}, ${dauY - 22}) rotate(${-10 * dir})`}>
          <ellipse cx={0} cy={0} rx={24} ry={10} fill={mauChuDao} stroke="#1E293B" strokeWidth={2.5} />
          <line x1={0} y1={-10} x2={2 * dir} y2={-17} stroke="#1E293B" strokeWidth={3} strokeLinecap="round" />
        </g>
      );

    case 'mu_tham_tu':
      return (
        <g transform={`translate(${dauX}, ${dauY - 20})`}>
          <path d="M -28 2 Q 0 -2 28 2 Q 0 9 -28 2 Z" fill="#92400E" stroke="#1E293B" strokeWidth={2.2} />
          <path d="M -18 0 Q -14 -20 0 -20 Q 14 -20 18 0 Z" fill="#B45309" stroke="#1E293B" strokeWidth={2.2} />
          <line x1={-16} y1={-5} x2={16} y2={-5} stroke="#78350F" strokeWidth={3.5} />
        </g>
      );

    case 'ao_choang':
      return (
        <g>
          <path
            d={`M ${coX} ${coY + 2} Q ${coX - 22 * dir} ${coY + 44} ${coX - (44 + nhipBay) * dir} ${coY + 90} L ${coX - (14 + nhipBay2 * 0.5) * dir} ${coY + 85} Q ${coX - 6 * dir} ${coY + 42} ${coX + 4 * dir} ${coY + 4} Z`}
            fill={mauChuDao}
            stroke="#1E293B"
            strokeWidth={2.8}
            strokeLinejoin="round"
          />
          <circle cx={coX + 2 * dir} cy={coY + 4} r={4.5} fill="#FACC15" stroke="#1E293B" strokeWidth={1.6} />
        </g>
      );

    case 'khan_choang':
      return (
        <g>
          <path
            d={`M ${coX - 2 * dir} ${coY + 4} Q ${coX - 28 * dir} ${coY + 14 + nhipBay} ${coX - (56 - nhipBay2) * dir} ${coY + 4 + nhipBay * 0.7}`}
            fill="none"
            stroke="#1E293B"
            strokeWidth={12}
            strokeLinecap="round"
          />
          <path
            d={`M ${coX - 2 * dir} ${coY + 4} Q ${coX - 28 * dir} ${coY + 14 + nhipBay} ${coX - (56 - nhipBay2) * dir} ${coY + 4 + nhipBay * 0.7}`}
            fill="none"
            stroke={mauChuDao}
            strokeWidth={7.5}
            strokeLinecap="round"
          />
          <rect x={coX - 12} y={coY - 2} width={24} height={11} rx={5} fill={mauChuDao} stroke="#1E293B" strokeWidth={2.2} />
        </g>
      );

    case 'khong':
    default:
      return null;
  }
};

/** 8 vat cam tay hoat hinh sac net */
const veVatCamTay = (
  vat: LoaiVatCamTay | undefined,
  x: number,
  y: number,
  dir: number,
  frame: number,
) => {
  if (!vat || vat === 'khong') {
    return null;
  }

  switch (vat) {
    case 'cuon_giay':
      return (
        <g transform={`translate(${x}, ${y}) scale(${dir}, 1) rotate(-14)`}>
          <rect x={-6} y={-24} width={28} height={38} rx={5} fill="#FEF3C7" stroke="#92400E" strokeWidth={2.5} />
          <ellipse cx={8} cy={-24} rx={14} ry={4.5} fill="#FDE68A" stroke="#92400E" strokeWidth={2} />
          <line x1={0} y1={-12} x2={16} y2={-12} stroke="#92400E" strokeWidth={2} strokeLinecap="round" />
          <line x1={0} y1={-4} x2={14} y2={-4} stroke="#92400E" strokeWidth={2} strokeLinecap="round" />
          <line x1={0} y1={4} x2={15} y2={4} stroke="#92400E" strokeWidth={2} strokeLinecap="round" />
        </g>
      );

    case 'qua_tao':
      return (
        <g transform={`translate(${x + 4 * dir}, ${y - 6})`}>
          <circle cx={0} cy={0} r={12.5} fill="#EF4444" stroke="#7F1D1D" strokeWidth={2.2} />
          <ellipse cx={-3.5} cy={-3.5} rx={3.5} ry={2} fill="#FCA5A5" />
          <line x1={0} y1={-12} x2={2} y2={-18} stroke="#78350F" strokeWidth={2.5} strokeLinecap="round" />
          <path d="M 1 -14 Q 8 -20 12 -15 Q 7 -11 1 -14 Z" fill="#22C55E" />
        </g>
      );

    case 'kinh_lup':
      return (
        <g transform={`translate(${x}, ${y}) scale(${dir}, 1) rotate(-24)`}>
          <line x1={0} y1={4} x2={16} y2={-14} stroke="#78350F" strokeWidth={6} strokeLinecap="round" />
          <circle cx={26} cy={-24} r={15} fill="#BAE6FD" fillOpacity={0.55} stroke="#334155" strokeWidth={4} />
          <path d="M 19 -30 Q 25 -34 31 -28" fill="none" stroke="#FFFFFF" strokeWidth={2.5} strokeLinecap="round" />
        </g>
      );

    case 'but_long_ngong':
      return (
        <g transform={`translate(${x}, ${y}) scale(${dir}, 1) rotate(-20)`}>
          <path d="M -2 6 L 26 -34 Q 32 -16 14 -4 Q 6 2 -2 6 Z" fill="#FFFBEB" stroke="#64748B" strokeWidth={2} />
          <line x1={-4} y1={9} x2={25} y2={-32} stroke="#D97706" strokeWidth={2.4} strokeLinecap="round" />
        </g>
      );

    case 'que_chi_bang':
      return (
        <g transform={`translate(${x}, ${y}) scale(${dir}, 1) rotate(-26)`}>
          <line x1={-6} y1={0} x2={72} y2={0} stroke="#1E293B" strokeWidth={6.5} strokeLinecap="round" />
          <line x1={-5} y1={0} x2={71} y2={0} stroke="#D97706" strokeWidth={3.5} strokeLinecap="round" />
          <circle cx={72} cy={0} r={4} fill="#EF4444" stroke="#1E293B" strokeWidth={1.5} />
        </g>
      );

    case 'den_long': {
      const chapChon = 0.8 + 0.2 * Math.sin(frame * 0.26);
      return (
        <g transform={`translate(${x + 6 * dir}, ${y + 8})`}>
          <circle cx={0} cy={14} r={34 * chapChon} fill="#FACC15" fillOpacity={0.18} />
          <line x1={0} y1={-8} x2={0} y2={2} stroke="#334155" strokeWidth={2.5} />
          <rect x={-11} y={2} width={22} height={24} rx={5} fill="#FEF08A" stroke="#78350F" strokeWidth={2.8} />
          <rect x={-14} y={0} width={28} height={5} rx={2} fill="#78350F" />
          <rect x={-14} y={24} width={28} height={5} rx={2} fill="#78350F" />
          <ellipse cx={0} cy={14} rx={4} ry={7} fill="#F97316" />
        </g>
      );
    }

    case 'ly_ca_phe': {
      const khoi1 = Math.sin(frame * 0.14) * 3;
      const khoi2 = Math.cos(frame * 0.14) * 3;
      return (
        <g transform={`translate(${x + 4 * dir}, ${y - 2}) scale(${dir}, 1)`}>
          {/* Khoi ca phe boc len theo duong cong sin */}
          <path
            d={`M -4 -14 Q ${-8 + khoi1} -24 -2 -32 Q ${4 - khoi1} -40 -2 -48`}
            fill="none"
            stroke="#FFFFFF"
            strokeOpacity={0.78}
            strokeWidth={2.4}
            strokeLinecap="round"
          />
          <path
            d={`M 5 -14 Q ${9 + khoi2} -23 4 -31 Q ${-2 - khoi2} -38 5 -45`}
            fill="none"
            stroke="#E2E8F0"
            strokeOpacity={0.72}
            strokeWidth={2.2}
            strokeLinecap="round"
          />
          {/* Than ly & quai cam */}
          <path d="M 10 -6 Q 20 -6 20 2 Q 20 9 10 9" fill="none" stroke="#1E293B" strokeWidth={3} />
          <rect x={-11} y={-11} width={22} height={24} rx={5} fill="#FFFFFF" stroke="#1E293B" strokeWidth={2.6} />
          <ellipse cx={0} cy={-11} rx={10} ry={3} fill="#78350F" />
        </g>
      );
    }

    default:
      return null;
  }
};

export const NguoiQueDong: React.FC<NguoiQueDongProps> = ({
  thongTin,
  trangThai,
  tiLe = 1,
  thoiLuongCanh,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const tongFrame = Math.max(1, thoiLuongCanh ?? durationInFrames);

  const dir = trangThai.huong === 'trai' ? -1 : 1;
  const xuong = tinhKhungXuongCoBan(trangThai.hanhDong, frame, trangThai.huong);
  const seedId = bamChuoiTatDinh(thongTin.id);

  const xHienTai =
    typeof trangThai.diChuyenDenX === 'number'
      ? interpolate(frame, [0, tongFrame], [trangThai.x, trangThai.diChuyenDenX], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        })
      : trangThai.x;

  const xTong = xHienTai + xuong.dichNgangNoiBo;
  const tiLeTong = tiLe * (trangThai.tiLe ?? 1);

  const mauNet = thongTin.mauThan || '#1E293B';
  const mauChuDao = thongTin.mauChuDao || '#2563EB';
  const mauDa = thongTin.mauDa ?? '#FFFDF7';

  // Bong do elip mem khong blur ngay duoi chan de nhan vat "dung dinh dat"
  const heSoBong = Math.max(0.55, 1 - xuong.doCaoNhay / 120);

  // Chieu rong bong bong thoai tu thich ung
  const doDaiChu = trangThai.bongBongThoai?.length ?? 0;
  const rongBongBong = Math.max(220, Math.min(440, doDaiChu * 11 + 56));

  return (
    <g transform={`translate(${xTong.toFixed(1)}, ${trangThai.y}) scale(${tiLeTong})`}>
      {/* Bong do elip mem (khong blur, fillOpacity: 0.22) */}
      <ellipse
        cx={xuong.hong.x}
        cy={4}
        rx={38 * heSoBong}
        ry={9 * heSoBong}
        fill="#0F172A"
        fillOpacity={0.22}
      />

      {/* Phu kien sau lung (ao choang / khan choang) */}
      {(thongTin.phuKien === 'ao_choang' || thongTin.phuKien === 'khan_choang') &&
        vePhuKien(
          thongTin.phuKien,
          xuong.dau.x,
          xuong.dau.y,
          xuong.co.x,
          xuong.co.y,
          dir,
          mauChuDao,
          frame,
        )}

      {/* Vien trang mong phia sau giup nhan vat noi bat sach se tren moi boi canh */}
      <g stroke="#FFFFFF" strokeOpacity={0.45} strokeWidth={13} strokeLinecap="round" strokeLinejoin="round" fill="none">
        <line x1={xuong.hong.x} y1={xuong.hong.y} x2={xuong.co.x} y2={xuong.co.y} />
        <polyline points={`${xuong.hong.x},${xuong.hong.y} ${xuong.goiTrai.x},${xuong.goiTrai.y} ${xuong.banChanTrai.x},${xuong.banChanTrai.y}`} />
        <polyline points={`${xuong.hong.x},${xuong.hong.y} ${xuong.goiPhai.x},${xuong.goiPhai.y} ${xuong.banChanPhai.x},${xuong.banChanPhai.y}`} />
        <polyline points={`${xuong.vaiTrai.x},${xuong.vaiTrai.y} ${xuong.khuyuTrai.x},${xuong.khuyuTrai.y} ${xuong.banTayTrai.x},${xuong.banTayTrai.y}`} />
        <polyline points={`${xuong.vaiPhai.x},${xuong.vaiPhai.y} ${xuong.khuyuPhai.x},${xuong.khuyuPhai.y} ${xuong.banTayPhai.x},${xuong.banTayPhai.y}`} />
      </g>

      {/* Than & tu chi nguoi que sac net */}
      <g stroke={mauNet} strokeWidth={8.5} strokeLinecap="round" strokeLinejoin="round" fill="none">
        <line x1={xuong.hong.x} y1={xuong.hong.y} x2={xuong.co.x} y2={xuong.co.y} />
        <polyline points={`${xuong.hong.x},${xuong.hong.y} ${xuong.goiTrai.x},${xuong.goiTrai.y} ${xuong.banChanTrai.x},${xuong.banChanTrai.y}`} />
        <polyline points={`${xuong.hong.x},${xuong.hong.y} ${xuong.goiPhai.x},${xuong.goiPhai.y} ${xuong.banChanPhai.x},${xuong.banChanPhai.y}`} />
        <polyline points={`${xuong.vaiTrai.x},${xuong.vaiTrai.y} ${xuong.khuyuTrai.x},${xuong.khuyuTrai.y} ${xuong.banTayTrai.x},${xuong.banTayTrai.y}`} />
        <polyline points={`${xuong.vaiPhai.x},${xuong.vaiPhai.y} ${xuong.khuyuPhai.x},${xuong.khuyuPhai.y} ${xuong.banTayPhai.x},${xuong.banTayPhai.y}`} />
      </g>

      {/* Dai nhan mau chu dao o co de phan biet nhan vat de dang */}
      <circle cx={xuong.co.x} cy={xuong.co.y + 4} r={5.5} fill={mauChuDao} stroke={mauNet} strokeWidth={2} />

      {/* Dau nhan vat xoay nhe theo gocDau */}
      <g transform={`translate(${xuong.dau.x.toFixed(1)}, ${xuong.dau.y.toFixed(1)}) rotate(${xuong.gocDau.toFixed(1)})`}>
        <circle cx={0} cy={0} r={25.5} fill={mauDa} stroke={mauNet} strokeWidth={6} />
        {veBieuCam(
          trangThai.bieuCam,
          dir,
          mauNet,
          Boolean(trangThai.dangNoi),
          frame,
          seedId,
        )}

        {/* Phu kien tren dau */}
        {thongTin.phuKien !== 'ao_choang' &&
          thongTin.phuKien !== 'khan_choang' &&
          vePhuKien(thongTin.phuKien, 0, 0, 0, 28, dir, mauChuDao, frame)}
      </g>

      {/* Vat cam tay */}
      {veVatCamTay(
        trangThai.vatCamTay,
        xuong.diemCamVat.x,
        xuong.diemCamVat.y,
        dir,
        frame,
      )}

      {/* The ten nhan vat gon dep duoi chan */}
      <g transform="translate(0, 34)">
        <rect
          x={-76}
          y={-17}
          width={152}
          height={28}
          rx={14}
          fill="#FFFDF7"
          fillOpacity={0.94}
          stroke={mauChuDao}
          strokeWidth={2.6}
        />
        <text
          x={0}
          y={2}
          textAnchor="middle"
          fill="#0F172A"
          fontSize={16}
          fontWeight={800}
          fontFamily="Segoe UI, Arial, sans-serif"
        >
          {thongTin.ten}
        </text>
      </g>

      {/* Bong bong thoai hoat hinh */}
      {trangThai.bongBongThoai && (
        <g transform={`translate(${xuong.dau.x + 22 * dir}, ${xuong.dau.y - 84})`}>
          <rect
            x={-rongBongBong / 2}
            y={-32}
            width={rongBongBong}
            height={56}
            rx={18}
            fill="#FFFFFF"
            stroke="#1E293B"
            strokeWidth={3.2}
          />
          <polygon points="-10,24 10,24 -3,39" fill="#FFFFFF" stroke="#1E293B" strokeWidth={2.6} strokeLinejoin="round" />
          <line x1={-8} y1={24} x2={8} y2={24} stroke="#FFFFFF" strokeWidth={4} />
          <text
            x={0}
            y={4}
            textAnchor="middle"
            fill="#0F172A"
            fontSize={18}
            fontWeight={700}
            fontFamily="Segoe UI, Arial, sans-serif"
          >
            {trangThai.bongBongThoai}
          </text>
        </g>
      )}
    </g>
  );
};
