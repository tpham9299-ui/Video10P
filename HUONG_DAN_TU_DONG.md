# Hướng Dẫn Vận Hành Hệ Thống AI Tự Chủ (`v0.5`)

Hệ thống `Video10P v0.5` cho phép AI **tự tìm kiếm & kiểm chứng tư liệu trên mạng**, **tự học hỏi qua bộ nhớ bền vững** (`du_lieu/bo_nho_hoc_hoi.json`), **tự biên kịch + tự kiểm định Toán học/LaTeX/nhịp hài**, và **tự sản xuất liên tục phim hoạt hình lịch sử Toán học dài > 10 phút (> 600 giây)** cả trên máy cục bộ lẫn tự động theo lịch trên GitHub Actions.

---

## 1. Chuẩn bị môi trường cục bộ

1. Cài đặt phụ thuộc Node.js và Python (Windows luôn chạy Python với `-X utf8`):
   ```bash
   npm ci
   pip install -r requirements.txt
   ```
2. Đảm bảo đã cài **FFmpeg** (có cả `ffmpeg` và `ffprobe` trong `PATH`).
3. Sao chép `.env.example` thành `.env` và điền danh sách nhiều API key Gemini (tách nhau bằng dấu phẩy để tự xoay vòng khi gặp `429`/`503`):
   ```env
   GEMINI_API_KEYS=key_1,key_2,key_3
   GEMINI_MODEL=gemini-flash-latest
   GEMINI_FALLBACK_MODELS=gemini-flash-latest,gemini-flash-lite-latest,gemini-pro-latest
   TTS_VOICE=vi-VN-NamMinhNeural
   ```
4. Chạy bộ kiểm thử offline (không tốn quota API):
   ```bash
   npm run kiem-tra:all
   ```

---

## 2. Chạy sản xuất tự chủ trên máy cục bộ

### Chạy hoàn toàn tự động (không cần truyền chủ đề)
AI tự kiểm tra hàng đợi trong `du_lieu/bo_nho_hoc_hoi.json` (nếu chủ đề `'cho'` còn `< 3` thì tự lên mạng săn thêm 5 chủ đề mới, lọc trùng) → chọn chủ đề điểm cao nhất → nghiên cứu Wikipedia + Google Search Grounding → biên kịch 6 hồi >10 phút + Tầng 3 Tự kiểm định → TTS Edge (cache SHA-256) → render tách hồi & ghép phim + xuất trọn gói YouTube:

```bash
python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py
```

### Sản xuất liên tiếp nhiều tập (có nghỉ giữa tập & chịu lỗi từng tập)
```bash
python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py --so-tap 3 --nghi-giay 30
```
- Nếu 1 tập lỗi (ví dụ nghẽn mạng), hệ thống ghi log vào `du_lieu/nhat_ky_san_xuat.log`, trả trạng thái chủ đề lỗi về `'cho'` và tiếp tục sang tập kế tiếp.

### Đặt hàng riêng 1 chủ đề cụ thể
```bash
python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py --chu-de "Leonhard Euler và bài toán 7 cây cầu Königsberg"
```

### Chỉ tạo tư liệu & kịch bản để đọc duyệt (bỏ qua TTS & Render MP4)
```bash
python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py --chi-tao-kich-ban
```

### Chạy từng mô-đun lẻ khi cần
- Tự săn thêm 5 chủ đề mới nạp vào hàng đợi:
  ```bash
  python -X utf8 scripts/pipeline/san_tim_chu_de.py --nap-hang-doi 5
  ```
- Nghiên cứu tư liệu web + Wikipedia cho 1 chủ đề:
  ```bash
  python -X utf8 scripts/pipeline/san_tim_chu_de.py --nghien-cuu <slug>
  ```
- Nạp phản hồi khán giả / chỉ số kênh để AI tự rút kinh nghiệm cho các tập sau:
  ```bash
  python -X utf8 scripts/pipeline/bo_nho_hoc_hoi.py --hoc-tu-phan-hoi --slug <slug> --ghi-chu "Khán giả thích miếng hài ở hồi 4, cần tăng ví dụ đời sống ở hồi 3"
  ```
- Xem tóm tắt bộ nhớ học hỏi & ngữ cảnh sẽ tiêm vào biên kịch:
  ```bash
  python -X utf8 scripts/pipeline/bo_nho_hoc_hoi.py --xem-ngu-canh
  ```

---

## 3. Sản phẩm đầu ra mỗi tập

- `du_lieu/<slug>/tu_lieu_nghien_cuu.json`: niên đại chuẩn, nhân vật thật, giai thoại đời thường, kiến thức/LaTeX cốt lõi, ứng dụng hiện đại và danh sách URL nguồn.
- `du_lieu/<slug>/doc_duyet_kich_ban.md`: bản đọc duyệt kịch bản 6 hồi kèm báo cáo Tầng 3 Tự kiểm định.
- `out/<slug>/video_hoan_chinh.mp4` (và bản tương thích `out/<slug>.mp4`): phim hoạt hình hoàn chỉnh 1080p 30fps (>10 phút).
- `out/<slug>/chapters_va_mo_ta.txt`: trọn gói đăng YouTube (3 tiêu đề gợi ý, đoạn mô tả hấp dẫn, mốc thời gian `MM:SS` từng hồi, nguồn tham khảo).
- `out/<slug>/luoi_kiem_dinh.png`: ảnh lưới 18 khung hình (3 khung/hồi) để kiểm tra nhanh chất lượng hình ảnh.

---

## 4. Cấu hình chạy tự động trên GitHub Actions (Public repo)

Workflow nằm tại `.github/workflows/tu-dong-video10p.yml` (chạy định kỳ thứ 2 & thứ 5 lúc 02:00 UTC và hỗ trợ bấm chạy tay `workflow_dispatch`).

### Bước 1: Bật Secret `GEMINI_API_KEYS`
1. Mở repository trên GitHub → chọn **Settings** → **Secrets and variables** → **Actions**.
2. Ở tab **Secrets**, bấm **New repository secret**:
   - **Name:** `GEMINI_API_KEYS`
   - **Secret:** Dán danh sách các Gemini API key cách nhau bằng dấu phẩy (VD: `AIzaSy...,AIzaSy...`).
   - *(Tùy chọn)* Bạn có thể thêm biến môi trường ở tab **Variables** nếu muốn đổi `GEMINI_MODEL` hoặc `TTS_VOICE`.

### Bước 2: Bật quyền ghi (`Read and write permissions`) để tự lưu bộ nhớ học hỏi
1. Vào **Settings** → **Actions** → **General**.
2. Kéo xuống mục **Workflow permissions**.
3. Chọn **Read and write permissions** rồi bấm **Save**.
   *(Cho phép workflow tự commit/push tệp `du_lieu/bo_nho_hoc_hoi.json` cùng tư liệu/kịch bản nhẹ về nhánh `main`, không đẩy `.mp4`/`.mp3` lên git.)*

### Bước 3: Chạy thử bằng tay
1. Vào tab **Actions** → chọn workflow **Tu Dong San Xuat Video Toan Hoc >10 Phut**.
2. Bấm **Run workflow**, điền `so_tap` (VD: `1`), tùy chọn `chu_de_tuy_chon` (hoặc để trống cho AI tự chọn), có thể tích `chi_tao_kich_ban` để test nhanh lần đầu.
3. Sau khi chạy xong, tải phim (`video_hoan_chinh.mp4`), `chapters_va_mo_ta.txt` và `luoi_kiem_dinh.png` tại mục **Artifacts** của lượt chạy.
