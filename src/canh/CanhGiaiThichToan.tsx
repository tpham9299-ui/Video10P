import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';
import type { BangMau, Canh, ThongTinNhanVat } from '../kieu_dai';
import { BoiCanhHoatHinh } from '../boicanh/BoiCanhHoatHinh';
import { locDaoCuKhongTrungLap } from '../boicanh/moi_truong_logic';
import { NguoiQueDong } from '../nhanvat/NguoiQueDong';
import { giaiTrangThaiNhanVatTrongCanh } from '../nhanvat/dien_xuat';
import { DaoCu } from '../daocu/DaoCu';
import { CongThucMath } from '../daocu/CongThucMath';
import { MinhHoaToan } from '../daocu/MinhHoaToan';
import { MayQuayDong } from '../vfx/MayQuayDong';
import { HieuUngHoatHinh } from '../vfx/HieuUngHoatHinh';
import { LopCauHoiTuongTac } from './LopCauHoiTuongTac';
import { coDuLieuMinhHoaHopLe } from '../daocu/minh_hoa_hop_le';

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
  const danhSachNhanVat = giaiTrangThaiNhanVatTrongCanh(canh, frame, thoiLuong);
  const danhSachCongThuc = canh.congThucLatex ?? [];

  let chiSoDangDoc = -1;
  for (let i = 0; i < danhSachCongThuc.length; i++) {
    const moc = danhSachCongThuc[i].tuFrame ?? i * 24;
    if (frame >= moc) {
      chiSoDangDoc = i;
    }
  }

  const coMinhHoa = coDuLieuMinhHoaHopLe(canh.minhHoaToan);
  const daoCuHienThi = locDaoCuKhongTrungLap(canh.daoCu, canh.nhanVat);

  // Chon phong cach bang phan khung go (lop hoc / giang duong) hoac cuon giay da co mo ra (boi canh lich su/ngoai troi)
  const dungBangPhanGo =
    canh.boiCanh === 'lop_hoc_bang_xanh' ||
    canh.boiCanh === 'giang_duong_dai_hoc' ||
    canh.boiCanh === 'giang_duong_hien_dai';
  const moCuon = interpolate(frame, [0, 14], [0.92, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // Cam hien thi "GOC BINH LUAN" tren bo cuc giang_toan de tranh de chu len bang Toan
  const lopHud = (
    <>
      {canh.cauHoiTuongTac && (
        <LopCauHoiTuongTac
          cauHoi={canh.cauHoiTuongTac}
          bangMau={bangMau}
          thoiLuongCanh={thoiLuong}
        />
      )}
    </>
  );

  return (
    <div style={{ position: 'absolute', inset: 0 }}>
      {/* Khoa zoom camera o 1.0x trong canh giang_toan de bang xanh + do thi luon nam gon 100% trong khung 1920x1080 */}
      <MayQuayDong
        camera={{ kieu: 'tinh', zoom: 1, panX: 0, panY: 0 }}
        mayQuay={{ gocQuay: 'toan_canh', doPhong: 1 }}
        luotThoai={canh.luotThoai}
        daoCu={daoCuHienThi}
        chuyenCanh={canh.chuyenCanh}
        nhanVat={canh.nhanVat}
        thoiLuongCanh={thoiLuong}
        anhSangMoiTruong={canh.anhSangMoiTruong}
        hud={lopHud}
      >
        <BoiCanhHoatHinh
          loai={canh.boiCanh}
          thoiTiet={canh.thoiTiet}
          vatTheXungQuanh={canh.vatTheXungQuanh}
          bienSoXe={canh.bienSoXe}
          nhanVat={canh.nhanVat}
          daoCu={daoCuHienThi}
          anhBoiCanh={canh.anhBoiCanh}
          anhSangMoiTruong={canh.anhSangMoiTruong}
          thoiLuongCanh={thoiLuong}
        />

        {/* Bang phan khung go hoac cuon giay da co mo ra dat gon ben canh nhan vat (Clean Cinema v3.0, khong tran khung) */}
        <div
          style={{
            position: 'absolute',
            top: 68,
            left: 468,
            right: 48,
            bottom: 146,
            borderRadius: dungBangPhanGo ? 18 : 14,
            backgroundColor: dungBangPhanGo ? '#134429' : '#FAF2DC',
            border: dungBangPhanGo ? '11px solid #78350F' : '4px solid #1A1A1A',
            boxShadow: dungBangPhanGo
              ? '0 10px 0 #451A03, inset 0 0 0 3px #1A1A1A'
              : '8px 8px 0px rgba(26, 26, 26, 0.36)',
            padding: dungBangPhanGo ? '18px 24px 24px' : '24px 30px 24px',
            display: 'flex',
            flexDirection: 'column',
            gap: 14,
            boxSizing: 'border-box',
            overflow: 'hidden',
            transform: `scale(${moCuon.toFixed(3)})`,
            transformOrigin: 'center center',
          }}
        >
          {/* Thanh cuon go tren/duoi cho cuon giay da co, hoac thanh dung phan cho bang phan */}
          {!dungBangPhanGo ? (
            <>
              <div
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  height: 11,
                  backgroundColor: '#92400E',
                  borderBottom: '2.5px solid #1A1A1A',
                }}
              />
              <div
                style={{
                  position: 'absolute',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  height: 11,
                  backgroundColor: '#92400E',
                  borderTop: '2.5px solid #1A1A1A',
                }}
              />
            </>
          ) : (
            <div
              style={{
                position: 'absolute',
                bottom: 0,
                left: 60,
                right: 60,
                height: 8,
                backgroundColor: '#B45309',
                borderTop: '2px solid #1A1A1A',
                display: 'flex',
                alignItems: 'center',
                gap: 14,
                paddingLeft: 24,
              }}
            >
              <div style={{ width: 32, height: 5, borderRadius: 2, backgroundColor: '#F8FAFC' }} />
              <div style={{ width: 24, height: 5, borderRadius: 2, backgroundColor: '#FEF08A' }} />
            </div>
          )}

          {/* Tieu de bang phan / cuon giay da */}
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              borderBottom: dungBangPhanGo
                ? '2.5px dashed rgba(254, 249, 195, 0.35)'
                : '2.5px dashed rgba(146, 64, 14, 0.35)',
              paddingBottom: 10,
              gap: 16,
            }}
          >
            <div
              style={{
                color: dungBangPhanGo ? '#FEF08A' : '#1A1A1A',
                fontSize: 31,
                fontWeight: 900,
              }}
            >
              {canh.tieuDeNho ?? 'Bảng Giải Thích Toán Học'}
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexShrink: 0 }}>
              {danhSachCongThuc.length > 0 && (
                <div
                  style={{
                    padding: '4px 14px',
                    borderRadius: 999,
                    backgroundColor: dungBangPhanGo ? '#FEF08A' : '#1A1A1A',
                    color: dungBangPhanGo ? '#14532D' : '#FAF2DC',
                    fontSize: 15,
                    fontWeight: 900,
                  }}
                >
                  Bước {Math.max(1, chiSoDangDoc + 1)} / {danhSachCongThuc.length}
                </div>
              )}
              {canh.namMoc && (
                <div
                  style={{
                    color: dungBangPhanGo ? '#BBF7D0' : '#92400E',
                    fontSize: 18,
                    fontWeight: 800,
                  }}
                >
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
              minWidth: 0,
              gap: 18,
              alignItems: 'stretch',
            }}
          >
            <div
              style={{
                flex: coMinhHoa ? '1 1 51%' : '1 1 100%',
                minWidth: 0,
                display: 'flex',
                flexDirection: 'column',
                gap: 12,
                justifyContent: 'center',
                overflow: 'hidden',
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
                const mauHighlight = dungBangPhanGo
                  ? ct.noiBat
                    ? '#FDE047'
                    : '#7DD3FC'
                  : ct.noiBat
                    ? '#B45309'
                    : '#1D4ED8';

                return (
                  <div
                    key={`${ct.latex}-${idx}`}
                    style={{
                      position: 'relative',
                      opacity: doMo * (daQua ? 0.86 : 1),
                      transform: `translateX(${dichX}px)`,
                      padding: '12px 18px 12px 24px',
                      borderRadius: 12,
                      backgroundColor: dungBangPhanGo
                        ? dangDoc
                          ? ct.noiBat
                            ? 'rgba(250, 204, 21, 0.22)'
                            : 'rgba(125, 211, 252, 0.16)'
                          : 'rgba(9, 43, 25, 0.72)'
                        : dangDoc
                          ? 'rgba(251, 191, 36, 0.24)'
                          : 'rgba(255, 253, 247, 0.88)',
                      border: dangDoc
                        ? `2.5px solid ${mauHighlight}`
                        : dungBangPhanGo
                          ? '1.5px solid rgba(255, 255, 255, 0.18)'
                          : '1.8px solid rgba(26, 26, 26, 0.28)',
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
                          : dungBangPhanGo
                            ? 'rgba(187, 247, 208, 0.4)'
                            : 'rgba(146, 64, 14, 0.4)',
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
                            color: dungBangPhanGo
                              ? dangDoc
                                ? ct.noiBat
                                  ? '#FEF08A'
                                  : '#BAE6FD'
                                : '#BBF7D0'
                              : '#78350F',
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
                            color: dungBangPhanGo ? '#14532D' : '#FFFDF7',
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
                      mau={
                        dungBangPhanGo
                          ? ct.noiBat
                            ? '#FEF08A'
                            : '#FFFFFF'
                          : ct.noiBat
                            ? '#9A3412'
                            : '#1A1A1A'
                      }
                    />
                  </div>
                );
              })}
            </div>

            {coMinhHoa && canh.minhHoaToan && (
              <div
                style={{
                  flex: '0 0 47%',
                  minWidth: 0,
                  minHeight: 0,
                  overflow: 'hidden',
                  borderRadius: 12,
                  backgroundColor: dungBangPhanGo ? 'transparent' : '#0F291E',
                  border: dungBangPhanGo ? 'none' : '2.5px solid #1A1A1A',
                }}
              >
                <MinhHoaToan
                  data={canh.minhHoaToan}
                  mauNhanManh={bangMau.nhanManh || '#FDE047'}
                  congThucLatex={danhSachCongThuc}
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
          {daoCuHienThi.map((dc, idx) => (
            <DaoCu key={`${dc.loai}-${idx}`} daoCu={dc} />
          ))}
          {danhSachNhanVat.map((nv, idx) => {
            const tt = banDoNhanVat[nv.id];
            if (!tt) return null;
            return (
              <NguoiQueDong
                key={`${nv.id}-${idx}`}
                thongTin={tt}
                trangThai={nv}
                tiLe={1.28}
                thoiLuongCanh={thoiLuong}
                bienDoAmThanh={canh.bienDoAmThanh}
              />
            );
          })}
          <HieuUngHoatHinh
            danhSach={canh.hieuUngHoatHinh}
            nhanVat={danhSachNhanVat}
            tiLeNhanVat={1.28}
          />
        </svg>
      </MayQuayDong>
    </div>
  );
};
