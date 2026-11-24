# Trạng thái bàn giao tác vụ (AGENT.md)

## Mốc hiện tại: `v0.2` — Phim hoạt hình 2D kể chuyện Toán học (Thiên nhiên sống động, Diễn xuất hài hước & Bảng giảng Toán)
- Tái cấu trúc sạch `src/kieu_dai.ts` bỏ hoàn toàn phong cách chiến đấu, chuyển sang bộ kiểu phim hoạt hình kể chuyện Toán học (7 bố cục, 8 bối cảnh thiên nhiên, 7 thời tiết, 14 động tác diễn xuất/hài, 9 biểu cảm, 8 phụ kiện, 8 vật cầm tay, 8 hiệu ứng hoạt hình, 5 minh họa Toán, `loiBinhHaiHuoc`, `chuyenCanh`).
- Xây dựng `src/boicanh/BoiCanhHoatHinh.tsx`: 8 bối cảnh SVG `1920×1080` có chiều sâu 3 lớp, chuyển động tự nhiên theo `useCurrentFrame()` (mây trôi, sóng nước, quả táo rơi, lá đung đưa, sao băng...) và lớp phủ thời tiết tất định không blur, không `Math.random()`.
- Nâng cấp `src/xuong/he_xuong.ts`, `src/xuong/dong_tac.ts`, `src/nhanvat/NguoiQueDong.tsx`: chu kỳ đi bộ/chạy tự nhiên, 14 động tác diễn xuất & hài (`giat_minh_nhay_dung`, `bo_tay_can_loi`, `khoanh_tay_tu_man`, `sup_do_tuyet_vong`...), tự động nháy mắt tất định, 9 biểu cảm (gồm `can_loi_mat_do`), bóng đổ dưới chân, 8 phụ kiện và 8 vật cầm tay.
- Xây dựng `src/vfx/HieuUngHoatHinh.tsx` (8 hiệu ứng hài/kể chuyện), `src/vfx/MayQuayDong.tsx` (`pan_nhe`, `zoom_cham`, `zoom_hai_huoc`, chuyển cảnh `mo_dan`/`quet_ngang`/`vong_tron_hoat_hinh`) và `src/amthanh/sfx.ts` (bản đồ SFX hoạt hình an toàn).
- Cập nhật `src/daocu/MinhHoaToan.tsx`, `src/canh/KhungLoiBinhHaiHuoc.tsx`, đủ 7 cảnh (`CanhMoDau`, `CanhKeChuyen`, `CanhDoiThoai`, `CanhHaiHuoc`, `CanhGiaiThichToan`, `CanhDongThoiGian`, `CanhKet`) và `src/VideoDai.tsx`.
- Viết lại kịch bản mẫu `du_lieu/mau_pythagoras.json` (750 frames / 25s) và mở rộng `scripts/test_khung.mjs` kiểm chứng đầy đủ hợp đồng `v0.2`.

## Mốc tiếp theo: `v0.3` — Pipeline sản xuất phim hoạt hình Toán học dài >10 phút
- [ ] Viết pipeline Python chuyển kịch bản kể chuyện văn bản → JSON chuẩn `DuLieuVideoDai`.
- [ ] Tích hợp giọng đọc TTS xuất ra `public/audio/*.mp3` và tự căn chỉnh `tuFrame..denFrame` khớp lời thoại.
- [ ] Bổ sung file âm thanh hoạt hình (`pop.mp3`, `ding.mp3`, `boing.mp3`, `crickets.mp3`, `whoosh.mp3`, `dramatic.mp3`) vào `public/sfx/` và bật `DANH_SACH_SFX_CO_SAN`.
- [ ] Viết script render tách từng chương rồi ghép bằng FFmpeg cho video dài 10+ phút.
