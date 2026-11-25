# -*- coding: utf-8 -*-
"""Sinh boi canh minh hoa 2D phong cach truyen tranh chau Au bang Gemini/Imagen & phan tich anh sang Pillow (v3.0)."""

from __future__ import annotations

import argparse
import base64
import colorsys
import copy
import hashlib
import io
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Callable

from PIL import Image

GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.gemini_client import (
    GeminiClient,
    _chuan_hoa_ten_model,
    _la_loi_het_quota_429,
    _la_loi_model_khong_hop_le,
    _la_loi_quota_hoac_tam_thoi,
    _tach_danh_sach_khong_trung,
    lay_cau_hinh_gemini,
    tai_env,
)

# Khoa chat phong cach do hoa dong nhat cho toan bo boi canh video (truyen tranh chau Au Ligne Claire / 2.5D)
STYLE_BIBLE_BOI_CANH = (
    "2D hand-drawn graphic novel background illustration, crisp dark ink outlines (#1a1a1a), "
    "flat cel-shading with warm atmospheric lighting and subtle shadows, rich historical "
    "architecture and natural environment details, earthy cinematic color palette, eye-level "
    "perspective with open flat ground in the lower 30% for animated characters to stand on, "
    "COMPLETELY EMPTY foreground with ZERO people, ZERO human figures, ZERO text, ZERO "
    "watermarks, 16:9 widescreen."
)

# Khoa phong cach cho khung hinh can canh dac ta vat the (ban do co, so tay cong thuc, qua dia cau, tau buom...)
STYLE_BIBLE_CAN_CANH_VAT_THE = (
    "2D hand-drawn European graphic novel close-up insert illustration, crisp dark ink outlines "
    "(#1a1a1a), flat cel-shading with warm atmospheric lighting and subtle shadows, richly "
    "detailed historical centerpiece object (antique parchment map, candlelit leather formula "
    "notebook, brass celestial globe, or wooden sailing ship at sea), earthy cinematic color "
    "palette, tight cinematic composition with gentle depth framing, ZERO people, ZERO human "
    "figures, ZERO hands, ZERO text, ZERO watermarks, 16:9 widescreen."
)

GEMINI_GENERATE_ENDPOINT_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
IMAGEN_PREDICT_ENDPOINT_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:predict"
)

MAC_DINH_IMAGE_MODELS: tuple[str, ...] = (
    "gemini-2.5-flash-image",
    "imagen-3.0-generate-002",
    "gemini-2.0-flash-exp-image-generation",
)

LOAI_ANH_SANG_HOP_LE: tuple[str, ...] = (
    "nang_am",
    "anh_nen",
    "dem_lanh",
    "trung_tinh",
    "hoang_hon",
)

KICH_THUOC_MAC_DINH: tuple[int, int] = (1280, 720)
CHAT_LUONG_JPEG_MAC_DINH = 86
GIOI_HAN_DUNG_LUONG_KB = 250
SO_LUONG_BOI_CANH_TOI_DA_MAC_DINH = 20
SO_LUONG_BOI_CANH_MUC_TIEU_MIN = 14

# Mo ta chi tiet kien truc/thien nhien cho du 22 boi canh v2.0
MO_TA_BOI_CANH_EN: dict[str, str] = {
    "bo_bien_hy_lap": (
        "Ancient Greek Mediterranean coastline with whitewashed marble colonnades, gnarled olive "
        "trees, terracotta rooftops along limestone cliffs, calm turquoise sea, and a wide sunlit "
        "stone promenade"
    ),
    "vuon_tao_dong_que": (
        "17th-century English countryside orchard with mature leafy apple trees, low mossy stone "
        "wall, distant timber cottage, rolling green meadows, and an open flat grass clearing"
    ),
    "pho_co_chau_au": (
        "Historic European cobblestone avenue lined with timber-framed and sandstone facades, "
        "wrought-iron streetlamps, arched wooden doors, and a wide flat stone walkway"
    ),
    "rung_nui_thien_nhien": (
        "Scenic European alpine valley with tall pine woods, distant rugged mountain peaks, "
        "winding dirt path, wildflower edges, and open level grassy ground"
    ),
    "thu_vien_co_dien": (
        "Grand classical European library hall with towering dark oak bookshelves filled with "
        "leather-bound volumes, tall arched windows, brass reading lamps, and open polished wooden floor"
    ),
    "lop_hoc_bang_xanh": (
        "19th-century European schoolroom interior with a wide green slate chalkboard on the far "
        "wall, wooden lectern, tall mullioned windows, oak paneling, and open plank floor"
    ),
    "bau_troi_dem_vu_tru": (
        "Wide hilltop ridge overlooking a deep indigo starry night sky with luminous constellations, "
        "faint Milky Way band, distant cypress silhouettes, and level rocky ground"
    ),
    "phong_nen_hai_huoc": (
        "Warm whimsical European graphic-novel studio backdrop with soft cream parchment arches, "
        "playful muted geometric motifs on the rear wall, and a clean flat wooden stage floor"
    ),
    "quang_truong_hy_lap": (
        "Classical ancient Greek agora courtyard with fluted Doric marble columns, carved stone "
        "steps, Mediterranean cypress trees, terracotta porticos, and open paved plaza ground"
    ),
    "thu_vien_trung_co": (
        "Medieval European abbey scriptorium with vaulted limestone arches, tall narrow arched "
        "windows, wooden shelves stacked with rolled parchment scrolls, and flat flagstone floor"
    ),
    "dai_thien_van_phuc_hung": (
        "Renaissance stone astronomical observatory terrace with classical arched colonnades, "
        "large brass armillary sphere set back near the balustrade, panoramic sky, and flat stone tiles"
    ),
    "giang_duong_hien_dai": (
        "Classic university mathematics lecture theater with wide dark slate board at the rear, "
        "tiered oak seating softly receding behind, warm pendant lights, and wide open wooden podium"
    ),
    "nha_co_phong_sinh": (
        "Warm traditional heritage wooden house interior with carved timber pillars, woven earthy "
        "rugs, glowing brass oil lamp on a distant wooden chest, open lattice window, and flat floor"
    ),
    "cang_bien_tau_thuy": (
        "Historic European stone harbor pier with tall wooden sailing ships moored along the quay, "
        "coiled mooring ropes, distant stone lighthouse, calm harbor water, and wide timber boardwalk"
    ),
    "phong_tro_bep_lua": (
        "Modest historic European attic study room with a glowing brick hearth fireplace, rustic "
        "wooden writing desk against the back wall, stacked old books, and open floorboards"
    ),
    "phong_benh_vien": (
        "Early 20th-century quiet sunlit sanatorium room with tall white paned windows showing green "
        "trees outside, soft cream plaster walls, tidy iron bed placed neatly to one side, and open floor"
    ),
    "duong_pho_xe_co": (
        "Early 20th-century London brick street with classical stone storefronts, vintage cast-iron "
        "streetlamps, parked antique black motorcar in the background, and wide flat cobblestone pavement"
    ),
    "giang_duong_dai_hoc": (
        "Historic Cambridge-style university lecture hall with tall gothic arched windows, rich oak "
        "wainscoting, wide slate chalkboard along the back wall, and spacious polished timber floor"
    ),
    "san_truong_co_dien": (
        "Historic European college quadrangle courtyard with ivy-draped sandstone arches, cloister "
        "walkways, manicured courtyard lawn, wrought-iron lanterns, and wide level stone path"
    ),
    "phong_thi_nghiem_co": (
        "19th-century natural philosophy laboratory with tall arched windows, wooden shelves of "
        "glass flasks and brass scientific instruments along the far wall, and open stone floor"
    ),
    "khong_gian_vu_tru_toan": (
        "Atmospheric stylized mathematical cosmos with translucent golden geometric polyhedra and "
        "delicate celestial arcs above a deep twilight horizon and a clean flat dark slate floor plane"
    ),
    "lang_que_an_do_a_dong": (
        "Traditional historic South Asian village courtyard with warm sandstone pillars, terracotta "
        "tiled roofs, lush banyan and palm trees, clay water jars near walls, and open swept earth ground"
    ),
}

MO_TA_THOI_TIET_EN: dict[str, str] = {
    "khong": "clear balanced natural daylight with gentle warm ambiance",
    "nang_dep": "bright warm golden sunlight casting soft crisp architectural shadows across the ground",
    "hoang_hon": "rich golden-amber sunset sky with warm orange and coral atmospheric light and long shadows",
    "ban_dem": "quiet deep midnight blue moonlit atmosphere with cool indigo shadows and subtle starlight",
    "mua_nhe": "soft overcast rainy atmosphere with misty cool grey-blue light and damp reflective stone",
    "la_roi": "crisp autumn afternoon golden light with a few drifting amber leaves in the background",
    "tuyet_roi": "serene winter overcast pale daylight with gentle light snowfall and soft frosted ledges",
}

MO_TA_VAT_THE_CAN_CANH_EN: dict[str, str] = {
    "ban_hoc_den_dau": (
        "Close-up of an open aged leather mathematical notebook with geometric diagrams and chalk "
        "sketches illuminated by a warm flickering brass oil lamp on a dark antique wooden desk"
    ),
    "qua_dia_cau": (
        "Close-up of an ornate antique brass-mounted parchment terrestrial globe resting on a carved "
        "oak library table bathed in warm slanted window sunlight"
    ),
    "tau_thuy": (
        "Close-up scenic view of an antique wooden multi-masted sailing ship with billowing cream "
        "sails cutting across sunlit ocean swells toward an expansive horizon"
    ),
    "phong_bi_thu_tay": (
        "Close-up of weathered cream parchment manuscript pages and a wax-sealed vintage envelope "
        "resting beside a brass inkwell and feather quill on a warm oak desk"
    ),
    "kinh_thien_van": (
        "Close-up of a polished antique brass refracting telescope on a wooden tripod angled through "
        "a stone observatory arch toward a glowing twilight sky"
    ),
    "cuon_giay": (
        "Close-up of an unrolled ancient parchment map and geometric scroll held flat by bronze "
        "weights on a warm candlelit stone table"
    ),
    "compa_co": (
        "Close-up of an antique brass drafting compass and wooden straightedge resting over an aged "
        "parchment map with delicate geometric arcs"
    ),
    "thuoc_compa": (
        "Close-up of classical wooden ruler, set square, and brass compass laid neatly across an "
        "old scholar's parchment sheet in warm directional light"
    ),
    "ban_tinh_co": (
        "Close-up of a handcrafted antique wooden abacus with worn beads beside parchment ledgers "
        "under warm golden lantern light"
    ),
    "bien_so_xe": (
        "Close-up of the gleaming brass radiator grille and classic vintage enamel plate on the front "
        "of an early 20th-century black motorcar parked on a misty cobblestone street"
    ),
    "dong_ho_cat": (
        "Close-up of an ornate brass-framed glass hourglass with glowing golden sand trickling down "
        "on a sunlit carved stone windowsill"
    ),
    "tach_tra_nong": (
        "Close-up of a warm porcelain teacup with delicate rising steam beside brass spectacles and "
        "an open notebook on a rustic wooden cafe table"
    ),
    "khoi_da_dien": (
        "Close-up of finely crafted wooden and brass Platonic polyhedra models arranged on a dark "
        "velvet scholar's desk in warm sidelight"
    ),
}

_NHOM_THOI_TIET_MAP: dict[str, str] = {
    "ban_dem": "dem",
    "hoang_hon": "hoang_hon",
    "mua_nhe": "am_u",
    "tuyet_roi": "am_u",
    "khong": "ngay",
    "nang_dep": "ngay",
    "la_roi": "ngay",
}

_BOI_CANH_NOI_THAT_NEN: frozenset[str] = frozenset(
    {
        "thu_vien_co_dien",
        "thu_vien_trung_co",
        "phong_tro_bep_lua",
        "nha_co_phong_sinh",
        "phong_thi_nghiem_co",
    }
)


def _la_model_imagen(model: str) -> bool:
    return "imagen" in _chuan_hoa_ten_model(model).lower()


def lay_cau_hinh_anh_ai(
    duong_dan_env: Path | str | None = None,
    env_override: dict[str, str] | None = None,
) -> tuple[list[str], list[str]]:
    """Lay danh sach GEMINI_API_KEYS va GEMINI_IMAGE_MODELS tu .env / bien moi truong."""
    keys, _ = lay_cau_hinh_gemini(duong_dan_env=duong_dan_env, env_override=env_override)
    tu_file = tai_env(duong_dan_env)
    nguon: dict[str, str] = {}
    nguon.update(tu_file)
    if os.environ.get("GEMINI_IMAGE_MODELS"):
        nguon["GEMINI_IMAGE_MODELS"] = os.environ["GEMINI_IMAGE_MODELS"]
    if env_override and "GEMINI_IMAGE_MODELS" in env_override:
        nguon["GEMINI_IMAGE_MODELS"] = env_override["GEMINI_IMAGE_MODELS"]

    raw_models = nguon.get("GEMINI_IMAGE_MODELS", "").strip()
    models = (
        _tach_danh_sach_khong_trung(raw_models, chuan_hoa=_chuan_hoa_ten_model)
        if raw_models
        else []
    )
    return keys, models or list(MAC_DINH_IMAGE_MODELS)


def _lam_sach_ma_file(chuoi: str) -> str:
    sach = re.sub(r"[^a-zA-Z0-9_]+", "_", str(chuoi or "").strip().lower()).strip("_")
    return sach or "boi_canh"


def tao_prompt_boi_canh(
    boi_canh: str,
    thoi_tiet: str = "nang_dep",
    mo_ta_bo_sung: str = "",
    loai_khung_hinh: str = "boi_canh",
    dao_cu_chinh: str = "",
    boi_canh_lich_su: str = "",
) -> str:
    """
    Xay dung prompt sinh anh minh hoa khoa chat STYLE_BIBLE_BOI_CANH hoac
    STYLE_BIBLE_CAN_CANH_VAT_THE de dam bao dong nhat tuyet doi toan tap.
    """
    thoi_tiet_sach = str(thoi_tiet or "nang_dep").strip().lower()
    mo_ta_tt = MO_TA_THOI_TIET_EN.get(thoi_tiet_sach, MO_TA_THOI_TIET_EN["nang_dep"])
    lich_su_sach = re.sub(r"\s+", " ", str(boi_canh_lich_su or "").strip())
    bo_sung_sach = re.sub(r"\s+", " ", str(mo_ta_bo_sung or "").strip())

    if str(loai_khung_hinh or "").strip().lower() == "can_canh_vat_the":
        dc_sach = str(dao_cu_chinh or "").strip().lower()
        mo_ta_vat = MO_TA_VAT_THE_CAN_CANH_EN.get(
            dc_sach,
            (
                "Close-up of antique mathematical instruments, parchment map, and leather formula "
                "notebook resting on a weathered wooden desk under warm atmospheric lighting"
            ),
        )
        phan: list[str] = [f"Subject: {mo_ta_vat}."]
        phan.append(f"Lighting and mood: {mo_ta_tt}.")
        if lich_su_sach:
            phan.append(f"Historical era tone: {lich_su_sach}.")
        if bo_sung_sach:
            phan.append(f"Visual details: {bo_sung_sach}.")
        phan.append(f"Art direction: {STYLE_BIBLE_CAN_CANH_VAT_THE}")
        return " ".join(phan)

    bc_sach = str(boi_canh or "thu_vien_co_dien").strip().lower()
    mo_ta_bc = MO_TA_BOI_CANH_EN.get(bc_sach, MO_TA_BOI_CANH_EN["thu_vien_co_dien"])
    phan = [f"Setting: {mo_ta_bc}.", f"Atmosphere and lighting: {mo_ta_tt}."]
    if lich_su_sach:
        phan.append(f"Historical era tone: {lich_su_sach}.")
    if bo_sung_sach:
        phan.append(f"Environmental details: {bo_sung_sach}.")
    phan.append(f"Art direction: {STYLE_BIBLE_BOI_CANH}")
    return " ".join(phan)


def bam_mo_ta_boi_canh(
    prompt: str,
    loai_khung_hinh: str = "boi_canh",
    kich_thuoc: tuple[int, int] = KICH_THUOC_MAC_DINH,
) -> str:
    """Tinh SHA-256 cho prompt + loai khung hinh + do phan giai de cache chong ton quota."""
    w, h = int(kich_thuoc[0]), int(kich_thuoc[1])
    payload = f"{loai_khung_hinh}|{w}x{h}|{prompt.strip()}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def suy_luan_anh_sang_mac_dinh(thoi_tiet: str = "nang_dep", boi_canh: str = "") -> dict[str, Any]:
    """Tra ve doi tuong anhSangMoiTruong mac dinh an toan khi dung fallback SVG."""
    tt = str(thoi_tiet or "nang_dep").strip().lower()
    bc = str(boi_canh or "").strip().lower()
    if tt == "ban_dem" or bc in ("bau_troi_dem_vu_tru", "khong_gian_vu_tru_toan"):
        if bc in _BOI_CANH_NOI_THAT_NEN:
            return {"mauAm": "#E8A24A", "doToi": 0.68, "loaiAnhSang": "anh_nen"}
        return {"mauAm": "#3B5284", "doToi": 0.78, "loaiAnhSang": "dem_lanh"}
    if tt == "hoang_hon":
        return {"mauAm": "#E88B5A", "doToi": 0.42, "loaiAnhSang": "hoang_hon"}
    if tt in ("mua_nhe", "tuyet_roi"):
        return {"mauAm": "#B9C6D2", "doToi": 0.36, "loaiAnhSang": "trung_tinh"}
    if bc in ("phong_tro_bep_lua", "thu_vien_trung_co", "nha_co_phong_sinh"):
        return {"mauAm": "#E6B46B", "doToi": 0.52, "loaiAnhSang": "anh_nen"}
    if tt == "khong":
        return {"mauAm": "#D8DCE2", "doToi": 0.24, "loaiAnhSang": "trung_tinh"}
    return {"mauAm": "#F4D99B", "doToi": 0.18, "loaiAnhSang": "nang_am"}


def phan_tich_anh_sang_moi_truong(
    nguon_anh: Path | str | bytes | Image.Image,
) -> dict[str, Any]:
    """
    Dung Pillow phan tich mau sac trung binh & do sang cua anh nen, tra ve doi tuong
    anhSangMoiTruong gom: mauAm (#RRGGBB), doToi (0..1), loaiAnhSang
    (nang_am | anh_nen | dem_lanh | trung_tinh | hoang_hon).
    """
    can_dong = False
    if isinstance(nguon_anh, Image.Image):
        img = nguon_anh
    elif isinstance(nguon_anh, (bytes, bytearray)):
        img = Image.open(io.BytesIO(nguon_anh))
        can_dong = True
    else:
        img = Image.open(Path(nguon_anh))
        can_dong = True

    try:
        rgb_nho = img.convert("RGB").resize((160, 90), _lay_bo_loc_resize())
        raw = rgb_nho.tobytes()
    finally:
        if can_dong:
            img.close()

    so_pixel = len(raw) // 3
    if so_pixel == 0:
        return {"mauAm": "#D8DCE2", "doToi": 0.3, "loaiAnhSang": "trung_tinh"}

    tong_lum = 0.0
    tong_r = 0.0
    tong_g = 0.0
    tong_b = 0.0
    # Tich luy mau tong sang chu dao (uu tien pixel sang de bat dung nguon sang moi truong)
    tong_w = 0.0
    wr = 0.0
    wg = 0.0
    wb = 0.0

    for i in range(0, len(raw), 3):
        r = raw[i]
        g = raw[i + 1]
        b = raw[i + 2]
        lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0
        tong_lum += lum
        tong_r += r
        tong_g += g
        tong_b += b
        trong_so = 0.15 + (lum * lum)
        tong_w += trong_so
        wr += r * trong_so
        wg += g * trong_so
        wb += b * trong_so

    avg_lum = tong_lum / float(so_pixel)
    do_toi = round(max(0.0, min(1.0, 1.0 - avg_lum)), 3)

    if tong_w > 0:
        lr = wr / tong_w
        lg = wg / tong_w
        lb = wb / tong_w
    else:
        lr = tong_r / float(so_pixel)
        lg = tong_g / float(so_pixel)
        lb = tong_b / float(so_pixel)

    ri = max(0, min(255, int(round(lr))))
    gi = max(0, min(255, int(round(lg))))
    bi = max(0, min(255, int(round(lb))))
    mau_am = f"#{ri:02X}{gi:02X}{bi:02X}"

    h, s, _v = colorsys.rgb_to_hsv(lr / 255.0, lg / 255.0, lb / 255.0)
    h_deg = h * 360.0
    do_am = (lr - lb) / 255.0

    # Phan loai 5 nhom anh sang moi truong cho Remotion dong bo len nhan vat
    if do_toi >= 0.58:
        if do_am >= 0.12 or (s >= 0.25 and (h_deg <= 55.0 or h_deg >= 330.0)):
            loai_anh_sang = "anh_nen"
        else:
            loai_anh_sang = "dem_lanh"
    elif 0.28 <= do_toi < 0.65 and s >= 0.28 and (h_deg <= 34.0 or h_deg >= 315.0) and (lr - lg) >= 22.0:
        loai_anh_sang = "hoang_hon"
    elif (
        (do_am >= 0.08 and s >= 0.15 and 25.0 <= h_deg <= 68.0)
        or (do_toi < 0.42 and do_am >= 0.14 and h_deg < 25.0)
    ):
        loai_anh_sang = "nang_am"
    elif do_toi >= 0.48 and do_am <= -0.05:
        loai_anh_sang = "dem_lanh"
    else:
        loai_anh_sang = "trung_tinh"

    return {
        "mauAm": mau_am,
        "doToi": do_toi,
        "loaiAnhSang": loai_anh_sang,
    }


def _lay_bo_loc_resize() -> Any:
    resampling = getattr(Image, "Resampling", None)
    if resampling is not None and hasattr(resampling, "LANCZOS"):
        return resampling.LANCZOS
    return getattr(Image, "LANCZOS", 1)


def _cat_can_giua_16_9(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    w, h = img.size
    if w <= 0 or h <= 0:
        return img
    ti_le_dich = float(target_w) / float(target_h)
    ti_le_goc = float(w) / float(h)
    if abs(ti_le_goc - ti_le_dich) < 0.005:
        return img
    if ti_le_goc > ti_le_dich:
        new_w = max(1, int(round(h * ti_le_dich)))
        x0 = (w - new_w) // 2
        return img.crop((x0, 0, x0 + new_w, h))
    new_h = max(1, int(round(w / ti_le_dich)))
    y0 = (h - new_h) // 2
    return img.crop((0, y0, w, y0 + new_h))


def luu_va_nen_anh_boi_canh(
    raw_bytes: bytes,
    file_dich: Path,
    kich_thuoc: tuple[int, int] = KICH_THUOC_MAC_DINH,
    chat_luong: int = CHAT_LUONG_JPEG_MAC_DINH,
    gioi_han_kb: int = GIOI_HAN_DUNG_LUONG_KB,
) -> dict[str, Any]:
    """
    Giai ma anh tho, cat can 16:9, resize chuan (1280x720 hoac 1920x1080) va nen JPEG
    chat luong 86 (tu dong ha nhe neu vuot gioi_han_kb de luon < 250KB).
    """
    target_w, target_h = int(kich_thuoc[0]), int(kich_thuoc[1])
    if target_w <= 0 or target_h <= 0:
        raise ValueError(f"Kich thuoc anh khong hop le: {kich_thuoc!r}")

    with Image.open(io.BytesIO(raw_bytes)) as img_goc:
        if img_goc.mode in ("RGBA", "LA") or (img_goc.mode == "P" and "transparency" in img_goc.info):
            rgba = img_goc.convert("RGBA")
            nen = Image.new("RGB", rgba.size, (242, 236, 224))
            nen.paste(rgba, mask=rgba.split()[-1])
            rgb = nen
        else:
            rgb = img_goc.convert("RGB")

        can_16_9 = _cat_can_giua_16_9(rgb, target_w, target_h)
        da_resize = can_16_9.resize((target_w, target_h), _lay_bo_loc_resize())

        max_bytes = max(32, int(gioi_han_kb)) * 1024
        q_hien_tai = max(40, min(95, int(chat_luong)))
        cac_muc_q = [q_hien_tai] + [
            q for q in (82, 78, 72, 66, 60, 52, 44, 36, 28, 20) if q < q_hien_tai
        ]

        du_lieu_jpg = b""
        q_cuoi = q_hien_tai
        for q in cac_muc_q:
            buf = io.BytesIO()
            da_resize.save(
                buf,
                format="JPEG",
                quality=q,
                optimize=True,
                progressive=True,
                subsampling="4:2:0",
            )
            du_lieu_jpg = buf.getvalue()
            q_cuoi = q
            if len(du_lieu_jpg) <= max_bytes:
                break

    file_dich.parent.mkdir(parents=True, exist_ok=True)
    file_tam = file_dich.with_suffix(".jpg.tmp")
    file_tam.write_bytes(du_lieu_jpg)
    file_tam.replace(file_dich)

    return {
        "width": target_w,
        "height": target_h,
        "sizeBytes": len(du_lieu_jpg),
        "quality": q_cuoi,
    }


def _trich_anh_tu_phan_hoi(body: str) -> bytes | None:
    """Trich bytes anh tu phan hoi Gemini generateContent (inlineData) hoac Imagen predict."""
    try:
        du_lieu = json.loads(body)
    except (json.JSONDecodeError, ValueError):
        return None
    if not isinstance(du_lieu, dict):
        return None

    # 1. Dinh dang Gemini generateContent: candidates[].content.parts[].inlineData.data
    for cand in du_lieu.get("candidates") or []:
        if not isinstance(cand, dict):
            continue
        parts = cand.get("content", {}).get("parts") or []
        for part in parts:
            if not isinstance(part, dict):
                continue
            inline = part.get("inlineData") or part.get("inline_data")
            if isinstance(inline, dict) and isinstance(inline.get("data"), str) and inline["data"].strip():
                mime = str(inline.get("mimeType") or inline.get("mime_type") or "image/png").lower()
                if mime.startswith("image/") or not mime:
                    try:
                        return base64.b64decode(inline["data"])
                    except (ValueError, TypeError):
                        continue

    # 2. Dinh dang Imagen predict: predictions[].bytesBase64Encoded (hoac image.imageBytes)
    for pred in du_lieu.get("predictions") or []:
        if not isinstance(pred, dict):
            continue
        b64_raw = pred.get("bytesBase64Encoded")
        if not b64_raw and isinstance(pred.get("image"), dict):
            b64_raw = pred["image"].get("imageBytes") or pred["image"].get("bytesBase64Encoded")
        if not b64_raw and isinstance(pred.get("inlineData"), dict):
            b64_raw = pred["inlineData"].get("data")
        if isinstance(b64_raw, str) and b64_raw.strip():
            try:
                return base64.b64decode(b64_raw)
            except (ValueError, TypeError):
                continue

    return None


class TrinhTaoBoiCanhAI:
    """
    Client tao anh boi canh 2D tu Gemini / Imagen REST API (Python stdlib urllib/json/base64 + Pillow).
    Tu dong xoay vong GEMINI_API_KEYS, thu lai khi 429/503, chuyen fallback qua GEMINI_IMAGE_MODELS
    va tra ve ket qua fallback an toan (duongDanAnh=None) khi offline hoac het quota.
    """

    def __init__(
        self,
        api_keys: list[str] | None = None,
        image_models: list[str] | tuple[str, ...] | None = None,
        duong_dan_env: Path | str | None = None,
        env_override: dict[str, str] | None = None,
        timeout_giay: int = 120,
        backoff_co_so: float = 1.5,
        so_vong_toi_da: int = 2,
        che_do_offline: bool = False,
        http_caller: Callable[[str, dict[str, Any], str, int], tuple[int, str]] | None = None,
        sleep_fn: Callable[[float], None] | None = None,
    ) -> None:
        env_keys, env_models = lay_cau_hinh_anh_ai(
            duong_dan_env=duong_dan_env,
            env_override=env_override,
        )
        self.api_keys = list(api_keys) if api_keys is not None else env_keys
        if image_models is not None:
            sach: list[str] = []
            for m in image_models:
                ten = _chuan_hoa_ten_model(m)
                if ten and ten not in sach:
                    sach.append(ten)
            self.image_models = sach or list(MAC_DINH_IMAGE_MODELS)
        else:
            self.image_models = env_models

        self.timeout_giay = int(timeout_giay)
        self.backoff_co_so = float(backoff_co_so)
        self.so_vong_toi_da = max(1, int(so_vong_toi_da))
        self.che_do_offline = bool(che_do_offline)
        self._chi_so_key = 0
        self._http_caller = http_caller or GeminiClient._goi_http_mac_dinh
        self._sleep = sleep_fn or time.sleep
        self._models_khong_kha_dung: set[str] = set()
        self._het_sach_quota = False

    def _xoay_key(self) -> None:
        if self.api_keys:
            self._chi_so_key = (self._chi_so_key + 1) % len(self.api_keys)

    @staticmethod
    def _dung_yeu_cau(model: str, prompt: str) -> tuple[str, dict[str, Any]]:
        if _la_model_imagen(model):
            url = IMAGEN_PREDICT_ENDPOINT_TEMPLATE.format(model=model)
            payload = {
                "instances": [{"prompt": prompt}],
                "parameters": {
                    "sampleCount": 1,
                    "aspectRatio": "16:9",
                },
            }
            return url, payload

        url = GEMINI_GENERATE_ENDPOINT_TEMPLATE.format(model=model)
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"],
            },
        }
        return url, payload

    def goi_tao_anh_tho(self, prompt: str) -> tuple[bytes | None, str | None, str | None]:
        """
        Goi REST tao anh qua danh sach GEMINI_IMAGE_MODELS va GEMINI_API_KEYS.
        Tra ve (raw_bytes, model_thanh_cong, thong_bao_loi). Khong bao gio nem ngoai le crash pipeline.
        """
        if self.che_do_offline:
            return None, None, "Che do offline/mock: bo qua goi API tao anh."
        if not self.api_keys:
            return None, None, "Chua cau hinh GEMINI_API_KEYS/GEMINI_API_KEY."
        if self._het_sach_quota:
            return None, None, "Toan bo key va model tao anh da het quota trong phien nay."

        so_key = len(self.api_keys)
        tong_luot_moi_model = so_key * self.so_vong_toi_da
        loi_cuoi = ""
        co_loi_quota_toan_cuc = True

        for model in self.image_models:
            if model in self._models_khong_kha_dung:
                continue
            url, payload = self._dung_yeu_cau(model, prompt)
            keys_bi_429: set[int] = set()

            for luot in range(tong_luot_moi_model):
                key = self.api_keys[self._chi_so_key]
                key_an = f"...{key[-4:]}" if len(key) >= 4 else "***"
                try:
                    status, body = self._http_caller(url, payload, key, self.timeout_giay)
                except Exception as err:
                    status, body = 503, f"ClientError: {err}"

                if status == 200:
                    anh_bytes = _trich_anh_tu_phan_hoi(body)
                    if anh_bytes:
                        return anh_bytes, model, None
                    loi_cuoi = (
                        f"HTTP 200 nhung khong tim thay du lieu anh tu model '{model}' "
                        f"(key #{self._chi_so_key + 1} {key_an})."
                    )
                    co_loi_quota_toan_cuc = False
                    break

                loi_cuoi = (
                    f"HTTP {status} (model {model}, key #{self._chi_so_key + 1} {key_an}): "
                    f"{body[:220]}"
                )

                if _la_loi_model_khong_hop_le(status, body) or status in (400, 403):
                    # Model khong ho tro tao anh / sai ten / khong co quyen -> bo qua model nay ngay
                    if status in (404, 400):
                        self._models_khong_kha_dung.add(model)
                    co_loi_quota_toan_cuc = False
                    print(f"[BoiCanhAI] Model '{model}' khong kha dung (HTTP {status}), chuyen model tiep theo...")
                    break

                if _la_loi_quota_hoac_tam_thoi(status, body):
                    if _la_loi_het_quota_429(status, body):
                        keys_bi_429.add(self._chi_so_key)
                    self._xoay_key()

                    if len(keys_bi_429) >= so_key:
                        print(
                            f"[BoiCanhAI] Model '{model}' het quota (429) tren tat ca {so_key} key, "
                            "chuyen model du phong..."
                        )
                        break

                    vong = (luot // so_key) + 1
                    cho = (
                        self.backoff_co_so * (2 ** (vong - 1))
                        if (luot + 1) % so_key == 0 or so_key == 1
                        else 0.35
                    )
                    print(
                        f"[BoiCanhAI] Loi tam thoi/quota ({status}) o '{model}', "
                        f"xoay key #{self._chi_so_key + 1}/{so_key}, cho {cho:.1f}s..."
                    )
                    self._sleep(cho)
                    continue

                co_loi_quota_toan_cuc = False
                break

        if co_loi_quota_toan_cuc and loi_cuoi:
            self._het_sach_quota = True
        return None, None, loi_cuoi or "Khong co model tao anh kha dung."

    def tao_mot_boi_canh(
        self,
        slug: str,
        ma_boi_canh: str,
        boi_canh: str,
        thoi_tiet: str = "nang_dep",
        mo_ta_bo_sung: str = "",
        loai_khung_hinh: str = "boi_canh",
        dao_cu_chinh: str = "",
        boi_canh_lich_su: str = "",
        thu_muc_public: Path | None = None,
        cache_hien_tai: dict[str, Any] | None = None,
        bo_cache: bool = False,
        kich_thuoc: tuple[int, int] = KICH_THUOC_MAC_DINH,
        chat_luong: int = CHAT_LUONG_JPEG_MAC_DINH,
        gioi_han_kb: int = GIOI_HAN_DUNG_LUONG_KB,
    ) -> dict[str, Any]:
        """
        Tao (hoac lay tu cache) 1 anh boi canh, nen JPEG <250KB va phan tich anh sang Pillow.
        Neu loi/offline/het quota -> tra ve duongDanAnh=None + anhSangMoiTruong an toan.
        """
        ma_sach = _lam_sach_ma_file(ma_boi_canh)
        prompt = tao_prompt_boi_canh(
            boi_canh=boi_canh,
            thoi_tiet=thoi_tiet,
            mo_ta_bo_sung=mo_ta_bo_sung,
            loai_khung_hinh=loai_khung_hinh,
            dao_cu_chinh=dao_cu_chinh,
            boi_canh_lich_su=boi_canh_lich_su,
        )
        hash_mo_ta = bam_mo_ta_boi_canh(prompt, loai_khung_hinh=loai_khung_hinh, kich_thuoc=kich_thuoc)

        public_root = thu_muc_public or (GOC_DU_AN / "public")
        rel_path = f"boi_canh/{slug}/{ma_sach}.jpg"
        file_dich = public_root / "boi_canh" / slug / f"{ma_sach}.jpg"

        # 1. Kiem tra cache theo hash mo ta + file ton tai
        if not bo_cache and isinstance(cache_hien_tai, dict):
            ban_ghi = cache_hien_tai.get(ma_sach)
            if (
                isinstance(ban_ghi, dict)
                and ban_ghi.get("hashMoTa") == hash_mo_ta
                and file_dich.exists()
                and file_dich.stat().st_size > 0
            ):
                anh_sang = ban_ghi.get("anhSangMoiTruong")
                if not (
                    isinstance(anh_sang, dict)
                    and isinstance(anh_sang.get("mauAm"), str)
                    and isinstance(anh_sang.get("doToi"), (int, float))
                    and anh_sang.get("loaiAnhSang") in LOAI_ANH_SANG_HOP_LE
                ):
                    anh_sang = phan_tich_anh_sang_moi_truong(file_dich)
                return {
                    "maBoiCanh": ma_sach,
                    "duongDanAnh": rel_path,
                    "duongDanTuyetDoi": str(file_dich),
                    "anhSangMoiTruong": anh_sang,
                    "tuCache": True,
                    "hashMoTa": hash_mo_ta,
                    "prompt": prompt,
                    "model": ban_ghi.get("model"),
                    "loaiKhungHinh": loai_khung_hinh,
                    "nguon": "cache",
                    "sizeBytes": file_dich.stat().st_size,
                    "loi": None,
                }

        # 2. Goi API sinh anh
        raw_bytes, model_ok, thong_bao_loi = self.goi_tao_anh_tho(prompt)
        if not raw_bytes:
            return {
                "maBoiCanh": ma_sach,
                "duongDanAnh": None,
                "duongDanTuyetDoi": None,
                "anhSangMoiTruong": suy_luan_anh_sang_mac_dinh(thoi_tiet=thoi_tiet, boi_canh=boi_canh),
                "tuCache": False,
                "hashMoTa": hash_mo_ta,
                "prompt": prompt,
                "model": None,
                "loaiKhungHinh": loai_khung_hinh,
                "nguon": "fallback_svg",
                "sizeBytes": 0,
                "loi": thong_bao_loi,
            }

        # 3. Luu anh JPEG chuan 16:9 <250KB va phan tich anh sang bang Pillow
        try:
            meta_anh = luu_va_nen_anh_boi_canh(
                raw_bytes=raw_bytes,
                file_dich=file_dich,
                kich_thuoc=kich_thuoc,
                chat_luong=chat_luong,
                gioi_han_kb=gioi_han_kb,
            )
            anh_sang = phan_tich_anh_sang_moi_truong(file_dich)
        except Exception as err:
            return {
                "maBoiCanh": ma_sach,
                "duongDanAnh": None,
                "duongDanTuyetDoi": None,
                "anhSangMoiTruong": suy_luan_anh_sang_mac_dinh(thoi_tiet=thoi_tiet, boi_canh=boi_canh),
                "tuCache": False,
                "hashMoTa": hash_mo_ta,
                "prompt": prompt,
                "model": model_ok,
                "loaiKhungHinh": loai_khung_hinh,
                "nguon": "fallback_svg",
                "sizeBytes": 0,
                "loi": f"Loi xu ly/nen anh Pillow: {err}",
            }

        return {
            "maBoiCanh": ma_sach,
            "duongDanAnh": rel_path,
            "duongDanTuyetDoi": str(file_dich),
            "anhSangMoiTruong": anh_sang,
            "tuCache": False,
            "hashMoTa": hash_mo_ta,
            "prompt": prompt,
            "model": model_ok,
            "loaiKhungHinh": loai_khung_hinh,
            "nguon": "ai",
            "sizeBytes": meta_anh["sizeBytes"],
            "width": meta_anh["width"],
            "height": meta_anh["height"],
            "quality": meta_anh["quality"],
            "loi": None,
        }


def _suy_luan_dao_cu_can_canh(canh: dict[str, Any]) -> str:
    """Tim dao cu noi bat phu hop cho khung hinh can canh vat the."""
    ds_dc = canh.get("daoCu")
    if isinstance(ds_dc, list):
        for item in ds_dc:
            if isinstance(item, dict):
                loai = str(item.get("loai") or "").strip().lower()
                if loai in MO_TA_VAT_THE_CAN_CANH_EN:
                    return loai
    return ""


def _la_canh_can_canh_vat_the(canh: dict[str, Any]) -> tuple[bool, str]:
    """Xac dinh canh nen dung khung hinh can canh vat the (STYLE_BIBLE_CAN_CANH_VAT_THE)."""
    dao_cu = _suy_luan_dao_cu_can_canh(canh)
    if not dao_cu:
        return False, ""
    may_quay = canh.get("mayQuay") if isinstance(canh.get("mayQuay"), dict) else {}
    goc_quay = str(may_quay.get("gocQuay") or "").strip().lower()
    if goc_quay == "zoom_dao_cu":
        return True, dao_cu
    loai_canh = str(canh.get("loaiCanh") or "").strip().lower()
    nhan_vat = canh.get("nhanVat") if isinstance(canh.get("nhanVat"), list) else []
    if loai_canh == "chuyen_canh_lich_su" and len(nhan_vat) == 0:
        return True, dao_cu
    return False, ""


def lap_ke_hoach_boi_canh_tap(
    du_lieu: dict[str, Any],
    so_luong_toi_da: int = SO_LUONG_BOI_CANH_TOI_DA_MAC_DINH,
    so_luong_muc_tieu_toi_thieu: int = SO_LUONG_BOI_CANH_MUC_TIEU_MIN,
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    """
    Gom nhom thong minh cac canh trong 1 tap de sinh toi da 14-20 boi canh doc ban
    (tai su dung chung cho cac canh cung dia diem/anh sang voi goc quay khac nhau).
    Tra ve (danh_sach_ke_hoach_boi_canh, ban_do_canh_id_sang_ma_boi_canh).
    """
    toi_da = max(1, int(so_luong_toi_da))
    muc_tieu_min = max(1, min(toi_da, int(so_luong_muc_tieu_toi_thieu)))

    thong_tin_canh: list[dict[str, Any]] = []
    for idx_ch, ch in enumerate(du_lieu.get("chuong") or []):
        if not isinstance(ch, dict):
            continue
        ch_id = str(ch.get("id") or f"chuong_{idx_ch + 1}")
        for idx_c, canh in enumerate(ch.get("canh") or []):
            if not isinstance(canh, dict):
                continue
            cid = str(canh.get("id") or f"canh_{len(thong_tin_canh) + 1:03d}")
            bc = str(canh.get("boiCanh") or "thu_vien_co_dien").strip().lower()
            tt = str(canh.get("thoiTiet") or "nang_dep").strip().lower()
            nhom_tt = _NHOM_THOI_TIET_MAP.get(tt, "ngay")
            la_cc, dc_cc = _la_canh_can_canh_vat_the(canh)
            nam_moc = str(canh.get("namMoc") or "").strip()
            tieu_de_nho = str(canh.get("tieuDeNho") or "").strip()
            thong_tin_canh.append(
                {
                    "canhId": cid,
                    "chuongIdx": idx_ch,
                    "chuongId": ch_id,
                    "boiCanh": bc,
                    "thoiTiet": tt,
                    "nhomThoiTiet": nhom_tt,
                    "loaiKhungHinh": "can_canh_vat_the" if la_cc else "boi_canh",
                    "daoCuChinh": dc_cc,
                    "namMoc": nam_moc,
                    "tieuDeNho": tieu_de_nho,
                    "thuTu": len(thong_tin_canh),
                }
            )

    if not thong_tin_canh:
        return [], {}

    # 0. Uu tien danhSachBoiCanhAI[] do AI Dao dien v3.0 quy hoach (14-20 dia diem + 4-6 can canh vat the)
    ds_ai_raw = du_lieu.get("danhSachBoiCanhAI")
    if isinstance(ds_ai_raw, list) and ds_ai_raw:
        tieu_de_tap = str(du_lieu.get("tieuDe") or "").strip()
        ai_items: list[dict[str, Any]] = []
        ai_by_ma: dict[str, dict[str, Any]] = {}
        for idx_ai, raw_item in enumerate(ds_ai_raw, start=1):
            if not isinstance(raw_item, dict):
                continue
            ma_raw = str(raw_item.get("maBoiCanhAI") or raw_item.get("maBoiCanh") or f"bc_{idx_ai:02d}").strip()
            ma_sach = _lam_sach_ma_file(ma_raw)
            if not ma_sach or ma_sach in ai_by_ma:
                continue
            loai_kh = str(raw_item.get("loaiKhungHinh") or "boi_canh").strip().lower()
            if loai_kh not in ("boi_canh", "can_canh_vat_the"):
                loai_kh = "boi_canh"
            bc_item = str(raw_item.get("boiCanh") or "thu_vien_co_dien").strip().lower()
            tt_item = str(raw_item.get("thoiTiet") or "nang_dep").strip().lower()
            mo_ta_en = re.sub(
                r"\s+",
                " ",
                str(raw_item.get("moTaTiengAnh") or raw_item.get("moTaBoSung") or "").strip(),
            )
            item_chuan = {
                "maBoiCanh": ma_sach,
                "loaiKhungHinh": loai_kh,
                "boiCanh": bc_item,
                "thoiTiet": tt_item,
                "nhomThoiTiet": _NHOM_THOI_TIET_MAP.get(tt_item, "ngay"),
                "daoCuChinh": str(raw_item.get("daoCuChinh") or "").strip().lower(),
                "boiCanhLichSu": tieu_de_tap,
                "moTaBoSung": mo_ta_en,
                "danhSachCanhId": [],
            }
            ai_items.append(item_chuan)
            ai_by_ma[ma_sach] = item_chuan

        if ai_items:
            # Anh xa canhId -> maBoiCanhAI theo truong maBoiCanhAI (hoac fallback khop boiCanh/loaiKhungHinh)
            canh_to_ma_ai: dict[str, str] = {}
            raw_canh_by_id: dict[str, dict[str, Any]] = {}
            for ch in du_lieu.get("chuong") or []:
                if not isinstance(ch, dict):
                    continue
                for c_obj in ch.get("canh") or []:
                    if isinstance(c_obj, dict) and c_obj.get("id"):
                        raw_canh_by_id[str(c_obj["id"])] = c_obj

            # Chi giu toi da `toi_da` boi canh uu tien cac ma duoc tham chieu
            ds_hop_le = ai_items[:toi_da]
            tap_hop_le = {m["maBoiCanh"]: m for m in ds_hop_le}

            for info in thong_tin_canh:
                cid = info["canhId"]
                c_raw = raw_canh_by_id.get(cid) or {}
                ma_ch = _lam_sach_ma_file(str(c_raw.get("maBoiCanhAI") or c_raw.get("maBoiCanh") or "")) if (c_raw.get("maBoiCanhAI") or c_raw.get("maBoiCanh")) else ""
                if ma_ch and ma_ch in tap_hop_le:
                    chon = tap_hop_le[ma_ch]
                else:
                    la_dac_ta = bool(c_raw.get("laKhungTranhDacTa")) or info["loaiKhungHinh"] == "can_canh_vat_the"
                    loai_tim = "can_canh_vat_the" if la_dac_ta else "boi_canh"
                    chon = next(
                        (m for m in ds_hop_le if m["loaiKhungHinh"] == loai_tim and m["boiCanh"] == info["boiCanh"]),
                        None,
                    )
                    if chon is None:
                        chon = next((m for m in ds_hop_le if m["boiCanh"] == info["boiCanh"]), None)
                    if chon is None:
                        chon = next((m for m in ds_hop_le if m["loaiKhungHinh"] == loai_tim), ds_hop_le[0])
                chon["danhSachCanhId"].append(cid)
                canh_to_ma_ai[cid] = chon["maBoiCanh"]

            ke_hoach_ai = [
                {
                    "maBoiCanh": m["maBoiCanh"],
                    "loaiKhungHinh": m["loaiKhungHinh"],
                    "boiCanh": m["boiCanh"],
                    "thoiTiet": m["thoiTiet"],
                    "nhomThoiTiet": m["nhomThoiTiet"],
                    "daoCuChinh": m["daoCuChinh"] if m["loaiKhungHinh"] == "can_canh_vat_the" else "",
                    "boiCanhLichSu": m["boiCanhLichSu"],
                    "moTaBoSung": m["moTaBoSung"],
                    "soCanhDung": len(m["danhSachCanhId"]),
                    "danhSachCanhId": list(m["danhSachCanhId"]),
                }
                for m in ds_hop_le
                if m["danhSachCanhId"]
            ]
            if ke_hoach_ai:
                return ke_hoach_ai, canh_to_ma_ai

    # 1. Gom nhom ban dau theo (loaiKhungHinh, boiCanh/daoCu, nhomThoiTiet)
    nhom_map: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    thu_tu_khoa: list[tuple[str, str, str]] = []
    for item in thong_tin_canh:
        if item["loaiKhungHinh"] == "can_canh_vat_the":
            khoa = ("can_canh_vat_the", item["daoCuChinh"], item["nhomThoiTiet"])
        else:
            khoa = ("boi_canh", item["boiCanh"], item["nhomThoiTiet"])
        if khoa not in nhom_map:
            nhom_map[khoa] = []
            thu_tu_khoa.append(khoa)
        nhom_map[khoa].append(item)

    # 2. Neu tap dai (>=40 canh) nhung co it nhom (< muc_tieu_min), tach them bien the theo hoi cho nhom lon
    nhom_danh_sach: list[dict[str, Any]] = [
        {
            "khoa": k,
            "items": list(nhom_map[k]),
            "bienThe": 1,
        }
        for k in thu_tu_khoa
    ]

    if len(thong_tin_canh) >= 40 and len(nhom_danh_sach) < muc_tieu_min:
        while len(nhom_danh_sach) < muc_tieu_min:
            # Tim nhom boi_canh co nhieu canh nhat trai tren >= 2 hoi
            ung_vien_idx = -1
            diem_tot = 0
            for idx, nh in enumerate(nhom_danh_sach):
                if nh["khoa"][0] != "boi_canh" or len(nh["items"]) < 6:
                    continue
                cac_hoi = sorted({it["chuongIdx"] for it in nh["items"]})
                if len(cac_hoi) < 2:
                    continue
                if len(nh["items"]) > diem_tot:
                    diem_tot = len(nh["items"])
                    ung_vien_idx = idx
            if ung_vien_idx == -1:
                break

            nh_tach = nhom_danh_sach[ung_vien_idx]
            cac_hoi = sorted({it["chuongIdx"] for it in nh_tach["items"]})
            moc_chia = cac_hoi[len(cac_hoi) // 2]
            phan_1 = [it for it in nh_tach["items"] if it["chuongIdx"] < moc_chia]
            phan_2 = [it for it in nh_tach["items"] if it["chuongIdx"] >= moc_chia]
            if not phan_1 or not phan_2:
                break
            nh_tach["items"] = phan_1
            so_bt = sum(1 for nh in nhom_danh_sach if nh["khoa"] == nh_tach["khoa"]) + 1
            nhom_danh_sach.insert(
                ung_vien_idx + 1,
                {
                    "khoa": nh_tach["khoa"],
                    "items": phan_2,
                    "bienThe": so_bt,
                },
            )

    # 3. Neu vuot qua so_luong_toi_da (mac dinh 20), gop bot nhom it xuat hien nhat vao nhom gan nhat
    while len(nhom_danh_sach) > toi_da:
        # Chon nhom it canh nhat (uu tien gop nhom it canh)
        idx_nho = min(range(len(nhom_danh_sach)), key=lambda i: (len(nhom_danh_sach[i]["items"]), -i))
        nh_gop = nhom_danh_sach.pop(idx_nho)
        k_gop = nh_gop["khoa"]

        # Tim dich gop tot nhat: cung (loai, dia_diem) -> cung dia_diem -> cung nhom_thoi_tiet -> nhom lon nhat
        def _diem_tuong_dong(nh: dict[str, Any]) -> tuple[int, int, int, int]:
            k = nh["khoa"]
            return (
                1 if (k[0] == k_gop[0] and k[1] == k_gop[1]) else 0,
                1 if (k[0] == k_gop[0] and k[2] == k_gop[2]) else 0,
                1 if k[0] == k_gop[0] else 0,
                len(nh["items"]),
            )

        idx_dich = max(range(len(nhom_danh_sach)), key=lambda i: _diem_tuong_dong(nhom_danh_sach[i]))
        nhom_danh_sach[idx_dich]["items"].extend(nh_gop["items"])

    # 4. Tao ke hoach chi tiet va anh xa canhId -> maBoiCanh
    tieu_de_tap = str(du_lieu.get("tieuDe") or "").strip()
    ke_hoach: list[dict[str, Any]] = []
    canh_to_ma: dict[str, str] = {}

    for stt, nh in enumerate(nhom_danh_sach, start=1):
        items = nh["items"]
        dai_dien = items[0]
        loai_kh, ten_chinh, nhom_tt = nh["khoa"]
        tien_to = "cc" if loai_kh == "can_canh_vat_the" else "bc"
        hau_to_bt = f"_v{nh['bienThe']}" if nh["bienThe"] > 1 else ""
        ma_boi_canh = _lam_sach_ma_file(f"{tien_to}_{stt:02d}_{ten_chinh}_{nhom_tt}{hau_to_bt}")

        nam_moc = next((it["namMoc"] for it in items if it["namMoc"]), "")
        mo_ta_them = ""
        if nh["bienThe"] > 1:
            mo_ta_them = f"alternate framing angle variant {nh['bienThe']} of the same historical place"

        boi_canh_lich_su = " — ".join(p for p in (nam_moc, tieu_de_tap) if p)

        ke_hoach.append(
            {
                "maBoiCanh": ma_boi_canh,
                "loaiKhungHinh": loai_kh,
                "boiCanh": dai_dien["boiCanh"],
                "thoiTiet": dai_dien["thoiTiet"],
                "nhomThoiTiet": nhom_tt,
                "daoCuChinh": dai_dien["daoCuChinh"] if loai_kh == "can_canh_vat_the" else "",
                "boiCanhLichSu": boi_canh_lich_su,
                "moTaBoSung": mo_ta_them,
                "soCanhDung": len(items),
                "danhSachCanhId": [it["canhId"] for it in items],
            }
        )
        for it in items:
            canh_to_ma[it["canhId"]] = ma_boi_canh

    return ke_hoach, canh_to_ma


def sinh_boi_canh_cho_tap(
    slug: str,
    du_lieu: dict[str, Any],
    thu_muc_du_lieu: Path | None = None,
    thu_muc_public: Path | None = None,
    duong_dan_env: Path | str | None = None,
    env_override: dict[str, str] | None = None,
    che_do_offline: bool = False,
    bo_cache: bool = False,
    so_luong_toi_da: int = SO_LUONG_BOI_CANH_TOI_DA_MAC_DINH,
    so_luong_muc_tieu_toi_thieu: int = SO_LUONG_BOI_CANH_MUC_TIEU_MIN,
    kich_thuoc: tuple[int, int] = KICH_THUOC_MAC_DINH,
    chat_luong: int = CHAT_LUONG_JPEG_MAC_DINH,
    gioi_han_kb: int = GIOI_HAN_DUNG_LUONG_KB,
    api_keys: list[str] | None = None,
    image_models: list[str] | tuple[str, ...] | None = None,
    http_caller: Callable[[str, dict[str, Any], str, int], tuple[int, str]] | None = None,
    sleep_fn: Callable[[float], None] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Sinh toi da 14-20 boi canh doc ban cho ca tap, luu public/boi_canh/<slug>/<ma>.jpg,
    cache theo hash mo ta tai du_lieu/<slug>/cache_boi_canh.json, va gan anhBoiCanh +
    anhSangMoiTruong vao tung canh cua du_lieu.
    """
    ket_qua_du_lieu = copy.deepcopy(du_lieu)
    ke_hoach, canh_to_ma = lap_ke_hoach_boi_canh_tap(
        ket_qua_du_lieu,
        so_luong_toi_da=so_luong_toi_da,
        so_luong_muc_tieu_toi_thieu=so_luong_muc_tieu_toi_thieu,
    )

    base_du_lieu = (thu_muc_du_lieu or (GOC_DU_AN / "du_lieu")) / slug
    base_du_lieu.mkdir(parents=True, exist_ok=True)
    file_cache = base_du_lieu / "cache_boi_canh.json"

    cache_cu: dict[str, Any] = {}
    if file_cache.exists() and not bo_cache:
        try:
            loaded = json.loads(file_cache.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                cache_cu = loaded
        except (OSError, json.JSONDecodeError):
            cache_cu = {}

    trinh = TrinhTaoBoiCanhAI(
        api_keys=api_keys,
        image_models=image_models,
        duong_dan_env=duong_dan_env,
        env_override=env_override,
        che_do_offline=che_do_offline,
        http_caller=http_caller,
        sleep_fn=sleep_fn,
    )

    ket_qua_theo_ma: dict[str, dict[str, Any]] = {}
    cache_moi: dict[str, Any] = dict(cache_cu)
    so_sinh_moi = 0
    so_hit_cache = 0
    so_fallback = 0

    print(
        f"[BoiCanhAI] Tap '{slug}': lap ke hoach {len(ke_hoach)} boi canh doc ban "
        f"(cho {len(canh_to_ma)} canh, offline={che_do_offline})."
    )

    for idx, muc in enumerate(ke_hoach, start=1):
        ma = muc["maBoiCanh"]
        kq = trinh.tao_mot_boi_canh(
            slug=slug,
            ma_boi_canh=ma,
            boi_canh=muc["boiCanh"],
            thoi_tiet=muc["thoiTiet"],
            mo_ta_bo_sung=muc["moTaBoSung"],
            loai_khung_hinh=muc["loaiKhungHinh"],
            dao_cu_chinh=muc["daoCuChinh"],
            boi_canh_lich_su=muc["boiCanhLichSu"],
            thu_muc_public=thu_muc_public,
            cache_hien_tai=cache_cu,
            bo_cache=bo_cache,
            kich_thuoc=kich_thuoc,
            chat_luong=chat_luong,
            gioi_han_kb=gioi_han_kb,
        )
        ket_qua_theo_ma[ma] = kq

        if kq["nguon"] == "cache":
            so_hit_cache += 1
        elif kq["nguon"] == "ai":
            so_sinh_moi += 1
            cache_moi[ma] = {
                "hashMoTa": kq["hashMoTa"],
                "duongDanAnh": kq["duongDanAnh"],
                "anhSangMoiTruong": kq["anhSangMoiTruong"],
                "model": kq["model"],
                "loaiKhungHinh": kq["loaiKhungHinh"],
                "sizeBytes": kq["sizeBytes"],
            }
            file_cache.write_text(
                json.dumps(cache_moi, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
        else:
            so_fallback += 1

        if idx % 5 == 0 or idx == len(ke_hoach):
            print(
                f"[BoiCanhAI] Tien do: {idx}/{len(ke_hoach)} "
                f"(AI moi: {so_sinh_moi}, cache: {so_hit_cache}, fallback SVG: {so_fallback})"
            )

    # Gan anhBoiCanh va anhSangMoiTruong vao tung canh trong du_lieu
    so_canh_co_anh = 0
    for ch in ket_qua_du_lieu.get("chuong") or []:
        if not isinstance(ch, dict):
            continue
        for canh in ch.get("canh") or []:
            if not isinstance(canh, dict):
                continue
            cid = str(canh.get("id") or "")
            ma = canh_to_ma.get(cid)
            kq_bc = ket_qua_theo_ma.get(ma) if ma else None
            if kq_bc is not None:
                canh["anhBoiCanh"] = kq_bc["duongDanAnh"]
                canh["anhSangMoiTruong"] = copy.deepcopy(kq_bc["anhSangMoiTruong"])
                if (
                    kq_bc.get("loaiKhungHinh") == "can_canh_vat_the"
                    and canh.get("laKhungTranhDacTa") is None
                    and not (canh.get("nhanVat") or [])
                ):
                    canh["laKhungTranhDacTa"] = True
                if kq_bc["duongDanAnh"]:
                    so_canh_co_anh += 1
            else:
                canh["anhBoiCanh"] = None
                canh["anhSangMoiTruong"] = suy_luan_anh_sang_mac_dinh(
                    thoi_tiet=str(canh.get("thoiTiet") or "nang_dep"),
                    boi_canh=str(canh.get("boiCanh") or ""),
                )

    thong_ke = {
        "trangThai": "hoan_tat",
        "tongBoiCanhDocBan": len(ke_hoach),
        "soSinhMoi": so_sinh_moi,
        "soDungCache": so_hit_cache,
        "soFallbackSvg": so_fallback,
        "soCanhCoAnhAi": so_canh_co_anh,
        "tongCanh": len(canh_to_ma),
        "danhSachBoiCanh": [
            {
                "maBoiCanh": m["maBoiCanh"],
                "duongDanAnh": ket_qua_theo_ma[m["maBoiCanh"]]["duongDanAnh"],
                "nguon": ket_qua_theo_ma[m["maBoiCanh"]]["nguon"],
                "loaiKhungHinh": m["loaiKhungHinh"],
                "soCanhDung": m["soCanhDung"],
                "anhSangMoiTruong": ket_qua_theo_ma[m["maBoiCanh"]]["anhSangMoiTruong"],
            }
            for m in ke_hoach
        ],
    }
    return ket_qua_du_lieu, thong_ke


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sinh boi canh minh hoa 2D phong cach truyen tranh chau Au & phan tich anh sang Pillow."
    )
    parser.add_argument("--slug", required=True, help="Slug tap phim trong du_lieu/<slug>/.")
    parser.add_argument("--input", default="", help="Duong dan file JSON dau vao (mac dinh du_lieu/<slug>/du_lieu_render.json).")
    parser.add_argument("--output", default="", help="Duong dan file JSON dau ra (mac dinh ghi de file dau vao).")
    parser.add_argument("--toi-da", type=int, default=SO_LUONG_BOI_CANH_TOI_DA_MAC_DINH, help="So boi canh doc ban toi da (mac dinh 20).")
    parser.add_argument("--chieu-rong", type=int, default=KICH_THUOC_MAC_DINH[0], help="Chieu rong anh JPEG (mac dinh 1280).")
    parser.add_argument("--chieu-cao", type=int, default=KICH_THUOC_MAC_DINH[1], help="Chieu cao anh JPEG (mac dinh 720).")
    parser.add_argument("--chat-luong", type=int, default=CHAT_LUONG_JPEG_MAC_DINH, help="Chat luong JPEG (mac dinh 86).")
    parser.add_argument("--bo-cache", action="store_true", help="Bo qua cache va sinh lai anh.")
    parser.add_argument("--offline", action="store_true", help="Chay che do offline/fallback SVG (khong goi API).")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    slug = args.slug.strip()
    file_in = Path(args.input) if args.input.strip() else (GOC_DU_AN / "du_lieu" / slug / "du_lieu_render.json")
    if not file_in.exists():
        print(f"[LOI] Khong tim thay file dau vao: {file_in}")
        return 2
    file_out = Path(args.output) if args.output.strip() else file_in

    du_lieu = json.loads(file_in.read_text(encoding="utf-8"))
    du_lieu_moi, thong_ke = sinh_boi_canh_cho_tap(
        slug=slug,
        du_lieu=du_lieu,
        che_do_offline=args.offline,
        bo_cache=args.bo_cache,
        so_luong_toi_da=args.toi_da,
        kich_thuoc=(args.chieu_rong, args.chieu_cao),
        chat_luong=args.chat_luong,
    )
    file_out.write_text(
        json.dumps(du_lieu_moi, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"[OK] Da cap nhat boi canh AI tai {file_out} | "
        f"{thong_ke['tongBoiCanhDocBan']} boi canh doc ban "
        f"(AI: {thong_ke['soSinhMoi']}, cache: {thong_ke['soDungCache']}, fallback: {thong_ke['soFallbackSvg']})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
