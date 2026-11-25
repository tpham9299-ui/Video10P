# Dự án Phim Hoạt Hình 2D Kể Chuyện Toán Học (`v2.0`)

Remotion `16:9` (`1920×1080`, `30fps` + `<Still>` Thumbnail `1280×720`), TypeScript strict + **Hệ thống AI tự chủ khép kín hoàn toàn hằng ngày (Python + GitHub Actions)** sản xuất phim hoạt hình kể chuyện lịch sử Toán học dài **> 10 phút (> 600 giây)** — phong cách thiên nhiên + hài hước dí dỏm (KHÔNG đánh đấm), với **8 góc quay đạo diễn** + tự động focus người nói, **4 độ tuổi × 5 tư thế × 20 động tác FK**, **22 bối cảnh 3 lớp Parallax** bọc `React.memo`, **10 sinh vật/đồ vật môi trường sống động tất định**, **20 đạo cụ kể chuyện**, cảnh **tương tác khán giả đếm ngược 3 giây**, **hội thoại đa giọng `luotThoai[]` + từ điển phát âm Edge TTS + RMS 30fps từng lượt**, **biên kịch 2 vai + Guardrail Python tự sửa cục bộ**, **chia chunk >120s song song chống OOM/timeout trên GitHub Actions** và **tự săn chủ đề chạy hằng ngày 07:00 giờ Việt Nam**.

## Sơ đồ thư mục
```text
├── .env.example                           # Mẫu cấu hình GEMINI_API_KEYS, fallback model, đa giọng TTS & YOUTUBE_API_KEY tùy chọn
├── .gitignore                             # Loại trừ tuyệt đối .env, node_modules/, out/, *.mp4, public/audio/, __pycache__/ & cache nặng
├── .github/workflows/tu-dong-video10p.yml # GitHub Actions 3 job nối tiếp (07:00 VN hằng ngày + workflow_dispatch): chuan-bi -> render-song-song (chunk matrix) -> ghep-va-luu
├── HUONG_DAN_TU_DONG.md                   # Hướng dẫn vận hành v2.0 cục bộ, GitHub Actions hằng ngày & tham số workflow_dispatch
├── requirements.txt                       # Thư viện Python gọn nhẹ: edge-tts, Pillow (không cài SDK nặng)
├── du_lieu/
│   ├── bo_nho_hoc_hoi.json                # Bộ nhớ tự học bền vững (chu_de_da_lam, hang_doi_chu_de, <=25 bài học ưu tiên, phan_hoi_kenh)
│   ├── mau_pythagoras.json                # Kịch bản mẫu tương thích ngược 750 frames (25s), đủ 7 bố cục + SFX + bảng giảng Toán
│   ├── mau_v2_tuong_tac.json              # Kịch bản mẫu v2.0 (900 frames, 30s): 8 bối cảnh, đa độ tuổi/tư thế, luotThoai[] đa giọng, đếm ngược 3s, bảng Toán tham số hóa
│   └── <slug>/                            # Dữ liệu từng tập (tu_lieu_nghien_cuu.json, nhap_kich_ban.json, doc_duyet_kich_ban.md, du_lieu_render.json)
├── public/
│   ├── audio/<slug>/                      # Audio TTS theo từng <slug>/ (bị loại trừ bởi .gitignore)
│   ├── sfx/                               # 6 SFX hoạt hình (pop, ding, boing, crickets, whoosh, dramatic)
│   └── bgm/nhac_nen_nhe.mp3               # Nhạc nền acoustic/marimba nhẹ 48s loop mượt
├── scripts/
│   ├── test_khung.mjs                     # Kiểm định TS/Remotion v2.0: 22 bối cảnh, 20 đạo cụ, 10 sinh vật, 8 góc quay, 20 động tác FK, Guard sạch Pythagoras & luật cấm
│   ├── test_pipeline.py                   # 49+ unit test offline toàn chuỗi Python v2.0 (săn chủ đề hằng ngày, Guardrail, từ điển phát âm, luotThoai RMS, chia chunk >120s, CI YAML)
│   └── pipeline/
│       ├── tao_am_thanh_mau.py            # Tổng hợp offline 6 SFX & nhạc nền 48s bằng stdlib + ffmpeg
│       ├── gemini_client.py               # Gemini REST text & Vision, xoay vòng key, fallback model & Google Search Grounding
│       ├── bo_nho_hoc_hoi.py              # Bộ nhớ tự học, chống trùng, xóa khỏi hàng đợi sau khi xong, nạp số liệu YouTube (CLI/CSV/JSON)
│       ├── dong_bo_youtube.py             # Cầu nối tùy chọn kéo thống kê YouTube Data API v3 bằng stdlib
│       ├── san_tim_chu_de.py              # Tự săn 6 chủ đề giàu giai thoại (--nap-hang-doi) & nghiên cứu xuất timeline_su_kien, tu_dien_phat_am, goi_y_boi_canh_va_dao_cu
│       ├── tao_kich_ban_10p.py            # AI biên kịch 2 vai (Biên kịch kể chuyện + Đạo diễn Storyboard), chống lặp ý & Guardrail tự sửa cục bộ
│       ├── chuan_hoa_doc_toan.py          # Chuẩn hóa ký hiệu Toán + từ điển phát âm mặc định & từ tư liệu (chỉ cho Edge TTS, giữ nguyên chữ gốc cho phụ đề)
│       ├── chuanbi_dai.py                 # Edge TTS phân vai & phân giọng từng nhân vật cho luotThoai[], RMS 30fps từng lượt, batDauFrame/ketThucFrame & xuất .srt
│       ├── render_dai.py                  # Chia chunk thông minh >120s (--chi-render-chunk / --chi-render-hoi), tự tối ưu CI=true, ghép FFmpeg -14 LUFS, keyframe Visual QA & Thumbnail A/B
│       ├── chay_tu_dong.py                # Lệnh chạy 1 chạm từ 1 câu chủ đề
│       └── san_xuat_lien_tuc.py           # Điều phối tự chủ hằng ngày (tự nạp hàng đợi <3 -> chọn #1 -> --chi-chuan-bi xuất danhSachChunk -> --hoan-tat-tu-meta)
└── src/
    ├── index.ts, Root.tsx                 # Composition VideoDaiNguoiQue (calculateMetadata) & Still ThumbnailToanHoc (1280×720)
    ├── Thumbnail.tsx                      # 3 biến thể Thumbnail A/B tương phản cao (không blur)
    ├── kieu_dai.ts                        # Hợp đồng dữ liệu v2.0 (22 bối cảnh, 20 đạo cụ, 10 sinh vật, 8 góc quay, 4 độ tuổi, 5 tư thế, 20 động tác, luotThoai, cauHoiTuongTac)
    ├── VideoDai.tsx                       # Điều phối Sequence liền mạch 0 gap frame, khóa outro chỉ ở cảnh cuối hồi cuối, SFX an toàn & phụ đề
    ├── boicanh/                           # BoiCanhHoatHinh.tsx, BoiCanhMoi.tsx (22 bối cảnh React.memo), SinhVatVaMoiTruong.tsx & moi_truong_logic.ts
    ├── canh/                              # 9 bố cục cảnh (gồm CanhTuongTacKhanGia 3s & CanhChiaDoiManHinh) + dieu_phoi_canh.ts + KhungLoiBinhHaiHuoc
    ├── daocu/                             # CongThucMath.tsx (KaTeX), DaoCu.tsx (20 đạo cụ), MinhHoaToan.tsx & minh_hoa_hop_le.ts (100% JSON, không hardcode)
    ├── amthanh/sfx.ts                     # Bản đồ 6 SFX hoạt hình an toàn
    ├── xuong/                             # duong_cong.ts, dong_tac.ts (20 chuỗi diễn xuất), he_xuong.ts (FK mềm + khóa góc cổ/đầu an toàn)
    ├── vfx/                               # tat_dinh.ts, MayQuayDong.tsx (8 góc quay + tuDongFocusNguoiNoi), HieuUngHoatHinh.tsx (8 VFX)
    └── nhanvat/                           # lip_sync.ts (RMS 4 khẩu hình), ten_nhan_vat.ts (hộp tên tự co giãn), NguoiQueDong.tsx (4 độ tuổi × 5 tư thế)
```

## Luật cấm tuyệt đối
- **CẤM** `backdrop-filter: blur`, `filter: blur`, SVG `<filter>` blur (gây chậm render headless Chromium).
- **CẤM** `Math.random()` ở mọi nơi trong `src/`. Toàn bộ chuyển động, sinh vật, thời tiết, nháy mắt, nhép miệng, đồ họa hình học và thumbnail phải tất định 100% theo `useCurrentFrame()`, RMS tiền tính toán hoặc `bamTatDinh`.
- **CẤM** dữ liệu fallback hardcode của tập Pythagoras trong `src/canh/`, `src/daocu/MinhHoaToan.tsx` hay pipeline cho các tập khác.
- **KHÔNG** cài thêm thư viện Python nặng; chỉ dùng Python stdlib + `edge-tts` + `Pillow`.
- **KHÔNG** ghi cứng API key hay OAuth token trong mã nguồn; chỉ đọc từ `.env` / GitHub Secrets (`GEMINI_API_KEYS`, `GEMINI_API_KEY`; `YOUTUBE_API_KEY` tùy chọn).
- Luôn tương thích Windows (`python -X utf8`), mã hóa UTF-8, xuống dòng `LF`.
- Phong cách xuyên suốt: hoạt hình kể chuyện lịch sử Toán học thiên nhiên + hài hước dí dỏm, **KHÔNG đánh đấm**.

## Lệnh kiểm tra & chạy nhanh
- Kiểm tra toàn bộ (TypeScript + khung Remotion v2.0 + 49+ test Python): `npm run kiem-tra:all`
- Kiểm tra riêng Remotion/TS/FK/SFX/RMS/v2.0 Guard: `npm run kiem-tra`
- Kiểm tra riêng pipeline Python (offline): `python -X utf8 scripts/test_pipeline.py`
- Mở Remotion Studio: `npm run dev`
- Render video mẫu 25s (tương thích ngược): `npm run render:mau`
- Render video mẫu tương tác v2.0 (30s): `npx remotion render src/index.ts VideoDaiNguoiQue out/mau_v2_tuong_tac.mp4 --props=du_lieu/mau_v2_tuong_tac.json`
- Render thử Thumbnail A/B (`1280×720`): `npx remotion still src/index.ts ThumbnailToanHoc out/mau_thumbnail_check.png`
- Chạy hệ thống AI tự chủ (1 lệnh cục bộ): `python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py --so-tap 1`
- Render tách pha theo chunk/hồi (CI & cục bộ):
  - `python -X utf8 scripts/pipeline/render_dai.py --slug <ten> --chi-render-chunk hoi_03_p1 --che-do-ci`
  - `python -X utf8 scripts/pipeline/render_dai.py --slug <ten> --chi-render-hoi 1`
  - `python -X utf8 scripts/pipeline/render_dai.py --slug <ten> --chi-ghep-hoan-chinh --che-do-ci`
- Nạp số liệu YouTube thật để tự học:
  - `python -X utf8 scripts/pipeline/bo_nho_hoc_hoi.py --nhap-so-lieu-youtube --slug <ten> --ctr 8.4 --giu-chan-30s 72.5 --thoi-luong-xem-tb 05:45 --moc-tut-view "00:45,04:20" --bien-the-thumbnail-thang 2`
  - `python -X utf8 scripts/pipeline/bo_nho_hoc_hoi.py --nhap-so-lieu-youtube --file-so-lieu du_lieu/so_lieu_youtube.csv`
