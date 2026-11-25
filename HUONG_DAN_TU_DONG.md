# Hướng Dẫn Vận Hành Hệ Thống AI Tự Chủ (`v3.0`)

Hệ thống `Video10P v3.0` là dây chuyền AI tự chủ khép kín hằng ngày theo kiến trúc **Lai 2.5D** sản xuất phim hoạt hình kể chuyện lịch sử Toán học dài **> 10 phút (> 600 giây)**: tự săn chủ đề web, kiểm chứng tư liệu (`timeline_su_kien`, `tu_dien_phat_am`, `goi_y_boi_canh_va_dao_cu`), biên kịch & đạo diễn `v3.0` (hồ sơ tạo hình nhân vật cố định, quy hoạch `danhSachBoiCanhAI[]` 14–20 bối cảnh + 4–6 cận cảnh vật thể, đối thoại 3–5 lượt ngắn + `dao_goc_can_mat` + bong bóng chat 4 kiểu + 6 VFX hài), sinh bối cảnh truyện tranh châu Âu đồng nhất bằng Gemini/Imagen + phân tích ánh sáng `Pillow` tự đồng bộ lên nhân vật (fallback an toàn sang 22 bối cảnh SVG), khóa dấu tiếng Việt trước Edge TTS, hội thoại đa giọng nhịp hài `0.25s–0.40s` + RMS 30fps, **Clean Cinema UI**, chia chunk song song `> 120s` trên GitHub Actions, ghép FFmpeg `-14 LUFS`, phụ đề `.srt`, 3 Thumbnail A/B và Visual QA.

---

## 1. Chuẩn bị môi trường cục bộ

1. Cài đặt phụ thuộc Node.js và Python (trên Windows luôn chạy Python với `-X utf8`):
   ```bash
   npm ci
   pip install -r requirements.txt
   ```
   *(Phụ thuộc Python tối giản: chỉ `edge-tts` và `Pillow`; toàn bộ Gemini/Imagen REST, phân tích ánh sáng, YouTube API v3, đọc CSV/JSON đều chạy thuần Python stdlib + Pillow.)*
2. Đảm bảo đã cài **FFmpeg** (`ffmpeg` và `ffprobe` có trong `PATH`).
3. Sao chép `.env.example` thành `.env` và điền danh sách API key Gemini (tách nhau bằng dấu phẩy để tự xoay vòng khi gặp `429`/`503`):
   ```env
   GEMINI_API_KEYS=key_1,key_2,key_3
   GEMINI_MODEL=gemini-flash-latest
   GEMINI_FALLBACK_MODELS=gemini-flash-latest,gemini-flash-lite-latest,gemini-pro-latest
   GEMINI_IMAGE_MODELS=gemini-2.5-flash-image,imagen-3.0-generate-002,gemini-2.0-flash-exp-image-generation

   TTS_VOICE=vi-VN-NamMinhNeural
   TTS_VOICE_NGUOI_DAN=vi-VN-NamMinhNeural
   TTS_VOICE_NHAN_VAT=vi-VN-HoaiMyNeural
   TTS_VOICE_BINH_LUAN_HAI=vi-VN-HoaiMyNeural

   # Tùy chọn tự động đăng video & hẹn giờ công khai lên YouTube (workflow vẫn thành công 100% nếu bỏ trống)
   # YOUTUBE_CLIENT_ID=your_google_oauth_client_id.apps.googleusercontent.com
   # YOUTUBE_CLIENT_SECRET=your_google_oauth_client_secret
   # YOUTUBE_REFRESH_TOKEN=your_youtube_oauth_refresh_token

   # Hoàn toàn tùy chọn (workflow vẫn chạy thành công 100% khi không đặt biến này)
   # YOUTUBE_API_KEY=your_youtube_data_api_v3_key
   # YOUTUBE_OAUTH_TOKEN=your_optional_youtube_oauth_access_token
   ```
4. Chạy bộ kiểm thử toàn hệ thống offline (không tốn quota API):
   ```bash
   npm run kiem-tra:all
   ```

---

## 2. Chạy sản xuất tự chủ trên máy cục bộ

### Chạy hoàn toàn tự động (1 lệnh — không cần truyền chủ đề)
AI tự kiểm tra hàng đợi trong `du_lieu/bo_nho_hoc_hoi.json` (nếu `< 3` chủ đề `'cho'` thì tự lên mạng săn thêm 6 chủ đề mới, lọc trùng tuyệt đối) → chọn chủ đề ưu tiên số 1 → nghiên cứu web → biên kịch & đạo diễn `v3.0` + Guardrail khóa dấu tiếng Việt → sinh bối cảnh minh họa AI (`public/boi_canh/<slug>/`, cache theo hash mô tả, phân tích `anhSangMoiTruong`) → TTS đa giọng nhịp hài `0.25s–0.40s` + RMS 30fps → render Clean Cinema UI, ghép FFmpeg auto-ducking `-14 LUFS`, xuất `.srt`, 3 Thumbnail A/B & Visual QA:

```bash
python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py
```

### Tùy chọn chạy cục bộ hữu ích
- Đặt hàng riêng 1 chủ đề cụ thể:
  ```bash
  python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py --chu-de "Leonhard Euler và bài toán 7 cây cầu Königsberg"
  ```
- Tắt sinh ảnh bối cảnh AI (chạy nhanh/tiết kiệm quota, Remotion tự dùng 22 bối cảnh Parallax SVG):
  ```bash
  python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py --tat-anh-ai
  ```
- Chạy riêng bước sinh bối cảnh minh họa AI & phân tích ánh sáng cho 1 tập:
  ```bash
  python -X utf8 scripts/pipeline/tao_boi_canh_ai.py --slug <slug>
  python -X utf8 scripts/pipeline/tao_boi_canh_ai.py --slug <slug> --offline
  ```
- Chỉ tạo tư liệu & kịch bản để đọc duyệt (bỏ qua TTS & Render MP4):
  ```bash
  python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py --chi-tao-kich-ban
  ```
- Render tách pha theo chunk thông minh (`> 120s` tự chia 2 mảnh `hoi_XX_p1`, `hoi_XX_p2`):
  ```bash
  python -X utf8 scripts/pipeline/render_dai.py --slug <slug> --chi-render-chunk hoi_03_p1 --che-do-ci
  python -X utf8 scripts/pipeline/render_dai.py --slug <slug> --chi-ghep-hoan-chinh --che-do-ci
  ```
- Render thử kịch bản mẫu điện ảnh `v3.0`, tương thích `v1/v2` và Thumbnail A/B:
  ```bash
  npx remotion render src/index.ts VideoDaiNguoiQue out/mau_v3_dien_anh.mp4 --props=du_lieu/mau_v3_dien_anh.json
  npm run render:mau
  npx remotion still src/index.ts ThumbnailToanHoc out/mau_thumbnail_check.png
  ```

---

## 3. Vận hành tự động cách 2 ngày & Tự động đăng YouTube trên GitHub Actions (`v3.0`)

Workflow `.github/workflows/tu-dong-video10p.yml` bật sẵn chế độ **tự động cách 2 ngày** (để tối ưu quota + nhịp xuất bản đều đặn), tự động đăng YouTube kèm hẹn giờ công khai `19:30` giờ Việt Nam (`+07:00`), và tối ưu chống OOM / timeout cho runner Ubuntu chuẩn:

### Lịch chạy tự động (`schedule`)
- Mặc định: `cron: '0 0 */2 * *'` — tự động chạy lúc **07:00 sáng theo giờ Việt Nam (UTC+7), cách 2 ngày 1 lần** (và mặc định đặt lịch YouTube công khai lúc **19:30 cùng ngày `+07:00`**).
- Dòng thay thế có sẵn trong YAML nếu muốn cố định Thứ 2 – Thứ 4 – Thứ 6 hằng tuần: `cron: '0 0 * * 1,3,5'`.
- Chống chồng chéo: `concurrency` nhóm theo `${{ github.workflow }}-${{ github.ref }}` (`cancel-in-progress: false`).

### Kiến trúc 3 Job tối ưu hiệu năng CI
1. **`chuan-bi` (`timeout-minutes: 25`)**:
   - Dùng cache `node_modules`, npm & pip; chạy `npm run kiem-tra:all`.
   - Tự nạp hàng đợi khi `< 3`, chạy nghiên cứu, biên kịch `v3.0` + Guardrail tiếng Việt có dấu, TTS đa giọng nhịp hài + RMS, sinh bối cảnh AI (`public/boi_canh/<slug>/`, trừ khi bật `tat_anh_ai`) và upload artifact trung gian (`du_lieu/<slug>/`, `public/audio/<slug>/`, `public/boi_canh/<slug>/`, `retention-days: 1`).
2. **`render-song-song` (`timeout-minutes: 35`, `fail-fast: false`, `max-parallel: 8`)**:
   - Render song song từng mảnh `matrix.chunk` với cache Chromium, `--concurrency 2 --jpeg-quality 85` và `NODE_OPTIONS=--max-old-space-size=4096`.
3. **`ghep-va-luu` (`timeout-minutes: 25`, `permissions: contents: write`)**:
   - Ghép FFmpeg auto-ducking `-14 LUFS`, xuất `.srt`, `chapters_va_mo_ta.txt`, trích nhanh lưới 18 khung keyframe, chạy Visual QA (trừ khi bật `tat_visual_qa`) và render 3 Thumbnail A/B.
   - Chạy `--hoan-tat-tu-meta` cập nhật `bo_nho_hoc_hoi.json`.
   - Chạy `scripts/pipeline/dang_youtube.py` (nếu bật `tu_dong_dang_youtube` và đã cài 3 Secrets OAuth YouTube; nếu chưa cài Secret thì in hướng dẫn & thoát mã `0` an toàn): tự upload Resumable 8MB, đặt lịch `publishAt` `19:30 +07:00` (hoặc `--chi-rieng-tu`), gắn `thumbnail_1.png`, tải phụ đề `phu_de.srt` và lưu `youtubeVideoId` + `youtubePublishAt` vào `bo_nho_hoc_hoi.json`.
   - Upload artifact sản phẩm hoàn chỉnh (`retention-days: 14`).
   - Lưu `bo_nho_hoc_hoi.json` & tư liệu nhẹ (loại trừ `cache_boi_canh.json` và `public/boi_canh/` khỏi git), `git pull --rebase origin main` và push lên `main`.

### Các tham số khi bấm chạy thủ công (`workflow_dispatch`)
Vào tab **Actions** → **Tu Dong San Xuat Video Toan Hoc >10 Phut** → **Run workflow**:

| Tham số (`input`) | Kiểu | Ý nghĩa |
| --- | --- | --- |
| `chu_de` | `string` | Chủ đề đặt hàng riêng (để trống để AI tự săn & chọn chủ đề ưu tiên số 1 trong hàng đợi). |
| `slug` | `string` | Slug tùy chọn hoặc slug đã tồn tại trong `du_lieu/` để tận dụng cache. |
| `chi_chay_lai_chunk` | `string` | Chỉ chạy lại 1 hoặc nhiều chunk cụ thể (VD: `hoi_03_p1` hoặc `hoi_02,hoi_03_p1`). |
| `tat_anh_ai` | `boolean` | Tắt sinh bối cảnh minh họa AI (dùng 22 bối cảnh Parallax SVG có sẵn để tiết kiệm quota/thời gian). |
| `tat_visual_qa` | `boolean` | Bỏ qua bước gọi Gemini Vision Visual QA. |
| `chi_tao_kich_ban` | `boolean` | Chỉ dừng sau bước nghiên cứu & biên kịch để tải `doc_duyet_kich_ban.md` về đọc trước. |
| `tat_nhac_nen` | `boolean` | Tắt nhạc nền khi ghép video (vẫn giữ chuẩn hóa thoại `-14 LUFS`). |
| `tu_dong_dang_youtube` | `boolean` | Tự động đăng video lên YouTube sau khi ghép xong (mặc định `true`; tự bỏ qua an toàn nếu thiếu Secret). |
| `che_do_dang` | `choice` | Chế độ đăng YouTube: `hen_gio` (công khai lúc `19:30` VN `+07:00`) hoặc `rieng_tu` (Private chờ duyệt tay). |

### Thiết lập tối thiểu trên GitHub (chỉ cần 2 bước)
1. **Secret `GEMINI_API_KEYS`**: vào **Settings** → **Secrets and variables** → **Actions** → **New repository secret**, tên `GEMINI_API_KEYS`, dán các API key Gemini cách nhau bằng dấu phẩy. *(Không bắt buộc cài `YOUTUBE_API_KEY`; có thể thêm biến `GEMINI_IMAGE_MODELS` nếu muốn đổi thứ tự model tạo ảnh.)*
2. **Quyền ghi nhánh `main`**: vào **Settings** → **Actions** → **General** → **Workflow permissions** → chọn **Read and write permissions** → **Save**.

---

## 4. Tự động đăng video & đặt lịch hẹn giờ YouTube (thuần Python stdlib)

Hệ thống tích hợp sẵn `scripts/pipeline/dang_youtube.py` dùng thuần `urllib` + `json` + `os` (không cài `google-api-python-client`), hỗ trợ Resumable Upload chia chunk `8MB`, tự đọc tiêu đề + mô tả + chapters từ `chapters_va_mo_ta.txt`, trích thẻ tag từ `du_lieu_render.json`, đặt lịch `publishAt` múi giờ `+07:00`, gắn `thumbnail_1.png`, tải phụ đề `phu_de.srt` và lưu `youtubeVideoId` vào `du_lieu/bo_nho_hoc_hoi.json`.

### Bước 1 — Lấy `YOUTUBE_REFRESH_TOKEN` trong 30 giây (chạy 1 lần trên máy cá nhân)
1. Vào [Google Cloud Console](https://console.cloud.google.com/) → bật **YouTube Data API v3** → **Credentials** → **Create Credentials** → **OAuth client ID** (chọn loại **Desktop app**).
2. Chạy tiện ích stdlib cục bộ (mở trình duyệt đăng nhập kênh YouTube và in sẵn 3 biến để copy):
   ```bash
   python -X utf8 scripts/pipeline/lay_refresh_token_youtube.py
   ```
3. Dán 3 Secrets vừa nhận vào GitHub (**Settings** → **Secrets and variables** → **Actions** → **New repository secret**) hoặc vào file `.env`:
   - `YOUTUBE_CLIENT_ID`
   - `YOUTUBE_CLIENT_SECRET`
   - `YOUTUBE_REFRESH_TOKEN`

> **Lưu ý về dự án Google Cloud chưa xác minh audit**: Nếu Google Cloud project đang ở chế độ *Testing* (chưa gửi duyệt YouTube API audit), video upload qua API có thể bị khóa ở chế độ Riêng tư (`private`). Khi đó hãy chọn `che_do_dang: rieng_tu` trên GitHub Actions hoặc truyền cờ `--chi-rieng-tu` ở cục bộ để đăng dạng Riêng tư rồi bấm công khai tay trong YouTube Studio.

### Bước 2 — Chạy đăng YouTube thủ công trên máy cục bộ (tùy chọn)
- Đăng và hẹn giờ công khai lúc **19:30 hôm nay** (giờ Việt Nam `+07:00`; nếu đã qua 19:30 thì tự đẩy sang 19:30 ngày mai):
  ```bash
  python -X utf8 scripts/pipeline/dang_youtube.py --slug <slug> --gio-cong-khai-vn "19:30" --cach-ngay 0
  ```
- Đăng và hẹn giờ công khai vào **19:30 ngày mai**:
  ```bash
  python -X utf8 scripts/pipeline/dang_youtube.py --slug <slug> --gio-cong-khai-vn "19:30" --cach-ngay 1
  ```
- Đăng ở chế độ **Riêng tư** (chờ duyệt tay, không gán `publishAt`):
  ```bash
  python -X utf8 scripts/pipeline/dang_youtube.py --slug <slug> --chi-rieng-tu
  ```

---

## 5. Vòng tự học từ số liệu YouTube thật (tùy chọn)

Sau khi đăng video lên YouTube (48–72 giờ sau khi chạy Test & Compare cho `thumbnail_1..3.png`), nạp số liệu để AI tối ưu Hook 30s, nhịp kể và Thumbnail cho tập sau:

- **Nạp qua CLI**:
  ```bash
  python -X utf8 scripts/pipeline/bo_nho_hoc_hoi.py --nhap-so-lieu-youtube \
    --slug euler_bay_cay_cau_konigsberg \
    --ctr 8.4 --giu-chan-30s 72.5 --thoi-luong-xem-tb 05:45 \
    --moc-tut-view "00:45,04:20" --bien-the-thumbnail-thang 2
  ```
- **Nạp từ file CSV/JSON xuất từ YouTube Studio**:
  ```bash
  python -X utf8 scripts/pipeline/bo_nho_hoc_hoi.py --nhap-so-lieu-youtube --file-so-lieu du_lieu/so_lieu_youtube.csv
  ```
- **Kéo tự động qua YouTube Data API v3** (nếu đã cài `YOUTUBE_API_KEY` trong `.env`; nếu đã dùng `dang_youtube.py` lưu `youtubeVideoId` vào `bo_nho_hoc_hoi.json` thì có thể bỏ qua `--video-id`):
  ```bash
  python -X utf8 scripts/pipeline/dong_bo_youtube.py --slug <slug>
  python -X utf8 scripts/pipeline/dong_bo_youtube.py --slug <slug> --video-id <YOUTUBE_VIDEO_ID>
  ```
