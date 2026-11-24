# Dự án Video Dài Người Que Kể Chuyện Lịch Sử Toán Học (`v0.1`)

Remotion `16:9` (`1920×1080`, `30fps`), TypeScript strict, tất định 100% theo `useCurrentFrame()`.

## Sơ đồ thư mục
```text
├── du_lieu/mau_pythagoras.json    # Dữ liệu mẫu 750 frames (25s), đủ 7 bố cục
├── public/{audio,sfx}/            # Thư mục âm thanh & SFX (chưa đặt mp3 ở v0.1)
├── scripts/test_khung.mjs         # Script kiểm tra schema, frame, xương khớp & luật cấm
└── src/
    ├── index.ts, Root.tsx         # Đăng ký Composition VideoDaiNguoiQue (calculateMetadata)
    ├── kieu_dai.ts                # Hợp đồng dữ liệu dùng chung cho v0.1 → v0.2+
    ├── VideoDai.tsx               # Điều phối Sequence, tiến độ chương, phụ đề 16:9, nền lưới
    ├── canh/                      # 7 bố cục cảnh (MoDau, KeChuyen, DoiThoai, HanhDong, GiaiThichToan, DongThoiGian, Ket)
    ├── daocu/                     # CongThucMath.tsx (KaTeX) & DaoCu.tsx (SVG)
    ├── amthanh/sfx.ts             # Bản đồ SFX (chặn render <Audio> khi chưa có file thật)
    ├── xuong/                     # [STUB v0.1] he_xuong.ts, dong_tac.ts
    ├── vfx/                       # [STUB v0.1] MayQuayDong.tsx, HieuUngTanCong.tsx
    └── nhanvat/NguoiQueDong.tsx   # [STUB v0.1] Vẽ người que cơ bản từ khung xương
```

## Luật cấm tuyệt đối
- **CẤM** `backdrop-filter: blur`, `filter: blur`, SVG `<filter>` blur (gây chậm render headless Chromium).
- **CẤM** `Math.random()` ở mọi nơi. Mọi chuyển động phải tất định theo `useCurrentFrame()`.
- Luôn dùng đường dẫn tương thích Windows, UTF-8, xuống dòng `LF`.

## Lệnh kiểm tra & chạy nhanh
- Kiểm tra TypeScript + schema + luật cấm: `npm run kiem-tra`
- Mở Remotion Studio: `npm run dev`
- Render video mẫu: `npm run render:mau`

## 3 phần cố tình giữ ở mức khung (`v0.1`) chờ nâng cấp `v0.2`
1. `src/xuong/` (`he_xuong.ts`, `dong_tac.ts`): mới chỉ trả tọa độ giữ chỗ nhún thở nhẹ; `v0.2` thay bằng hệ xương FK đầy đủ + keyframe 14 động tác.
2. `src/vfx/` (`MayQuayDong.tsx`, `HieuUngTanCong.tsx`): mới áp dụng `translate/scale` và vòng tròn kiểm chứng timing; `v0.2` bổ sung `cameraShake`, `hitstopFrames`, `impactFrame`, smear & VFX chiến đấu.
3. `src/nhanvat/NguoiQueDong.tsx`: mới vẽ nét người que cơ bản và biểu tượng vũ khí giữ chỗ; `v0.2` nâng cấp chi tiết vũ khí toán học, biểu cảm động & hiệu ứng năng lượng.
