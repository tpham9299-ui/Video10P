/**
 * Bo duong cong noi suy & lo xo vat ly tat dinh 100% cho hoat hinh 2D (v0.4).
 * Khong dung ham ngau nhien, khong bao gio tra ve NaN hoac Infinity.
 */

export function kepGiaTri(giaTri: number, nhoNhat: number, lonNhat: number): number {
  if (!Number.isFinite(giaTri)) {
    return nhoNhat;
  }
  return Math.max(nhoNhat, Math.min(lonNhat, giaTri));
}

export function noiSuy(tu: number, den: number, t: number): number {
  return tu + (den - tu) * t;
}

/** Noi suy muot vao-ra kieu bac 3 (chuyen canh, pan, zoom cham, vao the dong tac) */
export function easeInOutCubic(t: number): number {
  const x = kepGiaTri(t, 0, 1);
  return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
}

/** Noi suy cham dan ve dich kieu bac 3 */
export function easeOutCubic(t: number): number {
  const x = kepGiaTri(t, 0, 1);
  return 1 - Math.pow(1 - x, 3);
}

/** Noi suy hinh sin em ai cho pan/camera luot nhe */
export function easeInOutSine(t: number): number {
  const x = kepGiaTri(t, 0, 1);
  return -(Math.cos(Math.PI * x) - 1) / 2;
}

/**
 * Vuot da roi hoi nhe (overshoot & follow-through).
 * Dung cho zoom_hai_huoc, vung tay, dua tay len tran/dau.
 */
export function easeOutBack(t: number, doVuot = 1.70158): number {
  const x = kepGiaTri(t, 0, 1);
  const c1 = Number.isFinite(doVuot) ? doVuot : 1.70158;
  const c3 = c1 + 1;
  return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
}

/**
 * Lay da nguoc truoc khi bat (anticipation).
 * Dung cho nhun truoc khi nhay, lui nhe truoc khi khoanh tay/ho het.
 */
export function easeInBack(t: number, doVuot = 1.70158): number {
  const x = kepGiaTri(t, 0, 1);
  const c1 = Number.isFinite(doVuot) ? doVuot : 1.70158;
  const c3 = c1 + 1;
  return c3 * x * x * x - c1 * x * x;
}

/**
 * Lo xo vat ly tat dinh 100% theo phuong trinh dao dong tat dan giai tich (O(1)).
 * - frame <= 0 => 0
 * - frame tang => bat len vuot nhe qua 1 roi on dinh ve 1 (khi damping thap).
 */
export function springTatDinh(
  frame: number,
  damping = 12,
  stiffness = 180,
  mass = 1,
  fps = 30,
): number {
  if (!Number.isFinite(frame) || frame <= 0) {
    return 0;
  }

  const m = Math.max(0.1, Number.isFinite(mass) ? mass : 1);
  const k = Math.max(1, Number.isFinite(stiffness) ? stiffness : 180);
  const c = Math.max(0.5, Number.isFinite(damping) ? damping : 12);
  const t = frame / Math.max(1, Number.isFinite(fps) ? fps : 30);

  const omega0 = Math.sqrt(k / m);
  const zeta = c / (2 * Math.sqrt(k * m));

  let ketQua = 1;
  if (zeta < 0.999) {
    const omegaD = omega0 * Math.sqrt(1 - zeta * zeta);
    const bao = Math.exp(-zeta * omega0 * t);
    ketQua =
      1 -
      bao *
        (Math.cos(omegaD * t) + ((zeta * omega0) / omegaD) * Math.sin(omegaD * t));
  } else if (zeta <= 1.001) {
    const bao = Math.exp(-omega0 * t);
    ketQua = 1 - bao * (1 + omega0 * t);
  } else {
    const can = Math.sqrt(zeta * zeta - 1);
    const r1 = -omega0 * (zeta - can);
    const r2 = -omega0 * (zeta + can);
    ketQua =
      1 - (r2 * Math.exp(r1 * t) - r1 * Math.exp(r2 * t)) / (r2 - r1);
  }

  if (!Number.isFinite(ketQua)) {
    return 1;
  }
  return Math.abs(1 - ketQua) < 1e-4 && t > 1.5 ? 1 : ketQua;
}

/**
 * Bao toan dien tich co gian hoat hinh: squashX * squashY = 1.
 * Kep trong [0.72, 1.38] de hinh khoi nguoi que luon dep mat.
 */
export function baoToanCoGian(squashY: number): {
  squashX: number;
  squashY: number;
} {
  const sy = kepGiaTri(squashY, 0.72, 1.38);
  const sx = 1 / sy;
  return { squashX: sx, squashY: sy };
}
