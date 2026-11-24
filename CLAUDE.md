# Dự án Phim Hoạt Hình 2D Kể Chuyện Toán Học (`v0.3`)

Remotion `16:9` (`1920×1080`, `30fps`), TypeScript strict + Pipeline Python tự động hóa sản xuất phim hoạt hình kể chuyện lịch sử Toán học dài **> 10 phút (> 600 giây)** — tươi sáng/điện ảnh, dí dỏm và tất định 100% theo `useCurrentFrame()`.

## Sơ đồ thư mục
```text
├── .env.example                      # Mẫu cấu hình GEMINI_API_KEYS xoay vòng & TTS_VOICE
├── requirements.txt                  # Thư viện Python gọn nhẹ: edge-tts, Pillow
├── du_lieu/
│   ├── mau_pythagoras.json           # Kịch bản mẫu 750 frames (25s), đủ 7 bố cục + hài hước + bảng giảng Toán
│   └── <slug>/                       # Dữ liệu sản xuất từng tập phim (cache_chuong/, nhap_kich_ban.json, doc_duyet_kich_ban.md, du_lieu_render.json)
├── public/{audio,sfx}/               # Audio TTS theo từng <slug>/ & SFX hoạt hình
├── scripts/
│   ├── test_khung.mjs                # Kiểm tra schema, 14 động tác tất định, hàm băm & luật cấm
│   ├── test_pipeline.py              # Unit test offline cho toàn bộ pipeline Python v0.3
│   └── pipeline/
│       ├── gemini_client.py          # Gọi Gemini xoay vòng nhiều API key, backoff & parse JSON an toàn
│       ├── tao_kich_ban_10p.py       # AI biên kịch 3 tầng (Dàn ý 6 Hồi -> Chi tiết nối mạch -> Hậu kiểm LaTeX & duyệt)
│       ├── chuan_hoa_doc_toan.py     # Chuyển ký hiệu/công thức Toán (√2, π, x^2, TCN, phân số...) sang tiếng Việt TTS
│       ├── chuanbi_dai.py            # Edge TTS có cache SHA-256, đo ffprobe, căn frame 30fps & chia phụ đề
│       ├── render_dai.py             # Render tách hồi có cache hash, ghép FFmpeg + nhạc nền, chapters.txt & lưới 18 khung hình
│       └── chay_tu_dong.py           # Lệnh chạy 1 chạm từ 1 câu chủ đề (có cờ --dung-de-duyet)
└── src/
    ├── index.ts, Root.tsx            # Đăng ký Composition VideoDaiNguoiQue (calculateMetadata)
    ├── kieu_dai.ts                   # Hợp đồng dữ liệu cho phim hoạt hình kể chuyện Toán học
    ├── VideoDai.tsx                  # Điều phối Sequence, tiến độ chương, phụ đề 16:9 dễ đọc mọi nền
    ├── boicanh/BoiCanhHoatHinh.tsx   # 8 bối cảnh thiên nhiên/cảnh vật SVG 3 lớp động + 7 lớp thời tiết
    ├── canh/                         # 7 bố cục cảnh + KhungLoiBinhHaiHuoc
    ├── daocu/                        # CongThucMath.tsx (KaTeX), DaoCu.tsx (SVG), MinhHoaToan.tsx (5 dạng động)
    ├── amthanh/sfx.ts                # Bản đồ SFX hoạt hình (chặn render <Audio> khi chưa có file thật)
    ├── xuong/                        # he_xuong.ts (14 động tác diễn xuất/hài), dong_tac.ts
    ├── vfx/                          # tat_dinh.ts, MayQuayDong.tsx, HieuUngHoatHinh.tsx (8 VFX)
    └── nhanvat/NguoiQueDong.tsx      # Nhân vật hoạt hình nháy mắt tự động, 9 biểu cảm, 8 phụ kiện & 8 vật cầm tay
```

## Luật cấm tuyệt đối
- **CẤM** `backdrop-filter: blur`, `filter: blur`, SVG `<filter>` blur (gây chậm render headless Chromium).
- **CẤM** `Math.random()` ở mọi nơi trong `src/`. Toàn bộ chuyển động, thời tiết, nháy mắt và hiệu ứng hài phải tất định 100% theo `useCurrentFrame()` + `bamTatDinh`.
- **KHÔNG** ghi cứng API key trong mã nguồn; chỉ đọc từ `.env` (`GEMINI_API_KEYS` / `GEMINI_API_KEY`).
- Luôn tương thích Windows (`python -X utf8`), mã hóa UTF-8, xuống dòng `LF`.

## Lệnh kiểm tra & chạy nhanh
- Kiểm tra toàn bộ (TypeScript + khung Remotion + pipeline Python): `npm run kiem-tra:all`
- Kiểm tra riêng Remotion/TS: `npm run kiem-tra`
- Kiểm tra riêng pipeline Python (offline): `python -X utf8 scripts/test_pipeline.py`
- Mở Remotion Studio: `npm run dev`
- Render video mẫu: `npm run render:mau`
- Chạy pipeline 1 chạm tạo kịch bản để duyệt: `python -X utf8 scripts/pipeline/chay_tu_dong.py --chu-de "..." --slug <ten> --muc-tieu-phut 11 --dung-de-duyet`

## Đã hoàn thành ở `v0.3`
1. **Gemini Client xoay vòng key (`gemini_client.py`)**: Đọc `GEMINI_API_KEYS` (fallback `GEMINI_API_KEY`), tự xoay vòng kèm backoff khi gặp `429`/`503`/quota, tự làm sạch JSON bọc markdown và thử lại tối đa 2 lần nếu lỗi cú pháp.
2. **AI biên kịch 3 tầng dài >10 phút (`tao_kich_ban_10p.py`)**: Tầng 1 lập dàn ý 6 hồi khóa nhân vật & mạch bối cảnh/thời tiết; Tầng 2 viết 6 hồi nối mạch 15–22 cảnh/hồi, tự động gọi bổ sung nếu hồi < 250 từ, lưu `cache_chuong/` và sanitize 100% enum theo `src/kieu_dai.ts`; Tầng 3 hậu kiểm ngoặc `{}` LaTeX và xuất `nhap_kich_ban.json` + `doc_duyet_kich_ban.md`.
3. **Giọng đọc TTS chuẩn Toán & khớp frame (`chuan_hoa_doc_toan.py`, `chuanbi_dai.py`)**: Chuẩn hóa ký hiệu Toán sang tiếng Việt tự nhiên, tạo `.mp3` bằng `edge-tts` có cache SHA-256, đo thời lượng bằng `ffprobe`, cộng khoảng nghỉ `0.25s` giữa cảnh / `0.75s` chuyển hồi, tính `tuFrame`/`denFrame` liền mạch ở `30fps` và chia `phuDe[]`.
4. **Render tách hồi bền bỉ & Mắt kiểm định (`render_dai.py`, `chay_tu_dong.py`)**: Render từng hồi bằng `--frames`, cache hash từng hồi (hỗ trợ `--chuong 2,4`), ghép FFmpeg + nhạc nền (`volume=0.08`, fade-out 3s cuối), xuất `out/<slug>_chapters.txt` và ảnh lưới kiểm định 18 khung hình `out/<slug>/luoi_kiem_dinh.png`.
