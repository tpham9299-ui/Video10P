# Trạng thái bàn giao tác vụ (AGENT.md)

## Mốc hiện tại: `v2.0` — Hệ thống hoạt hình kể chuyện lịch sử Toán học điện ảnh, tương tác đa giọng & tự vận hành hằng ngày trên GitHub Actions

Toàn bộ 6 bước nâng cấp `v2.0` đã hoàn thiện và kiểm định end-to-end 100%:

1. **Bước 1/6 — Dọn sạch lỗi hardcode, banner kết thúc sớm & khung hình đen**:
   - Xóa sạch toàn bộ dữ liệu fallback hardcode của tập Pythagoras trong `src/canh/`, `src/daocu/MinhHoaToan.tsx` và [minh_hoa_hop_le.ts](file:///e:/Video10P/src/daocu/minh_hoa_hop_le.ts); render khung trống sạch hoặc báo lỗi schema rõ ràng khi thiếu dữ liệu.
   - Giới hạn banner kết thúc (`boCuc="ket_thuc"`) duy nhất ở cảnh cuối cùng của hồi cuối cùng toàn tập ([VideoDai.tsx](file:///e:/Video10P/src/VideoDai.tsx), [dieu_phoi_canh.ts](file:///e:/Video10P/src/canh/dieu_phoi_canh.ts), [chuanbi_dai.py](file:///e:/Video10P/scripts/pipeline/chuanbi_dai.py), [render_dai.py](file:///e:/Video10P/scripts/pipeline/render_dai.py)).
   - Xóa sạch gap frame giữa các `<Sequence>`, đảm bảo liền mạch tuyệt đối từ frame 0 đến frame cuối.
   - Hộp nhãn tên nhân vật tự co giãn theo độ dài chuỗi ([ten_nhan_vat.ts](file:///e:/Video10P/src/nhanvat/ten_nhan_vat.ts), [NguoiQueDong.tsx](file:///e:/Video10P/src/nhanvat/NguoiQueDong.tsx)) — không cắt tên dài như `"Srinivasa Ramanujan"`.
   - Khóa góc xoay đầu/cổ an toàn trong [he_xuong.ts](file:///e:/Video10P/src/xuong/he_xuong.ts) & [dong_tac.ts](file:///e:/Video10P/src/xuong/dong_tac.ts) trên cả 20 động tác FK.

2. **Bước 2/6 — Đạo diễn Camera 8 góc quay, Diễn xuất đa độ tuổi/tư thế & Tương tác khán giả**:
   - Nâng cấp máy quay đạo diễn [MayQuayDong.tsx](file:///e:/Video10P/src/vfx/MayQuayDong.tsx) hỗ trợ 8 `gocQuay` (`toan_canh`, `trung_canh`, `can_mat`, `focus_trai`, `focus_phai`, `zoom_dao_cu`, `pan_ngang`, `chia_doi_man_hinh`) + `tuDongFocusNguoiNoi` (tự lia & zoom 1.2x–1.45x bám đúng nhân vật đang nói theo `luotThoai[]` / RMS).
   - Mở rộng nhân vật hỗ trợ 4 `doTuoi` (`so_sinh`, `thieu_nien`, `truong_thanh`, `gia`), 5 `tuThe` (`dung`, `ngoi_ban`, `nam_giuong`, `om_em_be`, `mac_ao_khoac`), 6 động tác tương tác mới (tổng 20 `LoaiHanhDong`), `bieuCamTheoMoc[]`, `tuongTacVoi`.
   - Thêm cảnh tương tác khán giả đếm ngược 3 giây ([CanhTuongTacKhanGia.tsx](file:///e:/Video10P/src/canh/CanhTuongTacKhanGia.tsx)) và bố cục chia đôi màn hình ([CanhChiaDoiManHinh.tsx](file:///e:/Video10P/src/canh/CanhChiaDoiManHinh.tsx)).

3. **Bước 3/6 — 22 Bối cảnh 3 lớp Parallax, Thế giới sống động tất định & Tối ưu SVG `React.memo`**:
   - Mở rộng kho bối cảnh lên **22 bối cảnh** (12 cũ + 10 bối cảnh đời thường/lịch sử mới trong [BoiCanhMoi.tsx](file:///e:/Video10P/src/boicanh/BoiCanhMoi.tsx)), bọc toàn bộ nền tĩnh bằng `React.memo` cho tốc độ render CI cao, 100% vector SVG phẳng không blur.
   - Tạo lớp thế giới sống động tất định [SinhVatVaMoiTruong.tsx](file:///e:/Video10P/src/boicanh/SinhVatVaMoiTruong.tsx) với 10 vật thể/sinh vật (`chim_hai_au`, `chim_san_truong`, `ca_gon_song`, `buom_vuon`, `hoi_khoi`, `ngon_nen_den_dau`, `la_vang_gio`, `tuyet_cua_so`, `xe_taxi_co` gắn `bienSoXe` động từ JSON, `dong_ho_qua_lac`).
   - Mở rộng [DaoCu.tsx](file:///e:/Video10P/src/daocu/DaoCu.tsx) lên **20 đạo cụ** (+9 đạo cụ kể chuyện mới) và tham số hóa 100% [MinhHoaToan.tsx](file:///e:/Video10P/src/daocu/MinhHoaToan.tsx) từ JSON (`buoc[]`, trục tọa độ, màu nhấn).

4. **Bước 4/6 — Chuỗi AI 2 vai, Guardrail tự động, Từ điển phát âm & Hội thoại đa giọng**:
   - [san_tim_chu_de.py](file:///e:/Video10P/scripts/pipeline/san_tim_chu_de.py): xuất thêm `timeline_su_kien[]`, `tu_dien_phat_am{}` và `goi_y_boi_canh_va_dao_cu[]` vào `tu_lieu_nghien_cuu.json`; tự săn 6 chủ đề giàu giai thoại khi hàng đợi `< 3`.
   - [tao_kich_ban_10p.py](file:///e:/Video10P/scripts/pipeline/tao_kich_ban_10p.py): prompt 2 vai (**Biên kịch kể chuyện** + **Đạo diễn Storyboard**), khớp 1-1 beat câu chuyện, chống lặp ý giữa các hồi và bộ **Guardrail Python** (`kiem_dinh_guardrail_kich_ban`, `sua_loi_guardrail_cuc_bo`) kiểm định + sửa cục bộ 4 luật cứng (không trùng liên tiếp `boiCanh + gocQuay`, cấm rỗng `giang_toan`/`timeline`, cấm `"CẢM ƠN"` ở hồi giữa, ≥25% đối thoại/tương tác & ≥6 bối cảnh).
   - [chuan_hoa_doc_toan.py](file:///e:/Video10P/scripts/pipeline/chuan_hoa_doc_toan.py) & [chuanbi_dai.py](file:///e:/Video10P/scripts/pipeline/chuanbi_dai.py): tự nạp `tu_dien_phat_am` trước Edge TTS (giữ chính tả gốc đẹp cho phụ đề & `.srt`), phân giọng riêng cho Người dẫn chuyện và từng Nhân vật trong `luotThoai[]`, tính RMS 30fps & lưu chính xác `batDauFrame`/`ketThucFrame` từng lượt thoại.

5. **Bước 5/6 & Tự động hằng ngày — Chunking thông minh, CI chống OOM/Timeout & Lịch chạy 07:00 VN**:
   - [render_dai.py](file:///e:/Video10P/scripts/pipeline/render_dai.py) & [san_xuat_lien_tuc.py](file:///e:/Video10P/scripts/pipeline/san_xuat_lien_tuc.py): tự động chia nhỏ hồi dài `> 120s` thành 2 mảnh cân bằng (`--chi-render-chunk`, giữ tương thích ngược `--chi-render-hoi`), tự nhận diện `CI=true` áp dụng `--concurrency=2 --jpeg-quality=85 --log=warn` và `NODE_OPTIONS=--max-old-space-size=4096`, trích 18 khung Visual QA bằng fast keyframe seek FFmpeg.
   - [.github/workflows/tu-dong-video10p.yml](file:///e:/Video10P/.github/workflows/tu-dong-video10p.yml): lịch chạy tự động `0 0 * * *` (**07:00 sáng hằng ngày giờ Việt Nam UTC+7**), `permissions: contents: write`, `concurrency` theo workflow (`cancel-in-progress: false`), `timeout-minutes` (25/35/25), `strategy.fail-fast: false`, `max-parallel: 8`, cache `node_modules` + Chromium + pip, artifact trung gian `retention-days: 1` / sản phẩm cuối `retention-days: 14`, hoàn tất xóa chủ đề khỏi hàng đợi & `git pull --rebase origin main` trước khi push. `YOUTUBE_API_KEY` hoàn toàn tùy chọn.

6. **Bước 6/6 — Kịch bản mẫu v2.0 & Kiểm định tổng thể End-to-End**:
   - Bổ sung kịch bản mẫu tương tác [mau_v2_tuong_tac.json](file:///e:/Video10P/du_lieu/mau_v2_tuong_tac.json) (giữ nguyên tương thích [mau_pythagoras.json](file:///e:/Video10P/du_lieu/mau_pythagoras.json)).
   - Xác nhận pass 100%: `npm run kiem-tra:all`, `npm run render:mau`, render Still `ThumbnailToanHoc`, kiểm định cú pháp YAML workflow, và quét sạch `Math.random()` / `blur` / hardcode Pythagoras / API key.
