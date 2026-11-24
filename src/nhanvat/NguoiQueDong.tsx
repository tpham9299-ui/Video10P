import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import type {
  LoaiBieuCam,
  LoaiPhuKien,
  LoaiVatCamTay,
  NhanVatTrongCanh,
  ThongTinNhanVat,
} from '../kieu_dai';
import {
  tinhKhungXuongCoBan,
  type Diem2D,
  type DoTrePhuKien,
} from '../xuong/he_xuong';
import {
  easeInOutSine,
  kepGiaTri,
  noiSuy,
  springTatDinh,
} from '../xuong/duong_cong';
import { bamChuoiTatDinh, bamTatDinh } from '../vfx/tat_dinh';

type NguoiQueDongProps = {
  thongTin: ThongTinNhanVat;
  trangThai: NhanVatTrongCanh;
  tiLe?: number;
  thoiLuongCanh?: number;
};

// Chu ky chop mat khong deu tu nhien (co xen nhip chop doi 34 frame)
const CHU_KY_CHOP_MAT = [74, 118, 62, 34, 108, 86];
const TONG_CHU_KY_CHOP = CHU_KY_CHOP_MAT.reduce((tong, v) => tong + v, 0);

/** Tinh muc khep mi mat tat dinh (0 = mo han, 1 = nham han) theo nhip khong deu tu nhien */
function tinhMucChopMat(frame: number, seedId: number): number {
  const fLech = ((frame + (seedId % TONG_CHU_KY_CHOP)) % TONG_CHU_KY_CHOP + TONG_CHU_KY_CHOP) % TONG_CHU_KY_CHOP;
  let moc = 0;
  for (const khoang of CHU_KY_CHOP_MAT) {
    moc += khoang;
    const cachMoc = moc - fLech;
    if (cachMoc >= 0 && cachMoc < 5) {
      // 5 frame chop muot: 0.45 -> 0.95 -> 1 -> 0.85 -> 0.35
      const bang = [0.35, 0.85, 1, 0.95, 0.45];
      return bang[Math.floor(cachMoc)] ?? 0;
    }
  }
  return 0;
}

/** Tinh cuong do lip-sync theo am tiet: 3 song sin lech tan so (0.42, 0.73, 1.17) + khoang ngat lay hoi */
function tinhCuongDoLipSync(frame: number, seedId: number): {
  cuongDo: number;
  khauHinh: 0 | 1 | 2 | 3;
} {
  // Khoang ngat lay hoi dinh ky: moi 74 frame nghi lay hoi 8 frame
  const phaHoi = ((frame + (seedId % 37)) % 74 + 74) % 74;
  if (phaHoi >= 66) {
    return { cuongDo: 0, khauHinh: 0 };
  }

  // Lam mem bien do ngay truoc/sau khi lay hoi
  const baoHoi =
    phaHoi < 3 ? phaHoi / 3 : phaHoi > 63 ? (66 - phaHoi) / 3 : 1;

  const song =
    0.46 * Math.sin(frame * 0.42 + (seedId % 19) * 0.31) +
    0.34 * Math.sin(frame * 0.73 + (seedId % 23) * 0.47 + 1.2) +
    0.2 * Math.sin(frame * 1.17 + (seedId % 29) * 0.23 + 2.5);

  const cuongDo = kepGiaTri(((song + 1) * 0.5) * baoHoi, 0, 1);

  if (cuongDo < 0.22) {
    return { cuongDo, khauHinh: 0 }; // Ngam
  }
  if (cuongDo < 0.48) {
    return { cuongDo, khauHinh: 1 }; // Mo nho
  }
  if (cuongDo < 0.72) {
    return { cuongDo, khauHinh: 2 }; // Tron chu O
  }
  return { cuongDo, khauHinh: 3 }; // Mo rong cuoi
}

/** Ve khuon mat hoat hinh voi lip-sync 4 khau hinh, anh mat liec nhe, chop mat tu nhien & long may nhun */
const veBieuCam = (
  bieuCam: LoaiBieuCam,
  dir: number,
  mauNet: string,
  dangNoi: boolean,
  frame: number,
  seedId: number,
  huongNhinX: number,
  huongNhinY: number,
) => {
  const matTraiX = 3 * dir;
  const matPhaiX = 12.5 * dir;
  const matY = -4;
  const miengX = 7.5 * dir;
  const miengY = 8.2;

  const lip = dangNoi ? tinhCuongDoLipSync(frame, seedId) : { cuongDo: 0, khauHinh: 0 as const };

  const mucChop =
    bieuCam === 'can_loi_mat_do' || bieuCam === 'ngac_nhien'
      ? 0
      : tinhMucChopMat(frame, seedId);
  const dangNhamMat = mucChop >= 0.75;

  // Con nguoi liec nhe theo huong nhin / bang + dao mat vi mo tat dinh
  const liecViMoX = Math.sin(frame * 0.055 + seedId * 0.17) * 0.65;
  const liecViMoY = Math.cos(frame * 0.043 + seedId * 0.29) * 0.35;
  const nguoiX = kepGiaTri((huongNhinX + liecViMoX) * dir, -2.1, 2.1);
  const nguoiY = kepGiaTri(huongNhinY + liecViMoY, -1.6, 1.6);

  // Long may nhun theo nhip noi va nhip tho
  const nhunMay = dangNoi
    ? -lip.cuongDo * 2.4 - Math.sin(frame * 0.24) * 0.6
    : Math.sin(frame * 0.09 + seedId * 0.1) * 0.45;
  const mayY = matY + nhunMay;

  const veMiengKhiNoi = () => {
    const laNghiem = bieuCam === 'tuc_gian' || bieuCam === 'hoang_mang';
    switch (lip.khauHinh) {
      case 0: // Ngam
        return laNghiem ? (
          <line
            x1={miengX - 4.8}
            y1={miengY + 0.6}
            x2={miengX + 4.8}
            y2={miengY + 0.6}
            stroke={mauNet}
            strokeWidth={2.4}
            strokeLinecap="round"
          />
        ) : (
          <path
            d={`M ${miengX - 5} ${miengY - 0.3} Q ${miengX} ${miengY + 3.2} ${miengX + 5} ${miengY - 0.3}`}
            fill="none"
            stroke={mauNet}
            strokeWidth={2.4}
            strokeLinecap="round"
          />
        );

      case 1: {
        // Mo nho
        const ry = noiSuy(2.2, 3.4, (lip.cuongDo - 0.22) / 0.26);
        return (
          <ellipse
            cx={miengX}
            cy={miengY + 0.4}
            rx={4.4}
            ry={ry}
            fill="#991B1B"
            stroke={mauNet}
            strokeWidth={2}
          />
        );
      }

      case 2: {
        // Tron chu O
        const ty = (lip.cuongDo - 0.48) / 0.24;
        const rx = noiSuy(3.9, 4.7, ty);
        const ry = noiSuy(4.5, 5.6, ty);
        return (
          <g>
            <ellipse
              cx={miengX}
              cy={miengY + 0.6}
              rx={rx}
              ry={ry}
              fill="#991B1B"
              stroke={mauNet}
              strokeWidth={2.1}
            />
            <ellipse
              cx={miengX}
              cy={miengY + 2.4}
              rx={rx * 0.52}
              ry={1.4}
              fill="#FB7185"
            />
          </g>
        );
      }

      case 3:
      default: {
        // Mo rong cuoi (D-shape song dong)
        const doMoRong = noiSuy(6.2, 8.2, (lip.cuongDo - 0.72) / 0.28);
        return laNghiem ? (
          <g>
            <ellipse
              cx={miengX}
              cy={miengY + 0.8}
              rx={5.8}
              ry={doMoRong * 0.68}
              fill="#991B1B"
              stroke={mauNet}
              strokeWidth={2.1}
            />
            <ellipse cx={miengX} cy={miengY + 2.8} rx={3.2} ry={1.5} fill="#FB7185" />
          </g>
        ) : (
          <g>
            <path
              d={`M ${miengX - 6.8} ${miengY - 1.8} Q ${miengX} ${miengY - 0.4} ${miengX + 6.8} ${miengY - 1.8} Q ${miengX + 5.8} ${miengY + doMoRong} ${miengX} ${miengY + doMoRong} Q ${miengX - 5.8} ${miengY + doMoRong} ${miengX - 6.8} ${miengY - 1.8} Z`}
              fill="#991B1B"
              stroke={mauNet}
              strokeWidth={2}
              strokeLinejoin="round"
            />
            {/* Vien rang tren nho gon */}
            <path
              d={`M ${miengX - 4.6} ${miengY - 1.2} Q ${miengX} ${miengY - 0.3} ${miengX + 4.6} ${miengY - 1.2}`}
              fill="none"
              stroke="#FFFFFF"
              strokeWidth={1.6}
              strokeLinecap="round"
            />
            {/* Luoi hong */}
            <ellipse cx={miengX} cy={miengY + doMoRong * 0.58} rx={3.4} ry={1.6} fill="#FB7185" />
          </g>
        );
      }
    }
  };

  return (
    <g>
      {/* Ma hong duyen dang cho bieu cam vui tuoi / tu man */}
      {(bieuCam === 'vui_tuoi' || bieuCam === 'tu_man') && (
        <>
          <ellipse cx={matTraiX - 4 * dir} cy={matY + 8} rx={4.2} ry={2.4} fill="#FB7185" fillOpacity={0.38} />
          <ellipse cx={matPhaiX + 4 * dir} cy={matY + 8} rx={4.2} ry={2.4} fill="#FB7185" fillOpacity={0.38} />
        </>
      )}

      {/* Long may bieu cam cho du 9 trang thai, nhun theo nhip noi */}
      {bieuCam === 'tuc_gian' && (
        <>
          <line x1={matTraiX - 4.2} y1={mayY - 8.2} x2={matTraiX + 4.6} y2={mayY - 4.4} stroke={mauNet} strokeWidth={2.6} strokeLinecap="round" />
          <line x1={matPhaiX - 4.6} y1={mayY - 4.4} x2={matPhaiX + 4.2} y2={mayY - 8.2} stroke={mauNet} strokeWidth={2.6} strokeLinecap="round" />
        </>
      )}
      {bieuCam === 'ngac_nhien' && (
        <>
          <path d={`M ${matTraiX - 4.2} ${mayY - 9.5} Q ${matTraiX} ${mayY - 13} ${matTraiX + 4.2} ${mayY - 9.5}`} fill="none" stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
          <path d={`M ${matPhaiX - 4.2} ${mayY - 9.5} Q ${matPhaiX} ${mayY - 13} ${matPhaiX + 4.2} ${mayY - 9.5}`} fill="none" stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
        </>
      )}
      {bieuCam === 'hoang_mang' && (
        <>
          <line x1={matTraiX - 4.5} y1={mayY - 6} x2={matTraiX + 4} y2={mayY - 9.8} stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
          <line x1={matPhaiX - 4} y1={mayY - 9.8} x2={matPhaiX + 4.5} y2={mayY - 6} stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
        </>
      )}
      {bieuCam === 'tinh_quai' && (
        <>
          <line x1={matTraiX - 4} y1={mayY - 9} x2={matTraiX + 4} y2={mayY - 6} stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
          <path d={`M ${matPhaiX - 4} ${mayY - 9.2} Q ${matPhaiX} ${mayY - 12.6} ${matPhaiX + 4} ${mayY - 8}`} fill="none" stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
        </>
      )}
      {bieuCam === 'tram_tu' && (
        <>
          <line x1={matTraiX - 4} y1={mayY - 7.4} x2={matTraiX + 4} y2={mayY - 7.4} stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
          <line x1={matPhaiX - 4} y1={mayY - 9} x2={matPhaiX + 4} y2={mayY - 6.8} stroke={mauNet} strokeWidth={2.2} strokeLinecap="round" />
        </>
      )}
      {bieuCam === 'tu_man' && (
        <>
          <path d={`M ${matTraiX - 4} ${mayY - 8.2} Q ${matTraiX} ${mayY - 11.8} ${matTraiX + 4} ${mayY - 8.2}`} fill="none" stroke={mauNet} strokeWidth={2.4} strokeLinecap="round" />
          <line x1={matPhaiX - 4} y1={mayY - 7} x2={matPhaiX + 4} y2={mayY - 9.8} stroke={mauNet} strokeWidth={2.4} strokeLinecap="round" />
        </>
      )}
      {bieuCam === 'can_loi_mat_do' && (
        <>
          <line x1={matTraiX - 4} y1={mayY - 5.2} x2={matTraiX + 4} y2={mayY - 5.2} stroke={mauNet} strokeWidth={2} strokeLinecap="round" />
          <line x1={matPhaiX - 4} y1={mayY - 5.2} x2={matPhaiX + 4} y2={mayY - 5.2} stroke={mauNet} strokeWidth={2} strokeLinecap="round" />
        </>
      )}
      {(bieuCam === 'binh_thuong' || bieuCam === 'vui_tuoi') && (
        <>
          <path d={`M ${matTraiX - 3.6} ${mayY - 7.8} Q ${matTraiX} ${mayY - 10} ${matTraiX + 3.6} ${mayY - 7.8}`} fill="none" stroke={mauNet} strokeWidth={2} strokeLinecap="round" />
          <path d={`M ${matPhaiX - 3.6} ${mayY - 7.8} Q ${matPhaiX} ${mayY - 10} ${matPhaiX + 3.6} ${mayY - 7.8}`} fill="none" stroke={mauNet} strokeWidth={2} strokeLinecap="round" />
        </>
      )}

      {/* Doi mat co hon: chop mat khong deu tu nhien + con nguoi liec theo huong nhin */}
      {bieuCam === 'can_loi_mat_do' ? (
        <>
          <line x1={matTraiX - 3.4} y1={matY} x2={matTraiX + 3.4} y2={matY} stroke={mauNet} strokeWidth={3} strokeLinecap="round" />
          <line x1={matPhaiX - 3.4} y1={matY} x2={matPhaiX + 3.4} y2={matY} stroke={mauNet} strokeWidth={3} strokeLinecap="round" />
        </>
      ) : dangNhamMat ? (
        <>
          <path d={`M ${matTraiX - 4} ${matY} Q ${matTraiX} ${matY + 2.8} ${matTraiX + 4} ${matY}`} fill="none" stroke={mauNet} strokeWidth={2.5} strokeLinecap="round" />
          <path d={`M ${matPhaiX - 4} ${matY} Q ${matPhaiX} ${matY + 2.8} ${matPhaiX + 4} ${matY}`} fill="none" stroke={mauNet} strokeWidth={2.5} strokeLinecap="round" />
        </>
      ) : bieuCam === 'vui_tuoi' ? (
        <>
          <path d={`M ${matTraiX - 3.8} ${matY + 1.2} Q ${matTraiX} ${matY - 4.4} ${matTraiX + 3.8} ${matY + 1.2}`} fill="none" stroke={mauNet} strokeWidth={2.8} strokeLinecap="round" />
          <path d={`M ${matPhaiX - 3.8} ${matY + 1.2} Q ${matPhaiX} ${matY - 4.4} ${matPhaiX + 3.8} ${matY + 1.2}`} fill="none" stroke={mauNet} strokeWidth={2.8} strokeLinecap="round" />
        </>
      ) : bieuCam === 'ngac_nhien' || bieuCam === 'hoang_mang' ? (
        <>
          <circle cx={matTraiX} cy={matY} r={4.5} fill="#FFFFFF" stroke={mauNet} strokeWidth={2.2} />
          <circle cx={matPhaiX} cy={matY} r={4.5} fill="#FFFFFF" stroke={mauNet} strokeWidth={2.2} />
          <circle cx={matTraiX + nguoiX * 0.7} cy={matY + nguoiY * 0.7} r={1.8} fill={mauNet} />
          <circle cx={matPhaiX + nguoiX * 0.7} cy={matY + nguoiY * 0.7} r={1.8} fill={mauNet} />
          <circle cx={matTraiX + nguoiX * 0.7 - 0.7} cy={matY + nguoiY * 0.7 - 0.7} r={0.7} fill="#FFFFFF" />
          <circle cx={matPhaiX + nguoiX * 0.7 - 0.7} cy={matY + nguoiY * 0.7 - 0.7} r={0.7} fill="#FFFFFF" />
        </>
      ) : bieuCam === 'tu_man' ? (
        <>
          <ellipse cx={matTraiX} cy={matY + 0.8} rx={3.6} ry={2.4 * (1 - mucChop * 0.6)} fill="#FFFFFF" stroke={mauNet} strokeWidth={1.8} />
          <ellipse cx={matPhaiX} cy={matY + 0.8} rx={3.6} ry={2.4 * (1 - mucChop * 0.6)} fill="#FFFFFF" stroke={mauNet} strokeWidth={1.8} />
          <circle cx={matTraiX + nguoiX * 0.55} cy={matY + 1 + nguoiY * 0.4} r={1.8} fill={mauNet} />
          <circle cx={matPhaiX + nguoiX * 0.55} cy={matY + 1 + nguoiY * 0.4} r={1.8} fill={mauNet} />
          <line x1={matTraiX - 4.2} y1={matY - 1.4} x2={matTraiX + 4.2} y2={matY - 1.4} stroke={mauNet} strokeWidth={2.6} strokeLinecap="round" />
          <line x1={matPhaiX - 4.2} y1={matY - 1.4} x2={matPhaiX + 4.2} y2={matY - 1.4} stroke={mauNet} strokeWidth={2.6} strokeLinecap="round" />
        </>
      ) : (
        <>
          {/* Mat trong trang + con nguoi liec mem + dom sang co hon */}
          <ellipse cx={matTraiX} cy={matY} rx={3.7} ry={Math.max(1.2, 4.1 * (1 - mucChop * 0.7))} fill="#FFFFFF" stroke={mauNet} strokeWidth={1.8} />
          <ellipse cx={matPhaiX} cy={matY} rx={3.7} ry={Math.max(1.2, 4.1 * (1 - mucChop * 0.7))} fill="#FFFFFF" stroke={mauNet} strokeWidth={1.8} />
          <circle cx={matTraiX + nguoiX * 0.65} cy={matY + nguoiY * 0.65} r={2.1} fill={mauNet} />
          <circle cx={matPhaiX + nguoiX * 0.65} cy={matY + nguoiY * 0.65} r={2.1} fill={mauNet} />
          <circle cx={matTraiX + nguoiX * 0.65 - 0.8} cy={matY + nguoiY * 0.65 - 0.9} r={0.85} fill="#FFFFFF" />
          <circle cx={matPhaiX + nguoiX * 0.65 - 0.8} cy={matY + nguoiY * 0.65 - 0.9} r={0.85} fill="#FFFFFF" />
        </>
      )}

      {/* Mieng: lip-sync 4 khau hinh khi dangNoi, hoac 9 bieu cam sac net */}
      {dangNoi ? (
        veMiengKhiNoi()
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

/** 8 phu kien nhan vat sac net, co chuyen dong thu cap tre theo quan tinh (doTrePhuKien & vanTocThan) */
const vePhuKien = (
  phuKien: LoaiPhuKien,
  dauX: number,
  dauY: number,
  coX: number,
  coY: number,
  dir: number,
  mauChuDao: string,
  frame: number,
  doTre: DoTrePhuKien,
  vanToc: Diem2D,
) => {
  const gio1 = Math.sin(frame * 0.16) * 5;
  const gio2 = Math.cos(frame * 0.14) * 4;
  // Quan tinh bay nguoc chieu di chuyen + do tre tu frame - 3
  const bayX = kepGiaTri(doTre.dx * 1.15 - vanToc.x * 2.4, -26, 26);
  const bayY = kepGiaTri(doTre.dy * 0.9 - vanToc.y * 1.8, -18, 18);
  const lacGoc = kepGiaTri(doTre.gocTre * 0.75 - vanToc.x * 1.1, -16, 16);

  switch (phuKien) {
    case 'vong_nguyet_que':
      return (
        <g transform={`translate(${dauX}, ${dauY - 20}) rotate(${(lacGoc * 0.25).toFixed(1)})`}>
          <path d="M -22 5 Q 0 -9 22 5" fill="none" stroke="#B45309" strokeWidth={3.2} strokeLinecap="round" />
          {[-18, -11, -4, 4, 11, 18].map((lx, idx) => {
            const rungLa = Math.sin(frame * 0.2 + idx * 0.9) * 2.2 + lacGoc * 0.35;
            const goc = (idx < 3 ? -32 + idx * 10 : 32 - (5 - idx) * 10) + rungLa;
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
                transform={`rotate(${goc.toFixed(1)}, ${lx}, ${ly})`}
              />
            );
          })}
          <circle cx={0} cy={-4} r={3.5} fill="#FACC15" stroke="#854D0E" strokeWidth={1.2} />
        </g>
      );

    case 'toc_gia_17': {
      // Lon toc ben dung dua va tre nhip theo quan tinh quay dau/di chuyen
      const lonDX = kepGiaTri(bayX * 0.28 + doTre.doRung * 1.4, -7, 7);
      const lonDY = kepGiaTri(bayY * 0.22, -5, 5);
      return (
        <g transform={`translate(${dauX}, ${dauY}) rotate(${(lacGoc * 0.28).toFixed(1)})`}>
          <path
            d={`M ${-26 + lonDX * 0.6} ${14 + lonDY} Q -32 -12 -18 -26 Q 0 -33 18 -26 Q 32 -12 ${26 + lonDX * 0.6} ${14 + lonDY} Q 20 ${22 + lonDY} 15 14 Q 21 -6 14 -16 Q 0 -22 -14 -16 Q -21 -6 -15 14 Q -20 ${22 + lonDY} ${-26 + lonDX * 0.6} ${14 + lonDY} Z`}
            fill="#F1F5F9"
            stroke="#64748B"
            strokeWidth={2.2}
          />
          <circle cx={-23 + lonDX * 0.5} cy={-3 + lonDY * 0.4} r={7} fill="#FFFFFF" stroke="#94A3B8" strokeWidth={1.6} />
          <circle cx={-23 + lonDX} cy={8 + lonDY} r={6.5} fill="#E2E8F0" stroke="#94A3B8" strokeWidth={1.6} />
          <circle cx={23 + lonDX * 0.5} cy={-3 + lonDY * 0.4} r={7} fill="#FFFFFF" stroke="#94A3B8" strokeWidth={1.6} />
          <circle cx={23 + lonDX} cy={8 + lonDY} r={6.5} fill="#E2E8F0" stroke="#94A3B8" strokeWidth={1.6} />
        </g>
      );
    }

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

    case 'mu_noi_phap': {
      // Chop mu noi Phap lac mem theo quan tinh
      const chopX = 2 * dir + kepGiaTri(bayX * 0.35 + doTre.doRung * 1.2, -9, 9);
      const chopY = -17 + kepGiaTri(bayY * 0.25, -5, 5);
      return (
        <g transform={`translate(${dauX - 2 * dir}, ${dauY - 22}) rotate(${(-10 * dir + lacGoc * 0.35).toFixed(1)})`}>
          <ellipse cx={0} cy={0} rx={24} ry={10} fill={mauChuDao} stroke="#1E293B" strokeWidth={2.5} />
          <path
            d={`M 0 -10 Q ${(chopX * 0.5).toFixed(1)} -14 ${chopX.toFixed(1)} ${chopY.toFixed(1)}`}
            fill="none"
            stroke="#1E293B"
            strokeWidth={3.2}
            strokeLinecap="round"
          />
        </g>
      );
    }

    case 'mu_tham_tu':
      return (
        <g transform={`translate(${dauX}, ${dauY - 20}) rotate(${(lacGoc * 0.22).toFixed(1)})`}>
          <path d="M -28 2 Q 0 -2 28 2 Q 0 9 -28 2 Z" fill="#92400E" stroke="#1E293B" strokeWidth={2.2} />
          <path d="M -18 0 Q -14 -20 0 -20 Q 14 -20 18 0 Z" fill="#B45309" stroke="#1E293B" strokeWidth={2.2} />
          <line x1={-16} y1={-5} x2={16} y2={-5} stroke="#78350F" strokeWidth={3.5} />
        </g>
      );

    case 'ao_choang': {
      // Ta ao choang phap phoi nguoc huong di chuyen va do tre tu frame - 3
      const duoiNgoaiX = coX - (46 + gio1) * dir + bayX * 1.1;
      const duoiNgoaiY = coY + 90 + bayY * 0.7 - Math.abs(bayX) * 0.35;
      const duoiTrongX = coX - (15 + gio2 * 0.5) * dir + bayX * 0.65;
      const duoiTrongY = coY + 86 + bayY * 0.5;
      const uonX = coX - 22 * dir + bayX * 0.55;
      const uonY = coY + 44 + bayY * 0.35;
      return (
        <g>
          <path
            d={`M ${coX.toFixed(1)} ${(coY + 2).toFixed(1)} Q ${uonX.toFixed(1)} ${uonY.toFixed(1)} ${duoiNgoaiX.toFixed(1)} ${duoiNgoaiY.toFixed(1)} L ${duoiTrongX.toFixed(1)} ${duoiTrongY.toFixed(1)} Q ${(coX - 6 * dir + bayX * 0.25).toFixed(1)} ${(coY + 42).toFixed(1)} ${(coX + 4 * dir).toFixed(1)} ${(coY + 4).toFixed(1)} Z`}
            fill={mauChuDao}
            stroke="#1E293B"
            strokeWidth={2.8}
            strokeLinejoin="round"
          />
          <circle cx={coX + 2 * dir} cy={coY + 4} r={4.5} fill="#FACC15" stroke="#1E293B" strokeWidth={1.6} />
        </g>
      );
    }

    case 'khan_choang': {
      // Dai khan choang luon song va keo nguoc theo quan tinh
      const giuaX = coX - 28 * dir + bayX * 0.65;
      const giuaY = coY + 14 + gio1 + bayY * 0.55;
      const cuoiX = coX - (58 - gio2) * dir + bayX * 1.2;
      const cuoiY = coY + 4 + gio1 * 0.8 + bayY * 0.9;
      const d = `M ${(coX - 2 * dir).toFixed(1)} ${(coY + 4).toFixed(1)} Q ${giuaX.toFixed(1)} ${giuaY.toFixed(1)} ${cuoiX.toFixed(1)} ${cuoiY.toFixed(1)}`;
      return (
        <g>
          <path d={d} fill="none" stroke="#1E293B" strokeWidth={12} strokeLinecap="round" />
          <path d={d} fill="none" stroke={mauChuDao} strokeWidth={7.5} strokeLinecap="round" />
          <rect x={coX - 12} y={coY - 2} width={24} height={11} rx={5} fill={mauChuDao} stroke="#1E293B" strokeWidth={2.2} />
        </g>
      );
    }

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
  gocCangTay: number,
) => {
  if (!vat || vat === 'khong') {
    return null;
  }

  // Nghieng nhe vat cam tay theo chuyen dong cang tay (co gioi han de luon dep mat)
  const nghiengMem = kepGiaTri((gocCangTay * dir - 90) * 0.16, -16, 16);

  switch (vat) {
    case 'cuon_giay':
      return (
        <g transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)}) scale(${dir}, 1) rotate(${(-14 + nghiengMem * 0.5).toFixed(1)})`}>
          <rect x={-6} y={-24} width={28} height={38} rx={5} fill="#FEF3C7" stroke="#92400E" strokeWidth={2.5} />
          <ellipse cx={8} cy={-24} rx={14} ry={4.5} fill="#FDE68A" stroke="#92400E" strokeWidth={2} />
          <line x1={0} y1={-12} x2={16} y2={-12} stroke="#92400E" strokeWidth={2} strokeLinecap="round" />
          <line x1={0} y1={-4} x2={14} y2={-4} stroke="#92400E" strokeWidth={2} strokeLinecap="round" />
          <line x1={0} y1={4} x2={15} y2={4} stroke="#92400E" strokeWidth={2} strokeLinecap="round" />
        </g>
      );

    case 'qua_tao':
      return (
        <g transform={`translate(${(x + 4 * dir).toFixed(1)}, ${(y - 6).toFixed(1)})`}>
          <circle cx={0} cy={0} r={12.5} fill="#EF4444" stroke="#7F1D1D" strokeWidth={2.2} />
          <ellipse cx={-3.5} cy={-3.5} rx={3.5} ry={2} fill="#FCA5A5" />
          <line x1={0} y1={-12} x2={2} y2={-18} stroke="#78350F" strokeWidth={2.5} strokeLinecap="round" />
          <path d="M 1 -14 Q 8 -20 12 -15 Q 7 -11 1 -14 Z" fill="#22C55E" />
        </g>
      );

    case 'kinh_lup':
      return (
        <g transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)}) scale(${dir}, 1) rotate(${(-24 + nghiengMem).toFixed(1)})`}>
          <line x1={0} y1={4} x2={16} y2={-14} stroke="#78350F" strokeWidth={6} strokeLinecap="round" />
          <circle cx={26} cy={-24} r={15} fill="#BAE6FD" fillOpacity={0.55} stroke="#334155" strokeWidth={4} />
          <path d="M 19 -30 Q 25 -34 31 -28" fill="none" stroke="#FFFFFF" strokeWidth={2.5} strokeLinecap="round" />
        </g>
      );

    case 'but_long_ngong':
      return (
        <g transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)}) scale(${dir}, 1) rotate(${(-20 + nghiengMem).toFixed(1)})`}>
          <path d="M -2 6 L 26 -34 Q 32 -16 14 -4 Q 6 2 -2 6 Z" fill="#FFFBEB" stroke="#64748B" strokeWidth={2} />
          <line x1={-4} y1={9} x2={25} y2={-32} stroke="#D97706" strokeWidth={2.4} strokeLinecap="round" />
        </g>
      );

    case 'que_chi_bang':
      return (
        <g transform={`translate(${x.toFixed(1)}, ${y.toFixed(1)}) scale(${dir}, 1) rotate(${(-22 - nghiengMem * 1.2).toFixed(1)})`}>
          <line x1={-6} y1={0} x2={74} y2={0} stroke="#1E293B" strokeWidth={6.5} strokeLinecap="round" />
          <line x1={-5} y1={0} x2={73} y2={0} stroke="#D97706" strokeWidth={3.5} strokeLinecap="round" />
          <circle cx={74} cy={0} r={4.2} fill="#EF4444" stroke="#1E293B" strokeWidth={1.5} />
        </g>
      );

    case 'den_long': {
      const chapChon = 0.8 + 0.2 * Math.sin(frame * 0.26);
      return (
        <g transform={`translate(${(x + 6 * dir).toFixed(1)}, ${(y + 8).toFixed(1)})`}>
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
        <g transform={`translate(${(x + 4 * dir).toFixed(1)}, ${(y - 2).toFixed(1)}) scale(${dir}, 1)`}>
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

/** Vet bui nho duoi got chan khi chay voi va / bat nhay dap dat (tat dinh 100%) */
const veVetBuiDuoiGot = (frame: number, dir: number, seedId: number) => {
  return (
    <g pointerEvents="none">
      {[0, 1, 2, 3].map((i) => {
        const pha = ((frame + i * 4 + (seedId % 7)) % 14) / 14;
        const dx = (-16 - pha * 48 - bamTatDinh(seedId + i * 11) * 14) * dir;
        const dy = -4 - pha * 16 - (i % 2) * 5;
        const r = (5 + (i % 3) * 2.5) * (0.6 + pha * 0.75);
        const op = Math.max(0, (1 - pha) * 0.72);
        return (
          <circle
            key={`bui-chay-${i}`}
            cx={dx.toFixed(1)}
            cy={dy.toFixed(1)}
            r={r.toFixed(1)}
            fill="#F8FAFC"
            stroke="#CBD5E1"
            strokeWidth={1.6}
            fillOpacity={op}
            strokeOpacity={op}
          />
        );
      })}
    </g>
  );
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
  const seedId = bamChuoiTatDinh(thongTin.id);

  // Tinh vi tri ngang muot & van toc di chuyen cho chuyen dong thu cap phu kien
  let xHienTai = trangThai.x;
  let vanTocDiChuyenX = 0;
  if (typeof trangThai.diChuyenDenX === 'number') {
    const t0 = easeInOutSine(kepGiaTri(frame / tongFrame, 0, 1));
    const tTruoc = easeInOutSine(kepGiaTri((frame - 1) / tongFrame, 0, 1));
    xHienTai = noiSuy(trangThai.x, trangThai.diChuyenDenX, t0);
    const xTruoc = noiSuy(trangThai.x, trangThai.diChuyenDenX, tTruoc);
    vanTocDiChuyenX = xHienTai - xTruoc;
  }

  const xuong = tinhKhungXuongCoBan(trangThai.hanhDong, frame, trangThai.huong, {
    dangNoi: Boolean(trangThai.dangNoi),
    vanTocDiChuyenX,
  });

  const xTong = xHienTai + xuong.dichNgangNoiBo;
  const tiLeTong = tiLe * (trangThai.tiLe ?? 1);

  const mauNet = thongTin.mauThan || '#1E293B';
  const mauChuDao = thongTin.mauChuDao || '#2563EB';
  const mauDa = thongTin.mauDa ?? '#FFFDF7';

  // Bong do elip duoi chan tu co nho va nhat dan khi nhan vat nhay len cao (offsetY < 0)
  const doCaoBay = Math.max(xuong.doCaoNhay, Math.max(0, -xuong.offsetY));
  const heSoBong = kepGiaTri(1 - doCaoBay / 130, 0.36, 1.08);
  const doMoBong = kepGiaTri(0.24 * (1 - doCaoBay / 150), 0.06, 0.28);

  // Duong cong mem <path> cho cot song va 4 chi qua diem dieu khien khuyu/goi
  const dThan = `M ${xuong.hong.x.toFixed(1)} ${xuong.hong.y.toFixed(1)} Q ${xuong.diemUonThan.x.toFixed(1)} ${xuong.diemUonThan.y.toFixed(1)} ${xuong.co.x.toFixed(1)} ${xuong.co.y.toFixed(1)}`;
  const dChanTrai = `M ${xuong.hong.x.toFixed(1)} ${xuong.hong.y.toFixed(1)} Q ${xuong.goiTrai.x.toFixed(1)} ${xuong.goiTrai.y.toFixed(1)} ${xuong.banChanTrai.x.toFixed(1)} ${xuong.banChanTrai.y.toFixed(1)}`;
  const dChanPhai = `M ${xuong.hong.x.toFixed(1)} ${xuong.hong.y.toFixed(1)} Q ${xuong.goiPhai.x.toFixed(1)} ${xuong.goiPhai.y.toFixed(1)} ${xuong.banChanPhai.x.toFixed(1)} ${xuong.banChanPhai.y.toFixed(1)}`;
  const dTayTrai = `M ${xuong.vaiTrai.x.toFixed(1)} ${xuong.vaiTrai.y.toFixed(1)} Q ${xuong.khuyuTrai.x.toFixed(1)} ${xuong.khuyuTrai.y.toFixed(1)} ${xuong.banTayTrai.x.toFixed(1)} ${xuong.banTayTrai.y.toFixed(1)}`;
  const dTayPhai = `M ${xuong.vaiPhai.x.toFixed(1)} ${xuong.vaiPhai.y.toFixed(1)} Q ${xuong.khuyuPhai.x.toFixed(1)} ${xuong.khuyuPhai.y.toFixed(1)} ${xuong.banTayPhai.x.toFixed(1)} ${xuong.banTayPhai.y.toFixed(1)}`;

  // Co gian dau nhe theo squash & stretch de tang cam giac hoat hinh dan hoi
  const dauScaleX = 1 + (xuong.squashX - 1) * 0.42;
  const dauScaleY = 1 + (xuong.squashY - 1) * 0.42;

  // Bong bong thoai bat ra bang lo xo springTatDinh
  const doDaiChu = trangThai.bongBongThoai?.length ?? 0;
  const rongBongBong = Math.max(220, Math.min(440, doDaiChu * 11 + 56));
  const loXoThoai = springTatDinh(frame - 2, 11, 210);
  const tiLeThoai = kepGiaTri(loXoThoai, 0, 1.25);
  const nhunThoaiY = Math.sin(frame * 0.1) * 2.2;

  return (
    <g transform={`translate(${xTong.toFixed(1)}, ${trangThai.y}) scale(${tiLeTong})`}>
      {/* Bong do elip duoi chan (tu co nho & nhat dan khi nhay cao, khong blur) */}
      <ellipse
        cx={xuong.hong.x}
        cy={4}
        rx={38 * heSoBong}
        ry={9 * heSoBong}
        fill="#0F172A"
        fillOpacity={doMoBong}
      />

      {/* Vet bui nho duoi got chan khi chay voi va / bat nhay dap dat */}
      {xuong.coVetBui && veVetBuiDuoiGot(frame, dir, seedId)}

      {/* Phu kien sau lung (ao choang / khan choang) co do tre quan tinh */}
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
          xuong.doTrePhuKien,
          xuong.vanTocThan,
        )}

      {/* Vien trang mong phia sau giup nhan vat noi bat sach se tren moi boi canh */}
      <g stroke="#FFFFFF" strokeOpacity={0.48} strokeWidth={13} strokeLinecap="round" strokeLinejoin="round" fill="none">
        <path d={dThan} />
        <path d={dChanTrai} />
        <path d={dChanPhai} />
        <path d={dTayTrai} />
        <path d={dTayPhai} />
      </g>

      {/* Than & tu chi nguoi que cong mem mai bang <path> */}
      <g stroke={mauNet} strokeWidth={8.5} strokeLinecap="round" strokeLinejoin="round" fill="none">
        <path d={dChanTrai} />
        <path d={dTayTrai} />
        <path d={dThan} />
        <path d={dChanPhai} />
        <path d={dTayPhai} />
      </g>

      {/* Dai nhan mau chu dao o co */}
      <circle cx={xuong.co.x} cy={xuong.co.y + 4} r={5.5} fill={mauChuDao} stroke={mauNet} strokeWidth={2} />

      {/* Dau nhan vat xoay nhe theo gocDau + co gian dan hoi */}
      <g
        transform={`translate(${xuong.dau.x.toFixed(1)}, ${xuong.dau.y.toFixed(1)}) rotate(${xuong.gocDau.toFixed(1)}) scale(${dauScaleX.toFixed(3)}, ${dauScaleY.toFixed(3)})`}
      >
        <circle cx={0} cy={0} r={25.5} fill={mauDa} stroke={mauNet} strokeWidth={6} />
        {veBieuCam(
          trangThai.bieuCam,
          dir,
          mauNet,
          Boolean(trangThai.dangNoi),
          frame,
          seedId,
          xuong.huongNhinX,
          xuong.huongNhinY,
        )}

        {/* Phu kien tren dau */}
        {thongTin.phuKien !== 'ao_choang' &&
          thongTin.phuKien !== 'khan_choang' &&
          vePhuKien(
            thongTin.phuKien,
            0,
            0,
            0,
            28,
            dir,
            mauChuDao,
            frame,
            xuong.doTrePhuKien,
            xuong.vanTocThan,
          )}
      </g>

      {/* Vat cam tay */}
      {veVatCamTay(
        trangThai.vatCamTay,
        xuong.diemCamVat.x,
        xuong.diemCamVat.y,
        dir,
        frame,
        xuong.gocCangTayPhai,
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

      {/* Bong bong thoai hoat hinh bat ra bang lo xo springTatDinh */}
      {trangThai.bongBongThoai && tiLeThoai > 0.01 && (
        <g
          transform={`translate(${(xuong.dau.x + 22 * dir).toFixed(1)}, ${(xuong.dau.y - 84 + nhunThoaiY).toFixed(1)}) scale(${tiLeThoai.toFixed(3)})`}
        >
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
