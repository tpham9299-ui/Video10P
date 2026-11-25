# -*- coding: utf-8 -*-
"""Chuan hoa ky hieu/cong thuc Toan hoc trong loi thoai sang tieng Viet doc TTS tu nhien."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

# Tu dien phat am mac dinh cho cac nha Toan hoc, dia danh lich su & thuat ngu Toan tieng Anh pho bien
TU_DIEN_PHAT_AM_MAC_DINH: dict[str, str] = {
    "Srinivasa Ramanujan": "Xri-ni-va-xa Ra-ma-nu-gian",
    "Ramanujan": "Ra-ma-nu-gian",
    "Srinivasa": "Xri-ni-va-xa",
    "G. H. Hardy": "Gi-Ét Ha-đi",
    "Godfrey Harold Hardy": "Gót-phri Ha-rôn Ha-đi",
    "Hardy": "Ha-đi",
    "Littlewood": "Lít-tơ-út",
    "Madras": "Ma-đơ-rát",
    "Kumbakonam": "Kum-ba-cô-nam",
    "Erode": "I-rốt",
    "Cambridge": "Kem-brít",
    "Trinity College": "Tri-ni-ti Co-lít",
    "Namagiri": "Na-ma-ghi-ri",
    "mock theta": "móc thê-ta",
    "Pythagoras": "Pi-ta-go",
    "Hippasus": "Híp-pa-xút",
    "Euclid": "Ơ-clít",
    "Archimedes": "Ác-si-mét",
    "Leonhard Euler": "Lê-ô-na Ơ-le",
    "Euler": "Ơ-le",
    "Carl Friedrich Gauss": "Các Phri-đơ-rích Gau-xơ",
    "Gauss": "Gau-xơ",
    "Évariste Galois": "Ê-va-rít Ga-loa",
    "Evariste Galois": "Ê-va-rít Ga-loa",
    "Galois": "Ga-loa",
    "Isaac Newton": "Ai-dắc Niu-tơn",
    "Newton": "Niu-tơn",
    "Leibniz": "Lai-bơ-nít",
    "Fermat": "Phéc-ma",
    "Riemann": "Ri-man",
    "Georg Cantor": "Gê-oóc Can-to",
    "Cantor": "Can-to",
    "Emmy Noether": "Em-mi Nơ-tơ",
    "Noether": "Nơ-tơ",
    "Hilbert": "Hin-bét",
    "Kurt Gödel": "Cuốc Gơ-đen",
    "Gödel": "Gơ-đen",
    "Godel": "Gơ-đen",
    "Alan Turing": "A-lan Tua-ring",
    "Turing": "Tua-ring",
    "Fourier": "Phu-ri-ê",
    "Laplace": "La-plát",
    "Descartes": "Đề-các",
    "Pascal": "Pát-xcan",
    "Fibonacci": "Phi-bô-na-xi",
    "Al-Khwarizmi": "An Khoa-rít-mi",
    "Hypatia": "Hi-pa-ti-a",
    "Ada Lovelace": "A-đa Lấp-lây",
    "Königsberg": "Kơ-ních-béc",
    "Konigsberg": "Kơ-ních-béc",
    "Alexandria": "A-lếch-xan-đri-a",
    "Samos": "Xa-mốt",
    "Göttingen": "Gốt-tin-gen",
    "Oxford": "Óc-phớt",
    "Royal Society": "Roi-ồ Xô-xai-ơ-ti",
    "partition": "pa-ti-sần",
    "modular": "mô-đu-la",
    "zeta": "dê-ta",
    "theta": "thê-ta",
    "calculus": "can-kiu-lớt",
    "algorithm": "an-gô-ri-dầm",
    "theorem": "thi-ơ-rầm",
    "taxicab": "tắc-xi-cáp",
}


def chuan_hoa_tu_dien_phat_am(raw: Any) -> dict[str, str]:
    """Lam sach tu dien phat am {tu_goc: phien_am_tieng_viet}."""
    ket_qua: dict[str, str] = {}
    if not isinstance(raw, dict):
        return ket_qua
    for k, v in raw.items():
        khoa = re.sub(r"\s+", " ", str(k or "").strip())
        gia_tri = re.sub(r"\s+", " ", str(v or "").strip())
        if khoa and gia_tri:
            ket_qua[khoa] = gia_tri
    return ket_qua


def tai_tu_dien_phat_am(
    duong_dan_tu_lieu: Path | str | None = None,
    tu_dien_bo_sung: dict[str, str] | None = None,
    dung_mac_dinh: bool = True,
) -> dict[str, str]:
    """
    Nap tu dien phat am hop nhat theo thu tu uu tien tang dan:
    1. TU_DIEN_PHAT_AM_MAC_DINH (neu dung_mac_dinh=True)
    2. truong `tu_dien_phat_am` (hoac `tuDienPhatAm`) trong tu_lieu_nghien_cuu.json (neu ton tai)
    3. `tu_dien_bo_sung` truyen truc tiep
    """
    hop_nhat: dict[str, str] = {}
    khoa_lower_map: dict[str, str] = {}

    def _them_nguon(nguon: dict[str, str]) -> None:
        for k, v in chuan_hoa_tu_dien_phat_am(nguon).items():
            kl = k.casefold()
            if kl in khoa_lower_map and khoa_lower_map[kl] != k:
                hop_nhat.pop(khoa_lower_map[kl], None)
            khoa_lower_map[kl] = k
            hop_nhat[k] = v

    if dung_mac_dinh:
        _them_nguon(TU_DIEN_PHAT_AM_MAC_DINH)

    if duong_dan_tu_lieu is not None:
        p = Path(duong_dan_tu_lieu)
        if p.exists() and p.is_file():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                data = {}
            if isinstance(data, dict):
                raw_td = data.get("tu_dien_phat_am") or data.get("tuDienPhatAm")
                if isinstance(raw_td, dict):
                    _them_nguon(raw_td)

    if tu_dien_bo_sung:
        _them_nguon(tu_dien_bo_sung)

    return hop_nhat


def ap_dung_tu_dien_phat_am(van_ban: str, tu_dien: dict[str, str] | None) -> str:
    """
    Thay the ten rieng / dia danh / thuat ngu nuoc ngoai sang phien am tieng Viet cho Edge TTS.
    Uu tien cum tu dai truoc va dung ranh gioi tu de tranh cat nham ben trong tu khac.
    """
    if not van_ban or not tu_dien:
        return van_ban

    sach_td = chuan_hoa_tu_dien_phat_am(tu_dien)
    if not sach_td:
        return van_ban

    # Sap xep giam dan theo do dai cum tu de "Srinivasa Ramanujan" / "mock theta" khop truoc
    cac_khoa = sorted(sach_td.keys(), key=len, reverse=True)
    ban_do_lower = {k.casefold(): sach_td[k] for k in cac_khoa}
    pattern = re.compile(
        r"(?<!\w)(" + "|".join(re.escape(k) for k in cac_khoa) + r")(?!\w)",
        flags=re.IGNORECASE | re.UNICODE,
    )
    return pattern.sub(lambda m: ban_do_lower.get(m.group(1).casefold(), m.group(1)), van_ban)

BANG_CHI_SO_TREN: dict[str, str] = {
    "⁰": "0",
    "¹": "1",
    "²": "2",
    "³": "3",
    "⁴": "4",
    "⁵": "5",
    "⁶": "6",
    "⁷": "7",
    "⁸": "8",
    "⁹": "9",
    "⁻": "-",
    "⁺": "+",
    "ⁿ": "n",
}

PHAN_SO_PHO_BIEN: dict[tuple[str, str], str] = {
    ("1", "2"): "một phần hai",
    ("1", "3"): "một phần ba",
    ("1", "4"): "một phần tư",
    ("3", "4"): "ba phần tư",
}

DON_VI_GACH_CHEO: list[tuple[str, str]] = [
    (r"\bkm/h\b", "ki-lô-mét trên giờ"),
    (r"\bm/s\b", "mét trên giây"),
    (r"\bkm/s\b", "ki-lô-mét trên giây"),
]


def _doc_so_mu(mu_raw: str) -> str:
    mu = mu_raw.strip().strip("{}")
    if mu == "2":
        return " bình phương"
    if mu == "3":
        return " lập phương"
    if mu.startswith("-"):
        return f" mũ âm {mu[1:].strip()}"
    if mu.startswith("+"):
        return f" mũ dương {mu[1:].strip()}"
    return f" mũ {mu}"


def _chuyen_superscript(match: re.Match[str]) -> str:
    co_so = match.group(1)
    chuoi_mu = "".join(BANG_CHI_SO_TREN.get(ch, ch) for ch in match.group(2))
    return f"{co_so}{_doc_so_mu(chuoi_mu)}"


def _chuyen_phan_so(match: re.Match[str]) -> str:
    tu = match.group(1).strip()
    mau = match.group(2).strip()
    if (tu, mau) in PHAN_SO_PHO_BIEN:
        return PHAN_SO_PHO_BIEN[(tu, mau)]
    return f"{tu} phần {mau}"


def chuan_hoa_doc_toan(
    van_ban: str,
    tu_dien_phat_am: dict[str, str] | None = None,
    dung_tu_dien_mac_dinh: bool = True,
) -> str:
    """
    Chuyen ky hieu/cong thuc Toan va ten rieng/thuat ngu nuoc ngoai trong loi thoai
    sang cach doc tieng Viet tu nhien de Edge TTS doc troi chay
    (VD: √2, π, x^2, ∞, TCN, so thap phan, phan so, Ramanujan -> Ra-ma-nu-gian...).
    Khong lam thay doi van ban goc dung cho phu de / man hinh.
    """
    if not van_ban:
        return ""

    s = van_ban.strip()

    # 1. Boc dau $ neu co trong loi thoai
    s = re.sub(r"\$\$(.*?)\$\$", r" \1 ", s)
    s = re.sub(r"\$([^$]+)\$", r" \1 ", s)

    # 2. Xu ly cac lenh LaTeX co ban neu lo xuat hien trong loi thoai
    s = re.sub(
        r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}",
        lambda m: f" {m.group(1).strip()} phần {m.group(2).strip()} ",
        s,
    )
    s = re.sub(
        r"\\sqrt\s*\{([^{}]+)\}",
        lambda m: f" căn bậc hai của {m.group(1).strip()} ",
        s,
    )
    thay_latex = [
        (r"\\pi\b", " pi "),
        (r"\\infty\b", " vô cực "),
        (r"\\approx\b", " xấp xỉ "),
        (r"\\neq\b|\\ne\b", " khác "),
        (r"\\leq\b|\\le\b", " nhỏ hơn hoặc bằng "),
        (r"\\geq\b|\\ge\b", " lớn hơn hoặc bằng "),
        (r"\\times\b|\\cdot\b", " nhân "),
        (r"\\div\b", " chia "),
        (r"\\pm\b", " cộng trừ "),
        (r"\\implies\b|\\Rightarrow\b", " suy ra "),
        (r"\\to\b|\\rightarrow\b", " tiến tới "),
        (r"\\notin\b", " không thuộc "),
        (r"\\in\b", " thuộc "),
        (r"\\mathbb\{Q\}", " tập số hữu tỉ Q "),
        (r"\\mathbb\{R\}", " tập số thực R "),
        (r"\\mathbb\{Z\}", " tập số nguyên Z "),
        (r"\\mathbb\{N\}", " tập số tự nhiên N "),
        (r"\\gcd\b", " ước chung lớn nhất "),
        (r"\\quad\b|\\,", " "),
    ]
    for pattern, repl in thay_latex:
        s = re.sub(pattern, repl, s)

    # 3. Moc lich su TCN / SCN va ky hieu ~ truoc so
    s = re.sub(r"\bTCN\b", "trước Công nguyên", s)
    s = re.sub(r"\bSCN\b", "sau Công nguyên", s)
    s = re.sub(r"~\s*(\d+)", r"khoảng \1", s)

    # 4. Don vi gach cheo truoc khi xu ly phan so
    for pattern, repl in DON_VI_GACH_CHEO:
        s = re.sub(pattern, repl, s, flags=re.IGNORECASE)

    # 5. Can bac ba & can bac hai
    s = re.sub(r"∛\s*\(([^()]+)\)", r"căn bậc ba của \1", s)
    s = re.sub(r"∛\s*([a-zA-Z0-9.,]+)", r"căn bậc ba của \1", s)
    s = re.sub(r"√\s*\(([^()]+)\)", r"căn bậc hai của \1", s)
    s = re.sub(r"√\s*([a-zA-Z0-9.,]+)", r"căn bậc hai của \1", s)

    # 6. Luy thua dang ^ va dang chi so tren Unicode (x^2, x^{10}, x², 10⁻⁶)
    s = re.sub(
        r"([a-zA-Z0-9)])\s*\^\s*(\{[^{}]+\}|[+-]?[a-zA-Z0-9]+)",
        lambda m: f"{m.group(1)}{_doc_so_mu(m.group(2))}",
        s,
    )
    s = re.sub(
        r"([a-zA-Z0-9)])([⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺ⁿ]+)",
        _chuyen_superscript,
        s,
    )

    # 7. Hang so & ky hieu Toan Unicode
    thay_ky_hieu = [
        ("π", " pi "),
        ("∞", " vô cực "),
        ("φ", " phi "),
        ("θ", " thê-ta "),
        ("Δ", " đen-ta "),
        ("±", " cộng trừ "),
        ("≈", " xấp xỉ "),
        ("≠", " khác "),
        ("≤", " nhỏ hơn hoặc bằng "),
        ("≥", " lớn hơn hoặc bằng "),
        ("×", " nhân "),
        ("÷", " chia "),
        ("⇒", " suy ra "),
        ("→", " đến "),
        ("∉", " không thuộc "),
        ("∈", " thuộc "),
        ("ℚ", " tập số hữu tỉ Q "),
        ("ℝ", " tập số thực R "),
        ("ℤ", " tập số nguyên Z "),
        ("ℕ", " tập số tự nhiên N "),
        ("∫", " tích phân "),
        ("∑", " tổng xích ma "),
    ]
    for ky_hieu, cach_doc in thay_ky_hieu:
        s = s.replace(ky_hieu, cach_doc)

    # 8. Phan tram & do
    s = re.sub(r"(\d+(?:[.,]\d+)?)\s*%", r"\1 phần trăm", s)
    s = re.sub(r"(\d+(?:[.,]\d+)?)\s*°", r"\1 độ", s)

    # 9. Phan so (p/q, 3/4, 22/7, 1/2...) - tranh ngay thang dd/mm/yyyy
    s = re.sub(
        r"(?<![\w/])([a-zA-Z]|\d{1,4})\s*/\s*([a-zA-Z]|\d{1,4})(?![\w/])",
        _chuyen_phan_so,
        s,
    )

    # 10. So hang nghin co nhieu dau cham (vd 1.000.000 -> 1000000) va dang x.000 -> x000
    s = re.sub(r"\b(\d{1,3}(?:\.\d{3}){2,})\b", lambda m: m.group(1).replace(".", ""), s)
    s = re.sub(r"\b(\d{1,3})\.000\b", r"\g<1>000", s)

    # 11. So thap phan (3.14 -> 3 phẩy 14, 1,414 -> 1 phẩy 414)
    s = re.sub(r"(?<!\d)(\d+)[.,](\d+)(?!\d)", r"\1 phẩy \2", s)

    # 12. Cac toan tu ASCII trong bieu thuc (=>, ->, =, +)
    s = s.replace("=>", " suy ra ")
    s = s.replace("->", " đến ")
    s = re.sub(r"(?<=\w)\s*=\s*(?=\w)", " bằng ", s)
    s = re.sub(r"(?<=\w)\s*\+\s*(?=\w)", " cộng ", s)
    s = re.sub(r"\bgcd\s*\(([^()]+)\)", r"ước chung lớn nhất của \1", s, flags=re.IGNORECASE)

    # 13. Ap dung tu dien phat am ten rieng / dia danh / thuat ngu nuoc ngoai (chi dung cho TTS)
    if tu_dien_phat_am is not None or dung_tu_dien_mac_dinh:
        tu_dien_ap_dung = tai_tu_dien_phat_am(
            tu_dien_bo_sung=tu_dien_phat_am,
            dung_mac_dinh=dung_tu_dien_mac_dinh,
        )
        s = ap_dung_tu_dien_phat_am(s, tu_dien_ap_dung)

    # 14. Don dep khoang trang & dau cau thua
    s = s.replace("—", ", ")
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    s = re.sub(r"\s{2,}", " ", s)
    return s.strip()
