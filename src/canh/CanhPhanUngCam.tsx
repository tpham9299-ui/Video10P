import React from 'react';
import { useCurrentFrame } from 'remotion';
import type { BangMau, Canh, KieuPhanUngCam, NhanVatTrongCanh, ThongTinNhanVat } from '../kieu_dai';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { giaiTrangThaiNhanVatTrongCanh } from '../nhanvat/dien_xuat';
import { HieuUngHoatHinh } from '../vfx/HieuUngHoatHinh';
import { tinhTrangThaiPhanUngCam } from './ke_chuyen_v35_logic';

type Props = {
  canh: Canh;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

/**
 * CanhPhanUngCam (v3.5):
 * - Cat nhanh 1.5-2.5 giay can mat nhan vat phu dang nhap tra / nhuong may / tron mat / can loi
 * - Nen truyen tranh tia toc do phang + hieu ung hai + tem chu kich tinh (tat dinh 100%).
 */
export const CanhPhanUngCam: React.FC<Props> = ({ canh, banDoNhanVat }) => {
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const tt = tinhTrangThaiPhanUngCam(frame, thoiLuong);
  const data = canh.phanUngCam;
  const kieu: KieuPhanUngCam = data?.kieuPhanUng ?? 'nhap_tra';

  const danhSachGoc = giaiTrangThaiNhanVatTrongCanh(canh, frame, thoiLuong);
  const nvChonGoc =
    (data?.nhanVatId
      ? danhSachGoc.find((n) => n.id === data.nhanVatId)
      : undefined) ??
    danhSachGoc[danhSachGoc.length - 1] ??
    danhSachGoc[0];

  const idNv = data?.nhanVatId ?? nvChonGoc?.id ?? Object.keys(banDoNhanVat)[0] ?? 'nha_toan_hoc';
  const thongTinNv: ThongTinNhanVat | undefined = banDoNhanVat[idNv] ?? Object.values(banDoNhanVat)[0];

  const bieuCamMacDinh =
    kieu === 'tron_mat'
      ? 'ngac_nhien'
      : kieu === 'nhuong_may'
        ? 'tinh_quai'
        : 'can_loi_mat_do';

  const trangThaiCanMat: NhanVatTrongCanh = {
    ...(nvChonGoc ?? {
      id: idNv,
      x: 960,
      y: 860,
      huong: 'phai' as const,
      hanhDong: 'dung_tho' as const,
      bieuCam: bieuCamMacDinh,
    }),
    id: thongTinNv?.id ?? idNv,
    x: 960,
    y: 940,
    huong: nvChonGoc?.huong ?? 'phai',
    bieuCam: nvChonGoc?.bieuCam ?? bieuCamMacDinh,
    vatCamTay: kieu === 'nhap_tra' ? 'ly_ca_phe' : nvChonGoc?.vatCamTay,
    dangNoi: false,
    bongBongThoai: undefined,
    tamKhung: 'can_mat',
  };

  const mauNen =
    kieu === 'tron_mat'
      ? '#FEF08A'
      : kieu === 'nhuong_may'
        ? '#E0F2FE'
        : kieu === 'can_loi'
          ? '#E2E8F0'
          : '#FEF3C7';

  const mauTia =
    kieu === 'tron_mat'
      ? '#F59E0B'
      : kieu === 'nhuong_may'
        ? '#38BDF8'
        : kieu === 'can_loi'
          ? '#94A3B8'
          : '#FDBA74';

  const chuHieuUng = (
    data?.chuHieuUng ||
    (kieu === 'tron_mat'
      ? 'HẢ?!'
      : kieu === 'nhuong_may'
        ? 'THẬT KHÔNG ĐẤY?'
        : kieu === 'nhap_tra'
          ? 'XÌÌÌ...'
          : '...')
  ).trim();

  const hieuUngMacDinh =
    canh.hieuUngHoatHinh && canh.hieuUngHoatHinh.length > 0
      ? canh.hieuUngHoatHinh
      : [
          {
            loai:
              kieu === 'tron_mat'
                ? ('tia_toc_do' as const)
                : kieu === 'nhuong_may'
                  ? ('cham_hoi_nay' as const)
                  : ('mo_hoi_lon' as const),
            x: 1090,
            y: 350,
            tuFrame: 4,
            thoiLuong: Math.max(24, thoiLuong - 4),
          },
        ];

  const viTriTachTraY = 640 - tt.nhapTraTienDo * 95;

  return (
    <div style={{ position: 'absolute', inset: 0, backgroundColor: mauNen, overflow: 'hidden' }}>
      <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: 'absolute', inset: 0 }}>
        {/* Nen truyen tranh tia toc do phang (100% tat dinh, KHONG blur) */}
        <rect x={0} y={0} width={1920} height={1080} fill={mauNen} />
        {Array.from({ length: 24 }).map((_, i) => {
          const a1 = (i / 24) * Math.PI * 2 + frame * 0.008;
          const a2 = ((i + 0.36) / 24) * Math.PI * 2 + frame * 0.008;
          const r = 1400;
          return (
            <polygon
              key={`pu-tia-${i}`}
              points={`960,520 ${(960 + Math.cos(a1) * r).toFixed(1)},${(520 + Math.sin(a1) * r).toFixed(1)} ${(960 + Math.cos(a2) * r).toFixed(1)},${(520 + Math.sin(a2) * r).toFixed(1)}`}
              fill={mauTia}
              fillOpacity={0.32}
            />
          );
        })}

        {/* Vong tron spotlight phang sau nhan vat */}
        <circle cx={960} cy={520} r={340} fill="#FFFDF7" stroke="#1A1A1A" strokeWidth={8} />

        {/* Nhan vat can mat phong lon */}
        <g transform={`translate(960, 520) scale(${(tt.zoom * 0.62).toFixed(3)}) translate(-960, -560)`}>
          {thongTinNv && (
            <NguoiQueDong
              thongTin={thongTinNv}
              trangThai={trangThaiCanMat}
              tiLe={1.45}
              thoiLuongCanh={thoiLuong}
              nhinThangOngKinh={true}
              anhSangMoiTruong={canh.anhSangMoiTruong}
            />
          )}
        </g>

        {/* Chi tiet kieu phan ung: tach tra boc khoi hoac dau nhuong may kich tinh */}
        {kieu === 'nhap_tra' && (
          <g transform={`translate(1070, ${viTriTachTraY.toFixed(1)})`}>
            <rect x={-38} y={-24} width={76} height={58} rx={12} fill="#FFFBEB" stroke="#1A1A1A" strokeWidth={4.5} />
            <path d="M 38 -10 C 64 -10, 64 22, 38 22" fill="none" stroke="#1A1A1A" strokeWidth={4.5} />
            <line x1={-32} y1={-8} x2={32} y2={-8} stroke="#B45309" strokeWidth={6} />
            {/* 2 lan khoi tra tat dinh */}
            {[-14, 14].map((kx, ki) => {
              const drift = Math.sin(frame * 0.25 + ki * 1.8) * 6;
              return (
                <path
                  key={`khoi-tra-${ki}`}
                  d={`M ${kx} -32 Q ${(kx + drift).toFixed(1)} -54 ${kx} -74`}
                  fill="none"
                  stroke="#78716C"
                  strokeWidth={3.5}
                  strokeLinecap="round"
                />
              );
            })}
          </g>
        )}

        {kieu === 'nhuong_may' && (
          <g transform={`translate(960, ${(330 + tt.nhuongMayOffsetY).toFixed(1)})`}>
            <path d="M 18 0 Q 52 -24 88 -6" fill="none" stroke="#1A1A1A" strokeWidth={9} strokeLinecap="round" />
          </g>
        )}

        <HieuUngHoatHinh
          danhSach={hieuUngMacDinh}
          nhanVat={[trangThaiCanMat]}
          tiLeNhanVat={1.45}
        />

        {/* Vien truyen tranh bao quanh khung hinh */}
        <rect x={24} y={24} width={1872} height={1032} rx={18} fill="none" stroke="#1A1A1A" strokeWidth={10} />
      </svg>

      {/* Tem chu hieu ung hai goc tren trai (khong che mat nhan vat) */}
      {tt.hienTemChu && chuHieuUng && (
        <div
          style={{
            position: 'absolute',
            top: 96,
            left: 120,
            transform: `rotate(-8deg) scale(${tt.temScale})`,
            backgroundColor: '#DC2626',
            color: '#FEF08A',
            border: '5px solid #1A1A1A',
            borderRadius: 18,
            padding: '14px 34px',
            fontSize: 54,
            fontWeight: 900,
            letterSpacing: 1.5,
            boxShadow: '9px 9px 0px #1A1A1A',
            fontFamily: 'Segoe UI, Arial, sans-serif',
            pointerEvents: 'none',
          }}
        >
          {chuHieuUng}
        </div>
      )}
    </div>
  );
};
