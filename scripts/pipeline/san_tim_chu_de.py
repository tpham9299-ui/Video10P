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
from scripts.pipeline.chuan_hoa_doc_toan import chuan_hoa_tu_dien_phat_am
from scripts.pipeline.gemini_client import GeminiClient
from scripts.pipeline.tao_kich_ban_10p import (
    DO_TUOI_NHAN_VAT,
    LOAI_BOI_CANH,
    LOAI_DAO_CU,
    LOAI_VAT_THE_XUNG_QUANH,
    TU_THE_NHAN_VAT,
    cat_gon_theo_tu,
    chuan_hoa_enum,
    kiem_tra_latex,
    tao_slug,
)

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


SO_LUONG_NAP_MAC_DINH = 6


def nap_hang_doi_chu_de(
    so_luong: int = SO_LUONG_NAP_MAC_DINH,
    duong_dan_bo_nho: Path | str | None = None,
    client: GeminiClient | None = None,
) -> list[dict[str, Any]]:
    """
    Goi Gemini bat Google Search Grounding (bat_tim_kiem_web=True) de tu san 5-8 chu de lich su Toan hoc
    thu vi (uu tien tinh ke chuyen cao, nhieu giai thoai doi thuc), loai bo chu de trung voi
    chu_de_da_lam & hang_doi_chu_de, luu vao bo_nho_hoc_hoi.json.
    """
    so_can_them = max(1, int(so_luong))
    bo_nho = tai_bo_nho(duong_dan_bo_nho)
    gemini = client or GeminiClient()

    da_co_ds: list[str] = []
    for item in bo_nho.get("chu_de_da_lam") or []:
        da_co_ds.append(f"- [DA LAM] {item.get('tieuDe', '')} ({item.get('slug', '')})")
    for item in bo_nho.get("hang_doi_chu_de") or []:
        da_co_ds.append(f"- [HANG DOI] {item.get('tieuDe', '')} ({item.get('slug', '')})")
    danh_sach_tranh = "\n".join(da_co_ds) if da_co_ds else "(Chua co chu de nao)"

    so_goi_y = so_can_them + 3
    prompt = f"""
Hãy tìm kiếm trên mạng và đề xuất {so_goi_y} chủ đề câu chuyện LỊCH SỬ TOÁN HỌC CÓ THẬT cực kỳ hấp dẫn để làm phim hoạt hình kể chuyện dài >10 phút (phong cách thiên nhiên + hài hước dí dỏm, KHÔNG đánh đấm bạo lực).

TIÊU CHÍ BẮT BUỘC:
1. ƯU TIÊN CHỦ ĐỀ CÓ TÍNH KỂ CHUYỆN CAO & NHIỀU GIAI THOẠI ĐỜI THỰC: có nhân vật cá tính, tình huống đời thường dở khóc dở cười, cuộc đối thoại kịch tính, tranh luận học thuật gay cấn hoặc nghịch lý làm đảo lộn tư duy, dễ dựng bối cảnh hoạt hình sinh động (ví dụ: Évariste Galois và đêm trắng lý thuyết nhóm, Leonhard Euler & 7 cây cầu Königsberg, Srinivasa Ramanujan & con số 1729, Georg Cantor & các cấp độ vô cực, Cardano vs Tartaglia & phương trình bậc 3, Archimedes & chiếc vương miện, Emmy Noether & định lý đối xứng, Carl Friedrich Gauss & giai thoại tổng 1..100, Alan Turing & cỗ máy Enigma, Hypatia, Al-Khwarizmi, Ada Lovelace, John Nash, Maryam Mirzakhani...).
2. Góc khai thác phải gần gũi, hài hước dí dỏm, có tình huống đời thường và liên hệ rõ ràng tới công nghệ / đời sống hiện đại.
3. BẮT BUỘC 100% `tieuDe` và `gocKhaiThac` phải viết bằng TIẾNG VIỆT CÓ DẤU đầy đủ, chuẩn chính tả; TUYỆT ĐỐI CẤM viết tiếng Việt không dấu.
4. TUYỆT ĐỐI KHÔNG trùng lặp với bất kỳ chủ đề nào trong danh sách ĐÃ LÀM hoặc HÀNG ĐỢI dưới đây:
{danh_sach_tranh}

Trả về DUY NHẤT JSON hợp lệ đúng cấu trúc:
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
            "Bạn là biên tập viên lịch sử Toán học kiêm đạo diễn nội dung YouTube giáo dục. "
            "Sử dụng tìm kiếm web để đảm bảo sự kiện lịch sử có thật và trả về DUY NHẤT JSON hợp lệ với 100% tiếng Việt có dấu."
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

    # 1. timeline_su_kien[]: 5-8 moc nam & su kien that cua dung nhan vat/chu de tap nay
    timeline_raw = raw.get("timeline_su_kien") or raw.get("timelineSuKien") or []
    timeline_su_kien: list[dict[str, Any]] = []
    if isinstance(timeline_raw, list):
        for item in timeline_raw[:8]:
            if isinstance(item, dict):
                nam = str(item.get("nam") or "").strip()
                sk = str(item.get("suKien") or item.get("moTa") or "").strip()
                if nam or sk:
                    muc_tl: dict[str, Any] = {
                        "nam": cat_gon_theo_tu(nam, 30) or "...",
                        "suKien": cat_gon_theo_tu(sk, 160) or "...",
                    }
                    if isinstance(item.get("noiBat"), bool):
                        muc_tl["noiBat"] = item["noiBat"]
                    timeline_su_kien.append(muc_tl)
    if not timeline_su_kien and nien_dai:
        for idx, item in enumerate(nien_dai[:8]):
            timeline_su_kien.append(
                {
                    "nam": item["nam"],
                    "suKien": item["suKien"],
                    "noiBat": idx == 0 or idx == len(nien_dai[:8]) - 1,
                }
            )
    if not nien_dai and timeline_su_kien:
        nien_dai = [{"nam": m["nam"], "suKien": m["suKien"]} for m in timeline_su_kien]

    # 2. tu_dien_phat_am{}: anh xa ten rieng, dia danh, thuat ngu nuoc ngoai -> phien am Edge TTS
    tu_dien_phat_am = chuan_hoa_tu_dien_phat_am(
        raw.get("tu_dien_phat_am") or raw.get("tuDienPhatAm") or {}
    )

    # 3. goi_y_boi_canh_va_dao_cu[]: goi y boi canh, do tuoi, tu the, dao cu qua tung giai doan cuoc doi
    goi_y_raw = raw.get("goi_y_boi_canh_va_dao_cu") or raw.get("goiYBoiCanhVaDaoCu") or []
    goi_y_boi_canh_va_dao_cu: list[dict[str, Any]] = []
    if isinstance(goi_y_raw, list):
        for item in goi_y_raw[:10]:
            if not isinstance(item, dict):
                continue
            giai_doan = str(item.get("giaiDoan") or item.get("giai_doan") or "").strip()
            boi_canh = chuan_hoa_enum(item.get("boiCanh") or item.get("boi_canh"), LOAI_BOI_CANH, "")
            if not giai_doan and not boi_canh:
                continue
            do_tuoi = chuan_hoa_enum(item.get("doTuoi") or item.get("do_tuoi"), DO_TUOI_NHAN_VAT, "truong_thanh")
            tu_the = chuan_hoa_enum(item.get("tuThe") or item.get("tu_the"), TU_THE_NHAN_VAT, "dung")
            dao_cu_list: list[str] = []
            for dc in (item.get("daoCu") or item.get("dao_cu") or []):
                dc_clean = chuan_hoa_enum(dc, LOAI_DAO_CU, "")
                if dc_clean and dc_clean not in dao_cu_list:
                    dao_cu_list.append(dc_clean)
            vat_the_list: list[str] = []
            for vt in (item.get("vatTheXungQuanh") or item.get("vat_the_xung_quanh") or []):
                vt_clean = chuan_hoa_enum(vt, LOAI_VAT_THE_XUNG_QUANH, "")
                if vt_clean and vt_clean not in vat_the_list:
                    vat_the_list.append(vt_clean)
            goi_y_boi_canh_va_dao_cu.append(
                {
                    "giaiDoan": cat_gon_theo_tu(giai_doan, 100) or "Giai đoạn chính",
                    "doTuoi": do_tuoi,
                    "tuThe": tu_the,
                    "boiCanh": boi_canh or "thu_vien_co_dien",
                    "daoCu": dao_cu_list,
                    "vatTheXungQuanh": vat_the_list,
                    "ghiChu": cat_gon_theo_tu(str(item.get("ghiChu") or item.get("ghi_chu") or "").strip(), 160),
                }
            )

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
        "timeline_su_kien": timeline_su_kien,
        "tu_dien_phat_am": tu_dien_phat_am,
        "goi_y_boi_canh_va_dao_cu": goi_y_boi_canh_va_dao_cu,
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
Hãy nghiên cứu và kiểm chứng tư liệu lịch sử - Toán học CHÍNH XÁC 100% bằng Google Search cho chủ đề:
- Chủ đề: "{chu_de}"
- Góc khai thác gợi ý: "{goc_khai_thac or 'Kể chuyện lịch sử Toán học thiên nhiên + hài hước dí dỏm, KHÔNG đánh đấm'}"

TƯ LIỆU THAM KHẢO TỪ WIKIPEDIA:
{tom_tat_wiki_txt}

YÊU CẦU BẮT BUỘC:
1. Đối chiếu niên đại chuẩn (năm sinh/mất, mốc sự kiện chính xác, KHÔNG bịa đặt).
2. Xuất `timeline_su_kien` gồm 5 đến 8 mốc năm & sự kiện lịch sử THẬT của ĐÚNG nhân vật/chủ đề tập này (theo thứ tự thời gian, có `noiBat: true` cho 1-2 mốc bước ngoặt; mỗi `suKien` ngắn gọn 10-18 từ, trọn vẹn ý).
3. Xuất `tu_dien_phat_am`: ánh xạ tất cả tên riêng, địa danh, trường đại học, thuật ngữ Toán nước ngoài sang cách đọc phiên âm tiếng Việt tự nhiên cho Edge TTS (ví dụ: `"Ramanujan": "Ra-ma-nu-gian"`, `"Hardy": "Ha-đi"`, `"Madras": "Ma-đơ-rát"`, `"Littlewood": "Lít-tơ-út"`, `"Cambridge": "Kem-brít"`, `"Namagiri": "Na-ma-ghi-ri"`, `"mock theta": "móc thê-ta"`).
4. Xuất `goi_y_boi_canh_va_dao_cu` gồm 4 đến 7 giai đoạn cuộc đời / tình tiết chính, chỉ rõ `doTuoi`, `tuThe`, `boiCanh`, `daoCu[]`, `vatTheXungQuanh[]` KHỚP 1-1 với câu chuyện. Lưu ý: KHÔNG chọn `nha_co_phong_sinh` cho cảnh người già/nhận giải thưởng/cuối đời; KHÔNG đặt `la_vang_gio` trong phòng kín; KHÔNG đặt `ngon_nen_den_dau` trong `khong_gian_vu_tru_toan`. Chỉ được dùng các enum hợp lệ sau:
   - boiCanh: {", ".join(LOAI_BOI_CANH)}
   - doTuoi: {", ".join(DO_TUOI_NHAN_VAT)}
   - tuThe: {", ".join(TU_THE_NHAN_VAT)}
   - daoCu: {", ".join(LOAI_DAO_CU)}
   - vatTheXungQuanh: {", ".join(LOAI_VAT_THE_XUNG_QUANH)}
5. Liệt kê nhân vật lịch sử có thật và nét tính cách đời thường thú vị của họ.
6. Chọn 3 đến 4 GIAI THOẠI ĐỜI THƯỜNG / DÍ DỎM CÓ THẬT (hoặc giai thoại được ghi nhận rõ ràng là giai thoại truyền miệng, ghi chú minh bạch).
7. Trình bày 2 đến 3 KIẾN THỨC / CHỨNG MINH TOÁN CỐT LÕI kèm công thức LaTeX chuẩn KaTeX (thoát \\ thành \\\\ trong JSON, không bọc dấu $).
8. Nêu 2 đến 4 ứng dụng thực tế trong thế giới hiện đại và liệt kê URL nguồn tham khảo uy tín đã đối chiếu.
9. BẮT BUỘC 100% mọi chuỗi tiếng Việt trong JSON phải viết CÓ DẤU ĐẦY ĐỦ, đúng chính tả; TUYỆT ĐỐI CẤM viết tiếng Việt không dấu.

Trả về DUY NHẤT JSON hợp lệ đúng cấu trúc:
{{
  "tieuDe": "Tiêu đề tiếng Việt hấp dẫn cho tập phim",
  "tomTat1Cau": "Tóm tắt trọn vẹn câu chuyện trong 1 câu ngắn gọn.",
  "nienDaiChuan": [
    {{"nam": "1736", "suKien": "Leonhard Euler công bố bài báo giải bài toán 7 cây cầu Königsberg."}}
  ],
  "timeline_su_kien": [
    {{"nam": "1887", "suKien": "Srinivasa Ramanujan chào đời tại Erode, Ấn Độ.", "noiBat": false}},
    {{"nam": "1913", "suKien": "Gửi bức thư 9 trang chứa hơn 100 công thức tới giáo sư G. H. Hardy ở Cambridge.", "noiBat": true}}
  ],
  "tu_dien_phat_am": {{
    "Ramanujan": "Ra-ma-nu-gian",
    "Hardy": "Ha-đi",
    "Madras": "Ma-đơ-rát",
    "Littlewood": "Lít-tơ-út",
    "Cambridge": "Kem-brít",
    "Namagiri": "Na-ma-ghi-ri",
    "mock theta": "móc thê-ta"
  }},
  "goi_y_boi_canh_va_dao_cu": [
    {{
      "giaiDoan": "Chào đời và tuổi thơ ở Ấn Độ",
      "doTuoi": "so_sinh",
      "tuThe": "om_em_be",
      "boiCanh": "nha_co_phong_sinh",
      "daoCu": ["noi_em_be", "ban_hoc_den_dau"],
      "vatTheXungQuanh": ["ngon_nen_den_dau"],
      "ghiChu": "Cảnh mở đầu tuổi thơ với nôi em bé và ánh đèn ấm."
    }}
  ],
  "nhanVatThat": [
    {{
      "ten": "Leonhard Euler",
      "vaiTro": "Nhà Toán học Thụy Sĩ kiệt xuất",
      "nienDai": "1707-1783",
      "tinhCachDoiThuong": "Làm việc siêu nhanh ngay cả khi con cái chơi đùa quanh bàn."
    }}
  ],
  "giaiThoaiDoiThuong": [
    {{
      "tieuDe": "Trò đố đi dạo cuối tuần",
      "noiDung": "Người dân Königsberg thường cá cược xem ai đi qua cả 7 cây cầu đúng 1 lần...",
      "diemHaiHuoc": "Cả thành phố đi mòn giày mà vẫn không qua được cây cầu cuối."
    }}
  ],
  "kienThucToanCotLoi": [
    {{
      "tenKienThuc": "Điều kiện tồn tại đường đi Euler",
      "giaiThichDeHieu": "Mỗi vùng đất là 1 nút, mỗi cây cầu là 1 cạnh nối...",
      "congThucLatex": "\\\\sum_{{v \\\\in V}} \\\\deg(v) = 2|E|",
      "yNghia": "Đặt nền móng cho Lý thuyết Đồ thị."
    }}
  ],
  "ungDungHienDai": [
    "Thuật toán dẫn đường GPS và Google Maps",
    "Tối ưu hóa mạng viễn thông và giao hàng"
  ],
  "nguonThamKhao": [
    "https://en.wikipedia.org/wiki/Seven_Bridges_of_K%C3%B6nigsberg"
  ]
}}
""".strip()

    ket_qua_raw = gemini.tao_json(
        prompt=prompt,
        system_instruction=(
            "Bạn là nhà nghiên cứu lịch sử Toán học kỹ tính. "
            "Kiểm chứng sự kiện qua Google Search và trả về DUY NHẤT JSON hợp lệ với 100% tiếng Việt có dấu đầy đủ."
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
        f"({len(tu_lieu['timeline_su_kien'])} moc timeline, {len(tu_lieu['tu_dien_phat_am'])} tu phat am, "
        f"{len(tu_lieu['goi_y_boi_canh_va_dao_cu'])} goi y boi canh, {len(tu_lieu['giaiThoaiDoiThuong'])} giai thoai, "
        f"{len(tu_lieu['kienThucToanCotLoi'])} kien thuc Toan, {len(tu_lieu['nguonThamKhao'])} nguon)."
    )
    return file_tu_lieu, tu_lieu


def tao_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bo tu san chu de lich su Toan hoc & nghien cuu tu lieu web (Gemini Grounding + Wikipedia)."
    )
    parser.add_argument(
        "--nap-hang-doi",
        nargs="?",
        const=SO_LUONG_NAP_MAC_DINH,
        type=int,
        default=0,
        help="Tu san them N chu de moi tren mang (mac dinh 6 khi truyen khong kem so) va luu vao hang_doi_chu_de.",
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
