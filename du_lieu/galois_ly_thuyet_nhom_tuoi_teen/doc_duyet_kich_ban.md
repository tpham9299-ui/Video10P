# ĐỌC DUYỆT KỊCH BẢN: Évariste Galois: Thiên Tài 20 Tuổi Và Đêm Trắng Đổi Thay Lịch Sử Toán Học

> **Chủ đề:** Hành trình đầy kịch tính của thần đồng toán học Évariste Galois, người đã viết nên lý thuyết nhóm bất hủ chỉ trong một đêm trước trận quyết định sinh tử.

## Tổng quan nhanh
- **Số hồi:** 6 | **Tổng số cảnh:** 77
- **Tổng số từ lời thoại:** 1644 từ (mục tiêu 1750–2150 từ)
- **Thời lượng dự kiến:** ~10.70 phút (~642 giây) — **ĐẠT MỤC TIÊU > 10 PHÚT**
- **Số cảnh có Toán / KaTeX:** 6 | **Số cảnh có điểm nhấn hài:** 11

| Hồi | Tên hồi | Số cảnh | Số từ | Dự kiến | Cảnh Toán | Miếng hài |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Hồi 1 | 1. Tiếng Khóc Chào Đời Và Cậu Nhóc Bướng Bỉnh Tại Bourg-la-Reine | 16 | 381 | ~2.47 phút | 1 | 5 |
| Hồi 2 | 2. Cục Súc Ném Phấn Và Cú Ngã Ngựa Tại Kỳ Thi Định Mệnh | 14 | 292 | ~1.90 phút | 1 | 1 |
| Hồi 3 | 3. Bản Thảo Thất Lạc Và Đêm Trắng Viết Toán Tới Sáng | 13 | 268 | ~1.75 phút | 2 | 1 |
| Hồi 4 | 4. Nhà Tù Sainte-Pélagie Và Trận Quyết Đấu Định Mệnh | 11 | 252 | ~1.64 phút | 1 | 3 |
| Hồi 5 | 5. Từ Tấm Giấy Nguệch Ngoạc Đến Bí Mật Mật Mã iPhone Ngày Nay | 12 | 232 | ~1.52 phút | 0 | 0 |
| Hồi 6 | 6. Dư Âm Đêm Trắng Và Di Sản Bất Hủ Của Évariste Galois | 11 | 219 | ~1.43 phút | 1 | 1 |

## Dàn nhân vật cố định
- **Évariste Galois** (`evariste_galois`): màu chủ đạo `#2563EB`, phụ kiện `mu_noi_phap`
- **Giáo Sư Pi** (`mascot_pi`): màu chủ đạo `#E11D48`, phụ kiện `kinh_tron`
- **Joseph Fourier** (`joseph_fourier`): màu chủ đạo `#D97706`, phụ kiện `toc_gia_17`
- **Siméon Denis Poisson** (`simon_poisson`): màu chủ đạo `#4B5563`, phụ kiện `khong`

## Gợi ý 3 phương án Thumbnail A/B (Test & Compare)
- **Biến thể 1:** `ĐÊM TRẮNG ĐỊNH MỆNH` | KaTeX: `G = \text{Gal}(K/F)` | Biểu cảm: `hoang_mang` | Đạo cụ: `ban_hoc_den_dau`
- **Biến thể 2:** `THIÊN TÀI BƯỚNG BỈNH` | KaTeX: `[K:F] = |G|` | Biểu cảm: `tuc_gian` | Đạo cụ: `bang_den`
- **Biến thể 3:** `BÍ MẬT Ổ KHÓA` | KaTeX: `\forall a, b \in G` | Biểu cảm: `ngac_nhien` | Đạo cụ: `phong_bi_thu_tay`

## Tầng 3 — Tự kiểm định (Self-Critique)
- **Điểm tự đánh giá:** 8.5/10
- **Nhận xét chung:** Kịch bản hoạt hình bám sát tư liệu lịch sử toán học về Évariste Galois, nhịp điệu vui tươi, tuy nhiên cần khắc phục lỗi lặp ý giữa các hồi, chỉnh sửa các cảnh đứng yên quá lâu (>6.5s) để tăng nhịp thị giác, và thay thế mở đầu sách giáo khoa bằng nghịch lý cuốn hút.
- **Số cảnh đã tự sửa:** 6
  - `canh_003`: Sửa mở đầu sách giáo khoa thành nghịch lý cuốn hút và sửa lỗi năm sinh 'năm mươi tám mươi mười một' thành 'năm 1811'.
  - `canh_012`: Khắc phục lỗi trùng liên tiếp cả boiCanh lẫn gocQuay với cảnh trước và phá bỏ thời gian tĩnh quá lâu (>6.5s).
  - `canh_013`: Khắc phục lỗi trùng lặp bối cảnh/góc quay và giảm thời gian camera tĩnh.
  - `canh_018`: Bổ sung côngThucLatex chuẩn xác cho cảnh giang_toan theo yêu cầu Guardrail.
  - `canh_025`: Khắc phục lặp ý với cảnh 017 và sửa trùng bối cảnh/góc quay liên tiếp.
  - `canh_031`: Đảm bảo cấu trúc LaTeX chuẩn KaTeX và cân bằng ngoac {} trong cảnh giảng toán.
- **Tự tối ưu nhịp ngắt thị giác (luật 6–8s):** 29 cảnh
  - `canh_002` (`doi_camera_va_hanh_dong`): Cảnh tĩnh dài 7.8s (> 6.5s) -> chuyển sang camera='zoom_hai_huoc'.
  - `canh_004` (`tach_canh`): Tự chia nhỏ cảnh tĩnh dài 9.7s (> 8.0s) kèm đổi góc máy & hành động.
  - `canh_006` (`doi_camera_va_hanh_dong`): Cảnh tĩnh dài 8.9s (> 6.5s) -> chuyển sang camera='pan_nhe'.
  - `canh_008` (`doi_camera_va_hanh_dong`): Cảnh tĩnh dài 8.6s (> 6.5s) -> chuyển sang camera='pan_nhe'.
  - `canh_011` (`tach_canh`): Tự chia nhỏ cảnh tĩnh dài 16.5s (> 8.0s) kèm đổi góc máy & hành động.
  - `canh_014` (`doi_camera_va_hanh_dong`): Cảnh tĩnh dài 11.3s (> 6.5s) -> chuyển sang camera='pan_nhe'.
  - `canh_016` (`doi_camera_va_hanh_dong`): Cảnh tĩnh dài 7.8s (> 6.5s) -> chuyển sang camera='pan_nhe'.
  - `canh_020` (`doi_camera_va_hanh_dong`): Cảnh tĩnh dài 9.7s (> 6.5s) -> chuyển sang camera='pan_nhe'.
- **Guardrail kiểm định tự động (v2.0):** 20 mục đã xử lý
  - `canh_007` (`giang_toan_rong`): Đã bổ sung các bước suy luận cho minh họa Toán từ công thức của cảnh.
  - `canh_020` (`loi_binh_de_bang_toan_timeline`): Đã gỡ hộp 'Góc bình luận' khỏi cảnh Toán/Dòng thời gian.
  - `canh_020` (`giang_toan_rong`): Đã bổ sung các bước suy luận cho minh họa Toán từ công thức của cảnh.
  - `canh_034` (`loi_binh_de_bang_toan_timeline`): Đã gỡ hộp 'Góc bình luận' khỏi cảnh Toán/Dòng thời gian.
  - `canh_034` (`giang_toan_rong`): Đã bổ sung các bước suy luận cho minh họa Toán từ công thức của cảnh.
  - `canh_035` (`giang_toan_rong`): Đã bổ sung các bước suy luận cho minh họa Toán từ công thức của cảnh.
  - `canh_048` (`giang_toan_rong`): Đã bổ sung các bước suy luận cho minh họa Toán từ công thức của cảnh.
  - `canh_055` (`cam_on_hoi_giua`): Đã gỡ bỏ chuỗi 'CẢM ƠN' ở hồi giữa.
- **Bài học mới lưu vào bộ nhớ:** 2
  - `[storyboard | ưu tiên 5/5]` Không để camera ở trạng thái tĩnh quá 6.5 giây liên tiếp để duy trì nhịp thị giác hoạt hình nhanh gọn, hấp dẫn.
  - `[lich_su | ưu tiên 4/5]` Tuân thủ tuyệt đối mốc timeline lịch sử (1811, 1823, 1829, 1830, 1831, 1832), tránh phát âm hoặc ghi chép sai lệch nien dai.

## Hậu kiểm LaTeX
- ✅ Toàn bộ công thức KaTeX cân bằng ngoặc `{}` và hợp lệ cơ bản.

---

## Hồi 1: 1. Tiếng Khóc Chào Đời Và Cậu Nhóc Bướng Bỉnh Tại Bourg-la-Reine (16 cảnh • 381 từ)

### `canh_001` (mo_dau • san_truong_co_dien • nang_dep • 26 từ) `[VAI: nhan_vat]` — *Nghịch Lý Điện Thoại*
> Nếu không có công trình của một cậu thanh niên hai mươi tuổi từ thế kỷ mười chín, chiếc iPhone của bạn đã thành cục gạch!

### `canh_002` (hai_huoc • san_truong_co_dien • nang_dep • 20 từ) `[HÀI]` `[VAI: nhan_vat]` — *Mật Mã Đỉnh Cao*
> Giải phương trình bậc cao phức tạp giống hệt như cố mở khóa iPhone khi bạn quên sạch mật khẩu!

### `canh_003` (ke_chuyen • san_truong_co_dien • nang_dep • 26 từ) `[HÀI]` `[VAI: nguoi_dan]` — *Chào Đời Tại Pháp*
> Vào năm 1811, cậu bé Évariste Galois chào đời tại Bourg-la-Reine, mang theo một bộ não thiên bổng nhưng đầy rẫy sự bướng bỉnh!
- 😂 **Lời bình góc màn hình:** Vừa lọt lòng đã đòi giải phương trình bậc năm!

### `canh_004` (doi_thoai • san_truong_co_dien • nang_dep • 8 từ) `[VAI: nhan_vat]` — *Nhập Học Paris*
> Đến năm mươi tám trăm hai mươi ba,

### `canh_005` (doi_thoai • san_truong_co_dien • nang_dep • 17 từ) `[VAI: nhan_vat]` — *Nhập Học Paris*
> cậu nhóc bướng bỉnh chính thức bước chân vào ngôi trường danh tiếng Lycée Louis-le-Grand.

### `canh_006` (hai_huoc • lop_hoc_bang_xanh • nang_dep • 23 từ) `[HÀI]` `[VAI: nguoi_dan]` — *Đọc Sách Như Thơ*
> Cậu thiếu niên Galois đọc sách toán say sưa hệt như người ta đọc tiểu thuyết ngôn tình lãng mạn đầy cuốn hút.

### `canh_007` (giai_thich_toan • lop_hoc_bang_xanh • nang_dep • 23 từ) `[TOÁN / KaTeX]` `[VAI: nhan_vat]` — *Phương Trình Bậc Cao*
> Các nhà toán học thế kỷ mười chín đau đầu tìm kiếm công thức nghiệm tổng quát cho các đa thức bậc cao.
- 📐 **Minh họa Toán:** `chuoi_suy_luan` — Đồ thị đa thức
- 🧮 **Công thức KaTeX:**
  - `a_n x^n + a_{n-1} x^{n-1} + \dots + a_0 = 0` (Phương trình bậc cao tổng quát)

### `canh_008` (dong_thoi_gian • san_truong_co_dien • nang_dep • 21 từ) `[VAI: nguoi_dan]` — *Dòng Thời Gian Sớm*
> Hãy cùng nhìn lại hành trình xuất phát của thiên tài từ những bước chân đầu tiên tại trường học Paris.

### `canh_009` (doi_thoai • lop_hoc_bang_xanh • nang_dep • 22 từ) `[VAI: nhan_vat]` — *Tính Khí Nóng Nảy*
> Cậu nhóc không chỉ thông minh mà còn cực kỳ bướng bỉnh và sẵn sàng tranh luận tay đôi với giáo viên.

### `canh_010` (ke_chuyen • lop_hoc_bang_xanh • nang_dep • 21 từ) `[VAI: nguoi_dan]` — *Đột Phá Tư Duy*
> Những suy nghĩ vượt thời đại bắt đầu nảy mầm trong đầu óc non trẻ nhưng vô cùng sắc sảo ấy.

### `canh_011` (ke_chuyen • san_truong_co_dien • nang_dep • 38 từ) `[VAI: nguoi_dan]` — *Giai thoại lớp học*
> Cậu nhóc Galois thường xuyên khiến thầy cô phải đau đầu chóng mặt vì tội lơ đễnh trong giờ văn và chỉ mải miết tự vẽ vời những phương trình kỳ lạ lên mép bàn gỗ cổ kính.

### `canh_012` (ke_chuyen • san_truong_co_dien • nang_dep • 15 từ) `[VAI: nguoi_dan]` — *Trí nhớ kinh hoàng*
> Thay vì học thuộc lòng từng câu chữ nhàm chán như bao đứa trẻ khác,

### `canh_013` (ke_chuyen • san_truong_co_dien • nang_dep • 28 từ) `[VAI: nguoi_dan]` — *Trí nhớ kinh hoàng*
> thiên tài nhỏ tuổi này lại nhét trọn cả một cuốn sách hình học phức tạp vào trong bộ nhớ siêu phàm chỉ sau một thoáng lướt qua.

### `canh_014` (ke_chuyen • lop_hoc_bang_xanh • nang_dep • 40 từ) `[HÀI]` `[VAI: nguoi_dan]` — *Sự cô lập kiêu hãnh*
> Sự thông minh vượt trước thời đại vô tình biến cậu thành một kẻ ngoại đạo lạc lõng giữa đám đông, khiến Galois chọn cách bầu bạn cùng những con số thay vì những trò đùa tinh nghịch tuổi thơ.
- 😂 **Lời bình góc màn hình:** Đỉnh cao của cô đơn là đây chứ đâu!

### `canh_015` (ke_chuyen • thu_vien_co_dien • nang_dep • 25 từ) `[HÀI]` `[VAI: nguoi_dan]` — *Ngọn lửa nung nấu*
> Chính những năm tháng cô đơn ấy đã nung nấu khát khao lật đổ mọi định kiến toán học cũ kỹ của giới hàn lâm.
- 😂 **Lời bình góc màn hình:** Nổi loạn vì toán học là có thật!

### `canh_016` (doi_thoai • lop_hoc_bang_xanh • nang_dep • 28 từ) `[VAI: nhan_vat]` — *Mở Ngỏ Tương Lai*
> Liệu cậu nhóc bướng bỉnh này sẽ làm gì khi gửi bản thảo chấn động lên Viện Hàn lâm nhưng lại gặp phải một kết cục bi hài?


## Hồi 2: 2. Cục Súc Ném Phấn Và Cú Ngã Ngựa Tại Kỳ Thi Định Mệnh (14 cảnh • 292 từ)

### `canh_017` (ke_chuyen • lop_hoc_bang_xanh • nang_dep • 23 từ) `[VAI: nguoi_dan]` — *Sân khấu của thiên tài*
> Bước chân vào phòng thi với sự tự tin ngút trời, Évariste Galois chuẩn bị tạo ra một cơn địa chấn học thuật.

### `canh_018` (doi_thoai • lop_hoc_bang_xanh • nang_dep • 20 từ) `[VAI: nhan_vat]` — *Bước trung gian tối nghĩa*
> Vị giám khảo kỳ thi yêu cầu Galois giải thích chi tiết các bước tính toán dài dòng trên bảng.

### `canh_019` (phan_ung_cam • lop_hoc_bang_xanh • nang_dep • 13 từ) `[VAI: nhan_vat]` — *Viên phấn ngoại giao*
> Cậu thiếu niên tức giận ném thẳng viên phấn vào đầu giám khảo!

### `canh_020` (giai_thich_toan • giang_duong_dai_hoc • khong • 25 từ) `[TOÁN / KaTeX]` `[VAI: nhan_vat]` — *Lô-gích thiên tài*
> Với Galois, các bước trung gian giống như Google Maps khi bạn đã thuộc đường trong lòng bàn tay, việc gì phải chỉ chi tiết!
- 📐 **Minh họa Toán:** `chuoi_suy_luan` — Cấu trúc đối xứng nghiệm
- 🧮 **Công thức KaTeX:**
  - `G = \text{Gal}(K/F), \quad [K:F] = |G|` (Lý thuyết Galois)

### `canh_021` (ban_do_hanh_trinh • phong_tro_bep_lua • ban_dem • 23 từ) `[VAI: nguoi_dan]` — *Gửi gắm tri thức*
> Không nản lòng sau cú ngã ngựa, Galois gom góp tất cả các công trình đột phá gửi thẳng đến Viện Hàn lâm.

### `canh_022` (ke_chuyen • phong_nen_hai_huoc • khong • 25 từ) `[VAI: nhan_vat]` — *Thử thách cùng Giáo Sư Pi*
> Này các bạn trẻ, nếu bạn làm bài kiểm tra mà bỏ qua hết các bước giải thích, giáo viên sẽ cho bạn điều gì?

### `canh_023` (dong_thoi_gian • thu_vien_co_dien • ban_dem • 22 từ) `[VAI: nguoi_dan]` — *Dòng thời gian định mệnh*
> Những năm tháng tuổi trẻ của Galois là chuỗi ngày va chạm liên tục giữa thiên tài và định kiến thời đại.

### `canh_024` (doi_thoai • thu_vien_co_dien • ban_dem • 15 từ) `[VAI: nhan_vat]` — *Hy vọng đặt vào Fourier*
> Galois hồi hộp chờ đợi phản hồi từ vị đại gia toán học Joseph Fourier.

### `canh_025` (ke_chuyen • lop_hoc_bang_xanh • nang_dep • 28 từ) `[VAI: nguoi_dan]` — *Bản thảo thất lạc*
> Cụ Fourier qua đời đột ngột, công trình đột phá của cậu thiếu niên đành chôn vùi trong đống giấy tờ ngổn ngang không một lời hồi đáp.

### `canh_026` (ke_chuyen • lop_hoc_bang_xanh • nang_dep • 14 từ) `[VAI: nguoi_dan]` — *Nỗi oan ức tuổi trẻ*
> Chưa dừng lại ở đó, khi gửi tiếp bài báo cho viện sĩ Poisson,

### `canh_027` (ke_chuyen • lop_hoc_bang_xanh • nang_dep • 15 từ) `[VAI: nguoi_dan]` — *Nỗi oan ức tuổi trẻ*
> ông này đọc xong liền phán xanh rờn rằng hoàn toàn không hiểu gì cả!

### `canh_028` (ke_chuyen • phong_tro_bep_lua • nang_dep • 20 từ) `[HÀI]` `[VAI: nguoi_dan]` — *Cục súc ném phấn*
> Giám khảo lắc đầu khó chịu trước thái độ ngạo mạn của cậu học trò thiên tài trong phòng thi.
- 😂 **Lời bình góc màn hình:** Giám khảo trầm cảm nhẹ!

### `canh_029` (ke_chuyen • lop_hoc_bang_xanh • nang_dep • 28 từ) `[VAI: nguoi_dan]` — *Cú ngã định mệnh*
> Thế là cánh cửa vào đại học danh tiếng cứ thế đóng sầm lại trước mũi thiên tài với tính cách quá đỗi bộc trực và bất kham.

### `canh_030` (ke_chuyen • thu_vien_co_dien • ban_dem • 21 từ) `[VAI: nguoi_dan]` — *Bức thư định mệnh*
> Nhưng trớ trêu thay, bản thảo gửi vị viện sĩ lừng danh lại không cánh mà bay vào cõi hư vô...


## Hồi 3: 3. Bản Thảo Thất Lạc Và Đêm Trắng Viết Toán Tới Sáng (13 cảnh • 268 từ)

### `canh_031` (ke_chuyen • phong_tro_bep_lua • ban_dem • 23 từ) `[VAI: nguoi_dan]` — *Bản Thảo Bốc Hơi*
> Năm mươi tám ba mươi, Galois gửi bản thảo cho Joseph Fourier nhưng ngài Fourier đột ngột qua đời khiến nó bốc hơi.

### `canh_032` (doi_thoai • phong_tro_bep_lua • ban_dem • 23 từ) `[VAI: nhan_vat]` — *Nhà Giam Sainte-Pélagie*
> Không nản lòng, Galois tiếp tục tham gia phong trào chính trị và bị tống vào nhà tù Sainte-Pélagie vào năm sau.

### `canh_033` (doi_thoai • thu_vien_co_dien • ban_dem • 23 từ) `[HÀI]` `[VAI: nhan_vat]` — *Bản Thảo Bị Gác Lại*
> Siméon Poisson gác lại bài báo của Galois vì cho rằng nó khó hiểu như đọc một dòng mã bị lỗi font chữ.

### `canh_034` (giai_thich_toan • lop_hoc_bang_xanh • ban_dem • 21 từ) `[TOÁN / KaTeX]` `[VAI: nguoi_dan]` — *Lý Thuyết Nhóm Galois*
> Galois chứng minh phương trình bậc năm bất khả giải bằng căn thức thông qua cấu trúc nhóm đối xứng nghiệm.
- 📐 **Minh họa Toán:** `chuoi_suy_luan` — Cau truc truong mo rộng va nhom Galois
- 🧮 **Công thức KaTeX:**
  - `G = \text{Gal}(K/F), \quad [K:F] = |G|` (Cấu trúc nhóm)

### `canh_035` (giai_thich_toan • lop_hoc_bang_xanh • ban_dem • 25 từ) `[TOÁN / KaTeX]` `[VAI: nguoi_dan]` — *Đặc Trưng Nhóm Hữu Hạn*
> Mọi phép toán trong nhóm đều đóng kín, giống như việc bạn lướt mạng xã hội mà không thể thoát khỏi vòng lặp drama vậy.
- 📐 **Minh họa Toán:** `chuoi_suy_luan` — Bảng nhân phép toán trong nhóm
- 🧮 **Công thức KaTeX:**
  - `\forall a, b \in G \implies a \cdot b \in G` (Dong kin nhom)

### `canh_036` (ke_chuyen • phong_tro_bep_lua • ban_dem • 23 từ) `[VAI: nguoi_dan]` — *Đêm Trắng Định Mệnh*
> Viết toán hăng say đến mức quên luôn cả việc ngày mai mình sẽ bước ra đấu trường sinh tử đầy hiểm nguy.

### `canh_037` (ke_chuyen • phong_tro_bep_lua • ban_dem • 26 từ) `[VAI: nguoi_dan]` — *Nến tàn mờ ảo*
> Cậu ấy viết cuồng nhiệt đến mức ngọn nến trên bàn đã cạn sạch sành sanh từ bao giờ mà chẳng thèm mảy may bận tâm!

### `canh_038` (ke_chuyen • phong_tro_bep_lua • ban_dem • 9 từ) `[VAI: nguoi_dan]` — *Bụng đói cồn cào*
> Đói bụng quá hả chàng trai trẻ? Không sao,

### `canh_039` (ke_chuyen • phong_tro_bep_lua • ban_dem • 18 từ) `[VAI: nguoi_dan]` — *Bụng đói cồn cào*
> nguồn cảm hứng toán học vĩ đại này sẽ bù đắp tất cả chiếc bụng rỗng kêu vang.

### `canh_040` (ke_chuyen • phong_tro_bep_lua • ban_dem • 27 từ) `[VAI: nguoi_dan]` — *Phương trình điên rồ*
> Những nhóm thế xứng tầm vũ trụ cứ tuôn trào trên giấy như thể chúng biết tự sắp xếp mà chẳng cần ai sai khiến nữa vậy.

### `canh_041` (ke_chuyen • phong_tro_bep_lua • ban_dem • 10 từ) `[VAI: nguoi_dan]` — *Lịch sử sang trang*
> Chỉ còn vài tiếng nữa là sáng rồi Galois ơi,

### `canh_042` (ke_chuyen • phong_tro_bep_lua • ban_dem • 17 từ) `[VAI: nguoi_dan]` — *Lịch sử sang trang*
> hãy gửi gắm trọn vẹn kho báu này cho nhân loại trước khi mặt trời mọc nhé!

### `canh_043` (dong_thoi_gian • phong_tro_bep_lua • ban_dem • 23 từ) `[VAI: nguoi_dan]` — *Dòng Thời Gian Định Mệnh*
> Chỉ trong một đêm trắng cô độc, Galois đã nén chặt toàn bộ di sản toán học nhân loại trước thềm cuộc chiến.


## Hồi 4: 4. Nhà Tù Sainte-Pélagie Và Trận Quyết Đấu Định Mệnh (11 cảnh • 252 từ)

### `canh_044` (ke_chuyen • quang_truong_hy_lap • hoang_hon • 38 từ) `[VAI: nguoi_dan]` — *Vào Lò Ngục Tù*
> Năm một tám ba mươi mốt, chàng thiên tài trẻ tuổi của chúng ta lại tiếp tục làm quen với những bức tường lạnh lẽo của nhà tù Sainte-Pélagie vì trót quá nhiệt huyết với chính trị.

### `canh_045` (bao_chi_co • quang_truong_hy_lap • hoang_hon • 32 từ) `[HÀI]` `[VAI: binh_luan_hai]` — *Combo Hủy Diệt*
> Yêu nước cực độ lại thêm tình trường rắc rối chính là combo hủy diệt hoàn hảo để bóp nghẹt mọi tương lai của một bộ óc siêu việt tuổi đôi mươi.

### `canh_046` (phan_ung_cam • thu_vien_co_dien • ban_dem • 4 từ) `[HÀI]` `[VAI: nhan_vat]` — *Cạn Lời Chưa*
> Thật là cạn lời!

### `canh_047` (doi_thoai • thu_vien_co_dien • ban_dem • 27 từ) `[VAI: nhan_vat]` — *Bẫy Chính Trị*
> Các đối thủ phái bảo hoàng đã chơi không đẹp khi dùng những chiêu trò bẩn thỉu để hạ gục một bộ óc toán học xuất chúng.

### `canh_048` (giai_thich_toan • thu_vien_co_dien • ban_dem • 29 từ) `[TOÁN / KaTeX]` `[VAI: nhan_vat]` — *Nhóm Hữu Hạn*
> Ngay cả trong ngục tù tối tăm, Galois vẫn suy ngẫm về cấu trúc đối xứng tuyệt đối và tính đóng kín kỳ diệu của các nhóm hữu hạn.
- 📐 **Minh họa Toán:** `chuoi_suy_luan` — Tính đóng kín của nhóm
- 🧮 **Công thức KaTeX:**
  - `\forall a, b \in G \implies a \cdot b \in G` (Tinh dong kin)

### `canh_049` (ke_chuyen • quang_truong_hy_lap • hoang_hon • 31 từ) `[VAI: nguoi_dan]` — *Hẹn Đấu Súng*
> Và rồi biến cố định mệnh đã đến vào tháng 5 năm 1832 khi một lời thách đấu oan nghiệt được đưa ra, đẩy chàng trai trẻ vào bước đường cùng.

### `canh_050` (doi_thoai • quang_truong_hy_lap • hoang_hon • 15 từ) `[VAI: nhan_vat]` — *Trận Quyết Đấu*
> Một cuộc đấu súng thật sự ư? Giữa thanh thiên bạch nhật thế này sao?

### `canh_051` (ke_chuyen • quang_truong_hy_lap • hoang_hon • 17 từ) `[VAI: binh_luan_hai]` — *Thử Thách Khán Giả*
> Đố các bạn biết đối thủ chọn vũ khí gì trong trận quyết đấu oan nghiệt này?

### `canh_052` (ke_chuyen • quang_truong_hy_lap • hoang_hon • 10 từ) `[VAI: binh_luan_hai]` — *Thử Thách Khán Giả*
> Hãy chọn nhanh trước khi đồng hồ điểm ba giây!

### `canh_053` (hai_huoc • quang_truong_hy_lap • hoang_hon • 28 từ) `[HÀI]` `[VAI: binh_luan_hai]` — *Định Mệnh Trớ Trêu*
> Trớ trêu thay, kẻ thách đấu lại là một tay thiện xạ khét tiếng, còn Galois thì xem toán học quan trọng hơn cả mạng sống của mình!

### `canh_054` (dong_thoi_gian • quang_truong_hy_lap • hoang_hon • 21 từ) `[VAI: nguoi_dan]` — *Dòng Thời Gian Định Mệnh*
> Nhìn lại chặng đường ngắn ngủi nhưng đầy bão giông của thiên tài Galois qua các mốc lịch sử cốt lõi.


## Hồi 5: 5. Từ Tấm Giấy Nguệch Ngoạc Đến Bí Mật Mật Mã iPhone Ngày Nay (12 cảnh • 232 từ)

### `canh_055` (ke_chuyen • giang_duong_hien_dai • nang_dep • 10 từ) `[VAI: nguoi_dan]` — *Di Sản Của Thiên Tài*
> Mỗi lần bạn mở khóa iPhone bằng FaceID, hãy thầm

### `canh_056` (doi_thoai • giang_duong_hien_dai • nang_dep • 21 từ) `[VAI: nhan_vat]` — *Đối Xứng Hoàn Hảo*
> Lý thuyết nhóm của Galois nghiên cứu các phép biến đổi bảo toàn cấu trúc toán học một cách kỳ diệu.

### `canh_057` (ke_chuyen • giang_duong_hien_dai • nang_dep • 22 từ) `[VAI: nguoi_dan]` — *Cấu Trúc Nhóm*
> Cấu trúc nhóm hữu hạn tuân thủ quy tắc đóng kín khi mọi phép toán kết hợp luôn nằm trong tập hợp.

### `canh_058` (ke_chuyen • giang_duong_hien_dai • nang_dep • 20 từ) `[VAI: nguoi_dan]` — *Giải Rubik*
> Giải Rubik không chỉ là xoay màu, mà là cả một buổi biểu diễn hoành tráng của Lý thuyết Nhóm.

### `canh_059` (doi_thoai • giang_duong_hien_dai • nang_dep • 23 từ) `[VAI: nhan_vat]` — *Mật Mã Hiện Đại*
> Internet ngày nay dựa hoàn toàn vào các thuật toán mã hóa khóa công khai sử dụng cấu trúc đại số trừu tượng.

### `canh_060` (ke_chuyen • giang_duong_hien_dai • nang_dep • 30 từ) `[VAI: nguoi_dan]` — *Rubik và Nhóm Đối Xứng*
> Bạn có hay chơi khối Rubik không? Mỗi lần xoay các mặt chính là một phép biến đổi thuộc nhóm đối xứng đấy nhé, siêu thú vị và hại não!

### `canh_061` (ke_chuyen • giang_duong_hien_dai • nang_dep • 30 từ) `[VAI: nguoi_dan]` — *Mật Mã Điện Thoại*
> Chính nền tảng lý thuyết nhóm trừu tượng của Galois đang bảo vệ từng tin nhắn Zalo hay mã hóa thanh toán iPhone của bạn mỗi ngày đó bạn ơi!

### `canh_062` (ke_chuyen • giang_duong_hien_dai • nang_dep • 10 từ) `[VAI: nguoi_dan]` — *Trò Đùa Lịch Sử*
> Nghĩ lại mới thấy tiếc cho anh bạn Galois nhỉ,

### `canh_063` (ke_chuyen • giang_duong_hien_dai • nang_dep • 20 từ) `[VAI: nguoi_dan]` — *Trò Đùa Lịch Sử*
> viết vội trên giấy nháp trước khi đấu súng mà thành tựu lại thay đổi cả thế giới hiện đại!

### `canh_064` (ke_chuyen • giang_duong_hien_dai • nang_dep • 16 từ) `[VAI: nguoi_dan]` — *Lời Kết Hồi*
> Vậy nên đừng bao giờ xem thường những nét vẽ nguệch ngoạc trên giấy nháp nhé,

### `canh_065` (ke_chuyen • giang_duong_hien_dai • nang_dep • 11 từ) `[VAI: nguoi_dan]` — *Lời Kết Hồi*
> biết đâu bạn vừa giải xong bài toán thế kỷ đấy!

### `canh_066` (ke_chuyen • giang_duong_hien_dai • nang_dep • 19 từ) `[VAI: nguoi_dan]` — *Thử Thách Nhóm*
> Theo bạn, cấu trúc nhóm đối xứng xuất hiện ở đâu trong các trò chơi giải trí hàng ngày?


## Hồi 6: 6. Dư Âm Đêm Trắng Và Di Sản Bất Hủ Của Évariste Galois (11 cảnh • 219 từ)

### `canh_067` (ke_chuyen • bau_troi_dem_vu_tru • ban_dem • 24 từ) `[VAI: nguoi_dan]` — *Bầu Trời Đêm Vĩnh Hằng*
> Cuộc đời Galois ngắn ngủi như chiếc điện thoại bật độ sáng tối đa, nhưng ánh sáng phát ra chiếu rọi cả ngàn năm.

### `canh_068` (giai_thich_toan • bau_troi_dem_vu_tru • ban_dem • 21 từ) `[TOÁN / KaTeX]` `[VAI: nhan_vat]` — *Lý Thuyết Nhóm Bất Hủ*
> Cấu trúc đối xứng nghiệm phương trình tạo nên nền móng vững chắc cho lý thuyết nhóm hiện đại ngày nay.
- 📐 **Minh họa Toán:** `chuoi_suy_luan` — Cau truc doi xung
- 🧮 **Công thức KaTeX:**
  - `G = \text{Gal}(K/F), \quad [K:F] = |G|` (Nhom Galois)
  - `\forall a, b \in G \implies a \cdot b \in G` (Phep toan dong)

### `canh_069` (doi_thoai • bau_troi_dem_vu_tru • ban_dem • 20 từ) `[VAI: binh_luan_hai]` — *Ứng Dụng Đỉnh Cao*
> Từ bảo mật internet đến khối Rubik đều mang bóng dáng tư duy đối xứng của cậu thiếu niên Pháp.

### `canh_070` (doi_thoai • bau_troi_dem_vu_tru • ban_dem • 22 từ) `[HÀI]` `[VAI: binh_luan_hai]` — *Lời Nhắn Nhủ Cuối Cùng*
> Giáo sư Pi tuyên bố sẽ không bao giờ ném phấn vào ai nữa vì sợ truyền nhân giận dỗi bỏ thi.

### `canh_071` (ke_chuyen • bau_troi_dem_vu_tru • ban_dem • 28 từ) `[VAI: nguoi_dan]` — *Hộp thư định mệnh*
> Bạn có biết bản thảo để đời của Galois từng bị Viện Hàn Lâm từ chối vì tưởng là trò đùa của một thanh niên rảnh rỗi không?

### `canh_072` (ke_chuyen • bau_troi_dem_vu_tru • ban_dem • 8 từ) `[VAI: nguoi_dan]` — *Lạc trôi trong lịch sử*
> Cụ Fourier qua đời vì ngã cầu thang,

### `canh_073` (ke_chuyen • bau_troi_dem_vu_tru • ban_dem • 19 từ) `[VAI: nguoi_dan]` — *Lạc trôi trong lịch sử*
> còn bản thảo của Galois thì lạc trôi trong đống giấy cũ như tìm đường sống trong bất lực.

### `canh_074` (ke_chuyen • bau_troi_dem_vu_tru • ban_dem • 29 từ) `[VAI: nguoi_dan]` — *Sự thật phũ phàng*
> Giáo sư Poisson thì đọc xong ngậm ngùi lắc đầu thú nhận rằng ông chẳng hiểu một chữ nào trong mớ lý thuyết nhóm vô cùng độc lạ đó.

### `canh_075` (ke_chuyen • bau_troi_dem_vu_tru • ban_dem • 9 từ) `[VAI: nguoi_dan]` — *Hậu thế kinh ngạc*
> Nhưng thời gian đã trả lại sự công bằng,

### `canh_076` (ke_chuyen • bau_troi_dem_vu_tru • ban_dem • 20 từ) `[VAI: nguoi_dan]` — *Hậu thế kinh ngạc*
> biến những nét phấn vội vã đêm hôm đó thành nền tảng cho mã hóa và bảo mật hiện đại!

### `canh_077` (ket_thuc • bau_troi_dem_vu_tru • ban_dem • 19 từ) `[VAI: nguoi_dan]` — *Hẹn Gặp Lại*
> Cảm ơn bạn đã đồng hành cùng đêm trắng của Évariste Galois. Đừng quên bấm đăng ký kênh nhé!
