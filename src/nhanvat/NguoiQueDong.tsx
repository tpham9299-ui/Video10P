import React from 'react';
import { useCurrentFrame } from 'remotion';
import type {
  LoaiBieuCam,
  LoaiPhuKien,
  LoaiVuKhiToan,
  NhanVatTrongCanh,
  ThongTinNhanVat,
} from '../kieu_dai';
import { tinhKhungXuongCoBan } from '../xuong/he_xuong';

// TODO(v0.2): nang cap xuong khop & VFX

type NguoiQueDongProps = {
  thongTin: ThongTinNhanVat;
  trangThai: NhanVatTrongCanh;
  tiLe?: number;
};

const NHAN_VU_KHI: Record<Exclude<LoaiVuKhiToan, 'khong'>, string> = {
  kiem_can2: '√2',
  luoi_hai_tich_phan: '∫',
  gay_pi: 'π',
  khien_so_nguyen: 'ℤ',
  tia_vo_cuc: '∞',
};

const veBieuCam = (
  bieuCam: LoaiBieuCam,
  cx: number,
  cy: number,
  dir: number,
  mauNet: string,
  dangNoi: boolean,
  frame: number,
) => {
  const matTraiX = cx + 4 * dir;
  const matPhaiX = cx + 12 * dir;
  const matY = cy - 4;
  const miengX = cx + 8 * dir;
  const miengY = cy + 7;
  const moMieng = dangNoi ? Math.abs(Math.sin(frame * 0.6)) * 4 + 1.5 : 0;

  return (
    <g>
      {bieuCam === 'tuc_gian' && (
        <>
          <line
            x1={matTraiX - 4}
            y1={matY - 6}
            x2={matTraiX + 4}
            y2={matY - 3}
            stroke={mauNet}
            strokeWidth={2.5}
            strokeLinecap="round"
          />
          <line
            x1={matPhaiX - 4}
            y1={matY - 3}
            x2={matPhaiX + 4}
            y2={matY - 6}
            stroke={mauNet}
            strokeWidth={2.5}
            strokeLinecap="round"
          />
        </>
      )}

      {bieuCam === 'ngac_nhien' || bieuCam === 'hoang_mang' ? (
        <>
          <circle cx={matTraiX} cy={matY} r={3} fill="none" stroke={mauNet} strokeWidth={2} />
          <circle cx={matPhaiX} cy={matY} r={3} fill="none" stroke={mauNet} strokeWidth={2} />
        </>
      ) : (
        <>
          <circle cx={matTraiX} cy={matY} r={2.4} fill={mauNet} />
          <circle cx={matPhaiX} cy={matY} r={2.4} fill={mauNet} />
        </>
      )}

      {dangNoi ? (
        <ellipse
          cx={miengX}
          cy={miengY}
          rx={4.5}
          ry={moMieng}
          fill={mauNet}
        />
      ) : bieuCam === 'vui' || bieuCam === 'tinh_quai' ? (
        <path
          d={`M ${miengX - 5} ${miengY - 1} Q ${miengX} ${miengY + 5} ${miengX + 5} ${miengY - 1}`}
          fill="none"
          stroke={mauNet}
          strokeWidth={2.4}
          strokeLinecap="round"
        />
      ) : bieuCam === 'tuc_gian' || bieuCam === 'hoang_mang' ? (
        <path
          d={`M ${miengX - 5} ${miengY + 3} Q ${miengX} ${miengY - 3} ${miengX + 5} ${miengY + 3}`}
          fill="none"
          stroke={mauNet}
          strokeWidth={2.4}
          strokeLinecap="round"
        />
      ) : bieuCam === 'ngac_nhien' ? (
        <circle cx={miengX} cy={miengY} r={3.5} fill="none" stroke={mauNet} strokeWidth={2.2} />
      ) : (
        <line
          x1={miengX - 4}
          y1={miengY}
          x2={miengX + 4}
          y2={miengY}
          stroke={mauNet}
          strokeWidth={2.4}
          strokeLinecap="round"
        />
      )}
    </g>
  );
};

const vePhuKien = (
  phuKien: LoaiPhuKien,
  dauX: number,
  dauY: number,
  coX: number,
  coY: number,
  dir: number,
  mauNangLuong: string,
) => {
  switch (phuKien) {
    case 'vong_nguyet_que':
      return (
        <path
          d={`M ${dauX - 20} ${dauY - 16} Q ${dauX} ${dauY - 30} ${dauX + 20} ${dauY - 16}`}
          fill="none"
          stroke="#FACC15"
          strokeWidth={4}
          strokeLinecap="round"
        />
      );
    case 'kinh_tron':
      return (
        <g stroke="#E2E8F0" strokeWidth={2} fill="none">
          <circle cx={dauX + 4 * dir} cy={dauY - 4} r={5} />
          <circle cx={dauX + 14 * dir} cy={dauY - 4} r={5} />
        </g>
      );
    case 'toc_gia_17':
      return (
        <path
          d={`M ${dauX - 22} ${dauY + 4} Q ${dauX - 26} ${dauY - 24} ${dauX} ${dauY - 26} Q ${dauX + 26} ${dauY - 24} ${dauX + 22} ${dauY + 4}`}
          fill="none"
          stroke="#CBD5E1"
          strokeWidth={5}
          strokeLinecap="round"
        />
      );
    case 'ao_choang':
      return (
        <path
          d={`M ${coX} ${coY + 4} L ${coX - 36 * dir} ${coY + 76} L ${coX - 10 * dir} ${coY + 72} Z`}
          fill={mauNangLuong}
          fillOpacity={0.28}
          stroke={mauNangLuong}
          strokeWidth={2}
        />
      );
    case 'khan_choang_bay':
      return (
        <path
          d={`M ${coX - 8 * dir} ${coY + 4} Q ${coX - 34 * dir} ${coY + 8} ${coX - 52 * dir} ${coY - 4}`}
          fill="none"
          stroke={mauNangLuong}
          strokeWidth={6}
          strokeLinecap="round"
        />
      );
    case 'khong':
    default:
      return null;
  }
};

const veVuKhiGiuCho = (
  vuKhi: LoaiVuKhiToan | undefined,
  x: number,
  y: number,
  dir: number,
  mauNangLuong: string,
) => {
  if (!vuKhi || vuKhi === 'khong') {
    return null;
  }
  const kyHieu = NHAN_VU_KHI[vuKhi];

  if (vuKhi === 'khien_so_nguyen') {
    return (
      <g transform={`translate(${x + 12 * dir}, ${y})`}>
        <rect
          x={-16}
          y={-34}
          width={32}
          height={68}
          rx={12}
          fill="#0F172A"
          stroke={mauNangLuong}
          strokeWidth={4}
        />
        <text
          x={0}
          y={8}
          textAnchor="middle"
          fill={mauNangLuong}
          fontSize={24}
          fontWeight={800}
          fontFamily="sans-serif"
        >
          {kyHieu}
        </text>
      </g>
    );
  }

  return (
    <g transform={`translate(${x}, ${y})`}>
      <line
        x1={0}
        y1={0}
        x2={56 * dir}
        y2={-36}
        stroke={mauNangLuong}
        strokeWidth={6}
        strokeLinecap="round"
      />
      <circle
        cx={56 * dir}
        cy={-36}
        r={18}
        fill="#0F172A"
        stroke={mauNangLuong}
        strokeWidth={3}
      />
      <text
        x={56 * dir}
        y={-29}
        textAnchor="middle"
        fill={mauNangLuong}
        fontSize={18}
        fontWeight={800}
        fontFamily="sans-serif"
      >
        {kyHieu}
      </text>
    </g>
  );
};

export const NguoiQueDong: React.FC<NguoiQueDongProps> = ({
  thongTin,
  trangThai,
  tiLe = 1,
}) => {
  const frame = useCurrentFrame();
  const dir = trangThai.huong === 'trai' ? -1 : 1;
  const xuong = tinhKhungXuongCoBan(trangThai.hanhDong, frame, trangThai.huong);
  const mauThan = thongTin.mauThan;
  const mauNangLuong = thongTin.mauNangLuong;

  return (
    <g transform={`translate(${trangThai.x}, ${trangThai.y}) scale(${tiLe})`}>
      {/* Bong chan tren mat dat */}
      <ellipse cx={0} cy={4} rx={36} ry={8} fill="#020617" fillOpacity={0.55} />

      {/* Phu kien sau than */}
      {(thongTin.phuKien === 'ao_choang' || thongTin.phuKien === 'khan_choang_bay') &&
        vePhuKien(
          thongTin.phuKien,
          xuong.dau.x,
          xuong.dau.y,
          xuong.co.x,
          xuong.co.y,
          dir,
          mauNangLuong,
        )}

      {/* Than & tu chi nguoi que */}
      <g stroke={mauThan} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" fill="none">
        {/* Cot song */}
        <line x1={xuong.hong.x} y1={xuong.hong.y} x2={xuong.co.x} y2={xuong.co.y} />

        {/* Chan trai */}
        <polyline
          points={`${xuong.hong.x},${xuong.hong.y} ${xuong.goiTrai.x},${xuong.goiTrai.y} ${xuong.banChanTrai.x},${xuong.banChanTrai.y}`}
        />
        {/* Chan phai */}
        <polyline
          points={`${xuong.hong.x},${xuong.hong.y} ${xuong.goiPhai.x},${xuong.goiPhai.y} ${xuong.banChanPhai.x},${xuong.banChanPhai.y}`}
        />

        {/* Tay trai */}
        <polyline
          points={`${xuong.vaiTrai.x},${xuong.vaiTrai.y} ${xuong.khuyuTrai.x},${xuong.khuyuTrai.y} ${xuong.banTayTrai.x},${xuong.banTayTrai.y}`}
        />
        {/* Tay phai */}
        <polyline
          points={`${xuong.vaiPhai.x},${xuong.vaiPhai.y} ${xuong.khuyuPhai.x},${xuong.khuyuPhai.y} ${xuong.banTayPhai.x},${xuong.banTayPhai.y}`}
        />
      </g>

      {/* Dau */}
      <circle
        cx={xuong.dau.x}
        cy={xuong.dau.y}
        r={24}
        fill="#0F172A"
        stroke={mauThan}
        strokeWidth={6}
      />

      {/* Bieu cam */}
      {veBieuCam(
        trangThai.bieuCam,
        xuong.dau.x,
        xuong.dau.y,
        dir,
        mauThan,
        Boolean(trangThai.dangNoi),
        frame,
      )}

      {/* Phu kien tren dau */}
      {thongTin.phuKien !== 'ao_choang' &&
        thongTin.phuKien !== 'khan_choang_bay' &&
        vePhuKien(
          thongTin.phuKien,
          xuong.dau.x,
          xuong.dau.y,
          xuong.co.x,
          xuong.co.y,
          dir,
          mauNangLuong,
        )}

      {/* Vu khi giu cho */}
      {veVuKhiGiuCho(
        trangThai.vuKhiToan,
        xuong.diemCamVuKhi.x,
        xuong.diemCamVuKhi.y,
        dir,
        mauNangLuong,
      )}

      {/* Nhan ten duoi chan */}
      <g transform="translate(0, 34)">
        <rect
          x={-72}
          y={-18}
          width={144}
          height={28}
          rx={14}
          fill="#0F172A"
          fillOpacity={0.9}
          stroke={mauNangLuong}
          strokeWidth={2}
        />
        <text
          x={0}
          y={1}
          textAnchor="middle"
          fill="#F8FAFC"
          fontSize={16}
          fontWeight={700}
          fontFamily="Segoe UI, Arial, sans-serif"
        >
          {thongTin.ten}
        </text>
      </g>

      {/* Bong bong thoai */}
      {trangThai.bongBongThoai && (
        <g transform={`translate(${xuong.dau.x + 18 * dir}, ${xuong.dau.y - 84})`}>
          <rect
            x={-135}
            y={-32}
            width={270}
            height={58}
            rx={16}
            fill="#F8FAFC"
            stroke={mauNangLuong}
            strokeWidth={3}
          />
          <polygon points="-10,26 8,26 -2,40" fill="#F8FAFC" />
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
