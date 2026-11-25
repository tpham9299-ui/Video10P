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
    tinh_bien_do_rms_tu_pcm,
    tinh_moc_va_rms_luot_thoai,
    tinh_toan_khung_hinh,
    trich_xuat_bien_do_rms,
    xac_dinh_cau_hinh_tts_canh,
    xuat_file_srt,
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
    chuan_hoa_buoc_ve_toan,
    chuan_hoa_goi_y_thumbnail,
    chuan_hoa_toan_bo_kich_ban,
    kiem_dinh_guardrail_kich_ban,
    kiem_dinh_nhip_ngat_thi_giac,
    kiem_dinh_schema_du_lieu_canh,
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
                ["gemini-flash-latest", "gemini-flash-lite-latest", "gemini-pro-latest"],
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

        cmd_don = dung_lenh_render_thumbnail(Path("a.json"), Path("out.png"), npx_bin="npx")
        self.assertEqual(cmd_don, ["npx", "remotion", "still", "src/index.ts", THUMBNAIL_STILL_ID, "out.png", "--props=a.json"])

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

        # Xac minh du luong 3 job song song theo chunk, lich chay hang ngay & tu dong luu bo nho
        for bat_buoc in (
            "schedule:",
            "- cron: '0 0 * * *'",
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
            "actions/cache@v4",
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
        # YOUTUBE_API_KEY la tuy chon: workflow hang ngay KHONG duoc phu thuoc hay yeu cau secret nay
        self.assertNotIn("YOUTUBE_API_KEY", text)

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
        # 1. Xac minh enum v2.0 dong bo day du voi src/kieu_dai.ts
        self.assertEqual(len(GOC_QUAY_CAMERA), 8)
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
