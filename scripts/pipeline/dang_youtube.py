# -*- coding: utf-8 -*-
"""Tu dong dang video len YouTube Data API v3 (Resumable Upload 8MB, hen gio +07:00, thumbnail, phu de .srt) bang Python stdlib."""

from __future__ import annotations

import argparse
import datetime
import json
import mimetypes
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Callable

GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.bo_nho_hoc_hoi import (
    DUONG_DAN_BO_NHO_MAC_DINH,
    luu_bo_nho,
    tai_bo_nho,
)
from scripts.pipeline.gemini_client import tai_env

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
YOUTUBE_VIDEO_UPLOAD_URL = (
    "https://www.googleapis.com/upload/youtube/v3/videos"
    "?uploadType=resumable&part=snippet,status"
)
YOUTUBE_THUMBNAIL_UPLOAD_URL_TEMPLATE = (
    "https://www.googleapis.com/upload/youtube/v3/thumbnails/set"
    "?videoId={video_id}&uploadType=media"
)
YOUTUBE_CAPTION_UPLOAD_URL = (
    "https://www.googleapis.com/upload/youtube/v3/captions"
    "?part=snippet&uploadType=multipart"
)

KICH_THUOC_CHUNK_MAC_DINH = 8 * 1024 * 1024  # 8MB (boi so cua 256KB theo chuan Google Resumable Upload)
MUI_GIO_VN = datetime.timezone(datetime.timedelta(hours=7))
GIO_CONG_KHAI_MAC_DINH = "19:30"
CATEGORY_ID_GIAO_DUC = "27"
MA_LOI_THU_LAI = {429, 500, 502, 503, 504}
THE_TAG_MAC_DINH = (
    "lịch sử toán học",
    "hoạt hình toán học",
    "kể chuyện toán học",
    "toán học thú vị",
    "giáo dục",
)

# Kieu ham HTTP chuan hoa cho ca goi that lan mock trong unit test:
# (method, url, headers, data, timeout) -> (status_code, response_headers_dict, response_body_bytes)
HttpCaller = Callable[
    [str, str, dict[str, str], bytes | None, int],
    tuple[int, dict[str, str], bytes],
]


class LoiDangYouTube(RuntimeError):
    """Loi trong qua trinh xac thuc hoac tai video len YouTube."""


def lay_cau_hinh_oauth_youtube(
    duong_dan_env: Path | str | None = None,
    env_override: dict[str, str] | None = None,
) -> dict[str, str]:
    """Doc 3 bien YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REFRESH_TOKEN tu .env / env."""
    tu_file = tai_env(duong_dan_env)
    nguon: dict[str, str] = {}
    nguon.update(tu_file)
    for k in ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"):
        if os.environ.get(k):
            nguon[k] = os.environ[k]
    if env_override is not None:
        nguon.update(env_override)

    return {
        "client_id": str(nguon.get("YOUTUBE_CLIENT_ID") or "").strip(),
        "client_secret": str(nguon.get("YOUTUBE_CLIENT_SECRET") or "").strip(),
        "refresh_token": str(nguon.get("YOUTUBE_REFRESH_TOKEN") or "").strip(),
    }


def danh_sach_bien_thieu(cau_hinh: dict[str, str]) -> list[str]:
    """Tra ve ten cac bien moi truong OAuth YouTube con thieu."""
    anh_xa = (
        ("client_id", "YOUTUBE_CLIENT_ID"),
        ("client_secret", "YOUTUBE_CLIENT_SECRET"),
        ("refresh_token", "YOUTUBE_REFRESH_TOKEN"),
    )
    return [ten_bien for khoa, ten_bien in anh_xa if not str(cau_hinh.get(khoa) or "").strip()]


def tao_huong_dan_cau_hinh_youtube(thieu: list[str] | None = None) -> str:
    """In huong dan cau hinh 3 secret YouTube OAuth ro rang khi thieu bien moi truong."""
    ds_thieu = thieu or ["YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"]
    return (
        f"[BO QUA DANG YOUTUBE] Thieu bien moi truong / GitHub Secrets: {', '.join(ds_thieu)}.\n"
        "Workflow van thanh cong binh thuong va da luu video vao GitHub Artifacts!\n\n"
        "De bat tinh nang tu dong dang video + hen gio len YouTube (chi lam 1 lan duy nhat):\n"
        "  1. Vao Google Cloud Console -> Bat 'YouTube Data API v3' -> Tao OAuth Client ID (loai Desktop app).\n"
        "  2. Chay tien ich lay Refresh Token trong 30 giay tren may ca nhan:\n"
        "       python -X utf8 scripts/pipeline/lay_refresh_token_youtube.py\n"
        "  3. Them 3 Secrets vao GitHub (Settings -> Secrets and variables -> Actions) hoac file .env:\n"
        "       - YOUTUBE_CLIENT_ID\n"
        "       - YOUTUBE_CLIENT_SECRET\n"
        "       - YOUTUBE_REFRESH_TOKEN\n"
    )


def _http_call_mac_dinh(
    method: str,
    url: str,
    headers: dict[str, str],
    data: bytes | None = None,
    timeout: int = 120,
) -> tuple[int, dict[str, str], bytes]:
    """Thuc hien HTTP request bang urllib thuan stdlib, bat ca HTTP 308 (Resume Incomplete)."""
    req = urllib.request.Request(url, data=data, headers=dict(headers), method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = int(getattr(resp, "status", 200))
            resp_headers = {str(k).lower(): str(v) for k, v in resp.headers.items()}
            body = resp.read()
            return status, resp_headers, body
    except urllib.error.HTTPError as err:
        resp_headers = {str(k).lower(): str(v) for k, v in (err.headers.items() if err.headers else [])}
        body = err.read() if err.fp else str(err).encode("utf-8", errors="replace")
        return int(err.code), resp_headers, body
    except urllib.error.URLError as err:
        return 0, {}, f"Loi ket noi mang: {err}".encode("utf-8", errors="replace")


def _lay_header_khong_phan_biet_hoa_thuong(headers: dict[str, str], ten: str) -> str:
    muc_tieu = ten.lower()
    for k, v in (headers or {}).items():
        if str(k).lower() == muc_tieu:
            return str(v).strip()
    return ""


def _lam_sach_chuoi_youtube(van_ban: str) -> str:
    """Loai bo ky tu < va > (YouTube cam trong tieu de/mo ta/tag) va chuan hoa khoang trang."""
    s = str(van_ban or "").replace("<", "").replace(">", "")
    return re.sub(r"[ \t]+", " ", s).strip()


def _cat_tieu_de_youtube(tieu_de: str, toi_da: int = 100) -> str:
    """Cat tieu de YouTube an toan <= 100 ky tu, uu tien cat tron tu."""
    sach = _lam_sach_chuoi_youtube(tieu_de.replace("\n", " ").replace("\r", " "))
    if not sach:
        return "Câu Chuyện Lịch Sử Toán Học"
    if len(sach) <= toi_da:
        return sach
    cat = sach[: toi_da - 1].rsplit(" ", 1)[0].strip()
    if not cat:
        cat = sach[: toi_da - 1].strip()
    return cat + "…"


def tinh_thoi_diem_cong_khai_vn(
    gio_cong_khai_vn: str = GIO_CONG_KHAI_MAC_DINH,
    cach_ngay: int = 0,
    bay_gio: datetime.datetime | None = None,
    tu_dong_day_ngay_neu_qua_gio: bool = True,
    dem_toi_thieu_phut: int = 15,
) -> str:
    """
    Tinh chuoi thoi gian ISO-8601 chuan mui gio Viet Nam (+07:00) cho `status.publishAt`.
    - `gio_cong_khai_vn`: "HH:MM" hoac "HH:MM:SS" (mac dinh "19:30").
    - `cach_ngay`: so ngay cong them so voi hom nay theo gio VN (0 = hom nay, 1 = ngay mai).
    - Neu `cach_ngay == 0` nhung moc gio hom nay da qua (hoac con < 15 phut), tu dong day sang
      ngay hom sau de tranh YouTube tu choi `publishAt` trong qua khu.
    """
    mau = re.fullmatch(r"\s*(\d{1,2}):(\d{2})(?::(\d{2}))?\s*", str(gio_cong_khai_vn or ""))
    if not mau:
        raise ValueError(
            f"Dinh dang --gio-cong-khai-vn khong hop le: '{gio_cong_khai_vn}'. Can dang HH:MM (vd: 19:30)."
        )
    gio = int(mau.group(1))
    phut = int(mau.group(2))
    giay = int(mau.group(3) or 0)
    if not (0 <= gio <= 23 and 0 <= phut <= 59 and 0 <= giay <= 59):
        raise ValueError(f"Gia tri gio/phut/giay ngoai pham vi hop le: '{gio_cong_khai_vn}'.")

    so_ngay = max(0, int(cach_ngay))
    if bay_gio is None:
        hien_tai_vn = datetime.datetime.now(tz=MUI_GIO_VN)
    elif bay_gio.tzinfo is None:
        hien_tai_vn = bay_gio.replace(tzinfo=MUI_GIO_VN)
    else:
        hien_tai_vn = bay_gio.astimezone(MUI_GIO_VN)

    ngay_muc_tieu = hien_tai_vn.date() + datetime.timedelta(days=so_ngay)
    muc_tieu = datetime.datetime(
        ngay_muc_tieu.year,
        ngay_muc_tieu.month,
        ngay_muc_tieu.day,
        gio,
        phut,
        giay,
        tzinfo=MUI_GIO_VN,
    )

    nguong_som_nhat = hien_tai_vn + datetime.timedelta(minutes=max(0, int(dem_toi_thieu_phut)))
    if tu_dong_day_ngay_neu_qua_gio and muc_tieu < nguong_som_nhat:
        muc_tieu = muc_tieu + datetime.timedelta(days=1)

    return muc_tieu.isoformat(timespec="seconds")


def doc_tieu_de_va_mo_ta(
    file_chapters_va_mo_ta: Path | str | None,
    du_lieu_render: dict[str, Any] | None = None,
    slug: str = "",
) -> tuple[str, str]:
    """
    Trich xuat tieu de chuan (<= 100 ky tu) va mo ta + YouTube chapters (<= 5000 ky tu)
    tu file `chapters_va_mo_ta.txt` (do render_dai.py tao ra), fallback du_lieu_render.json.
    """
    tieu_de_fallback = str((du_lieu_render or {}).get("tieuDe") or slug or "Câu Chuyện Lịch Sử Toán Học").strip()
    chu_de_fallback = str((du_lieu_render or {}).get("chuDe") or "").strip()

    if file_chapters_va_mo_ta is None or not Path(file_chapters_va_mo_ta).exists():
        mo_ta_fb = chu_de_fallback or f"Hoạt hình kể chuyện lịch sử Toán học: {tieu_de_fallback}."
        return _cat_tieu_de_youtube(tieu_de_fallback), _lam_sach_chuoi_youtube(mo_ta_fb)[:5000]

    noi_dung = Path(file_chapters_va_mo_ta).read_text(encoding="utf-8-sig")
    cac_muc: dict[str, list[str]] = {}
    muc_hien_tai = "_goc"
    cac_muc[muc_hien_tai] = []

    for dong in noi_dung.splitlines():
        khop = re.fullmatch(r"\s*===\s*(.+?)\s*===\s*", dong)
        if khop:
            muc_hien_tai = khop.group(1).strip().upper()
            cac_muc.setdefault(muc_hien_tai, [])
        else:
            cac_muc.setdefault(muc_hien_tai, []).append(dong.rstrip())

    # 1. Lay tieu de uu tien dong "1. ..." trong phan TIÊU ĐỀ GỢI Ý CHO YOUTUBE
    tieu_de_chon = ""
    for ten_muc, ds_dong in cac_muc.items():
        if "TIÊU ĐỀ" in ten_muc or "TIEU DE" in ten_muc:
            for dong in ds_dong:
                s = dong.strip()
                if not s:
                    continue
                s = re.sub(r"^\d+[\.\)]\s*", "", s).strip()
                if s:
                    tieu_de_chon = s
                    break
            if tieu_de_chon:
                break

    if not tieu_de_chon:
        tieu_de_chon = tieu_de_fallback

    # 2. Ghep mo ta, moc thoi gian (chapters) va nguon tham khao sach se
    phan_mo_ta: list[str] = []
    co_cau_truc = any(k != "_goc" for k in cac_muc)

    if co_cau_truc:
        for ten_muc, ds_dong in cac_muc.items():
            if ten_muc == "_goc" or "TIÊU ĐỀ" in ten_muc or "TIEU DE" in ten_muc:
                continue
            khoi = "\n".join(ds_dong).strip()
            if not khoi:
                continue
            if "MỐC THỜI GIAN" in ten_muc or "CHAPTER" in ten_muc:
                phan_mo_ta.append("Mốc thời gian:\n" + khoi)
            elif "NGUỒN THAM KHẢO" in ten_muc or "NGUON THAM KHAO" in ten_muc:
                phan_mo_ta.append("Nguồn tham khảo:\n" + khoi)
            else:
                phan_mo_ta.append(khoi)
    else:
        khoi_tho = noi_dung.strip()
        if khoi_tho:
            phan_mo_ta.append(khoi_tho)

    mo_ta_day_du = "\n\n".join(phan_mo_ta).strip()
    if not mo_ta_day_du:
        mo_ta_day_du = chu_de_fallback or f"Hoạt hình kể chuyện lịch sử Toán học: {tieu_de_chon}."

    mo_ta_day_du = mo_ta_day_du.replace("<", "").replace(">", "")
    if len(mo_ta_day_du) > 5000:
        mo_ta_day_du = mo_ta_day_du[:4997].rstrip() + "..."

    return _cat_tieu_de_youtube(tieu_de_chon), mo_ta_day_du


def trich_xuat_the_tag(
    du_lieu_render: dict[str, Any] | None = None,
    mo_ta: str = "",
    gioi_han_tong_ky_tu: int = 480,
) -> list[str]:
    """
    Trich xuat danh sach the tag YouTube tu `du_lieu_render.json` (theTag/tags/tuKhoa,
    tieuDe, danhSachNhanVat, tenChuong) ket hop hashtag trong mo ta va tag mac dinh cua kenh.
    Dam bao khong trung lap va tong do dai an toan <= 480 ky tu theo gioi han YouTube (500).
    """
    ung_vien: list[str] = []
    dl = du_lieu_render if isinstance(du_lieu_render, dict) else {}

    # 1. Tag khai bao tuong minh trong du_lieu_render.json (neu co)
    for khoa in ("theTag", "tags", "tuKhoa", "keywords"):
        val = dl.get(khoa)
        if isinstance(val, list):
            for muc in val:
                s = str(muc or "").strip()
                if s:
                    ung_vien.append(s)
        elif isinstance(val, str) and val.strip():
            ung_vien.extend(p.strip() for p in val.split(",") if p.strip())

    # 2. Ten nhan vat lich su trong tap
    for nv in dl.get("danhSachNhanVat") or []:
        if isinstance(nv, dict):
            ten = str(nv.get("ten") or "").strip()
            if ten:
                ung_vien.append(ten)

    # 3. Tieu de tap (rut gon ve ve chinh truoc dau : hoac |)
    tieu_de = str(dl.get("tieuDe") or "").strip()
    if tieu_de:
        ve_dau = re.split(r"[:|—–]", tieu_de, maxsplit=1)[0].strip()
        if 2 <= len(ve_dau) <= 60:
            ung_vien.append(ve_dau)

    # 4. Hashtag trong mo ta
    for ht in re.findall(r"#([A-Za-z0-9_\u00C0-\u1EF9]{2,40})", mo_ta or ""):
        ung_vien.append(ht)

    # 5. Tag nen tang cua kenh
    ung_vien.extend(THE_TAG_MAC_DINH)

    ket_qua: list[str] = []
    da_co: set[str] = set()
    tong_ky_tu = 0

    for raw in ung_vien:
        tag = _lam_sach_chuoi_youtube(str(raw).lstrip("#").strip())
        if not tag or len(tag) < 2:
            continue
        if len(tag) > 100:
            tag = tag[:100].strip()
        khoa_so_sanh = tag.lower()
        if khoa_so_sanh in da_co:
            continue
        # YouTube tinh ca dau phay/dau ngoac kep cho tag co khoang trang
        chi_phi = len(tag) + (3 if " " in tag else 1)
        if tong_ky_tu + chi_phi > gioi_han_tong_ky_tu:
            continue
        da_co.add(khoa_so_sanh)
        ket_qua.append(tag)
        tong_ky_tu += chi_phi

    return ket_qua


def doi_refresh_token_lay_access_token(
    client_id: str,
    client_secret: str,
    refresh_token: str,
    http_caller: HttpCaller | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    """Doi YOUTUBE_REFRESH_TOKEN lay access_token moi tu https://oauth2.googleapis.com/token."""
    cid = str(client_id or "").strip()
    csec = str(client_secret or "").strip()
    rtok = str(refresh_token or "").strip()
    if not cid or not csec or not rtok:
        raise LoiDangYouTube("Thieu YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET hoac YOUTUBE_REFRESH_TOKEN.")

    caller = http_caller or _http_call_mac_dinh
    form_body = urllib.parse.urlencode(
        {
            "client_id": cid,
            "client_secret": csec,
            "refresh_token": rtok,
            "grant_type": "refresh_token",
        }
    ).encode("utf-8")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "User-Agent": "Video10P-YouTubeUploader/1.0",
    }

    status, _, raw_body = caller("POST", GOOGLE_TOKEN_URL, headers, form_body, timeout)
    text_body = raw_body.decode("utf-8", errors="replace")
    if status != 200:
        goi_y = ""
        if "invalid_grant" in text_body:
            goi_y = (
                " (Refresh token da het han hoac bi thu hoi — chay lai "
                "`python -X utf8 scripts/pipeline/lay_refresh_token_youtube.py` de cap moi.)"
            )
        raise LoiDangYouTube(f"Khong doi duoc access_token (HTTP {status}): {text_body[:320]}{goi_y}")

    try:
        data = json.loads(text_body)
    except json.JSONDecodeError as err:
        raise LoiDangYouTube(f"Phan hoi Google OAuth khong phai JSON hop le: {text_body[:200]}") from err

    access_token = str(data.get("access_token") or "").strip()
    if not access_token:
        raise LoiDangYouTube(f"Phan hoi Google OAuth thieu access_token: {text_body[:200]}")

    return {
        "access_token": access_token,
        "expires_in": int(data.get("expires_in") or 3600),
        "token_type": str(data.get("token_type") or "Bearer"),
        "scope": str(data.get("scope") or ""),
    }


def tao_metadata_video(
    tieu_de: str,
    mo_ta: str,
    the_tag: list[str] | None = None,
    publish_at: str = "",
    chi_rieng_tu: bool = False,
    category_id: str = CATEGORY_ID_GIAO_DUC,
    ngon_ngu: str = "vi",
) -> dict[str, Any]:
    """Tao payload JSON `snippet` + `status` chuan YouTube Data API v3 `videos.insert`."""
    snippet: dict[str, Any] = {
        "title": _cat_tieu_de_youtube(tieu_de),
        "description": str(mo_ta or "").replace("<", "").replace(">", "")[:5000],
        "categoryId": str(category_id or CATEGORY_ID_GIAO_DUC),
        "defaultLanguage": str(ngon_ngu or "vi"),
        "defaultAudioLanguage": str(ngon_ngu or "vi"),
    }
    if the_tag:
        snippet["tags"] = list(the_tag)

    # Theo quy chuan YouTube API: khi dat lich `publishAt`, `privacyStatus` BAT BUOC la "private".
    status: dict[str, Any] = {
        "privacyStatus": "private",
        "selfDeclaredMadeForKids": False,
    }
    if not chi_rieng_tu and str(publish_at or "").strip():
        status["publishAt"] = str(publish_at).strip()

    return {"snippet": snippet, "status": status}


def _phan_tich_byte_cuoi_tu_range(range_header: str) -> int | None:
    """Doc gia tri byte cuoi tu header `Range: bytes=0-8388607`."""
    khop = re.search(r"bytes=\d+-(\d+)", str(range_header or ""))
    if not khop:
        return None
    return int(khop.group(1))


def tai_video_resumable(
    file_video: Path | str,
    metadata: dict[str, Any],
    access_token: str,
    chunk_size: int = KICH_THUOC_CHUNK_MAC_DINH,
    http_caller: HttpCaller | None = None,
    so_lan_thu_lai: int = 4,
    sleep_fn: Callable[[float], None] = time.sleep,
    timeout: int = 300,
) -> dict[str, Any]:
    """
    Upload video lon bang giao thuc Resumable Upload (chia chunk 8MB) toi YouTube Data API v3.
    Tra ve dict gom: `video_id`, `so_chunk`, `tong_bytes`, `phan_hoi`.
    """
    path_video = Path(file_video)
    if not path_video.exists():
        raise FileNotFoundError(f"Khong tim thay file video de dang YouTube: {path_video}")
    tong_bytes = path_video.stat().st_size
    if tong_bytes <= 0:
        raise ValueError(f"File video rong (0 bytes): {path_video}")

    kich_thuoc_chunk = max(256 * 1024, int(chunk_size))
    # Google Resumable Upload khuyen nghi chunk la boi so cua 256KB (262144 bytes)
    if kich_thuoc_chunk % (256 * 1024) != 0 and kich_thuoc_chunk > 256 * 1024:
        kich_thuoc_chunk = (kich_thuoc_chunk // (256 * 1024)) * (256 * 1024)

    mime_type = mimetypes.guess_type(path_video.name)[0] or "video/mp4"
    caller = http_caller or _http_call_mac_dinh

    # Buoc 1: Khoi tao phien Resumable Upload -> lay URL tu header Location
    meta_bytes = json.dumps(metadata, ensure_ascii=False).encode("utf-8")
    init_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8",
        "Content-Length": str(len(meta_bytes)),
        "X-Upload-Content-Length": str(tong_bytes),
        "X-Upload-Content-Type": mime_type,
        "User-Agent": "Video10P-YouTubeUploader/1.0",
    }

    init_status, init_resp_headers, init_body = caller(
        "POST",
        YOUTUBE_VIDEO_UPLOAD_URL,
        init_headers,
        meta_bytes,
        min(60, timeout),
    )
    if init_status not in (200, 201):
        err_txt = init_body.decode("utf-8", errors="replace")
        raise LoiDangYouTube(
            f"Khoi tao Resumable Upload that bai (HTTP {init_status}): {err_txt[:360]}"
        )

    upload_url = _lay_header_khong_phan_biet_hoa_thuong(init_resp_headers, "location")
    if not upload_url:
        raise LoiDangYouTube("YouTube API khong tra ve header 'Location' cho phien Resumable Upload.")

    # Buoc 2: Day tung chunk (mac dinh 8MB) voi Content-Range va retry khi 429/5xx
    offset = 0
    so_chunk = 0
    phan_hoi_cuoi: dict[str, Any] = {}

    with path_video.open("rb") as fh:
        while offset < tong_bytes:
            fh.seek(offset)
            chunk = fh.read(min(kich_thuoc_chunk, tong_bytes - offset))
            if not chunk:
                break
            ket_thuc = offset + len(chunk) - 1
            put_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": mime_type,
                "Content-Length": str(len(chunk)),
                "Content-Range": f"bytes {offset}-{ket_thuc}/{tong_bytes}",
                "User-Agent": "Video10P-YouTubeUploader/1.0",
            }

            thanh_cong_chunk = False
            loi_cuoi = ""
            for lan in range(max(1, int(so_lan_thu_lai))):
                status, resp_headers, resp_body = caller("PUT", upload_url, put_headers, chunk, timeout)

                if status in (200, 201):
                    so_chunk += 1
                    txt = resp_body.decode("utf-8", errors="replace")
                    try:
                        phan_hoi_cuoi = json.loads(txt) if txt.strip() else {}
                    except json.JSONDecodeError as err:
                        raise LoiDangYouTube(f"Phan hoi hoan tat upload khong phai JSON: {txt[:240]}") from err
                    offset = tong_bytes
                    thanh_cong_chunk = True
                    break

                if status == 308:
                    so_chunk += 1
                    range_hdr = _lay_header_khong_phan_biet_hoa_thuong(resp_headers, "range")
                    byte_cuoi = _phan_tich_byte_cuoi_tu_range(range_hdr)
                    if byte_cuoi is not None and byte_cuoi >= offset:
                        offset = min(tong_bytes, byte_cuoi + 1)
                    else:
                        offset = ket_thuc + 1
                    thanh_cong_chunk = True
                    break

                loi_cuoi = f"HTTP {status}: {resp_body.decode('utf-8', errors='replace')[:280]}"
                if status in MA_LOI_THU_LAI or status == 0:
                    if lan + 1 < max(1, int(so_lan_thu_lai)):
                        sleep_fn(float(2**lan))
                        continue
                break

            if not thanh_cong_chunk:
                raise LoiDangYouTube(
                    f"Upload chunk bytes {offset}-{ket_thuc}/{tong_bytes} that bai: {loi_cuoi}"
                )

    video_id = str(phan_hoi_cuoi.get("id") or "").strip()
    if not video_id:
        raise LoiDangYouTube(f"Upload xong nhung YouTube API khong tra ve video_id: {phan_hoi_cuoi}")

    return {
        "video_id": video_id,
        "so_chunk": so_chunk,
        "tong_bytes": tong_bytes,
        "phan_hoi": phan_hoi_cuoi,
    }


def gan_thumbnail_youtube(
    video_id: str,
    file_thumbnail: Path | str,
    access_token: str,
    http_caller: HttpCaller | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    """Gan anh dai dien (`thumbnails.set`) — bat loi an toan (khong lam fail luong chinh)."""
    path_thumb = Path(file_thumbnail)
    if not path_thumb.exists():
        return {"thanhCong": False, "boQua": True, "lyDo": f"Khong tim thay file thumbnail: {path_thumb}"}

    raw_bytes = path_thumb.read_bytes()
    if not raw_bytes:
        return {"thanhCong": False, "boQua": True, "lyDo": f"File thumbnail rong: {path_thumb}"}

    mime = mimetypes.guess_type(path_thumb.name)[0] or "image/png"
    url = YOUTUBE_THUMBNAIL_UPLOAD_URL_TEMPLATE.format(
        video_id=urllib.parse.quote(str(video_id).strip(), safe="")
    )
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": mime,
        "Content-Length": str(len(raw_bytes)),
        "User-Agent": "Video10P-YouTubeUploader/1.0",
    }
    caller = http_caller or _http_call_mac_dinh
    try:
        status, _, body = caller("POST", url, headers, raw_bytes, timeout)
    except Exception as err:
        return {"thanhCong": False, "boQua": False, "lyDo": f"Ngoai le khi gan thumbnail: {err}"}

    if status in (200, 201):
        return {"thanhCong": True, "boQua": False, "lyDo": "ok"}

    err_txt = body.decode("utf-8", errors="replace")[:260]
    goi_y = " (co the kenh chua xac minh so dien thoai trong YouTube Studio)" if status == 403 else ""
    return {
        "thanhCong": False,
        "boQua": False,
        "maLoi": status,
        "lyDo": f"HTTP {status}{goi_y}: {err_txt}",
    }


def tai_phu_de_youtube(
    video_id: str,
    file_srt: Path | str,
    access_token: str,
    ngon_ngu: str = "vi",
    ten_phu_de: str = "Tiếng Việt",
    http_caller: HttpCaller | None = None,
    timeout: int = 60,
) -> dict[str, Any]:
    """Tai phu de .srt len YouTube (`captions.insert` multipart/related) — bat loi an toan."""
    path_srt = Path(file_srt)
    if not path_srt.exists():
        return {"thanhCong": False, "boQua": True, "lyDo": f"Khong tim thay file phu de: {path_srt}"}

    srt_bytes = path_srt.read_bytes()
    if not srt_bytes.strip():
        return {"thanhCong": False, "boQua": True, "lyDo": f"File phu de rong: {path_srt}"}

    boundary = f"video10p_cap_{uuid.uuid4().hex}"
    meta_json = json.dumps(
        {
            "snippet": {
                "videoId": str(video_id).strip(),
                "language": str(ngon_ngu or "vi"),
                "name": str(ten_phu_de or "Tiếng Việt"),
                "isDraft": False,
            }
        },
        ensure_ascii=False,
    ).encode("utf-8")

    body_parts = [
        f"--{boundary}\r\n".encode("ascii"),
        b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
        meta_json,
        b"\r\n",
        f"--{boundary}\r\n".encode("ascii"),
        b"Content-Type: application/octet-stream\r\n\r\n",
        srt_bytes,
        b"\r\n",
        f"--{boundary}--\r\n".encode("ascii"),
    ]
    payload = b"".join(body_parts)

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": f"multipart/related; boundary={boundary}",
        "Content-Length": str(len(payload)),
        "User-Agent": "Video10P-YouTubeUploader/1.0",
    }
    caller = http_caller or _http_call_mac_dinh
    try:
        status, _, body = caller("POST", YOUTUBE_CAPTION_UPLOAD_URL, headers, payload, timeout)
    except Exception as err:
        return {"thanhCong": False, "boQua": False, "lyDo": f"Ngoai le khi tai phu de: {err}"}

    if status in (200, 201):
        return {"thanhCong": True, "boQua": False, "lyDo": "ok"}

    err_txt = body.decode("utf-8", errors="replace")[:260]
    return {
        "thanhCong": False,
        "boQua": False,
        "maLoi": status,
        "lyDo": f"HTTP {status}: {err_txt}",
    }


def luu_thong_tin_youtube_vao_bo_nho(
    slug: str,
    video_id: str,
    publish_at: str = "",
    chi_rieng_tu: bool = False,
    tieu_de: str = "",
    da_gan_thumbnail: bool = False,
    da_tai_phu_de: bool = False,
    duong_dan_bo_nho: Path | str | None = None,
    thoi_diem_tai_len: str | None = None,
) -> dict[str, Any]:
    """
    Luu `video_id` va lich hen dang vao `du_lieu/bo_nho_hoc_hoi.json` (trong ban ghi `chu_de_da_lam`
    tuong ung voi `slug`) de vong tu hoc `dong_bo_youtube.py` tu keo so lieu sau vai ngay.
    """
    path_bn = Path(duong_dan_bo_nho) if duong_dan_bo_nho is not None else DUONG_DAN_BO_NHO_MAC_DINH
    bo_nho = tai_bo_nho(path_bn)
    slug_sach = str(slug or "").strip()
    vid = str(video_id or "").strip()
    moc_tai = thoi_diem_tai_len or datetime.datetime.now(tz=MUI_GIO_VN).isoformat(timespec="seconds")
    che_do = "rieng_tu" if (chi_rieng_tu or not str(publish_at or "").strip()) else "hen_gio"

    thong_tin_yt: dict[str, Any] = {
        "youtubeVideoId": vid,
        "youtubeUrl": f"https://www.youtube.com/watch?v={vid}",
        "youtubeCheDo": che_do,
        "youtubePublishAt": str(publish_at or "").strip() if che_do == "hen_gio" else "",
        "youtubeTaiLenLuc": moc_tai,
        "youtubeDaGanThumbnail": bool(da_gan_thumbnail),
        "youtubeDaTaiPhuDe": bool(da_tai_phu_de),
    }

    da_cap_nhat = False
    for muc in bo_nho.get("chu_de_da_lam") or []:
        if isinstance(muc, dict) and str(muc.get("slug") or "").strip() == slug_sach:
            muc.update(thong_tin_yt)
            da_cap_nhat = True
            break

    if not da_cap_nhat:
        ban_ghi_moi: dict[str, Any] = {
            "slug": slug_sach,
            "tieuDe": tieu_de or slug_sach,
            "nhanVatChinh": "Nhà Toán học",
            "tomTat1Cau": "",
            "thoiLuongGiay": 0.0,
            "ngayTao": datetime.datetime.now(tz=MUI_GIO_VN).date().isoformat(),
            "nguonThamKhao": [],
        }
        ban_ghi_moi.update(thong_tin_yt)
        bo_nho.setdefault("chu_de_da_lam", []).append(ban_ghi_moi)

    luu_bo_nho(bo_nho, path_bn)
    return thong_tin_yt


def dang_video_len_youtube(
    slug: str,
    file_video: Path | str | None = None,
    file_mo_ta: Path | str | None = None,
    file_render: Path | str | None = None,
    file_thumbnail: Path | str | None = None,
    file_phu_de: Path | str | None = None,
    gio_cong_khai_vn: str = GIO_CONG_KHAI_MAC_DINH,
    cach_ngay: int = 0,
    chi_rieng_tu: bool = False,
    category_id: str = CATEGORY_ID_GIAO_DUC,
    chunk_size: int = KICH_THUOC_CHUNK_MAC_DINH,
    thu_muc_out: Path | None = None,
    thu_muc_du_lieu: Path | None = None,
    duong_dan_bo_nho: Path | str | None = None,
    duong_dan_env: Path | str | None = None,
    env_override: dict[str, str] | None = None,
    http_caller: HttpCaller | None = None,
    bay_gio: datetime.datetime | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    """
    Dieu phoi tron ven 1 luot dang video len YouTube:
    1. Doc 3 secret OAuth (thieu -> tra ve trangThai='thieu_cau_hinh', khong bao loi).
    2. Doi refresh_token lay access_token moi.
    3. Doc tieu de + mo ta + chapters + the tag, tinh `publishAt` (+07:00) hoac che do Rieng tu.
    4. Upload video bang Resumable Upload (chunk 8MB).
    5. Gan thumbnail (`thumbnail_1.png`) & tai phu de (`phu_de.srt`) — bat loi an toan.
    6. Luu `video_id` va `publishAt` vao `du_lieu/bo_nho_hoc_hoi.json`.
    """
    cfg = lay_cau_hinh_oauth_youtube(duong_dan_env=duong_dan_env, env_override=env_override)
    thieu = danh_sach_bien_thieu(cfg)
    if thieu:
        return {
            "trangThai": "thieu_cau_hinh",
            "slug": slug,
            "bienThieu": thieu,
            "huongDan": tao_huong_dan_cau_hinh_youtube(thieu),
        }

    out_root = thu_muc_out or (GOC_DU_AN / "out")
    dl_root = thu_muc_du_lieu or (GOC_DU_AN / "du_lieu")
    thu_muc_xuat_tap = out_root / slug
    thu_muc_du_lieu_tap = dl_root / slug

    path_video = Path(file_video) if file_video else (thu_muc_xuat_tap / "video_hoan_chinh.mp4")
    if not path_video.exists():
        # Fallback file legacy out/<slug>.mp4
        legacy = out_root / f"{slug}.mp4"
        if legacy.exists():
            path_video = legacy
        else:
            raise FileNotFoundError(f"Khong tim thay file video de dang YouTube: {path_video}")

    path_mo_ta = Path(file_mo_ta) if file_mo_ta else (thu_muc_xuat_tap / "chapters_va_mo_ta.txt")
    path_render = Path(file_render) if file_render else (thu_muc_du_lieu_tap / "du_lieu_render.json")
    path_thumb = Path(file_thumbnail) if file_thumbnail else (thu_muc_xuat_tap / "thumbnail_1.png")
    path_srt = Path(file_phu_de) if file_phu_de else (thu_muc_xuat_tap / "phu_de.srt")

    du_lieu_render: dict[str, Any] = {}
    if path_render.exists():
        try:
            loaded = json.loads(path_render.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                du_lieu_render = loaded
        except (OSError, json.JSONDecodeError):
            du_lieu_render = {}

    tieu_de, mo_ta = doc_tieu_de_va_mo_ta(path_mo_ta, du_lieu_render=du_lieu_render, slug=slug)
    the_tag = trich_xuat_the_tag(du_lieu_render=du_lieu_render, mo_ta=mo_ta)

    publish_at = ""
    if not chi_rieng_tu:
        publish_at = tinh_thoi_diem_cong_khai_vn(
            gio_cong_khai_vn=gio_cong_khai_vn,
            cach_ngay=cach_ngay,
            bay_gio=bay_gio,
        )

    metadata = tao_metadata_video(
        tieu_de=tieu_de,
        mo_ta=mo_ta,
        the_tag=the_tag,
        publish_at=publish_at,
        chi_rieng_tu=chi_rieng_tu,
        category_id=category_id,
    )

    # 1. Doi refresh_token -> access_token
    token_info = doi_refresh_token_lay_access_token(
        client_id=cfg["client_id"],
        client_secret=cfg["client_secret"],
        refresh_token=cfg["refresh_token"],
        http_caller=http_caller,
    )
    access_token = token_info["access_token"]

    # 2. Resumable Upload video
    kq_upload = tai_video_resumable(
        file_video=path_video,
        metadata=metadata,
        access_token=access_token,
        chunk_size=chunk_size,
        http_caller=http_caller,
        sleep_fn=sleep_fn,
    )
    video_id = kq_upload["video_id"]

    # 3. Gan anh dai dien (an toan, khong lam hong buoc chinh)
    kq_thumb = gan_thumbnail_youtube(
        video_id=video_id,
        file_thumbnail=path_thumb,
        access_token=access_token,
        http_caller=http_caller,
    )

    # 4. Tai phu de .srt (an toan, khong lam hong buoc chinh)
    kq_srt = tai_phu_de_youtube(
        video_id=video_id,
        file_srt=path_srt,
        access_token=access_token,
        http_caller=http_caller,
    )

    # 5. Luu video_id & lich hen dang vao bo_nho_hoc_hoi.json
    thong_tin_bo_nho = luu_thong_tin_youtube_vao_bo_nho(
        slug=slug,
        video_id=video_id,
        publish_at=publish_at,
        chi_rieng_tu=chi_rieng_tu,
        tieu_de=tieu_de,
        da_gan_thumbnail=bool(kq_thumb.get("thanhCong")),
        da_tai_phu_de=bool(kq_srt.get("thanhCong")),
        duong_dan_bo_nho=duong_dan_bo_nho,
    )

    return {
        "trangThai": "thanh_cong",
        "slug": slug,
        "video_id": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "tieuDe": tieu_de,
        "theTag": the_tag,
        "chiRiengTu": bool(chi_rieng_tu),
        "publishAt": publish_at,
        "upload": kq_upload,
        "thumbnail": kq_thumb,
        "phuDe": kq_srt,
        "boNho": thong_tin_bo_nho,
    }


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Tu dong dang video len YouTube Data API v3 (Resumable Upload 8MB, hen gio +07:00, "
            "gan thumbnail_1.png & tai phu_de.srt) bang Python stdlib."
        )
    )
    parser.add_argument("--slug", required=True, help="Slug cua tap phim (vd: euler_bay_cay_cau).")
    parser.add_argument("--video", default="", help="Duong dan tuy chinh toi file .mp4.")
    parser.add_argument("--mo-ta", default="", help="Duong dan tuy chinh toi chapters_va_mo_ta.txt.")
    parser.add_argument("--du-lieu-render", default="", help="Duong dan tuy chinh toi du_lieu_render.json.")
    parser.add_argument("--thumbnail", default="", help="Duong dan tuy chinh toi thumbnail_1.png.")
    parser.add_argument("--phu-de", default="", help="Duong dan tuy chinh toi phu_de.srt.")
    parser.add_argument(
        "--gio-cong-khai-vn",
        default=GIO_CONG_KHAI_MAC_DINH,
        help="Gio cong khai theo mui gio Viet Nam +07:00 dang HH:MM (mac dinh: 19:30).",
    )
    parser.add_argument(
        "--cach-ngay",
        type=int,
        default=0,
        help="So ngay cong them tinh tu hom nay theo gio VN (0 = hom nay, 1 = ngay mai).",
    )
    parser.add_argument(
        "--chi-rieng-tu",
        action="store_true",
        help="Dang o che do Rieng tu (Private) cho duyet tay, khong dat lich publishAt.",
    )
    parser.add_argument(
        "--category-id",
        default=CATEGORY_ID_GIAO_DUC,
        help="YouTube categoryId (mac dinh: 27 = Education).",
    )
    parser.add_argument(
        "--chunk-mb",
        type=int,
        default=8,
        help="Kich thuoc moi chunk Resumable Upload tinh bang MB (mac dinh: 8MB).",
    )
    parser.add_argument("--bo-nho", default="", help="Duong dan tuy chinh toi du_lieu/bo_nho_hoc_hoi.json.")
    parser.add_argument("--env", default="", help="Duong dan tuy chinh toi file .env.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    slug = str(args.slug).strip()
    duong_dan_env = Path(args.env) if args.env else None
    duong_dan_bn = Path(args.bo_nho) if args.bo_nho else DUONG_DAN_BO_NHO_MAC_DINH

    # Kiem tra nhanh secrets truoc: thieu -> in huong dan va thoat 0 an toan (KHONG fail workflow)
    cfg = lay_cau_hinh_oauth_youtube(duong_dan_env=duong_dan_env)
    thieu = danh_sach_bien_thieu(cfg)
    if thieu:
        print(tao_huong_dan_cau_hinh_youtube(thieu))
        return 0

    chunk_bytes = max(1, int(args.chunk_mb)) * 1024 * 1024
    kq = dang_video_len_youtube(
        slug=slug,
        file_video=Path(args.video) if args.video else None,
        file_mo_ta=Path(args.mo_ta) if args.mo_ta else None,
        file_render=Path(args.du_lieu_render) if args.du_lieu_render else None,
        file_thumbnail=Path(args.thumbnail) if args.thumbnail else None,
        file_phu_de=Path(args.phu_de) if args.phu_de else None,
        gio_cong_khai_vn=args.gio_cong_khai_vn,
        cach_ngay=args.cach_ngay,
        chi_rieng_tu=bool(args.chi_rieng_tu),
        category_id=args.category_id,
        chunk_size=chunk_bytes,
        duong_dan_bo_nho=duong_dan_bn,
        duong_dan_env=duong_dan_env,
    )

    if kq.get("trangThai") == "thieu_cau_hinh":
        print(kq["huongDan"])
        return 0

    che_do_str = (
        "Riêng tư (chờ duyệt tay)"
        if kq["chiRiengTu"]
        else f"Hẹn giờ công khai lúc {kq['publishAt']}"
    )
    print(f"[OK] Da tai video len YouTube thanh cong!")
    print(f"  - Video ID : {kq['video_id']}")
    print(f"  - Lien ket : {kq['url']}")
    print(f"  - Tieu de  : {kq['tieuDe']}")
    print(f"  - Che do   : {che_do_str}")
    print(
        f"  - Upload   : {kq['upload']['tong_bytes']} bytes ({kq['upload']['so_chunk']} chunk)"
    )

    tb = kq["thumbnail"]
    if tb.get("thanhCong"):
        print("  - Thumbnail: Da gan thumbnail_1.png thanh cong.")
    else:
        print(f"  - [CANH BAO] Thumbnail chua gan duoc (khong anh huong video): {tb.get('lyDo')}")

    pd = kq["phuDe"]
    if pd.get("thanhCong"):
        print("  - Phu de   : Da tai phu_de.srt (Tieng Viet) thanh cong.")
    else:
        print(f"  - [CANH BAO] Phu de chua tai duoc (khong anh huong video): {pd.get('lyDo')}")

    print(f"  - Bo nho   : Da luu video_id & lich dang vao {duong_dan_bn}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
