import React from 'react';
import type { LoaiBoCuc, LoaiCanh, LoiBinhHaiHuoc } from '../kieu_dai';
import { coHienKhungLoiBinh } from './loi_binh_logic';

export { coHienKhungLoiBinh };

type KhungLoiBinhHaiHuocProps = {
  loiBinh?: LoiBinhHaiHuoc;
  boCuc?: LoaiBoCuc;
  loaiCanh?: LoaiCanh;
};

/**
 * Clean Cinema UI (v3.0): go bo hoan toan hop "GOC BINH LUAN" co dinh o goc phai
 * de nhuong 100% khung hinh cho hoat hinh, bong bong chat & 6 hieu ung hai thi giac.
 */
export const KhungLoiBinhHaiHuoc: React.FC<KhungLoiBinhHaiHuocProps> = () => {
  return null;
};
