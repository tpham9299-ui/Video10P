# -*- coding: utf-8 -*-
"""Bo test don vi offline (khong goi API that) cho he thong AI san xuat phim Toan hoc >10 phut (v0.5)."""

from __future__ import annotations

import json
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
    da_ton_tai_chu_de,
    ghi_nhan_tap_hoan_thanh,
    hoc_tu_phan_hoi,
    luu_bo_nho,
    tai_bo_nho,
    tao_ngu_canh_hoc_hoi,
    them_bai_hoc,
    them_chu_de_hang_doi,
)
from scripts.pipeline.chuan_hoa_doc_toan import chuan_hoa_doc_toan
from scripts.pipeline.chuanbi_dai import (
    bam_noi_dung_tts,
    chia_phu_de,
    chuan_bi_audio_va_du_lieu_render,
    tinh_toan_khung_hinh,
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
    chon_chuong_can_render,
    dinh_dang_thoi_gian_youtube,
    ghep_luoi_kiem_dinh,
    phan_tich_danh_sach_chuong_chon,
    tao_chapters_va_mo_ta,
    tao_noi_dung_chapters,
    tinh_hash_chuong,
    tinh_pham_vi_frame_chuong,
)
from scripts.pipeline.san_tim_chu_de import (
    nap_hang_doi_chu_de,
    nghien_cuu_chu_de,
    tra_cuu_tom_tat_wikipedia,
)
from scripts.pipeline.san_xuat_lien_tuc import chay_san_xuat_lien_tuc
from scripts.pipeline.tao_kich_ban_10p import (
    LOAI_BIEU_CAM,
    LOAI_BOI_CANH,
    LOAI_BO_CUC,
    LOAI_HANH_DONG,
    LOAI_HIEU_UNG_HOAT_HINH,
    LOAI_MINH_HOA_TOAN,
    LOAI_PHU_KIEN,
    LOAI_THOI_TIET,
    LOAI_VAT_CAM_TAY,
    bien_kich_3_tang,
    chuan_hoa_toan_bo_kich_ban,
    kiem_tra_latex,
    tao_markdown_doc_duyet,
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


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    if res.wasSuccessful():
        print("\n[THANH CONG] Tat ca unit test offline pipeline v0.5 deu xanh!")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
