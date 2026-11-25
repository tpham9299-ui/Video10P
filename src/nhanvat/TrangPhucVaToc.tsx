import type {
  DoTuoiNhanVat,
  LoaiCoRau,
  LoaiKieuToc,
} from '../kieu_dai';
import type { Diem2D } from '../xuong/he_xuong';
import { noiSuy } from '../xuong/duong_cong';
import {
  MAU_MUC_TRUYEN_TRANH,
  type HoaTrangHieuLuc,
  type ThamSoAnhSangNhanVat,
} from './hoa_trang_va_anh_sang';

const MUC = MAU_MUC_TRUYEN_TRANH;

/** Ve 1 canh tay mac tay ao truyen tranh 2 sac do + ban tay trang vien muc den #1A1A1A */
export const veCanhTayMacAo = (
  vai: Diem2D,
  khuyu: Diem2D,
  banTay: Diem2D,
  mauTayAo: string,
  mauTayAoBong: string,
  mauDa: string,
  doDayTay: number,
  laTaySau: boolean,
  anhSang: ThamSoAnhSangNhanVat,
) => {
  const d = `M ${vai.x.toFixed(1)} ${vai.y.toFixed(1)} Q ${khuyu.x.toFixed(1)} ${khuyu.y.toFixed(1)} ${banTay.x.toFixed(1)} ${banTay.y.toFixed(1)}`;
  const mauAoDung = laTaySau ? mauTayAoBong : mauTayAo;
  const rBanTay = Math.max(5.2, doDayTay * 0.54);

  return (
    <g>
      {/* Vien muc den #1A1A1A sac net kieu truyen tranh chau Au */}
      <path
        d={d}
        fill="none"
        stroke={MUC}
        strokeWidth={doDayTay + 5.2}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Tay ao mau chinh/bong */}
      <path
        d={d}
        fill="none"
        stroke={mauAoDung}
        strokeWidth={doDayTay + 0.4}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Phu anh sang moi truong phang len tay ao */}
      {anhSang.coPhuMau && (
        <path
          d={d}
          fill="none"
          stroke={anhSang.mauPhu}
          strokeOpacity={anhSang.doMoPhu}
          strokeWidth={doDayTay + 0.4}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      )}
      {/* Co tay ao trang nho gon */}
      <circle
        cx={noiSuy(khuyu.x, banTay.x, 0.84).toFixed(1)}
        cy={noiSuy(khuyu.y, banTay.y, 0.84).toFixed(1)}
        r={doDayTay * 0.48}
        fill="#F8FAFC"
        stroke={MUC}
        strokeWidth={2}
      />
      {/* Ban tay tron trang vien muc den */}
      <circle
        cx={banTay.x.toFixed(1)}
        cy={banTay.y.toFixed(1)}
        r={rBanTay}
        fill={mauDa}
        stroke={MUC}
        strokeWidth={2.6}
      />
      {anhSang.coPhuMau && (
        <circle
          cx={banTay.x.toFixed(1)}
          cy={banTay.y.toFixed(1)}
          r={rBanTay - 1}
          fill={anhSang.mauPhu}
          fillOpacity={anhSang.doMoPhu * 0.85}
        />
      )}
    </g>
  );
};

/** Ve 1 chan mac quan + giay truyen tranh 2 sac do vien muc den #1A1A1A */
export const veChanMacQuan = (
  hong: Diem2D,
  goi: Diem2D,
  banChan: Diem2D,
  dir: number,
  mauQuan: string,
  mauQuanBong: string,
  doDayChan: number,
  laChanSau: boolean,
  anhSang: ThamSoAnhSangNhanVat,
) => {
  const d = `M ${hong.x.toFixed(1)} ${hong.y.toFixed(1)} Q ${goi.x.toFixed(1)} ${goi.y.toFixed(1)} ${banChan.x.toFixed(1)} ${(banChan.y - 4).toFixed(1)}`;
  const mauDung = laChanSau ? mauQuanBong : mauQuan;

  return (
    <g>
      <path
        d={d}
        fill="none"
        stroke={MUC}
        strokeWidth={doDayChan + 5.4}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d={d}
        fill="none"
        stroke={mauDung}
        strokeWidth={doDayChan + 0.6}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {anhSang.coPhuMau && (
        <path
          d={d}
          fill="none"
          stroke={anhSang.mauPhu}
          strokeOpacity={anhSang.doMoPhu}
          strokeWidth={doDayChan + 0.6}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      )}
      {/* Giay co dien tron mem vien muc #1A1A1A */}
      <ellipse
        cx={(banChan.x + 4.5 * dir).toFixed(1)}
        cy={(banChan.y - 2.5).toFixed(1)}
        rx={11.5}
        ry={5.6}
        fill={laChanSau ? '#1F2937' : '#3F2A1D'}
        stroke={MUC}
        strokeWidth={2.5}
      />
      <ellipse
        cx={(banChan.x + 6.5 * dir).toFixed(1)}
        cy={(banChan.y - 4.2).toFixed(1)}
        rx={4}
        ry={1.5}
        fill="#FFFFFF"
        fillOpacity={0.22}
      />
    </g>
  );
};

/**
 * Ve than mac trang phuc chi tiet 2 sac do SVG phang cho du 7 LoaiTrangPhuc,
 * co nhip tho (thoNguc) & lop dong bo anhSangMoiTruong (khong blur, khong filter).
 */
export const veTrangPhucThan = (
  hoaTrang: HoaTrangHieuLuc,
  co: Diem2D,
  diemUonThan: Diem2D,
  hong: Diem2D,
  dir: number,
  thoNguc: number,
  anhSang: ThamSoAnhSangNhanVat,
) => {
  const { trangPhuc, mauAoChinh, mauAoBong, mauAoSang } = hoaTrang;

  const wVai = 18.5 * thoNguc;
  const wEo = 17.5 * thoNguc;
  const wGau =
    trangPhuc === 'ao_choang_hoc_gia' || trangPhuc === 'ao_choang_hy_lap'
      ? 26.5
      : trangPhuc === 'ao_co_an_do' || trangPhuc === 'quan_phuc_co'
        ? 22.5
        : 20.5;
  const daiDuoiHong =
    trangPhuc === 'ao_choang_hoc_gia'
      ? 36
      : trangPhuc === 'ao_choang_hy_lap'
        ? 34
        : trangPhuc === 'ao_co_an_do'
          ? 24
          : trangPhuc === 'quan_phuc_co'
            ? 20
            : 14;

  const yCo = co.y + 3;
  const yGiua = diemUonThan.y + 4;
  const yGau = hong.y + daiDuoiHong;

  // Khung hinh than ao chung uon mem theo cot song
  const dThanAo = `M ${(co.x - wVai).toFixed(1)} ${yCo.toFixed(1)} Q ${(diemUonThan.x - wEo).toFixed(1)} ${yGiua.toFixed(1)} ${(hong.x - wGau).toFixed(1)} ${yGau.toFixed(1)} L ${(hong.x + wGau).toFixed(1)} ${yGau.toFixed(1)} Q ${(diemUonThan.x + wEo).toFixed(1)} ${yGiua.toFixed(1)} ${(co.x + wVai).toFixed(1)} ${yCo.toFixed(1)} Z`;

  // Mang do bong cel-shading 2 sac do phia lung (nguoc huong nhin dir)
  const dMangBong =
    dir > 0
      ? `M ${(co.x - wVai).toFixed(1)} ${yCo.toFixed(1)} Q ${(diemUonThan.x - wEo).toFixed(1)} ${yGiua.toFixed(1)} ${(hong.x - wGau).toFixed(1)} ${yGau.toFixed(1)} L ${(hong.x - 1).toFixed(1)} ${yGau.toFixed(1)} Q ${(diemUonThan.x - 3).toFixed(1)} ${yGiua.toFixed(1)} ${(co.x - 2).toFixed(1)} ${yCo.toFixed(1)} Z`
      : `M ${(co.x + 2).toFixed(1)} ${yCo.toFixed(1)} Q ${(diemUonThan.x + 3).toFixed(1)} ${yGiua.toFixed(1)} ${(hong.x + 1).toFixed(1)} ${yGau.toFixed(1)} L ${(hong.x + wGau).toFixed(1)} ${yGau.toFixed(1)} Q ${(diemUonThan.x + wEo).toFixed(1)} ${yGiua.toFixed(1)} ${(co.x + wVai).toFixed(1)} ${yCo.toFixed(1)} Z`;

  // Vien sang mong rim-light phia truoc dong bo anhSangMoiTruong
  const dVienSang =
    dir > 0
      ? `M ${(co.x + wVai - 2).toFixed(1)} ${(yCo + 4).toFixed(1)} Q ${(diemUonThan.x + wEo - 2).toFixed(1)} ${yGiua.toFixed(1)} ${(hong.x + wGau - 3).toFixed(1)} ${(yGau - 4).toFixed(1)}`
      : `M ${(co.x - wVai + 2).toFixed(1)} ${(yCo + 4).toFixed(1)} Q ${(diemUonThan.x - wEo + 2).toFixed(1)} ${yGiua.toFixed(1)} ${(hong.x - wGau + 3).toFixed(1)} ${(yGau - 4).toFixed(1)}`;

  const veChiTietRieng = () => {
    switch (trangPhuc) {
      case 'ao_vest_co_dien':
        return (
          <g>
            {/* Ao so mi trang hinh chu V & ca vat / no */}
            <polygon
              points={`${(co.x - 9).toFixed(1)},${yCo.toFixed(1)} ${(co.x + 9).toFixed(1)},${yCo.toFixed(1)} ${(diemUonThan.x + 4 * dir).toFixed(1)},${(yGiua + 10).toFixed(1)}`}
              fill="#FFFDF7"
              stroke={MUC}
              strokeWidth={2}
              strokeLinejoin="round"
            />
            {/* Ca vat co dien */}
            <polygon
              points={`${(co.x + 1 * dir).toFixed(1)},${(yCo + 2).toFixed(1)} ${(co.x + 5 * dir).toFixed(1)},${(yCo + 6).toFixed(1)} ${(diemUonThan.x + 5 * dir).toFixed(1)},${(yGiua + 8).toFixed(1)} ${(diemUonThan.x + 1 * dir).toFixed(1)},${(yGiua + 4).toFixed(1)}`}
              fill="#B91C1C"
              stroke={MUC}
              strokeWidth={1.6}
              strokeLinejoin="round"
            />
            {/* Ve ao vest 2 ben sac net */}
            <polygon
              points={`${(co.x - 10).toFixed(1)},${yCo.toFixed(1)} ${(co.x - 15).toFixed(1)},${(yCo + 16).toFixed(1)} ${(diemUonThan.x + 3 * dir).toFixed(1)},${(yGiua + 11).toFixed(1)}`}
              fill={mauAoSang}
              stroke={MUC}
              strokeWidth={1.8}
              strokeLinejoin="round"
            />
            <polygon
              points={`${(co.x + 10).toFixed(1)},${yCo.toFixed(1)} ${(co.x + 15).toFixed(1)},${(yCo + 16).toFixed(1)} ${(diemUonThan.x + 3 * dir).toFixed(1)},${(yGiua + 11).toFixed(1)}`}
              fill={mauAoSang}
              stroke={MUC}
              strokeWidth={1.8}
              strokeLinejoin="round"
            />
            {/* Hang cuc ao dong & nap tui */}
            <line
              x1={(diemUonThan.x + 3 * dir).toFixed(1)}
              y1={(yGiua + 10).toFixed(1)}
              x2={(hong.x + 3 * dir).toFixed(1)}
              y2={yGau.toFixed(1)}
              stroke={MUC}
              strokeWidth={2.2}
            />
            {[0.45, 0.72].map((t) => (
              <circle
                key={`cuc-v-${t}`}
                cx={noiSuy(diemUonThan.x, hong.x, t) + 7.5 * dir}
                cy={noiSuy(yGiua + 6, yGau - 2, t)}
                r={2.5}
                fill="#FACC15"
                stroke={MUC}
                strokeWidth={1.3}
              />
            ))}
            <line
              x1={(hong.x + 8 * dir).toFixed(1)}
              y1={(yGau - 10).toFixed(1)}
              x2={(hong.x + 17 * dir).toFixed(1)}
              y2={(yGau - 10).toFixed(1)}
              stroke={MUC}
              strokeWidth={2}
              strokeLinecap="round"
            />
          </g>
        );

      case 'ao_choang_hoc_gia':
        return (
          <g>
            {/* Nep gap vai doc & vat ao choang rong */}
            <path
              d={`M ${(co.x - 16).toFixed(1)} ${(yCo + 2).toFixed(1)} Q ${co.x.toFixed(1)} ${(yCo + 18).toFixed(1)} ${(co.x + 16).toFixed(1)} ${(yCo + 2).toFixed(1)}`}
              fill={mauAoSang}
              stroke={MUC}
              strokeWidth={2.2}
            />
            <line
              x1={(co.x + 3 * dir).toFixed(1)}
              y1={(yCo + 12).toFixed(1)}
              x2={(hong.x + 4 * dir).toFixed(1)}
              y2={yGau.toFixed(1)}
              stroke={MUC}
              strokeWidth={2.2}
            />
            <line
              x1={(diemUonThan.x - 8 * dir).toFixed(1)}
              y1={(yGiua - 4).toFixed(1)}
              x2={(hong.x - 13 * dir).toFixed(1)}
              y2={(yGau - 3).toFixed(1)}
              stroke={MUC}
              strokeOpacity={0.55}
              strokeWidth={1.8}
              strokeLinecap="round"
            />
            {/* Dai lung vai + khoa vang co ao */}
            <rect
              x={hong.x - wEo + 1}
              y={hong.y - 6}
              width={(wEo - 1) * 2}
              height={7.5}
              rx={3}
              fill="#78350F"
              stroke={MUC}
              strokeWidth={1.8}
            />
            <circle
              cx={co.x + 2 * dir}
              cy={yCo + 10}
              r={4.2}
              fill="#FACC15"
              stroke={MUC}
              strokeWidth={1.7}
            />
          </g>
        );

      case 'ao_co_an_do':
        return (
          <g>
            {/* Co ao dung Kurta & nep cuc giua */}
            <rect
              x={co.x - 10}
              y={yCo - 4}
              width={20}
              height={9}
              rx={4}
              fill={mauAoSang}
              stroke={MUC}
              strokeWidth={2}
            />
            <rect
              x={co.x + 1 * dir - 3}
              y={yCo + 5}
              width={6}
              height={24}
              rx={2}
              fill="#FEF3C7"
              stroke={MUC}
              strokeWidth={1.6}
            />
            {/* Dai khan khoac vai cheo truyen thong (angavastram) co vien vang */}
            <path
              d={`M ${(co.x - 14 * dir).toFixed(1)} ${(yCo + 2).toFixed(1)} Q ${diemUonThan.x.toFixed(1)} ${(yGiua + 10).toFixed(1)} ${(hong.x + 18 * dir).toFixed(1)} ${(yGau - 16).toFixed(1)} L ${(hong.x + 12 * dir).toFixed(1)} ${(yGau - 4).toFixed(1)} Q ${(diemUonThan.x - 4 * dir).toFixed(1)} ${(yGiua + 16).toFixed(1)} ${(co.x - 17 * dir).toFixed(1)} ${(yCo + 13).toFixed(1)} Z`}
              fill="#FEF3C7"
              stroke={MUC}
              strokeWidth={2}
              strokeLinejoin="round"
            />
            <path
              d={`M ${(co.x - 14 * dir).toFixed(1)} ${(yCo + 6).toFixed(1)} Q ${diemUonThan.x.toFixed(1)} ${(yGiua + 13).toFixed(1)} ${(hong.x + 15 * dir).toFixed(1)} ${(yGau - 10).toFixed(1)}`}
              fill="none"
              stroke="#D97706"
              strokeWidth={2.4}
            />
          </g>
        );

      case 'ao_len_mua_dong':
        return (
          <g>
            {/* Co lo len am ap */}
            <rect
              x={co.x - 14}
              y={yCo - 6}
              width={28}
              height={12}
              rx={5}
              fill="#F8FAFC"
              stroke={MUC}
              strokeWidth={2.2}
            />
            {/* Hoa tiet soc len ngang + nep gau ao */}
            <line
              x1={diemUonThan.x - wEo + 3}
              y1={yGiua - 4}
              x2={diemUonThan.x + wEo - 3}
              y2={yGiua - 4}
              stroke={mauAoSang}
              strokeWidth={4.5}
              strokeLinecap="round"
            />
            <line
              x1={diemUonThan.x - wEo + 3}
              y1={yGiua + 5}
              x2={diemUonThan.x + wEo - 3}
              y2={yGiua + 5}
              stroke="#FEF3C7"
              strokeOpacity={0.75}
              strokeWidth={3}
              strokeLinecap="round"
            />
            <rect
              x={hong.x - wGau + 2}
              y={yGau - 8}
              width={(wGau - 2) * 2}
              height={8}
              rx={3}
              fill={mauAoBong}
              stroke={MUC}
              strokeWidth={1.8}
            />
          </g>
        );

      case 'ao_choang_hy_lap':
        return (
          <g>
            {/* Nen ao chiton trang nga + dai choang cheo vai mauChuDao + vien vang co dai */}
            <path d={dThanAo} fill="#FFFBEB" stroke={MUC} strokeWidth={2.8} strokeLinejoin="round" />
            <path d={dMangBong} fill="#E7DFC8" />
            <path
              d={`M ${(co.x - 16 * dir).toFixed(1)} ${yCo.toFixed(1)} L ${(co.x + 6 * dir).toFixed(1)} ${(yCo + 6).toFixed(1)} L ${(hong.x + 24 * dir).toFixed(1)} ${(yGau - 6).toFixed(1)} L ${(hong.x - 8 * dir).toFixed(1)} ${yGau.toFixed(1)} Z`}
              fill={mauAoChinh}
              stroke={MUC}
              strokeWidth={2.4}
              strokeLinejoin="round"
            />
            {/* Mang bong cheo tren dai toga */}
            <path
              d={`M ${(co.x - 16 * dir).toFixed(1)} ${yCo.toFixed(1)} L ${(co.x - 6 * dir).toFixed(1)} ${(yCo + 3).toFixed(1)} L ${(hong.x + 4 * dir).toFixed(1)} ${yGau.toFixed(1)} L ${(hong.x - 8 * dir).toFixed(1)} ${yGau.toFixed(1)} Z`}
              fill={mauAoBong}
            />
            {/* Vien vang gau ao Hy Lap */}
            <line
              x1={hong.x - wGau + 4}
              y1={yGau - 5}
              x2={hong.x + wGau - 4}
              y2={yGau - 5}
              stroke="#D97706"
              strokeWidth={3.2}
            />
            {/* Tram cai vai bang vang */}
            <circle cx={co.x - 11 * dir} cy={yCo + 5} r={4.2} fill="#FACC15" stroke={MUC} strokeWidth={1.6} />
          </g>
        );

      case 'quan_phuc_co':
        return (
          <g>
            {/* Co dung + cau vai vang 2 ben */}
            <rect x={co.x - 11} y={yCo - 5} width={22} height={9} rx={3} fill="#991B1B" stroke={MUC} strokeWidth={2} />
            <ellipse cx={co.x - 17} cy={yCo + 3} rx={7} ry={3.8} fill="#FACC15" stroke={MUC} strokeWidth={1.8} />
            <ellipse cx={co.x + 17} cy={yCo + 3} rx={7} ry={3.8} fill="#FACC15" stroke={MUC} strokeWidth={1.8} />
            {/* Dai cheo quan phuc + that lung */}
            <line
              x1={co.x - 12 * dir}
              y1={yCo + 4}
              x2={hong.x + 14 * dir}
              y2={hong.y + 4}
              stroke="#FEF3C7"
              strokeWidth={5}
            />
            <rect
              x={hong.x - wEo}
              y={hong.y - 3}
              width={wEo * 2}
              height={8}
              rx={2}
              fill="#1E293B"
              stroke={MUC}
              strokeWidth={1.8}
            />
            <rect
              x={hong.x + 2 * dir - 4}
              y={hong.y - 3}
              width={8}
              height={8}
              rx={1.5}
              fill="#FACC15"
              stroke={MUC}
              strokeWidth={1.6}
            />
            {/* 2 hang cuc dong */}
            {[0.3, 0.55].map((t) => (
              <g key={`cuc-qp-${t}`}>
                <circle cx={noiSuy(co.x, hong.x, t) - 5} cy={noiSuy(yCo + 8, hong.y - 4, t)} r={2.3} fill="#FACC15" stroke={MUC} strokeWidth={1.1} />
                <circle cx={noiSuy(co.x, hong.x, t) + 5} cy={noiSuy(yCo + 8, hong.y - 4, t)} r={2.3} fill="#FACC15" stroke={MUC} strokeWidth={1.1} />
              </g>
            ))}
          </g>
        );

      case 'thuong_dan':
      default:
        return (
          <g>
            {/* Co ao gap gon gang + day lung da co khoa dong */}
            <polygon
              points={`${(co.x - 11).toFixed(1)},${yCo.toFixed(1)} ${co.x.toFixed(1)},${(yCo + 11).toFixed(1)} ${(co.x - 3).toFixed(1)},${(yCo + 14).toFixed(1)} ${(co.x - 14).toFixed(1)},${(yCo + 5).toFixed(1)}`}
              fill="#FFFDF7"
              stroke={MUC}
              strokeWidth={1.8}
              strokeLinejoin="round"
            />
            <polygon
              points={`${(co.x + 11).toFixed(1)},${yCo.toFixed(1)} ${co.x.toFixed(1)},${(yCo + 11).toFixed(1)} ${(co.x + 3).toFixed(1)},${(yCo + 14).toFixed(1)} ${(co.x + 14).toFixed(1)},${(yCo + 5).toFixed(1)}`}
              fill="#FFFDF7"
              stroke={MUC}
              strokeWidth={1.8}
              strokeLinejoin="round"
            />
            <line
              x1={(co.x + 1.5 * dir).toFixed(1)}
              y1={(yCo + 11).toFixed(1)}
              x2={(hong.x + 1.5 * dir).toFixed(1)}
              y2={(hong.y + 4).toFixed(1)}
              stroke={MUC}
              strokeOpacity={0.55}
              strokeWidth={1.8}
            />
            <rect
              x={hong.x - wEo + 1}
              y={hong.y - 1}
              width={(wEo - 1) * 2}
              height={7.5}
              rx={3}
              fill="#78350F"
              stroke={MUC}
              strokeWidth={1.8}
            />
            <rect
              x={hong.x + 2 * dir - 3.5}
              y={hong.y - 1}
              width={7}
              height={7.5}
              rx={1.5}
              fill="#FACC15"
              stroke={MUC}
              strokeWidth={1.5}
            />
          </g>
        );
    }
  };

  return (
    <g>
      {/* Nen ao chinh + mang bong 2 sac do phang (rieng Hy Lap tu ve nen trang nga ben trong) */}
      {trangPhuc !== 'ao_choang_hy_lap' && (
        <>
          <path d={dThanAo} fill={mauAoChinh} stroke={MUC} strokeWidth={3} strokeLinejoin="round" />
          <path d={dMangBong} fill={mauAoBong} />
        </>
      )}

      {veChiTietRieng()}

      {/* Vien muc ngoai cung sac net giup hinh khoi sach se */}
      <path d={dThanAo} fill="none" stroke={MUC} strokeWidth={3} strokeLinejoin="round" />

      {/* Dong bo anhSangMoiTruong: lop phu mau phang (0.08..0.22) + rim light mong */}
      {anhSang.coPhuMau && (
        <>
          <path d={dThanAo} fill={anhSang.mauPhu} fillOpacity={anhSang.doMoPhu} />
          {anhSang.doMoToi > 0.01 && (
            <path d={dMangBong} fill={anhSang.mauToi} fillOpacity={anhSang.doMoToi} />
          )}
          {anhSang.doMoVienSang > 0.01 && (
            <path
              d={dVienSang}
              fill="none"
              stroke={anhSang.mauVienSang}
              strokeOpacity={anhSang.doMoVienSang}
              strokeWidth={2.4}
              strokeLinecap="round"
            />
          )}
        </>
      )}
    </g>
  );
};

/** Ve 7 kieu toc & mu lich su sac net co bong 2 sac do tren dau (toa do cuc bo dau: tam 0,0) */
export const veKieuTocNhanVat = (
  kieuToc: LoaiKieuToc | null,
  doTuoi: DoTuoiNhanVat,
  dir: number,
  mauChuDao: string,
  anhSang: ThamSoAnhSangNhanVat,
) => {
  if (!kieuToc) {
    return null;
  }

  const mauToc = doTuoi === 'gia' ? '#E2E8F0' : '#2C241E';
  const mauTocBong = doTuoi === 'gia' ? '#94A3B8' : '#161210';

  const veToc = () => {
    switch (kieuToc) {
      case 'gon_gang':
        return (
          <g>
            <path
              d={`M ${(-24 * dir).toFixed(1)} -4 Q ${(-26 * dir).toFixed(1)} -25 ${(-4 * dir).toFixed(1)} -28 Q ${(18 * dir).toFixed(1)} -30 ${(24 * dir).toFixed(1)} -12 Q ${(12 * dir).toFixed(1)} -18 ${(-6 * dir).toFixed(1)} -16 Q ${(-16 * dir).toFixed(1)} -14 ${(-24 * dir).toFixed(1)} -4 Z`}
              fill={mauToc}
              stroke={MUC}
              strokeWidth={2.5}
              strokeLinejoin="round"
            />
            <path
              d={`M ${(-18 * dir).toFixed(1)} -12 Q ${(-8 * dir).toFixed(1)} -22 ${(10 * dir).toFixed(1)} -21`}
              fill="none"
              stroke={mauTocBong}
              strokeWidth={2.2}
              strokeLinecap="round"
            />
          </g>
        );

      case 'xoan_co_dien':
        return (
          <g>
            <path
              d="M -26 6 Q -31 -14 -16 -27 Q 0 -33 16 -27 Q 31 -14 26 6 Q 21 -8 14 -16 Q 0 -22 -14 -16 Q -21 -8 -26 6 Z"
              fill={mauToc}
              stroke={MUC}
              strokeWidth={2.4}
              strokeLinejoin="round"
            />
            <circle cx={-23} cy={-4} r={6.5} fill={mauToc} stroke={MUC} strokeWidth={2.1} />
            <circle cx={-24} cy={7} r={5.8} fill={mauTocBong} stroke={MUC} strokeWidth={2} />
            <circle cx={23} cy={-4} r={6.5} fill={mauToc} stroke={MUC} strokeWidth={2.1} />
            <circle cx={24} cy={7} r={5.8} fill={mauTocBong} stroke={MUC} strokeWidth={2} />
          </g>
        );

      case 'toc_bac_dai':
        return (
          <g>
            <path
              d="M -27 18 Q -32 -12 -15 -27 Q 0 -32 15 -27 Q 32 -12 27 18 Q 20 14 18 4 Q 21 -12 12 -18 Q 0 -22 -12 -18 Q -21 -12 -18 4 Q -20 14 -27 18 Z"
              fill="#F1F5F9"
              stroke={MUC}
              strokeWidth={2.4}
              strokeLinejoin="round"
            />
            <path d="M -24 2 Q -25 10 -22 16" fill="none" stroke="#94A3B8" strokeWidth={2.2} strokeLinecap="round" />
            <path d="M 24 2 Q 25 10 22 16" fill="none" stroke="#94A3B8" strokeWidth={2.2} strokeLinecap="round" />
          </g>
        );

      case 'khan_quan':
        return (
          <g transform="translate(0, -16)">
            <ellipse cx={0} cy={-2} rx={27} ry={15} fill="#FEF3C7" stroke={MUC} strokeWidth={2.6} />
            <path d="M -24 2 Q -8 -12 16 -8" fill="none" stroke="#D97706" strokeWidth={3} strokeLinecap="round" />
            <path d="M -18 -8 Q 4 -15 22 1" fill="none" stroke={MUC} strokeWidth={2} strokeLinecap="round" />
            <circle cx={4 * dir} cy={-4} r={4.2} fill={mauChuDao} stroke={MUC} strokeWidth={1.7} />
          </g>
        );

      case 'mu_rong_vanh':
        return (
          <g transform="translate(0, -19)">
            <ellipse cx={0} cy={2} rx={36} ry={7.5} fill="#44403C" stroke={MUC} strokeWidth={2.5} />
            <path
              d="M -20 1 Q -18 -20 0 -20 Q 18 -20 20 1 Z"
              fill="#57534E"
              stroke={MUC}
              strokeWidth={2.5}
              strokeLinejoin="round"
            />
            <rect x={-19} y={-6} width={38} height={6} rx={2} fill={mauChuDao} stroke={MUC} strokeWidth={1.6} />
          </g>
        );

      case 'mu_noi':
        return (
          <g transform={`translate(${(-2 * dir).toFixed(1)}, -21) rotate(${(-9 * dir).toFixed(1)})`}>
            <ellipse cx={0} cy={0} rx={25} ry={10.5} fill={mauChuDao} stroke={MUC} strokeWidth={2.5} />
            <path d="M -22 2 Q 0 8 22 2" fill="none" stroke={MUC} strokeWidth={2.4} />
            <path d="M 0 -10 Q 3 -15 5 -16" fill="none" stroke={MUC} strokeWidth={3} strokeLinecap="round" />
          </g>
        );

      case 'hoi_hoi':
        return (
          <g>
            {/* Hai cum toc hai ben thai duong + dinh dau hoi kieu giao su co dien */}
            <path
              d="M -26 -2 Q -28 -14 -20 -17 Q -18 -8 -21 2 Z"
              fill={mauToc}
              stroke={MUC}
              strokeWidth={2}
              strokeLinejoin="round"
            />
            <path
              d="M 26 -2 Q 28 -14 20 -17 Q 18 -8 21 2 Z"
              fill={mauToc}
              stroke={MUC}
              strokeWidth={2}
              strokeLinejoin="round"
            />
            <path d="M -10 -20 Q -4 -23 2 -21" fill="none" stroke="#FFFFFF" strokeOpacity={0.65} strokeWidth={2.2} strokeLinecap="round" />
          </g>
        );

      default:
        return null;
    }
  };

  return (
    <g>
      {veToc()}
      {anhSang.coPhuMau && kieuToc !== 'hoi_hoi' && (
        <ellipse
          cx={0}
          cy={-18}
          rx={24}
          ry={12}
          fill={anhSang.mauPhu}
          fillOpacity={anhSang.doMoPhu * 0.55}
        />
      )}
    </g>
  );
};

/** Ve 4 kieu rau dac trung (dat lech khon kheo de KHONG che mieng lip-sync 30fps) */
export const veRauNhanVat = (
  coRau: LoaiCoRau,
  doTuoi: DoTuoiNhanVat,
  dir: number,
  nhinThangOngKinh: boolean,
) => {
  if (coRau === 'khong') {
    return null;
  }

  const miengX = nhinThangOngKinh ? 0 : 7.5 * dir;
  const mauRau =
    coRau === 'rau_bac_dai' || doTuoi === 'gia' ? '#F1F5F9' : '#3B2F2F';
  const mauRauBong =
    coRau === 'rau_bac_dai' || doTuoi === 'gia' ? '#CBD5E1' : '#1F1818';

  switch (coRau) {
    case 'ria_mep':
      return (
        <path
          d={`M ${(miengX - 10).toFixed(1)} 5.4 Q ${(miengX - 4).toFixed(1)} 1.2 ${miengX.toFixed(1)} 4.2 Q ${(miengX + 4).toFixed(1)} 1.2 ${(miengX + 10).toFixed(1)} 5.4 Q ${(miengX + 5).toFixed(1)} 6.8 ${miengX.toFixed(1)} 5.6 Q ${(miengX - 5).toFixed(1)} 6.8 ${(miengX - 10).toFixed(1)} 5.4 Z`}
          fill={mauRau}
          stroke={MUC}
          strokeWidth={1.6}
          strokeLinejoin="round"
        />
      );

    case 'rau_quai_non':
      return (
        <g>
          {/* Vien rau om ham & cam, chua khoang thoang cho mieng lip-sync */}
          <path
            d={`M ${(miengX - 15).toFixed(1)} 7 Q ${(miengX - 14).toFixed(1)} 23 ${miengX.toFixed(1)} 25 Q ${(miengX + 14).toFixed(1)} 23 ${(miengX + 15).toFixed(1)} 7 Q ${(miengX + 10).toFixed(1)} 17 ${miengX.toFixed(1)} 17 Q ${(miengX - 10).toFixed(1)} 17 ${(miengX - 15).toFixed(1)} 7 Z`}
            fill={mauRau}
            stroke={MUC}
            strokeWidth={1.8}
            strokeLinejoin="round"
          />
          <path
            d={`M ${(miengX - 9).toFixed(1)} 5.2 Q ${(miengX - 4).toFixed(1)} 1.8 ${miengX.toFixed(1)} 4.2 Q ${(miengX + 4).toFixed(1)} 1.8 ${(miengX + 9).toFixed(1)} 5.2`}
            fill="none"
            stroke={MUC}
            strokeWidth={2.4}
            strokeLinecap="round"
          />
        </g>
      );

    case 'rau_bac_dai':
      return (
        <g>
          {/* Chom rau bac dai chay xuong tu duoi cam */}
          <path
            d={`M ${(miengX - 13).toFixed(1)} 13 Q ${(miengX - 12).toFixed(1)} 32 ${miengX.toFixed(1)} 40 Q ${(miengX + 12).toFixed(1)} 32 ${(miengX + 13).toFixed(1)} 13 Q ${(miengX + 6).toFixed(1)} 17 ${miengX.toFixed(1)} 17 Q ${(miengX - 6).toFixed(1)} 17 ${(miengX - 13).toFixed(1)} 13 Z`}
            fill={mauRau}
            stroke={MUC}
            strokeWidth={2.1}
            strokeLinejoin="round"
          />
          <path
            d={`M ${(miengX - 5).toFixed(1)} 21 Q ${(miengX - 3).toFixed(1)} 30 ${miengX.toFixed(1)} 36`}
            fill="none"
            stroke={mauRauBong}
            strokeWidth={1.8}
            strokeLinecap="round"
          />
          <path
            d={`M ${(miengX + 5).toFixed(1)} 21 Q ${(miengX + 3).toFixed(1)} 30 ${miengX.toFixed(1)} 35`}
            fill="none"
            stroke={mauRauBong}
            strokeWidth={1.6}
            strokeLinecap="round"
          />
          <path
            d={`M ${(miengX - 9.5).toFixed(1)} 5.2 Q ${(miengX - 4).toFixed(1)} 1.6 ${miengX.toFixed(1)} 4.2 Q ${(miengX + 4).toFixed(1)} 1.6 ${(miengX + 9.5).toFixed(1)} 5.2`}
            fill={mauRau}
            stroke={MUC}
            strokeWidth={1.6}
            strokeLinejoin="round"
          />
        </g>
      );

    default:
      return null;
  }
};
