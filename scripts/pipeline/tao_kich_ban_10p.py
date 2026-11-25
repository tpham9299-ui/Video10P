# -*- coding: utf-8 -*-
"""AI bien kich phim hoat hinh ke chuyen lich su Toan hoc dai >10 phut (kien truc 3 tang)."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

# Cho phep chay truc tiep: python -X utf8 scripts/pipeline/tao_kich_ban_10p.py
GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.bo_nho_hoc_hoi import (
    DUONG_DAN_BO_NHO_MAC_DINH,
    luu_bo_nho,
    tai_bo_nho,
    tao_ngu_canh_hoc_hoi,
    them_bai_hoc,
)
from scripts.pipeline.gemini_client import GeminiClient, tai_env

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
    "ban_do_hanh_trinh",
    "bao_chi_co",
    "phan_ung_cam",
    "ket_thuc",
)

TAM_TRANG_NHAC: tuple[str, ...] = (
    "vui_tuoi",
    "bi_an",
    "kich_tinh",
    "tram_lang",
)

PHUONG_TIEN_HANH_TRINH: tuple[str, ...] = (
    "tau_thuy",
    "thu_tay",
    "nguoi_di_bo",
    "xe_ngua",
)

KIEU_PHAN_UNG_CAM: tuple[str, ...] = (
    "nhap_tra",
    "nhuong_may",
    "tron_mat",
    "can_loi",
)

ID_MASCOT_KENH = "mascot_pi"
MASCOT_KENH_MAC_DINH: dict[str, Any] = {
    "id": ID_MASCOT_KENH,
    "ten": "Giáo Sư Pi",
    "mauThan": "#1A1A1A",
    "mauChuDao": "#0284C7",
    "mauDa": "#FFFDF7",
    "phuKien": "kinh_tron",
    "doTuoi": "truong_thanh",
    "trangPhuc": "ao_choang_hoc_gia",
    "kieuToc": "mu_noi",
    "coRau": "khong",
    "mauAo": "#0284C7",
}

LOAI_BOI_CANH: tuple[str, ...] = (
    "bo_bien_hy_lap",
    "vuon_tao_dong_que",
    "pho_co_chau_au",
    "rung_nui_thien_nhien",
    "thu_vien_co_dien",
    "lop_hoc_bang_xanh",
    "bau_troi_dem_vu_tru",
    "phong_nen_hai_huoc",
    "quang_truong_hy_lap",
    "thu_vien_trung_co",
    "dai_thien_van_phuc_hung",
    "giang_duong_hien_dai",
    "nha_co_phong_sinh",
    "cang_bien_tau_thuy",
    "phong_tro_bep_lua",
    "phong_benh_vien",
    "duong_pho_xe_co",
    "giang_duong_dai_hoc",
    "san_truong_co_dien",
    "phong_thi_nghiem_co",
    "khong_gian_vu_tru_toan",
    "lang_que_an_do_a_dong",
)

LOAI_VAT_THE_XUNG_QUANH: tuple[str, ...] = (
    "chim_hai_au",
    "chim_san_truong",
    "ca_gon_song",
    "buom_vuon",
    "hoi_khoi",
    "ngon_nen_den_dau",
    "la_vang_gio",
    "tuyet_cua_so",
    "xe_taxi_co",
    "dong_ho_qua_lac",
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
    "trao_thu",
    "chi_bang_giang_bai",
    "quay_nhin_doi_thoai",
    "bat_tay",
    "giat_minh_bat_day",
    "quay_nhin_khan_gia",
)

GOC_QUAY_CAMERA: tuple[str, ...] = (
    "toan_canh",
    "trung_canh",
    "can_mat",
    "can_mat_trai",
    "can_mat_phai",
    "can_mat_kich_tinh",
    "dao_goc_can_mat",
    "focus_trai",
    "focus_phai",
    "zoom_dao_cu",
    "pan_ngang",
    "chia_doi_man_hinh",
)

LOAI_TRANG_PHUC: tuple[str, ...] = (
    "ao_vest_co_dien",
    "ao_choang_hoc_gia",
    "ao_co_an_do",
    "ao_len_mua_dong",
    "ao_choang_hy_lap",
    "quan_phuc_co",
    "thuong_dan",
)

LOAI_KIEU_TOC: tuple[str, ...] = (
    "gon_gang",
    "xoan_co_dien",
    "toc_bac_dai",
    "khan_quan",
    "mu_rong_vanh",
    "mu_noi",
    "hoi_hoi",
)

LOAI_CO_RAU: tuple[str, ...] = (
    "khong",
    "ria_mep",
    "rau_quai_non",
    "rau_bac_dai",
)

TAM_KHUNG_NHAN_VAT: tuple[str, ...] = (
    "toan_canh",
    "ban_than",
    "can_mat",
)

KIEU_BONG_BONG_CHAT: tuple[str, ...] = (
    "thuong",
    "quat_thao",
    "suy_nghi",
    "ca_khia",
)

LOAI_KHUNG_HINH_AI: tuple[str, ...] = (
    "boi_canh",
    "can_canh_vat_the",
)

LOAI_ANH_SANG_MOI_TRUONG: tuple[str, ...] = (
    "nang_am",
    "anh_nen",
    "dem_lanh",
    "trung_tinh",
    "hoang_hon",
)

LOAI_CANH: tuple[str, ...] = (
    "ke_chuyen",
    "doi_thoai",
    "tuong_tac_khan_gia",
    "giang_toan",
    "chuyen_canh_lich_su",
)

DO_TUOI_NHAN_VAT: tuple[str, ...] = (
    "so_sinh",
    "thieu_nien",
    "truong_thanh",
    "gia",
)

TU_THE_NHAN_VAT: tuple[str, ...] = (
    "dung",
    "ngoi_ban",
    "nam_giuong",
    "om_em_be",
    "mac_ao_khoac",
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
    "mo_hoi_lon",
    "khoi_boc_tai",
    "mat_xoan_oc",
    "cham_hoi_nay",
    "tia_toc_do",
    "bong_den_y_tuong",
)

LOAI_MINH_HOA_TOAN: tuple[str, ...] = (
    "tam_giac_vuong",
    "truc_so_vo_ti",
    "do_thi_ham_so",
    "hinh_hoc_chung_minh",
    "chuoi_suy_luan",
    "tung_buoc",
    "so_do_anh_xa",
    "luoi_duong_cheo",
    "bieu_do_cot",
)

BOI_CANH_TRONG_NHA: frozenset[str] = frozenset(
    {
        "thu_vien_co_dien",
        "lop_hoc_bang_xanh",
        "thu_vien_trung_co",
        "dai_thien_van_phuc_hung",
        "giang_duong_hien_dai",
        "nha_co_phong_sinh",
        "phong_tro_bep_lua",
        "phong_benh_vien",
        "giang_duong_dai_hoc",
        "phong_thi_nghiem_co",
        "phong_nen_hai_huoc",
    }
)

BOI_CANH_VU_TRU: frozenset[str] = frozenset(
    {
        "khong_gian_vu_tru_toan",
        "bau_troi_dem_vu_tru",
    }
)

VAT_THE_NGOAI_TROI_CAM_TRONG_NHA: frozenset[str] = frozenset(
    {
        "la_vang_gio",
        "chim_hai_au",
        "chim_san_truong",
        "ca_gon_song",
        "buom_vuon",
        "xe_taxi_co",
    }
)

VAT_THE_CAM_TRONG_VU_TRU: frozenset[str] = frozenset(
    {
        "ngon_nen_den_dau",
        "la_vang_gio",
        "chim_hai_au",
        "chim_san_truong",
        "ca_gon_song",
        "buom_vuon",
        "xe_taxi_co",
        "tuyet_cua_so",
        "hoi_khoi",
    }
)

BOI_CANH_CO_CUA_SO_TUYET: frozenset[str] = frozenset(
    {
        "phong_benh_vien",
        "phong_tro_bep_lua",
        "nha_co_phong_sinh",
        "thu_vien_co_dien",
        "giang_duong_dai_hoc",
        "phong_thi_nghiem_co",
    }
)

_TU_KHOA_NGUOI_GIA_GIAI_THUONG: tuple[str, ...] = (
    "giải thưởng",
    "huy chương",
    "vinh danh",
    "trao giải",
    "cuối đời",
    "qua đời",
    "tuổi già",
    "lúc về già",
    "viện hàn lâm",
    "giáo sư già",
    "bệnh viện tâm thần",
    "người già",
    "giai thuong",
    "huy chuong",
    "cuoi doi",
    "tuoi gia",
)

LOAI_BUOC_VE_TOAN: tuple[str, ...] = (
    "diem",
    "doan_thang",
    "cung_tron",
    "da_giac",
    "truc_toa_do",
    "duong_cong",
    "nhan_chu",
)

LOAI_HAM_DO_THI: tuple[str, ...] = (
    "parabol",
    "sin",
    "cos",
    "bac_ba",
    "mu",
    "tuyen_tinh",
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
    "compa_co",
    "ban_tinh_co",
    "khoi_da_dien",
    "kinh_thien_van",
    "noi_em_be",
    "noi_sup",
    "phong_bi_thu_tay",
    "giuong_benh",
    "bien_so_xe",
    "tach_tra_nong",
    "tau_thuy",
    "ban_hoc_den_dau",
    "qua_dia_cau",
)

HUONG_NHAN_VAT: tuple[str, ...] = ("trai", "phai")

LOAI_VAI_NOI: tuple[str, ...] = (
    "nguoi_dan",
    "nhan_vat",
    "binh_luan_hai",
)

NGUONG_NHIP_THI_GIAC_CANH_BAO_GIAY = 6.5
NGUONG_NHIP_THI_GIAC_TACH_CANH_GIAY = 8.0

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
        "tamTrangNhacMacDinh": "bi_an",
        "vaiTro": "Cold Open 15 giây đầu gây sốc tò mò (Mascot kênh) & Nhập cuộc câu chuyện",
        "phutMucTieu": 1.6,
        "tuToiThieu": 250,
        "tuMucTieu": "280-330",
        "soCanh": "16-19",
        "yeuCauDacBiet": (
            "BẮT BUỘC mở màn bằng COLD OPEN 15 GIÂY ĐẦU (2-3 cảnh đầu tiên, tổng 40-58 từ) có Mascot kênh (`mascot_pi`) "
            "đi thẳng vào nghịch lý Toán học gây sốc, ẩn dụ hiện đại hài hước hoặc tình huống dở khóc dở cười "
            "trước khi quay lại kể diễn biến lịch sử. "
            "CẤM TUYỆT ĐỐI mở bài kiểu tiểu sử sách giáo khoa ('X sinh năm ... tại ...') hay chào hỏi "
            "'Xin chào các bạn', xin like/subscribe. "
            "Cuối hồi BẮT BUỘC có câu móc nối Open Loop (`openLoopCuoiHoi`) khiến người xem muốn xem tiếp Hồi 2. "
            "Cảnh đầu tiên bắt buộc dùng boCuc='mo_dau' và chuyenCanh='vong_tron_hoat_hinh'."
        ),
    },
    {
        "soHoi": 2,
        "id": "chuong_2",
        "tamTrangNhacMacDinh": "vui_tuoi",
        "vaiTro": "Nhân vật, Rắc rối thời đại & Hành trình đầu tiên",
        "phutMucTieu": 2.0,
        "tuToiThieu": 280,
        "tuMucTieu": "300-360",
        "soCanh": "16-22",
        "yeuCauDacBiet": (
            "Giới thiệu nhân vật chính với tính cách đời thường dí dỏm (dùng ẩn dụ hiện đại hài hước), kèm bài toán hóc búa. "
            "Xen kẽ cảnh doi_thoai, dong_thoi_gian, ít nhất 1 cảnh `ban_do_hanh_trinh` (hoặc `bao_chi_co`) và 1 cảnh `phan_ung_cam` 1.5-2.5s. "
            "Chèn 1 câu đố `tuong_tac_khan_gia` do Mascot kênh (`mascot_pi`) dẫn dắt và khép hồi bằng câu móc nối Open Loop sang Hồi 3."
        ),
    },
    {
        "soHoi": 3,
        "id": "chuong_3",
        "tamTrangNhacMacDinh": "bi_an",
        "vaiTro": "Khoảnh khắc 'Ơ-rê-ca!' & Giải mã Toán học phần 1",
        "phutMucTieu": 2.0,
        "tuToiThieu": 280,
        "tuMucTieu": "310-360",
        "soCanh": "16-22",
        "yeuCauDacBiet": (
            "Khai thác ý tưởng đột phá bằng ẩn dụ hiện đại cực dễ hiểu. BẮT BUỘC có tối thiểu 2 cảnh boCuc='giai_thich_toan' "
            "dùng boiCanh='lop_hoc_bang_xanh', có congThucLatex rõ ràng và minhHoaToan trực quan "
            "(ưu tiên so_do_anh_xa, luoi_duong_cheo, bieu_do_cot, do_thi_ham_so, tam_giac_vuong, truc_so_vo_ti). "
            "Khép hồi bằng câu móc nối Open Loop sang Hồi 4."
        ),
    },
    {
        "soHoi": 4,
        "id": "chuong_4",
        "tamTrangNhacMacDinh": "kich_tinh",
        "vaiTro": "Bước ngoặt chấn động, Drama học thuật & Tình huống dở khóc dở cười",
        "phutMucTieu": 2.0,
        "tuToiThieu": 280,
        "tuMucTieu": "300-360",
        "soCanh": "16-22",
        "yeuCauDacBiet": (
            "Giai thoại thật thú vị, phản ứng 'cạn lời' của người đương thời. "
            "BẮT BUỘC có ít nhất 1 cảnh `bao_chi_co` (tờ báo giật gân xoay vào màn hình), 1 cảnh `phan_ung_cam` (1.5-2.5s nhấp trà/nhướng mày/trợn mắt), "
            "1 cảnh đánh dấu `ngatNhacPunchline: true` trước câu punchline hài đắt giá, và 1 cảnh `tuong_tac_khan_gia` do Mascot kênh dẫn. "
            "Khép hồi bằng câu móc nối Open Loop sang Hồi 5."
        ),
    },
    {
        "soHoi": 5,
        "id": "chuong_5",
        "tamTrangNhacMacDinh": "vui_tuoi",
        "vaiTro": "Chiều sâu Toán học & Thế giới hiện đại",
        "phutMucTieu": 2.0,
        "tuToiThieu": 280,
        "tuMucTieu": "300-360",
        "soCanh": "16-22",
        "yeuCauDacBiet": (
            "Mở rộng bản chất định lý (thêm ít nhất 1 cảnh boCuc='giai_thich_toan' có congThucLatex & minhHoaToan trực quan), "
            "dùng ẩn dụ hiện đại hài hước kết nối với GPS, Wi-Fi, điện thoại, trò chơi hay thiên văn ngày nay. "
            "Có thể xen 1 cảnh `ban_do_hanh_trinh` hoặc `phan_ung_cam` và khép hồi bằng Open Loop sang Hồi 6."
        ),
    },
    {
        "soHoi": 6,
        "id": "chuong_6",
        "tamTrangNhacMacDinh": "tram_lang",
        "vaiTro": "Dư âm câu chuyện, Cái kết dí dỏm & End-Screen 15 giây (Mascot)",
        "phutMucTieu": 1.6,
        "tuToiThieu": 250,
        "tuMucTieu": "280-330",
        "soCanh": "16-19",
        "yeuCauDacBiet": (
            "Khép lại vòng cung câu chuyện trên bối cảnh hoang_hon hoặc bau_troi_dem_vu_tru + ban_dem, "
            "đọng lại 3 ý chính + 1 câu kết có duyên. "
            "Cảnh cuối cùng BẮT BUỘC dùng boCuc='ket_thuc' (~15 giây cuối) có Mascot kênh (`mascot_pi`) và trường `endScreen` "
            "mời khán giả bấm chọn 1 trong 2 video gợi ý ở khung trái/phải."
        ),
    },
]

TONG_TU_TOI_THIEU = 1750
TONG_TU_TOI_DA = 2150

SYSTEM_BIEN_KICH = (
    "Bạn đảm nhiệm 2 vai chuyên môn song song cho phim hoạt hình 2D kể chuyện lịch sử Toán học "
    "phong cách Kurzgesagt kết hợp Oversimplified bản tiếng Việt: "
    "(1) BIÊN KỊCH KỂ CHUYỆN: kể chuyện cuốn hút, đối thoại nhân vật sống động có cá tính, "
    "tương tác khán giả tự nhiên, hài hước dí dỏm vừa đủ duyên (không lố, không bạo lực), "
    "chống lặp ý giữa các hồi, kiến thức Toán học chính xác 100%, "
    "BẮT BUỘC 100% văn bản tiếng Việt hiển thị (tiêu đề, phụ đề hồi, lời thoại, lượt thoại, minh họa Toán, gợi ý) "
    "phải CÓ DẤU ĐẦY ĐỦ và đúng chính tả, TUYỆT ĐỐI CẤM viết tiếng Việt không dấu; "
    "(2) ĐẠO DIỄN STORYBOARD: khớp boiCanh/doTuoi/tuThe/daoCu/vatTheXungQuanh 1-1 theo từng tình tiết "
    "câu chuyện, dàn dựng đa dạng gocQuay máy quay điện ảnh và bieuCamTheoMoc theo diễn biến cảm xúc. "
    "Trả về DUY NHẤT JSON hợp lệ, không giải thích thừa."
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


def cat_gon_theo_tu(van_ban: str, gioi_han: int) -> str:
    """
    Cat gon chuoi trong gioi han ky tu theo dung ranh gioi tu / dau cau,
    TUYET DOI KHONG cat cut giua tu (nhu '...Leopol', '...một sự công').
    """
    sach = re.sub(r"\s+", " ", str(van_ban or "").strip())
    if not sach or gioi_han <= 0 or len(sach) <= gioi_han:
        return sach
    cat = sach[:gioi_han]
    # Tim khoang trang cuoi cung de khong bao gio cat giua tu
    vi_tri_cach = cat.rfind(" ")
    if vi_tri_cach >= max(8, int(gioi_han * 0.45)):
        cat = cat[:vi_tri_cach]
    return cat.rstrip(" ,;:-—–(")


_PAT_KY_TU_DAU_VIET = re.compile(
    r"[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
    r"ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]"
)

# Tap tu vung tieng Viet khong dau dac trung (hau nhu chac chan phai co dau trong tieng Viet chuan)
_TU_VIET_BAT_BUOC_CO_DAU: frozenset[str] = frozenset(
    {
        "khong", "duoc", "nguoi", "chuyen", "nhung", "truong", "phuong", "luong",
        "nhieu", "thuong", "cuoc", "buoc", "nuoc", "tuyet", "nghich", "dinh",
        "chinh", "gioi", "thoi", "giai", "thoai", "biet", "thua", "luy", "cuc",
        "toan", "hoc", "lich", "su", "phat", "minh", "cong", "thuc", "chung",
        "tap", "hop", "nhien", "thuc", "cau", "hoi", "dap", "ngoai", "phong",
        "canh", "gian", "giay", "phut", "chuong", "trinh", "tuong", "tac",
        "khan", "gia", "phan", "tich", "suy", "luan", "duong", "cheo", "bang",
        "ket", "thuc", "dau", "hai", "huoc", "dom", "tinh", "huong", "nhan",
        "vat", "doi", "tuoi", "benh", "vien", "thu", "tru", "gay", "gat",
        "that", "tiet", "khac", "nhau", "nhat", "dang", "tranh", "anh", "mot",
        "cac", "ban", "bat", "ngo", "cua", "trong", "voi", "nhu", "the", "hien",
        "dai", "nay", "khi", "sao", "neu", "thi", "vao", "len", "xuong", "den",
        "cung", "hoac", "theo", "giua", "tren", "duoi", "truoc", "trai", "phai",
        "ngay", "dem", "sang", "toi", "dien", "thoai", "chieu", "sau", "ngo",
        "ngac", "nhien", "tuong", "trung", "vuong", "goc", "canh", "song",
        "dong", "bien", "thuyen", "nha", "sinh", "gia", "giai", "thuong",
        "chua", "phai", "nhin", "nghe", "noi", "viet", "doc", "tinh", "so",
        "lon", "nho", "hon", "kem", "rat", "qua", "lam", "viec", "cuoi",
    }
)

# Tap tu bat buoc phai co dau ngay ca khi chuoi co 1-2 dau lac (tranh false positive voi tu tieng Anh/ten rieng)
_TU_VIET_CHAC_CHAN_THIEU_DAU: frozenset[str] = frozenset(
    {
        "khong", "duoc", "nguoi", "chuyen", "nhung", "truong", "phuong", "luong",
        "nhieu", "thuong", "cuoc", "buoc", "nuoc", "tuyet", "nghich", "dinh",
        "chinh", "gioi", "thoi", "giai", "thoai", "biet", "thua", "luy", "cuc",
        "toan", "chung", "nhien", "ngoai", "phong", "canh", "giay", "phut",
        "chuong", "trinh", "tuong", "khan", "phan", "tich", "luan", "duong",
        "cheo", "huoc", "huong", "nhan", "tuoi", "benh", "vien", "tranh",
        "khac", "nhau", "nhat", "cua", "trong", "hien", "xuong", "hoac",
        "giua", "tren", "duoi", "truoc", "trai", "phai", "ngay", "chieu",
        "ngac", "vuong", "thuyen", "thuong", "chua", "viec", "cuoi", "cac",
    }
)


def _la_chuoi_tieng_viet_thieu_dau(van_ban: str, do_dai_toi_thieu: int = 20) -> bool:
    """
    Phat hien chuoi tieng Viet dai >= 20 ky tu bi viet KHONG DAU (hoac thieu dau nghiem trong).
    Bo qua URL, ma LaTeX thuan, hoac chuoi tieng Anh thuan.
    """
    sach = re.sub(r"\s+", " ", str(van_ban or "").strip())
    if len(sach) < do_dai_toi_thieu:
        return False
    if sach.startswith(("http://", "https://")):
        return False

    # Bo cac lenh LaTeX (\frac, \sqrt, ...) va ky hieu toan de chi xet phan chu tu nhien
    phan_chu = re.sub(r"\\[a-zA-Z]+", " ", sach)
    phan_chu = re.sub(r"https?://\S+", " ", phan_chu)
    tu_list = re.findall(r"[A-Za-zÀ-ỹđĐ]+", phan_chu, flags=re.UNICODE)
    if len(tu_list) < 3:
        return False

    so_ky_tu_dau = len(_PAT_KY_TU_DAU_VIET.findall(phan_chu))
    tu_thuong = [t.lower() for t in tu_list]
    so_tu_khong_dau_viet = sum(1 for t in tu_thuong if t in _TU_VIET_BAT_BUOC_CO_DAU)
    so_tu_chac_chan_thieu = sum(1 for t in tu_thuong if t in _TU_VIET_CHAC_CHAN_THIEU_DAU)

    # Truong hop 1: Hoan toan khong co ky tu dau tieng Viet nao va co >= 2 tu tieng Viet khong dau
    if so_ky_tu_dau == 0:
        if so_tu_chac_chan_thieu >= 1 and so_tu_khong_dau_viet >= 2:
            return True
        if so_tu_khong_dau_viet >= 3:
            return True
        return False

    # Truong hop 2: Co rat it dau (<= 1 dau) nhung nhieu tu chac chan thieu dau (>= 3 tu)
    if so_ky_tu_dau <= 1 and so_tu_chac_chan_thieu >= 3:
        return True

    # Truong hop 3: Chuoi dai co mat do tu chac chan thieu dau cao (>= 4 tu va >= 30% tong so tu)
    if so_tu_chac_chan_thieu >= 4 and (so_tu_chac_chan_thieu / max(1, len(tu_thuong))) >= 0.30:
        return True

    return False


def _duyet_chuoi_hien_thi_kich_ban(kich_ban: dict[str, Any]) -> list[tuple[str, str, str, str]]:
    """
    Thu thap tat ca (duong_dan, canh_id, ten_truong, gia_tri) cho cac truong van ban hien thi:
    tieuDe, chuDe, goiY, goiYThumbnail, tenChuong, phuDeHoi, tieuDeNho, loiThoai,
    luotThoai[].noiDung, bongBongThoai, loiBinhHaiHuoc.noiDung, mocThoiGian[].moTa,
    minhHoaToan, congThucLatex[].nhan, cauHoiTuongTac.
    """
    ket_qua: list[tuple[str, str, str, str]] = []

    def _them(duong_dan: str, canh_id: str, truong: str, val: Any) -> None:
        if isinstance(val, str) and val.strip():
            ket_qua.append((duong_dan, canh_id, truong, val.strip()))

    _them("tieuDe", "", "tieuDe", kich_ban.get("tieuDe"))
    _them("chuDe", "", "chuDe", kich_ban.get("chuDe"))
    if isinstance(kich_ban.get("goiY"), str):
        _them("goiY", "", "goiY", kich_ban.get("goiY"))
    elif isinstance(kich_ban.get("goiY"), list):
        for gi, g in enumerate(kich_ban["goiY"]):
            _them(f"goiY[{gi}]", "", "goiY", g)

    for ti, th in enumerate(kich_ban.get("goiYThumbnail") or []):
        if isinstance(th, dict):
            _them(f"goiYThumbnail[{ti}].tieuDeLon", "", "goiYThumbnail.tieuDeLon", th.get("tieuDeLon"))
            _them(f"goiYThumbnail[{ti}].nhanPhu", "", "goiYThumbnail.nhanPhu", th.get("nhanPhu"))

    for ci, ch in enumerate(kich_ban.get("chuong") or []):
        if not isinstance(ch, dict):
            continue
        _them(f"chuong[{ci}].tenChuong", "", "tenChuong", ch.get("tenChuong"))
        _them(f"chuong[{ci}].phuDeHoi", "", "phuDeHoi", ch.get("phuDeHoi"))
        _them(f"chuong[{ci}].openLoopCuoiHoi", "", "openLoopCuoiHoi", ch.get("openLoopCuoiHoi"))
        for ki, canh in enumerate(ch.get("canh") or []):
            if not isinstance(canh, dict):
                continue
            cid = str(canh.get("id") or f"canh_{ki + 1:03d}")
            base = f"chuong[{ci}].canh[{ki}]"
            _them(f"{base}.tieuDeNho", cid, "tieuDeNho", canh.get("tieuDeNho"))
            _them(f"{base}.phuDeHoi", cid, "phuDeHoi", canh.get("phuDeHoi"))
            _them(f"{base}.loiThoai", cid, "loiThoai", canh.get("loiThoai"))
            if isinstance(canh.get("goiY"), str):
                _them(f"{base}.goiY", cid, "goiY", canh.get("goiY"))
            elif isinstance(canh.get("goiY"), list):
                for gi, g in enumerate(canh["goiY"]):
                    _them(f"{base}.goiY[{gi}]", cid, "goiY", g)

            for li, lt in enumerate(canh.get("luotThoai") or []):
                if isinstance(lt, dict):
                    _them(f"{base}.luotThoai[{li}].noiDung", cid, "luotThoai", lt.get("noiDung"))

            for ni, nv in enumerate(canh.get("nhanVat") or []):
                if isinstance(nv, dict):
                    _them(f"{base}.nhanVat[{ni}].bongBongThoai", cid, "bongBongThoai", nv.get("bongBongThoai"))

            if isinstance(canh.get("loiBinhHaiHuoc"), dict):
                _them(f"{base}.loiBinhHaiHuoc.noiDung", cid, "loiBinhHaiHuoc", canh["loiBinhHaiHuoc"].get("noiDung"))

            for mi, moc in enumerate(canh.get("mocThoiGian") or []):
                if isinstance(moc, dict):
                    _them(f"{base}.mocThoiGian[{mi}].moTa", cid, "mocThoiGian", moc.get("moTa"))

            for cti, ct in enumerate(canh.get("congThucLatex") or []):
                if isinstance(ct, dict):
                    _them(f"{base}.congThucLatex[{cti}].nhan", cid, "congThucLatex.nhan", ct.get("nhan"))

            mh = canh.get("minhHoaToan")
            if isinstance(mh, dict):
                _them(f"{base}.minhHoaToan.tieuDe", cid, "minhHoaToan.tieuDe", mh.get("tieuDe"))
                _them(f"{base}.minhHoaToan.chuThichCuoi", cid, "minhHoaToan.chuThichCuoi", mh.get("chuThichCuoi"))
                ts = mh.get("thamSo")
                if isinstance(ts, dict):
                    for tk, tv in ts.items():
                        if tk in ("ham", "mauDuong", "mauNhanManh", "heToaDo"):
                            continue
                        if isinstance(tv, str):
                            _them(f"{base}.minhHoaToan.thamSo.{tk}", cid, "minhHoaToan", tv)
                        elif isinstance(tv, list):
                            for tvi, tval in enumerate(tv):
                                if isinstance(tval, str):
                                    _them(f"{base}.minhHoaToan.thamSo.{tk}[{tvi}]", cid, "minhHoaToan", tval)
                for bvi, bv in enumerate(mh.get("buocVe") or []):
                    if isinstance(bv, dict):
                        _them(f"{base}.minhHoaToan.buocVe[{bvi}].nhan", cid, "minhHoaToan", bv.get("nhan"))
                        _them(f"{base}.minhHoaToan.buocVe[{bvi}].noiDung", cid, "minhHoaToan", bv.get("noiDung"))

            chtt = canh.get("cauHoiTuongTac")
            if isinstance(chtt, dict):
                _them(f"{base}.cauHoiTuongTac.cauHoi", cid, "cauHoiTuongTac", chtt.get("cauHoi"))
                _them(f"{base}.cauHoiTuongTac.dapAn", cid, "cauHoiTuongTac", chtt.get("dapAn"))
                _them(f"{base}.cauHoiTuongTac.giaiThichNgan", cid, "cauHoiTuongTac", chtt.get("giaiThichNgan"))
                for lci, lc in enumerate(chtt.get("luaChon") or []):
                    _them(f"{base}.cauHoiTuongTac.luaChon[{lci}]", cid, "cauHoiTuongTac", lc)

            for hui, hu in enumerate(canh.get("hieuUngHoatHinh") or []):
                if isinstance(hu, dict):
                    _them(f"{base}.hieuUngHoatHinh[{hui}].chuHienThi", cid, "hieuUngHoatHinh", hu.get("chuHienThi"))

            # Truong v3.5: banDoHanhTrinh, baoChiCo, phanUngCam, endScreen
            bd = canh.get("banDoHanhTrinh")
            if isinstance(bd, dict):
                _them(f"{base}.banDoHanhTrinh.diemDi", cid, "banDoHanhTrinh", bd.get("diemDi"))
                _them(f"{base}.banDoHanhTrinh.diemDen", cid, "banDoHanhTrinh", bd.get("diemDen"))
                _them(f"{base}.banDoHanhTrinh.moTaHanhTrinh", cid, "banDoHanhTrinh", bd.get("moTaHanhTrinh"))
                _them(f"{base}.banDoHanhTrinh.diemDungGiua", cid, "banDoHanhTrinh", bd.get("diemDungGiua"))

            bc = canh.get("baoChiCo")
            if isinstance(bc, dict):
                _them(f"{base}.baoChiCo.tenToBao", cid, "baoChiCo", bc.get("tenToBao"))
                _them(f"{base}.baoChiCo.tieuDeBao", cid, "baoChiCo", bc.get("tieuDeBao"))
                _them(f"{base}.baoChiCo.tieuDePhu", cid, "baoChiCo", bc.get("tieuDePhu"))
                _them(f"{base}.baoChiCo.nhanAnhMinhHoa", cid, "baoChiCo", bc.get("nhanAnhMinhHoa"))

            pu = canh.get("phanUngCam")
            if isinstance(pu, dict):
                _them(f"{base}.phanUngCam.chuHieuUng", cid, "phanUngCam", pu.get("chuHieuUng"))

            es = canh.get("endScreen")
            if isinstance(es, dict):
                _them(f"{base}.endScreen.khungTraiNhan", cid, "endScreen", es.get("khungTraiNhan"))
                _them(f"{base}.endScreen.khungPhaiNhan", cid, "endScreen", es.get("khungPhaiNhan"))
                _them(f"{base}.endScreen.loiDanXemTiep", cid, "endScreen", es.get("loiDanXemTiep"))

    return ket_qua


def kiem_tra_dau_tieng_viet(
    kich_ban: dict[str, Any],
    do_dai_toi_thieu: int = 20,
) -> list[dict[str, Any]]:
    """
    Guardrail phat hien bat ky chuoi tieng Viet nao dai >= 20 ky tu bi thieu dau
    (o tieu de, loi thoai, luotThoai, minhHoaToan, goiY, mocThoiGian, cauHoiTuongTac...).
    """
    vi_pham: list[dict[str, Any]] = []
    for duong_dan, canh_id, truong, gia_tri in _duyet_chuoi_hien_thi_kich_ban(kich_ban):
        if _la_chuoi_tieng_viet_thieu_dau(gia_tri, do_dai_toi_thieu=do_dai_toi_thieu):
            vi_pham.append(
                {
                    "loai": "tieng_viet_khong_dau",
                    "duongDan": duong_dan,
                    "canhId": canh_id,
                    "truong": truong,
                    "giaTri": gia_tri,
                    "moTa": f"[{canh_id or duong_dan}] Phát hiện chuỗi tiếng Việt thiếu dấu ở '{truong}': \"{cat_gon_theo_tu(gia_tri, 70)}\"",
                }
            )
    return vi_pham


def _gan_gia_tri_theo_duong_dan(goc: Any, duong_dan: str, gia_tri_moi: str) -> bool:
    """Cap nhat gia tri chuoi trong dict/list theo duong dan kieu 'chuong[0].canh[2].loiThoai'."""
    tokens = re.findall(r"([A-Za-z0-9_]+)|\[(\d+)\]", duong_dan)
    if not tokens:
        return False
    cur = goc
    for idx, (khoa, chi_so_str) in enumerate(tokens):
        la_cuoi = idx == len(tokens) - 1
        if khoa:
            if not isinstance(cur, dict) or khoa not in cur:
                return False
            if la_cuoi:
                cur[khoa] = gia_tri_moi
                return True
            cur = cur[khoa]
        else:
            ci = int(chi_so_str)
            if not isinstance(cur, list) or ci < 0 or ci >= len(cur):
                return False
            if la_cuoi:
                cur[ci] = gia_tri_moi
                return True
            cur = cur[ci]
    return False


def tu_dong_sua_dau_tieng_viet(
    kich_ban: dict[str, Any],
    gemini: GeminiClient | None = None,
    do_dai_toi_thieu: int = 20,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """
    Quet toan bo kich ban bang kiem_tra_dau_tieng_viet(); neu phat hien chuoi thieu dau
    va co `gemini`, tu dong goi Gemini khoi phuc 100% dau tieng Viet chuan chinh ta
    truoc khi xuat nhap_kich_ban.json.
    """
    import copy

    ket_qua = copy.deepcopy(kich_ban)
    vi_pham = kiem_tra_dau_tieng_viet(ket_qua, do_dai_toi_thieu=do_dai_toi_thieu)
    if not vi_pham or gemini is None:
        return ket_qua, []

    da_sua: list[dict[str, Any]] = []
    # Xu ly theo lo toi da 30 chuoi/luot de bao dam JSON gon, nhanh, chinh xac
    for bat_dau in range(0, len(vi_pham), 30):
        lo = vi_pham[bat_dau : bat_dau + 30]
        danh_sach_nhap = [
            {"duongDan": vp["duongDan"], "vanBanGoc": vp["giaTri"]}
            for vp in lo
        ]
        prompt = (
            "Hãy khôi phục ĐẦY ĐỦ DẤU TIẾNG VIỆT tự nhiên, chuẩn chính tả cho các chuỗi dưới đây.\n"
            "QUY TẮC BẮT BUỘC:\n"
            "1. Giữ nguyên hoàn toàn tên riêng nước ngoài (Georg Cantor, Leopold Kronecker, Ramanujan, Hardy, Cambridge...), "
            "ký hiệu Toán học, con số và ý nghĩa gốc.\n"
            "2. Không thêm giải thích thừa; trả về DUY NHẤT JSON hợp lệ theo mẫu:\n"
            '{"daSua": [{"duongDan": "...", "vanBanCoDau": "..."}]}\n\n'
            f"DANH SÁCH CẦN SỬA:\n{json.dumps(danh_sach_nhap, ensure_ascii=False, indent=2)}"
        )
        try:
            raw = gemini.tao_json(
                prompt=prompt,
                system_instruction=(
                    "Bạn là biên tập viên chính tả tiếng Việt chuyên sâu cho kịch bản lịch sử Toán học. "
                    "Trả về DUY NHẤT JSON hợp lệ với 100% tiếng Việt có dấu chuẩn xác."
                ),
                nhiet_do=0.15,
                max_output_tokens=8192,
            )
        except Exception:
            continue

        ds_kq = raw.get("daSua") if isinstance(raw, dict) else []
        if not isinstance(ds_kq, list):
            continue
        ban_do_goc = {vp["duongDan"]: vp["giaTri"] for vp in lo}
        for item in ds_kq:
            if not isinstance(item, dict):
                continue
            dd = str(item.get("duongDan") or "").strip()
            moi = re.sub(r"\s+", " ", str(item.get("vanBanCoDau") or "").strip())
            if dd in ban_do_goc and moi and not _la_chuoi_tieng_viet_thieu_dau(moi, do_dai_toi_thieu=do_dai_toi_thieu):
                if _gan_gia_tri_theo_duong_dan(ket_qua, dd, moi):
                    da_sua.append({"duongDan": dd, "cu": ban_do_goc[dd], "moi": moi})

    return ket_qua, da_sua


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

def _chuan_hoa_mang_diem(raw_pts: Any) -> list[list[float]]:
    ket_qua: list[list[float]] = []
    if not isinstance(raw_pts, list):
        return ket_qua
    for pt in raw_pts[:40]:
        if isinstance(pt, (list, tuple)) and len(pt) >= 2:
            x = _ep_so(pt[0], 0.0, -5000, 5000)
            y = _ep_so(pt[1], 0.0, -5000, 5000)
            ket_qua.append([round(x, 3), round(y, 3)])
    return ket_qua


def chuan_hoa_buoc_ve_toan(raw_buoc_ve: Any) -> list[dict[str, Any]]:
    """Sanitize danh sach buocVe mini-DSL cho MinhHoaToan loai='tung_buoc'."""
    if not isinstance(raw_buoc_ve, list):
        return []
    ket_qua: list[dict[str, Any]] = []
    for idx, b in enumerate(raw_buoc_ve[:18]):
        if not isinstance(b, dict):
            continue
        loai = chuan_hoa_enum(b.get("loai"), LOAI_BUOC_VE_TOAN, "")
        if not loai:
            continue
        muc: dict[str, Any] = {"loai": loai}
        if b.get("tuFrame") is not None:
            muc["tuFrame"] = int(_ep_so(b.get("tuFrame"), idx * 16, 0, 600))
        if b.get("thoiLuong") is not None:
            muc["thoiLuong"] = int(_ep_so(b.get("thoiLuong"), 22, 4, 240))
        if b.get("mau"):
            muc["mau"] = _ep_mau_hex(b.get("mau"), "#FEF08A")
        if b.get("nhan"):
            muc["nhan"] = str(b["nhan"]).strip()[:40]

        if loai == "diem":
            muc["x"] = round(_ep_so(b.get("x"), 0.0, -5000, 5000), 3)
            muc["y"] = round(_ep_so(b.get("y"), 0.0, -5000, 5000), 3)
            if b.get("banKinh") is not None:
                muc["banKinh"] = round(_ep_so(b.get("banKinh"), 6.5, 2.0, 24.0), 1)
        elif loai == "doan_thang":
            muc["x1"] = round(_ep_so(b.get("x1"), 0.0, -5000, 5000), 3)
            muc["y1"] = round(_ep_so(b.get("y1"), 0.0, -5000, 5000), 3)
            muc["x2"] = round(_ep_so(b.get("x2"), 1.0, -5000, 5000), 3)
            muc["y2"] = round(_ep_so(b.get("y2"), 1.0, -5000, 5000), 3)
            if b.get("doDay") is not None:
                muc["doDay"] = round(_ep_so(b.get("doDay"), 3.6, 1.0, 12.0), 1)
            if isinstance(b.get("netDut"), bool):
                muc["netDut"] = b["netDut"]
            if isinstance(b.get("muiTen"), bool):
                muc["muiTen"] = b["muiTen"]
        elif loai == "cung_tron":
            muc["cx"] = round(_ep_so(b.get("cx"), 0.0, -5000, 5000), 3)
            muc["cy"] = round(_ep_so(b.get("cy"), 0.0, -5000, 5000), 3)
            muc["r"] = round(_ep_so(b.get("r"), 1.0, 0.05, 5000), 3)
            if b.get("gocBatDau") is not None:
                muc["gocBatDau"] = round(_ep_so(b.get("gocBatDau"), 0.0, -720, 720), 1)
            if b.get("gocKetThuc") is not None:
                muc["gocKetThuc"] = round(_ep_so(b.get("gocKetThuc"), 360.0, -720, 720), 1)
            if b.get("mauTo"):
                muc["mauTo"] = _ep_mau_hex(b.get("mauTo"), "#38BDF8")
            if b.get("doDay") is not None:
                muc["doDay"] = round(_ep_so(b.get("doDay"), 3.4, 1.0, 12.0), 1)
        elif loai == "da_giac":
            pts = _chuan_hoa_mang_diem(b.get("diem"))
            if len(pts) < 3:
                continue
            muc["diem"] = pts
            pts_dich = _chuan_hoa_mang_diem(b.get("diemDich"))
            if len(pts_dich) == len(pts):
                muc["diemDich"] = pts_dich
            if b.get("mauTo"):
                muc["mauTo"] = _ep_mau_hex(b.get("mauTo"), "#38BDF8")
            if b.get("doMoTo") is not None:
                muc["doMoTo"] = round(_ep_so(b.get("doMoTo"), 0.25, 0.05, 0.9), 2)
        elif loai == "truc_toa_do":
            if b.get("xMin") is not None:
                muc["xMin"] = round(_ep_so(b.get("xMin"), -5.0, -1000, 1000), 2)
            if b.get("xMax") is not None:
                muc["xMax"] = round(_ep_so(b.get("xMax"), 5.0, -1000, 1000), 2)
            if b.get("yMin") is not None:
                muc["yMin"] = round(_ep_so(b.get("yMin"), -4.0, -1000, 1000), 2)
            if b.get("yMax") is not None:
                muc["yMax"] = round(_ep_so(b.get("yMax"), 4.0, -1000, 1000), 2)
            if isinstance(b.get("hienLuoi"), bool):
                muc["hienLuoi"] = b["hienLuoi"]
            if b.get("nhanX"):
                muc["nhanX"] = str(b["nhanX"]).strip()[:16]
            if b.get("nhanY"):
                muc["nhanY"] = str(b["nhanY"]).strip()[:16]
        elif loai == "duong_cong":
            pts = _chuan_hoa_mang_diem(b.get("diem"))
            if len(pts) >= 2:
                muc["diem"] = pts
            else:
                muc["ham"] = chuan_hoa_enum(b.get("ham"), LOAI_HAM_DO_THI, "parabol")
                if b.get("heSoA") is not None:
                    muc["heSoA"] = round(_ep_so(b.get("heSoA"), 0.35, -50, 50), 3)
                if b.get("heSoB") is not None:
                    muc["heSoB"] = round(_ep_so(b.get("heSoB"), 0.0, -50, 50), 3)
                if b.get("heSoC") is not None:
                    muc["heSoC"] = round(_ep_so(b.get("heSoC"), 0.0, -50, 50), 3)
                if b.get("xTu") is not None:
                    muc["xTu"] = round(_ep_so(b.get("xTu"), -4.0, -1000, 1000), 2)
                if b.get("xDen") is not None:
                    muc["xDen"] = round(_ep_so(b.get("xDen"), 4.0, -1000, 1000), 2)
            if b.get("doDay") is not None:
                muc["doDay"] = round(_ep_so(b.get("doDay"), 4.0, 1.0, 12.0), 1)
        elif loai == "nhan_chu":
            nd = str(b.get("noiDung") or b.get("nhan") or "").strip()[:60]
            if not nd:
                continue
            muc["x"] = round(_ep_so(b.get("x"), 0.0, -5000, 5000), 3)
            muc["y"] = round(_ep_so(b.get("y"), 0.0, -5000, 5000), 3)
            muc["noiDung"] = nd
            if b.get("coChu") is not None:
                muc["coChu"] = int(_ep_so(b.get("coChu"), 20, 12, 42))

        ket_qua.append(muc)
    return ket_qua


def chuan_hoa_goi_y_thumbnail(
    raw_list: Any,
    danh_sach_nv: list[dict[str, Any]],
    tieu_de_video: str = "",
) -> list[dict[str, Any]]:
    """Chuan hoa 3 phuong an Thumbnail A/B (bien_the 1, 2, 3) tu blueprint/kich ban."""
    ban_do_nv = {nv["id"]: nv for nv in danh_sach_nv if isinstance(nv, dict) and nv.get("id")}
    nv_mac_dinh = danh_sach_nv[0] if danh_sach_nv else {
        "id": "nha_toan_hoc",
        "ten": "Nhà Toán Học",
        "mauThan": "#0F172A",
        "mauChuDao": "#2563EB",
        "mauDa": "#FFFDF7",
        "phuKien": "kinh_tron",
    }

    def _gioi_han_4_tu(txt: Any, fallback: str) -> str:
        tu = [t for t in str(txt or "").strip().split() if t]
        return " ".join(tu[:4]).upper() if tu else fallback

    raw_by_bt: dict[int, dict[str, Any]] = {}
    if isinstance(raw_list, list):
        for idx, item in enumerate(raw_list[:3], start=1):
            if not isinstance(item, dict):
                continue
            bt_val = item.get("bien_the")
            bt = int(bt_val) if isinstance(bt_val, int) and bt_val in (1, 2, 3) else idx
            raw_by_bt[bt] = item

    mac_dinh = {
        1: {
            "tieuDeLon": _gioi_han_4_tu(tieu_de_video, "BÍ MẬT TOÁN HỌC"),
            "nhanPhu": "SỰ THẬT SỐC",
            "congThucLatex": "a^2 + b^2 = c^2",
            "daoCuNoiBat": "compa_co",
            "boiCanh": "quang_truong_hy_lap",
            "bieuCam": "ngac_nhien",
            "hanhDong": "giat_minh_nhay_dung",
            "mauNhan": "#FACC15",
        },
        2: {
            "tieuDeLon": "NGHỊCH LÝ CHẤN ĐỘNG",
            "nhanPhu": "CÂU CHUYỆN CÓ THẬT",
            "congThucLatex": "\\sqrt{2} \\notin \\mathbb{Q}",
            "daoCuNoiBat": "khoi_da_dien",
            "boiCanh": "dai_thien_van_phuc_hung",
            "bieuCam": "hoang_mang",
            "hanhDong": "ho_het_sung_suong",
            "mauNhan": "#38BDF8",
        },
        3: {
            "tieuDeLon": "GIẢI MÃ TRONG 10P",
            "nhanPhu": "TOÁN HỌC DỄ HIỂU",
            "congThucLatex": "e^{i\\pi} + 1 = 0",
            "daoCuNoiBat": "kinh_thien_van",
            "boiCanh": "lop_hoc_bang_xanh",
            "bieuCam": "tinh_quai",
            "hanhDong": "chi_tro_giai_thich",
            "mauNhan": "#FACC15",
        },
    }

    ket_qua: list[dict[str, Any]] = []
    for bt in (1, 2, 3):
        item = raw_by_bt.get(bt, {})
        md = mac_dinh[bt]
        nv_obj = item.get("nhanVat") if isinstance(item.get("nhanVat"), dict) else None
        if nv_obj is None and isinstance(item.get("nhanVatId"), str):
            nv_obj = ban_do_nv.get(item["nhanVatId"].strip())
        if nv_obj is None:
            nv_obj = danh_sach_nv[(bt - 1) % len(danh_sach_nv)] if danh_sach_nv else nv_mac_dinh

        latex_clean, _ = kiem_tra_latex(str(item.get("congThucLatex") or md["congThucLatex"]))
        ket_qua.append(
            {
                "bien_the": bt,
                "tieuDeLon": _gioi_han_4_tu(item.get("tieuDeLon"), md["tieuDeLon"]),
                "nhanPhu": str(item.get("nhanPhu") or md["nhanPhu"]).strip()[:36],
                "congThucLatex": latex_clean or md["congThucLatex"],
                "daoCuNoiBat": chuan_hoa_enum(item.get("daoCuNoiBat"), LOAI_DAO_CU, md["daoCuNoiBat"]),
                "boiCanh": chuan_hoa_enum(item.get("boiCanh"), LOAI_BOI_CANH, md["boiCanh"]),
                "thoiTiet": chuan_hoa_enum(item.get("thoiTiet"), LOAI_THOI_TIET, "nang_dep"),
                "nhanVat": nv_obj,
                "bieuCam": chuan_hoa_enum(item.get("bieuCam"), LOAI_BIEU_CAM, md["bieuCam"]),
                "hanhDong": chuan_hoa_enum(item.get("hanhDong"), LOAI_HANH_DONG, md["hanhDong"]),
                "vatCamTay": chuan_hoa_enum(item.get("vatCamTay"), LOAI_VAT_CAM_TAY, "cuon_giay"),
                "mauNhan": _ep_mau_hex(item.get("mauNhan"), md["mauNhan"]),
            }
        )
    return ket_qua


def chuan_hoa_danh_sach_nhan_vat(raw_list: Any) -> list[dict[str, Any]]:
    """Chuan hoa danhSachNhanVat theo ThongTinNhanVat trong src/kieu_dai.ts (ho tro ho so tao hinh v3.0)."""
    mau_chu_dao_mac_dinh = ["#2563EB", "#EA580C", "#059669", "#7C3AED", "#DB2777"]
    trang_phuc_mac_dinh = ("ao_vest_co_dien", "ao_choang_hoc_gia", "ao_len_mua_dong", "thuong_dan")
    kieu_toc_mac_dinh = ("gon_gang", "xoan_co_dien", "toc_bac_dai", "mu_noi")
    ket_qua: list[dict[str, Any]] = []
    da_dung_id: set[str] = set()

    if isinstance(raw_list, list):
        for idx, item in enumerate(raw_list):
            if not isinstance(item, dict):
                continue
            ten = str(item.get("ten") or f"Nhân vật {idx + 1}").strip()
            nv_id = tao_slug(str(item.get("id") or ten))
            if not nv_id or nv_id in da_dung_id:
                nv_id = f"nhan_vat_{idx + 1}"
            da_dung_id.add(nv_id)
            mau_chu_dao = _ep_mau_hex(
                item.get("mauChuDao"),
                mau_chu_dao_mac_dinh[idx % len(mau_chu_dao_mac_dinh)],
            )
            muc_nv_info: dict[str, Any] = {
                "id": nv_id,
                "ten": ten,
                "mauThan": _ep_mau_hex(item.get("mauThan"), "#1E293B"),
                "mauChuDao": mau_chu_dao,
                "mauDa": _ep_mau_hex(item.get("mauDa"), "#FFFDF7"),
                "phuKien": chuan_hoa_enum(item.get("phuKien"), LOAI_PHU_KIEN, "khong"),
                "trangPhuc": chuan_hoa_enum(
                    item.get("trangPhuc"),
                    LOAI_TRANG_PHUC,
                    trang_phuc_mac_dinh[idx % len(trang_phuc_mac_dinh)],
                ),
                "kieuToc": chuan_hoa_enum(
                    item.get("kieuToc"),
                    LOAI_KIEU_TOC,
                    kieu_toc_mac_dinh[idx % len(kieu_toc_mac_dinh)],
                ),
                "coRau": chuan_hoa_enum(item.get("coRau"), LOAI_CO_RAU, "khong"),
                "mauAo": _ep_mau_hex(item.get("mauAo"), mau_chu_dao),
            }
            if item.get("doTuoi") is not None:
                muc_nv_info["doTuoi"] = chuan_hoa_enum(item.get("doTuoi"), DO_TUOI_NHAN_VAT, "truong_thanh")
            ket_qua.append(muc_nv_info)

    if not ket_qua:
        ket_qua = [
            {
                "id": "nguoi_ke_chuyen",
                "ten": "Người Kể Chuyện",
                "mauThan": "#1E293B",
                "mauChuDao": "#2563EB",
                "mauDa": "#FFFDF7",
                "phuKien": "kinh_tron",
                "trangPhuc": "ao_vest_co_dien",
                "kieuToc": "gon_gang",
                "coRau": "khong",
                "mauAo": "#2563EB",
            },
            {
                "id": "nha_toan_hoc",
                "ten": "Nhà Toán Học",
                "mauThan": "#1E293B",
                "mauChuDao": "#EA580C",
                "mauDa": "#FFFDF7",
                "phuKien": "ao_choang",
                "trangPhuc": "ao_choang_hoc_gia",
                "kieuToc": "xoan_co_dien",
                "coRau": "ria_mep",
                "mauAo": "#EA580C",
            },
        ]
    return ket_qua


def chuan_hoa_danh_sach_boi_canh_ai(raw_list: Any) -> list[dict[str, Any]]:
    """
    Chuan hoa danhSachBoiCanhAI[] (v3.0): 14-20 dia diem & 4-6 khung tranh dac ta can canh
    bang tieng Anh suc tich de truyen thang cho scripts/pipeline/tao_boi_canh_ai.py.
    """
    if not isinstance(raw_list, list):
        return []
    ket_qua: list[dict[str, Any]] = []
    da_dung_ma: set[str] = set()
    for idx, item in enumerate(raw_list[:26], start=1):
        if not isinstance(item, dict):
            continue
        loai_kh = chuan_hoa_enum(
            item.get("loaiKhungHinh") or item.get("loai"),
            LOAI_KHUNG_HINH_AI,
            "boi_canh",
        )
        boi_canh = chuan_hoa_enum(item.get("boiCanh"), LOAI_BOI_CANH, "thu_vien_co_dien")
        thoi_tiet = chuan_hoa_enum(item.get("thoiTiet"), LOAI_THOI_TIET, "nang_dep")
        mo_ta_en = re.sub(
            r"\s+",
            " ",
            str(item.get("moTaTiengAnh") or item.get("moTaEn") or item.get("promptEn") or "").strip(),
        )
        if not mo_ta_en:
            continue
        tien_to = "cc" if loai_kh == "can_canh_vat_the" else "bc"
        ma_raw = str(item.get("maBoiCanhAI") or item.get("maBoiCanh") or item.get("id") or f"{tien_to}_{idx:02d}_{boi_canh}").strip()
        ma_sach = tao_slug(ma_raw) or f"{tien_to}_{idx:02d}_{boi_canh}"
        if ma_sach in da_dung_ma:
            ma_sach = f"{ma_sach[:42]}_{idx:02d}"
        da_dung_ma.add(ma_sach)
        muc: dict[str, Any] = {
            "maBoiCanhAI": ma_sach,
            "loaiKhungHinh": loai_kh,
            "boiCanh": boi_canh,
            "thoiTiet": thoi_tiet,
            "moTaTiengAnh": mo_ta_en[:320],
        }
        if item.get("daoCuChinh"):
            muc["daoCuChinh"] = chuan_hoa_enum(item.get("daoCuChinh"), LOAI_DAO_CU, "")
            if not muc["daoCuChinh"]:
                muc.pop("daoCuChinh", None)
        ket_qua.append(muc)
    return ket_qua


def _canh_la_nguoi_gia_hoac_giai_thuong(
    nhan_vat: list[dict[str, Any]],
    tieu_de_nho: str = "",
    loi_thoai: str = "",
) -> bool:
    """Nhan dien canh nguoi gia / nhan giai thuong / cuoi doi de CAM chon nha_co_phong_sinh."""
    if any(isinstance(nv, dict) and nv.get("doTuoi") == "gia" for nv in nhan_vat):
        return True
    van_ban = f"{tieu_de_nho} {loi_thoai}".lower()
    return any(kw in van_ban for kw in _TU_KHOA_NGUOI_GIA_GIAI_THUONG)


def _loc_vat_the_hop_le_boi_canh(
    boi_canh: str,
    vat_the: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Chan vat the moi truong lech boi canh (la_vang_gio trong phong kin, ngon_nen_den_dau trong vu tru)."""
    ket_qua: list[dict[str, Any]] = []
    for vt in vat_the:
        loai = str(vt.get("loai") or "")
        if boi_canh in BOI_CANH_TRONG_NHA and loai in VAT_THE_NGOAI_TROI_CAM_TRONG_NHA:
            continue
        if boi_canh in BOI_CANH_VU_TRU and loai in VAT_THE_CAM_TRONG_VU_TRU:
            continue
        if loai == "tuyet_cua_so" and boi_canh not in BOI_CANH_CO_CUA_SO_TUYET:
            continue
        ket_qua.append(vt)
    return ket_qua


def _chuan_hoa_thoi_tiet_boi_canh(boi_canh: str, thoi_tiet: str) -> str:
    """Chan thoi tiet ngoai troi (la_roi, mua_nhe, tuyet_roi) roi tu do trong phong kin/vu tru."""
    if boi_canh in BOI_CANH_TRONG_NHA:
        if thoi_tiet == "la_roi":
            return "khong"
        if thoi_tiet in ("mua_nhe", "tuyet_roi") and boi_canh not in ("phong_benh_vien", "phong_tro_bep_lua"):
            return "khong"
    if boi_canh == "khong_gian_vu_tru_toan" and thoi_tiet in ("la_roi", "mua_nhe", "tuyet_roi"):
        return "khong"
    return thoi_tiet


def _tinh_head_y_nhan_vat(nv: dict[str, Any], ti_le_canh: float = 1.25) -> float:
    """Uoc tinh chinh xac toa do Y tam dau nhan vat tren khung 1920x1080."""
    y_chan = float(nv.get("y") or 810.0)
    ti_le = float(nv.get("tiLe") or 1.0) * ti_le_canh
    do_tuoi = str(nv.get("doTuoi") or "truong_thanh")
    tu_the = str(nv.get("tuThe") or "dung")
    if do_tuoi == "so_sinh":
        head_local = -62.0
    elif tu_the == "ngoi_ban":
        head_local = -136.0
    elif tu_the == "nam_giuong":
        head_local = -130.0
    elif do_tuoi == "thieu_nien":
        head_local = -142.0
    elif do_tuoi == "gia":
        head_local = -162.0
    else:
        head_local = -170.0
    return y_chan + head_local * ti_le


def lay_ho_so_mascot_kenh(
    duong_dan_env: Path | str | None = None,
    env_override: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Doc ho so Mascot kenh mac dinh (de tuy chinh ten/trangPhuc/kieuToc/mauAo qua .env)."""
    tu_file = tai_env(duong_dan_env)
    nguon: dict[str, str] = {}
    nguon.update(tu_file)
    for k in (
        "MASCOT_ID",
        "MASCOT_TEN",
        "MASCOT_TRANG_PHUC",
        "MASCOT_KIEU_TOC",
        "MASCOT_CO_RAU",
        "MASCOT_PHU_KIEN",
        "MASCOT_MAU_AO",
    ):
        if os.environ.get(k):
            nguon[k] = os.environ[k]
    if env_override:
        nguon.update(env_override)

    ho_so = dict(MASCOT_KENH_MAC_DINH)
    if str(nguon.get("MASCOT_ID") or "").strip():
        ho_so["id"] = tao_slug(str(nguon["MASCOT_ID"]))
    if str(nguon.get("MASCOT_TEN") or "").strip():
        ho_so["ten"] = str(nguon["MASCOT_TEN"]).strip()[:40]
    if str(nguon.get("MASCOT_TRANG_PHUC") or "").strip():
        ho_so["trangPhuc"] = chuan_hoa_enum(nguon["MASCOT_TRANG_PHUC"], LOAI_TRANG_PHUC, ho_so["trangPhuc"])
    if str(nguon.get("MASCOT_KIEU_TOC") or "").strip():
        ho_so["kieuToc"] = chuan_hoa_enum(nguon["MASCOT_KIEU_TOC"], LOAI_KIEU_TOC, ho_so["kieuToc"])
    if str(nguon.get("MASCOT_CO_RAU") or "").strip():
        ho_so["coRau"] = chuan_hoa_enum(nguon["MASCOT_CO_RAU"], LOAI_CO_RAU, ho_so["coRau"])
    if str(nguon.get("MASCOT_PHU_KIEN") or "").strip():
        ho_so["phuKien"] = chuan_hoa_enum(nguon["MASCOT_PHU_KIEN"], LOAI_PHU_KIEN, ho_so["phuKien"])
    if str(nguon.get("MASCOT_MAU_AO") or "").strip():
        mau_ao = _ep_mau_hex(nguon["MASCOT_MAU_AO"], ho_so["mauAo"])
        ho_so["mauAo"] = mau_ao
        ho_so["mauChuDao"] = mau_ao
    return ho_so


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
    tap_nv = set(danh_sach_nv_ids) | {ID_MASCOT_KENH}

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
        loi_thoai = "Câu chuyện Toán học vẫn đang tiếp tục mở ra những bất ngờ thú vị."

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
    if raw.get("vaiNoi") is not None:
        canh["vaiNoi"] = chuan_hoa_enum(raw.get("vaiNoi"), LOAI_VAI_NOI, "nguoi_dan")
    if raw.get("tieuDeNho"):
        canh["tieuDeNho"] = cat_gon_theo_tu(str(raw["tieuDeNho"]).strip(), 110)
    if raw.get("phuDeHoi"):
        canh["phuDeHoi"] = cat_gon_theo_tu(str(raw["phuDeHoi"]).strip(), 140)
    if raw.get("namMoc"):
        canh["namMoc"] = cat_gon_theo_tu(str(raw["namMoc"]).strip(), 50)
    if raw.get("loaiCanh") is not None:
        canh["loaiCanh"] = chuan_hoa_enum(raw.get("loaiCanh"), LOAI_CANH, "ke_chuyen")

    # Truong v3.0: boi canh AI, khung tranh dac ta & anh sang moi truong
    ma_bc_ai = str(raw.get("maBoiCanhAI") or raw.get("maBoiCanh") or "").strip()
    if ma_bc_ai:
        canh["maBoiCanhAI"] = tao_slug(ma_bc_ai)
    if isinstance(raw.get("laKhungTranhDacTa"), bool):
        canh["laKhungTranhDacTa"] = raw["laKhungTranhDacTa"]
    if isinstance(raw.get("anhBoiCanh"), str) and raw["anhBoiCanh"].strip():
        canh["anhBoiCanh"] = raw["anhBoiCanh"].strip()
    raw_asmt = raw.get("anhSangMoiTruong")
    if isinstance(raw_asmt, dict):
        canh["anhSangMoiTruong"] = {
            "mauAm": _ep_mau_hex(raw_asmt.get("mauAm"), "#FDE68A"),
            "doToi": round(_ep_so(raw_asmt.get("doToi"), 0.25, 0.0, 1.0), 3),
            "loaiAnhSang": chuan_hoa_enum(raw_asmt.get("loaiAnhSang"), LOAI_ANH_SANG_MOI_TRUONG, "trung_tinh"),
        }

    # Truong v3.5: ngat nhac punchline 0.8s, 3 khung hinh ke chuyen moi & End-Screen 15s
    if isinstance(raw.get("ngatNhacPunchline"), bool) and raw["ngatNhacPunchline"]:
        canh["ngatNhacPunchline"] = True

    raw_bd = raw.get("banDoHanhTrinh")
    if isinstance(raw_bd, dict):
        diem_di = cat_gon_theo_tu(str(raw_bd.get("diemDi") or "").strip(), 48)
        diem_den = cat_gon_theo_tu(str(raw_bd.get("diemDen") or "").strip(), 48)
        if diem_di or diem_den:
            bd_clean: dict[str, Any] = {
                "diemDi": diem_di or "Điểm Khởi Hành",
                "diemDen": diem_den or "Điểm Đích",
                "phuongTien": chuan_hoa_enum(raw_bd.get("phuongTien"), PHUONG_TIEN_HANH_TRINH, "tau_thuy"),
            }
            if raw_bd.get("khoangCachNhan"):
                bd_clean["khoangCachNhan"] = cat_gon_theo_tu(str(raw_bd["khoangCachNhan"]).strip(), 60)
            if raw_bd.get("moTaHanhTrinh"):
                bd_clean["moTaHanhTrinh"] = cat_gon_theo_tu(str(raw_bd["moTaHanhTrinh"]).strip(), 96)
            if raw_bd.get("diemDungGiua"):
                bd_clean["diemDungGiua"] = cat_gon_theo_tu(str(raw_bd["diemDungGiua"]).strip(), 40)
            canh["banDoHanhTrinh"] = bd_clean

    raw_bao = raw.get("baoChiCo")
    if isinstance(raw_bao, dict):
        td_bao = cat_gon_theo_tu(str(raw_bao.get("tieuDeBao") or "").strip(), 90)
        if td_bao:
            bao_clean: dict[str, Any] = {"tieuDeBao": td_bao}
            if raw_bao.get("tenToBao"):
                bao_clean["tenToBao"] = cat_gon_theo_tu(str(raw_bao["tenToBao"]).strip(), 50)
            if raw_bao.get("ngayPhatHanh"):
                bao_clean["ngayPhatHanh"] = cat_gon_theo_tu(str(raw_bao["ngayPhatHanh"]).strip(), 40)
            if raw_bao.get("tieuDePhu"):
                bao_clean["tieuDePhu"] = cat_gon_theo_tu(str(raw_bao["tieuDePhu"]).strip(), 110)
            if raw_bao.get("nhanAnhMinhHoa"):
                bao_clean["nhanAnhMinhHoa"] = cat_gon_theo_tu(str(raw_bao["nhanAnhMinhHoa"]).strip(), 70)
            if raw_bao.get("daoCuMinhHoa"):
                bao_clean["daoCuMinhHoa"] = chuan_hoa_enum(raw_bao["daoCuMinhHoa"], LOAI_DAO_CU, "cuon_giay")
            if raw_bao.get("congThucMinhHoa"):
                lx_bao, cb_bao = kiem_tra_latex(str(raw_bao["congThucMinhHoa"]))
                if lx_bao:
                    bao_clean["congThucMinhHoa"] = lx_bao
                for cb in cb_bao:
                    canh_bao_latex.append(f"[{canh_id}] {cb}")
            canh["baoChiCo"] = bao_clean

    raw_pu = raw.get("phanUngCam")
    if isinstance(raw_pu, dict):
        pu_clean: dict[str, Any] = {
            "kieuPhanUng": chuan_hoa_enum(raw_pu.get("kieuPhanUng"), KIEU_PHAN_UNG_CAM, "nhap_tra"),
        }
        nv_pu = str(raw_pu.get("nhanVatId") or "").strip()
        if nv_pu and nv_pu in tap_nv:
            pu_clean["nhanVatId"] = nv_pu
        if raw_pu.get("chuHieuUng"):
            pu_clean["chuHieuUng"] = cat_gon_theo_tu(str(raw_pu["chuHieuUng"]).strip(), 28)
        canh["phanUngCam"] = pu_clean

    raw_es = raw.get("endScreen")
    if isinstance(raw_es, dict):
        es_clean: dict[str, Any] = {}
        if raw_es.get("khungTraiNhan"):
            es_clean["khungTraiNhan"] = cat_gon_theo_tu(str(raw_es["khungTraiNhan"]).strip(), 42)
        if raw_es.get("khungPhaiNhan"):
            es_clean["khungPhaiNhan"] = cat_gon_theo_tu(str(raw_es["khungPhaiNhan"]).strip(), 42)
        if raw_es.get("loiDanXemTiep"):
            es_clean["loiDanXemTiep"] = cat_gon_theo_tu(str(raw_es["loiDanXemTiep"]).strip(), 110)
        if es_clean:
            canh["endScreen"] = es_clean

    # Phu de (neu co san)
    if isinstance(raw.get("phuDe"), list):
        phu_de_sach = [str(p).strip() for p in raw["phuDe"] if str(p).strip()]
        if phu_de_sach:
            canh["phuDe"] = phu_de_sach

    # Camera cu (tuong thich nguoc)
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

    # May quay dao dien v2.0 / v3.0 (gocQuay can mat + dao_goc_can_mat + tuDongFocusNguoiNoi)
    raw_mq = raw.get("mayQuay") if isinstance(raw.get("mayQuay"), dict) else {}
    goc_quay_raw = raw_mq.get("gocQuay") if raw_mq.get("gocQuay") is not None else raw.get("gocQuay")
    tu_dong_focus_raw = (
        raw_mq.get("tuDongFocusNguoiNoi")
        if isinstance(raw_mq.get("tuDongFocusNguoiNoi"), bool)
        else (raw.get("tuDongFocusNguoiNoi") if isinstance(raw.get("tuDongFocusNguoiNoi"), bool) else None)
    )
    if raw_mq or goc_quay_raw is not None or tu_dong_focus_raw is not None:
        mq_sach: dict[str, Any] = {}
        if goc_quay_raw is not None:
            mq_sach["gocQuay"] = chuan_hoa_enum(goc_quay_raw, GOC_QUAY_CAMERA, "trung_canh")
        if raw_mq.get("doPhong") is not None:
            mq_sach["doPhong"] = round(_ep_so(raw_mq.get("doPhong"), 1.15, 0.85, 2.35), 2)
        if isinstance(raw_mq.get("diemTieuCu"), dict):
            dtc = raw_mq["diemTieuCu"]
            mq_sach["diemTieuCu"] = {
                "x": round(_ep_so(dtc.get("x"), 960, 100, 1820), 1),
                "y": round(_ep_so(dtc.get("y"), 540, 100, 980), 1),
            }
        if isinstance(tu_dong_focus_raw, bool):
            mq_sach["tuDongFocusNguoiNoi"] = tu_dong_focus_raw
        if isinstance(raw_mq.get("rungNhe"), bool):
            mq_sach["rungNhe"] = raw_mq["rungNhe"]
        if mq_sach:
            canh["mayQuay"] = mq_sach

    # Luot thoai da nhan vat (v2.0 / v3.0: ho tro kieuBongBong & dao_goc_can_mat)
    if isinstance(raw.get("luotThoai"), list):
        lt_sach: list[dict[str, Any]] = []
        frame_lt = 0
        for idx_lt, lt in enumerate(raw["luotThoai"][:8]):
            if not isinstance(lt, dict):
                continue
            nd_lt = re.sub(r"\s+", " ", str(lt.get("noiDung") or "").strip())
            if not nd_lt:
                continue
            nv_lt_raw = str(lt.get("nhanVatId") or "").strip()
            nv_lt = nv_lt_raw if nv_lt_raw in tap_nv else danh_sach_nv_ids[idx_lt % len(danh_sach_nv_ids)]
            so_frame_uoc = max(45, int(round((max(2.0, dem_tu(nd_lt) / 2.65)) * 30)))
            bd_raw = lt.get("batDauFrame")
            kt_raw = lt.get("ketThucFrame")
            bd_f = int(_ep_so(bd_raw, frame_lt, 0, 10000)) if bd_raw is not None else frame_lt
            kt_f = int(_ep_so(kt_raw, bd_f + so_frame_uoc, bd_f + 15, 12000)) if kt_raw is not None else (bd_f + so_frame_uoc)
            muc_lt: dict[str, Any] = {
                "nhanVatId": nv_lt,
                "noiDung": nd_lt[:260],
                "batDauFrame": bd_f,
                "ketThucFrame": kt_f,
            }
            if lt.get("bieuCam") is not None:
                muc_lt["bieuCam"] = chuan_hoa_enum(lt.get("bieuCam"), LOAI_BIEU_CAM, "binh_thuong")
            if lt.get("dongTac") is not None:
                muc_lt["dongTac"] = chuan_hoa_enum(lt.get("dongTac"), LOAI_HANH_DONG, "quay_nhin_doi_thoai")
            if lt.get("kieuBongBong") is not None:
                muc_lt["kieuBongBong"] = chuan_hoa_enum(lt.get("kieuBongBong"), KIEU_BONG_BONG_CHAT, "thuong")
            if isinstance(lt.get("bienDoAmThanh"), list):
                rms_lt = [
                    round(min(1.0, max(0.0, float(v))), 2)
                    for v in lt["bienDoAmThanh"]
                    if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
                ]
                if rms_lt:
                    muc_lt["bienDoAmThanh"] = rms_lt
            lt_sach.append(muc_lt)
            frame_lt = kt_f + 9
        if lt_sach:
            canh["luotThoai"] = lt_sach
            if not str(raw.get("loiThoai") or "").strip():
                canh["loiThoai"] = " ".join(m["noiDung"] for m in lt_sach)
            # Mac dinh goc dao_goc_can_mat cho canh doi_thoai >= 2 nguoi noi neu chua chi dinh gocQuay
            nguoi_noi_khac = {m["nhanVatId"] for m in lt_sach}
            if (
                (bo_cuc == "doi_thoai" or canh.get("loaiCanh") == "doi_thoai")
                and len(nguoi_noi_khac) >= 2
                and not (isinstance(canh.get("mayQuay"), dict) and canh["mayQuay"].get("gocQuay"))
            ):
                mq_cur = canh.get("mayQuay") if isinstance(canh.get("mayQuay"), dict) else {}
                mq_cur["gocQuay"] = "dao_goc_can_mat"
                mq_cur["tuDongFocusNguoiNoi"] = True
                canh["mayQuay"] = mq_cur

    # Cau hoi tuong tac khan gia (v2.0)
    raw_chtt = raw.get("cauHoiTuongTac")
    if isinstance(raw_chtt, dict):
        cau_hoi = str(raw_chtt.get("cauHoi") or "").strip()
        dap_an = str(raw_chtt.get("dapAn") or "").strip()
        if cau_hoi and dap_an:
            chtt_sach: dict[str, Any] = {
                "cauHoi": cau_hoi[:160],
                "thoiGianDemNguocGiay": int(_ep_so(raw_chtt.get("thoiGianDemNguocGiay"), 3, 2, 5)),
                "dapAn": dap_an[:120],
            }
            if raw_chtt.get("batDauDemNguocFrame") is not None:
                chtt_sach["batDauDemNguocFrame"] = int(_ep_so(raw_chtt.get("batDauDemNguocFrame"), 24, 0, 600))
            if isinstance(raw_chtt.get("luaChon"), list):
                lc_sach = [str(x).strip()[:50] for x in raw_chtt["luaChon"][:4] if str(x).strip()]
                if lc_sach:
                    chtt_sach["luaChon"] = lc_sach
            if raw_chtt.get("giaiThichNgan"):
                chtt_sach["giaiThichNgan"] = str(raw_chtt["giaiThichNgan"]).strip()[:140]
            if raw_chtt.get("hienDapAnTuFrame") is not None:
                chtt_sach["hienDapAnTuFrame"] = int(_ep_so(raw_chtt.get("hienDapAnTuFrame"), 120, 30, 900))
            canh["cauHoiTuongTac"] = chtt_sach

    # Nhan vat trong canh (CHONG NHAN DOI cung 1 nhanVatId dung 2 lan trong cung canh)
    nv_sach: list[dict[str, Any]] = []
    da_xuat_hien_nv: set[str] = set()
    raw_nvs = raw.get("nhanVat") if isinstance(raw.get("nhanVat"), list) else []
    vi_tri_mac_dinh = [660, 1260, 960] if bo_cuc != "giai_thich_toan" else [255, 1660, 255]
    for idx, nv in enumerate(raw_nvs[:3]):
        if not isinstance(nv, dict):
            continue
        nv_id_raw = str(nv.get("id") or "").strip()
        if nv_id_raw in tap_nv:
            nv_id = nv_id_raw
        else:
            nv_id = next((nid for nid in danh_sach_nv_ids if nid not in da_xuat_hien_nv), "")
        if not nv_id or nv_id in da_xuat_hien_nv:
            continue
        da_xuat_hien_nv.add(nv_id)
        x_default = vi_tri_mac_dinh[len(nv_sach) % len(vi_tri_mac_dinh)]
        muc_nv: dict[str, Any] = {
            "id": nv_id,
            "x": round(_ep_so(nv.get("x"), x_default, 140, 1780), 1),
            "y": round(_ep_so(nv.get("y"), 810, 620, 880), 1),
            "huong": chuan_hoa_enum(nv.get("huong"), HUONG_NHAN_VAT, "phai" if len(nv_sach) % 2 == 0 else "trai"),
            "hanhDong": chuan_hoa_enum(nv.get("hanhDong"), LOAI_HANH_DONG, "dung_tho"),
            "bieuCam": chuan_hoa_enum(nv.get("bieuCam"), LOAI_BIEU_CAM, "binh_thuong"),
        }
        if nv.get("vatCamTay") is not None:
            muc_nv["vatCamTay"] = chuan_hoa_enum(nv.get("vatCamTay"), LOAI_VAT_CAM_TAY, "khong")
        if isinstance(nv.get("dangNoi"), bool):
            muc_nv["dangNoi"] = nv["dangNoi"]
        if nv.get("bongBongThoai"):
            muc_nv["bongBongThoai"] = cat_gon_theo_tu(str(nv["bongBongThoai"]).strip(), 90)
        if nv.get("kieuBongBong") is not None:
            muc_nv["kieuBongBong"] = chuan_hoa_enum(nv.get("kieuBongBong"), KIEU_BONG_BONG_CHAT, "thuong")
        if nv.get("diChuyenDenX") is not None:
            muc_nv["diChuyenDenX"] = round(_ep_so(nv.get("diChuyenDenX"), muc_nv["x"], 140, 1780), 1)
        if nv.get("tiLe") is not None:
            muc_nv["tiLe"] = round(_ep_so(nv.get("tiLe"), 1.0, 0.65, 1.45), 2)
        if nv.get("doTuoi") is not None:
            muc_nv["doTuoi"] = chuan_hoa_enum(nv.get("doTuoi"), DO_TUOI_NHAN_VAT, "truong_thanh")
        if nv.get("tuThe") is not None:
            muc_nv["tuThe"] = chuan_hoa_enum(nv.get("tuThe"), TU_THE_NHAN_VAT, "dung")
        if nv.get("trangPhuc") is not None:
            muc_nv["trangPhuc"] = chuan_hoa_enum(nv.get("trangPhuc"), LOAI_TRANG_PHUC, "ao_vest_co_dien")
        if nv.get("kieuToc") is not None:
            muc_nv["kieuToc"] = chuan_hoa_enum(nv.get("kieuToc"), LOAI_KIEU_TOC, "gon_gang")
        if nv.get("coRau") is not None:
            muc_nv["coRau"] = chuan_hoa_enum(nv.get("coRau"), LOAI_CO_RAU, "khong")
        if nv.get("mauAo") is not None:
            muc_nv["mauAo"] = _ep_mau_hex(nv.get("mauAo"), "#2563EB")
        if nv.get("tamKhung") is not None:
            muc_nv["tamKhung"] = chuan_hoa_enum(nv.get("tamKhung"), TAM_KHUNG_NHAN_VAT, "toan_canh")
        if isinstance(nv.get("tuongTacVoi"), str):
            ttv = nv["tuongTacVoi"].strip()
            if ttv == "khan_gia" or ttv in tap_nv:
                muc_nv["tuongTacVoi"] = ttv
        if isinstance(nv.get("bieuCamTheoMoc"), list):
            bcm_sach: list[dict[str, Any]] = []
            for moc in nv["bieuCamTheoMoc"][:6]:
                if not isinstance(moc, dict):
                    continue
                bc_m = chuan_hoa_enum(moc.get("bieuCam"), LOAI_BIEU_CAM, "")
                if not bc_m:
                    continue
                item_m: dict[str, Any] = {"bieuCam": bc_m}
                if moc.get("tuFrame") is not None:
                    item_m["tuFrame"] = int(_ep_so(moc.get("tuFrame"), 0, 0, 1200))
                elif moc.get("tienDo") is not None:
                    item_m["tienDo"] = round(_ep_so(moc.get("tienDo"), 0.5, 0.0, 1.0), 2)
                else:
                    item_m["tienDo"] = round(min(0.95, len(bcm_sach) * 0.35), 2)
                bcm_sach.append(item_m)
            if bcm_sach:
                muc_nv["bieuCamTheoMoc"] = bcm_sach
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

    # Chan chon nha_co_phong_sinh cho canh nguoi gia / nhan giai thuong / cuoi doi
    if canh["boiCanh"] == "nha_co_phong_sinh" and _canh_la_nguoi_gia_hoac_giai_thuong(
        nv_sach,
        str(canh.get("tieuDeNho") or ""),
        loi_thoai,
    ):
        van_ban_low = f"{canh.get('tieuDeNho', '')} {loi_thoai}".lower()
        canh["boiCanh"] = (
            "giang_duong_dai_hoc"
            if any(k in van_ban_low for k in ("giải thưởng", "huy chương", "vinh danh", "trao giải", "viện hàn lâm"))
            else "thu_vien_co_dien"
        )
    canh["thoiTiet"] = _chuan_hoa_thoi_tiet_boi_canh(canh["boiCanh"], canh["thoiTiet"])

    # Hieu ung hoat hinh (tu dong neo dung quanh headY cho cac hieu ung hai v3.0 & tranh de mat)
    if isinstance(raw.get("hieuUngHoatHinh"), list):
        hu_sach: list[dict[str, Any]] = []
        ti_le_canh_est = 1.45 if bo_cuc == "hai_huoc" else 1.25
        for hu in raw["hieuUngHoatHinh"][:4]:
            if not isinstance(hu, dict):
                continue
            loai_hu = chuan_hoa_enum(hu.get("loai"), LOAI_HIEU_UNG_HOAT_HINH, "sao_lap_lanh")
            hx = round(_ep_so(hu.get("x"), 960, 120, 1800), 1)
            hy = round(_ep_so(hu.get("y"), 480, 115, 860), 1)
            if loai_hu in ("bong_den_nay_so", "bong_den_y_tuong", "cham_hoi_nay") and nv_sach:
                nv_gan = min(nv_sach, key=lambda n: abs(float(n.get("x", 960)) - hx))
                head_y = _tinh_head_y_nhan_vat(nv_gan, ti_le_canh_est)
                hx = round(float(nv_gan.get("x", hx)), 1)
                hy = round(max(115.0, min(520.0, head_y - 75.0)), 1)
            elif loai_hu in ("mo_hoi_lon", "khoi_boc_tai", "mat_xoan_oc") and nv_sach:
                nv_gan = min(nv_sach, key=lambda n: abs(float(n.get("x", 960)) - hx))
                head_y = _tinh_head_y_nhan_vat(nv_gan, ti_le_canh_est)
                hx = round(float(nv_gan.get("x", hx)), 1)
                hy = round(max(120.0, min(620.0, head_y)), 1)
            elif loai_hu == "nhan_chu_hai_huoc" and nv_sach:
                for nv_c in nv_sach:
                    nx = float(nv_c.get("x", 960))
                    ny = float(nv_c.get("y", 810))
                    head_y = _tinh_head_y_nhan_vat(nv_c, ti_le_canh_est)
                    if abs(hx - nx) < 220 and (head_y - 45) <= hy <= (ny + 20):
                        hy = round(max(130.0, head_y - 105.0), 1)
            muc_hu: dict[str, Any] = {
                "loai": loai_hu,
                "x": hx,
                "y": hy,
                "tuFrame": int(_ep_so(hu.get("tuFrame"), 12, 0, 300)),
                "thoiLuong": int(_ep_so(hu.get("thoiLuong"), 75, 20, 360)),
            }
            if hu.get("chuHienThi"):
                muc_hu["chuHienThi"] = cat_gon_theo_tu(str(hu["chuHienThi"]).strip(), 45)
            if hu.get("mau"):
                muc_hu["mau"] = _ep_mau_hex(hu.get("mau"), "#FDE047")
            if hu.get("tiLe") is not None:
                muc_hu["tiLe"] = round(_ep_so(hu.get("tiLe"), 1.0, 0.5, 1.8), 2)
            hu_sach.append(muc_hu)
        if hu_sach:
            canh["hieuUngHoatHinh"] = hu_sach

    # Loi binh hai huoc (CAM hien thi tren boCuc giang_toan / dong_thoi_gian)
    raw_lb = raw.get("loiBinhHaiHuoc")
    la_canh_cam_loi_binh = (
        bo_cuc in ("giai_thich_toan", "dong_thoi_gian")
        or canh.get("loaiCanh") == "giang_toan"
    )
    if not la_canh_cam_loi_binh and isinstance(raw_lb, dict) and str(raw_lb.get("noiDung") or "").strip():
        vi_tri = raw_lb.get("viTri") if raw_lb.get("viTri") in ("goc_phai", "goc_trai") else "goc_phai"
        canh["loiBinhHaiHuoc"] = {
            "noiDung": cat_gon_theo_tu(str(raw_lb["noiDung"]).strip(), 140),
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
            if dc.get("bienSoXe"):
                muc_dc["bienSoXe"] = str(dc["bienSoXe"]).strip()[:14]
            dc_sach.append(muc_dc)
        if dc_sach:
            canh["daoCu"] = dc_sach

    # Bien so xe & vat the moi truong xung quanh (v2.0 Buoc 3)
    if raw.get("bienSoXe"):
        canh["bienSoXe"] = str(raw["bienSoXe"]).strip()[:14]
    if isinstance(raw.get("vatTheXungQuanh"), list):
        vt_sach: list[dict[str, Any]] = []
        for vt in raw["vatTheXungQuanh"][:6]:
            if not isinstance(vt, dict):
                continue
            loai_vt = chuan_hoa_enum(vt.get("loai"), LOAI_VAT_THE_XUNG_QUANH, "")
            if not loai_vt:
                continue
            muc_vt: dict[str, Any] = {"loai": loai_vt}
            if vt.get("x") is not None:
                muc_vt["x"] = round(_ep_so(vt.get("x"), 960, -200, 2120), 1)
            if vt.get("y") is not None:
                muc_vt["y"] = round(_ep_so(vt.get("y"), 540, -100, 1180), 1)
            if vt.get("tiLe") is not None:
                muc_vt["tiLe"] = round(_ep_so(vt.get("tiLe"), 1.0, 0.4, 2.2), 2)
            if vt.get("soLuong") is not None:
                muc_vt["soLuong"] = int(_ep_so(vt.get("soLuong"), 3, 1, 24))
            if vt.get("tocDo") is not None:
                muc_vt["tocDo"] = round(_ep_so(vt.get("tocDo"), 1.5, 0.2, 10.0), 2)
            if vt.get("mau"):
                muc_vt["mau"] = _ep_mau_hex(vt.get("mau"), "#FEF08A")
            if vt.get("bienSoXe"):
                muc_vt["bienSoXe"] = str(vt["bienSoXe"]).strip()[:14]
            vt_sach.append(muc_vt)
        vt_sach = _loc_vat_the_hop_le_boi_canh(canh["boiCanh"], vt_sach)
        if vt_sach:
            canh["vatTheXungQuanh"] = vt_sach

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
                    if ds_so and len(ds_so) == len(v):
                        tham_so_sach[khoa] = ds_so
                    else:
                        ds_chu = [str(x).strip()[:90] for x in v[:10] if isinstance(x, str) and x.strip()]
                        if ds_chu:
                            tham_so_sach[khoa] = ds_chu
                        elif ds_so:
                            tham_so_sach[khoa] = ds_so
            if tham_so_sach:
                mh_sach["thamSo"] = tham_so_sach
        if isinstance(raw_mh.get("khungToaDo"), dict):
            ktd = raw_mh["khungToaDo"]
            ktd_sach: dict[str, Any] = {}
            for fk, md_v in (("xMin", -5.0), ("xMax", 5.0), ("yMin", -4.0), ("yMax", 4.0)):
                if ktd.get(fk) is not None:
                    ktd_sach[fk] = round(_ep_so(ktd.get(fk), md_v, -1000, 1000), 2)
            for bk in ("hienLuoi", "hienTruc"):
                if isinstance(ktd.get(bk), bool):
                    ktd_sach[bk] = ktd[bk]
            if ktd.get("nhanX"):
                ktd_sach["nhanX"] = str(ktd["nhanX"]).strip()[:16]
            if ktd.get("nhanY"):
                ktd_sach["nhanY"] = str(ktd["nhanY"]).strip()[:16]
            if ktd.get("mauTruc"):
                ktd_sach["mauTruc"] = _ep_mau_hex(ktd["mauTruc"], "#94A3B8")
            if ktd.get("heToaDo") in ("toan", "svg"):
                ktd_sach["heToaDo"] = ktd["heToaDo"]
            if ktd_sach:
                mh_sach["khungToaDo"] = ktd_sach
        if isinstance(raw_mh.get("buocVe"), list):
            bv_sach = chuan_hoa_buoc_ve_toan(raw_mh["buocVe"])
            if bv_sach:
                mh_sach["buocVe"] = bv_sach
        if raw_mh.get("chuThichCuoi"):
            mh_sach["chuThichCuoi"] = str(raw_mh["chuThichCuoi"]).strip()[:90]
        if raw_mh.get("mauNhanManh"):
            mh_sach["mauNhanManh"] = _ep_mau_hex(raw_mh["mauNhanManh"], "#FACC15")
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

    # Moc thoi gian (cat gon theo ranh gioi tu, KHONG BAO GIO cat cut giua tu)
    if isinstance(raw.get("mocThoiGian"), list):
        mtg_sach: list[dict[str, Any]] = []
        for m in raw["mocThoiGian"][:5]:
            if not isinstance(m, dict):
                continue
            nam = str(m.get("nam") or "").strip()
            mo_ta = str(m.get("moTa") or m.get("suKien") or "").strip()
            if not nam and not mo_ta:
                continue
            muc_m: dict[str, Any] = {
                "nam": cat_gon_theo_tu(nam, 30) or "...",
                "moTa": cat_gon_theo_tu(mo_ta, 125) or "...",
            }
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
            # Canh tuong_tac_khan_gia can >= 7s (doc 1s + dem nguoc 3s + hien "DAP AN CHINH XAC" 3s)
            chtt = canh.get("cauHoiTuongTac")
            if str(canh.get("loaiCanh") or "") == "tuong_tac_khan_gia" or (
                isinstance(chtt, dict) and str(chtt.get("cauHoi") or "").strip()
            ):
                dem_g = max(1, int((chtt or {}).get("thoiGianDemNguocGiay") or 3))
                so_frame = max(so_frame, int(round((1.0 + dem_g + 3.0) * fps)))
            canh["tuFrame"] = frame_hien_tai
            canh["denFrame"] = frame_hien_tai + so_frame
            frame_hien_tai += so_frame
    return du_lieu


def kiem_dinh_schema_du_lieu_canh(du_lieu: dict[str, Any]) -> list[str]:
    """
    Kiem dinh schema cho tung canh:
    - Canh boCuc='dong_thoi_gian' BAT BUOC co mocThoiGian hop le (khong duoc bo trong).
    - Canh co minhHoaToan BAT BUOC co du lieu thamSo / buocVe hop le theo dung loai minh hoa.
    - Chi canh cuoi cung cua hoi cuoi cung toan tap moi duoc dung boCuc='ket_thuc'.
    """
    loi: list[str] = []
    tat_ca_canh = [
        canh
        for ch in (du_lieu.get("chuong") or [])
        if isinstance(ch, dict)
        for canh in (ch.get("canh") or [])
        if isinstance(canh, dict)
    ]

    for idx, canh in enumerate(tat_ca_canh):
        cid = str(canh.get("id") or f"canh_{idx + 1:03d}")
        la_cuoi_toan_tap = idx == len(tat_ca_canh) - 1

        if not la_cuoi_toan_tap and canh.get("boCuc") == "ket_thuc":
            loi.append(f"[{cid}] Khong duoc dung boCuc='ket_thuc' o hoi giua (chi cho phep o canh cuoi toan tap).")

        if canh.get("boCuc") == "dong_thoi_gian":
            mocs = canh.get("mocThoiGian")
            hop_le = isinstance(mocs, list) and any(
                isinstance(m, dict)
                and (str(m.get("nam") or "").strip() or str(m.get("moTa") or "").strip())
                for m in mocs
            )
            if not hop_le:
                loi.append(f"[{cid}] boCuc='dong_thoi_gian' bi thieu du lieu mocThoiGian hop le.")

        mh = canh.get("minhHoaToan")
        if isinstance(mh, dict):
            loai = str(mh.get("loai") or "")
            ts = mh.get("thamSo") if isinstance(mh.get("thamSo"), dict) else {}
            if loai in ("tam_giac_vuong", "hinh_hoc_chung_minh"):
                a, b = ts.get("canhA"), ts.get("canhB")
                if not (
                    isinstance(a, (int, float)) and not isinstance(a, bool) and a > 0
                    and isinstance(b, (int, float)) and not isinstance(b, bool) and b > 0
                ):
                    loi.append(f"[{cid}] minhHoaToan '{loai}' thieu thamSo.canhA/canhB hop le.")
            elif loai == "truc_so_vo_ti":
                g, nhan = ts.get("giaTri"), ts.get("nhan")
                if not (
                    isinstance(g, (int, float)) and not isinstance(g, bool)
                    and isinstance(nhan, str) and nhan.strip()
                ):
                    loi.append(f"[{cid}] minhHoaToan 'truc_so_vo_ti' thieu thamSo.giaTri/nhan hop le.")
            elif loai == "do_thi_ham_so":
                ham = str(ts.get("ham") or "").strip()
                if ham not in LOAI_HAM_DO_THI:
                    loi.append(f"[{cid}] minhHoaToan 'do_thi_ham_so' thieu thamSo.ham hop le ({', '.join(LOAI_HAM_DO_THI)}).")
            elif loai == "chuoi_suy_luan":
                co_buoc_le = any(
                    isinstance(ts.get(f"buoc{i}"), str) and str(ts.get(f"buoc{i}")).strip()
                    for i in range(1, 9)
                )
                co_mang_buoc = isinstance(ts.get("buoc"), list) and any(
                    isinstance(x, str) and x.strip() for x in ts["buoc"]
                )
                if not (co_buoc_le or co_mang_buoc):
                    loi.append(f"[{cid}] minhHoaToan 'chuoi_suy_luan' thieu thamSo.buoc1..buoc4 hoac thamSo.buoc[].")
            elif loai == "tung_buoc":
                bv = mh.get("buocVe")
                if not isinstance(bv, list) or len(bv) == 0:
                    loi.append(f"[{cid}] minhHoaToan 'tung_buoc' thieu danh sach buocVe.")
            elif loai == "so_do_anh_xa":
                ct = ts.get("cotTrai")
                cp = ts.get("cotPhai")
                if not (isinstance(ct, list) and len(ct) >= 2 and isinstance(cp, list) and len(cp) >= 2):
                    loi.append(f"[{cid}] minhHoaToan 'so_do_anh_xa' thieu thamSo.cotTrai[] va cotPhai[] (>=2 phan tu).")
            elif loai == "luoi_duong_cheo":
                hang = ts.get("hang")
                if not (isinstance(hang, list) and len(hang) >= 2):
                    loi.append(f"[{cid}] minhHoaToan 'luoi_duong_cheo' thieu thamSo.hang[] (>=2 hang).")
            elif loai == "bieu_do_cot":
                nhan_c = ts.get("nhan")
                gt_c = ts.get("giaTri")
                if not (isinstance(nhan_c, list) and len(nhan_c) >= 2 and isinstance(gt_c, list) and len(gt_c) >= 2):
                    loi.append(f"[{cid}] minhHoaToan 'bieu_do_cot' thieu thamSo.nhan[] va giaTri[] (>=2 cot).")

    return loi


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
        phu_de_hoi = cat_gon_theo_tu(str(ch.get("phuDeHoi") or "").strip(), 140)
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
            if not phu_de_hoi:
                td_dau = next(
                    (
                        str(c.get("tieuDeNho") or "").strip()
                        for c in canh_list_sach
                        if str(c.get("tieuDeNho") or "").strip()
                    ),
                    "",
                )
                phu_de_hoi = cat_gon_theo_tu(
                    f"{ten_chuong} — {td_dau}" if td_dau else f"Khám phá diễn biến trọng tâm của {ten_chuong}.",
                    140,
                )
            tam_trang_md = KHUNG_6_HOI[idx_ch % len(KHUNG_6_HOI)].get("tamTrangNhacMacDinh", "vui_tuoi")
            tam_trang = chuan_hoa_enum(ch.get("tamTrangNhac"), TAM_TRANG_NHAC, str(tam_trang_md))
            muc_ch: dict[str, Any] = {
                "id": ch_id,
                "tenChuong": ten_chuong,
                "phuDeHoi": phu_de_hoi,
                "tamTrangNhac": tam_trang,
                "canh": canh_list_sach,
            }
            open_loop = cat_gon_theo_tu(str(ch.get("openLoopCuoiHoi") or "").strip(), 160)
            if open_loop:
                muc_ch["openLoopCuoiHoi"] = open_loop
            if canh_list_sach[0].get("boCuc") == "mo_dau" and not canh_list_sach[0].get("phuDeHoi"):
                canh_list_sach[0]["phuDeHoi"] = phu_de_hoi
            chuong_sach.append(muc_ch)

    # Chi cho phep boCuc='ket_thuc' o dung canh cuoi cung cua hoi cuoi cung toan tap
    tat_ca_canh = [c for ch in chuong_sach for c in ch["canh"]]
    for idx, c in enumerate(tat_ca_canh):
        if idx < len(tat_ca_canh) - 1 and c.get("boCuc") == "ket_thuc":
            c["boCuc"] = "ke_chuyen"

    ket_qua: dict[str, Any] = {
        "tieuDe": str(raw.get("tieuDe") or "Câu Chuyện Lịch Sử Toán Học").strip(),
        "chuDe": str(raw.get("chuDe") or "").strip(),
        "batSfx": bool(raw.get("batSfx", True)),
        "batPhuDe": bool(raw.get("batPhuDe", True)),
        "bangMau": bang_mau,
        "danhSachNhanVat": danh_sach_nv,
        "chuong": chuong_sach,
    }
    if isinstance(raw.get("mascotKenh"), dict):
        ket_qua["mascotKenh"] = raw["mascotKenh"]
    ds_boi_canh_ai = chuan_hoa_danh_sach_boi_canh_ai(raw.get("danhSachBoiCanhAI"))
    if ds_boi_canh_ai:
        ket_qua["danhSachBoiCanhAI"] = ds_boi_canh_ai
        tap_ma_ai = {m["maBoiCanhAI"]: m for m in ds_boi_canh_ai}
        for c in tat_ca_canh:
            ma_c = str(c.get("maBoiCanhAI") or "").strip()
            if ma_c and ma_c not in tap_ma_ai:
                # Khop mem theo boiCanh neu AI sinh sai ma nhe
                khop = next((m["maBoiCanhAI"] for m in ds_boi_canh_ai if m["boiCanh"] == c.get("boiCanh")), "")
                if khop:
                    c["maBoiCanhAI"] = khop
                else:
                    c.pop("maBoiCanhAI", None)
            elif not ma_c:
                khop = next(
                    (
                        m["maBoiCanhAI"]
                        for m in ds_boi_canh_ai
                        if m["loaiKhungHinh"] == "boi_canh" and m["boiCanh"] == c.get("boiCanh")
                    ),
                    "",
                )
                if khop:
                    c["maBoiCanhAI"] = khop
    if isinstance(raw.get("goiYThumbnail"), list) and raw.get("goiYThumbnail"):
        ket_qua["goiYThumbnail"] = chuan_hoa_goi_y_thumbnail(
            raw.get("goiYThumbnail"),
            danh_sach_nv=danh_sach_nv,
            tieu_de_video=ket_qua["tieuDe"],
        )
    gan_frame_uoc_luong(ket_qua)
    return ket_qua, tat_ca_canh_bao


# ==============================================================================
# 4. KIEN TRUC BIEN KICH 3 TANG (BLUEPRINT -> 6 HOI -> TU KIEM DINH & HOC HOI)
# ==============================================================================

def dinh_dang_tu_lieu_nghien_cuu(tu_lieu: dict[str, Any] | None) -> str:
    """Chuyen tu_lieu_nghien_cuu.json thanh doan ngu canh co dong cho prompt bien kich."""
    if not isinstance(tu_lieu, dict) or not tu_lieu:
        return ""

    dong: list[str] = ["=== TU LIEU NGHIEN CUU DA KIEM CHUNG (BAT BUOC BAM SAT) ==="]
    if tu_lieu.get("tomTat1Cau"):
        dong.append(f"- Tom tat cot loi: {tu_lieu['tomTat1Cau']}")

    nien_dai = tu_lieu.get("timeline_su_kien") or tu_lieu.get("nienDaiChuan") or []
    if nien_dai:
        dong.append("- Moc thoi gian (timeline_su_kien — BAT BUOC dung cho canh dong_thoi_gian):")
        for m in nien_dai[:8]:
            if isinstance(m, dict):
                noi_bat = " [NOI BAT]" if m.get("noiBat") else ""
                dong.append(f"  * {m.get('nam', '')}: {m.get('suKien') or m.get('moTa', '')}{noi_bat}")

    goi_y_bc = tu_lieu.get("goi_y_boi_canh_va_dao_cu") or []
    if goi_y_bc:
        dong.append("- Goi y boi canh, do tuoi, tu the & dao cu qua tung giai doan (KHOP 1-1):")
        for g in goi_y_bc[:8]:
            if isinstance(g, dict):
                dc_txt = ", ".join(g.get("daoCu") or []) or "khong"
                vt_txt = ", ".join(g.get("vatTheXungQuanh") or []) or "tu_dong"
                dong.append(
                    f"  * {g.get('giaiDoan', '')}: boiCanh={g.get('boiCanh', '')}, doTuoi={g.get('doTuoi', 'truong_thanh')}, "
                    f"tuThe={g.get('tuThe', 'dung')}, daoCu=[{dc_txt}], vatThe=[{vt_txt}]"
                )

    tu_dien_pa = tu_lieu.get("tu_dien_phat_am") or {}
    if isinstance(tu_dien_pa, dict) and tu_dien_pa:
        ds_ten = ", ".join(list(tu_dien_pa.keys())[:10])
        dong.append(
            f"- Ten rieng/thuat ngu chuan (GIU NGUYEN chinh ta goc tren man hinh/phu de, TTS se tu phien am): {ds_ten}"
        )

    nhan_vat = tu_lieu.get("nhanVatThat") or []
    if nhan_vat:
        dong.append("- Nhan vat lich su that:")
        for nv in nhan_vat[:6]:
            if isinstance(nv, dict):
                dong.append(
                    f"  * {nv.get('ten', '')} ({nv.get('nienDai', '')}) - {nv.get('vaiTro', '')}: "
                    f"{nv.get('tinhCachDoiThuong', '')}"
                )

    giai_thoai = tu_lieu.get("giaiThoaiDoiThuong") or []
    if giai_thoai:
        dong.append("- Giai thoai doi thuong / di dom co that:")
        for gt in giai_thoai[:5]:
            if isinstance(gt, dict):
                dong.append(
                    f"  * {gt.get('tieuDe', '')}: {gt.get('noiDung', '')} "
                    f"(Diem hai: {gt.get('diemHaiHuoc', '')})"
                )

    kien_thuc = tu_lieu.get("kienThucToanCotLoi") or []
    if kien_thuc:
        dong.append("- Kien thuc & chung minh Toan cot loi:")
        for kt in kien_thuc[:4]:
            if isinstance(kt, dict):
                dong.append(
                    f"  * {kt.get('tenKienThuc', '')} | LaTeX: `{kt.get('congThucLatex', '')}` | "
                    f"Giai thich: {kt.get('giaiThichDeHieu', '')}"
                )

    ung_dung = tu_lieu.get("ungDungHienDai") or []
    if ung_dung:
        dong.append("- Ung dung hien dai: " + "; ".join(str(x) for x in ung_dung[:5]))

    return "\n".join(dong)


def tao_prompt_tang_1(
    chu_de: str,
    muc_tieu_phut: float,
    giong_ke: str,
    tu_lieu_nghien_cuu: dict[str, Any] | None = None,
    ngu_canh_hoc_hoi: str = "",
) -> str:
    """Tang 1: Dan y 6 Hoi (Story Blueprint) khoa danhSachNhanVat va mach boiCanh/thoiTiet."""
    mo_ta_6_hoi = "\n".join(
        f"  {h['soHoi']}. Hoi {h['soHoi']} ({h['vaiTro']}, ~{h['phutMucTieu']} phut, muc tieu {h['tuMucTieu']} tu): {h['yeuCauDacBiet']}"
        for h in KHUNG_6_HOI
    )
    khoi_tu_lieu = dinh_dang_tu_lieu_nghien_cuu(tu_lieu_nghien_cuu)
    khoi_bo_nho = ngu_canh_hoc_hoi.strip()
    phan_phu = "\n\n".join(x for x in (khoi_tu_lieu, khoi_bo_nho) if x)
    if phan_phu:
        phan_phu = "\n\n" + phan_phu + "\n"

    return f"""
Hay thiet ke DAN Y 6 HOI (Story Blueprint) cho 1 tap phim hoat hinh 2D ke chuyen lich su Toan hoc dai khoang {muc_tieu_phut:.1f} phut (CHAC CHAN > 10 phut, tong 1.750-2.150 tu).
- Chu de: "{chu_de}"
- Giong ke: "{giong_ke}" (thien nhien + hai huoc di dom, KHONG danh dam bao luc, giai thich Toan de hieu, co chieu sau lich su)
{phan_phu}
CAU TRUC 6 HOI BAT BUOC:
{mo_ta_6_hoi}

DANH SACH ENUM HOP LE (BAT BUOC CHI CHON TRONG CAC GIA TRI NAY):
- phuKien: {", ".join(LOAI_PHU_KIEN)}
- trangPhuc: {", ".join(LOAI_TRANG_PHUC)}
- kieuToc: {", ".join(LOAI_KIEU_TOC)}
- coRau: {", ".join(LOAI_CO_RAU)}
- doTuoi: {", ".join(DO_TUOI_NHAN_VAT)}
- tuThe: {", ".join(TU_THE_NHAN_VAT)}
- boiCanh (22 boi canh): {", ".join(LOAI_BOI_CANH)}
- thoiTiet: {", ".join(LOAI_THOI_TIET)}
- daoCuNoiBat (20 dao cu): {", ".join(LOAI_DAO_CU)}
- vatTheXungQuanh (10 sinh vat/do vat): {", ".join(LOAI_VAT_THE_XUNG_QUANH)}
- gocQuay (12 goc may v3.0): {", ".join(GOC_QUAY_CAMERA)}
- bieuCam: {", ".join(LOAI_BIEU_CAM)}
- tamTrangNhac (4 sac thai nhac nen theo tung Hoi v3.5): {", ".join(TAM_TRANG_NHAC)}
- boCuc ke chuyen moi (v3.5): ban_do_hanh_trinh (phuongTien: {", ".join(PHUONG_TIEN_HANH_TRINH)}), bao_chi_co, phan_ung_cam (kieuPhanUng: {", ".join(KIEU_PHAN_UNG_CAM)})

YEU CAU KHOA TINH NHAT QUAN v3.5 (2 VAI: BIEN KICH KE CHUYEN + DAO DIEN STORYBOARD & BOI CANH AI):
1. HO SO TAO HINH NHAN VAT CO DINH & MASCOT KENH (`{ID_MASCOT_KENH}`): Khoa 2-4 nhan vat lich su co dinh trong `danhSachNhanVat` voi HO SO TAO HINH CO DINH (`trangPhuc`, `kieuToc`, `coRau`, `mauAo`, `phuKien`, `doTuoi`). Dong thoi su dung Mascot dan chuyen co dinh cua kenh (`id: "{ID_MASCOT_KENH}"`, ten "{MASCOT_KENH_MAC_DINH['ten']}") cho 15 giay Cold Open mo man, cac canh do khan gia (`tuong_tac_khan_gia`) va 15 giay End-Screen cuoi tap.
2. DANH SACH BOI CANH MINH HOA AI (`danhSachBoiCanhAI[]`): Thiet ke san 14-20 dia diem boi canh (`loaiKhungHinh: "boi_canh"`) + 4-6 khung tranh dac ta can canh vat the/ban do/so tay/kien truc (`loaiKhungHinh: "can_canh_vat_the"`) bang tieng Anh suc tich (`moTaTiengAnh` mo ta ro boi canh, anh sang, thoi dai lich su, KHONG co nguoi) de truyen thang cho `tao_boi_canh_ai.py`.
3. COLD OPEN 15 GIAY DAU (`hookMoMan`) & AN DU HIEN DAI HAI HUOC: Chon 1 nghich ly Toan hoc gay soc, an du doi song/cong nghe hien dai hai huoc (vi du: Wi-Fi rot mang, drama mang xa hoi, GPS, kiem tra 15 phut...) hoac tinh huong do khoc do cuoi de mo man ngay giay thu 0 cung Mascot kenh (CAM tuyet doi mo bai tieu su sach giao khoa kieu "X sinh nam ... tai ...").
4. NHAC NEN DA CAM XUC (`tamTrangNhac`) & OPEN LOOP CUOI MOI HOI (`openLoopCuoiHoi`): Gan `tamTrangNhac` (`vui_tuoi | bi_an | kich_tinh | tram_lang`) cho TUNG hoi de FFmpeg crossfade 1.5s muot ma giua cac hoi; moi Hoi 1..5 BAT BUOC co `openLoopCuoiHoi` (1 cau moc noi bo ngo gay to mo keo khan gia xem tiep hoi ke tiep).
5. BEAT-DRIVEN 1-1, DA DANG BOI CANH & 3 KHUNG HINH KE CHUYEN MOI v3.5: Thiet ke mach chuyen doi `boiCanhChinh` va `thoiTietChinh` qua 6 hoi voi TOI THIEU 6 BOI CANH KHAC NHAU; phan bo hop ly trong 6 hoi it nhat 1-2 canh `ban_do_hanh_trinh`, 1-2 canh `bao_chi_co` va 2-3 canh `phan_ung_cam` (1.5-2.5s). KHONG chon `nha_co_phong_sinh` cho canh nguoi gia / nhan giai thuong / cuoi doi.
6. CHONG LAP Y GIUA CAC HOI & PHU DE HOI RIENG BIET: Moi hoi trong `cacHoi[]` BAT BUOC co `phuDeHoi` RIENG BIET (1 cau tieng Viet co dau 8-18 tu mo ta dung noi dung rieng cua hoi do, CAM dung chung 1 cau cho nhieu hoi). Phan bo giai thoai, cuoc doi thoai va kien thuc Toan doc lap cho tung hoi. Du kien san 2-3 cau do tuong tac khan gia (`tuong_tac_khan_gia`) rai deu o Hoi 2, Hoi 4 va Hoi 5.
7. DE XUAT 3 PHUONG AN THUMBNAIL A/B (`goiYThumbnail` gom `bien_the` 1, 2, 3) de chay YouTube Test & Compare: moi phuong an co `tieuDeLon` toi da 2-4 tu gay to mo tuong phan cao, 1 `congThucLatex` cot loi, 1 `daoCuNoiBat` va `bieuCam` manh.
8. BAT BUOC 100% TIENG VIET CO DAU DAY DU cho moi tieu de, phuDeHoi, openLoopCuoiHoi, mo ta, ten nhan vat, diem hai huoc; TUYET DOI CAM viet tieng Viet khong dau (ngoai tru truong `moTaTiengAnh` trong `danhSachBoiCanhAI[]`)!

Tra ve DUY NHAT JSON dung cau truc sau:
{{
  "tieuDe": "Tiêu đề video hấp dẫn bằng tiếng Việt có dấu",
  "chuDe": "Mô tả ngắn 1 câu gây tò mò bằng tiếng Việt có dấu",
  "hookMoMan": {{
    "loaiHook": "nghich_ly | cau_do_meo | tinh_huong_do_khoc_do_cuoi",
    "moTa20_30s": "Kịch bản tóm tắt 3-5 cảnh đầu (20-30 giây) kéo người xem vào nghịch lý hoặc tình huống oái oăm trước khi quay lại kể diễn biến...",
    "cauMoDauGaySoc": "1 câu mở màn ngắn gọn bất ngờ ngay giây thứ 0..."
  }},
  "goiYThumbnail": [
    {{
      "bien_the": 1,
      "tieuDeLon": "CON SỐ BỊ CẤM!",
      "nhanPhu": "SỰ THẬT SỐC",
      "congThucLatex": "\\\\sqrt{{2}} \\\\notin \\\\mathbb{{Q}}",
      "daoCuNoiBat": "compa_co",
      "boiCanh": "quang_truong_hy_lap",
      "nhanVatId": "ten_khong_dau",
      "bieuCam": "ngac_nhien",
      "hanhDong": "giat_minh_nhay_dung",
      "mauNhan": "#FACC15"
    }},
    {{
      "bien_the": 2,
      "tieuDeLon": "NGHỊCH LÝ CHẤN ĐỘNG",
      "nhanPhu": "CÂU CHUYỆN CÓ THẬT",
      "congThucLatex": "a^2 + b^2 = c^2",
      "daoCuNoiBat": "khoi_da_dien",
      "boiCanh": "dai_thien_van_phuc_hung",
      "nhanVatId": "ten_khong_dau",
      "bieuCam": "hoang_mang",
      "hanhDong": "ho_het_sung_suong",
      "mauNhan": "#38BDF8"
    }},
    {{
      "bien_the": 3,
      "tieuDeLon": "GIẢI MÃ TRONG 10P",
      "nhanPhu": "TOÁN HỌC DỄ HIỂU",
      "congThucLatex": "a^2 + b^2 = c^2",
      "daoCuNoiBat": "kinh_thien_van",
      "boiCanh": "lop_hoc_bang_xanh",
      "nhanVatId": "ten_khong_dau",
      "bieuCam": "tinh_quai",
      "hanhDong": "chi_tro_giai_thich",
      "mauNhan": "#FACC15"
    }}
  ],
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
      "ten": "Tên Hiển Thị Có Dấu",
      "mauThan": "#1E293B",
      "mauChuDao": "#2563EB",
      "mauDa": "#FFFDF7",
      "phuKien": "kinh_tron",
      "trangPhuc": "ao_vest_co_dien",
      "kieuToc": "gon_gang",
      "coRau": "ria_mep",
      "mauAo": "#1D4ED8"
    }}
  ],
  "danhSachBoiCanhAI": [
    {{
      "maBoiCanhAI": "bc_01_giang_duong_sang",
      "loaiKhungHinh": "boi_canh",
      "boiCanh": "giang_duong_dai_hoc",
      "thoiTiet": "nang_dep",
      "moTaTiengAnh": "19th-century European wooden university lecture hall with tall arched windows, warm morning sunbeams, large chalkboard and empty flat wooden floor in lower third, no people"
    }},
    {{
      "maBoiCanhAI": "cc_01_so_tay_nen",
      "loaiKhungHinh": "can_canh_vat_the",
      "boiCanh": "thu_vien_co_dien",
      "thoiTiet": "ban_dem",
      "daoCuChinh": "cuon_giay",
      "moTaTiengAnh": "Close-up tabletop illustration of an open antique leather notebook with geometric diagrams, brass compass and warm flickering candle on an oak desk, no text, no people"
    }}
  ],
  "cacHoi": [
    {{
      "soHoi": 1,
      "id": "chuong_1",
      "tenChuong": "1. Tên hồi cuốn hút bằng tiếng Việt có dấu",
      "phuDeHoi": "Câu mô tả riêng biệt tóm gọn nội dung chính của hồi 1 (không trùng hồi khác).",
      "tamTrangNhac": "bi_an",
      "openLoopCuoiHoi": "Câu móc nối bỏ ngỏ cuối hồi kéo người xem sang hồi tiếp theo...",
      "boiCanhChinh": "bo_bien_hy_lap",
      "thoiTietChinh": "nang_dep",
      "tomTat": "Tóm tắt diễn biến hồi...",
      "diemHaiHuoc": ["Miếng hài 1 kèm ẩn dụ hiện đại...", "Miếng hài 2..."],
      "kienThucToan": "Ý tưởng Toán học & công thức dự kiến..."
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
    tu_lieu_nghien_cuu: dict[str, Any] | None = None,
    ngu_canh_hoc_hoi: str = "",
    su_kien_da_dung: list[str] | None = None,
) -> str:
    """Tang 2: Viet chi tiet 16-22 canh ngan cho 1 Hoi (2 vai: Bien kich ke chuyen + Dao dien Storyboard)."""
    nv_json = json.dumps(blueprint["danhSachNhanVat"], ensure_ascii=False)
    ds_bc_ai = blueprint.get("danhSachBoiCanhAI") if isinstance(blueprint.get("danhSachBoiCanhAI"), list) else []
    bc_ai_json = (
        json.dumps(
            [
                {
                    "maBoiCanhAI": m.get("maBoiCanhAI"),
                    "loaiKhungHinh": m.get("loaiKhungHinh", "boi_canh"),
                    "boiCanh": m.get("boiCanh"),
                    "thoiTiet": m.get("thoiTiet"),
                }
                for m in ds_bc_ai[:24]
                if isinstance(m, dict)
            ],
            ensure_ascii=False,
        )
        if ds_bc_ai
        else "[]"
    )
    khoi_tu_lieu = dinh_dang_tu_lieu_nghien_cuu(tu_lieu_nghien_cuu)
    khoi_bo_nho = ngu_canh_hoc_hoi.strip()
    khoi_chong_lap = ""
    if su_kien_da_dung:
        ds_da_dung = "\n".join(f"- {sk}" for sk in su_kien_da_dung[-18:])
        khoi_chong_lap = (
            "=== DANH SACH SU KIEN / GIAI THOAI DA KE O CAC HOI TRUOC (CAM LAP LAI!) ===\n"
            "Tuyet doi KHONG ke lai, giai thich lai hay binh luan trung lap cac y sau:\n"
            f"{ds_da_dung}"
        )
    khoi_hook = ""
    if khung_hoi["soHoi"] == 1:
        hook_bp = blueprint.get("hookMoMan") if isinstance(blueprint.get("hookMoMan"), dict) else {}
        mo_ta_hook = str(hook_bp.get("moTa20_30s") or "").strip()
        cau_mo_dau = str(hook_bp.get("cauMoDauGaySoc") or "").strip()
        chi_tiet_hook = ""
        if mo_ta_hook or cau_mo_dau:
            chi_tiet_hook = (
                f"\n- Dinh huong Hook tu Dan y: {mo_ta_hook}"
                + (f"\n- Cau mo dau goi y: \"{cau_mo_dau}\"" if cau_mo_dau else "")
            )
        khoi_hook = (
            "=== YEU CAU BAT BUOC v3.5: COLD OPEN 15 GIAY DAU / HOOK 20-30 GIAY DAU (2-3 CANH DAU TIEN) ===\n"
            f"- 2-3 canh dau tien (tong 40-58 tu, tuong duong 15 giay) PHAI co Mascot kenh (`id: \"{ID_MASCOT_KENH}\"`) "
            "di thang vao nghich ly Toan hoc gay soc, an du hien dai hai huoc hoac tinh huong do khoc do cuoi TRUOC KHI quay lai ke dien bien lich su.\n"
            "- CAM mo bai kieu tieu su sach giao khoa ('Sinh nam ... tai ...') hay loi chao hoi thong thuong.\n"
            "- Doi goc may/bo cuc nhanh moi 4-5 giay (`can_mat`, `trung_canh`, `zoom_dao_cu`, `pan_ngang`) "
            "va chen it nhat 1 diem nhan hai (`hieuUngHoatHinh` hoac `ngatNhacPunchline: true`)."
            f"{chi_tiet_hook}"
        )
    phan_phu = "\n\n".join(x for x in (khoi_hook, khoi_chong_lap, khoi_tu_lieu, khoi_bo_nho) if x)
    if phan_phu:
        phan_phu = "\n\n" + phan_phu + "\n"

    luu_y_outro = (
        "CAM TUYET DOI chuoi 'CẢM ƠN' / 'Cảm ơn bạn đã theo dõi' va CAM `boCuc='ket_thuc'` o hoi nay (chi danh cho canh cuoi Hoi 6)!"
        if khung_hoi["soHoi"] < 6
        else "CHI canh CUOI CUNG cua Hoi 6 moi duoc dung `boCuc='ket_thuc'`."
    )
    yeu_cau_tuong_tac_hoi = (
        "BAT BUOC chen it nhat 1 canh `loaiCanh='tuong_tac_khan_gia'` trong hoi nay (nhan vat dung `hanhDong='quay_nhin_khan_gia'`, `tuongTacVoi='khan_gia'`, co `cauHoiTuongTac` gom `cauHoi`, `thoiGianDemNguocGiay: 3`, `dapAn`, `giaiThichNgan`)."
        if khung_hoi["soHoi"] in (2, 4, 5)
        else "Co the chen them 1 canh `tuong_tac_khan_gia` neu phu hop nhip ke."
    )

    return f"""
Ban dang dam nhiem 2 VAI (BIEN KICH KE CHUYEN + DAO DIEN STORYBOARD) de viet CHI TIET HOI {khung_hoi['soHoi']}/6 cho phim hoat hinh Toan hoc:
- Tieu de phim: "{blueprint['tieuDe']}"
- Giong ke: "{giong_ke}" (phong cach thien nhien + hai huoc di dom, KHONG danh dam)
- Ten hoi: "{thong_tin_hoi['tenChuong']}"
- Phu de mo hoi rieng biet (`phuDeHoi`): "{thong_tin_hoi.get('phuDeHoi') or thong_tin_hoi['tomTat']}"
- Vai tro hoi: {khung_hoi['vaiTro']}
- Boi canh chu dao: {thong_tin_hoi['boiCanhChinh']} | Thoi tiet chu dao: {thong_tin_hoi['thoiTietChinh']}
- Tom tat hoi nay: {thong_tin_hoi['tomTat']}
- Mieng hai du kien: {json.dumps(thong_tin_hoi.get('diemHaiHuoc', []), ensure_ascii=False)}
- Kien thuc Toan trong tam: {thong_tin_hoi.get('kienThucToan', '')}
- Mach noi tu hoi truoc: {tom_tat_hoi_truoc}
- Danh sach nhan vat CO DINH (chi duoc dung dung id trong nay; giu nguyen ho so trangPhuc/kieuToc/coRau/mauAo xuyen suot tap): {nv_json}
- Danh sach boi canh minh hoa AI da quy hoach (`maBoiCanhAI` de anh xa vao TUNG canh): {bc_ai_json}
{phan_phu}
=== VAI 1: BIEN KICH KE CHUYEN v3.5 ===
1. Sinh tu {khung_hoi['soCanh']} canh ngan (toi thieu 16 canh). Moi canh co `loiThoai` dai 16-28 tu tieng Viet tu nhien (TRANG canh dai >32 tu; rieng canh `phan_ung_cam` rat ngan 4-8 tu tuong duong 1.5-2.5 giay). TONG SO TU cua hoi nay BAT BUOC dat {khung_hoi['tuMucTieu']} tu (khong duoc duoi 260 tu).
2. DOI THOAI SAC BEN, AN DU HIEN DAI HAI HUOC & OPEN LOOP CUOI HOI (BAT BUOC):
   - Moi hoi PHAI co it nhat 3 canh `loaiCanh="doi_thoai"` (`boCuc="doi_thoai"`) voi mang `luotThoai[]` **3-5 luot ngan sac ben (8-22 tu/luot)**, `mayQuay: {{"gocQuay": "dao_goc_can_mat", "tuDongFocusNguoiNoi": true}}`, `kieuBongBong` da dang (`thuong`, `quat_thao`, `suy_nghi`, `ca_khia`).
   - Long ghep AN DU HIEN DAI HAI HUOC (so sanh khai niem Toan/lich su voi Wi-Fi rot mang, thuat toan Google Maps, drama mang xa hoi, deadline nop bai...) de giai thich vua di dom vua de hieu.
   - Cuoi hoi (Hoi 1..5) BAT BUOC dat 1 CAU MOC NOI OPEN LOOP (`openLoopCuoiHoi` va o cau ket canh cuoi hoi) bo ngo tinh tiet bat ngo keo khan gia xem tiep hoi sau.
3. NHAC NEN DA CAM XUC (`tamTrangNhac`) & NGAT NHAC PUNCHLINE (`ngatNhacPunchline`):
   - Giu dung sac thai `tamTrangNhac` cho hoi nay (`{thong_tin_hoi.get('tamTrangNhac') or khung_hoi.get('tamTrangNhacMacDinh', 'vui_tuoi')}` trong: {", ".join(TAM_TRANG_NHAC)}).
   - Gan `"ngatNhacPunchline": true` cho 1 canh punchline hai dat gia nhat trong hoi (neu phu hop) de FFmpeg ngat nhac dot ngot 0.8s tang do bat cuoi.
4. PHAN BO 3 KIEU KHUNG HINH KE CHUYEN MOI v3.5 & MASCOT KENH (`{ID_MASCOT_KENH}`):
   - `boCuc="ban_do_hanh_trinh"` kem `banDoHanhTrinh: {{"diemDi", "diemDen", "phuongTien": "tau_thuy|thu_tay|nguoi_di_bo|xe_ngua", "khoangCachNhan", "moTaHanhTrinh"}}` khi co chuyen di/gui thu/di cu lich su.
   - `boCuc="bao_chi_co"` kem `baoChiCo: {{"tenToBao", "ngayPhatHanh", "tieuDeBao", "tieuDePhu", "nhanAnhMinhHoa", "daoCuMinhHoa"}}` khi co phat minh chan dong / tranh cai hoc thuat.
   - `boCuc="phan_ung_cam"` (1.5-2.5s) kem `phanUngCam: {{"nhanVatId", "kieuPhanUng": "nhap_tra|nhuong_may|tron_mat|can_loi", "chuHieuUng"}}` de cat nhanh can mat phan ung hai ngay sau cau thoai gay soc.
   - Cho Mascot kenh (`id: "{ID_MASCOT_KENH}"`) xuat hien o Cold Open 15s (Hoi 1), canh `tuong_tac_khan_gia`, va canh cuoi `ket_thuc` 15s (Hoi 6 kem `endScreen: {{"khungTraiNhan", "khungPhaiNhan", "loiDanXemTiep"}}`).
5. NHIP TUONG TAC KHAN GIA: {yeu_cau_tuong_tac_hoi}
6. {luu_y_outro}
7. Yeu cau dac biet cua Hoi {khung_hoi['soHoi']}: {khung_hoi['yeuCauDacBiet']}

=== VAI 2: DAO DIEN STORYBOARD & DIEN ANH v3.0 ===
7. ANH XA `maBoiCanhAI` 1-1 & KHUNG TRANH DAC TA (6-12 GIAY DOI GOC MAY/BOI CANH):
   - Moi canh BAT BUOC gan `maBoiCanhAI` khop 100% voi `danhSachBoiCanhAI[]` va loi ke. Cu moi 6-12 giay phai doi goc may (`can_mat_trai`, `can_mat_phai`, `can_mat_kich_tinh`, `dao_goc_can_mat`, `trung_canh`, `toan_canh`) hoac chuyen sang `maBoiCanhAI` moi.
   - Xen ke 1-2 canh `laKhungTranhDacTa: true` (dung ma `cc_*` cua khung tranh can canh ban do/so tay/kien truc, `nhanVat: []`) de tao nhip dien anh.
   - Khi loi thoai doi moc doi, tuoi tac hoac dia diem, BAT BUOC doi `boiCanh`, `doTuoi`, `tuThe`, `daoCu`, `vatTheXungQuanh` tuong ung ngay lap tuc (nhac moi sinh -> `nha_co_phong_sinh` + `so_sinh`; vuot bien -> `cang_bien_tau_thuy`; benh vien -> `phong_benh_vien` + `nam_giuong`; giang duong -> `giang_duong_dai_hoc`). KHONG hardcode bien so xe `"1729"` (chi gan `bienSoXe` khi cau chuyen thuc su nhac bien so do).
8. DAO DIEN CAMERA CAN MAT, NHIP NGAT THI GIAC 6-8 GIAY & BIEU CAM DONG (CAM LAP):
   - LUAT NHIP NGAT THI GIAC 6-8 GIAY: Khong de canh nao hoac chuoi canh lien tiep dung yen cung 1 boCuc/camera='tinh' qua 6-8 giay.
   - Gan `mayQuay.gocQuay` da dang cho MOI canh (uu tien goc can mat dien anh: `can_mat_trai`, `can_mat_phai`, `can_mat_kich_tinh`, `dao_goc_can_mat`, `trung_canh`, `toan_canh`, `zoom_dao_cu`, `pan_ngang`).
   - CAM TUYET DOI 2 canh lien tiep trung CA `boiCanh` LAN `mayQuay.gocQuay`!
   - Dung `bieuCamTheoMoc` (`[{{"tienDo": 0.0, "bieuCam": "tram_tu"}}, {{"tienDo": 0.55, "bieuCam": "ngac_nhien"}}]`) cho nhan vat o cac canh chuyen bien cam xuc, va gan `vatTheXungQuanh` phu hop cho moi canh.
9. DU LIEU TOAN, TIMELINE, CHONG DE CHU & TIENG VIET CO DAU (BAT BUOC):
   - BAT BUOC 100% van ban tieng Viet (tieuDeNho, phuDeHoi, loiThoai, luotThoai[].noiDung, bongBongThoai, mocThoiGian[].moTa, minhHoaToan, congThucLatex[].nhan, cauHoiTuongTac) PHAI CO DAU DAY DU, dung chinh ta. CAM viet tieng Viet khong dau!
   - CAM dat `loiBinhHaiHuoc` tren cac canh `boCuc="giai_thich_toan"`, `loaiCanh="giang_toan"` hoac `boCuc="dong_thoi_gian"`.
   - CAM 1 `nhanVatId` xuat hien 2 lan trong cung 1 mang `nhanVat[]` cua 1 canh.
   - RANG BUOC BOI CANH/THOI TIET: CAM `la_vang_gio` va `thoiTiet="la_roi"` trong phong kin (`giang_duong_dai_hoc`, `thu_vien_co_dien`, `phong_tro_bep_lua`, `phong_benh_vien`, `lop_hoc_bang_xanh`...); CAM `ngon_nen_den_dau` trong `khong_gian_vu_tru_toan`; CAM `nha_co_phong_sinh` cho canh nguoi gia / nhan giai thuong / cuoi doi.
   - Trong `congThucLatex`: dung LaTeX chuan KaTeX (thoat dau \\ thanh \\\\ trong JSON, khong boc dau $).
   - Canh `giai_thich_toan` / `loaiCanh="giang_toan"` BAT BUOC co `congThucLatex[]` va `minhHoaToan` truc quan day du tham so (se hien thi tren cuon giay da / bang phan khung go):
     * `so_do_anh_xa`, `luoi_duong_cheo`, `bieu_do_cot`, `tam_giac_vuong`, `truc_so_vo_ti`, `do_thi_ham_so`, `hinh_hoc_chung_minh`, `chuoi_suy_luan`, hoac `buocVe` cho `loai="tung_buoc"` (co hinh ve that, CAM khung rong!).
   - Canh `dong_thoi_gian` BAT BUOC co `mocThoiGian[]` gom 3-5 moc that lay tu `timeline_su_kien` (moi `moTa` ngan gon 8-14 tu tron ven, khong cat cut).
10. CHI DUNG DUNG CAC GIA TRI ENUM SAU:
   - boCuc: {", ".join(LOAI_BO_CUC)}
   - loaiCanh: {", ".join(LOAI_CANH)}
   - vaiNoi: {", ".join(LOAI_VAI_NOI)}
   - boiCanh: {", ".join(LOAI_BOI_CANH)}
   - thoiTiet: {", ".join(LOAI_THOI_TIET)}
   - chuyenCanh: {", ".join(LOAI_CHUYEN_CANH)}
   - camera.kieu: {", ".join(KIEU_CAMERA)}
   - mayQuay.gocQuay: {", ".join(GOC_QUAY_CAMERA)}
   - kieuBongBong: {", ".join(KIEU_BONG_BONG_CHAT)}
   - doTuoi: {", ".join(DO_TUOI_NHAN_VAT)}
   - tuThe: {", ".join(TU_THE_NHAN_VAT)}
   - hanhDong: {", ".join(LOAI_HANH_DONG)}
   - bieuCam: {", ".join(LOAI_BIEU_CAM)}
   - vatCamTay: {", ".join(LOAI_VAT_CAM_TAY)}
   - hieuUngHoatHinh.loai: {", ".join(LOAI_HIEU_UNG_HOAT_HINH)}
   - minhHoaToan.loai: {", ".join(LOAI_MINH_HOA_TOAN)}
   - daoCu.loai: {", ".join(LOAI_DAO_CU)}
   - vatTheXungQuanh.loai: {", ".join(LOAI_VAT_THE_XUNG_QUANH)}
11. Toa do 1920x1080: nhan vat dung mat dat tai y=810, x khoang 560..1360 (rieng canh `giai_thich_toan` dat nhan vat x=255, y=808 de nhuong bang xanh ben phai).

Tra ve DUY NHAT JSON dung cau truc:
{{
  "id": "{khung_hoi['id']}",
  "tenChuong": "{thong_tin_hoi['tenChuong']}",
  "phuDeHoi": "{thong_tin_hoi.get('phuDeHoi') or thong_tin_hoi['tomTat']}",
  "tamTrangNhac": "{thong_tin_hoi.get('tamTrangNhac') or khung_hoi.get('tamTrangNhacMacDinh', 'vui_tuoi')}",
  "openLoopCuoiHoi": "{thong_tin_hoi.get('openLoopCuoiHoi') or 'Câu móc nối bỏ ngỏ kéo người xem sang hồi tiếp theo...'}",
  "tomTatKetHoi": "1-2 câu tóm tắt điểm kết hồi để nối mạch sang hồi sau",
  "suKienDaKe": ["Tóm tắt ngắn giai thoại/mốc chính 1 đã kể trong hồi này", "Mốc chính 2..."],
  "canh": [
    {{
      "boCuc": "ke_chuyen",
      "loaiCanh": "ke_chuyen",
      "vaiNoi": "nguoi_dan",
      "boiCanh": "{thong_tin_hoi['boiCanhChinh']}",
      "thoiTiet": "{thong_tin_hoi['thoiTietChinh']}",
      "chuyenCanh": "mo_dan",
      "namMoc": "1914",
      "tieuDeNho": "Tiêu đề ngắn gọn có dấu",
      "loiThoai": "Lời thoại tiếng Việt có dấu tự nhiên dài 16-26 từ...",
      "camera": {{"kieu": "pan_nhe"}},
      "mayQuay": {{"gocQuay": "trung_canh", "tuDongFocusNguoiNoi": true}},
      "vatTheXungQuanh": [{{"loai": "chim_san_truong", "soLuong": 3}}],
      "nhanVat": [
        {{
          "id": "{blueprint['danhSachNhanVat'][0]['id']}",
          "x": 760,
          "y": 810,
          "huong": "phai",
          "doTuoi": "truong_thanh",
          "tuThe": "dung",
          "hanhDong": "chi_tro_giai_thich",
          "vatCamTay": "cuon_giay",
          "bieuCam": "vui_tuoi",
          "bieuCamTheoMoc": [{{"tienDo": 0.0, "bieuCam": "tram_tu"}}, {{"tienDo": 0.6, "bieuCam": "vui_tuoi"}}],
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
Hồi "{thong_tin_hoi['tenChuong']}" hiện mới có {so_tu_hien_tai} từ (quá ngắn, cần thêm khoảng {can_them} từ).
Hãy viết BỔ SUNG thêm 4-5 cảnh kể chi tiết giai thoại lịch sử mới (KHÔNG lặp lại ý đã kể), ví dụ đời sống dễ hiểu hoặc 1 tình huống hài hước dí dỏm để chèn ngay trước cảnh kết của hồi này.
- Mạch đang kể: "{doan_cuoi}"
- Nhân vật cố định: {json.dumps(blueprint['danhSachNhanVat'], ensure_ascii=False)}
- Bối cảnh chủ đạo: {thong_tin_hoi['boiCanhChinh']} | Thời tiết: {thong_tin_hoi['thoiTietChinh']}
- Mỗi cảnh dài 22-35 từ, dùng đúng enum của hệ thống, BẮT BUỘC 100% tiếng Việt có dấu đầy đủ (CẤM viết không dấu).

Trả về DUY NHẤT JSON:
{{
  "canhBoSung": [
    {{
      "boCuc": "ke_chuyen",
      "boiCanh": "{thong_tin_hoi['boiCanhChinh']}",
      "thoiTiet": "{thong_tin_hoi['thoiTietChinh']}",
      "tieuDeNho": "Chi tiết thú vị",
      "loiThoai": "Lời thoại tiếng Việt có dấu tự nhiên dài 24-34 từ...",
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


_CAMERA_DONG_LUAN_PHIEN: tuple[str, ...] = ("pan_nhe", "zoom_cham", "zoom_hai_huoc")
_HANH_DONG_DONG_LUAN_PHIEN: tuple[str, ...] = (
    "chi_tro_giai_thich",
    "di_qua_di_lai",
    "gat_gu_dong_tinh",
    "nhin_len_troi",
    "gai_dau_kho_hieu",
    "khoanh_tay_tu_man",
)


def _uoc_luong_giay_canh(canh: dict[str, Any], fps: int = 30, tu_moi_giay: float = 2.65) -> float:
    """Uoc luong thoi luong canh (giay) uu tien tuFrame/denFrame, fallback theo so tu."""
    tu_f = canh.get("tuFrame")
    den_f = canh.get("denFrame")
    if isinstance(tu_f, (int, float)) and isinstance(den_f, (int, float)) and den_f > tu_f:
        return (float(den_f) - float(tu_f)) / float(max(1, fps))
    so_tu = dem_tu(str(canh.get("loiThoai") or ""))
    return max(3.5, so_tu / tu_moi_giay) + 0.25


def suy_luan_vai_noi_canh(canh: dict[str, Any]) -> str:
    """Xac dinh vai noi (nguoi_dan | nhan_vat | binh_luan_hai) cho 1 canh."""
    vai_hien_tai = canh.get("vaiNoi")
    if isinstance(vai_hien_tai, str) and vai_hien_tai.strip().lower() in LOAI_VAI_NOI:
        return vai_hien_tai.strip().lower()

    bo_cuc = str(canh.get("boCuc") or "")
    loi_thoai = str(canh.get("loiThoai") or "")
    co_loi_binh = isinstance(canh.get("loiBinhHaiHuoc"), dict) and bool(
        str(canh["loiBinhHaiHuoc"].get("noiDung") or "").strip()
    )
    cam_kieu = str((canh.get("camera") or {}).get("kieu") or "tinh")

    if bo_cuc == "hai_huoc" or (co_loi_binh and cam_kieu == "zoom_hai_huoc"):
        return "binh_luan_hai"

    co_bong_bong = any(
        isinstance(nv, dict) and bool(str(nv.get("bongBongThoai") or "").strip())
        for nv in (canh.get("nhanVat") or [])
    )
    co_trich_dan = bool(re.search(r'[“"«][^“"»]{4,}[”"»]', loi_thoai))
    if bo_cuc == "doi_thoai" or co_bong_bong or co_trich_dan:
        return "nhan_vat"

    return "nguoi_dan"


def _tach_loi_thoai_hai_canh(loi_thoai: str, tu_toi_thieu_moi_phan: int = 8) -> tuple[str, str] | None:
    """
    Thu chia 1 doan loiThoai dai thanh 2 phan can doi theo ranh gioi cau (. ! ? ;)
    hoac dau phay (,) / dau gach ngang (—) de khong cat ngang cum tu.
    """
    sach = re.sub(r"\s+", " ", (loi_thoai or "").strip())
    if dem_tu(sach) < tu_toi_thieu_moi_phan * 2:
        return None

    # Uu tien tach theo dau ket cau truoc, sau do moi den dau phay / gach ngang
    for pattern in (r"(?<=[.!?;])\s+", r"(?<=,)\s+|\s+[—–-]\s+"):
        manh = [m.strip() for m in re.split(pattern, sach) if m.strip()]
        if len(manh) < 2:
            continue
        tong_tu = dem_tu(sach)
        muc_tieu = tong_tu / 2.0
        chon_tot: tuple[float, str, str] | None = None
        for idx in range(1, len(manh)):
            p1 = " ".join(manh[:idx]).strip()
            p2 = " ".join(manh[idx:]).strip()
            t1, t2 = dem_tu(p1), dem_tu(p2)
            if t1 >= tu_toi_thieu_moi_phan and t2 >= tu_toi_thieu_moi_phan:
                lech = abs(t1 - muc_tieu)
                if chon_tot is None or lech < chon_tot[0]:
                    chon_tot = (lech, p1, p2)
        if chon_tot is not None:
            return chon_tot[1], chon_tot[2]

    return None


def phat_hien_canh_dung_yen(
    kich_ban: dict[str, Any],
    nguong_canh_bao_giay: float = NGUONG_NHIP_THI_GIAC_CANH_BAO_GIAY,
    fps: int = 30,
) -> list[str]:
    """Quet va bao cao cac canh hoac chuoi canh dung yen 1 bo cuc/camera qua nguong 6-8 giay."""
    canh_bao: list[str] = []
    for ch in kich_ban.get("chuong") or []:
        ds_canh = ch.get("canh") or []
        giay_tich_luy = 0.0
        khoa_truoc: tuple[str, str, str] | None = None

        for canh in ds_canh:
            cid = str(canh.get("id") or "")
            giay = _uoc_luong_giay_canh(canh, fps=fps)
            bo_cuc = str(canh.get("boCuc") or "ke_chuyen")
            cam_kieu = str((canh.get("camera") or {}).get("kieu") or "tinh")
            nv_list = canh.get("nhanVat") or []
            hanh_dong_chinh = str(nv_list[0].get("hanhDong") or "dung_tho") if nv_list and isinstance(nv_list[0], dict) else "dung_tho"
            co_di_chuyen = any(isinstance(nv, dict) and nv.get("diChuyenDenX") is not None for nv in nv_list)

            la_tinh = cam_kieu == "tinh" and not co_di_chuyen
            if la_tinh and giay > nguong_canh_bao_giay:
                canh_bao.append(
                    f"[{cid}] Dung yen camera='tinh' qua {giay:.1f}s (> {nguong_canh_bao_giay:.1f}s)"
                )

            khoa = (bo_cuc, cam_kieu, hanh_dong_chinh)
            if khoa == khoa_truoc:
                giay_tich_luy += giay
                if giay_tich_luy > nguong_canh_bao_giay:
                    canh_bao.append(
                        f"[{cid}] Chuoi lien tiep cung boCuc='{bo_cuc}' & camera='{cam_kieu}' keo dai {giay_tich_luy:.1f}s"
                    )
            else:
                khoa_truoc = khoa
                giay_tich_luy = giay

    return canh_bao


def kiem_dinh_nhip_ngat_thi_giac(
    kich_ban: dict[str, Any],
    nguong_canh_bao_giay: float = NGUONG_NHIP_THI_GIAC_CANH_BAO_GIAY,
    nguong_tach_canh_giay: float = NGUONG_NHIP_THI_GIAC_TACH_CANH_GIAY,
    fps: int = 30,
    gan_vai_noi: bool = True,
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """
    Tieu chi kiem tra cung Tang 3 (Luat nhip ngat thi giac 6-8 giay + phan vai noi):
    - Phat hien va tu chia nho canh tinh dai > 8s (neu tach cau sach se) thanh 2 canh co goc may/hanh dong khac nhau.
    - Doi camera dong / doi hanh dong / bat KhungLoiBinhHaiHuoc neu canh don le hoac chuoi canh lien tiep
      dung yen cung 1 bo cuc/camera qua 6-8 giay.
    - Chuan hoa / suy luan nhan `vaiNoi` (nguoi_dan, nhan_vat, binh_luan_hai) cho tung canh.
    """
    import copy

    ket_qua = copy.deepcopy(kich_ban)
    da_xu_ly: list[dict[str, str]] = []
    co_tach_canh = False
    chi_so_toan_cuc = 0

    for ch in ket_qua.get("chuong") or []:
        ds_canh_cu = ch.get("canh") or []
        ds_canh_moi: list[dict[str, Any]] = []
        giay_tich_luy = 0.0
        khoa_truoc: tuple[str, str, str] | None = None
        canh_tu_lan_hai_truoc = 3

        for canh in ds_canh_cu:
            chi_so_toan_cuc += 1
            cid = str(canh.get("id") or f"canh_{chi_so_toan_cuc:03d}")
            giay = _uoc_luong_giay_canh(canh, fps=fps)
            bo_cuc = str(canh.get("boCuc") or "ke_chuyen")
            cam = canh.get("camera") if isinstance(canh.get("camera"), dict) else {"kieu": "tinh"}
            cam_kieu = str(cam.get("kieu") or "tinh")
            canh["camera"] = cam
            nv_list = canh.get("nhanVat") if isinstance(canh.get("nhanVat"), list) else []
            co_di_chuyen = any(isinstance(nv, dict) and nv.get("diChuyenDenX") is not None for nv in nv_list)
            la_tinh = cam_kieu == "tinh" and not co_di_chuyen

            # 1. Neu canh tinh qua dai (> 8s) va tach cau sach se (tranh pha canh mo_dau/ket_thuc/bang cong thuc)
            co_cong_thuc = bool(canh.get("congThucLatex"))
            if (
                la_tinh
                and giay > nguong_tach_canh_giay
                and bo_cuc not in ("mo_dau", "ket_thuc")
                and not co_cong_thuc
            ):
                tach = _tach_loi_thoai_hai_canh(str(canh.get("loiThoai") or ""))
                if tach is not None:
                    p1, p2 = tach
                    canh_1 = copy.deepcopy(canh)
                    canh_2 = copy.deepcopy(canh)
                    canh_1["loiThoai"] = p1
                    canh_2["loiThoai"] = p2
                    canh_1.pop("phuDe", None)
                    canh_2.pop("phuDe", None)

                    cam_1 = "pan_nhe" if chi_so_toan_cuc % 2 == 0 else "zoom_cham"
                    cam_2 = "zoom_hai_huoc" if bo_cuc == "hai_huoc" else ("zoom_cham" if cam_1 == "pan_nhe" else "pan_nhe")
                    canh_1["camera"] = {**cam, "kieu": cam_1}
                    canh_2["camera"] = {**cam, "kieu": cam_2}
                    canh_2["chuyenCanh"] = "quet_ngang"

                    if canh_2.get("nhanVat") and isinstance(canh_2["nhanVat"][0], dict):
                        hd_cu = str(canh_2["nhanVat"][0].get("hanhDong") or "dung_tho")
                        hd_moi = next(
                            (h for h in _HANH_DONG_DONG_LUAN_PHIEN if h != hd_cu),
                            "chi_tro_giai_thich",
                        )
                        canh_2["nhanVat"][0]["hanhDong"] = hd_moi

                    if gan_vai_noi:
                        canh_1["vaiNoi"] = suy_luan_vai_noi_canh(canh_1)
                        canh_2["vaiNoi"] = suy_luan_vai_noi_canh(canh_2)

                    ds_canh_moi.extend([canh_1, canh_2])
                    co_tach_canh = True
                    khoa_truoc = None
                    giay_tich_luy = 0.0
                    da_xu_ly.append(
                        {
                            "id": cid,
                            "hanhDong": "tach_canh",
                            "lyDo": f"Tự chia nhỏ cảnh tĩnh dài {giay:.1f}s (> {nguong_tach_canh_giay:.1f}s) kèm đổi góc máy & hành động.",
                        }
                    )
                    continue

            # 2. Neu canh don le tinh qua nguong 6-8s -> nang cap camera dong + doi hanh dong (KHONG chen loi binh cung lap lai)
            if la_tinh and giay > nguong_canh_bao_giay:
                cam_moi = (
                    "zoom_hai_huoc"
                    if bo_cuc == "hai_huoc"
                    else _CAMERA_DONG_LUAN_PHIEN[chi_so_toan_cuc % 2]
                )
                canh["camera"]["kieu"] = cam_moi
                cam_kieu = cam_moi
                if nv_list and isinstance(nv_list[0], dict) and nv_list[0].get("hanhDong") == "dung_tho":
                    nv_list[0]["hanhDong"] = _HANH_DONG_DONG_LUAN_PHIEN[
                        chi_so_toan_cuc % len(_HANH_DONG_DONG_LUAN_PHIEN)
                    ]
                da_xu_ly.append(
                    {
                        "id": cid,
                        "hanhDong": "doi_camera_va_hanh_dong",
                        "lyDo": f"Cảnh tĩnh dài {giay:.1f}s (> {nguong_canh_bao_giay:.1f}s) -> chuyển sang camera='{cam_moi}'.",
                    }
                )

            # 3. Kiem tra chuoi canh lien tiep lap cung boCuc + camera + hanhDong > 6-8s
            hanh_dong_chinh = (
                str(nv_list[0].get("hanhDong") or "dung_tho")
                if nv_list and isinstance(nv_list[0], dict)
                else "dung_tho"
            )
            khoa = (bo_cuc, cam_kieu, hanh_dong_chinh)
            if khoa == khoa_truoc:
                giay_tich_luy += giay
                if giay_tich_luy > nguong_canh_bao_giay:
                    cam_moi = next(
                        (k for k in _CAMERA_DONG_LUAN_PHIEN if k != cam_kieu),
                        "pan_nhe",
                    )
                    canh["camera"]["kieu"] = cam_moi
                    cam_kieu = cam_moi
                    if nv_list and isinstance(nv_list[0], dict):
                        hd_moi = next(
                            (h for h in _HANH_DONG_DONG_LUAN_PHIEN if h != hanh_dong_chinh),
                            "di_qua_di_lai",
                        )
                        nv_list[0]["hanhDong"] = hd_moi
                        hanh_dong_chinh = hd_moi
                    if not canh.get("chuyenCanh"):
                        canh["chuyenCanh"] = "quet_ngang"
                    da_xu_ly.append(
                        {
                            "id": cid,
                            "hanhDong": "pha_chuoi_dung_yen",
                            "lyDo": f"Chuỗi liên tiếp cùng bố cục/camera kéo dài {giay_tich_luy:.1f}s -> đổi camera='{cam_moi}' & hanhDong='{hanh_dong_chinh}'.",
                        }
                    )
                    giay_tich_luy = giay
                    khoa = (bo_cuc, cam_kieu, hanh_dong_chinh)
            else:
                giay_tich_luy = giay
            khoa_truoc = khoa

            if canh.get("loiBinhHaiHuoc"):
                canh_tu_lan_hai_truoc = 0
            else:
                canh_tu_lan_hai_truoc += 1

            if gan_vai_noi:
                canh["vaiNoi"] = suy_luan_vai_noi_canh(canh)

            ds_canh_moi.append(canh)

        ch["canh"] = ds_canh_moi

    if co_tach_canh:
        stt = 1
        for ch in ket_qua.get("chuong") or []:
            for c in ch.get("canh") or []:
                c["id"] = f"canh_{stt:03d}"
                stt += 1

    if co_tach_canh or da_xu_ly:
        gan_frame_uoc_luong(ket_qua, fps=fps)

    return ket_qua, da_xu_ly


_GOC_QUAY_LUAN_PHIEN: tuple[str, ...] = (
    "trung_canh",
    "can_mat_trai",
    "can_mat_phai",
    "can_mat",
    "pan_ngang",
    "can_mat_kich_tinh",
    "focus_trai",
    "focus_phai",
    "toan_canh",
    "zoom_dao_cu",
)

_BOI_CANH_DA_DANG_MAC_DINH: tuple[str, ...] = (
    "thu_vien_co_dien",
    "san_truong_co_dien",
    "giang_duong_dai_hoc",
    "phong_thi_nghiem_co",
    "duong_pho_xe_co",
    "phong_tro_bep_lua",
    "cang_bien_tau_thuy",
    "bau_troi_dem_vu_tru",
)

_PAT_CAM_ON = re.compile(r"(cảm\s*ơn|cam\s*on)", flags=re.IGNORECASE | re.UNICODE)


def lay_goc_quay_canh(canh: dict[str, Any]) -> str:
    """Lay gocQuay hieu luc cua 1 canh (uu tien mayQuay.gocQuay, fallback anh xa tu camera.kieu)."""
    mq = canh.get("mayQuay")
    if isinstance(mq, dict):
        gq = str(mq.get("gocQuay") or "").strip().lower()
        if gq in GOC_QUAY_CAMERA:
            return gq
    cam_kieu = str((canh.get("camera") or {}).get("kieu") or "tinh").strip().lower()
    if cam_kieu == "pan_nhe":
        return "pan_ngang"
    if cam_kieu == "zoom_hai_huoc":
        return "can_mat"
    if cam_kieu == "zoom_cham":
        return "trung_canh"
    return "toan_canh"


def la_canh_doi_thoai_hoac_tuong_tac(canh: dict[str, Any]) -> bool:
    """Kiem tra canh co phai canh doi thoai nhan vat hoac tuong tac khan gia hay khong."""
    bo_cuc = str(canh.get("boCuc") or "").strip().lower()
    loai_canh = str(canh.get("loaiCanh") or "").strip().lower()
    if bo_cuc == "doi_thoai" or loai_canh in ("doi_thoai", "tuong_tac_khan_gia"):
        return True
    if isinstance(canh.get("luotThoai"), list) and len(canh["luotThoai"]) > 0:
        return True
    if isinstance(canh.get("cauHoiTuongTac"), dict) and str(canh["cauHoiTuongTac"].get("cauHoi") or "").strip():
        return True
    return False


def _canh_chua_cam_on(canh: dict[str, Any]) -> bool:
    """Phat hien chuoi 'CAM ON' / 'cam on' trong bat ky truong chu nao cua canh."""
    van_ban_kiem_tra: list[str] = [
        str(canh.get("loiThoai") or ""),
        str(canh.get("tieuDeNho") or ""),
    ]
    if isinstance(canh.get("phuDe"), list):
        van_ban_kiem_tra.extend(str(p or "") for p in canh["phuDe"])
    if isinstance(canh.get("loiBinhHaiHuoc"), dict):
        van_ban_kiem_tra.append(str(canh["loiBinhHaiHuoc"].get("noiDung") or ""))
    for nv in canh.get("nhanVat") or []:
        if isinstance(nv, dict):
            van_ban_kiem_tra.append(str(nv.get("bongBongThoai") or ""))
    for lt in canh.get("luotThoai") or []:
        if isinstance(lt, dict):
            van_ban_kiem_tra.append(str(lt.get("noiDung") or ""))
    return any(_PAT_CAM_ON.search(txt) for txt in van_ban_kiem_tra if txt)


def _la_canh_giang_toan_rong(canh: dict[str, Any]) -> bool:
    bo_cuc = str(canh.get("boCuc") or "")
    loai_canh = str(canh.get("loaiCanh") or "")
    if bo_cuc != "giai_thich_toan" and loai_canh != "giang_toan":
        return False
    cts = canh.get("congThucLatex")
    co_ct = isinstance(cts, list) and any(
        isinstance(x, dict) and str(x.get("latex") or "").strip() for x in cts
    )
    mh = canh.get("minhHoaToan")
    if not co_ct or not isinstance(mh, dict):
        return True
    # Kiem tra schema du lieu minhHoaToan bang kiem_dinh_schema_du_lieu_canh
    loi_mh = kiem_dinh_schema_du_lieu_canh({"chuong": [{"canh": [canh]}]})
    return any("minhHoaToan" in m for m in loi_mh)


def _la_canh_timeline_rong(canh: dict[str, Any]) -> bool:
    if str(canh.get("boCuc") or "") != "dong_thoi_gian":
        return False
    mocs = canh.get("mocThoiGian")
    return not (
        isinstance(mocs, list)
        and any(
            isinstance(m, dict)
            and (str(m.get("nam") or "").strip() or str(m.get("moTa") or "").strip())
            for m in mocs
        )
    )


def _chuan_hoa_tu_so_sanh(van_ban: str) -> list[str]:
    """Tach tu thuong de so sanh trung lap giai thoai/cau noi chinh xac."""
    return re.findall(r"[^\W_]+", (van_ban or "").lower(), flags=re.UNICODE)


def kiem_tra_lap_y_toan_tap(kich_ban: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Tang cuong kiem tra chong lap cung 1 giai thoai / cau noi / loi binh hai huoc qua 1 lan tren toan tap.
    Phat hien:
    - Cau loi thoai (>= 8 tu) bi lap nguyen cau hoac giong >= 75% (Jaccard) hoac trung 6-gram lien tiep giua 2 canh.
    - Loi binh hai huoc (`loiBinhHaiHuoc.noiDung`) bi lap lai qua 1 lan trong tap.
    """
    vi_pham: list[dict[str, Any]] = []
    cau_da_gap: list[tuple[str, str, set[str], set[tuple[str, ...]]]] = []
    loi_binh_da_gap: dict[str, str] = {}

    for ch in kich_ban.get("chuong") or []:
        if not isinstance(ch, dict):
            continue
        for canh in ch.get("canh") or []:
            if not isinstance(canh, dict):
                continue
            cid = str(canh.get("id") or "")

            # 1. Kiem tra trung loiBinhHaiHuoc
            lb = canh.get("loiBinhHaiHuoc")
            if isinstance(lb, dict) and str(lb.get("noiDung") or "").strip():
                nd_lb = str(lb["noiDung"]).strip()
                khoa_lb = " ".join(_chuan_hoa_tu_so_sanh(nd_lb))
                if khoa_lb:
                    if khoa_lb in loi_binh_da_gap:
                        vi_pham.append(
                            {
                                "loai": "lap_loi_binh_hai_huoc",
                                "canhId": cid,
                                "canhGoc": loi_binh_da_gap[khoa_lb],
                                "moTa": f"[{cid}] Lời bình '{cat_gon_theo_tu(nd_lb, 60)}' bị lặp lại từ {loi_binh_da_gap[khoa_lb]}.",
                            }
                        )
                    else:
                        loi_binh_da_gap[khoa_lb] = cid

            # 2. Kiem tra lap cau noi / giai thoai (>= 8 tu) giua cac canh
            cac_doan = [str(canh.get("loiThoai") or "")]
            for lt in canh.get("luotThoai") or []:
                if isinstance(lt, dict) and str(lt.get("noiDung") or "").strip():
                    cac_doan.append(str(lt["noiDung"]))
            da_bao_canh = False
            for doan in cac_doan:
                for cau in re.split(r"(?<=[.!?;])\s+", doan.strip()):
                    tu = _chuan_hoa_tu_so_sanh(cau)
                    if len(tu) < 8:
                        continue
                    tap_tu = set(tu)
                    ngrams = {tuple(tu[i : i + 6]) for i in range(max(0, len(tu) - 5))}
                    for cid_truoc, cau_truoc, tap_truoc, ng_truoc in cau_da_gap:
                        if cid_truoc == cid:
                            continue
                        giao = len(tap_tu & tap_truoc)
                        hop = max(1, len(tap_tu | tap_truoc))
                        jaccard = giao / float(hop)
                        trung_ngram = bool(ngrams and ng_truoc and (ngrams & ng_truoc))
                        if jaccard >= 0.72 or (trung_ngram and jaccard >= 0.55):
                            vi_pham.append(
                                {
                                    "loai": "lap_giai_thoai_cau_noi",
                                    "canhId": cid,
                                    "canhGoc": cid_truoc,
                                    "moTa": (
                                        f"[{cid}] Lặp câu nói/giai thoại với {cid_truoc}: "
                                        f"\"{cat_gon_theo_tu(cau, 70)}\""
                                    ),
                                }
                            )
                            da_bao_canh = True
                            break
                    if not da_bao_canh:
                        cau_da_gap.append((cid, cau.strip(), tap_tu, ngrams))
                    else:
                        break
                if da_bao_canh:
                    break

    return vi_pham


def kiem_dinh_guardrail_kich_ban(
    kich_ban: dict[str, Any],
    ty_le_tuong_tac_toi_thieu: float = 0.25,
    so_boi_canh_toi_thieu: int = 6,
) -> list[dict[str, Any]]:
    """
    Bo Guardrail kiem dinh tu dong (Python v2.5) sau khi sinh kich ban:
    1. Cam 2 canh lien tiep trung ca boiCanh lan gocQuay.
    2. Cam canh giang_toan hoac timeline (dong_thoi_gian) co mang du lieu rong.
    3. Cam chuoi 'CAM ON' xuat hien o bat ky hoi nao khac hoi cuoi.
    4. Bat buoc >= 25% so canh la doi thoai/tuong tac va toi thieu 6 boi canh khac nhau trong toan tap.
    5. Cam nhan doi cung 1 nhanVatId trong cung 1 canh.
    6. Cam loiBinhHaiHuoc tren giang_toan / dong_thoi_gian.
    7. Cam dao cu/thoi tiet lech boi canh (la_vang_gio trong phong kin, ngon_nen_den_dau trong vu tru, nha_co_phong_sinh cho nguoi gia/giai thuong).
    8. Bat buoc moi hoi co `phuDeHoi` rieng biet (khi >= 2 hoi) & chong lap giai thoai/cau noi/loi binh toan tap.
    9. Phat hien tieng Viet khong dau dai >= 20 ky tu.
    """
    vi_pham: list[dict[str, Any]] = []
    ds_chuong = [ch for ch in (kich_ban.get("chuong") or []) if isinstance(ch, dict)]
    if not ds_chuong:
        return [{"loai": "kich_ban_rong", "canhId": "", "moTa": "Kịch bản không có chương nào."}]

    tat_ca_canh: list[tuple[int, dict[str, Any]]] = []
    for idx_ch, ch in enumerate(ds_chuong):
        for canh in ch.get("canh") or []:
            if isinstance(canh, dict):
                tat_ca_canh.append((idx_ch, canh))

    if not tat_ca_canh:
        return [{"loai": "kich_ban_rong", "canhId": "", "moTa": "Kịch bản không có cảnh nào."}]

    so_hoi_cuoi = len(ds_chuong) - 1
    boi_canh_tap: set[str] = set()
    so_tuong_tac = 0

    # Kiem tra phuDeHoi rieng biet cho tung hoi (khi co >= 2 hoi)
    if len(ds_chuong) >= 2:
        phu_de_da_dung: dict[str, int] = {}
        for idx_ch, ch in enumerate(ds_chuong):
            pd = str(ch.get("phuDeHoi") or "").strip()
            khoa_pd = " ".join(_chuan_hoa_tu_so_sanh(pd))
            if not khoa_pd:
                vi_pham.append(
                    {
                        "loai": "thieu_hoac_trung_phu_de_hoi",
                        "canhId": "",
                        "chiSoChuong": idx_ch,
                        "moTa": f"Hồi {idx_ch + 1} bị thiếu `phuDeHoi` mô tả riêng cho hồi.",
                    }
                )
            elif khoa_pd in phu_de_da_dung:
                vi_pham.append(
                    {
                        "loai": "thieu_hoac_trung_phu_de_hoi",
                        "canhId": "",
                        "chiSoChuong": idx_ch,
                        "moTa": f"Hồi {idx_ch + 1} dùng trùng `phuDeHoi` với Hồi {phu_de_da_dung[khoa_pd] + 1}.",
                    }
                )
            else:
                phu_de_da_dung[khoa_pd] = idx_ch

    for i, (idx_ch, canh) in enumerate(tat_ca_canh):
        cid = str(canh.get("id") or f"canh_{i + 1:03d}")
        bc = str(canh.get("boiCanh") or "")
        gq = lay_goc_quay_canh(canh)
        if bc:
            boi_canh_tap.add(bc)
        if la_canh_doi_thoai_hoac_tuong_tac(canh):
            so_tuong_tac += 1

        # Rule 1: Cam 2 canh lien tiep trung ca boiCanh lan gocQuay
        if i > 0:
            _, canh_truoc = tat_ca_canh[i - 1]
            bc_truoc = str(canh_truoc.get("boiCanh") or "")
            gq_truoc = lay_goc_quay_canh(canh_truoc)
            if bc and bc == bc_truoc and gq == gq_truoc:
                vi_pham.append(
                    {
                        "loai": "trung_boi_canh_va_goc_quay",
                        "canhId": cid,
                        "moTa": f"[{cid}] Trùng liên tiếp cả boiCanh='{bc}' lẫn gocQuay='{gq}' với cảnh trước.",
                    }
                )

        # Rule 2: Cam canh giang_toan hoac timeline co mang du lieu rong
        if _la_canh_giang_toan_rong(canh):
            vi_pham.append(
                {
                    "loai": "giang_toan_rong",
                    "canhId": cid,
                    "moTa": f"[{cid}] Cảnh giang_toan thiếu congThucLatex hoặc minhHoaToan hợp lệ.",
                }
            )
        if _la_canh_timeline_rong(canh):
            vi_pham.append(
                {
                    "loai": "timeline_rong",
                    "canhId": cid,
                    "moTa": f"[{cid}] Cảnh dong_thoi_gian thiếu mảng mocThoiGian hợp lệ.",
                }
            )

        # Rule 3: Cam chuoi "CAM ON" o bat ky hoi nao khac hoi cuoi
        if idx_ch < so_hoi_cuoi and _canh_chua_cam_on(canh):
            vi_pham.append(
                {
                    "loai": "cam_on_hoi_giua",
                    "canhId": cid,
                    "moTa": f"[{cid}] Phát hiện chuỗi 'CẢM ƠN' ở Hồi {idx_ch + 1} (chỉ cho phép ở hồi cuối).",
                }
            )

        # Rule 5: Cam nhan doi cung 1 nhanVatId trong cung 1 canh
        nv_ids_canh = [str(nv.get("id") or "") for nv in (canh.get("nhanVat") or []) if isinstance(nv, dict) and nv.get("id")]
        if len(nv_ids_canh) != len(set(nv_ids_canh)):
            vi_pham.append(
                {
                    "loai": "nhan_doi_nhan_vat",
                    "canhId": cid,
                    "moTa": f"[{cid}] Phát hiện nhân đôi cùng 1 nhanVatId trong cùng một cảnh ({nv_ids_canh}).",
                }
            )

        # Rule 6: Cam loiBinhHaiHuoc tren giang_toan / dong_thoi_gian
        if (
            canh.get("boCuc") in ("giai_thich_toan", "dong_thoi_gian")
            or canh.get("loaiCanh") == "giang_toan"
        ) and isinstance(canh.get("loiBinhHaiHuoc"), dict) and str(canh["loiBinhHaiHuoc"].get("noiDung") or "").strip():
            vi_pham.append(
                {
                    "loai": "loi_binh_de_bang_toan_timeline",
                    "canhId": cid,
                    "moTa": f"[{cid}] Không được đặt 'GÓC BÌNH LUẬN' (loiBinhHaiHuoc) trên bố cục {canh.get('boCuc')}.",
                }
            )

        # Rule 7: Vat the moi truong / boi canh lech ngu canh
        vt_raw = canh.get("vatTheXungQuanh") if isinstance(canh.get("vatTheXungQuanh"), list) else []
        vt_hop_le = _loc_vat_the_hop_le_boi_canh(bc, vt_raw)
        if len(vt_hop_le) < len(vt_raw):
            vi_pham.append(
                {
                    "loai": "vat_the_lech_boi_canh",
                    "canhId": cid,
                    "moTa": f"[{cid}] Có vật thể môi trường trái bối cảnh '{bc}' (vd: lá rơi trong phòng kín hoặc nến trong vũ trụ).",
                }
            )
        if bc == "nha_co_phong_sinh" and _canh_la_nguoi_gia_hoac_giai_thuong(
            canh.get("nhanVat") or [],
            str(canh.get("tieuDeNho") or ""),
            str(canh.get("loiThoai") or ""),
        ):
            vi_pham.append(
                {
                    "loai": "phong_sinh_nguoi_gia",
                    "canhId": cid,
                    "moTa": f"[{cid}] Không được chọn bối cảnh 'nha_co_phong_sinh' cho cảnh người già / giải thưởng / cuối đời.",
                }
            )

        # Rule 7b: Cam bien so "1729" bi ro ri mac dinh sang tap khong phai Ramanujan
        tieu_de_tap_low = f"{kich_ban.get('tieuDe', '')} {kich_ban.get('chuDe', '')}".lower()
        la_tap_ramanujan = any(k in tieu_de_tap_low for k in ("ramanujan", "hardy", "taxicab", "1729"))
        if not la_tap_ramanujan:
            co_1729 = str(canh.get("bienSoXe") or "").strip() == "1729"
            if not co_1729:
                co_1729 = any(
                    isinstance(item, dict) and str(item.get("bienSoXe") or "").strip() == "1729"
                    for item in (list(canh.get("daoCu") or []) + list(canh.get("vatTheXungQuanh") or []))
                )
            if co_1729:
                vi_pham.append(
                    {
                        "loai": "bien_so_1729_mac_dinh",
                        "canhId": cid,
                        "moTa": f"[{cid}] Không được gắn biển số '1729' mặc định cho tập không phải Ramanujan.",
                    }
                )

    # Rule 4: >= 25% doi thoai/tuong tac & >= 6 boi canh khac nhau
    tong_canh = len(tat_ca_canh)
    ty_le_tt = so_tuong_tac / float(max(1, tong_canh))
    if ty_le_tt < ty_le_tuong_tac_toi_thieu:
        vi_pham.append(
            {
                "loai": "thieu_doi_thoai_tuong_tac",
                "canhId": "",
                "moTa": (
                    f"Tỉ lệ cảnh đối thoại/tương tác mới đạt {so_tuong_tac}/{tong_canh} "
                    f"({ty_le_tt * 100:.1f}% < {ty_le_tuong_tac_toi_thieu * 100:.0f}%)."
                ),
            }
        )

    nguong_bc = min(so_boi_canh_toi_thieu, tong_canh)
    if len(boi_canh_tap) < nguong_bc:
        vi_pham.append(
            {
                "loai": "thieu_da_dang_boi_canh",
                "canhId": "",
                "moTa": (
                    f"Toàn tập mới có {len(boi_canh_tap)} bối cảnh khác nhau "
                    f"(tối thiểu {nguong_bc} bối cảnh)."
                ),
            }
        )

    # Rule 8: Chong lap giai thoai / cau noi / loi binh toan tap
    vi_pham.extend(kiem_tra_lap_y_toan_tap(kich_ban))

    # Rule 9: Kiem tra tieng Viet khong dau >= 20 ky tu
    vi_pham.extend(kiem_tra_dau_tieng_viet(kich_ban))

    return vi_pham


def tao_prompt_sua_guardrail_cuc_bo(
    kich_ban: dict[str, Any],
    vi_pham: list[dict[str, Any]],
    tu_lieu_nghien_cuu: dict[str, Any] | None = None,
) -> str:
    """Tao prompt sua loi cuc bo cho dung cac canh vi pham Guardrail."""
    canh_ids = []
    for vp in vi_pham:
        cid = str(vp.get("canhId") or "").strip()
        if cid and cid not in canh_ids:
            canh_ids.append(cid)

    ban_do_canh: dict[str, dict[str, Any]] = {}
    for ch in kich_ban.get("chuong") or []:
        for c in ch.get("canh") or []:
            if isinstance(c, dict) and c.get("id"):
                ban_do_canh[str(c["id"])] = c

    chi_tiet_loi = "\n".join(f"- [{vp['loai']}] {vp['moTa']}" for vp in vi_pham[:20])
    trich_canh = "\n".join(
        f"- {cid}: boCuc={ban_do_canh[cid].get('boCuc')}, boiCanh={ban_do_canh[cid].get('boiCanh')}, "
        f"gocQuay={lay_goc_quay_canh(ban_do_canh[cid])}, loiThoai={ban_do_canh[cid].get('loiThoai', '')}"
        for cid in canh_ids[:12]
        if cid in ban_do_canh
    )
    khoi_tl = dinh_dang_tu_lieu_nghien_cuu(tu_lieu_nghien_cuu)
    return f"""
Bo Guardrail tu dong vua phat hien cac vi pham sau trong kich ban "{kich_ban.get('tieuDe', '')}":
{chi_tiet_loi}

CAC CANH LIEN QUAN CAN SUA CUC BO:
{trich_canh or "(Sua o cap toan tap theo danh sach vi pham tren)"}

{khoi_tl}

Hay tra ve DUY NHAT JSON hop le gom mang `canhSua` de khac phuc TRIET DE cac loi tren (chi dung dung enum he thong):
{{
  "canhSua": [
    {{
      "id": "canh_005",
      "boiCanh": "san_truong_co_dien",
      "gocQuay": "can_mat",
      "loiThoai": "Lời thoại đã sửa có dấu đầy đủ, không còn chuỗi cảm ơn ở hồi giữa...",
      "mocThoiGian": [{{"nam": "1913", "moTa": "Mốc thật từ tư liệu nghiên cứu", "noiBat": true}}],
      "congThucLatex": [{{"latex": "e^{{i\\pi}} + 1 = 0", "nhan": "Đồng nhất thức Euler", "noiBat": true}}],
      "minhHoaToan": {{"loai": "chuoi_suy_luan", "tieuDe": "Suy luận cốt lõi", "thamSo": {{"buoc": ["Bước 1", "Bước 2"]}}}}
    }}
  ]
}}
""".strip()


def _xoa_chuoi_cam_on(van_ban: str) -> str:
    """Loai bo cum 'Cam on ...' lac vao hoi giua nhung giu nguyen cau chuyen tu nhien."""
    if not van_ban or not _PAT_CAM_ON.search(van_ban):
        return van_ban
    sach = re.sub(
        r"(?:xin\s+)?(?:cảm\s*ơn|cam\s*on)[^.!?]*[.!?]?",
        "",
        van_ban,
        flags=re.IGNORECASE | re.UNICODE,
    )
    sach = re.sub(r"\s{2,}", " ", sach).strip(" ,;-—")
    return sach or "Câu chuyện vẫn còn những bước ngoặt bất ngờ đang chờ phía trước."


def _tach_2_luot_thoai_tu_loi(loi_thoai: str, nv_ids: list[str]) -> list[dict[str, Any]]:
    """Tao nhanh 3 luot thoai ngan sac ben (kem kieuBongBong v3.0) khi guardrail nang cap canh thanh doi_thoai."""
    nv1 = nv_ids[0]
    nv2 = nv_ids[1] if len(nv_ids) > 1 else nv_ids[0]
    tach = _tach_loi_thoai_hai_canh(loi_thoai, tu_toi_thieu_moi_phan=5)
    if tach is not None:
        p1, p2 = tach
    else:
        tu = [t for t in loi_thoai.split() if t]
        giua = max(1, len(tu) // 2)
        p1 = " ".join(tu[:giua]) or loi_thoai
        p2 = " ".join(tu[giua:]) or "Quả thật là một phát hiện khiến ai cũng phải tròn mắt!"

    # Thu chia thanh 3 luot sac ben (8-22 tu) neu p2 du dai, nguoc lai them 1 cau phan hoi hai huoc co dau
    tach_tiep = _tach_loi_thoai_hai_canh(p2, tu_toi_thieu_moi_phan=5)
    if tach_tiep is not None:
        p2a, p3 = tach_tiep
    else:
        p2a = p2
        p3 = "Chính xác, nhưng điều bất ngờ nhất thì vẫn còn ở ngay phía sau!"

    f1 = max(45, int(round(max(2.0, dem_tu(p1) / 2.65) * 30)))
    f2 = max(45, int(round(max(2.0, dem_tu(p2a) / 2.65) * 30)))
    f3 = max(45, int(round(max(2.0, dem_tu(p3) / 2.65) * 30)))
    gap = 9  # 0.30s nhip hai giua luot thoai v3.0
    return [
        {
            "nhanVatId": nv1,
            "noiDung": p1,
            "bieuCam": "tram_tu",
            "dongTac": "quay_nhin_doi_thoai",
            "kieuBongBong": "thuong",
            "batDauFrame": 0,
            "ketThucFrame": f1,
        },
        {
            "nhanVatId": nv2,
            "noiDung": p2a,
            "bieuCam": "ngac_nhien",
            "dongTac": "chi_tro_giai_thich",
            "kieuBongBong": "ca_khia",
            "batDauFrame": f1 + gap,
            "ketThucFrame": f1 + gap + f2,
        },
        {
            "nhanVatId": nv1,
            "noiDung": p3,
            "bieuCam": "tinh_quai",
            "dongTac": "gat_gu_dong_tinh",
            "kieuBongBong": "thuong",
            "batDauFrame": f1 + gap + f2 + gap,
            "ketThucFrame": f1 + gap + f2 + gap + f3,
        },
    ]


def sua_loi_guardrail_cuc_bo(
    kich_ban: dict[str, Any],
    tu_lieu_nghien_cuu: dict[str, Any] | None = None,
    gemini: GeminiClient | None = None,
    cho_phep_goi_ai: bool = False,
    ty_le_tuong_tac_toi_thieu: float = 0.25,
    so_boi_canh_toi_thieu: int = 6,
) -> tuple[dict[str, Any], list[dict[str, str]]]:
    """
    Chay Guardrail kiem dinh va tu dong sua loi cuc bo ngay sau khi sinh kich ban:
    - Neu `cho_phep_goi_ai=True` va co `gemini`, thu goi Gemini sua cuc bo truoc.
    - Sau do chay sua loi tat dinh (Python) dam bao 100% kich ban dat ca 4 quy tac Guardrail
      ma KHONG bao gio chen hardcode cua tap Pythagoras.
    """
    import copy

    ket_qua = copy.deepcopy(kich_ban)
    vi_pham_ban_dau = kiem_dinh_guardrail_kich_ban(
        ket_qua,
        ty_le_tuong_tac_toi_thieu=ty_le_tuong_tac_toi_thieu,
        so_boi_canh_toi_thieu=so_boi_canh_toi_thieu,
    )
    if not vi_pham_ban_dau:
        return ket_qua, []

    nhat_ky_sua: list[dict[str, str]] = []
    danh_sach_nv = ket_qua.get("danhSachNhanVat") or []
    nv_ids = [str(nv.get("id")) for nv in danh_sach_nv if isinstance(nv, dict) and nv.get("id")] or ["nguoi_ke_chuyen"]

    # Pha A (tuy chon): Goi AI sua cuc bo dung cac canh vi pham
    if cho_phep_goi_ai and gemini is not None:
        try:
            raw_fix = gemini.tao_json(
                prompt=tao_prompt_sua_guardrail_cuc_bo(ket_qua, vi_pham_ban_dau, tu_lieu_nghien_cuu),
                system_instruction="Ban la chuyen gia sua loi cuc bo storyboard & guardrail. Tra ve DUY NHAT JSON hop le.",
                nhiet_do=0.3,
                max_output_tokens=8192,
            )
            ds_patch = raw_fix.get("canhSua") if isinstance(raw_fix, dict) else []
            if isinstance(ds_patch, list) and ds_patch:
                ban_do_patch = {
                    str(p["id"]).strip(): p
                    for p in ds_patch
                    if isinstance(p, dict) and str(p.get("id") or "").strip()
                }
                for ch in ket_qua.get("chuong") or []:
                    for c in ch.get("canh") or []:
                        cid = str(c.get("id") or "")
                        p = ban_do_patch.get(cid)
                        if not p:
                            continue
                        if p.get("boiCanh"):
                            c["boiCanh"] = chuan_hoa_enum(p["boiCanh"], LOAI_BOI_CANH, str(c.get("boiCanh") or "thu_vien_co_dien"))
                        if p.get("gocQuay"):
                            mq = c.get("mayQuay") if isinstance(c.get("mayQuay"), dict) else {}
                            mq["gocQuay"] = chuan_hoa_enum(p["gocQuay"], GOC_QUAY_CAMERA, "trung_canh")
                            c["mayQuay"] = mq
                        if isinstance(p.get("loiThoai"), str) and p["loiThoai"].strip():
                            c["loiThoai"] = re.sub(r"\s+", " ", p["loiThoai"].strip())
                            c.pop("phuDe", None)
                        if isinstance(p.get("mocThoiGian"), list) and p["mocThoiGian"]:
                            c["mocThoiGian"] = [
                                {
                                    "nam": cat_gon_theo_tu(str(m.get("nam") or "...").strip(), 30) or "...",
                                    "moTa": cat_gon_theo_tu(str(m.get("moTa") or m.get("suKien") or "...").strip(), 125) or "...",
                                    **({"noiBat": bool(m["noiBat"])} if isinstance(m.get("noiBat"), bool) else {}),
                                }
                                for m in p["mocThoiGian"][:5]
                                if isinstance(m, dict)
                            ]
                        if isinstance(p.get("congThucLatex"), list) and p["congThucLatex"]:
                            c["congThucLatex"] = [
                                {
                                    "latex": kiem_tra_latex(str(ct.get("latex") or ""))[0],
                                    "nhan": str(ct.get("nhan") or "").strip()[:85],
                                    "tuFrame": int(_ep_so(ct.get("tuFrame"), idx_ct * 35, 0, 400)),
                                }
                                for idx_ct, ct in enumerate(p["congThucLatex"][:4])
                                if isinstance(ct, dict) and str(ct.get("latex") or "").strip()
                            ]
                        if isinstance(p.get("minhHoaToan"), dict):
                            c_tam, _ = chuan_hoa_canh({**c, "minhHoaToan": p["minhHoaToan"]}, cid, nv_ids)
                            if c_tam.get("minhHoaToan"):
                                c["minhHoaToan"] = c_tam["minhHoaToan"]
                        nhat_ky_sua.append({"id": cid, "loai": "ai_sua_cuc_bo", "moTa": "AI da sua cuc bo theo Guardrail."})
        except Exception as err:
            nhat_ky_sua.append({"id": "", "loai": "ai_sua_bo_qua", "moTa": f"Fallback sua tat dinh do loi AI: {err}"})

    # Pha B: Sua loi tat dinh cuc bo (dam bao 100% dat Guardrail)
    ds_chuong = [ch for ch in (ket_qua.get("chuong") or []) if isinstance(ch, dict)]
    so_hoi_cuoi = max(0, len(ds_chuong) - 1)
    tat_ca_canh: list[tuple[int, dict[str, Any]]] = [
        (idx_ch, c)
        for idx_ch, ch in enumerate(ds_chuong)
        for c in (ch.get("canh") or [])
        if isinstance(c, dict)
    ]

    # Lay moc timeline that tu tu_lieu_nghien_cuu (neu co)
    timeline_that: list[dict[str, Any]] = []
    if isinstance(tu_lieu_nghien_cuu, dict):
        nguon_tl = tu_lieu_nghien_cuu.get("timeline_su_kien") or tu_lieu_nghien_cuu.get("nienDaiChuan") or []
        for idx_m, m in enumerate(nguon_tl[:5]):
            if isinstance(m, dict) and (str(m.get("nam") or "").strip() or str(m.get("suKien") or m.get("moTa") or "").strip()):
                timeline_that.append(
                    {
                        "nam": cat_gon_theo_tu(str(m.get("nam") or "...").strip(), 30) or "...",
                        "moTa": cat_gon_theo_tu(str(m.get("suKien") or m.get("moTa") or "...").strip(), 125) or "...",
                        "noiBat": bool(m.get("noiBat", idx_m == 0)),
                    }
                )

    # 1. Xoa chuoi "CAM ON" o cac hoi truoc hoi cuoi + chan boCuc='ket_thuc' o hoi giua
    for idx_ch, canh in tat_ca_canh:
        cid = str(canh.get("id") or "")
        if idx_ch < so_hoi_cuoi and _canh_chua_cam_on(canh):
            canh["loiThoai"] = _xoa_chuoi_cam_on(str(canh.get("loiThoai") or ""))
            if canh.get("tieuDeNho"):
                canh["tieuDeNho"] = _xoa_chuoi_cam_on(str(canh["tieuDeNho"]))
            if isinstance(canh.get("phuDe"), list):
                canh["phuDe"] = [_xoa_chuoi_cam_on(str(p)) for p in canh["phuDe"] if str(p).strip()]
            if isinstance(canh.get("loiBinhHaiHuoc"), dict) and canh["loiBinhHaiHuoc"].get("noiDung"):
                canh["loiBinhHaiHuoc"]["noiDung"] = _xoa_chuoi_cam_on(str(canh["loiBinhHaiHuoc"]["noiDung"]))
            for nv in canh.get("nhanVat") or []:
                if isinstance(nv, dict) and nv.get("bongBongThoai"):
                    nv["bongBongThoai"] = _xoa_chuoi_cam_on(str(nv["bongBongThoai"]))
            for lt in canh.get("luotThoai") or []:
                if isinstance(lt, dict) and lt.get("noiDung"):
                    lt["noiDung"] = _xoa_chuoi_cam_on(str(lt["noiDung"]))
            if canh.get("boCuc") == "ket_thuc":
                canh["boCuc"] = "ke_chuyen"
            nhat_ky_sua.append({"id": cid, "loai": "cam_on_hoi_giua", "moTa": "Đã gỡ bỏ chuỗi 'CẢM ƠN' ở hồi giữa."})

        # 1b. Khu trung lap nhanVatId trong cung 1 canh
        nv_raw = canh.get("nhanVat") if isinstance(canh.get("nhanVat"), list) else []
        nv_khu_trung: list[dict[str, Any]] = []
        da_thay_nv: set[str] = set()
        for nv_item in nv_raw:
            if not isinstance(nv_item, dict):
                continue
            nid = str(nv_item.get("id") or "").strip()
            if not nid or nid in da_thay_nv:
                continue
            da_thay_nv.add(nid)
            nv_khu_trung.append(nv_item)
        if len(nv_khu_trung) < len(nv_raw):
            canh["nhanVat"] = nv_khu_trung
            nhat_ky_sua.append({"id": cid, "loai": "nhan_doi_nhan_vat", "moTa": "Đã loại bỏ nhân vật bị nhân đôi trong cùng cảnh."})

        # 1c. Go bo loiBinhHaiHuoc tren giang_toan / dong_thoi_gian
        if (
            canh.get("boCuc") in ("giai_thich_toan", "dong_thoi_gian")
            or canh.get("loaiCanh") == "giang_toan"
        ) and canh.get("loiBinhHaiHuoc"):
            canh.pop("loiBinhHaiHuoc", None)
            nhat_ky_sua.append({"id": cid, "loai": "loi_binh_de_bang_toan_timeline", "moTa": "Đã gỡ hộp 'Góc bình luận' khỏi cảnh Toán/Dòng thời gian."})

        # 1d. Chan dao cu / thoi tiet lech boi canh va nha_co_phong_sinh cho nguoi gia/giai thuong
        bc_c = str(canh.get("boiCanh") or "")
        if bc_c == "nha_co_phong_sinh" and _canh_la_nguoi_gia_hoac_giai_thuong(
            canh.get("nhanVat") or [],
            str(canh.get("tieuDeNho") or ""),
            str(canh.get("loiThoai") or ""),
        ):
            canh["boiCanh"] = "giang_duong_dai_hoc"
            bc_c = "giang_duong_dai_hoc"
            nhat_ky_sua.append({"id": cid, "loai": "phong_sinh_nguoi_gia", "moTa": "Đã đổi bối cảnh từ nha_co_phong_sinh sang giang_duong_dai_hoc."})
        if isinstance(canh.get("vatTheXungQuanh"), list):
            vt_moi = _loc_vat_the_hop_le_boi_canh(bc_c, canh["vatTheXungQuanh"])
            if len(vt_moi) < len(canh["vatTheXungQuanh"]):
                canh["vatTheXungQuanh"] = vt_moi
                nhat_ky_sua.append({"id": cid, "loai": "vat_the_lech_boi_canh", "moTa": f"Đã lọc bỏ vật thể môi trường lệch bối cảnh '{bc_c}'."})
        tt_cu = str(canh.get("thoiTiet") or "khong")
        tt_moi = _chuan_hoa_thoi_tiet_boi_canh(bc_c, tt_cu)
        if tt_moi != tt_cu:
            canh["thoiTiet"] = tt_moi

        # 1e. Go bien so "1729" mac dinh neu day khong phai tap Ramanujan
        tieu_de_tap_low = f"{ket_qua.get('tieuDe', '')} {ket_qua.get('chuDe', '')}".lower()
        if not any(k in tieu_de_tap_low for k in ("ramanujan", "hardy", "taxicab", "1729")):
            da_go_1729 = False
            if str(canh.get("bienSoXe") or "").strip() == "1729":
                canh.pop("bienSoXe", None)
                da_go_1729 = True
            for ds_ten in ("daoCu", "vatTheXungQuanh"):
                for item_bs in canh.get(ds_ten) or []:
                    if isinstance(item_bs, dict) and str(item_bs.get("bienSoXe") or "").strip() == "1729":
                        item_bs.pop("bienSoXe", None)
                        da_go_1729 = True
            if da_go_1729:
                nhat_ky_sua.append({"id": cid, "loai": "bien_so_1729_mac_dinh", "moTa": "Đã gỡ biển số '1729' mặc định khỏi tập không phải Ramanujan."})

        # 2. Sua canh giang_toan hoac timeline rong (KHONG hardcode Pythagoras!)
        if _la_canh_timeline_rong(canh):
            if timeline_that:
                canh["mocThoiGian"] = copy.deepcopy(timeline_that)
                nhat_ky_sua.append({"id": cid, "loai": "timeline_rong", "moTa": "Đã nạp mốc thời gian từ tư liệu nghiên cứu."})
            else:
                canh["boCuc"] = "ke_chuyen"
                nhat_ky_sua.append({"id": cid, "loai": "timeline_rong", "moTa": "Thiếu dữ liệu dòng thời gian -> chuyển bố cục về kể chuyện sạch."})

        if _la_canh_giang_toan_rong(canh):
            cts = canh.get("congThucLatex")
            co_ct = isinstance(cts, list) and any(isinstance(x, dict) and str(x.get("latex") or "").strip() for x in cts)
            if co_ct:
                ds_buoc = [
                    str(x.get("nhan") or x.get("latex") or "").strip()[:80]
                    for x in cts
                    if isinstance(x, dict) and (str(x.get("nhan") or "").strip() or str(x.get("latex") or "").strip())
                ]
                if not ds_buoc:
                    ds_buoc = [str(canh.get("tieuDeNho") or "Bước suy luận cốt lõi")[:80]]
                mh_hien_tai = canh.get("minhHoaToan") if isinstance(canh.get("minhHoaToan"), dict) else {}
                canh["minhHoaToan"] = {
                    "loai": "chuoi_suy_luan",
                    "tieuDe": str(mh_hien_tai.get("tieuDe") or canh.get("tieuDeNho") or "Các bước suy luận")[:70],
                    "thamSo": {"buoc": ds_buoc},
                }
                nhat_ky_sua.append({"id": cid, "loai": "giang_toan_rong", "moTa": "Đã bổ sung các bước suy luận cho minh họa Toán từ công thức của cảnh."})
            else:
                canh["boCuc"] = "ke_chuyen"
                if canh.get("loaiCanh") == "giang_toan":
                    canh["loaiCanh"] = "ke_chuyen"
                canh.pop("minhHoaToan", None)
                nhat_ky_sua.append({"id": cid, "loai": "giang_toan_rong", "moTa": "Cảnh giảng Toán thiếu công thức -> chuyển về bố cục kể chuyện sạch."})

    # 3. Da dang hoa boi canh toi thieu 6 boi canh khac nhau
    boi_canh_hien_co = {str(c.get("boiCanh") or "") for _, c in tat_ca_canh if c.get("boiCanh")}
    nguong_bc = min(so_boi_canh_toi_thieu, len(tat_ca_canh))
    if len(boi_canh_hien_co) < nguong_bc:
        ung_vien_bc: list[str] = []
        if isinstance(tu_lieu_nghien_cuu, dict):
            for g in tu_lieu_nghien_cuu.get("goi_y_boi_canh_va_dao_cu") or []:
                if isinstance(g, dict):
                    bc_g = chuan_hoa_enum(g.get("boiCanh"), LOAI_BOI_CANH, "")
                    if bc_g and bc_g not in ung_vien_bc:
                        ung_vien_bc.append(bc_g)
        for bc_md in _BOI_CANH_DA_DANG_MAC_DINH:
            if bc_md not in ung_vien_bc:
                ung_vien_bc.append(bc_md)

        con_thieu = [bc for bc in ung_vien_bc if bc not in boi_canh_hien_co]
        ung_vien_canh = [
            (idx_toan, c)
            for idx_toan, (_, c) in enumerate(tat_ca_canh)
            if c.get("boCuc") in ("ke_chuyen", "doi_thoai")
        ]
        if not ung_vien_canh:
            ung_vien_canh = list(enumerate(c for _, c in tat_ca_canh))
        buoc_nhay = max(1, len(ung_vien_canh) // max(1, len(con_thieu)))
        vi_tri_uv = 0
        while len(boi_canh_hien_co) < nguong_bc and con_thieu and vi_tri_uv < len(ung_vien_canh):
            bc_moi = con_thieu.pop(0)
            _, canh_doi = ung_vien_canh[vi_tri_uv]
            canh_doi["boiCanh"] = bc_moi
            boi_canh_hien_co.add(bc_moi)
            nhat_ky_sua.append(
                {
                    "id": str(canh_doi.get("id") or ""),
                    "loai": "thieu_da_dang_boi_canh",
                    "moTa": f"Da da dang hoa boiCanh sang '{bc_moi}'.",
                }
            )
            vi_tri_uv += buoc_nhay

    # 4. Dam bao >= 25% so canh la doi thoai / tuong tac khan gia
    tong_canh = len(tat_ca_canh)
    muc_tieu_tt = int(math.ceil(tong_canh * ty_le_tuong_tac_toi_thieu))
    so_tt_hien_tai = sum(1 for _, c in tat_ca_canh if la_canh_doi_thoai_hoac_tuong_tac(c))
    if so_tt_hien_tai < muc_tieu_tt:
        can_nang_cap = [
            (idx_ch, c)
            for idx_ch, c in tat_ca_canh
            if not la_canh_doi_thoai_hoac_tuong_tac(c) and c.get("boCuc") == "ke_chuyen"
        ]
        da_co_tuong_tac_kg = sum(
            1 for _, c in tat_ca_canh if str(c.get("loaiCanh") or "") == "tuong_tac_khan_gia"
        )
        buoc_nc = max(1, len(can_nang_cap) // max(1, muc_tieu_tt - so_tt_hien_tai))
        da_chon_ids: set[str] = set()
        thu_tu_duyet = [can_nang_cap[i] for i in range(0, len(can_nang_cap), buoc_nc)] + can_nang_cap
        for _, canh_nc in thu_tu_duyet:
            if so_tt_hien_tai >= muc_tieu_tt:
                break
            cid_nc = str(canh_nc.get("id") or "")
            if cid_nc in da_chon_ids:
                continue
            da_chon_ids.add(cid_nc)
            if da_co_tuong_tac_kg < 2 and tong_canh >= 6:
                canh_nc["loaiCanh"] = "tuong_tac_khan_gia"
                canh_nc["cauHoiTuongTac"] = {
                    "cauHoi": f"Theo bạn, bước ngoặt ở '{str(canh_nc.get('tieuDeNho') or 'tình huống này')[:60]}' dẫn tới kết quả nào?",
                    "thoiGianDemNguocGiay": 3,
                    "dapAn": "Đáp án chính là manh mối Toán học ngay trong câu chuyện!",
                    "giaiThichNgan": str(canh_nc.get("loiThoai") or "")[:120],
                }
                if canh_nc.get("nhanVat") and isinstance(canh_nc["nhanVat"][0], dict):
                    canh_nc["nhanVat"][0]["hanhDong"] = "quay_nhin_khan_gia"
                    canh_nc["nhanVat"][0]["tuongTacVoi"] = "khan_gia"
                mq = canh_nc.get("mayQuay") if isinstance(canh_nc.get("mayQuay"), dict) else {}
                mq["gocQuay"] = "can_mat"
                canh_nc["mayQuay"] = mq
                da_co_tuong_tac_kg += 1
                nhat_ky_sua.append({"id": cid_nc, "loai": "thieu_doi_thoai_tuong_tac", "moTa": "Nang cap thanh canh tuong_tac_khan_gia co dem nguoc 3s."})
            else:
                canh_nc["boCuc"] = "doi_thoai"
                canh_nc["loaiCanh"] = "doi_thoai"
                canh_nc["vaiNoi"] = "nhan_vat"
                canh_nc["luotThoai"] = _tach_2_luot_thoai_tu_loi(str(canh_nc.get("loiThoai") or ""), nv_ids)
                mq = canh_nc.get("mayQuay") if isinstance(canh_nc.get("mayQuay"), dict) else {}
                mq["tuDongFocusNguoiNoi"] = True
                if not mq.get("gocQuay"):
                    mq["gocQuay"] = "dao_goc_can_mat"
                canh_nc["mayQuay"] = mq
                # Dam bao co 2 nhan vat nhin ve phia nhau neu danhSachNhanVat >= 2
                nv_list = canh_nc.get("nhanVat") if isinstance(canh_nc.get("nhanVat"), list) else []
                if len(nv_ids) >= 2 and len(nv_list) < 2:
                    nv1_id = str(nv_list[0].get("id")) if nv_list and isinstance(nv_list[0], dict) else nv_ids[0]
                    nv2_id = next((nid for nid in nv_ids if nid != nv1_id), nv_ids[1])
                    if nv_list and isinstance(nv_list[0], dict):
                        nv_list[0]["x"] = 640
                        nv_list[0]["huong"] = "phai"
                        nv_list[0]["tuongTacVoi"] = nv2_id
                    nv_list.append(
                        {
                            "id": nv2_id,
                            "x": 1280,
                            "y": 810,
                            "huong": "trai",
                            "hanhDong": "quay_nhin_doi_thoai",
                            "bieuCam": "ngac_nhien",
                            "tuongTacVoi": nv1_id,
                            "dangNoi": False,
                        }
                    )
                    canh_nc["nhanVat"] = nv_list
                nhat_ky_sua.append({"id": cid_nc, "loai": "thieu_doi_thoai_tuong_tac", "moTa": "Đã nâng cấp thành cảnh đối thoại 3 lượt kèm góc đảo cận mặt."})
            so_tt_hien_tai += 1

    # 5. Cam 2 canh lien tiep trung ca boiCanh lan gocQuay (chay cuoi de bat moi va cham sau buoc 3 & 4)
    for i in range(1, len(tat_ca_canh)):
        _, canh_truoc = tat_ca_canh[i - 1]
        _, canh = tat_ca_canh[i]
        bc_truoc = str(canh_truoc.get("boiCanh") or "")
        gq_truoc = lay_goc_quay_canh(canh_truoc)
        bc = str(canh.get("boiCanh") or "")
        gq = lay_goc_quay_canh(canh)
        if bc and bc == bc_truoc and gq == gq_truoc:
            gq_moi = next(
                (
                    _GOC_QUAY_LUAN_PHIEN[(i + offset) % len(_GOC_QUAY_LUAN_PHIEN)]
                    for offset in range(len(_GOC_QUAY_LUAN_PHIEN))
                    if _GOC_QUAY_LUAN_PHIEN[(i + offset) % len(_GOC_QUAY_LUAN_PHIEN)] != gq_truoc
                ),
                "can_mat",
            )
            mq = canh.get("mayQuay") if isinstance(canh.get("mayQuay"), dict) else {}
            mq["gocQuay"] = gq_moi
            canh["mayQuay"] = mq
            nhat_ky_sua.append(
                {
                    "id": str(canh.get("id") or ""),
                    "loai": "trung_boi_canh_va_goc_quay",
                    "moTa": f"Doi gocQuay '{gq}' -> '{gq_moi}' de tranh trung lien tiep voi canh truoc.",
                }
            )

    # 5b. Dam bao moi hoi co phuDeHoi rieng biet & go bo loiBinhHaiHuoc bi lap lai toan tap
    if len(ds_chuong) >= 2:
        phu_de_da_co: set[str] = set()
        for idx_ch, ch in enumerate(ds_chuong):
            pd = str(ch.get("phuDeHoi") or "").strip()
            khoa_pd = " ".join(_chuan_hoa_tu_so_sanh(pd))
            if not khoa_pd or khoa_pd in phu_de_da_co:
                ten_ch = str(ch.get("tenChuong") or f"Hồi {idx_ch + 1}").strip()
                td_canh = next(
                    (
                        str(c.get("tieuDeNho") or "").strip()
                        for c in (ch.get("canh") or [])
                        if isinstance(c, dict) and str(c.get("tieuDeNho") or "").strip()
                    ),
                    "",
                )
                pd_moi = cat_gon_theo_tu(
                    f"Hồi {idx_ch + 1}: {td_canh} — {ten_ch}" if td_canh else f"Khám phá điểm nhấn riêng của Hồi {idx_ch + 1}: {ten_ch}",
                    140,
                )
                ch["phuDeHoi"] = pd_moi
                if ch.get("canh") and isinstance(ch["canh"][0], dict) and ch["canh"][0].get("boCuc") == "mo_dau":
                    ch["canh"][0]["phuDeHoi"] = pd_moi
                phu_de_da_co.add(" ".join(_chuan_hoa_tu_so_sanh(pd_moi)))
                nhat_ky_sua.append(
                    {
                        "id": str(ch.get("id") or f"chuong_{idx_ch + 1}"),
                        "loai": "thieu_hoac_trung_phu_de_hoi",
                        "moTa": f"Đã tạo `phuDeHoi` riêng biệt cho Hồi {idx_ch + 1}.",
                    }
                )
            else:
                phu_de_da_co.add(khoa_pd)

    loi_binh_duy_nhat: set[str] = set()
    for _, canh in tat_ca_canh:
        lb = canh.get("loiBinhHaiHuoc")
        if isinstance(lb, dict) and str(lb.get("noiDung") or "").strip():
            khoa_lb = " ".join(_chuan_hoa_tu_so_sanh(str(lb["noiDung"])))
            if khoa_lb in loi_binh_duy_nhat:
                canh.pop("loiBinhHaiHuoc", None)
                nhat_ky_sua.append(
                    {
                        "id": str(canh.get("id") or ""),
                        "loai": "lap_loi_binh_hai_huoc",
                        "moTa": "Đã gỡ hộp lời bình trùng lặp với cảnh trước.",
                    }
                )
            else:
                loi_binh_duy_nhat.add(khoa_lb)

    # 5c. Neu co Gemini va phat hien chuoi tieng Viet khong dau >= 20 ky tu -> tu dong sua dau
    if cho_phep_goi_ai and gemini is not None:
        ket_qua, ds_sua_dau = tu_dong_sua_dau_tieng_viet(ket_qua, gemini=gemini)
        for item_sd in ds_sua_dau:
            nhat_ky_sua.append(
                {
                    "id": item_sd["duongDan"],
                    "loai": "tieng_viet_khong_dau",
                    "moTa": f"Đã khôi phục dấu tiếng Việt cho {item_sd['duongDan']}.",
                }
            )

    if nhat_ky_sua:
        gan_frame_uoc_luong(ket_qua)
    return ket_qua, nhat_ky_sua


def _trich_su_kien_theo_hoi(kich_ban: dict[str, Any]) -> dict[int, list[str]]:
    """Trich danh sach su kien / tieu de chinh theo tung hoi de Tang 3 kiem tra chong lap y."""
    ket_qua: dict[int, list[str]] = {}
    for idx_ch, ch in enumerate(kich_ban.get("chuong") or [], start=1):
        if not isinstance(ch, dict):
            continue
        ds: list[str] = []
        for c in ch.get("canh") or []:
            if not isinstance(c, dict):
                continue
            td = str(c.get("tieuDeNho") or "").strip()
            nam = str(c.get("namMoc") or "").strip()
            lb = str((c.get("loiBinhHaiHuoc") or {}).get("noiDung") or "").strip() if isinstance(c.get("loiBinhHaiHuoc"), dict) else ""
            nhan = f"[{c.get('id', '')}]"
            if nam:
                nhan += f" ({nam})"
            if td:
                ds.append(f"{nhan} {td}")
            elif lb:
                ds.append(f"{nhan} {lb}")
        ket_qua[idx_ch] = ds[:10]
    return ket_qua


def tao_prompt_tu_kiem_dinh(
    kich_ban: dict[str, Any],
    tu_lieu_nghien_cuu: dict[str, Any] | None = None,
    canh_bao_latex: list[str] | None = None,
    canh_bao_thi_giac: list[str] | None = None,
    su_kien_theo_hoi: dict[int, list[str]] | None = None,
) -> str:
    """Tang 3: Prompt Tu kiem dinh (Self-Critique) doi chieu Toan hoc/lich su, chong lap y giua cac hoi, Hook 20-30s, Storyboard, LaTeX va phan vai."""
    khoi_tu_lieu = dinh_dang_tu_lieu_nghien_cuu(tu_lieu_nghien_cuu)
    sk_hoi = su_kien_theo_hoi if su_kien_theo_hoi is not None else _trich_su_kien_theo_hoi(kich_ban)
    dong_sk: list[str] = []
    for so_hoi, ds_sk in sorted(sk_hoi.items()):
        if ds_sk:
            dong_sk.append(f"- Hoi {so_hoi}: " + " | ".join(ds_sk[:8]))
    khoi_su_kien_cac_hoi = "\n".join(dong_sk) or "(Chua co du lieu tom tat su kien theo hoi)"

    canh_tom_tat: list[str] = []
    for idx_ch, ch in enumerate(kich_ban.get("chuong") or [], start=1):
        canh_tom_tat.append(f"## Hoi {idx_ch}: {ch.get('tenChuong', '')}")
        for c in ch.get("canh") or []:
            ct_str = ""
            if c.get("congThucLatex"):
                ds_ct = "; ".join(str(x.get("latex", "")) for x in c["congThucLatex"])
                ct_str = f" | LaTeX: [{ds_ct}]"
            lb_str = ""
            if isinstance(c.get("loiBinhHaiHuoc"), dict):
                lb_str = f" | Hai: {c['loiBinhHaiHuoc'].get('noiDung', '')}"
            cam_kieu = str((c.get("camera") or {}).get("kieu") or "tinh")
            goc_quay = lay_goc_quay_canh(c)
            vai_noi = str(c.get("vaiNoi") or suy_luan_vai_noi_canh(c))
            giay_est = _uoc_luong_giay_canh(c)
            canh_tom_tat.append(
                f"- {c.get('id')} ({c.get('boCuc')} | bc:{c.get('boiCanh')} | gq:{goc_quay} | cam:{cam_kieu} | vai:{vai_noi} | ~{giay_est:.1f}s): "
                f"{c.get('loiThoai', '')}{ct_str}{lb_str}"
            )

    tom_tat_kich_ban = "\n".join(canh_tom_tat)
    canh_bao_txt = "\n".join(f"- {cb}" for cb in (canh_bao_latex or [])) or "(Khong co canh bao cu phap LaTeX tu dong)"
    cb_thi_giac = canh_bao_thi_giac if canh_bao_thi_giac is not None else phat_hien_canh_dung_yen(kich_ban)
    canh_bao_tg_txt = (
        "\n".join(f"- {cb}" for cb in cb_thi_giac[:15])
        if cb_thi_giac
        else "(Khong co canh bao dung yen thi giac >6-8s)"
    )
    vi_pham_gr = kiem_dinh_guardrail_kich_ban(kich_ban)
    canh_bao_gr_txt = (
        "\n".join(f"- [{vp['loai']}] {vp['moTa']}" for vp in vi_pham_gr[:12])
        if vi_pham_gr
        else "(Dat toan bo Guardrail storyboard)"
    )

    return f"""
Ban la tong bien tap kiem dao dien Storyboard & chuyen gia kiem dinh Toan hoc - Lich su (Tang 3: TU KIEM DINH / SELF-CRITIQUE).
Hay ra soat toan bo kich ban phim hoat hinh duoi day theo 7 tieu chi bat buoc:
1. CHUAN XAC TOAN HOC & LICH SU: Doi chieu nien dai, ten nhan vat, dinh ly voi tu lieu nghien cuu (khong sai nien dai, khong sai cong thuc).
2. CHONG LAP Y GIUA CAC HOI (BAT BUOC): So sanh bang su kien da dung o cac hoi truoc ben duoi; neu bat ky giai thoai, vi du hay loi binh nao bi ke lap qua 1 lan giua cac hoi -> BAT BUOC dua vao `canhCanSua` voi `loiThoaiMoi` khai thac goc nhin moi!
3. HOOK 20-30 GIAY DAU (3-5 canh dau Hoi 1): Kiem tra xem phan mo dau co di thang vao nghich ly Toan hoc / cau do meo / tinh huong do khoc do cuoi khong. Neu mo bai kieu tieu su sach giao khoa ("Sinh nam ... tai ...") -> BAT BUOC sua lai loiThoaiMoi ngay lap tuc!
4. STORYBOARD, BOI CANH 1-1 & NHIP NGAT THI GIAC: Khong de 2 canh lien tiep trung ca `boiCanh` lan `gocQuay`; khong de canh dung yen qua 6-8 giay; khop `boiCanhMoi` / `gocQuayMoi` voi tinh tiet cau chuyen; CAM chuoi "CAM ON" o Hoi 1..5.
5. CU PHAP LATEX: Kiem tra congThucLatex can bang ngoac {{}}, dung cu phap KaTeX, thoat \\\\ dung chuan JSON.
6. PHONG CACH, DOI THOAI & PHAN VAI `vaiNoi`: Dam bao >= 25% canh doi thoai/tuong tac khan gia, nhip hai di dom khong bao luc, va gan `vaiNoiMoi` (`nguoi_dan` | `nhan_vat` | `binh_luan_hai`).
7. TU RUT KINH NGHIEM: Neu phat hien mau loi dang luu y (lap y giua cac hoi, sai boi canh, mo bai sach giao khoa, canh dung yen >8s, loi LaTeX...), rut ra 1-2 quy tac ngan gon vao `baiHocMoi`.

{khoi_tu_lieu}

SU KIEN / Y DA DUNG QUA TUNG HOI (DOI CHIEU CHONG LAP Y):
{khoi_su_kien_cac_hoi}

CANH BAO LATEX TU DONG:
{canh_bao_txt}

CANH BAO NHIP THI GIAC >6-8s TU DONG:
{canh_bao_tg_txt}

CANH BAO GUARDRAIL STORYBOARD TU DONG:
{canh_bao_gr_txt}

TOM TAT KICH BAN CAN KIEM DINH:
{tom_tat_kich_ban}

Chi liet ke vao `canhCanSua` nhung canh THUC SU co loi (toi da 10 canh). Neu kich ban da tot, de `canhCanSua: []`.
Tra ve DUY NHAT JSON hop le dung cau truc:
{{
  "diemTongThe": 8.8,
  "nhanXetChung": "Nhận xét ngắn gọn 1-2 câu về chất lượng toàn tập...",
  "canhCanSua": [
    {{
      "id": "canh_012",
      "lyDo": "Sửa lặp ý với Hồi 2 / khớp bối cảnh 1-1 / phá trùng góc quay / sửa nhịp hài...",
      "loiThoaiMoi": "Lời thoại đã sửa chuẩn xác, tự nhiên và có dấu tiếng Việt đầy đủ...",
      "boiCanhMoi": "phong_benh_vien",
      "gocQuayMoi": "can_mat",
      "vaiNoiMoi": "nguoi_dan",
      "cameraMoi": {{"kieu": "zoom_hai_huoc"}},
      "hanhDongMoi": "giat_minh_nhay_dung",
      "congThucLatexMoi": [
        {{"latex": "a^2 + b^2 = c^2", "nhan": "Định lý", "noiBat": true}}
      ],
      "loiBinhHaiHuocMoi": {{"noiDung": "Câu bình luận dí dỏm có dấu...", "viTri": "goc_phai"}}
    }}
  ],
  "baiHocMoi": [
    {{
      "loai": "toan_hoc",
      "noiDung": "Quy tắc ngắn gọn rút ra từ đợt kiểm định này...",
      "mucDoUuTien": 4
    }}
  ]
}}
""".strip()


def ap_dung_sua_tu_kiem_dinh(
    kich_ban: dict[str, Any],
    ket_qua_kiem_dinh: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, str]], list[str]]:
    """Ap dung danh sach canhCanSua tu Tang 3 vao kich ban, tai kiem tra LaTeX va uoc luong frame."""
    ds_sua = ket_qua_kiem_dinh.get("canhCanSua") if isinstance(ket_qua_kiem_dinh, dict) else []
    if not isinstance(ds_sua, list) or not ds_sua:
        # Van kiem tra lai LaTeX toan bo
        tat_ca_cb: list[str] = []
        for ch in kich_ban.get("chuong") or []:
            for c in ch.get("canh") or []:
                for ct in c.get("congThucLatex") or []:
                    if isinstance(ct, dict):
                        clean, cbs = kiem_tra_latex(str(ct.get("latex") or ""))
                        ct["latex"] = clean
                        for cb in cbs:
                            tat_ca_cb.append(f"[{c.get('id', '')}] {cb}")
        return kich_ban, [], tat_ca_cb

    ban_do_sua: dict[str, dict[str, Any]] = {}
    for item in ds_sua:
        if isinstance(item, dict) and str(item.get("id") or "").strip():
            ban_do_sua[str(item["id"]).strip()] = item

    da_sua: list[dict[str, str]] = []
    tat_ca_cb = []

    for ch in kich_ban.get("chuong") or []:
        for c in ch.get("canh") or []:
            cid = str(c.get("id") or "")
            patch = ban_do_sua.get(cid)
            if patch:
                if isinstance(patch.get("loiThoaiMoi"), str) and patch["loiThoaiMoi"].strip():
                    c["loiThoai"] = re.sub(r"\s+", " ", patch["loiThoaiMoi"].strip())
                if isinstance(patch.get("boiCanhMoi"), str) and patch["boiCanhMoi"].strip():
                    c["boiCanh"] = chuan_hoa_enum(
                        patch["boiCanhMoi"],
                        LOAI_BOI_CANH,
                        str(c.get("boiCanh") or "thu_vien_co_dien"),
                    )
                if isinstance(patch.get("gocQuayMoi"), str) and patch["gocQuayMoi"].strip():
                    mq_hien_tai = c.get("mayQuay") if isinstance(c.get("mayQuay"), dict) else {}
                    mq_hien_tai["gocQuay"] = chuan_hoa_enum(
                        patch["gocQuayMoi"],
                        GOC_QUAY_CAMERA,
                        lay_goc_quay_canh(c),
                    )
                    c["mayQuay"] = mq_hien_tai
                if isinstance(patch.get("vaiNoiMoi"), str) and patch["vaiNoiMoi"].strip():
                    c["vaiNoi"] = chuan_hoa_enum(patch["vaiNoiMoi"], LOAI_VAI_NOI, "nguoi_dan")
                if isinstance(patch.get("cameraMoi"), dict):
                    cam_hien_tai = c.get("camera") if isinstance(c.get("camera"), dict) else {}
                    cam_hien_tai["kieu"] = chuan_hoa_enum(
                        patch["cameraMoi"].get("kieu"),
                        KIEU_CAMERA,
                        str(cam_hien_tai.get("kieu") or "pan_nhe"),
                    )
                    c["camera"] = cam_hien_tai
                if isinstance(patch.get("hanhDongMoi"), str) and patch["hanhDongMoi"].strip():
                    nv_list = c.get("nhanVat")
                    if isinstance(nv_list, list) and nv_list and isinstance(nv_list[0], dict):
                        nv_list[0]["hanhDong"] = chuan_hoa_enum(
                            patch["hanhDongMoi"],
                            LOAI_HANH_DONG,
                            str(nv_list[0].get("hanhDong") or "chi_tro_giai_thich"),
                        )
                if isinstance(patch.get("congThucLatexMoi"), list):
                    ct_moi: list[dict[str, Any]] = []
                    for idx_ct, ct in enumerate(patch["congThucLatexMoi"][:5]):
                        if not isinstance(ct, dict):
                            continue
                        lx_clean, _ = kiem_tra_latex(str(ct.get("latex") or ""))
                        if not lx_clean:
                            continue
                        muc_ct: dict[str, Any] = {
                            "latex": lx_clean,
                            "tuFrame": int(_ep_so(ct.get("tuFrame"), idx_ct * 35, 0, 400)),
                        }
                        if ct.get("nhan"):
                            muc_ct["nhan"] = str(ct["nhan"]).strip()[:85]
                        if isinstance(ct.get("noiBat"), bool):
                            muc_ct["noiBat"] = ct["noiBat"]
                        ct_moi.append(muc_ct)
                    if ct_moi:
                        c["congThucLatex"] = ct_moi
                if isinstance(patch.get("loiBinhHaiHuocMoi"), dict):
                    nd_lb = str(patch["loiBinhHaiHuocMoi"].get("noiDung") or "").strip()
                    if nd_lb:
                        vi_tri = (
                            patch["loiBinhHaiHuocMoi"].get("viTri")
                            if patch["loiBinhHaiHuocMoi"].get("viTri") in ("goc_phai", "goc_trai")
                            else "goc_phai"
                        )
                        c["loiBinhHaiHuoc"] = {
                            "noiDung": nd_lb[:140],
                            "viTri": vi_tri,
                            "tuFrame": int(_ep_so(patch["loiBinhHaiHuocMoi"].get("tuFrame"), 14, 0, 240)),
                        }
                da_sua.append({"id": cid, "lyDo": str(patch.get("lyDo") or "Cap nhat tu kiem dinh").strip()})

            for ct in c.get("congThucLatex") or []:
                if isinstance(ct, dict):
                    lx_clean, cbs = kiem_tra_latex(str(ct.get("latex") or ""))
                    ct["latex"] = lx_clean
                    for cb in cbs:
                        tat_ca_cb.append(f"[{cid}] {cb}")

    gan_frame_uoc_luong(kich_ban)
    return kich_ban, da_sua, tat_ca_cb


def tu_kiem_dinh_kich_ban(
    kich_ban: dict[str, Any],
    gemini: GeminiClient,
    tu_lieu_nghien_cuu: dict[str, Any] | None = None,
    canh_bao_latex: list[str] | None = None,
    duong_dan_bo_nho: Path | str | None = None,
) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    """
    Tang 3 - Tu kiem dinh (Self-Critique) & Tu rut kinh nghiem:
    1. Kiem tra chuan xac Toan hoc/lich su doi chieu tu lieu + cu phap ngoac {} trong LaTeX.
    2. Tu sua canh loi neu co.
    3. Tu them quy tac moi vao bo_nho_hoc_hoi.json neu phat hien mau loi moi.
    """
    canh_bao_thi_giac = phat_hien_canh_dung_yen(kich_ban)
    raw_critique = gemini.tao_json(
        prompt=tao_prompt_tu_kiem_dinh(
            kich_ban=kich_ban,
            tu_lieu_nghien_cuu=tu_lieu_nghien_cuu,
            canh_bao_latex=canh_bao_latex,
            canh_bao_thi_giac=canh_bao_thi_giac,
        ),
        system_instruction=(
            "Ban la chuyen gia kiem dinh Toan hoc, lich su, giu chan nguoi xem va bien tap phim hoat hinh hai huoc. "
            "Tra ve DUY NHAT JSON hop le."
        ),
        nhiet_do=0.3,
        max_output_tokens=16384,
    )
    if not isinstance(raw_critique, dict):
        raw_critique = {}

    kich_ban_sau, da_sua, canh_bao_moi = ap_dung_sua_tu_kiem_dinh(kich_ban, raw_critique)
    # Tieu chi kiem tra cung Tang 3: tu dong pha canh dung yen >6-8s, gan nhan vaiNoi & chay Guardrail storyboard
    kich_ban_sau, sua_nhip_thi_giac = kiem_dinh_nhip_ngat_thi_giac(kich_ban_sau, gan_vai_noi=True)
    kich_ban_sau, sua_guardrail = sua_loi_guardrail_cuc_bo(
        kich_ban_sau,
        tu_lieu_nghien_cuu=tu_lieu_nghien_cuu,
    )

    bai_hoc_luu: list[dict[str, Any]] = []
    raw_bai_hoc = raw_critique.get("baiHocMoi")
    if isinstance(raw_bai_hoc, list) and raw_bai_hoc:
        bo_nho = tai_bo_nho(duong_dan_bo_nho)
        for bh in raw_bai_hoc[:4]:
            if not isinstance(bh, dict):
                continue
            nd = str(bh.get("noiDung") or "").strip()
            if not nd:
                continue
            loai = str(bh.get("loai") or "kich_ban").strip()
            uu_tien = int(_ep_so(bh.get("mucDoUuTien"), 3, 1, 5))
            them_bai_hoc(bo_nho, loai=loai, noi_dung=nd, muc_do_uu_tien=uu_tien)
            bai_hoc_luu.append({"loai": loai, "noiDung": nd, "mucDoUuTien": uu_tien})
        if bai_hoc_luu:
            luu_bo_nho(bo_nho, duong_dan_bo_nho)

    bao_cao = {
        "diemTongThe": round(_ep_so(raw_critique.get("diemTongThe"), 8.5, 1.0, 10.0), 2),
        "nhanXetChung": str(raw_critique.get("nhanXetChung") or "").strip(),
        "canhDaSua": da_sua,
        "canhSuaNhipThiGiac": sua_nhip_thi_giac,
        "canhSuaGuardrail": sua_guardrail,
        "baiHocMoi": bai_hoc_luu,
    }
    return kich_ban_sau, bao_cao, canh_bao_moi


def tao_markdown_doc_duyet(
    du_lieu: dict[str, Any],
    canh_bao_latex: list[str] | None = None,
    tu_moi_giay: float = 2.65,
    bao_cao_kiem_dinh: dict[str, Any] | None = None,
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
        f"- **Tổng số từ lời thoại:** {tong_tu} từ (mục tiêu {TONG_TU_TOI_THIEU}–{TONG_TU_TOI_DA} từ)",
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

    goi_y_thumb = du_lieu.get("goiYThumbnail") or []
    if isinstance(goi_y_thumb, list) and goi_y_thumb:
        dong.extend(["", "## Gợi ý 3 phương án Thumbnail A/B (Test & Compare)"])
        for pa in goi_y_thumb[:3]:
            if isinstance(pa, dict):
                dong.append(
                    f"- **Biến thể {pa.get('bien_the', '?')}:** `{pa.get('tieuDeLon', '')}` "
                    f"| KaTeX: `{pa.get('congThucLatex', '')}` | Biểu cảm: `{pa.get('bieuCam', '')}` | Đạo cụ: `{pa.get('daoCuNoiBat', '')}`"
                )

    if bao_cao_kiem_dinh:
        dong.extend(
            [
                "",
                "## Tầng 3 — Tự kiểm định (Self-Critique)",
                f"- **Điểm tự đánh giá:** {bao_cao_kiem_dinh.get('diemTongThe', 0)}/10",
            ]
        )
        if bao_cao_kiem_dinh.get("nhanXetChung"):
            dong.append(f"- **Nhận xét chung:** {bao_cao_kiem_dinh['nhanXetChung']}")
        ds_sua = bao_cao_kiem_dinh.get("canhDaSua") or []
        dong.append(f"- **Số cảnh đã tự sửa:** {len(ds_sua)}")
        for s in ds_sua:
            dong.append(f"  - `{s.get('id', '')}`: {s.get('lyDo', '')}")
        ds_sua_tg = bao_cao_kiem_dinh.get("canhSuaNhipThiGiac") or []
        if ds_sua_tg:
            dong.append(f"- **Tự tối ưu nhịp ngắt thị giác (luật 6–8s):** {len(ds_sua_tg)} cảnh")
            for s in ds_sua_tg[:8]:
                dong.append(f"  - `{s.get('id', '')}` (`{s.get('hanhDong', '')}`): {s.get('lyDo', '')}")
        ds_sua_gr = bao_cao_kiem_dinh.get("canhSuaGuardrail") or []
        if ds_sua_gr:
            dong.append(f"- **Guardrail kiểm định tự động (v2.0):** {len(ds_sua_gr)} mục đã xử lý")
            for s in ds_sua_gr[:8]:
                dong.append(f"  - `{s.get('id', 'toan_tap')}` (`{s.get('loai', '')}`): {s.get('moTa', '')}")
        ds_bh = bao_cao_kiem_dinh.get("baiHocMoi") or []
        if ds_bh:
            dong.append(f"- **Bài học mới lưu vào bộ nhớ:** {len(ds_bh)}")
            for bh in ds_bh:
                dong.append(
                    f"  - `[{bh.get('loai', 'kich_ban')} | ưu tiên {bh.get('mucDoUuTien', 3)}/5]` {bh.get('noiDung', '')}"
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
            if c.get("vaiNoi"):
                nhan.append(f"`[VAI: {c['vaiNoi']}]`")
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
    tu_lieu_nghien_cuu: dict[str, Any] | None = None,
    duong_dan_bo_nho: Path | str | None = None,
    bat_tu_kiem_dinh: bool = True,
) -> tuple[Path, Path, dict[str, Any]]:
    """Chay tron ven 3 tang bien kich (tich hop tu lieu web + bo nho hoc hoi + tu kiem dinh) va xuat nhap_kich_ban.json + doc_duyet_kich_ban.md."""
    muc_tieu_thuc = max(10.5, float(muc_tieu_phut))
    goc_du_lieu = thu_muc_du_lieu or (GOC_DU_AN / "du_lieu")
    base_dir = goc_du_lieu / slug
    cache_dir = base_dir / "cache_chuong"
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Tu dong nap tu_lieu_nghien_cuu.json neu ton tai trong du_lieu/<slug>/
    tu_lieu_dung = tu_lieu_nghien_cuu
    if tu_lieu_dung is None:
        file_tu_lieu = base_dir / "tu_lieu_nghien_cuu.json"
        if file_tu_lieu.exists():
            try:
                tu_lieu_dung = json.loads(file_tu_lieu.read_text(encoding="utf-8"))
                print(f"[Bien kich] Da tu dong nap tu lieu nghien cuu: {file_tu_lieu}")
            except json.JSONDecodeError:
                tu_lieu_dung = None

    # Nap ngu canh hoc hoi tu bo_nho_hoc_hoi.json
    path_bo_nho = (
        Path(duong_dan_bo_nho)
        if duong_dan_bo_nho is not None
        else (goc_du_lieu / "bo_nho_hoc_hoi.json" if thu_muc_du_lieu is not None else DUONG_DAN_BO_NHO_MAC_DINH)
    )
    ngu_canh_hoc_hoi = tao_ngu_canh_hoc_hoi(duong_dan=path_bo_nho) if path_bo_nho.exists() else ""

    gemini = client or GeminiClient()

    # --- TANG 1: DAN Y 6 HOI ---
    file_blueprint = cache_dir / "dan_y_6_hoi.json"
    if file_blueprint.exists() and not bo_cache:
        print(f"[Tang 1] Tai cache dan y 6 hoi: {file_blueprint}")
        blueprint = json.loads(file_blueprint.read_text(encoding="utf-8"))
    else:
        print(f"[Tang 1] Dang lap Dan y 6 Hoi cho chu de: {chu_de} (~{muc_tieu_thuc:.1f} phut)...")
        raw_bp = gemini.tao_json(
            prompt=tao_prompt_tang_1(
                chu_de=chu_de,
                muc_tieu_phut=muc_tieu_thuc,
                giong_ke=giong_ke,
                tu_lieu_nghien_cuu=tu_lieu_dung,
                ngu_canh_hoc_hoi=ngu_canh_hoc_hoi,
            ),
            system_instruction=SYSTEM_BIEN_KICH,
            nhiet_do=0.75,
            max_output_tokens=16384,
        )
        danh_sach_nv_bp = chuan_hoa_danh_sach_nhan_vat(raw_bp.get("danhSachNhanVat"))
        tieu_de_bp = str(raw_bp.get("tieuDe") or chu_de).strip()
        blueprint = {
            "tieuDe": tieu_de_bp,
            "chuDe": str(raw_bp.get("chuDe") or chu_de).strip(),
            "hookMoMan": raw_bp.get("hookMoMan") if isinstance(raw_bp.get("hookMoMan"), dict) else {},
            "goiYThumbnail": chuan_hoa_goi_y_thumbnail(
                raw_bp.get("goiYThumbnail"),
                danh_sach_nv=danh_sach_nv_bp,
                tieu_de_video=tieu_de_bp,
            ),
            "bangMau": raw_bp.get("bangMau") or BANG_MAU_MAC_DINH,
            "danhSachNhanVat": danh_sach_nv_bp,
            "danhSachBoiCanhAI": chuan_hoa_danh_sach_boi_canh_ai(raw_bp.get("danhSachBoiCanhAI")),
            "cacHoi": [],
        }
        raw_cac_hoi = raw_bp.get("cacHoi") if isinstance(raw_bp.get("cacHoi"), list) else []
        for idx, khung in enumerate(KHUNG_6_HOI):
            item = raw_cac_hoi[idx] if idx < len(raw_cac_hoi) and isinstance(raw_cac_hoi[idx], dict) else {}
            tom_tat_hoi = str(item.get("tomTat") or khung["vaiTro"]).strip()
            phu_de_hoi = cat_gon_theo_tu(
                str(item.get("phuDeHoi") or tom_tat_hoi or f"Khám phá nội dung trọng tâm của Hồi {khung['soHoi']}").strip(),
                140,
            )
            blueprint["cacHoi"].append(
                {
                    "soHoi": khung["soHoi"],
                    "id": khung["id"],
                    "tenChuong": str(item.get("tenChuong") or f"{khung['soHoi']}. {khung['vaiTro']}").strip(),
                    "phuDeHoi": phu_de_hoi,
                    "boiCanhChinh": chuan_hoa_enum(item.get("boiCanhChinh"), LOAI_BOI_CANH, "bo_bien_hy_lap"),
                    "thoiTietChinh": chuan_hoa_enum(item.get("thoiTietChinh"), LOAI_THOI_TIET, "nang_dep"),
                    "tomTat": tom_tat_hoi,
                    "diemHaiHuoc": item.get("diemHaiHuoc") if isinstance(item.get("diemHaiHuoc"), list) else [],
                    "kienThucToan": str(item.get("kienThucToan") or "").strip(),
                }
            )
        file_blueprint.write_text(
            json.dumps(blueprint, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    nv_ids = [nv["id"] for nv in blueprint["danhSachNhanVat"]]

    # --- TANG 2: VIET CHI TIET 6 HOI NOI MACH ---
    danh_sach_chuong_raw: list[dict[str, Any]] = []
    tom_tat_hoi_truoc = "Đây là Hồi mở đầu, đặt người xem ngay vào bối cảnh và tình huống tò mò."
    su_kien_da_dung: list[str] = []

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
                    tu_lieu_nghien_cuu=tu_lieu_dung,
                    ngu_canh_hoc_hoi=ngu_canh_hoc_hoi,
                    su_kien_da_dung=su_kien_da_dung,
                ),
                system_instruction=SYSTEM_BIEN_KICH,
                nhiet_do=0.75,
                max_output_tokens=32768,
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
                    max_output_tokens=16384,
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

            # Dam bao canh dau tien cua hoi 1 la mo_dau, hoi 1..5 khong co boCuc='ket_thuc', va canh cuoi hoi 6 la ket_thuc
            if khung["soHoi"] < 6:
                for c_hoi in canh_hoi_sach:
                    if c_hoi.get("boCuc") == "ket_thuc":
                        c_hoi["boCuc"] = "ke_chuyen"
            if khung["soHoi"] == 1 and canh_hoi_sach:
                canh_hoi_sach[0]["boCuc"] = "mo_dau"
                canh_hoi_sach[0]["chuyenCanh"] = "vong_tron_hoat_hinh"
            if khung["soHoi"] == 6 and canh_hoi_sach:
                for c_hoi in canh_hoi_sach[:-1]:
                    if c_hoi.get("boCuc") == "ket_thuc":
                        c_hoi["boCuc"] = "ke_chuyen"
                canh_hoi_sach[-1]["boCuc"] = "ket_thuc"

            phu_de_hoi_kq = cat_gon_theo_tu(
                str(du_lieu_hoi.get("phuDeHoi") or thong_tin_hoi.get("phuDeHoi") or thong_tin_hoi["tomTat"]).strip(),
                140,
            )
            du_lieu_hoi = {
                "id": khung["id"],
                "tenChuong": thong_tin_hoi["tenChuong"],
                "phuDeHoi": phu_de_hoi_kq,
                "tomTatKetHoi": str(du_lieu_hoi.get("tomTatKetHoi") or thong_tin_hoi["tomTat"]).strip(),
                "suKienDaKe": [
                    str(x).strip()[:120]
                    for x in (du_lieu_hoi.get("suKienDaKe") or [])
                    if str(x).strip()
                ][:6],
                "canh": canh_hoi_sach,
            }
            file_cache_hoi.write_text(
                json.dumps(du_lieu_hoi, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )

        tom_tat_hoi_truoc = str(du_lieu_hoi.get("tomTatKetHoi") or thong_tin_hoi["tomTat"])
        sk_hoi_nay = du_lieu_hoi.get("suKienDaKe") if isinstance(du_lieu_hoi.get("suKienDaKe"), list) else []
        if sk_hoi_nay:
            for sk_item in sk_hoi_nay[:5]:
                su_kien_da_dung.append(f"Hoi {khung['soHoi']}: {sk_item}")
        else:
            su_kien_da_dung.append(f"Hoi {khung['soHoi']}: {tom_tat_hoi_truoc[:120]}")
        danh_sach_chuong_raw.append(du_lieu_hoi)

    # --- TANG 3: HAU KIEM LATEX + TU KIEM DINH (SELF-CRITIQUE) & TU RUT KINH NGHIEM ---
    raw_tong = {
        "tieuDe": blueprint["tieuDe"],
        "chuDe": blueprint["chuDe"],
        "batSfx": True,
        "batPhuDe": True,
        "bangMau": blueprint["bangMau"],
        "danhSachNhanVat": blueprint["danhSachNhanVat"],
        "danhSachBoiCanhAI": blueprint.get("danhSachBoiCanhAI") or [],
        "goiYThumbnail": blueprint.get("goiYThumbnail")
        or chuan_hoa_goi_y_thumbnail([], blueprint["danhSachNhanVat"], blueprint["tieuDe"]),
        "chuong": danh_sach_chuong_raw,
    }
    kich_ban_sach, canh_bao_latex = chuan_hoa_toan_bo_kich_ban(raw_tong)

    bao_cao_kiem_dinh: dict[str, Any] | None = None
    file_cache_kd = cache_dir / "tu_kiem_dinh.json"
    if bat_tu_kiem_dinh:
        if file_cache_kd.exists() and not bo_cache:
            print(f"[Tang 3] Tai cache tu kiem dinh: {file_cache_kd.name}")
            cache_kd = json.loads(file_cache_kd.read_text(encoding="utf-8"))
            bao_cao_kiem_dinh = cache_kd.get("baoCao")
            if isinstance(cache_kd.get("kichBanSauKiemDinh"), dict):
                kich_ban_sach = cache_kd["kichBanSauKiemDinh"]
                canh_bao_latex = list(cache_kd.get("canhBaoLatex") or [])
        else:
            print("[Tang 3] Dang chay Tu kiem dinh (Self-Critique) Toan hoc/lich su, LaTeX & nhip hai...")
            kich_ban_sach, bao_cao_kiem_dinh, canh_bao_latex = tu_kiem_dinh_kich_ban(
                kich_ban=kich_ban_sach,
                gemini=gemini,
                tu_lieu_nghien_cuu=tu_lieu_dung,
                canh_bao_latex=canh_bao_latex,
                duong_dan_bo_nho=path_bo_nho,
            )
            file_cache_kd.write_text(
                json.dumps(
                    {
                        "baoCao": bao_cao_kiem_dinh,
                        "canhBaoLatex": canh_bao_latex,
                        "kichBanSauKiemDinh": kich_ban_sach,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
                newline="\n",
            )
            print(
                f"[Tang 3] Tu kiem dinh xong: {bao_cao_kiem_dinh['diemTongThe']}/10 | "
                f"Da sua {len(bao_cao_kiem_dinh['canhDaSua'])} canh | "
                f"Guardrail {len(bao_cao_kiem_dinh.get('canhSuaGuardrail') or [])} muc | "
                f"Luu {len(bao_cao_kiem_dinh['baiHocMoi'])} bai hoc moi."
            )
    else:
        # Ke ca khi --bo-tu-kiem-dinh, van chay bo Guardrail kiem dinh Python tu dong
        kich_ban_sach, _ = sua_loi_guardrail_cuc_bo(
            kich_ban_sach,
            tu_lieu_nghien_cuu=tu_lieu_dung,
        )

    # Guardrail dau tieng Viet: phat hien bat ky chuoi >= 20 ky tu thieu dau va tu sua bang Gemini truoc khi xuat
    vi_pham_dau = kiem_tra_dau_tieng_viet(kich_ban_sach)
    if vi_pham_dau:
        print(f"[Guardrail Tiếng Việt] Phát hiện {len(vi_pham_dau)} chuỗi thiếu dấu (>=20 ký tự), đang tự sửa bằng Gemini...")
        kich_ban_sach, da_sua_dau = tu_dong_sua_dau_tieng_viet(kich_ban_sach, gemini=gemini)
        print(f"[Guardrail Tiếng Việt] Đã tự động khôi phục dấu cho {len(da_sua_dau)}/{len(vi_pham_dau)} chuỗi.")

    file_json = base_dir / "nhap_kich_ban.json"
    file_md = base_dir / "doc_duyet_kich_ban.md"
    file_json.write_text(
        json.dumps(kich_ban_sach, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    file_md.write_text(
        tao_markdown_doc_duyet(
            kich_ban_sach,
            canh_bao_latex,
            bao_cao_kiem_dinh=bao_cao_kiem_dinh,
        ),
        encoding="utf-8",
        newline="\n",
    )

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
        description="AI bien kich phim hoat hinh ke chuyen lich su Toan hoc >10 phut (3 tang + tu kiem dinh)."
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
    parser.add_argument(
        "--bo-tu-kiem-dinh",
        action="store_true",
        help="Bo qua luot AI Tu kiem dinh Tang 3.",
    )
    parser.add_argument(
        "--bo-nho",
        default="",
        help="Duong dan tuy chinh toi bo_nho_hoc_hoi.json.",
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
        duong_dan_bo_nho=Path(args.bo_nho) if args.bo_nho else None,
        bat_tu_kiem_dinh=not args.bo_tu_kiem_dinh,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
