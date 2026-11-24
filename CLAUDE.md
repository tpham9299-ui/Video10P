# Dự án Phim Hoạt Hình 2D Kể Chuyện Toán Học (`v0.4`)

Remotion `16:9` (`1920×1080`, `30fps`), TypeScript strict + Pipeline Python tự động hóa sản xuất phim hoạt hình kể chuyện lịch sử Toán học dài **> 10 phút (> 600 giây)** — chuyển động hoạt hình 2D mềm mượt có trọng lượng, tươi sáng, dí dỏm và tất định 100% theo `useCurrentFrame()`.

## Sơ đồ thư mục
```text
├── .env.example                      # Mẫu cấu hình GEMINI_API_KEYS xoay vòng & TTS_VOICE
├── requirements.txt                  # Thư viện Python gọn nhẹ: edge-tts, Pillow
├── du_lieu/
│   ├── mau_pythagoras.json           # Kịch bản mẫu 750 frames (25s), đủ 7 bố cục + hài hước + bảng giảng Toán
│   └── <slug>/                       # Dữ liệu sản xuất từng tập phim (cache_chuong/, nhap_kich_ban.json, doc_duyet_kich_ban.md, du_lieu_render.json)
├── public/{audio,sfx}/               # Audio TTS theo từng <slug>/ & SFX hoạt hình
├── scripts/
│   ├── test_khung.mjs                # Kiểm tra schema, bộ giải FK 14 động tác, duong_cong, hàm băm & luật cấm
│   ├── test_pipeline.py              # Unit test offline cho toàn bộ pipeline Python
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
    ├── VideoDai.tsx                  # Điều phối Sequence, 3 kiểu chuyển cảnh (mờ dần, quét ngang, iris wipe), tiến độ chương & phụ đề
    ├── boicanh/BoiCanhHoatHinh.tsx   # 8 bối cảnh SVG Parallax 3 lớp (0.2x / 0.5x / 1.0x) khớp camera + 7 lớp thời tiết
    ├── canh/                         # 7 bố cục cảnh + KhungLoiBinhHaiHuoc (bật lò xo springTatDinh)
    ├── daocu/                        # CongThucMath.tsx (KaTeX), DaoCu.tsx (SVG), MinhHoaToan.tsx (5 dạng động)
    ├── amthanh/sfx.ts                # Bản đồ SFX hoạt hình (chặn render <Audio> khi chưa có file thật)
    ├── xuong/                        # duong_cong.ts (ease/spring), dong_tac.ts (14 chuỗi diễn xuất), he_xuong.ts (FK mềm + độ trễ phụ kiện)
    ├── vfx/                          # tat_dinh.ts, MayQuayDong.tsx (CameraParallaxContext + easeOutBack), HieuUngHoatHinh.tsx (8 VFX lò xo)
    └── nhanvat/NguoiQueDong.tsx      # Thân & tứ chi <path> cong mềm, lip-sync 4 khẩu hình, ánh mắt liếc + chớp mắt tự nhiên, 9 biểu cảm, 8 phụ kiện
```

## Luật cấm tuyệt đối
- **CẤM** `backdrop-filter: blur`, `filter: blur`, SVG `<filter>` blur (gây chậm render headless Chromium).
- **CẤM** `Math.random()` ở mọi nơi trong `src/`. Toàn bộ chuyển động, thời tiết, nháy mắt, nhép miệng và hiệu ứng hài phải tất định 100% theo `useCurrentFrame()` + `bamTatDinh`.
- **KHÔNG** ghi cứng API key trong mã nguồn; chỉ đọc từ `.env` (`GEMINI_API_KEYS` / `GEMINI_API_KEY`).
- Luôn tương thích Windows (`python -X utf8`), mã hóa UTF-8, xuống dòng `LF`.

## Lệnh kiểm tra & chạy nhanh
- Kiểm tra toàn bộ (TypeScript + khung Remotion/FK + pipeline Python): `npm run kiem-tra:all`
- Kiểm tra riêng Remotion/TS/FK: `npm run kiem-tra`
- Kiểm tra riêng pipeline Python (offline): `python -X utf8 scripts/test_pipeline.py`
- Mở Remotion Studio: `npm run dev`
- Render video mẫu 25s: `npm run render:mau`
- Chạy pipeline 1 chạm tạo kịch bản để duyệt: `python -X utf8 scripts/pipeline/chay_tu_dong.py --chu-de "..." --slug <ten> --muc-tieu-phut 11 --dung-de-duyet`

## Đã hoàn thành ở `v0.4`
1. **Đường cong hoạt hình & Bộ giải xương khớp FK mềm (`duong_cong.ts`, `he_xuong.ts`)**: Thêm `easeInOutCubic`, `easeOutBack`, `easeInBack`, `springTatDinh`; nâng cấp khung xương sang FK phân cấp theo góc khớp có `offsetX`/`offsetY`, co giãn bảo toàn diện tích (`squashX * squashY = 1`), cột sống cong Quadratic Bezier (`diemUonThan`), tự kẹp bàn chân sát mặt đất và tính độ trễ phụ kiện từ `frame - 3` (`vanTocThan`, `doTrePhuKien`).
2. **14 chuỗi động tác diễn xuất sống động (`dong_tac.ts`)**: Mọi động tác đều có pha vào thế mượt 8–12 frame, lấy đà (anticipation), độ nảy (follow-through), chu kỳ sống động và lớp cử chỉ khi đang nói (`dangNoi = true`), nổi bật: `di_bo` 4 pha, `chay_voi_va` nghiêng 18–22° kèm bụi chân, `giat_minh_nhay_dung` có squash/stretch + lơ lửng 4 frame + đáp đất lò xo.
3. **Diễn xuất khuôn mặt & thân mềm (`NguoiQueDong.tsx`)**: Vẽ thân & tứ chi bằng `<path>` cong mềm qua khuỷu/gối, lip-sync 4 khẩu hình từ 3 sóng sin lệch tần số (`0.42`, `0.73`, `1.17`) + nhịp lấy hơi, con ngươi liếc theo hướng nhìn, chớp mắt không đều tự nhiên, lông mày nhún theo nhịp nói, phụ kiện bay theo quán tính và bóng đổ co nhạt khi nhảy cao.
4. **Parallax 3 lớp, Camera, VFX lò xo & 3 kiểu chuyển cảnh (`BoiCanhHoatHinh.tsx`, `MayQuayDong.tsx`, `HieuUngHoatHinh.tsx`, `KhungLoiBinhHaiHuoc.tsx`, `VideoDai.tsx`)**: Dịch mặt trời `bo_bien_hy_lap` sang trái (~30% bề ngang) tránh thẻ `GÓC BÌNH LUẬN`; thêm Parallax 3 lớp (`0.2x / 0.5x / 1.0x`) ăn khớp camera kèm chim vỗ cánh, tán cây lệch pha và sóng cuộn mượt; nâng cấp `zoom_hai_huoc` (`easeOutBack`), VFX/bong bóng thoại/thẻ bình luận bật bằng `springTatDinh`, và đủ 3 chuyển cảnh (`mo_dan`, `quet_ngang`, `vong_tron_hoat_hinh` iris wipe đóng-mở).
