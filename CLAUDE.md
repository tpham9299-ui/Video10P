# Dự án Phim Hoạt Hình 2D/2.5D Kể Chuyện Toán Học (`v3.5`)

Remotion `16:9` (`1920×1080`, `30fps` + `<Still>` Thumbnail `1280×720`), TypeScript strict + **Hệ thống AI tự chủ khép kín cách 2 ngày (Python stdlib + GitHub Actions + Tự động đăng YouTube hẹn giờ `+07:00`)** theo kiến trúc **Lai 2.5D & Kể Chuyện Điện Ảnh `v3.5`**: bối cảnh minh họa truyện tranh châu Âu đồng nhất sinh bằng AI (`STYLE_BIBLE_BOI_CANH` + phân tích ánh sáng `Pillow` tự đồng bộ lên nhân vật, fallback mượt về 22 bối cảnh Parallax SVG), nhân vật truyện tranh viền mực `#1A1A1A` mặc **7 bộ trang phục 2 sắc độ + 7 kiểu tóc + 4 kiểu râu + bóng tiếp đất + 4 độ tuổi × 5 tư thế × 20 động tác FK**, **Mascot dẫn chuyện cố định của kênh (`mascot_pi`)**, **Clean Cinema UI** (thẻ tên hồi giấy da 2.8s, phụ đề viền mảnh không che chân, bảng phấn / cuộn giấy da cổ), **12 góc quay điện ảnh** gồm 4 góc cận mặt & **Shot-Reverse-Shot (`dao_goc_can_mat`)**, **3 khung hình kể chuyện v3.5** (`CanhBanDoHanhTrinh`, `CanhBaoChiCo`, `CanhPhanUngCam`), **End-Screen 15s chuẩn YouTube 2 khung**, **nhạc nền đa cảm xúc 4 sắc thái (`vui_tuoi`, `bi_an`, `kich_tinh`, `tram_lang`) crossfade 1.5s + ngắt nhạc punchline 0.8s**, **bong bóng chat 4 kiểu**, **14 VFX hoạt hình**, **Guardrail khóa dấu tiếng Việt trước Edge TTS**, **Cold Open 15s + Open Loop cuối hồi + ẩn dụ hiện đại hài hước** và **Thumbnail A/B ưu tiên ảnh nền AI**.

## Sơ đồ thư mục
```text
├── .env.example                           # Mẫu cấu hình GEMINI_API_KEYS, GEMINI_IMAGE_MODELS, đa giọng TTS, Mascot & OAuth YouTube tùy chọn
├── .gitignore                             # Loại trừ .env, node_modules/, out/, *.mp4, public/audio/, public/boi_canh/, cache_boi_canh.json & cache nặng
├── .github/workflows/tu-dong-video10p.yml # GitHub Actions 3 job nối tiếp (07:00 VN cách 2 ngày `0 0 */2 * *` + workflow_dispatch gồm tat_anh_ai, tu_dong_dang_youtube, che_do_dang)
├── HUONG_DAN_TU_DONG.md                   # Hướng dẫn vận hành v3.5 cục bộ, sinh bối cảnh AI, GitHub Actions cách 2 ngày & tự động đăng YouTube
├── requirements.txt                       # Thư viện Python gọn nhẹ: edge-tts, Pillow (không cài SDK nặng)
├── du_lieu/
│   ├── bo_nho_hoc_hoi.json                # Bộ nhớ tự học bền vững (chu_de_da_lam + youtubeVideoId/youtubePublishAt, hang_doi_chu_de, <=25 bài học ưu tiên, phan_hoi_kenh)
│   ├── mau_pythagoras.json                # Kịch bản mẫu tương thích ngược 750 frames (25s), đủ 7 bố cục + SFX + bảng giảng Toán
│   ├── mau_v2_tuong_tac.json              # Kịch bản mẫu tương tác v2.0 (900 frames, 30s)
│   ├── mau_v3_dien_anh.json               # Kịch bản mẫu điện ảnh v3.0 (935 frames, ~31s): Euler & 7 cây cầu, 7 trang phục/tóc/râu, Clean Cinema UI, 4 góc cận mặt, 4 kiểu bong bóng, 6 VFX hài
│   └── <slug>/                            # Dữ liệu từng tập (tu_lieu_nghien_cuu.json, nhap_kich_ban.json, doc_duyet_kich_ban.md, du_lieu_render.json)
├── public/
│   ├── audio/<slug>/                      # Audio TTS theo từng <slug>/ (loại trừ bởi .gitignore)
│   ├── boi_canh/<slug>/                   # Ảnh nền minh họa AI JPEG 16:9 <250KB theo <slug>/ (loại trừ bởi .gitignore)
│   ├── sfx/                               # 6 SFX hoạt hình (pop, ding, boing, crickets, whoosh, dramatic)
│   └── bgm/                               # 5 nhạc nền loop mượt: nhac_nen_nhe.mp3 + 4 sắc thái v3.5 (vui_tuoi, bi_an, kich_tinh, tram_lang)
├── scripts/
│   ├── test_khung.mjs                     # Kiểm định TS/Remotion v3.5: Lai 2.5D, Clean Cinema UI, 4 BGM, 3 cảnh mới, Mascot, End-Screen 2 khung, Thumbnail AI & luật cấm
│   ├── test_pipeline.py                   # 70 unit test offline toàn chuỗi Python v3.5 (nhạc 4 cảm xúc crossfade 1.5s + ngắt 0.8s, dang_youtube.py, 3 cảnh mới, Mascot, Guardrail dấu TV)
│   └── pipeline/
│       ├── tao_am_thanh_mau.py            # Tổng hợp offline 6 SFX + 5 nhạc nền loop mượt (nhac_nen_nhe + 4 sắc thái cảm xúc v3.5) bằng stdlib + ffmpeg
│       ├── gemini_client.py               # Gemini REST text & Vision, xoay vòng key, fallback model & Google Search Grounding
│       ├── tao_boi_canh_ai.py             # Sinh 14-20 bối cảnh + 4-6 cận cảnh vật thể AI (Gemini/Imagen), nén JPEG <250KB, cache hash & phân tích anhSangMoiTruong bằng Pillow
│       ├── bo_nho_hoc_hoi.py              # Bộ nhớ tự học, chống trùng, xóa khỏi hàng đợi sau khi xong, giữ metadata YouTube & nạp số liệu YouTube
│       ├── dong_bo_youtube.py             # Cầu nối tùy chọn kéo thống kê YouTube Data API v3 bằng stdlib (tự tra youtubeVideoId từ bộ nhớ)
│       ├── dang_youtube.py                # Tự động đăng YouTube bằng Python stdlib (Resumable Upload 8MB, hẹn giờ publishAt +07:00, thumbnail, phụ đề .srt, thoát 0 khi thiếu secret)
│       ├── lay_refresh_token_youtube.py   # Tiện ích chạy 1 lần trên máy cá nhân lấy YOUTUBE_REFRESH_TOKEN trong 30s (thuần stdlib http.server + webbrowser)
│       ├── san_tim_chu_de.py              # Tự săn 6 chủ đề giàu giai thoại & nghiên cứu xuất timeline_su_kien, tu_dien_phat_am, goi_y_boi_canh_va_dao_cu
│       ├── tao_kich_ban_10p.py            # AI biên kịch & đạo diễn v3.5: Cold Open 15s, Open Loop, ẩn dụ hiện đại, tamTrangNhac, ngatNhacPunchline, 3 cảnh mới, Mascot & Guardrail dấu TV
│       ├── chuan_hoa_doc_toan.py          # Chuẩn hóa ký hiệu Toán + từ điển phát âm (chỉ cho Edge TTS, giữ nguyên chính tả gốc cho phụ đề)
│       ├── chuanbi_dai.py                 # Guardrail dấu TV trước TTS, Edge TTS đa giọng rõ vai, nhịp nghỉ hài 0.25-0.4s cho luotThoai[], RMS 30fps, sinh bối cảnh AI & xuất .srt
│       ├── render_dai.py                  # Chia chunk >120s, tối ưu CI=true, ghép FFmpeg nhạc 4 cảm xúc crossfade 1.5s + ngắt 0.8s + -14 LUFS, keyframe QA & Thumbnail A/B ưu tiên ảnh AI
│       ├── chay_tu_dong.py                # Lệnh chạy 1 chạm từ 1 câu chủ đề (hỗ trợ --tat-anh-ai)
│       └── san_xuat_lien_tuc.py           # Điều phối tự chủ (hỗ trợ --tat-anh-ai, --chi-chuan-bi, --hoan-tat-tu-meta)
└── src/
    ├── index.ts, Root.tsx                 # Composition VideoDaiNguoiQue (calculateMetadata) & Still ThumbnailToanHoc (1280×720)
    ├── Thumbnail.tsx                      # 3 biến thể Thumbnail A/B tương phản cao (ưu tiên ảnh nền AI anhBoiCanh v3.5, không blur)
    ├── kieu_dai.ts                        # Hợp đồng dữ liệu v3.5 (10 bố cục, 4 sắc thái nhạc, 12 góc quay, 7 trang phục/tóc, 4 râu, Mascot, End-Screen, 3 cảnh mới)
    ├── VideoDai.tsx                       # Clean Cinema UI: tự đăng ký Mascot kênh, định tuyến 10 bố cục kể chuyện, TheTenHoi 2.8s, phụ đề viền mảnh, 0 gap frame
    ├── boicanh/                           # NenMinhHoaAI.tsx + nen_ai_logic.ts (Ken Burns + không khí tất định), BoiCanhHoatHinh.tsx, BoiCanhMoi.tsx (22 bối cảnh React.memo), SinhVatVaMoiTruong.tsx
    ├── canh/                              # 12 component cảnh gồm 3 cảnh v3.5 (CanhBanDoHanhTrinh, CanhBaoChiCo, CanhPhanUngCam) + CanhKet End-Screen 2 khung + ke_chuyen_v35_logic.ts + TheTenHoi + BongBongChat
    ├── daocu/                             # CongThucMath.tsx (KaTeX), DaoCu.tsx (20 đạo cụ), MinhHoaToan.tsx & minh_hoa_hop_le.ts (100% JSON, không hardcode)
    ├── amthanh/sfx.ts                     # Bản đồ 6 SFX hoạt hình an toàn (đồng bộ 6 VFX hài & 4 kiểu bong bóng)
    ├── xuong/                             # duong_cong.ts, dong_tac.ts (20 chuỗi diễn xuất), he_xuong.ts (FK mềm + khóa góc cổ/đầu an toàn)
    ├── vfx/                               # tat_dinh.ts, dao_dien_camera.ts + MayQuayDong.tsx (12 góc quay + tia tốc độ + AnhSangCanhContext), vi_tri_vfx.ts + HieuUngHoatHinh.tsx (14 VFX)
    └── nhanvat/                           # mascot_kenh.ts (Mascot mặc định dễ tùy chỉnh), lip_sync.ts (RMS 4 khẩu hình), ten_nhan_vat.ts, hoa_trang_va_anh_sang.ts, TrangPhucVaToc.tsx, NguoiQueDong.tsx
```

## Luật cấm tuyệt đối
- **CẤM** `backdrop-filter: blur`, `filter: blur`, SVG `<filter>` blur ở mọi nơi trong `src/`.
- **CẤM** `Math.random()` ở mọi nơi trong `src/`. Toàn bộ chuyển động, không khí, sinh vật, thời tiết, nháy mắt, nhép miệng, đồ họa hình học, bản đồ, báo cổ, phản ứng câm và thumbnail phải tất định 100% theo `useCurrentFrame()`, RMS tiền tính toán hoặc `bamTatDinh`.
- **CẤM** dữ liệu fallback hardcode của tập Pythagoras trong `src/` hay pipeline cho tập khác; **CẤM** hardcode biển số `"1729"` mặc định.
- **KHÔNG** cài thêm thư viện Python nặng; chỉ dùng Python stdlib + `edge-tts` + `Pillow`.
- **KHÔNG** ghi cứng API key hay OAuth token trong mã nguồn; chỉ đọc từ `.env` / GitHub Secrets (`GEMINI_API_KEYS`, `GEMINI_API_KEY`, `GEMINI_IMAGE_MODELS`; `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`, `YOUTUBE_API_KEY` tùy chọn).
- Luôn tương thích Windows (`python -X utf8`), mã hóa UTF-8, xuống dòng `LF`.
- Phong cách xuyên suốt: hoạt hình kể chuyện lịch sử Toán học thiên nhiên + hài hước dí dỏm, **KHÔNG đánh đấm**.

## Lệnh kiểm tra & chạy nhanh
- Kiểm tra toàn bộ (TypeScript + khung Remotion v3.5 + 70 unit test Python): `npm run kiem-tra:all`
- Kiểm tra riêng Remotion/TS/v3.5: `npm run kiem-tra`
- Kiểm tra riêng pipeline Python (offline): `python -X utf8 scripts/test_pipeline.py`
- Mở Remotion Studio: `npm run dev`
- Sinh lại 6 SFX & 5 nhạc nền mẫu (`nhac_nen_nhe` + 4 sắc thái cảm xúc): `python -X utf8 scripts/pipeline/tao_am_thanh_mau.py`
- Lấy Refresh Token YouTube 1 lần trong 30 giây: `python -X utf8 scripts/pipeline/lay_refresh_token_youtube.py`
- Tự động đăng YouTube kèm hẹn giờ công khai 19:30 VN: `python -X utf8 scripts/pipeline/dang_youtube.py --slug <ten> --gio-cong-khai-vn "19:30" --cach-ngay 0`
- Chạy hệ thống AI tự chủ (1 lệnh cục bộ, tự sinh bối cảnh AI hoặc truyền `--tat-anh-ai` để dùng SVG): `python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py --so-tap 1`
- Render thử Thumbnail A/B (`1280×720`): `npx remotion still src/index.ts ThumbnailToanHoc out/mau_thumbnail_check.png`
