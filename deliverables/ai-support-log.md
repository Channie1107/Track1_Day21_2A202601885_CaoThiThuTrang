# AI Support Log — Cao Thị Thu Trang

> Nhật ký ghi lại phạm vi AI hỗ trợ trong phần việc do Cao Thị Thu Trang thực
> hiện. AI chỉ hỗ trợ soạn thảo, kiểm tra cấu trúc và phân tích; quyết định chất
> lượng cuối cùng thuộc về người thực hiện.

## Phạm vi công việc cá nhân

| Hạng mục | AI hỗ trợ | Cách kiểm chứng |
|---|---|---|
| Lead coverage design và scenario bank | Gợi ý biến thể câu hỏi, expected behavior và cách tổ chức Input Grid | Đối chiếu từng scenario với mục tiêu coverage; kiểm tra đủ 25 dòng và rà soát các slice OOS, ambiguous, high-risk |
| Human baseline và disagreement review | Hỗ trợ chuẩn hóa format nhãn, phát hiện lỗi scenario ID/header và tổng hợp disagreement | Đối chiếu CSV với results/verdicts; giữ nhãn baseline theo quyết định của Lead PM |
| Prompt calibration và final verdict | Gợi ý cấu trúc rubric, near-miss examples, routing map và monitoring plan | Chạy pipeline, kiểm tra confusion matrix, đọc thủ công các disagreement và kiểm tra evidence trước khi kết luận |
| README, REPORT và evidence bundle | Hỗ trợ sắp xếp nội dung Markdown, bảng scorecard và liên kết artifact | Đối chiếu số liệu report với dataset, labels, verdicts; kiểm tra UTF-8, JSONL và link public |

## Các phần AI gợi ý nhưng không sử dụng nguyên trạng

- Không sử dụng metric hoặc kết luận do AI tự suy đoán khi không có evidence.
- Không coi LLM Judge là nguồn sự thật duy nhất; high-risk và disagreement vẫn
  được route cho người kiểm duyệt.
- Không đưa API key, thông tin cá nhân hoặc dữ liệu nhạy cảm vào public trace.

## Các quyết định cá nhân

- Chọn coverage 25 scenario, gồm các slice OOS, ambiguous và high-risk.
- Resolve các trường hợp human disagreement theo nhãn của Lead PM.
- Chọn verdict **Ship with conditions** dựa trên 21/25 agreement và các false
  positive cần theo dõi trong regression set.
- Sử dụng public dataset link để chia sẻ evidence thay vì invite member vào
  project private có thể phát sinh chi phí workspace.
