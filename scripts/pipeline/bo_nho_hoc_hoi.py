# -*- coding: utf-8 -*-
"""Bo nho tu hoc hoi ben vung & hang doi chu de cho he thong AI san xuat phim Toan hoc."""

from __future__ import annotations

import argparse
import datetime
import json
import math
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.gemini_client import GeminiClient

DUONG_DAN_BO_NHO_MAC_DINH = GOC_DU_AN / "du_lieu" / "bo_nho_hoc_hoi.json"
LOAI_BAI_HOC_HOP_LE: tuple[str, ...] = (
    "toan_hoc",
    "kich_ban",
    "hai_huoc",
    "thoi_luong",
    "hinh_anh",
)
TRANG_THAI_HANG_DOI_HOP_LE: tuple[str, ...] = ("cho", "dang_lam", "xong")
TOI_DA_BAI_HOC = 25


def _ngay_hom_nay() -> str:
    return datetime.date.today().isoformat()


def _thoi_diem_hien_tai() -> str:
    return datetime.datetime.now().replace(microsecond=0).isoformat()


def _tao_slug_sach(van_ban: str) -> str:
    s = (van_ban or "").replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s.lower()).strip("_")
    return s[:48] or "chu_de_toan_hoc"


def _chuan_hoa_chuoi_so_sanh(van_ban: str) -> str:
    s = (van_ban or "").replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = re.sub(r"[^a-zA-Z0-9\s]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def _tap_tu(van_ban: str) -> set[str]:
    return {t for t in _chuan_hoa_chuoi_so_sanh(van_ban).split(" ") if len(t) >= 2}


def _do_tuong_dong_jaccard(a: str, b: str) -> float:
    ta, tb = _tap_tu(a), _tap_tu(b)
    if not ta or not tb:
        return 0.0
    giao = len(ta & tb)
    hop = len(ta | tb)
    return giao / float(hop) if hop else 0.0


def _ep_so_thuc(gia_tri: Any, mac_dinh: float, min_v: float, max_v: float) -> float:
    try:
        so = float(gia_tri)
        if not math.isfinite(so):
            so = mac_dinh
    except (TypeError, ValueError):
        so = mac_dinh
    return round(max(min_v, min(max_v, so)), 2)


def _ep_uu_tien(gia_tri: Any, mac_dinh: int = 3) -> int:
    try:
        so = int(round(float(gia_tri)))
    except (TypeError, ValueError):
        so = mac_dinh
    return max(1, min(5, so))


def _chuan_hoa_loai_bai_hoc(gia_tri: Any) -> str:
    if isinstance(gia_tri, str):
        s = _chuan_hoa_chuoi_so_sanh(gia_tri).replace(" ", "_")
        if s in LOAI_BAI_HOC_HOP_LE:
            return s
    return "kich_ban"


def _chuan_hoa_trang_thai(gia_tri: Any) -> str:
    if isinstance(gia_tri, str):
        s = _chuan_hoa_chuoi_so_sanh(gia_tri).replace(" ", "_")
        if s in TRANG_THAI_HANG_DOI_HOP_LE:
            return s
    return "cho"


def tao_bo_nho_rong() -> dict[str, Any]:
    """Khoi tao cau truc bo nho hoc hoi sach gom 4 phan chuan."""
    return {
        "phienBan": "0.5",
        "capNhatLanCuoi": _thoi_diem_hien_tai(),
        "chu_de_da_lam": [],
        "hang_doi_chu_de": [],
        "bai_hoc_rut_ra": [],
        "phan_hoi_kenh": [],
    }


def _chuan_hoa_cau_truc_bo_nho(raw: Any) -> dict[str, Any]:
    goc = tao_bo_nho_rong()
    if not isinstance(raw, dict):
        return goc
    for khoa in ("chu_de_da_lam", "hang_doi_chu_de", "bai_hoc_rut_ra", "phan_hoi_kenh"):
        val = raw.get(khoa)
        if isinstance(val, list):
            goc[khoa] = [item for item in val if isinstance(item, dict)]
    if isinstance(raw.get("capNhatLanCuoi"), str) and raw["capNhatLanCuoi"].strip():
        goc["capNhatLanCuoi"] = raw["capNhatLanCuoi"].strip()
    return goc


def tai_bo_nho(duong_dan: Path | str | None = None) -> dict[str, Any]:
    """Doc du_lieu/bo_nho_hoc_hoi.json; tu khoi tao sach neu chua co."""
    path = Path(duong_dan) if duong_dan is not None else DUONG_DAN_BO_NHO_MAC_DINH
    if not path.exists():
        bo_nho = tao_bo_nho_rong()
        luu_bo_nho(bo_nho, path)
        return bo_nho
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        raw = tao_bo_nho_rong()
    return _chuan_hoa_cau_truc_bo_nho(raw)


def luu_bo_nho(du_lieu: dict[str, Any], duong_dan: Path | str | None = None) -> Path:
    """Luu bo nho hoc hoi ra dia dinh dang UTF-8 + LF."""
    path = Path(duong_dan) if duong_dan is not None else DUONG_DAN_BO_NHO_MAC_DINH
    path.parent.mkdir(parents=True, exist_ok=True)
    sach = _chuan_hoa_cau_truc_bo_nho(du_lieu)
    sach["capNhatLanCuoi"] = _thoi_diem_hien_tai()
    path.write_text(
        json.dumps(sach, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def da_ton_tai_chu_de(
    du_lieu: dict[str, Any],
    slug: str,
    tieu_de: str = "",
) -> bool:
    """Kiem tra chu de co trung voi chu_de_da_lam hoac hang_doi_chu_de hay khong."""
    slug_sach = _tao_slug_sach(slug or tieu_de)
    tieu_de_chuan = _chuan_hoa_chuoi_so_sanh(tieu_de)

    tat_ca = list(du_lieu.get("chu_de_da_lam") or []) + list(du_lieu.get("hang_doi_chu_de") or [])
    for muc in tat_ca:
        if not isinstance(muc, dict):
            continue
        muc_slug = _tao_slug_sach(str(muc.get("slug") or muc.get("tieuDe") or ""))
        if slug_sach and muc_slug == slug_sach:
            return True
        muc_td = _chuan_hoa_chuoi_so_sanh(str(muc.get("tieuDe") or ""))
        if tieu_de_chuan and muc_td:
            if tieu_de_chuan == muc_td:
                return True
            if _do_tuong_dong_jaccard(tieu_de_chuan, muc_td) >= 0.72:
                return True
    return False


def them_chu_de_hang_doi(
    du_lieu: dict[str, Any],
    danh_sach_moi: list[dict[str, Any]],
    gioi_han_them: int | None = None,
) -> list[dict[str, Any]]:
    """Them chu de moi vao hang_doi_chu_de sau khi loc trung voi chu_de_da_lam va hang_doi_chu_de."""
    du_lieu.setdefault("hang_doi_chu_de", [])
    du_lieu.setdefault("chu_de_da_lam", [])

    da_them: list[dict[str, Any]] = []
    for raw in danh_sach_moi:
        if not isinstance(raw, dict):
            continue
        if gioi_han_them is not None and len(da_them) >= gioi_han_them:
            break
        tieu_de = str(raw.get("tieuDe") or "").strip()
        slug = _tao_slug_sach(str(raw.get("slug") or tieu_de))
        if not tieu_de or not slug:
            continue
        if da_ton_tai_chu_de(du_lieu, slug=slug, tieu_de=tieu_de):
            continue
        ban_ghi = {
            "slug": slug,
            "tieuDe": tieu_de,
            "gocKhaiThac": str(raw.get("gocKhaiThac") or "").strip(),
            "diemThuHut": _ep_so_thuc(raw.get("diemThuHut"), 8.0, 1.0, 10.0),
            "doSauToanHoc": _ep_so_thuc(raw.get("doSauToanHoc"), 8.0, 1.0, 10.0),
            "trangThai": _chuan_hoa_trang_thai(raw.get("trangThai") or "cho"),
        }
        du_lieu["hang_doi_chu_de"].append(ban_ghi)
        da_them.append(ban_ghi)
    return da_them


def dem_chu_de_dang_cho(du_lieu: dict[str, Any]) -> int:
    return sum(
        1
        for item in (du_lieu.get("hang_doi_chu_de") or [])
        if isinstance(item, dict) and item.get("trangThai") == "cho"
    )


def diem_xep_hang_chu_de(item: dict[str, Any]) -> float:
    thu_hut = _ep_so_thuc(item.get("diemThuHut"), 8.0, 1.0, 10.0)
    do_sau = _ep_so_thuc(item.get("doSauToanHoc"), 8.0, 1.0, 10.0)
    return round(thu_hut * 0.55 + do_sau * 0.45, 4)


def chon_chu_de_tiep_theo(
    du_lieu: dict[str, Any],
    loai_tru_slugs: set[str] | None = None,
) -> dict[str, Any] | None:
    """Chon chu de trangThai='cho' co diem cao nhat trong hang_doi_chu_de."""
    bo_qua = loai_tru_slugs or set()
    ung_vien = [
        item
        for item in (du_lieu.get("hang_doi_chu_de") or [])
        if isinstance(item, dict)
        and item.get("trangThai") == "cho"
        and str(item.get("slug") or "") not in bo_qua
    ]
    if not ung_vien:
        return None
    ung_vien.sort(key=diem_xep_hang_chu_de, reverse=True)
    return ung_vien[0]


def cap_nhat_trang_thai_hang_doi(
    du_lieu: dict[str, Any],
    slug: str,
    trang_thai: str,
) -> bool:
    tt = _chuan_hoa_trang_thai(trang_thai)
    slug_sach = _tao_slug_sach(slug)
    for item in du_lieu.get("hang_doi_chu_de") or []:
        if isinstance(item, dict) and _tao_slug_sach(str(item.get("slug") or "")) == slug_sach:
            item["trangThai"] = tt
            return True
    return False


def ghi_nhan_tap_hoan_thanh(
    du_lieu: dict[str, Any],
    slug: str,
    tieu_de: str,
    nhan_vat_chinh: str,
    tom_tat_1_cau: str,
    thoi_luong_giay: float,
    nguon_tham_khao: list[str] | None = None,
    ngay_tao: str | None = None,
) -> dict[str, Any]:
    """Luu tap da san xuat vao chu_de_da_lam va danh dau 'xong' trong hang_doi_chu_de."""
    du_lieu.setdefault("chu_de_da_lam", [])
    slug_sach = _tao_slug_sach(slug or tieu_de)
    nguon_sach: list[str] = []
    for u in nguon_tham_khao or []:
        if isinstance(u, dict):
            s = str(u.get("url") or u.get("tieuDe") or "").strip()
        else:
            s = str(u or "").strip()
        if s and s not in nguon_sach:
            nguon_sach.append(s)

    ban_ghi = {
        "slug": slug_sach,
        "tieuDe": str(tieu_de).strip(),
        "nhanVatChinh": str(nhan_vat_chinh).strip(),
        "tomTat1Cau": str(tom_tat_1_cau).strip(),
        "thoiLuongGiay": round(max(0.0, float(thoi_luong_giay)), 2),
        "ngayTao": ngay_tao or _ngay_hom_nay(),
        "nguonThamKhao": nguon_sach,
    }

    da_cap_nhat = False
    for idx, cu in enumerate(du_lieu["chu_de_da_lam"]):
        if isinstance(cu, dict) and _tao_slug_sach(str(cu.get("slug") or "")) == slug_sach:
            du_lieu["chu_de_da_lam"][idx] = ban_ghi
            da_cap_nhat = True
            break
    if not da_cap_nhat:
        du_lieu["chu_de_da_lam"].append(ban_ghi)

    cap_nhat_trang_thai_hang_doi(du_lieu, slug_sach, "xong")
    return ban_ghi


def _tia_va_gop_bai_hoc(
    danh_sach: list[dict[str, Any]],
    toi_da: int = TOI_DA_BAI_HOC,
) -> list[dict[str, Any]]:
    """Gop cac bai hoc trung/gan trung va giu toi da 25 bai uu tien cao nhat."""
    gop: list[dict[str, Any]] = []
    for item in danh_sach:
        if not isinstance(item, dict):
            continue
        noi_dung = re.sub(r"\s+", " ", str(item.get("noiDung") or "").strip())
        if not noi_dung:
            continue
        loai = _chuan_hoa_loai_bai_hoc(item.get("loai"))
        uu_tien = _ep_uu_tien(item.get("mucDoUuTien"), 3)
        ngay = str(item.get("ngay") or _ngay_hom_nay()).strip()
        chuan = _chuan_hoa_chuoi_so_sanh(noi_dung)

        tim_thay = -1
        for idx, cu in enumerate(gop):
            cu_chuan = _chuan_hoa_chuoi_so_sanh(str(cu.get("noiDung") or ""))
            if chuan == cu_chuan:
                tim_thay = idx
                break
            if cu.get("loai") == loai and _do_tuong_dong_jaccard(chuan, cu_chuan) >= 0.80:
                tim_thay = idx
                break

        if tim_thay >= 0:
            cu = gop[tim_thay]
            cu["mucDoUuTien"] = max(_ep_uu_tien(cu.get("mucDoUuTien"), 3), uu_tien)
            cu["ngay"] = max(str(cu.get("ngay") or ""), ngay)
            if len(noi_dung) > len(str(cu.get("noiDung") or "")):
                cu["noiDung"] = noi_dung
        else:
            gop.append(
                {
                    "ngay": ngay,
                    "loai": loai,
                    "noiDung": noi_dung,
                    "mucDoUuTien": uu_tien,
                }
            )

    if len(gop) > toi_da:
        # Giu uu tien cao nhat, sau do ngay moi nhat va bai duoc them sau cung
        xep_hang = list(enumerate(gop))
        xep_hang.sort(
            key=lambda cap: (
                _ep_uu_tien(cap[1].get("mucDoUuTien"), 3),
                str(cap[1].get("ngay") or ""),
                cap[0],
            ),
            reverse=True,
        )
        gop = [item for _, item in xep_hang[:toi_da]]
        gop.sort(
            key=lambda b: (
                -_ep_uu_tien(b.get("mucDoUuTien"), 3),
                str(b.get("ngay") or ""),
            )
        )

    return gop


def them_bai_hoc(
    du_lieu: dict[str, Any],
    loai: str,
    noi_dung: str,
    muc_do_uu_tien: int = 3,
    ngay: str | None = None,
    toi_da: int = TOI_DA_BAI_HOC,
) -> list[dict[str, Any]]:
    """Them 1 bai hoc moi vao bai_hoc_rut_ra, tu dong gop trung va gioi han toi da 25 bai."""
    du_lieu.setdefault("bai_hoc_rut_ra", [])
    sach = re.sub(r"\s+", " ", (noi_dung or "").strip())
    if not sach:
        return du_lieu["bai_hoc_rut_ra"]

    du_lieu["bai_hoc_rut_ra"].append(
        {
            "ngay": ngay or _ngay_hom_nay(),
            "loai": _chuan_hoa_loai_bai_hoc(loai),
            "noiDung": sach,
            "mucDoUuTien": _ep_uu_tien(muc_do_uu_tien, 3),
        }
    )
    du_lieu["bai_hoc_rut_ra"] = _tia_va_gop_bai_hoc(du_lieu["bai_hoc_rut_ra"], toi_da=toi_da)
    return du_lieu["bai_hoc_rut_ra"]


def tao_ngu_canh_hoc_hoi(
    duong_dan: Path | str | None = None,
    du_lieu: dict[str, Any] | None = None,
    toi_da_chu_de: int = 12,
    toi_da_bai_hoc: int = 10,
) -> str:
    """
    Tra ve chuoi ngu canh ngan gon de tiem vao prompt bien kich:
    - Danh sach chu de da lam (chong lap + goi y cau 'callback' hai huoc nhac tap cu)
    - Top bai hoc bat buoc ap dung tu kho bai_hoc_rut_ra.
    """
    bo_nho = _chuan_hoa_cau_truc_bo_nho(du_lieu) if du_lieu is not None else tai_bo_nho(duong_dan)
    da_lam = list(bo_nho.get("chu_de_da_lam") or [])
    bai_hoc = list(bo_nho.get("bai_hoc_rut_ra") or [])

    if not da_lam and not bai_hoc:
        return (
            "BO NHO HOC HOI HIEN TAI: Day la tap phim dau tien trong he thong. "
            "Hay giu phong cach ke chuyen lich su Toan hoc thien nhien + hai huoc di dom, "
            "chinh xac Toan hoc va KHONG danh dam."
        )

    dong: list[str] = ["=== BO NHO TU HOC HOI (BAT BUOC THAM CHIEU) ==="]

    if da_lam:
        dong.append(
            "1. CAC TAP DA SAN XUAT (KHONG lap lai chu de nay; co the cai 1 cau 'callback' hai huoc "
            "nhac duyen dang toi nhan vat/su kien tap cu neu phu hop mach chuyen):"
        )
        for tap in da_lam[-toi_da_chu_de:]:
            td = tap.get("tieuDe") or tap.get("slug") or ""
            nv = tap.get("nhanVatChinh") or ""
            tt = tap.get("tomTat1Cau") or ""
            dong.append(f"   - [{tap.get('slug', '')}] {td} (Nhan vat: {nv}): {tt}")
    else:
        dong.append("1. CAC TAP DA SAN XUAT: Chua co tap nao truoc do.")

    if bai_hoc:
        bai_hoc_sap_xep = sorted(
            bai_hoc,
            key=lambda b: (_ep_uu_tien(b.get("mucDoUuTien"), 3), str(b.get("ngay") or "")),
            reverse=True,
        )[:toi_da_bai_hoc]
        dong.append("2. TOP BAI HOC & QUY TAC BAT BUOC AP DUNG:")
        for bh in bai_hoc_sap_xep:
            dong.append(
                f"   - [{bh.get('loai', 'kich_ban')} | uu tien {bh.get('mucDoUuTien', 3)}/5] "
                f"{bh.get('noiDung', '')}"
            )

    return "\n".join(dong)


def hoc_tu_phan_hoi(
    slug: str,
    ghi_chu: str,
    duong_dan: Path | str | None = None,
    client: GeminiClient | None = None,
) -> list[dict[str, Any]]:
    """Ghi nhan phan hoi/chi so kenh va nho Gemini rut ra bai hoc moi nap vao bai_hoc_rut_ra."""
    bo_nho = tai_bo_nho(duong_dan)
    gemini = client or GeminiClient()

    tap_lien_quan = next(
        (t for t in bo_nho.get("chu_de_da_lam") or [] if t.get("slug") == _tao_slug_sach(slug)),
        None,
    )
    thong_tin_tap = (
        f"Tap '{tap_lien_quan.get('tieuDe')}' (slug={slug}, thoi luong={tap_lien_quan.get('thoiLuongGiay')}s)"
        if tap_lien_quan
        else f"Tap slug='{slug}'"
    )

    prompt = f"""
Ban la chuyen gia phan tich chat luong kenh phim hoat hinh ke chuyen lich su Toan hoc (>10 phut, thien nhien + hai huoc di dom, KHONG danh dam).
Day la phan hoi / chi so kenh cho {thong_tin_tap}:
"{ghi_chu}"

Hay rut ra 1 den 3 bai hoc CU THE, ngan gon, co the ap dung ngay cho cac tap sau.
Chi chon `loai` trong: {", ".join(LOAI_BAI_HOC_HOP_LE)}.
`mucDoUuTien` tu 1 (thap) den 5 (rat quan trong).

Tra ve DUY NHAT JSON dung cau truc:
{{
  "baiHocMoi": [
    {{
      "loai": "hai_huoc",
      "noiDung": "Quy tac cu the ap dung cho tap sau...",
      "mucDoUuTien": 4
    }}
  ]
}}
""".strip()

    phan_hoi_ai = gemini.tao_json(
        prompt=prompt,
        system_instruction="Tra ve DUY NHAT JSON hop le gom mang baiHocMoi.",
        nhiet_do=0.4,
        max_output_tokens=1024,
    )
    raw_list = phan_hoi_ai.get("baiHocMoi") if isinstance(phan_hoi_ai, dict) else []
    bai_hoc_moi: list[dict[str, Any]] = []
    if isinstance(raw_list, list):
        for item in raw_list[:5]:
            if not isinstance(item, dict):
                continue
            nd = str(item.get("noiDung") or "").strip()
            if not nd:
                continue
            loai = _chuan_hoa_loai_bai_hoc(item.get("loai"))
            uu_tien = _ep_uu_tien(item.get("mucDoUuTien"), 3)
            them_bai_hoc(bo_nho, loai=loai, noi_dung=nd, muc_do_uu_tien=uu_tien)
            bai_hoc_moi.append(
                {
                    "ngay": _ngay_hom_nay(),
                    "loai": loai,
                    "noiDung": nd,
                    "mucDoUuTien": uu_tien,
                }
            )

    bo_nho.setdefault("phan_hoi_kenh", []).append(
        {
            "ngay": _ngay_hom_nay(),
            "slug": _tao_slug_sach(slug),
            "ghiChu": str(ghi_chu).strip(),
            "baiHocDaRut": [b["noiDung"] for b in bai_hoc_moi],
        }
    )
    luu_bo_nho(bo_nho, duong_dan)
    return bai_hoc_moi


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Quan ly bo nho tu hoc hoi ben vung & hang doi chu de (du_lieu/bo_nho_hoc_hoi.json)."
    )
    parser.add_argument(
        "--bo-nho",
        default="",
        help="Duong dan tuy chinh toi bo_nho_hoc_hoi.json (mac dinh du_lieu/bo_nho_hoc_hoi.json).",
    )
    parser.add_argument(
        "--hoc-tu-phan-hoi",
        action="store_true",
        help="Ghi nhan phan hoi kenh va nho Gemini rut ra bai hoc moi.",
    )
    parser.add_argument("--slug", default="", help="Slug cua tap phim can ghi nhan phan hoi.")
    parser.add_argument("--ghi-chu", default="", help="Noi dung phan hoi/chi so kenh.")
    parser.add_argument(
        "--xem-ngu-canh",
        action="store_true",
        help="In chuoi ngu canh hoc hoi hien tai.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    duong_dan = Path(args.bo_nho) if args.bo_nho else DUONG_DAN_BO_NHO_MAC_DINH

    if args.hoc_tu_phan_hoi:
        if not args.slug.strip() or not args.ghi_chu.strip():
            print("[LOI] --hoc-tu-phan-hoi can truyen du --slug va --ghi-chu.")
            return 2
        moi = hoc_tu_phan_hoi(slug=args.slug.strip(), ghi_chu=args.ghi_chu.strip(), duong_dan=duong_dan)
        print(f"[OK] Da ghi nhan phan hoi cho '{args.slug.strip()}' va rut ra {len(moi)} bai hoc moi:")
        for b in moi:
            print(f"  - [{b['loai']} | {b['mucDoUuTien']}/5] {b['noiDung']}")
        return 0

    if args.xem_ngu_canh:
        print(tao_ngu_canh_hoc_hoi(duong_dan=duong_dan))
        return 0

    bo_nho = tai_bo_nho(duong_dan)
    print(
        f"[Bo nho hoc hoi] {duong_dan}\n"
        f"  - Chu de da lam  : {len(bo_nho['chu_de_da_lam'])}\n"
        f"  - Hang doi chu de: {len(bo_nho['hang_doi_chu_de'])} (dang cho: {dem_chu_de_dang_cho(bo_nho)})\n"
        f"  - Bai hoc rut ra : {len(bo_nho['bai_hoc_rut_ra'])}/{TOI_DA_BAI_HOC}\n"
        f"  - Phan hoi kenh  : {len(bo_nho['phan_hoi_kenh'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
