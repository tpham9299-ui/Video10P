# -*- coding: utf-8 -*-
"""Module dong bo so lieu YouTube tuy chon bang Python stdlib (khong can SDK ngoai)."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.bo_nho_hoc_hoi import (
    DUONG_DAN_BO_NHO_MAC_DINH,
    nhap_so_lieu_youtube,
)
from scripts.pipeline.gemini_client import GeminiClient, tai_env

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"


def lay_cau_hinh_youtube(
    duong_dan_env: Path | str | None = None,
    env_override: dict[str, str] | None = None,
) -> dict[str, str]:
    """Doc YOUTUBE_API_KEY va YOUTUBE_OAUTH_TOKEN tu .env / bien moi truong (khong ghi cung)."""
    tu_file = tai_env(duong_dan_env)
    nguon: dict[str, str] = {}
    nguon.update(tu_file)
    for k in ("YOUTUBE_API_KEY", "YOUTUBE_OAUTH_TOKEN", "YOUTUBE_ACCESS_TOKEN"):
        if os.environ.get(k):
            nguon[k] = os.environ[k]
    if env_override:
        nguon.update(env_override)

    api_key = str(nguon.get("YOUTUBE_API_KEY") or "").strip()
    oauth_token = str(
        nguon.get("YOUTUBE_OAUTH_TOKEN") or nguon.get("YOUTUBE_ACCESS_TOKEN") or ""
    ).strip()
    return {
        "api_key": api_key,
        "oauth_token": oauth_token,
    }


def tao_huong_dan_nhap_tay(slug: str = "<slug>") -> str:
    """Tra ve huong dan chi tiet cach nap file CSV/JSON xuat tay tu YouTube Studio khi chua co API key."""
    ten_slug = slug.strip() or "<slug>"
    return (
        "[HUONG DAN] Chua cau hinh YOUTUBE_API_KEY hoac YOUTUBE_OAUTH_TOKEN trong .env / bien moi truong.\n"
        "He thong VAN hoat dong binh thuong ma khong can API YouTube! Ban co 2 cach:\n\n"
        "Cach 1 (Khuyen dung — day du CTR, giu chan 30s, moc tut view, Thumbnail A/B):\n"
        "  1. Mo YouTube Studio -> Analytics -> Xuat file CSV (hoac tao file JSON theo mau ben duoi).\n"
        "  2. Chay lenh nap truc tiep vao bo nho tu hoc:\n"
        f"     python -X utf8 scripts/pipeline/bo_nho_hoc_hoi.py --nhap-so-lieu-youtube --slug {ten_slug} "
        "--file-so-lieu du_lieu/so_lieu_youtube.csv\n"
        "  Hoac truyen nhanh qua tham so CLI:\n"
        f"     python -X utf8 scripts/pipeline/bo_nho_hoc_hoi.py --nhap-so-lieu-youtube --slug {ten_slug} "
        '--ctr 7.8 --giu-chan-30s 68.5 --thoi-luong-xem-tb 05:45 --moc-tut-view "00:45,04:20" '
        '--bien-the-thumbnail-thang 2 --binh-luan-noi-bat "Giải thích dễ hiểu quá!"\n\n'
        "Cach 2 (Keo tu dong luot xem, luot thich, binh luan noi bat qua YouTube Data API v3):\n"
        "  Them YOUTUBE_API_KEY=<key_cua_ban> (hoac YOUTUBE_OAUTH_TOKEN=<token>) vao file .env roi chay lai."
    )


def _http_get_json_mac_dinh(
    url: str,
    headers: dict[str, str] | None = None,
    timeout: int = 20,
) -> tuple[int, str]:
    req = urllib.request.Request(url, headers=headers or {}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            body = resp.read().decode("utf-8", errors="replace")
            return int(status), body
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8", errors="replace") if err.fp else str(err)
        return int(err.code), body
    except urllib.error.URLError as err:
        return 0, f"Loi ket noi mang: {err}"


def _xay_dung_headers_va_params(
    params: dict[str, str],
    api_key: str = "",
    oauth_token: str = "",
) -> tuple[dict[str, str], dict[str, str]]:
    p = dict(params)
    h = {"Accept": "application/json", "User-Agent": "Video10P-YouTubeSync/1.0"}
    if api_key:
        p["key"] = api_key
    if oauth_token:
        h["Authorization"] = f"Bearer {oauth_token}"
    return p, h


def _ep_int_an_toan(gia_tri: Any) -> int | None:
    if gia_tri is None:
        return None
    try:
        return max(0, int(str(gia_tri).strip()))
    except (ValueError, TypeError):
        return None


def keo_thong_ke_video_youtube(
    video_id: str,
    api_key: str = "",
    oauth_token: str = "",
    http_get_caller: Callable[[str, dict[str, str], int], tuple[int, str]] | None = None,
    toi_da_binh_luan: int = 5,
    timeout: int = 20,
) -> dict[str, Any]:
    """
    Keo thong ke co ban (luot xem, luot thich, so binh luan) va binh luan noi bat
    tu YouTube Data API v3 bang urllib thuan stdlib.
    """
    vid = str(video_id or "").strip()
    if not vid:
        raise ValueError("Thieu video_id YouTube hop le.")
    if not api_key and not oauth_token:
        raise RuntimeError("Thieu YOUTUBE_API_KEY hoac YOUTUBE_OAUTH_TOKEN.")

    caller = http_get_caller or _http_get_json_mac_dinh

    # 1. Lay thong ke co ban cua video
    params_v, headers_v = _xay_dung_headers_va_params(
        {"part": "snippet,statistics", "id": vid},
        api_key=api_key,
        oauth_token=oauth_token,
    )
    url_video = f"{YOUTUBE_API_BASE}/videos?{urllib.parse.urlencode(params_v)}"
    status_v, body_v = caller(url_video, headers_v, timeout)
    if status_v != 200:
        raise RuntimeError(f"YouTube API /videos tra ve ma {status_v}: {body_v[:280]}")

    data_v = json.loads(body_v)
    items = data_v.get("items") if isinstance(data_v, dict) else []
    if not items or not isinstance(items[0], dict):
        raise ValueError(f"Khong tim thay video YouTube voi id='{vid}'.")

    muc = items[0]
    snippet = muc.get("snippet") if isinstance(muc.get("snippet"), dict) else {}
    stats = muc.get("statistics") if isinstance(muc.get("statistics"), dict) else {}

    ket_qua: dict[str, Any] = {
        "video_id": vid,
        "tieu_de": str(snippet.get("title") or "").strip(),
        "ngay_dang": str(snippet.get("publishedAt") or "").strip(),
        "luot_xem": _ep_int_an_toan(stats.get("viewCount")),
        "luot_thich": _ep_int_an_toan(stats.get("likeCount")),
        "so_binh_luan": _ep_int_an_toan(stats.get("commentCount")),
        "binh_luan_noi_bat": [],
    }

    # 2. Lay binh luan noi bat (bo qua an toan neu video tat binh luan / 403)
    so_bl = max(0, min(20, int(toi_da_binh_luan)))
    if so_bl > 0:
        params_c, headers_c = _xay_dung_headers_va_params(
            {
                "part": "snippet",
                "videoId": vid,
                "order": "relevance",
                "maxResults": str(so_bl),
                "textFormat": "plainText",
            },
            api_key=api_key,
            oauth_token=oauth_token,
        )
        url_comments = f"{YOUTUBE_API_BASE}/commentThreads?{urllib.parse.urlencode(params_c)}"
        status_c, body_c = caller(url_comments, headers_c, timeout)
        if status_c == 200:
            try:
                data_c = json.loads(body_c)
                bl_list: list[str] = []
                for thread in (data_c.get("items") or []):
                    if not isinstance(thread, dict):
                        continue
                    top = (thread.get("snippet") or {}).get("topLevelComment") or {}
                    top_sn = top.get("snippet") or {}
                    text = str(top_sn.get("textDisplay") or top_sn.get("textOriginal") or "").strip()
                    if text:
                        bl_list.append(" ".join(text.split())[:280])
                ket_qua["binh_luan_noi_bat"] = bl_list
            except json.JSONDecodeError:
                pass

    return ket_qua


def dong_bo_video_youtube(
    slug: str,
    video_id: str,
    ctr_phan_tram: Any = None,
    giu_chan_30s: Any = None,
    thoi_luong_xem_tb_giay: Any = None,
    moc_tut_view: Any = None,
    bien_the_thumbnail_thang: str = "",
    ghi_chu: str = "",
    toi_da_binh_luan: int = 5,
    duong_dan_bo_nho: Path | str | None = None,
    thu_muc_du_lieu: Path | None = None,
    duong_dan_env: Path | str | None = None,
    env_override: dict[str, str] | None = None,
    http_get_caller: Callable[[str, dict[str, str], int], tuple[int, str]] | None = None,
    gemini_client: GeminiClient | None = None,
    tu_dong_phan_tich: bool = True,
) -> dict[str, Any]:
    """
    Dong bo thong ke 1 video YouTube theo video_id gan voi <slug> va day thang vao bo_nho_hoc_hoi.py.
    Neu chua cau hinh bien moi truong YOUTUBE_API_KEY / YOUTUBE_OAUTH_TOKEN -> tra ve huong dan, KHONG crash.
    """
    cfg = lay_cau_hinh_youtube(duong_dan_env=duong_dan_env, env_override=env_override)
    if not cfg["api_key"] and not cfg["oauth_token"]:
        huong_dan = tao_huong_dan_nhap_tay(slug=slug)
        return {
            "trangThai": "chua_cau_hinh",
            "slug": slug,
            "video_id": video_id,
            "huongDan": huong_dan,
        }

    thong_ke = keo_thong_ke_video_youtube(
        video_id=video_id,
        api_key=cfg["api_key"],
        oauth_token=cfg["oauth_token"],
        http_get_caller=http_get_caller,
        toi_da_binh_luan=toi_da_binh_luan,
    )

    ghi_chu_day_du = ghi_chu.strip()
    if not ghi_chu_day_du and thong_ke.get("tieu_de"):
        ghi_chu_day_du = f"Dong bo tu dong tu YouTube API cho video '{thong_ke['tieu_de']}'"

    ket_qua_nap = nhap_so_lieu_youtube(
        slug=slug,
        ctr_phan_tram=ctr_phan_tram,
        giu_chan_30s=giu_chan_30s,
        thoi_luong_xem_tb_giay=thoi_luong_xem_tb_giay,
        moc_tut_view=moc_tut_view,
        bien_the_thumbnail_thang=bien_the_thumbnail_thang,
        binh_luan_noi_bat=thong_ke.get("binh_luan_noi_bat"),
        ghi_chu=ghi_chu_day_du,
        video_id=thong_ke["video_id"],
        luot_xem=thong_ke.get("luot_xem"),
        luot_thich=thong_ke.get("luot_thich"),
        so_binh_luan=thong_ke.get("so_binh_luan"),
        nguon="youtube_api",
        duong_dan=duong_dan_bo_nho or DUONG_DAN_BO_NHO_MAC_DINH,
        thu_muc_du_lieu=thu_muc_du_lieu,
        client=gemini_client,
        tu_dong_phan_tich=tu_dong_phan_tich,
    )

    return {
        "trangThai": "thanh_cong",
        "slug": ket_qua_nap["slug"],
        "video_id": thong_ke["video_id"],
        "thongKeYouTube": thong_ke,
        "ketQuaNap": ket_qua_nap,
    }


def dong_bo_hang_loat_tu_file(
    file_anh_xa: Path | str,
    duong_dan_bo_nho: Path | str | None = None,
    thu_muc_du_lieu: Path | None = None,
    duong_dan_env: Path | str | None = None,
    env_override: dict[str, str] | None = None,
    http_get_caller: Callable[[str, dict[str, str], int], tuple[int, str]] | None = None,
    gemini_client: GeminiClient | None = None,
    tu_dong_phan_tich: bool = True,
) -> list[dict[str, Any]]:
    """Dong bo nhieu tap tu file JSON anh xa [{"slug": "...", "video_id": "..."}]."""
    path = Path(file_anh_xa)
    if not path.exists():
        raise FileNotFoundError(f"Khong tim thay file anh xa YouTube: {path}")

    raw = json.loads(path.read_text(encoding="utf-8-sig"))
    ds = raw if isinstance(raw, list) else (raw.get("videos") if isinstance(raw, dict) else [])
    if not isinstance(ds, list):
        raise ValueError("File anh xa phai la mang JSON cac doi tuong {slug, video_id}.")

    cfg = lay_cau_hinh_youtube(duong_dan_env=duong_dan_env, env_override=env_override)
    if not cfg["api_key"] and not cfg["oauth_token"]:
        return [{"trangThai": "chua_cau_hinh", "huongDan": tao_huong_dan_nhap_tay()}]

    ket_qua: list[dict[str, Any]] = []
    for item in ds:
        if not isinstance(item, dict):
            continue
        slug = str(item.get("slug") or "").strip()
        vid = str(item.get("video_id") or item.get("videoId") or "").strip()
        if not slug or not vid:
            continue
        kq = dong_bo_video_youtube(
            slug=slug,
            video_id=vid,
            ctr_phan_tram=item.get("ctr_phan_tram"),
            giu_chan_30s=item.get("giu_chan_30s"),
            thoi_luong_xem_tb_giay=item.get("thoi_luong_xem_tb_giay"),
            moc_tut_view=item.get("moc_tut_view"),
            bien_the_thumbnail_thang=str(item.get("bien_the_thumbnail_thang") or ""),
            ghi_chu=str(item.get("ghi_chu") or ""),
            duong_dan_bo_nho=duong_dan_bo_nho,
            thu_muc_du_lieu=thu_muc_du_lieu,
            duong_dan_env=duong_dan_env,
            env_override=env_override,
            http_get_caller=http_get_caller,
            gemini_client=gemini_client,
            tu_dong_phan_tich=tu_dong_phan_tich,
        )
        ket_qua.append(kq)
    return ket_qua


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Dong bo so lieu YouTube Data API v3 (tuy chon, stdlib) va day vao bo_nho_hoc_hoi.py."
    )
    parser.add_argument("--slug", default="", help="Slug cua tap phim trong du_lieu/<slug>/.")
    parser.add_argument("--video-id", default="", help="ID video tren YouTube (vd: dQw4w9WgXcQ).")
    parser.add_argument(
        "--file-anh-xa",
        default="",
        help='File JSON danh sach anh xa nhieu tap: [{"slug": "...", "video_id": "..."}].',
    )
    parser.add_argument("--ctr", default="", help="Bo sung CTR phan tram tu YouTube Studio (tuy chon).")
    parser.add_argument("--giu-chan-30s", default="", help="Bo sung giu chan 30s phan tram (tuy chon).")
    parser.add_argument(
        "--thoi-luong-xem-tb",
        default="",
        help="Bo sung thoi luong xem trung binh (giay hoac MM:SS, tuy chon).",
    )
    parser.add_argument("--moc-tut-view", default="", help="Bo sung moc tut view (vd: 00:45,04:20).")
    parser.add_argument(
        "--bien-the-thumbnail-thang",
        default="",
        help="Bo sung bien the Thumbnail A/B thang (vd: 1, 2, 3).",
    )
    parser.add_argument("--ghi-chu", default="", help="Ghi chu bo sung cho tap.")
    parser.add_argument("--toi-da-binh-luan", type=int, default=5, help="So binh luan noi bat keo ve (mac dinh 5).")
    parser.add_argument(
        "--khong-goi-ai",
        action="store_true",
        help="Chi luu so lieu vao phan_hoi_kenh[], bo qua buoc goi Gemini phan tich.",
    )
    parser.add_argument("--bo-nho", default="", help="Duong dan tuy chinh toi bo_nho_hoc_hoi.json.")
    parser.add_argument("--thu-muc-du-lieu", default="", help="Thu muc du_lieu tuy chinh.")
    parser.add_argument("--env", default="", help="Duong dan file .env tuy chinh.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    duong_dan_bn = Path(args.bo_nho) if args.bo_nho else DUONG_DAN_BO_NHO_MAC_DINH
    thu_muc_dl = Path(args.thu_muc_du_lieu) if args.thu_muc_du_lieu else None
    duong_dan_env = Path(args.env) if args.env else None
    goi_ai = not bool(args.khong_goi_ai)

    cfg = lay_cau_hinh_youtube(duong_dan_env=duong_dan_env)
    if not cfg["api_key"] and not cfg["oauth_token"]:
        print(tao_huong_dan_nhap_tay(slug=args.slug.strip() or "<slug>"))
        return 0

    if args.file_anh_xa.strip():
        ds = dong_bo_hang_loat_tu_file(
            file_anh_xa=Path(args.file_anh_xa.strip()),
            duong_dan_bo_nho=duong_dan_bn,
            thu_muc_du_lieu=thu_muc_dl,
            duong_dan_env=duong_dan_env,
            tu_dong_phan_tich=goi_ai,
        )
        print(f"[OK] Da dong bo {len(ds)} video YouTube vao bo_nho_hoc_hoi.json.")
        return 0

    if not args.slug.strip() or not args.video_id.strip():
        print("[LOI] Can truyen du --slug va --video-id (hoac --file-anh-xa <file.json>).")
        return 2

    kq = dong_bo_video_youtube(
        slug=args.slug.strip(),
        video_id=args.video_id.strip(),
        ctr_phan_tram=args.ctr or None,
        giu_chan_30s=args.giu_chan_30s or None,
        thoi_luong_xem_tb_giay=args.thoi_luong_xem_tb or None,
        moc_tut_view=args.moc_tut_view or None,
        bien_the_thumbnail_thang=args.bien_the_thumbnail_thang,
        ghi_chu=args.ghi_chu,
        toi_da_binh_luan=args.toi_da_binh_luan,
        duong_dan_bo_nho=duong_dan_bn,
        thu_muc_du_lieu=thu_muc_dl,
        duong_dan_env=duong_dan_env,
        tu_dong_phan_tich=goi_ai,
    )
    if kq.get("trangThai") == "chua_cau_hinh":
        print(kq["huongDan"])
        return 0

    tk = kq["thongKeYouTube"]
    nap = kq["ketQuaNap"]
    print(
        f"[OK] Da dong bo YouTube video '{kq['video_id']}' cho tap '{kq['slug']}': "
        f"xem={tk.get('luot_xem')}, thich={tk.get('luot_thich')}, "
        f"binh_luan={len(tk.get('binh_luan_noi_bat') or [])} | rut {len(nap['baiHocMoi'])} bai hoc moi."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
