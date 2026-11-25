# -*- coding: utf-8 -*-
"""Tao giong doc Edge TTS co cache SHA-256, do thoi luong bang ffprobe, tinh frame 30fps va chia phu de."""

from __future__ import annotations

import argparse
import array
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

from scripts.pipeline.chuan_hoa_doc_toan import chuan_hoa_doc_toan, tai_tu_dien_phat_am
from scripts.pipeline.gemini_client import tai_env

MAC_DINH_VOICE = "vi-VN-NamMinhNeural"
MAC_DINH_VOICE_NHAN_VAT = "vi-VN-HoaiMyNeural"
MAC_DINH_VOICE_BINH_LUAN_HAI = "vi-VN-HoaiMyNeural"
MAC_DINH_RATE = "+0%"
MAC_DINH_PITCH = "+0Hz"
MAC_DINH_FPS = 30
NGHI_GIUA_CANH_GIAY = 0.25
NGHI_CHUYEN_HOI_GIAY = 0.75
NGHI_TRUOC_PUNCHLINE_GIAY = 0.35
NGHI_GIUA_LUOT_THOAI_GIAY = 0.20
NGUONG_TOI_THIEU_GIAY = 600.0
RMS_SAMPLE_RATE = 16000
RMS_NGUONG_IM_LANG = 0.008
RMS_SAN_CHUAN_HOA = 0.08

VAI_NOI_HOP_LE: tuple[str, ...] = ("nguoi_dan", "nhan_vat", "binh_luan_hai")

# Ho so giong on dinh phan biet ro rang tung nhan vat voi nguoi dan chuyen (vi-VN-NamMinhNeural, +0%, +0Hz)
HO_SO_GIONG_NHAN_VAT: tuple[dict[str, str], ...] = (
    {"voice": "vi-VN-HoaiMyNeural", "rate": "-2%", "pitch": "+0Hz"},
    {"voice": "vi-VN-NamMinhNeural", "rate": "-5%", "pitch": "-5Hz"},
    {"voice": "vi-VN-HoaiMyNeural", "rate": "+4%", "pitch": "+5Hz"},
    {"voice": "vi-VN-NamMinhNeural", "rate": "+4%", "pitch": "+4Hz"},
)

# Cau hinh mac dinh theo vai noi (co the ghi de bang bien moi truong trong .env)
CAU_HINH_VAI_MAC_DINH: dict[str, dict[str, str]] = {
    "nguoi_dan": {
        "env_voice": "TTS_VOICE_NGUOI_DAN",
        "env_rate": "TTS_RATE_NGUOI_DAN",
        "env_pitch": "TTS_PITCH_NGUOI_DAN",
        "voice": MAC_DINH_VOICE,
        "rate": "+0%",
        "pitch": "+0Hz",
    },
    "nhan_vat": {
        "env_voice": "TTS_VOICE_NHAN_VAT",
        "env_rate": "TTS_RATE_NHAN_VAT",
        "env_pitch": "TTS_PITCH_NHAN_VAT",
        "voice": MAC_DINH_VOICE_NHAN_VAT,
        "rate": "-2%",
        "pitch": "+1Hz",
    },
    "binh_luan_hai": {
        "env_voice": "TTS_VOICE_BINH_LUAN_HAI",
        "env_rate": "TTS_RATE_BINH_LUAN_HAI",
        "env_pitch": "TTS_PITCH_BINH_LUAN_HAI",
        "voice": MAC_DINH_VOICE_BINH_LUAN_HAI,
        "rate": "+6%",
        "pitch": "+4Hz",
    },
}


def _cong_phan_tram(base: str, delta: str) -> str:
    """Cong hai chuoi phan tram Edge TTS (vd: '+5%' + '-2%' -> '+3%')."""
    def _doc(s: str) -> int:
        m = re.match(r"^\s*([+-]?\d+)\s*%?\s*$", str(s or "0"))
        return int(m.group(1)) if m else 0

    tong = max(-50, min(80, _doc(base) + _doc(delta)))
    return f"+{tong}%" if tong >= 0 else f"{tong}%"


def _cong_hz(base: str, delta: str) -> str:
    """Cong hai chuoi cao do Hz Edge TTS (vd: '+0Hz' + '+4Hz' -> '+4Hz')."""
    def _doc(s: str) -> int:
        m = re.match(r"^\s*([+-]?\d+)\s*(?:hz)?\s*$", str(s or "0"), flags=re.IGNORECASE)
        return int(m.group(1)) if m else 0

    tong = max(-30, min(30, _doc(base) + _doc(delta)))
    return f"+{tong}Hz" if tong >= 0 else f"{tong}Hz"


def lay_cau_hinh_giong_theo_vai(
    vai_noi: str | None,
    env_cfg: dict[str, str] | None = None,
    voice_mac_dinh: str | None = None,
    rate_mac_dinh: str = MAC_DINH_RATE,
    pitch_mac_dinh: str = MAC_DINH_PITCH,
) -> tuple[str, str, str]:
    """
    Anh xa vaiNoi (nguoi_dan | nhan_vat | binh_luan_hai) sang (voice, rate, pitch).
    Neu kich ban cu khong co nhan vaiNoi -> fallback 100% ve TTS_VOICE/rate/pitch mac dinh.
    """
    cfg = env_cfg if env_cfg is not None else {}
    voice_fallback = (voice_mac_dinh or "").strip() or cfg.get("TTS_VOICE", "").strip() or MAC_DINH_VOICE
    vai_sach = str(vai_noi or "").strip().lower()
    if vai_sach not in CAU_HINH_VAI_MAC_DINH:
        return voice_fallback, rate_mac_dinh, pitch_mac_dinh

    spec = CAU_HINH_VAI_MAC_DINH[vai_sach]
    env_voice = cfg.get(spec["env_voice"], "").strip()
    env_rate = cfg.get(spec["env_rate"], "").strip()
    env_pitch = cfg.get(spec["env_pitch"], "").strip()

    if vai_sach == "nguoi_dan":
        voice_kq = (voice_mac_dinh or "").strip() or env_voice or cfg.get("TTS_VOICE", "").strip() or spec["voice"]
    else:
        voice_kq = env_voice or spec["voice"]

    rate_delta = env_rate or spec["rate"]
    pitch_delta = env_pitch or spec["pitch"]
    rate_kq = _cong_phan_tram(rate_mac_dinh, rate_delta)
    pitch_kq = _cong_hz(pitch_mac_dinh, pitch_delta)
    return voice_kq, rate_kq, pitch_kq


def lay_cau_hinh_giong_nhan_vat(
    nhan_vat_id: str,
    danh_sach_nv: list[dict[str, Any]] | None = None,
    env_cfg: dict[str, str] | None = None,
    rate_mac_dinh: str = MAC_DINH_RATE,
    pitch_mac_dinh: str = MAC_DINH_PITCH,
) -> tuple[str, str, str]:
    """
    Gan giong Edge TTS on dinh & phan biet ro rang cho tung nhan vat (khac Nguoi dan chuyen
    va khac nhau giua cac nhan vat trong cung canh doi thoai luotThoai[]).
    """
    cfg = env_cfg if env_cfg is not None else {}
    nv_sach = re.sub(r"[^a-zA-Z0-9_]+", "_", str(nhan_vat_id or "").strip().lower()).strip("_")

    # Cho phep ghi de rieng qua .env: TTS_VOICE_NHAN_VAT_<ID>, TTS_RATE_NHAN_VAT_<ID>, TTS_PITCH_NHAN_VAT_<ID>
    if nv_sach:
        khoa_up = nv_sach.upper()
        env_v = cfg.get(f"TTS_VOICE_NHAN_VAT_{khoa_up}", "").strip()
        env_r = cfg.get(f"TTS_RATE_NHAN_VAT_{khoa_up}", "").strip()
        env_p = cfg.get(f"TTS_PITCH_NHAN_VAT_{khoa_up}", "").strip()
        if env_v or env_r or env_p:
            return (
                env_v or MAC_DINH_VOICE_NHAN_VAT,
                _cong_phan_tram(rate_mac_dinh, env_r or "+0%"),
                _cong_hz(pitch_mac_dinh, env_p or "+0Hz"),
            )

    chi_so: int | None = None
    if isinstance(danh_sach_nv, list):
        for idx, item in enumerate(danh_sach_nv):
            if isinstance(item, dict) and str(item.get("id") or "").strip().lower() == str(nhan_vat_id or "").strip().lower():
                chi_so = idx
                break
    if chi_so is None:
        digest = hashlib.sha256((nv_sach or "nhan_vat").encode("utf-8")).digest()
        chi_so = digest[0] % len(HO_SO_GIONG_NHAN_VAT)

    ho_so = HO_SO_GIONG_NHAN_VAT[chi_so % len(HO_SO_GIONG_NHAN_VAT)]
    return (
        ho_so["voice"],
        _cong_phan_tram(rate_mac_dinh, ho_so["rate"]),
        _cong_hz(pitch_mac_dinh, ho_so["pitch"]),
    )


def tinh_moc_va_rms_luot_thoai(
    luot_thoai_goc: list[dict[str, Any]],
    thoi_luong_luot: list[float],
    rms_luot: list[list[float]],
    fps: int = MAC_DINH_FPS,
    nghi_giua_luot: float = NGHI_GIUA_LUOT_THOAI_GIAY,
) -> tuple[list[dict[str, Any]], list[float], float]:
    """
    Tinh batDauFrame / ketThucFrame chinh xac va mang RMS 30fps rieng cho tung luot thoai
    trong luotThoai[], dong thoi ghep mang RMS tong hop cua ca canh (co 0.0 o khoang nghi giua luot).
    """
    fps_an_toan = max(1, int(fps))
    nghi_frames = max(0, int(round(max(0.0, float(nghi_giua_luot)) * fps_an_toan)))
    ket_qua_luot: list[dict[str, Any]] = []
    rms_tong: list[float] = []
    frame_hien_tai = 0
    tong_giay = 0.0

    so_luot = len(luot_thoai_goc)
    for idx, luot in enumerate(luot_thoai_goc):
        dur = float(thoi_luong_luot[idx]) if idx < len(thoi_luong_luot) else 2.0
        if not math.isfinite(dur) or dur <= 0:
            dur = 2.0
        so_frame_luot = max(15, int(math.ceil(dur * fps_an_toan)))
        rms_raw = rms_luot[idx] if idx < len(rms_luot) else []
        rms_can = can_chinh_mang_rms(rms_raw, so_frame_luot) if rms_raw else [0.0] * so_frame_luot

        ban_sao = copy.deepcopy(luot)
        ban_sao["batDauFrame"] = int(frame_hien_tai)
        ban_sao["ketThucFrame"] = int(frame_hien_tai + so_frame_luot)
        if rms_raw:
            ban_sao["bienDoAmThanh"] = rms_can

        ket_qua_luot.append(ban_sao)
        rms_tong.extend(rms_can)
        frame_hien_tai += so_frame_luot
        tong_giay += dur

        if idx < so_luot - 1 and nghi_frames > 0:
            rms_tong.extend([0.0] * nghi_frames)
            frame_hien_tai += nghi_frames
            tong_giay += nghi_giua_luot

    return ket_qua_luot, rms_tong, round(tong_giay, 4)


def ghep_audio_luot_thoai_ffmpeg(
    ds_file_mp3: list[Path],
    file_dich: Path,
    nghi_giua_luot_giay: float = NGHI_GIUA_LUOT_THOAI_GIAY,
) -> Path:
    """
    Ghep cac file MP3 cua tung luot thoai (co chen khoang lang ngan giua luot) thanh 1 file MP3
    thong nhat cho canh bang ffmpeg.
    """
    if not ds_file_mp3:
        raise ValueError("Danh sach file MP3 luot thoai rong.")
    file_dich.parent.mkdir(parents=True, exist_ok=True)
    if len(ds_file_mp3) == 1:
        file_dich.write_bytes(ds_file_mp3[0].read_bytes())
        return file_dich

    file_tam = file_dich.with_suffix(".concat.mp3")
    if file_tam.exists():
        try:
            file_tam.unlink()
        except OSError:
            pass

    cmd: list[str] = ["ffmpeg", "-y", "-v", "error"]
    for p in ds_file_mp3:
        cmd.extend(["-i", str(p)])

    nghi_s = max(0.0, float(nghi_giua_luot_giay))
    filter_parts: list[str] = []
    concat_inputs: list[str] = []
    for idx in range(len(ds_file_mp3)):
        filter_parts.append(f"[{idx}:a]aformat=sample_fmts=fltp:sample_rates=24000:channel_layouts=mono[a{idx}]")
        concat_inputs.append(f"[a{idx}]")
        if idx < len(ds_file_mp3) - 1 and nghi_s > 0:
            filter_parts.append(
                f"anullsrc=r=24000:cl=mono,atrim=0:{nghi_s:.3f},asetpts=PTS-STARTPTS[s{idx}]"
            )
            concat_inputs.append(f"[s{idx}]")

    n_seg = len(concat_inputs)
    filter_complex = ";".join(filter_parts) + f";{''.join(concat_inputs)}concat=n={n_seg}:v=0:a=1[aout]"
    cmd.extend(
        [
            "-filter_complex",
            filter_complex,
            "-map",
            "[aout]",
            "-c:a",
            "libmp3lame",
            "-q:a",
            "3",
            str(file_tam),
        ]
    )
    res = subprocess.run(cmd, capture_output=True, check=False)
    if res.returncode != 0 or not file_tam.exists() or file_tam.stat().st_size == 0:
        loi_str = res.stderr.decode("utf-8", errors="replace").strip() if res.stderr else ""
        if file_tam.exists():
            try:
                file_tam.unlink()
            except OSError:
                pass
        raise RuntimeError(f"Ghep audio luotThoai bang ffmpeg that bai cho {file_dich.name}: {loi_str}")

    file_tam.replace(file_dich)
    return file_dich


def co_loi_binh_hai_huoc(canh: dict[str, Any]) -> bool:
    """Kiem tra canh co bat KhungLoiBinhHaiHuoc (loiBinhHaiHuoc.noiDung) hay khong."""
    lb = canh.get("loiBinhHaiHuoc")
    return isinstance(lb, dict) and bool(str(lb.get("noiDung") or "").strip())


def xac_dinh_cau_hinh_tts_canh(
    canh: dict[str, Any],
    env_cfg: dict[str, str] | None = None,
    voice_mac_dinh: str | None = None,
    rate_mac_dinh: str = MAC_DINH_RATE,
    pitch_mac_dinh: str = MAC_DINH_PITCH,
    nghi_truoc_punchline: float = NGHI_TRUOC_PUNCHLINE_GIAY,
) -> dict[str, Any]:
    """
    Xac dinh tron bo tham so TTS cho 1 canh:
    - voice, rate, pitch theo vaiNoi (hoac fallback TTS_VOICE neu canh cu khong co vaiNoi).
    - nghiDauGiay > 0 truoc canh co KhungLoiBinhHaiHuoc hoac vaiNoi='binh_luan_hai' de tao nhip punchline tu nhien.
    """
    vai_raw = str(canh.get("vaiNoi") or "").strip().lower()
    vai_hop_le = vai_raw if vai_raw in VAI_NOI_HOP_LE else ""
    voice_c, rate_c, pitch_c = lay_cau_hinh_giong_theo_vai(
        vai_noi=vai_hop_le or None,
        env_cfg=env_cfg,
        voice_mac_dinh=voice_mac_dinh,
        rate_mac_dinh=rate_mac_dinh,
        pitch_mac_dinh=pitch_mac_dinh,
    )
    can_nghi_punchline = co_loi_binh_hai_huoc(canh) or vai_hop_le == "binh_luan_hai"
    nghi_dau = round(max(0.0, float(nghi_truoc_punchline)), 3) if can_nghi_punchline else 0.0
    return {
        "vaiNoi": vai_hop_le,
        "voice": voice_c,
        "rate": rate_c,
        "pitch": pitch_c,
        "nghiDauGiay": nghi_dau,
    }


def bam_noi_dung_tts(
    van_ban_doc: str,
    voice: str,
    rate: str = "+0%",
    pitch: str = "+0Hz",
    nghi_dau_giay: float = 0.0,
) -> str:
    """Tinh SHA-256 cho bo (giong, toc do, cao do, khoang nghi punchline, van ban da chuan hoa)."""
    if nghi_dau_giay and nghi_dau_giay > 0:
        payload = f"{voice}|{rate}|{pitch}|delay={nghi_dau_giay:.2f}|{van_ban_doc}".encode("utf-8")
    else:
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


def dinh_dang_thoi_gian_srt(giay: float) -> str:
    """Dinh dang moc thoi gian (giay) sang chuan SubRip HH:MM:SS,mmm."""
    tong_ms = max(0, int(round(float(giay) * 1000.0)))
    gio = tong_ms // 3_600_000
    phut = (tong_ms % 3_600_000) // 60_000
    s = (tong_ms % 60_000) // 1000
    ms = tong_ms % 1000
    return f"{gio:02d}:{phut:02d}:{s:02d},{ms:03d}"


def ngat_dong_phu_de_srt(van_ban: str, max_ky_tu_dong: int = 44) -> str:
    """Ngat 1 cue phu de thanh 1-2 dong can doi, gon de doc tren YouTube."""
    sach = re.sub(r"\s+", " ", (van_ban or "").strip())
    if not sach or len(sach) <= max_ky_tu_dong:
        return sach

    tu_list = sach.split(" ")
    if len(tu_list) < 2:
        return sach

    # Tim diem ngat gan giua nhat de 2 dong can doi, khong lech qua dai
    muc_tieu = len(sach) / 2.0
    chon_idx = 1
    do_lech_tot = float("inf")
    for idx in range(1, len(tu_list)):
        d1 = " ".join(tu_list[:idx])
        d2 = " ".join(tu_list[idx:])
        lech = abs(len(d1) - muc_tieu)
        # Uu tien nhe khi ca hai dong <= max_ky_tu_dong
        phat = 0.0 if (len(d1) <= max_ky_tu_dong and len(d2) <= max_ky_tu_dong) else 25.0
        diem = lech + phat
        if diem < do_lech_tot:
            do_lech_tot = diem
            chon_idx = idx

    return " ".join(tu_list[:chon_idx]) + "\n" + " ".join(tu_list[chon_idx:])


def tao_noi_dung_srt(
    du_lieu: dict[str, Any],
    fps: int = MAC_DINH_FPS,
    max_ky_tu_dong: int = 44,
) -> str:
    """
    Xuat noi dung phu de chuan SubRip (.srt) tu moc thoi gian 30fps (tuFrame/denFrame)
    va danh sach phuDe[] da chia san trong du_lieu_render.json.
    """
    fps_an_toan = max(1, int(fps))
    khoi_srt: list[str] = []
    stt = 1
    moc_cuoi_ms = 0

    for ch in du_lieu.get("chuong") or []:
        for canh in ch.get("canh") or []:
            tu_frame = int(canh.get("tuFrame", 0))
            den_frame = int(canh.get("denFrame", tu_frame))
            if den_frame <= tu_frame:
                continue

            # Uu tien moc chinh xac tung luot thoai neu canh co luotThoai[] (giu nguyen chu goc dep cho SRT)
            luot_thoai = canh.get("luotThoai")
            if isinstance(luot_thoai, list) and any(
                isinstance(lt, dict)
                and str(lt.get("noiDung") or "").strip()
                and isinstance(lt.get("batDauFrame"), int)
                and isinstance(lt.get("ketThucFrame"), int)
                and int(lt["ketThucFrame"]) > int(lt["batDauFrame"])
                for lt in luot_thoai
            ):
                for lt in luot_thoai:
                    if not isinstance(lt, dict):
                        continue
                    nd_lt = re.sub(r"\s+", " ", str(lt.get("noiDung") or "").strip())
                    if not nd_lt:
                        continue
                    bd_f = tu_frame + max(0, int(lt.get("batDauFrame") or 0))
                    kt_f = min(den_frame, tu_frame + max(int(lt.get("batDauFrame") or 0) + 1, int(lt.get("ketThucFrame") or 0)))
                    s_ms = max(moc_cuoi_ms, int(round((bd_f / float(fps_an_toan)) * 1000.0)))
                    e_ms = int(round((kt_f / float(fps_an_toan)) * 1000.0))
                    if e_ms <= s_ms:
                        e_ms = s_ms + 300
                    noi_dung_cue = ngat_dong_phu_de_srt(nd_lt, max_ky_tu_dong=max_ky_tu_dong)
                    khoi_srt.append(
                        f"{stt}\n"
                        f"{dinh_dang_thoi_gian_srt(s_ms / 1000.0)} --> {dinh_dang_thoi_gian_srt(e_ms / 1000.0)}\n"
                        f"{noi_dung_cue}"
                    )
                    stt += 1
                    moc_cuoi_ms = max(moc_cuoi_ms, e_ms)
                continue

            ds_dong = canh.get("phuDe") if isinstance(canh.get("phuDe"), list) else []
            ds_dong = [re.sub(r"\s+", " ", str(d).strip()) for d in ds_dong if str(d).strip()]
            if not ds_dong:
                ds_dong = chia_phu_de(str(canh.get("loiThoai") or ""))
            if not ds_dong:
                continue

            bat_dau_ms = max(moc_cuoi_ms, int(round((tu_frame / float(fps_an_toan)) * 1000.0)))
            ket_thuc_ms = int(round((den_frame / float(fps_an_toan)) * 1000.0))

            # Dich nhe diem bat dau neu canh co khoang nghi punchline o dau MP3
            nghi_dau = float(canh.get("nghiDauGiay") or 0.0)
            if nghi_dau > 0 and (ket_thuc_ms - bat_dau_ms) > int(nghi_dau * 1000) + 500:
                bat_dau_ms += int(round(nghi_dau * 1000.0))

            if ket_thuc_ms <= bat_dau_ms:
                ket_thuc_ms = bat_dau_ms + 300

            tong_ms_canh = ket_thuc_ms - bat_dau_ms
            trong_so = [max(1, len(d)) for d in ds_dong]
            tong_ts = float(sum(trong_so))

            con_tro_ms = bat_dau_ms
            for idx, dong in enumerate(ds_dong):
                if idx == len(ds_dong) - 1:
                    end_ms = ket_thuc_ms
                else:
                    phan_ms = max(250, int(round(tong_ms_canh * (trong_so[idx] / tong_ts))))
                    con_lai_toi_thieu = (len(ds_dong) - 1 - idx) * 200
                    end_ms = min(ket_thuc_ms - con_lai_toi_thieu, con_tro_ms + phan_ms)
                    if end_ms <= con_tro_ms:
                        end_ms = con_tro_ms + 200

                noi_dung_cue = ngat_dong_phu_de_srt(dong, max_ky_tu_dong=max_ky_tu_dong)
                khoi_srt.append(
                    f"{stt}\n"
                    f"{dinh_dang_thoi_gian_srt(con_tro_ms / 1000.0)} --> {dinh_dang_thoi_gian_srt(end_ms / 1000.0)}\n"
                    f"{noi_dung_cue}"
                )
                stt += 1
                con_tro_ms = end_ms
                moc_cuoi_ms = max(moc_cuoi_ms, end_ms)

    return ("\n\n".join(khoi_srt) + "\n") if khoi_srt else ""


def xuat_file_srt(
    du_lieu: dict[str, Any],
    duong_dan_xuat: Path,
    fps: int = MAC_DINH_FPS,
    max_ky_tu_dong: int = 44,
) -> Path:
    """Ghi tep phu de chuan SubRip (.srt) ma hoa UTF-8, xuong dong LF."""
    noi_dung = tao_noi_dung_srt(du_lieu, fps=fps, max_ky_tu_dong=max_ky_tu_dong)
    duong_dan_xuat.parent.mkdir(parents=True, exist_ok=True)
    duong_dan_xuat.write_text(noi_dung, encoding="utf-8", newline="\n")
    return duong_dan_xuat


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


def tinh_bien_do_rms_tu_pcm(
    pcm_bytes: bytes,
    sample_rate: int = RMS_SAMPLE_RATE,
    fps: int = MAC_DINH_FPS,
    tong_frames: int | None = None,
) -> list[float]:
    """
    Tinh mang bien do RMS chuan hoa [0.0..1.0] (lam tron 2 chu so thap phan) theo tung frame
    tu du lieu PCM s16le mono (16-bit signed little-endian).
    """
    if sample_rate <= 0 or fps <= 0:
        raise ValueError("sample_rate va fps phai lon hon 0.")

    so_byte_chan = len(pcm_bytes) - (len(pcm_bytes) % 2)
    samples = array.array("h")
    if so_byte_chan > 0:
        samples.frombytes(pcm_bytes[:so_byte_chan])
        if sys.byteorder != "little":
            samples.byteswap()

    so_mau = len(samples)
    if so_mau == 0:
        return [0.0] * max(0, tong_frames or 0)

    so_frame_audio = max(1, int(math.ceil((so_mau / float(sample_rate)) * fps)))
    so_frame = tong_frames if (tong_frames is not None and tong_frames > 0) else so_frame_audio

    rms_tho: list[float] = []
    for i in range(so_frame):
        bat_dau = int(round(i * sample_rate / float(fps)))
        ket_thuc = int(round((i + 1) * sample_rate / float(fps)))
        if bat_dau >= so_mau or ket_thuc <= bat_dau:
            rms_tho.append(0.0)
            continue
        ket_thuc = min(so_mau, ket_thuc)
        tong_bp = 0
        for s in samples[bat_dau:ket_thuc]:
            tong_bp += s * s
        rms = math.sqrt(tong_bp / float(ket_thuc - bat_dau)) / 32768.0
        rms_tho.append(rms)

    max_rms = max(rms_tho) if rms_tho else 0.0
    if max_rms < RMS_NGUONG_IM_LANG:
        return [0.0] * so_frame

    hoat_dong = sorted(r for r in rms_tho if r >= RMS_NGUONG_IM_LANG)
    idx_p95 = min(len(hoat_dong) - 1, int(0.95 * (len(hoat_dong) - 1)))
    p95 = hoat_dong[idx_p95] if hoat_dong else max_rms
    dinh_chuan = max(p95, max_rms * 0.65, RMS_SAN_CHUAN_HOA)
    mau_so = max(1e-6, dinh_chuan - RMS_NGUONG_IM_LANG)

    ket_qua: list[float] = []
    for r in rms_tho:
        if r < RMS_NGUONG_IM_LANG:
            ket_qua.append(0.0)
        else:
            val = min(1.0, max(0.0, (r - RMS_NGUONG_IM_LANG) / mau_so))
            ket_qua.append(round(val**0.85, 2))
    return ket_qua


def trich_xuat_bien_do_rms(
    duong_dan_audio: Path,
    fps: int = MAC_DINH_FPS,
    tong_frames: int | None = None,
    sample_rate: int = RMS_SAMPLE_RATE,
) -> list[float]:
    """
    Giai ma file audio thanh PCM s16le 16kHz mono bang ffmpeg roi tinh mang bien do RMS [0.0..1.0] theo tung frame.
    Tra ve [] an toan neu file khong giai ma duoc (de frontend tu dong fallback lip-sync tat dinh).
    """
    cmd = [
        "ffmpeg",
        "-v",
        "error",
        "-i",
        str(duong_dan_audio),
        "-f",
        "s16le",
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "-",
    ]
    res = subprocess.run(cmd, capture_output=True, check=False)
    if res.returncode != 0 or not res.stdout:
        loi_str = res.stderr.decode("utf-8", errors="replace").strip() if res.stderr else ""
        print(f"[CANH BAO] Khong trich xuat duoc RMS cho {duong_dan_audio.name}: {loi_str or 'khong co du lieu PCM'}")
        return []
    return tinh_bien_do_rms_tu_pcm(
        res.stdout,
        sample_rate=sample_rate,
        fps=fps,
        tong_frames=tong_frames,
    )


def can_chinh_mang_rms(bien_do: list[float], so_frame: int) -> list[float]:
    """Can chinh mang RMS khop dung so_frame cua canh (phan nghi cuoi canh duoc dem bang 0.0)."""
    if so_frame <= 0:
        return []
    sach = [round(min(1.0, max(0.0, float(v))), 2) for v in bien_do[:so_frame]]
    if len(sach) < so_frame:
        sach.extend([0.0] * (so_frame - len(sach)))
    return sach


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


def chuan_hoa_bo_cuc_ket_thuc(du_lieu: dict[str, Any]) -> int:
    """
    Chi cho phep boCuc='ket_thuc' o dung canh cuoi cung cua hoi cuoi cung toan tap.
    Moi canh o cac hoi giua bi gan nham boCuc='ket_thuc' se tu dong doi thanh 'ke_chuyen'
    de khong hien thi nham banner 'CAM ON BAN DA THEO DOI!'.
    """
    tat_ca_canh = [
        canh
        for ch in (du_lieu.get("chuong") or [])
        if isinstance(ch, dict)
        for canh in (ch.get("canh") or [])
        if isinstance(canh, dict)
    ]
    if not tat_ca_canh:
        return 0
    da_sua = 0
    for idx, canh in enumerate(tat_ca_canh):
        la_canh_cuoi_toan_tap = idx == len(tat_ca_canh) - 1
        if not la_canh_cuoi_toan_tap and canh.get("boCuc") == "ket_thuc":
            canh["boCuc"] = "ke_chuyen"
            da_sua += 1
    return da_sua


def kiem_tra_lien_mach_khung_hinh(du_lieu: dict[str, Any]) -> list[str]:
    """
    Kiem tra toan bo cac canh noi tiep lien mach tu frame 0 den frame cuoi (khong gap frame, khong chong de).
    Tra ve danh sach mo ta loi (rong neu hop le 100%).
    """
    loi: list[str] = []
    tat_ca_canh = [
        canh
        for ch in (du_lieu.get("chuong") or [])
        if isinstance(ch, dict)
        for canh in (ch.get("canh") or [])
        if isinstance(canh, dict)
    ]
    if not tat_ca_canh:
        return ["Khong co canh nao trong du lieu video."]

    frame_truoc = 0
    for idx, canh in enumerate(tat_ca_canh):
        cid = str(canh.get("id") or f"canh_{idx + 1:03d}")
        tu = canh.get("tuFrame")
        den = canh.get("denFrame")
        if not isinstance(tu, int) or isinstance(tu, bool) or not isinstance(den, int) or isinstance(den, bool):
            loi.append(f"[{cid}] tuFrame/denFrame phai la so nguyen (hien tai: {tu!r}, {den!r}).")
            continue
        if den <= tu:
            loi.append(f"[{cid}] denFrame ({den}) phai lon hon tuFrame ({tu}).")
        if idx == 0 and tu != 0:
            loi.append(f"[{cid}] Canh dau tien phai bat dau tu frame 0 (hien tai: {tu}).")
        elif idx > 0 and tu > frame_truoc:
            loi.append(f"[{cid}] Phat hien gap frame giua canh truoc ({frame_truoc}) va {cid} ({tu}).")
        elif idx > 0 and tu < frame_truoc:
            loi.append(f"[{cid}] Phat hien chong de frame tai {cid} ({tu} < {frame_truoc}).")
        frame_truoc = den

    return loi


DAU_HIEU_HARDCODE_PYTHAGORAS: tuple[str, ...] = (
    "~530 tcn",
    "~500 tcn",
    "trường phái pythagoras",
    "hippasus",
    "giả sử √2 = p/q",
    "mâu thuẫn! ⇒ √2 vô tỉ",
    "√2 ≈ 1.4142",
    "y = f(x) • đạo hàm & diện tích ∫",
)


def kiem_tra_ro_ri_pythagoras(
    du_lieu: dict[str, Any],
    la_tap_pythagoras: bool | None = None,
) -> list[str]:
    """
    Phat hien ngay neu du lieu hardcode cua tap Pythagoras lot vao 1 tap phim khac
    (trong mocThoiGian, minhHoaToan hoac tieuDeNho/congThuc).
    """
    if la_tap_pythagoras is None:
        tieu_de_chung = f"{du_lieu.get('tieuDe', '')} {du_lieu.get('chuDe', '')}".lower()
        la_tap_pythagoras = any(k in tieu_de_chung for k in ("pythagoras", "py-ta-go", "hippasus"))

    if la_tap_pythagoras:
        return []

    loi: list[str] = []
    for ch in du_lieu.get("chuong") or []:
        if not isinstance(ch, dict):
            continue
        for canh in ch.get("canh") or []:
            if not isinstance(canh, dict):
                continue
            cid = str(canh.get("id") or "?")
            cac_truong_kiem_tra = [
                ("mocThoiGian", canh.get("mocThoiGian")),
                ("minhHoaToan", canh.get("minhHoaToan")),
            ]
            for ten_truong, gia_tri in cac_truong_kiem_tra:
                if not gia_tri:
                    continue
                chuoi_low = json.dumps(gia_tri, ensure_ascii=False).lower()
                for dau_hieu in DAU_HIEU_HARDCODE_PYTHAGORAS:
                    if dau_hieu in chuoi_low:
                        loi.append(
                            f"[{cid}] Phat hien du lieu hardcode Pythagoras ('{dau_hieu}') "
                            f"lot vao truong '{ten_truong}' cua tap khac!"
                        )
    return loi


def tinh_toan_khung_hinh(
    du_lieu: dict[str, Any],
    thoi_luong_theo_canh: dict[str, float],
    slug: str,
    fps: int = MAC_DINH_FPS,
    nghi_giua_canh: float = NGHI_GIUA_CANH_GIAY,
    nghi_chuyen_hoi: float = NGHI_CHUYEN_HOI_GIAY,
    bien_do_theo_canh: dict[str, list[float]] | None = None,
    nghi_dau_theo_canh: dict[str, float] | None = None,
    luot_thoai_theo_canh: dict[str, list[dict[str, Any]]] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """
    Tinh tuFrame/denFrame lien mach o 30fps, gan audioSrc, cap nhat luotThoai[] (batDauFrame/ketThucFrame/RMS)
    va chia phuDe[] giu nguyen chu goc dep.
    Dam bao khong bao gio co gap frame va chi canh cuoi hoi cuoi moi duoc dung boCuc='ket_thuc'.
    Tra ve (du_lieu_render, thong_ke).
    """
    ket_qua = copy.deepcopy(du_lieu)
    so_ket_thuc_sua = chuan_hoa_bo_cuc_ket_thuc(ket_qua)
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
            if not math.isfinite(audio_giay) or audio_giay <= 0:
                audio_giay = 4.0
            la_cuoi_chuong = idx_c == len(ds_canh) - 1
            co_chuong_sau = idx_ch < len(ds_chuong) - 1
            khoang_nghi = nghi_chuyen_hoi if (la_cuoi_chuong and co_chuong_sau) else nghi_giua_canh

            tong_giay_canh = audio_giay + khoang_nghi
            so_frame = max(30, int(math.ceil(tong_giay_canh * fps)))

            if luot_thoai_theo_canh and luot_thoai_theo_canh.get(canh_id):
                ds_luot = copy.deepcopy(luot_thoai_theo_canh[canh_id])
                canh["luotThoai"] = ds_luot
                max_kt = max((int(lt.get("ketThucFrame") or 0) for lt in ds_luot), default=0)
                if max_kt > 0:
                    so_frame = max(so_frame, max_kt + int(math.ceil(khoang_nghi * fps)))

            canh["tuFrame"] = int(frame_hien_tai)
            canh["denFrame"] = int(frame_hien_tai + so_frame)
            canh["audioSrc"] = f"audio/{slug}/{canh_id}.mp3"

            if bien_do_theo_canh and bien_do_theo_canh.get(canh_id):
                canh["bienDoAmThanh"] = can_chinh_mang_rms(bien_do_theo_canh[canh_id], so_frame)

            if nghi_dau_theo_canh and nghi_dau_theo_canh.get(canh_id, 0.0) > 0:
                canh["nghiDauGiay"] = round(float(nghi_dau_theo_canh[canh_id]), 3)

            # Giu nguyen chinh ta goc dep cho phuDe[] tren man hinh & .srt
            if isinstance(canh.get("luotThoai"), list) and canh["luotThoai"]:
                dong_tu_luot = [
                    re.sub(r"\s+", " ", str(lt.get("noiDung") or "").strip())
                    for lt in canh["luotThoai"]
                    if isinstance(lt, dict) and str(lt.get("noiDung") or "").strip()
                ]
                canh["phuDe"] = dong_tu_luot or chia_phu_de(canh.get("loiThoai", ""))
            else:
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

    loi_lien_mach = kiem_tra_lien_mach_khung_hinh(ket_qua)
    if loi_lien_mach:
        raise ValueError("Loi can khung hinh khong lien mach: " + "; ".join(loi_lien_mach))

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
        "soCanhKetThucDaSua": so_ket_thuc_sua,
        "chuong": thong_ke_chuong,
    }
    return ket_qua, thong_ke


def _chen_khoang_nghi_dau_mp3(duong_dan_mp3: Path, nghi_dau_giay: float) -> bool:
    """
    Chen khoang nghi ngan (im lang) vao dau file MP3 bang ffmpeg (adelay) de tao nhip punchline tu nhien.
    Tra ve True neu chen thanh cong, False neu bo qua hoac gap loi (giu nguyen file goc an toan).
    """
    delay_ms = int(round(max(0.0, float(nghi_dau_giay)) * 1000.0))
    if delay_ms <= 0 or not duong_dan_mp3.exists():
        return False

    file_tam = duong_dan_mp3.with_suffix(".delay.mp3")
    if file_tam.exists():
        try:
            file_tam.unlink()
        except OSError:
            pass

    cmd = [
        "ffmpeg",
        "-y",
        "-v",
        "error",
        "-i",
        str(duong_dan_mp3),
        "-af",
        f"adelay={delay_ms}:all=1",
        "-c:a",
        "libmp3lame",
        "-q:a",
        "3",
        str(file_tam),
    ]
    res = subprocess.run(cmd, capture_output=True, check=False)
    if res.returncode == 0 and file_tam.exists() and file_tam.stat().st_size > 0:
        file_tam.replace(duong_dan_mp3)
        return True

    if file_tam.exists():
        try:
            file_tam.unlink()
        except OSError:
            pass
    return False


async def _tao_file_edge_tts(
    van_ban_doc: str,
    duong_dan_mp3: Path,
    voice: str,
    rate: str,
    pitch: str,
    nghi_dau_giay: float = 0.0,
) -> None:
    try:
        import edge_tts
    except ImportError as err:
        raise RuntimeError(
            "Chua cai dat edge-tts. Hay chay: pip install -r requirements.txt"
        ) from err

    duong_dan_mp3.parent.mkdir(parents=True, exist_ok=True)
    file_tam = duong_dan_mp3.with_suffix(".mp3.tmp")
    if file_tam.exists():
        file_tam.unlink()
    try:
        comm = edge_tts.Communicate(text=van_ban_doc, voice=voice, rate=rate, pitch=pitch)
        await comm.save(str(file_tam))
        if not file_tam.exists() or file_tam.stat().st_size == 0:
            raise RuntimeError("Edge TTS tra ve file rong (0 byte).")
        file_tam.replace(duong_dan_mp3)
        if nghi_dau_giay > 0:
            _chen_khoang_nghi_dau_mp3(duong_dan_mp3, nghi_dau_giay)
    except Exception:
        if file_tam.exists():
            try:
                file_tam.unlink()
            except OSError:
                pass
        raise


async def _sinh_audio_hang_loat(
    tac_vu: list[Any],
    voice: str = MAC_DINH_VOICE,
    rate: str = MAC_DINH_RATE,
    pitch: str = MAC_DINH_PITCH,
    toi_da_dong_thoi: int = 1,
    so_lan_thu: int = 7,
    tre_giua_luot: float = 0.35,
    on_done: Callable[[str, Path], None] | None = None,
    tts_coro: Callable[..., Any] | None = None,
    sleep_coro: Callable[[float], Any] | None = None,
) -> None:
    sem = asyncio.Semaphore(max(1, toi_da_dong_thoi))
    ham_tts = tts_coro or _tao_file_edge_tts
    ham_ngu = sleep_coro or asyncio.sleep
    tong = len(tac_vu)
    da_xong = 0

    def _giai_nen_tac_vu(muc: Any) -> tuple[str, str, Path, str, str, str, float]:
        if isinstance(muc, dict):
            return (
                str(muc["id"]),
                str(muc["text"]),
                Path(muc["path"]),
                str(muc.get("voice") or voice),
                str(muc.get("rate") or rate),
                str(muc.get("pitch") or pitch),
                float(muc.get("nghiDauGiay") or 0.0),
            )
        if len(muc) == 3:
            cid, txt, p = muc
            return str(cid), str(txt), Path(p), voice, rate, pitch, 0.0
        cid, txt, p, v_c, r_c, p_c, d_c = muc
        return str(cid), str(txt), Path(p), str(v_c), str(r_c), str(p_c), float(d_c)

    async def _chay_mot(muc: Any) -> None:
        nonlocal da_xong
        canh_id, van_ban_doc, duong_dan_mp3, v_c, r_c, p_c, d_c = _giai_nen_tac_vu(muc)
        async with sem:
            for lan in range(max(1, so_lan_thu)):
                try:
                    if tts_coro is None:
                        await _tao_file_edge_tts(
                            van_ban_doc,
                            duong_dan_mp3,
                            v_c,
                            r_c,
                            p_c,
                            nghi_dau_giay=d_c,
                        )
                    else:
                        await ham_tts(van_ban_doc, duong_dan_mp3, v_c, r_c, p_c)
                    da_xong += 1
                    if on_done is not None:
                        on_done(canh_id, duong_dan_mp3)
                    if da_xong % 15 == 0 or da_xong == tong:
                        print(f"[TTS] Tien do: {da_xong}/{tong} canh...")
                    if tre_giua_luot > 0:
                        await ham_ngu(tre_giua_luot)
                    return
                except Exception as err:
                    if lan >= so_lan_thu - 1:
                        raise RuntimeError(f"TTS loi o {canh_id} sau {so_lan_thu} lan thu: {err}") from err
                    cho_giay = min(25.0, 2.0 + lan * 3.5)
                    print(
                        f"[TTS] Tam loi o {canh_id} (lan {lan + 1}/{so_lan_thu}): {err}. "
                        f"Cho {cho_giay:.1f}s roi thu lai..."
                    )
                    await ham_ngu(cho_giay)

    await asyncio.gather(*(_chay_mot(muc) for muc in tac_vu))


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
    thu_muc_out: Path | None = None,
    env_override: dict[str, str] | None = None,
    tu_dien_phat_am: dict[str, str] | None = None,
    tts_generator: Callable[..., None] | None = None,
    duration_prober: Callable[[Path], float] | None = None,
    rms_extractor: Callable[[Path, int], list[float]] | None = None,
    audio_concatenator: Callable[[list[Path], Path, float], Path] | None = None,
) -> tuple[Path, dict[str, Any]]:
    """
    Chay toan bo quy trinh:
    - Nap tu dong tu_dien_phat_am tu tu_lieu_nghien_cuu.json + tu dien mac dinh (chi ap dung cho Edge TTS,
      giu nguyen chu goc dep cho phu de & man hinh).
    - TTS phan vai da giong (ho tro luotThoai[] nhieu nhan vat voi giong/rate/pitch rieng + RMS 30fps
      rieng tung luot + batDauFrame/ketThucFrame chinh xac) co cache SHA-256.
    - ffprobe -> trich xuat RMS 30fps -> tinh frame -> xuat du_lieu_render.json & phu_de.srt.
    """
    env_cfg = dict(tai_env())
    if env_override:
        env_cfg.update(env_override)
    voice_dung = voice or env_cfg.get("TTS_VOICE") or MAC_DINH_VOICE

    base_du_lieu = (thu_muc_du_lieu or (GOC_DU_AN / "du_lieu")) / slug
    file_nhap = duong_dan_nhap or (base_du_lieu / "nhap_kich_ban.json")
    if not file_nhap.exists():
        raise FileNotFoundError(f"Khong tim thay kich ban nhap: {file_nhap}")

    du_lieu_nhap = json.loads(file_nhap.read_text(encoding="utf-8"))
    danh_sach_nv = du_lieu_nhap.get("danhSachNhanVat") if isinstance(du_lieu_nhap.get("danhSachNhanVat"), list) else []

    # Tu dong nap tu_dien_phat_am tu du_lieu/<slug>/tu_lieu_nghien_cuu.json (+ tu dien mac dinh)
    file_tu_lieu = base_du_lieu / "tu_lieu_nghien_cuu.json"
    tu_dien_dung = tai_tu_dien_phat_am(
        duong_dan_tu_lieu=file_tu_lieu if file_tu_lieu.exists() else None,
        tu_dien_bo_sung=tu_dien_phat_am,
        dung_mac_dinh=True,
    )

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
    extractor = rms_extractor or (lambda p, f: trich_xuat_bien_do_rms(p, fps=f))
    concatenator = audio_concatenator or ghep_audio_luot_thoai_ffmpeg

    can_sinh: list[dict[str, Any]] = []
    thoi_luong_map: dict[str, float] = {}
    bien_do_map: dict[str, list[float]] = {}
    luot_thoai_map: dict[str, list[dict[str, Any]]] = {}
    canh_co_luot_thoai: list[tuple[str, list[dict[str, Any]], list[dict[str, Any]]]] = []
    cache_moi: dict[str, Any] = {}
    thong_ke_vai: dict[str, int] = {}
    so_hit_cache = 0
    so_canh_da_luot = 0

    tat_ca_canh = [c for ch in (du_lieu_nhap.get("chuong") or []) for c in (ch.get("canh") or [])]

    def _goi_tts_generator(muc: dict[str, Any]) -> None:
        assert tts_generator is not None
        file_mp3 = muc["path"]
        file_mp3.parent.mkdir(parents=True, exist_ok=True)
        # Tuong thich nguoc ca ham 3 tham so (cid, txt, path) lan ham nhan them voice/rate/pitch
        try:
            import inspect

            so_ts = len(inspect.signature(tts_generator).parameters)
        except (ValueError, TypeError):
            so_ts = 3
        if so_ts >= 6:
            tts_generator(muc["id"], muc["text"], file_mp3, muc["voice"], muc["rate"], muc["pitch"])
        else:
            tts_generator(muc["id"], muc["text"], file_mp3)

    for canh in tat_ca_canh:
        canh_id = str(canh["id"])
        raw_luot = canh.get("luotThoai")
        ds_luot_hop_le = [
            lt
            for lt in (raw_luot if isinstance(raw_luot, list) else [])
            if isinstance(lt, dict) and str(lt.get("noiDung") or "").strip()
        ]

        if ds_luot_hop_le:
            so_canh_da_luot += 1
            thong_ke_vai["doi_thoai_nhieu_luot"] = thong_ke_vai.get("doi_thoai_nhieu_luot", 0) + 1
            meta_luot_list: list[dict[str, Any]] = []
            for idx_lt, lt in enumerate(ds_luot_hop_le):
                lt_id = f"{canh_id}_luot_{idx_lt + 1:02d}"
                nv_id = str(lt.get("nhanVatId") or "")
                van_ban_lt = chuan_hoa_doc_toan(str(lt.get("noiDung") or ""), tu_dien_phat_am=tu_dien_dung)
                v_lt, r_lt, p_lt = lay_cau_hinh_giong_nhan_vat(
                    nhan_vat_id=nv_id,
                    danh_sach_nv=danh_sach_nv,
                    env_cfg=env_cfg,
                    rate_mac_dinh=rate,
                    pitch_mac_dinh=pitch,
                )
                ma_hash_lt = bam_noi_dung_tts(van_ban_lt, v_lt, r_lt, p_lt, nghi_dau_giay=0.0)
                file_mp3_lt = audio_dir / f"{lt_id}.mp3"

                ban_ghi_lt = cache_cu.get(lt_id)
                if (
                    not bo_cache
                    and isinstance(ban_ghi_lt, dict)
                    and ban_ghi_lt.get("hash") == ma_hash_lt
                    and file_mp3_lt.exists()
                    and file_mp3_lt.stat().st_size > 0
                ):
                    so_hit_cache += 1
                    giay_lt = float(ban_ghi_lt.get("duration") or 0)
                    if giay_lt <= 0:
                        giay_lt = prober(file_mp3_lt)
                    if isinstance(ban_ghi_lt.get("bienDoAmThanh"), list) and ban_ghi_lt.get("fps") == fps:
                        rms_lt = list(ban_ghi_lt["bienDoAmThanh"])
                    else:
                        rms_lt = extractor(file_mp3_lt, fps)
                    cache_moi[lt_id] = {
                        "hash": ma_hash_lt,
                        "duration": round(giay_lt, 4),
                        "fps": fps,
                        "bienDoAmThanh": rms_lt,
                        "nhanVatId": nv_id,
                        "voice": v_lt,
                        "rate": r_lt,
                        "pitch": p_lt,
                        "vanBanDoc": van_ban_lt,
                    }
                else:
                    can_sinh.append(
                        {
                            "id": lt_id,
                            "text": van_ban_lt,
                            "path": file_mp3_lt,
                            "hash": ma_hash_lt,
                            "vaiNoi": f"nhan_vat:{nv_id}",
                            "nhanVatId": nv_id,
                            "voice": v_lt,
                            "rate": r_lt,
                            "pitch": p_lt,
                            "nghiDauGiay": 0.0,
                            "laLuotThoai": True,
                        }
                    )
                meta_luot_list.append(
                    {
                        "id": lt_id,
                        "path": file_mp3_lt,
                        "hash": ma_hash_lt,
                        "nhanVatId": nv_id,
                        "voice": v_lt,
                        "rate": r_lt,
                        "pitch": p_lt,
                        "vanBanDoc": van_ban_lt,
                    }
                )
            canh_co_luot_thoai.append((canh_id, ds_luot_hop_le, meta_luot_list))
            continue

        van_ban_doc = chuan_hoa_doc_toan(canh.get("loiThoai", ""), tu_dien_phat_am=tu_dien_dung)
        cfg_tts = xac_dinh_cau_hinh_tts_canh(
            canh,
            env_cfg=env_cfg,
            voice_mac_dinh=voice,
            rate_mac_dinh=rate,
            pitch_mac_dinh=pitch,
        )
        vai_key = cfg_tts["vaiNoi"] or "mac_dinh"
        thong_ke_vai[vai_key] = thong_ke_vai.get(vai_key, 0) + 1

        ma_hash = bam_noi_dung_tts(
            van_ban_doc,
            cfg_tts["voice"],
            cfg_tts["rate"],
            cfg_tts["pitch"],
            nghi_dau_giay=cfg_tts["nghiDauGiay"],
        )
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
            if isinstance(ban_ghi.get("bienDoAmThanh"), list) and ban_ghi.get("fps") == fps:
                mang_rms = list(ban_ghi["bienDoAmThanh"])
            else:
                mang_rms = extractor(file_mp3, fps)
            thoi_luong_map[canh_id] = giay
            if mang_rms:
                bien_do_map[canh_id] = mang_rms
            cache_moi[canh_id] = {
                "hash": ma_hash,
                "duration": round(giay, 4),
                "fps": fps,
                "bienDoAmThanh": mang_rms,
                "vaiNoi": cfg_tts["vaiNoi"],
                "voice": cfg_tts["voice"],
                "rate": cfg_tts["rate"],
                "pitch": cfg_tts["pitch"],
                "nghiDauGiay": cfg_tts["nghiDauGiay"],
                "vanBanDoc": van_ban_doc,
            }
        else:
            can_sinh.append(
                {
                    "id": canh_id,
                    "text": van_ban_doc,
                    "path": file_mp3,
                    "hash": ma_hash,
                    "vaiNoi": cfg_tts["vaiNoi"],
                    "voice": cfg_tts["voice"],
                    "rate": cfg_tts["rate"],
                    "pitch": cfg_tts["pitch"],
                    "nghiDauGiay": cfg_tts["nghiDauGiay"],
                    "laLuotThoai": False,
                }
            )

    print(
        f"[TTS] Tong {len(tat_ca_canh)} canh ({so_canh_da_luot} canh da luot thoai) | "
        f"Tu dien phat am: {len(tu_dien_dung)} muc | Dung lai cache: {so_hit_cache} | "
        f"Can sinh moi: {len(can_sinh)} (mac dinh: {voice_dung} | vai: {thong_ke_vai})"
    )

    if can_sinh:
        meta_can_sinh = {muc["id"]: muc for muc in can_sinh}

        def _luu_tien_do_mot_muc(muc_id: str, file_mp3: Path) -> None:
            muc = meta_can_sinh[muc_id]
            giay = prober(file_mp3)
            mang_rms = extractor(file_mp3, fps)
            if not muc.get("laLuotThoai"):
                thoi_luong_map[muc_id] = giay
                if mang_rms:
                    bien_do_map[muc_id] = mang_rms
            cache_moi[muc_id] = {
                "hash": muc["hash"],
                "duration": round(giay, 4),
                "fps": fps,
                "bienDoAmThanh": mang_rms,
                "vaiNoi": muc["vaiNoi"],
                "voice": muc["voice"],
                "rate": muc["rate"],
                "pitch": muc["pitch"],
                "nghiDauGiay": muc["nghiDauGiay"],
                "vanBanDoc": muc["text"],
                **({"nhanVatId": muc["nhanVatId"]} if muc.get("nhanVatId") else {}),
            }
            # Luu cache tung buoc de neu mang dut giua chung van giu nguyen cac muc da tao xong
            file_cache.write_text(json.dumps(cache_moi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        if tts_generator is not None:
            for muc in can_sinh:
                _goi_tts_generator(muc)
                _luu_tien_do_mot_muc(muc["id"], muc["path"])
        else:
            asyncio.run(
                _sinh_audio_hang_loat(
                    can_sinh,
                    voice=voice_dung,
                    rate=rate,
                    pitch=pitch,
                    on_done=_luu_tien_do_mot_muc,
                )
            )

    # Tong hop audio & moc batDauFrame/ketThucFrame/RMS cho cac canh co luotThoai[]
    for canh_id, ds_luot_goc, meta_luot_list in canh_co_luot_thoai:
        thoi_luong_luot: list[float] = []
        rms_luot: list[list[float]] = []
        ds_file_luot: list[Path] = []
        ds_hash_luot: list[str] = []
        for meta_lt in meta_luot_list:
            lt_id = meta_lt["id"]
            info_lt = cache_moi.get(lt_id) or {}
            dur_lt = float(info_lt.get("duration") or prober(meta_lt["path"]))
            rms_item = list(info_lt.get("bienDoAmThanh") or [])
            thoi_luong_luot.append(dur_lt)
            rms_luot.append(rms_item)
            ds_file_luot.append(meta_lt["path"])
            ds_hash_luot.append(meta_lt["hash"])

        luot_can_chinh, rms_tong_canh, tong_giay_luot = tinh_moc_va_rms_luot_thoai(
            luot_thoai_goc=ds_luot_goc,
            thoi_luong_luot=thoi_luong_luot,
            rms_luot=rms_luot,
            fps=fps,
            nghi_giua_luot=NGHI_GIUA_LUOT_THOAI_GIAY,
        )
        hash_ghep = hashlib.sha256(
            f"luot_thoai|gap={NGHI_GIUA_LUOT_THOAI_GIAY:.2f}|{'|'.join(ds_hash_luot)}".encode("utf-8")
        ).hexdigest()
        file_mp3_canh = audio_dir / f"{canh_id}.mp3"
        ban_ghi_cu_canh = cache_cu.get(canh_id)
        if not (
            not bo_cache
            and isinstance(ban_ghi_cu_canh, dict)
            and ban_ghi_cu_canh.get("hash") == hash_ghep
            and file_mp3_canh.exists()
            and file_mp3_canh.stat().st_size > 0
        ):
            concatenator(ds_file_luot, file_mp3_canh, NGHI_GIUA_LUOT_THOAI_GIAY)

        thoi_luong_map[canh_id] = tong_giay_luot
        if any(v > 0 for v in rms_tong_canh):
            bien_do_map[canh_id] = rms_tong_canh
        luot_thoai_map[canh_id] = luot_can_chinh
        cache_moi[canh_id] = {
            "hash": hash_ghep,
            "duration": round(tong_giay_luot, 4),
            "fps": fps,
            "bienDoAmThanh": rms_tong_canh,
            "vaiNoi": "doi_thoai_nhieu_luot",
            "soLuotThoai": len(luot_can_chinh),
        }

    file_cache.write_text(json.dumps(cache_moi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    nghi_dau_map = {
        cid: float(info.get("nghiDauGiay") or 0.0)
        for cid, info in cache_moi.items()
        if float(info.get("nghiDauGiay") or 0.0) > 0
    }
    du_lieu_render, thong_ke = tinh_toan_khung_hinh(
        du_lieu=du_lieu_nhap,
        thoi_luong_theo_canh=thoi_luong_map,
        slug=slug,
        fps=fps,
        bien_do_theo_canh=bien_do_map,
        nghi_dau_theo_canh=nghi_dau_map,
        luot_thoai_theo_canh=luot_thoai_map,
    )

    file_render = base_du_lieu / "du_lieu_render.json"
    file_render.write_text(
        json.dumps(du_lieu_render, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    # Tu dong xuat phu de chuan SubRip out/<slug>/phu_de.srt
    out_root = (
        thu_muc_out
        if thu_muc_out is not None
        else ((thu_muc_du_lieu.parent / "out") if thu_muc_du_lieu is not None else (GOC_DU_AN / "out"))
    )
    file_srt = xuat_file_srt(du_lieu_render, out_root / slug / "phu_de.srt", fps=fps)
    thong_ke["fileSrt"] = str(file_srt)
    thong_ke["thongKeVaiNoi"] = thong_ke_vai
    thong_ke["soCanhDaLuotThoai"] = so_canh_da_luot
    thong_ke["soTuTrongTuDienPhatAm"] = len(tu_dien_dung)

    print(f"[OK] Da xuat du lieu render: {file_render}")
    print(f"[OK] Da xuat phu de chuan SRT: {file_srt}")
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
