/**
 * Ham bam so nguyen tat dinh trong khoang [0, 1).
 * Dam bao moi frame Remotion giong nhau 100%, khong dung ham ngau nhien.
 */
export function bamTatDinh(seed: number): number {
  const x = Math.sin(seed * 12.9898 + 78.233) * 43758.5453;
  return x - Math.floor(x);
}

/**
 * Bam chuoi thanh so nguyen duong tat dinh (dung cho seed nhay mat theo id nhan vat).
 */
export function bamChuoiTatDinh(chuoi: string): number {
  let h = 2166136261;
  for (let i = 0; i < chuoi.length; i++) {
    h ^= chuoi.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return Math.abs(h);
}
