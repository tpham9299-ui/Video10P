# -*- coding: utf-8 -*-
"""Bo nho tu hoc hoi ben vung, hang doi chu de & vong tu hoc tu so lieu YouTube that (v1.0)."""

from __future__ import annotations

import argparse
import csv
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
THU_MUC_DU_LIEU_MAC_DINH = GOC_DU_AN / "du_lieu"
LOAI_BAI_HOC_HOP_LE: tuple[str, ...] = (
    "toan_hoc",
    "kich_ban",
    "hai_huoc",
    "thoi_luong",
    "hinh_anh",
    "hook",
    "thumbnail",
    "giu_chan",
)
LOAI_BAI_HOC_YOUTUBE: tuple[str, ...] = ("hook", "thumbnail", "giu_chan")
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


def _ep_so_nguyen_tuy_chon(gia_tri: Any) -> int | None:
    if gia_tri is None or isinstance(gia_tri, bool):
        return None
    if isinstance(gia_tri, int):
        return max(0, gia_tri)
    if isinstance(gia_tri, float) and math.isfinite(gia_tri):
        return max(0, int(round(gia_tri)))
    s = str(gia_tri).strip().replace(",", "").replace(".", "")
    if not s:
        return None
    try:
        return max(0, int(s))
    except ValueError:
        return None


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
        anh_xa = {
            "ctr": "thumbnail",
            "anh_bia": "thumbnail",
            "retention": "giu_chan",
            "nhip_ke": "giu_chan",
            "mo_dau": "hook",
            "hook_30s": "hook",
        }
        if s in anh_xa:
            return anh_xa[s]
    return "kich_ban"


def _chuan_hoa_trang_thai(gia_tri: Any) -> str:
    if isinstance(gia_tri, str):
        s = _chuan_hoa_chuoi_so_sanh(gia_tri).replace(" ", "_")
        if s in TRANG_THAI_HANG_DOI_HOP_LE:
            return s
    return "cho"


def _phan_tich_phan_tram(gia_tri: Any) -> float | None:
    """Chuyen chuoi/so phan tram (vd: 7.8, '7.8%', '68,5 %') thanh float [0..100]."""
    if gia_tri is None or isinstance(gia_tri, bool):
        return None
    if isinstance(gia_tri, (int, float)):
        if not math.isfinite(float(gia_tri)):
            return None
        return round(max(0.0, min(100.0, float(gia_tri))), 2)
    s = str(gia_tri).strip().replace("%", "").replace(" ", "")
    if not s:
        return None
    if "," in s and "." not in s:
        s = s.replace(",", ".")
    try:
        so = float(s)
    except ValueError:
        return None
    if not math.isfinite(so):
        return None
    return round(max(0.0, min(100.0, so)), 2)


def chuyen_moc_thoi_gian_sang_giay(moc: Any) -> float | None:
    """Chuyen moc thoi gian ('00:45', '04:20', '1:02:10', '345', '5m45s') thanh giay."""
    if moc is None or isinstance(moc, bool):
        return None
    if isinstance(moc, (int, float)):
        if not math.isfinite(float(moc)):
            return None
        return round(max(0.0, float(moc)), 2)
    s = str(moc).strip()
    if not s:
        return None
    # Dinh dang H:MM:SS hoac MM:SS
    if ":" in s:
        phan = [p.strip() for p in s.split(":")]
        if len(phan) in (2, 3):
            try:
                so = [float(p) for p in phan]
            except ValueError:
                return None
            if len(so) == 2:
                return round(max(0.0, so[0] * 60.0 + so[1]), 2)
            return round(max(0.0, so[0] * 3600.0 + so[1] * 60.0 + so[2]), 2)
    # Dinh dang 5m45s / 45s
    khop_ms = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+(?:\.\d+)?)s)?", s.lower())
    if khop_ms and any(khop_ms.groups()):
        gio = float(khop_ms.group(1) or 0)
        phut = float(khop_ms.group(2) or 0)
        giay = float(khop_ms.group(3) or 0)
        return round(max(0.0, gio * 3600.0 + phut * 60.0 + giay), 2)
    # So thuan
    s_num = s.replace(",", ".") if ("," in s and "." not in s) else s
    try:
        so_f = float(s_num)
    except ValueError:
        return None
    if not math.isfinite(so_f):
        return None
    return round(max(0.0, so_f), 2)


def _dinh_dang_mm_ss(giay: float) -> str:
    tong = max(0, int(round(giay)))
    gio = tong // 3600
    phut = (tong % 3600) // 60
    s = tong % 60
    if gio > 0:
        return f"{gio}:{phut:02d}:{s:02d}"
    return f"{phut:02d}:{s:02d}"


def _phan_tich_moc_tut_view(gia_tri: Any) -> list[str]:
    """Chuan hoa danh sach moc tut view (vd: '00:45, 04:20' -> ['00:45', '04:20'])."""
    if gia_tri is None:
        return []
    cac_muc: list[str] = []
    if isinstance(gia_tri, (list, tuple)):
        for m in gia_tri:
            s = str(m or "").strip()
            if s:
                cac_muc.append(s)
    else:
        raw = str(gia_tri).strip()
        if raw:
            for m in re.split(r"[,;|\n]+", raw):
                s = m.strip()
                if s:
                    cac_muc.append(s)

    ket_qua: list[str] = []
    for m in cac_muc:
        giay = chuyen_moc_thoi_gian_sang_giay(m)
        chuan = _dinh_dang_mm_ss(giay) if giay is not None else m[:24]
        if chuan and chuan not in ket_qua:
            ket_qua.append(chuan)
    return ket_qua[:12]


def _phan_tich_binh_luan(gia_tri: Any) -> list[str]:
    """Chuan hoa danh sach binh luan noi bat tu list hoac chuoi phan tach boi | ; hoac xuong dong."""
    if gia_tri is None:
        return []
    raw_list: list[str] = []
    if isinstance(gia_tri, (list, tuple)):
        for item in gia_tri:
            s = str(item or "").strip()
            if not s:
                continue
            if "|" in s or "\n" in s:
                raw_list.extend(p.strip() for p in re.split(r"[|\n]+", s) if p.strip())
            else:
                raw_list.append(s)
    else:
        s = str(gia_tri).strip()
        if s:
            raw_list.extend(p.strip() for p in re.split(r"[|;\n]+", s) if p.strip())

    ket_qua: list[str] = []
    for bl in raw_list:
        sach = re.sub(r"\s+", " ", bl).strip()[:300]
        if sach and sach not in ket_qua:
            ket_qua.append(sach)
    return ket_qua[:15]


def _chuan_hoa_ten_cot(ten: str) -> str:
    s = _chuan_hoa_chuoi_so_sanh(ten).replace(" ", "_")
    return re.sub(r"_+", "_", s).strip("_")


def _tim_gia_tri_theo_bi_danh(raw: dict[str, Any], bi_danh: tuple[str, ...]) -> Any:
    for khoa in bi_danh:
        if khoa in raw and raw[khoa] not in (None, ""):
            return raw[khoa]
    ban_do = {_chuan_hoa_ten_cot(str(k)): v for k, v in raw.items()}
    for khoa in bi_danh:
        k_chuan = _chuan_hoa_ten_cot(khoa)
        if k_chuan in ban_do and ban_do[k_chuan] not in (None, ""):
            return ban_do[k_chuan]
    return None


def chuan_hoa_so_lieu_youtube(raw: dict[str, Any]) -> dict[str, Any]:
    """Chuan hoa du lieu chi so YouTube (CLI, CSV/JSON YouTube Studio hoac YouTube API)."""
    du_lieu = raw if isinstance(raw, dict) else {}

    ctr = _phan_tich_phan_tram(
        _tim_gia_tri_theo_bi_danh(
            du_lieu,
            (
                "ctr_phan_tram",
                "ctr",
                "ctrPhanTram",
                "impressions_click_through_rate",
                "impressions_click_through_rate_%",
                "click_through_rate",
                "ty_le_nhap",
                "ty_le_nhap_hien_thi",
            ),
        )
    )
    giu_chan_30s = _phan_tich_phan_tram(
        _tim_gia_tri_theo_bi_danh(
            du_lieu,
            (
                "giu_chan_30s",
                "giuChan30s",
                "retention_30s",
                "giu_chan_30_giay",
                "still_watching_at_0_30",
                "intro_retention",
                "ty_le_giu_chan_30s",
            ),
        )
    )
    thoi_luong_tb = chuyen_moc_thoi_gian_sang_giay(
        _tim_gia_tri_theo_bi_danh(
            du_lieu,
            (
                "thoi_luong_xem_tb_giay",
                "thoiLuongXemTbGiay",
                "thoi_luong_xem_tb",
                "thoi_luong_xem_trung_binh",
                "average_view_duration",
                "avd",
            ),
        )
    )
    moc_tut = _phan_tich_moc_tut_view(
        _tim_gia_tri_theo_bi_danh(
            du_lieu,
            (
                "moc_tut_view",
                "mocTutView",
                "cac_moc_tut_view",
                "drop_off_points",
                "dropoff_timestamps",
            ),
        )
    )
    thumb_raw = _tim_gia_tri_theo_bi_danh(
        du_lieu,
        (
            "bien_the_thumbnail_thang",
            "bienTheThumbnailThang",
            "thumbnail_thang",
            "winning_thumbnail",
            "thumbnail_winner",
        ),
    )
    bien_the_thumb = str(thumb_raw).strip()[:60] if thumb_raw is not None else ""
    binh_luan = _phan_tich_binh_luan(
        _tim_gia_tri_theo_bi_danh(
            du_lieu,
            (
                "binh_luan_noi_bat",
                "binhLuanNoiBat",
                "top_comments",
                "comments",
                "binh_luan",
            ),
        )
    )

    ket_qua: dict[str, Any] = {
        "ctr_phan_tram": ctr,
        "giu_chan_30s": giu_chan_30s,
        "thoi_luong_xem_tb_giay": thoi_luong_tb,
        "moc_tut_view": moc_tut,
        "bien_the_thumbnail_thang": bien_the_thumb,
        "binh_luan_noi_bat": binh_luan,
    }

    video_id_raw = _tim_gia_tri_theo_bi_danh(du_lieu, ("video_id", "videoId", "id_video", "content"))
    if video_id_raw is not None:
        vid = str(video_id_raw).strip()
        if vid and vid.lower() != "total":
            ket_qua["video_id"] = vid[:64]

    luot_xem = _ep_so_nguyen_tuy_chon(
        _tim_gia_tri_theo_bi_danh(du_lieu, ("luot_xem", "luotXem", "views", "viewCount"))
    )
    if luot_xem is not None:
        ket_qua["luot_xem"] = luot_xem

    luot_thich = _ep_so_nguyen_tuy_chon(
        _tim_gia_tri_theo_bi_danh(du_lieu, ("luot_thich", "luotThich", "likes", "likeCount"))
    )
    if luot_thich is not None:
        ket_qua["luot_thich"] = luot_thich

    so_binh_luan = _ep_so_nguyen_tuy_chon(
        _tim_gia_tri_theo_bi_danh(du_lieu, ("so_binh_luan", "soBinhLuan", "comment_count", "commentCount"))
    )
    if so_binh_luan is not None:
        ket_qua["so_binh_luan"] = so_binh_luan

    return ket_qua


def _co_so_lieu_youtube_hop_le(so_lieu: dict[str, Any]) -> bool:
    if not isinstance(so_lieu, dict):
        return False
    return any(
        [
            so_lieu.get("ctr_phan_tram") is not None,
            so_lieu.get("giu_chan_30s") is not None,
            so_lieu.get("thoi_luong_xem_tb_giay") is not None,
            bool(so_lieu.get("moc_tut_view")),
            bool(str(so_lieu.get("bien_the_thumbnail_thang") or "").strip()),
            bool(so_lieu.get("binh_luan_noi_bat")),
            so_lieu.get("luot_xem") is not None,
            so_lieu.get("luot_thich") is not None,
        ]
    )


def doc_so_lieu_youtube_tu_file(
    duong_dan_file: Path | str,
    slug_mac_dinh: str = "",
) -> list[dict[str, Any]]:
    """
    Doc file CSV hoac JSON xuat tu YouTube Studio thanh danh sach ban ghi chuan hoa.
    Moi phan tu gom: {"slug", "ghiChu", "soLieuYouTube", "nguon"}.
    """
    path = Path(duong_dan_file)
    if not path.exists():
        raise FileNotFoundError(f"Khong tim thay file so lieu YouTube: {path}")

    duoi = path.suffix.lower()
    dong_tho: list[dict[str, Any]] = []
    nguon = "csv" if duoi == ".csv" else "json"

    if duoi == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                if not isinstance(row, dict):
                    continue
                # Bo qua dong tong ket 'Total' cua YouTube Studio
                val_dau = next((str(v or "").strip() for v in row.values() if str(v or "").strip()), "")
                if val_dau.lower() in ("total", "tong", "tổng"):
                    continue
                dong_tho.append(dict(row))
    else:
        raw_text = path.read_text(encoding="utf-8-sig")
        raw_json = json.loads(raw_text)
        if isinstance(raw_json, list):
            dong_tho = [r for r in raw_json if isinstance(r, dict)]
        elif isinstance(raw_json, dict):
            for khoa_list in ("tap", "videos", "items", "du_lieu", "records"):
                if isinstance(raw_json.get(khoa_list), list):
                    dong_tho = [r for r in raw_json[khoa_list] if isinstance(r, dict)]
                    break
            else:
                dong_tho = [raw_json]
        else:
            raise ValueError(f"Cau truc JSON khong hop le trong file: {path}")

    ket_qua: list[dict[str, Any]] = []
    for item in dong_tho:
        slug_raw = _tim_gia_tri_theo_bi_danh(
            item,
            ("slug", "ma_tap", "video_title", "tieu_de", "tieuDe", "title"),
        )
        slug_val = str(slug_raw or slug_mac_dinh).strip()
        if not slug_val:
            vid_fallback = _tim_gia_tri_theo_bi_danh(item, ("video_id", "videoId", "content"))
            slug_val = str(vid_fallback or "").strip()
        if not slug_val:
            continue

        ghi_chu_raw = _tim_gia_tri_theo_bi_danh(item, ("ghi_chu", "ghiChu", "notes", "note"))
        so_lieu = chuan_hoa_so_lieu_youtube(item)
        if not _co_so_lieu_youtube_hop_le(so_lieu) and not str(ghi_chu_raw or "").strip():
            continue

        ket_qua.append(
            {
                "slug": _tao_slug_sach(slug_val),
                "ghiChu": str(ghi_chu_raw or "").strip(),
                "soLieuYouTube": so_lieu,
                "nguon": nguon,
            }
        )
    return ket_qua


def tao_bo_nho_rong() -> dict[str, Any]:
    """Khoi tao cau truc bo nho hoc hoi sach gom 4 phan chuan."""
    return {
        "phienBan": "1.0",
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
    if isinstance(raw.get("phienBan"), str) and raw["phienBan"].strip():
        goc["phienBan"] = raw["phienBan"].strip()
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
    """Chon chu de trangThai='cho' co diem cao nhat trong hang_doi_chu_de (loai tru moi slug da lam)."""
    da_lam = {
        _tao_slug_sach(str(item.get("slug") or item.get("tieuDe") or ""))
        for item in (du_lieu.get("chu_de_da_lam") or [])
        if isinstance(item, dict)
    }
    bo_qua = {_tao_slug_sach(s) for s in (loai_tru_slugs or set())} | da_lam
    ung_vien = [
        item
        for item in (du_lieu.get("hang_doi_chu_de") or [])
        if isinstance(item, dict)
        and item.get("trangThai") == "cho"
        and _tao_slug_sach(str(item.get("slug") or "")) not in bo_qua
    ]
    if not ung_vien:
        return None
    ung_vien.sort(key=diem_xep_hang_chu_de, reverse=True)
    return ung_vien[0]


def xoa_chu_de_khoi_hang_doi(
    du_lieu: dict[str, Any],
    slug: str,
) -> bool:
    """Xoa chu de khoi hang_doi_chu_de sau khi da hoan thanh de giu hang doi gon sach, chong trung ngay hom sau."""
    slug_sach = _tao_slug_sach(slug)
    hang_doi_cu = du_lieu.get("hang_doi_chu_de") or []
    hang_doi_moi = [
        item
        for item in hang_doi_cu
        if not (isinstance(item, dict) and _tao_slug_sach(str(item.get("slug") or "")) == slug_sach)
    ]
    if len(hang_doi_moi) != len(hang_doi_cu):
        du_lieu["hang_doi_chu_de"] = hang_doi_moi
        return True
    return False


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
    xoa_khoi_hang_doi: bool = False,
) -> dict[str, Any]:
    """Luu tap da san xuat vao chu_de_da_lam va danh dau 'xong' (hoac xoa khoi hang_doi_chu_de)."""
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

    if xoa_khoi_hang_doi:
        xoa_chu_de_khoi_hang_doi(du_lieu, slug_sach)
    else:
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


def tai_ngu_canh_kich_ban_doi_chieu(
    slug: str,
    thu_muc_du_lieu: Path | None = None,
    moc_tut_view: list[str] | None = None,
    fps: int = 30,
) -> str:
    """
    Doc kich ban da luu (du_lieu_render.json hoac nhap_kich_ban.json) cua tap `slug`
    de Gemini doi chieu truc tiep Hook 30s, Thumbnail A/B va cac canh tai `moc_tut_view`.
    """
    slug_sach = _tao_slug_sach(slug)
    goc_dl = thu_muc_du_lieu or THU_MUC_DU_LIEU_MAC_DINH
    thu_muc_tap = goc_dl / slug_sach

    file_kb: Path | None = None
    for ten in ("du_lieu_render.json", "nhap_kich_ban.json"):
        p = thu_muc_tap / ten
        if p.exists():
            file_kb = p
            break

    if file_kb is None:
        return "Khong tim thay file kich ban luu tren dia cho tap nay (chi phan tich theo so lieu cung cap)."

    try:
        kb = json.loads(file_kb.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "Khong doc duoc file kich ban cua tap nay."

    if not isinstance(kb, dict):
        return "Du lieu kich ban khong hop le."

    dong: list[str] = [f"=== DOI CHIEU KICH BAN THUC TE ({file_kb.name}) ==="]
    tieu_de = str(kb.get("tieuDe") or slug_sach).strip()
    dong.append(f"- Tieu de: {tieu_de}")

    tat_ca_canh: list[tuple[str, dict[str, Any]]] = []
    cac_hoi_tom_tat: list[str] = []
    for idx_ch, ch in enumerate(kb.get("chuong") or [], start=1):
        if not isinstance(ch, dict):
            continue
        ten_ch = str(ch.get("tenChuong") or f"Hoi {idx_ch}").strip()
        ds_c = [c for c in (ch.get("canh") or []) if isinstance(c, dict)]
        if ds_c:
            tu_f = int(ds_c[0].get("tuFrame") or 0)
            den_f = int(ds_c[-1].get("denFrame") or 0)
            moc_ch = f"{_dinh_dang_mm_ss(tu_f / float(fps))}..{_dinh_dang_mm_ss(den_f / float(fps))}" if den_f > tu_f else f"{len(ds_c)} canh"
            cac_hoi_tom_tat.append(f"  * {ten_ch} ({moc_ch}, {len(ds_c)} canh)")
            for c in ds_c:
                tat_ca_canh.append((ten_ch, c))

    if cac_hoi_tom_tat:
        dong.append("- Cau truc cac hoi:")
        dong.extend(cac_hoi_tom_tat[:8])

    # 1. Hook 30 giay dau
    hook_canh: list[str] = []
    for idx_c, (_, c) in enumerate(tat_ca_canh[:5], start=1):
        tu_f = int(c.get("tuFrame") or 0)
        den_f = int(c.get("denFrame") or 0)
        if idx_c > 3 and tu_f > 35 * fps:
            break
        moc = f"{_dinh_dang_mm_ss(tu_f / float(fps))}-{_dinh_dang_mm_ss(den_f / float(fps))}" if den_f > tu_f else f"canh #{idx_c}"
        cam = str((c.get("camera") or {}).get("kieu") or "tinh")
        thoai = re.sub(r"\s+", " ", str(c.get("loiThoai") or "").strip())[:160]
        hook_canh.append(
            f"  * [{c.get('id', f'canh_{idx_c}')} | {moc} | boCuc={c.get('boCuc', '')} | cam={cam}] {thoai}"
        )
    if hook_canh:
        dong.append("- Doan Hook 30 giay dau:")
        dong.extend(hook_canh)

    # 2. 3 phuong an Thumbnail A/B (de doi chieu bien_the_thumbnail_thang)
    goi_y_thumb = kb.get("goiYThumbnail")
    if isinstance(goi_y_thumb, list) and goi_y_thumb:
        dong.append("- Cac bien the Thumbnail A/B da thiet ke:")
        for item in goi_y_thumb[:3]:
            if not isinstance(item, dict):
                continue
            dong.append(
                f"  * Bien the {item.get('bien_the', '?')}: tieuDeLon='{item.get('tieuDeLon', '')}', "
                f"nhanPhu='{item.get('nhanPhu', '')}', congThuc='{item.get('congThucLatex', '')}', "
                f"daoCu='{item.get('daoCuNoiBat', '')}', bieuCam='{item.get('bieuCam', '')}', "
                f"boiCanh='{item.get('boiCanh', '')}'"
            )

    # 3. Anh xa chinh xac tung moc_tut_view sang canh tuong ung trong kich ban
    if moc_tut_view and tat_ca_canh:
        dong.append("- Canh phat tai cac moc tut view:")
        for moc in moc_tut_view:
            giay = chuyen_moc_thoi_gian_sang_giay(moc)
            if giay is None:
                continue
            frame_muc_tieu = int(round(giay * fps))
            canh_khop: tuple[str, dict[str, Any]] | None = None
            for ten_ch, c in tat_ca_canh:
                tu_f = int(c.get("tuFrame") or 0)
                den_f = int(c.get("denFrame") or 0)
                if den_f > tu_f and tu_f <= frame_muc_tieu < den_f:
                    canh_khop = (ten_ch, c)
                    break
            if canh_khop is None:
                # Tim canh gan nhat neu moc tut o ranh gioi
                canh_co_frame = [
                    (ten_ch, c) for ten_ch, c in tat_ca_canh if int(c.get("denFrame") or 0) > int(c.get("tuFrame") or 0)
                ]
                if canh_co_frame:
                    canh_khop = min(
                        canh_co_frame,
                        key=lambda cap: abs(((int(cap[1]["tuFrame"]) + int(cap[1]["denFrame"])) / 2.0) - frame_muc_tieu),
                    )
            if canh_khop is not None:
                ten_ch, c = canh_khop
                cam = str((c.get("camera") or {}).get("kieu") or "tinh")
                thoai = re.sub(r"\s+", " ", str(c.get("loiThoai") or "").strip())[:170]
                dong.append(
                    f"  * Moc {moc} ({int(round(giay))}s) -> {ten_ch} / {c.get('id', '')} "
                    f"(boCuc={c.get('boCuc', '')}, boiCanh={c.get('boiCanh', '')}, cam={cam}): \"{thoai}\""
                )

    return "\n".join(dong)


def _tong_hop_so_lieu_kenh_cho_ngu_canh(phan_hoi_kenh: list[dict[str, Any]]) -> list[str]:
    """Tom tat chi so CTR, giu chan 30s, thoi luong xem TB va Thumbnail thang tu phan_hoi_kenh."""
    ctrs: list[float] = []
    ret30s: list[float] = []
    avds: list[float] = []
    dem_thumb: dict[str, int] = {}
    moc_tut_gan_day: list[str] = []

    for item in phan_hoi_kenh:
        if not isinstance(item, dict):
            continue
        sl = item.get("soLieuYouTube")
        if not isinstance(sl, dict):
            continue
        if isinstance(sl.get("ctr_phan_tram"), (int, float)):
            ctrs.append(float(sl["ctr_phan_tram"]))
        if isinstance(sl.get("giu_chan_30s"), (int, float)):
            ret30s.append(float(sl["giu_chan_30s"]))
        if isinstance(sl.get("thoi_luong_xem_tb_giay"), (int, float)):
            avds.append(float(sl["thoi_luong_xem_tb_giay"]))
        bt = str(sl.get("bien_the_thumbnail_thang") or "").strip()
        if bt:
            dem_thumb[bt] = dem_thumb.get(bt, 0) + 1
        slug_tap = str(item.get("slug") or "")
        for m in (sl.get("moc_tut_view") or [])[:3]:
            nhan = f"{m} ({slug_tap})" if slug_tap else str(m)
            if nhan not in moc_tut_gan_day:
                moc_tut_gan_day.append(nhan)

    dong: list[str] = []
    chi_so_tb: list[str] = []
    if ctrs:
        chi_so_tb.append(f"CTR trung binh={sum(ctrs)/len(ctrs):.2f}% ({len(ctrs)} tap)")
    if ret30s:
        chi_so_tb.append(f"Giu chan 30s TB={sum(ret30s)/len(ret30s):.1f}%")
    if avds:
        tb_s = sum(avds) / len(avds)
        chi_so_tb.append(f"Thoi luong xem TB={_dinh_dang_mm_ss(tb_s)} ({tb_s:.0f}s)")
    if chi_so_tb:
        dong.append("   - Chi so YouTube thuc te cua kenh: " + " | ".join(chi_so_tb))

    if dem_thumb:
        xep_thumb = sorted(dem_thumb.items(), key=lambda kv: (-kv[1], kv[0]))
        chuoi_thumb = ", ".join(f"bien the '{k}' ({v} lan thang)" for k, v in xep_thumb[:3])
        dong.append(
            f"   - Bien the Thumbnail A/B thang nhieu nhat: {chuoi_thumb} "
            "(uu tien nhan rong phong cach nay khi thiet ke goiYThumbnail)."
        )

    if moc_tut_gan_day:
        dong.append(
            "   - Cac moc thuong bi tut view o tap cu: "
            + ", ".join(moc_tut_gan_day[-6:])
            + " -> can chen mieng hai, doi goc may hoac cau hoi mo to mo ngay truoc cac moc nay."
        )

    return dong


def tao_ngu_canh_hoc_hoi(
    duong_dan: Path | str | None = None,
    du_lieu: dict[str, Any] | None = None,
    toi_da_chu_de: int = 12,
    toi_da_bai_hoc: int = 10,
) -> str:
    """
    Tra ve chuoi ngu canh ngan gon de tiem vao prompt bien kich va goi y Thumbnail:
    - Danh sach chu de da lam (chong lap + goi y cau 'callback' hai huoc nhac tap cu)
    - Top bai hoc bat buoc ap dung tu kho bai_hoc_rut_ra
    - Quy tac toi uu CTR, Hook 30s, giu chan & Thumbnail A/B tu so lieu YouTube that.
    """
    bo_nho = _chuan_hoa_cau_truc_bo_nho(du_lieu) if du_lieu is not None else tai_bo_nho(duong_dan)
    da_lam = list(bo_nho.get("chu_de_da_lam") or [])
    bai_hoc = list(bo_nho.get("bai_hoc_rut_ra") or [])
    phan_hoi = list(bo_nho.get("phan_hoi_kenh") or [])
    tom_tat_yt = _tong_hop_so_lieu_kenh_cho_ngu_canh(phan_hoi)

    if not da_lam and not bai_hoc and not tom_tat_yt:
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

    bai_hoc_yt = sorted(
        [b for b in bai_hoc if b.get("loai") in LOAI_BAI_HOC_YOUTUBE],
        key=lambda b: (_ep_uu_tien(b.get("mucDoUuTien"), 3), str(b.get("ngay") or "")),
        reverse=True,
    )[:6]
    if tom_tat_yt or bai_hoc_yt:
        dong.append(
            "3. QUY TAC TOI UU CTR, HOOK 30S, GIU CHAN & GOI Y THUMBNAIL TU SO LIEU YOUTUBE THAT:"
        )
        dong.extend(tom_tat_yt)
        for bh in bai_hoc_yt:
            dong.append(
                f"   - [YouTube/{bh.get('loai')} | uu tien {bh.get('mucDoUuTien', 3)}/5] "
                f"{bh.get('noiDung', '')}"
            )

    return "\n".join(dong)


def _dinh_dang_so_lieu_youtube_cho_prompt(so_lieu: dict[str, Any]) -> str:
    dong: list[str] = []
    if so_lieu.get("video_id"):
        dong.append(f"- Video ID: {so_lieu['video_id']}")
    if so_lieu.get("luot_xem") is not None:
        dong.append(f"- Luot xem: {so_lieu['luot_xem']}")
    if so_lieu.get("luot_thich") is not None:
        dong.append(f"- Luot thich: {so_lieu['luot_thich']}")
    if so_lieu.get("so_binh_luan") is not None:
        dong.append(f"- Tong so binh luan: {so_lieu['so_binh_luan']}")
    if so_lieu.get("ctr_phan_tram") is not None:
        dong.append(f"- CTR (ti le nhap): {so_lieu['ctr_phan_tram']}%")
    if so_lieu.get("giu_chan_30s") is not None:
        dong.append(f"- Giu chan 30 giay dau (Retention 30s): {so_lieu['giu_chan_30s']}%")
    if so_lieu.get("thoi_luong_xem_tb_giay") is not None:
        s = float(so_lieu["thoi_luong_xem_tb_giay"])
        dong.append(f"- Thoi luong xem trung binh: {_dinh_dang_mm_ss(s)} ({s:.1f} giay)")
    if so_lieu.get("moc_tut_view"):
        dong.append("- Cac moc tut view dot ngot: " + ", ".join(so_lieu["moc_tut_view"]))
    if so_lieu.get("bien_the_thumbnail_thang"):
        dong.append(f"- Bien the Thumbnail A/B thang: {so_lieu['bien_the_thumbnail_thang']}")
    if so_lieu.get("binh_luan_noi_bat"):
        dong.append("- Binh luan noi bat cua khan gia:")
        for bl in so_lieu["binh_luan_noi_bat"]:
            dong.append(f'  * "{bl}"')
    return "\n".join(dong)


def hoc_tu_phan_hoi(
    slug: str,
    ghi_chu: str = "",
    duong_dan: Path | str | None = None,
    client: GeminiClient | None = None,
    so_lieu_youtube: dict[str, Any] | None = None,
    thu_muc_du_lieu: Path | None = None,
    nguon: str = "cli",
    tu_dong_phan_tich: bool = True,
) -> list[dict[str, Any]]:
    """
    Ghi nhan phan hoi/so lieu YouTube that vao phan_hoi_kenh[], doi chieu kich ban cua tap
    va nho Gemini rut ra bai hoc cu the (Hook, nhip ke, Thumbnail A/B thang) nap vao bai_hoc_rut_ra[].
    """
    bo_nho = tai_bo_nho(duong_dan)
    slug_sach = _tao_slug_sach(slug)
    so_lieu_sach = chuan_hoa_so_lieu_youtube(so_lieu_youtube) if so_lieu_youtube is not None else None
    co_so_lieu = bool(so_lieu_sach and _co_so_lieu_youtube_hop_le(so_lieu_sach))

    tap_lien_quan = next(
        (t for t in bo_nho.get("chu_de_da_lam") or [] if _tao_slug_sach(str(t.get("slug") or "")) == slug_sach),
        None,
    )
    thong_tin_tap = (
        f"Tap '{tap_lien_quan.get('tieuDe')}' (slug={slug_sach}, thoi luong={tap_lien_quan.get('thoiLuongGiay')}s)"
        if tap_lien_quan
        else f"Tap slug='{slug_sach}'"
    )

    bai_hoc_moi: list[dict[str, Any]] = []

    if tu_dong_phan_tich:
        gemini = client or GeminiClient()
        phan_so_lieu = _dinh_dang_so_lieu_youtube_cho_prompt(so_lieu_sach) if (co_so_lieu and so_lieu_sach) else ""
        ngu_canh_kb = (
            tai_ngu_canh_kich_ban_doi_chieu(
                slug=slug_sach,
                thu_muc_du_lieu=thu_muc_du_lieu,
                moc_tut_view=so_lieu_sach.get("moc_tut_view") if so_lieu_sach else None,
            )
            if co_so_lieu
            else ""
        )

        khoi_du_lieu: list[str] = []
        if ghi_chu.strip():
            khoi_du_lieu.append(f'Ghi chu / phan hoi: "{ghi_chu.strip()}"')
        if phan_so_lieu:
            khoi_du_lieu.append("SO LIEU YOUTUBE THUC TE:\n" + phan_so_lieu)
        if ngu_canh_kb:
            khoi_du_lieu.append(ngu_canh_kb)

        yeu_cau_phan_tich = (
            "Hay phan tich cheo so lieu YouTube thuc te voi kich ban/Thumbnail cua tap nay de rut ra 2 den 4 bai hoc CU THE, "
            "ngan gon, co the ap dung ngay cho cac tap sau ve:\n"
            "  1. Hook 20-30s dau (tu giu_chan_30s & canh mo dau -> dung loai='hook')\n"
            "  2. Nhip ke & giu chan nguoi xem (tu thoi_luong_xem_tb_giay & cac canh tai moc_tut_view -> dung loai='giu_chan' hoac 'kich_ban'/'hai_huoc')\n"
            "  3. Thiet ke Thumbnail A/B (tu ctr_phan_tram & bien_the_thumbnail_thang doi chieu goiYThumbnail -> dung loai='thumbnail')\n"
            "  4. Phan hoi khan gia trong binh luan noi bat."
            if co_so_lieu
            else "Hay rut ra 1 den 3 bai hoc CU THE, ngan gon, co the ap dung ngay cho cac tap sau."
        )

        prompt = f"""
Ban la chuyen gia phan tich chat luong va tang truong kenh phim hoat hinh ke chuyen lich su Toan hoc (>10 phut, thien nhien + hai huoc di dom, KHONG danh dam).
Day la du lieu phan hoi & chi so kenh cho {thong_tin_tap}:

{chr(10).join(khoi_du_lieu)}

{yeu_cau_phan_tich}
Chi chon `loai` trong: {", ".join(LOAI_BAI_HOC_HOP_LE)}.
`mucDoUuTien` tu 1 (thap) den 5 (rat quan trong; uu tien 4-5 cho quy tac CTR/Hook/Giu chan rut tu so lieu that).

Tra ve DUY NHAT JSON dung cau truc:
{{
  "baiHocMoi": [
    {{
      "loai": "hook",
      "noiDung": "Quy tac cu the ap dung cho tap sau...",
      "mucDoUuTien": 5
    }}
  ]
}}
""".strip()

        phan_hoi_ai = gemini.tao_json(
            prompt=prompt,
            system_instruction="Tra ve DUY NHAT JSON hop le gom mang baiHocMoi.",
            nhiet_do=0.35,
            max_output_tokens=1536,
        )
        raw_list = phan_hoi_ai.get("baiHocMoi") if isinstance(phan_hoi_ai, dict) else []
        if isinstance(raw_list, list):
            for item in raw_list[:5]:
                if not isinstance(item, dict):
                    continue
                nd = str(item.get("noiDung") or "").strip()
                if not nd:
                    continue
                loai = _chuan_hoa_loai_bai_hoc(item.get("loai"))
                uu_tien = _ep_uu_tien(item.get("mucDoUuTien"), 4 if co_so_lieu else 3)
                them_bai_hoc(bo_nho, loai=loai, noi_dung=nd, muc_do_uu_tien=uu_tien)
                bai_hoc_moi.append(
                    {
                        "ngay": _ngay_hom_nay(),
                        "loai": loai,
                        "noiDung": nd,
                        "mucDoUuTien": uu_tien,
                    }
                )

    ban_ghi_phan_hoi: dict[str, Any] = {
        "ngay": _ngay_hom_nay(),
        "slug": slug_sach,
        "ghiChu": str(ghi_chu or "").strip(),
        "baiHocDaRut": [b["noiDung"] for b in bai_hoc_moi],
    }
    if co_so_lieu and so_lieu_sach is not None:
        ban_ghi_phan_hoi["nguon"] = nguon
        ban_ghi_phan_hoi["soLieuYouTube"] = so_lieu_sach

    bo_nho.setdefault("phan_hoi_kenh", []).append(ban_ghi_phan_hoi)
    luu_bo_nho(bo_nho, duong_dan)
    return bai_hoc_moi


def nhap_so_lieu_youtube(
    slug: str,
    ctr_phan_tram: Any = None,
    giu_chan_30s: Any = None,
    thoi_luong_xem_tb_giay: Any = None,
    moc_tut_view: Any = None,
    bien_the_thumbnail_thang: Any = "",
    binh_luan_noi_bat: Any = None,
    ghi_chu: str = "",
    video_id: str = "",
    luot_xem: Any = None,
    luot_thich: Any = None,
    so_binh_luan: Any = None,
    nguon: str = "cli",
    duong_dan: Path | str | None = None,
    thu_muc_du_lieu: Path | None = None,
    client: GeminiClient | None = None,
    tu_dong_phan_tich: bool = True,
) -> dict[str, Any]:
    """Nap so lieu YouTube co cau truc cho 1 tap vao bo_nho_hoc_hoi.json va phan tich rut bai hoc."""
    raw_so_lieu: dict[str, Any] = {
        "ctr_phan_tram": ctr_phan_tram,
        "giu_chan_30s": giu_chan_30s,
        "thoi_luong_xem_tb_giay": thoi_luong_xem_tb_giay,
        "moc_tut_view": moc_tut_view,
        "bien_the_thumbnail_thang": bien_the_thumbnail_thang,
        "binh_luan_noi_bat": binh_luan_noi_bat,
    }
    if video_id:
        raw_so_lieu["video_id"] = video_id
    if luot_xem is not None:
        raw_so_lieu["luot_xem"] = luot_xem
    if luot_thich is not None:
        raw_so_lieu["luot_thich"] = luot_thich
    if so_binh_luan is not None:
        raw_so_lieu["so_binh_luan"] = so_binh_luan

    so_lieu_sach = chuan_hoa_so_lieu_youtube(raw_so_lieu)
    if not _co_so_lieu_youtube_hop_le(so_lieu_sach) and not ghi_chu.strip():
        raise ValueError("Can cung cap it nhat 1 chi so YouTube hoac ghi chu phan hoi.")

    bai_hoc_moi = hoc_tu_phan_hoi(
        slug=slug,
        ghi_chu=ghi_chu,
        duong_dan=duong_dan,
        client=client,
        so_lieu_youtube=so_lieu_sach,
        thu_muc_du_lieu=thu_muc_du_lieu,
        nguon=nguon,
        tu_dong_phan_tich=tu_dong_phan_tich,
    )
    bo_nho_sau = tai_bo_nho(duong_dan)
    return {
        "slug": _tao_slug_sach(slug),
        "nguon": nguon,
        "soLieuYouTube": so_lieu_sach,
        "baiHocMoi": bai_hoc_moi,
        "tongBaiHoc": len(bo_nho_sau["bai_hoc_rut_ra"]),
    }


def nhap_so_lieu_youtube_tu_file(
    duong_dan_file: Path | str,
    slug_mac_dinh: str = "",
    duong_dan: Path | str | None = None,
    thu_muc_du_lieu: Path | None = None,
    client: GeminiClient | None = None,
    tu_dong_phan_tich: bool = True,
) -> list[dict[str, Any]]:
    """Nap hang loat so lieu YouTube tu file CSV/JSON xuat tu YouTube Studio."""
    danh_sach = doc_so_lieu_youtube_tu_file(duong_dan_file, slug_mac_dinh=slug_mac_dinh)
    if not danh_sach:
        raise ValueError(f"Khong tim thay dong so lieu YouTube hop le nao trong file: {duong_dan_file}")

    ket_qua: list[dict[str, Any]] = []
    for item in danh_sach:
        sl = item["soLieuYouTube"]
        kq = nhap_so_lieu_youtube(
            slug=item["slug"],
            ctr_phan_tram=sl.get("ctr_phan_tram"),
            giu_chan_30s=sl.get("giu_chan_30s"),
            thoi_luong_xem_tb_giay=sl.get("thoi_luong_xem_tb_giay"),
            moc_tut_view=sl.get("moc_tut_view"),
            bien_the_thumbnail_thang=sl.get("bien_the_thumbnail_thang", ""),
            binh_luan_noi_bat=sl.get("binh_luan_noi_bat"),
            ghi_chu=item.get("ghiChu", ""),
            video_id=sl.get("video_id", ""),
            luot_xem=sl.get("luot_xem"),
            luot_thich=sl.get("luot_thich"),
            so_binh_luan=sl.get("so_binh_luan"),
            nguon=item.get("nguon", "json"),
            duong_dan=duong_dan,
            thu_muc_du_lieu=thu_muc_du_lieu,
            client=client,
            tu_dong_phan_tich=tu_dong_phan_tich,
        )
        ket_qua.append(kq)
    return ket_qua


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Quan ly bo nho tu hoc hoi ben vung, hang doi chu de & tu hoc tu so lieu YouTube (du_lieu/bo_nho_hoc_hoi.json)."
    )
    parser.add_argument(
        "--bo-nho",
        default="",
        help="Duong dan tuy chinh toi bo_nho_hoc_hoi.json (mac dinh du_lieu/bo_nho_hoc_hoi.json).",
    )
    parser.add_argument(
        "--thu-muc-du-lieu",
        default="",
        help="Thu muc chua kich ban tung tap (mac dinh du_lieu/).",
    )
    parser.add_argument(
        "--hoc-tu-phan-hoi",
        action="store_true",
        help="Ghi nhan phan hoi kenh (co the kem so lieu YouTube) va nho Gemini rut ra bai hoc moi.",
    )
    parser.add_argument(
        "--nhap-so-lieu-youtube",
        action="store_true",
        help="Nap so lieu YouTube thuc te (qua co CLI hoac --file-so-lieu CSV/JSON) va doi chieu kich ban rut bai hoc.",
    )
    parser.add_argument("--slug", default="", help="Slug cua tap phim can ghi nhan phan hoi/so lieu.")
    parser.add_argument("--ghi-chu", default="", help="Noi dung phan hoi/chi so bo sung.")
    parser.add_argument(
        "--file-so-lieu",
        default="",
        help="Duong dan file CSV hoac JSON xuat tu YouTube Studio.",
    )
    parser.add_argument(
        "--ctr",
        "--ctr-phan-tram",
        dest="ctr_phan_tram",
        default="",
        help="Ti le nhap CTR phan tram (vd: 7.8 hoac 7.8%%).",
    )
    parser.add_argument(
        "--giu-chan-30s",
        default="",
        help="Ti le giu chan nguoi xem o 30 giay dau (vd: 68.5 hoac 68.5%%).",
    )
    parser.add_argument(
        "--thoi-luong-xem-tb",
        "--thoi-luong-xem-tb-giay",
        dest="thoi_luong_xem_tb_giay",
        default="",
        help="Thoi luong xem trung binh (giay hoac MM:SS, vd: 345 hoac 05:45).",
    )
    parser.add_argument(
        "--moc-tut-view",
        default="",
        help="Cac moc tut view cach nhau dau phay (vd: 00:45,04:20).",
    )
    parser.add_argument(
        "--bien-the-thumbnail-thang",
        default="",
        help="Bien the Thumbnail A/B thang (vd: 1, 2, 3 hoac thumbnail_2).",
    )
    parser.add_argument(
        "--binh-luan-noi-bat",
        action="append",
        default=[],
        help="Binh luan noi bat cua khan gia (co the truyen nhieu lan hoac cach nhau boi |).",
    )
    parser.add_argument("--video-id", default="", help="YouTube video_id tuy chon.")
    parser.add_argument("--luot-xem", default="", help="So luot xem tuy chon.")
    parser.add_argument("--luot-thich", default="", help="So luot thich tuy chon.")
    parser.add_argument("--so-binh-luan", default="", help="Tong so binh luan tuy chon.")
    parser.add_argument(
        "--khong-goi-ai",
        action="store_true",
        help="Chi luu so lieu vao phan_hoi_kenh[], bo qua buoc goi Gemini phan tich.",
    )
    parser.add_argument(
        "--xem-ngu-canh",
        action="store_true",
        help="In chuoi ngu canh hoc hoi hien tai.",
    )
    return parser


def _co_co_so_lieu_cli(args: argparse.Namespace) -> bool:
    return any(
        [
            bool(str(args.ctr_phan_tram or "").strip()),
            bool(str(args.giu_chan_30s or "").strip()),
            bool(str(args.thoi_luong_xem_tb_giay or "").strip()),
            bool(str(args.moc_tut_view or "").strip()),
            bool(str(args.bien_the_thumbnail_thang or "").strip()),
            bool(args.binh_luan_noi_bat),
            bool(str(args.luot_xem or "").strip()),
            bool(str(args.luot_thich or "").strip()),
        ]
    )


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    duong_dan = Path(args.bo_nho) if args.bo_nho else DUONG_DAN_BO_NHO_MAC_DINH
    thu_muc_dl = Path(args.thu_muc_du_lieu) if args.thu_muc_du_lieu else None
    goi_ai = not bool(args.khong_goi_ai)

    if args.nhap_so_lieu_youtube or args.file_so_lieu.strip():
        if args.file_so_lieu.strip():
            ds_kq = nhap_so_lieu_youtube_tu_file(
                duong_dan_file=Path(args.file_so_lieu.strip()),
                slug_mac_dinh=args.slug.strip(),
                duong_dan=duong_dan,
                thu_muc_du_lieu=thu_muc_dl,
                tu_dong_phan_tich=goi_ai,
            )
            print(f"[OK] Da nap so lieu YouTube cho {len(ds_kq)} tap tu '{args.file_so_lieu.strip()}':")
            for kq in ds_kq:
                print(
                    f"  * {kq['slug']}: rut {len(kq['baiHocMoi'])} bai hoc moi "
                    f"(tong {kq['tongBaiHoc']}/{TOI_DA_BAI_HOC})"
                )
                for b in kq["baiHocMoi"]:
                    print(f"    - [{b['loai']} | {b['mucDoUuTien']}/5] {b['noiDung']}")
            return 0

        if not args.slug.strip():
            print("[LOI] --nhap-so-lieu-youtube can truyen --slug (hoac --file-so-lieu <file.csv|file.json>).")
            return 2
        if not _co_co_so_lieu_cli(args) and not args.ghi_chu.strip():
            print(
                "[LOI] Can truyen it nhat 1 chi so (--ctr, --giu-chan-30s, --thoi-luong-xem-tb, "
                "--moc-tut-view, --bien-the-thumbnail-thang, --binh-luan-noi-bat) hoac --ghi-chu."
            )
            return 2

        kq = nhap_so_lieu_youtube(
            slug=args.slug.strip(),
            ctr_phan_tram=args.ctr_phan_tram or None,
            giu_chan_30s=args.giu_chan_30s or None,
            thoi_luong_xem_tb_giay=args.thoi_luong_xem_tb_giay or None,
            moc_tut_view=args.moc_tut_view or None,
            bien_the_thumbnail_thang=args.bien_the_thumbnail_thang,
            binh_luan_noi_bat=args.binh_luan_noi_bat or None,
            ghi_chu=args.ghi_chu.strip(),
            video_id=args.video_id.strip(),
            luot_xem=args.luot_xem or None,
            luot_thich=args.luot_thich or None,
            so_binh_luan=args.so_binh_luan or None,
            nguon="cli",
            duong_dan=duong_dan,
            thu_muc_du_lieu=thu_muc_dl,
            tu_dong_phan_tich=goi_ai,
        )
        print(
            f"[OK] Da nap so lieu YouTube cho '{kq['slug']}' va rut ra {len(kq['baiHocMoi'])} bai hoc moi "
            f"(tong {kq['tongBaiHoc']}/{TOI_DA_BAI_HOC}):"
        )
        for b in kq["baiHocMoi"]:
            print(f"  - [{b['loai']} | {b['mucDoUuTien']}/5] {b['noiDung']}")
        return 0

    if args.hoc_tu_phan_hoi:
        co_sl = _co_co_so_lieu_cli(args)
        if not args.slug.strip() or (not args.ghi_chu.strip() and not co_sl):
            print("[LOI] --hoc-tu-phan-hoi can truyen --slug va --ghi-chu (hoac cac chi so YouTube).")
            return 2
        so_lieu_dict = (
            {
                "ctr_phan_tram": args.ctr_phan_tram or None,
                "giu_chan_30s": args.giu_chan_30s or None,
                "thoi_luong_xem_tb_giay": args.thoi_luong_xem_tb_giay or None,
                "moc_tut_view": args.moc_tut_view or None,
                "bien_the_thumbnail_thang": args.bien_the_thumbnail_thang,
                "binh_luan_noi_bat": args.binh_luan_noi_bat or None,
                "video_id": args.video_id.strip() or None,
                "luot_xem": args.luot_xem or None,
                "luot_thich": args.luot_thich or None,
                "so_binh_luan": args.so_binh_luan or None,
            }
            if co_sl
            else None
        )
        moi = hoc_tu_phan_hoi(
            slug=args.slug.strip(),
            ghi_chu=args.ghi_chu.strip(),
            duong_dan=duong_dan,
            so_lieu_youtube=so_lieu_dict,
            thu_muc_du_lieu=thu_muc_dl,
            nguon="cli",
            tu_dong_phan_tich=goi_ai,
        )
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
