# -*- coding: utf-8 -*-
"""Render tach hoi chong tran RAM, ghep FFmpeg + nhac nen, xuat YouTube chapters va luoi kiem dinh 18 khung hinh."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.chuanbi_dai import do_thoi_luong_ffprobe

MAC_DINH_FPS = 30
COMPOSITION_ID = "VideoDaiNguoiQue"
ENTRY_FILE = "src/index.ts"


def dinh_dang_thoi_gian_youtube(giay: float) -> str:
    """Dinh dang giay thanh MM:SS (hoac H:MM:SS neu >= 60 phut) chuan YouTube chapters."""
    tong_giay = max(0, int(round(giay)))
    gio = tong_giay // 3600
    phut = (tong_giay % 3600) // 60
    s = tong_giay % 60
    if gio > 0:
        return f"{gio}:{phut:02d}:{s:02d}"
    return f"{phut:02d}:{s:02d}"


def tinh_pham_vi_frame_chuong(du_lieu: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Tinh pham vi frame inclusive (startFrame..endFrame) cho tung hoi de truyen vao Remotion --frames.
    Vi --frames=start-end bao gom ca 2 dau mut nen endFrame = denFrame - 1 (tranh trung frame bien).
    """
    ket_qua: list[dict[str, Any]] = []
    for idx, ch in enumerate(du_lieu.get("chuong") or [], start=1):
        ds_canh = ch.get("canh") or []
        if not ds_canh:
            continue
        tu_frame = int(ds_canh[0]["tuFrame"])
        den_frame = int(ds_canh[-1]["denFrame"])
        end_inclusive = max(tu_frame, den_frame - 1)
        ket_qua.append(
            {
                "soHoi": idx,
                "id": str(ch.get("id") or f"chuong_{idx}"),
                "tenChuong": str(ch.get("tenChuong") or f"Hồi {idx}"),
                "tuFrame": tu_frame,
                "denFrame": den_frame,
                "endFrameInclusive": end_inclusive,
                "soFrame": max(1, den_frame - tu_frame),
                "chuongData": ch,
            }
        )
    return ket_qua


def tao_noi_dung_chapters(du_lieu: dict[str, Any], fps: int = MAC_DINH_FPS) -> str:
    """Xuat danh sach moc thoi gian YouTube chapters (bat dau tu 00:00)."""
    pham_vi = tinh_pham_vi_frame_chuong(du_lieu)
    dong: list[str] = []
    for idx, ch in enumerate(pham_vi):
        giay = 0.0 if idx == 0 else ch["tuFrame"] / float(fps)
        dong.append(f"{dinh_dang_thoi_gian_youtube(giay)} {ch['tenChuong']}")
    return "\n".join(dong) + ("\n" if dong else "")


def tao_chapters_va_mo_ta(
    du_lieu: dict[str, Any],
    tu_lieu_nghien_cuu: dict[str, Any] | None = None,
    fps: int = MAC_DINH_FPS,
) -> str:
    """Xuat tron goi chapters_va_mo_ta.txt cho YouTube: tieu de goi y, mo ta hap dan, moc MM:SS va nguon tham khao."""
    tieu_de = str(du_lieu.get("tieuDe") or "Câu Chuyện Lịch Sử Toán Học").strip()
    chu_de = str(du_lieu.get("chuDe") or "").strip()
    chapters_str = tao_noi_dung_chapters(du_lieu, fps=fps).strip()

    pham_vi = tinh_pham_vi_frame_chuong(du_lieu)
    tong_giay = (pham_vi[-1]["denFrame"] / float(fps)) if pham_vi else 0.0
    thoi_luong_str = dinh_dang_thoi_gian_youtube(tong_giay)

    nhan_vat = [
        str(nv.get("ten")).strip()
        for nv in (du_lieu.get("danhSachNhanVat") or [])
        if isinstance(nv, dict) and str(nv.get("ten") or "").strip()
    ]
    chuoi_nv = ", ".join(nhan_vat) if nhan_vat else "các nhà Toán học huyền thoại"

    tom_tat_tu_lieu = ""
    ung_dung: list[str] = []
    nguon_tham_khao: list[str] = []
    if isinstance(tu_lieu_nghien_cuu, dict):
        tom_tat_tu_lieu = str(tu_lieu_nghien_cuu.get("tomTat1Cau") or "").strip()
        ung_dung = [
            str(u).strip()
            for u in (tu_lieu_nghien_cuu.get("ungDungHienDai") or [])
            if str(u).strip()
        ]
        for u in tu_lieu_nghien_cuu.get("nguonThamKhao") or []:
            s = str(u).strip()
            if s and s not in nguon_tham_khao:
                nguon_tham_khao.append(s)

    mo_ta_chinh = tom_tat_tu_lieu or chu_de or (
        f"Hành trình khám phá câu chuyện có thật đầy bất ngờ trong lịch sử Toán học cùng {chuoi_nv}."
    )

    dong: list[str] = [
        "=== TIÊU ĐỀ GỢI Ý CHO YOUTUBE ===",
        f"1. {tieu_de} | Hoạt Hình Kể Chuyện Lịch Sử Toán Học",
        f"2. Chuyện Có Thật Đằng Sau: {tieu_de} (Giải Thích Siêu Dễ Hiểu)",
        f"3. {tieu_de} — Khi Toán Học Đời Thường Lại Thay Đổi Cả Thế Giới",
        "",
        "=== ĐOẠN MÔ TẢ HẤP DẪN ===",
        mo_ta_chinh,
        "",
        (
            f"Trong tập phim hoạt hình kể chuyện dài {thoi_luong_str} này, chúng ta cùng theo chân {chuoi_nv} "
            "bước vào những giai thoại đời thường dí dỏm, những khoảnh khắc 'Ơ-rê-ka!' bùng nổ và giải mã "
            "bản chất Toán học bằng hình ảnh trực quan cực dễ hiểu."
        ),
    ]

    if ung_dung:
        dong.append("")
        dong.append("Điều bất ngờ: Ý tưởng Toán học trong tập này đang âm thầm vận hành quanh ta mỗi ngày:")
        for u in ung_dung[:4]:
            dong.append(f"- {u}")

    dong.extend(
        [
            "",
            "Nếu bạn thích phong cách hoạt hình kể chuyện lịch sử Toán học hài hước và dễ hiểu, hãy bình luận chủ đề Toán học bạn muốn xem ở tập tiếp theo nhé!",
            "",
            "=== MỐC THỜI GIAN (YOUTUBE CHAPTERS) ===",
            chapters_str or "00:00 Mở đầu",
            "",
            "=== NGUỒN THAM KHẢO ===",
        ]
    )

    if nguon_tham_khao:
        for idx, url in enumerate(nguon_tham_khao, start=1):
            dong.append(f"{idx}. {url}")
    else:
        dong.append("- Tổng hợp từ tư liệu lịch sử Toán học phổ thông và bách khoa toàn thư mở.")

    dong.extend(
        [
            "",
            "#LichSuToanHoc #HoatHinhToanHoc #KeChuyenToanHoc #ToanHocThuVi #GiaoDuc",
        ]
    )
    return "\n".join(dong).strip() + "\n"


def tinh_hash_chuong(
    du_lieu: dict[str, Any],
    chuong_data: dict[str, Any],
    thu_muc_public: Path | None = None,
) -> str:
    """Tinh SHA-256 cho 1 hoi (gom props toan cuc + noi dung hoi + dau van tay file audio)."""
    public_dir = thu_muc_public or (GOC_DU_AN / "public")
    dau_van_tay_audio: list[dict[str, Any]] = []
    for canh in chuong_data.get("canh") or []:
        src = canh.get("audioSrc")
        if src:
            p = public_dir / str(src)
            if p.exists():
                st = p.stat()
                dau_van_tay_audio.append({"src": src, "size": st.st_size, "mtime": st.st_mtime_ns})
            else:
                dau_van_tay_audio.append({"src": src, "missing": True})

    goi_du_lieu = {
        "global": {
            "tieuDe": du_lieu.get("tieuDe"),
            "chuDe": du_lieu.get("chuDe"),
            "bangMau": du_lieu.get("bangMau"),
            "batSfx": du_lieu.get("batSfx"),
            "batPhuDe": du_lieu.get("batPhuDe"),
            "danhSachNhanVat": du_lieu.get("danhSachNhanVat"),
        },
        "chuong": chuong_data,
        "audio": dau_van_tay_audio,
    }
    raw = json.dumps(goi_du_lieu, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def phan_tich_danh_sach_chuong_chon(chuoi_chuong: str) -> set[str]:
    """Phan tich co --chuong 2,4 hoac chuong_2,chuong_4 thanh tap chi so/id."""
    if not chuoi_chuong or not chuoi_chuong.strip():
        return set()
    return {muc.strip().lower() for muc in chuoi_chuong.split(",") if muc.strip()}


def chon_chuong_can_render(
    pham_vi_chuong: list[dict[str, Any]],
    du_lieu: dict[str, Any],
    cache_cu: dict[str, str],
    thu_muc_hoi: Path,
    chuong_ep_render: set[str] | None = None,
    bo_cache: bool = False,
    thu_muc_public: Path | None = None,
) -> list[tuple[dict[str, Any], str, bool, str]]:
    """
    Quyet dinh tung hoi co can render lai hay bo qua nho cache hash.
    Tra ve list (thong_tin_hoi, hash_moi, can_render, ly_do).
    """
    ep = chuong_ep_render or set()
    ket_qua: list[tuple[dict[str, Any], str, bool, str]] = []

    for ch in pham_vi_chuong:
        so_hoi_str = str(ch["soHoi"])
        ch_id_low = ch["id"].lower()
        hash_moi = tinh_hash_chuong(du_lieu, ch["chuongData"], thu_muc_public=thu_muc_public)
        file_mp4 = thu_muc_hoi / f"hoi_{ch['soHoi']:02d}.mp4"

        duoc_chi_dinh = so_hoi_str in ep or ch_id_low in ep
        if bo_cache:
            ket_qua.append((ch, hash_moi, True, "bo-cache"))
        elif duoc_chi_dinh:
            ket_qua.append((ch, hash_moi, True, "chi-dinh --chuong"))
        elif not file_mp4.exists() or file_mp4.stat().st_size == 0:
            ket_qua.append((ch, hash_moi, True, "chua co file mp4"))
        elif cache_cu.get(ch["id"]) != hash_moi:
            ket_qua.append((ch, hash_moi, True, "noi dung/audio da thay doi"))
        else:
            ket_qua.append((ch, hash_moi, False, "khong doi (dung cache)"))

    return ket_qua


def _chay_lenh(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"[CMD] {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=str(cwd or GOC_DU_AN), check=False)
    if res.returncode != 0:
        raise RuntimeError(f"Lenh that bai (ma {res.returncode}): {' '.join(cmd)}")


def _co_luong_audio(duong_dan_video: Path) -> bool:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "a",
        "-show_entries",
        "stream=codec_type",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(duong_dan_video),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)
    return res.returncode == 0 and "audio" in res.stdout.lower()


def ghep_cac_hoi_ffmpeg(
    danh_sach_mp4: list[Path],
    file_xuat: Path,
    nhac_nen: Path | None = None,
    am_luong_nhac_nen: float = 0.08,
    fade_out_giay: float = 3.0,
) -> Path:
    """Ghep toan bo cac hoi bang FFmpeg concat; neu co --nhac-nen thi tu lap va fade-out 3s cuoi."""
    file_xuat.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ghep_video_") as tmp_str:
        tmp_dir = Path(tmp_str)
        concat_list = tmp_dir / "concat_list.txt"
        dong_concat = []
        for p in danh_sach_mp4:
            duong_dan_sach = p.resolve().as_posix().replace("'", "'\\''")
            dong_concat.append(f"file '{duong_dan_sach}'")
        concat_list.write_text("\n".join(dong_concat) + "\n", encoding="utf-8")

        file_ghep_tho = tmp_dir / "ghep_tho.mp4" if nhac_nen else file_xuat
        _chay_lenh(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_list),
                "-c",
                "copy",
                "-movflags",
                "+faststart",
                str(file_ghep_tho),
            ]
        )

        if nhac_nen:
            if not nhac_nen.exists():
                raise FileNotFoundError(f"Khong tim thay file nhac nen: {nhac_nen}")
            tong_giay = do_thoi_luong_ffprobe(file_ghep_tho)
            bat_dau_fade = max(0.0, tong_giay - fade_out_giay)
            co_audio_chinh = _co_luong_audio(file_ghep_tho)

            if co_audio_chinh:
                filter_complex = (
                    f"[1:a]volume={am_luong_nhac_nen:.3f},"
                    f"afade=t=out:st={bat_dau_fade:.3f}:d={fade_out_giay:.2f}[bgm];"
                    "[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]"
                )
            else:
                filter_complex = (
                    f"[1:a]volume={am_luong_nhac_nen:.3f},"
                    f"atrim=0:{tong_giay:.3f},"
                    f"afade=t=out:st={bat_dau_fade:.3f}:d={fade_out_giay:.2f}[aout]"
                )

            _chay_lenh(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(file_ghep_tho),
                    "-stream_loop",
                    "-1",
                    "-i",
                    str(nhac_nen),
                    "-filter_complex",
                    filter_complex,
                    "-map",
                    "0:v:0",
                    "-map",
                    "[aout]",
                    "-c:v",
                    "copy",
                    "-c:a",
                    "aac",
                    "-b:a",
                    "192k",
                    "-shortest",
                    "-movflags",
                    "+faststart",
                    str(file_xuat),
                ]
            )

    return file_xuat


def _tai_font_pillow(co_chu: int) -> Any:
    from PIL import ImageFont

    ung_vien = [
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path_str in ung_vien:
        if Path(path_str).exists():
            try:
                return ImageFont.truetype(path_str, co_chu)
            except Exception:
                pass
    return ImageFont.load_default()


def ghep_luoi_kiem_dinh(
    cac_o_anh: list[tuple[Path, str]],
    duong_dan_xuat: Path,
    tieu_de: str = "Lưới kiểm định 18 khung hình",
    so_cot: int = 3,
    kich_thuoc_o: tuple[int, int] = (480, 270),
) -> Path:
    """Ghep cac khung hinh thanh luoi anh kiem dinh bang Pillow, in ro so hoi + moc giay."""
    try:
        from PIL import Image, ImageDraw
    except ImportError as err:
        raise RuntimeError("Chua cai dat Pillow. Hay chay: pip install -r requirements.txt") from err

    if not cac_o_anh:
        raise ValueError("Danh sach anh kiem dinh rong.")

    tile_w, tile_h = kich_thuoc_o
    pad = 14
    header_h = 54
    so_hang = (len(cac_o_anh) + so_cot - 1) // so_cot

    tong_w = pad + so_cot * (tile_w + pad)
    tong_h = header_h + pad + so_hang * (tile_h + pad)

    canvas = Image.new("RGB", (tong_w, tong_h), color=(15, 23, 42))
    draw = ImageDraw.Draw(canvas)
    font_header = _tai_font_pillow(24)
    font_nhan = _tai_font_pillow(17)

    draw.rectangle([0, 0, tong_w, header_h], fill=(30, 41, 59))
    draw.text((pad, 14), tieu_de, fill=(254, 240, 138), font=font_header)

    for idx, (img_path, nhan) in enumerate(cac_o_anh):
        hang = idx // so_cot
        cot = idx % so_cot
        x0 = pad + cot * (tile_w + pad)
        y0 = header_h + pad + hang * (tile_h + pad)

        with Image.open(img_path) as im:
            tile = im.convert("RGB").resize((tile_w, tile_h))
        canvas.paste(tile, (x0, y0))

        # Vien khung & nhan so hoi + moc giay o goc tren trai
        draw.rectangle([x0, y0, x0 + tile_w - 1, y0 + tile_h - 1], outline=(250, 204, 21), width=2)
        draw.rectangle([x0 + 8, y0 + 8, x0 + min(tile_w - 12, 330), y0 + 38], fill=(15, 23, 42))
        draw.text((x0 + 16, y0 + 13), nhan, fill=(255, 255, 255), font=font_nhan)

    duong_dan_xuat.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(str(duong_dan_xuat), format="PNG")
    return duong_dan_xuat


def tao_luoi_kiem_dinh_tu_video(
    pham_vi_chuong: list[dict[str, Any]],
    thu_muc_hoi: Path,
    file_anh_xuat: Path,
    tieu_de: str,
    fps: int = MAC_DINH_FPS,
    so_anh_moi_hoi: int = 3,
) -> Path:
    """Trich 3 khung hinh/hoi (tong 18 khung hinh cho 6 hoi) bang FFmpeg va ghep luoi Pillow."""
    ti_le_mau = [0.15, 0.50, 0.85] if so_anh_moi_hoi == 3 else [
        (i + 0.5) / so_anh_moi_hoi for i in range(so_anh_moi_hoi)
    ]

    with tempfile.TemporaryDirectory(prefix="luoi_qa_") as tmp_str:
        tmp_dir = Path(tmp_str)
        cac_o: list[tuple[Path, str]] = []

        for ch in pham_vi_chuong:
            file_mp4 = thu_muc_hoi / f"hoi_{ch['soHoi']:02d}.mp4"
            if not file_mp4.exists():
                continue
            thoi_luong_hoi = ch["soFrame"] / float(fps)
            bat_dau_toan_cuc = ch["tuFrame"] / float(fps)

            for idx_mau, ti_le in enumerate(ti_le_mau, start=1):
                moc_cuc_bo = max(0.0, min(max(0.0, thoi_luong_hoi - 0.1), thoi_luong_hoi * ti_le))
                moc_toan_cuc = bat_dau_toan_cuc + moc_cuc_bo
                anh_tam = tmp_dir / f"hoi_{ch['soHoi']:02d}_{idx_mau}.png"
                _chay_lenh(
                    [
                        "ffmpeg",
                        "-y",
                        "-ss",
                        f"{moc_cuc_bo:.3f}",
                        "-i",
                        str(file_mp4),
                        "-frames:v",
                        "1",
                        "-vf",
                        "scale=480:270",
                        str(anh_tam),
                    ]
                )
                nhan = (
                    f"Hồi {ch['soHoi']} (#{idx_mau}) • "
                    f"{dinh_dang_thoi_gian_youtube(moc_toan_cuc)} ({int(round(moc_toan_cuc))}s)"
                )
                cac_o.append((anh_tam, nhan))

        return ghep_luoi_kiem_dinh(
            cac_o_anh=cac_o,
            duong_dan_xuat=file_anh_xuat,
            tieu_de=f"Kiểm định {len(cac_o)} khung hình — {tieu_de}",
        )


def render_toan_bo_video(
    slug: str,
    duong_dan_props: Path | None = None,
    chuong_chon: str = "",
    nhac_nen: Path | None = None,
    bo_cache: bool = False,
    chi_ghep: bool = False,
    concurrency: int | None = None,
    fps: int = MAC_DINH_FPS,
) -> dict[str, Path]:
    """Dieu phoi render tach hoi, luu hash cache, ghep FFmpeg, xuat chapters.txt va luoi_kiem_dinh.png."""
    file_props = duong_dan_props or (GOC_DU_AN / "du_lieu" / slug / "du_lieu_render.json")
    if not file_props.exists():
        raise FileNotFoundError(f"Khong tim thay du_lieu_render.json: {file_props}")

    du_lieu = json.loads(file_props.read_text(encoding="utf-8"))
    pham_vi = tinh_pham_vi_frame_chuong(du_lieu)
    if not pham_vi:
        raise ValueError("du_lieu_render.json khong co hoi/canh nao de render.")

    out_root = GOC_DU_AN / "out"
    thu_muc_slug = out_root / slug
    thu_muc_hoi = thu_muc_slug / "chuong"
    thu_muc_hoi.mkdir(parents=True, exist_ok=True)

    file_cache = thu_muc_slug / "cache_render.json"
    cache_cu: dict[str, str] = {}
    if file_cache.exists() and not bo_cache:
        try:
            cache_cu = json.loads(file_cache.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache_cu = {}

    tap_ep = phan_tich_danh_sach_chuong_chon(chuong_chon)
    ke_hoach = chon_chuong_can_render(
        pham_vi_chuong=pham_vi,
        du_lieu=du_lieu,
        cache_cu=cache_cu,
        thu_muc_hoi=thu_muc_hoi,
        chuong_ep_render=tap_ep,
        bo_cache=bo_cache,
    )

    npx_bin = shutil.which("npx") or ("npx.cmd" if os.name == "nt" else "npx")
    cache_moi = dict(cache_cu)

    if not chi_ghep:
        for ch, hash_moi, can_render, ly_do in ke_hoach:
            file_hoi = thu_muc_hoi / f"hoi_{ch['soHoi']:02d}.mp4"
            if not can_render:
                print(f"[Bo qua] Hoi {ch['soHoi']} ({ch['tenChuong']}): {ly_do}")
                continue
            print(
                f"[Render] Hoi {ch['soHoi']}/{len(pham_vi)} ({ch['tenChuong']}) "
                f"frames {ch['tuFrame']}-{ch['endFrameInclusive']} | Ly do: {ly_do}"
            )
            cmd = [
                npx_bin,
                "remotion",
                "render",
                ENTRY_FILE,
                COMPOSITION_ID,
                str(file_hoi),
                f"--props={file_props}",
                f"--frames={ch['tuFrame']}-{ch['endFrameInclusive']}",
            ]
            if concurrency and concurrency > 0:
                cmd.append(f"--concurrency={concurrency}")
            _chay_lenh(cmd, cwd=GOC_DU_AN)
            cache_moi[ch["id"]] = hash_moi
            file_cache.write_text(json.dumps(cache_moi, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Kiem tra du file hoi truoc khi ghep
    ds_file_hoi: list[Path] = []
    for ch in pham_vi:
        p = thu_muc_hoi / f"hoi_{ch['soHoi']:02d}.mp4"
        if not p.exists():
            raise FileNotFoundError(f"Thieu file hoi da render: {p}")
        ds_file_hoi.append(p)

    # 1. Ghep video tong (+ nhac nen neu co) vao out/<slug>/video_hoan_chinh.mp4 va dong bo out/<slug>.mp4
    file_video_cuoi = thu_muc_slug / "video_hoan_chinh.mp4"
    ghep_cac_hoi_ffmpeg(ds_file_hoi, file_video_cuoi, nhac_nen=nhac_nen)
    print(f"[OK] Video hoan chinh: {file_video_cuoi}")

    file_video_legacy = out_root / f"{slug}.mp4"
    try:
        if file_video_legacy.exists():
            file_video_legacy.unlink()
        os.link(file_video_cuoi, file_video_legacy)
    except OSError:
        shutil.copy2(file_video_cuoi, file_video_legacy)

    # Nap tu_lieu_nghien_cuu.json neu co de bo sung nguon tham khao vao chapters_va_mo_ta.txt
    tu_lieu_nghien_cuu: dict[str, Any] | None = None
    file_tu_lieu = file_props.parent / "tu_lieu_nghien_cuu.json"
    if file_tu_lieu.exists():
        try:
            tu_lieu_nghien_cuu = json.loads(file_tu_lieu.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            tu_lieu_nghien_cuu = None

    # 2. Xuat chapters.txt (tuong thich cu) va out/<slug>/chapters_va_mo_ta.txt (tron goi YouTube)
    file_chapters = out_root / f"{slug}_chapters.txt"
    file_chapters.write_text(tao_noi_dung_chapters(du_lieu, fps=fps), encoding="utf-8", newline="\n")
    print(f"[OK] Moc chuong YouTube: {file_chapters}")

    file_chapters_mo_ta = thu_muc_slug / "chapters_va_mo_ta.txt"
    file_chapters_mo_ta.write_text(
        tao_chapters_va_mo_ta(du_lieu, tu_lieu_nghien_cuu=tu_lieu_nghien_cuu, fps=fps),
        encoding="utf-8",
        newline="\n",
    )
    print(f"[OK] Tron goi YouTube (tieu de, mo ta, chapters, nguon): {file_chapters_mo_ta}")

    # 3. Xuat anh luoi kiem dinh 18 khung hinh
    file_luoi = thu_muc_slug / "luoi_kiem_dinh.png"
    tao_luoi_kiem_dinh_tu_video(
        pham_vi_chuong=pham_vi,
        thu_muc_hoi=thu_muc_hoi,
        file_anh_xuat=file_luoi,
        tieu_de=str(du_lieu.get("tieuDe") or slug),
        fps=fps,
    )
    print(f"[OK] Luoi kiem dinh 18 khung hinh: {file_luoi}")

    return {
        "video": file_video_cuoi,
        "video_legacy": file_video_legacy,
        "chapters": file_chapters,
        "chapters_va_mo_ta": file_chapters_mo_ta,
        "luoi": file_luoi,
    }


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render tach hoi chong tran RAM, ghep FFmpeg, nhac nen va luoi kiem dinh 18 khung hinh."
    )
    parser.add_argument("--slug", required=True, help="Ten slug du an trong du_lieu/<slug>/.")
    parser.add_argument("--input", default="", help="Duong dan tuy chinh toi du_lieu_render.json.")
    parser.add_argument(
        "--chuong",
        default="",
        help="Chi ep render lai cac hoi cu the (vd: --chuong 2,4).",
    )
    parser.add_argument(
        "--nhac-nen",
        default="",
        help="File MP3 nhac nen (tu lap diu nhe volume=0.08, fade-out 3s cuoi).",
    )
    parser.add_argument("--bo-cache", action="store_true", help="Render lai toan bo tat ca cac hoi.")
    parser.add_argument("--chi-ghep", action="store_true", help="Bo qua buoc Remotion, chi ghep & xuat luoi.")
    parser.add_argument("--concurrency", type=int, default=0, help="So luong song song truyen cho Remotion.")
    parser.add_argument("--fps", type=int, default=MAC_DINH_FPS, help="So khung hinh/giay (mac dinh 30).")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    render_toan_bo_video(
        slug=args.slug.strip(),
        duong_dan_props=Path(args.input) if args.input else None,
        chuong_chon=args.chuong,
        nhac_nen=Path(args.nhac_nen) if args.nhac_nen else None,
        bo_cache=args.bo_cache,
        chi_ghep=args.chi_ghep,
        concurrency=args.concurrency if args.concurrency > 0 else None,
        fps=args.fps,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
