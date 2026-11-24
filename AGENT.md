# Trạng thái bàn giao tác vụ (AGENT.md)

## Mốc hiện tại: `v0.3` — Trọn bộ pipeline Python tự động sản xuất phim hoạt hình Toán học dài >10 phút
- Tạo `requirements.txt` (`edge-tts`, `Pillow`) và `.env.example` hỗ trợ nhiều khóa `GEMINI_API_KEYS` xoay vòng tự động (không ghi cứng key trong mã nguồn).
- Xây dựng `scripts/pipeline/gemini_client.py`: nạp `.env` bằng thư viện chuẩn, xoay vòng API key + backoff khi gặp `429`/`503`/quota, tự làm sạch JSON bọc markdown và thử lại tối đa 2 lần khi JSON lỗi cú pháp.
- Xây dựng `scripts/pipeline/tao_kich_ban_10p.py`: kiến trúc biên kịch 3 tầng (Dàn ý 6 hồi khóa `danhSachNhanVat` + mạch `boiCanh`/`thoiTiet` → Viết chi tiết 6 hồi nối mạch 15–22 cảnh/hồi, tự bổ sung nếu <250 từ, lưu cache `du_lieu/<slug>/cache_chuong/`, sanitize 100% enum theo `src/kieu_dai.ts` → Hậu kiểm ngoặc `{}` LaTeX, xuất `nhap_kich_ban.json` và `doc_duyet_kich_ban.md`).
- Xây dựng `scripts/pipeline/chuan_hoa_doc_toan.py` & `scripts/pipeline/chuanbi_dai.py`: chuẩn hóa ký hiệu Toán (`√2`, `π`, `x^2`, `∞`, `TCN`, số thập phân, phân số...) sang tiếng Việt tự nhiên, sinh MP3 `edge-tts` vào `public/audio/<slug>/` có cache SHA-256, đo `ffprobe`, căn `tuFrame`/`denFrame` liền mạch `30fps` (nghỉ `0.25s` giữa cảnh, `0.75s` chuyển hồi), chia `phuDe[]` và cảnh báo nếu tổng thời lượng < 600 giây.
- Xây dựng `scripts/pipeline/render_dai.py`: render tách hồi bằng Remotion `--frames=<start>-<end>` với cache hash hồi (hỗ trợ `--chuong 2,4`), ghép FFmpeg `concat`, trộn `--nhac-nen` (`volume=0.08`, fade-out 3s cuối), xuất `out/<slug>_chapters.txt` và lưới kiểm định 18 khung hình `out/<slug>/luoi_kiem_dinh.png` bằng Pillow.
- Xây dựng lệnh 1 chạm `scripts/pipeline/chay_tu_dong.py` (hỗ trợ `--dung-de-duyet` & `--tiep-tuc-tu-kich-ban`) và bộ unit test offline `scripts/test_pipeline.py`; thêm `"kiem-tra:all"` vào `package.json`.

## Mốc tiếp theo: `v0.4` — Âm thanh hoạt hình SFX & Sản xuất tập phim >10 phút đầu tiên
- [ ] Bổ sung file âm thanh hoạt hình (`pop.mp3`, `ding.mp3`, `boing.mp3`, `crickets.mp3`, `whoosh.mp3`, `dramatic.mp3`) vào `public/sfx/` và bật `DANH_SACH_SFX_CO_SAN` trong `src/amthanh/sfx.ts`.
- [ ] Thêm nhạc nền nhẹ (royalty-free `.mp3`) và chạy sản xuất thực tế tập phim >10 phút đầu tiên.
- [ ] Tối ưu thumbnail tự động / chuyển cảnh âm thanh giữa các hồi dựa trên phản hồi từ `luoi_kiem_dinh.png`.
