# -*- coding: utf-8 -*-
"""Tong hop offline 6 file SFX hoat hinh (public/sfx/) va 1 ban nhac nen nhe loop muot (public/bgm/)."""

from __future__ import annotations

import argparse
import math
import struct
import subprocess
import tempfile
import wave
from pathlib import Path
from typing import Callable

GOC_DU_AN = Path(__file__).resolve().parents[2]
THU_MUC_SFX_MAC_DINH = GOC_DU_AN / "public" / "sfx"
THU_MUC_BGM_MAC_DINH = GOC_DU_AN / "public" / "bgm"

SAMPLE_RATE = 44100

DANH_SACH_TEN_SFX: tuple[str, ...] = (
    "pop.mp3",
    "ding.mp3",
    "boing.mp3",
    "crickets.mp3",
    "whoosh.mp3",
    "dramatic.mp3",
)
TEN_FILE_BGM_MAC_DINH = "nhac_nen_nhe.mp3"


def _gioi_han_mem(mau: float) -> float:
    """Soft limiter dung tanh de am thanh sach, khong bao gio bi re/clipping."""
    return math.tanh(mau)


def _chuan_hoa_peak(
    trai: list[float],
    phai: list[float],
    peak_muc_tieu: float = 0.85,
) -> tuple[list[float], list[float]]:
    """Chuan hoa bien do toi da ve peak_muc_tieu ma van giu nguyen do dong deu 2 kenh."""
    max_abs = 0.0
    for s in trai:
        a = abs(s)
        if a > max_abs:
            max_abs = a
    for s in phai:
        a = abs(s)
        if a > max_abs:
            max_abs = a
    if max_abs <= 1e-9:
        return trai, phai
    he_so = peak_muc_tieu / max_abs
    return [s * he_so for s in trai], [s * he_so for s in phai]


def _ghi_wav_stereo(duong_dan_wav: Path, trai: list[float], phai: list[float], sr: int = SAMPLE_RATE) -> None:
    """Ghi 2 mang float [-1.0, 1.0] ra file WAV 16-bit PCM stereo."""
    so_mau = min(len(trai), len(phai))
    duong_dan_wav.parent.mkdir(parents=True, exist_ok=True)
    buf = bytearray(so_mau * 4)
    pack_into = struct.pack_into
    for i in range(so_mau):
        l_val = max(-1.0, min(1.0, trai[i]))
        r_val = max(-1.0, min(1.0, phai[i]))
        pack_into("<hh", buf, i * 4, int(round(l_val * 32767.0)), int(round(r_val * 32767.0)))

    with wave.open(str(duong_dan_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(buf)


def _chuyen_wav_sang_mp3(duong_dan_wav: Path, duong_dan_mp3: Path, bitrate: str = "192k") -> None:
    """Nen WAV sang MP3 sach bang ffmpeg (libmp3lame, 44.1kHz stereo)."""
    duong_dan_mp3.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-v",
        "error",
        "-i",
        str(duong_dan_wav),
        "-ar",
        str(SAMPLE_RATE),
        "-ac",
        "2",
        "-codec:a",
        "libmp3lame",
        "-b:a",
        bitrate,
        str(duong_dan_mp3),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)
    if res.returncode != 0:
        raise RuntimeError(
            f"FFmpeg nen MP3 that bai cho {duong_dan_mp3.name}: {res.stderr.strip() or res.stdout.strip()}"
        )


def _tao_sfx_pop(sr: int = SAMPLE_RATE) -> tuple[list[float], list[float]]:
    """Tieng 'pop!' bong bong hoat hinh ngan gon, vui tai (~0.18s)."""
    thoi_luong = 0.18
    n = int(sr * thoi_luong)
    trai: list[float] = [0.0] * n
    phai: list[float] = [0.0] * n
    pha = 0.0
    pha2 = 0.0

    for i in range(n):
        t = i / sr
        tien_do = t / thoi_luong
        # Quet tan so nhanh tu 260 Hz -> 940 Hz tao cam giac bong bong bat no
        freq = 260.0 + 680.0 * (tien_do**0.62)
        pha += 2.0 * math.pi * freq / sr
        pha2 += 2.0 * math.pi * (freq * 1.98) / sr

        attack = min(1.0, t / 0.005)
        decay = math.exp(-t * 24.0)
        fade_end = max(0.0, min(1.0, (thoi_luong - t) / 0.02))
        env = attack * decay * fade_end

        # Them 1 cu go tram nho o dau de tieng pop day dan hon
        thump = 0.35 * math.sin(2.0 * math.pi * 145.0 * t) * math.exp(-t * 65.0)
        val = (math.sin(pha) + 0.18 * math.sin(pha2)) * env + thump * fade_end
        s = _gioi_han_mem(val * 1.15)
        trai[i] = s
        phai[i] = s

    return _chuan_hoa_peak(trai, phai, peak_muc_tieu=0.82)


def _tao_sfx_ding(sr: int = SAMPLE_RATE) -> tuple[list[float], list[float]]:
    """Tieng 'ding!' bong den nay so / sao lap lanh trong treo (~0.90s)."""
    thoi_luong = 0.90
    n = int(sr * thoi_luong)
    trai: list[float] = [0.0] * n
    phai: list[float] = [0.0] * n

    # Hop am chuong C6 (1046.5Hz) + hoa am lap lanh nhe
    hoa_am = [
        (1046.50, 1.00, 4.2),
        (1567.98, 0.28, 5.4),  # G6
        (2093.00, 0.36, 6.8),  # C7
        (3135.96, 0.16, 9.5),  # G7
        (4186.01, 0.08, 13.0),  # C8
    ]

    for i in range(n):
        t = i / sr
        attack = min(1.0, t / 0.004)
        fade_end = max(0.0, min(1.0, (thoi_luong - t) / 0.06))
        shimmer_l = 1.0 + 0.06 * math.sin(2.0 * math.pi * 6.0 * t)
        shimmer_r = 1.0 + 0.06 * math.sin(2.0 * math.pi * 6.0 * t + 0.9)

        tong = 0.0
        for freq, amp, rate in hoa_am:
            tong += amp * math.sin(2.0 * math.pi * freq * t) * math.exp(-t * rate)

        # Them 1 tieng go nhe bang kim loai o 2ms dau
        click = 0.22 * math.sin(2.0 * math.pi * 2637.0 * t) * math.exp(-t * 90.0)
        base = (tong + click) * attack * fade_end
        trai[i] = _gioi_han_mem(base * shimmer_l * 0.9)
        phai[i] = _gioi_han_mem(base * shimmer_r * 0.9)

    return _chuan_hoa_peak(trai, phai, peak_muc_tieu=0.80)


def _tao_sfx_boing(sr: int = SAMPLE_RATE) -> tuple[list[float], list[float]]:
    """Tieng 'boing!' lo xo bat nay hai huoc (~0.55s)."""
    thoi_luong = 0.55
    n = int(sr * thoi_luong)
    trai: list[float] = [0.0] * n
    phai: list[float] = [0.0] * n
    pha = 0.0
    pha2 = 0.0

    for i in range(n):
        t = i / sr
        # Cao do bat len tu 175 Hz -> 430 Hz kem rung lo xo giam dan
        base_freq = 175.0 + 255.0 * (1.0 - math.exp(-t * 7.5))
        wobble = 62.0 * math.sin(2.0 * math.pi * 15.5 * t) * math.exp(-t * 3.8)
        freq = max(90.0, base_freq + wobble)

        pha += 2.0 * math.pi * freq / sr
        pha2 += 2.0 * math.pi * (freq * 2.0) / sr

        attack = min(1.0, t / 0.008)
        decay = math.exp(-t * 4.2)
        fade_end = max(0.0, min(1.0, (thoi_luong - t) / 0.05))
        env = attack * decay * fade_end

        val = (0.85 * math.sin(pha) + 0.22 * math.sin(pha2) + 0.08 * math.sin(pha * 3.0)) * env
        s = _gioi_han_mem(val * 1.1)
        trai[i] = s
        phai[i] = s

    return _chuan_hoa_peak(trai, phai, peak_muc_tieu=0.80)


def _tao_sfx_crickets(sr: int = SAMPLE_RATE) -> tuple[list[float], list[float]]:
    """Tieng de keu 'ri-ri... ri-ri...' cho khoanh khac im lang hai huoc (~1.60s)."""
    thoi_luong = 1.60
    n = int(sr * thoi_luong)
    trai: list[float] = [0.0] * n
    phai: list[float] = [0.0] * n

    # 3 nhip de keu tu nhien voi vi tri stereo hoi lech nhau
    cac_nhip = [
        (0.08, 0.34, 4150.0, 0.72, 0.92),
        (0.54, 0.36, 4220.0, 0.90, 0.70),
        (1.05, 0.38, 4120.0, 0.78, 0.88),
    ]

    for i in range(n):
        t = i / sr
        tong_l = 0.0
        tong_r = 0.0
        for bat_dau, do_dai, carrier_hz, pan_l, pan_r in cac_nhip:
            dt = t - bat_dau
            if 0.0 <= dt <= do_dai:
                # Moi nhip gom 4 xung nho lien tiep (am thanh dac trung cua de)
                env_chung = max(0.0, math.sin(math.pi * dt / do_dai)) ** 0.7
                xung = max(0.0, math.sin(2.0 * math.pi * 18.0 * dt)) ** 1.6
                song = (
                    0.78 * math.sin(2.0 * math.pi * carrier_hz * dt)
                    + 0.22 * math.sin(2.0 * math.pi * (carrier_hz * 1.505) * dt)
                )
                mau = song * xung * env_chung
                tong_l += mau * pan_l
                tong_r += mau * pan_r

        fade_end = max(0.0, min(1.0, (thoi_luong - t) / 0.08))
        trai[i] = _gioi_han_mem(tong_l * fade_end * 0.9)
        phai[i] = _gioi_han_mem(tong_r * fade_end * 0.9)

    # Giu am luong vua phai vi tan so ~4.2kHz rat nhay voi tai nguoi
    return _chuan_hoa_peak(trai, phai, peak_muc_tieu=0.58)


def _tao_sfx_whoosh(sr: int = SAMPLE_RATE) -> tuple[list[float], list[float]]:
    """Tieng 'vuut!' luot gio nhanh gon cho khoi chay tron / chuyen dong (~0.42s, tat dinh 100%)."""
    thoi_luong = 0.42
    n = int(sr * thoi_luong)
    trai: list[float] = [0.0] * n
    phai: list[float] = [0.0] * n

    # Bo sinh nhieu tat dinh (LCG) + bo loc thong dai 2 cuc quet tan so 280Hz -> 1500Hz -> 320Hz
    seed = 20261125
    y1 = 0.0
    y2 = 0.0
    low_pass = 0.0

    for i in range(n):
        t = i / sr
        u = t / thoi_luong
        # LCG 32-bit tat dinh
        seed = (1664525 * seed + 1013904223) & 0xFFFFFFFF
        noise = ((seed / 2147483648.0) - 1.0)

        # Tan so trung tam quet len dinh o giua roi ha xuong mem mai
        cong_bell = max(0.0, math.sin(math.pi * u)) ** 1.35
        fc = 280.0 + 1350.0 * cong_bell
        r = 0.88
        omega = 2.0 * math.pi * fc / sr
        a1 = -2.0 * r * math.cos(omega)
        a2 = r * r
        bp = (1.0 - r) * noise - a1 * y1 - a2 * y2
        y2 = y1
        y1 = bp

        # Them 1 lop gio tram em tai
        low_pass = 0.96 * low_pass + 0.04 * noise
        env = max(0.0, math.sin(math.pi * u)) ** 1.15
        val = (bp * 1.4 + low_pass * 0.55) * env

        # Pan nhe tu trai sang phai tao cam giac luot ngang khung hinh
        pan_l = math.cos(u * math.pi * 0.5) * 0.65 + 0.35
        pan_r = math.sin(u * math.pi * 0.5) * 0.65 + 0.35
        trai[i] = _gioi_han_mem(val * pan_l)
        phai[i] = _gioi_han_mem(val * pan_r)

    return _chuan_hoa_peak(trai, phai, peak_muc_tieu=0.76)


def _tao_sfx_dramatic(sr: int = SAMPLE_RATE) -> tuple[list[float], list[float]]:
    """Tieng 'DANG!' kich tinh / soc set danh vui nhon, day dan (~1.20s)."""
    thoi_luong = 1.20
    n = int(sr * thoi_luong)
    trai: list[float] = [0.0] * n
    phai: list[float] = [0.0] * n

    # Hop am Re thu (D minor) kich tinh: D2, A2, D3, F3, A3, D4
    not_nhac = [
        (73.42, 0.95, 2.2),
        (110.00, 0.70, 2.5),
        (146.83, 0.80, 2.8),
        (174.61, 0.58, 3.1),
        (220.00, 0.48, 3.4),
        (293.66, 0.35, 3.9),
    ]

    for i in range(n):
        t = i / sr
        attack = min(1.0, t / 0.014)
        fade_end = max(0.0, min(1.0, (thoi_luong - t) / 0.14))

        tong_l = 0.0
        tong_r = 0.0
        for idx, (freq, amp, rate) in enumerate(not_nhac):
            # Them hoa am bac 2 va 3 giam nhanh tao am sac ken dong / dan day hoat hinh
            env_not = math.exp(-t * rate)
            harm = (
                math.sin(2.0 * math.pi * freq * t)
                + 0.42 * math.sin(2.0 * math.pi * freq * 2.0 * t) * math.exp(-t * 3.5)
                + 0.18 * math.sin(2.0 * math.pi * freq * 3.0 * t) * math.exp(-t * 6.0)
            )
            mau = amp * harm * env_not
            # Trai stereo nhe giua cac not cho am thanh rong rai
            if idx % 2 == 0:
                tong_l += mau * 1.04
                tong_r += mau * 0.96
            else:
                tong_l += mau * 0.96
                tong_r += mau * 1.04

        # Nhip trong timpani tram o khoanh khac mo dau
        timpani_freq = 92.0 - 26.0 * min(1.0, t / 0.12)
        timpani = 0.75 * math.sin(2.0 * math.pi * timpani_freq * t) * math.exp(-t * 9.0)

        trai[i] = _gioi_han_mem((tong_l * 0.34 + timpani * 0.45) * attack * fade_end)
        phai[i] = _gioi_han_mem((tong_r * 0.34 + timpani * 0.45) * attack * fade_end)

    return _chuan_hoa_peak(trai, phai, peak_muc_tieu=0.84)


def _midi_sang_hz(midi: float) -> float:
    return 440.0 * (2.0 ** ((midi - 69.0) / 12.0))


def _cong_not_marimba_vong(
    trai: list[float],
    phai: list[float],
    bat_dau_giay: float,
    midi: float,
    bien_do: float,
    do_dai_giay: float,
    pan: float = 0.0,
    sr: int = SAMPLE_RATE,
) -> None:
    """Cong 1 not marimba/kalimba am ap vao bo dem vong tron (seamless loop khong tach)."""
    tong_mau = len(trai)
    freq = _midi_sang_hz(midi)
    idx_dau = int(round(bat_dau_giay * sr))
    so_mau = int(round(do_dai_giay * sr))

    pan_l = math.cos((pan + 1.0) * math.pi * 0.25)
    pan_r = math.sin((pan + 1.0) * math.pi * 0.25)
    two_pi_f = 2.0 * math.pi * freq

    for k in range(so_mau):
        t = k / sr
        attack = min(1.0, t / 0.010)
        decay_chinh = math.exp(-t * 4.4)
        decay_hoa_am = math.exp(-t * 16.0)
        fade_cuoi = max(0.0, min(1.0, (do_dai_giay - t) / 0.04))

        # Am sac go marimba: co ban am + hoa am bac 4 tat nhanh dac trung thanh go
        mau = (
            math.sin(two_pi_f * t) * decay_chinh
            + 0.16 * math.sin(two_pi_f * 2.0 * t) * math.exp(-t * 9.0)
            + 0.12 * math.sin(two_pi_f * 4.0 * t) * decay_hoa_am
        ) * attack * fade_cuoi * bien_do

        pos = (idx_dau + k) % tong_mau
        trai[pos] += mau * pan_l
        phai[pos] += mau * pan_r


def _cong_not_bass_vong(
    trai: list[float],
    phai: list[float],
    bat_dau_giay: float,
    midi: float,
    bien_do: float,
    do_dai_giay: float,
    sr: int = SAMPLE_RATE,
) -> None:
    """Cong 1 not bass acoustic em tai vao bo dem vong tron."""
    tong_mau = len(trai)
    freq = _midi_sang_hz(midi)
    idx_dau = int(round(bat_dau_giay * sr))
    so_mau = int(round(do_dai_giay * sr))
    two_pi_f = 2.0 * math.pi * freq

    for k in range(so_mau):
        t = k / sr
        attack = min(1.0, t / 0.025)
        decay = math.exp(-t * 1.9)
        fade_cuoi = max(0.0, min(1.0, (do_dai_giay - t) / 0.08))
        mau = (
            math.sin(two_pi_f * t)
            + 0.22 * math.sin(two_pi_f * 2.0 * t) * math.exp(-t * 4.5)
        ) * attack * decay * fade_cuoi * bien_do

        pos = (idx_dau + k) % tong_mau
        trai[pos] += mau * 0.72
        phai[pos] += mau * 0.72


def _cong_pad_hop_am_vong(
    trai: list[float],
    phai: list[float],
    bat_dau_giay: float,
    cac_midi: tuple[int, ...],
    bien_do: float,
    do_dai_giay: float,
    sr: int = SAMPLE_RATE,
) -> None:
    """Cong 1 lop dem hoa am rat em (khong lan giong doc) co fade-in/out muot."""
    tong_mau = len(trai)
    idx_dau = int(round(bat_dau_giay * sr))
    so_mau = int(round(do_dai_giay * sr))
    freqs = [_midi_sang_hz(m) for m in cac_midi]

    for k in range(so_mau):
        t = k / sr
        # Bao hinh cong sin mem mai de chuyen hop am khong bi dut quang
        env = max(0.0, math.sin(math.pi * (t / do_dai_giay))) ** 0.85
        tong_l = 0.0
        tong_r = 0.0
        for idx, freq in enumerate(freqs):
            w = 2.0 * math.pi * freq * t
            # Detune sieu nhe tao cam giac am ap, tu nhien
            s_l = math.sin(w)
            s_r = math.sin(w * 1.0008 + 0.4)
            if idx % 2 == 0:
                tong_l += s_l
                tong_r += s_r * 0.92
            else:
                tong_l += s_l * 0.92
                tong_r += s_r
        he_so = (bien_do / max(1, len(freqs))) * env
        pos = (idx_dau + k) % tong_mau
        trai[pos] += tong_l * he_so
        phai[pos] += tong_r * he_so


def _tao_nhac_nen_nhe(sr: int = SAMPLE_RATE, so_giay: float = 48.0) -> tuple[list[float], list[float]]:
    """
    Tong hop ban nhac nen acoustic/marimba 48 giay (80 BPM, 16 o nhip 4/4) em tai,
    vui tuoi nhe nhang, loop muot 100% va chừa dai tan trung de khong lan giong ke.
    """
    # 80 BPM -> 1 phach = 0.75s, 1 o nhip = 3.0s, 16 o nhip = 48.0s chuan
    beat = 0.75
    n = int(round(sr * so_giay))
    trai = [0.0] * n
    phai = [0.0] * n

    # Vong hop am 4 o nhip am ap, de nghe (Do truong - La thu - Fa truong - Sol 6)
    # (bass_midi, pad_chord, arpeggio_notes)
    vong_hop_am: list[tuple[int, tuple[int, ...], tuple[int, ...]]] = [
        (48, (60, 64, 67, 71), (60, 64, 67, 72, 67, 64, 71, 67)),  # Cmaj7
        (45, (57, 60, 64, 67), (57, 60, 64, 69, 64, 60, 67, 64)),  # Am7
        (41, (57, 60, 65, 69), (65, 69, 72, 69, 65, 64, 60, 64)),  # Fmaj7
        (43, (59, 62, 67, 71), (67, 71, 74, 71, 67, 64, 62, 67)),  # G6
    ]

    # Giai dieu marimba nhe nhang bien tau qua 4 chu ky (16 o nhip)
    giai_dieu_chu_ky: list[list[tuple[float, int, float]]] = [
        # Chu ky 1: nhe nhang mo dau
        [(0.0, 76, 0.24), (2.0, 74, 0.20), (3.0, 72, 0.22)],
        [(0.5, 72, 0.22), (2.0, 71, 0.20), (3.0, 69, 0.22)],
        [(0.0, 72, 0.24), (1.5, 74, 0.20), (3.0, 76, 0.22)],
        [(0.0, 74, 0.24), (2.0, 71, 0.20), (3.0, 72, 0.20)],
    ]
    giai_dieu_chu_ky_2: list[list[tuple[float, int, float]]] = [
        # Chu ky 2: vui tuoi hon 1 chut
        [(0.0, 79, 0.22), (1.5, 76, 0.20), (2.5, 74, 0.18), (3.0, 72, 0.22)],
        [(0.0, 76, 0.22), (1.5, 72, 0.20), (3.0, 69, 0.22)],
        [(0.0, 77, 0.20), (1.0, 76, 0.20), (2.0, 74, 0.20), (3.0, 72, 0.22)],
        [(0.0, 74, 0.22), (1.5, 76, 0.20), (3.0, 74, 0.18)],
    ]

    so_o_nhip = max(4, int(round(so_giay / (4.0 * beat))))
    for bar in range(so_o_nhip):
        t_bar = bar * 4.0 * beat
        chu_ky = bar // 4
        vi_tri = bar % 4
        bass_midi, pad_chord, arp = vong_hop_am[vi_tri]

        # 1. Lop pad nen sieu em giup am thanh day dan, muot ma
        _cong_pad_hop_am_vong(
            trai,
            phai,
            t_bar,
            pad_chord,
            bien_do=0.14,
            do_dai_giay=4.0 * beat + 0.35,
            sr=sr,
        )

        # 2. Bass acoustic nhip cham o phach 1 va phach 3
        _cong_not_bass_vong(trai, phai, t_bar + 0.0 * beat, bass_midi, bien_do=0.28, do_dai_giay=1.65, sr=sr)
        _cong_not_bass_vong(trai, phai, t_bar + 2.0 * beat, bass_midi + 7, bien_do=0.18, do_dai_giay=1.35, sr=sr)

        # 3. Rai hop am marimba nhip moc don (8 not/o nhip) dan xen trai-phai nhe
        for step, note_midi in enumerate(arp):
            t_not = t_bar + step * (0.5 * beat)
            nhan = 0.22 if step in (0, 4) else 0.14
            pan = -0.32 if step % 2 == 0 else 0.32
            _cong_not_marimba_vong(
                trai,
                phai,
                t_not,
                note_midi,
                bien_do=nhan,
                do_dai_giay=0.85,
                pan=pan,
                sr=sr,
            )

        # 4. Diem giai dieu nhe (o chu ky 2 va 4 them bien tau vui tuoi, chu ky 1 va 3 toi gian hon)
        mau_gd = giai_dieu_chu_ky_2[vi_tri] if (chu_ky % 2 == 1) else giai_dieu_chu_ky[vi_tri]
        if chu_ky >= 1:
            for offset_beat, note_midi, amp in mau_gd:
                _cong_not_marimba_vong(
                    trai,
                    phai,
                    t_bar + offset_beat * beat,
                    note_midi,
                    bien_do=amp * (0.85 if chu_ky == 2 else 1.0),
                    do_dai_giay=1.05,
                    pan=0.18 if vi_tri % 2 == 0 else -0.18,
                    sr=sr,
                )

    # Soft limiter nhe + chuan hoa peak ve 0.78 de giu headroom rong cho auto-ducking
    trai = [_gioi_han_mem(s * 0.92) for s in trai]
    phai = [_gioi_han_mem(s * 0.92) for s in phai]
    return _chuan_hoa_peak(trai, phai, peak_muc_tieu=0.78)


BAN_DO_HAM_TAO_SFX: dict[str, Callable[[int], tuple[list[float], list[float]]]] = {
    "pop.mp3": _tao_sfx_pop,
    "ding.mp3": _tao_sfx_ding,
    "boing.mp3": _tao_sfx_boing,
    "crickets.mp3": _tao_sfx_crickets,
    "whoosh.mp3": _tao_sfx_whoosh,
    "dramatic.mp3": _tao_sfx_dramatic,
}


def tao_tat_ca_am_thanh_mau(
    thu_muc_sfx: Path | None = None,
    thu_muc_bgm: Path | None = None,
    ghi_de: bool = False,
    thoi_luong_bgm_giay: float = 48.0,
) -> dict[str, list[Path]]:
    """
    Sinh 6 file SFX vao public/sfx/ va 1 file nhac nen vao public/bgm/.
    Neu file da ton tai va ghi_de=False thi giu nguyen (de nguoi dung tu chep de file mp3 that).
    """
    sfx_dir = thu_muc_sfx or THU_MUC_SFX_MAC_DINH
    bgm_dir = thu_muc_bgm or THU_MUC_BGM_MAC_DINH
    sfx_dir.mkdir(parents=True, exist_ok=True)
    bgm_dir.mkdir(parents=True, exist_ok=True)

    da_tao: list[Path] = []
    bo_qua: list[Path] = []

    with tempfile.TemporaryDirectory(prefix="tao_am_thanh_mau_") as tmp_str:
        tmp_dir = Path(tmp_str)

        for ten_file in DANH_SACH_TEN_SFX:
            dich = sfx_dir / ten_file
            if dich.exists() and dich.stat().st_size > 0 and not ghi_de:
                print(f"[Bo qua] Da ton tai {dich} (dung --ghi-de de tao lai)")
                bo_qua.append(dich)
                continue

            ham_tao = BAN_DO_HAM_TAO_SFX[ten_file]
            trai, phai = ham_tao(SAMPLE_RATE)
            wav_tam = tmp_dir / f"{dich.stem}.wav"
            _ghi_wav_stereo(wav_tam, trai, phai, sr=SAMPLE_RATE)
            _chuyen_wav_sang_mp3(wav_tam, dich, bitrate="192k")
            print(f"[OK] Da tao SFX: {dich} ({dich.stat().st_size:,} bytes)")
            da_tao.append(dich)

        dich_bgm = bgm_dir / TEN_FILE_BGM_MAC_DINH
        if dich_bgm.exists() and dich_bgm.stat().st_size > 0 and not ghi_de:
            print(f"[Bo qua] Da ton tai {dich_bgm} (dung --ghi-de de tao lai)")
            bo_qua.append(dich_bgm)
        else:
            trai_bgm, phai_bgm = _tao_nhac_nen_nhe(sr=SAMPLE_RATE, so_giay=thoi_luong_bgm_giay)
            wav_bgm = tmp_dir / "nhac_nen_nhe.wav"
            _ghi_wav_stereo(wav_bgm, trai_bgm, phai_bgm, sr=SAMPLE_RATE)
            _chuyen_wav_sang_mp3(wav_bgm, dich_bgm, bitrate="192k")
            print(f"[OK] Da tao nhac nen ({thoi_luong_bgm_giay:.0f}s loop): {dich_bgm} ({dich_bgm.stat().st_size:,} bytes)")
            da_tao.append(dich_bgm)

    return {"da_tao": da_tao, "bo_qua": bo_qua}


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tong hop offline 6 file SFX hoat hinh (public/sfx/) va 1 ban nhac nen nhe (public/bgm/)."
    )
    parser.add_argument(
        "--ghi-de",
        action="store_true",
        help="Ghi de ca cac file .mp3 da ton tai (mac dinh giu nguyen file nguoi dung chep de).",
    )
    parser.add_argument(
        "--thoi-luong-bgm",
        type=float,
        default=48.0,
        help="Thoi luong ban nhac nen loop tinh bang giay (mac dinh 48s, chia het cho 12s de loop muot).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    ket_qua = tao_tat_ca_am_thanh_mau(
        ghi_de=args.ghi_de,
        thoi_luong_bgm_giay=max(12.0, float(args.thoi_luong_bgm)),
    )
    print(
        f"\n[HOAN TAT] Da tao moi: {len(ket_qua['da_tao'])} file | Giu nguyen: {len(ket_qua['bo_qua'])} file."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
