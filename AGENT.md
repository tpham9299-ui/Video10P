# Trạng thái bàn giao tác vụ (AGENT.md)

## Mốc hiện tại: `v0.5` — Hệ thống AI Tự Chủ Hoàn Toàn (Web Grounding, Tự học hỏi, Tự kiểm định & Sản xuất liên tục)
- Mở rộng `scripts/pipeline/gemini_client.py`: thêm `bat_tim_kiem_web` và `tra_ve_nguon` trong `tao_van_ban()` / `tao_json()`, gắn `"tools": [{"google_search": {}}]`, trích xuất URL nguồn từ `groundingMetadata` / `groundingChunks`, giữ nguyên cơ chế xoay vòng `GEMINI_API_KEYS` và tự đổi/fallback model khi gặp `404`/`400`/`429`.
- Tạo `scripts/pipeline/bo_nho_hoc_hoi.py`: quản lý tệp bền vững `du_lieu/bo_nho_hoc_hoi.json` gồm `chu_de_da_lam[]`, `hang_doi_chu_de[]`, `bai_hoc_rut_ra[]` (tự gộp trùng & tỉa tối đa 25 bài học ưu tiên cao nhất) và `phan_hoi_kenh[]` (CLI `--hoc-tu-phan-hoi --slug <slug> --ghi-chu "..."`); cung cấp `tao_ngu_canh_hoc_hoi()` chống lặp, gợi ý "callback" tập cũ và tiêm quy tắc học được.
- Tạo `scripts/pipeline/san_tim_chu_de.py`: hỗ trợ `--nap-hang-doi N` (Gemini Google Search Grounding + lọc trùng) và `--nghien-cuu <slug>` / `--chu-de "..."` (kết hợp Wikipedia REST API + Gemini Grounding xuất `du_lieu/<slug>/tu_lieu_nghien_cuu.json`).
- Nâng cấp `scripts/pipeline/tao_kich_ban_10p.py`: tự nạp `tu_lieu_nghien_cuu.json` và `tao_ngu_canh_hoc_hoi()` vào prompt 6 hồi mục tiêu 1.750–2.150 từ (>10 phút, thiên nhiên + hài hước dí dỏm, KHÔNG đánh đấm); thêm **Tầng 3 — Tự kiểm định (Self-Critique) & Tự rút kinh nghiệm** kiểm tra Toán học/lịch sử/LaTeX `{}`, tự sửa cảnh lỗi và tự thêm quy tắc mới vào `bo_nho_hoc_hoi.json`.
- Mở rộng `scripts/pipeline/render_dai.py` & `scripts/pipeline/chay_tu_dong.py`: xuất thêm `out/<slug>/video_hoan_chinh.mp4` (giữ tương thích `out/<slug>.mp4`), `out/<slug>/chapters_va_mo_ta.txt` (tiêu đề gợi ý, mô tả hấp dẫn, mốc `MM:SS`, nguồn tham khảo) bên cạnh `out/<slug>/luoi_kiem_dinh.png`.
- Tạo `scripts/pipeline/san_xuat_lien_tuc.py`: bộ điều phối tự chủ không cần `--chu-de` (hàng đợi `'cho'` < 3 tự nạp 5 chủ đề → chọn điểm cao nhất → nghiên cứu web → biên kịch + tự kiểm định → TTS → render → cập nhật `chu_de_da_lam` & `'xong'`), hỗ trợ `--so-tap`, `--nghi-giay 30`, `--chu-de`, `--chi-tao-kich-ban` và tự ghi log/chạy tiếp khi 1 tập lỗi.
- Tạo `.github/workflows/tu-dong-video10p.yml`, `HUONG_DAN_TU_DONG.md`, cập nhật `.env.example`, `CLAUDE.md`, `package.json` và mở rộng `scripts/test_pipeline.py` (offline/mock toàn diện).

## Mốc tiếp theo: `v0.6` — Âm thanh hoạt hình SFX & Tối ưu xuất bản kênh
- [ ] Bổ sung file âm thanh hoạt hình (`pop.mp3`, `ding.mp3`, `boing.mp3`, `crickets.mp3`, `whoosh.mp3`, `dramatic.mp3`) vào `public/sfx/` và bật `DANH_SACH_SFX_CO_SAN` trong `src/amthanh/sfx.ts`.
- [ ] Thêm nhạc nền nhẹ (royalty-free `.mp3`) và chạy sản xuất thực tế các tập phim >10 phút đầu tiên trên máy cục bộ / GitHub Actions.
- [ ] Bổ sung tạo ảnh thumbnail tự động từ khung hình nổi bật + tối ưu vòng học hỏi từ dữ liệu phản hồi kênh thật.
