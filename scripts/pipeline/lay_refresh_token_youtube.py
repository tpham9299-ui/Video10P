# -*- coding: utf-8 -*-
"""Tien ich chay 1 lan tren may ca nhan de lay YOUTUBE_REFRESH_TOKEN trong 30 giay bang Python stdlib."""

from __future__ import annotations

import argparse
import html
import http.server
import json
import os
import secrets
import sys
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path
from typing import Any, Callable

GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.gemini_client import tai_env

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
YOUTUBE_SCOPES = (
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
)
PORT_MAC_DINH = 8765


def tao_url_xac_thuc_google(
    client_id: str,
    redirect_uri: str,
    state: str,
    scopes: tuple[str, ...] = YOUTUBE_SCOPES,
) -> str:
    """Tao duong dan dang nhap Google OAuth2 voi access_type=offline & prompt=consent."""
    params = {
        "client_id": str(client_id).strip(),
        "redirect_uri": str(redirect_uri).strip(),
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "true",
        "state": str(state).strip(),
    }
    return f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"


def doi_code_lay_tokens(
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str,
    urlopen_fn: Callable[..., Any] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    """Doi authorization code lay refresh_token va access_token tu Google OAuth2."""
    payload = urllib.parse.urlencode(
        {
            "client_id": str(client_id).strip(),
            "client_secret": str(client_secret).strip(),
            "code": str(code).strip(),
            "redirect_uri": str(redirect_uri).strip(),
            "grant_type": "authorization_code",
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        GOOGLE_TOKEN_URL,
        data=payload,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "User-Agent": "Video10P-OAuthHelper/1.0",
        },
        method="POST",
    )
    opener = urlopen_fn or urllib.request.urlopen
    try:
        with opener(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as err:
        err_body = err.read().decode("utf-8", errors="replace") if err.fp else str(err)
        raise RuntimeError(f"Google OAuth tra ve HTTP {err.code}: {err_body[:360]}") from err
    except urllib.error.URLError as err:
        raise RuntimeError(f"Khong ket noi duoc toi Google OAuth: {err}") from err

    data = json.loads(raw)
    if not isinstance(data, dict) or not data.get("refresh_token"):
        raise RuntimeError(
            "Google khong tra ve `refresh_token`. Hay thu thu hoi quyen ung dung tai "
            "https://myaccount.google.com/permissions roi chay lai lenh nay. "
            f"Phan hoi: {raw[:260]}"
        )
    return data


def _doc_thong_tin_client(
    client_id_arg: str = "",
    client_secret_arg: str = "",
    duong_dan_env: Path | str | None = None,
) -> tuple[str, str]:
    tu_env = tai_env(duong_dan_env)
    cid = (
        str(client_id_arg or "").strip()
        or str(os.environ.get("YOUTUBE_CLIENT_ID") or "").strip()
        or str(tu_env.get("YOUTUBE_CLIENT_ID") or "").strip()
    )
    csec = (
        str(client_secret_arg or "").strip()
        or str(os.environ.get("YOUTUBE_CLIENT_SECRET") or "").strip()
        or str(tu_env.get("YOUTUBE_CLIENT_SECRET") or "").strip()
    )
    if not cid:
        cid = input("Nhap YOUTUBE_CLIENT_ID (tu Google Cloud Console): ").strip()
    if not csec:
        csec = input("Nhap YOUTUBE_CLIENT_SECRET (tu Google Cloud Console): ").strip()
    return cid, csec


def cho_nhan_ma_xac_thuc_cuc_bo(
    host: str,
    port: int,
    state_ky_vong: str,
    timeout_giay: int = 300,
) -> str:
    """Khoi dong HTTP server cuc bo 1 lan de hung callback OAuth2 `?code=...&state=...`."""
    ket_qua: dict[str, str] = {"code": "", "error": ""}
    da_het_gio = {"flag": False}

    class _TimeoutHTTPServer(http.server.HTTPServer):
        def handle_timeout(self) -> None:
            da_het_gio["flag"] = True

    class _OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:
            return

        def do_GET(self) -> None:  # noqa: N802
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
                return
            qs = urllib.parse.parse_qs(parsed.query)
            err = (qs.get("error") or [""])[0].strip()
            code = (qs.get("code") or [""])[0].strip()
            state = (qs.get("state") or [""])[0].strip()

            if err:
                ket_qua["error"] = f"Nguoi dung tu choi hoac Google bao loi: {err}"
                self._tra_html(
                    400,
                    "Xác thực thất bại",
                    f"Google trả về lỗi: <b>{html.escape(err)}</b>. Hãy quay lại cửa sổ dòng lệnh.",
                )
                return

            if not code:
                self._tra_html(
                    200,
                    "Đang chờ xác thực",
                    "Trình duyệt đã mở trang callback cục bộ nhưng chưa có mã xác thực.",
                )
                return

            if state != state_ky_vong:
                ket_qua["error"] = "Ma `state` khong khop (nghi ngo callback khong hop le)."
                self._tra_html(
                    400,
                    "Lỗi bảo mật state",
                    "Mã state không khớp. Hãy chạy lại tiện ích trong cửa sổ dòng lệnh.",
                )
                return

            ket_qua["code"] = code
            self._tra_html(
                200,
                "Đã nhận mã xác thực YouTube!",
                "Hoàn tất bước đăng nhập Google. Bạn có thể đóng tab trình duyệt này và quay lại cửa sổ dòng lệnh để sao chép <b>YOUTUBE_REFRESH_TOKEN</b>.",
            )

        def _tra_html(self, status_code: int, tieu_de: str, noi_dung: str) -> None:
            trang = (
                "<!doctype html><html lang='vi'><head><meta charset='utf-8'>"
                f"<title>{html.escape(tieu_de)}</title>"
                "<style>body{font-family:system-ui,sans-serif;max-width:600px;margin:48px auto;padding:24px;"
                "line-height:1.6;color:#111827;background:#f8fafc;}"
                ".box{background:#fff;border:1px solid #cbd5e1;border-radius:12px;padding:24px;}</style>"
                f"</head><body><div class='box'><h2>{html.escape(tieu_de)}</h2><p>{noi_dung}</p></div></body></html>"
            ).encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(trang)))
            self.end_headers()
            self.wfile.write(trang)

    server = _TimeoutHTTPServer((host, port), _OAuthCallbackHandler)
    server.timeout = float(timeout_giay)
    try:
        while not ket_qua["code"] and not ket_qua["error"] and not da_het_gio["flag"]:
            server.handle_request()
    finally:
        server.server_close()

    if ket_qua["error"]:
        raise RuntimeError(ket_qua["error"])
    if not ket_qua["code"]:
        raise TimeoutError(f"Het thoi gian cho ({timeout_giay}s) ma chua nhan duoc callback tu Google.")
    return ket_qua["code"]


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Lay YOUTUBE_REFRESH_TOKEN trong 30 giay bang trinh duyet cuc bo (thuan Python stdlib)."
    )
    parser.add_argument("--client-id", default="", help="YOUTUBE_CLIENT_ID (mac dinh doc tu .env/env hoac nhap tay).")
    parser.add_argument(
        "--client-secret",
        default="",
        help="YOUTUBE_CLIENT_SECRET (mac dinh doc tu .env/env hoac nhap tay).",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Dia chi lang nghe callback cuc bo (mac dinh: 127.0.0.1).")
    parser.add_argument("--port", type=int, default=PORT_MAC_DINH, help=f"Cong callback cuc bo (mac dinh: {PORT_MAC_DINH}).")
    parser.add_argument(
        "--khong-tu-mo-trinh-duyet",
        action="store_true",
        help="Chi in link dang nhap ra man hinh de ban tu copy mo tren trinh duyet.",
    )
    parser.add_argument("--env", default="", help="Duong dan file .env tuy chinh.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    duong_dan_env = Path(args.env) if args.env else None
    client_id, client_secret = _doc_thong_tin_client(
        client_id_arg=args.client_id,
        client_secret_arg=args.client_secret,
        duong_dan_env=duong_dan_env,
    )
    if not client_id or not client_secret:
        print("[LOI] Can cung cap day du YOUTUBE_CLIENT_ID va YOUTUBE_CLIENT_SECRET.")
        return 2

    redirect_uri = f"http://{args.host}:{int(args.port)}/oauth2callback"
    state = secrets.token_urlsafe(24)
    auth_url = tao_url_xac_thuc_google(client_id=client_id, redirect_uri=redirect_uri, state=state)

    print("=" * 76)
    print("TIEN ICH LAY YOUTUBE_REFRESH_TOKEN (CHAY 1 LAN TREN MAY CA NHAN)")
    print("=" * 76)
    print(f"Redirect URI cuc bo: {redirect_uri}")
    print("Neu Google Cloud Client la loai 'Desktop app', Google tu chap nhan redirect URI nay.")
    print("Neu la 'Web application', hay them dung Redirect URI o tren vao Authorized redirect URIs.\n")
    print("Link dang nhap Google OAuth2:")
    print(auth_url)
    print()

    if not args.khong_tu_mo_trinh_duyet:
        try:
            webbrowser.open(auth_url)
            print("[OK] Da mo trinh duyet. Hay chon kenh YouTube va bam Cho phep (Allow)...")
        except Exception as err:
            print(f"[CANH BAO] Khong tu mo duoc trinh duyet ({err}). Hay copy link o tren mo thu cong.")
    else:
        print("Hay copy link o tren dan vao trinh duyet de dang nhap va cho phep...")

    code = cho_nhan_ma_xac_thuc_cuc_bo(host=args.host, port=int(args.port), state_ky_vong=state)
    tokens = doi_code_lay_tokens(
        client_id=client_id,
        client_secret=client_secret,
        code=code,
        redirect_uri=redirect_uri,
    )
    refresh_token = str(tokens["refresh_token"]).strip()

    print("\n" + "=" * 76)
    print("[THANH CONG] DA LAY DUOC YOUTUBE_REFRESH_TOKEN!")
    print("=" * 76)
    print("\n1) Dan 3 dong sau vao file `.env` (neu chay tu dong tren may ca nhan):")
    print(f"YOUTUBE_CLIENT_ID={client_id}")
    print(f"YOUTUBE_CLIENT_SECRET={client_secret}")
    print(f"YOUTUBE_REFRESH_TOKEN={refresh_token}")
    print("\n2) Hoac tao 3 Repository Secrets tren GitHub")
    print("   (Settings -> Secrets and variables -> Actions -> New repository secret):")
    print("   - YOUTUBE_CLIENT_ID")
    print("   - YOUTUBE_CLIENT_SECRET")
    print("   - YOUTUBE_REFRESH_TOKEN")
    print("\n[LUU Y BAO MAT] Tuyet doi KHONG commit Refresh Token hoac file .env len Git!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
