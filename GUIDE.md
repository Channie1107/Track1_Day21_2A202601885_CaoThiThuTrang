# GUIDE — Làm bài lab với eval-kit (bản repo, chạy local)

Repo này là **bản "mang về"** của eval workflow trên platform: cùng tutor (system prompt
và cơ chế tool-calling y hệt), cùng corpus, nhưng chạy ở máy bạn bằng Python — để bạn nhìn
tận mắt mọi thứ platform giấu đi: prompt thật, retrieval, tool calls, verdict của judge.

> **Đọc trước:** file lab tổng `day21-lab-ai-evaluation-capstone.md` là kim chỉ nam.
> File này chỉ trả lời một câu: **bước X của lab thì chạy cái gì, ở đâu?**

## Bản đồ: bước nào — platform hay repo?

| Bước lab | Làm ở đâu | Vì sao |
|---|---|---|
| P1. Thiết kế coverage (grid → dataset) | Ngoài (giấy/sheet + AI chat) | Con người giữ quyền coverage |
| P2. Chạy dataset + chấm tay | **Platform** (batch run + label) | Team cần chấm chung, có version |
| P3. Siết rubric + routing | Ngoài (thảo luận nhóm) | Quyết định con người |
| P4. Code check + judge + calibrate | **Platform** chính · **repo** nếu muốn nhanh/rẻ hơn | Repo chạy local, không tốn quota |
| P5. Đọc kết quả, đặt ngưỡng | **Platform** (board/calibration) · **repo** cho phân tích sâu | Một số phân tích chỉ repo mới có |
| P6. Verdict + report | Ngoài (file eval-pack/) | Viết bằng ngôn ngữ PM |

Nguyên tắc: **mọi thứ cần chia sẻ trong nhóm → platform; mọi thứ muốn mổ xẻ sâu → repo.**

## Setup một lần (2 phút)

```bash
cd eval-kit
pip install -r requirements.txt          # chỉ cần thư viện requests
cp dataset.example.jsonl dataset.jsonl   # dataset mẫu, sửa/thêm tuỳ ý
printf 'OPENAI_API_KEY=sk-...\nDEEPSEEK_API_KEY=sk-...\n' > .env   # key coach cấp, KHÔNG commit
python3 test_eval_kit.py                 # 31 test offline — sạch hết mới đi tiếp
```

Gợi ý: nếu test fail ngay tầng 2 (corpus), gần như chắc chắn bạn đang chạy sai thư mục —
`cd` vào đúng `eval-kit/` rồi chạy lại.

## Luồng chạy — 3 lệnh chính

```bash
python3 run_eval.py        # 1. chạy tutor trên dataset.jsonl      -> results.jsonl
python3 judge.py           # 2. judge chấm results (theo judge_prompt.md) -> verdicts.jsonl
python3 report.py          # 3. sinh report.html (mở double-click, không cần mạng)
```

Mỗi lệnh ghi đè file output của nó — muốn giữ vòng cũ, copy file đi trước
(vd `cp results.jsonl runs/v1-results.jsonl`).

### Bước 1 — `run_eval.py`: tutor thật chạy trên dataset

- Đọc từng dòng `dataset.jsonl`, gọi tutor theo **cơ chế tool-calling y hệt platform**:
  model tự quyết định gọi `kb_search` bao nhiêu lần, với truy vấn nào (xem trong
  `results.jsonl`, trường `tool_calls`).
- In từng dòng: thời gian, số token, chi phí ước tính. Tổng chi phí in ở cuối.
- Gợi ý: chạy thử `dataset.example.jsonl` (5 câu) trước khi chạy dataset lớn của nhóm.

### Bước 2 — `judge.py`: LLM judge chấm

- Judge là model KHÁC tutor (mặc định `gpt-4o-mini`) — tránh tự chấm chéo.
- Rubric judge nằm trong `judge_prompt.md` — **đây là file bạn sẽ sửa nhiều nhất** khi
  calibrate. Sửa ít một thứ mỗi vòng, chạy lại, so agreement.
- Chấm một vài câu thôi: `python3 judge.py sc-01 sc-03`.
- Nếu `labels.csv` đã có nhãn người (export từ report), judge.py in luôn confusion matrix
  + % agreement — **đây là con số calibration của bạn**.

### Bước 3 — `report.py`: nhìn và gán nhãn

- `report.html` tự chứa mọi dữ liệu: câu hỏi, slide context, câu trả lời, nguồn trích,
  verdict judge. Bấm pass/fail/uncertain để gán nhãn người (lưu trong trình duyệt).
- Bấm **Export labels.csv** → lưu đè `labels.csv` → chạy lại `judge.py` để xem agreement.

## Những việc CHỈ repo làm được (platform không có)

| Việc | Làm sao |
|---|---|
| Xem tutor gọi `kb_search` với truy vấn gì, bao nhiêu vòng | Mở `results.jsonl`, trường `tool_calls` và `steps` của từng row |
| Sửa retrieval (BM25, top-k) để thử nghiệm | Sửa `retrieve_corpus()` trong `tutor.py` |
| Đọc system prompt thật của tutor | Đầu file `tutor.py` — biến `SYSTEM_PROMPT` |
| Chạy judge bằng model khác để so sánh | `EVAL_JUDGE_MODEL=deepseek/deepseek-v4-flash python3 judge.py` |
| Xem raw output chưa parse (khi JSON vỡ) | `results.jsonl` trường `raw_content`; report.html nút "xem raw" |
| Test offline toàn bộ pipeline | `python3 test_eval_kit.py` (không tốn API) |

## Cấu hình (biến môi trường, đặt trong .env)

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `EVAL_MODEL` | `deepseek/deepseek-v4-flash` | Model của tutor |
| `EVAL_JUDGE_MODEL` | `openai/gpt-4o-mini` | Model của judge (nên khác tutor) |
| `EVAL_BASE_URL` | `https://litellm.vlearn.dev/v1` | Gateway |
| `DEEPSEEK_API_KEY` / `OPENAI_API_KEY` | — | Key theo family model |

## Gỡ lỗi nhanh

| Triệu chứng | Nguyên nhân thường gặp |
|---|---|
| `Chưa có API key...` | Thiếu `.env`, hoặc tên biến sai family (deepseek cần `DEEPSEEK_API_KEY`) |
| Row có `_parse_error` / `_truncated` | Model trả JSON vỡ (thường do cắt output) — mở `raw_content` xem; đó là một failure mode thật, đáng ghi vào bài |
| Judge toàn 401 | Key không phải của gateway LiteLLM (xem Lưu ý trong README) |
| Retrieve trượt chủ đề | Câu hỏi quá ngắn/deixis — gắn `metadata.slide` với `keyword` vào row dataset |

## Nộp bài thì lấy gì từ repo?

Quy cách nộp đầy đủ: **`eval-pack/README.md`** (đã align với mục 10 của file lab tổng).
Từ repo này, copy sang `evidence/` của bài nộp:

- `dataset.jsonl` → `evidence/dataset-v1.jsonl` — dataset nhóm chốt (đầu vào).
- `results.jsonl` → `evidence/results-v1.jsonl` (v2, v3... mỗi lần chạy lại) — output
  tutor thật, có cả `tool_calls`, tokens, cost từng câu.
- `verdicts.jsonl` → `evidence/verdicts-v1.jsonl` (v2... từng vòng calibration).
- `judge_prompt.md` → `evidence/judge-prompt-v1.md` (copy MỖI LẦN trước khi sửa).
- `labels.csv` (export từ report.html) → `evidence/labels.csv` — nhãn người.
- Số liệu agreement/confusion matrix in ra từ `judge.py` → chép vào
  `eval-pack/5-calibration-report.md`.

Nhớ: chạy xong một vòng là copy ngay — cuối buổi mới gom là mất dấu các vòng trước.
