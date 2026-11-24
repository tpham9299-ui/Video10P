import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { BoiCanhHoatHinh } from '../boicanh/BoiCanhHoatHinh';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { DaoCu } from '../daocu/DaoCu';
import { CongThucMath } from '../daocu/CongThucMath';
import { MinhHoaToan } from '../daocu/MinhHoaToan';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngHoatHinh } from '../vfx/HieuUngHoatHinh';
import { KhungLoiBinhHaiHuoc } from './KhungLoiBinhHaiHuoc';

type Props = {
  canh: Canh;
  bangMau: BangMau;
  banDoNhanVat: Record<string, ThongTinNhanVat>;
};

/**
 * San khau giang Toan hai hoa voi phim hoat hinh (v0.2):
 * - Boi canh lop hoc bang xanh am ap
 * - Ben trai (~25%): nhan vat dung tren san go chi bang, hieu ung hoat hinh (bong den nay so...)
 * - Ben phai (~72%): bang xanh vien go chua cong thuc KaTeX tuan tu + MinhHoaToan dong
 */
export const CanhGiaiThichToan: React.FC<Props> = ({
  canh,
  bangMau,
  banDoNhanVat,
}) => {
  const frame = useCurrentFrame();
  const thoiLuong = Math.max(1, canh.denFrame - canh.tuFrame);
  const danhSachCongThuc = canh.congThucLatex ?? [];

  let chiSoDangDoc = -1;
  for (let i = 0; i < danhSachCongThuc.length; i++) {
    const moc = danhSachCongThuc[i].tuFrame ?? i * 24;
    if (frame >= moc) {
      chiSoDangDoc = i;
    }
  }

  const coMinhHoa = Boolean(canh.minhHoaToan);

  return (
    <div style={{ position: 'absolute', inset: 0 }}>
      <MayQuayDong
        camera={canh.camera}
        chuyenCanh={canh.chuyenCanh}
        nhanVat={canh.nhanVat}
        thoiLuongCanh={thoiLuong}
      >
        <BoiCanhHoatHinh loai={canh.boiCanh} thoiTiet={canh.thoiTiet} />

        {/* Bang xanh lon vien go nam gon ben phai man hinh */}
        <div
          style={{
            position: 'absolute',
            top: 62,
            left: 520,
            right: 48,
            bottom: 146,
            borderRadius: 20,
            backgroundColor: '#114226',
            border: '12px solid #92400E',
            boxShadow: '0 10px 0 rgba(120, 53, 15, 0.35)',
            padding: '22px 28px',
            display: 'flex',
            flexDirection: 'column',
            gap: 16,
            boxSizing: 'border-box',
          }}
        >
          {/* Tieu de bang xanh */}
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              borderBottom: '2.5px dashed rgba(254, 249, 195, 0.35)',
              paddingBottom: 12,
              gap: 16,
            }}
          >
            <div style={{ color: '#FEF08A', fontSize: 32, fontWeight: 900 }}>
              {canh.tieuDeNho ?? 'Bảng Giải Thích Toán Học'}
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
              {danhSachCongThuc.length > 0 && (
                <div
                  style={{
                    padding: '5px 15px',
                    borderRadius: 999,
                    backgroundColor: '#FEF08A',
                    color: '#14532D',
                    fontSize: 16,
                    fontWeight: 900,
                  }}
                >
                  Bước {Math.max(1, chiSoDangDoc + 1)} / {danhSachCongThuc.length}
                </div>
              )}
              {canh.namMoc && (
                <div style={{ color: '#BBF7D0', fontSize: 19, fontWeight: 700 }}>
                  {canh.namMoc}
                </div>
              )}
            </div>
          </div>

          {/* Than bang: Cong thuc KaTeX (trai) + MinhHoaToan dong (phai) */}
          <div
            style={{
              display: 'flex',
              flex: 1,
              minHeight: 0,
              gap: 22,
              alignItems: 'stretch',
            }}
          >
            <div
              style={{
                flex: coMinhHoa ? '1 1 55%' : '1 1 100%',
                display: 'flex',
                flexDirection: 'column',
                gap: 13,
                justifyContent: 'center',
              }}
            >
              {danhSachCongThuc.map((ct, idx) => {
                const batDau = ct.tuFrame ?? idx * 24;
                const doMo = interpolate(frame, [batDau, batDau + 12], [0, 1], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                });
                const dichX = interpolate(frame, [batDau, batDau + 12], [20, 0], {
                  extrapolateLeft: 'clamp',
                  extrapolateRight: 'clamp',
                });
                const dangDoc = idx === chiSoDangDoc;
                const daQua = idx < chiSoDangDoc;
                const mauHighlight = ct.noiBat ? '#FDE047' : '#7DD3FC';

                return (
                  <div
                    key={`${ct.latex}-${idx}`}
                    style={{
                      position: 'relative',
                      opacity: doMo * (daQua ? 0.86 : 1),
                      transform: `translateX(${dichX}px)`,
                      padding: '12px 18px 12px 24px',
                      borderRadius: 14,
                      backgroundColor: dangDoc
                        ? ct.noiBat
                          ? 'rgba(250, 204, 21, 0.22)'
                          : 'rgba(125, 211, 252, 0.16)'
                        : 'rgba(9, 43, 25, 0.72)',
                      border: dangDoc
                        ? `2.5px solid ${mauHighlight}`
                        : '1.5px solid rgba(255, 255, 255, 0.18)',
                      overflow: 'hidden',
                    }}
                  >
                    <div
                      style={{
                        position: 'absolute',
                        top: 0,
                        bottom: 0,
                        left: 0,
                        width: dangDoc ? 7 : 3,
                        backgroundColor: dangDoc
                          ? mauHighlight
                          : 'rgba(187, 247, 208, 0.4)',
                      }}
                    />

                    <div
                      style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        marginBottom: 4,
                      }}
                    >
                      {ct.nhan && (
                        <div
                          style={{
                            color: dangDoc
                              ? ct.noiBat
                                ? '#FEF08A'
                                : '#BAE6FD'
                              : '#BBF7D0',
                            fontSize: 18,
                            fontWeight: 700,
                          }}
                        >
                          {ct.nhan}
                        </div>
                      )}
                      {dangDoc && (
                        <div
                          style={{
                            padding: '2px 10px',
                            borderRadius: 999,
                            backgroundColor: mauHighlight,
                            color: '#14532D',
                            fontSize: 12,
                            fontWeight: 900,
                            letterSpacing: 0.5,
                          }}
                        >
                          ĐANG GIẢI THÍCH
                        </div>
                      )}
                    </div>

                    <CongThucMath
                      latex={ct.latex}
                      fontSize={coMinhHoa ? (ct.noiBat ? 30 : 26) : ct.noiBat ? 38 : 32}
                      mau={ct.noiBat ? '#FEF08A' : '#FFFFFF'}
                    />
                  </div>
                );
              })}
            </div>

            {canh.minhHoaToan && (
              <div style={{ flex: '0 0 43%', minHeight: 0 }}>
                <MinhHoaToan
                  data={canh.minhHoaToan}
                  mauNhanManh={bangMau.nhanManh || '#FDE047'}
                />
              </div>
            )}
          </div>
        </div>

        {/* Lop nhan vat + dao cu + hieu ung hoat hinh dung ben trai bang */}
        <svg
          width={1920}
          height={1080}
          viewBox="0 0 1920 1080"
          style={{ position: 'absolute', inset: 0, pointerEvents: 'none' }}
        >
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
                trangThai={nv}
                tiLe={1.32}
                thoiLuongCanh={thoiLuong}
              />
            );
          })}
          <HieuUngHoatHinh danhSach={canh.hieuUngHoatHinh} />
        </svg>
      </MayQuayDong>

      <KhungLoiBinhHaiHuoc loiBinh={canh.loiBinhHaiHuoc} />
    </div>
  );
};
