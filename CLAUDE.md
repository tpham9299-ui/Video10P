# Dự án Phim Hoạt Hình 2D Kể Chuyện Toán Học (`v0.2`)

Remotion `16:9` (`1920×1080`, `30fps`), TypeScript strict, phong cách phim hoạt hình 2D tươi sáng/điện ảnh, dí dỏm và tất định 100% theo `useCurrentFrame()`.

## Sơ đồ thư mục
```text
├── du_lieu/mau_pythagoras.json       # Kịch bản mẫu 750 frames (25s), đủ 7 bố cục + hài hước + bảng giảng Toán
├── public/{audio,sfx}/               # Thư mục âm thanh & SFX hoạt hình (chưa đặt mp3 ở v0.2)
├── scripts/test_khung.mjs            # Kiểm tra schema v0.2, 14 động tác tất định, hàm băm & luật cấm
└── src/
    ├── index.ts, Root.tsx            # Đăng ký Composition VideoDaiNguoiQue (calculateMetadata)
    ├── kieu_dai.ts                   # Hợp đồng dữ liệu v0.2 cho phim hoạt hình kể chuyện Toán học
    ├── VideoDai.tsx                  # Điều phối Sequence, tiến độ chương, phụ đề 16:9 dễ đọc mọi nền
    ├── boicanh/BoiCanhHoatHinh.tsx   # 8 bối cảnh thiên nhiên/cảnh vật SVG 3 lớp động + 7 lớp thời tiết
    ├── canh/                         # 7 bố cục cảnh (MoDau, KeChuyen, DoiThoai, HaiHuoc, GiaiThichToan, DongThoiGian, Ket) + KhungLoiBinhHaiHuoc
    ├── daocu/                        # CongThucMath.tsx (KaTeX), DaoCu.tsx (SVG), MinhHoaToan.tsx (5 dạng động)
    ├── amthanh/sfx.ts                # Bản đồ SFX hoạt hình (chặn render <Audio> khi chưa có file thật)
    ├── xuong/                        # he_xuong.ts (14 động tác diễn xuất/hài), dong_tac.ts
    ├── vfx/                          # tat_dinh.ts, MayQuayDong.tsx (pan/zoom_cham/zoom_hai_huoc + 3 chuyển cảnh), HieuUngHoatHinh.tsx (8 VFX)
    └── nhanvat/NguoiQueDong.tsx      # Nhân vật hoạt hình có nháy mắt tự động, 9 biểu cảm, bóng đổ elip, 8 phụ kiện & 8 vật cầm tay
```

## Luật cấm tuyệt đối
- **CẤM** `backdrop-filter: blur`, `filter: blur`, SVG `<filter>` blur (gây chậm render headless Chromium).
- **CẤM** `Math.random()` ở mọi nơi. Toàn bộ mây trôi, sóng nước, lá rơi, mưa/tuyết, chim bay, nháy mắt và hiệu ứng hài phải tất định 100% theo `useCurrentFrame()` + seed cố định (`bamTatDinh`).
- Luôn dùng đường dẫn tương thích Windows, UTF-8, xuống dòng `LF`.

## Lệnh kiểm tra & chạy nhanh
- Kiểm tra TypeScript + schema + xương khớp + luật cấm: `npm run kiem-tra`
- Mở Remotion Studio: `npm run dev`
- Render video mẫu: `npm run render:mau`

## Đã hoàn thành ở `v0.2`
1. **8 Bối cảnh hoạt hình 3 lớp & Thời tiết tất định** (`BoiCanhHoatHinh.tsx`): `bo_bien_hy_lap`, `vuon_tao_dong_que`, `pho_co_chau_au`, `rung_nui_thien_nhien`, `thu_vien_co_dien`, `lop_hoc_bang_xanh`, `bau_troi_dem_vu_tru`, `phong_nen_hai_huoc` kèm `nang_dep`, `hoang_hon`, `ban_dem`, `mua_nhe`, `la_roi`, `tuyet_roi`.
2. **Nhân vật diễn xuất có hồn** (`he_xuong.ts`, `dong_tac.ts`, `NguoiQueDong.tsx`): 14 động tác diễn xuất/hài hước, nháy mắt tự động mỗi ~95 frame, 9 biểu cảm sắc nét (gồm `can_loi_mat_do` mắt `— —` và `tu_man`), bóng đổ dưới chân, 8 phụ kiện và 8 vật cầm tay.
3. **VFX Hài hước, Camera điện ảnh & Sân khấu giảng Toán** (`HieuUngHoatHinh.tsx`, `MayQuayDong.tsx`, `MinhHoaToan.tsx`, `src/canh/`): 8 hiệu ứng kể chuyện/hài, `pan_nhe`/`zoom_cham`/`zoom_hai_huoc`, chuyển cảnh `vong_tron_hoat_hinh`, khung `loiBinhHaiHuoc` góc màn hình và bảng xanh giảng Toán kết hợp KaTeX + 5 minh họa hình học động.
