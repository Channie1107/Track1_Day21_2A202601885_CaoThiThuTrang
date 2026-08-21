# Hồ sơ nộp bài — AI Evaluation

## Thông tin cá nhân & Nhóm

- **Cao Thị Thu Trang** — 2A202601885
- **Nguyễn Thị Trà My** — 2A202601026
- **Bùi Thị Như Ngọc** — 2A202601882
- **Tên nhóm:** `Node.01`
- **Ngày nộp:** `21/08/2026`

## Sơ đồ 6 Phase & Artifacts

```text
P1 Coverage Design       → Input Grid, scenario bank
P2 Human Baseline        → Dataset v1, nhãn human, agreement log
P3 Rubric & Routing      → Rubric v1, Routing Map, decision rules
P4 Scale & Calibrate     → Code checks, Judge prompt, confusion matrix
P5 Read Results          → Scorecard, slice breakdown, regression cases
P6 Final Verdict         → PM report, evidence bundle, monitoring plan
```

Artifacts chính:

- Dataset: [dataset-v1.jsonl](deliverables/evidence/dataset-v1.jsonl)
- Human labels: [labels.csv](deliverables/evidence/labels.csv)
- Judge prompt đang dùng: [judge_prompt.md](eval/judge_prompt.md)
- Judge prompt v1: [judge_prompt-v1.md](deliverables/evidence/judge_prompt-v1.md)
- Judge prompt v2 đã calibration: [judge_prompt-v2.md](deliverables/evidence/judge_prompt-v2.md)
- Verdicts v1: [verdicts-v1.json](deliverables/evidence/verdicts-v1.json)
- Verdicts v2: [verdicts-v2.jsonl](deliverables/evidence/verdicts-v2.jsonl)
- Trace project: [braintrust-link.md](deliverables/braintrust-link.md)
- Báo cáo: [deliverables/REPORT.md](deliverables/REPORT.md)

## Lịch sử hai lần chạy

- **Run v1:** dùng prompt ban đầu; agreement theo log là **19/25 = 76%**.
- **Run v2:** prompt được calibration bằng near-miss examples G16, G18, G19;
  kết quả hiện tại là **21/25 = 84%**. Đây là bản cải thiện dùng cho verdict
  cuối, còn v1 được giữ lại để audit và so sánh regression.

## Đóng góp cá nhân

- **Lead coverage design:** thiết kế các scenario đại diện cho in-scope, OOS,
  ambiguous và high-risk; bảo đảm dataset có các tình huống thực tế.
- **Prompt calibration:** xây dựng tiêu chí groundedness cho LLM Judge và thêm
  các near-miss examples từ những trường hợp Judge đánh Pass nhưng human đánh Fail.
- **Final Product Verdict:** tổng hợp confusion matrix, phân tích false positive,
  kiểm tra regression cases và đề xuất cách route giữa code, Judge và expert.

## Verdict của nhóm & Lý do

- **Verdict:** **Ship with conditions**.
- **Lý do:** Judge v2 đạt 21/25 agreement (84%), nhưng còn 3 false positive
  tại G08, G17 và G18. Vì vậy Judge phù hợp làm LLM Assist/Judge có kiểm soát,
  chưa nên là bộ phận quyết định duy nhất cho high-risk.
- **Điều kiện:** giữ code checks ở các lỗi xác định được, chuyển high-risk và
  các case bất đồng cho expert, đồng thời theo dõi lại agreement sau mỗi lần
  sửa prompt hoặc corpus.

## Bài học áp dụng cho dự án thật

Quality bar cần được chuyển thành các quy tắc quan sát được trước khi chạy eval.
Human baseline giúp phát hiện claim nghe hợp lý nhưng không có citation trực tiếp.
LLM Judge nên là một thành phần trong routing, không phải nguồn sự thật tuyệt đối.
Trong dự án thật, cần version hóa dataset, rubric và prompt; lưu regression cases;
và đặt alert theo slice thay vì chỉ nhìn điểm trung bình toàn hệ thống.
