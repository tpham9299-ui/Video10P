# Trạng thái bàn giao tác vụ (AGENT.md)

## Mốc hiện tại: `v3.5` — Nâng Cấp Kể Chuyện Điện Ảnh, Nhạc Nền Đa Cảm Xúc & Tự Động Đăng YouTube (Pure Stdlib)

Toàn bộ nền tảng `v3.0` (Lai 2.5D + Clean Cinema UI + Khóa dấu tiếng Việt 100%) đã được nâng cấp lên **`v3.5`** cùng tính năng tự động đăng YouTube định kỳ cách 2 ngày; toàn bộ kiểm định offline (`npm run kiem-tra:all` ở cả thường và `CI=true`: 0 lỗi TS, toàn bộ kiểm khung Remotion xanh, 70/70 unit test Python xanh) đều đạt:

1. **Nhạc nền đa cảm xúc 4 sắc thái & Nhịp ngắt hài punchline (`tao_am_thanh_mau.py`, `render_dai.py`)**:
   - Sinh sẵn 4 sắc thái nhạc nền loop mượt trong `public/bgm/`: `vui_tuoi.mp3`, `bi_an.mp3`, `kich_tinh.mp3`, `tram_lang.mp3` (giữ nguyên `nhac_nen_nhe.mp3` và không ghi đè file người dùng tự chép đè).
   - AI gán `tamTrangNhac` theo từng Hồi; [render_dai.py](file:///e:/Video10P/scripts/pipeline/render_dai.py) tự lập lịch `tinh_lich_trinh_nhac_nen()`, ghép chuyển đổi mượt giữa các hồi bằng FFmpeg `acrossfade=d=1.50` và chèn khoảng ngắt nhạc đột ngột `0.8s` (`volume=0:enable='between(t,...)'`) trước các cảnh đánh dấu `ngatNhacPunchline: true`, rồi chạy auto-ducking `-14 LUFS`.

2. **3 kiểu khung hình kể chuyện mới (`src/canh/`)**:
   - [CanhBanDoHanhTrinh.tsx](file:///e:/Video10P/src/canh/CanhBanDoHanhTrinh.tsx): bản đồ giấy da cổ 2 sắc độ có đường cong nét đứt chạy dần theo frame nối `diemDi` → `diemDen` cùng 4 biểu tượng (`tau_thuy`, `thu_tay`, `nguoi_di_bo`, `xe_ngua`) di chuyển mượt theo tiếp tuyến Bezier.
   - [CanhBaoChiCo.tsx](file:///e:/Video10P/src/canh/CanhBaoChiCo.tsx): tờ báo giấy cổ xoay/phóng ra màn hình tất định (`tinhBienDoiBaoChiCo`) với tiêu đề giật gân (`tieuDeBao`), ảnh/đạo cụ minh họa nhỏ và tiêu đề phụ hài hước (`tieuDePhu`).
   - [CanhPhanUngCam.tsx](file:///e:/Video10P/src/canh/CanhPhanUngCam.tsx): cắt nhanh 1.5–2.5 giây cận mặt nhân vật phụ (`nhap_tra`, `nhuong_may`, `tron_mat`, `can_loi`) trên nền tia tốc độ phẳng kèm VFX hài và tem chữ.

3. **Mascot kênh cố định, Khung End-Screen 15s & Thumbnail ưu tiên ảnh AI**:
   - [mascot_kenh.ts](file:///e:/Video10P/src/nhanvat/mascot_kenh.ts) & `lay_ho_so_mascot_kenh()` trong [tao_kich_ban_10p.py](file:///e:/Video10P/scripts/pipeline/tao_kich_ban_10p.py): hồ sơ Mascot mặc định `mascot_pi` (*Giáo Sư Pi*, dễ tùy chỉnh tên/trang phục/màu áo qua `mascotKenh` hoặc `.env`), xuất hiện ở 15 giây Cold Open mở màn, cảnh đố `tuong_tac_khan_gia` và 15 giây End-Screen.
   - [CanhKet.tsx](file:///e:/Video10P/src/canh/CanhKet.tsx): nâng cấp cảnh `ket_thuc` (15 giây cuối) chừa sẵn 2 khung viền 16:9 đúng vùng chuẩn YouTube End-Screen (trái & phải) cùng mũi tên dẫn hướng từ Mascot ở giữa.
   - [Thumbnail.tsx](file:///e:/Video10P/src/Thumbnail.tsx) & `chuan_bi_phuong_an_thumbnail()`: ưu tiên lấy ảnh bối cảnh AI đẹp nhất của tập (`anhBoiCanh`) làm phông nền cho cả 3 biến thể A/B (fallback mượt về SVG khi không có ảnh AI).

4. **Prompt biên kịch `v3.5` & Tự động đăng YouTube cách 2 ngày**:
   - [tao_kich_ban_10p.py](file:///e:/Video10P/scripts/pipeline/tao_kich_ban_10p.py): nâng cấp prompt dùng **Cold Open 15 giây đầu**, **Open Loop cuối mỗi hồi (`openLoopCuoiHoi`)**, **ẩn dụ hiện đại hài hước**, `tamTrangNhac`, `ngatNhacPunchline`, Mascot & phân bổ hợp lý 3 khung hình mới; mở rộng Guardrail khóa dấu tiếng Việt bao phủ toàn bộ trường mới.
   - [dang_youtube.py](file:///e:/Video10P/scripts/pipeline/dang_youtube.py), [lay_refresh_token_youtube.py](file:///e:/Video10P/scripts/pipeline/lay_refresh_token_youtube.py) & [tu-dong-video10p.yml](file:///e:/Video10P/.github/workflows/tu-dong-video10p.yml): tự chạy cách 2 ngày (`cron: '0 0 */2 * *'`), Resumable Upload 8MB thuần stdlib, hẹn giờ công khai `publishAt` `+07:00` (hoặc `--chi-rieng-tu`), gắn `thumbnail_1.png`, tải `phu_de.srt` và lưu `youtubeVideoId` vào `du_lieu/bo_nho_hoc_hoi.json`.
