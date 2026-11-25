# -*- coding: utf-8 -*-
"""Bo goi Gemini REST API xoay vong nhieu API key va parse JSON an toan."""

from __future__ import annotations

import base64
import http.client
import json
import mimetypes
import os
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

MAC_DINH_MODEL = "gemini-flash-latest"
MAC_DINH_FALLBACK_MODELS = (
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-2.0-flash",
    "gemini-pro-latest",
)
# Lich nghi lui dan (giay) sau moi vong xoay het toan bo API key khi gap 503 qua tai server (toi da 3 vong)
LICH_BACKOFF_THEO_VONG: tuple[float, ...] = (8.0, 20.0, 40.0)
SO_VONG_TOI_DA_MAC_DINH = 3
THOI_GIAN_NGHI_DOI_KEY_GIAY = 1.0
THOI_GIAN_NGHI_CHUYEN_MODEL_429_GIAY = 2.0
GEMINI_ENDPOINT_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
GEMINI_MODELS_LIST_URL = "https://generativelanguage.googleapis.com/v1beta/models"
MA_LOI_XOAY_KEY = {429, 500, 502, 503, 504}
MA_LOI_QUA_TAI_SERVER = {500, 502, 503, 504}
TU_KHOA_LOAI_BO_MODEL = (
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
)


class GeminiError(RuntimeError):
    """Loi chung khi goi Gemini API."""


class GeminiQuotaError(GeminiError):
    """Loi het quota / rate limit tren tat ca cac API key."""


def tai_env(duong_dan_env: Path | str | None = None) -> dict[str, str]:
    """Doc file .env don gian bang thu vien chuan (khong can python-dotenv)."""
    ket_qua: dict[str, str] = {}
    if duong_dan_env is None:
        duong_dan_env = Path(__file__).resolve().parents[2] / ".env"
    else:
        duong_dan_env = Path(duong_dan_env)

    if not duong_dan_env.exists():
        return ket_qua

    for dong in duong_dan_env.read_text(encoding="utf-8").splitlines():
        sach = dong.strip()
        if not sach or sach.startswith("#") or "=" not in sach:
            continue
        khoa, gia_tri = sach.split("=", 1)
        khoa = khoa.strip()
        gia_tri = gia_tri.strip()
        if len(gia_tri) >= 2 and (
            (gia_tri[0] == '"' and gia_tri[-1] == '"')
            or (gia_tri[0] == "'" and gia_tri[-1] == "'")
        ):
            gia_tri = gia_tri[1:-1]
        if khoa:
            ket_qua[khoa] = gia_tri
    return ket_qua


def _chuan_hoa_ten_model(ten: str) -> str:
    sach = ten.strip()
    if sach.startswith("models/"):
        sach = sach[len("models/") :]
    return sach.strip()


def _tach_danh_sach_khong_trung(raw: str, chuan_hoa: Callable[[str], str] | None = None) -> list[str]:
    ket_qua: list[str] = []
    for item in raw.split(","):
        gt = chuan_hoa(item) if chuan_hoa else item.strip()
        if gt and gt not in ket_qua:
            ket_qua.append(gt)
    return ket_qua


def lay_cau_hinh_gemini(
    duong_dan_env: Path | str | None = None,
    env_override: dict[str, str] | None = None,
) -> tuple[list[str], str]:
    """Lay danh sach GEMINI_API_KEYS (fallback GEMINI_API_KEY) va GEMINI_MODEL."""
    tu_file = tai_env(duong_dan_env)
    nguon: dict[str, str] = {}
    nguon.update(tu_file)
    for k in ("GEMINI_API_KEYS", "GEMINI_API_KEY", "GEMINI_MODEL", "GEMINI_FALLBACK_MODELS"):
        if os.environ.get(k):
            nguon[k] = os.environ[k]
    if env_override:
        nguon.update(env_override)

    raw_keys = nguon.get("GEMINI_API_KEYS", "").strip()
    if not raw_keys:
        raw_keys = nguon.get("GEMINI_API_KEY", "").strip()

    keys = _tach_danh_sach_khong_trung(raw_keys)
    model = _chuan_hoa_ten_model(nguon.get("GEMINI_MODEL", "")) or MAC_DINH_MODEL
    return keys, model


def lay_fallback_models(
    duong_dan_env: Path | str | None = None,
    env_override: dict[str, str] | None = None,
) -> list[str]:
    """Lay danh sach GEMINI_FALLBACK_MODELS tu .env / bien moi truong (co gia tri mac dinh)."""
    tu_file = tai_env(duong_dan_env)
    nguon: dict[str, str] = {}
    nguon.update(tu_file)
    if os.environ.get("GEMINI_FALLBACK_MODELS"):
        nguon["GEMINI_FALLBACK_MODELS"] = os.environ["GEMINI_FALLBACK_MODELS"]
    if env_override:
        nguon.update(env_override)

    raw = nguon.get("GEMINI_FALLBACK_MODELS", "").strip()
    models = _tach_danh_sach_khong_trung(raw, chuan_hoa=_chuan_hoa_ten_model) if raw else []
    return models or list(MAC_DINH_FALLBACK_MODELS)


def lam_sach_json(van_ban: str) -> str:
    """Bo boc markdown ```json ... ``` va trich phan JSON sach nhat."""
    s = van_ban.strip()
    if not s:
        return s

    # Boc markdown fenced block neu co
    khop_fence = re.search(r"```(?:json|JSON)?\s*\n?(.*?)```", s, flags=re.DOTALL)
    if khop_fence:
        s = khop_fence.group(1).strip()

    # Neu van con van ban thua truoc/sau, tim cap ngoac ngoai cung {...} hoac [...]
    vi_tri_obj = s.find("{")
    vi_tri_arr = s.find("[")
    bat_dau = -1
    ket_thuc_ky_tu = ""

    if vi_tri_obj != -1 and (vi_tri_arr == -1 or vi_tri_obj < vi_tri_arr):
        bat_dau = vi_tri_obj
        ket_thuc_ky_tu = "}"
    elif vi_tri_arr != -1:
        bat_dau = vi_tri_arr
        ket_thuc_ky_tu = "]"

    if bat_dau != -1:
        cuoi = s.rfind(ket_thuc_ky_tu)
        if cuoi > bat_dau:
            s = s[bat_dau : cuoi + 1]

    # Loai bo trailing comma pho bien truoc } hoac ]
    s = re.sub(r",\s*([}\]])", r"\1", s)
    return s.strip()


def parse_json_an_toan(van_ban: str) -> Any:
    """Parse chuoi JSON sau khi lam sach markdown va sua ky tu dieu khien nhe."""
    sach = lam_sach_json(van_ban)
    try:
        return json.loads(sach)
    except json.JSONDecodeError:
        # Thu them mot luot bo BOM va ky tu control bat hop le trong chuoi
        sach2 = sach.lstrip("\ufeff")
        sach2 = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", " ", sach2)
        return json.loads(sach2)


def _la_loi_het_quota_429(status_code: int | None, body_text: str) -> bool:
    if status_code == 429:
        return True
    thap = body_text.lower()
    return any(
        tk in thap
        for tk in ("resource_exhausted", "quota", "rate limit", "too many requests")
    )


def _la_loi_quota_hoac_tam_thoi(status_code: int | None, body_text: str) -> bool:
    if status_code in MA_LOI_XOAY_KEY:
        return True
    if _la_loi_het_quota_429(status_code, body_text):
        return True
    thap = body_text.lower()
    return any(tk in thap for tk in ("overloaded", "unavailable"))


def _la_loi_model_khong_hop_le(status_code: int | None, body_text: str) -> bool:
    """Nhan dien loi 404 (model bi go/khong ton tai) hoac 400 do sai ten model."""
    if status_code == 404:
        return True
    if status_code == 400:
        thap = body_text.lower()
        if "model" in thap and any(
            tk in thap
            for tk in (
                "not found",
                "invalid",
                "not supported",
                "unsupported",
                "unknown",
                "does not exist",
                "unexpected",
                "unrecognized",
                "deprecated",
                "retired",
            )
        ):
            return True
    return False


def _khoa_xep_hang_model(ten: str) -> tuple[Any, ...]:
    """Xep hang uu tien model: gemini-flash-latest -> cac ban flash moi nhat -> cac ban con lai."""
    thap = ten.lower()
    if thap == "gemini-flash-latest":
        return (0, 0, 0, 0, 0, 0, (), thap)

    la_gemini = thap.startswith("gemini")
    co_flash = "flash" in thap
    co_lite = "lite" in thap
    co_pro = "pro" in thap
    la_exp_hoac_preview = any(tk in thap for tk in ("exp", "preview", "experimental"))
    co_latest = "latest" in thap

    khop_ver = re.search(r"gemini-(\d+)(?:\.(\d+))?", thap)
    major = int(khop_ver.group(1)) if khop_ver else 0
    minor = int(khop_ver.group(2)) if (khop_ver and khop_ver.group(2)) else 0

    phan_sau = re.sub(r"^gemini-\d+(?:\.\d+)?", "", thap)
    so_phu = tuple(int(x) for x in re.findall(r"(?<=-)\d+(?=-|$)", phan_sau))

    if la_gemini and co_flash and not co_lite:
        nhom = 1
    elif la_gemini and co_flash and co_lite:
        nhom = 2
    elif co_flash:
        nhom = 3
    elif thap == "gemini-pro-latest":
        nhom = 4
    elif la_gemini and co_pro:
        nhom = 5
    elif la_gemini:
        nhom = 6
    else:
        nhom = 7

    la_alias_latest_khong_so = 1 if (co_latest and major == 0) else 0

    return (
        nhom,
        -la_alias_latest_khong_so,
        -major,
        -minor,
        1 if la_exp_hoac_preview else 0,
        0 if (co_latest or not so_phu) else 1,
        tuple(-n for n in so_phu),
        thap,
    )


def loc_va_xep_hang_models(danh_sach_models: list[dict[str, Any]]) -> list[str]:
    """Loc cac model sinh van ban Gemini chuan (generateContent), loai bo toan bo model chuyen biet/khong phu hop."""
    hop_le: list[str] = []
    for item in danh_sach_models:
        if not isinstance(item, dict):
            continue
        methods = item.get("supportedGenerationMethods") or []
        if not isinstance(methods, list) or "generateContent" not in methods:
            continue
        raw_name = item.get("name")
        if not isinstance(raw_name, str):
            continue
        ten = _chuan_hoa_ten_model(raw_name)
        if not ten:
            continue
        thap = ten.lower()
        if any(tk in thap for tk in TU_KHOA_LOAI_BO_MODEL):
            continue
        # Chi giu lai cac dong model van ban Gemini chuan (flash / pro)
        if not thap.startswith("gemini-") or not ("flash" in thap or "pro" in thap):
            continue
        if ten not in hop_le:
            hop_le.append(ten)

    hop_le.sort(key=_khoa_xep_hang_model)
    return hop_le


class GeminiClient:
    """Client goi Gemini co xoay vong API key, tu do/doi model an toan, backoff va thu lai JSON."""

    def __init__(
        self,
        api_keys: list[str] | None = None,
        model: str | None = None,
        fallback_models: list[str] | tuple[str, ...] | None = None,
        duong_dan_env: Path | str | None = None,
        timeout_giay: int = 180,
        backoff_co_so: float = 1.5,
        lich_backoff_theo_vong: tuple[float, ...] | list[float] | None = None,
        nghi_doi_key_giay: float = THOI_GIAN_NGHI_DOI_KEY_GIAY,
        nghi_chuyen_model_429_giay: float = THOI_GIAN_NGHI_CHUYEN_MODEL_429_GIAY,
        so_vong_toi_da: int = SO_VONG_TOI_DA_MAC_DINH,
        http_caller: Callable[[str, dict[str, Any], str, int], tuple[int, str]] | None = None,
        http_get_caller: Callable[[str, int], tuple[int, str]] | None = None,
        sleep_fn: Callable[[float], None] | None = None,
    ) -> None:
        env_keys, env_model = lay_cau_hinh_gemini(duong_dan_env=duong_dan_env)
        self.api_keys = list(api_keys) if api_keys is not None else env_keys
        self.model = _chuan_hoa_ten_model(model) if model else env_model
        if fallback_models is not None:
            fb_sach: list[str] = []
            for m in fallback_models:
                ten = _chuan_hoa_ten_model(m)
                if ten and ten not in fb_sach:
                    fb_sach.append(ten)
            self.fallback_models = fb_sach or list(MAC_DINH_FALLBACK_MODELS)
        else:
            self.fallback_models = lay_fallback_models(duong_dan_env=duong_dan_env)

        self.timeout_giay = timeout_giay
        self.backoff_co_so = backoff_co_so
        if lich_backoff_theo_vong is not None:
            lich_sach = tuple(max(0.0, float(x)) for x in lich_backoff_theo_vong)
            self.lich_backoff_theo_vong = lich_sach or LICH_BACKOFF_THEO_VONG
        else:
            self.lich_backoff_theo_vong = LICH_BACKOFF_THEO_VONG
        self.nghi_doi_key_giay = max(0.0, float(nghi_doi_key_giay))
        self.nghi_chuyen_model_429_giay = max(0.0, float(nghi_chuyen_model_429_giay))
        self.so_vong_toi_da = max(1, int(so_vong_toi_da))
        self._chi_so_key = 0
        self._http_caller = http_caller or self._goi_http_mac_dinh
        self._http_get_caller = http_get_caller or self._goi_http_get_mac_dinh
        self._sleep = sleep_fn or time.sleep
        self._models_khong_kha_dung: set[str] = set()
        self._models_da_do: list[str] = []
        self._google_search_het_quota = False
        self.nguon_tham_khao_gan_nhat: list[dict[str, str]] = []
        self.truy_van_web_gan_nhat: list[str] = []

        if not self.api_keys:
            raise GeminiError(
                "Chua cau hinh GEMINI_API_KEYS hoac GEMINI_API_KEY trong .env / bien moi truong."
            )

    @property
    def chi_so_key_hien_tai(self) -> int:
        return self._chi_so_key

    def _xoay_key(self) -> None:
        self._chi_so_key = (self._chi_so_key + 1) % len(self.api_keys)

    @staticmethod
    def _goi_http_mac_dinh(
        url: str,
        payload: dict[str, Any],
        api_key: str,
        timeout_giay: int,
    ) -> tuple[int, str]:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "x-goog-api-key": api_key,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout_giay) as resp:
                return resp.getcode(), resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as err:
            body = ""
            try:
                body = err.read().decode("utf-8", errors="replace")
            except Exception:
                body = str(err)
            return err.code, body
        except urllib.error.URLError as err:
            return 503, f"URLError: {err.reason}"
        except (TimeoutError, socket.timeout, http.client.HTTPException, OSError) as err:
            return 504, f"Timeout/NetworkError: {err}"

    @staticmethod
    def _goi_http_get_mac_dinh(url: str, timeout_giay: int) -> tuple[int, str]:
        req = urllib.request.Request(url, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=timeout_giay) as resp:
                return resp.getcode(), resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as err:
            body = ""
            try:
                body = err.read().decode("utf-8", errors="replace")
            except Exception:
                body = str(err)
            return err.code, body
        except urllib.error.URLError as err:
            return 503, f"URLError: {err.reason}"
        except (TimeoutError, socket.timeout, http.client.HTTPException, OSError) as err:
            return 504, f"Timeout/NetworkError: {err}"

    def tu_do_model_kha_dung(
        self,
        loai_tru: set[str] | None = None,
        buoc_tai_lai: bool = False,
    ) -> str | None:
        """Goi GET /v1beta/models?key=... de loc model generateContent hop le va ghi nho cho phien."""
        bo_qua = set(self._models_khong_kha_dung)
        if loai_tru:
            bo_qua.update(_chuan_hoa_ten_model(m) for m in loai_tru if m)

        if buoc_tai_lai or not self._models_da_do:
            so_key = len(self.api_keys)
            danh_sach_moi: list[str] = []
            for offset in range(so_key):
                chi_so = (self._chi_so_key + offset) % so_key
                key = self.api_keys[chi_so]
                query = urllib.parse.urlencode({"key": key})
                url = f"{GEMINI_MODELS_LIST_URL}?{query}"
                status, body = self._http_get_caller(url, self.timeout_giay)
                if status == 200:
                    try:
                        du_lieu = json.loads(body)
                        raw_models = du_lieu.get("models") if isinstance(du_lieu, dict) else []
                        if isinstance(raw_models, list):
                            danh_sach_moi = loc_va_xep_hang_models(raw_models)
                    except (json.JSONDecodeError, ValueError):
                        danh_sach_moi = []
                    if danh_sach_moi:
                        self._models_da_do = danh_sach_moi
                        break

        for ung_vien in self._models_da_do:
            if ung_vien not in bo_qua:
                model_cu = self.model
                self.model = ung_vien
                if ung_vien not in self.fallback_models:
                    self.fallback_models.insert(0, ung_vien)
                if model_cu != ung_vien:
                    print(
                        f"[Gemini] Da tu do va chuyen model: '{model_cu}' -> '{ung_vien}'."
                    )
                return ung_vien
        return None

    def _tinh_thoi_gian_cho_het_vong(self, vong_hien_tai: int) -> float:
        """Tra ve so giay nghi sau khi xoay het 1 vong tat ca API key (mac dinh 8s -> 20s -> 40s -> 60s)."""
        lich = self.lich_backoff_theo_vong or LICH_BACKOFF_THEO_VONG
        chi_so = max(0, min(len(lich) - 1, int(vong_hien_tai) - 1))
        return float(lich[chi_so])

    def _tao_hang_doi_model(self) -> list[str]:
        """Xay dung danh sach model se thu theo dung thu tu uu tien: model hien tai -> fallback -> model da do."""
        hang_doi: list[str] = []

        def _them(ten: str) -> None:
            m = _chuan_hoa_ten_model(ten)
            if m and m not in hang_doi and m not in self._models_khong_kha_dung:
                hang_doi.append(m)

        _them(self.model)

        # Giu nguyen thu tu uu tien trong fallback_models (dam bao gemini-pro-latest luon nam cuoi cung)
        for m in self.fallback_models:
            _them(m)

        for m in self._models_da_do:
            _them(m)

        if not hang_doi:
            hang_doi.append(self.model)
        return hang_doi

    @staticmethod
    def _trich_van_ban_tu_phan_hoi(body: str) -> str:
        du_lieu = json.loads(body)
        candidates = du_lieu.get("candidates") or []
        if not candidates:
            raise GeminiError(f"Gemini tra ve khong co candidates: {body[:300]}")
        cand = candidates[0]
        parts = cand.get("content", {}).get("parts") or []
        doan: list[str] = []
        for p in parts:
            if not isinstance(p, dict):
                continue
            # Bo qua phan suy luan noi bo (thought=True) cua cac model Gemini thinking de khong lam hong JSON
            if p.get("thought") is True:
                continue
            if isinstance(p.get("text"), str):
                doan.append(p["text"])
        ket_qua = "\n".join(doan).strip()
        if not ket_qua:
            ly_do = cand.get("finishReason") or "UNKNOWN"
            raise GeminiError(
                f"Gemini tra ve noi dung rong (finishReason={ly_do}): {body[:300]}"
            )
        return ket_qua

    @staticmethod
    def _trich_nguon_tu_phan_hoi(body: str) -> tuple[list[dict[str, str]], list[str]]:
        """Trich danh sach nguon tham khao va truy van web tu groundingMetadata/groundingChunks."""
        try:
            du_lieu = json.loads(body)
        except (json.JSONDecodeError, ValueError):
            return [], []

        candidates = du_lieu.get("candidates") or []
        if not candidates or not isinstance(candidates[0], dict):
            return [], []

        cand = candidates[0]
        meta = cand.get("groundingMetadata")
        if not isinstance(meta, dict):
            meta = du_lieu.get("groundingMetadata")
        if not isinstance(meta, dict):
            return [], []

        nguon: list[dict[str, str]] = []
        da_co_url: set[str] = set()

        def _them_nguon(url_raw: Any, tieu_de_raw: Any = "") -> None:
            url = str(url_raw or "").strip()
            if not url or url in da_co_url:
                return
            da_co_url.add(url)
            tieu_de = str(tieu_de_raw or "").strip() or url
            nguon.append({"tieuDe": tieu_de, "url": url})

        chunks = meta.get("groundingChunks") or []
        if isinstance(chunks, list):
            for ch in chunks:
                if not isinstance(ch, dict):
                    continue
                web = ch.get("web")
                if isinstance(web, dict):
                    _them_nguon(web.get("uri") or web.get("url"), web.get("title"))
                ctx = ch.get("retrievedContext")
                if isinstance(ctx, dict):
                    _them_nguon(ctx.get("uri") or ctx.get("url"), ctx.get("title"))

        attributions = meta.get("groundingAttributions") or []
        if isinstance(attributions, list):
            for attr in attributions:
                if not isinstance(attr, dict):
                    continue
                web = attr.get("web")
                if isinstance(web, dict):
                    _them_nguon(web.get("uri") or web.get("url"), web.get("title"))

        raw_queries = meta.get("webSearchQueries") or []
        truy_van = [
            str(q).strip()
            for q in raw_queries
            if isinstance(q, str) and q.strip()
        ] if isinstance(raw_queries, list) else []

        return nguon, truy_van

    @staticmethod
    def _la_loi_khong_ho_tro_tool_tim_kiem(status_code: int | None, body_text: str) -> bool:
        if status_code != 400:
            return False
        thap = body_text.lower()
        return any(
            tk in thap
            for tk in ("google_search", "search grounding", "grounding", "tools are not supported")
        )

    def _goi_generate_content(
        self,
        parts: list[dict[str, Any]],
        system_instruction: str | None = None,
        nhiet_do: float = 0.75,
        yeu_cau_json: bool = False,
        max_output_tokens: int = 8192,
        so_vong_toi_da: int | None = None,
        bat_tim_kiem_web: bool = False,
        tra_ve_nguon: bool = False,
        cho_phep_ha_cap_khong_tim_kiem: bool = True,
    ) -> str | tuple[str, list[dict[str, str]]]:
        """Loi goi chung Gemini generateContent (text hoac da phuong thuc kem anh inlineData), xoay key & fallback model."""
        if bat_tim_kiem_web and cho_phep_ha_cap_khong_tim_kiem and self._google_search_het_quota:
            bat_tim_kiem_web = False
        model_ban_dau = self.model
        so_vong = max(1, int(self.so_vong_toi_da if so_vong_toi_da is None else so_vong_toi_da))
        generation_config: dict[str, Any] = {
            "temperature": nhiet_do,
            "maxOutputTokens": max_output_tokens,
        }
        # Khi bat Google Search Grounding, mot so model khong cho ket hop responseMimeType=application/json
        if yeu_cau_json and not bat_tim_kiem_web:
            generation_config["responseMimeType"] = "application/json"

        payload: dict[str, Any] = {
            "contents": [{"role": "user", "parts": parts}],
            "generationConfig": generation_config,
        }
        if bat_tim_kiem_web:
            payload["tools"] = [{"google_search": {}}]
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        so_key = len(self.api_keys)
        tong_luot_thu_moi_model = so_key * so_vong
        hang_doi_model = self._tao_hang_doi_model()
        models_da_thu: set[str] = set()
        thu_tu_models_da_thu: list[str] = []
        da_tu_do_trong_luot = False
        co_loi_quota = False
        loi_cuoi = ""

        while hang_doi_model:
            model_hien_tai = hang_doi_model.pop(0)
            if model_hien_tai in models_da_thu:
                continue
            models_da_thu.add(model_hien_tai)
            thu_tu_models_da_thu.append(model_hien_tai)

            url = GEMINI_ENDPOINT_TEMPLATE.format(model=model_hien_tai)
            keys_bi_429: set[int] = set()
            chuyen_model = False

            for luot in range(tong_luot_thu_moi_model):
                key = self.api_keys[self._chi_so_key]
                key_an = f"...{key[-4:]}" if len(key) >= 4 else "***"
                status, body = self._http_caller(url, payload, key, self.timeout_giay)

                if status == 200:
                    self.model = model_hien_tai
                    van_ban = self._trich_van_ban_tu_phan_hoi(body)
                    nguon, truy_van = self._trich_nguon_tu_phan_hoi(body)
                    self.nguon_tham_khao_gan_nhat = nguon
                    self.truy_van_web_gan_nhat = truy_van
                    if tra_ve_nguon:
                        return van_ban, nguon
                    return van_ban

                loi_cuoi = (
                    f"HTTP {status} (model {model_hien_tai}, key #{self._chi_so_key + 1} {key_an}): "
                    f"{body[:240]}"
                )

                if bat_tim_kiem_web and self._la_loi_khong_ho_tro_tool_tim_kiem(status, body):
                    con_fallback = [
                        m
                        for m in hang_doi_model
                        if m not in models_da_thu and m not in self._models_khong_kha_dung
                    ]
                    if con_fallback:
                        model_ke_tiep = con_fallback[0]
                        print(
                            f"[Gemini] Model '{model_hien_tai}' khong ho tro google_search. "
                            f"Chuyen sang model du phong '{model_ke_tiep}'..."
                        )
                        hang_doi_model = con_fallback
                        chuyen_model = True
                        break

                if _la_loi_model_khong_hop_le(status, body):
                    self._models_khong_kha_dung.add(model_hien_tai)
                    con_fallback = [
                        m
                        for m in hang_doi_model
                        if m not in models_da_thu and m not in self._models_khong_kha_dung
                    ]
                    if con_fallback:
                        model_ke_tiep = con_fallback[0]
                        print(
                            f"[Gemini] Model '{model_hien_tai}' khong ton tai/khong hop le (HTTP {status}). "
                            f"Chuyen sang model van ban chuan '{model_ke_tiep}'..."
                        )
                        self.model = model_ke_tiep
                        hang_doi_model = con_fallback
                        chuyen_model = True
                        break

                    print(
                        f"[Gemini] Model '{model_hien_tai}' khong ton tai/khong hop le (HTTP {status}). "
                        "Dang tu do model van ban chuan kha dung..."
                    )
                    model_tu_do = self.tu_do_model_kha_dung(
                        loai_tru=self._models_khong_kha_dung | models_da_thu,
                        buoc_tai_lai=not da_tu_do_trong_luot,
                    )
                    da_tu_do_trong_luot = True

                    if model_tu_do and model_tu_do not in models_da_thu:
                        hang_doi_model = [model_tu_do]
                        for m_do in self._models_da_do:
                            if (
                                m_do != model_tu_do
                                and m_do not in hang_doi_model
                                and m_do not in models_da_thu
                                and m_do not in self._models_khong_kha_dung
                            ):
                                hang_doi_model.append(m_do)
                        chuyen_model = True
                        break

                    raise GeminiError(f"Loi khong the thu lai tu Gemini: {loi_cuoi}")

                if _la_loi_quota_hoac_tam_thoi(status, body):
                    co_loi_quota = True
                    la_429 = _la_loi_het_quota_429(status, body)
                    if la_429:
                        keys_bi_429.add(self._chi_so_key)
                    self._xoay_key()

                    con_fallback = [
                        m
                        for m in hang_doi_model
                        if m not in models_da_thu and m not in self._models_khong_kha_dung
                    ]
                    vong_hien_tai = (luot // so_key) + 1
                    het_vong = (luot + 1) % so_key == 0 or so_key == 1

                    # Khi tat ca API key deu tra ve 429 tren 1 model -> chuyen nhanh sau 2.0s (KHONG lap 3 vong dai)
                    if len(keys_bi_429) >= so_key:
                        if con_fallback:
                            model_ke_tiep = con_fallback[0]
                            thoi_gian_cho_429 = self.nghi_chuyen_model_429_giay
                            print(
                                f"[Gemini] Model '{model_hien_tai}' het quota (429) tren tat ca {so_key} API key. "
                                f"Cho {thoi_gian_cho_429:.1f}s roi chuyen ngay sang model du phong '{model_ke_tiep}'..."
                            )
                            self._sleep(thoi_gian_cho_429)
                            self.model = model_ke_tiep
                            hang_doi_model = con_fallback
                            chuyen_model = True
                            break
                        # Het sach fallback va tat ca key deu 429 -> thoat ngay (de ha cap grounding hoac bao QuotaError)
                        break

                    nhan_loi = (
                        f"rate limit/quota ({status})"
                        if la_429
                        else (f"qua tai server ({status})" if status in MA_LOI_QUA_TAI_SERVER else f"tam thoi ({status})")
                    )
                    if het_vong:
                        thoi_gian_cho = self._tinh_thoi_gian_cho_het_vong(vong_hien_tai)
                        if vong_hien_tai < so_vong:
                            print(
                                f"[Gemini] Het vong {vong_hien_tai}/{so_vong} tren model '{model_hien_tai}' "
                                f"van gap loi {nhan_loi} -> nghi {thoi_gian_cho:.1f}s truoc khi thu vong "
                                f"{vong_hien_tai + 1}/{so_vong} (key #{self._chi_so_key + 1}/{so_key})..."
                            )
                            self._sleep(thoi_gian_cho)
                        elif con_fallback or (bat_tim_kiem_web and cho_phep_ha_cap_khong_tim_kiem):
                            print(
                                f"[Gemini] Het vong cuoi {vong_hien_tai}/{so_vong} tren model '{model_hien_tai}' "
                                f"van gap loi {nhan_loi} -> nghi {thoi_gian_cho:.1f}s truoc khi chuyen phuong an du phong..."
                            )
                            self._sleep(thoi_gian_cho)
                    else:
                        thoi_gian_cho = self.nghi_doi_key_giay
                        print(
                            f"[Gemini] Gap loi {nhan_loi} o model '{model_hien_tai}' "
                            f"(vong {vong_hien_tai}/{so_vong}), xoay sang key #{self._chi_so_key + 1}/{so_key}, "
                            f"cho {thoi_gian_cho:.1f}s..."
                        )
                        self._sleep(thoi_gian_cho)
                    continue

                raise GeminiError(f"Loi khong the thu lai tu Gemini: {loi_cuoi}")

            if not chuyen_model:
                con_fallback = [
                    m
                    for m in hang_doi_model
                    if m not in models_da_thu and m not in self._models_khong_kha_dung
                ]
                if con_fallback:
                    model_ke_tiep = con_fallback[0]
                    print(
                        f"[Gemini] Model '{model_hien_tai}' that bai sau {so_vong} vong ({tong_luot_thu_moi_model} luot thu). "
                        f"Chuyen sang model du phong '{model_ke_tiep}'..."
                    )
                    self.model = model_ke_tiep
                    hang_doi_model = con_fallback

        if co_loi_quota:
            if bat_tim_kiem_web and cho_phep_ha_cap_khong_tim_kiem:
                self._google_search_het_quota = True
                print(
                    "[Gemini] Google Search Grounding gap loi quota/qua tai (429/503) tren tat ca key/model. "
                    f"Tu dong ha cap goi lai model '{model_ban_dau}' khong dung tool google_search..."
                )
                self.model = model_ban_dau
                return self._goi_generate_content(
                    parts=parts,
                    system_instruction=system_instruction,
                    nhiet_do=nhiet_do,
                    yeu_cau_json=yeu_cau_json,
                    max_output_tokens=max_output_tokens,
                    so_vong_toi_da=so_vong,
                    bat_tim_kiem_web=False,
                    tra_ve_nguon=tra_ve_nguon,
                    cho_phep_ha_cap_khong_tim_kiem=False,
                )
            raise GeminiQuotaError(
                f"Tat ca {so_key} API key Gemini va cac model ({' -> '.join(thu_tu_models_da_thu)}) "
                f"deu gap loi quota/tam thoi. Loi cuoi: {loi_cuoi}"
            )
        raise GeminiError(f"Khong the goi Gemini API. Loi cuoi: {loi_cuoi}")

    def tao_van_ban(
        self,
        prompt: str,
        system_instruction: str | None = None,
        nhiet_do: float = 0.75,
        yeu_cau_json: bool = False,
        max_output_tokens: int = 8192,
        so_vong_toi_da: int | None = None,
        bat_tim_kiem_web: bool = False,
        tra_ve_nguon: bool = False,
        cho_phep_ha_cap_khong_tim_kiem: bool = True,
    ) -> str | tuple[str, list[dict[str, str]]]:
        """Goi Gemini API, tu dong xoay key, tu do model khi 404/400, chuyen fallback khi 429 va ho tro Google Search Grounding."""
        return self._goi_generate_content(
            parts=[{"text": prompt}],
            system_instruction=system_instruction,
            nhiet_do=nhiet_do,
            yeu_cau_json=yeu_cau_json,
            max_output_tokens=max_output_tokens,
            so_vong_toi_da=so_vong_toi_da,
            bat_tim_kiem_web=bat_tim_kiem_web,
            tra_ve_nguon=tra_ve_nguon,
            cho_phep_ha_cap_khong_tim_kiem=cho_phep_ha_cap_khong_tim_kiem,
        )

    @staticmethod
    def _tao_parts_anh_inline(
        duong_dan_anh: Path | str | list[Path | str],
        mime_type: str | None = None,
    ) -> list[dict[str, Any]]:
        """Doc 1 hoac nhieu file anh PNG/JPEG sang danh sach parts inlineData base64 cho Gemini Vision."""
        ds_path = (
            [Path(p) for p in duong_dan_anh]
            if isinstance(duong_dan_anh, (list, tuple))
            else [Path(duong_dan_anh)]
        )
        if not ds_path:
            raise ValueError("Can truyen it nhat 1 duong dan anh cho Gemini Vision.")
        parts_anh: list[dict[str, Any]] = []
        for p in ds_path:
            if not p.exists():
                raise FileNotFoundError(f"Khong tim thay file anh cho Gemini Vision: {p}")
            du_lieu_bytes = p.read_bytes()
            if not du_lieu_bytes:
                raise ValueError(f"File anh rong: {p}")
            mt = mime_type
            if not mt:
                doan_mime, _ = mimetypes.guess_type(str(p))
                mt = doan_mime if (doan_mime and doan_mime.startswith("image/")) else "image/png"
            b64 = base64.b64encode(du_lieu_bytes).decode("ascii")
            parts_anh.append(
                {
                    "inlineData": {
                        "mimeType": mt,
                        "data": b64,
                    }
                }
            )
        return parts_anh

    def tao_van_ban_voi_anh(
        self,
        prompt: str,
        duong_dan_anh: Path | str | list[Path | str],
        mime_type: str | None = None,
        system_instruction: str | None = None,
        nhiet_do: float = 0.3,
        yeu_cau_json: bool = False,
        max_output_tokens: int = 8192,
        so_vong_toi_da: int | None = None,
    ) -> str:
        """Goi Gemini Vision voi 1 hoac nhieu anh (base64 inlineData), dung chung co che xoay key & fallback model."""
        parts = [{"text": prompt}] + self._tao_parts_anh_inline(duong_dan_anh, mime_type=mime_type)
        kq = self._goi_generate_content(
            parts=parts,
            system_instruction=system_instruction,
            nhiet_do=nhiet_do,
            yeu_cau_json=yeu_cau_json,
            max_output_tokens=max_output_tokens,
            so_vong_toi_da=so_vong_toi_da,
            bat_tim_kiem_web=False,
            tra_ve_nguon=False,
        )
        assert isinstance(kq, str)
        return kq

    def tao_json_voi_anh(
        self,
        prompt: str,
        duong_dan_anh: Path | str | list[Path | str],
        mime_type: str | None = None,
        system_instruction: str | None = None,
        nhiet_do: float = 0.25,
        max_output_tokens: int = 8192,
        so_lan_thu_lai_json: int = 2,
    ) -> Any:
        """Goi Gemini Vision yeu cau tra ve JSON hop le (co lam sach markdown va thu lai khi loi cu phap)."""
        prompt_hien_tai = prompt
        loi_gan_nhat: Exception | None = None
        gioi_han_token = max(1024, int(max_output_tokens))

        for lan in range(so_lan_thu_lai_json + 1):
            try:
                raw = self.tao_van_ban_voi_anh(
                    prompt=prompt_hien_tai,
                    duong_dan_anh=duong_dan_anh,
                    mime_type=mime_type,
                    system_instruction=system_instruction,
                    nhiet_do=nhiet_do if lan == 0 else max(0.1, nhiet_do - 0.1 * lan),
                    yeu_cau_json=True,
                    max_output_tokens=gioi_han_token,
                )
                return parse_json_an_toan(raw)
            except (json.JSONDecodeError, ValueError, GeminiError) as err:
                if isinstance(err, GeminiQuotaError):
                    raise
                if isinstance(err, GeminiError) and "noi dung rong" not in str(err).lower():
                    raise
                loi_gan_nhat = err
                if lan < so_lan_thu_lai_json:
                    gioi_han_token = min(32768, max(gioi_han_token * 2, 8192))
                    prompt_hien_tai = (
                        f"{prompt}\n\n"
                        f"LUU Y BAT BUOC: Lan tra loi truoc bi loi JSON ({err}). "
                        "Hay tra ve DUY NHAT 1 doi tuong JSON hop le 100%, khong boc markdown."
                    )

        raise GeminiError(
            f"Khong the parse JSON hop le tu Gemini Vision sau {so_lan_thu_lai_json + 1} lan: {loi_gan_nhat}"
        )

    def tao_json(
        self,
        prompt: str,
        system_instruction: str | None = None,
        nhiet_do: float = 0.7,
        max_output_tokens: int = 16384,
        so_lan_thu_lai_json: int = 2,
        bat_tim_kiem_web: bool = False,
        tra_ve_nguon: bool = False,
    ) -> Any:
        """Goi Gemini yeu cau tra ve JSON, tu lam sach, thu lai toi da 2 lan (tu tang max_output_tokens neu cat cut) va ho tro Google Search Grounding."""
        prompt_hien_tai = prompt
        loi_gan_nhat: Exception | None = None
        nguon_gop: list[dict[str, str]] = []
        url_da_co: set[str] = set()
        gioi_han_token = max(1024, int(max_output_tokens))

        for lan in range(so_lan_thu_lai_json + 1):
            try:
                ket_qua_raw = self.tao_van_ban(
                    prompt=prompt_hien_tai,
                    system_instruction=system_instruction,
                    nhiet_do=nhiet_do if lan == 0 else max(0.2, nhiet_do - 0.25 * lan),
                    yeu_cau_json=True,
                    max_output_tokens=gioi_han_token,
                    bat_tim_kiem_web=bat_tim_kiem_web,
                    tra_ve_nguon=True,
                )
                assert isinstance(ket_qua_raw, tuple)
                raw, nguon_lan = ket_qua_raw
                for item in nguon_lan:
                    u = item.get("url", "")
                    if u and u not in url_da_co:
                        url_da_co.add(u)
                        nguon_gop.append(item)

                parsed = parse_json_an_toan(raw)
                self.nguon_tham_khao_gan_nhat = nguon_gop
                if tra_ve_nguon:
                    return parsed, nguon_gop
                return parsed
            except (json.JSONDecodeError, ValueError, GeminiError) as err:
                if isinstance(err, GeminiQuotaError):
                    raise
                if isinstance(err, GeminiError) and "noi dung rong" not in str(err).lower():
                    raise
                loi_gan_nhat = err
                if lan < so_lan_thu_lai_json:
                    gioi_han_token = min(65536, max(gioi_han_token * 2, 16384))
                    print(
                        f"[Gemini] JSON loi cu phap / rong (lan {lan + 1}/{so_lan_thu_lai_json}), "
                        f"dang thu lai voi maxOutputTokens={gioi_han_token}..."
                    )
                    prompt_hien_tai = (
                        f"{prompt}\n\n"
                        "LUU Y BAT BUOC: Lan tra loi truoc bi loi cu phap JSON hoac het token "
                        f"({err}). Hay tra ve DUY NHAT 1 doi tuong JSON hop le 100%, ngan gon dung cau truc, "
                        "khong kem giai thich, khong boc markdown, thoat ky tu \\\\ dung chuan (dac biet trong cong thuc LaTeX)."
                    )

        raise GeminiError(
            f"Khong the parse JSON hop le sau {so_lan_thu_lai_json + 1} lan goi Gemini: {loi_gan_nhat}"
        )
