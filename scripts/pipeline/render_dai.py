# -*- coding: utf-8 -*-
"""Render tach hoi chong tran RAM, ghep FFmpeg + nhac nen, xuat YouTube chapters va luoi kiem dinh 18 khung hinh."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.chuanbi_dai import (
    chuan_hoa_bo_cuc_ket_thuc,
    do_thoi_luong_ffprobe,
    kiem_tra_lien_mach_khung_hinh,
    xuat_file_srt,
)
from scripts.pipeline.gemini_client import GeminiClient

MAC_DINH_FPS = 30
COMPOSITION_ID = "VideoDaiNguoiQue"
THUMBNAIL_STILL_ID = "ThumbnailToanHoc"
ENTRY_FILE = "src/index.ts"
NHAC_NEN_MAC_DINH = GOC_DU_AN / "public" / "bgm" / "nhac_nen_nhe.mp3"
AM_LUONG_BGM_DB = -25.0
FADE_IN_MAC_DINH_GIAY = 2.0
FADE_OUT_MAC_DINH_GIAY = 3.0
NGUONG_CHIA_CHUNK_GIAY = 120.0
CI_CONCURRENCY_MAC_DINH = 2
CI_JPEG_QUALITY_MAC_DINH = 85
CI_MAX_OLD_SPACE_MB = 4096


def dang_chay_tren_ci(env: dict[str, str] | None = None) -> bool:
    """Nhan dien moi truong GitHub Actions / CI (CI=true hoac GITHUB_ACTIONS=true)."""
    nguon = env if env is not None else os.environ
    for khoa in ("CI", "GITHUB_ACTIONS"):
        val = str(nguon.get(khoa) or "").strip().lower()
        if val in ("1", "true", "yes"):
            return True
    return False


def xac_dinh_tham_so_render_ci(
    concurrency: int | None = None,
    jpeg_quality: int | None = None,
    che_do_ci: bool | None = None,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    """
    Xac dinh bo thong so render Remotion an toan cho runner GitHub Actions (2-4 vCPU, 7GB RAM):
    - Khi CI=true hoac che_do_ci=True: tu dong ap dung concurrency=2, jpeg_quality=85,
      log_level='warn', gioi han NODE_OPTIONS --max-old-space-size=4096.
    """
    la_ci = dang_chay_tren_ci(env) if che_do_ci is None else bool(che_do_ci)
    conc = concurrency if (concurrency is not None and concurrency > 0) else (CI_CONCURRENCY_MAC_DINH if la_ci else None)
    jq = jpeg_quality if (jpeg_quality is not None and 1 <= jpeg_quality <= 100) else (CI_JPEG_QUALITY_MAC_DINH if la_ci else None)
    log_level = "warn" if la_ci else None
    return {
        "laCi": la_ci,
        "concurrency": conc,
        "jpegQuality": jq,
        "logLevel": log_level,
        "maxOldSpaceMb": CI_MAX_OLD_SPACE_MB if la_ci else None,
    }


def dung_lenh_render_remotion(
    file_mp4: Path,
    file_props: Path,
    tu_frame: int,
    end_frame_inclusive: int,
    npx_bin: str | None = None,
    concurrency: int | None = None,
    jpeg_quality: int | None = None,
    che_do_ci: bool | None = None,
    env: dict[str, str] | None = None,
) -> list[str]:
    """Dung lenh Remotion render chuan, giu cmd[5] = file_mp4 va tu dong toi uu co khi chay CI."""
    bin_cmd = npx_bin or shutil.which("npx") or ("npx.cmd" if os.name == "nt" else "npx")
    cfg = xac_dinh_tham_so_render_ci(
        concurrency=concurrency,
        jpeg_quality=jpeg_quality,
        che_do_ci=che_do_ci,
        env=env,
    )
    cmd = [
        bin_cmd,
        "remotion",
        "render",
        ENTRY_FILE,
        COMPOSITION_ID,
        str(file_mp4),
        f"--props={file_props}",
        f"--frames={int(tu_frame)}-{int(end_frame_inclusive)}",
    ]
    if cfg["concurrency"]:
        cmd.append(f"--concurrency={int(cfg['concurrency'])}")
    if cfg["jpegQuality"]:
        cmd.append(f"--jpeg-quality={int(cfg['jpegQuality'])}")
    if cfg["logLevel"]:
        cmd.append(f"--log={cfg['logLevel']}")
    return cmd


def dinh_dang_thoi_gian_youtube(giay: float) -> str:
    """Dinh dang giay thanh MM:SS (hoac H:MM:SS neu >= 60 phut) chuan YouTube chapters."""
    tong_giay = max(0, int(round(giay)))
    gio = tong_giay // 3600
    phut = (tong_giay % 3600) // 60
    s = tong_giay % 60
    if gio > 0:
        return f"{gio}:{phut:02d}:{s:02d}"
    return f"{phut:02d}:{s:02d}"


def chuan_hoa_du_lieu_truoc_render(du_lieu: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """
    Chuan hoa du_lieu_render.json truoc khi gui cho Remotion:
    1. Chi cho phep boCuc='ket_thuc' o dung canh cuoi cung cua hoi cuoi cung toan tap
       (chan tuyet doi loi banner 'CAM ON BAN DA THEO DOI!' xuat hien o cuoi cac hoi giua).
    2. Kiem tra & can lai khung hinh noi tiep lien mach tu frame 0 neu phat hien gap frame / chong de.
    """
    sach = copy.deepcopy(du_lieu)
    ghi_chu: list[str] = []

    so_ket_thuc_sua = chuan_hoa_bo_cuc_ket_thuc(sach)
    if so_ket_thuc_sua > 0:
        ghi_chu.append(
            f"Da doi {so_ket_thuc_sua} canh hoi giua tu boCuc='ket_thuc' sang 'ke_chuyen' de chan banner outro."
        )

    loi_khung = kiem_tra_lien_mach_khung_hinh(sach)
    if loi_khung:
        con_tro = 0
        for ch in sach.get("chuong") or []:
            if not isinstance(ch, dict):
                continue
            for canh in ch.get("canh") or []:
                if not isinstance(canh, dict):
                    continue
                tu_cu = canh.get("tuFrame", 0)
                den_cu = canh.get("denFrame", 1)
                try:
                    dur = max(1, int(round(float(den_cu) - float(tu_cu))))
                except (TypeError, ValueError):
                    dur = 30
                canh["tuFrame"] = con_tro
                canh["denFrame"] = con_tro + dur
                con_tro += dur
        ghi_chu.append(
            f"Da can lai khung hinh lien mach 0..{con_tro} de xoa {len(loi_khung)} loi gap/lech frame."
        )

    return sach, ghi_chu


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


def tinh_danh_sach_chunk_render(
    du_lieu: dict[str, Any],
    fps: int = MAC_DINH_FPS,
    nguong_giay: float = NGUONG_CHIA_CHUNK_GIAY,
) -> list[dict[str, Any]]:
    """
    Chia thong minh cac don vi render song song theo thoi luong:
    - Hoi <= nguong_giay (mac dinh 120s): giu nguyen 1 chunk (`hoi_01`, file `hoi_01.mp4`).
    - Hoi > nguong_giay (> 120s): tu dong tach thanh 2 manh can bang (`hoi_03_p1`, `hoi_03_p2`),
      uu tien cat tai ranh gioi canh gan trung diem nhat de tranh nut that co chai tren CI.
    """
    fps_an_toan = max(1, int(fps))
    nguong_s = max(10.0, float(nguong_giay))
    pham_vi = tinh_pham_vi_frame_chuong(du_lieu)
    ket_qua: list[dict[str, Any]] = []

    for ch in pham_vi:
        so_hoi = int(ch["soHoi"])
        tu_f = int(ch["tuFrame"])
        den_f = int(ch["denFrame"])
        so_frame = max(1, den_f - tu_f)
        giay = so_frame / float(fps_an_toan)

        if giay <= nguong_s or so_frame < 2:
            chunk_id = f"hoi_{so_hoi:02d}"
            ket_qua.append(
                {
                    "chunkId": chunk_id,
                    "soHoi": so_hoi,
                    "phan": 1,
                    "tongPhan": 1,
                    "id": ch["id"],
                    "tenChuong": ch["tenChuong"],
                    "tuFrame": tu_f,
                    "denFrame": den_f,
                    "endFrameInclusive": max(tu_f, den_f - 1),
                    "soFrame": so_frame,
                    "giay": round(giay, 2),
                    "tenFileMp4": f"{chunk_id}.mp4",
                    "tenFileCache": f"cache_{chunk_id}.json",
                    "chuongData": ch["chuongData"],
                }
            )
            continue

        # Tim diem cat toi uu tai ranh gioi canh gan giua hoi nhat
        giua_f = (tu_f + den_f) / 2.0
        ds_canh = ch["chuongData"].get("canh") or []
        diem_cat_canh: list[int] = []
        for c in ds_canh[:-1]:
            if isinstance(c, dict) and isinstance(c.get("denFrame"), int):
                df = int(c["denFrame"])
                if tu_f < df < den_f:
                    diem_cat_canh.append(df)

        if diem_cat_canh:
            mid_f = min(diem_cat_canh, key=lambda x: abs(x - giua_f))
        else:
            mid_f = tu_f + (so_frame // 2)

        mid_f = max(tu_f + 1, min(den_f - 1, int(mid_f)))
        cac_doan = (
            (1, tu_f, mid_f),
            (2, mid_f, den_f),
        )
        for phan, bd, kt in cac_doan:
            chunk_id = f"hoi_{so_hoi:02d}_p{phan}"
            sf_p = max(1, kt - bd)
            ket_qua.append(
                {
                    "chunkId": chunk_id,
                    "soHoi": so_hoi,
                    "phan": phan,
                    "tongPhan": 2,
                    "id": f"{ch['id']}_p{phan}",
                    "tenChuong": f"{ch['tenChuong']} (Phần {phan}/2)",
                    "tuFrame": bd,
                    "denFrame": kt,
                    "endFrameInclusive": max(bd, kt - 1),
                    "soFrame": sf_p,
                    "giay": round(sf_p / float(fps_an_toan), 2),
                    "tenFileMp4": f"{chunk_id}.mp4",
                    "tenFileCache": f"cache_{chunk_id}.json",
                    "chuongData": ch["chuongData"],
                }
            )

    return ket_qua


def giai_danh_sach_file_ghep(
    pham_vi_chuong: list[dict[str, Any]],
    thu_muc_hoi: Path,
    danh_sach_chunk: list[dict[str, Any]] | None = None,
) -> list[Path]:
    """
    Thu thap danh sach file MP4 theo dung thu tu thoi gian de ghep FFmpeg:
    - Ho tro linh hoat ca che do chunk chia nho (`hoi_XX_p1.mp4`, `hoi_XX_p2.mp4`)
      lan che do 1 hoi/file (`hoi_XX.mp4`) de tuong thich nguoc 100%.
    """
    chunks_theo_hoi: dict[int, list[dict[str, Any]]] = {}
    for ck in (danh_sach_chunk or []):
        chunks_theo_hoi.setdefault(int(ck["soHoi"]), []).append(ck)

    ds_file: list[Path] = []
    for ch in pham_vi_chuong:
        so_hoi = int(ch["soHoi"])
        file_hoi_don = thu_muc_hoi / f"hoi_{so_hoi:02d}.mp4"
        ck_list = chunks_theo_hoi.get(so_hoi) or []

        if len(ck_list) > 1:
            ck_paths = [thu_muc_hoi / ck["tenFileMp4"] for ck in ck_list]
            if all(p.exists() for p in ck_paths):
                ds_file.extend(ck_paths)
                continue
            if file_hoi_don.exists():
                ds_file.append(file_hoi_don)
                continue
            thieu = [str(p) for p in ck_paths if not p.exists()]
            raise FileNotFoundError(f"Thieu file chunk/hoi da render cho Hoi {so_hoi}: {', '.join(thieu)}")

        # Truong hop 1 hoi khong chia (van chap nhan neu ton tai p1+p2 thu cong)
        if file_hoi_don.exists():
            ds_file.append(file_hoi_don)
        else:
            p1 = thu_muc_hoi / f"hoi_{so_hoi:02d}_p1.mp4"
            p2 = thu_muc_hoi / f"hoi_{so_hoi:02d}_p2.mp4"
            if p1.exists() and p2.exists():
                ds_file.extend([p1, p2])
            else:
                raise FileNotFoundError(f"Thieu file hoi da render: {file_hoi_don}")

    return ds_file


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


def _chay_lenh(cmd: list[str], cwd: Path | None = None, env_extra: dict[str, str] | None = None) -> None:
    print(f"[CMD] {' '.join(cmd)}")
    env_run = os.environ.copy()
    if dang_chay_tren_ci(env_run) and "--max-old-space-size" not in env_run.get("NODE_OPTIONS", ""):
        existing_node_opts = env_run.get("NODE_OPTIONS", "").strip()
        env_run["NODE_OPTIONS"] = f"{existing_node_opts} --max-old-space-size={CI_MAX_OLD_SPACE_MB}".strip()
    if env_extra:
        env_run.update(env_extra)
    res = subprocess.run(cmd, cwd=str(cwd or GOC_DU_AN), env=env_run, check=False)
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


def xac_dinh_nhac_nen(
    nhac_nen: Path | None = None,
    tat_nhac_nen: bool = False,
    duong_dan_mac_dinh: Path | None = None,
) -> Path | None:
    """
    Xac dinh file nhac nen su dung:
    - Neu tat_nhac_nen=True -> None.
    - Neu nguoi dung chi dinh --nhac-nen -> kiem tra ton tai va dung file do.
    - Nguoc lai: tu dong dung public/bgm/nhac_nen_nhe.mp3 neu co san, khong co thi tra None an toan.
    """
    if tat_nhac_nen:
        return None
    if nhac_nen is not None:
        if not nhac_nen.exists():
            raise FileNotFoundError(f"Khong tim thay file nhac nen: {nhac_nen}")
        return nhac_nen
    mac_dinh = duong_dan_mac_dinh if duong_dan_mac_dinh is not None else NHAC_NEN_MAC_DINH
    if mac_dinh.exists() and mac_dinh.stat().st_size > 0:
        return mac_dinh
    return None


def tao_filter_hau_ky_audio(
    tong_giay: float,
    co_audio_chinh: bool,
    co_nhac_nen: bool,
    am_luong_bgm_db: float = AM_LUONG_BGM_DB,
    fade_in_giay: float = FADE_IN_MAC_DINH_GIAY,
    fade_out_giay: float = FADE_OUT_MAC_DINH_GIAY,
) -> str:
    """
    Tao chuoi filter_complex FFmpeg cho hau ky am thanh chuan YouTube:
    - Nhac nen lap khop thoi luong, fade-in 2s dau, fade-out 3s cuoi, muc nen ~ -24..-28dB.
    - Auto-ducking bang sidechaincompress de ha nhac nen sau hon moi khi co tieng thoai.
    - Chuan hoa am luong dau ra -14 LUFS (loudnorm=I=-14:TP=-1.5:LRA=11).
    """
    thoi_luong = max(0.1, float(tong_giay))
    fi = min(max(0.0, float(fade_in_giay)), thoi_luong * 0.4)
    fo = min(max(0.0, float(fade_out_giay)), thoi_luong * 0.45)
    st_out = max(0.0, thoi_luong - fo)

    if co_audio_chinh and co_nhac_nen:
        return (
            "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,asplit=2[voice][sc];"
            f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"atrim=0:{thoi_luong:.3f},asetpts=PTS-STARTPTS,"
            f"volume={am_luong_bgm_db:.1f}dB,"
            f"afade=t=in:st=0:d={fi:.2f},"
            f"afade=t=out:st={st_out:.3f}:d={fo:.2f}[bgm_base];"
            "[bgm_base][sc]sidechaincompress=threshold=0.02:ratio=6:attack=35:release=350:makeup=1[bgm_ducked];"
            "[voice][bgm_ducked]amix=inputs=2:duration=first:dropout_transition=2:normalize=0,"
            "loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
        )

    if co_audio_chinh and not co_nhac_nen:
        return (
            "[0:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            "loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
        )

    if not co_audio_chinh and co_nhac_nen:
        return (
            f"[1:a]aformat=sample_rates=48000:channel_layouts=stereo,"
            f"atrim=0:{thoi_luong:.3f},asetpts=PTS-STARTPTS,"
            f"volume={am_luong_bgm_db:.1f}dB,"
            f"afade=t=in:st=0:d={fi:.2f},"
            f"afade=t=out:st={st_out:.3f}:d={fo:.2f},"
            "loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
        )

    return ""


def dung_lenh_hau_ky_audio_ffmpeg(
    file_vao: Path,
    file_xuat: Path,
    tong_giay: float,
    co_audio_chinh: bool,
    nhac_nen: Path | None = None,
    am_luong_bgm_db: float = AM_LUONG_BGM_DB,
    fade_in_giay: float = FADE_IN_MAC_DINH_GIAY,
    fade_out_giay: float = FADE_OUT_MAC_DINH_GIAY,
) -> list[str]:
    """Dung lenh FFmpeg hoan chinh cho buoc hau ky am thanh (auto-ducking + loudnorm -14 LUFS)."""
    co_bgm = nhac_nen is not None
    filter_complex = tao_filter_hau_ky_audio(
        tong_giay=tong_giay,
        co_audio_chinh=co_audio_chinh,
        co_nhac_nen=co_bgm,
        am_luong_bgm_db=am_luong_bgm_db,
        fade_in_giay=fade_in_giay,
        fade_out_giay=fade_out_giay,
    )
    if not filter_complex:
        return [
            "ffmpeg",
            "-y",
            "-i",
            str(file_vao),
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(file_xuat),
        ]

    cmd = ["ffmpeg", "-y", "-i", str(file_vao)]
    if nhac_nen is not None:
        cmd.extend(["-stream_loop", "-1", "-i", str(nhac_nen)])
    cmd.extend(
        [
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
            "-ar",
            "48000",
        ]
    )
    if nhac_nen is not None:
        cmd.append("-shortest")
    cmd.extend(["-movflags", "+faststart", str(file_xuat)])
    return cmd


def ghep_cac_hoi_ffmpeg(
    danh_sach_mp4: list[Path],
    file_xuat: Path,
    nhac_nen: Path | None = None,
    tat_nhac_nen: bool = False,
    am_luong_bgm_db: float = AM_LUONG_BGM_DB,
    fade_in_giay: float = FADE_IN_MAC_DINH_GIAY,
    fade_out_giay: float = FADE_OUT_MAC_DINH_GIAY,
) -> Path:
    """
    Ghep toan bo cac hoi bang FFmpeg concat, tu dong tron nhac nen (neu co & khong tat),
    auto-ducking (sidechaincompress) + fade-in 2s / fade-out 3s + chuan hoa -14 LUFS.
    Co fallback an toan de tuyet doi khong crash neu audio rong hoac khong co nhac nen.
    """
    file_xuat.parent.mkdir(parents=True, exist_ok=True)
    nhac_nen_dung = xac_dinh_nhac_nen(nhac_nen=nhac_nen, tat_nhac_nen=tat_nhac_nen)

    with tempfile.TemporaryDirectory(prefix="ghep_video_") as tmp_str:
        tmp_dir = Path(tmp_str)
        concat_list = tmp_dir / "concat_list.txt"
        dong_concat = []
        for p in danh_sach_mp4:
            duong_dan_sach = p.resolve().as_posix().replace("'", "'\\''")
            dong_concat.append(f"file '{duong_dan_sach}'")
        concat_list.write_text("\n".join(dong_concat) + "\n", encoding="utf-8")

        file_ghep_tho = tmp_dir / "ghep_tho.mp4"
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

        co_audio_chinh = _co_luong_audio(file_ghep_tho)
        if not co_audio_chinh and nhac_nen_dung is None:
            shutil.copy2(file_ghep_tho, file_xuat)
            return file_xuat

        tong_giay = do_thoi_luong_ffprobe(file_ghep_tho)
        cmd_hau_ky = dung_lenh_hau_ky_audio_ffmpeg(
            file_vao=file_ghep_tho,
            file_xuat=file_xuat,
            tong_giay=tong_giay,
            co_audio_chinh=co_audio_chinh,
            nhac_nen=nhac_nen_dung,
            am_luong_bgm_db=am_luong_bgm_db,
            fade_in_giay=fade_in_giay,
            fade_out_giay=fade_out_giay,
        )
        try:
            _chay_lenh(cmd_hau_ky)
        except RuntimeError as err:
            print(
                f"[CANH BAO] Hau ky am thanh (auto-ducking/loudnorm) gap loi: {err}. "
                "Chuyen sang fallback an toan giu nguyen video da ghep."
            )
            shutil.copy2(file_ghep_tho, file_xuat)

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
    file_video_tong: Path | None = None,
) -> Path:
    """
    Trich nhanh 12-18 khung hinh (3 khung/hoi cho 6 hoi = 18 khung) truc tiep bang FFmpeg
    su dung fast keyframe seek (`-ss` truoc `-i` + `-noaccurate_seek`, KHONG goi Remotion)
    va ghep luoi Pillow. Ho tro ca video da ghep hoan chinh lan cac file chunk/hoi.
    """
    ti_le_mau = [0.15, 0.50, 0.85] if so_anh_moi_hoi == 3 else [
        (i + 0.5) / so_anh_moi_hoi for i in range(so_anh_moi_hoi)
    ]

    with tempfile.TemporaryDirectory(prefix="luoi_qa_") as tmp_str:
        tmp_dir = Path(tmp_str)
        cac_o: list[tuple[Path, str]] = []
        dung_video_tong = file_video_tong is not None and file_video_tong.exists() and file_video_tong.stat().st_size > 0

        for ch in pham_vi_chuong:
            so_hoi = int(ch["soHoi"])
            thoi_luong_hoi = ch["soFrame"] / float(fps)
            bat_dau_toan_cuc = ch["tuFrame"] / float(fps)

            file_hoi_don = thu_muc_hoi / f"hoi_{so_hoi:02d}.mp4"
            file_p1 = thu_muc_hoi / f"hoi_{so_hoi:02d}_p1.mp4"
            file_p2 = thu_muc_hoi / f"hoi_{so_hoi:02d}_p2.mp4"

            for idx_mau, ti_le in enumerate(ti_le_mau, start=1):
                moc_cuc_bo = max(0.0, min(max(0.0, thoi_luong_hoi - 0.1), thoi_luong_hoi * ti_le))
                moc_toan_cuc = bat_dau_toan_cuc + moc_cuc_bo

                nguon_video: Path | None = None
                moc_seek = moc_cuc_bo
                if dung_video_tong and file_video_tong is not None:
                    nguon_video = file_video_tong
                    moc_seek = moc_toan_cuc
                elif file_hoi_don.exists():
                    nguon_video = file_hoi_don
                    moc_seek = moc_cuc_bo
                elif file_p1.exists() and file_p2.exists():
                    nua_hoi = thoi_luong_hoi / 2.0
                    if moc_cuc_bo < nua_hoi:
                        nguon_video = file_p1
                        moc_seek = moc_cuc_bo
                    else:
                        nguon_video = file_p2
                        moc_seek = max(0.0, moc_cuc_bo - nua_hoi)
                elif file_p1.exists():
                    nguon_video = file_p1
                    moc_seek = min(moc_cuc_bo, max(0.0, thoi_luong_hoi * 0.45))

                if nguon_video is None:
                    continue

                anh_tam = tmp_dir / f"hoi_{so_hoi:02d}_{idx_mau}.png"
                _chay_lenh(
                    [
                        "ffmpeg",
                        "-y",
                        "-v",
                        "error",
                        "-ss",
                        f"{moc_seek:.3f}",
                        "-noaccurate_seek",
                        "-i",
                        str(nguon_video),
                        "-frames:v",
                        "1",
                        "-vf",
                        "scale=480:270",
                        str(anh_tam),
                    ]
                )
                nhan = (
                    f"Hồi {so_hoi} (#{idx_mau}) • "
                    f"{dinh_dang_thoi_gian_youtube(moc_toan_cuc)} ({int(round(moc_toan_cuc))}s)"
                )
                cac_o.append((anh_tam, nhan))

        return ghep_luoi_kiem_dinh(
            cac_o_anh=cac_o,
            duong_dan_xuat=file_anh_xuat,
            tieu_de=f"Kiểm định {len(cac_o)} khung hình — {tieu_de}",
        )


def _rut_gon_2_4_tu(van_ban: str, mac_dinh: str) -> str:
    tu = [t for t in str(van_ban or "").strip().split() if t]
    if not tu:
        return mac_dinh
    return " ".join(tu[:4]).upper()


def chuan_bi_phuong_an_thumbnail(du_lieu: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Lay 3 phuong an Thumbnail A/B (bien_the 1, 2, 3) tu goiYThumbnail trong kich ban,
    hoac tu dong tong hop tu du_lieu video (tuong thich nguoc 100% voi kich ban cu).
    """
    tieu_de_video = str(du_lieu.get("tieuDe") or "Câu Chuyện Toán Học").strip()
    ds_nv = [nv for nv in (du_lieu.get("danhSachNhanVat") or []) if isinstance(nv, dict)]
    nv_mac_dinh = ds_nv[0] if ds_nv else {
        "id": "nha_toan_hoc",
        "ten": "Nhà Toán Học",
        "mauThan": "#0F172A",
        "mauChuDao": "#2563EB",
        "mauDa": "#FFFDF7",
        "phuKien": "kinh_tron",
    }

    # Tim cong thuc KaTeX noi bat, boi canh va dao cu dau tien trong kich ban
    cong_thuc_mac_dinh = "a^2 + b^2 = c^2"
    boi_canh_mac_dinh = "quang_truong_hy_lap"
    dao_cu_mac_dinh = "compa_co"
    tim_thay_ct = False
    for ch in du_lieu.get("chuong") or []:
        for c in ch.get("canh") or []:
            if boi_canh_mac_dinh == "quang_truong_hy_lap" and c.get("boiCanh"):
                boi_canh_mac_dinh = str(c["boiCanh"])
            if not tim_thay_ct and isinstance(c.get("congThucLatex"), list):
                for ct in c["congThucLatex"]:
                    if isinstance(ct, dict) and str(ct.get("latex") or "").strip():
                        cong_thuc_mac_dinh = str(ct["latex"]).strip()
                        if ct.get("noiBat"):
                            tim_thay_ct = True
                            break
            if dao_cu_mac_dinh == "compa_co" and isinstance(c.get("daoCu"), list):
                for dc in c["daoCu"]:
                    if isinstance(dc, dict) and dc.get("loai"):
                        dao_cu_mac_dinh = str(dc["loai"])
                        break

    goi_y_raw = du_lieu.get("goiYThumbnail")
    ban_do_goi_y: dict[int, dict[str, Any]] = {}
    if isinstance(goi_y_raw, list):
        for idx, item in enumerate(goi_y_raw[:3], start=1):
            if not isinstance(item, dict):
                continue
            bt = item.get("bien_the")
            bien_the = int(bt) if isinstance(bt, int) and bt in (1, 2, 3) else idx
            ban_do_goi_y[bien_the] = item

    cau_hinh_mac_dinh = {
        1: {
            "tieuDeLon": _rut_gon_2_4_tu(tieu_de_video, "BÍ MẬT TOÁN HỌC"),
            "nhanPhu": "SỰ THẬT SỐC",
            "bieuCam": "ngac_nhien",
            "hanhDong": "giat_minh_nhay_dung",
            "daoCuNoiBat": dao_cu_mac_dinh,
            "mauNhan": "#FACC15",
        },
        2: {
            "tieuDeLon": "CON SỐ BỊ CẤM!",
            "nhanPhu": "NGHỊCH LÝ LỊCH SỬ",
            "bieuCam": "hoang_mang",
            "hanhDong": "ho_het_sung_suong",
            "daoCuNoiBat": "khoi_da_dien",
            "mauNhan": "#38BDF8",
        },
        3: {
            "tieuDeLon": "GIẢI MÃ TRONG 10P",
            "nhanPhu": "CHỨNG MINH ĐỈNH CAO",
            "bieuCam": "tinh_quai",
            "hanhDong": "chi_tro_giai_thich",
            "daoCuNoiBat": "kinh_thien_van",
            "mauNhan": "#FACC15",
        },
    }

    ket_qua: list[dict[str, Any]] = []
    for bt in (1, 2, 3):
        raw = ban_do_goi_y.get(bt, {})
        md = cau_hinh_mac_dinh[bt]
        nv_chon = raw.get("nhanVat") if isinstance(raw.get("nhanVat"), dict) else None
        if nv_chon is None and isinstance(raw.get("nhanVatId"), str):
            nv_chon = next((n for n in ds_nv if n.get("id") == raw["nhanVatId"]), None)
        if nv_chon is None:
            nv_chon = ds_nv[(bt - 1) % len(ds_nv)] if ds_nv else nv_mac_dinh

        ket_qua.append(
            {
                "bien_the": bt,
                "tieuDeLon": _rut_gon_2_4_tu(raw.get("tieuDeLon") or md["tieuDeLon"], md["tieuDeLon"]),
                "nhanPhu": str(raw.get("nhanPhu") or md["nhanPhu"]).strip()[:36],
                "congThucLatex": str(raw.get("congThucLatex") or cong_thuc_mac_dinh).strip(),
                "daoCuNoiBat": str(raw.get("daoCuNoiBat") or md["daoCuNoiBat"]).strip(),
                "boiCanh": str(raw.get("boiCanh") or boi_canh_mac_dinh).strip(),
                "thoiTiet": str(raw.get("thoiTiet") or "nang_dep").strip(),
                "nhanVat": nv_chon,
                "bieuCam": str(raw.get("bieuCam") or md["bieuCam"]).strip(),
                "hanhDong": str(raw.get("hanhDong") or md["hanhDong"]).strip(),
                "vatCamTay": str(raw.get("vatCamTay") or "cuon_giay").strip(),
                "mauNhan": str(raw.get("mauNhan") or md["mauNhan"]).strip(),
                "tieuDeVideo": tieu_de_video,
            }
        )
    return ket_qua


def dung_lenh_render_thumbnail(
    file_props_tam: Path,
    file_anh_xuat: Path,
    npx_bin: str | None = None,
    che_do_ci: bool | None = None,
) -> list[str]:
    """Dung lenh Remotion still de render 1 anh Thumbnail 1280x720."""
    bin_cmd = npx_bin or shutil.which("npx") or ("npx.cmd" if os.name == "nt" else "npx")
    la_ci = dang_chay_tren_ci() if che_do_ci is None else bool(che_do_ci)
    cmd = [
        bin_cmd,
        "remotion",
        "still",
        ENTRY_FILE,
        THUMBNAIL_STILL_ID,
        str(file_anh_xuat),
        f"--props={file_props_tam}",
    ]
    if la_ci:
        cmd.append("--log=warn")
    return cmd


def render_bo_thumbnail(
    du_lieu: dict[str, Any],
    thu_muc_slug: Path,
    npx_bin: str | None = None,
    command_runner: Callable[[list[str], Path | None], None] | None = None,
) -> list[Path]:
    """Tu dong render 3 bien the thumbnail_1.png, thumbnail_2.png, thumbnail_3.png bang Remotion <Still>."""
    thu_muc_slug.mkdir(parents=True, exist_ok=True)
    runner = command_runner or _chay_lenh
    phuong_an_list = chuan_bi_phuong_an_thumbnail(du_lieu)
    ket_qua: list[Path] = []

    with tempfile.TemporaryDirectory(prefix="thumb_props_") as tmp_str:
        tmp_dir = Path(tmp_str)
        for pa in phuong_an_list:
            bt = int(pa["bien_the"])
            file_props_tam = tmp_dir / f"thumbnail_{bt}_props.json"
            file_props_tam.write_text(
                json.dumps(pa, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )
            file_anh = thu_muc_slug / f"thumbnail_{bt}.png"
            cmd = dung_lenh_render_thumbnail(file_props_tam, file_anh, npx_bin=npx_bin)
            runner(cmd, GOC_DU_AN)
            ket_qua.append(file_anh)

    return ket_qua


def tao_prompt_visual_qa(tieu_de: str = "") -> str:
    """Tao prompt kiem dinh thi giac (Visual QA) tren luoi 18 khung hinh cho Gemini Vision."""
    return (
        f'Ban la chuyen gia kiem dinh chat luong hinh anh (Visual QA) cho phim hoat hinh 2D ke chuyen Toan hoc: "{tieu_de}".\n'
        "Hay quan sat ky luoi 18 khung hinh trong anh dinh kem (moi o co nhan o goc tren trai, vi du: Hoi 1 (#1), Hoi 3 (#2)...).\n"
        "Kiem tra 4 nhom loi thi giac nghiem trong:\n"
        "1. `katex_tran_vien`: Cong thuc KaTeX bi tran khung, bi cat vien, chong de chu hoac hien thi ma LaTeX tho chua render.\n"
        "2. `phu_de_de_mat`: Phu de o canh duoi de len mat nhan vat, bong bong thoai hoac che mat cong thuc/hinh ve quan trong.\n"
        "3. `chu_qua_nho`: Chu tieu de, nhan hinh ve hoac cong thuc qua nho / tuong phan kem kho doc tren man hinh dien thoai.\n"
        "4. `trung_bo_cuc`: Nhieu khung hinh lien tiep trung lap bo cuc, boi canh hoac goc may gay nham chan.\n\n"
        "Tra ve DUY NHAT 1 doi tuong JSON hop le dung cau truc sau (tieng Viet co dau, ngan gon, thuc te):\n"
        "{\n"
        '  "diemTongThe": 8.5,\n'
        '  "nhanXetChung": "Nhan xet tong quan 1-2 cau ve chat luong hinh anh va do de doc.",\n'
        '  "danhSachCanhLoi": [\n'
        "    {\n"
        '      "oKhungHinh": "Hồi 3 (#2)",\n'
        '      "loaiLoi": "katex_tran_vien | phu_de_de_mat | chu_qua_nho | trung_bo_cuc | khac",\n'
        '      "mucDo": "cao | trung_binh | thap",\n'
        '      "moTa": "Mo ta ngan gon loi nhin thay trong o khung hinh nay.",\n'
        '      "deXuatSua": "Cach sua cu the trong kich ban hoac component Remotion."\n'
        "    }\n"
        "  ],\n"
        '  "deXuatSuaChung": ["De xuat toi uu chung 1...", "De xuat 2..."]\n'
        "}\n"
        "Neu khong phat hien loi nao dang ke, de `danhSachCanhLoi: []` va cham diem 9-10."
    )


def chuan_hoa_bao_cao_visual_qa(raw: Any, ten_anh: str = "luoi_kiem_dinh.png") -> dict[str, Any]:
    """Chuan hoa ket qua JSON tu Gemini Vision ve schema bao_cao_visual_qa.json nhat quan."""
    data = raw if isinstance(raw, dict) else {}
    try:
        diem = float(data.get("diemTongThe", 8.0))
    except (TypeError, ValueError):
        diem = 8.0
    diem = round(max(1.0, min(10.0, diem)), 2)

    loai_hop_le = {"katex_tran_vien", "phu_de_de_mat", "chu_qua_nho", "trung_bo_cuc", "khac"}
    muc_hop_le = {"cao", "trung_binh", "thap"}

    canh_loi_sach: list[dict[str, str]] = []
    for item in (data.get("danhSachCanhLoi") or []):
        if not isinstance(item, dict):
            continue
        loai_raw = str(item.get("loaiLoi") or "khac").strip().lower()
        muc_raw = str(item.get("mucDo") or "trung_binh").strip().lower()
        canh_loi_sach.append(
            {
                "oKhungHinh": str(item.get("oKhungHinh") or "Khong ro").strip()[:60],
                "loaiLoi": loai_raw if loai_raw in loai_hop_le else "khac",
                "mucDo": muc_raw if muc_raw in muc_hop_le else "trung_binh",
                "moTa": str(item.get("moTa") or "").strip()[:300],
                "deXuatSua": str(item.get("deXuatSua") or "").strip()[:300],
            }
        )

    de_xuat_chung = [
        str(x).strip()[:240]
        for x in (data.get("deXuatSuaChung") or [])
        if str(x).strip()
    ]

    return {
        "trangThai": "hoan_thanh",
        "anhKiemDinh": ten_anh,
        "diemTongThe": diem,
        "nhanXetChung": str(data.get("nhanXetChung") or "").strip()[:500],
        "danhSachCanhLoi": canh_loi_sach,
        "deXuatSuaChung": de_xuat_chung[:8],
    }


def chay_visual_qa_gemini(
    file_luoi: Path,
    file_bao_cao: Path,
    tieu_de: str = "",
    client: GeminiClient | None = None,
) -> dict[str, Any]:
    """
    Gui luoi_kiem_dinh.png cho Gemini Vision kiem dinh thi giac va luu bao_cao_visual_qa.json.
    Khong bao gio lam crash pipeline neu mat mang, thieu API key hoac het quota.
    """
    file_bao_cao.parent.mkdir(parents=True, exist_ok=True)
    try:
        if not file_luoi.exists():
            raise FileNotFoundError(f"Khong tim thay anh luoi kiem dinh: {file_luoi}")
        gemini = client or GeminiClient()
        raw = gemini.tao_json_voi_anh(
            prompt=tao_prompt_visual_qa(tieu_de=tieu_de),
            duong_dan_anh=file_luoi,
            mime_type="image/png",
            system_instruction=(
                "Ban la chuyen gia Visual QA kiem dinh hinh anh phim hoat hinh 2D Toan hoc. "
                "Tra ve DUY NHAT 1 doi tuong JSON hop le."
            ),
            nhiet_do=0.2,
            max_output_tokens=4096,
        )
        bao_cao = chuan_hoa_bao_cao_visual_qa(raw, ten_anh=file_luoi.name)
    except Exception as err:
        print(
            f"[CANH BAO] Bo qua Visual QA Gemini Vision (khong lam gian doan pipeline): {err}"
        )
        bao_cao = {
            "trangThai": "bo_qua_loi",
            "anhKiemDinh": file_luoi.name,
            "diemTongThe": None,
            "nhanXetChung": f"Khong the chay Visual QA tu dong: {err}",
            "danhSachCanhLoi": [],
            "deXuatSuaChung": [],
            "lyDoLoi": str(err)[:400],
        }

    file_bao_cao.write_text(
        json.dumps(bao_cao, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return bao_cao


def render_mot_hoi(
    slug: str,
    so_hoi: int,
    duong_dan_props: Path | None = None,
    bo_cache: bool = False,
    concurrency: int | None = None,
    jpeg_quality: int | None = None,
    che_do_ci: bool | None = None,
    thu_muc_out: Path | None = None,
    thu_muc_public: Path | None = None,
    npx_bin: str | None = None,
    command_runner: Callable[[list[str], Path | None], None] | None = None,
) -> dict[str, Any]:
    """
    Chi render dung 1 hoi theo so thu tu (1..N) de phuc vu chay song song (tuong thich nguoc 100%).
    Khong chay ghep FFmpeg, chapters, luoi kiem dinh, Visual QA hay Thumbnail.
    """
    file_props = duong_dan_props or (GOC_DU_AN / "du_lieu" / slug / "du_lieu_render.json")
    if not file_props.exists():
        raise FileNotFoundError(f"Khong tim thay du_lieu_render.json: {file_props}")

    du_lieu_raw = json.loads(file_props.read_text(encoding="utf-8"))
    du_lieu, ghi_chu_chuan_hoa = chuan_hoa_du_lieu_truoc_render(du_lieu_raw)
    pham_vi = tinh_pham_vi_frame_chuong(du_lieu)
    if not pham_vi:
        raise ValueError("du_lieu_render.json khong co hoi/canh nao de render.")

    ch_chon = next((ch for ch in pham_vi if int(ch["soHoi"]) == int(so_hoi)), None)
    if ch_chon is None:
        hop_le = [int(ch["soHoi"]) for ch in pham_vi]
        raise ValueError(f"So thu tu hoi khong hop le: {so_hoi}. Cac hoi hop le: {hop_le}")

    out_root = thu_muc_out or (GOC_DU_AN / "out")
    thu_muc_slug = out_root / slug
    thu_muc_hoi = thu_muc_slug / "chuong"
    thu_muc_hoi.mkdir(parents=True, exist_ok=True)

    file_props_render = file_props
    if ghi_chu_chuan_hoa:
        for gc in ghi_chu_chuan_hoa:
            print(f"[Chuan hoa render] {gc}")
        file_props_render = thu_muc_slug / "du_lieu_render_sach.json"
        file_props_render.write_text(
            json.dumps(du_lieu, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    file_cache_tong = thu_muc_slug / "cache_render.json"
    file_cache_hoi = thu_muc_hoi / f"cache_hoi_{ch_chon['soHoi']:02d}.json"
    cache_cu: dict[str, str] = {}
    if not bo_cache:
        for fc in (file_cache_tong, file_cache_hoi):
            if fc.exists():
                try:
                    loaded = json.loads(fc.read_text(encoding="utf-8"))
                    if isinstance(loaded, dict):
                        for k, v in loaded.items():
                            if isinstance(v, str):
                                cache_cu[k] = v
                except json.JSONDecodeError:
                    pass

    hash_moi = tinh_hash_chuong(du_lieu, ch_chon["chuongData"], thu_muc_public=thu_muc_public)
    file_hoi = thu_muc_hoi / f"hoi_{ch_chon['soHoi']:02d}.mp4"
    can_render = (
        bo_cache
        or not file_hoi.exists()
        or file_hoi.stat().st_size == 0
        or cache_cu.get(ch_chon["id"]) != hash_moi
    )

    runner = command_runner or _chay_lenh

    if can_render:
        print(
            f"[Render rieng] Hoi {ch_chon['soHoi']}/{len(pham_vi)} ({ch_chon['tenChuong']}) "
            f"frames {ch_chon['tuFrame']}-{ch_chon['endFrameInclusive']}"
        )
        cmd = dung_lenh_render_remotion(
            file_mp4=file_hoi,
            file_props=file_props_render,
            tu_frame=ch_chon["tuFrame"],
            end_frame_inclusive=ch_chon["endFrameInclusive"],
            npx_bin=npx_bin,
            concurrency=concurrency,
            jpeg_quality=jpeg_quality,
            che_do_ci=che_do_ci,
        )
        t_hoi = time.perf_counter()
        runner(cmd, GOC_DU_AN)
        print(f"[Thoi gian] Render rieng Hoi {ch_chon['soHoi']}/{len(pham_vi)}: {time.perf_counter() - t_hoi:.2f}s")

        # Ghi file cache rieng cua hoi (an toan cho song song)
        file_cache_hoi.write_text(
            json.dumps({ch_chon["id"]: hash_moi}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    else:
        print(f"[Bo qua] Hoi {ch_chon['soHoi']} ({ch_chon['tenChuong']}): khong doi (dung cache)")

    return {
        "cheDo": "chi_render_hoi",
        "soHoi": int(ch_chon["soHoi"]),
        "id": ch_chon["id"],
        "fileHoi": file_hoi,
        "hash": hash_moi,
        "daRender": can_render,
        "tuFrame": int(ch_chon["tuFrame"]),
        "endFrameInclusive": int(ch_chon["endFrameInclusive"]),
    }


def render_mot_chunk(
    slug: str,
    chunk_id: str,
    duong_dan_props: Path | None = None,
    bo_cache: bool = False,
    concurrency: int | None = None,
    jpeg_quality: int | None = None,
    che_do_ci: bool | None = None,
    fps: int = MAC_DINH_FPS,
    nguong_chia_chunk_giay: float = NGUONG_CHIA_CHUNK_GIAY,
    thu_muc_out: Path | None = None,
    thu_muc_public: Path | None = None,
    npx_bin: str | None = None,
    command_runner: Callable[[list[str], Path | None], None] | None = None,
) -> dict[str, Any]:
    """
    Render dung 1 chunk thoi luong (vd: `hoi_01`, `hoi_03_p1`, `hoi_03_p2`) cho GitHub Actions matrix.
    """
    file_props = duong_dan_props or (GOC_DU_AN / "du_lieu" / slug / "du_lieu_render.json")
    if not file_props.exists():
        raise FileNotFoundError(f"Khong tim thay du_lieu_render.json: {file_props}")

    du_lieu_raw = json.loads(file_props.read_text(encoding="utf-8"))
    du_lieu, ghi_chu_chuan_hoa = chuan_hoa_du_lieu_truoc_render(du_lieu_raw)
    ds_chunk = tinh_danh_sach_chunk_render(du_lieu, fps=fps, nguong_giay=nguong_chia_chunk_giay)
    if not ds_chunk:
        raise ValueError("du_lieu_render.json khong co chunk/canh nao de render.")

    cid_chuan = str(chunk_id or "").strip().lower()
    if cid_chuan.isdigit():
        cid_chuan = f"hoi_{int(cid_chuan):02d}"
    ck_chon = next((ck for ck in ds_chunk if ck["chunkId"].lower() == cid_chuan), None)
    if ck_chon is None:
        hop_le = [ck["chunkId"] for ck in ds_chunk]
        raise ValueError(f"Chunk ID khong hop le: {chunk_id!r}. Cac chunk hop le: {hop_le}")

    out_root = thu_muc_out or (GOC_DU_AN / "out")
    thu_muc_slug = out_root / slug
    thu_muc_hoi = thu_muc_slug / "chuong"
    thu_muc_hoi.mkdir(parents=True, exist_ok=True)

    file_props_render = file_props
    if ghi_chu_chuan_hoa:
        for gc in ghi_chu_chuan_hoa:
            print(f"[Chuan hoa render] {gc}")
        file_props_render = thu_muc_slug / "du_lieu_render_sach.json"
        file_props_render.write_text(
            json.dumps(du_lieu, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    file_cache_chunk = thu_muc_hoi / ck_chon["tenFileCache"]
    cache_cu: dict[str, str] = {}
    if not bo_cache and file_cache_chunk.exists():
        try:
            loaded = json.loads(file_cache_chunk.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                cache_cu = {str(k): str(v) for k, v in loaded.items() if isinstance(v, str)}
        except json.JSONDecodeError:
            pass

    hash_chuong = tinh_hash_chuong(du_lieu, ck_chon["chuongData"], thu_muc_public=thu_muc_public)
    hash_moi = hashlib.sha256(
        f"{hash_chuong}|{ck_chon['chunkId']}|{ck_chon['tuFrame']}-{ck_chon['endFrameInclusive']}".encode("utf-8")
    ).hexdigest()
    file_chunk = thu_muc_hoi / ck_chon["tenFileMp4"]
    can_render = (
        bo_cache
        or not file_chunk.exists()
        or file_chunk.stat().st_size == 0
        or cache_cu.get(ck_chon["chunkId"]) != hash_moi
    )

    runner = command_runner or _chay_lenh
    if can_render:
        print(
            f"[Render chunk] {ck_chon['chunkId']} ({ck_chon['tenChuong']}, ~{ck_chon['giay']}s) "
            f"frames {ck_chon['tuFrame']}-{ck_chon['endFrameInclusive']}"
        )
        cmd = dung_lenh_render_remotion(
            file_mp4=file_chunk,
            file_props=file_props_render,
            tu_frame=ck_chon["tuFrame"],
            end_frame_inclusive=ck_chon["endFrameInclusive"],
            npx_bin=npx_bin,
            concurrency=concurrency,
            jpeg_quality=jpeg_quality,
            che_do_ci=che_do_ci,
        )
        t_ck = time.perf_counter()
        runner(cmd, GOC_DU_AN)
        print(f"[Thoi gian] Render chunk {ck_chon['chunkId']}: {time.perf_counter() - t_ck:.2f}s")
        file_cache_chunk.write_text(
            json.dumps({ck_chon["chunkId"]: hash_moi}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    else:
        print(f"[Bo qua] Chunk {ck_chon['chunkId']} ({ck_chon['tenChuong']}): khong doi (dung cache)")

    return {
        "cheDo": "chi_render_chunk",
        "chunkId": ck_chon["chunkId"],
        "soHoi": int(ck_chon["soHoi"]),
        "phan": int(ck_chon["phan"]),
        "tongPhan": int(ck_chon["tongPhan"]),
        "fileChunk": file_chunk,
        "hash": hash_moi,
        "daRender": can_render,
        "tuFrame": int(ck_chon["tuFrame"]),
        "endFrameInclusive": int(ck_chon["endFrameInclusive"]),
        "giay": float(ck_chon["giay"]),
    }


def render_toan_bo_video(
    slug: str,
    duong_dan_props: Path | None = None,
    chuong_chon: str = "",
    nhac_nen: Path | None = None,
    tat_nhac_nen: bool = False,
    bo_cache: bool = False,
    chi_ghep: bool = False,
    chi_render_hoi: int | None = None,
    chi_render_chunk: str = "",
    chi_ghep_hoan_chinh: bool = False,
    bo_qua_thumbnail: bool = False,
    bo_qua_visual_qa: bool = False,
    concurrency: int | None = None,
    jpeg_quality: int | None = None,
    che_do_ci: bool | None = None,
    nguong_chia_chunk_giay: float = NGUONG_CHIA_CHUNK_GIAY,
    fps: int = MAC_DINH_FPS,
    gemini_client: GeminiClient | None = None,
    thu_muc_out: Path | None = None,
    thu_muc_public: Path | None = None,
    npx_bin: str | None = None,
    command_runner: Callable[[list[str], Path | None], None] | None = None,
    merge_fn: Callable[..., Path] | None = None,
    grid_fn: Callable[..., Path] | None = None,
) -> dict[str, Any]:
    """
    Dieu phoi render tach hoi / chunk thoi luong, luu hash cache, ghep FFmpeg, xuat chapters.txt, phu_de.srt, thumbnail A/B, luoi 18 khung & Visual QA.
    Ho tro tach pha song song:
      - chi_render_chunk=<chunk_id>: chi render dung 1 chunk (vd: hoi_01, hoi_03_p1, hoi_03_p2).
      - chi_render_hoi=<so>: chi render dung 1 hoi (tuong thich nguoc 100%).
      - chi_ghep_hoan_chinh=True (hoac bi danh cu chi_ghep=True): chi gom cac chunk/hoi da render san & xuat tron bo.
      - Mac dinh: chay day du 1 lenh cho may cuc bo.
    """
    bo_qua_render_hoi = bool(chi_ghep or chi_ghep_hoan_chinh)
    co_render_rieng = chi_render_hoi is not None or bool(str(chi_render_chunk or "").strip())
    if co_render_rieng and bo_qua_render_hoi:
        raise ValueError("Khong the ket hop --chi-render-hoi/--chi-render-chunk voi --chi-ghep-hoan-chinh / --chi-ghep.")
    if chi_render_hoi is not None and str(chi_render_chunk or "").strip():
        raise ValueError("Khong the ket hop --chi-render-hoi voi --chi-render-chunk cung luc.")

    if str(chi_render_chunk or "").strip():
        return render_mot_chunk(
            slug=slug,
            chunk_id=str(chi_render_chunk).strip(),
            duong_dan_props=duong_dan_props,
            bo_cache=bo_cache,
            concurrency=concurrency,
            jpeg_quality=jpeg_quality,
            che_do_ci=che_do_ci,
            fps=fps,
            nguong_chia_chunk_giay=nguong_chia_chunk_giay,
            thu_muc_out=thu_muc_out,
            thu_muc_public=thu_muc_public,
            npx_bin=npx_bin,
            command_runner=command_runner,
        )

    if chi_render_hoi is not None:
        return render_mot_hoi(
            slug=slug,
            so_hoi=int(chi_render_hoi),
            duong_dan_props=duong_dan_props,
            bo_cache=bo_cache,
            concurrency=concurrency,
            jpeg_quality=jpeg_quality,
            che_do_ci=che_do_ci,
            thu_muc_out=thu_muc_out,
            thu_muc_public=thu_muc_public,
            npx_bin=npx_bin,
            command_runner=command_runner,
        )

    file_props = duong_dan_props or (GOC_DU_AN / "du_lieu" / slug / "du_lieu_render.json")
    if not file_props.exists():
        raise FileNotFoundError(f"Khong tim thay du_lieu_render.json: {file_props}")

    du_lieu_raw = json.loads(file_props.read_text(encoding="utf-8"))
    du_lieu, ghi_chu_chuan_hoa = chuan_hoa_du_lieu_truoc_render(du_lieu_raw)
    pham_vi = tinh_pham_vi_frame_chuong(du_lieu)
    if not pham_vi:
        raise ValueError("du_lieu_render.json khong co hoi/canh nao de render.")

    out_root = thu_muc_out or (GOC_DU_AN / "out")
    thu_muc_slug = out_root / slug
    thu_muc_hoi = thu_muc_slug / "chuong"
    thu_muc_hoi.mkdir(parents=True, exist_ok=True)

    file_props_render = file_props
    if ghi_chu_chuan_hoa:
        for gc in ghi_chu_chuan_hoa:
            print(f"[Chuan hoa render] {gc}")
        file_props_render = thu_muc_slug / "du_lieu_render_sach.json"
        file_props_render.write_text(
            json.dumps(du_lieu, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

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
        thu_muc_public=thu_muc_public,
    )

    bin_cmd = npx_bin or shutil.which("npx") or ("npx.cmd" if os.name == "nt" else "npx")
    runner = command_runner or _chay_lenh
    ham_ghep = merge_fn or ghep_cac_hoi_ffmpeg
    ham_luoi = grid_fn or tao_luoi_kiem_dinh_tu_video
    cache_moi = dict(cache_cu)

    if not bo_qua_render_hoi:
        for ch, hash_moi, can_render, ly_do in ke_hoach:
            file_hoi = thu_muc_hoi / f"hoi_{ch['soHoi']:02d}.mp4"
            if not can_render:
                print(f"[Bo qua] Hoi {ch['soHoi']} ({ch['tenChuong']}): {ly_do}")
                continue
            print(
                f"[Render] Hoi {ch['soHoi']}/{len(pham_vi)} ({ch['tenChuong']}) "
                f"frames {ch['tuFrame']}-{ch['endFrameInclusive']} | Ly do: {ly_do}"
            )
            cmd = dung_lenh_render_remotion(
                file_mp4=file_hoi,
                file_props=file_props_render,
                tu_frame=ch["tuFrame"],
                end_frame_inclusive=ch["endFrameInclusive"],
                npx_bin=bin_cmd,
                concurrency=concurrency,
                jpeg_quality=jpeg_quality,
                che_do_ci=che_do_ci,
            )
            t_hoi = time.perf_counter()
            runner(cmd, GOC_DU_AN)
            print(f"[Thoi gian] Render Hoi {ch['soHoi']}/{len(pham_vi)}: {time.perf_counter() - t_hoi:.2f}s")
            cache_moi[ch["id"]] = hash_moi
            file_cache.write_text(
                json.dumps(cache_moi, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
                newline="\n",
            )

    # Kiem tra du file hoi/chunk theo dung thu tu thoi gian truoc khi ghep
    ds_chunk = tinh_danh_sach_chunk_render(du_lieu, fps=fps, nguong_giay=nguong_chia_chunk_giay)
    ds_file_hoi = giai_danh_sach_file_ghep(
        pham_vi_chuong=pham_vi,
        thu_muc_hoi=thu_muc_hoi,
        danh_sach_chunk=ds_chunk,
    )

    # 1. Ghep video tong (+ nhac nen auto-ducking & chuan hoa -14 LUFS) vao out/<slug>/video_hoan_chinh.mp4 va dong bo out/<slug>.mp4
    t_ghep = time.perf_counter()
    file_video_cuoi = thu_muc_slug / "video_hoan_chinh.mp4"
    ham_ghep(
        ds_file_hoi,
        file_video_cuoi,
        nhac_nen=nhac_nen,
        tat_nhac_nen=tat_nhac_nen,
    )
    print(f"[OK] Video hoan chinh: {file_video_cuoi} ({time.perf_counter() - t_ghep:.2f}s)")

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

    # 3. Xuat phu de chuan SubRip out/<slug>/phu_de.srt
    file_srt = xuat_file_srt(du_lieu, thu_muc_slug / "phu_de.srt", fps=fps)
    print(f"[OK] Phu de chuan YouTube (.srt): {file_srt}")

    # 4. Xuat anh luoi kiem dinh 18 khung hinh (trich nhanh theo keyframe FFmpeg, khong goi Remotion)
    file_luoi = thu_muc_slug / "luoi_kiem_dinh.png"
    ham_luoi_kwargs: dict[str, Any] = {
        "pham_vi_chuong": pham_vi,
        "thu_muc_hoi": thu_muc_hoi,
        "file_anh_xuat": file_luoi,
        "tieu_de": str(du_lieu.get("tieuDe") or slug),
        "fps": fps,
    }
    if grid_fn is None:
        ham_luoi_kwargs["file_video_tong"] = file_video_cuoi
    ham_luoi(**ham_luoi_kwargs)
    print(f"[OK] Luoi kiem dinh 18 khung hinh: {file_luoi}")

    ket_qua_xuat: dict[str, Any] = {
        "video": file_video_cuoi,
        "video_legacy": file_video_legacy,
        "chapters": file_chapters,
        "chapters_va_mo_ta": file_chapters_mo_ta,
        "phu_de_srt": file_srt,
        "luoi": file_luoi,
    }

    # 5. Tu kiem dinh thi giac (Visual QA) bang Gemini Vision tren luoi_kiem_dinh.png
    if not bo_qua_visual_qa:
        file_visual_qa = thu_muc_slug / "bao_cao_visual_qa.json"
        bao_cao_qa = chay_visual_qa_gemini(
            file_luoi=file_luoi,
            file_bao_cao=file_visual_qa,
            tieu_de=str(du_lieu.get("tieuDe") or slug),
            client=gemini_client,
        )
        ket_qua_xuat["bao_cao_visual_qa"] = file_visual_qa
        if bao_cao_qa.get("trangThai") == "hoan_thanh":
            print(
                f"[OK] Visual QA (Gemini Vision): {bao_cao_qa.get('diemTongThe')}/10 | "
                f"{len(bao_cao_qa.get('danhSachCanhLoi') or [])} canh luu y -> {file_visual_qa}"
            )

    # 6. Tu dong render 3 mau Thumbnail A/B (thumbnail_1.png .. thumbnail_3.png) bang Remotion <Still>
    if not bo_qua_thumbnail:
        try:
            ds_thumb = render_bo_thumbnail(
                du_lieu,
                thu_muc_slug,
                npx_bin=bin_cmd,
                command_runner=runner,
            )
            ket_qua_xuat["thumbnails"] = ds_thumb
            print(
                f"[OK] Da render {len(ds_thumb)} bien the Thumbnail A/B: "
                + ", ".join(p.name for p in ds_thumb)
            )
        except Exception as err:
            print(
                f"[CANH BAO] Render Thumbnail A/B gap loi (khong lam mat video da xuat): {err}"
            )

    return ket_qua_xuat


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render tach hoi chong tran RAM (ho tro song song), ghep FFmpeg, nhac nen, Thumbnail A/B, luoi 18 khung & Visual QA."
    )
    parser.add_argument("--slug", required=True, help="Ten slug du an trong du_lieu/<slug>/.")
    parser.add_argument("--input", default="", help="Duong dan tuy chinh toi du_lieu_render.json.")
    parser.add_argument(
        "--chuong",
        default="",
        help="Chi ep render lai cac hoi cu the (vd: --chuong 2,4).",
    )
    parser.add_argument(
        "--chi-render-hoi",
        type=int,
        default=None,
        help="Chi render dung 1 hoi theo so thu tu (vd: --chi-render-hoi 1) de phuc vu chay song song theo matrix.",
    )
    parser.add_argument(
        "--chi-render-chunk",
        default="",
        help="Chi render dung 1 chunk thoi luong (vd: --chi-render-chunk hoi_03_p1 hoac hoi_01) cho GitHub Actions matrix.",
    )
    parser.add_argument(
        "--nguong-chia-chunk",
        type=float,
        default=NGUONG_CHIA_CHUNK_GIAY,
        help="Nguong giay toi da moi chunk (mac dinh 120s; hoi vuot nguong se tu dong chia thanh 2 manh).",
    )
    parser.add_argument(
        "--chi-ghep-hoan-chinh",
        action="store_true",
        help="Gom cac chunk/hoi da render san, ghep FFmpeg auto-ducking -14 LUFS, xuat chapters, phu_de.srt, luoi 18 khung, Thumbnail A/B & Visual QA.",
    )
    parser.add_argument(
        "--nhac-nen",
        default="",
        help="File MP3 nhac nen tuy chinh (mac dinh tu dong dung public/bgm/nhac_nen_nhe.mp3 neu co, auto-ducking + -14 LUFS).",
    )
    parser.add_argument(
        "--tat-nhac-nen",
        action="store_true",
        help="Tat nhac nen khi ghep video (van giu chuan hoa am luong -14 LUFS cho giong thoai).",
    )
    parser.add_argument("--bo-cache", action="store_true", help="Render lai toan bo tat ca cac hoi.")
    parser.add_argument(
        "--chi-ghep",
        action="store_true",
        help="Bi danh tuong thich cu cua --chi-ghep-hoan-chinh.",
    )
    parser.add_argument(
        "--bo-qua-thumbnail",
        action="store_true",
        help="Bo qua buoc tu dong render 3 mau Thumbnail A/B (thumbnail_1..3.png).",
    )
    parser.add_argument(
        "--bo-qua-visual-qa",
        action="store_true",
        help="Bo qua buoc gui luoi_kiem_dinh.png cho Gemini Vision kiem dinh thi giac.",
    )
    parser.add_argument("--concurrency", type=int, default=0, help="So luong song song truyen cho Remotion.")
    parser.add_argument(
        "--jpeg-quality",
        type=int,
        default=0,
        help="Chat luong JPEG frame tam cho Remotion (tu dong 85 khi CI=true hoac --che-do-ci).",
    )
    parser.add_argument(
        "--che-do-ci",
        action="store_true",
        help="Ep dung bo thong so an toan cho GitHub Actions runner (--concurrency=2, --jpeg-quality=85, --log=warn).",
    )
    parser.add_argument("--fps", type=int, default=MAC_DINH_FPS, help="So khung hinh/giay (mac dinh 30).")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    if args.chi_render_hoi is not None and args.chi_render_hoi <= 0:
        print("[LOI] --chi-render-hoi phai la so nguyen duong (>= 1).")
        return 2
    if args.chi_render_hoi is not None and args.chi_render_chunk.strip():
        print("[LOI] Khong the ket hop --chi-render-hoi voi --chi-render-chunk.")
        return 2
    if (args.chi_render_hoi is not None or args.chi_render_chunk.strip()) and (args.chi_ghep or args.chi_ghep_hoan_chinh):
        print("[LOI] Khong the ket hop --chi-render-hoi/--chi-render-chunk voi --chi-ghep-hoan-chinh / --chi-ghep.")
        return 2

    render_toan_bo_video(
        slug=args.slug.strip(),
        duong_dan_props=Path(args.input) if args.input else None,
        chuong_chon=args.chuong,
        nhac_nen=Path(args.nhac_nen) if args.nhac_nen else None,
        tat_nhac_nen=args.tat_nhac_nen,
        bo_cache=args.bo_cache,
        chi_ghep=args.chi_ghep,
        chi_render_hoi=args.chi_render_hoi,
        chi_render_chunk=args.chi_render_chunk.strip(),
        chi_ghep_hoan_chinh=args.chi_ghep_hoan_chinh,
        bo_qua_thumbnail=args.bo_qua_thumbnail,
        bo_qua_visual_qa=args.bo_qua_visual_qa,
        concurrency=args.concurrency if args.concurrency > 0 else None,
        jpeg_quality=args.jpeg_quality if args.jpeg_quality > 0 else None,
        che_do_ci=True if args.che_do_ci else None,
        nguong_chia_chunk_giay=args.nguong_chia_chunk,
        fps=args.fps,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
