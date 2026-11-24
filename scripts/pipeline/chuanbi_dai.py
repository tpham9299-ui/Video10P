# -*- coding: utf-8 -*-
"""Tao giong doc Edge TTS co cache SHA-256, do thoi luong bang ffprobe, tinh frame 30fps va chia phu de."""

from __future__ import annotations

import argparse
import asyncio
import copy
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.chuan_hoa_doc_toan import chuan_hoa_doc_toan
from scripts.pipeline.gemini_client import tai_env

MAC_DINH_VOICE = "vi-VN-NamMinhNeural"
MAC_DINH_RATE = "+0%"
MAC_DINH_PITCH = "+0Hz"
MAC_DINH_FPS = 30
NGHI_GIUA_CANH_GIAY = 0.25
NGHI_CHUYEN_HOI_GIAY = 0.75
NGUONG_TOI_THIEU_GIAY = 600.0


def bam_noi_dung_tts(van_ban_doc: str, voice: str, rate: str = "+0%", pitch: str = "+0Hz") -> str:
    """Tinh SHA-256 cho cap (giong, toc do, cao do, van ban da chuan hoa)."""
    payload = f"{voice}|{rate}|{pitch}|{van_ban_doc}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def chia_phu_de(loi_thoai: str, max_ky_tu: int = 86) -> list[str]:
    """Chia loi thoai thanh cac dong phu de gon dep cho khung hinh 16:9."""
    sach = re.sub(r"\s+", " ", (loi_thoai or "").strip())
    if not sach:
        return []
    if len(sach) <= max_ky_tu:
        return [sach]

    # Uu tien tach theo cau / ve cau (. ! ? ; : —)
    cac_cau = [c.strip() for c in re.split(r"(?<=[.!?;:])\s+|\s+—\s+", sach) if c.strip()]
    ket_qua: list[str] = []

    def _cat_theo_tu(doan: str) -> list[str]:
        if len(doan) <= max_ky_tu:
            return [doan]
        # Thu tach theo dau phay truoc neu hop ly
        ve_phay = [v.strip() for v in re.split(r"(?<=,)\s+", doan) if v.strip()]
        if len(ve_phay) > 1 and all(len(v) <= max_ky_tu for v in ve_phay):
            gom: list[str] = []
            buf = ""
            for v in ve_phay:
                if not buf:
                    buf = v
                elif len(buf) + 1 + len(v) <= max_ky_tu:
                    buf = f"{buf} {v}"
                else:
                    gom.append(buf)
                    buf = v
            if buf:
                gom.append(buf)
            return gom

        tu_list = doan.split(" ")
        dong_list: list[str] = []
        buf = ""
        for tu in tu_list:
            if not buf:
                buf = tu
            elif len(buf) + 1 + len(tu) <= max_ky_tu:
                buf = f"{buf} {tu}"
            else:
                dong_list.append(buf)
                buf = tu
        if buf:
            dong_list.append(buf)
        return dong_list

    for cau in cac_cau:
        for manh in _cat_theo_tu(cau):
            if ket_qua and len(ket_qua[-1]) + 1 + len(manh) <= max_ky_tu:
                ket_qua[-1] = f"{ket_qua[-1]} {manh}"
            else:
                ket_qua.append(manh)

    return ket_qua


def do_thoi_luong_ffprobe(duong_dan_audio: Path) -> float:
    """Do thoi luong chinh xac (giay) cua file audio bang ffprobe."""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(duong_dan_audio),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)
    if res.returncode != 0:
        raise RuntimeError(
            f"ffprobe that bai cho {duong_dan_audio}: {res.stderr.strip() or res.stdout.strip()}"
        )
    try:
        giay = float(res.stdout.strip())
        if not math.isfinite(giay) or giay <= 0:
            raise ValueError(f"Gia tri duration khong hop le: {res.stdout!r}")
        return giay
    except ValueError as err:
        raise RuntimeError(f"Khong doc duoc thoi luong tu ffprobe cho {duong_dan_audio}: {err}") from err


def _dieu_chinh_moc_noi_bo_canh(canh: dict[str, Any], tong_frame_canh: int) -> None:
    """Dam bao tuFrame/thoiLuong cua hieu ung & cong thuc nam gon trong thoi luong canh."""
    gioi_han_bat_dau = max(0, tong_frame_canh - 20)

    if isinstance(canh.get("hieuUngHoatHinh"), list):
        for hu in canh["hieuUngHoatHinh"]:
            tu = min(int(hu.get("tuFrame", 0)), gioi_han_bat_dau)
            hu["tuFrame"] = max(0, tu)
            con_lai = max(15, tong_frame_canh - hu["tuFrame"])
            hu["thoiLuong"] = min(int(hu.get("thoiLuong", 75)), con_lai)

    if isinstance(canh.get("loiBinhHaiHuoc"), dict) and "tuFrame" in canh["loiBinhHaiHuoc"]:
        canh["loiBinhHaiHuoc"]["tuFrame"] = min(
            max(0, int(canh["loiBinhHaiHuoc"]["tuFrame"])),
            gioi_han_bat_dau,
        )

    if isinstance(canh.get("congThucLatex"), list) and canh["congThucLatex"]:
        so_ct = len(canh["congThucLatex"])
        buoc = max(15, min(40, (tong_frame_canh - 30) // max(1, so_ct)))
        for idx, ct in enumerate(canh["congThucLatex"]):
            mac_dinh = idx * buoc
            tu = int(ct.get("tuFrame", mac_dinh))
            if tu > gioi_han_bat_dau:
                tu = min(gioi_han_bat_dau, mac_dinh)
            ct["tuFrame"] = max(0, tu)


def tinh_toan_khung_hinh(
    du_lieu: dict[str, Any],
    thoi_luong_theo_canh: dict[str, float],
    slug: str,
    fps: int = MAC_DINH_FPS,
    nghi_giua_canh: float = NGHI_GIUA_CANH_GIAY,
    nghi_chuyen_hoi: float = NGHI_CHUYEN_HOI_GIAY,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Tinh tuFrame/denFrame lien mach o 30fps, gan audioSrc va chia phuDe[].
    Tra ve (du_lieu_render, thong_ke).
    """
    ket_qua = copy.deepcopy(du_lieu)
    ds_chuong = ket_qua.get("chuong") or []

    frame_hien_tai = 0
    tong_audio_giay = 0.0
    tong_canh = 0
    thong_ke_chuong: list[dict[str, Any]] = []

    for idx_ch, ch in enumerate(ds_chuong):
        ds_canh = ch.get("canh") or []
        frame_bat_dau_ch = frame_hien_tai
        for idx_c, canh in enumerate(ds_canh):
            canh_id = str(canh["id"])
            audio_giay = float(thoi_luong_theo_canh.get(canh_id, 4.0))
            la_cuoi_chuong = idx_c == len(ds_canh) - 1
            co_chuong_sau = idx_ch < len(ds_chuong) - 1
            khoang_nghi = nghi_chuyen_hoi if (la_cuoi_chuong and co_chuong_sau) else nghi_giua_canh

            tong_giay_canh = audio_giay + khoang_nghi
            so_frame = max(30, int(math.ceil(tong_giay_canh * fps)))

            canh["tuFrame"] = frame_hien_tai
            canh["denFrame"] = frame_hien_tai + so_frame
            canh["audioSrc"] = f"audio/{slug}/{canh_id}.mp3"

            # Chi tao lai phuDe neu chua co hoac de rong (van giu phuDe tuy chinh neu nguoi dung sua tay?
            # Luon chia tu loiThoai neu chua co phuDe, hoac cap nhat de dong bo 100% voi loiThoai moi nhat)
            canh["phuDe"] = chia_phu_de(canh.get("loiThoai", ""))
            _dieu_chinh_moc_noi_bo_canh(canh, so_frame)

            frame_hien_tai += so_frame
            tong_audio_giay += audio_giay
            tong_canh += 1

        thong_ke_chuong.append(
            {
                "id": ch.get("id", f"chuong_{idx_ch + 1}"),
                "tenChuong": ch.get("tenChuong", f"Hồi {idx_ch + 1}"),
                "soCanh": len(ds_canh),
                "tuFrame": frame_bat_dau_ch,
                "denFrame": frame_hien_tai,
                "giay": round((frame_hien_tai - frame_bat_dau_ch) / fps, 2),
            }
        )

    tong_frames = frame_hien_tai
    tong_giay = tong_frames / float(fps)
    thong_ke = {
        "tongChuong": len(ds_chuong),
        "tongCanh": tong_canh,
        "tongFrames": tong_frames,
        "tongGiay": round(tong_giay, 2),
        "tongPhut": round(tong_giay / 60.0, 2),
        "tongAudioGiay": round(tong_audio_giay, 2),
        "datTren10Phut": tong_giay >= NGUONG_TOI_THIEU_GIAY,
        "chuong": thong_ke_chuong,
    }
    return ket_qua, thong_ke


async def _tao_file_edge_tts(
    van_ban_doc: str,
    duong_dan_mp3: Path,
    voice: str,
    rate: str,
    pitch: str,
) -> None:
    try:
        import edge_tts
    except ImportError as err:
        raise RuntimeError(
            "Chua cai dat edge-tts. Hay chay: pip install -r requirements.txt"
        ) from err

    duong_dan_mp3.parent.mkdir(parents=True, exist_ok=True)
    comm = edge_tts.Communicate(text=van_ban_doc, voice=voice, rate=rate, pitch=pitch)
    await comm.save(str(duong_dan_mp3))


async def _sinh_audio_hang_loat(
    tac_vu: list[tuple[str, str, Path]],
    voice: str,
    rate: str,
    pitch: str,
    toi_da_dong_thoi: int = 4,
) -> None:
    sem = asyncio.Semaphore(max(1, toi_da_dong_thoi))

    async def _chay_mot(canh_id: str, van_ban_doc: str, duong_dan_mp3: Path) -> None:
        async with sem:
            for lan in range(3):
                try:
                    await _tao_file_edge_tts(van_ban_doc, duong_dan_mp3, voice, rate, pitch)
                    return
                except Exception as err:
                    if lan == 2:
                        raise RuntimeError(f"TTS loi o {canh_id} sau 3 lan thu: {err}") from err
                    await asyncio.sleep(1.5 * (lan + 1))

    await asyncio.gather(*(_chay_mot(cid, txt, p) for cid, txt, p in tac_vu))


def chuan_bi_audio_va_du_lieu_render(
    slug: str,
    duong_dan_nhap: Path | None = None,
    voice: str | None = None,
    rate: str = MAC_DINH_RATE,
    pitch: str = MAC_DINH_PITCH,
    fps: int = MAC_DINH_FPS,
    bo_cache: bool = False,
    thu_muc_du_lieu: Path | None = None,
    thu_muc_public: Path | None = None,
    tts_generator: Callable[[str, str, Path], None] | None = None,
    duration_prober: Callable[[Path], float] | None = None,
) -> tuple[Path, dict[str, Any]]:
    """
    Chay toan bo quy trinh TTS co cache SHA-256 -> ffprobe -> tinh frame 30fps -> xuat du_lieu_render.json.
    Ho tro inject `tts_generator` va `duration_prober` de unit-test offline.
    """
    env_cfg = tai_env()
    voice_dung = voice or env_cfg.get("TTS_VOICE") or MAC_DINH_VOICE

    base_du_lieu = (thu_muc_du_lieu or (GOC_DU_AN / "du_lieu")) / slug
    file_nhap = duong_dan_nhap or (base_du_lieu / "nhap_kich_ban.json")
    if not file_nhap.exists():
        raise FileNotFoundError(f"Khong tim thay kich ban nhap: {file_nhap}")

    du_lieu_nhap = json.loads(file_nhap.read_text(encoding="utf-8"))
    audio_dir = (thu_muc_public or (GOC_DU_AN / "public")) / "audio" / slug
    audio_dir.mkdir(parents=True, exist_ok=True)

    file_cache = base_du_lieu / "cache_audio.json"
    cache_cu: dict[str, Any] = {}
    if file_cache.exists() and not bo_cache:
        try:
            cache_cu = json.loads(file_cache.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache_cu = {}

    prober = duration_prober or do_thoi_luong_ffprobe
    can_sinh: list[tuple[str, str, Path, str]] = []
    thoi_luong_map: dict[str, float] = {}
    cache_moi: dict[str, Any] = {}
    so_hit_cache = 0

    tat_ca_canh = [c for ch in (du_lieu_nhap.get("chuong") or []) for c in (ch.get("canh") or [])]

    for canh in tat_ca_canh:
        canh_id = str(canh["id"])
        van_ban_doc = chuan_hoa_doc_toan(canh.get("loiThoai", ""))
        ma_hash = bam_noi_dung_tts(van_ban_doc, voice_dung, rate, pitch)
        file_mp3 = audio_dir / f"{canh_id}.mp3"

        ban_ghi = cache_cu.get(canh_id)
        if (
            not bo_cache
            and isinstance(ban_ghi, dict)
            and ban_ghi.get("hash") == ma_hash
            and file_mp3.exists()
            and file_mp3.stat().st_size > 0
        ):
            so_hit_cache += 1
            giay = float(ban_ghi.get("duration") or 0)
            if giay <= 0:
                giay = prober(file_mp3)
            thoi_luong_map[canh_id] = giay
            cache_moi[canh_id] = {
                "hash": ma_hash,
                "duration": round(giay, 4),
                "voice": voice_dung,
                "rate": rate,
                "pitch": pitch,
                "vanBanDoc": van_ban_doc,
            }
        else:
            can_sinh.append((canh_id, van_ban_doc, file_mp3, ma_hash))

    print(
        f"[TTS] Tong {len(tat_ca_canh)} canh | Dung lai cache: {so_hit_cache} | Can sinh moi: {len(can_sinh)} (giong: {voice_dung})"
    )

    if can_sinh:
        if tts_generator is not None:
            for canh_id, van_ban_doc, file_mp3, _ in can_sinh:
                file_mp3.parent.mkdir(parents=True, exist_ok=True)
                tts_generator(canh_id, van_ban_doc, file_mp3)
        else:
            asyncio.run(
                _sinh_audio_hang_loat(
                    [(cid, txt, p) for cid, txt, p, _ in can_sinh],
                    voice=voice_dung,
                    rate=rate,
                    pitch=pitch,
                )
            )

        for canh_id, van_ban_doc, file_mp3, ma_hash in can_sinh:
            giay = prober(file_mp3)
            thoi_luong_map[canh_id] = giay
            cache_moi[canh_id] = {
                "hash": ma_hash,
                "duration": round(giay, 4),
                "voice": voice_dung,
                "rate": rate,
                "pitch": pitch,
                "vanBanDoc": van_ban_doc,
            }

    file_cache.write_text(json.dumps(cache_moi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    du_lieu_render, thong_ke = tinh_toan_khung_hinh(
        du_lieu=du_lieu_nhap,
        thoi_luong_theo_canh=thoi_luong_map,
        slug=slug,
        fps=fps,
    )

    file_render = base_du_lieu / "du_lieu_render.json"
    file_render.write_text(
        json.dumps(du_lieu_render, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"[OK] Da xuat du lieu render: {file_render}")
    print(
        f"[Thong ke] {thong_ke['tongChuong']} hoi | {thong_ke['tongCanh']} canh | "
        f"{thong_ke['tongFrames']} frames | {thong_ke['tongGiay']:.2f}s ({thong_ke['tongPhut']:.2f} phut)"
    )
    if not thong_ke["datTren10Phut"]:
        thieu = NGUONG_TOI_THIEU_GIAY - thong_ke["tongGiay"]
        print(
            f"[CANH BAO] Tong thoi luong thuc te la {thong_ke['tongGiay']:.1f}s (< 600s / 10 phut, thieu {thieu:.1f}s)! "
            "Hay bo sung them canh hoac tang do dai loi thoai trong nhap_kich_ban.json roi chay lai chuanbi_dai.py."
        )

    return file_render, thong_ke


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tao giong doc TTS co cache SHA-256, do ffprobe va xuat du_lieu_render.json."
    )
    parser.add_argument("--slug", required=True, help="Ten slug du an trong du_lieu/<slug>/.")
    parser.add_argument("--input", default="", help="Duong dan tuy chinh toi nhap_kich_ban.json.")
    parser.add_argument("--giong", default="", help="Giong Edge TTS (mac dinh vi-VN-NamMinhNeural).")
    parser.add_argument("--toc-do", default=MAC_DINH_RATE, help="Toc do doc TTS (vd: +0%%, +5%%, -5%%).")
    parser.add_argument("--cao-do", default=MAC_DINH_PITCH, help="Cao do giong TTS (mac dinh +0Hz).")
    parser.add_argument("--fps", type=int, default=MAC_DINH_FPS, help="So khung hinh/giay (mac dinh 30).")
    parser.add_argument("--bo-cache", action="store_true", help="Bo qua cache va sinh lai toan bo MP3.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    chuan_bi_audio_va_du_lieu_render(
        slug=args.slug.strip(),
        duong_dan_nhap=Path(args.input) if args.input else None,
        voice=args.giong.strip() or None,
        rate=args.toc_do,
        pitch=args.cao_do,
        fps=args.fps,
        bo_cache=args.bo_cache,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
