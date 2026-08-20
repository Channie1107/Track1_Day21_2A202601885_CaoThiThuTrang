# Eval Pack — quy cách bài nộp capstone AI Evaluation (Day 20–21)

"Chiếc hộp" chứa toàn bộ minh chứng eval loop của nhóm cho VLearn AI Tutor.

**Nguyên tắc bắt buộc:** mỗi bước của eval loop phải nộp đủ ba thứ —
**đầu vào** (bạn cho gì vào), **đầu ra** (hệ thống trả gì ra — file data thô),
và **quyết định** (bạn kết luận/lựa chọn gì ở bước đó, VÌ SAO). Thiếu một trong ba,
bước đó coi như chưa làm.

## Cấu trúc repo nộp (tên thư mục/file cố định)

```text
Track1_Day21_MHV_HoVaTen/
├── README.md                  # thông tin cá nhân + nhóm, đóng góp của tôi, verdict tóm tắt
├── eval-pack/                 # 7 file QUYẾT ĐỊNH — viết bằng ngôn ngữ PM
│   ├── 1-input-grid.md            # dimensions chọn gì, vì sao → grid → combinations giữ/loại
│   ├── 2-dataset-v1.md            # 20–30 câu: quyết định Keep/Rewrite/Reject từng câu AI sinh
│   ├── 3-rubric-v1.md             # tiêu chí + định nghĩa pass/fail siết từ case bất đồng nào
│   ├── 4-routing-map.md           # tiêu chí → Code / LLM assist / LLM judge / Expert, kèm lý do
│   ├── 5-calibration-report.md    # mỗi judge: 2+ vòng, confusion matrix, diff prompt, pattern lệch
│   ├── 6-scorecard-and-gate.md    # kết quả theo slice + thresholds chốt TRƯỚC khi xem số
│   └── 7-verdict.md               # Ship / Ship có điều kiện / Hold + report 1 trang đủ 5 phần
├── evidence/                  # DATA THÔ — input/output thật của từng bước chạy
│   ├── dataset-v1.jsonl           # dataset nhóm chốt (đầu vào mọi lần chạy)
│   ├── results-v1.jsonl           # output tutor (mỗi row: input, output JSON, tool_calls, tokens, cost)
│   ├── labels.csv                 # nhãn người của 3 thành viên (vòng chấm độc lập)
│   ├── judge-prompt-v1.md         # judge prompt vòng 1
│   ├── judge-prompt-v2.md         # judge prompt vòng 2 (diff với v1 phải giải thích trong file 5)
│   ├── verdicts-v1.jsonl          # output judge vòng 1
│   ├── verdicts-v2.jsonl          # output judge vòng 2
│   └── platform-export.json       # runs + labels export từ platform
└── ai-support-log.md          # bạn dùng AI ở đâu, AI sai ở đâu, bạn quyết lại gì
```

Quy ước phiên bản: mỗi lần chạy lại là một version mới — `results-v2.jsonl`,
`verdicts-v3.jsonl`... Không ghi đè file cũ; calibration report cần đối chiếu được
từng vòng.

## Checklist trước khi nộp

- [ ] `eval-pack/` đủ 7 file, đúng tên; file nào cũng có phần **quyết định + vì sao**
- [ ] `evidence/` có đủ data thô của mọi bước: dataset, results, labels, judge prompts
      từng vòng, verdicts từng vòng, export platform
- [ ] Số liệu trong eval-pack khớp với data trong evidence/ (kiểm chứng được)
- [ ] Verdict có đủ 5 phần report và một quyết định rõ ràng
- [ ] `ai-support-log.md` là của chính người nộp

## Gợi ý

- Mỗi file trong `eval-pack/` đã có sẵn khung câu hỏi dẫn — trả lời ngắn, dẫn chứng
  bằng số/file thật trong `evidence/`, đừng viết chung chung.
- Chạy xong một vòng là copy file ngay vào `evidence/` — để cuối buổi mới gom là mất.
