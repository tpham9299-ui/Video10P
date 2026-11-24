# -*- coding: utf-8 -*-
"""Bo tu san chu de lich su Toan hoc & nghien cuu tu lieu da nguon (Gemini Google Search + Wikipedia REST API)."""

from __future__ import annotations

import argparse
import datetime
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

GOC_DU_AN = Path(__file__).resolve().parents[2]
if str(GOC_DU_AN) not in sys.path:
    sys.path.insert(0, str(GOC_DU_AN))

from scripts.pipeline.bo_nho_hoc_hoi import (
    DUONG_DAN_BO_NHO_MAC_DINH,
    luu_bo_nho,
    tai_bo_nho,
    them_chu_de_hang_doi,
)
from scripts.pipeline.gemini_client import GeminiClient
from scripts.pipeline.tao_kich_ban_10p import kiem_tra_latex, tao_slug

WIKI_SUMMARY_TEMPLATE = "https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
WIKI_OPENSEARCH_TEMPLATE = (
    "https://{lang}.wikipedia.org/w/api.php?action=opensearch&limit=3&namespace=0&format=json&search={query}"
)
WIKI_USER_AGENT = "Video10P-MathHistoryBot/0.5 (Educational Animated Math Storytelling)"


def _goi_http_get_wiki_mac_dinh(url: str, timeout_giay: int = 12) -> tuple[int, str]:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": WIKI_USER_AGENT,
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_giay) as resp:
            return resp.getcode(), resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as err:
        return err.code, ""
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, ""


def tra_cuu_tom_tat_wikipedia(
    tu_khoa: str,
    ngon_ngu: tuple[str, ...] = ("vi", "en"),
    wiki_fetcher: Callable[[str, int], tuple[int, str]] | None = None,
    timeout_giay: int = 12,
) -> list[dict[str, str]]:
    """
    Tra cuu tom tat nhanh tu Wikipedia REST API (uu tien vi -> en).
    Neu ten trang truc tiep khong khop (404), thu tim tieu de bang OpenSearch API.
    """
    fetcher = wiki_fetcher or _goi_http_get_wiki_mac_dinh
    tu_khoa_sach = (tu_khoa or "").strip()
    if not tu_khoa_sach:
        return []

    ket_qua: list[dict[str, str]] = []
    da_co_url: set[str] = set()

    for lang in ngon_ngu:
        tieu_de_ung_vien = [tu_khoa_sach]
        # Thu goi summary truc tiep truoc
        tim_thay_lang = False
        for tieu_de in tieu_de_ung_vien:
            encoded = urllib.parse.quote(tieu_de.replace(" ", "_"), safe="")
            url = WIKI_SUMMARY_TEMPLATE.format(lang=lang, title=encoded)
            status, body = fetcher(url, timeout_giay)
            if status == 200 and body:
                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                    data = {}
                extract = str(data.get("extract") or "").strip()
                page_url = (
                    str((data.get("content_urls") or {}).get("desktop", {}).get("page") or "").strip()
                    or f"https://{lang}.wikipedia.org/wiki/{encoded}"
                )
                if extract and page_url not in da_co_url:
                    da_co_url.add(page_url)
                    ket_qua.append(
                        {
                            "ngonNgu": lang,
                            "tieuDe": str(data.get("title") or tieu_de).strip(),
                            "tomTat": extract[:1400],
                            "url": page_url,
                        }
                    )
                    tim_thay_lang = True
                    break

        if tim_thay_lang:
            continue

        # Fallback: OpenSearch de tim ten bai gan dung tren Wikipedia
        q = urllib.parse.quote(tu_khoa_sach)
        search_url = WIKI_OPENSEARCH_TEMPLATE.format(lang=lang, query=q)
        st_s, body_s = fetcher(search_url, timeout_giay)
        if st_s == 200 and body_s:
            try:
                parsed = json.loads(body_s)
                titles = parsed[1] if isinstance(parsed, list) and len(parsed) >= 2 and isinstance(parsed[1], list) else []
            except (json.JSONDecodeError, IndexError):
                titles = []
            for t in titles[:2]:
                if not isinstance(t, str) or not t.strip():
                    continue
                encoded = urllib.parse.quote(t.strip().replace(" ", "_"), safe="")
                url = WIKI_SUMMARY_TEMPLATE.format(lang=lang, title=encoded)
                status, body = fetcher(url, timeout_giay)
                if status == 200 and body:
                    try:
                        data = json.loads(body)
                    except json.JSONDecodeError:
                        data = {}
                    extract = str(data.get("extract") or "").strip()
                    page_url = (
                        str((data.get("content_urls") or {}).get("desktop", {}).get("page") or "").strip()
                        or f"https://{lang}.wikipedia.org/wiki/{encoded}"
                    )
                    if extract and page_url not in da_co_url:
                        da_co_url.add(page_url)
                        ket_qua.append(
                            {
                                "ngonNgu": lang,
                                "tieuDe": str(data.get("title") or t).strip(),
                                "tomTat": extract[:1400],
                                "url": page_url,
                            }
                        )
                        break

    return ket_qua


def nap_hang_doi_chu_de(
    so_luong: int = 5,
    duong_dan_bo_nho: Path | str | None = None,
    client: GeminiClient | None = None,
) -> list[dict[str, Any]]:
    """
    Goi Gemini bat Google Search Grounding (bat_tim_kiem_web=True) de tu san chu de lich su Toan hoc
    thu vi, loai bo chu de trung voi chu_de_da_lam & hang_doi_chu_de, luu vao bo_nho_hoc_hoi.json.
    """
    so_can_them = max(1, int(so_luong))
    bo_nho = tai_bo_nho(duong_dan_bo_nho)
    gemini = client or GeminiClient()

    da_co_ds: list[str] = []
    for item in bo_nho.get("chu_de_da_lam") or []:
        da_co_ds.append(f"- {item.get('tieuDe', '')} ({item.get('slug', '')})")
    for item in bo_nho.get("hang_doi_chu_de") or []:
        da_co_ds.append(f"- {item.get('tieuDe', '')} ({item.get('slug', '')})")
    danh_sach_tranh = "\n".join(da_co_ds) if da_co_ds else "(Chua co chu de nao)"

    so_goi_y = so_can_them + 3
    prompt = f"""
Hay tim kiem tren mang va de xuat {so_goi_y} chu de cau chuyen LICH SU TOAN HOC CO THAT cuc ky hap dan de lam phim hoat hinh ke chuyen dai >10 phut (phong cach thien nhien + hai huoc di dom, KHONG danh dam bao luc).

TIEU CHI BAT BUOC:
1. Cau chuyen phai co THAT trong lich su Toan hoc: giai thoai thu vi, tranh luan hoc thuat gay can, nghich ly lam dao lon tu duy hoac nguon goc bat ngo cua khai niem Toan (vi du: Evariste Galois va ly thuyet nhom, Leonhard Euler & bai toan 7 cay cau Konigsberg, Srinivasa Ramanujan & cuon so tay bi an, Georg Cantor & cac cap do vo cuc, hanh trinh so 0 va so ao i, Archimedes & chiec vuong mien/phep tinh dien tich, Emmy Noether & dinh ly doi xung, Cardano vs Tartaglia va phuong trinh bac 3, Hypatia, Al-Khwarizmi, Ada Lovelace...).
2. Goc khai thac phai gan gui, hai huoc di dom, co tinh huong doi thuong va lien he ro rang toi cong nghe / doi song hien dai.
3. TUYET DOI KHONG trung lap voi danh sach chu de da lam hoac da co trong hang doi duoi day:
{danh_sach_tranh}

Tra ve DUY NHAT JSON hop le dung cau truc:
{{
  "chuDeDeXuat": [
    {{
      "slug": "euler_bay_cay_cau_konigsberg",
      "tieuDe": "Leonhard Euler và Bài Toán 7 Cây Cầu Làm Cả Thành Phố Bó Tay",
      "gocKhaiThac": "Từ một trò đố vui đi dạo cuối tuần năm 1736 đến sự ra đời của Lý thuyết Đồ thị và Google Maps hôm nay.",
      "diemThuHut": 9.3,
      "doSauToanHoc": 8.9
    }}
  ]
}}
""".strip()

    phan_hoi = gemini.tao_json(
        prompt=prompt,
        system_instruction=(
            "Ban la bien tap vien lich su Toan hoc kiem dao dien noi dung YouTube giao duc. "
            "Su dung tim kiem web de dam bao su kien lich su co that va tra ve DUY NHAT JSON hop le."
        ),
        nhiet_do=0.75,
        max_output_tokens=4096,
        bat_tim_kiem_web=True,
    )

    if isinstance(phan_hoi, dict):
        raw_items = phan_hoi.get("chuDeDeXuat") or phan_hoi.get("chu_de") or phan_hoi.get("topics") or []
    elif isinstance(phan_hoi, list):
        raw_items = phan_hoi
    else:
        raw_items = []

    da_them = them_chu_de_hang_doi(bo_nho, raw_items, gioi_han_them=so_can_them)
    luu_bo_nho(bo_nho, duong_dan_bo_nho)
    print(f"[San chu de] Da nap them {len(da_them)}/{so_can_them} chu de moi vao hang doi.")
    for item in da_them:
        print(
            f"  + [{item['slug']}] {item['tieuDe']} "
            f"(thu hut {item['diemThuHut']}, do sau {item['doSauToanHoc']})"
        )
    return da_them


def _chuan_hoa_tu_lieu_nghien_cuu(
    raw: dict[str, Any],
    slug: str,
    chu_de: str,
    wiki_list: list[dict[str, str]],
    nguon_grounding: list[dict[str, str]],
) -> dict[str, Any]:
    """Lam sach tu_lieu_nghien_cuu.json, kiem tra LaTeX va hop nhat URL nguon tham khao."""
    nien_dai: list[dict[str, str]] = []
    for item in raw.get("nienDaiChuan") or []:
        if isinstance(item, dict):
            nam = str(item.get("nam") or "").strip()
            sk = str(item.get("suKien") or "").strip()
            if nam or sk:
                nien_dai.append({"nam": nam or "...", "suKien": sk})

    nhan_vat: list[dict[str, str]] = []
    for item in raw.get("nhanVatThat") or []:
        if isinstance(item, dict):
            ten = str(item.get("ten") or "").strip()
            if ten:
                nhan_vat.append(
                    {
                        "ten": ten,
                        "vaiTro": str(item.get("vaiTro") or "").strip(),
                        "nienDai": str(item.get("nienDai") or "").strip(),
                        "tinhCachDoiThuong": str(item.get("tinhCachDoiThuong") or "").strip(),
                    }
                )

    giai_thoai: list[dict[str, str]] = []
    for item in raw.get("giaiThoaiDoiThuong") or []:
        if isinstance(item, dict):
            nd = str(item.get("noiDung") or "").strip()
            if nd:
                giai_thoai.append(
                    {
                        "tieuDe": str(item.get("tieuDe") or "Giai thoại thú vị").strip(),
                        "noiDung": nd,
                        "diemHaiHuoc": str(item.get("diemHaiHuoc") or "").strip(),
                    }
                )

    kien_thuc_toan: list[dict[str, str]] = []
    for item in raw.get("kienThucToanCotLoi") or []:
        if isinstance(item, dict):
            ten = str(item.get("tenKienThuc") or "").strip()
            if not ten:
                continue
            latex_raw = str(item.get("congThucLatex") or "").strip()
            latex_clean, _ = kiem_tra_latex(latex_raw) if latex_raw else ("", [])
            kien_thuc_toan.append(
                {
                    "tenKienThuc": ten,
                    "giaiThichDeHieu": str(item.get("giaiThichDeHieu") or "").strip(),
                    "congThucLatex": latex_clean,
                    "yNghia": str(item.get("yNghia") or "").strip(),
                }
            )

    ung_dung = [
        str(x).strip()
        for x in (raw.get("ungDungHienDai") or [])
        if str(x).strip()
    ]

    nguon_url: list[str] = []
    da_co: set[str] = set()

    def _them_url(val: Any) -> None:
        if isinstance(val, dict):
            u = str(val.get("url") or val.get("uri") or "").strip()
        else:
            u = str(val or "").strip()
        if u and u not in da_co:
            da_co.add(u)
            nguon_url.append(u)

    for g in nguon_grounding:
        _them_url(g)
    for w in wiki_list:
        _them_url(w.get("url"))
    for u in raw.get("nguonThamKhao") or []:
        _them_url(u)

    return {
        "slug": slug,
        "tieuDe": str(raw.get("tieuDe") or chu_de).strip(),
        "chuDe": chu_de,
        "ngayNghienCuu": datetime.date.today().isoformat(),
        "tomTat1Cau": str(raw.get("tomTat1Cau") or "").strip(),
        "nienDaiChuan": nien_dai,
        "nhanVatThat": nhan_vat,
        "giaiThoaiDoiThuong": giai_thoai,
        "kienThucToanCotLoi": kien_thuc_toan,
        "ungDungHienDai": ung_dung,
        "tomTatWikipedia": wiki_list,
        "nguonThamKhao": nguon_url,
    }


def nghien_cuu_chu_de(
    slug: str = "",
    chu_de: str = "",
    goc_khai_thac: str = "",
    thu_muc_du_lieu: Path | None = None,
    duong_dan_bo_nho: Path | str | None = None,
    client: GeminiClient | None = None,
    wiki_fetcher: Callable[[str, int], tuple[int, str]] | None = None,
    bo_cache: bool = False,
) -> tuple[Path, dict[str, Any]]:
    """
    Nghien cuu tu lieu xac thuc tu Wikipedia REST API + Gemini Google Search Grounding,
    luu ra du_lieu/<slug>/tu_lieu_nghien_cuu.json.
    """
    bo_nho = tai_bo_nho(duong_dan_bo_nho)
    muc_hang_doi: dict[str, Any] | None = None

    if slug and not chu_de:
        slug_chuan = tao_slug(slug)
        for item in bo_nho.get("hang_doi_chu_de") or []:
            if tao_slug(str(item.get("slug") or "")) == slug_chuan:
                muc_hang_doi = item
                break
        if muc_hang_doi:
            chu_de = str(muc_hang_doi.get("tieuDe") or slug).strip()
            goc_khai_thac = goc_khai_thac or str(muc_hang_doi.get("gocKhaiThac") or "").strip()
        else:
            chu_de = slug.replace("_", " ").strip()

    if not chu_de.strip():
        raise ValueError("Can truyen --slug (co trong hang doi) hoac --chu-de de nghien cuu.")

    slug_cuoi = tao_slug(slug or chu_de)
    base_dir = (thu_muc_du_lieu or (GOC_DU_AN / "du_lieu")) / slug_cuoi
    base_dir.mkdir(parents=True, exist_ok=True)
    file_tu_lieu = base_dir / "tu_lieu_nghien_cuu.json"

    if file_tu_lieu.exists() and not bo_cache:
        print(f"[Nghien cuu] Tai cache tu lieu: {file_tu_lieu}")
        return file_tu_lieu, json.loads(file_tu_lieu.read_text(encoding="utf-8"))

    print(f"[Nghien cuu] Dang tra cuu Wikipedia & Gemini Web Search cho: {chu_de} ({slug_cuoi})...")
    wiki_list = tra_cuu_tom_tat_wikipedia(chu_de, wiki_fetcher=wiki_fetcher)
    tom_tat_wiki_txt = (
        "\n".join(
            f"- [{w['ngonNgu'].upper()}] {w['tieuDe']} ({w['url']}): {w['tomTat']}"
            for w in wiki_list
        )
        if wiki_list
        else "(Chua lay duoc tom tat Wikipedia truc tiep, hay dung Google Search de kiem chung ky.)"
    )

    gemini = client or GeminiClient()
    prompt = f"""
Hay nghien cuu va kiem chung tu lieu lich su - Toan hoc CHINH XAC 100% bang Google Search cho chu de:
- Chu de: "{chu_de}"
- Goc khai thac goi y: "{goc_khai_thac or 'Ke chuyen lich su Toan hoc thien nhien + hai huoc di dom, KHONG danh dam'}"

TU LIEU THAM KHAO TU WIKIPEDIA:
{tom_tat_wiki_txt}

YEU CAU BAT BUOC:
1. Doi chieu nien dai chuan (nam sinh/mat, moc su kien chinh xac, KHONG bia dat).
2. Liet ke nhan vat lich su co that va net tinh cach doi thuong thu vi cua ho.
3. Chon 3 den 4 GIAI THOAI DOI THUONG / DI DOM CO THAT (hoac giai thoai duoc ghi nhan ro rang la giai thoai truyen mieng, ghi chu minh bach).
4. Trinh bay 2 den 3 KIEN THUC / CHUNG MINH TOAN COT LOI kem cong thuc LaTeX chuan KaTeX (thoat \\ thanh \\\\ trong JSON, khong boc dau $).
5. Neu 2 den 4 ung dung thuc te trong the gioi hien dai.
6. Liet ke URL nguon tham khao uy tin da doi chieu.

Tra ve DUY NHAT JSON hop le dung cau truc:
{{
  "tieuDe": "Tieu de tieng Viet hap dan cho tap phim",
  "tomTat1Cau": "Tom tat tron ven cau chuyen trong 1 cau ngan gon.",
  "nienDaiChuan": [
    {{"nam": "1736", "suKien": "Leonhard Euler cong bo bai bao giai bai toan 7 cay cau Konigsberg."}}
  ],
  "nhanVatThat": [
    {{
      "ten": "Leonhard Euler",
      "vaiTro": "Nha Toan hoc Thuy Si kiet xuat",
      "nienDai": "1707-1783",
      "tinhCachDoiThuong": "Lam viec sieu nhanh ngay ca khi con cai choi dua quanh ban."
    }}
  ],
  "giaiThoaiDoiThuong": [
    {{
      "tieuDe": "Tro do di dao cuoi tuan",
      "noiDung": "Nguoi dan Konigsberg thuong ca cuoc xem ai di qua ca 7 cay cau dung 1 lan...",
      "diemHaiHuoc": "Ca thanh pho di mon giay ma van khong qua duoc cau cuoi."
    }}
  ],
  "kienThucToanCotLoi": [
    {{
      "tenKienThuc": "Dieu kien ton tai duong di Euler",
      "giaiThichDeHieu": "Moi vung dat la 1 nut, moi cay cau la 1 canh noi...",
      "congThucLatex": "\\\\sum_{{v \\\\in V}} \\\\deg(v) = 2|E|",
      "yNghia": "Dat nen mong cho Ly thuyet Do thi."
    }}
  ],
  "ungDungHienDai": [
    "Thuat toan dan duong GPS va Google Maps",
    "Toi uu hoa mang vien thong va giao hang"
  ],
  "nguonThamKhao": [
    "https://en.wikipedia.org/wiki/Seven_Bridges_of_K%C3%B6nigsberg"
  ]
}}
""".strip()

    ket_qua_raw = gemini.tao_json(
        prompt=prompt,
        system_instruction=(
            "Ban la nha nghien cuu lich su Toan hoc ky tinh. "
            "Kiem chung su kien qua Google Search va tra ve DUY NHAT JSON hop le."
        ),
        nhiet_do=0.35,
        max_output_tokens=6144,
        bat_tim_kiem_web=True,
        tra_ve_nguon=True,
    )
    if isinstance(ket_qua_raw, tuple):
        raw_dict, nguon_grounding = ket_qua_raw
    else:
        raw_dict, nguon_grounding = ket_qua_raw, list(getattr(gemini, "nguon_tham_khao_gan_nhat", []))

    if not isinstance(raw_dict, dict):
        raw_dict = {}

    tu_lieu = _chuan_hoa_tu_lieu_nghien_cuu(
        raw=raw_dict,
        slug=slug_cuoi,
        chu_de=chu_de,
        wiki_list=wiki_list,
        nguon_grounding=nguon_grounding,
    )
    file_tu_lieu.write_text(
        json.dumps(tu_lieu, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        f"[Nghien cuu] Da xuat {file_tu_lieu} "
        f"({len(tu_lieu['nienDaiChuan'])} moc nien dai, {len(tu_lieu['giaiThoaiDoiThuong'])} giai thoai, "
        f"{len(tu_lieu['kienThucToanCotLoi'])} kien thuc Toan, {len(tu_lieu['nguonThamKhao'])} nguon)."
    )
    return file_tu_lieu, tu_lieu


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bo tu san chu de lich su Toan hoc & nghien cuu tu lieu web (Gemini Grounding + Wikipedia)."
    )
    parser.add_argument(
        "--nap-hang-doi",
        type=int,
        default=0,
        help="Tu san them N chu de moi tren mang va luu vao hang_doi_chu_de.",
    )
    parser.add_argument(
        "--nghien-cuu",
        default="",
        help="Slug cua chu de can nghien cuu tu lieu (xuat du_lieu/<slug>/tu_lieu_nghien_cuu.json).",
    )
    parser.add_argument("--chu-de", default="", help="Ten chu de tuy chinh de nghien cuu.")
    parser.add_argument("--slug", default="", help="Slug tuy chinh khi dung kem --chu-de.")
    parser.add_argument("--bo-cache", action="store_true", help="Nghien cuu lai ke ca khi da co file tu lieu.")
    parser.add_argument(
        "--bo-nho",
        default="",
        help="Duong dan tuy chinh toi bo_nho_hoc_hoi.json.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = tao_parser().parse_args(argv)
    duong_dan_bo_nho = Path(args.bo_nho) if args.bo_nho else DUONG_DAN_BO_NHO_MAC_DINH

    if args.nap_hang_doi > 0:
        nap_hang_doi_chu_de(so_luong=args.nap_hang_doi, duong_dan_bo_nho=duong_dan_bo_nho)
        if not args.nghien_cuu and not args.chu_de:
            return 0

    if args.nghien_cuu or args.chu_de:
        slug_dung = args.nghien_cuu.strip() or args.slug.strip()
        nghien_cuu_chu_de(
            slug=slug_dung,
            chu_de=args.chu_de.strip(),
            duong_dan_bo_nho=duong_dan_bo_nho,
            bo_cache=args.bo_cache,
        )
        return 0

    print("[LOI] Can truyen --nap-hang-doi N hoac --nghien-cuu <slug> (hoac --chu-de \"...\").")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
