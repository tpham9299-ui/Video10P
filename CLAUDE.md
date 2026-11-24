# Dự án Phim Hoạt Hình 2D Kể Chuyện Toán Học (`v0.5`)

Remotion `16:9` (`1920×1080`, `30fps`), TypeScript strict + **Hệ thống AI tự chủ hoàn toàn (Python)** sản xuất phim hoạt hình kể chuyện lịch sử Toán học dài **> 10 phút (> 600 giây)** — phong cách thiên nhiên + hài hước dí dỏm (KHÔNG đánh đấm), tự tra cứu kiểm chứng tư liệu web, tự học hỏi qua bộ nhớ bền vững và tự sản xuất liên tục cục bộ lẫn trên GitHub Actions.

## Sơ đồ thư mục
```text
├── .env.example                           # Mẫu cấu hình GEMINI_API_KEYS xoay vòng, fallback model & TTS_VOICE
├── .github/workflows/tu-dong-video10p.yml # GitHub Actions chạy định kỳ (cron) & chạy tay (workflow_dispatch)
├── HUONG_DAN_TU_DONG.md                   # Hướng dẫn vận hành hệ thống tự chủ cục bộ & GitHub Actions
├── requirements.txt                       # Thư viện Python gọn nhẹ: edge-tts, Pillow
├── du_lieu/
│   ├── bo_nho_hoc_hoi.json                # Bộ nhớ tự học bền vững (tập đã làm, hàng đợi, <=25 bài học, phản hồi kênh)
│   ├── mau_pythagoras.json                # Kịch bản mẫu 750 frames (25s), đủ 7 bố cục + hài hước + bảng giảng Toán
│   └── <slug>/                            # Dữ liệu từng tập (tu_lieu_nghien_cuu.json, cache_chuong/, nhap_kich_ban.json, doc_duyet_kich_ban.md, du_lieu_render.json)
├── public/{audio,sfx}/                    # Audio TTS theo từng <slug>/ & SFX hoạt hình
├── scripts/
│   ├── test_khung.mjs                     # Kiểm tra schema, bộ giải FK 14 động tác, duong_cong, hàm băm & luật cấm
│   ├── test_pipeline.py                   # Unit test offline cho toàn bộ hệ thống AI & pipeline Python v0.5
│   └── pipeline/
│       ├── gemini_client.py               # Gọi Gemini xoay vòng key, fallback model (404/400/429) & Google Search Grounding
│       ├── bo_nho_hoc_hoi.py              # Bộ nhớ tự học bền vững, chống trùng chủ đề, tỉa tối đa 25 bài học & học từ phản hồi
│       ├── san_tim_chu_de.py              # Tự săn chủ đề web (--nap-hang-doi) & nghiên cứu Wikipedia + Gemini Grounding (--nghien-cuu)
│       ├── tao_kich_ban_10p.py            # AI biên kịch 3 tầng (Dàn ý 6 Hồi -> 1.750–2.150 từ -> Tầng 3 Tự kiểm định & tự học)
│       ├── chuan_hoa_doc_toan.py          # Chuyển ký hiệu/công thức Toán (√2, π, x^2, TCN, phân số...) sang tiếng Việt TTS
│       ├── chuanbi_dai.py                 # Edge TTS có cache SHA-256, đo ffprobe, căn frame 30fps & chia phụ đề
│       ├── render_dai.py                  # Render tách hồi có cache hash, ghép FFmpeg, video_hoan_chinh.mp4, chapters_va_mo_ta.txt & lưới 18 khung hình
│       ├── chay_tu_dong.py                # Lệnh chạy 1 chạm từ 1 câu chủ đề (giữ tương thích cờ CLI cũ)
│       └── san_xuat_lien_tuc.py           # Bộ điều phối tự chủ liên tục nhiều tập (--so-tap, --nghi-giay, --chu-de, --chi-tao-kich-ban)
└── src/
    ├── index.ts, Root.tsx                 # Đăng ký Composition VideoDaiNguoiQue (calculateMetadata)
    ├── kieu_dai.ts                        # Hợp đồng dữ liệu cho phim hoạt hình kể chuyện Toán học
    ├── VideoDai.tsx                       # Điều phối Sequence, 3 kiểu chuyển cảnh (mờ dần, quét ngang, iris wipe), tiến độ chương & phụ đề
    ├── boicanh/BoiCanhHoatHinh.tsx        # 8 bối cảnh SVG Parallax 3 lớp (0.2x / 0.5x / 1.0x) khớp camera + 7 lớp thời tiết
    ├── canh/                              # 7 bố cục cảnh + KhungLoiBinhHaiHuoc (bật lò xo springTatDinh)
    ├── daocu/                             # CongThucMath.tsx (KaTeX), DaoCu.tsx (SVG), MinhHoaToan.tsx (5 dạng động)
    ├── amthanh/sfx.ts                     # Bản đồ SFX hoạt hình (chặn render <Audio> khi chưa có file thật)
    ├── xuong/                             # duong_cong.ts (ease/spring), dong_tac.ts (14 chuỗi diễn xuất), he_xuong.ts (FK mềm + độ trễ phụ kiện)
    ├── vfx/                               # tat_dinh.ts, MayQuayDong.tsx (CameraParallaxContext + easeOutBack), HieuUngHoatHinh.tsx (8 VFX lò xo)
    └── nhanvat/NguoiQueDong.tsx           # Thân & tứ chi <path> cong mềm, lip-sync 4 khẩu hình, ánh mắt liếc + chớp mắt tự nhiên, 9 biểu cảm, 8 phụ kiện
```

## Luật cấm tuyệt đối
- **CẤM** `backdrop-filter: blur`, `filter: blur`, SVG `<filter>` blur (gây chậm render headless Chromium).
- **CẤM** `Math.random()` ở mọi nơi trong `src/`. Toàn bộ chuyển động, thời tiết, nháy mắt, nhép miệng và hiệu ứng hài phải tất định 100% theo `useCurrentFrame()` + `bamTatDinh`.
- **KHÔNG** ghi cứng API key trong mã nguồn; chỉ đọc từ `.env` / biến môi trường (`GEMINI_API_KEYS` tách dấu phẩy, fallback `GEMINI_API_KEY`).
- Luôn tương thích Windows (`python -X utf8`), mã hóa UTF-8, xuống dòng `LF`.
- Phong cách xuyên suốt: hoạt hình kể chuyện lịch sử Toán học thiên nhiên + hài hước dí dỏm, **KHÔNG đánh đấm**.

## Lệnh kiểm tra & chạy nhanh
- Kiểm tra toàn bộ (TypeScript + khung Remotion/FK + pipeline Python v0.5): `npm run kiem-tra:all`
- Kiểm tra riêng Remotion/TS/FK: `npm run kiem-tra`
- Kiểm tra riêng pipeline Python (offline): `python -X utf8 scripts/test_pipeline.py`
- Mở Remotion Studio: `npm run dev`
- Render video mẫu 25s: `npm run render:mau`
- Chạy hệ thống AI tự chủ (tự săn chủ đề, nghiên cứu web, biên kịch, TTS & render): `python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py --so-tap 1`
- Nạp phản hồi kênh để AI tự rút bài học: `python -X utf8 scripts/pipeline/bo_nho_hoc_hoi.py --hoc-tu-phan-hoi --slug <ten> --ghi-chu "..."`
- Chạy pipeline 1 chạm thủ công (tương thích cũ): `python -X utf8 scripts/pipeline/chay_tu_dong.py --chu-de "..." --slug <ten> --muc-tieu-phut 11 --dung-de-duyet`

## Đã hoàn thành ở `v0.5`
1. **Google Search Grounding (`gemini_client.py`)**: Bổ sung `bat_tim_kiem_web` và `tra_ve_nguon` cho `tao_van_ban()` & `tao_json()`, tự gắn `"tools": [{"google_search": {}}]`, trích xuất danh sách nguồn tham khảo từ `groundingMetadata` / `groundingChunks`, giữ nguyên cơ chế xoay vòng nhiều key (`GEMINI_API_KEYS`) và tự đổi model khi `404`/`400`/`429`.
2. **Bộ nhớ Tự học hỏi & Hàng đợi (`bo_nho_hoc_hoi.py`)**: Quản lý `du_lieu/bo_nho_hoc_hoi.json` (tự khởi tạo sạch), chống trùng chủ đề theo slug và độ tương đồng tiêu đề, tự gộp & giữ tối đa 25 bài học ưu tiên cao nhất, hỗ trợ `--hoc-tu-phan-hoi` và `tao_ngu_canh_hoc_hoi()` (chống lặp + gợi ý "callback" tập cũ + top bài học).
3. **Tự săn chủ đề & Nghiên cứu đa nguồn (`san_tim_chu_de.py`)**: `--nap-hang-doi N` dùng Gemini Grounding lọc trùng nạp hàng đợi; `--nghien-cuu <slug>` kết hợp Wikipedia REST API + Gemini Grounding xuất `du_lieu/<slug>/tu_lieu_nghien_cuu.json` đầy đủ niên đại, nhân vật thật, 3–4 giai thoại đời thường, 2–3 kiến thức/LaTeX cốt lõi, ứng dụng hiện đại và URL nguồn.
4. **Biên kịch 3 tầng + Tầng 3 Tự kiểm định (`tao_kich_ban_10p.py`)**: Tự nạp `tu_lieu_nghien_cuu.json` + ngữ cảnh tự học hỏi vào prompt, mục tiêu 1.750–2.150 từ (>10 phút), bổ sung Tầng 3 Self-Critique đối chiếu Toán/lịch sử/LaTeX/nhịp hài, tự sửa cảnh lỗi và tự lưu bài học mới vào `bo_nho_hoc_hoi.json`.
5. **Trọn gói YouTube & Điều phối sản xuất liên tục (`render_dai.py`, `san_xuat_lien_tuc.py`)**: Xuất `out/<slug>/video_hoan_chinh.mp4`, `out/<slug>/chapters_va_mo_ta.txt` và `out/<slug>/luoi_kiem_dinh.png`; bộ điều phối `san_xuat_lien_tuc.py` chạy tự chủ không cần `--chu-de`, tự nạp hàng đợi khi `< 3`, hỗ trợ `--so-tap`, `--nghi-giay`, `--chu-de`, `--chi-tao-kich-ban` và tự ghi log/tiếp tục khi 1 tập lỗi.
6. **GitHub Actions & Kiểm thử offline (`.github/workflows/tu-dong-video10p.yml`, `scripts/test_pipeline.py`, `HUONG_DAN_TU_DONG.md`)**: Tự động chạy theo lịch `cron` & `workflow_dispatch`, cache Node/Python/Chromium, upload artifact đầy đủ và tự commit/push cập nhật `du_lieu/bo_nho_hoc_hoi.json` + tư liệu/kịch bản nhẹ về `main`.
