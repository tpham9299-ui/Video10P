# -*- coding: utf-8 -*-
"""Bo test don vi offline (khong goi API that) cho he thong AI san xuat phim Toan hoc >10 phut (v0.5)."""

from __future__ import annotations

import array
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

GOC_DU_AN = Path(__file__).resolve().parents[1]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.bo_nho_hoc_hoi import (
    TOI_DA_BAI_HOC,
    chon_chu_de_tiep_theo,
    chuan_hoa_so_lieu_youtube,
    da_ton_tai_chu_de,
    doc_so_lieu_youtube_tu_file,
    ghi_nhan_tap_hoan_thanh,
    hoc_tu_phan_hoi,
    luu_bo_nho,
    main as main_bo_nho_hoc_hoi,
    nhap_so_lieu_youtube,
    nhap_so_lieu_youtube_tu_file,
    tai_bo_nho,
    tai_ngu_canh_kich_ban_doi_chieu,
    tao_ngu_canh_hoc_hoi,
    tao_parser as tao_parser_bo_nho,
    them_bai_hoc,
    them_chu_de_hang_doi,
)
from scripts.pipeline.dong_bo_youtube import (
    dong_bo_video_youtube,
    keo_thong_ke_video_youtube,
    lay_cau_hinh_youtube,
    main as main_dong_bo_youtube,
    tao_huong_dan_nhap_tay,
    tim_video_id_tu_bo_nho,
)
from scripts.pipeline.dang_youtube import (
    KICH_THUOC_CHUNK_MAC_DINH,
    LoiDangYouTube,
    MUI_GIO_VN,
    dang_video_len_youtube,
    danh_sach_bien_thieu,
    doc_tieu_de_va_mo_ta,
    doi_refresh_token_lay_access_token,
    lay_cau_hinh_oauth_youtube,
    main as main_dang_youtube,
    tai_video_resumable,
    tao_huong_dan_cau_hinh_youtube,
    tao_metadata_video,
    tinh_thoi_diem_cong_khai_vn,
    trich_xuat_the_tag,
)
from scripts.pipeline.lay_refresh_token_youtube import (
    YOUTUBE_SCOPES,
    doi_code_lay_tokens,
    tao_url_xac_thuc_google,
)
from scripts.pipeline.chuan_hoa_doc_toan import (
    TU_DIEN_PHAT_AM_MAC_DINH,
    ap_dung_tu_dien_phat_am,
    chuan_hoa_doc_toan,
    tai_tu_dien_phat_am,
)
from scripts.pipeline.chuanbi_dai import (
    NGHI_GIUA_LUOT_THOAI_GIAY,
    NGHI_TRUOC_PUNCHLINE_GIAY,
    THOI_GIAN_HIEN_DAP_AN_TOI_THIEU_GIAY,
    _chen_khoang_nghi_dau_mp3,
    bam_noi_dung_tts,
    can_chinh_mang_rms,
    chia_phu_de,
    chuan_bi_audio_va_du_lieu_render,
    chuan_hoa_bo_cuc_ket_thuc,
    dinh_dang_thoi_gian_srt,
    do_thoi_luong_ffprobe,
    kiem_tra_lien_mach_khung_hinh,
    kiem_tra_ro_ri_pythagoras,
    lay_cau_hinh_giong_nhan_vat,
    lay_cau_hinh_giong_theo_vai,
    ngat_dong_phu_de_srt,
    tao_noi_dung_srt,
    tao_parser as tao_parser_chuanbi_dai,
    tinh_bien_do_rms_tu_pcm,
    tinh_moc_va_rms_luot_thoai,
    tinh_toan_khung_hinh,
    trich_xuat_bien_do_rms,
    xac_dinh_cau_hinh_tts_canh,
    xuat_file_srt,
)
from scripts.pipeline.tao_boi_canh_ai import (
    GIOI_HAN_DUNG_LUONG_KB,
    LOAI_ANH_SANG_HOP_LE,
    MAC_DINH_IMAGE_MODELS,
    STYLE_BIBLE_BOI_CANH,
    STYLE_BIBLE_CAN_CANH_VAT_THE,
    TrinhTaoBoiCanhAI,
    bam_mo_ta_boi_canh,
    lap_ke_hoach_boi_canh_tap,
    lay_cau_hinh_anh_ai,
    luu_va_nen_anh_boi_canh,
    phan_tich_anh_sang_moi_truong,
    sinh_boi_canh_cho_tap,
    tao_prompt_boi_canh,
)
from scripts.pipeline.gemini_client import (
    GeminiClient,
    GeminiQuotaError,
    MAC_DINH_FALLBACK_MODELS,
    MAC_DINH_MODEL,
    lam_sach_json,
    lay_cau_hinh_gemini,
    lay_fallback_models,
    parse_json_an_toan,
)
from scripts.pipeline.render_dai import (
    NGUONG_CHIA_CHUNK_GIAY,
    THUMBNAIL_STILL_ID,
    chay_visual_qa_gemini,
    chon_chuong_can_render,
    chuan_bi_phuong_an_thumbnail,
    chuan_hoa_bao_cao_visual_qa,
    chuan_hoa_du_lieu_truoc_render,
    dang_chay_tren_ci,
    dinh_dang_thoi_gian_youtube,
    dung_lenh_hau_ky_audio_ffmpeg,
    dung_lenh_render_remotion,
    dung_lenh_render_thumbnail,
    ghep_cac_hoi_ffmpeg,
    ghep_luoi_kiem_dinh,
    giai_danh_sach_file_ghep,
    main as main_render_dai,
    phan_tich_danh_sach_chuong_chon,
    render_bo_thumbnail,
    render_mot_chunk,
    render_mot_hoi,
    render_toan_bo_video,
    tao_chapters_va_mo_ta,
    tao_filter_hau_ky_audio,
    tao_noi_dung_chapters,
    tao_parser as tao_parser_render_dai,
    tao_prompt_visual_qa,
    tinh_danh_sach_chunk_render,
    tinh_hash_chuong,
    tinh_pham_vi_frame_chuong,
    xac_dinh_nhac_nen,
    xac_dinh_tham_so_render_ci,
)
from scripts.pipeline.san_tim_chu_de import (
    nap_hang_doi_chu_de,
    nghien_cuu_chu_de,
    tra_cuu_tom_tat_wikipedia,
)
from scripts.pipeline.san_xuat_lien_tuc import (
    chay_san_xuat_lien_tuc,
    hoan_tat_tap_tu_meta,
    tao_parser as tao_parser_san_xuat,
)
from scripts.pipeline.tao_kich_ban_10p import (
    DO_TUOI_NHAN_VAT,
    GOC_QUAY_CAMERA,
    KHUNG_6_HOI,
    LOAI_BIEU_CAM,
    LOAI_BOI_CANH,
    LOAI_BO_CUC,
    LOAI_CANH,
    LOAI_DAO_CU,
    LOAI_HANH_DONG,
    LOAI_HIEU_UNG_HOAT_HINH,
    LOAI_MINH_HOA_TOAN,
    LOAI_PHU_KIEN,
    LOAI_THOI_TIET,
    LOAI_VAI_NOI,
    LOAI_VAT_CAM_TAY,
    LOAI_VAT_THE_XUNG_QUANH,
    TU_THE_NHAN_VAT,
    bien_kich_3_tang,
    cat_gon_theo_tu,
    chuan_hoa_buoc_ve_toan,
    chuan_hoa_canh,
    chuan_hoa_goi_y_thumbnail,
    chuan_hoa_toan_bo_kich_ban,
    kiem_dinh_guardrail_kich_ban,
    kiem_dinh_nhip_ngat_thi_giac,
    kiem_dinh_schema_du_lieu_canh,
    kiem_tra_dau_tieng_viet,
    kiem_tra_lap_y_toan_tap,
    kiem_tra_latex,
    la_canh_doi_thoai_hoac_tuong_tac,
    lay_goc_quay_canh,
    phat_hien_canh_dung_yen,
    sua_loi_guardrail_cuc_bo,
    suy_luan_vai_noi_canh,
    tao_markdown_doc_duyet,
    tao_prompt_tang_1,
    tao_prompt_tang_2_hoi,
    tao_prompt_tu_kiem_dinh,
    tao_slug,
    tu_dong_sua_dau_tieng_viet,
    tu_kiem_dinh_kich_ban,
)


def _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi: int = 18) -> dict[str, Any]:
    """Tao kich ban 6 hoi x 18 canh = 108 canh (~11+ phut) de test offline."""
    chuong = []
    stt = 1
    for h in range(1, 7):
        canh_list = []
        for c in range(so_canh_moi_hoi):
            bo_cuc = "ke_chuyen"
            if h == 1 and c == 0:
                bo_cuc = "mo_dau"
            elif h == 3 and c in (4, 10):
                bo_cuc = "giai_thich_toan"
            elif h == 4 and c in (5, 11):
                bo_cuc = "hai_huoc"
            elif h == 6 and c == so_canh_moi_hoi - 1:
                bo_cuc = "ket_thuc"

            muc: dict[str, Any] = {
                "id": f"canh_{stt:03d}",
                "boCuc": bo_cuc,
                "boiCanh": "lop_hoc_bang_xanh" if bo_cuc == "giai_thich_toan" else "bo_bien_hy_lap",
                "thoiTiet": "ban_dem" if h == 6 else "nang_dep",
                "tuFrame": 0,
                "denFrame": 180,
                "tieuDeNho": f"Cảnh {stt} của hồi {h}",
                "loiThoai": (
                    f"Ở hồi {h} cảnh {stt}, các nhà Toán học phát hiện ra đường chéo √2 không thể viết "
                    f"thành phân số p/q dù thử tới 3.14 lần vào khoảng 500 TCN."
                ),
                "nhanVat": [
                    {
                        "id": "pythagoras",
                        "x": 760,
                        "y": 810,
                        "huong": "phai",
                        "hanhDong": "chi_tro_giai_thich",
                        "bieuCam": "vui_tuoi",
                        "dangNoi": True,
                    }
                ],
            }
            if bo_cuc == "giai_thich_toan":
                muc["congThucLatex"] = [
                    {"latex": "\\sqrt{2} = \\frac{p}{q}", "nhan": "Giả sử tối giản", "tuFrame": 0},
                    {"latex": "p^2 = 2q^2", "nhan": "Bình phương hai vế", "tuFrame": 40, "noiBat": True},
                ]
                muc["minhHoaToan"] = {"loai": "tam_giac_vuong", "tieuDe": "Tam giác 1-1-√2"}
            if bo_cuc == "hai_huoc":
                muc["loiBinhHaiHuoc"] = {"noiDung": "Lỗi 404: Không tìm thấy phân số!", "viTri": "goc_phai", "tuFrame": 12}
                muc["hieuUngHoatHinh"] = [
                    {"loai": "giot_mo_hoi", "x": 960, "y": 460, "tuFrame": 10, "thoiLuong": 80}
                ]
            canh_list.append(muc)
            stt += 1

        chuong.append(
            {
                "id": f"chuong_{h}",
                "tenChuong": f"{h}. Hồi thứ {h} của câu chuyện Toán",
                "canh": canh_list,
            }
        )

    return {
        "tieuDe": "Pythagoras & Cú Sốc √2",
        "chuDe": "Bí mật số vô tỉ làm rung chuyển Hy Lạp cổ đại",
        "batSfx": False,
        "batPhuDe": True,
        "bangMau": {
            "nenChinh": "#0EA5E9",
            "nenPhu": "#FEF3C7",
            "luoi": "#CBD5E1",
            "chuChinh": "#FFFFFF",
            "chuPhu": "#FEF08A",
            "nhanManh": "#FACC15",
            "canhBao": "#FB923C",
        },
        "danhSachNhanVat": [
            {
                "id": "pythagoras",
                "ten": "Pythagoras",
                "mauThan": "#1E293B",
                "mauChuDao": "#2563EB",
                "mauDa": "#FFFDF7",
                "phuKien": "vong_nguyet_que",
            },
            {
                "id": "hippasus",
                "ten": "Hippasus",
                "mauThan": "#1E293B",
                "mauChuDao": "#EA580C",
                "mauDa": "#FFFDF7",
                "phuKien": "kinh_tron",
            },
        ],
        "chuong": chuong,
    }


class TestChuanHoaDocToan(unittest.TestCase):
    def test_ky_hieu_co_ban(self) -> None:
        self.assertIn("căn bậc hai của 2", chuan_hoa_doc_toan("Đường chéo bằng √2"))
        self.assertIn("pi", chuan_hoa_doc_toan("Số π rất đặc biệt"))
        self.assertIn("x bình phương", chuan_hoa_doc_toan("Xét hàm x^2 + 1"))
        self.assertIn("x lập phương", chuan_hoa_doc_toan("Thể tích x³"))
        self.assertIn("2 mũ n", chuan_hoa_doc_toan("Tăng theo 2^n"))
        self.assertIn("vô cực", chuan_hoa_doc_toan("Khi tiến tới ∞"))
        self.assertIn("trước Công nguyên", chuan_hoa_doc_toan("Vào năm ~500 TCN"))

    def test_so_thap_phan_va_phan_so(self) -> None:
        self.assertIn("3 phẩy 14", chuan_hoa_doc_toan("Giá trị xấp xỉ 3.14"))
        self.assertIn("1 phẩy 414", chuan_hoa_doc_toan("Bằng khoảng 1,414"))
        self.assertIn("1000 năm", chuan_hoa_doc_toan("Suốt 1.000 năm qua"))
        self.assertIn("p phần q", chuan_hoa_doc_toan("Viết thành phân số p/q"))
        self.assertIn("một phần hai", chuan_hoa_doc_toan("Chia đúng 1/2 diện tích"))
        self.assertIn("22 phần 7", chuan_hoa_doc_toan("Gần đúng 22/7"))
        self.assertIn("90 độ", chuan_hoa_doc_toan("Góc vuông 90°"))
        self.assertIn("50 phần trăm", chuan_hoa_doc_toan("Tỉ lệ 50%"))

    def test_latex_trong_loi_thoai(self) -> None:
        kq = chuan_hoa_doc_toan(r"Ta có $\frac{a}{b} = \sqrt{2}$ và $\pi \approx 3.14$")
        self.assertIn("a phần b", kq)
        self.assertIn("căn bậc hai của 2", kq)
        self.assertIn("pi", kq)
        self.assertIn("3 phẩy 14", kq)


class TestGeminiClientOffline(unittest.TestCase):
    def test_doc_env_nhieu_key_va_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            env1 = Path(tmp) / ".env.multi"
            env1.write_text(
                (
                    "GEMINI_API_KEYS=keyA, keyB , keyC\n"
                    "GEMINI_MODEL=gemini-2.5-pro\n"
                    "GEMINI_FALLBACK_MODELS=gemini-flash-latest, gemini-pro-latest , gemini-flash-latest\n"
                ),
                encoding="utf-8",
            )
            keys, model = lay_cau_hinh_gemini(
                duong_dan_env=env1,
                env_override={"GEMINI_API_KEYS": "k1,k2", "GEMINI_MODEL": "gemini-flash-latest"},
            )
            self.assertEqual(keys, ["k1", "k2"])
            self.assertEqual(model, "gemini-flash-latest")

            fb1 = lay_fallback_models(duong_dan_env=env1, env_override={})
            self.assertEqual(fb1, ["gemini-flash-latest", "gemini-pro-latest"])

            # Test fallback GEMINI_API_KEY + model mac dinh moi (gemini-flash-latest) + fallback mac dinh
            keys2, model2 = lay_cau_hinh_gemini(
                duong_dan_env=Path(tmp) / "khong_ton_tai",
                env_override={"GEMINI_API_KEYS": "", "GEMINI_API_KEY": "single_key", "GEMINI_MODEL": ""},
            )
            self.assertEqual(keys2, ["single_key"])
            self.assertEqual(model2, MAC_DINH_MODEL)
            self.assertEqual(model2, "gemini-flash-latest")

            fb2 = lay_fallback_models(
                duong_dan_env=Path(tmp) / "khong_ton_tai",
                env_override={"GEMINI_FALLBACK_MODELS": ""},
            )
            self.assertEqual(fb2, list(MAC_DINH_FALLBACK_MODELS))
            self.assertEqual(
                fb2,
                [
                    "gemini-2.5-flash",
                    "gemini-2.5-flash-lite",
                    "gemini-flash-latest",
                    "gemini-flash-lite-latest",
                    "gemini-2.0-flash",
                    "gemini-pro-latest",
                ],
            )

    def test_xoay_vong_key_khi_429_503_va_thu_lai_json(self) -> None:
        lich_su_keys: list[str] = []
        phan_hoi = [
            (429, '{"error": {"status": "RESOURCE_EXHAUSTED"}}'),
            (503, "Service Unavailable"),
            (200, json.dumps({"candidates": [{"content": {"parts": [{"text": "{loi_json_thieu_ngoac"}]}}]})),
            (
                200,
                json.dumps(
                    {
                        "candidates": [
                            {
                                "content": {
                                    "parts": [
                                        {"text": 'Day la JSON:\n```json\n{"ok": true, "so": 42,}\n```'}
                                    ]
                                }
                            }
                        ]
                    }
                ),
            ),
        ]
        con_tro = {"i": 0}

        def fake_http(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            lich_su_keys.append(api_key)
            idx = con_tro["i"]
            con_tro["i"] += 1
            return phan_hoi[idx]

        client = GeminiClient(
            api_keys=["key_1", "key_2", "key_3"],
            model="gemini-flash-latest",
            http_caller=fake_http,
            sleep_fn=lambda _: None,
        )
        ket_qua = client.tao_json("Tra ve JSON test")
        self.assertEqual(ket_qua, {"ok": True, "so": 42})
        # Key 1 gap 429 -> xoay sang key 2 gap 503 -> xoay sang key 3 tra JSON loi -> retry tren key 3 thanh cong
        self.assertEqual(lich_su_keys, ["key_1", "key_2", "key_3", "key_3"])

    def test_tu_do_model_khi_404_va_ghi_nho_trong_phien(self) -> None:
        lich_su_post: list[str] = []
        lich_su_get: list[str] = []

        def fake_post(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            lich_su_post.append(url)
            if "/models/gemini-1.5-flash-cu:generateContent" in url:
                return 404, '{"error": {"code": 404, "message": "models/gemini-1.5-flash-cu is not found"}}'
            if "/models/gemini-flash-latest:generateContent" in url:
                return (
                    200,
                    json.dumps(
                        {"candidates": [{"content": {"parts": [{"text": "OK tu gemini-flash-latest"}]}}]}
                    ),
                )
            return 500, "Unexpected model"

        def fake_get(url: str, timeout: int) -> tuple[int, str]:
            lich_su_get.append(url)
            danh_sach = {
                "models": [
                    {
                        "name": "models/text-embedding-004",
                        "supportedGenerationMethods": ["embedContent", "generateContent"],
                    },
                    {
                        "name": "models/aqa",
                        "supportedGenerationMethods": ["generateAnswer", "generateContent"],
                    },
                    {
                        "name": "models/gemini-2.5-flash-preview-tts",
                        "supportedGenerationMethods": ["generateContent"],
                    },
                    {
                        "name": "models/gemini-2.0-flash-exp-image-generation",
                        "supportedGenerationMethods": ["generateContent"],
                    },
                    {
                        "name": "models/gemini-2.5-flash-khong-ho-tro",
                        "supportedGenerationMethods": ["countTokens"],
                    },
                    {
                        "name": "models/gemini-2.0-flash",
                        "supportedGenerationMethods": ["generateContent"],
                    },
                    {
                        "name": "models/gemini-2.5-flash",
                        "supportedGenerationMethods": ["generateContent"],
                    },
                    {
                        "name": "models/gemini-flash-latest",
                        "supportedGenerationMethods": ["generateContent"],
                    },
                    {
                        "name": "models/gemini-2.5-pro",
                        "supportedGenerationMethods": ["generateContent"],
                    },
                ]
            }
            return 200, json.dumps(danh_sach)

        client = GeminiClient(
            api_keys=["key_1", "key_2"],
            model="gemini-1.5-flash-cu",
            fallback_models=["gemini-1.5-flash-cu"],
            http_caller=fake_post,
            http_get_caller=fake_get,
            sleep_fn=lambda _: None,
        )

        # Luot 1: 404 -> tu do qua GET /v1beta/models?key=key_1 -> chuyen sang gemini-flash-latest
        kq1 = client.tao_van_ban("Xin chao lan 1")
        self.assertEqual(kq1, "OK tu gemini-flash-latest")
        self.assertEqual(client.model, "gemini-flash-latest")
        self.assertEqual(
            lich_su_get,
            ["https://generativelanguage.googleapis.com/v1beta/models?key=key_1"],
        )

        # Luot 2: da ghi nho gemini-flash-latest -> goi thang, khong goi lai model cu hay GET /models
        kq2 = client.tao_van_ban("Xin chao lan 2")
        self.assertEqual(kq2, "OK tu gemini-flash-latest")
        self.assertEqual(len(lich_su_get), 1)
        self.assertEqual(len(lich_su_post), 3)
        self.assertIn("/models/gemini-1.5-flash-cu:generateContent", lich_su_post[0])
        self.assertIn("/models/gemini-flash-latest:generateContent", lich_su_post[1])
        self.assertIn("/models/gemini-flash-latest:generateContent", lich_su_post[2])

    def test_tu_do_model_khi_400_sai_ten_chon_flash_moi_nhat(self) -> None:
        def fake_post(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            if "/models/model-sai-ten:generateContent" in url:
                return 400, '{"error": {"code": 400, "message": "Unexpected model name format"}}'
            if "/models/gemini-2.5-flash:generateContent" in url:
                return (
                    200,
                    json.dumps({"candidates": [{"content": {"parts": [{"text": "OK 2.5 flash"}]}}]}),
                )
            return 500, f"Unexpected URL: {url}"

        def fake_get(url: str, timeout: int) -> tuple[int, str]:
            # Khong co gemini-flash-latest -> phai loc bo embedding/tts/image/aqa va chon flash moi nhat (2.5)
            danh_sach = {
                "models": [
                    {"name": "models/gemini-embedding-001", "supportedGenerationMethods": ["generateContent"]},
                    {"name": "models/gemini-2.5-flash-tts", "supportedGenerationMethods": ["generateContent"]},
                    {"name": "models/gemini-2.5-flash-image", "supportedGenerationMethods": ["generateContent"]},
                    {"name": "models/aqa", "supportedGenerationMethods": ["generateContent"]},
                    {"name": "models/gemini-1.5-flash", "supportedGenerationMethods": ["generateContent"]},
                    {"name": "models/gemini-2.0-flash", "supportedGenerationMethods": ["generateContent"]},
                    {"name": "models/gemini-2.5-flash-preview-05-20", "supportedGenerationMethods": ["generateContent"]},
                    {"name": "models/gemini-2.5-flash", "supportedGenerationMethods": ["generateContent"]},
                    {"name": "models/gemini-2.5-pro", "supportedGenerationMethods": ["generateContent"]},
                ]
            }
            return 200, json.dumps(danh_sach)

        client = GeminiClient(
            api_keys=["key_1"],
            model="model-sai-ten",
            fallback_models=["model-sai-ten"],
            http_caller=fake_post,
            http_get_caller=fake_get,
            sleep_fn=lambda _: None,
        )
        kq = client.tao_van_ban("Thu 400 sai ten model")
        self.assertEqual(kq, "OK 2.5 flash")
        self.assertEqual(client.model, "gemini-2.5-flash")

    def test_xoay_het_key_429_tu_chuyen_fallback_model(self) -> None:
        lich_su_goi: list[tuple[str, str]] = []

        def fake_post(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            model_name = url.split("/models/")[1].split(":")[0]
            lich_su_goi.append((model_name, api_key))
            if model_name == "gemini-flash-latest":
                return 429, '{"error": {"status": "RESOURCE_EXHAUSTED"}}'
            if model_name == "gemini-flash-lite-latest" and api_key == "key_1":
                return 429, '{"error": {"status": "RESOURCE_EXHAUSTED"}}'
            if model_name == "gemini-flash-lite-latest" and api_key == "key_2":
                return (
                    200,
                    json.dumps({"candidates": [{"content": {"parts": [{"text": "OK tu flash-lite"}]}}]}),
                )
            return 429, '{"error": {"status": "RESOURCE_EXHAUSTED"}}'

        client = GeminiClient(
            api_keys=["key_1", "key_2"],
            model="gemini-flash-latest",
            fallback_models=[
                "gemini-flash-latest",
                "gemini-flash-lite-latest",
                "gemini-pro-latest",
            ],
            http_caller=fake_post,
            sleep_fn=lambda _: None,
        )
        kq = client.tao_van_ban("Test 429 doi fallback")
        self.assertEqual(kq, "OK tu flash-lite")
        self.assertEqual(client.model, "gemini-flash-lite-latest")
        # Xoay het key_1, key_2 o gemini-flash-latest -> chuyen sang gemini-flash-lite-latest -> thanh cong o key_2
        self.assertEqual(
            lich_su_goi,
            [
                ("gemini-flash-latest", "key_1"),
                ("gemini-flash-latest", "key_2"),
                ("gemini-flash-lite-latest", "key_1"),
                ("gemini-flash-lite-latest", "key_2"),
            ],
        )

        # Neu tat ca key va tat ca fallback deu 429 -> bao GeminiQuotaError sau khi thu du cac model
        models_da_thu_het: list[str] = []

        def always_429(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            m = url.split("/models/")[1].split(":")[0]
            if m not in models_da_thu_het:
                models_da_thu_het.append(m)
            return 429, '{"error": {"status": "RESOURCE_EXHAUSTED"}}'

        client_het = GeminiClient(
            api_keys=["key_1", "key_2"],
            model="gemini-flash-latest",
            fallback_models=[
                "gemini-flash-latest",
                "gemini-flash-lite-latest",
                "gemini-pro-latest",
            ],
            http_caller=always_429,
            sleep_fn=lambda _: None,
        )
        with self.assertRaises(GeminiQuotaError):
            client_het.tao_van_ban("Test het sach quota")
        self.assertEqual(
            models_da_thu_het,
            ["gemini-flash-latest", "gemini-flash-lite-latest", "gemini-pro-latest"],
        )

    def test_lam_sach_json(self) -> None:
        raw = 'Loi mo dau...\n```json\n{"a": 1, "b": [2, 3,],}\n```\nLoi ket.'
        self.assertEqual(parse_json_an_toan(raw), {"a": 1, "b": [2, 3]})
        self.assertTrue(lam_sach_json(raw).startswith("{"))

    def test_backoff_503_3_vong_chuyen_nhanh_429_2s_va_loc_model_chuan(self) -> None:
        import io
        from unittest import mock

        from scripts.pipeline.gemini_client import (
            LICH_BACKOFF_THEO_VONG,
            SO_VONG_TOI_DA_MAC_DINH,
            THOI_GIAN_NGHI_CHUYEN_MODEL_429_GIAY,
            THOI_GIAN_NGHI_DOI_KEY_GIAY,
            TU_KHOA_LOAI_BO_MODEL,
            loc_va_xep_hang_models,
        )

        self.assertEqual(LICH_BACKOFF_THEO_VONG, (8.0, 20.0, 40.0))
        self.assertEqual(SO_VONG_TOI_DA_MAC_DINH, 3)
        self.assertEqual(THOI_GIAN_NGHI_DOI_KEY_GIAY, 1.0)
        self.assertEqual(THOI_GIAN_NGHI_CHUYEN_MODEL_429_GIAY, 2.0)

        # 0. Bo loc ListModels: loc sach toan bo model chuyen biet/khong phu hop sinh van ban
        for tk in (
            "transcribe",
            "computer-use",
            "robotics",
            "nano-banana",
            "neon",
            "image",
            "imagen",
            "veo",
            "tts",
            "audio",
            "embedding",
            "aqa",
            "learnlm",
            "exp",
        ):
            self.assertIn(tk, TU_KHOA_LOAI_BO_MODEL)

        ds_tho = [
            {"name": "models/gemini-4-neon", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-3.5-transcribe", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-2.5-computer-use-preview-10-2025", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-nano-banana-2.1", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-robotics-er-2-preview", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-2.5-flash-image", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/imagen-3.0-generate-002", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/veo-2.0-generate-001", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-2.5-flash-tts", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-2.5-flash-native-audio", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-embedding-001", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/aqa", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/learnlm-2.0-flash", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-2.0-flash-exp", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-2.5-flash", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-2.5-flash-lite", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-flash-latest", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-2.0-flash", "supportedGenerationMethods": ["generateContent"]},
            {"name": "models/gemini-pro-latest", "supportedGenerationMethods": ["generateContent"]},
        ]
        ds_sach = loc_va_xep_hang_models(ds_tho)
        self.assertEqual(
            set(ds_sach),
            {
                "gemini-flash-latest",
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
                "gemini-2.0-flash",
                "gemini-pro-latest",
            },
        )

        # 1. Hang doi model mac dinh: khi bat dau tu gemini-flash-latest, gemini-pro-latest LUON o cuoi cung
        client_q = GeminiClient(
            api_keys=["k1"],
            model="gemini-flash-latest",
            fallback_models=list(MAC_DINH_FALLBACK_MODELS),
            http_caller=lambda u, p, k, t: (200, "{}"),
            sleep_fn=lambda _: None,
        )
        hang_doi = client_q._tao_hang_doi_model()
        self.assertEqual(hang_doi[0], "gemini-flash-latest")
        self.assertEqual(hang_doi[-1], "gemini-pro-latest")
        self.assertIn("gemini-2.5-flash", hang_doi[:-1])
        self.assertIn("gemini-2.5-flash-lite", hang_doi[:-1])
        self.assertIn("gemini-2.0-flash", hang_doi[:-1])

        # 2. Khi tat ca key deu 429 tren 1 model -> nghi dung 2.0s roi chuyen ngay sang model du phong (KHONG lap 3 vong)
        cho_429: list[float] = []
        goi_429: list[tuple[str, str]] = []

        def fake_429_all_keys(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            m = url.split("/models/")[1].split(":")[0]
            goi_429.append((m, api_key))
            return 429, '{"error": {"status": "RESOURCE_EXHAUSTED"}}'

        client_429 = GeminiClient(
            api_keys=["key_1", "key_2"],
            model="gemini-2.5-flash",
            fallback_models=["gemini-2.5-flash", "gemini-2.5-flash-lite"],
            http_caller=fake_429_all_keys,
            sleep_fn=cho_429.append,
        )
        with self.assertRaises(GeminiQuotaError):
            client_429.tao_van_ban("Test 429 chuyen nhanh 2s")
        # Moi model chi thu dung 1 vong (2 key), giua 2 key nghi 1.0s, chuyen model nghi 2.0s, model cuoi thoat ngay!
        self.assertEqual(
            goi_429,
            [
                ("gemini-2.5-flash", "key_1"),
                ("gemini-2.5-flash", "key_2"),
                ("gemini-2.5-flash-lite", "key_1"),
                ("gemini-2.5-flash-lite", "key_2"),
            ],
        )
        self.assertEqual(cho_429, [1.0, 2.0, 1.0])

        # 3. Gap 503 lien tiep 2 vong (4 luot voi 2 key) -> nghi 1.0s doi key, 8s/20s het vong -> thanh cong o vong 3
        cac_lan_cho: list[float] = []
        luot_503 = {"n": 0}

        def fake_503_then_ok(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            luot_503["n"] += 1
            if luot_503["n"] <= 4:
                return 503, '{"error": {"code": 503, "message": "The model is overloaded. Please try again later."}}'
            return 200, json.dumps({"candidates": [{"content": {"parts": [{"text": "OK sau 2 vong 503"}]}}]})

        client_503 = GeminiClient(
            api_keys=["key_1", "key_2"],
            model="gemini-2.5-flash",
            fallback_models=["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-pro-latest"],
            http_caller=fake_503_then_ok,
            sleep_fn=cac_lan_cho.append,
        )
        buf = io.StringIO()
        with mock.patch("sys.stdout", buf):
            kq = client_503.tao_van_ban("Test 503 backoff 3 vong")
        self.assertEqual(kq, "OK sau 2 vong 503")
        self.assertEqual(client_503.model, "gemini-2.5-flash")
        self.assertEqual(cac_lan_cho, [1.0, 8.0, 1.0, 20.0])
        log_txt = buf.getvalue()
        self.assertIn("vong 1/3", log_txt)
        self.assertIn("vong 2/3", log_txt)
        self.assertIn("8.0s", log_txt)
        self.assertIn("20.0s", log_txt)

        # 4. Gap 503 tron 3 vong tren model 1 -> nghi du 8s, 20s, 40s roi sang model du phong 2
        cac_lan_cho_2: list[float] = []
        models_goi: list[str] = []

        def fake_503_full_3_vong(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            m = url.split("/models/")[1].split(":")[0]
            models_goi.append(m)
            if m == "gemini-2.5-flash":
                return 503, "Service Unavailable"
            return 200, json.dumps({"candidates": [{"content": {"parts": [{"text": "OK tu 2.5-flash-lite"}]}}]})

        client_chuyen = GeminiClient(
            api_keys=["key_1", "key_2"],
            model="gemini-2.5-flash",
            fallback_models=["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-pro-latest"],
            http_caller=fake_503_full_3_vong,
            sleep_fn=cac_lan_cho_2.append,
        )
        kq2 = client_chuyen.tao_van_ban("Test 503 chuyen model sau 3 vong")
        self.assertEqual(kq2, "OK tu 2.5-flash-lite")
        self.assertEqual(client_chuyen.model, "gemini-2.5-flash-lite")
        self.assertEqual(models_goi.count("gemini-2.5-flash"), 6)  # 3 vong x 2 key
        self.assertEqual(cac_lan_cho_2, [1.0, 8.0, 1.0, 20.0, 1.0, 40.0])

        # 5. Google Search Grounding gap 503 tren tat ca key/model -> tu ha cap goi khong dung search thanh cong
        luot_search: list[tuple[str, bool]] = []

        def fake_grounding_503(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            m = url.split("/models/")[1].split(":")[0]
            co_search = bool(payload.get("tools"))
            luot_search.append((m, co_search))
            if co_search:
                return 503, "Search Grounding Overloaded"
            return 200, json.dumps({"candidates": [{"content": {"parts": [{"text": '{"ok": true}'}]}}]})

        client_gs = GeminiClient(
            api_keys=["key_1"],
            model="gemini-2.5-flash",
            fallback_models=["gemini-2.5-flash"],
            so_vong_toi_da=2,
            lich_backoff_theo_vong=(0.0, 0.0),
            nghi_doi_key_giay=0.0,
            http_caller=fake_grounding_503,
            sleep_fn=lambda _: None,
        )
        kq_gs, nguon_gs = client_gs.tao_json("Nghien cuu web", bat_tim_kiem_web=True, tra_ve_nguon=True)
        self.assertEqual(kq_gs, {"ok": True})
        self.assertEqual(nguon_gs, [])
        self.assertTrue(any(cs for _, cs in luot_search))
        self.assertEqual(luot_search[-1], ("gemini-2.5-flash", False))


class TestSanitizerVaBienKichOffline(unittest.TestCase):
    def test_sanitizer_enum_va_latex(self) -> None:
        raw_ban = {
            "tieuDe": "Test Sanitizer",
            "chuDe": "Kiem thu enum",
            "danhSachNhanVat": [
                {"id": "euclid", "ten": "Euclid", "mauThan": "sai_mau", "mauChuDao": "#2563EB", "phuKien": "mu_bay_mau"}
            ],
            "chuong": [
                {
                    "id": "chuong_1",
                    "tenChuong": "Hồi 1",
                    "canh": [
                        {
                            "boCuc": "bo_cuc_la",
                            "boiCanh": "vu_tru_la",
                            "thoiTiet": "bao_cat",
                            "chuyenCanh": "nhay_lo_xo",
                            "loiThoai": "Đây là lời thoại kiểm thử sanitizer enum hoàn toàn hợp lệ.",
                            "camera": {"kieu": "quay_360", "zoom": 9.9},
                            "nhanVat": [
                                {
                                    "id": "nhan_vat_ma",
                                    "x": 9999,
                                    "y": 50,
                                    "huong": "len_tren",
                                    "hanhDong": "bay_len_troi",
                                    "bieuCam": "sieu_buon",
                                    "vatCamTay": "kiem_laser",
                                }
                            ],
                            "hieuUngHoatHinh": [
                                {"loai": "no_tung", "x": -100, "y": 5000, "tuFrame": -5, "thoiLuong": 999}
                            ],
                            "minhHoaToan": {"loai": "hinh_bat_ky", "thamSo": {"a": 3, "sai": True}},
                            "congThucLatex": [
                                {"latex": "$\\frac{p}{q$"},
                                {"latex": "a^2 + b^2 = c^2"},
                            ],
                        }
                    ],
                }
            ],
        }

        sach, canh_bao = chuan_hoa_toan_bo_kich_ban(raw_ban)
        self.assertEqual(sach["danhSachNhanVat"][0]["phuKien"], "khong")
        self.assertIn(sach["danhSachNhanVat"][0]["phuKien"], LOAI_PHU_KIEN)

        c = sach["chuong"][0]["canh"][0]
        self.assertIn(c["boCuc"], LOAI_BO_CUC)
        self.assertIn(c["boiCanh"], LOAI_BOI_CANH)
        self.assertIn(c["thoiTiet"], LOAI_THOI_TIET)
        nv = c["nhanVat"][0]
        self.assertEqual(nv["id"], "euclid")
        self.assertIn(nv["hanhDong"], LOAI_HANH_DONG)
        self.assertIn(nv["bieuCam"], LOAI_BIEU_CAM)
        self.assertIn(nv["vatCamTay"], LOAI_VAT_CAM_TAY)
        self.assertTrue(140 <= nv["x"] <= 1780)
        self.assertIn(c["hieuUngHoatHinh"][0]["loai"], LOAI_HIEU_UNG_HOAT_HINH)
        self.assertIn(c["minhHoaToan"]["loai"], LOAI_MINH_HOA_TOAN)
        # Canh bao thieu ngoac } trong \frac{p}{q
        self.assertGreaterEqual(len(canh_bao), 1)
        self.assertTrue(c["congThucLatex"][0]["latex"].endswith("}"))

    def test_kiem_tra_latex_ngoac(self) -> None:
        clean_ok, cb_ok = kiem_tra_latex(r"\sqrt{2} = \frac{p}{q}")
        self.assertEqual(cb_ok, [])
        self.assertEqual(clean_ok, r"\sqrt{2} = \frac{p}{q}")

        clean_fix, cb_fix = kiem_tra_latex(r"\frac{1}{2")
        self.assertEqual(clean_fix, r"\frac{1}{2}")
        self.assertTrue(any("Thieu 1 ngoac dong" in w for w in cb_fix))

    def test_bien_kich_3_tang_tu_dong_bo_sung_va_cache(self) -> None:
        # Mock GeminiClient: Hoi 1 tra ngan (<250 tu) de kich hoat luot bo sung tu dong
        class FakeGemini:
            def __init__(self) -> None:
                self.so_lan_goi = 0

            def tao_json(self, prompt: str, **kwargs: Any) -> Any:
                self.so_lan_goi += 1
                if "DAN Y 6 HOI" in prompt:
                    return {
                        "tieuDe": "Hành Trình Số 0",
                        "chuDe": "Vì sao con số không từng bị cấm đoán?",
                        "danhSachNhanVat": [
                            {"id": "brahmagupta", "ten": "Brahmagupta", "mauThan": "#1E293B", "mauChuDao": "#2563EB", "phuKien": "ao_choang"}
                        ],
                        "cacHoi": [
                            {
                                "soHoi": i,
                                "id": f"chuong_{i}",
                                "tenChuong": f"{i}. Hồi {i}",
                                "boiCanhChinh": "thu_vien_co_dien",
                                "thoiTietChinh": "nang_dep",
                                "tomTat": f"Tóm tắt hồi {i}",
                                "diemHaiHuoc": ["Miếng hài vui"],
                                "kienThucToan": "0 + a = a",
                            }
                            for i in range(1, 7)
                        ],
                    }
                if "TU KIEM DINH" in prompt:
                    return {
                        "diemTongThe": 9.1,
                        "nhanXetChung": "Kich ban mach lac, hai huoc di dom va dung kien thuc Toan hoc.",
                        "canhCanSua": [],
                        "baiHocMoi": [],
                    }
                if "canhBoSung" in prompt:
                    return {
                        "canhBoSung": [
                            {
                                "boCuc": "hai_huoc",
                                "boiCanh": "phong_nen_hai_huoc",
                                "loiThoai": " ".join(["Chi tiết giai thoại bổ sung rất thú vị về số không"] * 3),
                                "loiBinhHaiHuoc": {"noiDung": "Không có gì mà lại có tất cả!"},
                                "nhanVat": [{"id": "brahmagupta", "x": 960, "y": 810, "huong": "phai", "hanhDong": "bo_tay_can_loi", "bieuCam": "can_loi_mat_do"}],
                            }
                            for _ in range(4)
                        ]
                    }
                # Tra ve 15 canh; rieng Hoi 1 chi co 4 canh ngan de kich hoat bo sung
                if "HOI 1/6" in prompt:
                    return {
                        "id": "chuong_1",
                        "tenChuong": "1. Hồi 1",
                        "tomTatKetHoi": "Hết hồi 1",
                        "canh": [
                            {"boCuc": "ke_chuyen", "loiThoai": "Cảnh mở màn ngắn gây tò mò về con số không ở Ấn Độ cổ đại."}
                            for _ in range(4)
                        ],
                    }
                return {
                    "id": "chuong_x",
                    "tenChuong": "Hồi đầy đủ",
                    "tomTatKetHoi": "Hết hồi",
                    "canh": [
                        {
                            "boCuc": "giai_thich_toan" if idx == 2 else "ke_chuyen",
                            "loiThoai": " ".join(["Lời thoại kể chuyện lịch sử Toán học sống động và dí dỏm"] * 2),
                            "congThucLatex": [{"latex": "a + 0 = a"}] if idx == 2 else None,
                            "minhHoaToan": {"loai": "chuoi_suy_luan"} if idx == 2 else None,
                        }
                        for idx in range(15)
                    ],
                }

        with tempfile.TemporaryDirectory() as tmp:
            fake = FakeGemini()
            f_json, f_md, kq = bien_kich_3_tang(
                chu_de="Lịch sử số 0",
                slug=tao_slug("Lịch sử số 0"),
                muc_tieu_phut=11,
                client=fake,  # type: ignore[arg-type]
                thu_muc_du_lieu=Path(tmp),
            )
            self.assertTrue(f_json.exists())
            self.assertTrue(f_md.exists())
            self.assertEqual(len(kq["chuong"]), 6)
            # Hoi 1 da duoc bo sung tu 4 canh -> 8 canh va canh dau bat buoc la mo_dau
            self.assertEqual(len(kq["chuong"][0]["canh"]), 8)
            self.assertEqual(kq["chuong"][0]["canh"][0]["boCuc"], "mo_dau")
            self.assertEqual(kq["chuong"][5]["canh"][-1]["boCuc"], "ket_thuc")
            # 1 blueprint + 6 hoi + 1 luot bo sung cho hoi 1 + 1 luot tu kiem dinh tang 3 = 9 luot goi
            self.assertEqual(fake.so_lan_goi, 9)
            md_text = f_md.read_text(encoding="utf-8")
            self.assertIn("[TOÁN / KaTeX]", md_text)
            self.assertIn("[HÀI]", md_text)
            self.assertIn("Tự kiểm định", md_text)

            # Chay lai lan 2 phai dung 100% cache (so_lan_goi khong tang!)
            bien_kich_3_tang(
                chu_de="Lịch sử số 0",
                slug=tao_slug("Lịch sử số 0"),
                muc_tieu_phut=11,
                client=fake,  # type: ignore[arg-type]
                thu_muc_du_lieu=Path(tmp),
            )
            self.assertEqual(fake.so_lan_goi, 9)


class TestTinhFrameVaCacheAudio(unittest.TestCase):
    def test_tinh_frame_tren_10_phut_khong_lech_khong_chong(self) -> None:
        du_lieu = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=18)  # 108 canh
        # Gia lap moi canh doc ~5.8s -> 108 * (5.8 + 0.25) ~ 653s (~19.600+ frames > 18.000)
        thoi_luong = {f"canh_{i:03d}": 5.8 for i in range(1, 109)}

        kq, thong_ke = tinh_toan_khung_hinh(du_lieu, thoi_luong, slug="pythagoras_10p", fps=30)
        self.assertTrue(thong_ke["datTren10Phut"])
        self.assertGreaterEqual(thong_ke["tongFrames"], 18000)
        self.assertGreaterEqual(thong_ke["tongGiay"], 600.0)

        # Kiem tra lien mach 100%: khong khoang trong, khong chong de
        tat_ca = [c for ch in kq["chuong"] for c in ch["canh"]]
        self.assertEqual(len(tat_ca), 108)
        self.assertEqual(tat_ca[0]["tuFrame"], 0)
        for i in range(1, len(tat_ca)):
            self.assertEqual(
                tat_ca[i]["tuFrame"],
                tat_ca[i - 1]["denFrame"],
                f"Lech frame giua {tat_ca[i - 1]['id']} va {tat_ca[i]['id']}",
            )
            self.assertGreater(tat_ca[i]["denFrame"], tat_ca[i]["tuFrame"])

        # Kiem tra khoang nghi chuyen hoi (0.75s) lon hon giua canh (0.25s)
        canh_giua_hoi = tat_ca[0]
        canh_cuoi_hoi_1 = tat_ca[17]
        self.assertEqual(canh_giua_hoi["denFrame"] - canh_giua_hoi["tuFrame"], 182)  # ceil((5.8+0.25)*30)=182
        self.assertEqual(canh_cuoi_hoi_1["denFrame"] - canh_cuoi_hoi_1["tuFrame"], 197)  # ceil((5.8+0.75)*30)=197

        # Kiem tra audioSrc dung dinh dang forward slash cho staticFile()
        self.assertEqual(tat_ca[0]["audioSrc"], "audio/pythagoras_10p/canh_001.mp3")
        # Kiem tra phuDe duoc chia gon gang
        self.assertGreaterEqual(len(tat_ca[0]["phuDe"]), 2)
        for dong in tat_ca[0]["phuDe"]:
            self.assertLessEqual(len(dong), 90)

    def test_cache_sha256_chi_sinh_lai_2_cau_sua(self) -> None:
        du_lieu = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=2)  # 12 canh cho nhanh
        sinh_lan_1: list[str] = []
        sinh_lan_2: list[str] = []

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            du_lieu_dir = root / "du_lieu"
            public_dir = root / "public"
            slug = "test_cache"
            (du_lieu_dir / slug).mkdir(parents=True)
            file_nhap = du_lieu_dir / slug / "nhap_kich_ban.json"
            file_nhap.write_text(json.dumps(du_lieu, ensure_ascii=False), encoding="utf-8")

            def gen1(cid: str, txt: str, path: Path) -> None:
                sinh_lan_1.append(cid)
                path.write_bytes(b"FAKE_MP3_" + cid.encode("ascii"))

            chuan_bi_audio_va_du_lieu_render(
                slug=slug,
                thu_muc_du_lieu=du_lieu_dir,
                thu_muc_public=public_dir,
                tts_generator=gen1,
                duration_prober=lambda _: 5.5,
            )
            self.assertEqual(len(sinh_lan_1), 12)

            # Sua dung 2 cau thoai roi chay lai
            du_lieu["chuong"][0]["canh"][1]["loiThoai"] = "Câu thoại thứ hai vừa được người dùng chỉnh sửa lại!"
            du_lieu["chuong"][3]["canh"][0]["loiThoai"] = "Câu thoại mở đầu hồi 4 cũng vừa được cập nhật mới!"
            file_nhap.write_text(json.dumps(du_lieu, ensure_ascii=False), encoding="utf-8")

            def gen2(cid: str, txt: str, path: Path) -> None:
                sinh_lan_2.append(cid)
                path.write_bytes(b"FAKE_MP3_V2_" + cid.encode("ascii"))

            file_render, thong_ke = chuan_bi_audio_va_du_lieu_render(
                slug=slug,
                thu_muc_du_lieu=du_lieu_dir,
                thu_muc_public=public_dir,
                tts_generator=gen2,
                duration_prober=lambda _: 5.5,
            )
            self.assertTrue(file_render.exists())
            self.assertEqual(sinh_lan_2, ["canh_002", "canh_007"])
            self.assertFalse(thong_ke["datTren10Phut"])  # 12 canh < 600s -> bao co False

    def test_chia_phu_de_va_bam_tts(self) -> None:
        h1 = bam_noi_dung_tts("Xin chào", "vi-VN-NamMinhNeural")
        h2 = bam_noi_dung_tts("Xin chào", "vi-VN-HoaiMyNeural")
        self.assertNotEqual(h1, h2)
        phu_de = chia_phu_de(
            "Câu đầu tiên rất ngắn gọn. Câu thứ hai dài hơn một chút để kiểm tra bộ tách dòng phụ đề tự động cho màn hình 16:9 cực kỳ sắc nét.",
            max_ky_tu=70,
        )
        self.assertGreaterEqual(len(phu_de), 2)
        self.assertTrue(all(len(p) <= 75 for p in phu_de))


class TestRenderChaptersVaLuoiKiemDinh(unittest.TestCase):
    def test_pham_vi_frame_va_chapters_txt(self) -> None:
        du_lieu = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=18)
        thoi_luong = {f"canh_{i:03d}": 5.8 for i in range(1, 109)}
        du_lieu_render, _ = tinh_toan_khung_hinh(du_lieu, thoi_luong, slug="pythagoras", fps=30)

        pham_vi = tinh_pham_vi_frame_chuong(du_lieu_render)
        self.assertEqual(len(pham_vi), 6)
        # Kiem tra --frames inclusive khong trung bien giua cac hoi
        for i in range(1, len(pham_vi)):
            self.assertEqual(pham_vi[i]["tuFrame"], pham_vi[i - 1]["endFrameInclusive"] + 1)

        chapters = tao_noi_dung_chapters(du_lieu_render, fps=30)
        dong = [d for d in chapters.strip().splitlines() if d.strip()]
        self.assertEqual(len(dong), 6)
        self.assertTrue(dong[0].startswith("00:00 "))
        # Hoi 6 phai o khoang 09:xx hoac hon trong video > 10 phut
        self.assertRegex(dong[-1], r"^\d{2}:\d{2} 6\.")
        self.assertEqual(dinh_dang_thoi_gian_youtube(3665), "1:01:05")

    def test_cache_hash_chuong_va_chon_chuong(self) -> None:
        du_lieu = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=4)
        thoi_luong = {f"canh_{i:03d}": 5.0 for i in range(1, 25)}
        du_lieu_render, _ = tinh_toan_khung_hinh(du_lieu, thoi_luong, slug="demo", fps=30)
        pham_vi = tinh_pham_vi_frame_chuong(du_lieu_render)

        with tempfile.TemporaryDirectory() as tmp:
            thu_muc_hoi = Path(tmp) / "chuong"
            thu_muc_hoi.mkdir()
            cache = {}
            for ch in pham_vi:
                (thu_muc_hoi / f"hoi_{ch['soHoi']:02d}.mp4").write_bytes(b"MP4")
                cache[ch["id"]] = tinh_hash_chuong(du_lieu_render, ch["chuongData"], thu_muc_public=Path(tmp))

            # Khong doi -> bo qua tat ca 6 hoi
            ke_hoach_1 = chon_chuong_can_render(pham_vi, du_lieu_render, cache, thu_muc_hoi, thu_muc_public=Path(tmp))
            self.assertEqual([x[2] for x in ke_hoach_1], [False] * 6)

            # Chi dinh --chuong 2,4 -> chi render lai dung hoi 2 va 4
            tap = phan_tich_danh_sach_chuong_chon("2,4")
            ke_hoach_2 = chon_chuong_can_render(
                pham_vi, du_lieu_render, cache, thu_muc_hoi, chuong_ep_render=tap, thu_muc_public=Path(tmp)
            )
            self.assertEqual([x[0]["soHoi"] for x in ke_hoach_2 if x[2]], [2, 4])

            # Sua 1 canh o Hoi 3 -> tu dong phat hien va chi render lai Hoi 3
            du_lieu_render["chuong"][2]["canh"][0]["loiThoai"] += " (đã sửa)"
            pham_vi_moi = tinh_pham_vi_frame_chuong(du_lieu_render)
            ke_hoach_3 = chon_chuong_can_render(pham_vi_moi, du_lieu_render, cache, thu_muc_hoi, thu_muc_public=Path(tmp))
            self.assertEqual([x[0]["soHoi"] for x in ke_hoach_3 if x[2]], [3])

    def test_tao_luoi_kiem_dinh_18_khung_hinh_pillow(self) -> None:
        from PIL import Image

        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            cac_o: list[tuple[Path, str]] = []
            for h in range(1, 7):
                for m in range(1, 4):
                    p = tmp_dir / f"tile_{h}_{m}.png"
                    img = Image.new("RGB", (320, 180), color=(30 * h, 60 * m, 140))
                    img.save(p)
                    cac_o.append((p, f"Hồi {h} (#{m}) • 0{h}:0{m}"))

            out_png = tmp_dir / "luoi_kiem_dinh.png"
            ghep_luoi_kiem_dinh(cac_o, out_png, tieu_de="Kiểm định 18 khung hình")
            self.assertTrue(out_png.exists())
            with Image.open(out_png) as grid:
                self.assertEqual(grid.format, "PNG")
                # 3 cot x 480 + 4*14 = 1496; 6 hang x 270 + header 54 + 7*14 = 1772
                self.assertEqual(grid.size, (1496, 1772))


class TestHeThongTuChuV05Offline(unittest.TestCase):
    def test_google_search_grounding_payload_va_trich_nguon_voi_xoay_key(self) -> None:
        payloads_ghi_nhan: list[dict[str, Any]] = []
        keys_da_goi: list[str] = []
        models_da_goi: list[str] = []

        def fake_post(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            payloads_ghi_nhan.append(payload)
            keys_da_goi.append(api_key)
            model_name = url.split("/models/")[1].split(":")[0]
            models_da_goi.append(model_name)

            if len(keys_da_goi) == 1:
                return 429, '{"error": {"status": "RESOURCE_EXHAUSTED"}}'
            if len(keys_da_goi) == 2:
                return 429, '{"error": {"status": "RESOURCE_EXHAUSTED"}}'

            body = {
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {"text": '```json\n{"suKien": "7 cay cau Konigsberg", "nam": 1736}\n```'}
                            ]
                        },
                        "groundingMetadata": {
                            "webSearchQueries": ["Euler seven bridges of Konigsberg 1736"],
                            "groundingChunks": [
                                {
                                    "web": {
                                        "uri": "https://en.wikipedia.org/wiki/Seven_Bridges_of_K%C3%B6nigsberg",
                                        "title": "Seven Bridges of Konigsberg - Wikipedia",
                                    }
                                },
                                {
                                    "web": {
                                        "uri": "https://mathshistory.st-andrews.ac.uk/Biographies/Euler/",
                                        "title": "Leonhard Euler - MacTutor",
                                    }
                                },
                                {
                                    "web": {
                                        "uri": "https://en.wikipedia.org/wiki/Seven_Bridges_of_K%C3%B6nigsberg",
                                        "title": "Trung URL phai bi loai",
                                    }
                                },
                            ],
                        },
                    }
                ]
            }
            return 200, json.dumps(body)

        client = GeminiClient(
            api_keys=["key_1", "key_2"],
            model="gemini-flash-latest",
            fallback_models=["gemini-flash-latest", "gemini-pro-latest"],
            http_caller=fake_post,
            sleep_fn=lambda _: None,
        )

        du_lieu, nguon = client.tao_json(
            "Tim thong tin ve Euler va 7 cay cau Konigsberg",
            bat_tim_kiem_web=True,
            tra_ve_nguon=True,
        )
        self.assertEqual(du_lieu, {"suKien": "7 cay cau Konigsberg", "nam": 1736})
        # Moi request deu gan tools: [{"google_search": {}}] va khong gay xung dot responseMimeType
        self.assertEqual(len(payloads_ghi_nhan), 3)
        for pl in payloads_ghi_nhan:
            self.assertEqual(pl.get("tools"), [{"google_search": {}}])
            self.assertNotIn("responseMimeType", pl.get("generationConfig", {}))
        # Xoay het key_1, key_2 o gemini-flash-latest -> tu chuyen sang gemini-pro-latest
        self.assertEqual(
            models_da_goi,
            ["gemini-flash-latest", "gemini-flash-latest", "gemini-pro-latest"],
        )
        # Trich nguon khong trung lap tu groundingChunks
        self.assertEqual(len(nguon), 2)
        self.assertIn("Seven_Bridges", nguon[0]["url"])
        self.assertEqual(client.nguon_tham_khao_gan_nhat, nguon)

    def test_bo_nho_hoc_hoi_chong_trung_gioi_han_25_va_ngu_canh(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path_bn = Path(tmp) / "bo_nho_hoc_hoi.json"
            bo_nho = tai_bo_nho(path_bn)
            self.assertTrue(path_bn.exists())
            for k in ("chu_de_da_lam", "hang_doi_chu_de", "bai_hoc_rut_ra", "phan_hoi_kenh"):
                self.assertIn(k, bo_nho)

            # Ghi nhan 1 tap da lam
            ghi_nhan_tap_hoan_thanh(
                bo_nho,
                slug="pythagoras_vo_ti",
                tieu_de="Pythagoras và Cú Sốc Số Vô Tỉ √2",
                nhan_vat_chinh="Pythagoras, Hippasus",
                tom_tat_1_cau="Hippasus chứng minh √2 không viết được thành phân số làm hội Pythagoras đứng hình.",
                thoi_luong_giay=672.5,
                nguon_tham_khao=["https://en.wikipedia.org/wiki/Hippasus"],
            )
            self.assertTrue(da_ton_tai_chu_de(bo_nho, "pythagoras_vo_ti"))
            self.assertTrue(
                da_ton_tai_chu_de(bo_nho, "khac_slug", "Pythagoras và cú sốc số vô tỉ √2")
            )

            # Them hang doi: 1 trung chu_de_da_lam, 2 moi, 1 trung trong cung luot
            da_them = them_chu_de_hang_doi(
                bo_nho,
                [
                    {"slug": "pythagoras_vo_ti", "tieuDe": "Pythagoras và số vô tỉ", "diemThuHut": 9.9, "doSauToanHoc": 9.9},
                    {"slug": "euler_7_cay_cau", "tieuDe": "Euler và 7 Cây Cầu Königsberg", "diemThuHut": 9.4, "doSauToanHoc": 9.1},
                    {"slug": "euler_7_cay_cau", "tieuDe": "Trùng slug Euler", "diemThuHut": 7.0, "doSauToanHoc": 7.0},
                    {"slug": "ramanujan_so_tay", "tieuDe": "Ramanujan và Cuốn Sổ Tay Bí Ẩn", "diemThuHut": 9.1, "doSauToanHoc": 8.7},
                ],
            )
            self.assertEqual([x["slug"] for x in da_them], ["euler_7_cay_cau", "ramanujan_so_tay"])
            chon = chon_chu_de_tiep_theo(bo_nho)
            self.assertIsNotNone(chon)
            assert chon is not None
            self.assertEqual(chon["slug"], "euler_7_cay_cau")

            # Them 30 bai hoc khac biet ro rang + 1 bai trung -> phai gop bai trung va giu toi da 25 bai uu tien cao nhat
            tu_khoa_khac_nhau = [
                "tam giác vuông cổ đại", "phân số tối giản", "đồ thị cầu Konigsberg", "chuỗi vô hạn Euler",
                "số ảo mặt phẳng phức", "hình học phi Euclid", "xác suất xúc xắc", "nguyên lý chuồng bồ câu",
                "dãy Fibonacci tự nhiên", "tỉ lệ vàng kiến trúc", "logarit thiên văn", "tích phân diện tích",
                "đạo hàm vận tốc tức thời", "nhóm đối xứng Galois", "số nguyên tố sàng Eratosthenes",
                "nghịch lý khách sạn Hilbert", "tập hợp vô hạn Cantor", "định lý bốn màu bản đồ",
                "ma trận biến đổi đồ họa", "mã hóa khóa công khai RSA", "hình học fractal tuyết",
                "định lý Bayes suy luận", "hàm zeta Riemann", "phép đo bán kính Trái Đất",
                "bàn tính cổ đại", "lịch sử số không Ấn Độ", "hệ nhị phân máy tính",
                "đường cong cycloid nhanh nhất", "định lý Noether bảo toàn", "bài toán người bán hàng",
            ]
            for i, chu_de_bh in enumerate(tu_khoa_khac_nhau, start=1):
                them_bai_hoc(
                    bo_nho,
                    loai="toan_hoc" if i % 2 == 0 else "hai_huoc",
                    noi_dung=f"Khi minh họa chủ đề {chu_de_bh}, hãy kiểm tra kỹ ví dụ trực quan #{i}.",
                    muc_do_uu_tien=5 if i > 20 else 2,
                    ngay=f"2026-11-{(i % 28) + 1:02d}",
                )
            # Bai trung noi dung -> khong lam vuot gioi han va giu ban gop
            them_bai_hoc(
                bo_nho,
                loai="toan_hoc",
                noi_dung="Khi minh họa chủ đề bài toán người bán hàng, hãy kiểm tra kỹ ví dụ trực quan #30.",
                muc_do_uu_tien=5,
            )
            self.assertEqual(len(bo_nho["bai_hoc_rut_ra"]), TOI_DA_BAI_HOC)
            # Tat ca 10 bai uu tien 5 (21..30) phai duoc giu lai
            uu_tien_5 = [b for b in bo_nho["bai_hoc_rut_ra"] if b["mucDoUuTien"] == 5]
            self.assertEqual(len(uu_tien_5), 10)
            luu_bo_nho(bo_nho, path_bn)

            # Tiem ngu canh hoc hoi
            ngu_canh = tao_ngu_canh_hoc_hoi(duong_dan=path_bn)
            self.assertIn("Pythagoras", ngu_canh)
            self.assertIn("callback", ngu_canh)
            self.assertIn("uu tien 5/5", ngu_canh)

            # Test --hoc-tu-phan-hoi voi mock Gemini
            class FakeFeedbackGemini:
                def tao_json(self, prompt: str, **kwargs: Any) -> Any:
                    return {
                        "baiHocMoi": [
                            {
                                "loai": "hai_huoc",
                                "noiDung": "Tăng thêm 1 câu bình luận góc màn hình ở phút thứ 6 để giữ nhịp xem.",
                                "mucDoUuTien": 5,
                            }
                        ]
                    }

            moi = hoc_tu_phan_hoi(
                slug="pythagoras_vo_ti",
                ghi_chu="Khán giả thích đoạn hài hước nhưng phút 6 hơi lắng.",
                duong_dan=path_bn,
                client=FakeFeedbackGemini(),  # type: ignore[arg-type]
            )
            self.assertEqual(len(moi), 1)
            bo_nho_moi = tai_bo_nho(path_bn)
            self.assertEqual(len(bo_nho_moi["phan_hoi_kenh"]), 1)
            self.assertLessEqual(len(bo_nho_moi["bai_hoc_rut_ra"]), TOI_DA_BAI_HOC)

    def test_san_tim_chu_de_va_nghien_cuu_web_wikipedia_offline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path_bn = root / "bo_nho_hoc_hoi.json"
            bo_nho = tai_bo_nho(path_bn)
            ghi_nhan_tap_hoan_thanh(
                bo_nho,
                slug="so_0_an_do",
                tieu_de="Hành Trình Số 0 Ấn Độ",
                nhan_vat_chinh="Brahmagupta",
                tom_tat_1_cau="Số 0 từ dấu chấm nhỏ thành nền tảng đại số.",
                thoi_luong_giay=650,
            )
            luu_bo_nho(bo_nho, path_bn)

            goi_bat_search: list[bool] = []

            class FakeResearchGemini:
                def tao_json(self, prompt: str, **kwargs: Any) -> Any:
                    goi_bat_search.append(bool(kwargs.get("bat_tim_kiem_web")))
                    if "chuDeDeXuat" in prompt:
                        return {
                            "chuDeDeXuat": [
                                {
                                    "slug": "so_0_an_do",
                                    "tieuDe": "Hành Trình Số 0 Ấn Độ",
                                    "gocKhaiThac": "Trung lap phai bi loai",
                                    "diemThuHut": 9.0,
                                    "doSauToanHoc": 9.0,
                                },
                                {
                                    "slug": "euler_7_cay_cau",
                                    "tieuDe": "Euler và 7 Cây Cầu Königsberg",
                                    "gocKhaiThac": "Từ trò đố đi dạo đến Lý thuyết Đồ thị và Google Maps.",
                                    "diemThuHut": 9.4,
                                    "doSauToanHoc": 9.0,
                                },
                                {
                                    "slug": "cantor_vo_cuc",
                                    "tieuDe": "Georg Cantor và Những Cấp Độ Vô Cực",
                                    "gocKhaiThac": "Vô cực này lớn hơn vô cực kia như thế nào?",
                                    "diemThuHut": 9.2,
                                    "doSauToanHoc": 9.5,
                                },
                            ]
                        }
                    du_lieu = {
                        "tieuDe": "Leonhard Euler và Bài Toán 7 Cây Cầu Königsberg",
                        "tomTat1Cau": "Euler biến 7 cây cầu thành đồ thị điểm-cạnh năm 1736 và khai sinh Lý thuyết Đồ thị.",
                        "nienDaiChuan": [{"nam": "1736", "suKien": "Euler trình bày lời giải tại Viện Hàn lâm St. Petersburg."}],
                        "nhanVatThat": [
                            {"ten": "Leonhard Euler", "vaiTro": "Nhà Toán học Thụy Sĩ", "nienDai": "1707-1783", "tinhCachDoiThuong": "Siêu năng suất và dí dỏm"}
                        ],
                        "giaiThoaiDoiThuong": [
                            {"tieuDe": "Trò đố cuối tuần", "noiDung": "Người dân Königsberg thi nhau đi dạo qua 7 cây cầu.", "diemHaiHuoc": "Ai cũng kẹt ở cây cầu thứ 7!"},
                            {"tieuDe": "Bức thư ban đầu", "noiDung": "Euler ban đầu tưởng đây chỉ là trò giải trí nhỏ.", "diemHaiHuoc": "Ai ngờ lại đẻ ra cả ngành Toán mới."},
                            {"tieuDe": "Mảnh đất hóa điểm", "noiDung": "Euler vứt bỏ bản đồ rườm rà, chỉ giữ 4 chấm và 7 nét.", "diemHaiHuoc": "Thiết kế tối giản đi trước thời đại 300 năm."},
                        ],
                        "kienThucToanCotLoi": [
                            {
                                "tenKienThuc": "Định lý đường đi Euler",
                                "giaiThichDeHieu": "Đồ thị liên thông có tối đa 2 đỉnh bậc lẻ mới đi qua mọi cạnh đúng 1 lần.",
                                "congThucLatex": r"\sum_{v \in V} \deg(v) = 2|E|",
                                "yNghia": "Khởi đầu Lý thuyết Đồ thị và Topo học.",
                            }
                        ],
                        "ungDungHienDai": ["Dẫn đường GPS / Google Maps", "Tối ưu mạng máy tính"],
                        "nguonThamKhao": ["https://mathshistory.st-andrews.ac.uk/Biographies/Euler/"],
                    }
                    nguon = [{"tieuDe": "MacTutor", "url": "https://mathshistory.st-andrews.ac.uk/Biographies/Euler/"}]
                    if kwargs.get("tra_ve_nguon"):
                        return du_lieu, nguon
                    return du_lieu

            def fake_wiki(url: str, timeout: int) -> tuple[int, str]:
                if "vi.wikipedia.org/api/rest_v1/page/summary/" in url:
                    return 200, json.dumps(
                        {
                            "title": "Bảy cây cầu ở Königsberg",
                            "extract": "Bài toán bảy cây cầu ở Königsberg được Leonhard Euler giải quyết năm 1736.",
                            "content_urls": {
                                "desktop": {"page": "https://vi.wikipedia.org/wiki/Bay_cay_cau_o_Konigsberg"}
                            },
                        }
                    )
                return 404, ""

            fake_gemini = FakeResearchGemini()
            them = nap_hang_doi_chu_de(so_luong=5, duong_dan_bo_nho=path_bn, client=fake_gemini)  # type: ignore[arg-type]
            self.assertEqual([t["slug"] for t in them], ["euler_7_cay_cau", "cantor_vo_cuc"])

            wiki_res = tra_cuu_tom_tat_wikipedia("Euler", wiki_fetcher=fake_wiki)
            self.assertEqual(len(wiki_res), 1)
            self.assertEqual(wiki_res[0]["ngonNgu"], "vi")

            file_tl, tl = nghien_cuu_chu_de(
                slug="euler_7_cay_cau",
                thu_muc_du_lieu=root,
                duong_dan_bo_nho=path_bn,
                client=fake_gemini,  # type: ignore[arg-type]
                wiki_fetcher=fake_wiki,
            )
            self.assertTrue(file_tl.exists())
            self.assertEqual(len(tl["giaiThoaiDoiThuong"]), 3)
            self.assertIn("https://vi.wikipedia.org/wiki/Bay_cay_cau_o_Konigsberg", tl["nguonThamKhao"])
            self.assertIn("https://mathshistory.st-andrews.ac.uk/Biographies/Euler/", tl["nguonThamKhao"])
            self.assertEqual(goi_bat_search, [True, True])

    def test_tu_kiem_dinh_sua_canh_va_luu_bai_hoc_moi(self) -> None:
        du_lieu = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=2)
        with tempfile.TemporaryDirectory() as tmp:
            path_bn = Path(tmp) / "bo_nho_hoc_hoi.json"
            tai_bo_nho(path_bn)

            class FakeCritiqueGemini:
                def tao_json(self, prompt: str, **kwargs: Any) -> Any:
                    self.prompt_da_nhan = prompt
                    return {
                        "diemTongThe": 8.4,
                        "nhanXetChung": "Phát hiện 1 lỗi công thức cần chỉnh ở canh_001.",
                        "canhCanSua": [
                            {
                                "id": "canh_001",
                                "lyDo": "Sửa niên đại và bổ sung công thức LaTeX chuẩn.",
                                "loiThoaiMoi": "Vào khoảng thế kỷ thứ 5 TCN, Hippasus phát hiện √2 không thể viết thành phân số tối giản p/q.",
                                "congThucLatexMoi": [{"latex": r"\sqrt{2} \neq \frac{p}{q}", "nhan": "Vô tỉ", "noiBat": True}],
                            }
                        ],
                        "baiHocMoi": [
                            {
                                "loai": "toan_hoc",
                                "noiDung": "Luôn đối chiếu niên đại cổ đại trước Công nguyên với tư liệu nghiên cứu.",
                                "mucDoUuTien": 5,
                            }
                        ],
                    }

            fake = FakeCritiqueGemini()
            kb_sau, bao_cao, cb = tu_kiem_dinh_kich_ban(
                kich_ban=du_lieu,
                gemini=fake,  # type: ignore[arg-type]
                tu_lieu_nghien_cuu={"tomTat1Cau": "Hippasus và √2 thế kỷ 5 TCN"},
                duong_dan_bo_nho=path_bn,
            )
            self.assertEqual(cb, [])
            self.assertEqual(len(bao_cao["canhDaSua"]), 1)
            self.assertIn("thế kỷ thứ 5 TCN", kb_sau["chuong"][0]["canh"][0]["loiThoai"])
            self.assertEqual(kb_sau["chuong"][0]["canh"][0]["congThucLatex"][0]["latex"], r"\sqrt{2} \neq \frac{p}{q}")

            bo_nho_sau = tai_bo_nho(path_bn)
            self.assertEqual(len(bo_nho_sau["bai_hoc_rut_ra"]), 1)
            self.assertEqual(bo_nho_sau["bai_hoc_rut_ra"][0]["loai"], "toan_hoc")

    def test_xuat_chapters_va_mo_ta_youtube(self) -> None:
        du_lieu = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=18)
        thoi_luong = {f"canh_{i:03d}": 5.8 for i in range(1, 109)}
        du_lieu_render, _ = tinh_toan_khung_hinh(du_lieu, thoi_luong, slug="pythagoras", fps=30)

        tu_lieu = {
            "tomTat1Cau": "Câu chuyện có thật về số vô tỉ √2 khiến hội Pythagoras phải bất ngờ.",
            "ungDungHienDai": ["Thiết kế khổ giấy A4 tỉ lệ √2", "Đồ họa máy tính 3D"],
            "nguonThamKhao": [
                "https://en.wikipedia.org/wiki/Square_root_of_2",
                "https://en.wikipedia.org/wiki/Hippasus",
            ],
        }
        noi_dung = tao_chapters_va_mo_ta(du_lieu_render, tu_lieu_nghien_cuu=tu_lieu, fps=30)
        self.assertIn("TIÊU ĐỀ GỢI Ý CHO YOUTUBE", noi_dung)
        self.assertIn("ĐOẠN MÔ TẢ HẤP DẪN", noi_dung)
        self.assertIn("00:00 1. Hồi thứ 1", noi_dung)
        self.assertIn("NGUỒN THAM KHẢO", noi_dung)
        self.assertIn("https://en.wikipedia.org/wiki/Square_root_of_2", noi_dung)
        self.assertIn("Thiết kế khổ giấy A4", noi_dung)

    def test_san_xuat_lien_tuc_nhieu_tap_tu_nap_va_xu_ly_loi_tung_tap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path_bn = root / "bo_nho_hoc_hoi.json"
            tai_bo_nho(path_bn)

            so_lan_nap = {"dem": 0}
            slugs_da_chay: list[str] = []
            giay_da_ngu: list[float] = []

            def fake_nap(so_luong: int = 5, duong_dan_bo_nho: Any = None, **kwargs: Any) -> list[dict[str, Any]]:
                so_lan_nap["dem"] += 1
                bn = tai_bo_nho(duong_dan_bo_nho)
                them = them_chu_de_hang_doi(
                    bn,
                    [
                        {"slug": "tap_1_ok", "tieuDe": "Tập 1 Euler", "diemThuHut": 9.8, "doSauToanHoc": 9.5},
                        {"slug": "tap_2_loi", "tieuDe": "Tập 2 Galois (lỗi giả lập)", "diemThuHut": 9.5, "doSauToanHoc": 9.0},
                        {"slug": "tap_3_ok", "tieuDe": "Tập 3 Ramanujan", "diemThuHut": 9.1, "doSauToanHoc": 8.9},
                        {"slug": "tap_4_du", "tieuDe": "Tập 4 Cantor", "diemThuHut": 8.5, "doSauToanHoc": 8.5},
                    ],
                )
                luu_bo_nho(bn, duong_dan_bo_nho)
                return them

            def fake_nghien_cuu(slug: str, chu_de: str, **kwargs: Any) -> tuple[Path, dict[str, Any]]:
                slugs_da_chay.append(slug)
                if slug == "tap_2_loi":
                    raise RuntimeError("Gia lap loi mang o tap 2")
                p = root / slug / "tu_lieu_nghien_cuu.json"
                p.parent.mkdir(parents=True, exist_ok=True)
                data = {
                    "slug": slug,
                    "tieuDe": chu_de,
                    "tomTat1Cau": f"Tóm tắt {chu_de}",
                    "nguonThamKhao": [f"https://example.org/{slug}"],
                }
                p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
                return p, data

            def fake_bien_kich(chu_de: str, slug: str, **kwargs: Any) -> tuple[Path, Path, dict[str, Any]]:
                p_json = root / slug / "nhap_kich_ban.json"
                p_md = root / slug / "doc_duyet_kich_ban.md"
                kb = {
                    "tieuDe": chu_de,
                    "chuDe": chu_de,
                    "danhSachNhanVat": [{"id": "nv1", "ten": "Nhà Toán Học"}],
                    "chuong": [],
                }
                p_json.write_text(json.dumps(kb, ensure_ascii=False), encoding="utf-8")
                p_md.write_text("# Doc duyet\n", encoding="utf-8")
                return p_json, p_md, kb

            def fake_tts(slug: str, **kwargs: Any) -> tuple[Path, dict[str, Any]]:
                p_render = root / slug / "du_lieu_render.json"
                p_render.write_text("{}", encoding="utf-8")
                return p_render, {"tongGiay": 665.0, "datTren10Phut": True}

            def fake_render(slug: str, **kwargs: Any) -> dict[str, Path]:
                return {
                    "video": root / "out" / slug / "video_hoan_chinh.mp4",
                    "chapters_va_mo_ta": root / "out" / slug / "chapters_va_mo_ta.txt",
                    "luoi": root / "out" / slug / "luoi_kiem_dinh.png",
                }

            ket_qua = chay_san_xuat_lien_tuc(
                so_tap=3,
                nghi_giay=15.0,
                duong_dan_bo_nho=path_bn,
                thu_muc_du_lieu=root,
                sleep_fn=lambda s: giay_da_ngu.append(s),
                nap_hang_doi_fn=fake_nap,
                nghien_cuu_fn=fake_nghien_cuu,
                bien_kich_fn=fake_bien_kich,
                tts_fn=fake_tts,
                render_fn=fake_render,
            )

            # Da tu dong nap hang doi khi so chu de 'cho' < 3
            self.assertGreaterEqual(so_lan_nap["dem"], 1)
            # Tap 1 ok -> Tap 2 loi -> Tap 3 van tiep tuc thanh cong!
            self.assertEqual([r["trangThai"] for r in ket_qua], ["thanh_cong", "loi", "thanh_cong"])
            self.assertEqual(slugs_da_chay, ["tap_1_ok", "tap_2_loi", "tap_3_ok"])
            self.assertEqual(giay_da_ngu, [15.0, 15.0])
            self.assertTrue((root / "nhat_ky_san_xuat.log").exists())

            # Kiem tra bo_nho_hoc_hoi.json da cap nhat 2 tap thanh cong va trang thai hang doi dung
            bn_cuoi = tai_bo_nho(path_bn)
            self.assertEqual([t["slug"] for t in bn_cuoi["chu_de_da_lam"]], ["tap_1_ok", "tap_3_ok"])
            trang_thai_map = {item["slug"]: item["trangThai"] for item in bn_cuoi["hang_doi_chu_de"]}
            self.assertEqual(trang_thai_map["tap_1_ok"], "xong")
            self.assertEqual(trang_thai_map["tap_3_ok"], "xong")
            # Tap 2 bi loi duoc tra ve 'cho' de khong ket mai o 'dang_lam'
            self.assertEqual(trang_thai_map["tap_2_loi"], "cho")

            # Test che do --chi-tao-kich-ban voi --chu-de dat hang rieng
            kq_kb = chay_san_xuat_lien_tuc(
                so_tap=1,
                chu_de="Archimedes và chiếc vương miện",
                chi_tao_kich_ban=True,
                duong_dan_bo_nho=path_bn,
                thu_muc_du_lieu=root,
                sleep_fn=lambda _: None,
                nghien_cuu_fn=fake_nghien_cuu,
                bien_kich_fn=fake_bien_kich,
                tts_fn=lambda **kw: (_ for _ in ()).throw(AssertionError("Khong duoc goi TTS khi --chi-tao-kich-ban")),
                render_fn=lambda **kw: (_ for _ in ()).throw(AssertionError("Khong duoc goi Render khi --chi-tao-kich-ban")),
            )
            self.assertEqual(kq_kb[0]["trangThai"], "thanh_cong")
            self.assertTrue(kq_kb[0]["chiTaoKichBan"])


class TestAmThanhVaLipSyncV06Offline(unittest.TestCase):
    def test_tinh_bien_do_rms_tu_pcm_cac_muc_va_im_lang(self) -> None:
        sr = 16000
        fps = 30
        # 4 doan x 0.5s = 2.0s = 60 frames: im lang -> nho -> to -> im lang
        mau = array.array("h")
        n_doan = sr // 2
        mau.extend([0] * n_doan)
        for i in range(n_doan):
            mau.append(int(2600 * math.sin(2.0 * math.pi * 440.0 * i / sr)))
        for i in range(n_doan):
            mau.append(int(22000 * math.sin(2.0 * math.pi * 440.0 * i / sr)))
        mau.extend([0] * n_doan)
        if sys.byteorder != "little":
            mau.byteswap()

        rms = tinh_bien_do_rms_tu_pcm(mau.tobytes(), sample_rate=sr, fps=fps)
        self.assertEqual(len(rms), 60)
        self.assertTrue(all(0.0 <= v <= 1.0 for v in rms))
        # Doan 0 va doan 3 im lang -> dung 0.0 (mieng khep hoan toan)
        self.assertTrue(all(v == 0.0 for v in rms[:14]))
        self.assertTrue(all(v == 0.0 for v in rms[46:]))
        # Doan 1 nho hon doan 2 ro ret
        tb_nho = sum(rms[16:28]) / 12.0
        tb_to = sum(rms[31:44]) / 13.0
        self.assertGreater(tb_nho, 0.05)
        self.assertGreater(tb_to, 0.75)
        self.assertGreater(tb_to, tb_nho * 2.0)

        # PCM toan 0 -> mang toan 0.0 (khong khuech dai nhieu nen)
        im_lang = tinh_bien_do_rms_tu_pcm(bytes(sr * 2), sample_rate=sr, fps=fps)
        self.assertEqual(len(im_lang), 30)
        self.assertTrue(all(v == 0.0 for v in im_lang))

        # Kiem tra can_chinh_mang_rms dem 0.0 cho khoang nghi cuoi canh
        dem = can_chinh_mang_rms([0.5, 0.8], 5)
        self.assertEqual(dem, [0.5, 0.8, 0.0, 0.0, 0.0])

    def test_trich_xuat_rms_ffmpeg_va_cache_sha256_trong_chuanbi_dai(self) -> None:
        file_ding = GOC_DU_AN / "public" / "sfx" / "ding.mp3"
        self.assertTrue(file_ding.exists())
        rms1 = trich_xuat_bien_do_rms(file_ding, fps=30)
        rms2 = trich_xuat_bien_do_rms(file_ding, fps=30)
        self.assertGreaterEqual(len(rms1), 20)
        self.assertEqual(rms1, rms2)
        self.assertTrue(any(v > 0.5 for v in rms1))

        # File hong/khong phai audio -> tra ve [] an toan, khong crash
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file_loi = root / "khong_hop_le.mp3"
            file_loi.write_bytes(b"KHONG_PHAI_AUDIO")
            self.assertEqual(trich_xuat_bien_do_rms(file_loi, fps=30), [])

            # Kiem tra chuan_bi_audio_va_du_lieu_render nhung bienDoAmThanh & tai su dung cache SHA-256
            du_lieu = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=1)  # 6 canh
            du_lieu_dir = root / "du_lieu"
            public_dir = root / "public"
            slug = "test_rms_cache"
            (du_lieu_dir / slug).mkdir(parents=True)
            (du_lieu_dir / slug / "nhap_kich_ban.json").write_text(
                json.dumps(du_lieu, ensure_ascii=False), encoding="utf-8"
            )

            lan_trich_rms: list[str] = []

            def fake_rms(p: Path, fps: int) -> list[float]:
                lan_trich_rms.append(p.stem)
                return [0.45, 0.82, 0.15]

            f_render, _ = chuan_bi_audio_va_du_lieu_render(
                slug=slug,
                thu_muc_du_lieu=du_lieu_dir,
                thu_muc_public=public_dir,
                tts_generator=lambda cid, txt, p: p.write_bytes(b"MP3_" + cid.encode("ascii")),
                duration_prober=lambda _: 1.0,
                rms_extractor=fake_rms,
            )
            self.assertEqual(len(lan_trich_rms), 6)
            data_render = json.loads(f_render.read_text(encoding="utf-8"))
            canh_dau = data_render["chuong"][0]["canh"][0]
            so_frame_canh_dau = canh_dau["denFrame"] - canh_dau["tuFrame"]
            self.assertEqual(len(canh_dau["bienDoAmThanh"]), so_frame_canh_dau)
            self.assertEqual(canh_dau["bienDoAmThanh"][:3], [0.45, 0.82, 0.15])
            # Phan nghi cuoi canh duoc dem bang 0.0 de mieng khep dung luc ngung noi
            self.assertEqual(canh_dau["bienDoAmThanh"][-1], 0.0)

            # Chay lan 2 khong doi loi thoai -> dung cache SHA-256, khong trich RMS lai
            lan_trich_rms.clear()
            chuan_bi_audio_va_du_lieu_render(
                slug=slug,
                thu_muc_du_lieu=du_lieu_dir,
                thu_muc_public=public_dir,
                tts_generator=lambda cid, txt, p: (_ for _ in ()).throw(AssertionError("Phai dung cache TTS!")),
                duration_prober=lambda _: 1.0,
                rms_extractor=fake_rms,
            )
            self.assertEqual(lan_trich_rms, [])

    def test_lenh_ffmpeg_auto_ducking_loudnorm_va_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bgm_gia = root / "bgm.mp3"
            bgm_gia.write_bytes(b"ID3_BGM")
            vao = root / "tho.mp4"
            ra = root / "cuoi.mp4"

            # Kiem tra xac_dinh_nhac_nen (mac dinh, tat-nhac-nen, thieu file)
            self.assertEqual(xac_dinh_nhac_nen(duong_dan_mac_dinh=bgm_gia), bgm_gia)
            self.assertIsNone(xac_dinh_nhac_nen(tat_nhac_nen=True, duong_dan_mac_dinh=bgm_gia))
            self.assertIsNone(xac_dinh_nhac_nen(duong_dan_mac_dinh=root / "khong_co.mp3"))
            with self.assertRaises(FileNotFoundError):
                xac_dinh_nhac_nen(nhac_nen=root / "chi_dinh_sai.mp3")

            # 1. Co thoai + co BGM -> auto-ducking sidechaincompress + fade-in 2s + fade-out 3s + -14 LUFS
            flt_day_du = tao_filter_hau_ky_audio(
                tong_giay=600.0,
                co_audio_chinh=True,
                co_nhac_nen=True,
            )
            self.assertIn("sidechaincompress=", flt_day_du)
            self.assertIn("volume=-25.0dB", flt_day_du)
            self.assertIn("afade=t=in:st=0:d=2.00", flt_day_du)
            self.assertIn("afade=t=out:st=597.000:d=3.00", flt_day_du)
            self.assertIn("loudnorm=I=-14:TP=-1.5:LRA=11", flt_day_du)

            cmd_day_du = dung_lenh_hau_ky_audio_ffmpeg(
                file_vao=vao,
                file_xuat=ra,
                tong_giay=600.0,
                co_audio_chinh=True,
                nhac_nen=bgm_gia,
            )
            self.assertIn("-stream_loop", cmd_day_du)
            self.assertIn("-shortest", cmd_day_du)
            self.assertIn("loudnorm=I=-14:TP=-1.5:LRA=11[aout]", " ".join(cmd_day_du))

            # 2. Chi co thoai (tat nhac nen) -> van chuan hoa -14 LUFS, khong sidechaincompress
            cmd_khong_bgm = dung_lenh_hau_ky_audio_ffmpeg(
                file_vao=vao,
                file_xuat=ra,
                tong_giay=600.0,
                co_audio_chinh=True,
                nhac_nen=None,
            )
            chuoi_khong_bgm = " ".join(cmd_khong_bgm)
            self.assertNotIn("sidechaincompress", chuoi_khong_bgm)
            self.assertNotIn("-stream_loop", cmd_khong_bgm)
            self.assertIn("loudnorm=I=-14:TP=-1.5:LRA=11", chuoi_khong_bgm)

            # 3. Khong co ca audio chinh lan BGM -> fallback copy an toan
            cmd_rong = dung_lenh_hau_ky_audio_ffmpeg(
                file_vao=vao,
                file_xuat=ra,
                tong_giay=10.0,
                co_audio_chinh=False,
                nhac_nen=None,
            )
            self.assertIn("copy", cmd_rong)
            self.assertNotIn("-filter_complex", cmd_rong)

            # 4. Kiem chung thuc thi that voi FFmpeg tren video ngan 2s (co audio thoai + BGM that)
            bgm_that = GOC_DU_AN / "public" / "bgm" / "nhac_nen_nhe.mp3"
            self.assertTrue(bgm_that.exists())
            hoi_test = root / "hoi_01.mp4"
            res = subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-v",
                    "error",
                    "-f",
                    "lavfi",
                    "-i",
                    "color=c=blue:s=320x180:d=2:r=30",
                    "-f",
                    "lavfi",
                    "-i",
                    "sine=frequency=440:duration=2",
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    "-c:a",
                    "aac",
                    str(hoi_test),
                ],
                capture_output=True,
                check=False,
            )
            self.assertEqual(res.returncode, 0, res.stderr.decode("utf-8", errors="replace"))

            out_co_bgm = root / "out_co_bgm.mp4"
            ghep_cac_hoi_ffmpeg([hoi_test], out_co_bgm, nhac_nen=bgm_that)
            self.assertTrue(out_co_bgm.exists())
            self.assertGreater(out_co_bgm.stat().st_size, 0)

            out_tat_bgm = root / "out_tat_bgm.mp4"
            ghep_cac_hoi_ffmpeg([hoi_test], out_tat_bgm, tat_nhac_nen=True)
            self.assertTrue(out_tat_bgm.exists())
            self.assertGreater(out_tat_bgm.stat().st_size, 0)

    def test_hoi_quy_ha_cap_khi_google_search_grounding_429(self) -> None:
        """Khi key free-tier bi 429 rieng voi tool google_search nhung goi thuong van 200, client phai tu ha cap thanh cong."""
        luot_goi: list[tuple[str, bool]] = []

        def fake_post(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            model_name = url.split("/models/")[1].split(":")[0]
            co_search = bool(payload.get("tools"))
            luot_goi.append((model_name, co_search))
            if co_search:
                return 429, '{"error": {"code": 429, "status": "RESOURCE_EXHAUSTED"}}'
            return (
                200,
                json.dumps(
                    {
                        "candidates": [
                            {"content": {"parts": [{"text": '{"ok": true, "nguon": "fallback_khong_search"}'}]}}
                        ]
                    }
                ),
            )

        client = GeminiClient(
            api_keys=["key_1", "key_2"],
            model="gemini-3.6-flash",
            fallback_models=["gemini-3.6-flash", "gemini-flash-latest"],
            http_caller=fake_post,
            sleep_fn=lambda _: None,
        )
        du_lieu, nguon = client.tao_json(
            "Tim chu de Toan hoc",
            bat_tim_kiem_web=True,
            tra_ve_nguon=True,
        )
        self.assertEqual(du_lieu, {"ok": True, "nguon": "fallback_khong_search"})
        self.assertEqual(nguon, [])
        self.assertEqual(client.model, "gemini-3.6-flash")
        # Phai thu grounding truoc, sau do tu ha cap sang goi thuong (co_search=False) o model ban dau
        self.assertTrue(any(co_search for _, co_search in luot_goi))
        self.assertEqual(luot_goi[-1], ("gemini-3.6-flash", False))

    def test_hoi_quy_timeout_khi_doc_body_duoc_xu_ly_nhu_504_va_thu_lai(self) -> None:
        """Loi TimeoutError trong resp.read() phai duoc chuyen thanh ma 504 de xoay key va thu lai an toan."""
        from unittest.mock import patch

        class FakeRespTimeout:
            def __enter__(self) -> "FakeRespTimeout":
                return self

            def __exit__(self, *args: Any) -> bool:
                return False

            def getcode(self) -> int:
                return 200

            def read(self) -> bytes:
                raise TimeoutError("The read operation timed out")

        with patch("urllib.request.urlopen", return_value=FakeRespTimeout()):
            code, body = GeminiClient._goi_http_mac_dinh(
                "https://example.invalid/generateContent",
                {"contents": []},
                "fake_key",
                5,
            )
        self.assertEqual(code, 504)
        self.assertIn("timed out", body.lower())

        # Kiem chung GeminiClient xoay key khi gap 504 va thanh cong o key ke tiep
        lich_su: list[str] = []

        def fake_post(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            lich_su.append(api_key)
            if len(lich_su) == 1:
                return 504, "Timeout/NetworkError: The read operation timed out"
            return 200, json.dumps({"candidates": [{"content": {"parts": [{"text": "OK sau timeout"}]}}]})

        client = GeminiClient(
            api_keys=["key_1", "key_2"],
            model="gemini-3.6-flash",
            http_caller=fake_post,
            sleep_fn=lambda _: None,
        )
        self.assertEqual(client.tao_van_ban("Thu timeout"), "OK sau timeout")
        self.assertEqual(lich_su, ["key_1", "key_2"])

    def test_hoi_quy_loc_part_thought_va_tang_max_tokens_khi_cat_cut_json(self) -> None:
        """Model thinking co the tra part thought=True hoac het MAX_TOKENS; client phai loc thought va tu tang maxOutputTokens khi thu lai."""
        tokens_da_gui: list[int] = []

        def fake_post(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            max_tok = int(payload["generationConfig"]["maxOutputTokens"])
            tokens_da_gui.append(max_tok)
            if len(tokens_da_gui) == 1:
                # Lan 1: thinking an het 4096 token -> chi co part thought=True, khong co text chinh
                return (
                    200,
                    json.dumps(
                        {
                            "candidates": [
                                {
                                    "finishReason": "MAX_TOKENS",
                                    "content": {
                                        "parts": [{"text": "Dang suy nghi...", "thought": True}]
                                    },
                                }
                            ]
                        }
                    ),
                )
            return (
                200,
                json.dumps(
                    {
                        "candidates": [
                            {
                                "finishReason": "STOP",
                                "content": {
                                    "parts": [
                                        {"text": "Suy nghi noi bo khong phai JSON", "thought": True},
                                        {"text": '{"tieuDe": "Ramanujan 1729", "ok": true}'},
                                    ]
                                },
                            }
                        ]
                    }
                ),
            )

        client = GeminiClient(
            api_keys=["key_1"],
            model="gemini-3.6-flash",
            http_caller=fake_post,
            sleep_fn=lambda _: None,
        )
        kq = client.tao_json("Tra ve JSON", max_output_tokens=4096)
        self.assertEqual(kq, {"tieuDe": "Ramanujan 1729", "ok": True})
        self.assertEqual(len(tokens_da_gui), 2)
        self.assertEqual(tokens_da_gui[0], 4096)
        self.assertGreaterEqual(tokens_da_gui[1], 16384)

    def test_hoi_quy_tts_retry_khi_no_audio_received_va_luu_cache_tung_buoc(self) -> None:
        """Khi Edge TTS bi rate-limit NoAudioReceived 2 lan dau, _sinh_audio_hang_loat phai thu lai den khi thanh cong va goi on_done."""
        import asyncio
        from scripts.pipeline.chuanbi_dai import _sinh_audio_hang_loat

        dem_lan: dict[str, int] = {}
        hoan_thanh: list[str] = []

        async def fake_tts_coro(txt: str, path: Path, voice: str, rate: str, pitch: str) -> None:
            cid = path.stem
            dem_lan[cid] = dem_lan.get(cid, 0) + 1
            if cid == "canh_010" and dem_lan[cid] <= 2:
                raise RuntimeError("No audio was received.")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"MP3_OK_" + cid.encode("ascii"))

        async def fake_sleep(s: float) -> None:
            return None

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tac_vu = [
                ("canh_009", "Cau 9", root / "canh_009.mp3"),
                ("canh_010", "Cau 10", root / "canh_010.mp3"),
            ]
            asyncio.run(
                _sinh_audio_hang_loat(
                    tac_vu,
                    voice="vi-VN-NamMinhNeural",
                    rate="+0%",
                    pitch="+0Hz",
                    toi_da_dong_thoi=2,
                    so_lan_thu=5,
                    tre_giua_luot=0.0,
                    on_done=lambda cid, p: hoan_thanh.append(cid),
                    tts_coro=fake_tts_coro,
                    sleep_coro=fake_sleep,
                )
            )
            self.assertEqual(dem_lan["canh_010"], 3)
            self.assertEqual(set(hoan_thanh), {"canh_009", "canh_010"})
            self.assertTrue((root / "canh_010.mp3").exists())


class TestGiuChanNguoiXemV07Offline(unittest.TestCase):
    def test_prompt_hook_20_30s_va_kiem_dinh_nhip_thi_giac_6_8s(self) -> None:
        # 1. Kiem tra prompt Tang 1, Tang 2 (Hoi 1) va Tang 3 yeu cau Hook 20-30s + luat 6-8s + vaiNoi
        p1 = tao_prompt_tang_1("Nghịch lý khách sạn Hilbert", 11.0, "di_dom_gan_gui")
        self.assertIn("hookMoMan", p1)
        self.assertIn("20-30", p1)
        self.assertIn("tieu su sach giao khoa", p1.lower())

        bp = {
            "tieuDe": "Nghịch Lý Khách Sạn Vô Cực",
            "hookMoMan": {
                "loaiHook": "nghich_ly",
                "moTa20_30s": "Khách sạn vô hạn phòng đã kín chỗ nhưng vẫn nhận thêm cả đoàn khách mới.",
                "cauMoDauGaySoc": "Nếu khách sạn vô hạn phòng đã kín mít, bạn còn xếp thêm khách được không?",
            },
            "danhSachNhanVat": [{"id": "hilbert", "ten": "Hilbert", "phuKien": "kinh_tron"}],
        }
        hoi1 = {
            "tenChuong": "1. Khách sạn không bao giờ hết phòng",
            "boiCanhChinh": "thu_vien_co_dien",
            "thoiTietChinh": "nang_dep",
            "tomTat": "Mở màn bằng nghịch lý khách sạn vô cực.",
            "diemHaiHuoc": ["Lễ tân toát mồ hôi"],
            "kienThucToan": "Tập đếm được",
        }
        p2 = tao_prompt_tang_2_hoi(bp, hoi1, KHUNG_6_HOI[0], "di_dom_gan_gui", "Mở đầu")
        self.assertIn("HOOK 20-30 GIAY DAU", p2)
        self.assertIn("6-8 GIAY", p2)
        self.assertIn("vaiNoi", p2)

        # 2. Kiem tra kiem_dinh_nhip_ngat_thi_giac: tu tach canh tinh dai >8s & pha chuoi dung yen >6-8s
        kich_ban_tinh = {
            "tieuDe": "Test nhịp ngắt thị giác",
            "chuDe": "Kiểm thử v0.7",
            "danhSachNhanVat": [{"id": "hilbert", "ten": "Hilbert", "phuKien": "kinh_tron"}],
            "chuong": [
                {
                    "id": "chuong_1",
                    "tenChuong": "1. Mở đầu",
                    "canh": [
                        {
                            "id": "canh_001",
                            "boCuc": "ke_chuyen",
                            "boiCanh": "thu_vien_co_dien",
                            "tuFrame": 0,
                            "denFrame": 300,  # 10.0s camera tinh -> phai tu chia nho thanh 2 canh!
                            "camera": {"kieu": "tinh"},
                            "loiThoai": (
                                "Hãy tưởng tượng bạn đứng trước một khách sạn kỳ lạ có vô hạn căn phòng đã kín chỗ hoàn toàn. "
                                "Bỗng nhiên một vị khách mới bước vào và lễ tân vẫn tươi cười nhận phòng ngay lập tức!"
                            ),
                            "nhanVat": [
                                {"id": "hilbert", "x": 760, "y": 810, "huong": "phai", "hanhDong": "dung_tho", "bieuCam": "binh_thuong"}
                            ],
                        },
                        {
                            "id": "canh_002",
                            "boCuc": "ke_chuyen",
                            "boiCanh": "thu_vien_co_dien",
                            "tuFrame": 300,
                            "denFrame": 435,  # 4.5s
                            "camera": {"kieu": "tinh"},
                            "loiThoai": "Nhân viên lễ tân chỉ cần bấm chuông báo cho toàn bộ khách cũ.",
                            "nhanVat": [
                                {"id": "hilbert", "x": 760, "y": 810, "huong": "phai", "hanhDong": "dung_tho", "bieuCam": "binh_thuong"}
                            ],
                        },
                        {
                            "id": "canh_003",
                            "boCuc": "ke_chuyen",
                            "boiCanh": "thu_vien_co_dien",
                            "tuFrame": 435,
                            "denFrame": 570,  # 4.5s tiep -> cong don 9.0s dung yen -> phai pha chuoi!
                            "camera": {"kieu": "tinh"},
                            "loiThoai": "Mỗi người chỉ việc chuyển sang căn phòng có số lớn hơn một đơn vị.",
                            "nhanVat": [
                                {"id": "hilbert", "x": 760, "y": 810, "huong": "phai", "hanhDong": "dung_tho", "bieuCam": "binh_thuong"}
                            ],
                        },
                        {
                            "id": "canh_004",
                            "boCuc": "doi_thoai",
                            "boiCanh": "thu_vien_co_dien",
                            "tuFrame": 570,
                            "denFrame": 720,
                            "camera": {"kieu": "pan_nhe"},
                            "loiThoai": "“Ủa vậy phòng số một bây giờ trống trơn rồi sao?”",
                            "nhanVat": [
                                {
                                    "id": "hilbert",
                                    "x": 760,
                                    "y": 810,
                                    "huong": "phai",
                                    "hanhDong": "gai_dau_kho_hieu",
                                    "bieuCam": "ngac_nhien",
                                    "bongBongThoai": "Phòng 1 trống rồi sao?!",
                                }
                            ],
                        },
                        {
                            "id": "canh_005",
                            "boCuc": "hai_huoc",
                            "boiCanh": "phong_nen_hai_huoc",
                            "tuFrame": 720,
                            "denFrame": 870,
                            "camera": {"kieu": "zoom_hai_huoc"},
                            "loiThoai": "Nghe xong nhân viên dọn phòng chỉ biết đứng hình toát mồ hôi!",
                            "loiBinhHaiHuoc": {"noiDung": "Tăng ca vô cực không có lương!", "viTri": "goc_phai", "tuFrame": 12},
                            "nhanVat": [
                                {"id": "hilbert", "x": 960, "y": 810, "huong": "phai", "hanhDong": "bo_tay_can_loi", "bieuCam": "can_loi_mat_do"}
                            ],
                        },
                    ],
                }
            ],
        }

        canh_bao_truoc = phat_hien_canh_dung_yen(kich_ban_tinh)
        self.assertGreaterEqual(len(canh_bao_truoc), 2)
        p3 = tao_prompt_tu_kiem_dinh(kich_ban_tinh, canh_bao_thi_giac=canh_bao_truoc)
        self.assertIn("CANH BAO NHIP THI GIAC >6-8s TU DONG", p3)
        self.assertIn("vaiNoiMoi", p3)

        kb_sau, ds_xu_ly = kiem_dinh_nhip_ngat_thi_giac(kich_ban_tinh, gan_vai_noi=True)
        canh_sau = kb_sau["chuong"][0]["canh"]
        # canh_001 dai 10s da duoc tu tach thanh 2 canh -> tong 5 canh thanh 6 canh
        self.assertEqual(len(canh_sau), 6)
        self.assertTrue(any(x["hanhDong"] == "tach_canh" for x in ds_xu_ly))
        self.assertTrue(any(x["hanhDong"] == "pha_chuoi_dung_yen" for x in ds_xu_ly))
        # Hai nua sau khi tach co goc may khac nhau va khong con 'tinh'
        self.assertNotEqual(canh_sau[0]["camera"]["kieu"], "tinh")
        self.assertNotEqual(canh_sau[1]["camera"]["kieu"], "tinh")
        self.assertNotEqual(canh_sau[0]["camera"]["kieu"], canh_sau[1]["camera"]["kieu"])
        # Canh pha chuoi (canh_004 moi = canh_003 cu) da doi camera + hanhDong
        self.assertNotEqual(canh_sau[3]["camera"]["kieu"], "tinh")
        self.assertNotEqual(canh_sau[3]["nhanVat"][0]["hanhDong"], "dung_tho")
        # Gan nhan vaiNoi dung cho 3 vai
        self.assertEqual(canh_sau[0]["vaiNoi"], "nguoi_dan")
        self.assertEqual(canh_sau[4]["vaiNoi"], "nhan_vat")
        self.assertEqual(canh_sau[5]["vaiNoi"], "binh_luan_hai")
        self.assertTrue(all(c["vaiNoi"] in LOAI_VAI_NOI for c in canh_sau))
        # Frame lien mach khong lech
        for i in range(1, len(canh_sau)):
            self.assertEqual(canh_sau[i]["tuFrame"], canh_sau[i - 1]["denFrame"])

        # Kiem tra suy_luan_vai_noi_canh giu nguyen nhan hop le da gan san
        self.assertEqual(suy_luan_vai_noi_canh({"vaiNoi": "nhan_vat", "boCuc": "ke_chuyen"}), "nhan_vat")

    def test_phan_vai_da_giong_tts_punchline_va_cache_sha256(self) -> None:
        env_custom = {
            "TTS_VOICE": "vi-VN-NamMinhNeural",
            "TTS_VOICE_NGUOI_DAN": "vi-VN-NamMinhNeural",
            "TTS_VOICE_NHAN_VAT": "vi-VN-HoaiMyNeural",
            "TTS_VOICE_BINH_LUAN_HAI": "vi-VN-HoaiMyNeural",
            "TTS_RATE_BINH_LUAN_HAI": "+8%",
            "TTS_PITCH_BINH_LUAN_HAI": "+5Hz",
        }

        # 1. Kich ban cu khong co vaiNoi -> fallback 100% ve TTS_VOICE/rate/pitch mac dinh
        v_cu, r_cu, p_cu = lay_cau_hinh_giong_theo_vai(None, env_cfg=env_custom)
        self.assertEqual((v_cu, r_cu, p_cu), ("vi-VN-NamMinhNeural", "+0%", "+0Hz"))

        # 2. 3 vai noi khac nhau -> giong / toc do / cao do khac nhau & hash SHA-256 khac nhau
        c_dan = xac_dinh_cau_hinh_tts_canh({"vaiNoi": "nguoi_dan"}, env_cfg=env_custom)
        c_nv = xac_dinh_cau_hinh_tts_canh({"vaiNoi": "nhan_vat"}, env_cfg=env_custom)
        c_hai = xac_dinh_cau_hinh_tts_canh(
            {
                "vaiNoi": "binh_luan_hai",
                "loiBinhHaiHuoc": {"noiDung": "Cười xỉu!", "viTri": "goc_phai"},
            },
            env_cfg=env_custom,
        )
        self.assertEqual(c_dan["voice"], "vi-VN-NamMinhNeural")
        self.assertEqual(c_dan["nghiDauGiay"], 0.0)
        self.assertEqual(c_nv["voice"], "vi-VN-HoaiMyNeural")
        self.assertEqual(c_nv["rate"], "-2%")
        self.assertEqual(c_hai["voice"], "vi-VN-HoaiMyNeural")
        self.assertEqual(c_hai["rate"], "+8%")
        self.assertEqual(c_hai["pitch"], "+5Hz")
        self.assertAlmostEqual(c_hai["nghiDauGiay"], NGHI_TRUOC_PUNCHLINE_GIAY, places=2)

        h_dan = bam_noi_dung_tts("Cùng một câu", c_dan["voice"], c_dan["rate"], c_dan["pitch"], c_dan["nghiDauGiay"])
        h_nv = bam_noi_dung_tts("Cùng một câu", c_nv["voice"], c_nv["rate"], c_nv["pitch"], c_nv["nghiDauGiay"])
        h_hai = bam_noi_dung_tts("Cùng một câu", c_hai["voice"], c_hai["rate"], c_hai["pitch"], c_hai["nghiDauGiay"])
        self.assertEqual(len({h_dan, h_nv, h_hai}), 3)

        # 3. Kiem tra cache SHA-256 tu vo hieu khi doi vaiNoi / doi giong / bat loiBinhHaiHuoc
        du_lieu = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=1)  # 6 canh
        du_lieu["chuong"][0]["canh"][0]["vaiNoi"] = "nguoi_dan"
        du_lieu["chuong"][1]["canh"][0]["vaiNoi"] = "nhan_vat"
        du_lieu["chuong"][2]["canh"][0]["vaiNoi"] = "binh_luan_hai"
        du_lieu["chuong"][2]["canh"][0]["loiBinhHaiHuoc"] = {"noiDung": "Cú twist cực gắt!"}

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            du_lieu_dir = root / "du_lieu"
            public_dir = root / "public"
            out_dir = root / "out"
            slug = "test_da_giong"
            (du_lieu_dir / slug).mkdir(parents=True)
            file_nhap = du_lieu_dir / slug / "nhap_kich_ban.json"
            file_nhap.write_text(json.dumps(du_lieu, ensure_ascii=False), encoding="utf-8")

            sinh_lan_1: list[str] = []
            f_render, tk1 = chuan_bi_audio_va_du_lieu_render(
                slug=slug,
                thu_muc_du_lieu=du_lieu_dir,
                thu_muc_public=public_dir,
                thu_muc_out=out_dir,
                env_override=env_custom,
                tts_generator=lambda cid, txt, p: (sinh_lan_1.append(cid), p.write_bytes(b"MP3_" + cid.encode("ascii")))[1],
                duration_prober=lambda _: 4.2,
                rms_extractor=lambda p, f: [0.3, 0.7],
            )
            self.assertEqual(len(sinh_lan_1), 6)
            self.assertTrue(f_render.exists())
            # Tu dong xuat out/<slug>/phu_de.srt
            file_srt = out_dir / slug / "phu_de.srt"
            self.assertTrue(file_srt.exists())
            self.assertEqual(Path(tk1["fileSrt"]), file_srt)

            cache_data = json.loads((du_lieu_dir / slug / "cache_audio.json").read_text(encoding="utf-8"))
            self.assertEqual(cache_data["canh_001"]["voice"], "vi-VN-NamMinhNeural")
            self.assertEqual(cache_data["canh_002"]["voice"], "vi-VN-HoaiMyNeural")
            self.assertEqual(cache_data["canh_003"]["rate"], "+8%")
            self.assertGreater(cache_data["canh_003"]["nghiDauGiay"], 0.0)
            # Canh cu khong co vaiNoi (canh_004) fallback ve TTS_VOICE
            self.assertEqual(cache_data["canh_004"]["voice"], "vi-VN-NamMinhNeural")

            # Doi vaiNoi cua canh_001 tu nguoi_dan -> nhan_vat: chi sinh lai DUNG canh_001!
            du_lieu["chuong"][0]["canh"][0]["vaiNoi"] = "nhan_vat"
            file_nhap.write_text(json.dumps(du_lieu, ensure_ascii=False), encoding="utf-8")
            sinh_lan_2: list[str] = []
            chuan_bi_audio_va_du_lieu_render(
                slug=slug,
                thu_muc_du_lieu=du_lieu_dir,
                thu_muc_public=public_dir,
                thu_muc_out=out_dir,
                env_override=env_custom,
                tts_generator=lambda cid, txt, p: (sinh_lan_2.append(cid), p.write_bytes(b"MP3_V2_" + cid.encode("ascii")))[1],
                duration_prober=lambda _: 4.2,
                rms_extractor=lambda p, f: [0.3, 0.7],
            )
            self.assertEqual(sinh_lan_2, ["canh_001"])

            # 4. Kiem chung that ffmpeg chen khoang nghi punchline vao dau file MP3
            pop_src = GOC_DU_AN / "public" / "sfx" / "pop.mp3"
            self.assertTrue(pop_src.exists())
            mp3_test = root / "punchline_test.mp3"
            mp3_test.write_bytes(pop_src.read_bytes())
            dur_truoc = do_thoi_luong_ffprobe(mp3_test)
            ok_delay = _chen_khoang_nghi_dau_mp3(mp3_test, 0.35)
            self.assertTrue(ok_delay)
            dur_sau = do_thoi_luong_ffprobe(mp3_test)
            self.assertGreater(dur_sau, dur_truoc + 0.25)

    def test_xuat_phu_de_srt_chuan_subrip_va_moc_thoi_gian(self) -> None:
        # 1. Dinh dang HH:MM:SS,mmm chuan SubRip (khong bao gio ,1000 hay :60)
        self.assertEqual(dinh_dang_thoi_gian_srt(0.0), "00:00:00,000")
        self.assertEqual(dinh_dang_thoi_gian_srt(65.432), "00:01:05,432")
        self.assertEqual(dinh_dang_thoi_gian_srt(3661.9999), "01:01:02,000")

        # 2. Ngat dong gon de doc tren YouTube (toi da 2 dong can doi)
        wrapped = ngat_dong_phu_de_srt(
            "Pythagoras từng tin rằng mọi thứ trong vũ trụ đều là tỉ số của hai số nguyên.",
            max_ky_tu_dong=44,
        )
        cac_dong = wrapped.splitlines()
        self.assertEqual(len(cac_dong), 2)
        self.assertTrue(all(len(d) <= 46 for d in cac_dong))

        # 3. Xuat file .srt day du tu du_lieu_render 30fps
        du_lieu = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=2)  # 12 canh
        thoi_luong = {f"canh_{i:03d}": 5.4 for i in range(1, 13)}
        du_lieu_render, _ = tinh_toan_khung_hinh(du_lieu, thoi_luong, slug="test_srt", fps=30)

        with tempfile.TemporaryDirectory() as tmp:
            out_srt = Path(tmp) / "phu_de.srt"
            xuat_file_srt(du_lieu_render, out_srt, fps=30)
            self.assertTrue(out_srt.exists())
            raw = out_srt.read_text(encoding="utf-8")
            self.assertNotIn("\r\n", raw)  # LF

            khoi = [k.strip() for k in raw.strip().split("\n\n") if k.strip()]
            self.assertGreaterEqual(len(khoi), 12)

            import re as _re

            prev_end_ms = 0
            for idx, k in enumerate(khoi, start=1):
                lines = k.splitlines()
                self.assertGreaterEqual(len(lines), 3)
                self.assertEqual(lines[0], str(idx))
                m = _re.match(
                    r"^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})$",
                    lines[1],
                )
                self.assertIsNotNone(m, f"Moc thoi gian SRT sai dinh dang: {lines[1]}")
                assert m is not None
                h1, m1, s1, ms1, h2, m2, s2, ms2 = (int(g) for g in m.groups())
                start_ms = ((h1 * 60 + m1) * 60 + s1) * 1000 + ms1
                end_ms = ((h2 * 60 + m2) * 60 + s2) * 1000 + ms2
                self.assertGreaterEqual(start_ms, prev_end_ms)
                self.assertGreater(end_ms, start_ms)
                prev_end_ms = end_ms
                # Noi dung tieng Viet UTF-8 gon <= 2 dong
                self.assertLessEqual(len(lines[2:]), 2)

            # Kiem tra tao_noi_dung_srt tuong thich du_lieu/mau_pythagoras.json
            mau_data = json.loads((GOC_DU_AN / "du_lieu" / "mau_pythagoras.json").read_text(encoding="utf-8"))
            srt_mau = tao_noi_dung_srt(mau_data, fps=30)
            self.assertIn("00:00:00,000 -->", srt_mau)
            self.assertIn("Pythagoras", srt_mau)

    # ==========================================================================
    # v0.8 TESTS: Gemini Vision Visual QA, Thumbnail A/B Still & MinhHoaToan tung_buoc
    # ==========================================================================
    def test_gemini_vision_inline_data_xoay_key_va_fallback_model(self) -> None:
        import base64
        from PIL import Image

        with tempfile.TemporaryDirectory() as tmp:
            img_path = Path(tmp) / "luoi_test.png"
            Image.new("RGB", (64, 36), color=(20, 83, 45)).save(str(img_path), format="PNG")
            expected_b64 = base64.b64encode(img_path.read_bytes()).decode("ascii")

            cac_cuoc_goi: list[tuple[str, str, dict[str, Any]]] = []

            def fake_http(url: str, payload: dict[str, Any], key: str, timeout: int) -> tuple[int, str]:
                cac_cuoc_goi.append((url, key, payload))
                # Luot 1: model_1 gap 404 -> chuyen fallback sang model_2
                if "model_cu_404" in url:
                    return 404, '{"error": {"message": "Model not found"}}'
                # Luot 2: key_1 gap 429 -> xoay sang key_2
                if key == "KEY_1":
                    return 429, '{"error": {"message": "RESOURCE_EXHAUSTED"}}'
                # Luot 3: thanh cong tren model_2 + key_2
                phan_hoi = {
                    "candidates": [
                        {
                            "content": {
                                "parts": [
                                    {
                                        "text": json.dumps(
                                            {
                                                "diemTongThe": 9.2,
                                                "nhanXetChung": "Bố cục rõ nét, KaTeX sạch đẹp.",
                                                "danhSachCanhLoi": [],
                                                "deXuatSuaChung": ["Tiếp tục duy trì độ tương phản tốt."],
                                            },
                                            ensure_ascii=False,
                                        )
                                    }
                                ]
                            }
                        }
                    ]
                }
                return 200, json.dumps(phan_hoi, ensure_ascii=False)

            client = GeminiClient(
                api_keys=["KEY_1", "KEY_2"],
                model="model_cu_404",
                fallback_models=["model_vision_ok"],
                http_caller=fake_http,
                http_get_caller=lambda url, timeout: (500, "skip auto-discover"),
                sleep_fn=lambda _: None,
            )

            ket_qua = client.tao_json_voi_anh(
                prompt="Kiem dinh luoi khung hinh nay",
                duong_dan_anh=img_path,
                mime_type="image/png",
            )
            self.assertEqual(ket_qua["diemTongThe"], 9.2)
            self.assertEqual(len(cac_cuoc_goi), 3)
            # Xac minh payload gui len co inlineData base64 dung byte file PNG
            parts_cuoi = cac_cuoc_goi[-1][2]["contents"][0]["parts"]
            self.assertEqual(len(parts_cuoi), 2)
            self.assertIn("text", parts_cuoi[0])
            self.assertEqual(parts_cuoi[1]["inlineData"]["mimeType"], "image/png")
            self.assertEqual(parts_cuoi[1]["inlineData"]["data"], expected_b64)

    def test_visual_qa_gemini_bao_cao_va_khong_crash_khi_het_quota(self) -> None:
        from PIL import Image

        prompt_qa = tao_prompt_visual_qa("Bí mật số vô tỉ √2")
        self.assertIn("katex_tran_vien", prompt_qa)
        self.assertIn("phu_de_de_mat", prompt_qa)
        self.assertIn("chu_qua_nho", prompt_qa)
        self.assertIn("trung_bo_cuc", prompt_qa)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            img_luoi = root / "luoi_kiem_dinh.png"
            Image.new("RGB", (120, 68), color=(15, 23, 42)).save(str(img_luoi), format="PNG")

            # 1. Truong hop thanh cong (mock Gemini Vision tra ve 1 canh loi)
            def fake_http_ok(url: str, payload: dict[str, Any], key: str, timeout: int) -> tuple[int, str]:
                resp = {
                    "candidates": [
                        {
                            "content": {
                                "parts": [
                                    {
                                        "text": json.dumps(
                                            {
                                                "diemTongThe": 7.5,
                                                "nhanXetChung": "Tổng thể tốt nhưng có 1 cảnh KaTeX sát mép.",
                                                "danhSachCanhLoi": [
                                                    {
                                                        "oKhungHinh": "Hồi 3 (#2)",
                                                        "loaiLoi": "katex_tran_vien",
                                                        "mucDo": "trung_binh",
                                                        "moTa": "Công thức dài chạm sát viền phải bảng xanh.",
                                                        "deXuatSua": "Tách công thức thành 2 dòng ngắn hơn.",
                                                    }
                                                ],
                                                "deXuatSuaChung": ["Giữ mỗi công thức dưới 40 ký tự."],
                                            },
                                            ensure_ascii=False,
                                        )
                                    }
                                ]
                            }
                        }
                    ]
                }
                return 200, json.dumps(resp, ensure_ascii=False)

            client_ok = GeminiClient(
                api_keys=["KEY_QA"],
                model="gemini-flash-latest",
                http_caller=fake_http_ok,
                sleep_fn=lambda _: None,
            )
            file_bc_ok = root / "bao_cao_visual_qa.json"
            bc_ok = chay_visual_qa_gemini(img_luoi, file_bc_ok, tieu_de="Pythagoras", client=client_ok)
            self.assertTrue(file_bc_ok.exists())
            self.assertEqual(bc_ok["trangThai"], "hoan_thanh")
            self.assertEqual(bc_ok["diemTongThe"], 7.5)
            self.assertEqual(len(bc_ok["danhSachCanhLoi"]), 1)
            self.assertEqual(bc_ok["danhSachCanhLoi"][0]["loaiLoi"], "katex_tran_vien")

            # 2. Truong hop het quota / mat mang -> KHONG CRASH pipeline, luu bao cao bo_qua_loi
            client_loi = GeminiClient(
                api_keys=["KEY_QA"],
                model="gemini-flash-latest",
                fallback_models=["gemini-flash-latest"],
                http_caller=lambda u, p, k, t: (429, "RESOURCE_EXHAUSTED"),
                sleep_fn=lambda _: None,
            )
            file_bc_loi = root / "bao_cao_visual_qa_loi.json"
            bc_loi = chay_visual_qa_gemini(img_luoi, file_bc_loi, tieu_de="Pythagoras", client=client_loi)
            self.assertTrue(file_bc_loi.exists())
            self.assertEqual(bc_loi["trangThai"], "bo_qua_loi")
            self.assertIsNone(bc_loi["diemTongThe"])
            self.assertIn("lyDoLoi", bc_loi)

            # 3. Kiem tra chuan hoa bao cao khi AI tra diem vuot khoang hoac loaiLoi la
            bc_norm = chuan_hoa_bao_cao_visual_qa(
                {"diemTongThe": 15, "danhSachCanhLoi": [{"oKhungHinh": "Hồi 1 (#1)", "loaiLoi": "la_hoac"}]}
            )
            self.assertEqual(bc_norm["diemTongThe"], 10.0)
            self.assertEqual(bc_norm["danhSachCanhLoi"][0]["loaiLoi"], "khac")

    def test_thumbnail_ab_3_bien_the_va_lenh_render_still(self) -> None:
        mau_data = json.loads((GOC_DU_AN / "du_lieu" / "mau_pythagoras.json").read_text(encoding="utf-8"))
        # Tu dong tong hop 3 bien the tu du lieu cu khong co goiYThumbnail
        pa_list = chuan_bi_phuong_an_thumbnail(mau_data)
        self.assertEqual([p["bien_the"] for p in pa_list], [1, 2, 3])
        for pa in pa_list:
            self.assertLessEqual(len(pa["tieuDeLon"].split()), 4)
            self.assertTrue(pa["congThucLatex"])
            self.assertIn("ten", pa["nhanVat"])

        # Kiem tra dung lenh Remotion Still & mock render_bo_thumbnail
        with tempfile.TemporaryDirectory() as tmp:
            thu_muc = Path(tmp) / "out_pyth"
            lenh_da_chay: list[list[str]] = []

            def fake_runner(cmd: list[str], cwd: Path | None) -> None:
                lenh_da_chay.append(cmd)
                # Ghi file PNG gia lap tai tham so file_anh_xuat (index 5)
                out_png = Path(cmd[5])
                out_png.write_bytes(b"\x89PNG\r\n\x1a\nMOCK")
                # Xac nhan file --props tam ton tai va la JSON hop le
                props_arg = next(a for a in cmd if a.startswith("--props="))
                props_data = json.loads(Path(props_arg.split("=", 1)[1]).read_text(encoding="utf-8"))
                self.assertIn(props_data["bien_the"], (1, 2, 3))

            ds_anh = render_bo_thumbnail(mau_data, thu_muc, npx_bin="npx", command_runner=fake_runner)
            self.assertEqual(len(ds_anh), 3)
            self.assertEqual([p.name for p in ds_anh], ["thumbnail_1.png", "thumbnail_2.png", "thumbnail_3.png"])
            self.assertTrue(all(p.exists() for p in ds_anh))
            self.assertEqual(len(lenh_da_chay), 3)
            for cmd in lenh_da_chay:
                self.assertEqual(cmd[:5], ["npx", "remotion", "still", "src/index.ts", THUMBNAIL_STILL_ID])

        # Kiem tra co CLI --bo-qua-thumbnail va --bo-qua-visual-qa trong render_dai.py
        args_cli = tao_parser_render_dai().parse_args(
            ["--slug", "test_v08", "--bo-qua-thumbnail", "--bo-qua-visual-qa"]
        )
        self.assertTrue(args_cli.bo_qua_thumbnail)
        self.assertTrue(args_cli.bo_qua_visual_qa)

        cmd_cuc_bo = dung_lenh_render_thumbnail(
            Path("a.json"),
            Path("out.png"),
            npx_bin="npx",
            env={},
        )
        self.assertEqual(
            cmd_cuc_bo,
            ["npx", "remotion", "still", "src/index.ts", THUMBNAIL_STILL_ID, "out.png", "--props=a.json"],
        )

        cmd_ci = dung_lenh_render_thumbnail(
            Path("a.json"),
            Path("out.png"),
            npx_bin="npx",
            env={"CI": "true"},
        )
        self.assertEqual(
            cmd_ci,
            ["npx", "remotion", "still", "src/index.ts", THUMBNAIL_STILL_ID, "out.png", "--props=a.json", "--log=warn"],
        )
        # remotion still khong ho tro --concurrency va anh PNG khong can --jpeg-quality
        self.assertFalse(any(a.startswith("--concurrency") for a in cmd_ci))
        self.assertFalse(any(a.startswith("--jpeg-quality") for a in cmd_ci))

        # Goi mac dinh (doc env hien tai) phai khop dung che do local hoac CI=true
        cmd_mac_dinh = dung_lenh_render_thumbnail(Path("a.json"), Path("out.png"), npx_bin="npx")
        self.assertEqual(cmd_mac_dinh, cmd_ci if dang_chay_tren_ci() else cmd_cuc_bo)

    def test_v08_enum_moi_minh_hoa_tung_buoc_va_goi_y_thumbnail(self) -> None:
        # 1. Kiem tra 12 boi canh, 11 dao cu, va 'tung_buoc'
        for bc in ("quang_truong_hy_lap", "thu_vien_trung_co", "dai_thien_van_phuc_hung", "giang_duong_hien_dai"):
            self.assertIn(bc, LOAI_BOI_CANH)
        for dc in ("compa_co", "ban_tinh_co", "khoi_da_dien", "kinh_thien_van"):
            self.assertIn(dc, LOAI_DAO_CU)
        self.assertIn("tung_buoc", LOAI_MINH_HOA_TOAN)

        # 2. Kiem tra sanitizer chuan_hoa_buoc_ve_toan & minhHoaToan "tung_buoc"
        buoc_raw = [
            {"loai": "truc_toa_do", "xMin": -2, "xMax": 6, "yMin": -1, "yMax": 5, "hienLuoi": True},
            {"loai": "diem", "x": 0, "y": 0, "nhan": "O"},
            {"loai": "doan_thang", "x1": 0, "y1": 0, "x2": 3, "y2": 4, "nhan": "c = 5", "muiTen": True},
            {"loai": "cung_tron", "cx": 0, "cy": 0, "r": 1.2, "gocBatDau": 0, "gocKetThuc": 53, "nhan": "α"},
            {
                "loai": "da_giac",
                "diem": [[0, 0], [3, 0], [3, 4]],
                "diemDich": [[1, 0], [4, 0], [4, 4]],
                "nhan": "S = 6",
                "mauTo": "#38BDF8",
            },
            {"loai": "duong_cong", "ham": "parabol", "heSoA": 0.25, "xTu": -2, "xDen": 4, "nhan": "y = x²/4"},
            {"loai": "nhan_chu", "x": 2, "y": 4.2, "noiDung": "Định lý tổng quát"},
            {"loai": "khong_hop_le_bi_bo_qua"},
        ]
        buoc_sach = chuan_hoa_buoc_ve_toan(buoc_raw)
        self.assertEqual(len(buoc_sach), 7)
        self.assertEqual(buoc_sach[4]["diemDich"], [[1.0, 0.0], [4.0, 0.0], [4.0, 4.0]])

        # 3. Kiem tra chuan_hoa_toan_bo_kich_ban giu nguyen minhHoaToan tung_buoc + goiYThumbnail + boiCanh/daoCu moi
        raw_kb = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=1)
        raw_kb["chuong"][0]["canh"][0]["boiCanh"] = "dai_thien_van_phuc_hung"
        raw_kb["chuong"][0]["canh"][0]["daoCu"] = [{"loai": "kinh_thien_van", "x": 1500, "y": 650}]
        raw_kb["chuong"][0]["canh"][0]["minhHoaToan"] = {
            "loai": "tung_buoc",
            "tieuDe": "Chứng minh từng bước",
            "khungToaDo": {"xMin": -2, "xMax": 6, "yMin": -1, "yMax": 5, "hienLuoi": True},
            "buocVe": buoc_raw,
            "chuThichCuoi": "Biến hình diện tích bảo toàn S",
        }
        raw_kb["goiYThumbnail"] = [
            {"bien_the": 1, "tieuDeLon": "BÍ MẬT SỐ VÔ TỈ QUÁ DÀI SẼ BỊ CẮT", "congThucLatex": "\\sqrt{2}", "daoCuNoiBat": "compa_co"},
        ]
        kb_sach, _ = chuan_hoa_toan_bo_kich_ban(raw_kb)
        c0 = kb_sach["chuong"][0]["canh"][0]
        self.assertEqual(c0["boiCanh"], "dai_thien_van_phuc_hung")
        self.assertEqual(c0["daoCu"][0]["loai"], "kinh_thien_van")
        self.assertEqual(c0["minhHoaToan"]["loai"], "tung_buoc")
        self.assertEqual(len(c0["minhHoaToan"]["buocVe"]), 7)
        self.assertEqual(len(kb_sach["goiYThumbnail"]), 3)
        self.assertEqual(len(kb_sach["goiYThumbnail"][0]["tieuDeLon"].split()), 4)

        # 4. Kiem tra prompt Tang 1 & Tang 2 + markdown doc duyet
        p1 = tao_prompt_tang_1("Định lý Euler", 11.0, "di_dom_gan_gui")
        self.assertIn("goiYThumbnail", p1)
        self.assertIn("quang_truong_hy_lap", p1)
        bp_gia = {
            "tieuDe": "Định lý Euler",
            "danhSachNhanVat": kb_sach["danhSachNhanVat"],
        }
        p2 = tao_prompt_tang_2_hoi(
            blueprint=bp_gia,
            thong_tin_hoi={
                "tenChuong": "Hồi 3",
                "boiCanhChinh": "giang_duong_hien_dai",
                "thoiTietChinh": "nang_dep",
                "tomTat": "Chứng minh",
            },
            khung_hoi=KHUNG_6_HOI[2],
            giong_ke="di_dom_gan_gui",
            tom_tat_hoi_truoc="Hồi 2",
        )
        self.assertIn("tung_buoc", p2)
        self.assertIn("buocVe", p2)
        md = tao_markdown_doc_duyet(kb_sach)
        self.assertIn("Thumbnail A/B", md)

        # 5. Kiem tra chuan_hoa_goi_y_thumbnail voi input rong van sinh du 3 bien the
        gt_empty = chuan_hoa_goi_y_thumbnail([], kb_sach["danhSachNhanVat"], "Bí Ẩn Số Pi")
        self.assertEqual([x["bien_the"] for x in gt_empty], [1, 2, 3])

    # ==========================================================================
    # v1.0 TESTS: Vong tu hoc so lieu YouTube, Dong bo YouTube stdlib, Render song song & CI YAML
    # ==========================================================================
    def test_v10_nhap_so_lieu_youtube_cli_csv_json_doi_chieu_va_gioi_han_25(self) -> None:
        du_lieu_kb = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=18)
        du_lieu_kb["goiYThumbnail"] = [
            {
                "bien_the": 1,
                "tieuDeLon": "BÍ MẬT CĂN 2",
                "nhanPhu": "SỰ THẬT SỐC",
                "congThucLatex": r"\sqrt{2}",
                "daoCuNoiBat": "compa_co",
                "bieuCam": "ngac_nhien",
                "boiCanh": "quang_truong_hy_lap",
            },
            {
                "bien_the": 2,
                "tieuDeLon": "CON SỐ BỊ CẤM!",
                "nhanPhu": "NGHỊCH LÝ HY LẠP",
                "congThucLatex": r"\sqrt{2} \notin \mathbb{Q}",
                "daoCuNoiBat": "khoi_da_dien",
                "bieuCam": "hoang_mang",
                "boiCanh": "bo_bien_hy_lap",
            },
            {
                "bien_the": 3,
                "tieuDeLon": "GIẢI MÃ 10P",
                "nhanPhu": "SIÊU DỄ HIỂU",
                "congThucLatex": "p^2 = 2q^2",
                "daoCuNoiBat": "kinh_thien_van",
                "bieuCam": "tinh_quai",
                "boiCanh": "lop_hoc_bang_xanh",
            },
        ]
        thoi_luong = {f"canh_{i:03d}": 5.8 for i in range(1, 109)}
        du_lieu_render, _ = tinh_toan_khung_hinh(du_lieu_kb, thoi_luong, slug="pythagoras_can2", fps=30)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            du_lieu_dir = root / "du_lieu"
            (du_lieu_dir / "pythagoras_can2").mkdir(parents=True)
            (du_lieu_dir / "pythagoras_can2" / "du_lieu_render.json").write_text(
                json.dumps(du_lieu_render, ensure_ascii=False),
                encoding="utf-8",
            )
            path_bn = du_lieu_dir / "bo_nho_hoc_hoi.json"
            bo_nho = tai_bo_nho(path_bn)
            ghi_nhan_tap_hoan_thanh(
                bo_nho,
                slug="pythagoras_can2",
                tieu_de="Pythagoras & Cú Sốc √2",
                nhan_vat_chinh="Pythagoras, Hippasus",
                tom_tat_1_cau="Hippasus chứng minh √2 là số vô tỉ.",
                thoi_luong_giay=655.0,
            )
            # Nap san 25 bai hoc khac biet ro rang muc uu tien 2 de kiem tra gioi han 25 khi co bai hoc YouTube uu tien 5
            chu_de_phu = [
                "hình học Euclid cổ đại", "số nguyên tố Mersenne", "đồ thị Euler", "chuỗi Fourier",
                "tích phân Riemann", "đạo hàm Newton", "nhóm Galois", "mặt phẳng phức Gauss",
                "xác suất Pascal", "tam giác nhị thức", "tỉ lệ vàng Fibonacci", "logarit Napier",
                "hình học xạ ảnh", "không gian Hilbert", "tập hợp Cantor", "định lý bốn màu",
                "mã hóa RSA", "hình học fractal", "suy luận Bayes", "bán kính Trái Đất",
                "bàn tính cổ", "hệ nhị phân Leibniz", "đường cong cycloid", "định lý Noether",
                "bài toán người bán hàng",
            ]
            for i, cdp in enumerate(chu_de_phu, start=1):
                them_bai_hoc(
                    bo_nho,
                    loai="kich_ban",
                    noi_dung=f"Chu de {cdp} can vi du doi thuong rieng biet muc #{i}.",
                    muc_do_uu_tien=2,
                    ngay=f"2026-10-{(i % 28) + 1:02d}",
                )
            luu_bo_nho(bo_nho, path_bn)

            prompts_da_gui: list[str] = []

            class FakeYouTubeLearningGemini:
                def tao_json(self, prompt: str, **kwargs: Any) -> Any:
                    prompts_da_gui.append(prompt)
                    return {
                        "baiHocMoi": [
                            {
                                "loai": "hook",
                                "noiDung": "Trong 30 giây đầu, đặt câu hỏi nghịch lý trực diện ngay ở giây 0 giúp giữ chân >70%.",
                                "mucDoUuTien": 5,
                            },
                            {
                                "loai": "thumbnail",
                                "noiDung": "Biến thể Thumbnail 2 (CON SỐ BỊ CẤM! + biểu cảm hoang_mang) thắng A/B test CTR 8.4%.",
                                "mucDoUuTien": 5,
                            },
                            {
                                "loai": "giu_chan",
                                "noiDung": "Trước mốc 04:20 cần chèn 1 miếng hài góc màn hình để tránh tụt view đoạn giải thích dài.",
                                "mucDoUuTien": 5,
                            },
                        ]
                    }

            fake_ai = FakeYouTubeLearningGemini()

            # 1. Nap qua ham nhap_so_lieu_youtube (tuong duong CLI --nhap-so-lieu-youtube)
            kq_cli = nhap_so_lieu_youtube(
                slug="pythagoras_can2",
                ctr_phan_tram="8.4%",
                giu_chan_30s="72.5%",
                thoi_luong_xem_tb_giay="05:45",
                moc_tut_view="00:45, 04:20",
                bien_the_thumbnail_thang="2",
                binh_luan_noi_bat=["Giải thích √2 siêu dễ hiểu!", "Khúc 04:20 hơi dài một chút"],
                ghi_chu="Chạy thử Test & Compare 72 giờ",
                duong_dan=path_bn,
                thu_muc_du_lieu=du_lieu_dir,
                client=fake_ai,  # type: ignore[arg-type]
            )
            self.assertEqual(kq_cli["slug"], "pythagoras_can2")
            self.assertEqual(kq_cli["soLieuYouTube"]["ctr_phan_tram"], 8.4)
            self.assertEqual(kq_cli["soLieuYouTube"]["giu_chan_30s"], 72.5)
            self.assertEqual(kq_cli["soLieuYouTube"]["thoi_luong_xem_tb_giay"], 345.0)
            self.assertEqual(kq_cli["soLieuYouTube"]["moc_tut_view"], ["00:45", "04:20"])
            self.assertEqual(kq_cli["soLieuYouTube"]["bien_the_thumbnail_thang"], "2")
            self.assertEqual(len(kq_cli["baiHocMoi"]), 3)
            self.assertEqual(kq_cli["tongBaiHoc"], TOI_DA_BAI_HOC)

            # Xac minh Gemini nhan duoc doi chieu kich ban: Hook 30s, Thumbnail bien the 2 va canh tai moc 00:45 & 04:20
            self.assertEqual(len(prompts_da_gui), 1)
            self.assertIn("CON SỐ BỊ CẤM!", prompts_da_gui[0])
            self.assertIn("Moc 00:45 (45s)", prompts_da_gui[0])
            self.assertIn("Moc 04:20 (260s)", prompts_da_gui[0])
            self.assertIn("Doan Hook 30 giay dau", prompts_da_gui[0])

            # 2. Nap tu file CSV xuat tu YouTube Studio (co BOM UTF-8 va dong Total)
            csv_path = root / "youtube_studio_export.csv"
            csv_path.write_text(
                "\ufeffContent,Video title,Views,Impressions click-through rate (%),Average view duration,giu_chan_30s,moc_tut_view,bien_the_thumbnail_thang,binh_luan_noi_bat\n"
                "Total,,25000,7.5%,05:30,,,,\n"
                "abc123XYZ,euler_7_cay_cau,12500,9.1%,06:12,74%,\"00:50, 05:10\",2,\"Quá cuốn!|Làm thêm về Gauss nhé\"\n",
                encoding="utf-8",
            )
            ds_csv = doc_so_lieu_youtube_tu_file(csv_path)
            self.assertEqual(len(ds_csv), 1)
            self.assertEqual(ds_csv[0]["slug"], "euler_7_cay_cau")
            self.assertEqual(ds_csv[0]["soLieuYouTube"]["ctr_phan_tram"], 9.1)
            self.assertEqual(ds_csv[0]["soLieuYouTube"]["thoi_luong_xem_tb_giay"], 372.0)
            self.assertEqual(ds_csv[0]["soLieuYouTube"]["luot_xem"], 12500)
            self.assertEqual(len(ds_csv[0]["soLieuYouTube"]["binh_luan_noi_bat"]), 2)

            kq_csv = nhap_so_lieu_youtube_tu_file(
                csv_path,
                duong_dan=path_bn,
                thu_muc_du_lieu=du_lieu_dir,
                client=fake_ai,  # type: ignore[arg-type]
            )
            self.assertEqual(len(kq_csv), 1)

            # 3. Nap tu file JSON (co the bo qua AI bang tu_dong_phan_tich=False)
            json_path = root / "youtube_metrics.json"
            json_path.write_text(
                json.dumps(
                    {
                        "videos": [
                            {
                                "slug": "ramanujan_1729",
                                "ctr_phan_tram": 7.9,
                                "giu_chan_30s": 69.0,
                                "thoi_luong_xem_tb_giay": 390,
                                "moc_tut_view": ["01:15", "06:30"],
                                "bien_the_thumbnail_thang": "1",
                                "binh_luan_noi_bat": ["Con số 1729 quá thú vị!"],
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            kq_json = nhap_so_lieu_youtube_tu_file(
                json_path,
                duong_dan=path_bn,
                thu_muc_du_lieu=du_lieu_dir,
                tu_dong_phan_tich=False,
            )
            self.assertEqual(len(kq_json), 1)
            self.assertEqual(kq_json[0]["baiHocMoi"], [])

            # 4. Kiem tra bo nho sau nap: gioi han <= 25 bai hoc, giu 3 bai uu tien 5, phan_hoi_kenh co 3 ban ghi co cau truc
            bn_sau = tai_bo_nho(path_bn)
            self.assertLessEqual(len(bn_sau["bai_hoc_rut_ra"]), TOI_DA_BAI_HOC)
            self.assertEqual(len(bn_sau["phan_hoi_kenh"]), 3)
            self.assertEqual(bn_sau["phan_hoi_kenh"][0]["soLieuYouTube"]["ctr_phan_tram"], 8.4)
            self.assertEqual(bn_sau["phan_hoi_kenh"][1]["nguon"], "csv")
            self.assertEqual(bn_sau["phan_hoi_kenh"][2]["nguon"], "json")

            # 5. Kiem tra tao_ngu_canh_hoc_hoi() dua ro quy tac CTR, Retention & Thumbnail vao prompt tao_kich_ban_10p
            ngu_canh = tao_ngu_canh_hoc_hoi(duong_dan=path_bn)
            self.assertIn("QUY TAC TOI UU CTR, HOOK 30S, GIU CHAN & GOI Y THUMBNAIL", ngu_canh)
            self.assertIn("CTR trung binh=", ngu_canh)
            self.assertIn("Giu chan 30s TB=", ngu_canh)
            self.assertIn("bien the '2'", ngu_canh)
            self.assertIn("YouTube/thumbnail", ngu_canh)
            p1 = tao_prompt_tang_1("Định lý Fermat", 11.0, "di_dom_gan_gui", ngu_canh_hoc_hoi=ngu_canh)
            self.assertIn("QUY TAC TOI UU CTR, HOOK 30S", p1)
            self.assertIn("goiYThumbnail", p1)

            # 6. Kiem tra CLI --nhap-so-lieu-youtube & --hoc-tu-phan-hoi (tuong thich cu + moi)
            rc_cli = main_bo_nho_hoc_hoi(
                [
                    "--bo-nho",
                    str(path_bn),
                    "--nhap-so-lieu-youtube",
                    "--slug",
                    "test_cli_khong_ai",
                    "--ctr",
                    "6.8",
                    "--giu-chan-30s",
                    "65",
                    "--moc-tut-view",
                    "00:35,03:50",
                    "--bien-the-thumbnail-thang",
                    "3",
                    "--khong-goi-ai",
                ]
            )
            self.assertEqual(rc_cli, 0)
            args_cu = tao_parser_bo_nho().parse_args(
                ["--hoc-tu-phan-hoi", "--slug", "demo", "--ghi-chu", "Hay lam"]
            )
            self.assertTrue(args_cu.hoc_tu_phan_hoi)
            self.assertEqual(
                chuan_hoa_so_lieu_youtube({"ctr": "8,2%", "avd": "04:10"})["thoi_luong_xem_tb_giay"],
                250.0,
            )
            self.assertIn("Moc 00:45", tai_ngu_canh_kich_ban_doi_chieu("pythagoras_can2", du_lieu_dir, ["00:45"]))

    def test_v10_dong_bo_youtube_thieu_env_va_keo_api_mock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path_bn = root / "bo_nho_hoc_hoi.json"
            env_rong = root / ".env.rong"
            env_rong.write_text("# Chua cau hinh YouTube API\n", encoding="utf-8")

            # 1. Chua cau hinh bien moi truong -> KHONG crash, tra ve huong dan nap CSV/JSON tay
            cfg_rong = lay_cau_hinh_youtube(
                duong_dan_env=env_rong,
                env_override={"YOUTUBE_API_KEY": "", "YOUTUBE_OAUTH_TOKEN": "", "YOUTUBE_ACCESS_TOKEN": ""},
            )
            self.assertEqual(cfg_rong, {"api_key": "", "oauth_token": ""})
            kq_chua_cfg = dong_bo_video_youtube(
                slug="ramanujan_1729",
                video_id="vid_demo_01",
                duong_dan_bo_nho=path_bn,
                duong_dan_env=env_rong,
                env_override={"YOUTUBE_API_KEY": "", "YOUTUBE_OAUTH_TOKEN": "", "YOUTUBE_ACCESS_TOKEN": ""},
            )
            self.assertEqual(kq_chua_cfg["trangThai"], "chua_cau_hinh")
            self.assertIn("--nhap-so-lieu-youtube", kq_chua_cfg["huongDan"])
            self.assertIn("YouTube Studio", tao_huong_dan_nhap_tay("ramanujan_1729"))

            # CLI exit code 0 khi chua cau hinh (neu env he thong khong set san)
            import os as _os

            cu_key = _os.environ.pop("YOUTUBE_API_KEY", None)
            cu_tok = _os.environ.pop("YOUTUBE_OAUTH_TOKEN", None)
            cu_acc = _os.environ.pop("YOUTUBE_ACCESS_TOKEN", None)
            try:
                rc_rong = main_dong_bo_youtube(
                    ["--slug", "ramanujan_1729", "--video-id", "vid_demo_01", "--env", str(env_rong)]
                )
                self.assertEqual(rc_rong, 0)
            finally:
                if cu_key is not None:
                    _os.environ["YOUTUBE_API_KEY"] = cu_key
                if cu_tok is not None:
                    _os.environ["YOUTUBE_OAUTH_TOKEN"] = cu_tok
                if cu_acc is not None:
                    _os.environ["YOUTUBE_ACCESS_TOKEN"] = cu_acc

            # 2. Da cau hinh YOUTUBE_API_KEY + YOUTUBE_OAUTH_TOKEN -> keo thong ke & binh luan -> day vao bo_nho_hoc_hoi.json
            cac_url: list[tuple[str, dict[str, str]]] = []

            def fake_yt_get(url: str, headers: dict[str, str], timeout: int) -> tuple[int, str]:
                cac_url.append((url, headers))
                if "/videos?" in url:
                    return 200, json.dumps(
                        {
                            "items": [
                                {
                                    "id": "vid_1729",
                                    "snippet": {
                                        "title": "Ramanujan và con số 1729",
                                        "publishedAt": "2026-11-25T09:00:00Z",
                                    },
                                    "statistics": {
                                        "viewCount": "15420",
                                        "likeCount": "1230",
                                        "commentCount": "89",
                                    },
                                }
                            ]
                        }
                    )
                if "/commentThreads?" in url:
                    return 200, json.dumps(
                        {
                            "items": [
                                {
                                    "snippet": {
                                        "topLevelComment": {
                                            "snippet": {
                                                "textDisplay": "Đoạn giải thích 1729 = 1^3 + 12^3 quá đỉnh!"
                                            }
                                        }
                                    }
                                },
                                {
                                    "snippet": {
                                        "topLevelComment": {
                                            "snippet": {
                                                "textDisplay": "Làm tập tiếp theo về Galois nha kênh ơi!"
                                            }
                                        }
                                    }
                                },
                            ]
                        }
                    )
                return 404, "{}"

            tk = keo_thong_ke_video_youtube(
                video_id="vid_1729",
                api_key="TEST_YT_KEY",
                oauth_token="TEST_OAUTH",
                http_get_caller=fake_yt_get,
            )
            self.assertEqual(tk["luot_xem"], 15420)
            self.assertEqual(tk["luot_thich"], 1230)
            self.assertEqual(len(tk["binh_luan_noi_bat"]), 2)
            self.assertEqual(cac_url[0][1].get("Authorization"), "Bearer TEST_OAUTH")
            self.assertIn("key=TEST_YT_KEY", cac_url[0][0])

            # Truong hop video tat binh luan (403) -> van keo thong ke thanh cong khong crash
            tk_no_cmt = keo_thong_ke_video_youtube(
                video_id="vid_1729",
                api_key="TEST_YT_KEY",
                http_get_caller=lambda u, h, t: fake_yt_get(u, h, t) if "/videos?" in u else (403, "commentsDisabled"),
            )
            self.assertEqual(tk_no_cmt["luot_xem"], 15420)
            self.assertEqual(tk_no_cmt["binh_luan_noi_bat"], [])

            class FakeSyncGemini:
                def tao_json(self, prompt: str, **kwargs: Any) -> Any:
                    return {
                        "baiHocMoi": [
                            {
                                "loai": "kich_ban",
                                "noiDung": "Khán giả rất thích các đẳng thức số học bất ngờ như 1729 = 1^3 + 12^3.",
                                "mucDoUuTien": 4,
                            }
                        ]
                    }

            kq_sync = dong_bo_video_youtube(
                slug="ramanujan_1729",
                video_id="vid_1729",
                ctr_phan_tram=8.1,
                bien_the_thumbnail_thang="1",
                duong_dan_bo_nho=path_bn,
                env_override={"YOUTUBE_API_KEY": "TEST_YT_KEY", "YOUTUBE_OAUTH_TOKEN": ""},
                http_get_caller=fake_yt_get,
                gemini_client=FakeSyncGemini(),  # type: ignore[arg-type]
            )
            self.assertEqual(kq_sync["trangThai"], "thanh_cong")
            bn_sync = tai_bo_nho(path_bn)
            self.assertEqual(len(bn_sync["phan_hoi_kenh"]), 1)
            self.assertEqual(bn_sync["phan_hoi_kenh"][0]["nguon"], "youtube_api")
            self.assertEqual(bn_sync["phan_hoi_kenh"][0]["soLieuYouTube"]["luot_xem"], 15420)
            self.assertEqual(bn_sync["phan_hoi_kenh"][0]["soLieuYouTube"]["ctr_phan_tram"], 8.1)

    def test_v10_render_tach_pha_song_song_va_san_xuat_chuan_bi(self) -> None:
        from PIL import Image

        du_lieu = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=2)  # 6 hoi x 2 canh
        thoi_luong = {f"canh_{i:03d}": 4.5 for i in range(1, 13)}
        du_lieu_render, _ = tinh_toan_khung_hinh(du_lieu, thoi_luong, slug="song_song_demo", fps=30)
        pham_vi = tinh_pham_vi_frame_chuong(du_lieu_render)

        # 1. Kiem tra CLI parser & bao loi xung dot co
        args_hoi = tao_parser_render_dai().parse_args(["--slug", "demo", "--chi-render-hoi", "3"])
        self.assertEqual(args_hoi.chi_render_hoi, 3)
        self.assertFalse(args_hoi.chi_ghep_hoan_chinh)

        args_ghep = tao_parser_render_dai().parse_args(["--slug", "demo", "--chi-ghep-hoan-chinh"])
        self.assertTrue(args_ghep.chi_ghep_hoan_chinh)
        self.assertIsNone(args_ghep.chi_render_hoi)

        self.assertEqual(
            main_render_dai(["--slug", "demo", "--chi-render-hoi", "2", "--chi-ghep-hoan-chinh"]),
            2,
        )
        self.assertEqual(main_render_dai(["--slug", "demo", "--chi-render-hoi", "0"]), 2)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file_props = root / "du_lieu" / "song_song_demo" / "du_lieu_render.json"
            file_props.parent.mkdir(parents=True)
            file_props.write_text(json.dumps(du_lieu_render, ensure_ascii=False), encoding="utf-8")
            out_dir = root / "out"

            # 2. Test --chi-render-hoi 3: chi chay dung 1 lenh Remotion voi --frames cua hoi 3
            lenh_hoi_3: list[list[str]] = []

            def fake_run_hoi(cmd: list[str], cwd: Path | None) -> None:
                lenh_hoi_3.append(cmd)
                Path(cmd[5]).write_bytes(b"FAKE_MP4_HOI_3")

            kq_hoi_3 = render_mot_hoi(
                slug="song_song_demo",
                so_hoi=3,
                duong_dan_props=file_props,
                thu_muc_out=out_dir,
                thu_muc_public=root / "public",
                npx_bin="npx",
                command_runner=fake_run_hoi,
            )
            self.assertEqual(kq_hoi_3["cheDo"], "chi_render_hoi")
            self.assertEqual(kq_hoi_3["soHoi"], 3)
            self.assertTrue(kq_hoi_3["daRender"])
            self.assertEqual(len(lenh_hoi_3), 1)
            self.assertIn(
                f"--frames={pham_vi[2]['tuFrame']}-{pham_vi[2]['endFrameInclusive']}",
                lenh_hoi_3[0],
            )
            self.assertTrue((out_dir / "song_song_demo" / "chuong" / "hoi_03.mp4").exists())
            self.assertTrue((out_dir / "song_song_demo" / "chuong" / "cache_hoi_03.json").exists())
            # Khong duoc tao video_hoan_chinh.mp4 khi dang o che do --chi-render-hoi
            self.assertFalse((out_dir / "song_song_demo" / "video_hoan_chinh.mp4").exists())

            # Hoi ngoai pham vi -> bao ValueError
            with self.assertRaises(ValueError):
                render_mot_hoi(slug="song_song_demo", so_hoi=9, duong_dan_props=file_props, thu_muc_out=out_dir)

            # 3. Test --chi-ghep-hoan-chinh: gia lap da co du 6 file hoi_01..06.mp4
            for h in range(1, 7):
                p_hoi = out_dir / "song_song_demo" / "chuong" / f"hoi_{h:02d}.mp4"
                p_hoi.write_bytes(f"FAKE_HOI_{h}".encode("ascii"))

            lenh_still: list[list[str]] = []

            def fake_still_runner(cmd: list[str], cwd: Path | None) -> None:
                lenh_still.append(cmd)
                Path(cmd[5]).write_bytes(b"\x89PNG\r\n\x1a\nTHUMB")

            def fake_merge(ds_mp4: list[Path], out_mp4: Path, **kwargs: Any) -> Path:
                self.assertEqual(len(ds_mp4), 6)
                out_mp4.write_bytes(b"MERGED_VIDEO_14LUFS")
                return out_mp4

            def fake_grid(file_anh_xuat: Path, **kwargs: Any) -> Path:
                Image.new("RGB", (120, 68), color=(15, 23, 42)).save(str(file_anh_xuat), format="PNG")
                return file_anh_xuat

            class FakeVisionQA:
                def tao_json_voi_anh(self, **kwargs: Any) -> Any:
                    return {
                        "diemTongThe": 9.3,
                        "nhanXetChung": "Đạt chuẩn xuất bản.",
                        "danhSachCanhLoi": [],
                        "deXuatSuaChung": [],
                    }

            kq_ghep = render_toan_bo_video(
                slug="song_song_demo",
                duong_dan_props=file_props,
                chi_ghep_hoan_chinh=True,
                thu_muc_out=out_dir,
                thu_muc_public=root / "public",
                npx_bin="npx",
                command_runner=fake_still_runner,
                merge_fn=fake_merge,
                grid_fn=fake_grid,
                gemini_client=FakeVisionQA(),  # type: ignore[arg-type]
            )
            # Khong goi remotion render video, chi goi 3 lenh remotion still Thumbnail A/B
            self.assertEqual(len(lenh_still), 3)
            self.assertTrue(all(cmd[2] == "still" for cmd in lenh_still))
            self.assertTrue(kq_ghep["video"].exists())
            self.assertTrue(kq_ghep["chapters_va_mo_ta"].exists())
            self.assertTrue(kq_ghep["phu_de_srt"].exists())
            self.assertTrue(kq_ghep["luoi"].exists())
            self.assertTrue(kq_ghep["bao_cao_visual_qa"].exists())
            self.assertEqual(len(kq_ghep["thumbnails"]), 3)

            # 4. Test pha --chi-chuan-bi & --hoan-tat-tu-meta trong san_xuat_lien_tuc.py
            args_sx = tao_parser_san_xuat().parse_args(
                ["--chi-chuan-bi", "--xuat-meta-json", "out/thong_tin_chuan_bi.json"]
            )
            self.assertTrue(args_sx.chi_chuan_bi)
            path_bn = root / "bo_nho_chuan_bi.json"
            tai_bo_nho(path_bn)
            file_meta = root / "out" / "thong_tin_chuan_bi.json"

            kq_cb = chay_san_xuat_lien_tuc(
                chu_de="Gauss và tổng 1 đến 100",
                chi_chuan_bi=True,
                file_meta_json=file_meta,
                duong_dan_bo_nho=path_bn,
                thu_muc_du_lieu=root / "du_lieu_sx",
                nghien_cuu_fn=lambda slug, chu_de, **kw: (
                    root / "tl.json",
                    {"tomTat1Cau": "Gauss tính tổng trong 3 giây.", "nguonThamKhao": ["https://example.org/gauss"]},
                ),
                bien_kich_fn=lambda chu_de, slug, **kw: (
                    root / "kb.json",
                    root / "kb.md",
                    du_lieu_render,
                ),
                tts_fn=lambda slug, **kw: (file_props, {"tongGiay": 640.5, "datTren10Phut": True}),
                render_fn=lambda **kw: (_ for _ in ()).throw(AssertionError("Khong duoc goi render khi --chi-chuan-bi")),
            )
            self.assertEqual(kq_cb[0]["trangThai"], "thanh_cong")
            self.assertEqual(kq_cb[0]["danhSachHoi"], [1, 2, 3, 4, 5, 6])
            self.assertTrue(file_meta.exists())
            meta_doc = json.loads(file_meta.read_text(encoding="utf-8"))
            self.assertEqual(meta_doc["danhSachHoi"], [1, 2, 3, 4, 5, 6])

            ban_ghi_xong = hoan_tat_tap_tu_meta(file_meta, duong_dan_bo_nho=path_bn)
            self.assertEqual(ban_ghi_xong["slug"], meta_doc["slug"])
            bn_xong = tai_bo_nho(path_bn)
            self.assertEqual(len(bn_xong["chu_de_da_lam"]), 1)
            self.assertEqual(bn_xong["chu_de_da_lam"][0]["slug"], meta_doc["slug"])
            # Chu de da hoan thanh phai duoc xoa khoi hang_doi_chu_de de tranh lap ngay hom sau
            self.assertEqual(bn_xong["hang_doi_chu_de"], [])

    def test_v10_validate_github_actions_workflow_yaml(self) -> None:
        wf_path = GOC_DU_AN / ".github" / "workflows" / "tu-dong-video10p.yml"
        self.assertTrue(wf_path.exists(), f"Thieu workflow YAML: {wf_path}")
        raw_bytes = wf_path.read_bytes()
        self.assertNotIn(b"\r\n", raw_bytes, "Workflow YAML phai dung xuong dong LF")
        text = raw_bytes.decode("utf-8")

        # Khong duoc dung tab thut le trong YAML & khong duoc ghi cung API key/token
        for idx, line in enumerate(text.splitlines(), start=1):
            self.assertFalse(line.startswith("\t"), f"Dong {idx} dung tab thut le YAML")
            self.assertNotIn("AIza", line, f"Dong {idx} nghi ngo ghi cung Google API key")
            self.assertNotIn("ya29.", line, f"Dong {idx} nghi ngo ghi cung OAuth token")
            # Kiem tra can bang bieu thuc GitHub Actions ${{ ... }}
            self.assertEqual(line.count("${{"), line.count("}}"), f"Dong {idx} lech ngoac ${{{{ ... }}}}")

        # Neu PyYAML co san thi parse that, dong thoi kiem tra cau truc bang stdlib
        try:
            import yaml  # type: ignore[import-not-found]
        except ImportError:
            yaml = None

        if yaml is not None:
            parsed = yaml.safe_load(text)
            self.assertIsInstance(parsed, dict)
            jobs = parsed.get("jobs") or {}
            self.assertEqual(list(jobs.keys()), ["chuan-bi", "render-song-song", "ghep-va-luu"])
            self.assertEqual(jobs["render-song-song"].get("needs"), ["chuan-bi"])
            self.assertIn("matrix", jobs["render-song-song"].get("strategy") or {})
            self.assertEqual(jobs["ghep-va-luu"].get("needs"), ["chuan-bi", "render-song-song"])
        else:
            import re as _re

            jobs_section = text.split("\njobs:\n", 1)[1]
            cac_job = _re.findall(r"^  ([a-z0-9-]+):\s*$", jobs_section, flags=_re.MULTILINE)
            self.assertEqual(cac_job, ["chuan-bi", "render-song-song", "ghep-va-luu"])

        # Xac minh du luong 3 job song song theo chunk, lich chay cach 2 ngay, dang YouTube & tu dong luu bo nho
        for bat_buoc in (
            "schedule:",
            "- cron: '0 0 */2 * *'",
            "0 0 * * 1,3,5",
            "workflow_dispatch:",
            "concurrency:",
            "group: ${{ github.workflow }}-${{ github.ref }}",
            "cancel-in-progress: false",
            "jobs:",
            "  chuan-bi:",
            "  render-song-song:",
            "  ghep-va-luu:",
            "permissions:",
            "contents: write",
            "timeout-minutes: 25",
            "timeout-minutes: 35",
            "fail-fast: false",
            "max-parallel: 8",
            "needs: [chuan-bi]",
            "needs: [chuan-bi, render-song-song]",
            "strategy:",
            "matrix:",
            "fromJson(needs.chuan-bi.outputs.danh_sach_chunk)",
            "--chi-chuan-bi",
            "--chi-render-chunk",
            "--che-do-ci",
            "--chi-ghep-hoan-chinh",
            "--hoan-tat-tu-meta",
            "scripts/pipeline/dang_youtube.py",
            "YOUTUBE_CLIENT_ID",
            "YOUTUBE_CLIENT_SECRET",
            "YOUTUBE_REFRESH_TOKEN",
            "tu_dong_dang_youtube:",
            "che_do_dang:",
            "- hen_gio",
            "- rieng_tu",
            "--gio-cong-khai-vn",
            "--chi-rieng-tu",
            "actions/cache@v4",
            "node-version: '22'",
            "Cai dat Node.js 22 (co cache npm)",
            "node-modules-${{ runner.os }}-node22-",
            "node_modules/.remotion",
            "~/.cache/remotion",
            "retention-days: 1",
            "retention-days: 14",
            "git pull --rebase origin main",
            "chu_de:",
            "slug:",
            "chi_chay_lai_chunk:",
            "tat_visual_qa:",
            "UTC+7",
            "du_lieu/bo_nho_hoc_hoi.json",
            "bao_cao_visual_qa.json",
            "thumbnail_*.png",
        ):
            self.assertIn(bat_buoc, text, f"Workflow thieu cau hinh bat buoc: {bat_buoc}")
        # Buoc dang YouTube phai chay truoc buoc commit bo_nho_hoc_hoi.json len main
        self.assertLess(
            text.index("scripts/pipeline/dang_youtube.py"),
            text.index("git pull --rebase origin main"),
        )
        # Dam bao da nang toan bo 3 job len Node 22 va khong con sot cau hinh Node 20
        self.assertEqual(text.count("node-version: '22'"), 3)
        self.assertNotIn("node-version: '20'", text)
        self.assertNotIn("node20", text)
        # YOUTUBE_API_KEY la tuy chon: workflow hang ngay KHONG duoc phu thuoc hay yeu cau secret nay
        self.assertNotIn("YOUTUBE_API_KEY", text)
        # Kiem tra scripts/test_khung.mjs khong import tinh truc tiep file .ts (de chay duoc tren ca Node 20 & 22+)
        test_khung_txt = (GOC_DU_AN / "scripts" / "test_khung.mjs").read_text(encoding="utf-8")
        self.assertIn("esbuild", test_khung_txt)
        self.assertNotRegex(test_khung_txt, r"(?m)^import\s+[\s\S]*?from\s+['\"]\.\./src/[^'\"]+\.ts['\"]")

    def test_v20_buoc1_chong_ro_ri_pythagoras_outro_va_gap_frame(self) -> None:
        # 1. Xac minh ma nguon src/canh/ va src/daocu/MinhHoaToan.tsx KHONG con hardcode fallback Pythagoras
        cac_file_ts = [
            GOC_DU_AN / "src" / "VideoDai.tsx",
            GOC_DU_AN / "src" / "daocu" / "MinhHoaToan.tsx",
            *(GOC_DU_AN / "src" / "canh").glob("*.tsx"),
        ]
        chuoi_cam = (
            "~530 TCN",
            "Trường phái Pythagoras",
            "Hippasus phát hiện √2",
            "Giả sử √2 = p/q",
            "y = f(x) • Đạo hàm & Diện tích ∫",
            "MOC_MAC_DINH",
            "BUOC_VE_MAC_DINH",
        )
        for p in cac_file_ts:
            noi_dung = p.read_text(encoding="utf-8")
            for cam in chuoi_cam:
                self.assertNotIn(cam, noi_dung, f"Phat hien chuoi hardcode '{cam}' trong {p.name}")

        # 2. Kiem tra phat hien ro ri du lieu Pythagoras vao tap khac (vd: Ramanujan)
        tap_ramanujan_loi = {
            "tieuDe": "Ramanujan & Con Số 1729",
            "chuDe": "Sổ tay bí ẩn của thiên tài Ấn Độ Srinivasa Ramanujan",
            "danhSachNhanVat": [
                {"id": "ramanujan", "ten": "Srinivasa Ramanujan", "mauThan": "#1E293B", "mauChuDao": "#2563EB", "phuKien": "ao_choang"}
            ],
            "chuong": [
                {
                    "id": "chuong_1",
                    "tenChuong": "1. Hồi 1",
                    "canh": [
                        {
                            "id": "canh_001",
                            "boCuc": "dong_thoi_gian",
                            "boiCanh": "thu_vien_co_dien",
                            "tuFrame": 0,
                            "denFrame": 120,
                            "loiThoai": "Mốc lịch sử của Ramanujan tại Cambridge.",
                            "mocThoiGian": [
                                {"nam": "~530 TCN", "moTa": "Trường phái Pythagoras tôn thờ số hữu tỉ"}
                            ],
                            "nhanVat": [],
                        },
                        {
                            "id": "canh_002",
                            "boCuc": "ket_thuc",  # Loi outro o cuoi Hoi 1
                            "boiCanh": "thu_vien_co_dien",
                            "tuFrame": 120,
                            "denFrame": 240,
                            "loiThoai": "Kết hồi 1 chuyển sang hồi 2.",
                            "nhanVat": [],
                        },
                    ],
                },
                {
                    "id": "chuong_2",
                    "tenChuong": "2. Hồi 2",
                    "canh": [
                        {
                            "id": "canh_003",
                            "boCuc": "giai_thich_toan",
                            "boiCanh": "lop_hoc_bang_xanh",
                            "tuFrame": 245,  # Co tinh chen gap frame 240 -> 245
                            "denFrame": 360,
                            "loiThoai": "Giải thích số taxi 1729.",
                            "minhHoaToan": {
                                "loai": "chuoi_suy_luan",
                                "thamSo": {"buoc1": "1. Giả sử √2 = p/q (tối giản)"},
                            },
                            "nhanVat": [],
                        },
                        {
                            "id": "canh_004",
                            "boCuc": "ket_thuc",
                            "boiCanh": "bau_troi_dem_vu_tru",
                            "tuFrame": 360,
                            "denFrame": 480,
                            "loiThoai": "Hẹn gặp lại ở tập sau!",
                            "nhanVat": [],
                        },
                    ],
                },
            ],
        }

        loi_ro_ri = kiem_tra_ro_ri_pythagoras(tap_ramanujan_loi)
        self.assertGreaterEqual(len(loi_ro_ri), 2, f"Phai bat duoc ro ri Pythagoras, thuc te: {loi_ro_ri}")

        # Tap Pythagoras that (mau_pythagoras.json) phai qua sach khong bao gia
        mau_pyth = json.loads((GOC_DU_AN / "du_lieu" / "mau_pythagoras.json").read_text(encoding="utf-8"))
        self.assertEqual(kiem_tra_ro_ri_pythagoras(mau_pyth), [])
        self.assertEqual(kiem_tra_lien_mach_khung_hinh(mau_pyth), [])
        self.assertEqual(kiem_dinh_schema_du_lieu_canh(mau_pyth), [])

        # 3. Kiem tra phat hien gap frame & tu dong can lai lien mach khi render
        loi_gap = kiem_tra_lien_mach_khung_hinh(tap_ramanujan_loi)
        self.assertTrue(any("gap frame" in m for m in loi_gap), f"Phai phat hien gap frame, thuc te: {loi_gap}")

        da_chuan_hoa, ghi_chu = chuan_hoa_du_lieu_truoc_render(tap_ramanujan_loi)
        self.assertEqual(kiem_tra_lien_mach_khung_hinh(da_chuan_hoa), [])
        self.assertEqual(da_chuan_hoa["chuong"][0]["canh"][1]["boCuc"], "ke_chuyen")
        self.assertEqual(da_chuan_hoa["chuong"][1]["canh"][-1]["boCuc"], "ket_thuc")
        self.assertGreaterEqual(len(ghi_chu), 2)

        # 4. Kiem tra chan outro o hoi giua trong tao_kich_ban_10p & chuanbi_dai
        kb_6_hoi = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=2)
        for h_idx in (0, 2, 3):  # Hoi 1, Hoi 3, Hoi 4 bi gan nham ket_thuc
            kb_6_hoi["chuong"][h_idx]["canh"][-1]["boCuc"] = "ket_thuc"

        kb_sach, _ = chuan_hoa_toan_bo_kich_ban(kb_6_hoi)
        for h_idx in range(5):
            for c in kb_sach["chuong"][h_idx]["canh"]:
                self.assertNotEqual(c["boCuc"], "ket_thuc", f"Hoi {h_idx + 1} khong duoc co boCuc='ket_thuc'")
        self.assertEqual(kb_sach["chuong"][5]["canh"][-1]["boCuc"], "ket_thuc")

        thoi_luong_map = {f"canh_{i:03d}": 4.0 for i in range(1, 13)}
        # Gan nham lai ket_thuc de kiem tra chuanbi_dai.tinh_toan_khung_hinh cung tu dong chan
        kb_6_hoi["chuong"][0]["canh"][-1]["boCuc"] = "ket_thuc"
        kb_6_hoi["chuong"][2]["canh"][-1]["boCuc"] = "ket_thuc"
        du_lieu_render, tk = tinh_toan_khung_hinh(kb_6_hoi, thoi_luong_map, slug="test_outro_guard")
        self.assertEqual(tk["soCanhKetThucDaSua"], 3)
        self.assertEqual(kiem_tra_lien_mach_khung_hinh(du_lieu_render), [])
        self.assertEqual(chuan_hoa_bo_cuc_ket_thuc(du_lieu_render), 0)

        # 5. Kiem tra bao loi schema ro rang khi thieu mocThoiGian hoac minhHoaToan rong
        tap_thieu_du_lieu = {
            "tieuDe": "Ramanujan 1729",
            "chuDe": "Toan hoc",
            "chuong": [
                {
                    "id": "chuong_1",
                    "tenChuong": "Hồi 1",
                    "canh": [
                        {"id": "c1", "boCuc": "dong_thoi_gian", "tuFrame": 0, "denFrame": 90},
                        {"id": "c2", "boCuc": "giai_thich_toan", "tuFrame": 90, "denFrame": 180, "minhHoaToan": {"loai": "chuoi_suy_luan"}},
                        {"id": "c3", "boCuc": "giai_thich_toan", "tuFrame": 180, "denFrame": 270, "minhHoaToan": {"loai": "do_thi_ham_so"}},
                    ],
                }
            ],
        }
        loi_schema = kiem_dinh_schema_du_lieu_canh(tap_thieu_du_lieu)
        self.assertEqual(len(loi_schema), 3, f"Phai bao du 3 loi schema thieu du lieu, thuc te: {loi_schema}")

    def test_v20_buoc3_boi_canh_dao_cu_va_vat_the_xung_quanh(self) -> None:
        self.assertGreaterEqual(len(LOAI_BOI_CANH), 22)
        self.assertGreaterEqual(len(LOAI_DAO_CU), 20)
        self.assertEqual(len(LOAI_VAT_THE_XUNG_QUANH), 10)
        for bc in (
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
        ):
            self.assertIn(bc, LOAI_BOI_CANH)
        for dc in (
            "noi_em_be",
            "noi_sup",
            "phong_bi_thu_tay",
            "giuong_benh",
            "bien_so_xe",
            "tach_tra_nong",
            "tau_thuy",
            "ban_hoc_den_dau",
            "qua_dia_cau",
        ):
            self.assertIn(dc, LOAI_DAO_CU)

        raw_kb = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=1)
        raw_kb["chuong"][0]["canh"][0]["boiCanh"] = "duong_pho_xe_co"
        raw_kb["chuong"][0]["canh"][0]["bienSoXe"] = "1729"
        raw_kb["chuong"][0]["canh"][0]["daoCu"] = [
            {"loai": "bien_so_xe", "x": 1450, "y": 540, "bienSoXe": "1729"},
            {"loai": "tach_tra_nong", "x": 620, "y": 680},
        ]
        raw_kb["chuong"][0]["canh"][0]["vatTheXungQuanh"] = [
            {"loai": "xe_taxi_co", "x": 340, "y": 745, "tocDo": 3.2, "bienSoXe": "1729"},
            {"loai": "chim_san_truong", "soLuong": 3},
            {"loai": "khong_hop_le_bi_bo"},
        ]
        kb_sach, _ = chuan_hoa_toan_bo_kich_ban(raw_kb)
        c0 = kb_sach["chuong"][0]["canh"][0]
        self.assertEqual(c0["boiCanh"], "duong_pho_xe_co")
        self.assertEqual(c0["bienSoXe"], "1729")
        self.assertEqual(c0["daoCu"][0]["loai"], "bien_so_xe")
        self.assertEqual(c0["daoCu"][0]["bienSoXe"], "1729")
        self.assertEqual(len(c0["vatTheXungQuanh"]), 2)
        self.assertEqual(c0["vatTheXungQuanh"][0]["loai"], "xe_taxi_co")
        self.assertEqual(c0["vatTheXungQuanh"][0]["bienSoXe"], "1729")

    def test_v20_buoc4_san_tim_chu_de_timeline_phat_am_va_goi_y_boi_canh(self) -> None:
        prompts_nhan: list[str] = []

        class FakeResearchV20:
            def tao_json(self, prompt: str, **kwargs: Any) -> Any:
                prompts_nhan.append(prompt)
                du_lieu = {
                    "tieuDe": "Srinivasa Ramanujan và Con Số 1729",
                    "tomTat1Cau": "Thiên tài tự học từ Madras chinh phục Cambridge và để lại hơn 3.900 đẳng thức.",
                    "timeline_su_kien": [
                        {"nam": "1887", "suKien": "Chào đời tại Erode, Nam Ấn Độ.", "noiBat": False},
                        {"nam": "1903", "suKien": "Đọc cuốn sách 5.000 định lý của G. S. Carr.", "noiBat": False},
                        {"nam": "1913", "suKien": "Gửi bức thư 9 trang chấn động tới G. H. Hardy ở Cambridge.", "noiBat": True},
                        {"nam": "1914", "suKien": "Lên tàu vượt biển sang Anh nghiên cứu tại Trinity College.", "noiBat": False},
                        {"nam": "1918", "suKien": "Trở thành viện sĩ Royal Society và giai thoại số taxi 1729.", "noiBat": True},
                        {"nam": "1920", "suKien": "Phát minh hàm mock theta trong những tháng ngày cuối đời.", "noiBat": False},
                    ],
                    "tu_dien_phat_am": {
                        "Ramanujan": "Ra-ma-nu-gian",
                        "Hardy": "Ha-đi",
                        "Madras": "Ma-đơ-rát",
                        "Littlewood": "Lít-tơ-út",
                        "Cambridge": "Kem-brít",
                        "Namagiri": "Na-ma-ghi-ri",
                        "mock theta": "móc thê-ta",
                        "  ": "bo_qua",
                    },
                    "goi_y_boi_canh_va_dao_cu": [
                        {
                            "giaiDoan": "Chào đời tại Erode",
                            "doTuoi": "so_sinh",
                            "tuThe": "om_em_be",
                            "boiCanh": "nha_co_phong_sinh",
                            "daoCu": ["noi_em_be", "khong_hop_le"],
                            "vatTheXungQuanh": ["ngon_nen_den_dau"],
                            "ghiChu": "Ánh đèn ấm và chiếc nôi em bé.",
                        },
                        {
                            "giaiDoan": "Vượt biển sang Anh",
                            "doTuoi": "truong_thanh",
                            "tuThe": "mac_ao_khoac",
                            "boiCanh": "cang_bien_tau_thuy",
                            "daoCu": ["tau_thuy", "phong_bi_thu_tay"],
                            "vatTheXungQuanh": ["chim_hai_au", "ca_gon_song"],
                        },
                        {
                            "giaiDoan": "Bệnh viện Putney & số taxi 1729",
                            "doTuoi": "truong_thanh",
                            "tuThe": "nam_giuong",
                            "boiCanh": "phong_benh_vien",
                            "daoCu": ["giuong_benh", "bien_so_xe"],
                            "vatTheXungQuanh": ["tuyet_cua_so"],
                        },
                    ],
                    "nhanVatThat": [
                        {"ten": "Srinivasa Ramanujan", "vaiTro": "Nhà Toán học Ấn Độ", "nienDai": "1887-1920", "tinhCachDoiThuong": "Mê công thức đến quên ăn."}
                    ],
                    "giaiThoaiDoiThuong": [
                        {"tieuDe": "Chiếc taxi 1729", "noiDung": "Hardy chê số 1729 tẻ nhạt, Ramanujan bật ngay 1^3+12^3 = 9^3+10^3.", "diemHaiHuoc": "Nhẩm lập phương nhanh hơn bấm máy tính."}
                    ],
                    "kienThucToanCotLoi": [
                        {"tenKienThuc": "Số Taxicab 1729", "giaiThichDeHieu": "Số nhỏ nhất là tổng 2 lập phương theo 2 cách.", "congThucLatex": "1729 = 1^3 + 12^3 = 9^3 + 10^3", "yNghia": "Mở đầu bài toán số Taxicab."}
                    ],
                    "ungDungHienDai": ["Lý thuyết dây & lỗ đen (hàm mock theta)"],
                    "nguonThamKhao": ["https://en.wikipedia.org/wiki/Srinivasa_Ramanujan"],
                }
                if kwargs.get("tra_ve_nguon"):
                    return du_lieu, [{"tieuDe": "Wiki", "url": "https://en.wikipedia.org/wiki/Srinivasa_Ramanujan"}]
                return du_lieu

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path_bn = root / "bo_nho.json"
            tai_bo_nho(path_bn)
            file_tl, tl = nghien_cuu_chu_de(
                slug="ramanujan_1729",
                chu_de="Srinivasa Ramanujan và Con Số 1729",
                thu_muc_du_lieu=root,
                duong_dan_bo_nho=path_bn,
                client=FakeResearchV20(),  # type: ignore[arg-type]
                wiki_fetcher=lambda u, t: (404, ""),
            )
            self.assertTrue(file_tl.exists())
            self.assertEqual(len(prompts_nhan), 1)
            for req in ("timeline_su_kien", "tu_dien_phat_am", "goi_y_boi_canh_va_dao_cu"):
                self.assertIn(req, prompts_nhan[0])

            self.assertEqual(len(tl["timeline_su_kien"]), 6)
            self.assertEqual(tl["timeline_su_kien"][2]["nam"], "1913")
            self.assertTrue(tl["timeline_su_kien"][2]["noiBat"])
            self.assertEqual(tl["tu_dien_phat_am"]["Ramanujan"], "Ra-ma-nu-gian")
            self.assertEqual(tl["tu_dien_phat_am"]["mock theta"], "móc thê-ta")
            self.assertNotIn("  ", tl["tu_dien_phat_am"])
            self.assertEqual(len(tl["goi_y_boi_canh_va_dao_cu"]), 3)
            self.assertEqual(tl["goi_y_boi_canh_va_dao_cu"][0]["boiCanh"], "nha_co_phong_sinh")
            self.assertEqual(tl["goi_y_boi_canh_va_dao_cu"][0]["doTuoi"], "so_sinh")
            self.assertEqual(tl["goi_y_boi_canh_va_dao_cu"][0]["daoCu"], ["noi_em_be"])
            self.assertEqual(tl["goi_y_boi_canh_va_dao_cu"][2]["tuThe"], "nam_giuong")

    def test_v20_buoc4_prompt_2_vai_chong_lap_va_guardrail_cuc_bo(self) -> None:
        # 1. Xac minh enum v2.0 -> v3.0 dong bo day du voi src/kieu_dai.ts
        self.assertGreaterEqual(len(GOC_QUAY_CAMERA), 12)
        self.assertEqual(len(LOAI_CANH), 5)
        self.assertEqual(len(DO_TUOI_NHAN_VAT), 4)
        self.assertEqual(len(TU_THE_NHAN_VAT), 5)
        self.assertGreaterEqual(len(LOAI_HANH_DONG), 20)

        tu_lieu_ram = {
            "tomTat1Cau": "Ramanujan và Hardy tại Cambridge.",
            "timeline_su_kien": [
                {"nam": "1887", "suKien": "Ramanujan chào đời tại Erode.", "noiBat": False},
                {"nam": "1913", "suKien": "Bức thư 9 trang gửi tới Hardy.", "noiBat": True},
                {"nam": "1918", "suKien": "Giai thoại số taxi 1729 tại bệnh viện Putney.", "noiBat": True},
            ],
            "goi_y_boi_canh_va_dao_cu": [
                {"giaiDoan": "Chào đời", "doTuoi": "so_sinh", "tuThe": "om_em_be", "boiCanh": "nha_co_phong_sinh", "daoCu": ["noi_em_be"], "vatTheXungQuanh": ["ngon_nen_den_dau"]},
                {"giaiDoan": "Vượt biển", "doTuoi": "truong_thanh", "tuThe": "mac_ao_khoac", "boiCanh": "cang_bien_tau_thuy", "daoCu": ["tau_thuy"], "vatTheXungQuanh": ["chim_hai_au"]},
                {"giaiDoan": "Bệnh viện", "doTuoi": "truong_thanh", "tuThe": "nam_giuong", "boiCanh": "phong_benh_vien", "daoCu": ["giuong_benh"], "vatTheXungQuanh": ["tuyet_cua_so"]},
                {"giaiDoan": "Phố London", "doTuoi": "truong_thanh", "tuThe": "dung", "boiCanh": "duong_pho_xe_co", "daoCu": ["bien_so_xe"], "vatTheXungQuanh": ["xe_taxi_co"]},
                {"giaiDoan": "Cambridge", "doTuoi": "truong_thanh", "tuThe": "dung", "boiCanh": "san_truong_co_dien", "daoCu": ["cuon_giay"], "vatTheXungQuanh": ["chim_san_truong"]},
                {"giaiDoan": "Giảng đường", "doTuoi": "truong_thanh", "tuThe": "dung", "boiCanh": "giang_duong_dai_hoc", "daoCu": ["bang_den"], "vatTheXungQuanh": []},
            ],
            "tu_dien_phat_am": {"Ramanujan": "Ra-ma-nu-gian", "Hardy": "Ha-đi"},
        }

        bp = {
            "tieuDe": "Ramanujan & Con Số 1729",
            "chuDe": "Thiên tài từ Madras",
            "danhSachNhanVat": [
                {"id": "ramanujan", "ten": "Srinivasa Ramanujan", "mauThan": "#1E293B", "mauChuDao": "#2563EB", "phuKien": "ao_choang"},
                {"id": "hardy", "ten": "G. H. Hardy", "mauThan": "#1E293B", "mauChuDao": "#EA580C", "phuKien": "kinh_tron"},
            ],
        }
        hoi_info = {
            "soHoi": 2,
            "id": "chuong_2",
            "tenChuong": "2. Bức thư 9 trang",
            "boiCanhChinh": "san_truong_co_dien",
            "thoiTietChinh": "nang_dep",
            "tomTat": "Ramanujan gửi thư cho Hardy.",
            "diemHaiHuoc": ["Hardy tưởng trò đùa"],
            "kienThucToan": "Hàm phân hoạch p(n)",
        }
        p2 = tao_prompt_tang_2_hoi(
            blueprint=bp,
            thong_tin_hoi=hoi_info,
            khung_hoi=KHUNG_6_HOI[1],
            giong_ke="di_dom_gan_gui",
            tom_tat_hoi_truoc="Hết hồi 1",
            tu_lieu_nghien_cuu=tu_lieu_ram,
            su_kien_da_dung=["Hoi 1: Giai thoai chiec taxi 1729 o benh vien Putney"],
        )
        for bat_buoc in (
            "BIEN KICH KE CHUYEN",
            "DAO DIEN STORYBOARD",
            "nha_co_phong_sinh",
            "cang_bien_tau_thuy",
            "phong_benh_vien",
            "nam_giuong",
            "duong_pho_xe_co",
            "luotThoai[]",
            "tuongTacVoi",
            "tuDongFocusNguoiNoi",
            "tuong_tac_khan_gia",
            "bieuCamTheoMoc",
            "Giai thoai chiec taxi 1729",
        ):
            self.assertIn(bat_buoc, p2)

        # 2. Tao kich ban co tinh vi pham CA 4 nhom Guardrail
        kb_loi = {
            "tieuDe": "Ramanujan & Con Số 1729",
            "chuDe": "Thiên tài Ấn Độ",
            "danhSachNhanVat": bp["danhSachNhanVat"],
            "chuong": [
                {
                    "id": "chuong_1",
                    "tenChuong": "1. Mở đầu",
                    "canh": [
                        {
                            "id": "canh_001",
                            "boCuc": "mo_dau",
                            "boiCanh": "thu_vien_co_dien",
                            "mayQuay": {"gocQuay": "trung_canh"},
                            "tieuDeNho": "Bức thư kỳ lạ",
                            "loiThoai": "Một phong bì từ Madras đáp xuống bàn làm việc ở Cambridge.",
                            "nhanVat": [{"id": "hardy", "x": 960, "y": 810, "huong": "phai", "hanhDong": "dung_tho", "bieuCam": "ngac_nhien"}],
                        },
                        {
                            "id": "canh_002",
                            "boCuc": "ke_chuyen",
                            "boiCanh": "thu_vien_co_dien",  # Trung boiCanh + trung gocQuay voi canh_001!
                            "mayQuay": {"gocQuay": "trung_canh"},
                            "tieuDeNho": "Đọc thư",
                            "loiThoai": "Hardy mở thư và sững sờ. Cảm ơn bạn đã theo dõi hồi một!",  # Loi CAM ON o hoi giua!
                            "nhanVat": [{"id": "hardy", "x": 960, "y": 810, "huong": "phai", "hanhDong": "ngoi_doc_sach", "bieuCam": "tram_tu"}],
                        },
                        {
                            "id": "canh_003",
                            "boCuc": "dong_thoi_gian",  # Loi timeline rong!
                            "boiCanh": "thu_vien_co_dien",
                            "mayQuay": {"gocQuay": "toan_canh"},
                            "tieuDeNho": "Hành trình cuộc đời",
                            "loiThoai": "Hãy nhìn lại những cột mốc lịch sử của Ramanujan.",
                            "nhanVat": [{"id": "ramanujan", "x": 960, "y": 810, "huong": "phai", "hanhDong": "dung_tho", "bieuCam": "vui_tuoi"}],
                        },
                        {
                            "id": "canh_004",
                            "boCuc": "giai_thich_toan",  # Loi giang_toan rong minhHoaToan!
                            "loaiCanh": "giang_toan",
                            "boiCanh": "lop_hoc_bang_xanh",
                            "mayQuay": {"gocQuay": "trung_canh"},
                            "tieuDeNho": "Số Taxicab 1729",
                            "loiThoai": "1729 bằng 1 lập phương cộng 12 lập phương, và cũng bằng 9 lập phương cộng 10 lập phương.",
                            "congThucLatex": [{"latex": "1729 = 1^3 + 12^3 = 9^3 + 10^3", "nhan": "Tổng hai lập phương"}],
                            "minhHoaToan": {"loai": "chuoi_suy_luan"},
                            "nhanVat": [{"id": "ramanujan", "x": 255, "y": 808, "huong": "phai", "hanhDong": "chi_bang_giang_bai", "bieuCam": "vui_tuoi"}],
                        },
                    ],
                },
                {
                    "id": "chuong_2",
                    "tenChuong": "2. Kết thúc",
                    "canh": [
                        {
                            "id": "canh_005",
                            "boCuc": "ke_chuyen",
                            "boiCanh": "thu_vien_co_dien",
                            "mayQuay": {"gocQuay": "pan_ngang"},
                            "tieuDeNho": "Giai thoại 1729",
                            "loiThoai": "Chiếc taxi mang biển số 1729 đi vào lịch sử Toán học.",
                            "nhanVat": [{"id": "ramanujan", "x": 860, "y": 810, "huong": "phai", "hanhDong": "dung_tho", "bieuCam": "vui_tuoi"}],
                        },
                        {
                            "id": "canh_006",
                            "boCuc": "ke_chuyen",
                            "boiCanh": "thu_vien_co_dien",
                            "mayQuay": {"gocQuay": "pan_ngang"},
                            "tieuDeNho": "Hàm mock theta",
                            "loiThoai": "Những tháng cuối đời ông vẫn sáng tạo hàm mock theta kỳ diệu.",
                            "nhanVat": [{"id": "ramanujan", "x": 860, "y": 810, "huong": "phai", "hanhDong": "ngoi_doc_sach", "bieuCam": "tram_tu"}],
                        },
                        {
                            "id": "canh_007",
                            "boCuc": "ke_chuyen",
                            "boiCanh": "thu_vien_co_dien",
                            "mayQuay": {"gocQuay": "toan_canh"},
                            "tieuDeNho": "Di sản hiện đại",
                            "loiThoai": "Công thức của ông ngày nay giúp nghiên cứu lỗ đen lượng tử.",
                            "nhanVat": [{"id": "ramanujan", "x": 860, "y": 810, "huong": "phai", "hanhDong": "nhin_len_troi", "bieuCam": "vui_tuoi"}],
                        },
                        {
                            "id": "canh_008",
                            "boCuc": "ket_thuc",
                            "boiCanh": "bau_troi_dem_vu_tru",
                            "mayQuay": {"gocQuay": "toan_canh"},
                            "tieuDeNho": "Tạm biệt",
                            "loiThoai": "Cảm ơn bạn đã theo dõi hành trình của Ramanujan!",
                            "nhanVat": [{"id": "ramanujan", "x": 960, "y": 810, "huong": "phai", "hanhDong": "quay_nhin_khan_gia", "bieuCam": "vui_tuoi"}],
                        },
                    ],
                },
            ],
        }

        # Kiem tra prompt tu kiem dinh co muc chong lap y giua cac hoi & canh bao guardrail
        p3 = tao_prompt_tu_kiem_dinh(kb_loi, tu_lieu_nghien_cuu=tu_lieu_ram)
        self.assertIn("SU KIEN / Y DA DUNG QUA TUNG HOI", p3)
        self.assertIn("CANH BAO GUARDRAIL STORYBOARD TU DONG", p3)

        vi_pham = kiem_dinh_guardrail_kich_ban(kb_loi)
        loai_vp = {v["loai"] for v in vi_pham}
        for ky_vong in (
            "trung_boi_canh_va_goc_quay",
            "timeline_rong",
            "giang_toan_rong",
            "cam_on_hoi_giua",
            "thieu_doi_thoai_tuong_tac",
            "thieu_da_dang_boi_canh",
        ):
            self.assertIn(ky_vong, loai_vp, f"Thieu vi pham '{ky_vong}' trong {loai_vp}")

        # 3. Sua loi cuc bo bang Python Guardrail -> 0 vi pham, 0 ro ri Pythagoras
        kb_da_sua, nhat_ky = sua_loi_guardrail_cuc_bo(kb_loi, tu_lieu_nghien_cuu=tu_lieu_ram)
        self.assertGreater(len(nhat_ky), 0)
        self.assertEqual(kiem_dinh_guardrail_kich_ban(kb_da_sua), [])
        self.assertEqual(kiem_tra_ro_ri_pythagoras(kb_da_sua), [])
        self.assertEqual(kiem_dinh_schema_du_lieu_canh(kb_da_sua), [])

        # Xac minh Hoi 1 khong con "Cam on", Hoi 2 (hoi cuoi) van giu "Cam on"
        self.assertNotIn("cảm ơn", kb_da_sua["chuong"][0]["canh"][1]["loiThoai"].lower())
        self.assertIn("Cảm ơn", kb_da_sua["chuong"][1]["canh"][-1]["loiThoai"])
        # Xac minh timeline da lay dung du lieu Ramanujan (nam 1887/1913/1918)
        mocs = kb_da_sua["chuong"][0]["canh"][2]["mocThoiGian"]
        self.assertEqual([m["nam"] for m in mocs], ["1887", "1913", "1918"])
        # Xac minh >= 25% doi thoai/tuong tac & >= 6 boi canh khac nhau
        tat_ca = [c for ch in kb_da_sua["chuong"] for c in ch["canh"]]
        self.assertGreaterEqual(len({c["boiCanh"] for c in tat_ca}), 6)
        self.assertGreaterEqual(sum(1 for c in tat_ca if la_canh_doi_thoai_hoac_tuong_tac(c)) / len(tat_ca), 0.25)
        for i in range(1, len(tat_ca)):
            self.assertFalse(
                tat_ca[i]["boiCanh"] == tat_ca[i - 1]["boiCanh"]
                and lay_goc_quay_canh(tat_ca[i]) == lay_goc_quay_canh(tat_ca[i - 1])
            )

        # 4. Kiem tra che do AI sua cuc bo (cho_phep_goi_ai=True) voi FakeGemini
        goi_ai_fix = {"n": 0}

        class FakeGuardrailAI:
            def tao_json(self, prompt: str, **kwargs: Any) -> Any:
                goi_ai_fix["n"] += 1
                return {
                    "canhSua": [
                        {
                            "id": "canh_002",
                            "gocQuay": "can_mat",
                            "loiThoai": "Hardy mở thư và sững sờ trước những đẳng thức chưa từng thấy.",
                        }
                    ]
                }

        kb_ai_fix, _ = sua_loi_guardrail_cuc_bo(
            kb_loi,
            tu_lieu_nghien_cuu=tu_lieu_ram,
            gemini=FakeGuardrailAI(),  # type: ignore[arg-type]
            cho_phep_goi_ai=True,
        )
        self.assertEqual(goi_ai_fix["n"], 1)
        self.assertEqual(kiem_dinh_guardrail_kich_ban(kb_ai_fix), [])
        self.assertIn("sững sờ trước những đẳng thức", kb_ai_fix["chuong"][0]["canh"][1]["loiThoai"])

    def test_v20_buoc4_tu_dien_phat_am_va_luot_thoai_da_giong_rms(self) -> None:
        # 1. Kiem tra tu dien phat am mac dinh & tuy chinh cho Edge TTS
        self.assertIn("Ramanujan", TU_DIEN_PHAT_AM_MAC_DINH)
        self.assertIn("mock theta", TU_DIEN_PHAT_AM_MAC_DINH)
        cau_goc = "Ramanujan từ Madras gửi thư tới Hardy và Littlewood tại Cambridge về nữ thần Namagiri và hàm mock theta."
        cau_tts = chuan_hoa_doc_toan(cau_goc)
        for phien_am in ("Ra-ma-nu-gian", "Ma-đơ-rát", "Ha-đi", "Lít-tơ-út", "Kem-brít", "Na-ma-ghi-ri", "móc thê-ta"):
            self.assertIn(phien_am, cau_tts)

        # 2. Kiem tra phan giong on dinh & khac biet giua Nguoi dan va tung Nhan vat
        ds_nv = [
            {"id": "ramanujan", "ten": "Srinivasa Ramanujan"},
            {"id": "hardy", "ten": "G. H. Hardy"},
            {"id": "littlewood", "ten": "J. E. Littlewood"},
        ]
        g_dan = lay_cau_hinh_giong_theo_vai("nguoi_dan")
        g_ram = lay_cau_hinh_giong_nhan_vat("ramanujan", ds_nv)
        g_har = lay_cau_hinh_giong_nhan_vat("hardy", ds_nv)
        g_lit = lay_cau_hinh_giong_nhan_vat("littlewood", ds_nv)
        self.assertNotEqual(g_dan, g_ram)
        self.assertNotEqual(g_dan, g_har)
        self.assertNotEqual(g_ram, g_har)
        self.assertNotEqual(g_ram, g_lit)
        # On dinh tuyet doi giua cac lan goi
        self.assertEqual(g_ram, lay_cau_hinh_giong_nhan_vat("ramanujan", ds_nv))

        # 3. Chay tron ven chuan_bi_audio_va_du_lieu_render offline voi tu_lieu_nghien_cuu.json + luotThoai[]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            du_lieu_dir = root / "du_lieu"
            public_dir = root / "public"
            out_dir = root / "out"
            slug = "ramanujan_demo"
            (du_lieu_dir / slug).mkdir(parents=True)

            # Luu tu_lieu_nghien_cuu.json chua tu_dien_phat_am rieng cua tap
            (du_lieu_dir / slug / "tu_lieu_nghien_cuu.json").write_text(
                json.dumps(
                    {
                        "slug": slug,
                        "tu_dien_phat_am": {
                            "Putney": "Pát-ni",
                            "Taxicab": "Tắc-xi-cáp",
                        },
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            td_nap = tai_tu_dien_phat_am(du_lieu_dir / slug / "tu_lieu_nghien_cuu.json")
            self.assertEqual(td_nap["Putney"], "Pát-ni")
            self.assertEqual(td_nap["Ramanujan"], "Ra-ma-nu-gian")
            self.assertIn("Pát-ni", ap_dung_tu_dien_phat_am("Bệnh viện Putney", td_nap))

            kb_ram = {
                "tieuDe": "Ramanujan & Con Số 1729",
                "chuDe": "Bí mật số Taxicab tại bệnh viện Putney",
                "batSfx": False,
                "batPhuDe": True,
                "bangMau": {
                    "nenChinh": "#0EA5E9",
                    "nenPhu": "#FEF3C7",
                    "luoi": "#CBD5E1",
                    "chuChinh": "#FFFFFF",
                    "chuPhu": "#FEF08A",
                    "nhanManh": "#FACC15",
                    "canhBao": "#FB923C",
                },
                "danhSachNhanVat": [
                    {"id": "ramanujan", "ten": "Srinivasa Ramanujan", "mauThan": "#1E293B", "mauChuDao": "#2563EB", "phuKien": "ao_choang"},
                    {"id": "hardy", "ten": "G. H. Hardy", "mauThan": "#1E293B", "mauChuDao": "#EA580C", "phuKien": "kinh_tron"},
                ],
                "chuong": [
                    {
                        "id": "chuong_1",
                        "tenChuong": "1. Bệnh viện Putney",
                        "canh": [
                            {
                                "id": "canh_001",
                                "boCuc": "ke_chuyen",
                                "vaiNoi": "nguoi_dan",
                                "boiCanh": "phong_benh_vien",
                                "loiThoai": "Năm 1918, Hardy ghé thăm Ramanujan tại bệnh viện Putney gần Cambridge.",
                                "nhanVat": [{"id": "ramanujan", "x": 760, "y": 810, "huong": "phai", "hanhDong": "dung_tho", "bieuCam": "tram_tu"}],
                            },
                            {
                                "id": "canh_002",
                                "boCuc": "doi_thoai",
                                "loaiCanh": "doi_thoai",
                                "boiCanh": "phong_benh_vien",
                                "mayQuay": {"gocQuay": "focus_trai", "tuDongFocusNguoiNoi": True},
                                "loiThoai": "Chiếc taxi mang số 1729 tẻ nhạt quá! Không đâu Hardy, đó là số Taxicab cực kỳ đặc biệt!",
                                "luotThoai": [
                                    {
                                        "nhanVatId": "hardy",
                                        "noiDung": "Chiếc taxi ở Putney mang số 1729 tẻ nhạt quá!",
                                        "bieuCam": "tram_tu",
                                        "dongTac": "quay_nhin_doi_thoai",
                                        "batDauFrame": 0,
                                        "ketThucFrame": 60,
                                    },
                                    {
                                        "nhanVatId": "ramanujan",
                                        "noiDung": "Không đâu Hardy, đó là số Taxicab và liên hệ cả hàm mock theta!",
                                        "bieuCam": "vui_tuoi",
                                        "dongTac": "giat_minh_bat_day",
                                        "batDauFrame": 66,
                                        "ketThucFrame": 140,
                                    },
                                ],
                                "nhanVat": [
                                    {"id": "hardy", "x": 640, "y": 810, "huong": "phai", "hanhDong": "quay_nhin_doi_thoai", "bieuCam": "tram_tu", "tuongTacVoi": "ramanujan"},
                                    {"id": "ramanujan", "x": 1280, "y": 810, "huong": "trai", "hanhDong": "giat_minh_bat_day", "bieuCam": "vui_tuoi", "tuongTacVoi": "hardy"},
                                ],
                            },
                        ],
                    }
                ],
            }
            (du_lieu_dir / slug / "nhap_kich_ban.json").write_text(
                json.dumps(kb_ram, ensure_ascii=False),
                encoding="utf-8",
            )

            tts_calls: list[tuple[str, str, str, str, str]] = []
            concat_calls: list[tuple[list[str], str]] = []

            def fake_tts(cid: str, txt: str, path: Path, v: str, r: str, p: str) -> None:
                tts_calls.append((cid, txt, v, r, p))
                path.write_bytes(f"MP3_{cid}_{v}_{r}_{p}".encode("utf-8"))

            def fake_probe(path: Path) -> float:
                if "luot_01" in path.name:
                    return 2.0
                if "luot_02" in path.name:
                    return 3.0
                return 4.0

            def fake_rms(path: Path, fps: int) -> list[float]:
                n = int(round(fake_probe(path) * fps))
                val = 0.72 if "luot_01" in path.name else (0.88 if "luot_02" in path.name else 0.55)
                return [val] * n

            def fake_concat(ds: list[Path], out_p: Path, gap: float) -> Path:
                concat_calls.append(([p.name for p in ds], out_p.name))
                out_p.write_bytes(b"CONCAT_DIALOGUE_MP3")
                return out_p

            file_render, tk = chuan_bi_audio_va_du_lieu_render(
                slug=slug,
                thu_muc_du_lieu=du_lieu_dir,
                thu_muc_public=public_dir,
                thu_muc_out=out_dir,
                tts_generator=fake_tts,
                duration_prober=fake_probe,
                rms_extractor=fake_rms,
                audio_concatenator=fake_concat,
            )
            self.assertTrue(file_render.exists())
            self.assertEqual(tk["soCanhDaLuotThoai"], 1)
            self.assertEqual(len(tts_calls), 3)  # canh_001 + canh_002_luot_01 + canh_002_luot_02
            self.assertEqual(len(concat_calls), 1)
            self.assertEqual(concat_calls[0], (["canh_002_luot_01.mp3", "canh_002_luot_02.mp3"], "canh_002.mp3"))

            # Xac minh Edge TTS nhan phien am tieng Viet tu tu_dien_phat_am
            by_id = {c[0]: c for c in tts_calls}
            self.assertIn("Ha-đi", by_id["canh_001"][1])
            self.assertIn("Ra-ma-nu-gian", by_id["canh_001"][1])
            self.assertIn("Pát-ni", by_id["canh_001"][1])
            self.assertIn("Kem-brít", by_id["canh_001"][1])
            self.assertIn("Pát-ni", by_id["canh_002_luot_01"][1])
            self.assertIn("Tắc-xi-cáp", by_id["canh_002_luot_02"][1])
            self.assertIn("móc thê-ta", by_id["canh_002_luot_02"][1])

            # Xac minh giong Nguoi dan != Hardy != Ramanujan
            v_dan = by_id["canh_001"][2:5]
            v_har = by_id["canh_002_luot_01"][2:5]
            v_ram = by_id["canh_002_luot_02"][2:5]
            self.assertNotEqual(v_dan, v_har)
            self.assertNotEqual(v_dan, v_ram)
            self.assertNotEqual(v_har, v_ram)

            # Xac minh du_lieu_render.json & phu_de.srt GIU NGUYEN chinh ta goc dep + moc frame & RMS tung luot
            render_data = json.loads(file_render.read_text(encoding="utf-8"))
            self.assertEqual(kiem_tra_lien_mach_khung_hinh(render_data), [])
            c1, c2 = render_data["chuong"][0]["canh"]
            self.assertIn("Ramanujan", c1["loiThoai"])
            self.assertIn("Putney", c1["loiThoai"])
            self.assertNotIn("Ra-ma-nu-gian", c1["loiThoai"])
            self.assertIn("Taxicab", c2["luotThoai"][1]["noiDung"])
            self.assertIn("mock theta", c2["luotThoai"][1]["noiDung"])

            # Kiem tra batDauFrame / ketThucFrame va RMS 30fps rieng cho tung luot thoai
            nghi_f = int(round(NGHI_GIUA_LUOT_THOAI_GIAY * 30))
            lt0, lt1 = c2["luotThoai"]
            self.assertEqual(lt0["batDauFrame"], 0)
            self.assertEqual(lt0["ketThucFrame"], 60)
            self.assertEqual(len(lt0["bienDoAmThanh"]), 60)
            self.assertEqual(lt0["bienDoAmThanh"][0], 0.72)

            self.assertEqual(lt1["batDauFrame"], 60 + nghi_f)
            self.assertEqual(lt1["ketThucFrame"], 60 + nghi_f + 90)
            self.assertEqual(len(lt1["bienDoAmThanh"]), 90)
            self.assertEqual(lt1["bienDoAmThanh"][0], 0.88)

            # SRT phai giu nguyen chinh ta goc dep (khong chua phien am TTS)
            srt_txt = (out_dir / slug / "phu_de.srt").read_text(encoding="utf-8")
            self.assertIn("Ramanujan", srt_txt)
            self.assertIn("Putney", srt_txt)
            self.assertIn("Taxicab", srt_txt)
            self.assertNotIn("Ra-ma-nu-gian", srt_txt)
            self.assertNotIn("Pát-ni", srt_txt)

            # Chay lan 2 phai hit cache 100% (khong goi TTS va khong ghep lai)
            tts_calls.clear()
            concat_calls.clear()
            chuan_bi_audio_va_du_lieu_render(
                slug=slug,
                thu_muc_du_lieu=du_lieu_dir,
                thu_muc_public=public_dir,
                thu_muc_out=out_dir,
                tts_generator=fake_tts,
                duration_prober=fake_probe,
                rms_extractor=fake_rms,
                audio_concatenator=fake_concat,
            )
            self.assertEqual(tts_calls, [])
            self.assertEqual(concat_calls, [])

        # Kiem tra tinh_moc_va_rms_luot_thoai truc tiep
        luot_res, rms_tong, tong_s = tinh_moc_va_rms_luot_thoai(
            [{"nhanVatId": "a", "noiDung": "A"}, {"nhanVatId": "b", "noiDung": "B"}],
            [1.0, 1.5],
            [[0.5] * 30, [0.9] * 45],
            fps=30,
            nghi_giua_luot=0.2,
        )
        self.assertEqual(luot_res[0]["batDauFrame"], 0)
        self.assertEqual(luot_res[0]["ketThucFrame"], 30)
        self.assertEqual(luot_res[1]["batDauFrame"], 36)
        self.assertEqual(luot_res[1]["ketThucFrame"], 81)
        self.assertEqual(len(rms_tong), 81)
        self.assertEqual(rms_tong[30:36], [0.0] * 6)
        self.assertAlmostEqual(tong_s, 2.7, places=2)

    def test_v20_buoc5_chia_chunk_thong_minh_ci_va_gitignore(self) -> None:
        from PIL import Image

        # 1. Tao kich ban 6 hoi: Hoi 1,2,5,6 <= 120s; Hoi 3 (~150s) & Hoi 4 (~160s) > 120s -> phai chia 2 manh!
        kb = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=6)  # 36 canh
        thoi_luong: dict[str, float] = {}
        stt = 1
        for h in range(1, 7):
            dur_moi_canh = 26.0 if h in (3, 4) else 12.0  # Hoi 3,4 ~158s (>120s); Hoi 1,2,5,6 ~74s (<=120s)
            for _ in range(6):
                thoi_luong[f"canh_{stt:03d}"] = dur_moi_canh
                stt += 1

        du_lieu_render, _ = tinh_toan_khung_hinh(kb, thoi_luong, slug="chunk_demo", fps=30)
        chunks = tinh_danh_sach_chunk_render(du_lieu_render, fps=30, nguong_giay=NGUONG_CHIA_CHUNK_GIAY)
        chunk_ids = [c["chunkId"] for c in chunks]
        self.assertEqual(
            chunk_ids,
            ["hoi_01", "hoi_02", "hoi_03_p1", "hoi_03_p2", "hoi_04_p1", "hoi_04_p2", "hoi_05", "hoi_06"],
        )

        # Kiem tra khung hinh cac chunk noi tiep lien mach 100%, khong trung frame bien, khong gap frame
        self.assertEqual(chunks[0]["tuFrame"], 0)
        for i in range(len(chunks)):
            self.assertEqual(chunks[i]["endFrameInclusive"], chunks[i]["denFrame"] - 1)
            self.assertLessEqual(chunks[i]["giay"], 120.0)
            if i > 0:
                self.assertEqual(chunks[i]["tuFrame"], chunks[i - 1]["denFrame"])

        # 2. Kiem tra nhan dien CI=true & thong so Remotion an toan (--concurrency=2, --jpeg-quality=85, --log=warn)
        self.assertTrue(dang_chay_tren_ci({"CI": "true"}))
        self.assertTrue(dang_chay_tren_ci({"GITHUB_ACTIONS": "true"}))
        self.assertFalse(dang_chay_tren_ci({"CI": "false"}))
        cfg_ci = xac_dinh_tham_so_render_ci(env={"CI": "true"})
        self.assertTrue(cfg_ci["laCi"])
        self.assertEqual(cfg_ci["concurrency"], 2)
        self.assertEqual(cfg_ci["jpegQuality"], 85)
        self.assertEqual(cfg_ci["logLevel"], "warn")
        self.assertEqual(cfg_ci["maxOldSpaceMb"], 4096)

        cmd_ci = dung_lenh_render_remotion(
            file_mp4=Path("out/demo/chuong/hoi_03_p1.mp4"),
            file_props=Path("du_lieu/demo/du_lieu_render.json"),
            tu_frame=100,
            end_frame_inclusive=200,
            npx_bin="npx",
            env={"CI": "true"},
        )
        self.assertEqual(cmd_ci[5], str(Path("out/demo/chuong/hoi_03_p1.mp4")))
        self.assertIn("--concurrency=2", cmd_ci)
        self.assertIn("--jpeg-quality=85", cmd_ci)
        self.assertIn("--log=warn", cmd_ci)

        # 3. Kiem tra render_mot_chunk + giai_danh_sach_file_ghep + chi_ghep_hoan_chinh + san_xuat_lien_tuc meta JSON
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            file_props = root / "du_lieu" / "chunk_demo" / "du_lieu_render.json"
            file_props.parent.mkdir(parents=True)
            file_props.write_text(json.dumps(du_lieu_render, ensure_ascii=False), encoding="utf-8")
            out_dir = root / "out"

            lenh_chunks: list[list[str]] = []

            def fake_run_chunk(cmd: list[str], cwd: Path | None) -> None:
                lenh_chunks.append(cmd)
                Path(cmd[5]).write_bytes(b"FAKE_CHUNK_MP4")

            # Render tung chunk (8 chunks) o che do CI
            for ck in chunks:
                res_ck = render_mot_chunk(
                    slug="chunk_demo",
                    chunk_id=ck["chunkId"],
                    duong_dan_props=file_props,
                    che_do_ci=True,
                    thu_muc_out=out_dir,
                    thu_muc_public=root / "public",
                    npx_bin="npx",
                    command_runner=fake_run_chunk,
                )
                self.assertEqual(res_ck["cheDo"], "chi_render_chunk")
                self.assertTrue(res_ck["daRender"])
                self.assertTrue(res_ck["fileChunk"].exists())

            self.assertEqual(len(lenh_chunks), 8)
            self.assertIn("--concurrency=2", lenh_chunks[2])
            self.assertIn("--jpeg-quality=85", lenh_chunks[2])

            # Giai danh sach file ghep dung thu tu 8 manh
            ds_ghep = giai_danh_sach_file_ghep(
                pham_vi_chuong=tinh_pham_vi_frame_chuong(du_lieu_render),
                thu_muc_hoi=out_dir / "chunk_demo" / "chuong",
                danh_sach_chunk=chunks,
            )
            self.assertEqual(
                [p.name for p in ds_ghep],
                [f"{cid}.mp4" for cid in chunk_ids],
            )

            # Ghep hoan chinh tu 8 chunk
            so_file_ghep: list[int] = []

            def fake_merge_ck(ds_mp4: list[Path], out_mp4: Path, **kwargs: Any) -> Path:
                so_file_ghep.append(len(ds_mp4))
                out_mp4.write_bytes(b"MERGED_8_CHUNKS")
                return out_mp4

            kq_ghep = render_toan_bo_video(
                slug="chunk_demo",
                duong_dan_props=file_props,
                chi_ghep_hoan_chinh=True,
                bo_qua_thumbnail=True,
                bo_qua_visual_qa=True,
                thu_muc_out=out_dir,
                thu_muc_public=root / "public",
                merge_fn=fake_merge_ck,
                grid_fn=lambda file_anh_xuat, **kw: (
                    Image.new("RGB", (120, 68), color=(15, 23, 42)).save(str(file_anh_xuat), format="PNG") or file_anh_xuat
                ),
            )
            self.assertEqual(so_file_ghep, [8])
            self.assertTrue(kq_ghep["video"].exists())

            # Kiem tra CLI parser bao loi khi xung dot --chi-render-hoi va --chi-render-chunk
            self.assertEqual(
                main_render_dai(["--slug", "demo", "--chi-render-hoi", "1", "--chi-render-chunk", "hoi_01"]),
                2,
            )
            self.assertEqual(
                main_render_dai(["--slug", "demo", "--chi-render-chunk", "hoi_01", "--chi-ghep-hoan-chinh"]),
                2,
            )

            # Kiem tra san_xuat_lien_tuc --chi-chuan-bi xuat danhSachChunk trong meta JSON
            path_bn = root / "bo_nho_ck.json"
            tai_bo_nho(path_bn)
            file_meta = root / "out" / "meta_chunk.json"
            chay_san_xuat_lien_tuc(
                chu_de="Ramanujan va so 1729",
                slug="chunk_demo",
                chi_chuan_bi=True,
                file_meta_json=file_meta,
                duong_dan_bo_nho=path_bn,
                thu_muc_du_lieu=root / "du_lieu_sx",
                nghien_cuu_fn=lambda slug, chu_de, **kw: (root / "tl.json", {"tomTat1Cau": "Test chunk"}),
                bien_kich_fn=lambda chu_de, slug, **kw: (root / "kb.json", root / "kb.md", du_lieu_render),
                tts_fn=lambda slug, **kw: (file_props, {"tongGiay": 640.0, "datTren10Phut": True}),
            )
            meta_doc = json.loads(file_meta.read_text(encoding="utf-8"))
            self.assertEqual(meta_doc["danhSachHoi"], [1, 2, 3, 4, 5, 6])
            self.assertEqual(meta_doc["danhSachChunk"], chunk_ids)
            self.assertEqual(meta_doc["soChunk"], 8)
            self.assertEqual(len(meta_doc["chiTietChunk"]), 8)

        # 4. Kiem tra .gitignore chan tuyet doi .env, node_modules/, out/, __pycache__/, *.mp4, audio tam
        gi_text = (GOC_DU_AN / ".gitignore").read_text(encoding="utf-8")
        for dong_gi in (".env", "node_modules/", "out/", "__pycache__/", "*.mp4", "public/audio/**/*.mp3"):
            self.assertIn(dong_gi, gi_text, f".gitignore thieu quy tac loai tru: {dong_gi}")

    def test_v20_tu_dong_hang_ngay_san_chu_de_khi_hang_doi_rong_va_khong_trung(self) -> None:
        """
        Kiem chung kich ban chay tu dong hang ngay tren GitHub Actions (khong truyen --chu-de):
        Hang doi rong -> tu goi san_tim_chu_de nap 6 chu de -> chon chu de uu tien #1 ->
        hoan tat & xoa khoi hang doi -> ngay hom sau chon chu de khac khong bao gio trung.
        """
        du_lieu_mau = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=2)
        thoi_luong = {f"canh_{i:03d}": 4.5 for i in range(1, 13)}
        du_lieu_render, _ = tinh_toan_khung_hinh(du_lieu_mau, thoi_luong, slug="daily_auto", fps=30)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path_bn = root / "bo_nho_hang_ngay.json"
            tai_bo_nho(path_bn)  # Bat dau voi hang_doi_chu_de = [], chu_de_da_lam = []

            lan_san: list[int] = []
            dot_san = {"i": 0}

            class FakeDailyHunterGemini:
                def tao_json(self, prompt: str, **kwargs: Any) -> Any:
                    dot_san["i"] += 1
                    if dot_san["i"] == 1:
                        # Dot 1: san 6 chu de khi hang doi rong
                        return {
                            "chuDeDeXuat": [
                                {"slug": "galois_dem_trang", "tieuDe": "Évariste Galois và Đêm Trắng Lý Thuyết Nhóm", "gocKhaiThac": "Giai thoai doi thuc", "diemThuHut": 9.8, "doSauToanHoc": 9.5},
                                {"slug": "euler_7_cau", "tieuDe": "Leonhard Euler và 7 Cây Cầu Königsberg", "gocKhaiThac": "Tro do cuoi tuan", "diemThuHut": 9.4, "doSauToanHoc": 9.1},
                                {"slug": "cardano_tartaglia", "tieuDe": "Cardano vs Tartaglia và Phương Trình Bậc 3", "gocKhaiThac": "Loi the bi mat", "diemThuHut": 9.1, "doSauToanHoc": 8.9},
                                {"slug": "cantor_vo_cuc", "tieuDe": "Georg Cantor và Các Cấp Độ Vô Cực", "gocKhaiThac": "Vo cuc lon hon vo cuc", "diemThuHut": 8.9, "doSauToanHoc": 9.0},
                                {"slug": "noether_doi_xung", "tieuDe": "Emmy Noether và Định Lý Đối Xứng Vũ Trụ", "gocKhaiThac": "Bao toan nang luong", "diemThuHut": 8.8, "doSauToanHoc": 9.0},
                                {"slug": "turing_enigma", "tieuDe": "Alan Turing và Cỗ Máy Giải Mã Enigma", "gocKhaiThac": "Chiec may tinh dau tien", "diemThuHut": 8.7, "doSauToanHoc": 8.8},
                            ]
                        }
                    # Dot 2 (khi hang doi tut < 3): co tinh goi y lai galois_dem_trang de kiem tra chong trung!
                    return {
                        "chuDeDeXuat": [
                            {"slug": "galois_dem_trang", "tieuDe": "Évariste Galois và Đêm Trắng Lý Thuyết Nhóm", "gocKhaiThac": "Trung da lam", "diemThuHut": 9.9, "doSauToanHoc": 9.9},
                            {"slug": "gauss_tong_100", "tieuDe": "Carl Friedrich Gauss và Phép Tính 3 Giây", "gocKhaiThac": "Giai thoai lop hoc", "diemThuHut": 9.3, "doSauToanHoc": 8.8},
                            {"slug": "hypatia_alexandria", "tieuDe": "Hypatia và Thư Viện Alexandria", "gocKhaiThac": "Nha Toan hoc nu tien phong", "diemThuHut": 9.0, "doSauToanHoc": 8.7},
                            {"slug": "ada_lovelace_may_tinh", "tieuDe": "Ada Lovelace và Chương Trình Máy Tính Đầu Tiên", "gocKhaiThac": "Lap trinh vien dau tien", "diemThuHut": 9.2, "doSauToanHoc": 8.9},
                            {"slug": "archimedes_vuong_mien", "tieuDe": "Archimedes và Chiếc Vương Miện Vàng", "gocKhaiThac": "Tieng het Eureka", "diemThuHut": 9.1, "doSauToanHoc": 8.8},
                        ]
                    }

            def fake_nap_wrapper(so_luong: int, duong_dan_bo_nho: Path | str, client: Any = None) -> list[dict[str, Any]]:
                lan_san.append(so_luong)
                return nap_hang_doi_chu_de(so_luong=so_luong, duong_dan_bo_nho=duong_dan_bo_nho, client=FakeDailyHunterGemini())  # type: ignore[arg-type]

            def chay_1_ngay(ten_meta: str) -> str:
                file_meta = root / "out" / ten_meta
                file_props = root / "du_lieu" / "render_tmp.json"
                file_props.parent.mkdir(parents=True, exist_ok=True)
                file_props.write_text(json.dumps(du_lieu_render, ensure_ascii=False), encoding="utf-8")

                kq = chay_san_xuat_lien_tuc(
                    chu_de="",  # Khong truyen chu de nhu khi chay schedule 07:00 sang hang ngay
                    chi_chuan_bi=True,
                    file_meta_json=file_meta,
                    duong_dan_bo_nho=path_bn,
                    thu_muc_du_lieu=root / "du_lieu_run",
                    nap_hang_doi_fn=fake_nap_wrapper,
                    nghien_cuu_fn=lambda slug, chu_de, **kw: (root / f"{slug}_tl.json", {"tomTat1Cau": f"Tóm tắt {chu_de}", "nguonThamKhao": ["https://example.org/" + slug]}),
                    bien_kich_fn=lambda chu_de, slug, **kw: (root / f"{slug}_kb.json", root / f"{slug}_kb.md", {**du_lieu_render, "tieuDe": chu_de}),
                    tts_fn=lambda slug, **kw: (file_props, {"tongGiay": 645.0, "datTren10Phut": True}),
                )
                self.assertEqual(kq[0]["trangThai"], "thanh_cong")
                slug_chon = str(kq[0]["slug"])
                # Gia lap job ghep-va-luu hoan tat -> ghi vao chu_de_da_lam & xoa khoi hang_doi_chu_de
                hoan_tat_tap_tu_meta(file_meta, duong_dan_bo_nho=path_bn)
                return slug_chon

            # Ngay 1: hang doi rong (0 < 3) -> tu san 6 chu de -> chon #1 (galois_dem_trang)
            s1 = chay_1_ngay("meta_ngay_1.json")
            self.assertEqual(s1, "galois_dem_trang")
            self.assertEqual(lan_san, [6])  # San 6 chu de (trong khoang 5-8)
            bn1 = tai_bo_nho(path_bn)
            self.assertEqual([x["slug"] for x in bn1["chu_de_da_lam"]], ["galois_dem_trang"])
            self.assertNotIn("galois_dem_trang", [x["slug"] for x in bn1["hang_doi_chu_de"]])
            self.assertEqual(len(bn1["hang_doi_chu_de"]), 5)

            # Ngay 2..4: con >= 3 chu de cho -> chon lan luot theo uu tien, KHONG goi san them
            s2 = chay_1_ngay("meta_ngay_2.json")
            s3 = chay_1_ngay("meta_ngay_3.json")
            s4 = chay_1_ngay("meta_ngay_4.json")
            self.assertEqual(s2, "euler_7_cau")
            self.assertEqual(s3, "cardano_tartaglia")
            self.assertEqual(s4, "cantor_vo_cuc")
            self.assertEqual(lan_san, [6])  # Chua can san lai vi van >= 3

            # Ngay 5: hang doi chi con 2 (< 3) -> TU DONG san them dot 2 va LOAI BO galois_dem_trang da lam!
            s5 = chay_1_ngay("meta_ngay_5.json")
            self.assertEqual(lan_san, [6, 6])
            self.assertNotIn(s5, {s1, s2, s3, s4})
            bn5 = tai_bo_nho(path_bn)
            slugs_da_lam = [x["slug"] for x in bn5["chu_de_da_lam"]]
            slugs_hang_doi = [x["slug"] for x in bn5["hang_doi_chu_de"]]
            self.assertEqual(len(slugs_da_lam), 5)
            self.assertEqual(len(set(slugs_da_lam)), 5)  # 0 trung lap
            self.assertEqual(set(slugs_da_lam) & set(slugs_hang_doi), set())  # Da xoa sach khoi hang doi

    def test_v20_buoc6_mau_v2_tuong_tac_end_to_end(self) -> None:
        p_mau_v2 = GOC_DU_AN / "du_lieu" / "mau_v2_tuong_tac.json"
        self.assertTrue(p_mau_v2.exists(), "Thieu du_lieu/mau_v2_tuong_tac.json")
        mau_v2 = json.loads(p_mau_v2.read_text(encoding="utf-8"))
        self.assertEqual(kiem_tra_lien_mach_khung_hinh(mau_v2), [])
        self.assertEqual(kiem_tra_ro_ri_pythagoras(mau_v2), [])
        self.assertEqual(kiem_dinh_schema_du_lieu_canh(mau_v2), [])
        self.assertEqual(kiem_dinh_guardrail_kich_ban(mau_v2), [])
        tat_ca = [c for ch in mau_v2["chuong"] for c in ch["canh"]]
        self.assertGreaterEqual(len({c["boiCanh"] for c in tat_ca}), 6)
        self.assertTrue(any(c.get("loaiCanh") == "doi_thoai" and c.get("luotThoai") for c in tat_ca))
        self.assertTrue(any(c.get("loaiCanh") == "tuong_tac_khan_gia" and c.get("cauHoiTuongTac") for c in tat_ca))
        self.assertTrue(any(c.get("boCuc") == "giai_thich_toan" and c.get("minhHoaToan") for c in tat_ca))


class TestNangCapV25Buoc1Offline(unittest.TestCase):
    """Unit test offline cho 6 nhom sua loi v2.5 Buoc 1 (tap Georg Cantor)."""

    def test_v25_1_kiem_tra_va_tu_dong_sua_dau_tieng_viet(self) -> None:
        kb = {
            "tieuDe": "Georg Cantor va Cuoc cach mang vo cuc",
            "chuDe": "Hành trình chinh phục những cấp độ vô cực",
            "danhSachNhanVat": [{"id": "cantor", "ten": "Georg Cantor"}],
            "chuong": [
                {
                    "id": "hoi_1",
                    "tenChuong": "Hồi 1: Cú sốc vô cực",
                    "phuDeHoi": "Cuoc tranh luan gay gat giua Cantor va Kronecker ve tap vo han",
                    "canh": [
                        {
                            "id": "canh_001",
                            "boCuc": "giai_thich_toan",
                            "tieuDeNho": "Anh xa mot mot giua hai tap hop",
                            "loiThoai": "Cac ban biet khong, tap so tu nhien va tap so chan co cung luc luong vo cuc!",
                            "luotThoai": [
                                {
                                    "nhanVatId": "cantor",
                                    "noiDung": "Giai thoai bat ngo nay khien ca giang duong im lang!",
                                }
                            ],
                            "minhHoaToan": {
                                "loai": "so_do_anh_xa",
                                "tieuDe": "Luy thua vo cuc va anh xa mot mot",
                                "thamSo": {
                                    "tenTrai": "Tap so tu nhien N",
                                    "tenPhai": "Tap so chan",
                                    "cotTrai": ["1", "2", "3"],
                                    "cotPhai": ["2", "4", "6"],
                                },
                            },
                            "goiY": "Goi y cho khan gia suy nghi ky truoc khi tra loi",
                        }
                    ],
                }
            ],
        }
        vi_pham = kiem_tra_dau_tieng_viet(kb)
        duong_dan = {v["duongDan"] for v in vi_pham}
        self.assertTrue(any("tieuDe" in p for p in duong_dan))
        self.assertTrue(any("phuDeHoi" in p for p in duong_dan))
        self.assertTrue(any("loiThoai" in p for p in duong_dan))
        self.assertTrue(any("luotThoai" in p for p in duong_dan))
        self.assertTrue(any("minhHoaToan" in p for p in duong_dan))
        self.assertTrue(any("goiY" in p for p in duong_dan))

        # Mock Gemini sua toan bo chuoi thieu dau
        class _MockGeminiSuaDau:
            def tao_json(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
                # Tra ve ban da them dau cho tat ca duongDan tim thay
                kq: list[dict[str, str]] = []
                for v in vi_pham:
                    kq.append(
                        {
                            "duongDan": v["duongDan"],
                            "vanBanCoDau": "Đã khôi phục đầy đủ dấu tiếng Việt tự nhiên cho nội dung này!",
                        }
                    )
                return {"daSua": kq}

        kb_da_sua, ds_sua = tu_dong_sua_dau_tieng_viet(kb, gemini=_MockGeminiSuaDau())
        self.assertGreaterEqual(len(ds_sua), 6)
        self.assertEqual(kiem_tra_dau_tieng_viet(kb_da_sua), [])

    def test_v25_2_chan_dao_cu_thoi_tiet_lech_boi_canh_va_phong_sinh(self) -> None:
        nv_ids = ["cantor"]
        # 2a. Cam la_vang_gio trong giang_duong_dai_hoc & thoiTiet=la_roi trong phong kin
        c_giang_duong, _ = chuan_hoa_canh(
            {
                "id": "canh_010",
                "boCuc": "ke_chuyen",
                "boiCanh": "giang_duong_dai_hoc",
                "thoiTiet": "la_roi",
                "loiThoai": "Cantor đứng trên bục giảng đường trình bày chứng minh mới.",
                "vatTheXungQuanh": [
                    {"loai": "la_vang_gio", "soLuong": 8},
                    {"loai": "dong_ho_qua_lac", "x": 1680, "y": 220},
                ],
                "nhanVat": [{"id": "cantor", "x": 760, "y": 810}],
            },
            "canh_010",
            nv_ids,
        )
        self.assertEqual(c_giang_duong["thoiTiet"], "khong")
        self.assertNotIn("la_vang_gio", [v["loai"] for v in c_giang_duong.get("vatTheXungQuanh") or []])

        # 2b. Cam ngon_nen_den_dau trong khong_gian_vu_tru_toan
        c_vu_tru, _ = chuan_hoa_canh(
            {
                "id": "canh_011",
                "boCuc": "ke_chuyen",
                "boiCanh": "khong_gian_vu_tru_toan",
                "thoiTiet": "ban_dem",
                "loiThoai": "Giữa vũ trụ toán học bao la, từng tầng vô cực mở ra nối tiếp.",
                "vatTheXungQuanh": [{"loai": "ngon_nen_den_dau", "x": 420, "y": 500}],
                "nhanVat": [{"id": "cantor", "x": 760, "y": 810}],
            },
            "canh_011",
            nv_ids,
        )
        self.assertNotIn("ngon_nen_den_dau", [v["loai"] for v in c_vu_tru.get("vatTheXungQuanh") or []])

        # 2c. Cam nha_co_phong_sinh cho canh nguoi gia nhan giai thuong / cuoi doi
        c_giai_thuong, _ = chuan_hoa_canh(
            {
                "id": "canh_012",
                "boCuc": "ke_chuyen",
                "boiCanh": "nha_co_phong_sinh",
                "tieuDeNho": "Nhận huy chương Sylvester cuối đời",
                "loiThoai": "Năm 1904, Hội Hoàng gia London trao huy chương Sylvester vinh danh Cantor.",
                "nhanVat": [{"id": "cantor", "x": 760, "y": 810, "doTuoi": "gia"}],
            },
            "canh_012",
            nv_ids,
        )
        self.assertNotEqual(c_giai_thuong["boiCanh"], "nha_co_phong_sinh")

    def test_v25_3_cam_loi_binh_tren_toan_timeline_khong_cat_giua_tu_va_khong_lap_fallback(self) -> None:
        nv_ids = ["cantor"]
        # 3a. Goi loiBinhHaiHuoc bi go khoi giai_thich_toan & dong_thoi_gian
        c_toan, _ = chuan_hoa_canh(
            {
                "id": "canh_020",
                "boCuc": "giai_thich_toan",
                "loaiCanh": "giang_toan",
                "boiCanh": "giang_duong_dai_hoc",
                "loiThoai": "Ta lập bảng đường chéo để tạo ra một số thực hoàn toàn mới.",
                "loiBinhHaiHuoc": {"noiDung": "Góc nhìn này mới là chìa khóa của cả câu chuyện!"},
                "congThucLatex": [{"latex": "|\\mathbb{R}| > |\\mathbb{N}|", "nhan": "Lực lượng số thực"}],
                "minhHoaToan": {
                    "loai": "luoi_duong_cheo",
                    "tieuDe": "Lập luận đường chéo Cantor",
                    "thamSo": {
                        "nhanHang": ["r1", "r2", "r3"],
                        "hang": ["0.141...", "0.333...", "0.718..."],
                    },
                },
                "nhanVat": [{"id": "cantor", "x": 255, "y": 808}],
            },
            "canh_020",
            nv_ids,
        )
        self.assertNotIn("loiBinhHaiHuoc", c_toan)

        # 3b. cat_gon_theo_tu khong bao gio cat cut giua tu (nhu "...Leopol")
        mo_ta_dai = (
            "Cuộc tranh luận lịch sử giữa Georg Cantor và Leopold Kronecker về nền tảng tập hợp vô hạn "
            "khiến cả cộng đồng toán học châu Âu chia rẽ sâu sắc suốt nhiều thập kỷ"
        )
        ket_qua_cat = cat_gon_theo_tu(mo_ta_dai, 90)
        self.assertLessEqual(len(ket_qua_cat), 90)
        self.assertFalse(ket_qua_cat.endswith("Leopol"))
        # Moi tu (tru dau cham lung neu co) phai la tu nguyen ven trong mo_ta_dai
        phan_chu = ket_qua_cat.rstrip("….")
        self.assertTrue(mo_ta_dai.startswith(phan_chu))
        if len(phan_chu) < len(mo_ta_dai):
            self.assertEqual(mo_ta_dai[len(phan_chu)], " ")

        # 3c. kiem_dinh_nhip_ngat_thi_giac KHONG bom chuoi fallback cung lap 5-6 lan
        kb_thu = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=6)
        kb_sau, _ = kiem_dinh_nhip_ngat_thi_giac(kb_thu)
        toan_bo_json = json.dumps(kb_sau, ensure_ascii=False)
        self.assertNotIn("Góc nhìn này mới là chìa khóa của cả câu chuyện!", toan_bo_json)

    def test_v25_4_khu_nhan_doi_nhan_vat_va_tuong_tac_giu_dap_an_it_nhat_25_den_3_giay(self) -> None:
        nv_ids = ["cantor", "kronecker"]
        # 4a. Chong nhan doi cung 1 nhanVatId trong 1 canh
        c_trung, _ = chuan_hoa_canh(
            {
                "id": "canh_030",
                "boCuc": "ke_chuyen",
                "boiCanh": "thu_vien_co_dien",
                "loiThoai": "Cantor suy tư trước những trang bản thảo chứng minh mới.",
                "nhanVat": [
                    {"id": "cantor", "x": 640, "y": 810},
                    {"id": "cantor", "x": 1240, "y": 810},
                    {"id": "kronecker", "x": 1320, "y": 810},
                ],
            },
            "canh_030",
            nv_ids,
        )
        ids_sau = [nv["id"] for nv in c_trung["nhanVat"]]
        self.assertEqual(ids_sau, ["cantor", "kronecker"])

        # 4b. Canh tuong_tac_khan_gia trong chuanbi_dai.py luon giu du >= 2.5-3s hien "DAP AN CHINH XAC"
        kb_tt = {
            "tieuDe": "Thử thách vô cực",
            "chuDe": "So sánh hai tập vô hạn",
            "chuong": [
                {
                    "id": "hoi_1",
                    "tenChuong": "Hồi 1",
                    "phuDeHoi": "Thử thách tương tác về tập số chẵn và số tự nhiên",
                    "canh": [
                        {
                            "id": "canh_001",
                            "boCuc": "ke_chuyen",
                            "loaiCanh": "tuong_tac_khan_gia",
                            "boiCanh": "san_truong_co_dien",
                            "loiThoai": "Theo bạn tập số tự nhiên hay tập số chẵn có nhiều phần tử hơn?",
                            "cauHoiTuongTac": {
                                "cauHoi": "Tập nào nhiều phần tử hơn?",
                                "thoiGianDemNguocGiay": 3,
                                "batDauDemNguocFrame": 30,
                                "dapAn": "Hai tập có lực lượng bằng nhau!",
                            },
                            "nhanVat": [{"id": "cantor", "x": 420, "y": 810}],
                        }
                    ],
                }
            ],
        }
        # Gia lap audio ngan chi 4.0s (120 frame) -> tinh_toan_khung_hinh phai tu mo rong thoi luong
        kb_out, _ = tinh_toan_khung_hinh(kb_tt, {"canh_001": 4.0}, slug="cantor_test", fps=30)
        canh_out = kb_out["chuong"][0]["canh"][0]
        tong_frame = canh_out["denFrame"] - canh_out["tuFrame"]
        hien_tu = canh_out["cauHoiTuongTac"]["hienDapAnTuFrame"]
        so_frame_hien_dap_an = tong_frame - hien_tu
        self.assertGreaterEqual(
            so_frame_hien_dap_an,
            int(round(THOI_GIAN_HIEN_DAP_AN_TOI_THIEU_GIAY * 30)),
        )

    def test_v25_5_phu_de_hoi_rieng_biet_va_chong_lap_y_toan_tap(self) -> None:
        kb_lap = {
            "tieuDe": "Georg Cantor và những cấp độ vô cực",
            "chuDe": "Cuộc cách mạng lý thuyết tập hợp",
            "danhSachNhanVat": [{"id": "cantor", "ten": "Georg Cantor"}],
            "chuong": [
                {
                    "id": "hoi_1",
                    "tenChuong": "Hồi 1: Cú sốc ban đầu",
                    "phuDeHoi": "Câu mô tả dùng chung cho cả 3 hồi",
                    "canh": [
                        {
                            "id": "canh_001",
                            "boCuc": "mo_dau",
                            "boiCanh": "giang_duong_dai_hoc",
                            "tieuDeNho": "Khởi đầu nghịch lý",
                            "loiThoai": "Georg Cantor chứng minh rằng tập số thực có lực lượng lớn hơn hẳn tập số tự nhiên.",
                            "loiBinhHaiHuoc": {"noiDung": "Khán giả nghe xong lập tức choáng váng!"},
                            "nhanVat": [{"id": "cantor", "x": 760, "y": 810}],
                        }
                    ],
                },
                {
                    "id": "hoi_2",
                    "tenChuong": "Hồi 2: Đường chéo kỳ diệu",
                    "phuDeHoi": "Câu mô tả dùng chung cho cả 3 hồi",
                    "canh": [
                        {
                            "id": "canh_002",
                            "boCuc": "ke_chuyen",
                            "boiCanh": "thu_vien_co_dien",
                            "tieuDeNho": "Lặp lại câu chuyện",
                            "loiThoai": "Georg Cantor chứng minh rằng tập số thực có lực lượng lớn hơn hẳn tập số tự nhiên.",
                            "loiBinhHaiHuoc": {"noiDung": "Khán giả nghe xong lập tức choáng váng!"},
                            "nhanVat": [{"id": "cantor", "x": 760, "y": 810}],
                        }
                    ],
                },
            ],
        }
        vp = kiem_dinh_guardrail_kich_ban(kb_lap)
        loai_vp = {v["loai"] for v in vp}
        self.assertIn("thieu_hoac_trung_phu_de_hoi", loai_vp)
        self.assertIn("lap_giai_thoai_cau_noi", loai_vp)
        self.assertIn("lap_loi_binh_hai_huoc", loai_vp)

        # sua_loi_guardrail_cuc_bo phai tu tao phuDeHoi rieng biet va go loiBinhHaiHuoc trung
        kb_fix, _ = sua_loi_guardrail_cuc_bo(kb_lap)
        phu_de_cac_hoi = [ch["phuDeHoi"] for ch in kb_fix["chuong"]]
        self.assertEqual(len(set(phu_de_cac_hoi)), 2)
        self.assertNotIn("loiBinhHaiHuoc", kb_fix["chuong"][1]["canh"][0])


class TestTaoBoiCanhAIV30Offline(unittest.TestCase):
    """Unit test offline/mock cho module sinh boi canh minh hoa 2D & phan tich anh sang v3.0 (Buoc 1/4)."""

    @staticmethod
    def _tao_png_bytes(mau: tuple[int, int, int], kich_thuoc: tuple[int, int] = (320, 180)) -> bytes:
        import io
        from PIL import Image

        buf = io.BytesIO()
        Image.new("RGB", kich_thuoc, color=mau).save(buf, format="PNG")
        return buf.getvalue()

    def test_v30_prompt_khoa_style_bible_va_can_canh_vat_the(self) -> None:
        # 1. STYLE_BIBLE_BOI_CANH phai chua du cac chi dan khoa phong cach dong nhat
        for yeu_cau in (
            "2D hand-drawn graphic novel background illustration",
            "#1a1a1a",
            "flat cel-shading",
            "lower 30%",
            "ZERO people",
            "ZERO human figures",
            "ZERO text",
            "ZERO watermarks",
            "16:9 widescreen",
        ):
            self.assertIn(yeu_cau, STYLE_BIBLE_BOI_CANH)

        # 2. Moi trong 22 boi canh deu tao prompt khoa chat STYLE_BIBLE_BOI_CANH
        for bc in LOAI_BOI_CANH:
            p = tao_prompt_boi_canh(
                boi_canh=bc,
                thoi_tiet="hoang_hon",
                boi_canh_lich_su="Cambridge 1914",
            )
            self.assertIn(STYLE_BIBLE_BOI_CANH, p)
            self.assertIn("Cambridge 1914", p)

        # 3. Khung hinh can canh vat the khoa chat STYLE_BIBLE_CAN_CANH_VAT_THE
        for dc in ("ban_hoc_den_dau", "qua_dia_cau", "tau_thuy", "cuon_giay"):
            p_cc = tao_prompt_boi_canh(
                boi_canh="thu_vien_co_dien",
                thoi_tiet="ban_dem",
                loai_khung_hinh="can_canh_vat_the",
                dao_cu_chinh=dc,
            )
            self.assertIn(STYLE_BIBLE_CAN_CANH_VAT_THE, p_cc)
            self.assertIn("ZERO people", p_cc)
            self.assertIn("16:9 widescreen", p_cc)

        # Hash thay doi khi prompt hoac do phan giai doi
        h1 = bam_mo_ta_boi_canh("prompt A", "boi_canh", (1280, 720))
        h2 = bam_mo_ta_boi_canh("prompt A", "boi_canh", (1920, 1080))
        h3 = bam_mo_ta_boi_canh("prompt B", "boi_canh", (1280, 720))
        self.assertNotEqual(h1, h2)
        self.assertNotEqual(h1, h3)

    def test_v30_phan_tich_anh_sang_pillow_va_nen_jpeg_duoi_250kb(self) -> None:
        from PIL import Image, ImageDraw

        # 1. Nang am (vang sang)
        img_nang = Image.new("RGB", (320, 180), color=(245, 220, 145))
        as_nang = phan_tich_anh_sang_moi_truong(img_nang)
        self.assertEqual(as_nang["loaiAnhSang"], "nang_am")
        self.assertLess(as_nang["doToi"], 0.35)
        self.assertRegex(as_nang["mauAm"], r"^#[0-9A-F]{6}$")

        # 2. Anh nen (phong toi + vung anh nen am ap)
        img_nen = Image.new("RGB", (320, 180), color=(35, 22, 12))
        draw_nen = ImageDraw.Draw(img_nen)
        draw_nen.ellipse((110, 50, 210, 130), fill=(245, 160, 50))
        as_nen = phan_tich_anh_sang_moi_truong(img_nen)
        self.assertEqual(as_nen["loaiAnhSang"], "anh_nen")
        self.assertGreaterEqual(as_nen["doToi"], 0.58)

        # 3. Dem lanh (xanh toi)
        img_dem = Image.new("RGB", (320, 180), color=(18, 32, 78))
        as_dem = phan_tich_anh_sang_moi_truong(img_dem)
        self.assertEqual(as_dem["loaiAnhSang"], "dem_lanh")
        self.assertGreaterEqual(as_dem["doToi"], 0.7)

        # 4. Hoang hon (cam do chieu ta)
        img_hh = Image.new("RGB", (320, 180), color=(225, 115, 70))
        as_hh = phan_tich_anh_sang_moi_truong(img_hh)
        self.assertEqual(as_hh["loaiAnhSang"], "hoang_hon")
        self.assertTrue(0.28 <= as_hh["doToi"] < 0.65)

        # 5. Trung tinh (xam/trang can bang)
        img_tt = Image.new("RGB", (320, 180), color=(195, 200, 204))
        as_tt = phan_tich_anh_sang_moi_truong(img_tt)
        self.assertEqual(as_tt["loaiAnhSang"], "trung_tinh")

        for kq_as in (as_nang, as_nen, as_dem, as_hh, as_tt):
            self.assertIn(kq_as["loaiAnhSang"], LOAI_ANH_SANG_HOP_LE)
            self.assertTrue(0.0 <= kq_as["doToi"] <= 1.0)

        # 6. Kiem tra resize 1280x720 & 1920x1080 va dung luong JPEG < 250KB (ke ca anh nhieu phuc tap)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # Tao anh phuc tap nhieu chi tiet (ti le 4:3 -> tu cat 16:9 & resize)
            img_phuc_tap = Image.new("RGB", (800, 600))
            px = img_phuc_tap.load()
            for y in range(600):
                for x in range(800):
                    px[x, y] = ((x * 7 + y * 3) % 256, (x * 5 ^ y * 11) % 256, (x * 13 + y * 17) % 256)
            import io

            buf = io.BytesIO()
            img_phuc_tap.save(buf, format="PNG")
            raw_phuc_tap = buf.getvalue()

            f_720 = root / "test_720.jpg"
            meta_720 = luu_va_nen_anh_boi_canh(raw_phuc_tap, f_720, kich_thuoc=(1280, 720), chat_luong=86)
            self.assertEqual((meta_720["width"], meta_720["height"]), (1280, 720))
            self.assertLessEqual(f_720.stat().st_size, GIOI_HAN_DUNG_LUONG_KB * 1024)
            with Image.open(f_720) as chk:
                self.assertEqual(chk.size, (1280, 720))
                self.assertEqual(chk.format, "JPEG")

            f_1080 = root / "test_1080.jpg"
            meta_1080 = luu_va_nen_anh_boi_canh(raw_phuc_tap, f_1080, kich_thuoc=(1920, 1080), chat_luong=86)
            self.assertEqual((meta_1080["width"], meta_1080["height"]), (1920, 1080))
            self.assertLessEqual(f_1080.stat().st_size, GIOI_HAN_DUNG_LUONG_KB * 1024)

    def test_v30_xoay_key_fallback_generateContent_imagen_predict_va_cache(self) -> None:
        import base64

        png_nang_b64 = base64.b64encode(self._tao_png_bytes((240, 212, 138))).decode("ascii")
        png_dem_b64 = base64.b64encode(self._tao_png_bytes((20, 35, 82))).decode("ascii")

        # 1. Test lay_cau_hinh_anh_ai doc .env / env_override
        keys, models = lay_cau_hinh_anh_ai(
            duong_dan_env=Path("khong_ton_tai.env"),
            env_override={
                "GEMINI_API_KEYS": "k_img_1, k_img_2",
                "GEMINI_IMAGE_MODELS": "gemini-2.5-flash-image, imagen-3.0-generate-002",
            },
        )
        self.assertEqual(keys, ["k_img_1", "k_img_2"])
        self.assertEqual(models, ["gemini-2.5-flash-image", "imagen-3.0-generate-002"])

        _, models_mac_dinh = lay_cau_hinh_anh_ai(
            duong_dan_env=Path("khong_ton_tai.env"),
            env_override={"GEMINI_API_KEYS": "k1", "GEMINI_IMAGE_MODELS": ""},
        )
        self.assertEqual(models_mac_dinh, list(MAC_DINH_IMAGE_MODELS))

        # 2. Test xoay key 429/503 o generateContent -> chuyen sang Imagen predict khi model 1 het sach quota
        lich_su_goi: list[tuple[str, str]] = []

        def fake_http_imagen_fallback(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            lich_su_goi.append((url, api_key))
            if ":generateContent" in url:
                return 429, '{"error": {"status": "RESOURCE_EXHAUSTED"}}'
            if ":predict" in url and api_key == "k1":
                return 503, "Service Unavailable"
            if ":predict" in url and api_key == "k2":
                # Kiem tra payload Imagen chuan instances/parameters 16:9
                self.assertIn("instances", payload)
                self.assertEqual(payload["parameters"]["aspectRatio"], "16:9")
                return 200, json.dumps({"predictions": [{"bytesBase64Encoded": png_dem_b64}]})
            return 500, "Unexpected"

        trinh = TrinhTaoBoiCanhAI(
            api_keys=["k1", "k2"],
            image_models=["gemini-2.5-flash-image", "imagen-3.0-generate-002"],
            http_caller=fake_http_imagen_fallback,
            sleep_fn=lambda _: None,
        )
        with tempfile.TemporaryDirectory() as tmp:
            pub = Path(tmp) / "public"
            kq = trinh.tao_mot_boi_canh(
                slug="demo_imagen",
                ma_boi_canh="bc_01_dem",
                boi_canh="bau_troi_dem_vu_tru",
                thoi_tiet="ban_dem",
                thu_muc_public=pub,
            )
            self.assertEqual(kq["nguon"], "ai")
            self.assertEqual(kq["model"], "imagen-3.0-generate-002")
            self.assertEqual(kq["duongDanAnh"], "boi_canh/demo_imagen/bc_01_dem.jpg")
            self.assertTrue((pub / "boi_canh" / "demo_imagen" / "bc_01_dem.jpg").exists())
            self.assertEqual(kq["anhSangMoiTruong"]["loaiAnhSang"], "dem_lanh")
            # Model 1 thu het 2 key (429) -> chuyen sang model 2 :predict, key 1 gap 503 -> key 2 thanh cong
            self.assertEqual(len(lich_su_goi), 4)
            self.assertIn(":generateContent", lich_su_goi[0][0])
            self.assertIn(":predict", lich_su_goi[2][0])
            self.assertIn(":predict", lich_su_goi[3][0])

        # 3. Test generateContent tra inlineData + cache hash tren lan chay 2 (0 luot goi API)
        so_luot_api = {"n": 0}

        def fake_http_inline(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            so_luot_api["n"] += 1
            self.assertIn(":generateContent", url)
            self.assertIn("IMAGE", payload["generationConfig"]["responseModalities"])
            return (
                200,
                json.dumps(
                    {
                        "candidates": [
                            {
                                "content": {
                                    "parts": [
                                        {"inlineData": {"mimeType": "image/png", "data": png_nang_b64}}
                                    ]
                                }
                            }
                        ]
                    }
                ),
            )

        du_lieu_nho = {
            "tieuDe": "Câu chuyện Euler",
            "chuDe": "7 cây cầu Königsberg",
            "chuong": [
                {
                    "id": "chuong_1",
                    "tenChuong": "Hồi 1",
                    "canh": [
                        {
                            "id": "canh_001",
                            "boCuc": "mo_dau",
                            "boiCanh": "pho_co_chau_au",
                            "thoiTiet": "nang_dep",
                            "mayQuay": {"gocQuay": "toan_canh"},
                            "loiThoai": "Cảnh 1 toàn cảnh phố cổ.",
                            "nhanVat": [],
                        },
                        {
                            "id": "canh_002",
                            "boCuc": "doi_thoai",
                            "boiCanh": "pho_co_chau_au",
                            "thoiTiet": "nang_dep",
                            "mayQuay": {"gocQuay": "focus_trai"},
                            "loiThoai": "Cảnh 2 cùng phố cổ nhưng đổi góc quay focus trái.",
                            "nhanVat": [],
                        },
                        {
                            "id": "canh_003",
                            "boCuc": "ke_chuyen",
                            "boiCanh": "thu_vien_co_dien",
                            "thoiTiet": "ban_dem",
                            "mayQuay": {"gocQuay": "zoom_dao_cu"},
                            "daoCu": [{"loai": "qua_dia_cau", "x": 960, "y": 540}],
                            "loiThoai": "Cảnh 3 cận cảnh quả địa cầu.",
                            "nhanVat": [],
                        },
                    ],
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dl_out1, tk1 = sinh_boi_canh_cho_tap(
                slug="euler_cache",
                du_lieu=du_lieu_nho,
                thu_muc_du_lieu=root / "du_lieu",
                thu_muc_public=root / "public",
                api_keys=["key_ok"],
                image_models=["gemini-2.5-flash-image"],
                http_caller=fake_http_inline,
                sleep_fn=lambda _: None,
            )
            # 3 canh -> chi sinh 2 boi canh doc ban (canh_001 & canh_002 tai su dung chung 1 anh, canh_003 la can canh vat the)
            self.assertEqual(tk1["tongBoiCanhDocBan"], 2)
            self.assertEqual(tk1["soSinhMoi"], 2)
            self.assertEqual(so_luot_api["n"], 2)
            c1, c2, c3 = dl_out1["chuong"][0]["canh"]
            self.assertEqual(c1["anhBoiCanh"], c2["anhBoiCanh"])
            self.assertNotEqual(c1["anhBoiCanh"], c3["anhBoiCanh"])
            self.assertEqual(c1["anhSangMoiTruong"]["loaiAnhSang"], "nang_am")

            # Lan chay 2: hit cache 100%, so_luot_api KHONG tang!
            dl_out2, tk2 = sinh_boi_canh_cho_tap(
                slug="euler_cache",
                du_lieu=du_lieu_nho,
                thu_muc_du_lieu=root / "du_lieu",
                thu_muc_public=root / "public",
                api_keys=["key_ok"],
                image_models=["gemini-2.5-flash-image"],
                http_caller=fake_http_inline,
                sleep_fn=lambda _: None,
            )
            self.assertEqual(so_luot_api["n"], 2)
            self.assertEqual(tk2["soDungCache"], 2)
            self.assertEqual(tk2["soSinhMoi"], 0)
            self.assertEqual(dl_out2["chuong"][0]["canh"][0]["anhBoiCanh"], c1["anhBoiCanh"])

    def test_v30_fallback_an_toan_khi_offline_hoac_het_quota(self) -> None:
        du_lieu_mini = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=1)  # 6 canh
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # 1. Che do offline/mock -> khong goi HTTP, tra anhBoiCanh=None & anhSangMoiTruong an toan
            dl_off, tk_off = sinh_boi_canh_cho_tap(
                slug="test_offline_bg",
                du_lieu=du_lieu_mini,
                thu_muc_du_lieu=root / "du_lieu",
                thu_muc_public=root / "public",
                che_do_offline=True,
                api_keys=["k1"],
                http_caller=lambda *a, **kw: (_ for _ in ()).throw(AssertionError("Khong duoc goi API khi offline!")),
            )
            self.assertEqual(tk_off["soCanhCoAnhAi"], 0)
            self.assertEqual(tk_off["soFallbackSvg"], tk_off["tongBoiCanhDocBan"])
            for ch in dl_off["chuong"]:
                for c in ch["canh"]:
                    self.assertIsNone(c["anhBoiCanh"])
                    self.assertIn(c["anhSangMoiTruong"]["loaiAnhSang"], LOAI_ANH_SANG_HOP_LE)

            # 2. Toan bo API key & model bi 429/503 -> KHONG crash, fallback duongDanAnh=None
            def always_429(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
                return 429, '{"error": {"status": "RESOURCE_EXHAUSTED"}}'

            dl_err, tk_err = sinh_boi_canh_cho_tap(
                slug="test_quota_bg",
                du_lieu=du_lieu_mini,
                thu_muc_du_lieu=root / "du_lieu",
                thu_muc_public=root / "public",
                api_keys=["k1", "k2"],
                image_models=["gemini-2.5-flash-image", "imagen-3.0-generate-002"],
                http_caller=always_429,
                sleep_fn=lambda _: None,
            )
            self.assertEqual(tk_err["soCanhCoAnhAi"], 0)
            self.assertEqual(tk_err["soFallbackSvg"], tk_err["tongBoiCanhDocBan"])
            self.assertTrue(all(c["anhBoiCanh"] is None for ch in dl_err["chuong"] for c in ch["canh"]))

    def test_v30_ke_hoach_14_den_20_boi_canh_tich_hop_chuanbi_dai_va_workflow(self) -> None:
        import base64

        # 1. Tap 6 hoi x 18 canh = 108 canh voi nhieu dia diem + goc quay -> gon trong 14..20 boi canh doc ban
        kb_lon = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=18)
        ds_bc_mau = [
            "bo_bien_hy_lap",
            "quang_truong_hy_lap",
            "thu_vien_co_dien",
            "lop_hoc_bang_xanh",
            "san_truong_co_dien",
            "cang_bien_tau_thuy",
            "phong_tro_bep_lua",
            "bau_troi_dem_vu_tru",
        ]
        ds_tt_mau = ["nang_dep", "hoang_hon", "ban_dem", "nang_dep"]
        for idx_ch, ch in enumerate(kb_lon["chuong"]):
            for idx_c, canh in enumerate(ch["canh"]):
                canh["boiCanh"] = ds_bc_mau[(idx_ch + idx_c) % len(ds_bc_mau)]
                canh["thoiTiet"] = ds_tt_mau[(idx_ch + idx_c) % len(ds_tt_mau)]
                if idx_c == 3:
                    canh["mayQuay"] = {"gocQuay": "zoom_dao_cu"}
                    canh["daoCu"] = [{"loai": "cuon_giay", "x": 960, "y": 540}]

        ke_hoach, canh_to_ma = lap_ke_hoach_boi_canh_tap(kb_lon, so_luong_toi_da=20)
        self.assertGreaterEqual(len(ke_hoach), 14)
        self.assertLessEqual(len(ke_hoach), 20)
        self.assertEqual(len(canh_to_ma), 108)
        self.assertTrue(any(m["loaiKhungHinh"] == "can_canh_vat_the" for m in ke_hoach))

        # 2. Tich hop cuoi pha chuanbi_dai.py: bat anh AI (mock HTTP) vs co --tat-anh-ai
        parser_cb = tao_parser_chuanbi_dai()
        args_tat = parser_cb.parse_args(["--slug", "demo_v3", "--tat-anh-ai"])
        self.assertTrue(args_tat.tat_anh_ai)
        args_bat = parser_cb.parse_args(["--slug", "demo_v3"])
        self.assertFalse(args_bat.tat_anh_ai)

        png_b64 = base64.b64encode(self._tao_png_bytes((235, 200, 130))).decode("ascii")

        def fake_img_http(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> tuple[int, str]:
            return (
                200,
                json.dumps(
                    {
                        "candidates": [
                            {"content": {"parts": [{"inlineData": {"mimeType": "image/png", "data": png_b64}}]}}
                        ]
                    }
                ),
            )

        kb_ngan = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=1)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dl_dir = root / "du_lieu"
            pub_dir = root / "public"
            out_dir = root / "out"
            (dl_dir / "v3_demo").mkdir(parents=True)
            (dl_dir / "v3_demo" / "nhap_kich_ban.json").write_text(
                json.dumps(kb_ngan, ensure_ascii=False), encoding="utf-8"
            )

            # 2a. Bat anh AI trong chuan_bi_audio_va_du_lieu_render
            f_render, tk = chuan_bi_audio_va_du_lieu_render(
                slug="v3_demo",
                thu_muc_du_lieu=dl_dir,
                thu_muc_public=pub_dir,
                thu_muc_out=out_dir,
                env_override={"GEMINI_API_KEYS": "k_v3", "GEMINI_IMAGE_MODELS": "gemini-2.5-flash-image"},
                tts_generator=lambda cid, txt, p: p.write_bytes(b"FAKE_MP3"),
                duration_prober=lambda _: 4.0,
                rms_extractor=lambda p, f: [0.4] * 120,
                tat_anh_ai=False,
                image_http_caller=fake_img_http,
            )
            self.assertGreater(tk["boiCanhAi"]["tongBoiCanhDocBan"], 0)
            self.assertEqual(tk["boiCanhAi"]["soCanhCoAnhAi"], 6)
            render_json = json.loads(f_render.read_text(encoding="utf-8"))
            c0 = render_json["chuong"][0]["canh"][0]
            self.assertTrue(str(c0["anhBoiCanh"]).startswith("boi_canh/v3_demo/"))
            self.assertTrue((pub_dir / c0["anhBoiCanh"]).exists())
            self.assertIn(c0["anhSangMoiTruong"]["loaiAnhSang"], LOAI_ANH_SANG_HOP_LE)

            # 2b. Tat anh AI (--tat-anh-ai)
            _, tk_tat = chuan_bi_audio_va_du_lieu_render(
                slug="v3_demo",
                thu_muc_du_lieu=dl_dir,
                thu_muc_public=pub_dir,
                thu_muc_out=out_dir,
                tts_generator=lambda cid, txt, p: p.write_bytes(b"FAKE_MP3"),
                duration_prober=lambda _: 4.0,
                rms_extractor=lambda p, f: [0.4] * 120,
                tat_anh_ai=True,
            )
            self.assertEqual(tk_tat["boiCanhAi"]["trangThai"], "da_tat")

        # 3. Kiem tra workflow YAML goi public/boi_canh/<slug>/ & .gitignore chan public/boi_canh/
        wf_text = (GOC_DU_AN / ".github" / "workflows" / "tu-dong-video10p.yml").read_text(encoding="utf-8")
        self.assertIn("public/boi_canh/${{ steps.xuat_output.outputs.slug }}/", wf_text)
        self.assertIn("GEMINI_IMAGE_MODELS", wf_text)
        gi_text = (GOC_DU_AN / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("public/boi_canh/", gi_text)


class TestNangCapV30Buoc4Offline(unittest.TestCase):
    """Kiem tra toan dien Buoc 4/4 (v3.0): Dao dien AI v3.0, danhSachBoiCanhAI, pre-TTS guard, nhip hai & mau_v3_dien_anh.json."""

    def test_v30_buoc4_enum_ho_so_tao_hinh_va_danh_sach_boi_canh_ai(self) -> None:
        from scripts.pipeline.tao_kich_ban_10p import (
            GOC_QUAY_CAMERA,
            KIEU_BONG_BONG_CHAT,
            LOAI_CO_RAU,
            LOAI_HIEU_UNG_HOAT_HINH,
            LOAI_KIEU_TOC,
            LOAI_TRANG_PHUC,
            TAM_KHUNG_NHAN_VAT,
            chuan_hoa_danh_sach_boi_canh_ai,
            chuan_hoa_danh_sach_nhan_vat,
        )

        # 1. Xac minh enum v3.0 dong bo 100% voi src/kieu_dai.ts
        for gq in ("can_mat_trai", "can_mat_phai", "can_mat_kich_tinh", "dao_goc_can_mat"):
            self.assertIn(gq, GOC_QUAY_CAMERA)
        for hu in ("mo_hoi_lon", "khoi_boc_tai", "mat_xoan_oc", "cham_hoi_nay", "tia_toc_do", "bong_den_y_tuong"):
            self.assertIn(hu, LOAI_HIEU_UNG_HOAT_HINH)
        self.assertEqual(len(LOAI_TRANG_PHUC), 7)
        self.assertEqual(len(LOAI_KIEU_TOC), 7)
        self.assertEqual(len(LOAI_CO_RAU), 4)
        self.assertEqual(len(TAM_KHUNG_NHAN_VAT), 3)
        self.assertEqual(len(KIEU_BONG_BONG_CHAT), 4)

        # 2. Ho so tao hinh co dinh xuyen suot tap
        nvs = chuan_hoa_danh_sach_nhan_vat(
            [
                {
                    "id": "euler",
                    "ten": "Leonhard Euler",
                    "mauChuDao": "#1D4ED8",
                    "trangPhuc": "ao_choang_hoc_gia",
                    "kieuToc": "mu_noi",
                    "coRau": "khong",
                    "mauAo": "#1E40AF",
                },
                {"id": "thi_truong", "ten": "Thị Trưởng"},
            ]
        )
        self.assertEqual(nvs[0]["trangPhuc"], "ao_choang_hoc_gia")
        self.assertEqual(nvs[0]["kieuToc"], "mu_noi")
        self.assertEqual(nvs[0]["mauAo"], "#1E40AF")
        self.assertIn(nvs[1]["trangPhuc"], LOAI_TRANG_PHUC)
        self.assertIn(nvs[1]["kieuToc"], LOAI_KIEU_TOC)

        # 3. chuan_hoa_danh_sach_boi_canh_ai & anh xa thang sang tao_boi_canh_ai.lap_ke_hoach_boi_canh_tap
        ds_ai = chuan_hoa_danh_sach_boi_canh_ai(
            [
                {
                    "maBoiCanhAI": "bc_01_giang_duong",
                    "loaiKhungHinh": "boi_canh",
                    "boiCanh": "giang_duong_dai_hoc",
                    "thoiTiet": "nang_dep",
                    "moTaTiengAnh": "18th century European lecture hall with tall arched windows, no people",
                },
                {
                    "maBoiCanhAI": "cc_01_ban_do",
                    "loaiKhungHinh": "can_canh_vat_the",
                    "boiCanh": "thu_vien_co_dien",
                    "thoiTiet": "ban_dem",
                    "daoCuChinh": "cuon_giay",
                    "moTaTiengAnh": "Close-up antique map of seven bridges with candle on wooden desk, no people",
                },
            ]
        )
        self.assertEqual(len(ds_ai), 2)

        raw_kb = {
            "tieuDe": "Leonhard Euler & 7 Cây Cầu",
            "chuDe": "Lý thuyết đồ thị",
            "danhSachNhanVat": nvs,
            "danhSachBoiCanhAI": ds_ai,
            "chuong": [
                {
                    "id": "chuong_1",
                    "tenChuong": "1. Khởi đầu",
                    "phuDeHoi": "Mở màn câu chuyện bảy cây cầu lịch sử",
                    "canh": [
                        {
                            "boCuc": "doi_thoai",
                            "loaiCanh": "doi_thoai",
                            "boiCanh": "giang_duong_dai_hoc",
                            "maBoiCanhAI": "bc_01_giang_duong",
                            "loiThoai": "Chào ngài, bảy cây cầu này đi thế nào? Cứ đếm bậc đỉnh là ra ngay!",
                            "luotThoai": [
                                {"nhanVatId": "thi_truong", "noiDung": "Chào ngài, bảy cây cầu này đi thế nào?", "kieuBongBong": "quat_thao"},
                                {"nhanVatId": "euler", "noiDung": "Cứ đếm bậc đỉnh là ra ngay!", "kieuBongBong": "ca_khia"},
                            ],
                            "nhanVat": [
                                {"id": "thi_truong", "x": 640, "y": 810, "tamKhung": "ban_than"},
                                {"id": "euler", "x": 1280, "y": 810, "tamKhung": "can_mat"},
                            ],
                            "hieuUngHoatHinh": [
                                {"loai": "bong_den_y_tuong", "x": 1280, "y": 400},
                            ],
                        },
                        {
                            "boCuc": "ke_chuyen",
                            "boiCanh": "thu_vien_co_dien",
                            "maBoiCanhAI": "cc_01_ban_do",
                            "laKhungTranhDacTa": True,
                            "mayQuay": {"gocQuay": "can_mat_kich_tinh", "doPhong": 2.2},
                            "loiThoai": "Trên tấm bản đồ cổ, bảy cây cầu hiện lên như một mê cung hóc búa.",
                            "nhanVat": [{"id": "euler", "x": 960, "y": 810}],
                        },
                    ],
                }
            ],
        }
        kb_sach, _ = chuan_hoa_toan_bo_kich_ban(raw_kb)
        c1, c2 = kb_sach["chuong"][0]["canh"]
        # Tu dong gan dao_goc_can_mat & bao toan kieuBongBong, doPhong=2.2
        self.assertEqual(c1["mayQuay"]["gocQuay"], "dao_goc_can_mat")
        self.assertTrue(c1["mayQuay"]["tuDongFocusNguoiNoi"])
        self.assertEqual(c1["luotThoai"][0]["kieuBongBong"], "quat_thao")
        self.assertEqual(c1["luotThoai"][1]["kieuBongBong"], "ca_khia")
        self.assertEqual(c2["mayQuay"]["doPhong"], 2.2)

        ke_hoach, canh_to_ma = lap_ke_hoach_boi_canh_tap(kb_sach)
        self.assertEqual(canh_to_ma["canh_001"], "bc_01_giang_duong")
        self.assertEqual(canh_to_ma["canh_002"], "cc_01_ban_do")
        by_ma = {m["maBoiCanh"]: m for m in ke_hoach}
        self.assertIn("18th century European lecture hall", by_ma["bc_01_giang_duong"]["moTaBoSung"])
        self.assertEqual(by_ma["cc_01_ban_do"]["loaiKhungHinh"], "can_canh_vat_the")

    def test_v30_buoc4_pre_tts_guard_nhip_hai_va_chong_ro_ri_1729(self) -> None:
        from scripts.pipeline.chuanbi_dai import (
            HO_SO_GIONG_NHAN_VAT,
            NGHI_GIUA_LUOT_THOAI_GIAY,
            tinh_moc_va_rms_luot_thoai,
            tinh_nghi_nhip_hai_luot_thoai,
        )

        # 1. Khoang nghi nhip hai nam chuan trong 0.25s..0.40s & phan biet giong
        self.assertGreaterEqual(NGHI_GIUA_LUOT_THOAI_GIAY, 0.25)
        self.assertLessEqual(NGHI_GIUA_LUOT_THOAI_GIAY, 0.40)
        nghi_thuong = tinh_nghi_nhip_hai_luot_thoai({"kieuBongBong": "thuong", "bieuCam": "vui_tuoi"})
        nghi_punch = tinh_nghi_nhip_hai_luot_thoai({"kieuBongBong": "ca_khia", "bieuCam": "tinh_quai"})
        self.assertGreaterEqual(nghi_thuong, 0.25)
        self.assertLessEqual(nghi_punch, 0.40)
        self.assertGreater(nghi_punch, nghi_thuong)

        luot_res, _, _ = tinh_moc_va_rms_luot_thoai(
            [
                {"nhanVatId": "a", "noiDung": "Câu mở đầu"},
                {"nhanVatId": "b", "noiDung": "Cà khịa ngay!", "kieuBongBong": "ca_khia"},
            ],
            [1.0, 1.0],
            [[0.5] * 30, [0.8] * 30],
            fps=30,
            dung_nhip_hai_dong=True,
        )
        self.assertEqual(luot_res[1]["batDauFrame"], 30 + int(round(nghi_punch * 30)))

        # Tat ca ho so giong phan biet ro rang voi nhau va voi nguoi dan (+0%, +0Hz)
        giong_set = {(h["voice"], h["rate"], h["pitch"]) for h in HO_SO_GIONG_NHAN_VAT}
        self.assertEqual(len(giong_set), len(HO_SO_GIONG_NHAN_VAT))
        self.assertNotIn(("vi-VN-NamMinhNeural", "+0%", "+0Hz"), giong_set)

        # 2. Guardrail chan bien so '1729' mac dinh trong tap khong phai Ramanujan
        kb_euler = _tao_kich_ban_gia_6_hoi(so_canh_moi_hoi=2)
        kb_euler["tieuDe"] = "Leonhard Euler & 7 Cây Cầu"
        kb_euler["chuDe"] = "Lý thuyết đồ thị"
        kb_euler["chuong"][0]["canh"][0]["bienSoXe"] = "1729"
        kb_euler["chuong"][0]["canh"][0]["daoCu"] = [{"loai": "bien_so_xe", "x": 960, "y": 620, "bienSoXe": "1729"}]
        vp = kiem_dinh_guardrail_kich_ban(kb_euler)
        self.assertTrue(any(v["loai"] == "bien_so_1729_mac_dinh" for v in vp))
        kb_fixed, _ = sua_loi_guardrail_cuc_bo(kb_euler)
        self.assertNotIn("bienSoXe", kb_fixed["chuong"][0]["canh"][0])
        self.assertNotIn("bienSoXe", kb_fixed["chuong"][0]["canh"][0]["daoCu"][0])

        # 3. Guardrail kiem_tra_dau_tieng_viet() chay TRUOC Edge TTS trong chuanbi_dai.py
        class _FakeGeminiFixDau:
            def tao_json(self, **kwargs: Any) -> dict[str, Any]:
                return {
                    "daSua": [
                        {
                            "duongDan": "chuong[0].canh[0].loiThoai",
                            "vanBanCoDau": "Đây là câu thoại lịch sử Toán học đã được khôi phục dấu đầy đủ.",
                        }
                    ]
                }

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dl_dir, pub_dir, out_dir = root / "du_lieu", root / "public", root / "out"
            (dl_dir / "test_dau").mkdir(parents=True)
            kb_thieu_dau = {
                "tieuDe": "Câu Chuyện Euler",
                "chuDe": "Lịch sử Toán học",
                "danhSachNhanVat": [{"id": "euler", "ten": "Euler", "mauThan": "#1E293B", "mauChuDao": "#1D4ED8", "mauDa": "#FFFDF7", "phuKien": "khong"}],
                "chuong": [
                    {
                        "id": "chuong_1",
                        "tenChuong": "1. Khởi đầu",
                        "phuDeHoi": "Hồi mở màn đầy thú vị",
                        "canh": [
                            {
                                "id": "canh_001",
                                "boCuc": "ke_chuyen",
                                "boiCanh": "thu_vien_co_dien",
                                "thoiTiet": "khong",
                                "tuFrame": 0,
                                "denFrame": 120,
                                "loiThoai": "Day la cau thoai lich su Toan hoc khong co dau tieng Viet nao ca.",
                                "nhanVat": [{"id": "euler", "x": 960, "y": 810, "huong": "phai", "hanhDong": "dung_tho", "bieuCam": "vui_tuoi"}],
                            },
                            {
                                "id": "canh_002",
                                "boCuc": "ke_chuyen",
                                "loaiCanh": "tuong_tac_khan_gia",
                                "boiCanh": "giang_duong_dai_hoc",
                                "thoiTiet": "khong",
                                "tuFrame": 120,
                                "denFrame": 240,
                                "loiThoai": "Theo bạn đáp án đúng cho câu đố bảy cây cầu là gì?",
                                "cauHoiTuongTac": {
                                    "cauHoi": "Cần thêm bao nhiêu cây cầu?",
                                    "thoiGianDemNguocGiay": 3,
                                    "batDauDemNguocFrame": 15,
                                    "dapAn": "Chỉ cần thêm đúng 1 cây cầu!",
                                },
                                "nhanVat": [{"id": "euler", "x": 960, "y": 810, "huong": "phai", "hanhDong": "quay_nhin_khan_gia", "bieuCam": "tinh_quai"}],
                            },
                        ],
                    }
                ],
            }
            (dl_dir / "test_dau" / "nhap_kich_ban.json").write_text(
                json.dumps(kb_thieu_dau, ensure_ascii=False), encoding="utf-8"
            )
            da_doc_tts: list[str] = []

            def fake_tts_rec(cid: str, txt: str, p: Path) -> None:
                da_doc_tts.append(txt)
                p.write_bytes(b"MP3")

            f_render, tk = chuan_bi_audio_va_du_lieu_render(
                slug="test_dau",
                thu_muc_du_lieu=dl_dir,
                thu_muc_public=pub_dir,
                thu_muc_out=out_dir,
                tts_generator=fake_tts_rec,
                duration_prober=lambda _: 2.0,
                rms_extractor=lambda p, f: [0.5] * 60,
                gemini_client=_FakeGeminiFixDau(),
                tu_sua_dau_tieng_viet=True,
                tat_anh_ai=True,
            )
            self.assertEqual(tk["soChuoiThieuDauPhatHien"], 1)
            self.assertEqual(tk["soChuoiDaSuaDau"], 1)
            # Edge TTS phai nhan ban DA CO DAU DAY DU
            self.assertIn("khôi phục dấu đầy đủ", da_doc_tts[0])

            # Canh tuong_tac_khan_gia phai giu hop dap an >= 2.5s (75 frames) sau khi dem nguoc ve 0
            render_obj = json.loads(f_render.read_text(encoding="utf-8"))
            c_tt = render_obj["chuong"][0]["canh"][1]
            tong_f_tt = c_tt["denFrame"] - c_tt["tuFrame"]
            hien_f = c_tt["cauHoiTuongTac"]["hienDapAnTuFrame"]
            self.assertGreaterEqual((tong_f_tt - hien_f) / 30.0, 2.5)

    def test_v30_buoc4_mau_v3_dien_anh_dat_toan_bo_guardrail(self) -> None:
        duong_dan = GOC_DU_AN / "du_lieu" / "mau_v3_dien_anh.json"
        self.assertTrue(duong_dan.exists(), "Thieu du_lieu/mau_v3_dien_anh.json")
        du_lieu = json.loads(duong_dan.read_text(encoding="utf-8"))

        self.assertEqual(kiem_dinh_guardrail_kich_ban(du_lieu), [])
        self.assertEqual(kiem_dinh_schema_du_lieu_canh(du_lieu), [])
        self.assertEqual(kiem_tra_lien_mach_khung_hinh(du_lieu), [])
        self.assertEqual(kiem_tra_dau_tieng_viet(du_lieu), [])
        self.assertEqual(kiem_tra_ro_ri_pythagoras(du_lieu), [])

        tat_ca_canh = [c for ch in du_lieu["chuong"] for c in ch["canh"]]
        goc_quays = {str((c.get("mayQuay") or {}).get("gocQuay") or "") for c in tat_ca_canh}
        for gq in ("can_mat_trai", "can_mat_phai", "can_mat_kich_tinh", "dao_goc_can_mat"):
            self.assertIn(gq, goc_quays)

        kieu_bb = {
            str(lt.get("kieuBongBong") or "")
            for c in tat_ca_canh
            for lt in (c.get("luotThoai") or [])
        }
        for bb in ("thuong", "quat_thao", "suy_nghi", "ca_khia"):
            self.assertIn(bb, kieu_bb)

        vfx_loai = {
            str(hu.get("loai") or "")
            for c in tat_ca_canh
            for hu in (c.get("hieuUngHoatHinh") or [])
        }
        for fx in ("mo_hoi_lon", "khoi_boc_tai", "mat_xoan_oc", "cham_hoi_nay", "tia_toc_do", "bong_den_y_tuong"):
            self.assertIn(fx, vfx_loai)

        # Kiem tra canh tuong_tac_khan_gia giu dap an >= 2.5s
        c_tt = next(c for c in tat_ca_canh if c.get("loaiCanh") == "tuong_tac_khan_gia")
        tong_f = c_tt["denFrame"] - c_tt["tuFrame"]
        self.assertGreaterEqual((tong_f - c_tt["cauHoiTuongTac"]["hienDapAnTuFrame"]) / 30.0, 2.5)


class TestDangYouTubeOffline(unittest.TestCase):
    """Bo unit test mock offline cho dang_youtube.py va lay_refresh_token_youtube.py (thuan stdlib)."""

    def test_thieu_secret_thoat_an_toan_ma_0(self) -> None:
        import io
        from unittest import mock

        with tempfile.TemporaryDirectory() as tmp:
            env_rong = Path(tmp) / ".env.rong"
            env_rong.write_text("# Khong co bien YouTube\n", encoding="utf-8")

            # 1. Thieu toan bo 3 bien
            cfg = lay_cau_hinh_oauth_youtube(
                duong_dan_env=env_rong,
                env_override={
                    "YOUTUBE_CLIENT_ID": "",
                    "YOUTUBE_CLIENT_SECRET": "",
                    "YOUTUBE_REFRESH_TOKEN": "",
                },
            )
            self.assertEqual(
                danh_sach_bien_thieu(cfg),
                ["YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"],
            )

            # 2. Chi thieu 1 bien (YOUTUBE_REFRESH_TOKEN) -> dang_video_len_youtube tra ve thieu_cau_hinh
            kq = dang_video_len_youtube(
                slug="tap_demo",
                duong_dan_env=env_rong,
                env_override={
                    "YOUTUBE_CLIENT_ID": "cid_demo",
                    "YOUTUBE_CLIENT_SECRET": "csec_demo",
                    "YOUTUBE_REFRESH_TOKEN": "",
                },
            )
            self.assertEqual(kq["trangThai"], "thieu_cau_hinh")
            self.assertEqual(kq["bienThieu"], ["YOUTUBE_REFRESH_TOKEN"])
            self.assertIn("lay_refresh_token_youtube.py", kq["huongDan"])

            # 3. Chay CLI main() khi thieu secret -> in huong dan va thoat ma 0 an toan (KHONG fail workflow)
            buf = io.StringIO()
            env_sach = {
                k: v
                for k, v in __import__("os").environ.items()
                if k not in ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN")
            }
            with mock.patch.dict("os.environ", env_sach, clear=True):
                with mock.patch("sys.stdout", buf):
                    rc = main_dang_youtube(["--slug", "tap_demo", "--env", str(env_rong)])
            self.assertEqual(rc, 0)
            out_txt = buf.getvalue()
            self.assertIn("YOUTUBE_CLIENT_ID", out_txt)
            self.assertIn("lay_refresh_token_youtube.py", out_txt)

    def test_doi_refresh_token_lay_access_token_va_loi_oauth(self) -> None:
        import urllib.parse

        da_goi: list[tuple[str, str, dict[str, str], bytes | None]] = []

        def fake_http_ok(
            method: str,
            url: str,
            headers: dict[str, str],
            data: bytes | None,
            timeout: int,
        ) -> tuple[int, dict[str, str], bytes]:
            da_goi.append((method, url, headers, data))
            body = json.dumps(
                {
                    "access_token": "mock_access_token_xyz",
                    "expires_in": 3599,
                    "token_type": "Bearer",
                    "scope": "https://www.googleapis.com/auth/youtube.upload",
                }
            ).encode("utf-8")
            return 200, {"content-type": "application/json"}, body

        kq = doi_refresh_token_lay_access_token(
            client_id="cid_123",
            client_secret="csec_456",
            refresh_token="rtok_789",
            http_caller=fake_http_ok,
        )
        self.assertEqual(kq["access_token"], "mock_access_token_xyz")
        self.assertEqual(kq["expires_in"], 3599)
        self.assertEqual(len(da_goi), 1)
        method, url, _, data = da_goi[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "https://oauth2.googleapis.com/token")
        form = urllib.parse.parse_qs((data or b"").decode("utf-8"))
        self.assertEqual(form["client_id"], ["cid_123"])
        self.assertEqual(form["client_secret"], ["csec_456"])
        self.assertEqual(form["refresh_token"], ["rtok_789"])
        self.assertEqual(form["grant_type"], ["refresh_token"])

        # Truong hop invalid_grant -> nem LoiDangYouTube kem goi y chay lay_refresh_token_youtube.py
        def fake_http_err(
            method: str, url: str, headers: dict[str, str], data: bytes | None, timeout: int
        ) -> tuple[int, dict[str, str], bytes]:
            return 400, {}, b'{"error": "invalid_grant", "error_description": "Token has been expired or revoked."}'

        with self.assertRaises(LoiDangYouTube) as ctx:
            doi_refresh_token_lay_access_token("cid", "csec", "rtok_cu", http_caller=fake_http_err)
        self.assertIn("lay_refresh_token_youtube.py", str(ctx.exception))

    def test_tinh_thoi_diem_cong_khai_vn_chuan_plus_0700(self) -> None:
        import datetime

        # 1. Chay luc 00:00 UTC = 07:00 sang gio VN -> cach_ngay=0 ra 19:30 cung ngay +07:00
        bay_gio_utc = datetime.datetime(2026, 11, 26, 0, 0, 0, tzinfo=datetime.timezone.utc)
        p0 = tinh_thoi_diem_cong_khai_vn("19:30", cach_ngay=0, bay_gio=bay_gio_utc)
        self.assertEqual(p0, "2026-11-26T19:30:00+07:00")

        # 2. cach_ngay=1 ra 19:30 ngay hom sau +07:00
        p1 = tinh_thoi_diem_cong_khai_vn("19:30", cach_ngay=1, bay_gio=bay_gio_utc)
        self.assertEqual(p1, "2026-11-27T19:30:00+07:00")

        # 3. Neu bay gio la 21:00 toi VN ma cach_ngay=0 -> tu dong day sang 19:30 ngay mai (tranh loi qua khu)
        bay_gio_toi = datetime.datetime(2026, 11, 26, 21, 0, 0, tzinfo=MUI_GIO_VN)
        p_day = tinh_thoi_diem_cong_khai_vn("19:30", cach_ngay=0, bay_gio=bay_gio_toi)
        self.assertEqual(p_day, "2026-11-27T19:30:00+07:00")

        # 4. Dinh dang gio khong hop le -> ValueError
        with self.assertRaises(ValueError):
            tinh_thoi_diem_cong_khai_vn("25:99", cach_ngay=0, bay_gio=bay_gio_utc)

    def test_resumable_upload_multi_chunk_thumbnail_srt_va_bo_nho(self) -> None:
        import datetime

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slug = "euler_bay_cay_cau_test"
            out_dir = root / "out"
            dl_dir = root / "du_lieu"
            (out_dir / slug).mkdir(parents=True)
            (dl_dir / slug).mkdir(parents=True)
            bo_nho_path = dl_dir / "bo_nho_hoc_hoi.json"

            # Khoi tao bo_nho_hoc_hoi.json co san tap trong chu_de_da_lam (nhu sau --hoan-tat-tu-meta)
            bn_init = tai_bo_nho(bo_nho_path)
            ghi_nhan_tap_hoan_thanh(
                bn_init,
                slug=slug,
                tieu_de="Leonhard Euler & 7 Cây Cầu Königsberg",
                nhan_vat_chinh="Leonhard Euler",
                tom_tat_1_cau="Câu chuyện ra đời Lý thuyết Đồ thị.",
                thoi_luong_giay=640.0,
            )
            luu_bo_nho(bn_init, bo_nho_path)

            # Tao du_lieu_render.json & chapters_va_mo_ta.txt
            du_lieu_render = {
                "tieuDe": "Leonhard Euler & 7 Cây Cầu Königsberg",
                "chuDe": "Sự ra đời của Lý thuyết Đồ thị năm 1736",
                "theTag": ["Euler", "Lý thuyết đồ thị", "7 cây cầu Königsberg"],
                "danhSachNhanVat": [{"id": "euler", "ten": "Leonhard Euler"}],
                "chuong": [
                    {
                        "id": "chuong_1",
                        "tenChuong": "1. Trò cá cược thành phố",
                        "canh": [{"id": "c1", "tuFrame": 0, "denFrame": 1800}],
                    },
                    {
                        "id": "chuong_2",
                        "tenChuong": "2. Nét bút thiên tài của Euler",
                        "canh": [{"id": "c2", "tuFrame": 1800, "denFrame": 3600}],
                    },
                ],
            }
            (dl_dir / slug / "du_lieu_render.json").write_text(
                json.dumps(du_lieu_render, ensure_ascii=False), encoding="utf-8"
            )
            (out_dir / slug / "chapters_va_mo_ta.txt").write_text(
                tao_chapters_va_mo_ta(du_lieu_render), encoding="utf-8"
            )

            # Video 600KB chia theo chunk 256KB -> 3 chunk (256KB + 256KB + 88KB)
            noi_dung_video = (b"MP4DATA_BLOCK_1234567890" * 26000)[: 600 * 1024]
            (out_dir / slug / "video_hoan_chinh.mp4").write_bytes(noi_dung_video)
            (out_dir / slug / "thumbnail_1.png").write_bytes(b"\x89PNG\r\n\x1a\nMOCK_THUMB")
            (out_dir / slug / "phu_de.srt").write_text(
                "1\n00:00:00,000 --> 00:00:03,000\nChào mừng đến với Königsberg năm 1736!\n",
                encoding="utf-8",
            )

            # Mock toan bo HTTP cho OAuth, Resumable Upload (co 1 lan 503 retry), Thumbnail 403 an toan, Caption 200
            bytes_nhan_duoc = bytearray()
            metadata_gui_len: dict[str, Any] = {}
            content_ranges: list[str] = []
            caption_payloads: list[bytes] = []
            so_lan_put = {"n": 0}
            da_mo_phong_503 = {"flag": False}

            def fake_http(
                method: str,
                url: str,
                headers: dict[str, str],
                data: bytes | None,
                timeout: int,
            ) -> tuple[int, dict[str, str], bytes]:
                if url == "https://oauth2.googleapis.com/token":
                    return 200, {}, json.dumps({"access_token": "mock_token_upload_1"}).encode("utf-8")

                if "upload/youtube/v3/videos" in url and method == "POST":
                    self.assertEqual(headers.get("Authorization"), "Bearer mock_token_upload_1")
                    self.assertEqual(headers.get("X-Upload-Content-Length"), str(len(noi_dung_video)))
                    metadata_gui_len.update(json.loads((data or b"{}").decode("utf-8")))
                    return 200, {"location": "https://upload.mock/resumable/session_abc"}, b""

                if url == "https://upload.mock/resumable/session_abc" and method == "PUT":
                    if not da_mo_phong_503["flag"]:
                        da_mo_phong_503["flag"] = True
                        return 503, {}, b"Temporary backend error"
                    so_lan_put["n"] += 1
                    cr = headers.get("Content-Range", "")
                    content_ranges.append(cr)
                    chunk_data = data or b""
                    bytes_nhan_duoc.extend(chunk_data)
                    if len(bytes_nhan_duoc) < len(noi_dung_video):
                        return 308, {"range": f"bytes=0-{len(bytes_nhan_duoc) - 1}"}, b""
                    return 200, {}, json.dumps({"id": "yt_video_98765"}).encode("utf-8")

                if "thumbnails/set" in url and method == "POST":
                    # Mo phong kenh chua xac minh SDT (403) -> KHONG duoc lam fail luong chinh
                    return 403, {}, b'{"error": {"message": "The authenticated user does not have permissions to upload and set custom video thumbnails."}}'

                if "upload/youtube/v3/captions" in url and method == "POST":
                    caption_payloads.append(data or b"")
                    return 200, {}, json.dumps({"id": "cap_001"}).encode("utf-8")

                raise AssertionError(f"Request khong mong doi: {method} {url}")

            bay_gio_sang_vn = datetime.datetime(2026, 11, 26, 7, 15, 0, tzinfo=MUI_GIO_VN)
            kq = dang_video_len_youtube(
                slug=slug,
                gio_cong_khai_vn="19:30",
                cach_ngay=0,
                chi_rieng_tu=False,
                chunk_size=256 * 1024,
                thu_muc_out=out_dir,
                thu_muc_du_lieu=dl_dir,
                duong_dan_bo_nho=bo_nho_path,
                env_override={
                    "YOUTUBE_CLIENT_ID": "cid_ok",
                    "YOUTUBE_CLIENT_SECRET": "csec_ok",
                    "YOUTUBE_REFRESH_TOKEN": "rtok_ok",
                },
                http_caller=fake_http,
                bay_gio=bay_gio_sang_vn,
                sleep_fn=lambda _: None,
            )

            self.assertEqual(kq["trangThai"], "thanh_cong")
            self.assertEqual(kq["video_id"], "yt_video_98765")
            self.assertEqual(kq["publishAt"], "2026-11-26T19:30:00+07:00")
            # Kiem tra Resumable Upload dung 3 chunk va khop tung byte
            self.assertEqual(so_lan_put["n"], 3)
            self.assertEqual(kq["upload"]["so_chunk"], 3)
            self.assertEqual(bytes(bytes_nhan_duoc), noi_dung_video)
            self.assertTrue(content_ranges[0].startswith("bytes 0-262143/"))
            self.assertTrue(content_ranges[-1].endswith(f"/{len(noi_dung_video)}"))
            # Kiem tra metadata snippet + status hen gio chuan YouTube (private + publishAt +07:00)
            self.assertIn("Leonhard Euler", metadata_gui_len["snippet"]["title"])
            self.assertIn("00:00 1. Trò cá cược thành phố", metadata_gui_len["snippet"]["description"])
            self.assertNotIn("TIÊU ĐỀ GỢI Ý", metadata_gui_len["snippet"]["description"])
            self.assertIn("Euler", metadata_gui_len["snippet"]["tags"])
            self.assertEqual(metadata_gui_len["status"]["privacyStatus"], "private")
            self.assertEqual(metadata_gui_len["status"]["publishAt"], "2026-11-26T19:30:00+07:00")
            # Thumbnail 403 bi bat an toan, phu de .srt thanh cong
            self.assertFalse(kq["thumbnail"]["thanhCong"])
            self.assertTrue(kq["phuDe"]["thanhCong"])
            self.assertEqual(len(caption_payloads), 1)
            self.assertIn(b"yt_video_98765", caption_payloads[0])
            self.assertIn("Königsberg năm 1736".encode("utf-8"), caption_payloads[0])

            # Kiem tra bo_nho_hoc_hoi.json da luu video_id + publishAt de dong_bo_youtube.py tu keo so lieu
            bn_sau = tai_bo_nho(bo_nho_path)
            tap = next(m for m in bn_sau["chu_de_da_lam"] if m["slug"] == slug)
            self.assertEqual(tap["youtubeVideoId"], "yt_video_98765")
            self.assertEqual(tap["youtubePublishAt"], "2026-11-26T19:30:00+07:00")
            self.assertEqual(tap["youtubeCheDo"], "hen_gio")
            self.assertFalse(tap["youtubeDaGanThumbnail"])
            self.assertTrue(tap["youtubeDaTaiPhuDe"])
            self.assertEqual(tim_video_id_tu_bo_nho(slug, duong_dan_bo_nho=bo_nho_path), "yt_video_98765")

    def test_che_do_chi_rieng_tu_va_tien_ich_lay_refresh_token(self) -> None:
        import urllib.parse

        # 1. Metadata che do --chi-rieng-tu: privacyStatus='private', KHONG gan publishAt
        meta_priv = tao_metadata_video(
            tieu_de="Chủ đề thử nghiệm",
            mo_ta="Mô tả ngắn",
            the_tag=["toán học"],
            publish_at="2026-11-26T19:30:00+07:00",
            chi_rieng_tu=True,
        )
        self.assertEqual(meta_priv["status"]["privacyStatus"], "private")
        self.assertNotIn("publishAt", meta_priv["status"])
        self.assertEqual(KICH_THUOC_CHUNK_MAC_DINH, 8 * 1024 * 1024)

        # 2. Tien ich lay_refresh_token_youtube.py: tao URL OAuth2 va doi code -> refresh_token
        auth_url = tao_url_xac_thuc_google(
            client_id="cid_local",
            redirect_uri="http://127.0.0.1:8765/oauth2callback",
            state="state_xyz",
        )
        parsed = urllib.parse.urlparse(auth_url)
        qs = urllib.parse.parse_qs(parsed.query)
        self.assertEqual(qs["access_type"], ["offline"])
        self.assertEqual(qs["prompt"], ["consent"])
        self.assertEqual(qs["state"], ["state_xyz"])
        for sc in YOUTUBE_SCOPES:
            self.assertIn(sc, qs["scope"][0])

        class _FakeResp:
            def __enter__(self) -> "_FakeResp":
                return self

            def __exit__(self, *args: Any) -> None:
                return None

            def read(self) -> bytes:
                return json.dumps(
                    {"refresh_token": "rtok_moi_30s", "access_token": "atok_moi"}
                ).encode("utf-8")

        tokens = doi_code_lay_tokens(
            client_id="cid_local",
            client_secret="csec_local",
            code="auth_code_123",
            redirect_uri="http://127.0.0.1:8765/oauth2callback",
            urlopen_fn=lambda req, timeout=30: _FakeResp(),
        )
        self.assertEqual(tokens["refresh_token"], "rtok_moi_30s")


class TestNangCapV35KeChuyenOffline(unittest.TestCase):
    """Bo unit test offline cho dot nang cap ke chuyen v3.5 (nhac 4 cam xuc, crossfade 1.5s, ngat 0.8s, 3 canh moi, Mascot & Thumbnail AI)."""

    def test_v35_nhac_nen_4_cam_xuc_crossfade_15s_va_ngat_punchline_08s(self) -> None:
        from scripts.pipeline.render_dai import (
            CROSSFADE_NHAC_HOI_GIAY,
            NGAT_NHAC_PUNCHLINE_GIAY,
            TAM_TRANG_NHAC_HOP_LE,
            tinh_lich_trinh_nhac_nen,
            xac_dinh_nhac_nen_theo_tam_trang,
        )
        from scripts.pipeline.tao_am_thanh_mau import DANH_SACH_TEN_BGM_CAM_XUC

        self.assertEqual(CROSSFADE_NHAC_HOI_GIAY, 1.5)
        self.assertEqual(NGAT_NHAC_PUNCHLINE_GIAY, 0.8)
        self.assertEqual(len(DANH_SACH_TEN_BGM_CAM_XUC), 4)

        # 1. Xac minh 4 file nhac nen cam xuc ton tai trong public/bgm/
        for mood in TAM_TRANG_NHAC_HOP_LE:
            p = xac_dinh_nhac_nen_theo_tam_trang(mood)
            self.assertIsNotNone(p, f"Thieu file public/bgm/{mood}.mp3")
            assert p is not None
            self.assertEqual(p.name, f"{mood}.mp3")
            self.assertGreater(p.stat().st_size, 1024)

        # 2. Lich trinh nhac nen da cam xuc theo hoi + ngat 0.8s truoc punchline
        kb_nhac = {
            "chuong": [
                {
                    "id": "chuong_1",
                    "tenChuong": "1. Bi an mo man",
                    "tamTrangNhac": "bi_an",
                    "canh": [
                        {"id": "canh_001", "tuFrame": 0, "denFrame": 300},
                    ],
                },
                {
                    "id": "chuong_2",
                    "tenChuong": "2. Cao trao kich tinh",
                    "tamTrangNhac": "kich_tinh",
                    "canh": [
                        {"id": "canh_002", "tuFrame": 300, "denFrame": 450},
                        {"id": "canh_003", "tuFrame": 450, "denFrame": 600, "ngatNhacPunchline": True},
                    ],
                },
                {
                    "id": "chuong_3",
                    "tenChuong": "3. Du am tram lang",
                    "tamTrangNhac": "tram_lang",
                    "canh": [
                        {"id": "canh_004", "tuFrame": 600, "denFrame": 900},
                    ],
                },
            ]
        }
        lich = tinh_lich_trinh_nhac_nen(kb_nhac, fps=30)
        self.assertEqual(len(lich["cacDoanNhac"]), 3)
        self.assertEqual(
            [d["tamTrangNhac"] for d in lich["cacDoanNhac"]],
            ["bi_an", "kich_tinh", "tram_lang"],
        )
        self.assertEqual(len(lich["cacMocNgatPunchline"]), 1)
        moc = lich["cacMocNgatPunchline"][0]
        self.assertEqual(moc["canhId"], "canh_003")
        self.assertAlmostEqual(moc["thoiLuongGiay"], 0.8, places=2)

        # 3. Chuoi filter_complex FFmpeg co acrossfade=d=1.50 va volume=0:enable='between(t,...)'
        fc = tao_filter_hau_ky_audio(
            tong_giay=30.0,
            co_audio_chinh=True,
            co_nhac_nen=True,
            cac_doan_nhac=lich["cacDoanNhac"],
            cac_moc_ngat_punchline=lich["cacMocNgatPunchline"],
        )
        self.assertIn("acrossfade=d=1.50:c1=tri:c2=tri", fc)
        self.assertIn("volume=0:enable='between(t,", fc)
        self.assertIn("sidechaincompress", fc)
        self.assertIn("loudnorm=I=-14:TP=-1.5:LRA=11", fc)

        cmd = dung_lenh_hau_ky_audio_ffmpeg(
            file_vao=Path("in.mp4"),
            file_xuat=Path("out.mp4"),
            tong_giay=30.0,
            co_audio_chinh=True,
            cac_doan_nhac=lich["cacDoanNhac"],
            cac_moc_ngat_punchline=lich["cacMocNgatPunchline"],
        )
        # 3 track BGM -> 3 lan -stream_loop -1
        self.assertEqual(cmd.count("-stream_loop"), 3)

    def test_v35_schema_3_canh_moi_mascot_thumbnail_ai_va_prompt(self) -> None:
        from scripts.pipeline.tao_kich_ban_10p import (
            ID_MASCOT_KENH,
            KIEU_PHAN_UNG_CAM,
            PHUONG_TIEN_HANH_TRINH,
            TAM_TRANG_NHAC,
            lay_ho_so_mascot_kenh,
        )

        # 1. Enum & Mascot tuy chinh tu env
        for bc in ("ban_do_hanh_trinh", "bao_chi_co", "phan_ung_cam"):
            self.assertIn(bc, LOAI_BO_CUC)
        self.assertEqual(len(TAM_TRANG_NHAC), 4)
        self.assertEqual(len(PHUONG_TIEN_HANH_TRINH), 4)
        self.assertEqual(len(KIEU_PHAN_UNG_CAM), 4)

        m_mac_dinh = lay_ho_so_mascot_kenh(env_override={})
        self.assertEqual(m_mac_dinh["id"], ID_MASCOT_KENH)
        m_tuy_chinh = lay_ho_so_mascot_kenh(
            env_override={"MASCOT_TEN": "Cô Sigma", "MASCOT_MAU_AO": "#16A34A", "MASCOT_TRANG_PHUC": "ao_vest_co_dien"}
        )
        self.assertEqual(m_tuy_chinh["ten"], "Cô Sigma")
        self.assertEqual(m_tuy_chinh["mauAo"], "#16A34A")
        self.assertEqual(m_tuy_chinh["trangPhuc"], "ao_vest_co_dien")

        # 2. Sanitizer giu nguyen 3 canh moi + tamTrangNhac + openLoopCuoiHoi + ngatNhacPunchline + endScreen + Mascot
        kb_raw = {
            "tieuDe": "Leonhard Euler & 7 Cây Cầu",
            "chuDe": "Khám phá Lý thuyết Đồ thị",
            "danhSachNhanVat": [{"id": "euler", "ten": "Leonhard Euler", "mauChuDao": "#1D4ED8"}],
            "chuong": [
                {
                    "id": "chuong_1",
                    "tenChuong": "1. Chuyến đi định mệnh",
                    "tamTrangNhac": "bi_an",
                    "openLoopCuoiHoi": "Nhưng điều gì khiến bức thư năm 1736 làm cả châu Âu sững sờ?",
                    "canh": [
                        {
                            "boCuc": "ban_do_hanh_trinh",
                            "loiThoai": "Bức thư vượt hàng trăm cây số từ Königsberg đến Saint Petersburg.",
                            "banDoHanhTrinh": {
                                "diemDi": "Königsberg",
                                "diemDen": "Saint Petersburg",
                                "phuongTien": "thu_tay",
                                "khoangCachNhan": "1.000 km • 1736",
                            },
                            "anhBoiCanh": "boi_canh/euler/bc_01_cau.jpg",
                            "nhanVat": [{"id": ID_MASCOT_KENH, "x": 960, "y": 810, "huong": "phai"}],
                        },
                        {
                            "boCuc": "bao_chi_co",
                            "loiThoai": "Tin chấn động xuất hiện ngay trên trang nhất giới học thuật châu Âu.",
                            "baoChiCo": {
                                "tenToBao": "Nhật Báo Toán Học",
                                "tieuDeBao": "KHÔNG AI ĐI QUA ĐƯỢC BẢY CÂY CẦU!",
                                "tieuDePhu": "Cả thành phố đi mòn giày mà vẫn bó tay",
                                "daoCuMinhHoa": "cuon_giay",
                            },
                            "ngatNhacPunchline": True,
                            "anhBoiCanh": "boi_canh/euler/bc_02_pho.jpg",
                        },
                        {
                            "boCuc": "phan_ung_cam",
                            "loiThoai": "Thị trưởng khựng lại không tin nổi.",
                            "phanUngCam": {
                                "nhanVatId": "euler",
                                "kieuPhanUng": "nhap_tra",
                                "chuHieuUng": "HẢ?!",
                            },
                        },
                        {
                            "boCuc": "ket_thuc",
                            "loiThoai": "Cảm ơn bạn đã xem hết câu chuyện, bấm chọn tập tiếp theo bên cạnh nhé!",
                            "endScreen": {
                                "khungTraiNhan": "TẬP KẾ TIẾP",
                                "khungPhaiNhan": "DANH SÁCH PHÁT",
                                "loiDanXemTiep": "Chọn video ở hai bên để khám phá tiếp!",
                            },
                            "nhanVat": [{"id": ID_MASCOT_KENH, "x": 960, "y": 830, "huong": "phai"}],
                        },
                    ],
                }
            ],
        }
        kb_sach, _ = chuan_hoa_toan_bo_kich_ban(kb_raw)
        ch0 = kb_sach["chuong"][0]
        self.assertEqual(ch0["tamTrangNhac"], "bi_an")
        self.assertIn("bức thư năm 1736", ch0["openLoopCuoiHoi"])
        self.assertEqual(ch0["canh"][0]["banDoHanhTrinh"]["phuongTien"], "thu_tay")
        self.assertEqual(ch0["canh"][0]["nhanVat"][0]["id"], ID_MASCOT_KENH)
        self.assertTrue(ch0["canh"][1]["ngatNhacPunchline"])
        self.assertEqual(ch0["canh"][1]["baoChiCo"]["tieuDeBao"], "KHÔNG AI ĐI QUA ĐƯỢC BẢY CÂY CẦU!")
        self.assertEqual(ch0["canh"][2]["phanUngCam"]["kieuPhanUng"], "nhap_tra")
        self.assertEqual(ch0["canh"][3]["endScreen"]["khungTraiNhan"], "TẬP KẾ TIẾP")
        self.assertEqual(kiem_tra_dau_tieng_viet(kb_sach), [])

        # 3. Thumbnail A/B uu tien anhBoiCanh AI cua tap
        ds_thumb = chuan_bi_phuong_an_thumbnail(kb_sach)
        self.assertEqual(len(ds_thumb), 3)
        self.assertTrue(all(str(pa.get("anhBoiCanh") or "").startswith("boi_canh/euler/") for pa in ds_thumb))

        # 4. Prompt tang 1 & tang 2 bao gom Cold Open 15s, Open Loop, an du hien dai, 3 canh moi & Mascot
        p1 = tao_prompt_tang_1("Euler và 7 cây cầu", 11.0, "di_dom_gan_gui")
        for kw in ("COLD OPEN 15 GIÂY", "openLoopCuoiHoi", "tamTrangNhac", "ban_do_hanh_trinh", "bao_chi_co", "phan_ung_cam", ID_MASCOT_KENH):
            self.assertIn(kw.lower(), p1.lower(), f"Prompt tang 1 thieu '{kw}'")

        bp_gia = {
            "tieuDe": "Euler & 7 Cây Cầu",
            "danhSachNhanVat": [{"id": "euler", "ten": "Leonhard Euler"}],
            "hookMoMan": {"cauMoDauGaySoc": "Đi dạo mà khai sinh cả ngành Toán?"},
        }
        hoi_gia = {
            "tenChuong": "1. Mở màn",
            "boiCanhChinh": "pho_co_chau_au",
            "thoiTietChinh": "nang_dep",
            "tomTat": "Giới thiệu bài toán",
            "tamTrangNhac": "bi_an",
        }
        p2 = tao_prompt_tang_2_hoi(bp_gia, hoi_gia, KHUNG_6_HOI[0], "di_dom_gan_gui", "")
        for kw in ("COLD OPEN 15 GIAY", "OPEN LOOP", "AN DU HIEN DAI", "ngatNhacPunchline", "ban_do_hanh_trinh", "bao_chi_co", "phan_ung_cam", "endScreen"):
            self.assertIn(kw.lower(), p2.lower(), f"Prompt tang 2 thieu '{kw}'")


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    if res.wasSuccessful():
        print("\n[THANH CONG] Tat ca unit test offline pipeline v1.0 deu xanh!")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
