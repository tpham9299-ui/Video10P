import React from 'react';
import { Img, staticFile, useCurrentFrame } from 'remotion';
import type { BangMau, Canh } from '../kieu_dai';
import { DaoCu } from '../daocu/DaoCu';
import { CongThucMath } from '../daocu/CongThucMath';
import { tinhBienDoiBaoChiCo } from './ke_chuyen_v35_logic';

type Props = {
  canh: Canh;
  bangMau: BangMau;
};

/**
 * CanhBaoChiCo (v3.5):
 * - To bao giay co xoay/phong ra man hinh tat dinh 100% (do hoa phang sac net)
 * - Hien thi tieuDeBao giat gan, anh/dao cu minh hoa nho va tieuDePhu hai huoc.
 */
export const CanhBaoChiCo: React.FC<Props> = ({ canh }) => {
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const bd = tinhBienDoiBaoChiCo(frame, thoiLuong);
  const data = canh.baoChiCo;

  const tenToBao = (data?.tenToBao || 'NHẬT BÁO TOÁN HỌC THẾ KỶ').trim().toUpperCase();
  const ngayPhatHanh = (data?.ngayPhatHanh || canh.namMoc || 'ẤN BẢN ĐẶC BIỆT').trim().toUpperCase();
  const tieuDeBao = (data?.tieuDeBao || canh.tieuDeNho || 'CHẤN ĐỘNG GIỚI HỌC THUẬT!').trim().toUpperCase();
  const tieuDePhu = (data?.tieuDePhu || '').trim();
  const nhanAnhMinhHoa = (data?.nhanAnhMinhHoa || 'Ảnh minh họa tại hiện trường').trim();
  const daoCuMinhHoa = data?.daoCuMinhHoa ?? canh.daoCu?.[0]?.loai ?? 'cuon_giay';
  const congThucMinhHoa = (data?.congThucMinhHoa || canh.congThucLatex?.[0]?.latex || '').trim();

  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        backgroundColor: '#27201A',
        overflow: 'hidden',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      {/* Tia nen kich tinh phang (khong blur) */}
      <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: 'absolute', inset: 0 }}>
        <rect x={0} y={0} width={1920} height={1080} fill="#2A2118" />
        {Array.from({ length: 18 }).map((_, i) => {
          const a1 = (i / 18) * Math.PI * 2;
          const a2 = ((i + 0.42) / 18) * Math.PI * 2;
          const r = 1350;
          return (
            <polygon
              key={`bao-tia-${i}`}
              points={`960,540 ${(960 + Math.cos(a1) * r).toFixed(1)},${(540 + Math.sin(a1) * r).toFixed(1)} ${(960 + Math.cos(a2) * r).toFixed(1)},${(540 + Math.sin(a2) * r).toFixed(1)}`}
              fill="#F59E0B"
              fillOpacity={0.12}
            />
          );
        })}
      </svg>

      {/* To bao giay co xoay phong ra giua khung hinh */}
      <div
        style={{
          width: 1360,
          minHeight: 770,
          backgroundColor: '#F6ECD4',
          border: '6px solid #1A1A1A',
          borderRadius: 8,
          boxShadow: '18px 20px 0px rgba(10, 8, 6, 0.72)',
          padding: '30px 44px 36px',
          boxSizing: 'border-box',
          opacity: bd.opacity,
          transform: `rotate(${bd.xoayDeg}deg) scale(${bd.scale})`,
          fontFamily: 'Georgia, "Times New Roman", serif',
          color: '#1A1A1A',
          position: 'relative',
        }}
      >
        {/* Dau moc TIN NONG goc tren phai */}
        <div
          style={{
            position: 'absolute',
            top: 22,
            right: 30,
            backgroundColor: '#B91C1C',
            color: '#FEF08A',
            border: '3px solid #1A1A1A',
            padding: '5px 16px',
            fontSize: 20,
            fontWeight: 900,
            letterSpacing: 1.8,
            transform: 'rotate(5deg)',
            fontFamily: 'Segoe UI, Arial, sans-serif',
          }}
        >
          TIN CHẤN ĐỘNG
        </div>

        {/* Masthead ten to bao */}
        <div
          style={{
            borderBottom: '5px double #1A1A1A',
            paddingBottom: 12,
            marginBottom: 16,
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: 44, fontWeight: 900, letterSpacing: 4 }}>{tenToBao}</div>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginTop: 8,
              borderTop: '2px solid #1A1A1A',
              paddingTop: 6,
              fontSize: 18,
              fontWeight: 700,
              color: '#57534E',
              fontFamily: 'Segoe UI, Arial, sans-serif',
            }}
          >
            <span>SỐ ĐẶC BIỆT • LỊCH SỬ TOÁN HỌC</span>
            <span>{ngayPhatHanh}</span>
            <span>GIÁ BÁN: 1 NỤ CƯỜI</span>
          </div>
        </div>

        {/* Dong tieu de giat gan */}
        <div
          style={{
            fontSize: tieuDeBao.length > 42 ? 52 : 64,
            fontWeight: 900,
            lineHeight: 1.1,
            textAlign: 'center',
            marginBottom: 16,
            letterSpacing: -0.5,
            fontFamily: 'Segoe UI, Arial, sans-serif',
          }}
        >
          {tieuDeBao}
        </div>

        {/* Tieu de phu hai huoc */}
        {tieuDePhu && bd.hienTieuDePhu && (
          <div
            style={{
              backgroundColor: '#1A1A1A',
              color: '#FEF08A',
              padding: '10px 22px',
              fontSize: 26,
              fontWeight: 800,
              textAlign: 'center',
              marginBottom: 22,
              fontFamily: 'Segoe UI, Arial, sans-serif',
            }}
          >
            {tieuDePhu}
          </div>
        )}

        {/* Phan than bao 2 cot: anh minh hoa nho ben trai + bai bao cach dieu ben phai */}
        <div style={{ display: 'flex', gap: 30, alignItems: 'stretch' }}>
          {/* Khung anh minh hoa nho */}
          <div
            style={{
              width: 560,
              flexShrink: 0,
              border: '4px solid #1A1A1A',
              backgroundColor: '#E8D8B2',
              padding: 12,
              boxSizing: 'border-box',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div
              style={{
                width: '100%',
                height: 290,
                backgroundColor: '#1E293B',
                border: '2.5px solid #1A1A1A',
                position: 'relative',
                overflow: 'hidden',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
              }}
            >
              {canh.anhBoiCanh ? (
                <Img
                  src={staticFile(canh.anhBoiCanh)}
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
              ) : (
                <svg width={520} height={290} viewBox="0 0 520 290">
                  <rect x={0} y={0} width={520} height={290} fill="#1E293B" />
                  <circle cx={260} cy={145} r={96} fill="#FDE68A" fillOpacity={0.18} />
                  <DaoCu daoCu={{ loai: daoCuMinhHoa, x: 260, y: 155, tiLe: 1.55, mau: '#FEF08A' }} />
                </svg>
              )}
              {congThucMinhHoa && (
                <div
                  style={{
                    position: 'absolute',
                    bottom: 10,
                    right: 10,
                    backgroundColor: 'rgba(15, 23, 42, 0.92)',
                    border: '2px solid #FACC15',
                    borderRadius: 10,
                    padding: '6px 14px',
                  }}
                >
                  <CongThucMath latex={congThucMinhHoa} fontSize={28} mau="#FEF08A" />
                </div>
              )}
            </div>
            <div
              style={{
                marginTop: 8,
                fontSize: 18,
                fontStyle: 'italic',
                fontWeight: 700,
                color: '#44403C',
                textAlign: 'center',
                fontFamily: 'Segoe UI, Arial, sans-serif',
              }}
            >
              {nhanAnhMinhHoa}
            </div>
          </div>

          {/* Cot bai bao kieu giay in co */}
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <div
              style={{
                fontSize: 25,
                fontWeight: 700,
                lineHeight: 1.45,
                color: '#292524',
                borderLeft: '5px solid #B91C1C',
                paddingLeft: 18,
                fontFamily: 'Segoe UI, Arial, sans-serif',
              }}
            >
              {canh.loiThoai}
            </div>

            {/* Cac dong chu gia bao in tao ket cau to bao chan that */}
            <div style={{ display: 'flex', gap: 20, marginTop: 18 }}>
              {[0, 1].map((col) => (
                <div key={`bcol-${col}`} style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 10 }}>
                  {[0.96, 0.88, 0.92, 0.74].map((w, li) => (
                    <div
                      key={`bl-${col}-${li}`}
                      style={{
                        height: 8,
                        width: `${Math.round(w * 100)}%`,
                        backgroundColor: '#78716C',
                        opacity: 0.35,
                        borderRadius: 2,
                      }}
                    />
                  ))}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
