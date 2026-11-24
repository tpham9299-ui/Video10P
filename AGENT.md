# Trạng thái bàn giao tác vụ (AGENT.md)

## Mốc hiện tại: `v0.1` — Đã hoàn thành khung sạch
- Khởi tạo dự án Remotion 16:9 (`1920×1080`, `30fps`, TypeScript `strict: true`).
- Khóa hợp đồng dữ liệu tại `src/kieu_dai.ts` (đủ 7 bố cục, 14 hành động, 6 vũ khí, 7 biểu cảm, 6 phụ kiện, 7 hiệu ứng tấn công, 7 đạo cụ).
- Hoàn thiện 7 cảnh trong `src/canh/`, điều phối `src/VideoDai.tsx`, `src/Root.tsx`, công thức KaTeX (`CongThucMath.tsx`), đạo cụ SVG (`DaoCu.tsx`) và bản đồ SFX an toàn (`src/amthanh/sfx.ts`).
- Tạo kịch bản mẫu `du_lieu/mau_pythagoras.json` (750 frames = 25s, 3 chương, đủ 7 bố cục) và kiểm tra tự động `scripts/test_khung.mjs`.

## Mốc tiếp theo: `v0.2` — Nâng cấp Xương khớp FK & VFX chiến đấu
- [ ] Xây dựng bộ giải FK (`src/xuong/he_xuong.ts`) theo chiều dài xương cố định + nội suy góc mượt.
- [ ] Điền đầy đủ keyframe cho 14 `LoaiHanhDong` trong `src/xuong/dong_tac.ts` (đặc biệt chuỗi đòn đánh nhiều pha: tích lực → ra đòn → hồi chiêu).
- [ ] Nâng cấp `src/vfx/MayQuayDong.tsx`: thêm `cameraShake` tất định, `theoDoiNhanVat`, `hitstopFrames` và `impactFrame` tương phản đen-trắng.
- [ ] Nâng cấp `src/vfx/HieuUngTanCong.tsx`: vẽ vệt chém smear đa giác, sóng xung kích, tia lửa va chạm, tia laser toán học, đường tốc độ, bụi đất (không dùng blur, không `Math.random()`).
- [ ] Nâng cấp `src/nhanvat/NguoiQueDong.tsx`: vẽ đầy đủ 5 vũ khí toán học và hoạt ảnh phụ kiện theo vận tốc.

## Mốc tương lai: `v0.3` — Pipeline Python kịch bản, TTS & render tách chương
- [ ] Viết pipeline Python chuyển kịch bản văn bản → JSON chuẩn `DuLieuVideoDai`.
- [ ] Tích hợp tạo giọng đọc TTS xuất ra `public/audio/*.mp3` và tự căn chỉnh `tuFrame..denFrame` theo độ dài audio.
- [ ] Bổ sung file SFX thật vào `public/sfx/` và bật `DANH_SACH_SFX_CO_SAN`.
- [ ] Viết script render tách từng chương rồi ghép bằng FFmpeg cho video dài 10+ phút.
