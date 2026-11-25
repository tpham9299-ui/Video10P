# -*- coding: utf-8 -*-
"""Lenh chay 1 cham tu 1 cau chu de -> kich ban 6 hoi -> TTS cache -> render tach hoi & luoi kiem dinh."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.chuanbi_dai import MAC_DINH_FPS, MAC_DINH_RATE, chuan_bi_audio_va_du_lieu_render
from scripts.pipeline.render_dai import render_toan_bo_video
from scripts.pipeline.tao_kich_ban_10p import bien_kich_3_tang, tao_slug


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Pipeline 1 cham san xuat phim hoat hinh ke chuyen lich su Toan hoc >10 phut."
    )
    parser.add_argument(
        "--chu-de",
        default="",
        help="Chu de cau chuyen Toan hoc (bat buoc tru khi dung --tiep-tuc-tu-kich-ban).",
    )
    parser.add_argument(
        "--slug",
        default="",
        help="Ten thu muc du an du_lieu/<slug>/ (tu dong tao tu --chu-de neu de trong).",
    )
    parser.add_argument(
        "--muc-tieu-phut",
        type=float,
        default=11.0,
        help="Thoi luong muc tieu tinh bang phut (mac dinh 11, bao dam > 10 phut).",
    )
    parser.add_argument(
        "--giong-ke",
        default="di_dom_gan_gui",
        help="Phong cach ke chuyen (mac dinh: di_dom_gan_gui).",
    )
    parser.add_argument(
        "--dung-de-duyet",
        action="store_true",
        help="Dung sau khi tao doc_duyet_kich_ban.md de nguoi dung doc/sua truoc khi tao TTS va render.",
    )
    parser.add_argument(
        "--tiep-tuc-tu-kich-ban",
        action="store_true",
        help="Bo qua buoc goi AI bien kich, chay tiep tu du_lieu/<slug>/nhap_kich_ban.json da duyet.",
    )
    parser.add_argument(
        "--chi-tao-audio",
        action="store_true",
        help="Dung sau khi tao TTS va du_lieu_render.json (de xem truoc trong Remotion Studio).",
    )
    parser.add_argument("--giong", default="", help="Giong Edge TTS (mac dinh vi-VN-NamMinhNeural).")
    parser.add_argument("--toc-do", default=MAC_DINH_RATE, help="Toc do doc TTS (mac dinh +0%%).")
    parser.add_argument("--nhac-nen", default="", help="File MP3 nhac nen tuy chinh (mac dinh dung public/bgm/nhac_nen_nhe.mp3).")
    parser.add_argument("--tat-nhac-nen", action="store_true", help="Tat nhac nen khi xuat video.")
    parser.add_argument("--chuong", default="", help="Chi ep render lai cac hoi cu the (vd: 2,4).")
    parser.add_argument("--bo-cache", action="store_true", help="Bo qua cache o cac buoc duoc chay.")
    parser.add_argument("--tat-anh-ai", action="store_true", help="Tat sinh anh boi canh minh hoa AI (dung nen SVG).")
    parser.add_argument("--bo-qua-thumbnail", action="store_true", help="Bo qua buoc render 3 mau Thumbnail A/B.")
    parser.add_argument("--bo-qua-visual-qa", action="store_true", help="Bo qua buoc Visual QA Gemini Vision.")
    parser.add_argument("--concurrency", type=int, default=0, help="So luong song song cho Remotion.")
    parser.add_argument("--fps", type=int, default=MAC_DINH_FPS, help="So khung hinh/giay (mac dinh 30).")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)

    if not args.tiep_tuc_tu_kich_ban and not args.chu_de.strip():
        print("[LOI] Can truyen --chu-de \"...\" (hoac dung --tiep-tuc-tu-kich-ban --slug <ten>).")
        return 2

    slug = args.slug.strip() or tao_slug(args.chu_de)
    if not slug:
        print("[LOI] Khong xac dinh duoc --slug.")
        return 2

    print("=" * 72)
    print(f"PIPELINE PHIM HOAT HINH TOAN HOC >10 PHUT | SLUG: {slug}")
    print("=" * 72)

    # BUOC 1: BIEN KICH 3 TANG
    if not args.tiep_tuc_tu_kich_ban:
        file_json, file_md, _ = bien_kich_3_tang(
            chu_de=args.chu_de.strip(),
            slug=slug,
            muc_tieu_phut=args.muc_tieu_phut,
            giong_ke=args.giong_ke,
            bo_cache=args.bo_cache,
        )
        if args.dung_de_duyet:
            print("\n" + "-" * 72)
            print("[TAM DUNG DE DUYET KICH BAN]")
            print(f"1. Mo file doc duyet (doc nhanh ~3 phut): {file_md}")
            print(f"2. Neu muon sua loi thoai/canh, sua tai: {file_json}")
            print("3. Khi da ung y, chay tiep lenh sau de tao giong doc TTS va render video:")
            print(f"   python -X utf8 scripts/pipeline/chay_tu_dong.py --slug {slug} --tiep-tuc-tu-kich-ban")
            print("-" * 72)
            return 0
    else:
        print(f"[Buoc 1] Bo qua bien kich, dung san du_lieu/{slug}/nhap_kich_ban.json")

    # BUOC 2: TAO GIONG DOC TTS CO CACHE, TINH FRAME 30FPS & SINH BOI CANH MINH HOA AI
    file_render, _ = chuan_bi_audio_va_du_lieu_render(
        slug=slug,
        voice=args.giong.strip() or None,
        rate=args.toc_do,
        fps=args.fps,
        bo_cache=args.bo_cache,
        tat_anh_ai=args.tat_anh_ai,
    )
    if args.chi_tao_audio:
        print(f"\n[TAM DUNG] Da san sang {file_render}. Co the xem truoc trong Remotion Studio hoac chay render_dai.py.")
        return 0

    # BUOC 3: RENDER TACH HOI, GHEP FFMPEG, CHAPTERS, LUOI KIEM DINH, VISUAL QA & THUMBNAIL A/B
    ket_qua = render_toan_bo_video(
        slug=slug,
        duong_dan_props=file_render,
        chuong_chon=args.chuong,
        nhac_nen=Path(args.nhac_nen) if args.nhac_nen else None,
        tat_nhac_nen=args.tat_nhac_nen,
        bo_cache=args.bo_cache,
        bo_qua_thumbnail=args.bo_qua_thumbnail,
        bo_qua_visual_qa=args.bo_qua_visual_qa,
        concurrency=args.concurrency if args.concurrency > 0 else None,
        fps=args.fps,
    )

    print("\n" + "=" * 72)
    print("[HOAN TAT] Da xuat tron bo san pham:")
    print(f"  - Video cuoi cung   : {ket_qua['video']}")
    print(f"  - Moc chuong YouTube: {ket_qua['chapters']}")
    if "chapters_va_mo_ta" in ket_qua:
        print(f"  - Tron goi YouTube  : {ket_qua['chapters_va_mo_ta']}")
    if "phu_de_srt" in ket_qua:
        print(f"  - Phu de YouTube SRT: {ket_qua['phu_de_srt']}")
    print(f"  - Luoi kiem dinh 18 : {ket_qua['luoi']}")
    if "bao_cao_visual_qa" in ket_qua:
        print(f"  - Bao cao Visual QA : {ket_qua['bao_cao_visual_qa']}")
    if "thumbnails" in ket_qua:
        print("  - Thumbnail A/B     : " + ", ".join(str(p) for p in ket_qua["thumbnails"]))
    print("=" * 72)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
