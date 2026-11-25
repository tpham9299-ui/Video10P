import React from 'react';
import { useCurrentFrame, useVideoConfig } from 'remotion';
import type {
  AnhSangMoiTruong,
  DoTuoiNhanVat,
  LoaiBieuCam,
  LoaiPhuKien,
  LoaiVatCamTay,
  NhanVatTrongCanh,
  ThongTinNhanVat,
  TuTheNhanVat,
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
} from '../xuong/duong_cong';
import { bamChuoiTatDinh, bamTatDinh } from '../vfx/tat_dinh';
import {
  HUD_BOTTOM_SAFE,
  useAnhSangMoiTruong,
  useCameraParallax,
} from '../vfx/MayQuayDong';
import { tinhLipSyncChoFrame } from './lip_sync';
import { tinhThongSoHopTen } from './ten_nhan_vat';
import { BongBongChat } from '../canh/BongBongChat';
import {
  giaiBieuCamTheoMoc,
  tinhHuongNhinTuongTac,
  type TrangThaiNhanVatDaGiai,
} from './dien_xuat';
import {
  MAU_MUC_TRUYEN_TRANH,
  giaiTrangPhucHieuLuc,
  tinhBongTiepDat,
  tinhThamSoAnhSangNhanVat,
  tinhTiLeTamKhung,
} from './hoa_trang_va_anh_sang';
import {
  veCanhTayMacAo,
  veChanMacQuan,
  veKieuTocNhanVat,
  veRauNhanVat,
  veTrangPhucThan,
} from './TrangPhucVaToc';

type NguoiQueDongProps = {
  thongTin: ThongTinNhanVat;
  trangThai: NhanVatTrongCanh | TrangThaiNhanVatDaGiai;
  tiLe?: number;
  thoiLuongCanh?: number;
  bienDoAmThanh?: readonly number[];
  /** Ep nhin thang vao ong kinh (canh tuong_tac_khan_gia) */
  nhinThangOngKinh?: boolean;
  /** Danh sach nhan vat cung canh (tuy chon, de tu tinh tuongTacVoi khi goi truc tiep) */
  danhSachNhanVatTrongCanh?: readonly NhanVatTrongCanh[];
  /** Thong so anh sang moi truong tu canh (v3.0, neu bo trong tu doc tu AnhSangCanhContext) */
  anhSangMoiTruong?: AnhSangMoiTruong;
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

/** Ve khuon mat hoat hinh voi lip-sync 4 khau hinh (uu tien bien do RMS that, fallback tat dinh), anh mat liec nhe / nhin thang ong kinh, chop mat tu nhien & long may nhun */
const veBieuCam = (
  bieuCam: LoaiBieuCam,
  dir: number,
  mauNet: string,
  dangNoi: boolean,
  frame: number,
  seedId: number,
  huongNhinX: number,
  huongNhinY: number,
  bienDoAmThanh?: readonly number[],
  nhinThangOngKinh = false,
  laSoSinh = false,
) => {
  const matTraiX = nhinThangOngKinh ? -7.5 : 3 * dir;
  const matPhaiX = nhinThangOngKinh ? 7.5 : 12.5 * dir;
  const matY = laSoSinh ? -3 : -4;
  const miengX = nhinThangOngKinh ? 0 : 7.5 * dir;
  const miengY = laSoSinh ? 8.6 : 8.2;

  const lip = dangNoi
    ? tinhLipSyncChoFrame(frame, seedId, bienDoAmThanh)
    : { cuongDo: 0, khauHinh: 0 as const, nguon: 'du_phong' as const };

  const mucChop =
    bieuCam === 'can_loi_mat_do' || bieuCam === 'ngac_nhien'
      ? 0
      : tinhMucChopMat(frame, seedId);
  const dangNhamMat = mucChop >= 0.75;

  // Con nguoi liec nhe theo huong nhin / bang + dao mat vi mo tat dinh (khi nhin thang ong kinh thi con nguoi o giua)
  const liecViMoX = Math.sin(frame * 0.055 + seedId * 0.17) * (nhinThangOngKinh ? 0.28 : 0.65);
  const liecViMoY = Math.cos(frame * 0.043 + seedId * 0.29) * (nhinThangOngKinh ? 0.2 : 0.35);
  const nguoiX = nhinThangOngKinh
    ? kepGiaTri(liecViMoX, -0.8, 0.8)
    : kepGiaTri((huongNhinX + liecViMoX) * dir, -2.1, 2.1);
  const nguoiY = nhinThangOngKinh
    ? kepGiaTri(liecViMoY, -0.6, 0.6)
    : kepGiaTri(huongNhinY + liecViMoY, -1.6, 1.6);

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
        // Mo nho / he nhe
        const ry = noiSuy(2.2, 3.5, kepGiaTri((lip.cuongDo - 0.08) / 0.24, 0, 1));
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
        // Mo vua / tron chu O
        const ty = kepGiaTri((lip.cuongDo - 0.32) / 0.3, 0, 1);
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
        const doMoRong = noiSuy(6.2, 8.2, kepGiaTri((lip.cuongDo - 0.62) / 0.38, 0, 1));
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
      {/* Ma hong duyen dang cho bieu cam vui tuoi / tu man / em be so sinh */}
      {(laSoSinh || bieuCam === 'vui_tuoi' || bieuCam === 'tu_man') && (
        <>
          <ellipse
            cx={nhinThangOngKinh ? matTraiX - 5.2 : matTraiX - 4 * dir}
            cy={matY + 8}
            rx={laSoSinh ? 5.2 : 4.2}
            ry={laSoSinh ? 3.2 : 2.4}
            fill="#FB7185"
            fillOpacity={laSoSinh ? 0.58 : 0.38}
          />
          <ellipse
            cx={nhinThangOngKinh ? matPhaiX + 5.2 : matPhaiX + 4 * dir}
            cy={matY + 8}
            rx={laSoSinh ? 5.2 : 4.2}
            ry={laSoSinh ? 3.2 : 2.4}
            fill="#FB7185"
            fillOpacity={laSoSinh ? 0.58 : 0.38}
          />
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

/** Ve chi tiet toc / kinh / rau theo doTuoi tren dau nhan vat (v2.0 + tuong thich v3.0) */
const veChiTietDauTheoDoTuoi = (
  doTuoi: DoTuoiNhanVat,
  dir: number,
  nhinThangOngKinh: boolean,
  phuKien: LoaiPhuKien,
  mauChuDao: string,
  daCoKieuTocRieng = false,
  daCoRauRieng = false,
) => {
  if (doTuoi === 'thieu_nien' && !daCoKieuTocRieng) {
    // Chom toc nang dong tuoi thieu nien
    return (
      <g>
        <path
          d={`M ${-14 * dir} -20 Q ${-4 * dir} -34 ${5 * dir} -24 Q ${12 * dir} -34 ${18 * dir} -20 Q ${8 * dir} -24 0 -22 Q ${-8 * dir} -24 ${-14 * dir} -20 Z`}
          fill="#1E293B"
          stroke="#1A1A1A"
          strokeWidth={1.8}
          strokeLinejoin="round"
        />
      </g>
    );
  }

  if (doTuoi === 'gia') {
    const matTraiX = nhinThangOngKinh ? -7.5 : 3 * dir;
    const matPhaiX = nhinThangOngKinh ? 7.5 : 12.5 * dir;
    const miengX = nhinThangOngKinh ? 0 : 7.5 * dir;
    return (
      <g>
        {/* Mai toc bac hai ben thai duong va dinh dau (chi ve neu chua chi dinh kieuToc v3.0) */}
        {!daCoKieuTocRieng && (
          <>
            <path
              d="M -24 -6 Q -27 -24 -12 -27 Q 0 -30 12 -27 Q 27 -24 24 -6 Q 18 -18 0 -20 Q -18 -18 -24 -6 Z"
              fill="#E2E8F0"
              stroke="#1A1A1A"
              strokeWidth={2}
              strokeLinejoin="round"
            />
            <circle cx={-21} cy={-4} r={5.5} fill="#F1F5F9" stroke="#1A1A1A" strokeWidth={1.6} />
            <circle cx={21} cy={-4} r={5.5} fill="#F1F5F9" stroke="#1A1A1A" strokeWidth={1.6} />
          </>
        )}
        {/* Chom rau bac hien hau o cam (chi ve neu chua chi dinh coRau v3.0) */}
        {!daCoRauRieng && (
          <path
            d={`M ${miengX - 7} 15 Q ${miengX} 26 ${miengX + 7} 15 Q ${miengX} 19 ${miengX - 7} 15 Z`}
            fill="#F1F5F9"
            stroke="#1A1A1A"
            strokeWidth={1.6}
            strokeLinejoin="round"
          />
        )}
        {/* Kinh lao tron (tu dong ve neu nhan vat chua deo kinh_tron) */}
        {phuKien !== 'kinh_tron' && (
          <g>
            <circle
              cx={matTraiX}
              cy={-4}
              r={5.8}
              fill="#E0F2FE"
              fillOpacity={0.32}
              stroke="#1A1A1A"
              strokeWidth={2}
            />
            <circle
              cx={matPhaiX}
              cy={-4}
              r={5.8}
              fill="#E0F2FE"
              fillOpacity={0.32}
              stroke="#1A1A1A"
              strokeWidth={2}
            />
            <line
              x1={matTraiX + (nhinThangOngKinh ? 5.8 : 4.5 * dir)}
              y1={-4}
              x2={matPhaiX - (nhinThangOngKinh ? 5.8 : 4.5 * dir)}
              y2={-4}
              stroke="#1A1A1A"
              strokeWidth={2}
            />
          </g>
        )}
        {/* Cham nhan nho tren vong co/ao */}
        <circle cx={0} cy={27} r={2.2} fill={mauChuDao} />
      </g>
    );
  }

  return null;
};

/** Ve em be so sinh nam trong noi go / ta quan co ma hong (v2.0) */
const veEmBeSoSinh = (
  bieuCam: LoaiBieuCam,
  dir: number,
  mauNet: string,
  mauChuDao: string,
  mauDa: string,
  dangNoi: boolean,
  frame: number,
  seedId: number,
  nhinThangOngKinh: boolean,
  bienDoAmThanh?: readonly number[],
) => {
  const lacNoi = Math.sin(frame * 0.09 + seedId * 0.1) * 3.4;
  const vayTay = Math.sin(frame * 0.24) * 5;
  return (
    <g transform={`translate(0, -18) rotate(${lacNoi.toFixed(2)}, 0, 18)`}>
      {/* Khung noi go em ai */}
      <path
        d="M -66 12 Q 0 34 66 12"
        fill="none"
        stroke="#92400E"
        strokeWidth={7}
        strokeLinecap="round"
      />
      <rect
        x={-54}
        y={-34}
        width={108}
        height={44}
        rx={16}
        fill="#FEF3C7"
        stroke="#78350F"
        strokeWidth={4}
      />
      {/* Goi mem trong noi */}
      <ellipse
        cx={-18 * dir}
        cy={-26}
        rx={26}
        ry={13}
        fill="#FFFFFF"
        stroke="#CBD5E1"
        strokeWidth={2.2}
      />
      {/* Than ta quan em be */}
      <path
        d={`M ${-34 * dir} -24 Q ${4 * dir} -36 ${38 * dir} -16 Q ${32 * dir} 4 ${-10 * dir} 2 Q ${-36 * dir} -4 ${-34 * dir} -24 Z`}
        fill={mauChuDao}
        fillOpacity={0.26}
        stroke={mauChuDao}
        strokeWidth={3.2}
      />
      <path
        d={`M ${-16 * dir} -26 Q ${8 * dir} -10 ${24 * dir} -22`}
        fill="none"
        stroke={mauChuDao}
        strokeWidth={2.6}
        strokeLinecap="round"
      />
      {/* Hai ban tay ti hon vay nhe */}
      <circle cx={-4 * dir} cy={-28 + vayTay * 0.5} r={6} fill={mauDa} stroke={mauNet} strokeWidth={2.5} />
      <circle cx={14 * dir} cy={-24 - vayTay * 0.5} r={6} fill={mauDa} stroke={mauNet} strokeWidth={2.5} />
      {/* Dau em be tron trinh ma hong + chom toc xoan */}
      <g transform={`translate(${(-20 * dir).toFixed(1)}, -40)`}>
        <circle cx={0} cy={0} r={24} fill={mauDa} stroke={mauNet} strokeWidth={5} />
        <path
          d="M -3 -24 Q 4 -36 10 -27 Q 4 -24 2 -23"
          fill="none"
          stroke={mauNet}
          strokeWidth={2.8}
          strokeLinecap="round"
        />
        {veBieuCam(
          bieuCam,
          dir,
          mauNet,
          dangNoi,
          frame,
          seedId,
          0,
          0,
          bienDoAmThanh,
          nhinThangOngKinh || true,
          true,
        )}
      </g>
      {/* Thanh lan can phia truoc noi */}
      {[-34, -17, 0, 17, 34].map((sx) => (
        <line
          key={`nan-${sx}`}
          x1={sx}
          y1={-28}
          x2={sx}
          y2={6}
          stroke="#B45309"
          strokeWidth={3}
          strokeLinecap="round"
        />
      ))}
      <line x1={-56} y1={-28} x2={56} y2={-28} stroke="#78350F" strokeWidth={5} strokeLinecap="round" />
    </g>
  );
};

/** Ve do vat nen phia sau cho tuThe (ghe ngoi ban / dau giuong + goi nam giuong) */
const veNenTuThePhiaSau = (
  tuThe: TuTheNhanVat,
  dir: number,
  mauChuDao: string,
) => {
  if (tuThe === 'ngoi_ban') {
    return (
      <g>
        {/* Ghe go phia sau */}
        <rect
          x={dir > 0 ? -42 : 12}
          y={-114}
          width={30}
          height={64}
          rx={6}
          fill="#B45309"
          stroke="#451A03"
          strokeWidth={3}
        />
        <rect
          x={dir > 0 ? -38 : -16}
          y={-56}
          width={54}
          height={12}
          rx={5}
          fill="#D97706"
          stroke="#451A03"
          strokeWidth={3}
        />
        <line x1={dir > 0 ? -32 : 32} y1={-44} x2={dir > 0 ? -32 : 32} y2={0} stroke="#451A03" strokeWidth={5} strokeLinecap="round" />
        <line x1={dir > 0 ? 8 : -8} y1={-44} x2={dir > 0 ? 8 : -8} y2={0} stroke="#451A03" strokeWidth={5} strokeLinecap="round" />
      </g>
    );
  }

  if (tuThe === 'nam_giuong') {
    return (
      <g>
        {/* Khung giuong go + dau giuong */}
        <rect
          x={dir > 0 ? -64 : -92}
          y={-56}
          width={156}
          height={42}
          rx={10}
          fill="#92400E"
          stroke="#451A03"
          strokeWidth={3.5}
        />
        <rect
          x={dir > 0 ? -66 : 44}
          y={-146}
          width={22}
          height={146}
          rx={8}
          fill="#78350F"
          stroke="#451A03"
          strokeWidth={3.5}
        />
        <rect
          x={dir > 0 ? 78 : -94}
          y={-76}
          width={16}
          height={76}
          rx={6}
          fill="#78350F"
          stroke="#451A03"
          strokeWidth={3.5}
        />
        {/* Nem trang em ai */}
        <rect
          x={dir > 0 ? -50 : -80}
          y={-64}
          width={130}
          height={20}
          rx={9}
          fill="#FFFDF7"
          stroke="#CBD5E1"
          strokeWidth={2.5}
        />
        {/* Goi trang phong sau lung va dau */}
        <ellipse
          cx={-26 * dir}
          cy={-114}
          rx={24}
          ry={32}
          fill="#FFFFFF"
          stroke="#94A3B8"
          strokeWidth={3}
          transform={`rotate(${(-14 * dir).toFixed(1)}, ${(-26 * dir).toFixed(1)}, -114)`}
        />
        <circle cx={-26 * dir} cy={-114} r={3} fill={mauChuDao} fillOpacity={0.3} />
      </g>
    );
  }

  return null;
};

/** Ve lop phia truoc cua tuThe (ban viet bai / chan giuong / em be om / ao khoac mua dong) */
const veLopTuThePhiaTruoc = (
  tuThe: TuTheNhanVat,
  dir: number,
  mauNet: string,
  mauChuDao: string,
  mauDa: string,
  frame: number,
  hong: Diem2D,
  diemUonThan: Diem2D,
  co: Diem2D,
  banTayTrai: Diem2D,
  banTayPhai: Diem2D,
) => {
  if (tuThe === 'ngoi_ban') {
    const xBan = dir > 0 ? 6 : -106;
    const xVo = dir > 0 ? 22 : -76;
    return (
      <g>
        {/* Mat ban go & chan ban */}
        <rect
          x={xBan}
          y={-74}
          width={100}
          height={15}
          rx={5}
          fill="#B45309"
          stroke="#451A03"
          strokeWidth={3.2}
        />
        <line x1={xBan + 12} y1={-59} x2={xBan + 12} y2={0} stroke="#451A03" strokeWidth={6} strokeLinecap="round" />
        <line x1={xBan + 88} y1={-59} x2={xBan + 88} y2={0} stroke="#451A03" strokeWidth={6} strokeLinecap="round" />
        {/* Quyen vo mo & lo muc viet bai */}
        <rect x={xVo} y={-84} width={54} height={11} rx={3} fill="#FFFBEB" stroke="#1E293B" strokeWidth={2.2} />
        <line x1={xVo + 27} y1={-84} x2={xVo + 27} y2={-73} stroke="#94A3B8" strokeWidth={2} />
        <rect x={xVo + (dir > 0 ? 58 : -16)} y={-90} width={12} height={16} rx={3} fill="#1E293B" />
        <path
          d={`M ${xVo + (dir > 0 ? 64 : -10)} -90 L ${xVo + (dir > 0 ? 74 : -20)} -108`}
          stroke="#F8FAFC"
          strokeWidth={3}
          strokeLinecap="round"
        />
      </g>
    );
  }

  if (tuThe === 'nam_giuong') {
    const xDauChan = dir > 0 ? -16 : -84;
    return (
      <g>
        {/* Chan bong am ap phu len than duoi & chan */}
        <path
          d={`M ${xDauChan} -78 Q ${xDauChan + 50} -92 ${xDauChan + 100} -74 L ${xDauChan + 100} -40 L ${xDauChan} -40 Z`}
          fill={mauChuDao}
          stroke="#1E293B"
          strokeWidth={3.4}
          strokeLinejoin="round"
        />
        {/* Mep chan gap trang sach se */}
        <path
          d={`M ${xDauChan} -78 Q ${xDauChan + 18} -84 ${xDauChan + 26} -76 L ${xDauChan + 22} -64 Q ${xDauChan + 12} -70 ${xDauChan} -64 Z`}
          fill="#FFFDF7"
          stroke="#1E293B"
          strokeWidth={2.4}
          strokeLinejoin="round"
        />
        <path
          d={`M ${xDauChan + 36} -66 Q ${xDauChan + 62} -72 ${xDauChan + 88} -62`}
          fill="none"
          stroke="#FFFFFF"
          strokeOpacity={0.45}
          strokeWidth={3}
          strokeLinecap="round"
        />
      </g>
    );
  }

  if (tuThe === 'om_em_be') {
    const cx = (banTayTrai.x + banTayPhai.x) * 0.5 + 4 * dir;
    const cy = (banTayTrai.y + banTayPhai.y) * 0.5 - 2;
    const ru = Math.sin(frame * 0.12) * 3;
    return (
      <g transform={`translate(${cx.toFixed(1)}, ${cy.toFixed(1)}) rotate(${(ru - 12 * dir).toFixed(1)})`}>
        {/* Bo ta quan em be */}
        <ellipse cx={0} cy={6} rx={24} ry={13} fill="#FEF08A" stroke="#1E293B" strokeWidth={2.6} />
        <path d="M -16 4 Q 0 13 16 4" fill="none" stroke="#F59E0B" strokeWidth={2.2} strokeLinecap="round" />
        {/* Dau em be nho xinh voi ma hong */}
        <circle cx={-12 * dir} cy={-2} r={11.5} fill={mauDa} stroke={mauNet} strokeWidth={2.6} />
        <ellipse cx={-16 * dir} cy={1} rx={2.5} ry={1.5} fill="#FB7185" fillOpacity={0.6} />
        <ellipse cx={-8 * dir} cy={1} rx={2.5} ry={1.5} fill="#FB7185" fillOpacity={0.6} />
        <path d={`M ${-15 * dir} -3 Q ${-13 * dir} -1 ${-11 * dir} -3`} fill="none" stroke={mauNet} strokeWidth={1.6} strokeLinecap="round" />
        <path d={`M ${-9 * dir} -3 Q ${-7 * dir} -1 ${-5 * dir} -3`} fill="none" stroke={mauNet} strokeWidth={1.6} strokeLinecap="round" />
      </g>
    );
  }

  if (tuThe === 'mac_ao_khoac') {
    // Ao khoac mua dong bam theo cot song hong -> diemUonThan -> co
    const xCo = co.x;
    const yCo = co.y + 4;
    const xHong = hong.x;
    const yHong = hong.y + 18;
    const xGiua = diemUonThan.x;
    const yGiua = diemUonThan.y + 8;
    return (
      <g>
        <path
          d={`M ${(xCo - 14).toFixed(1)} ${yCo.toFixed(1)} Q ${(xGiua - 21).toFixed(1)} ${yGiua.toFixed(1)} ${(xHong - 22).toFixed(1)} ${yHong.toFixed(1)} L ${(xHong + 22).toFixed(1)} ${yHong.toFixed(1)} Q ${(xGiua + 21).toFixed(1)} ${yGiua.toFixed(1)} ${(xCo + 14).toFixed(1)} ${yCo.toFixed(1)} Z`}
          fill={mauChuDao}
          stroke="#1E293B"
          strokeWidth={3.2}
          strokeLinejoin="round"
        />
        {/* Co ao long am ap */}
        <rect
          x={xCo - 17}
          y={yCo - 6}
          width={34}
          height={12}
          rx={6}
          fill="#F8FAFC"
          stroke="#1E293B"
          strokeWidth={2.4}
        />
        {/* Hang cuc ao & ve ao */}
        <line
          x1={xCo + 2 * dir}
          y1={yCo + 6}
          x2={xHong + 2 * dir}
          y2={yHong - 2}
          stroke="#0F172A"
          strokeOpacity={0.45}
          strokeWidth={2.2}
        />
        {[0.28, 0.54, 0.78].map((t) => (
          <circle
            key={`cuc-${t}`}
            cx={noiSuy(xCo, xHong, t) + 6 * dir}
            cy={noiSuy(yCo + 6, yHong, t)}
            r={2.8}
            fill="#FEF08A"
            stroke="#1E293B"
            strokeWidth={1.3}
          />
        ))}
      </g>
    );
  }

  return null;
};

export const NguoiQueDong: React.FC<NguoiQueDongProps> = ({
  thongTin,
  trangThai,
  tiLe = 1,
  thoiLuongCanh,
  bienDoAmThanh,
  nhinThangOngKinh: nhinThangProp,
  danhSachNhanVatTrongCanh,
  anhSangMoiTruong: anhSangProp,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const cam = useCameraParallax();
  const anhSangContext = useAnhSangMoiTruong();
  const anhSangHieuLuc = anhSangProp ?? anhSangContext;
  const thamSoAnhSang = tinhThamSoAnhSangNhanVat(anhSangHieuLuc);
  const tongFrame = Math.max(1, thoiLuongCanh ?? durationInFrames);

  const daGiai = trangThai as Partial<TrangThaiNhanVatDaGiai>;
  const doTuoi: DoTuoiNhanVat =
    trangThai.doTuoi ?? thongTin.doTuoi ?? 'truong_thanh';
  const tuThe: TuTheNhanVat = trangThai.tuThe ?? 'dung';
  const hoaTrang = giaiTrangPhucHieuLuc(thongTin, trangThai);
  const tamKhungTransform = tinhTiLeTamKhung(hoaTrang.tamKhung);

  // Giai huong mat & anh mat tuong tac (ho tro ca khi goi qua giaiTrangThaiNhanVatTrongCanh lan goi truc tiep)
  const huongTuongTac =
    typeof daGiai.nhinThangOngKinh === 'boolean'
      ? {
          huongHieuLuc: trangThai.huong,
          nhinThangOngKinh: daGiai.nhinThangOngKinh,
          lechNhinX: daGiai.lechNhinX ?? 0,
          lechNhinY: daGiai.lechNhinY ?? 0,
        }
      : tinhHuongNhinTuongTac(
          trangThai,
          danhSachNhanVatTrongCanh ?? [trangThai],
          undefined,
        );

  const nhinThangOngKinh = Boolean(
    nhinThangProp ?? huongTuongTac.nhinThangOngKinh,
  );
  const huongHieuLuc = huongTuongTac.huongHieuLuc;
  const dir = huongHieuLuc === 'trai' ? -1 : 1;
  const seedId = bamChuoiTatDinh(thongTin.id);

  // Giai bieu cam theo moc frame (bieuCamTheoMoc[])
  const bieuCamHieuLuc =
    typeof daGiai.frameBatDauThoai === 'number'
      ? trangThai.bieuCam
      : giaiBieuCamTheoMoc(
          trangThai.bieuCam,
          trangThai.bieuCamTheoMoc,
          frame,
          tongFrame,
        ).bieuCam;

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

  const xuong = tinhKhungXuongCoBan(trangThai.hanhDong, frame, huongHieuLuc, {
    dangNoi: Boolean(trangThai.dangNoi),
    vanTocDiChuyenX,
    doTuoi,
    tuThe,
  });

  // Nhip tho nguc & cu chi tay linh hoat bam bien do RMS khi noi (100% tat dinh)
  const rmsHienTai = trangThai.dangNoi
    ? tinhLipSyncChoFrame(frame, seedId, trangThai.bienDoAmThanh ?? bienDoAmThanh).cuongDo
    : 0;
  const thoNguc = 1 + Math.sin(frame * 0.11 + seedId * 0.13) * 0.024 + rmsHienTai * 0.022;
  const nhunVaiNoiY = trangThai.dangNoi ? -rmsHienTai * 2.4 : Math.sin(frame * 0.11 + seedId * 0.13) * 0.8;
  const tayNoiOffsetY = trangThai.dangNoi ? -rmsHienTai * 4.5 : 0;

  const vaiTraiHieuLuc: Diem2D = {
    x: xuong.vaiTrai.x - 10 * thoNguc,
    y: xuong.vaiTrai.y + nhunVaiNoiY,
  };
  const vaiPhaiHieuLuc: Diem2D = {
    x: xuong.vaiPhai.x + 10 * thoNguc,
    y: xuong.vaiPhai.y + nhunVaiNoiY,
  };
  const banTayPhaiHieuLuc: Diem2D = {
    x: xuong.banTayPhai.x + (trangThai.dangNoi ? rmsHienTai * 3.5 * dir : 0),
    y: xuong.banTayPhai.y + tayNoiOffsetY,
  };
  const banTayTraiHieuLuc: Diem2D = {
    x: xuong.banTayTrai.x,
    y: xuong.banTayTrai.y + tayNoiOffsetY * 0.55,
  };

  const xTong = xHienTai + xuong.dichNgangNoiBo;
  const yTong = trangThai.y + tamKhungTransform.dichY;
  const tiLeTong = tiLe * (trangThai.tiLe ?? 1) * tamKhungTransform.heSoTiLe;

  const mauNet = MAU_MUC_TRUYEN_TRANH;
  const mauChuDao = hoaTrang.mauAoChinh;
  const mauDa = thongTin.mauDa ?? '#FFFDF7';

  // Bong tiep dat (ground shadow) elip ban trong suot tu co gian khi nhay & khi buoc di
  const doCaoBay = Math.max(xuong.doCaoNhay, Math.max(0, -xuong.offsetY));
  const doRongBuocChan = Math.abs(xuong.banChanPhai.x - xuong.banChanTrai.x);
  const bongDat = tinhBongTiepDat(
    doCaoBay,
    doTuoi,
    tuThe,
    doRongBuocChan,
    anhSangHieuLuc,
  );

  // Co gian dau nhe theo squash & stretch de tang cam giac hoat hinh dan hoi
  const dauScaleX = 1 + (xuong.squashX - 1) * 0.42;
  const dauScaleY = 1 + (xuong.squashY - 1) * 0.42;
  const banKinhDau = doTuoi === 'thieu_nien' ? 24.5 : 26;
  const doDayNet = doTuoi === 'thieu_nien' ? 8.2 : 9.4;

  const frameBatDauThoai = daGiai.frameBatDauThoai ?? 0;

  // Hop nhan ten nhan vat tu co gian + rang buoc luon nam TREN vung phu de (>= 150px tu mep duoi)
  const hopTen = tinhThongSoHopTen(thongTin.ten);
  const zoomCam = Math.max(1, Number.isFinite(cam.zoom) ? cam.zoom : 1);
  const panYCam = Number.isFinite(cam.panY) ? cam.panY : 0;
  const gioiHanDuoiManHinh = 1080 - HUD_BOTTOM_SAFE - 10; // 920px (tren han vung phu de 150px)
  const gioiHanDuoiTheGioi = 540 + (gioiHanDuoiManHinh - 540 - panYCam) / zoomCam;
  const maxLocalTenY =
    (gioiHanDuoiTheGioi - trangThai.y) / Math.max(0.2, tiLeTong) -
    hopTen.height / 2;
  const viTriTenY = Math.max(-36, Math.min(28, maxLocalTenY));

  const huongNhinTongX = xuong.huongNhinX + huongTuongTac.lechNhinX;
  const huongNhinTongY = xuong.huongNhinY + huongTuongTac.lechNhinY;

  return (
    <g transform={`translate(${xTong.toFixed(1)}, ${yTong.toFixed(1)}) scale(${tiLeTong.toFixed(3)})`}>
      {/* Bong tiep dat (ground shadow) elip ban trong suot tu co gian theo nhay/buoc di & dong bo anh sang */}
      <ellipse
        cx={doTuoi === 'so_sinh' ? 0 : (xuong.banChanTrai.x + xuong.banChanPhai.x) * 0.5}
        cy={4}
        rx={bongDat.rx}
        ry={bongDat.ry}
        fill={bongDat.fill}
        fillOpacity={bongDat.opacity}
      />
      {/* Lop bong tiep dat trong dam hon nhe o chinh tam giup chan dung chac tren mat dat 2.5D */}
      <ellipse
        cx={doTuoi === 'so_sinh' ? 0 : (xuong.banChanTrai.x + xuong.banChanPhai.x) * 0.5}
        cy={4}
        rx={(bongDat.rx * 0.62).toFixed(1)}
        ry={(bongDat.ry * 0.64).toFixed(1)}
        fill={bongDat.fill}
        fillOpacity={(bongDat.opacity * 0.65).toFixed(3)}
      />

      {doTuoi === 'so_sinh' ? (
        veEmBeSoSinh(
          bieuCamHieuLuc,
          dir,
          mauNet,
          mauChuDao,
          mauDa,
          Boolean(trangThai.dangNoi),
          frame,
          seedId,
          nhinThangOngKinh,
          trangThai.bienDoAmThanh ?? bienDoAmThanh,
        )
      ) : (
        <>
          {/* Vet bui nho duoi got chan khi chay voi va / bat nhay dap dat */}
          {xuong.coVetBui && veVetBuiDuoiGot(frame, dir, seedId)}

          {/* Do vat nen phia sau cho tuThe (ghe ngoi ban / giuong + goi) */}
          {veNenTuThePhiaSau(tuThe, dir, mauChuDao)}

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

          {/* Lop sau: chan sau & tay sau mac quan/ao 2 sac do vien muc den #1A1A1A */}
          {veChanMacQuan(
            xuong.hong,
            xuong.goiTrai,
            xuong.banChanTrai,
            dir,
            hoaTrang.mauQuanChinh,
            hoaTrang.mauQuanBong,
            doDayNet,
            true,
            thamSoAnhSang,
          )}
          {veCanhTayMacAo(
            vaiTraiHieuLuc,
            xuong.khuyuTrai,
            banTayTraiHieuLuc,
            hoaTrang.mauAoChinh,
            hoaTrang.mauAoBong,
            mauDa,
            doDayNet * 0.9,
            true,
            thamSoAnhSang,
          )}

          {/* Chan truoc mac quan + giay co dien */}
          {veChanMacQuan(
            xuong.hong,
            xuong.goiPhai,
            xuong.banChanPhai,
            dir,
            hoaTrang.mauQuanChinh,
            hoaTrang.mauQuanBong,
            doDayNet,
            false,
            thamSoAnhSang,
          )}

          {/* Than mac trang phuc truyen tranh chi tiet 2 sac do SVG phang theo trangPhuc */}
          {veTrangPhucThan(
            hoaTrang,
            { x: xuong.co.x, y: xuong.co.y + nhunVaiNoiY * 0.5 },
            xuong.diemUonThan,
            xuong.hong,
            dir,
            thoNguc,
            thamSoAnhSang,
          )}

          {/* Ao khoac mua dong them chi tiet co long khi dung tuThe mac_ao_khoac */}
          {tuThe === 'mac_ao_khoac' &&
            veLopTuThePhiaTruoc(
              tuThe,
              dir,
              mauNet,
              mauChuDao,
              mauDa,
              frame,
              xuong.hong,
              xuong.diemUonThan,
              xuong.co,
              banTayTraiHieuLuc,
              banTayPhaiHieuLuc,
            )}

          {/* Tay truoc mac tay ao & ban tay tron trang vien muc den #1A1A1A */}
          {veCanhTayMacAo(
            vaiPhaiHieuLuc,
            xuong.khuyuPhai,
            banTayPhaiHieuLuc,
            hoaTrang.mauAoChinh,
            hoaTrang.mauAoBong,
            mauDa,
            doDayNet * 0.9,
            false,
            thamSoAnhSang,
          )}

          {/* Gay go cho bien the tuoi gia (khi khong cam vat khac) */}
          {doTuoi === 'gia' && (!trangThai.vatCamTay || trangThai.vatCamTay === 'khong') && (
            <g>
              <path
                d={`M ${(banTayPhaiHieuLuc.x - 4 * dir).toFixed(1)} ${(banTayPhaiHieuLuc.y - 6).toFixed(1)} Q ${(banTayPhaiHieuLuc.x + 8 * dir).toFixed(1)} ${(banTayPhaiHieuLuc.y - 16).toFixed(1)} ${(banTayPhaiHieuLuc.x + 12 * dir).toFixed(1)} ${(banTayPhaiHieuLuc.y - 2).toFixed(1)} L ${(banTayPhaiHieuLuc.x + 14 * dir).toFixed(1)} 0`}
                fill="none"
                stroke="#78350F"
                strokeWidth={5.5}
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </g>
          )}

          {/* Khan quang gon cho thieu_nien */}
          {doTuoi === 'thieu_nien' && (
            <polygon
              points={`${xuong.co.x - 9},${xuong.co.y + 1} ${xuong.co.x + 9},${xuong.co.y + 1} ${xuong.co.x + 2 * dir},${xuong.co.y + 15}`}
              fill={mauChuDao}
              stroke={mauNet}
              strokeWidth={2}
              strokeLinejoin="round"
            />
          )}

          {/* Dau tron trang vien muc den #1A1A1A sac net + bong 2 sac do + bieu cam RMS + rau + toc */}
          <g
            transform={`translate(${xuong.dau.x.toFixed(1)}, ${(xuong.dau.y + nhunVaiNoiY * 0.5).toFixed(1)}) rotate(${xuong.gocDau.toFixed(1)}) scale(${dauScaleX.toFixed(3)}, ${dauScaleY.toFixed(3)})`}
          >
            {/* Nen dau tron trang */}
            <circle cx={0} cy={0} r={banKinhDau} fill={mauDa} stroke={mauNet} strokeWidth={5.2} />
            {/* Mang bong cel-shading cong mem phia sau dau (SVG phang) */}
            <path
              d={
                dir > 0
                  ? `M -4 ${-banKinhDau + 2} A ${banKinhDau - 2} ${banKinhDau - 2} 0 0 0 -4 ${banKinhDau - 2} Q -15 0 -4 ${-banKinhDau + 2} Z`
                  : `M 4 ${-banKinhDau + 2} A ${banKinhDau - 2} ${banKinhDau - 2} 0 0 1 4 ${banKinhDau - 2} Q 15 0 4 ${-banKinhDau + 2} Z`
              }
              fill="#CBD5E1"
              fillOpacity={0.34}
            />
            {/* Dong bo anhSangMoiTruong len dau bang lop phu mau phang do mo 0.08..0.22 */}
            {thamSoAnhSang.coPhuMau && (
              <>
                <circle
                  cx={0}
                  cy={0}
                  r={banKinhDau - 2.4}
                  fill={thamSoAnhSang.mauPhu}
                  fillOpacity={thamSoAnhSang.doMoPhu}
                />
                {thamSoAnhSang.doMoVienSang > 0.01 && (
                  <path
                    d={
                      dir > 0
                        ? `M 6 ${-banKinhDau + 4} A ${banKinhDau - 4} ${banKinhDau - 4} 0 0 1 ${banKinhDau - 4} 5`
                        : `M -6 ${-banKinhDau + 4} A ${banKinhDau - 4} ${banKinhDau - 4} 0 0 0 ${-(banKinhDau - 4)} 5`
                    }
                    fill="none"
                    stroke={thamSoAnhSang.mauVienSang}
                    strokeOpacity={thamSoAnhSang.doMoVienSang}
                    strokeWidth={2.5}
                    strokeLinecap="round"
                  />
                )}
              </>
            )}

            {veBieuCam(
              bieuCamHieuLuc,
              dir,
              mauNet,
              Boolean(trangThai.dangNoi),
              frame,
              seedId,
              huongNhinTongX,
              huongNhinTongY,
              trangThai.bienDoAmThanh ?? bienDoAmThanh,
              nhinThangOngKinh,
              false,
            )}

            {/* 4 kieu rau lich su (khong che mieng lip-sync) */}
            {veRauNhanVat(hoaTrang.coRau, doTuoi, dir, nhinThangOngKinh)}

            {/* Chi tiet doTuoi (toc/rau mac dinh neu chua chi dinh v3.0 + kinh lao) */}
            {veChiTietDauTheoDoTuoi(
              doTuoi,
              dir,
              nhinThangOngKinh,
              thongTin.phuKien,
              mauChuDao,
              hoaTrang.kieuToc !== null,
              hoaTrang.coRau !== 'khong',
            )}

            {/* 7 kieu toc & mu lich su v3.0 */}
            {veKieuTocNhanVat(
              hoaTrang.kieuToc,
              doTuoi,
              dir,
              mauChuDao,
              thamSoAnhSang,
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

            {/* Vien muc #1A1A1A bao quanh khuon mat sac net */}
            <circle cx={0} cy={0} r={banKinhDau} fill="none" stroke={mauNet} strokeWidth={5.2} />
          </g>

          {/* Vat cam tay (tu dong ve phong bi thu dep mat neu dang trao_thu ma chua chon vatCamTay) */}
          {trangThai.hanhDong === 'trao_thu' &&
          (!trangThai.vatCamTay || trangThai.vatCamTay === 'khong') ? (
            <g
              transform={`translate(${(xuong.diemCamVat.x + 6 * dir).toFixed(1)}, ${(xuong.diemCamVat.y + tayNoiOffsetY - 4).toFixed(1)}) scale(${dir}, 1) rotate(-8)`}
            >
              <rect x={-4} y={-14} width={30} height={21} rx={3} fill="#FEF3C7" stroke="#92400E" strokeWidth={2.4} />
              <path d="M -4 -14 L 11 -2 L 26 -14" fill="none" stroke="#92400E" strokeWidth={2.2} strokeLinejoin="round" />
              <circle cx={11} cy={-2} r={3} fill="#DC2626" />
            </g>
          ) : (
            veVatCamTay(
              trangThai.vatCamTay,
              xuong.diemCamVat.x,
              xuong.diemCamVat.y + tayNoiOffsetY,
              dir,
              frame,
              xuong.gocCangTayPhai,
            )
          )}

          {/* Lop truoc cua tuThe (ban viet, chan giuong, em be om) */}
          {tuThe !== 'mac_ao_khoac' &&
            veLopTuThePhiaTruoc(
              tuThe,
              dir,
              mauNet,
              mauChuDao,
              mauDa,
              frame,
              xuong.hong,
              xuong.diemUonThan,
              xuong.co,
              banTayTraiHieuLuc,
              banTayPhaiHieuLuc,
            )}
        </>
      )}

      {/* The ten nhan vat tu co gian theo do dai chuoi & luon nam tren vung phu de */}
      {hopTen.text.length > 0 && (
        <g transform={`translate(0, ${viTriTenY.toFixed(1)})`}>
          <rect
            x={-hopTen.width / 2}
            y={-hopTen.height / 2}
            width={hopTen.width}
            height={hopTen.height}
            rx={14}
            fill="#FFFDF7"
            fillOpacity={0.95}
            stroke={mauChuDao}
            strokeWidth={2.6}
          />
          <text
            x={0}
            y={5.5}
            textAnchor="middle"
            fill="#0F172A"
            fontSize={hopTen.fontSize}
            fontWeight={800}
            fontFamily="Segoe UI, Arial, sans-serif"
          >
            {hopTen.text}
          </text>
        </g>
      )}

      {/* Bong bong chat hoat hinh ve net muc dong bo truyen tranh 4 kieu (v3.0) */}
      {trangThai.bongBongThoai && (
        <BongBongChat
          noiDung={trangThai.bongBongThoai}
          kieu={trangThai.kieuBongBong ?? 'thuong'}
          frameBatDau={frameBatDauThoai}
          nhanVatWorldX={xTong}
          nhanVatWorldY={yTong}
          tiLeNhanVat={tiLeTong}
          dauLocalX={doTuoi === 'so_sinh' ? -20 * dir : xuong.dau.x}
          dauLocalY={doTuoi === 'so_sinh' ? -58 : xuong.dau.y}
          dir={dir}
          banKinhDau={banKinhDau}
        />
      )}
    </g>
  );
};
