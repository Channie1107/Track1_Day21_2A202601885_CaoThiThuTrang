# K3 Track 1 · Day 20–21 — AI Evaluation (eval-kit)

Repo làm bài capstone **AI Evaluation** của case **VLearn AI Tutor** — trợ giảng trả lời
câu hỏi học viên, chỉ dựa trên tài liệu khóa học, output là JSON
`{scope, answer, sources, followup_questions}`.

Đây là **môi trường chính của bài lab**: tutor thật (system prompt + tool-calling
`kb_search`), corpus 18 tài liệu, vòng eval đầy đủ — chạy bằng Python trên máy bạn, dùng
**API key của chính bạn** (OpenAI / DeepSeek / Gemini / Anthropic / OpenRouter).

> **File lab tổng (kim chỉ nam, có timeline + rubric chấm):** đọc kèm
> `day21-lab-ai-evaluation-capstone.md` do lớp phát. Repo này hướng dẫn phần **chạy**:
> bước nào gõ lệnh gì, file nào ra file nào. Chi tiết từng lệnh: [GUIDE.md](GUIDE.md).

## Quickstart (3 phút)

```bash
pip install -r requirements.txt      # 1. cài đặt
cp .env.example .env                 # 2. điền API key của provider bạn dùng (+ BRAINTRUST_API_KEY để log trace)
cp dataset.example.jsonl dataset.jsonl
python3 test_eval_kit.py             # 3. 37 test offline phải sạch hết
python3 run_eval.py                  # 4. chạy tutor trên dataset -> results.jsonl
python3 report.py && open report.html  # 5. xem kết quả, gán nhãn
```

## Làm bài theo 6 phase — bước nào chạy gì?

| Phase (theo file lab tổng) | Làm ở đâu | Trong repo này chạy gì |
|---|---|---|
| **P1. Thiết kế coverage** — chọn dimensions, tổ hợp, sinh câu hỏi | Giấy/sheet + AI chat | Chưa cần repo. Kết quả: viết vào `dataset.jsonl` (format xem `dataset.example.jsonl`, nhớ field `metadata.slide`) |
| **P2. Human baseline** — chạy dataset, chấm tay | Repo | `python3 run_eval.py` → `python3 report.py` → mở `report.html` gán nhãn → Export `labels-<tên>.csv` → `python3 agreement.py labels-*.csv` đo đồng thuận |
| **P3. Rubric + routing** | Thảo luận nhóm | Không chạy repo. Viết vào `eval-pack/3-rubric-v1.md`, `4-routing-map.md` |
| **P4. Scale & calibrate judge** | Repo | `python3 code_checks.py` (làn code) → sửa `judge_prompt.md` → `python3 judge.py` → đọc confusion matrix + % agreement. Sửa ít một thứ, chạy lại — mỗi vòng copy `judge_prompt.md` + `verdicts.jsonl` ra `evidence/` |
| **P5. Đọc kết quả, đặt ngưỡng** | Repo | `results.jsonl` có sẵn latency/tokens/cost từng câu; `report.html` để đọc theo slice |
| **P6. Verdict + report** | Viết trong `eval-pack/` | Điền `eval-pack/6-scorecard-and-gate.md` và `7-verdict.md` |

**Nguyên tắc nộp bài:** mỗi bước phải nộp đủ **đầu vào + đầu ra (data thô) + quyết định
kèm vì sao**. Cấu trúc thư mục nộp và checklist: [eval-pack/README.md](eval-pack/README.md).

**Tracing bắt buộc:** đặt `BRAINTRUST_API_KEY` trong `.env` (hoặc LangSmith tương đương)
trước khi chạy — mọi run tutor/judge log thành trace, link project là một phần bài nộp.

## Các lệnh

```bash
python3 run_eval.py        # tutor chạy dataset.jsonl -> results.jsonl (kèm tool_calls, tokens, cost)
python3 code_checks.py     # làn code: schema/citation/quote bằng rule Python (không tốn API)
python3 report.py          # results + verdicts + labels -> report.html (mở double-click)
python3 agreement.py labels-a.csv labels-b.csv   # so nhãn giữa các thành viên
python3 judge.py           # LLM judge chấm -> verdicts.jsonl (+ confusion matrix nếu có labels.csv)
```

Chỉ chấm vài câu: `python3 judge.py sc-01 sc-03`.
Chạy dataset khác: `python3 run_eval.py ten-file.jsonl`.

## Chọn model & provider

Model viết dạng `provider/model` — repo gọi **thẳng API chuẩn của từng hãng**:

| Prefix model | Cần key trong .env |
|---|---|
| `openai/gpt-4o-mini`, ... | `OPENAI_API_KEY` |
| `deepseek/deepseek-v4-flash`, ... | `DEEPSEEK_API_KEY` |
| `gemini/gemini-3.1-flash-lite`, ... | `GEMINI_API_KEY` |
| `anthropic/claude-...` | `ANTHROPIC_API_KEY` |
| `openrouter/<vendor>/<model>` | `OPENROUTER_API_KEY` |

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `EVAL_MODEL` | `deepseek/deepseek-v4-flash` | Model của tutor |
| `EVAL_JUDGE_MODEL` | `openai/gpt-4o-mini` | Model của judge (nên KHÁC tutor — tránh tự chấm chéo) |
| `BRAINTRUST_API_KEY` | — | Bật log trace (bắt buộc khi nộp bài) |
| `EVAL_BASE_URL` + `EVAL_API_KEY` | — (không đặt = gọi thẳng provider) | Tuỳ chọn: gateway OpenAI-compatible riêng |

## Cấu trúc repo

- `tutor.py` — tutor thật: system prompt + tool `kb_search` (BM25 local trên `corpus/`),
  vòng tool-calling cap 6 vòng. `python3 tutor.py` = demo retrieve.
- `run_eval.py` / `code_checks.py` / `judge.py` / `report.py` / `agreement.py` — các bước
  của eval loop.
- `test_eval_kit.py` — 37 test offline (không tốn API); `EVAL_LIVE=1` để thêm 3 test live.
- `corpus/` — 18 tài liệu nguồn + `manifest.json` (địa chỉ nguồn: `doc_id#section_id`).
- `dataset.example.jsonl` — 5 câu mẫu đủ loại (in-scope, out-of-scope, mơ hồ, xin đáp án).
- `judge_prompt.md` — prompt judge; **file bạn sẽ sửa nhiều nhất khi calibrate**.
- `labels.csv` — nhãn người (`scenario_id,label,note`), export từ `report.html`.
- `eval-pack/` — 7 template bài nộp + quy cách `evidence/` (xem README trong đó).

## Định dạng một dòng dataset

```json
{"id": "sc-01", "input": "câu hỏi của học viên",
 "metadata": {"slide": {"id": "s53", "title": "Pass rate giống nhau — không có nghĩa judge nghĩ giống bạn",
                        "keyword": "calibration"}}}
```

`metadata.slide` (tuỳ chọn) là slide học viên đang xem khi hỏi — đưa vào prompt tutor
và cả judge, để câu deixis kiểu "giải thích đoạn này" chấm được đúng bối cảnh.
Câu noise/out-of-scope không gắn slide thì bỏ field này.

## Lưu ý

- Model deepseek v4 được gửi kèm `"thinking": {"type": "disabled"}` (đã xử lý sẵn trong
  `tutor.py`) — thiếu nó output sẽ bị reasoning tokens ăn mất.
- Tutor chạy `max_tokens=2000`: câu dài bị cắt giữa JSON sẽ được đánh dấu
  `_truncated`/`_parse_error` trong `results.jsonl` — đó là một failure mode thật,
  đáng ghi vào bài, đừng xoá.
- Provider thỉnh thoảng trả HTTP 200 nhưng body JSON bị cắt ngang — `chat()` tự retry
  tối đa 3 lần.
- `.env` trong repo được nạp **ghi đè** biến shell sẵn có — nếu shell bạn export sẵn
  `OPENAI_API_KEY` khác thì `.env` vẫn thắng.
- `report.py` không gọi mạng; `report.html` nhúng sẵn toàn bộ dữ liệu.
- Giá token dùng để ước tính chi phí nằm trong `run_eval.py` (biến `PRICING`).
