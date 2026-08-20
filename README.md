# eval-kit — chạy lại eval loop của AI Tutor ở local

Bản "mang về" của eval loop trên platform web: tutor gọi tool `kb_search` theo đúng cơ
chế agentic của platform (cùng system prompt, cùng corpus) → chấm bằng LLM judge → xem
report và gán nhãn. Chạy hoàn toàn ở local bằng Python 3, **không cần đăng nhập** gì
ngoài một API key của LiteLLM gateway.

> **Đang làm bài lab? Đọc [GUIDE.md](GUIDE.md)** — bản đồ từng bước: bước nào làm trên
> platform, bước nào chạy repo, lệnh nào, file nào, kèm gợi ý gỡ lỗi.

## 3 lệnh duy nhất

```bash
pip install -r requirements.txt      # 1. cài đặt (chỉ cần thư viện requests)
python3 run_eval.py                  # 2. chạy eval trên dataset.jsonl -> results.jsonl
open report.html                     # 3. mở report (sau khi chạy: python3 report.py)
```

Trước lần chạy đầu tiên, tạo 2 thứ trong thư mục này:

```bash
cp dataset.example.jsonl dataset.jsonl   # dataset mẫu 5 câu, sửa/thêm tuỳ ý
printf 'OPENAI_API_KEY=sk-...\n' > .env  # key LiteLLM, KHÔNG commit file này lên git
python3 test_eval_kit.py                 # kiểm tra nhanh: 31 test offline phải sạch
```

Lần lượt sau mỗi lệnh chạy eval, để có report thì chạy thêm `python3 report.py` rồi
mở `report.html` (double-click cũng được — file tĩnh, không cần server).

## Quy trình đầy đủ (tuỳ chọn thêm bước judge)

1. `python3 run_eval.py` — đọc `dataset.jsonl`, gọi tutor từng câu (tuần tự, in tiến
   độ), ghi `results.jsonl` kèm latency, số token và chi phí ước tính.
2. `python3 judge.py` — LLM judge chấm từng row theo rubric trong `judge_prompt.md`
   (mặc định tiêu chí groundedness), ghi `verdicts.jsonl`. Nếu `labels.csv` đã có nhãn
   người thì in luôn confusion matrix + tỉ lệ agreement. Muốn chỉ chấm vài row:
   `python3 judge.py sc-01 sc-03`.
3. `python3 report.py && open report.html` — report tĩnh: xem từng câu hỏi, câu trả
   lời đã parse đẹp, nguồn trích dẫn, verdict của judge; bấm nút để gán nhãn
   pass/fail/uncertain (lưu trong localStorage), rồi bấm **Export labels.csv** để lấy
   nhãn người về, lưu đè lên `labels.csv` và chạy lại bước 2 để xem agreement.

## Cấu hình (biến môi trường, có thể đặt trong .env)

Model viết dạng `provider/model` — repo gọi **thẳng API chuẩn của từng hãng**,
không bắt buộc gateway nào:

| Prefix model | Cần key | Endpoint mặc định |
|---|---|---|
| `openai/gpt-4o-mini`, ... | `OPENAI_API_KEY` | api.openai.com |
| `deepseek/deepseek-v4-flash`, ... | `DEEPSEEK_API_KEY` | api.deepseek.com |
| `gemini/gemini-3.1-flash-lite`, ... | `GEMINI_API_KEY` | generativelanguage.googleapis.com (chế độ tương thích OpenAI) |
| `anthropic/claude-...` | `ANTHROPIC_API_KEY` | api.anthropic.com (chế độ tương thích OpenAI) |
| `openrouter/<vendor>/<model>` | `OPENROUTER_API_KEY` | openrouter.ai |

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `EVAL_MODEL` | `deepseek/deepseek-v4-flash` | Model của tutor |
| `EVAL_JUDGE_MODEL` | `openai/gpt-4o-mini` | Model của judge (nên khác tutor) |
| `EVAL_BASE_URL` + `EVAL_API_KEY` | — (không đặt = gọi thẳng provider) | Tuỳ chọn: đi qua gateway OpenAI-compatible riêng (LiteLLM, proxy nội bộ...) — model id giữ nguyên nguyên chuỗi |

## Cấu trúc repo

- `tutor.py` — system prompt thật của tutor + tool `kb_search` chạy theo cơ chế agentic
  y hệt platform (model tự quyết định gọi bao nhiêu lần, truy vấn gì; retrieval là BM25
  local tách section theo heading, bỏ dấu + lowercase, top-k mặc định 5). Chạy
  `python3 tutor.py` để xem demo retrieve không cần API key.
- `run_eval.py` / `judge.py` / `report.py` — 3 bước của eval loop như trên.
- `test_eval_kit.py` — 31 test offline (không tốn API); `EVAL_LIVE=1` để thêm 3 test live.
- `corpus/` — 18 tài liệu nguồn + `manifest.json` (địa chỉ nguồn: `doc_id#section_id`).
- `dataset.example.jsonl` — 5 câu mẫu (in-scope, out-of-scope, mơ hồ, xin đáp án).
- `judge_prompt.md` — prompt judge mẫu, sửa rubric tuỳ tiêu chí muốn đo.
- `labels.csv` — nhãn người (`scenario_id,label,note`), export từ report.
- `eval-pack/` — template nộp bài capstone (xem `eval-pack/README.md`).

## Định dạng một dòng dataset

```json
{"scenario_id": "sc-01", "input": "câu hỏi của học viên",
 "metadata": {"slide": {"id": "s51", "title": "Vì sao calibration là bước cốt lõi",
                        "keyword": "calibration"}}}
```

`metadata.slide` (tuỳ chọn) là slide học viên đang xem khi hỏi — run_eval đưa context
này vào prompt tutor, đồng thời nối `keyword` vào truy vấn retrieve (để câu deixis kiểu
"giải thích đoạn này" vẫn retrieve trúng slide); judge cũng nhận context để chấm đúng
bối cảnh. Không có slide (noise, chào hỏi, out-of-scope...) thì để `null` hoặc bỏ hẳn.

## Lưu ý

- Model deepseek v4 được gửi kèm `"thinking": {"type": "disabled"}` (đã xử lý sẵn trong
  `tutor.py`) — thiếu nó output sẽ bị reasoning tokens ăn mất.
- Tutor chạy với `max_tokens=2000`: với 800, câu trả lời dài bị cắt giữa JSON
  (`finish_reason=length`) thành output không parse được — row như vậy được đánh dấu
  `_truncated` / `_parse_error` trong results thay vì làm chết cả batch.
- Gateway thỉnh thoảng trả HTTP 200 nhưng body JSON bị cắt ngang — `chat()` tự retry
  tối đa 3 lần.
- `.env` trong repo được nạp **ghi đè** biến shell sẵn có — nếu không, một
  `OPENAI_API_KEY` global (vd export trong `~/.zshrc`) sẽ lấn key gateway và judge
  sẽ 401.
- `report.py` không gọi mạng; `report.html` nhúng sẵn toàn bộ dữ liệu.
- Giá token dùng để ước tính chi phí nằm trong `run_eval.py` (biến `PRICING`).
