# -*- coding: utf-8 -*-
"""AI bien kich phim hoat hinh ke chuyen lich su Toan hoc dai >10 phut (kien truc 3 tang)."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

# Cho phep chay truc tiep: python -X utf8 scripts/pipeline/tao_kich_ban_10p.py
GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.gemini_client import GeminiClient

# ==============================================================================
# 1. HOP DONG ENUM DONG BO 100% VOI src/kieu_dai.ts
# ==============================================================================

LOAI_BO_CUC: tuple[str, ...] = (
    "mo_dau",
    "ke_chuyen",
    "doi_thoai",
    "hai_huoc",
    "giai_thich_toan",
    "dong_thoi_gian",
    "ket_thuc",
)

LOAI_BOI_CANH: tuple[str, ...] = (
    "bo_bien_hy_lap",
    "vuon_tao_dong_que",
    "pho_co_chau_au",
    "rung_nui_thien_nhien",
    "thu_vien_co_dien",
    "lop_hoc_bang_xanh",
    "bau_troi_dem_vu_tru",
    "phong_nen_hai_huoc",
)

LOAI_THOI_TIET: tuple[str, ...] = (
    "khong",
    "nang_dep",
    "hoang_hon",
    "ban_dem",
    "mua_nhe",
    "la_roi",
    "tuyet_roi",
)

LOAI_HANH_DONG: tuple[str, ...] = (
    "dung_tho",
    "di_bo",
    "chay_voi_va",
    "ngoi_doc_sach",
    "chi_tro_giai_thich",
    "nhin_len_troi",
    "gat_gu_dong_tinh",
    "gai_dau_kho_hieu",
    "giat_minh_nhay_dung",
    "bo_tay_can_loi",
    "khoanh_tay_tu_man",
    "ho_het_sung_suong",
    "di_qua_di_lai",
    "sup_do_tuyet_vong",
)

LOAI_BIEU_CAM: tuple[str, ...] = (
    "binh_thuong",
    "vui_tuoi",
    "ngac_nhien",
    "tuc_gian",
    "hoang_mang",
    "tinh_quai",
    "tram_tu",
    "can_loi_mat_do",
    "tu_man",
)

LOAI_PHU_KIEN: tuple[str, ...] = (
    "khong",
    "vong_nguyet_que",
    "toc_gia_17",
    "kinh_tron",
    "mu_noi_phap",
    "ao_choang",
    "khan_choang",
    "mu_tham_tu",
)

LOAI_VAT_CAM_TAY: tuple[str, ...] = (
    "khong",
    "cuon_giay",
    "qua_tao",
    "kinh_lup",
    "but_long_ngong",
    "que_chi_bang",
    "den_long",
    "ly_ca_phe",
)

LOAI_HIEU_UNG_HOAT_HINH: tuple[str, ...] = (
    "bong_den_nay_so",
    "giot_mo_hoi",
    "dau_cham_hoi",
    "soc_set_danh",
    "sao_lap_lanh",
    "khoi_chay_tron",
    "co_lan_im_lang",
    "nhan_chu_hai_huoc",
)

LOAI_MINH_HOA_TOAN: tuple[str, ...] = (
    "tam_giac_vuong",
    "truc_so_vo_ti",
    "do_thi_ham_so",
    "hinh_hoc_chung_minh",
    "chuoi_suy_luan",
)

LOAI_CHUYEN_CANH: tuple[str, ...] = (
    "mo_dan",
    "quet_ngang",
    "vong_tron_hoat_hinh",
)

KIEU_CAMERA: tuple[str, ...] = (
    "tinh",
    "pan_nhe",
    "zoom_cham",
    "zoom_hai_huoc",
)

LOAI_DAO_CU: tuple[str, ...] = (
    "bang_den",
    "cuon_giay",
    "bong_den",
    "dong_ho_cat",
    "can_thang_bang",
    "thuoc_compa",
    "dau_hoi_cham",
)

HUONG_NHAN_VAT: tuple[str, ...] = ("trai", "phai")

BANG_MAU_MAC_DINH: dict[str, str] = {
    "nenChinh": "#0EA5E9",
    "nenPhu": "#FEF3C7",
    "luoi": "#CBD5E1",
    "chuChinh": "#FFFFFF",
    "chuPhu": "#FEF08A",
    "nhanManh": "#FACC15",
    "canhBao": "#FB923C",
}

KHUNG_6_HOI: list[dict[str, Any]] = [
    {
        "soHoi": 1,
        "id": "chuong_1",
        "vaiTro": "Mo man to mo & Boi canh song dong",
        "phutMucTieu": 1.5,
        "tuToiThieu": 250,
        "tuMucTieu": "270-320",
        "soCanh": "15-18",
        "yeuCauDacBiet": (
            "Dat nguoi xem NGAY giua khung canh thien nhien/lich su cu the cung mot tinh huong oai oam "
            "hoac nghich ly Toan hoc gay to mo. CAM chao hoi kieu 'Xin chao cac ban' hay xin like/subscribe. "
            "Canh dau tien bat buoc dung boCuc='mo_dau' va chuyenCanh='vong_tron_hoat_hinh'."
        ),
    },
    {
        "soHoi": 2,
        "id": "chuong_2",
        "vaiTro": "Nhan vat & Rac roi thoi dai",
        "phutMucTieu": 2.0,
        "tuToiThieu": 280,
        "tuMucTieu": "300-360",
        "soCanh": "16-21",
        "yeuCauDacBiet": (
            "Gioi thieu nhan vat chinh voi tinh cach doi thuong di dom, kem bai toan hoc bua "
            "lam ca gioi hoc gia dau dau. Xen ke canh doi_thoai va dong_thoi_gian."
        ),
    },
    {
        "soHoi": 3,
        "id": "chuong_3",
        "vaiTro": "Khoanh khac 'O-re-ca!' & Giai ma Toan hoc phan 1",
        "phutMucTieu": 2.0,
        "tuToiThieu": 280,
        "tuMucTieu": "310-360",
        "soCanh": "16-22",
        "yeuCauDacBiet": (
            "Khai thac y tuong dot pha. BAT BUOC co toi thieu 2 canh boCuc='giai_thich_toan' "
            "dung boiCanh='lop_hoc_bang_xanh', co congThucLatex ro rang va minhHoaToan, "
            "giai thich cuc de hieu bang vi du doi song."
        ),
    },
    {
        "soHoi": 4,
        "id": "chuong_4",
        "vaiTro": "Buoc ngoat bat ngo & Tinh huong do khoc do cuoi",
        "phutMucTieu": 2.0,
        "tuToiThieu": 280,
        "tuMucTieu": "300-360",
        "soCanh": "16-21",
        "yeuCauDacBiet": (
            "Giai thoai that thu vi, phan ung 'can loi' cua nguoi duong thoi. "
            "BAT BUOC co it nhat 2 canh boCuc='hai_huoc' (dung zoom_hai_huoc, giot_mo_hoi, "
            "co_lan_im_lang, nhan_chu_hai_huoc va loiBinhHaiHuoc pha vo buc tuong thu 4)."
        ),
    },
    {
        "soHoi": 5,
        "id": "chuong_5",
        "vaiTro": "Chieu sau Toan hoc & The gioi hien dai",
        "phutMucTieu": 2.0,
        "tuToiThieu": 280,
        "tuMucTieu": "300-360",
        "soCanh": "16-21",
        "yeuCauDacBiet": (
            "Mo rong ban chat dinh ly (them it nhat 1 canh boCuc='giai_thich_toan' co congThucLatex & minhHoaToan) "
            "va chung minh no dang am tham van hanh thu gi quanh ta hom nay (GPS, dien thoai, tro choi, thien van...)."
        ),
    },
    {
        "soHoi": 6,
        "id": "chuong_6",
        "vaiTro": "Du am cau chuyen & Cai ket di dom",
        "phutMucTieu": 1.5,
        "tuToiThieu": 250,
        "tuMucTieu": "270-320",
        "soCanh": "15-18",
        "yeuCauDacBiet": (
            "Khep lai vong cung cau chuyen tren boi canh hoang_hon hoac bau_troi_dem_vu_tru + ban_dem, "
            "dong lai 3 y chinh + 1 cau ket co duyen, goi mo tap tiep theo. "
            "Canh cuoi cung bat buoc dung boCuc='ket_thuc'."
        ),
    },
]

SYSTEM_BIEN_KICH = (
    "Ban la dao dien & bien kich phim hoat hinh 2D ke chuyen lich su Toan hoc phong cach "
    "Kurzgesagt ket hop Oversimplified ban tieng Viet: ke chuyen cuon hut, hinh anh thien nhien "
    "chuyen dong giau chat dien anh, hai huoc di dom vua du duyen (khong lo, khong dung tuc), "
    "kien thuc Toan hoc chinh xac 100% nhung giai thich de hieu nhu dang tro chuyen cung ban than. "
    "Tra ve DUY NHAT JSON hop le, khong giai thich thua."
)


# ==============================================================================
# 2. TIEN ICH CHUNG & DEM TU / SLUG / KIEM TRA LATEX
# ==============================================================================

def tao_slug(van_ban: str) -> str:
    """Chuyen tieu de tieng Viet sang slug ASCII an toan cho ten thu muc/file."""
    s = van_ban.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s.lower()).strip("_")
    return s[:48] or "video_toan_hoc"


def dem_tu(van_ban: str) -> int:
    """Dem so tu tieng Viet thuc te trong loi thoai."""
    return len(re.findall(r"[^\W_]+", van_ban or "", flags=re.UNICODE))


def chuan_hoa_enum(gia_tri: Any, hop_le: tuple[str, ...], mac_dinh: str) -> str:
    """Chuan hoa gia tri enum theo tap hop le; fallback an toan neu sai."""
    if isinstance(gia_tri, str):
        sach = gia_tri.strip().lower().replace("-", "_").replace(" ", "_")
        if sach in hop_le:
            return sach
    return mac_dinh


def _ep_so(gia_tri: Any, mac_dinh: float, min_v: float | None = None, max_v: float | None = None) -> float:
    try:
        so = float(gia_tri)
        if not math.isfinite(so):
            so = mac_dinh
    except (TypeError, ValueError):
        so = mac_dinh
    if min_v is not None:
        so = max(min_v, so)
    if max_v is not None:
        so = min(max_v, so)
    return so


def _ep_mau_hex(gia_tri: Any, mac_dinh: str) -> str:
    if isinstance(gia_tri, str) and re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", gia_tri.strip()):
        return gia_tri.strip()
    return mac_dinh


def kiem_tra_latex(latex: str) -> tuple[str, list[str]]:
    """
    Kiem tra can bang ngoac {} va cu phap co ban trong congThucLatex.
    Tra ve (latex_da_lam_sach, danh_sach_canh_bao).
    """
    canh_bao: list[str] = []
    sach = (latex or "").strip()

    # Bo dau $ boc ngoai neu AI lo them vao
    if sach.startswith("$$") and sach.endswith("$$") and len(sach) > 4:
        sach = sach[2:-2].strip()
    elif sach.startswith("$") and sach.endswith("$") and len(sach) > 2:
        sach = sach[1:-1].strip()

    if not sach:
        canh_bao.append("Cong thuc LaTeX rong")
        return sach, canh_bao

    # Kiem tra ngoac nhon {} (bo qua \{ va \})
    do_sau = 0
    i = 0
    n = len(sach)
    ngoac_am = False
    while i < n:
        if sach[i] == "\\" and i + 1 < n:
            i += 2
            continue
        if sach[i] == "{":
            do_sau += 1
        elif sach[i] == "}":
            do_sau -= 1
            if do_sau < 0:
                ngoac_am = True
                do_sau = 0
        i += 1

    if ngoac_am:
        canh_bao.append(f"Du ngoac dong '}}' trong LaTeX: {sach}")
    if do_sau > 0:
        canh_bao.append(f"Thieu {do_sau} ngoac dong '}}' trong LaTeX (da tu dong dong): {sach}")
        sach = sach + ("}" * do_sau)

    # Kiem tra \frac phai co 2 nhom {...}{...}
    for m in re.finditer(r"\\frac(?!\s*\{)", sach):
        canh_bao.append(f"Cu phap \\frac khong theo sau boi '{{' tai vi tri {m.start()}: {sach}")

    # Kiem tra lenh \left va \right can doi
    so_left = len(re.findall(r"\\left\b", sach))
    so_right = len(re.findall(r"\\right\b", sach))
    if so_left != so_right:
        canh_bao.append(f"So luong \\left ({so_left}) != \\right ({so_right}) trong LaTeX: {sach}")

    # Kiem tra ky tu \x08 / \t / \f bi thoat nham trong JSON (vd \frac thanh \x0crac)
    if re.search(r"[\x07\x08\x0b\x0c]", sach):
        canh_bao.append(f"Phat hien ky tu dieu khien (co the quen thoat \\\\ trong JSON): {sach!r}")

    return sach, canh_bao


# ==============================================================================
# 3. SANITIZER 100% THEO src/kieu_dai.ts
# ==============================================================================

def chuan_hoa_danh_sach_nhan_vat(raw_list: Any) -> list[dict[str, Any]]:
    """Chuan hoa danhSachNhanVat theo ThongTinNhanVat trong src/kieu_dai.ts."""
    mau_chu_dao_mac_dinh = ["#2563EB", "#EA580C", "#059669", "#7C3AED", "#DB2777"]
    ket_qua: list[dict[str, Any]] = []
    da_dung_id: set[str] = set()

    if isinstance(raw_list, list):
        for idx, item in enumerate(raw_list):
            if not isinstance(item, dict):
                continue
            ten = str(item.get("ten") or f"Nhan vat {idx + 1}").strip()
            nv_id = tao_slug(str(item.get("id") or ten))
            if not nv_id or nv_id in da_dung_id:
                nv_id = f"nhan_vat_{idx + 1}"
            da_dung_id.add(nv_id)
            ket_qua.append(
                {
                    "id": nv_id,
                    "ten": ten,
                    "mauThan": _ep_mau_hex(item.get("mauThan"), "#1E293B"),
                    "mauChuDao": _ep_mau_hex(
                        item.get("mauChuDao"),
                        mau_chu_dao_mac_dinh[idx % len(mau_chu_dao_mac_dinh)],
                    ),
                    "mauDa": _ep_mau_hex(item.get("mauDa"), "#FFFDF7"),
                    "phuKien": chuan_hoa_enum(item.get("phuKien"), LOAI_PHU_KIEN, "khong"),
                }
            )

    if not ket_qua:
        ket_qua = [
            {
                "id": "nguoi_ke_chuyen",
                "ten": "Nguoi Ke Chuyen",
                "mauThan": "#1E293B",
                "mauChuDao": "#2563EB",
                "mauDa": "#FFFDF7",
                "phuKien": "kinh_tron",
            },
            {
                "id": "nha_toan_hoc",
                "ten": "Nha Toan Hoc",
                "mauThan": "#1E293B",
                "mauChuDao": "#EA580C",
                "mauDa": "#FFFDF7",
                "phuKien": "ao_choang",
            },
        ]
    return ket_qua


def chuan_hoa_canh(
    raw: dict[str, Any],
    canh_id: str,
    danh_sach_nv_ids: list[str],
    boi_canh_mac_dinh: str = "bo_bien_hy_lap",
    thoi_tiet_mac_dinh: str = "nang_dep",
) -> tuple[dict[str, Any], list[str]]:
    """Chuan hoa 1 canh theo hop dong Canh trong src/kieu_dai.ts, tra ve (canh_sach, canh_bao_latex)."""
    canh_bao_latex: list[str] = []
    id_mac_dinh = danh_sach_nv_ids[0]
    tap_nv = set(danh_sach_nv_ids)

    bo_cuc = chuan_hoa_enum(raw.get("boCuc"), LOAI_BO_CUC, "ke_chuyen")
    boi_canh_default_theo_bo_cuc = (
        "lop_hoc_bang_xanh"
        if bo_cuc == "giai_thich_toan"
        else ("phong_nen_hai_huoc" if bo_cuc == "hai_huoc" else boi_canh_mac_dinh)
    )
    boi_canh = chuan_hoa_enum(raw.get("boiCanh"), LOAI_BOI_CANH, boi_canh_default_theo_bo_cuc)
    thoi_tiet = chuan_hoa_enum(raw.get("thoiTiet"), LOAI_THOI_TIET, thoi_tiet_mac_dinh)

    loi_thoai = re.sub(r"\s+", " ", str(raw.get("loiThoai") or "").strip())
    if not loi_thoai:
        loi_thoai = "Cau chuyen Toan hoc van dang tiep tuc mo ra nhung bat ngo thu vi."

    canh: dict[str, Any] = {
        "id": canh_id,
        "boCuc": bo_cuc,
        "boiCanh": boi_canh,
        "thoiTiet": thoi_tiet,
        "tuFrame": 0,
        "denFrame": 180,
        "loiThoai": loi_thoai,
        "nhanVat": [],
    }

    if raw.get("chuyenCanh") is not None:
        canh["chuyenCanh"] = chuan_hoa_enum(raw.get("chuyenCanh"), LOAI_CHUYEN_CANH, "mo_dan")
    if raw.get("tieuDeNho"):
        canh["tieuDeNho"] = str(raw["tieuDeNho"]).strip()[:110]
    if raw.get("namMoc"):
        canh["namMoc"] = str(raw["namMoc"]).strip()[:50]

    # Phu de (neu co san)
    if isinstance(raw.get("phuDe"), list):
        phu_de_sach = [str(p).strip() for p in raw["phuDe"] if str(p).strip()]
        if phu_de_sach:
            canh["phuDe"] = phu_de_sach

    # Camera
    raw_cam = raw.get("camera")
    if isinstance(raw_cam, dict):
        cam: dict[str, Any] = {
            "kieu": chuan_hoa_enum(raw_cam.get("kieu"), KIEU_CAMERA, "tinh"),
        }
        if raw_cam.get("zoom") is not None:
            cam["zoom"] = round(_ep_so(raw_cam.get("zoom"), 1.05, 0.85, 1.55), 3)
        if raw_cam.get("panX") is not None:
            cam["panX"] = round(_ep_so(raw_cam.get("panX"), 0, -240, 240), 1)
        if raw_cam.get("panY") is not None:
            cam["panY"] = round(_ep_so(raw_cam.get("panY"), 0, -160, 160), 1)
        if isinstance(raw_cam.get("rungNhe"), bool):
            cam["rungNhe"] = raw_cam["rungNhe"]
        if raw_cam.get("mucTieuX") is not None:
            cam["mucTieuX"] = round(_ep_so(raw_cam.get("mucTieuX"), 960, 200, 1720), 1)
        if raw_cam.get("mucTieuY") is not None:
            cam["mucTieuY"] = round(_ep_so(raw_cam.get("mucTieuY"), 620, 180, 920), 1)
        if isinstance(raw_cam.get("theoDoiNhanVat"), str) and raw_cam["theoDoiNhanVat"] in tap_nv:
            cam["theoDoiNhanVat"] = raw_cam["theoDoiNhanVat"]
        canh["camera"] = cam
    else:
        canh["camera"] = {
            "kieu": "zoom_hai_huoc" if bo_cuc == "hai_huoc" else ("zoom_cham" if bo_cuc in ("mo_dau", "ket_thuc") else "tinh")
        }

    # Nhan vat trong canh
    nv_sach: list[dict[str, Any]] = []
    raw_nvs = raw.get("nhanVat") if isinstance(raw.get("nhanVat"), list) else []
    vi_tri_mac_dinh = [660, 1260, 960] if bo_cuc != "giai_thich_toan" else [255, 1660, 255]
    for idx, nv in enumerate(raw_nvs[:3]):
        if not isinstance(nv, dict):
            continue
        nv_id_raw = str(nv.get("id") or "").strip()
        nv_id = nv_id_raw if nv_id_raw in tap_nv else danh_sach_nv_ids[idx % len(danh_sach_nv_ids)]
        x_default = vi_tri_mac_dinh[idx % len(vi_tri_mac_dinh)]
        muc_nv: dict[str, Any] = {
            "id": nv_id,
            "x": round(_ep_so(nv.get("x"), x_default, 140, 1780), 1),
            "y": round(_ep_so(nv.get("y"), 810, 620, 880), 1),
            "huong": chuan_hoa_enum(nv.get("huong"), HUONG_NHAN_VAT, "phai" if idx % 2 == 0 else "trai"),
            "hanhDong": chuan_hoa_enum(nv.get("hanhDong"), LOAI_HANH_DONG, "dung_tho"),
            "bieuCam": chuan_hoa_enum(nv.get("bieuCam"), LOAI_BIEU_CAM, "binh_thuong"),
        }
        if nv.get("vatCamTay") is not None:
            muc_nv["vatCamTay"] = chuan_hoa_enum(nv.get("vatCamTay"), LOAI_VAT_CAM_TAY, "khong")
        if isinstance(nv.get("dangNoi"), bool):
            muc_nv["dangNoi"] = nv["dangNoi"]
        if nv.get("bongBongThoai"):
            muc_nv["bongBongThoai"] = str(nv["bongBongThoai"]).strip()[:90]
        if nv.get("diChuyenDenX") is not None:
            muc_nv["diChuyenDenX"] = round(_ep_so(nv.get("diChuyenDenX"), muc_nv["x"], 140, 1780), 1)
        if nv.get("tiLe") is not None:
            muc_nv["tiLe"] = round(_ep_so(nv.get("tiLe"), 1.0, 0.65, 1.45), 2)
        nv_sach.append(muc_nv)

    if not nv_sach:
        nv_sach.append(
            {
                "id": id_mac_dinh,
                "x": 255 if bo_cuc == "giai_thich_toan" else 960,
                "y": 810,
                "huong": "phai",
                "hanhDong": "chi_tro_giai_thich" if bo_cuc == "giai_thich_toan" else "dung_tho",
                "bieuCam": "vui_tuoi",
                "dangNoi": True,
            }
        )
    canh["nhanVat"] = nv_sach

    # Hieu ung hoat hinh
    if isinstance(raw.get("hieuUngHoatHinh"), list):
        hu_sach: list[dict[str, Any]] = []
        for hu in raw["hieuUngHoatHinh"][:4]:
            if not isinstance(hu, dict):
                continue
            loai_hu = chuan_hoa_enum(hu.get("loai"), LOAI_HIEU_UNG_HOAT_HINH, "sao_lap_lanh")
            muc_hu: dict[str, Any] = {
                "loai": loai_hu,
                "x": round(_ep_so(hu.get("x"), 960, 120, 1800), 1),
                "y": round(_ep_so(hu.get("y"), 480, 120, 860), 1),
                "tuFrame": int(_ep_so(hu.get("tuFrame"), 12, 0, 300)),
                "thoiLuong": int(_ep_so(hu.get("thoiLuong"), 75, 20, 360)),
            }
            if hu.get("chuHienThi"):
                muc_hu["chuHienThi"] = str(hu["chuHienThi"]).strip()[:45]
            if hu.get("mau"):
                muc_hu["mau"] = _ep_mau_hex(hu.get("mau"), "#FDE047")
            if hu.get("tiLe") is not None:
                muc_hu["tiLe"] = round(_ep_so(hu.get("tiLe"), 1.0, 0.5, 1.8), 2)
            hu_sach.append(muc_hu)
        if hu_sach:
            canh["hieuUngHoatHinh"] = hu_sach

    # Loi binh hai huoc
    raw_lb = raw.get("loiBinhHaiHuoc")
    if isinstance(raw_lb, dict) and str(raw_lb.get("noiDung") or "").strip():
        vi_tri = raw_lb.get("viTri") if raw_lb.get("viTri") in ("goc_phai", "goc_trai") else "goc_phai"
        canh["loiBinhHaiHuoc"] = {
            "noiDung": str(raw_lb["noiDung"]).strip()[:140],
            "viTri": vi_tri,
            "tuFrame": int(_ep_so(raw_lb.get("tuFrame"), 14, 0, 240)),
        }

    # Dao cu
    if isinstance(raw.get("daoCu"), list):
        dc_sach: list[dict[str, Any]] = []
        for dc in raw["daoCu"][:3]:
            if not isinstance(dc, dict):
                continue
            muc_dc: dict[str, Any] = {
                "loai": chuan_hoa_enum(dc.get("loai"), LOAI_DAO_CU, "cuon_giay"),
                "x": round(_ep_so(dc.get("x"), 960, 120, 1800), 1),
                "y": round(_ep_so(dc.get("y"), 620, 140, 900), 1),
            }
            if dc.get("tiLe") is not None:
                muc_dc["tiLe"] = round(_ep_so(dc.get("tiLe"), 1.0, 0.5, 1.8), 2)
            if dc.get("nhan"):
                muc_dc["nhan"] = str(dc["nhan"]).strip()[:40]
            if dc.get("mau"):
                muc_dc["mau"] = _ep_mau_hex(dc.get("mau"), "#FACC15")
            dc_sach.append(muc_dc)
        if dc_sach:
            canh["daoCu"] = dc_sach

    # Minh hoa Toan
    raw_mh = raw.get("minhHoaToan")
    if isinstance(raw_mh, dict):
        mh_sach: dict[str, Any] = {
            "loai": chuan_hoa_enum(raw_mh.get("loai"), LOAI_MINH_HOA_TOAN, "chuoi_suy_luan"),
        }
        if raw_mh.get("tieuDe"):
            mh_sach["tieuDe"] = str(raw_mh["tieuDe"]).strip()[:70]
        if isinstance(raw_mh.get("thamSo"), dict):
            tham_so_sach: dict[str, Any] = {}
            for k, v in raw_mh["thamSo"].items():
                khoa = str(k).strip()
                if not khoa:
                    continue
                if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v):
                    tham_so_sach[khoa] = v
                elif isinstance(v, str):
                    tham_so_sach[khoa] = v.strip()[:80]
                elif isinstance(v, list):
                    ds_so = [
                        float(x)
                        for x in v
                        if isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
                    ]
                    if ds_so:
                        tham_so_sach[khoa] = ds_so
            if tham_so_sach:
                mh_sach["thamSo"] = tham_so_sach
        canh["minhHoaToan"] = mh_sach

    # Cong thuc LaTeX + Hau kiem ngoac {}
    if isinstance(raw.get("congThucLatex"), list):
        ct_sach: list[dict[str, Any]] = []
        for idx, ct in enumerate(raw["congThucLatex"][:5]):
            if not isinstance(ct, dict):
                continue
            latex_clean, cb_list = kiem_tra_latex(str(ct.get("latex") or ""))
            for cb in cb_list:
                canh_bao_latex.append(f"[{canh_id}] {cb}")
            if not latex_clean:
                continue
            muc_ct: dict[str, Any] = {
                "latex": latex_clean,
                "tuFrame": int(_ep_so(ct.get("tuFrame"), idx * 35, 0, 400)),
            }
            if ct.get("nhan"):
                muc_ct["nhan"] = str(ct["nhan"]).strip()[:85]
            if isinstance(ct.get("noiBat"), bool):
                muc_ct["noiBat"] = ct["noiBat"]
            ct_sach.append(muc_ct)
        if ct_sach:
            canh["congThucLatex"] = ct_sach

    # Moc thoi gian
    if isinstance(raw.get("mocThoiGian"), list):
        mtg_sach: list[dict[str, Any]] = []
        for m in raw["mocThoiGian"][:5]:
            if not isinstance(m, dict):
                continue
            nam = str(m.get("nam") or "").strip()
            mo_ta = str(m.get("moTa") or "").strip()
            if not nam and not mo_ta:
                continue
            muc_m: dict[str, Any] = {"nam": nam[:30] or "...", "moTa": mo_ta[:90] or "..."}
            if isinstance(m.get("noiBat"), bool):
                muc_m["noiBat"] = m["noiBat"]
            mtg_sach.append(muc_m)
        if mtg_sach:
            canh["mocThoiGian"] = mtg_sach

    return canh, canh_bao_latex


def gan_frame_uoc_luong(du_lieu: dict[str, Any], fps: int = 30, tu_moi_giay: float = 2.65) -> dict[str, Any]:
    """Gan tuFrame/denFrame uoc luong lien mach (30fps) de nhap_kich_ban.json san sang xem truoc."""
    frame_hien_tai = 0
    ds_chuong = du_lieu.get("chuong") or []
    for idx_ch, ch in enumerate(ds_chuong):
        ds_canh = ch.get("canh") or []
        for idx_c, canh in enumerate(ds_canh):
            so_tu = dem_tu(canh.get("loiThoai", ""))
            la_cuoi_chuong = idx_c == len(ds_canh) - 1 and idx_ch < len(ds_chuong) - 1
            khoang_nghi = 0.75 if la_cuoi_chuong else 0.25
            giay = max(3.5, so_tu / tu_moi_giay) + khoang_nghi
            so_frame = max(90, int(round(giay * fps)))
            canh["tuFrame"] = frame_hien_tai
            canh["denFrame"] = frame_hien_tai + so_frame
            frame_hien_tai += so_frame
    return du_lieu


def chuan_hoa_toan_bo_kich_ban(raw: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Sanitize toan bo DuLieuVideoDai ve hop dong src/kieu_dai.ts."""
    tat_ca_canh_bao: list[str] = []
    danh_sach_nv = chuan_hoa_danh_sach_nhan_vat(raw.get("danhSachNhanVat"))
    nv_ids = [nv["id"] for nv in danh_sach_nv]

    raw_bm = raw.get("bangMau") if isinstance(raw.get("bangMau"), dict) else {}
    bang_mau = {
        khoa: _ep_mau_hex(raw_bm.get(khoa), gia_tri_md)
        for khoa, gia_tri_md in BANG_MAU_MAC_DINH.items()
    }

    chuong_sach: list[dict[str, Any]] = []
    stt_canh = 1
    for idx_ch, ch in enumerate(raw.get("chuong") or []):
        if not isinstance(ch, dict):
            continue
        ch_id = str(ch.get("id") or f"chuong_{idx_ch + 1}").strip()
        ten_chuong = str(ch.get("tenChuong") or f"Hồi {idx_ch + 1}").strip()
        canh_list_sach: list[dict[str, Any]] = []
        for c_raw in ch.get("canh") or []:
            if not isinstance(c_raw, dict):
                continue
            canh_id = f"canh_{stt_canh:03d}"
            stt_canh += 1
            canh_clean, cb_list = chuan_hoa_canh(c_raw, canh_id, nv_ids)
            tat_ca_canh_bao.extend(cb_list)
            canh_list_sach.append(canh_clean)
        if canh_list_sach:
            chuong_sach.append(
                {
                    "id": ch_id,
                    "tenChuong": ten_chuong,
                    "canh": canh_list_sach,
                }
            )

    ket_qua = {
        "tieuDe": str(raw.get("tieuDe") or "Câu Chuyện Lịch Sử Toán Học").strip(),
        "chuDe": str(raw.get("chuDe") or "").strip(),
        "batSfx": bool(raw.get("batSfx", False)),
        "batPhuDe": bool(raw.get("batPhuDe", True)),
        "bangMau": bang_mau,
        "danhSachNhanVat": danh_sach_nv,
        "chuong": chuong_sach,
    }
    gan_frame_uoc_luong(ket_qua)
    return ket_qua, tat_ca_canh_bao


# ==============================================================================
# 4. KIEN TRUC BIEN KICH 3 TANG (BLUEPRINT -> 6 HOI -> HAU KIEM & DUYET)
# ==============================================================================

def tao_prompt_tang_1(chu_de: str, muc_tieu_phut: float, giong_ke: str) -> str:
    """Tang 1: Dan y 6 Hoi (Story Blueprint) khoa danhSachNhanVat va mach boiCanh/thoiTiet."""
    mo_ta_6_hoi = "\n".join(
        f"  {h['soHoi']}. Hoi {h['soHoi']} ({h['vaiTro']}, ~{h['phutMucTieu']} phut, muc tieu {h['tuMucTieu']} tu): {h['yeuCauDacBiet']}"
        for h in KHUNG_6_HOI
    )
    return f"""
Hay thiet ke DAN Y 6 HOI (Story Blueprint) cho 1 tap phim hoat hinh 2D ke chuyen lich su Toan hoc dai khoang {muc_tieu_phut:.1f} phut (CHAC CHAN > 10 phut).
- Chu de: "{chu_de}"
- Giong ke: "{giong_ke}" (di dom, gan gui, giai thich Toan de hieu, co chieu sau lich su, KHONG kho khan nhu sach giao khoa)

CAU TRUC 6 HOI BAT BUOC:
{mo_ta_6_hoi}

DANH SACH ENUM HOP LE (BAT BUOC CHI CHON TRONG CAC GIA TRI NAY):
- phuKien: {", ".join(LOAI_PHU_KIEN)}
- boiCanh: {", ".join(LOAI_BOI_CANH)}
- thoiTiet: {", ".join(LOAI_THOI_TIET)}

YEU CAU KHOA TINH NHAT QUAN:
1. Khoa 2-4 nhan vat co dinh trong `danhSachNhanVat` (ten de nho, mauChuDao khac nhau, phuKien phu hop lich su).
2. Thiet ke mach chuyen doi `boiCanhChinh` va `thoiTietChinh` qua 6 hoi de phim co cam giac troi chay theo thoi gian (tu sang/nang dep -> ban ngay/lop hoc/thu vien -> hoang hon/hai huoc -> bau troi dem vu tru).
3. Moi hoi neu ro: tom tat cot truyen, 2-3 y tuong mieng hai tu nhien, kien thuc Toan trong tam & cong thuc du kien.

Tra ve DUY NHAT JSON dung cau truc sau:
{{
  "tieuDe": "Tieu de video hap dan tieng Viet",
  "chuDe": "Mo ta ngan 1 cau gay to mo",
  "bangMau": {{
    "nenChinh": "#0EA5E9",
    "nenPhu": "#FEF3C7",
    "luoi": "#CBD5E1",
    "chuChinh": "#FFFFFF",
    "chuPhu": "#FEF08A",
    "nhanManh": "#FACC15",
    "canhBao": "#FB923C"
  }},
  "danhSachNhanVat": [
    {{
      "id": "ten_khong_dau",
      "ten": "Ten Hien Thi",
      "mauThan": "#1E293B",
      "mauChuDao": "#2563EB",
      "mauDa": "#FFFDF7",
      "phuKien": "kinh_tron"
    }}
  ],
  "cacHoi": [
    {{
      "soHoi": 1,
      "id": "chuong_1",
      "tenChuong": "1. Ten hoi cuon hut",
      "boiCanhChinh": "bo_bien_hy_lap",
      "thoiTietChinh": "nang_dep",
      "tomTat": "Tom tat dien bien hoi...",
      "diemHaiHuoc": ["Mieng hai 1...", "Mieng hai 2..."],
      "kienThucToan": "Y tuong Toan hoc & cong thuc du kien..."
    }}
  ]
}}
""".strip()


def tao_prompt_tang_2_hoi(
    blueprint: dict[str, Any],
    thong_tin_hoi: dict[str, Any],
    khung_hoi: dict[str, Any],
    giong_ke: str,
    tom_tat_hoi_truoc: str,
) -> str:
    """Tang 2: Viet chi tiet 15-22 canh ngan cho 1 Hoi, noi mach voi Hoi truoc."""
    nv_json = json.dumps(blueprint["danhSachNhanVat"], ensure_ascii=False)
    return f"""
Ban dang viet CHI TIET HOI {khung_hoi['soHoi']}/6 cho phim hoat hinh Toan hoc:
- Tieu de phim: "{blueprint['tieuDe']}"
- Giong ke: "{giong_ke}"
- Ten hoi: "{thong_tin_hoi['tenChuong']}"
- Vai tro hoi: {khung_hoi['vaiTro']}
- Boi canh chu dao: {thong_tin_hoi['boiCanhChinh']} | Thoi tiet chu dao: {thong_tin_hoi['thoiTietChinh']}
- Tom tat hoi nay: {thong_tin_hoi['tomTat']}
- Mieng hai du kien: {json.dumps(thong_tin_hoi.get('diemHaiHuoc', []), ensure_ascii=False)}
- Kien thuc Toan trong tam: {thong_tin_hoi.get('kienThucToan', '')}
- Mach noi tu hoi truoc: {tom_tat_hoi_truoc}
- Danh sach nhan vat CO DINH (chi duoc dung dung id trong nay): {nv_json}

YEU CAU CHAT LUONG & DO DAI BAT BUOC:
1. Sinh tu {khung_hoi['soCanh']} canh ngan (toi thieu 15 canh).
2. Moi canh co `loiThoai` dai 18-35 tu tieng Viet tu nhien nhu dang ke chuyen. TONG SO TU cua hoi nay BAT BUOC dat {khung_hoi['tuMucTieu']} tu (khong duoc duoi 260 tu!).
3. Cai 2-3 diem nhan hai huoc tu nhien (vi von hien dai, `loiBinhHaiHuoc` pha buc tuong thu 4, bieu cam `can_loi_mat_do` + hieu ung `giot_mo_hoi`/`co_lan_im_lang`/`nhan_chu_hai_huoc`).
4. Yeu cau dac biet cua Hoi {khung_hoi['soHoi']}: {khung_hoi['yeuCauDacBiet']}
5. Trong `congThucLatex`: dung LaTeX chuan KaTeX (NHAC LAI: thoat dau \\ thanh \\\\ trong JSON, khong boc dau $).
6. CHI DUNG DUNG CAC GIA TRI ENUM SAU:
   - boCuc: {", ".join(LOAI_BO_CUC)}
   - boiCanh: {", ".join(LOAI_BOI_CANH)}
   - thoiTiet: {", ".join(LOAI_THOI_TIET)}
   - chuyenCanh: {", ".join(LOAI_CHUYEN_CANH)}
   - camera.kieu: {", ".join(KIEU_CAMERA)}
   - hanhDong: {", ".join(LOAI_HANH_DONG)}
   - bieuCam: {", ".join(LOAI_BIEU_CAM)}
   - vatCamTay: {", ".join(LOAI_VAT_CAM_TAY)}
   - hieuUngHoatHinh.loai: {", ".join(LOAI_HIEU_UNG_HOAT_HINH)}
   - minhHoaToan.loai: {", ".join(LOAI_MINH_HOA_TOAN)}
   - daoCu.loai: {", ".join(LOAI_DAO_CU)}
7. Toa do 1920x1080: nhan vat dung mat dat tai y=810, x khoang 560..1360 (rieng canh giai_thich_toan dat nhan vat x=255, y=808 de nhuong bang xanh ben phai).

Tra ve DUY NHAT JSON dung cau truc:
{{
  "id": "{khung_hoi['id']}",
  "tenChuong": "{thong_tin_hoi['tenChuong']}",
  "tomTatKetHoi": "1-2 cau tom tat diem ket hoi de noi mach sang hoi sau",
  "canh": [
    {{
      "boCuc": "ke_chuyen",
      "boiCanh": "{thong_tin_hoi['boiCanhChinh']}",
      "thoiTiet": "{thong_tin_hoi['thoiTietChinh']}",
      "chuyenCanh": "mo_dan",
      "namMoc": "~500 TCN",
      "tieuDeNho": "Tieu de ngan gon",
      "loiThoai": "Loi thoai tieng Viet tu nhien dai 20-32 tu...",
      "camera": {{"kieu": "pan_nhe"}},
      "nhanVat": [
        {{
          "id": "{blueprint['danhSachNhanVat'][0]['id']}",
          "x": 760,
          "y": 810,
          "huong": "phai",
          "hanhDong": "chi_tro_giai_thich",
          "vatCamTay": "cuon_giay",
          "bieuCam": "vui_tuoi",
          "dangNoi": true
        }}
      ],
      "hieuUngHoatHinh": [],
      "loiBinhHaiHuoc": null
    }}
  ]
}}
""".strip()


def tao_prompt_bo_sung_hoi(
    blueprint: dict[str, Any],
    thong_tin_hoi: dict[str, Any],
    canh_hien_co: list[dict[str, Any]],
    so_tu_hien_tai: int,
    muc_tieu_tu: int = 300,
) -> str:
    """Goi bo sung 4-5 canh ke chi tiet giai thoai/vi du neu hoi bi ngan (<250 tu)."""
    can_them = max(80, muc_tieu_tu - so_tu_hien_tai)
    doan_cuoi = " | ".join(c.get("loiThoai", "") for c in canh_hien_co[-2:])
    return f"""
Hoi "{thong_tin_hoi['tenChuong']}" hien moi co {so_tu_hien_tai} tu (qua ngan, can them khoang {can_them} tu).
Hay viet BO SUNG them 4-5 canh ke chi tiet giai thoai lich su, vi du doi song de hieu hoac 1 tinh huong hai huoc di dom de chen ngay truoc canh ket cua hoi nay.
- Mach dang ke: "{doan_cuoi}"
- Nhan vat co dinh: {json.dumps(blueprint['danhSachNhanVat'], ensure_ascii=False)}
- Boi canh chu dao: {thong_tin_hoi['boiCanhChinh']} | Thoi tiet: {thong_tin_hoi['thoiTietChinh']}
- Moi canh dai 22-35 tu, dung dung enum cua he thong.

Tra ve DUY NHAT JSON:
{{
  "canhBoSung": [
    {{
      "boCuc": "ke_chuyen",
      "boiCanh": "{thong_tin_hoi['boiCanhChinh']}",
      "thoiTiet": "{thong_tin_hoi['thoiTietChinh']}",
      "tieuDeNho": "Chi tiet thu vi",
      "loiThoai": "Loi thoai 24-34 tu...",
      "camera": {{"kieu": "pan_nhe"}},
      "nhanVat": [
        {{
          "id": "{blueprint['danhSachNhanVat'][0]['id']}",
          "x": 860,
          "y": 810,
          "huong": "phai",
          "hanhDong": "chi_tro_giai_thich",
          "bieuCam": "tinh_quai",
          "dangNoi": true
        }}
      ]
    }}
  ]
}}
""".strip()


def tao_markdown_doc_duyet(
    du_lieu: dict[str, Any],
    canh_bao_latex: list[str] | None = None,
    tu_moi_giay: float = 2.65,
) -> str:
    """Tang 3: Xuat file doc_duyet_kich_ban.md trinh bay dep theo 6 hoi de duyet nhanh trong 3 phut."""
    canh_bao_latex = canh_bao_latex or []
    ds_chuong = du_lieu.get("chuong") or []

    tong_canh = 0
    tong_tu = 0
    tong_canh_toan = 0
    tong_canh_hai = 0
    bang_hoi: list[str] = []

    for idx_ch, ch in enumerate(ds_chuong, start=1):
        ds_canh = ch.get("canh") or []
        tu_hoi = sum(dem_tu(c.get("loiThoai", "")) for c in ds_canh)
        canh_toan = sum(1 for c in ds_canh if c.get("boCuc") == "giai_thich_toan" or c.get("congThucLatex"))
        canh_hai = sum(
            1
            for c in ds_canh
            if c.get("boCuc") == "hai_huoc"
            or c.get("loiBinhHaiHuoc")
            or any(
                hu.get("loai") in ("giot_mo_hoi", "co_lan_im_lang", "nhan_chu_hai_huoc")
                for hu in (c.get("hieuUngHoatHinh") or [])
            )
        )
        phut_hoi = (tu_hoi / tu_moi_giay + len(ds_canh) * 0.25 + 0.5) / 60.0
        tong_canh += len(ds_canh)
        tong_tu += tu_hoi
        tong_canh_toan += canh_toan
        tong_canh_hai += canh_hai
        bang_hoi.append(
            f"| Hồi {idx_ch} | {ch.get('tenChuong', '')} | {len(ds_canh)} | {tu_hoi} | ~{phut_hoi:.2f} phút | {canh_toan} | {canh_hai} |"
        )

    tong_giay_du_kien = tong_tu / tu_moi_giay + tong_canh * 0.25 + max(0, len(ds_chuong) - 1) * 0.5
    tong_phut_du_kien = tong_giay_du_kien / 60.0
    trang_thai_thoi_luong = (
        "ĐẠT MỤC TIÊU > 10 PHÚT" if tong_giay_du_kien >= 600 else "CẢNH BÁO: DỰ KIẾN < 10 PHÚT"
    )

    dong: list[str] = [
        f"# ĐỌC DUYỆT KỊCH BẢN: {du_lieu.get('tieuDe', '')}",
        "",
        f"> **Chủ đề:** {du_lieu.get('chuDe', '')}",
        "",
        "## Tổng quan nhanh",
        f"- **Số hồi:** {len(ds_chuong)} | **Tổng số cảnh:** {tong_canh}",
        f"- **Tổng số từ lời thoại:** {tong_tu} từ",
        f"- **Thời lượng dự kiến:** ~{tong_phut_du_kien:.2f} phút (~{int(round(tong_giay_du_kien))} giây) — **{trang_thai_thoi_luong}**",
        f"- **Số cảnh có Toán / KaTeX:** {tong_canh_toan} | **Số cảnh có điểm nhấn hài:** {tong_canh_hai}",
        "",
        "| Hồi | Tên hồi | Số cảnh | Số từ | Dự kiến | Cảnh Toán | Miếng hài |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
        *bang_hoi,
        "",
        "## Dàn nhân vật cố định",
    ]

    for nv in du_lieu.get("danhSachNhanVat") or []:
        dong.append(
            f"- **{nv.get('ten')}** (`{nv.get('id')}`): màu chủ đạo `{nv.get('mauChuDao')}`, phụ kiện `{nv.get('phuKien')}`"
        )

    if canh_bao_latex:
        dong.extend(["", "## Cảnh báo hậu kiểm LaTeX"])
        for cb in canh_bao_latex:
            dong.append(f"- ⚠️ {cb}")
    else:
        dong.extend(["", "## Hậu kiểm LaTeX", "- ✅ Toàn bộ công thức KaTeX cân bằng ngoặc `{}` và hợp lệ cơ bản."])

    dong.append("")
    dong.append("---")

    for idx_ch, ch in enumerate(ds_chuong, start=1):
        ds_canh = ch.get("canh") or []
        tu_hoi = sum(dem_tu(c.get("loiThoai", "")) for c in ds_canh)
        dong.extend(
            [
                "",
                f"## Hồi {idx_ch}: {ch.get('tenChuong', '')} ({len(ds_canh)} cảnh • {tu_hoi} từ)",
                "",
            ]
        )
        for c in ds_canh:
            nhan: list[str] = []
            if c.get("boCuc") == "giai_thich_toan" or c.get("congThucLatex"):
                nhan.append("`[TOÁN / KaTeX]`")
            if (
                c.get("boCuc") == "hai_huoc"
                or c.get("loiBinhHaiHuoc")
                or any(
                    hu.get("loai") in ("giot_mo_hoi", "co_lan_im_lang", "nhan_chu_hai_huoc")
                    for hu in (c.get("hieuUngHoatHinh") or [])
                )
            ):
                nhan.append("`[HÀI]`")
            tag_str = (" " + " ".join(nhan)) if nhan else ""
            so_tu_c = dem_tu(c.get("loiThoai", ""))
            tieu_de_nho = f" — *{c['tieuDeNho']}*" if c.get("tieuDeNho") else ""
            dong.append(
                f"### `{c['id']}` ({c['boCuc']} • {c['boiCanh']} • {c.get('thoiTiet', 'khong')} • {so_tu_c} từ){tag_str}{tieu_de_nho}"
            )
            dong.append(f"> {c.get('loiThoai', '')}")
            if c.get("loiBinhHaiHuoc"):
                dong.append(f"- 😂 **Lời bình góc màn hình:** {c['loiBinhHaiHuoc'].get('noiDung', '')}")
            if c.get("minhHoaToan"):
                mh = c["minhHoaToan"]
                dong.append(f"- 📐 **Minh họa Toán:** `{mh.get('loai')}` — {mh.get('tieuDe', '')}")
            if c.get("congThucLatex"):
                dong.append("- 🧮 **Công thức KaTeX:**")
                for ct in c["congThucLatex"]:
                    nhan_ct = f" ({ct['nhan']})" if ct.get("nhan") else ""
                    dong.append(f"  - `{ct.get('latex', '')}`{nhan_ct}")
            dong.append("")

    return "\n".join(dong).strip() + "\n"


def bien_kich_3_tang(
    chu_de: str,
    slug: str,
    muc_tieu_phut: float = 11.0,
    giong_ke: str = "di_dom_gan_gui",
    bo_cache: bool = False,
    client: GeminiClient | None = None,
    thu_muc_du_lieu: Path | None = None,
) -> tuple[Path, Path, dict[str, Any]]:
    """Chay tron ven 3 tang bien kich va xuat nhap_kich_ban.json + doc_duyet_kich_ban.md."""
    muc_tieu_thuc = max(10.5, float(muc_tieu_phut))
    base_dir = (thu_muc_du_lieu or (GOC_DU_AN / "du_lieu")) / slug
    cache_dir = base_dir / "cache_chuong"
    cache_dir.mkdir(parents=True, exist_ok=True)

    gemini = client or GeminiClient()

    # --- TANG 1: DAN Y 6 HOI ---
    file_blueprint = cache_dir / "dan_y_6_hoi.json"
    if file_blueprint.exists() and not bo_cache:
        print(f"[Tang 1] Tai cache dan y 6 hoi: {file_blueprint}")
        blueprint = json.loads(file_blueprint.read_text(encoding="utf-8"))
    else:
        print(f"[Tang 1] Dang lap Dan y 6 Hoi cho chu de: {chu_de} (~{muc_tieu_thuc:.1f} phut)...")
        raw_bp = gemini.tao_json(
            prompt=tao_prompt_tang_1(chu_de, muc_tieu_thuc, giong_ke),
            system_instruction=SYSTEM_BIEN_KICH,
            nhiet_do=0.75,
            max_output_tokens=4096,
        )
        blueprint = {
            "tieuDe": str(raw_bp.get("tieuDe") or chu_de).strip(),
            "chuDe": str(raw_bp.get("chuDe") or chu_de).strip(),
            "bangMau": raw_bp.get("bangMau") or BANG_MAU_MAC_DINH,
            "danhSachNhanVat": chuan_hoa_danh_sach_nhan_vat(raw_bp.get("danhSachNhanVat")),
            "cacHoi": [],
        }
        raw_cac_hoi = raw_bp.get("cacHoi") if isinstance(raw_bp.get("cacHoi"), list) else []
        for idx, khung in enumerate(KHUNG_6_HOI):
            item = raw_cac_hoi[idx] if idx < len(raw_cac_hoi) and isinstance(raw_cac_hoi[idx], dict) else {}
            blueprint["cacHoi"].append(
                {
                    "soHoi": khung["soHoi"],
                    "id": khung["id"],
                    "tenChuong": str(item.get("tenChuong") or f"{khung['soHoi']}. {khung['vaiTro']}").strip(),
                    "boiCanhChinh": chuan_hoa_enum(item.get("boiCanhChinh"), LOAI_BOI_CANH, "bo_bien_hy_lap"),
                    "thoiTietChinh": chuan_hoa_enum(item.get("thoiTietChinh"), LOAI_THOI_TIET, "nang_dep"),
                    "tomTat": str(item.get("tomTat") or khung["vaiTro"]).strip(),
                    "diemHaiHuoc": item.get("diemHaiHuoc") if isinstance(item.get("diemHaiHuoc"), list) else [],
                    "kienThucToan": str(item.get("kienThucToan") or "").strip(),
                }
            )
        file_blueprint.write_text(json.dumps(blueprint, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    nv_ids = [nv["id"] for nv in blueprint["danhSachNhanVat"]]

    # --- TANG 2: VIET CHI TIET 6 HOI NOI MACH ---
    danh_sach_chuong_raw: list[dict[str, Any]] = []
    tom_tat_hoi_truoc = "Day la Hoi mo dau, dat nguoi xem ngay vao boi canh va tinh huong to mo."

    for idx, khung in enumerate(KHUNG_6_HOI):
        thong_tin_hoi = blueprint["cacHoi"][idx]
        file_cache_hoi = cache_dir / f"hoi_{khung['soHoi']:02d}.json"

        if file_cache_hoi.exists() and not bo_cache:
            print(f"[Tang 2] Tai cache Hoi {khung['soHoi']}/6: {file_cache_hoi.name}")
            du_lieu_hoi = json.loads(file_cache_hoi.read_text(encoding="utf-8"))
        else:
            print(f"[Tang 2] Dang viet chi tiet Hoi {khung['soHoi']}/6: {thong_tin_hoi['tenChuong']}...")
            du_lieu_hoi = gemini.tao_json(
                prompt=tao_prompt_tang_2_hoi(
                    blueprint=blueprint,
                    thong_tin_hoi=thong_tin_hoi,
                    khung_hoi=khung,
                    giong_ke=giong_ke,
                    tom_tat_hoi_truoc=tom_tat_hoi_truoc,
                ),
                system_instruction=SYSTEM_BIEN_KICH,
                nhiet_do=0.75,
                max_output_tokens=8192,
            )
            canh_list = du_lieu_hoi.get("canh") if isinstance(du_lieu_hoi.get("canh"), list) else []
            so_tu_hoi = sum(dem_tu(c.get("loiThoai", "")) for c in canh_list if isinstance(c, dict))

            # Tu dong bo sung neu hoi duoi 250 tu
            if so_tu_hoi < 250:
                print(
                    f"[Tang 2] Hoi {khung['soHoi']} moi co {so_tu_hoi} tu (<250), tu dong goi Gemini bo sung 4-5 canh..."
                )
                bo_sung = gemini.tao_json(
                    prompt=tao_prompt_bo_sung_hoi(
                        blueprint=blueprint,
                        thong_tin_hoi=thong_tin_hoi,
                        canh_hien_co=canh_list,
                        so_tu_hien_tai=so_tu_hoi,
                    ),
                    system_instruction=SYSTEM_BIEN_KICH,
                    nhiet_do=0.75,
                    max_output_tokens=4096,
                )
                canh_them = bo_sung.get("canhBoSung") if isinstance(bo_sung.get("canhBoSung"), list) else []
                if canh_them:
                    if len(canh_list) >= 2:
                        canh_list = canh_list[:-1] + canh_them + canh_list[-1:]
                    else:
                        canh_list = canh_list + canh_them
                    du_lieu_hoi["canh"] = canh_list

            # Sanitize so bo truoc khi luu cache hoi
            canh_hoi_sach = []
            for idx_c, c_raw in enumerate(du_lieu_hoi.get("canh") or [], start=1):
                if not isinstance(c_raw, dict):
                    continue
                c_clean, _ = chuan_hoa_canh(
                    c_raw,
                    canh_id=f"h{khung['soHoi']}_c{idx_c:02d}",
                    danh_sach_nv_ids=nv_ids,
                    boi_canh_mac_dinh=thong_tin_hoi["boiCanhChinh"],
                    thoi_tiet_mac_dinh=thong_tin_hoi["thoiTietChinh"],
                )
                canh_hoi_sach.append(c_clean)

            # Dam bao canh dau tien cua hoi 1 la mo_dau va canh cuoi hoi 6 la ket_thuc
            if khung["soHoi"] == 1 and canh_hoi_sach:
                canh_hoi_sach[0]["boCuc"] = "mo_dau"
                canh_hoi_sach[0]["chuyenCanh"] = "vong_tron_hoat_hinh"
            if khung["soHoi"] == 6 and canh_hoi_sach:
                canh_hoi_sach[-1]["boCuc"] = "ket_thuc"

            du_lieu_hoi = {
                "id": khung["id"],
                "tenChuong": thong_tin_hoi["tenChuong"],
                "tomTatKetHoi": str(du_lieu_hoi.get("tomTatKetHoi") or thong_tin_hoi["tomTat"]).strip(),
                "canh": canh_hoi_sach,
            }
            file_cache_hoi.write_text(
                json.dumps(du_lieu_hoi, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        tom_tat_hoi_truoc = str(du_lieu_hoi.get("tomTatKetHoi") or thong_tin_hoi["tomTat"])
        danh_sach_chuong_raw.append(du_lieu_hoi)

    # --- TANG 3: HAU KIEM TOAN HOC & XUAT BAN DOC DUYET ---
    raw_tong = {
        "tieuDe": blueprint["tieuDe"],
        "chuDe": blueprint["chuDe"],
        "batSfx": False,
        "batPhuDe": True,
        "bangMau": blueprint["bangMau"],
        "danhSachNhanVat": blueprint["danhSachNhanVat"],
        "chuong": danh_sach_chuong_raw,
    }
    kich_ban_sach, canh_bao_latex = chuan_hoa_toan_bo_kich_ban(raw_tong)

    file_json = base_dir / "nhap_kich_ban.json"
    file_md = base_dir / "doc_duyet_kich_ban.md"
    file_json.write_text(json.dumps(kich_ban_sach, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    file_md.write_text(tao_markdown_doc_duyet(kich_ban_sach, canh_bao_latex), encoding="utf-8")

    tong_tu = sum(
        dem_tu(c.get("loiThoai", ""))
        for ch in kich_ban_sach["chuong"]
        for c in ch["canh"]
    )
    tong_frames = max(
        (c["denFrame"] for ch in kich_ban_sach["chuong"] for c in ch["canh"]),
        default=0,
    )
    print(f"[Tang 3] Da xuat nhap kich ban: {file_json}")
    print(f"[Tang 3] Da xuat ban doc duyet: {file_md}")
    print(
        f"[Thong ke] {len(kich_ban_sach['chuong'])} hoi | {tong_tu} tu | du kien ~{tong_frames / 30 / 60:.2f} phut ({tong_frames} frames)"
    )
    if canh_bao_latex:
        print(f"[Canh bao LaTeX] Phat hien {len(canh_bao_latex)} luu y (xem trong {file_md.name}).")
    return file_json, file_md, kich_ban_sach


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI bien kich phim hoat hinh ke chuyen lich su Toan hoc >10 phut (3 tang)."
    )
    parser.add_argument("--chu-de", required=True, help="Chu de cau chuyen Toan hoc.")
    parser.add_argument(
        "--muc-tieu-phut",
        type=float,
        default=11.0,
        help="Thoi luong muc tieu tinh bang phut (mac dinh 11, luon >= 10.5).",
    )
    parser.add_argument(
        "--slug",
        default="",
        help="Ten thu muc luu du_lieu/<slug>/ (tu dong tao tu chu de neu de trong).",
    )
    parser.add_argument(
        "--giong-ke",
        default="di_dom_gan_gui",
        help="Phong cach ke chuyen (mac dinh: di_dom_gan_gui).",
    )
    parser.add_argument(
        "--bo-cache",
        action="store_true",
        help="Bo qua cache_chuong va sinh lai toan bo 6 hoi.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    slug = args.slug.strip() or tao_slug(args.chu_de)
    bien_kich_3_tang(
        chu_de=args.chu_de,
        slug=slug,
        muc_tieu_phut=args.muc_tieu_phut,
        giong_ke=args.giong_ke,
        bo_cache=args.bo_cache,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
