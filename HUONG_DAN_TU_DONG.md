# Hướng Dẫn Vận Hành Hệ Thống AI Tự Chủ (`v2.0`)

Hệ thống `Video10P v2.0` là dây chuyền AI tự chủ khép kín hoàn toàn hằng ngày để sản xuất phim hoạt hình 2D kể chuyện lịch sử Toán học dài **> 10 phút (> 600 giây)** — từ tự động săn chủ đề web, kiểm chứng tư liệu (kèm `timeline_su_kien`, `tu_dien_phat_am`, `goi_y_boi_canh_va_dao_cu`), biên kịch 2 vai (**Biên kịch kể chuyện** + **Đạo diễn Storyboard**) & Guardrail tự sửa cục bộ, hội thoại đa giọng `luotThoai[]` + RMS 30fps từng lượt, 22 bối cảnh 3 lớp Parallax `React.memo` + 10 sinh vật/đồ vật động + 8 góc quay camera tự động focus người nói + tương tác khán giả đếm ngược 3 giây, chia chunk song song `> 120s` chống OOM/timeout trên GitHub Actions, đến hậu kỳ âm thanh auto-ducking `-14 LUFS`, phụ đề `.srt`, 3 Thumbnail A/B và Visual QA Gemini Vision.

---

## 1. Chuẩn bị môi trường cục bộ

1. Cài đặt phụ thuộc Node.js và Python (trên Windows luôn chạy Python với `-X utf8`):
   ```bash
   npm ci
   pip install -r requirements.txt
   ```
   *(Phụ thuộc Python tối giản: chỉ `edge-tts` và `Pillow`; toàn bộ Gemini REST, YouTube API v3, đọc CSV/JSON đều chạy thuần Python stdlib.)*
2. Đảm bảo đã cài **FFmpeg** (`ffmpeg` và `ffprobe` có trong `PATH`).
3. Sao chép `.env.example` thành `.env` và điền danh sách API key Gemini (tách nhau bằng dấu phẩy để tự xoay vòng khi gặp `429`/`503`):
   ```env
   GEMINI_API_KEYS=key_1,key_2,key_3
   GEMINI_MODEL=gemini-flash-latest
   GEMINI_FALLBACK_MODELS=gemini-flash-latest,gemini-flash-lite-latest,gemini-pro-latest
   TTS_VOICE=vi-VN-NamMinhNeural
   TTS_VOICE_NGUOI_DAN=vi-VN-NamMinhNeural
   TTS_VOICE_NHAN_VAT=vi-VN-HoaiMyNeural
   TTS_VOICE_BINH_LUAN_HAI=vi-VN-HoaiMyNeural

   # Hoàn toàn tùy chọn (workflow hằng ngày vẫn chạy thành công 100% khi không đặt biến này)
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
AI tự kiểm tra hàng đợi trong `du_lieu/bo_nho_hoc_hoi.json` (nếu số chủ đề `'cho'` còn `< 3` thì tự lên mạng săn thêm 6 chủ đề giàu giai thoại mới, lọc trùng hoàn toàn với `chu_de_da_lam` và `hang_doi_chu_de`) → chọn chủ đề ưu tiên số 1 → nghiên cứu web & xuất `timeline_su_kien` + `tu_dien_phat_am` + `goi_y_boi_canh_va_dao_cu` → biên kịch 2 vai + Guardrail tự sửa cục bộ → TTS đa giọng theo từng nhân vật + RMS 30fps → render, ghép FFmpeg auto-ducking `-14 LUFS`, xuất `.srt`, 3 Thumbnail A/B, lưới 18 khung keyframe & Visual QA:

```bash
python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py
```

### Tùy chọn chạy cục bộ hữu ích
- Đặt hàng riêng 1 chủ đề cụ thể:
  ```bash
  python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py --chu-de "Srinivasa Ramanujan và con số 1729"
  ```
- Chỉ tạo tư liệu & kịch bản để đọc duyệt (bỏ qua TTS & Render MP4):
  ```bash
  python -X utf8 scripts/pipeline/san_xuat_lien_tuc.py --chi-tao-kich-ban
  ```
- Render tách pha theo chunk thông minh (`> 120s` tự chia 2 mảnh `hoi_XX_p1`, `hoi_XX_p2`) hoặc theo từng hồi:
  ```bash
  python -X utf8 scripts/pipeline/render_dai.py --slug <slug> --chi-render-chunk hoi_03_p1 --che-do-ci
  python -X utf8 scripts/pipeline/render_dai.py --slug <slug> --chi-render-hoi 1
  python -X utf8 scripts/pipeline/render_dai.py --slug <slug> --chi-ghep-hoan-chinh --che-do-ci
  ```
- Render thử kịch bản mẫu tương tác `v2.0` và Thumbnail A/B:
  ```bash
  npm run render:mau
  npx remotion render src/index.ts VideoDaiNguoiQue out/mau_v2_tuong_tac.mp4 --props=du_lieu/mau_v2_tuong_tac.json
  npx remotion still src/index.ts ThumbnailToanHoc out/mau_thumbnail_check.png
  ```

---

## 3. Vận hành tự động hằng ngày trên GitHub Actions (`v2.0`)

Workflow `.github/workflows/tu-dong-video10p.yml` đã bật sẵn chế độ **hoàn toàn tự động hằng ngày** và tối ưu chống tràn RAM / timeout cho runner Ubuntu chuẩn (2–4 vCPU, 7GB RAM):

### Lịch chạy tự động (`schedule`)
- Mặc định: `cron: '0 0 * * *'` — tự động chạy lúc **07:00 sáng hằng ngày theo giờ Việt Nam (UTC+7)** mà không cần nhập chủ đề thủ công.
- Gợi ý tiết kiệm quota cho repo Private: đã có sẵn dòng comment `# - cron: '0 0 * * 1,3,5'` (chạy cách ngày thứ 2, 4, 6 lúc 07:00 VN) trong file YAML để đổi trong 5 giây.
- Cơ chế chống chồng chéo: `concurrency` nhóm theo `${{ github.workflow }}-${{ github.ref }}` với `cancel-in-progress: false` đảm bảo hai lần chạy không bao giờ ghi đè `du_lieu/bo_nho_hoc_hoi.json`.

### Kiến trúc 3 Job tối ưu hiệu năng CI
1. **`chuan-bi` (`timeout-minutes: 25`)**:
   - Dùng cache `node_modules`, npm & pip; chạy kiểm định `npm run kiem-tra:all`.
   - Khi bỏ trống `chu_de`, tự kiểm tra `du_lieu/bo_nho_hoc_hoi.json`; nếu `< 3` chủ đề đang chờ thì tự gọi `san_tim_chu_de.py` săn thêm 6 chủ đề mới.
   - Chạy nghiên cứu, biên kịch 2 vai + Guardrail, TTS đa giọng + RMS (`--chi-chuan-bi --nguong-chia-chunk 120`), xuất `danhSachChunk` và upload artifact trung gian gọn nhẹ (`retention-days: 1`).
2. **`render-song-song` (`timeout-minutes: 35`, `fail-fast: false`, `max-parallel: 8`)**:
   - Chạy song song từng mảnh `matrix.chunk` (`fromJson(needs.chuan-bi.outputs.danh_sach_chunk)`).
   - Dùng cache trình duyệt Chromium (`node_modules/.remotion`, `~/.cache/remotion`) không tải lại.
   - Chạy `render_dai.py --chi-render-chunk <chunk> --che-do-ci --concurrency 2 --jpeg-quality 85` kèm `NODE_OPTIONS=--max-old-space-size=4096` chống OOM; upload mảnh MP4 (`retention-days: 1`).
3. **`ghep-va-luu` (`timeout-minutes: 25`, `permissions: contents: write`)**:
   - Tải toàn bộ mảnh chunk, ghép FFmpeg auto-ducking `-14 LUFS`, xuất `.srt`, `chapters_va_mo_ta.txt`, trích nhanh lưới 18 khung bằng keyframe FFmpeg, chạy Visual QA (trừ khi bật `tat_visual_qa`) và render 3 Thumbnail A/B.
   - Upload artifact sản phẩm hoàn chỉnh (`retention-days: 14`): `video_hoan_chinh.mp4`, `thumbnail_*.png`, `phu_de.srt`, `chapters_va_mo_ta.txt`, `luoi_kiem_dinh.png`, `bao_cao_visual_qa.json`, `doc_duyet_kich_ban.md`.
   - Chạy `--hoan-tat-tu-meta` ghi chủ đề vào `chu_de_da_lam` và **xóa khỏi `hang_doi_chu_de`**, sau đó `git pull --rebase origin main` và push lại lên `main` để ngày hôm sau chắc chắn chọn chủ đề mới.

### Các tham số khi bấm chạy thủ công (`workflow_dispatch`)
Vào tab **Actions** → **Tu Dong San Xuat Video Toan Hoc >10 Phut** → **Run workflow**:

| Tham số (`input`) | Kiểu | Ý nghĩa |
| --- | --- | --- |
| `chu_de` | `string` | Chủ đề đặt hàng riêng (để trống để AI tự săn & chọn chủ đề ưu tiên số 1 trong hàng đợi). |
| `slug` | `string` | Slug tùy chọn hoặc slug đã tồn tại trong `du_lieu/` để chạy lại tận dụng cache. |
| `chi_chay_lai_chunk` | `string` | Chỉ chạy lại 1 hoặc nhiều chunk cụ thể (VD: `hoi_03_p1` hoặc `hoi_02,hoi_03_p1`; để trống = chạy toàn bộ). |
| `tat_visual_qa` | `boolean` | Bỏ qua bước gọi Gemini Vision Visual QA nếu muốn tiết kiệm quota/thời gian. |
| `chi_tao_kich_ban` | `boolean` | Chỉ dừng sau bước nghiên cứu & biên kịch để tải `doc_duyet_kich_ban.md` về đọc trước. |
| `tat_nhac_nen` | `boolean` | Tắt nhạc nền khi ghép video (vẫn giữ chuẩn hóa âm lượng thoại `-14 LUFS`). |

### Thiết lập tối thiểu trên GitHub (chỉ cần 2 bước)
1. **Secret `GEMINI_API_KEYS`**: vào **Settings** → **Secrets and variables** → **Actions** → **New repository secret**, tên `GEMINI_API_KEYS`, dán các API key Gemini cách nhau bằng dấu phẩy. *(Không bắt buộc cài `YOUTUBE_API_KEY`.)*
2. **Quyền ghi nhánh `main`**: vào **Settings** → **Actions** → **General** → **Workflow permissions** → chọn **Read and write permissions** → **Save**.

---

## 4. Vòng tự học từ số liệu YouTube thật (tùy chọn)

Sau khi đăng video lên YouTube (48–72 giờ sau khi chạy Test & Compare cho `thumbnail_1..3.png`), nạp số liệu để AI tối ưu Hook 30s, nhịp kể và Thumbnail cho tập sau:

- **Nạp qua CLI**:
  ```bash
  python -X utf8 scripts/pipeline/bo_nho_hoc_hoi.py --nhap-so-lieu-youtube \
    --slug ramanujan_so_tay_bi_an_1729 \
    --ctr 8.4 --giu-chan-30s 72.5 --thoi-luong-xem-tb 05:45 \
    --moc-tut-view "00:45,04:20" --bien-the-thumbnail-thang 2 \
    --binh-luan-noi-bat "Giải thích con số 1729 siêu dễ hiểu!"
  ```
- **Nạp từ file CSV/JSON xuất từ YouTube Studio**:
  ```bash
  python -X utf8 scripts/pipeline/bo_nho_hoc_hoi.py --nhap-so-lieu-youtube --file-so-lieu du_lieu/so_lieu_youtube.csv
  ```
- **Kéo tự động qua YouTube Data API v3** (nếu đã cài `YOUTUBE_API_KEY` trong `.env`):
  ```bash
  python -X utf8 scripts/pipeline/dong_bo_youtube.py --slug <slug> --video-id <YOUTUBE_VIDEO_ID>
  ```
