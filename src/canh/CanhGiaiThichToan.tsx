import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { DaoCu } from '../daocu/DaoCu';
import { CongThucMath } from '../daocu/CongThucMath';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngTanCong } from '../vfx/HieuUngTanCong';

type Props = {
  canh: Canh;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

/**
 * Bo cuc chia doi 35% khu vuc nguoi que (trai) - 65% bang den KaTeX (phai).
 */
export const CanhGiaiThichToan: React.FC<Props> = ({
  canh,
  bangMau,
  banDoNhanVat,
}) => {
  const frame = useCurrentFrame();

  return (
    <MayQuayDong camera={canh.camera} hieuUngTanCong={canh.hieuUngTanCong}>
      <div
        style={{
          position: 'absolute',
          top: 72,
          left: 64,
          right: 64,
          bottom: 168,
          display: 'flex',
          gap: 32,
        }}
      >
        {/* 35% ben trai: vung nguoi que */}
        <div
          style={{
            flex: '0 0 35%',
            position: 'relative',
            borderRadius: 20,
            border: `2px solid ${bangMau.luoi}`,
            backgroundColor: '#0F172A',
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              position: 'absolute',
              top: 20,
              left: 24,
              color: bangMau.nhanManh,
              fontSize: 18,
              fontWeight: 700,
              letterSpacing: 1.2,
            }}
          >
            PHÂN TÍCH TRỰC QUAN
          </div>
          <svg width="100%" height="100%" viewBox="0 0 640 840">
            <line
              x1={60}
              y1={700}
              x2={580}
              y2={700}
              stroke={bangMau.luoi}
              strokeWidth={4}
              strokeLinecap="round"
            />
            {canh.daoCu?.map((dc, idx) => (
              <DaoCu key={`${dc.loai}-${idx}`} daoCu={dc} />
            ))}
            {canh.nhanVat.map((nv, idx) => {
              const tt = banDoNhanVat[nv.id];
              if (!tt) return null;
              return (
                <NguoiQueDong
                  key={`${nv.id}-${idx}`}
                  thongTin={tt}
                  trangThai={{ ...nv, x: nv.x > 640 ? 320 : nv.x, y: nv.y > 760 ? 700 : nv.y }}
                  tiLe={1.25}
                />
              );
            })}
            <HieuUngTanCong danhSach={canh.hieuUngTanCong} />
          </svg>
        </div>

        {/* 65% ben phai: bang den KaTeX */}
        <div
          style={{
            flex: '1 1 65%',
            borderRadius: 20,
            backgroundColor: '#0D241E',
            border: '6px solid #92400E',
            padding: '36px 44px',
            display: 'flex',
            flexDirection: 'column',
            gap: 24,
            boxSizing: 'border-box',
          }}
        >
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              borderBottom: '2px solid rgba(226, 232, 240, 0.2)',
              paddingBottom: 16,
            }}
          >
            <div style={{ color: '#FEF08A', fontSize: 34, fontWeight: 800 }}>
              {canh.tieuDeNho ?? 'Chứng minh Toán học'}
            </div>
            {canh.namMoc && (
              <div style={{ color: '#94A3B8', fontSize: 22, fontWeight: 700 }}>{canh.namMoc}</div>
            )}
          </div>

          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: 22,
              flex: 1,
              justifyContent: 'center',
            }}
          >
            {(canh.congThucLatex ?? []).map((ct, idx) => {
              const batDau = ct.tuFrame ?? idx * 18;
              const doMo = interpolate(frame, [batDau, batDau + 12], [0, 1], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              const dichX = interpolate(frame, [batDau, batDau + 12], [24, 0], {
                extrapolateLeft: 'clamp',
                extrapolateRight: 'clamp',
              });
              return (
                <div
                  key={`${ct.latex}-${idx}`}
                  style={{
                    opacity: doMo,
                    transform: `translateX(${dichX}px)`,
                    padding: '16px 24px',
                    borderRadius: 14,
                    backgroundColor: ct.noiBat
                      ? 'rgba(250, 204, 21, 0.14)'
                      : 'rgba(15, 23, 42, 0.45)',
                    border: ct.noiBat
                      ? '2px solid #FACC15'
                      : '1px solid rgba(226, 232, 240, 0.18)',
                  }}
                >
                  {ct.nhan && (
                    <div
                      style={{
                        color: ct.noiBat ? '#FDE047' : '#94A3B8',
                        fontSize: 20,
                        fontWeight: 700,
                        marginBottom: 8,
                      }}
                    >
                      {ct.nhan}
                    </div>
                  )}
                  <CongThucMath
                    latex={ct.latex}
                    fontSize={ct.noiBat ? 42 : 34}
                    mau={ct.noiBat ? '#FEF08A' : '#F8FAFC'}
                  />
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </MayQuayDong>
  );
};
