# -*- coding: utf-8 -*-
"""Bo goi Gemini REST API xoay vong nhieu API key va parse JSON an toan."""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

MAC_DINH_MODEL = "gemini-2.5-flash"
GEMINI_ENDPOINT_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
MA_LOI_XOAY_KEY = {429, 500, 502, 503, 504}


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


def lay_cau_hinh_gemini(
    duong_dan_env: Path | str | None = None,
    env_override: dict[str, str] | None = None,
) -> tuple[list[str], str]:
    """Lay danh sach GEMINI_API_KEYS (fallback GEMINI_API_KEY) va GEMINI_MODEL."""
    tu_file = tai_env(duong_dan_env)
    nguon: dict[str, str] = {}
    nguon.update(tu_file)
    for k in ("GEMINI_API_KEYS", "GEMINI_API_KEY", "GEMINI_MODEL"):
        if os.environ.get(k):
            nguon[k] = os.environ[k]
    if env_override:
        nguon.update(env_override)

    raw_keys = nguon.get("GEMINI_API_KEYS", "").strip()
    if not raw_keys:
        raw_keys = nguon.get("GEMINI_API_KEY", "").strip()

    keys: list[str] = []
    for item in raw_keys.split(","):
        k = item.strip()
        if k and k not in keys:
            keys.append(k)

    model = nguon.get("GEMINI_MODEL", "").strip() or MAC_DINH_MODEL
    return keys, model


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


def _la_loi_quota_hoac_tam_thoi(status_code: int | None, body_text: str) -> bool:
    if status_code in MA_LOI_XOAY_KEY:
        return True
    thap = body_text.lower()
    tu_khoa = (
        "resource_exhausted",
        "quota",
        "rate limit",
        "too many requests",
        "overloaded",
        "unavailable",
    )
    return any(tk in thap for tk in tu_khoa)


class GeminiClient:
    """Client goi Gemini co xoay vong API key, backoff va thu lai JSON."""

    def __init__(
        self,
        api_keys: list[str] | None = None,
        model: str | None = None,
        duong_dan_env: Path | str | None = None,
        timeout_giay: int = 120,
        backoff_co_so: float = 1.5,
        http_caller: Callable[[str, dict[str, Any], str, int], tuple[int, str]] | None = None,
        sleep_fn: Callable[[float], None] | None = None,
    ) -> None:
        env_keys, env_model = lay_cau_hinh_gemini(duong_dan_env=duong_dan_env)
        self.api_keys = list(api_keys) if api_keys is not None else env_keys
        self.model = model or env_model
        self.timeout_giay = timeout_giay
        self.backoff_co_so = backoff_co_so
        self._chi_so_key = 0
        self._http_caller = http_caller or self._goi_http_mac_dinh
        self._sleep = sleep_fn or time.sleep

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

    @staticmethod
    def _trich_van_ban_tu_phan_hoi(body: str) -> str:
        du_lieu = json.loads(body)
        candidates = du_lieu.get("candidates") or []
        if not candidates:
            raise GeminiError(f"Gemini tra ve khong co candidates: {body[:300]}")
        parts = candidates[0].get("content", {}).get("parts") or []
        doan: list[str] = []
        for p in parts:
            if isinstance(p, dict) and isinstance(p.get("text"), str):
                doan.append(p["text"])
        ket_qua = "\n".join(doan).strip()
        if not ket_qua:
            raise GeminiError(f"Gemini tra ve noi dung rong: {body[:300]}")
        return ket_qua

    def tao_van_ban(
        self,
        prompt: str,
        system_instruction: str | None = None,
        nhiet_do: float = 0.75,
        yeu_cau_json: bool = False,
        max_output_tokens: int = 8192,
        so_vong_toi_da: int = 2,
    ) -> str:
        """Goi Gemini API, tu dong xoay vong key + backoff khi gap 429/503/quota."""
        url = GEMINI_ENDPOINT_TEMPLATE.format(model=self.model)
        generation_config: dict[str, Any] = {
            "temperature": nhiet_do,
            "maxOutputTokens": max_output_tokens,
        }
        if yeu_cau_json:
            generation_config["responseMimeType"] = "application/json"

        payload: dict[str, Any] = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": generation_config,
        }
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }

        so_key = len(self.api_keys)
        tong_luot_thu = so_key * max(1, so_vong_toi_da)
        loi_cuoi = ""

        for luot in range(tong_luot_thu):
            key = self.api_keys[self._chi_so_key]
            key_an = f"...{key[-4:]}" if len(key) >= 4 else "***"
            status, body = self._http_caller(url, payload, key, self.timeout_giay)

            if status == 200:
                return self._trich_van_ban_tu_phan_hoi(body)

            loi_cuoi = f"HTTP {status} (key #{self._chi_so_key + 1} {key_an}): {body[:240]}"
            if _la_loi_quota_hoac_tam_thoi(status, body):
                self._xoay_key()
                vong_hien_tai = (luot // so_key) + 1
                # Neu xoay qua key khac trong cung vong -> nghi ngan; sang vong moi -> backoff tang dan
                thoi_gian_cho = (
                    self.backoff_co_so * (2 ** (vong_hien_tai - 1))
                    if (luot + 1) % so_key == 0 or so_key == 1
                    else 0.4
                )
                print(
                    f"[Gemini] Gap loi tam thoi/quota ({status}), xoay sang key #{self._chi_so_key + 1}/{so_key}, cho {thoi_gian_cho:.1f}s..."
                )
                self._sleep(thoi_gian_cho)
                continue

            raise GeminiError(f"Loi khong the thu lai tu Gemini: {loi_cuoi}")

        raise GeminiQuotaError(
            f"Tat ca {so_key} API key Gemini deu gap loi quota/tam thoi sau {tong_luot_thu} luot thu. Loi cuoi: {loi_cuoi}"
        )

    def tao_json(
        self,
        prompt: str,
        system_instruction: str | None = None,
        nhiet_do: float = 0.7,
        max_output_tokens: int = 8192,
        so_lan_thu_lai_json: int = 2,
    ) -> Any:
        """Goi Gemini yeu cau tra ve JSON, tu lam sach va thu lai toi da 2 lan neu JSON loi."""
        prompt_hien_tai = prompt
        loi_gan_nhat: Exception | None = None

        for lan in range(so_lan_thu_lai_json + 1):
            raw = self.tao_van_ban(
                prompt=prompt_hien_tai,
                system_instruction=system_instruction,
                nhiet_do=nhiet_do if lan == 0 else max(0.2, nhiet_do - 0.25 * lan),
                yeu_cau_json=True,
                max_output_tokens=max_output_tokens,
            )
            try:
                return parse_json_an_toan(raw)
            except (json.JSONDecodeError, ValueError) as err:
                loi_gan_nhat = err
                if lan < so_lan_thu_lai_json:
                    print(
                        f"[Gemini] JSON loi cu phap (lan {lan + 1}/{so_lan_thu_lai_json}), dang yeu cau sinh lai JSON sach..."
                    )
                    prompt_hien_tai = (
                        f"{prompt}\n\n"
                        "LUU Y BAT BUOC: Lan tra loi truoc bi loi cu phap JSON "
                        f"({err}). Hay tra ve DUY NHAT 1 doi tuong JSON hop le 100%, "
                        "khong kem giai thich, khong boc markdown, thoat ky tu \\\\ dung chuan (dac biet trong cong thuc LaTeX)."
                    )

        raise GeminiError(
            f"Khong the parse JSON hop le sau {so_lan_thu_lai_json + 1} lan goi Gemini: {loi_gan_nhat}"
        )
