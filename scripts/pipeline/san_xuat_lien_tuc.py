# -*- coding: utf-8 -*-
"""Bo dieu phoi AI san xuat video lich su Toan hoc >10 phut tu chu hoan toan theo hang doi."""

from __future__ import annotations

import argparse
import datetime
import sys
import time
from pathlib import Path
from typing import Any, Callable

GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.bo_nho_hoc_hoi import (
    DUONG_DAN_BO_NHO_MAC_DINH,
    cap_nhat_trang_thai_hang_doi,
    chon_chu_de_tiep_theo,
    dem_chu_de_dang_cho,
    ghi_nhan_tap_hoan_thanh,
    luu_bo_nho,
    tai_bo_nho,
    them_chu_de_hang_doi,
)
from scripts.pipeline.chuanbi_dai import (
    MAC_DINH_FPS,
    MAC_DINH_RATE,
    chuan_bi_audio_va_du_lieu_render,
)
from scripts.pipeline.gemini_client import GeminiClient
from scripts.pipeline.render_dai import render_toan_bo_video
from scripts.pipeline.san_tim_chu_de import nap_hang_doi_chu_de, nghien_cuu_chu_de
from scripts.pipeline.tao_kich_ban_10p import bien_kich_3_tang, tao_slug

NGUONG_TOI_THIEU_HANG_DOI = 3
SO_LUONG_NAP_MAC_DINH = 5


def _ghi_nhat_ky_loi(duong_dan_log: Path, thong_diep: str) -> None:
    duong_dan_log.parent.mkdir(parents=True, exist_ok=True)
    moc = datetime.datetime.now().replace(microsecond=0).isoformat()
    with duong_dan_log.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"[{moc}] {thong_diep}\n")


def san_xuat_mot_tap(
    chu_de_tuy_chon: str = "",
    slug_tuy_chon: str = "",
    chi_tao_kich_ban: bool = False,
    muc_tieu_phut: float = 11.0,
    giong_ke: str = "di_dom_gan_gui",
    voice: str | None = None,
    rate: str = MAC_DINH_RATE,
    nhac_nen: Path | None = None,
    concurrency: int | None = None,
    fps: int = MAC_DINH_FPS,
    bo_cache: bool = False,
    duong_dan_bo_nho: Path | str | None = None,
    thu_muc_du_lieu: Path | None = None,
    loai_tru_slugs: set[str] | None = None,
    nguong_hang_doi: int = NGUONG_TOI_THIEU_HANG_DOI,
    so_luong_nap: int = SO_LUONG_NAP_MAC_DINH,
    client: GeminiClient | None = None,
    nap_hang_doi_fn: Callable[..., list[dict[str, Any]]] | None = None,
    nghien_cuu_fn: Callable[..., tuple[Path, dict[str, Any]]] | None = None,
    bien_kich_fn: Callable[..., tuple[Path, Path, dict[str, Any]]] | None = None,
    tts_fn: Callable[..., tuple[Path, dict[str, Any]]] | None = None,
    render_fn: Callable[..., dict[str, Path]] | None = None,
) -> dict[str, Any]:
    """
    Chay tron ven 1 chu trinh san xuat tu chu:
    Kiem tra hang doi (<3 -> tu nap 5) -> Chon chu de diem cao nhat -> Nghien cuu web
    -> Bien kich 3 tang + tu kiem dinh -> TTS -> Render & YouTube bundle -> Cap nhat bo_nho_hoc_hoi.json.
    """
    path_bo_nho = Path(duong_dan_bo_nho) if duong_dan_bo_nho is not None else DUONG_DAN_BO_NHO_MAC_DINH
    bo_nho = tai_bo_nho(path_bo_nho)

    ham_nap = nap_hang_doi_fn or nap_hang_doi_chu_de
    ham_nghien_cuu = nghien_cuu_fn or nghien_cuu_chu_de
    ham_bien_kich = bien_kich_fn or bien_kich_3_tang
    ham_tts = tts_fn or chuan_bi_audio_va_du_lieu_render
    ham_render = render_fn or render_toan_bo_video

    goc_khai_thac = ""
    tu_hang_doi = False

    if chu_de_tuy_chon.strip():
        chu_de_chinh = chu_de_tuy_chon.strip()
        slug = tao_slug(slug_tuy_chon.strip() or chu_de_chinh)
        # Them vao hang doi o trang thai dang_lam neu chua co
        them_chu_de_hang_doi(
            bo_nho,
            [
                {
                    "slug": slug,
                    "tieuDe": chu_de_chinh,
                    "gocKhaiThac": "Chu de dat hang rieng",
                    "diemThuHut": 9.5,
                    "doSauToanHoc": 9.0,
                    "trangThai": "dang_lam",
                }
            ],
        )
        cap_nhat_trang_thai_hang_doi(bo_nho, slug, "dang_lam")
        luu_bo_nho(bo_nho, path_bo_nho)
    else:
        tu_hang_doi = True
        so_cho = dem_chu_de_dang_cho(bo_nho)
        if so_cho < nguong_hang_doi:
            print(
                f"[Hang doi] Chi con {so_cho} chu de 'cho' (< {nguong_hang_doi}). "
                f"Tu dong san them {so_luong_nap} chu de moi tu mang..."
            )
            ham_nap(so_luong=so_luong_nap, duong_dan_bo_nho=path_bo_nho, client=client)
            bo_nho = tai_bo_nho(path_bo_nho)

        muc_chon = chon_chu_de_tiep_theo(bo_nho, loai_tru_slugs=loai_tru_slugs)
        if muc_chon is None:
            # Thu nap them 1 lan nua neu tat ca ung vien dang co bi bo qua
            print("[Hang doi] Khong con chu de kha dung trong hang doi, thu san bo sung...")
            ham_nap(so_luong=so_luong_nap, duong_dan_bo_nho=path_bo_nho, client=client)
            bo_nho = tai_bo_nho(path_bo_nho)
            muc_chon = chon_chu_de_tiep_theo(bo_nho, loai_tru_slugs=loai_tru_slugs)

        if muc_chon is None:
            raise RuntimeError("Khong tim duoc chu de nao co trangThai='cho' trong hang_doi_chu_de.")

        slug = str(muc_chon["slug"])
        chu_de_chinh = str(muc_chon["tieuDe"])
        goc_khai_thac = str(muc_chon.get("gocKhaiThac") or "")
        cap_nhat_trang_thai_hang_doi(bo_nho, slug, "dang_lam")
        luu_bo_nho(bo_nho, path_bo_nho)

    print("=" * 76)
    print(f"[SAN XUAT TU CHU] Slug: {slug} | Chu de: {chu_de_chinh}")
    print("=" * 76)

    try:
        # 1. Nghien cuu tu lieu tren web + Wikipedia
        file_tu_lieu, tu_lieu = ham_nghien_cuu(
            slug=slug,
            chu_de=chu_de_chinh,
            goc_khai_thac=goc_khai_thac,
            thu_muc_du_lieu=thu_muc_du_lieu,
            duong_dan_bo_nho=path_bo_nho,
            client=client,
            bo_cache=bo_cache,
        )

        # 2. Bien kich 3 tang (>10 phut) + tu kiem dinh & tu hoc
        file_nhap, file_md, kich_ban = ham_bien_kich(
            chu_de=chu_de_chinh,
            slug=slug,
            muc_tieu_phut=muc_tieu_phut,
            giong_ke=giong_ke,
            bo_cache=bo_cache,
            client=client,
            thu_muc_du_lieu=thu_muc_du_lieu,
            tu_lieu_nghien_cuu=tu_lieu,
            duong_dan_bo_nho=path_bo_nho,
            bat_tu_kiem_dinh=True,
        )

        ket_qua: dict[str, Any] = {
            "trangThai": "thanh_cong",
            "slug": slug,
            "tieuDe": str(kich_ban.get("tieuDe") or chu_de_chinh),
            "tuLieu": str(file_tu_lieu),
            "kichBan": str(file_nhap),
            "docDuyet": str(file_md),
            "chiTaoKichBan": chi_tao_kich_ban,
        }

        if chi_tao_kich_ban:
            print(f"[TAM DUNG] Che do --chi-tao-kich-ban: da hoan tat kich ban tai {file_md}")
            if tu_hang_doi:
                bo_nho_ht = tai_bo_nho(path_bo_nho)
                cap_nhat_trang_thai_hang_doi(bo_nho_ht, slug, "cho")
                luu_bo_nho(bo_nho_ht, path_bo_nho)
            return ket_qua

        # 3. Tao giong doc TTS co cache SHA-256 & tinh frame 30fps
        file_render, thong_ke_tts = ham_tts(
            slug=slug,
            duong_dan_nhap=file_nhap,
            voice=voice,
            rate=rate,
            fps=fps,
            bo_cache=bo_cache,
            thu_muc_du_lieu=thu_muc_du_lieu,
        )

        # 4. Render tach hoi, ghep FFmpeg, xuat chapters_va_mo_ta.txt & luoi 18 khung hinh
        san_pham = ham_render(
            slug=slug,
            duong_dan_props=file_render,
            nhac_nen=nhac_nen,
            bo_cache=bo_cache,
            concurrency=concurrency,
            fps=fps,
        )

        # 5. Cap nhat chu_de_da_lam & danh dau 'xong' trong bo_nho_hoc_hoi.json
        ds_nv = kich_ban.get("danhSachNhanVat") or []
        nhan_vat_chinh = (
            ", ".join(str(nv.get("ten") or "") for nv in ds_nv[:2] if isinstance(nv, dict) and nv.get("ten"))
            or "Nhà Toán học"
        )
        tom_tat_1_cau = (
            str(tu_lieu.get("tomTat1Cau") or "").strip()
            or str(kich_ban.get("chuDe") or chu_de_chinh).strip()
        )
        thoi_luong_giay = float(thong_ke_tts.get("tongGiay") or 0.0)
        nguon_tk = list(tu_lieu.get("nguonThamKhao") or [])

        bo_nho_sau = tai_bo_nho(path_bo_nho)
        ghi_nhan_tap_hoan_thanh(
            bo_nho_sau,
            slug=slug,
            tieu_de=str(kich_ban.get("tieuDe") or chu_de_chinh),
            nhan_vat_chinh=nhan_vat_chinh,
            tom_tat_1_cau=tom_tat_1_cau,
            thoi_luong_giay=thoi_luong_giay,
            nguon_tham_khao=nguon_tk,
        )
        luu_bo_nho(bo_nho_sau, path_bo_nho)

        ket_qua["thoiLuongGiay"] = thoi_luong_giay
        ket_qua["sanPham"] = {k: str(v) for k, v in san_pham.items()}
        print(
            f"[HOAN TAT TAP] {slug} ({thoi_luong_giay:.1f}s) | Da cap nhat bo_nho_hoc_hoi.json (trangThai='xong')."
        )
        return ket_qua

    except Exception as err:
        # Tra lai trang thai 'cho' de chu de khong bi ket mai o 'dang_lam'
        bo_nho_loi = tai_bo_nho(path_bo_nho)
        cap_nhat_trang_thai_hang_doi(bo_nho_loi, slug, "cho")
        luu_bo_nho(bo_nho_loi, path_bo_nho)
        if loai_tru_slugs is not None and slug:
            loai_tru_slugs.add(slug)
        try:
            setattr(err, "slug_that_bai", slug)
        except Exception:
            pass
        raise


def chay_san_xuat_lien_tuc(
    so_tap: int = 1,
    nghi_giay: float = 30.0,
    chu_de: str = "",
    slug: str = "",
    chi_tao_kich_ban: bool = False,
    muc_tieu_phut: float = 11.0,
    giong_ke: str = "di_dom_gan_gui",
    voice: str | None = None,
    rate: str = MAC_DINH_RATE,
    nhac_nen: Path | None = None,
    concurrency: int | None = None,
    fps: int = MAC_DINH_FPS,
    bo_cache: bool = False,
    duong_dan_bo_nho: Path | str | None = None,
    thu_muc_du_lieu: Path | None = None,
    file_log: Path | None = None,
    sleep_fn: Callable[[float], None] | None = None,
    client: GeminiClient | None = None,
    nap_hang_doi_fn: Callable[..., list[dict[str, Any]]] | None = None,
    nghien_cuu_fn: Callable[..., tuple[Path, dict[str, Any]]] | None = None,
    bien_kich_fn: Callable[..., tuple[Path, Path, dict[str, Any]]] | None = None,
    tts_fn: Callable[..., tuple[Path, dict[str, Any]]] | None = None,
    render_fn: Callable[..., dict[str, Path]] | None = None,
) -> list[dict[str, Any]]:
    """
    San xuat lien tiep N tap (mac dinh 1). Neu 1 tap gap loi thi ghi log, bo qua slug loi trong phien
    va tiep tuc tap tiep theo sau --nghi-giay.
    """
    tong_tap = 1 if chu_de.strip() else max(1, int(so_tap))
    ham_ngu = sleep_fn or time.sleep
    path_log = file_log or ((thu_muc_du_lieu or (GOC_DU_AN / "du_lieu")) / "nhat_ky_san_xuat.log")
    path_bo_nho = Path(duong_dan_bo_nho) if duong_dan_bo_nho is not None else DUONG_DAN_BO_NHO_MAC_DINH

    ket_qua_tong: list[dict[str, Any]] = []
    slugs_bi_loi: set[str] = set()

    for chi_so in range(1, tong_tap + 1):
        print(f"\n>>> BAT DAU TAP {chi_so}/{tong_tap} <<<")
        slug_du_kien = ""
        if not chu_de.strip():
            bo_nho_hien_tai = tai_bo_nho(path_bo_nho)
            muc_truoc = chon_chu_de_tiep_theo(bo_nho_hien_tai, loai_tru_slugs=slugs_bi_loi)
            if muc_truoc:
                slug_du_kien = str(muc_truoc.get("slug") or "")
        else:
            slug_du_kien = tao_slug(slug or chu_de)

        try:
            kq = san_xuat_mot_tap(
                chu_de_tuy_chon=chu_de if chi_so == 1 else "",
                slug_tuy_chon=slug if chi_so == 1 else "",
                chi_tao_kich_ban=chi_tao_kich_ban,
                muc_tieu_phut=muc_tieu_phut,
                giong_ke=giong_ke,
                voice=voice,
                rate=rate,
                nhac_nen=nhac_nen,
                concurrency=concurrency,
                fps=fps,
                bo_cache=bo_cache,
                duong_dan_bo_nho=path_bo_nho,
                thu_muc_du_lieu=thu_muc_du_lieu,
                loai_tru_slugs=slugs_bi_loi,
                client=client,
                nap_hang_doi_fn=nap_hang_doi_fn,
                nghien_cuu_fn=nghien_cuu_fn,
                bien_kich_fn=bien_kich_fn,
                tts_fn=tts_fn,
                render_fn=render_fn,
            )
            ket_qua_tong.append(kq)
        except Exception as err:
            slug_loi = str(getattr(err, "slug_that_bai", "") or slug_du_kien)
            if slug_loi:
                slugs_bi_loi.add(slug_loi)
            thong_diep = f"Tap {chi_so}/{tong_tap} (slug={slug_loi or 'tu_dong'}) that bai: {err}"
            print(f"[LOI TAP] {thong_diep}")
            _ghi_nhat_ky_loi(path_log, thong_diep)
            ket_qua_tong.append(
                {
                    "trangThai": "loi",
                    "slug": slug_loi,
                    "loi": str(err),
                }
            )

        if chi_so < tong_tap and nghi_giay > 0:
            print(f"[Nghi] Cho {nghi_giay:.1f}s truoc khi chuyen sang tap {chi_so + 1}/{tong_tap}...")
            ham_ngu(nghi_giay)

    so_ok = sum(1 for r in ket_qua_tong if r.get("trangThai") == "thanh_cong")
    so_loi = len(ket_qua_tong) - so_ok
    print("\n" + "=" * 76)
    print(f"[TONG KET SAN XUAT LIEN TUC] Thanh cong: {so_ok}/{len(ket_qua_tong)} | Loi: {so_loi}")
    print("=" * 76)
    return ket_qua_tong


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="He thong AI tu chu hoan toan san xuat lien tuc phim hoat hinh lich su Toan hoc >10 phut."
    )
    parser.add_argument(
        "--so-tap",
        type=int,
        default=1,
        help="So tap san xuat lien tiep tu hang doi (mac dinh 1).",
    )
    parser.add_argument(
        "--nghi-giay",
        type=float,
        default=30.0,
        help="So giay nghi giua 2 tap lien tiep (mac dinh 30).",
    )
    parser.add_argument(
        "--chu-de",
        default="",
        help="Dat hang rieng 1 chu de cu the (bo trong de AI tu chon tu hang doi va tu san chu de moi).",
    )
    parser.add_argument("--slug", default="", help="Slug tuy chinh khi dung kem --chu-de.")
    parser.add_argument(
        "--chi-tao-kich-ban",
        action="store_true",
        help="Chi chay den buoc nghien cuu web + bien kich 3 tang & tu kiem dinh (bo qua TTS & render).",
    )
    parser.add_argument(
        "--muc-tieu-phut",
        type=float,
        default=11.0,
        help="Thoi luong muc tieu tinh bang phut (mac dinh 11, bao dam > 10 phut).",
    )
    parser.add_argument("--giong-ke", default="di_dom_gan_gui", help="Phong cach ke chuyen.")
    parser.add_argument("--giong", default="", help="Giong Edge TTS (mac dinh vi-VN-NamMinhNeural).")
    parser.add_argument("--toc-do", default=MAC_DINH_RATE, help="Toc do doc TTS (mac dinh +0%%).")
    parser.add_argument("--nhac-nen", default="", help="File MP3 nhac nen (volume=0.08, fade-out 3s).")
    parser.add_argument("--concurrency", type=int, default=0, help="So luong song song cho Remotion.")
    parser.add_argument("--fps", type=int, default=MAC_DINH_FPS, help="So khung hinh/giay (mac dinh 30).")
    parser.add_argument("--bo-cache", action="store_true", help="Bo qua cache o cac buoc duoc chay.")
    parser.add_argument("--bo-nho", default="", help="Duong dan tuy chinh toi bo_nho_hoc_hoi.json.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    ket_qua = chay_san_xuat_lien_tuc(
        so_tap=args.so_tap,
        nghi_giay=args.nghi_giay,
        chu_de=args.chu_de,
        slug=args.slug,
        chi_tao_kich_ban=args.chi_tao_kich_ban,
        muc_tieu_phut=args.muc_tieu_phut,
        giong_ke=args.giong_ke,
        voice=args.giong.strip() or None,
        rate=args.toc_do,
        nhac_nen=Path(args.nhac_nen) if args.nhac_nen else None,
        concurrency=args.concurrency if args.concurrency > 0 else None,
        fps=args.fps,
        bo_cache=args.bo_cache,
        duong_dan_bo_nho=Path(args.bo_nho) if args.bo_nho else None,
    )
    co_thanh_cong = any(r.get("trangThai") == "thanh_cong" for r in ket_qua)
    return 0 if co_thanh_cong else 1


if __name__ == "__main__":
    raise SystemExit(main())
