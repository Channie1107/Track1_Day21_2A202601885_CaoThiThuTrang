---
doc_id: "slide-day19-20"
title: "AI Evaluation — slide deck Day 19–20 (Track 1)"
author: "Mai Anh Nguyen (Blue)"
type: "course-slides"
source_url: "local: day20/d20-full.pdf"
retrieved: "2026-08-19"
lang: "vi"
---
# AI Evaluation — Day 19–20 deck

## s01 — AI Evaluation

Định nghĩa, đo lường và tự động hoá chất lượng sản phẩm AI —
hai buổi, năm kỹ năng

## s02 — Năm kỹ năng bạn sẽ mang về

Transcript là thứ user thấy — trace là thứ PM phải đọc, từng bước
01 Đọc trace
agent thực thi.
User Input Grid: LLM giúp sinh input, con người kiểm soát coverage
02 Thiết kế dataset có coverage
và review lại.
Thu hẹp scope, định nghĩa “đủ tốt”, formalize thành rubric cả team
03 Cảm tính → tiêu chí đo được chấm giống nhau.
Cái gì kiểm bằng code, cái gì cần LLM judge, cái gì phải đến tay
04 Chọn evaluator cho từng tiêu chí
expert.
Expert định nghĩa chuẩn vàng — dùng để calibrate judge và bắt
05 Đưa expert vào loop
failure mode mới.

## s03 — Mai Anh Nguyen (Blue)

Generalist Product Builder
2026 FPT Long Châu · PM, Healthcare Product
2025 Thongtincuuho.org · Co-founder
2025 FPT Software AI Center · PM, AI Agent
2021–2025 Xantus · PM, On-chain Analytics & AI Agent
2016–2021 DYNO, Kalapa · PM, OCR & eKYC & Credit Scoring
LinkedIn | Facebook

## s04 — BỐI CẢNH

Câu chuyện quen thuộc của mọi team làm AI
NGÀY DEMO VÀI TUẦN SAU HÔM NAY
Demo chạy tốt Bức tranh mờ dần Product Review ngày mai
Khách hàng sớm khen, stakeholder User đông hơn: người rất thích, Leadership hỏi bạn track chất
đồng thuận. Bạn quyết định mở người phàn nàn, người không quay lượng bằng cách nào. Usage
rộng. lại. Đổi model — không biết còn ổn metrics không trả lời được.
không.
“AI của mình có đang làm việc tốt một cách ổn định không?”
— bạn không có câu trả lời. Đó là evaluation gap.

## s05 — Vai trò của PM đã mở rộng: luồng sử

dụng cộng thêm phân bố chất lượng
TRADITIONAL PRODUCT AI PRODUCT
Deterministic — đúng hoặc sai Wide outcome distributions
Input A Output B ✓ Pass
Input A Output B ✓ Pass
Input A Output B ✓ Pass
Chạy bao nhiêu lần cũng y hệt — kiểm thử chỉ có hai kết quả: 1 Poor Good Great
hoặc 0.
METRIC Test Pass / Fail — 1 hoặc 0
METRIC Agent Success Rate
Thế giới deterministic — cùng input, cùng output; test pass
hay fail. Thế giới probabilistic — cùng input, output vẫn khác nhau.

## s06 — AI Evals có hai lớp — product team làm lớp trên

PRODUCT TEAM · LÀM
Ở ĐÂY
Application Accuracy Helpfulness Tone / Style Safety Latency Format compliance
Evals User intent match Cost efficiency
Chất lượng sản phẩm
trong ngữ cảnh user thật
MODEL PROVIDER
Model Evals Reasoning Coding Math Instruction following Safety
Benchmark chuẩn hoá
cho năng lực nền
Model giỏi benchmark không đảm bảo sản phẩm đạt chất lượng — hai lớp đo hai thứ khác nhau.

## s07 — AI Evals Lifecycle

Từ quan sát thủ công đến kiểm soát chất lượng liên tục.

## s08 — Evals là một vòng lặp, không phải một lần kiểm thử

Chuẩn bị Vibe Check Offline Evals Production Monitoring
PHA PROTOTYPE PHA PROTOTYPE PHA BUILD PHA PRODUCTION
Product promise Chạy case nhỏ Formalize rubric Theo dõi quality và cost
Unit of evaluation Đọc output và trace tay Xây reference dataset Sample traces để review
Instrument agent Tìm failure modes So sánh candidates Phát hiện drift
Scenarios ban đầu Định nghĩa “đủ tốt” Ship / Limited / Hold Điều tra incidents
↺ Continuous Improvement failure thật thành dataset · cập nhật rubric · regression test · lặp lại lifecycle
“Evals không phải một lần kiểm thử trước release — đó là vòng lặp Tham chiếu: Anthropic — demystifying evals for AI agents
biến quan sát thực tế thành quyết định sản phẩm có thể kiểm chứng.”

## s09 — Ba bộ chấm điểm bổ sung nhau, không thay thế nhau

Mỗi bộ chấm chỉ đánh giá được một phần của bản ghi hội thoại hoặc kết quả cuối.
Code-based grader Model-based grader Human grader
Kiểm tra điều xác minh được Đánh giá chất lượng ngữ nghĩa Định nghĩa và kiểm chứng ranh giới
CÁCH LÀM CÁCH LÀM CÁCH LÀM
Khớp chuỗi, biểu thức, gần đúng Chấm theo thang tiêu chí Chuyên gia lĩnh vực rà soát
Kiểm thử nhị phân Khẳng định bằng ngôn ngữ tự nhiên Phán đoán đám đông
Phân tích tĩnh So sánh từng cặp, đối chiếu mẫu Kiểm tra mẫu ngẫu nhiên, A/B test
Xác minh tool call và tham số + chuẩn + Đo độ đồng thuận giữa người chấm
Đồng thuận nhiều giám khảo
✓ Nhanh, rẻ, khách quan, tái lập ✓ Linh hoạt, mở rộng được, bắt được
được sắc thái ✓ Chuẩn vàng, dùng để hiệu chỉnh
✕ Cứng nhắc với output hợp lệ nhưng ✕ Không ổn định, đắt hơn code, cần model-based grader
khác định dạng; kém với tác vụ hiệu chỉnh bằng nhãn của con ✕ Đắt, chậm, cần huy động chuyên
cảm tính người gia ở quy mô lớn
Câu hỏi không phải “bộ chấm nào tốt nhất?” mà là “tiêu chí này cần loại bằng chứng nào?” — chọn bộ chấm cho từng
tiêu chí.

## s10 — Bước 1 — Vibe Check: chạy trước khi viết PRD

Mục tiêu là khám phá behavior, chưa phải chấm điểm chính thức.
Generate inputs Run prototype Label outputs Note patterns
10–30 đầu vào bao phủ Chạy từng đầu vào qua Gắn nhãn từng đầu ra, ghi lý Model làm được gì, không
nhiều persona và use case. prototype, quan sát model do pass hoặc fail. làm được gì, hành vi nào
vận hành thật. bất ngờ?
happy path edge case input → agent → output Ship Chỉnh Fail what works surprises
FAIL LẶP LẠI → SEEDS YOUR PRD PASS TỐT NHẤT → SEEDS GOLDEN OUTPUTS
Những gì model không làm được định hình chính xác Output tốt nhất từ vibe check trở thành reference
những gì PRD cần đặc tả. dataset cho few-shot và evals.
Demo before memo — quan sát model trước, viết yêu cầu sau.

## s11 — Output bước 1 — Golden Outputs

Reference dataset là câu thật cộng nhãn đúng kỳ vọng — dùng cho few-shot và cho evals.
# CÂU NGƯỜI DÙNG Ý ĐỊNH CẢM XÚC ƯU TIÊN
PHẢI CÓ EDGE CASE
Mình nhận áo rồi mà
Câu mơ hồ · Thiếu thông tin · Nhiều ý trong
1 chật quá, đổi size sao Đổi hàng Khó chịu Trung bình
một câu · Không nhớ mã đơn
vậy?
“Áo không giống hình lắm, giờ đổi hay trả được ta”
Shop giao nhầm màu “Mình đặt 2 đơn, 1 đơn muốn trả, 1 đơn muốn đổi
2 Đổi hàng Bực bội Cao
cho mình rồi size”
“Cái đơn hôm trước đó, check giúp mình với”
App báo giao rồi mà
3 mình chưa thấy đơn Tra cứu đơn Tức giận Cao
đâu ✓ Case mơ hồ giúp test khả năng hỏi lại
✓ Không ép model đoán khi chưa rõ
Mình muốn trả đôi giày
4 hôm trước mà không Trả hàng Lo lắng Trung bình ✓ Dataset tiếp tục lớn dần sau production
còn mã đơn nữa
Cái đơn hôm bữa ấy,
5 thôi giờ mình không lấy Cần làm rõ Trung tính Trung bình
nữa được không

## s12 — Bước 2 — Offline Evals: chấm dataset trước release

01 Trigger thay đổi BENCHMARK CỐ ĐỊNH — MỌI RELEASE DÙNG CHUNG
Prompt mới · model upgrade · tool integration
Reference dataset
50 historical tickets, labels đã verify
Categorization accuracy eval
Chạy trên reference dataset
02 Sentiment precision eval
Tự động, không cần manual review
Escalation recall eval
Critical — không được phép regression
So với baseline
03 CẬP NHẬT DATASET KHI
Version hiện tại là chuẩn so sánh
Phát hiện failure mode mới từ production
Scope sản phẩm thay đổi
Deploy Fix & iterate
Evals quá dễ pass
Quality ok, approve Regression — điều tra rồi
chạy lại
Sau khi fix, quay lại bước 01 và chạy lại toàn bộ eval.
“Nếu không thể ship model mới ngay trong ngày ra mắt —
bottleneck là evaluation, không phải model.”

## s13 — Một kết quả eval nhìn như thế nào

DIMENSION BASELINE CANDIDATE DELTA
Accuracy VERDICT
71% 78% +7%
% output đúng rubric
Ship
Latency Accuracy +7%, edge case +17%, gate đã
1.2s 1.8s +0.6s qua.
P50 response time
Edge case pass rate
44% 61% +17%
% edge case xử lý đúng CẦN ĐỌC THÊM
3 regression traces — hiểu tại sao fail
Regression count trước khi ship.
— 3 Cần review
Case từng pass, nay fail
Số liệu cho phép ship. Nó không thay việc đọc
Quality gate
71% — fail 78% — pass Gate cleared trace.
Pass threshold ≥ 75%
Đừng chỉ nhìn con số tổng — trung bình che khuyết điểm: tổng score tăng 82%→85% vẫn có thể giấu một phân khúc tụt 70%→55%.
Luôn đọc theo slice và mở regression traces trước khi ship.

## s14 — Bước 3 — Sau launch, user tạo ra case bạn chưa nghĩ tới

SIGNAL MỚI TỪ PRODUCTION
Q1 Q2
Intent mới Product còn đạt quality Offline và online score có
User dùng AI theo cách team chưa nghĩ tới khi thiết kế bar ngay lúc này không? đang diverge?
Agent Success Rate trong Offline tốt mà online xấu —
Ngôn ngữ và data format lạ production có dưới ngưỡng? dataset chưa phản ánh thực
Tiếng địa phương, ký tự đặc biệt, input không chuẩn tế.
Behavior ngoài use case ban đầu
User kéo AI về tình huống không nằm trong PRD
REAL-TIME CHECK DISTRIBUTION GAP
Tool và data source thay đổi
API third-party update, schema đổi, pipeline drift
Q3 Q4
User expectation thay đổi
Failure mode nào mới User feedback có mâu
Chuẩn “tốt” của user dịch chuyển theo thời gian dùng
xuất hiện? thuẫn với eval?
Unknown unknowns — offline Thumbs-down tăng mà eval
eval không thấy được cho tới score ổn — rubric đang đo sai
khi có user thật. thứ.
NEW BLIND SPOTS SIGNAL CONFLICT

## s15 — PRD cho sản phẩm AI cần thêm

bốn mục — và một mục mới hẳn
TRADITIONAL PRD AI-NATIVE PRD BỔ SUNG TẠI SAO CẦN THÊM
Goals & success metrics Evaluation Rubric AI không có conversion rate — cần rubric
+ riêng để đo chất lượng output.
DAU · Conversion · Retention Accuracy %, latency, pass/fail rubric
Golden Outputs
User stories / use cases “As a user, I want” không test được — cần
+ Input → expected output cụ thể, test được output mẫu thật để eval.
Luồng người dùng · Acceptance criteria
ngay
Functional requirements Prompt Logic & Tools AI cần biết cách xử lý edge case — không
+ chỉ “tính năng là gì”.
Feature list · Business logic System instructions, API tools, failure rules
Open questions Dataset Strategy “Chưa rõ” phải thành “cần thu thập dataset
Câu hỏi chưa rõ Unknowns → dataset cần thu thập để eval này”.
Edge Case Handling
AI fail theo nhiều cách — PRD phải định
(không có tương đương) MỚI Khi model fail — thất bại thế nào là chấp nghĩa “fail gracefully” nghĩa là gì.
nhận được?
“PRD định nghĩa quality bar — không chỉ danh sách tính năng.”

## s16 — Một AI PRD hoàn chỉnh — Support Ticket Triage v1.0

Sample AI PRD — v1.0 Status: Prototyping
Quality bar viết thành số, không phải tính từ
1 Problem & Business Value — 4 giờ/ngày tag tay →
agent phân loại real time Accuracy > 92% Sentiment > 85% Latency < 2s
2 Prompt Logic & Dataset — system instruction + 50 Hallucination = 0%
golden tickets đính kèm
3 Tool Specification — 4 API agent được phép gọi, và
để làm gì Fail gracefully được thiết kế trước
4 Evaluation Criteria — target đo được cho từng Confidence < 0.7 → không auto-tag, chuyển Needs Human
metric Review · audit tay 5% ticket mỗi tuần · nút “Tag này đúng
5 Edge Cases Handling — fallback khi model không không?” cho support.
chắc chắn
6 Prototype & Early Findings — những gì chạy thử dạy
cho spec PRD viết SAU khi prototype
7 Technical Constraints — PII scrubbing, cost < Findings thật quay lại sửa spec: input quá ngắn gây hallucinate
$0.01/ticket → thêm chế độ hỏi lại · 20% ticket có 2 issue → cần multi-label
· sarcasm → thêm 5 ví dụ vào golden dataset.
■ Mục 4–6: phần không tồn tại trong PRD truyền thống

## s17 — Định nghĩa tiêu chí chất lượng

Thu hẹp scope tới mức viết được rubric ngay.

## s18 — Thu hẹp scope đến khi viết được rubric

Unit of AI Work — đầu việc AI cụ thể mà ta muốn giao, đo và chịu trách nhiệm cho nó.
✓ Đủ hẹp — viết được rubric ngay
✕ Quá rộng — không eval được
Trả lời câu hỏi về AI evals từ course corpus, phân biệt
“AI hữu ích”
rõ nội dung bài giảng với research bên ngoài
Hữu ích theo cách nào? Với ai? Trong context nào?
User goal rõ · Input rõ · Output quan sát được · Failure xác định
được
“Agent trả lời tốt”
Tốt theo tiêu chí nào? Không so sánh hay đo được.
Phân loại ticket support vào đúng queue và
escalation level
“Trải nghiệm thông minh”
Input: ticket text · Output: queue + level · Failure: sai queue, bỏ
Không có output quan sát được, không có failure rõ ràng. escalation
“Đánh giá AI assistant”
Tạo itinerary khả thi theo ngân sách và thời gian di
Một assistant làm hàng chục loại task — mỗi cái một rubric
chuyển đã cho
khác.
Constraint rõ · End state quan sát được · Failure cost xác định

## s19 — AI Flywheel — bánh đà cải thiện liên tục sau launch

01
User Monitoring &
04 Feedback
Offline Evals
Unit test cho agent — thử ▶ Tín hiệu production:
thumbs, hành vi sau output,
mọi thay đổi trước khi ship. ngữ nghĩa hội thoại.
NORTH STAR
Agent Success
Composite: feedback +
hành vi + ngữ nghĩa hội
thoại
03
Reference Datasets
▶ 02
Trace Analysis
Golden outputs + edge case Nguồn sự thật — đọc trace
chưng cất từ trace thật. theo user intent, gắn mã
error mode.
“Những sản phẩm AI tốt nhất không tự nhiên đã tuyệt vời ngay từ đầu — họ xây một AI Flywheel Framework · Calibre Labs
flywheel để liên tục cải thiện theo thời gian.”

## s20 — Thiết kế coverage &

candidate scenarios
Chọn biến làm agent phải hành xử khác đi, trước khi viết
test prompt.

## s21 — Vấn đề của việc “hãy tạo 50 test prompts”

Dataset nhiều rows chưa chắc có coverage tốt.
✕ LLM-generated dataset ✓ Real production dataset
Trông nhiều — thực ra rất đồng nhất. Ít rows hơn — coverage thật sự.
happy path A variant 1 near-dup edge case persona B happy path
vs
happy path B variant 2 duplicate ambiguous biz rule multi-intent
happy path C duplicate near-dup real trace zero-hit stale source
50 rows ≈ 3 real cases 20 rows = 20 real cases
Đo được: xin LLM 4.000 ý tưởng về một chủ đề → chỉ còn ~200 ý không trùng lặp — khả năng tự sinh đa dạng bão hoà rất nhanh (Si
& Yang 2024).

## s22 — User Input Grid — những biến

làm agent phải hành xử khác đi
CONTEXT
WHO
Language / Ngôn ngữ, timezone, currency, policy
Persona / ICP Ai đang dùng? Goal và expertise khác locale region?
nhau thế nào?
Data freshness Context mới, cũ, hay không rõ timestamp?
WHAT
User intent User đang cố hoàn thành task gì? RISK
HOW — CHẤT LƯỢNG INPUT Failure cost Hậu quả khi sai là thấp hay cao?
Context richness Đủ dữ liệu, thiếu, hay mâu thuẫn?
Permission state User hoặc system có quyền thực hiện
action không?
Ambiguity Request rõ hay có nhiều cách hiểu?
OUTPUT
Complexity Một intent hay nhiều? Đơn bước hay đa
bước? Expected Act · Ask · Don’t act
agency

## s23 — Quy trình tạo User Input Grid

Thiết kế coverage trước khi viết test prompt.
BƯỚC 1 BƯỚC 2 BƯỚC 3 BƯỚC 4 BƯỚC 5
Chọn dimensions Định nghĩa values Tạo combinations Thêm constraint Viết thành user
Yếu tố nào làm Đổi value thì câu trả Giữ lại combination đời thật inputs
expected behavior lời đúng cũng phải khi: Làm scenario bớt LLM chỉ paraphrase
thay đổi? đổi theo. “sạch”, giống user — cùng scenario,
thật. nhiều cách diễn đạt.
Hỏi mà không rõ bài
Có slide trả lời trực Có khả năng xuất hiện nào
Loại câu hỏi của user tiếp thật Slide và transcript
Độ phủ tài liệu khóa Cần tổng hợp nhiều Làm agent phải đổi dùng thuật ngữ khác
học module chiến lược ngắn / dài
Source cũ vẫn đứng
Có cần research ngoài Course chỉ cover một Failure cost cao đầu retrieval formal / informal
không phần Team chưa chắc Answer đúng nhưng tiếng Việt / tiếng Anh
Ngôn ngữ và expertise Course chưa đề cập quality boundary follow-up lặp lại beginner / advanced
✕ Không giao cho LLM tự chọn test coverage — human kiểm soát coverage, LLM chỉ diễn đạt lại.

## s24 — Từ grid tới Candidate Scenario Bank

CẤU TRÚC MỘT S CENARIO BA LOẠI S CENARIO
SC-042 Challenge Representative scenarios
Gần với cách user thường hỏi — về sau phải phản ánh
NATURAL-LANGUAGE INPUT production distribution.
“Trong bài có nói sâu về retrieval không, hay chỉ là giới thiệu?”
GRID COMBINATION Challenge scenarios — cố ý over-sample
intent: clarify · coverage: partial · external-research: no ·
Ambiguous inputs Source conflicts
stage: mid-course
Retrieval zero-hit Multi-intent requests
EXPECTED BEHAVIOR
Stale external sources Follow-up lặp hoặc sai scope
Hỏi lại để xác định “bài nào”, rồi trả lời trong phạm vi tài liệu
— không tự suy thêm. Pass rate trên challenge set không phải production success
rate.
WHY INCLUDED
Ambiguous reference cộng partial coverage — failure cost
cao nếu agent tự đoán.
Critical regression candidates
Claim ngoài bị nói thành nội Citation không support claim
dung đã dạy
Agent reasoning từ false View source dẫn tới source
premise không liên quan
Coverage đến từ cách chọn dimension và combination — không đến từ số lượng rows.

## s25 — Chạy agent, đọc trace,

chuẩn hoá chất lượng
Đừng bắt đầu bằng automation — đọc trace trước.

## s26 — Trace là gì, và vì sao PM phải đọc trace

Trace là record đầy đủ của một lần agent thực hiện task.
NHÓM THÔNG TIN VÍ DỤ
User input User hỏi gì, ngữ cảnh ban đầu là gì
câu hỏi
vs
Instruction & config System prompt, model, tool version,
câu trả lời cuối
prompt version
Context Slide, transcript, policy, external sources
TRANSCRIPT TRACE
Thứ user nhìn thấy Toàn bộ những gì system Model calls Gọi lúc nào, với input nào
làm bên trong
Tool usage Tool nào, parameter, output, có lỗi không
Intermediate steps Phân loại intent, chọn nguồn, tổng hợp,
validate
Final response Câu trả lời cuối user nhìn thấy
Outcome / end state Ticket chuyển queue? Citation đúng?
Itinerary khả thi?
NGU Y CƠ Metadata Latency, token, cost, timestamp
Final response nhìn ổn nhưng trace bên trong sai —
Feedback User correction, rating, retry, complaint
chỉ đọc câu trả lời cuối là không đủ.

## s27 — Một trace đọc ra sao

trace SC-042 · 4.2s · 3 tool calls
NẾU CHỈ ĐỌC TRANSCRIPT
1 USER INPUT “Trong bài có nói sâu về retrieval không?”
Câu trả lời trôi chảy, đúng ngữ pháp, nghe
có thẩm quyền — không thấy vấn đề.
2 INTENT classified: course_content_lookup
3 TOOL: top hit: blog post ngoài khoá học (2023) ĐỌC TRACE MỚI THẤY
RETRIEVAL slide của bài không nằm trong 5 kết quả đầu
Lỗi bắt đầu ở bước 3: retrieval lấy nguồn
4 SYNTHESIZE Tổng hợp từ nguồn ngoài, không kiểm tra lại nguồn ngoài. Bước 4 và 5 chỉ là hệ quả.
nội bộ
5 FINAL “Bài có nói khá sâu về retrieval, gồm ba chiến NÊN SỬA Ở ĐÂU
RESPONSE lược…”
Sửa retrieval và thêm bước xác nhận nguồn
6 FEEDBACK thumbs-down: “bài không có phần này” — không sửa câu chữ của response.

## s28 — Từ chạy thử agent đến rubric đánh giá

VÒNG 1 — KHÁM PHÁ BEHAVIOR VÒNG 2 — CHUẨN HOÁ
STEP 1 STEP 2 STEP 3 STEP 4 STEP 5
Chạy bộ tình Đọc trace, ghi Gom nhóm Xác định lỗi bắt Biến pattern thành
huống test nhận tự do pattern lặp lại đầu từ đâu tiêu chí
Tình huống phổ biến, Chưa chấm điểm. Lỗi hay mắc, điểm Bước cuối còn đúng Trace codes, định
khó, rủi ro cao. Cố Ghi điều bất ngờ, lỗi chất lượng yếu, là gì? Bước đầu tiên nghĩa pass/fail, ví dụ
định prompt, model, rõ ràng, behavior behavior tốt cần giữ, sai là gì? Đâu là đúng và sai, rubric,
tool, version tốt, kèm evidence cụ nhóm scenario bị nguyên nhân, đâu là human label có cấu
dataset. thể. ảnh hưởng. hệ quả? trúc.
Output: notes thô có Output: failure / Output: root-cause Output: trace codes +
Output: traces đã log evidence success patterns map rubric v1
✕ Đừng chạy vài prompt ngẫu nhiên rồi gọi đó là eval — phải biết mình đang test loại tình huống nào.

## s29 — Chuẩn hoá notes thành trace codes

Trace codes — ngôn ngữ chung của team
Cùng một vấn đề, cùng một tên.
wrong_intent
Notes tự do sau vòng discovery Agent hiểu sai nhu cầu chính của user
Mỗi người nói một kiểu.
“con bot này xử lý sai ý khách” missing_lookup
Không tra cứu dữ liệu trước khi trả lời
“nó hơi bị lạc hướng”
“nó không hiểu khách muốn đổi hàng” formalize premature_commit
“agent trả lời mà không tra cứu đơn” Hứa kết quả khi chưa đủ điều kiện
“agent hứa hoàn tiền quá sớm”
missing_escalation
“agent không chuyển human khi phức tạp”
Không chuyển human khi vượt thẩm quyền
Khó đo Khó so sánh Khó sửa
no_next_step
Đúng policy nhưng thiếu hành động tiếp theo
Đo được So sánh được Sửa được

## s30 — Taxonomy phải tuỳ theo use case

Không có một taxonomy dùng chung — xây từ trace analysis của chính mình.
AI Support đơn hàng AI Learning Assistant AI Travel Planner
Xoay quanh: intent · order · policy · Xoay quanh: retrieval · grounding · Xoay quanh: feasibility · data ·
authority boundary authority
wrong_intent wrong_question_intent missing_constraint
missing_order_lookup poor_retrieval stale_live_data
policy_misapplied unsupported_claim infeasible_schedule
premature_refund_commit external_boundary_violation budget_violation
missing_escalation poor_followup_quality booking_overreach
unclear_next_step missing_recovery
Đừng copy taxonomy từ bài khác — dùng trace analysis để xem use case của mình thật sự fail ở tầng nào.

## s31 — Notion AI

Một team coi evals là IP của mình.

## s32 — Notion AI dành 90% thời gian cho evals

Chỉ 10% là viết prompts.
100M+ 60% < 1 ngày
users toàn cầu users không nói tiếng Anh để ship model mới
Scale khổng lồ — không thể test 100% engineer nói tiếng Anh — buộc Evals tự động cho biết ngay prompt
bằng tay hay intuition. phải dựa vào evals. nào regression khi model mới ra.
“Evals is our IP — everything we build, how we decide if those work well, lives inside Braintrust.”
Sarah Sachs — AI lead, Notion
Nguồn: How to build world-class AI products — Sarah Sachs (AI lead @ Notion) & Carlos Esteban (Braintrust)

## s33 — Evals là user research mới của PM

“You can think of this as your version of User Research.” Sarah Sachs — AI lead, Notion
EVALS AS USER RESEARCH — CÁCH NOT ION LÀM
USER RESEARCH TRU YỀN THỐNG
Thumbs-down data
User interviews Natural-language request thật từ user — không phải câu
Hỏi user nghĩ gì — không phải user thật sự làm gì. hỏi PM đặt ra trước.
Surveys Behavior thật, không phải claimed behavior
Số lượng lớn nhưng context nghèo — khó biết tại sao user User muốn draft report, không chỉ research — tìm ra từ
không hài lòng. data, không từ interview.
Chậm và tốn kém Real-time, liên tục
Vài tuần để có insight — không kịp với tốc độ release AI. PM ngồi trong eval tool mỗi ngày — insight cập nhật theo
từng release.
PM không cần viết scoring function — nhưng phải là người đọc data và escalate findings. Việc này không ai làm thay
được.

## s34 — Notion quản lý evals như thế nào — ai làm gì

BƯỚC PRODUCT MANAGER ENGINEER DATA SPECIALIST
1 · Decide Đọc thumbs-down data và usage Xác định cải tiến cần làm — ví dụ —
Xác định vấn đề log để tìm điểm cần cải thiện. thêm một connector mới.
cụ thể
2 · Curate Kiêm luôn vai data specialist ở — Tạo dataset từ log thật. Bắt đầu
Tạo targeted team nhỏ. với 10 samples, format đúng trước.
dataset
3 · Score — Viết scoring function sau khi đã Viết judge prompt riêng cho từng
Gắn scoring nhìn data lâu. Mix LLM-as-judge và sample — tốn công nhưng sâu hơn
functions heuristic. nhiều.
4 · Inspect Phát hiện pattern thật, rồi escalate Đưa failures vào một LLM để tóm Human label failures. Quality quan
Review failures kỹ findings lên roadmap. tắt theme, ra báo cáo nhanh. trọng hơn quantity.
↺ Loop trở lại bước 1: chỉnh prompt theo failure theme, thêm rows dataset từ log mới.

## s35 — Data lấy từ đâu, và dùng theo nguyên tắc nào

LẤY DATA TỪ ĐÂU BA NGU YÊN TẮC KHI DÙNG DATA
1 Dog-fooding — data tự nhiên Bắt đầu nhỏ: 10 samples, không phải 1000
Format đúng trước — dummy data sai cấu trúc là sai từ gốc.
Team dùng sản phẩm của mình hàng ngày, nên mọi
interaction đều là data tiềm năng. Không cần giả lập
hay synthetic data từ đầu. Quality quan trọng hơn quantity
Đặc biệt khi fine-tuning — ít sample tốt hơn nhiều sample kém.
2 Thumbs-down — signal từ user Data flywheel tích lũy theo thời gian
Mỗi release thêm log mới, dataset lớn dần, evals ngày càng
Chỉ lấy natural-language request, không lấy output
chính xác hơn.
cũ vì output lỗi thời rất nhanh. Request thật của user
là tài sản dài hạn, dùng lại được mãi để eval model
mới.
“The people closest to the data should be the ones
creating the dataset.”
Sarah Sachs — AI lead, Notion

## s36 — Có hệ thống evals thì thay đổi những gì

✕ Trước
✓ Sau — với hệ thống evals
Dùng spreadsheet để label data
Model mới ship trong một ngày
Human labeler quá tải, phải parse prompt bằng công thức
Chạy toàn bộ evals, biết ngay regression, đổi model tự tin.
bảng tính.
Tự tin build cho user đa ngôn ngữ
Model mới cần vài tuần để validate
Multilingual evals đảm bảo chất lượng cho ngôn ngữ
Không biết prompt nào regression — phải test thủ công
engineer không nói được.
từng cái.
Insight sản phẩm đến từ data
Ship dựa trên gut feeling
User muốn draft report — phát hiện từ thumbs-down,
Chạy tốt trong demo — không biết có nhất quán với user
không từ interview.
thật không.
“I don’t think that we could exist without a tool like this today — it is critical to our iteration flow, and it actually is
our IP.”
Sarah Sachs — AI lead, Notion

## s37 — Automated Evaluators

Khi nào nên automate · Code-based vs LLM-judge · Common
mistakes

## s38 — VẤN ĐỀ MỚI

Manual review không thể scale
GIAI ĐOẠN ĐẦU SAU KHI S CALE
~100 traces / tuần 100k production traces
✓ Hiểu được patterns ✕ Không thể review hết
✓ Manual review khả thi ✕ Không thể chậm mỗi release
AUTOMATION MUA LẠI Ship nhanh hơn — chạy eval thay vì tranh luận Bắt drift và regression trước khi user thấy
Đo được → cải thiện được
⚠ Build quá sớm → mất thời gian đo sai thứ ⚠ Build sai → false confidence, system fail âm thầm

## s39 — Không phải vấn đề nào cũng cần eval

Ba câu hỏi trước khi viết eval cho một trace category — chỉ generalization gap mới đáng tự động hoá.
CÂU HỎI 1 · SPECIFICATION CHECK Specification gap — thiếu đặc tả
Prompt có được giao xử lý tình huống này KHÔNG Sửa system prompt — chưa cần viết eval.
không? Email drafter không tạo subject line vì prompt chưa hề yêu
cầu.
Có, prompt đã rõ
CÂU HỎI 2 · SYSTEM CHECK Architectural issue — thiếu năng lực hệ thống
Agent có bao giờ làm được việc này không? KHÔNG Engineering fix — thiếu tool, integration, hoặc model
BAO GIỜ capability.
Calendar API chưa connect — prompt rõ đến đâu cũng
không làm được.
Có lúc làm được
CÂU HỎI 3 · GENERALIZATION CHECK Generalization gap — thiếu tính nhất quán
Lúc được lúc không — dù prompt đã rõ? CÓ Viết automated eval ✓ — đây là ứng viên phù hợp.
Email drafter đôi khi cá nhân hoá đúng, nhưng chỉ ở case rất
rõ ràng.

## s40 — Chọn cách đánh giá: Code-based hay LLM-as-Judge?

Nếu có thể kiểm tra bằng code — hãy dùng code trước.
CODE-BASED — MẶC ĐỊNH ƯU TIÊN LLM-AS-JUDGE — KHI CODE KHÔNG ĐỦ
Nhanh hơn Rẻ hơn Ổn định Dùng khi tiêu chí phụ thuộc vào sắc thái ngôn ngữ và
ngữ cảnh — không thể viết thành rule rõ ràng.
Dễ gắn critical path Dễ debug
CODE KHÔNG LÀM TỐT
CODE LÀM TỐT Câu trả lời có hữu ích với đúng người dùng không?
Có đúng format không Explanation có hợp lý và nhất quán không?
Có thiếu trường bắt buộc không Cách diễn đạt có đủ thuyết phục không?
Có gọi đúng tool không Output có đúng brand voice không?
Có lộ thông tin cấm không
Có trả lời sai schema không
Rule rõ, kiểm được bằng code → dùng code Cần sắc thái, ngữ cảnh → LLM Judge

## s41 — Tiêu chí nào giao được cho máy? Hỏi một câu duy nhất

“Tiêu chí giao được cho máy khi và chỉ khi nó có một referent kiểm chứng được — một thứ bên ngoài phán
đoán của model mà kết luận có thể quy về.”
Tài liệu nguồn → chấm được tính đúng Bộ quy tắc rõ ràng → chấm được hình thức
Referent = “phán đoán của người” → không bao giờ giao máy chấm
REFERENT RÕ, TÁCH NHỎ ĐƯỢC REFERENT MỘT PHẦN KHÔNG CÓ REFERENT
Máy chấm — người kiểm mẫu Máy sàng lọc — người thẩm Người quyết — máy nêu bằng
Máy ra quyết định; người kiểm ~10% định chứng
ngẫu nhiên để canh drift. Máy xếp hạng nghi ngờ và nêu bằng Máy không được xuất điểm số — chỉ
chứng; người quyết mọi case bị cờ. xuất dữ kiện trung gian cho người
xem.
Tổng hợp từ khảo sát 239 tài liệu về LLM-as-a-judge (2024–2026)

## s42 — Code-based Evaluation

Deterministic checks chạy tự động trên mọi prompt change — nền
tảng không thể thương lượng của eval suite.

## s43 — Ba phần của một code-based eval

① Input — lấy đúng phần cần kiểm tra
Output string, JSON, tool calls — hoặc kết hợp cả user input khi
① INPUT cần kiểm tra theo ngữ cảnh.
def check(output_str, user_input):
② LOGIC ② Logic — rule đủ rõ để máy quyết định
if "Subject:" not in output_str: Condition, pattern match, schema validation — nếu viết được
“phải có X” hay “đúng format Z” thì dùng code.
③ RESULT + REASON
return False, "Missing subject line"
return True, None
③ Result — pass/fail kèm reason string
Reason string không phải “có thì tốt” — khi fail ở trace 38/50,
team phải biết ngay tại sao, không cần mở lại trace để đoán.

## s44 — Category checking — Support Triage Agent

Agent phải chọn đúng 1 trong 3 labels: Technical · Billing · Feature Request
VALID = {"Technical", "Billing", "Feature Request"} Danh sách labels được phép
def check_category_label(output: str) -> dict: Chỉ 3 giá trị exact string. “billing issue” hay “tech problem”
không được tính.
found = [c for c in VALID if c in output]
if len(found) == 1: Đếm bao nhiêu label xuất hiện
return {"pass": True, Quét output, gom tất cả label tìm thấy — rỗng, 1 phần tử,
"reason": f"Single valid: {found[0]}"} hoặc nhiều hơn.
elif len(found) == 0:
return {"pass": False, Ba trường hợp, một kết quả rõ ràng
"reason": "No valid category found"} pass Đúng 1 → ghi rõ label nào
else: fail Không có → “No valid category found”
return {"pass": False,
fail Nhiều hơn 1 → liệt kê cụ thể để debug
"reason": f"Multiple labels: {found}"}

## s45 — Bốn nơi nên bắt đầu với code-based evals

Đủ field, đúng format, đúng schema, trong giới hạn cho phép.
Output có đúng cấu trúc STRUCTURE /
Quan trọng khi output đi tiếp vào UI, database hoặc downstream
không? FORMAT
system.
Có nhắc đúng product name, ticket ID, required policy, source,
Output có đủ phần bắt PRESENCE /
next step? Bắt những output nghe ổn nhưng chưa đủ để user hành
buộc không? COVERAGE
động.
Agent có đi đúng quy trình TOOL-CALL / Gọi đúng tool, đúng thứ tự, đúng parameter. Nhiều lỗi không nằm ở
không? SEQUENCING câu trả lời cuối mà nằm ở cách agent thực thi workflow.
Latency, cost, token count, confidence score có vượt ngưỡng
Chỉ số vận hành có trong
THRESHOLD CHECKS không? Trả lời đúng nhưng chậm hơn hoặc đắt hơn nhiều vẫn là
ngưỡng không? regression.
Output phải dùng được · nội dung phải đủ ý · quy trình phải đúng · chi phí phải trong ngưỡng.

## s46 — Case study — ba kiểm tra tự

động cho Support Triage Agent
KIỂM TRA 1 KIỂM TRA 2 KIỂM TRA 3
Câu trả lời có dùng đúng nhãn Agent có bịa thông tin không Thời gian phản hồi có còn
chuẩn không? có trong yêu cầu không? trong ngưỡng không?
Phải chọn đúng một trong ba nhãn. So sánh mã ticket trong câu trả lời Câu trả lời đúng nhưng chậm hơn
Diễn đạt lại sẽ làm hỏng hệ thống với mã trong yêu cầu ban đầu. nhiều vẫn là lỗi cần bắt.
phân loại phía sau.
✓ Đúng ✓ Đúng
Danh mục: Billing — khách khiếu Yêu cầu có TKT-00421 · câu trả lời ✓ Đúng
nại hoá đơn tháng 3. chỉ nhắc TKT-00421. Thời gian 1.1 giây · ngưỡng tối đa
2.0 giây.
✕ Không tìm thấy nhãn hợp lệ ✕ Bịa ra mã TKT-00422
“Đây có vẻ là vấn đề liên quan đến Yêu cầu có TKT-00421 · câu trả lời ✕ Vượt ngưỡng 2.0 giây
thanh toán.” nhắc TKT-00422. Thời gian 2.4 giây.
Sau khi cập nhật prompt: cả ba pass → mới xem Đây là mức sàn tối thiểu — câu hỏi tinh tế hơn vẫn cần người đọc
xét release. và đánh giá.

## s47 — Đọc kết quả eval trên dataset

Pass rate tổng là bao
nhiêu? TÍN HIỆU TỐT CẦN XEM LẠI
So với phiên bản production
✓ Pass rate bằng hoặc cao hơn baseline ✕ Pass rate tụt đáng kể dù spot check trông
Failures tập trung ở đâu? ổn
Nhóm input nào đang fail
nhiều? ✓ Failures rải đều — không nhóm nào nổi bật ✕ 80%+ failures từ cùng một loại input →
failure mode cụ thể
Lỗi có đi cùng nhau
không? ✓ Failures phân tán, không row nào fail nhiều ✕ Cùng row fail 2+ evals → cụm input khó,
Row nào fail nhiều evals cùng evals không phải lỗi rời rạc
lúc?
✓ Kết quả nằm trong range hợp lý, khớp Pass rate = 0% → kiểm tra eval trước!
Kết quả có bất thường expectation Regex sai, field sai — đừng vội điều tra agent.
không?
Pass rate = 0% hoặc quá thấp

## s48 — Không cần 100% — pass rate là một quyết định sản phẩm

Cùng một con số 90% — là thành công với sản phẩm này, là thảm hoạ với sản phẩm khác.
Gợi ý nội dung sáng tạo
User chọn — lỗi gần như miễn phí
80%
Email draft — có người duyệt
Human review đứng chắn phía sau
90%
Tư vấn y tế, tài chính
Một lỗi = mất niềm tin, rủi ro pháp lý
99,9%
NGƯỠNG PHỤ THUỘC Chi phí của một lỗi Có human review phía sau không Ai là người chịu rủi ro
“Pass rate không phải chỉ số kỹ thuật — đó là mức rủi ro bạn chọn chấp nhận thay cho user.”

## s49 — Đưa code evals vào quy trình release

NGU YÊN TẮC 1 NGU YÊN TẮC 2
Eval là release gate, không phải kiểm Chốt ngưỡng trước khi bắt đầu
tra tuỳ hứng iterate
Mỗi prompt change hoặc model upgrade chạy Quyết định sau khi thấy số thì không còn là
lại eval tự động. Mọi thay đổi đi qua cùng một tiêu chuẩn. Viết ngưỡng ra trước: nhãn >90%,
tiêu chuẩn — không chờ đến sát release. 0 lỗi bịa nghiêm trọng, latency <2s.
Pass → Ship Fail → Dừng “78% cũng ổn mà” — không phải threshold, là
thương lượng.

## s50 — LLM Judge Calibration

Hiệu chỉnh bộ chấm để biết nó có đúng, không chỉ biết nó nghĩ gì.

## s51 — Vì sao calibration là bước cốt lõi

VÍ DỤ · 10 TRACES
Pass rate chỉ cho biết judge đang nghĩ gì ✓ ✓ ✓ ✓ ✓ ✓ ✕ ✕ ✕ ✕
Thấy 85% pass rate không có nghĩa là đã đo được chất
Người có chuyên môn đã chấm: 6 output tốt · 4 output xấu
lượng thật.
Trong 6 output tốt, judge đồng Trong 4 output xấu, judge
Calibration mới cho biết judge có đúng không
ý mấy lần? phát hiện mấy lần?
So kết quả của judge với đánh giá của người có chuyên
5/6 = 83% 3/4 = 75%
Chưa calibrate còn nguy hiểm hơn không có
1 output tốt bị nhầm là xấu 1 output xấu bị nhầm là tốt
Tạo cảm giác chắc chắn sai — đang dùng hệ thống chưa
kiểm chứng để ra quyết định ship.
Cả hai cùng cao → judge đủ tin cậy. Một bên thấp → biết rõ
lệch ở đâu để chỉnh.

## s52 — Nhìn xem judge đang lệch ở đâu

Calibration giúp biết judge sai theo hướng nào — không chỉ biết “chưa tốt”.
THẬT SỰ TỐT THẬT SỰ XẤU
Judge nói TỐT
✓ Đúng ⚠ Cho qua lỗi — nguy hiểm nhất
Nhận ra đúng output tốt Team tưởng ổn, lỗi thật vẫn lọt production
Judge nói XẤU
⚠ Chặn nhầm — tốn thời gian ✓ Đúng
Team đi sửa thứ không phải vấn đề thật Bắt đúng output xấu
Judge chưa calibrate thường quá dễ dãi — xu hướng chấm tích cực hơn mức nên có, trừ khi prompt được thiết kế rõ để
buộc khắt khe với failure.

## s53 — Ba sự thật khó chịu về LLM judge

Judge dễ dãi, không phải nhiễu “85% đồng thuận” ≠ ngang Thiên vị “người nhà”
người
96% nhận đúng output tốt Tỉ lệ khớp thô cao hơn hệ số κ đã
Judge có xác suất cho qua lỗi của
chính họ model mình cao hơn trên
<25% bắt được output lỗi hiệu chỉnh ngẫu nhiên tới 33–41
điểm — “85% khớp” thường chỉ là κ
50%.
≈ 0.45–0.52.
Judge lặp lại rất ổn định — cùng một
Rủi ro là cho qua lỗi — đúng ô nguy sai lầm. Ổn định không phải là đúng. Quy tắc: generator và judge phải
hiểm nhất trong ma trận slide trước. khác họ model.
Norman 2026 · 541.000 phán đoán, 21
Jain 2025 judge Pombal 2026
Hệ quả cho hội đồng nhiều judge: đừng lấy đa số phiếu — đa số thừa hưởng sự dễ dãi. Một model gắn cờ là đủ để đưa case
cho người xem.

## s54 — Sáu bước calibration

MỤC TIÊU
Không phải để
judge “nghe có vẻ
1 Chọn 50–100 traces đại diện 2 Expert gắn nhãn Pass/Fail hợp lý hơn”
Case dễ lẫn khó, có cả trường hợp mơ hồ. Đúng theo tiêu chí đánh giá đang đo. Calibration là để biết
judge có chấm đủ gần
chuẩn của team chưa.
3 Chạy judge — lưu verdict và 4 So sánh chỗ bất đồng với expert
reasoning Bước quan trọng nhất — thấy judge lệch Có một judge mà
Kèm human label để đối chiếu. theo kiểu nào. team dám tin khi ra
quyết định.
5 Sửa prompt theo pattern sai 6 Kiểm tra trên tập riêng → baseline Mẹo: checklist
Đổi ít một — biết rõ cái nào có tác dụng. Chưa ổn thì quay lại bước 4. có/không thắng thang
điểm
Câu hỏi nhị phân, quy lên
điểm — κ 0.60→0.74
(Chen 2026).

## s55 — Calibrate judge không cần hạ

tầng — một spreadsheet là đủ
calibration_round_3.xlsx 1 Gửi expert 25–50 case, vài ngày một lần
Kèm cả verdict và lý do của judge để expert phản biện.
OUTPUT CỦA AGENT JUDGE EXPERT
2 Chỉ đào sâu chỗ hai bên bất đồng
Hoàn tiền đúng chính sách, giải thích rõ ✓ ✓ Bất đồng cho biết judge hiểu sai tiêu chí ở đâu — hoặc
tiêu chí đang mơ hồ.
Đúng chính sách nhưng bỏ sót câu hỏi thứ
hai
3 Sửa prompt của judge, đo lại vòng sau
Từ chối một yêu cầu hoàn toàn hợp lệ ✕ ✕ Theo dõi tỉ lệ đồng thuận tăng dần qua từng vòng —
ngay trong spreadsheet.
■ Dòng bất đồng — nơi duy nhất đáng đào sâu
Tham chiếu: Hamel Husain — Your AI Product Needs Evals

## s56 — Khi nào LLM Judge đã chạm trần?

Nhận ra thời điểm này quan trọng — tránh tốn thời gian tối ưu thứ không còn cải thiện được.
DẤU HIỆU 1 DẤU HIỆU 2 DẤU HIỆU 3
Model không thật sự hiểu Thêm prompt mà chất lượng Ngay cả humans cũng chưa
domain gần như không nhích thống nhất
Reasoning strings cho thấy model Effort tăng nhưng improvement Trên tiêu chí cảm tính, chính các
thiếu nền tảng. Ví dụ: đánh giá hầu như bằng không qua nhiều expert chỉ đồng thuận với nhau ở
legal citation hay medical vòng. Đã rút gần hết giá trị có thể mức ICC 0.07–0.18 (Linde 2026).
recommendation — model không lấy từ model này. Judge đạt 0.30 ở đó không hề kém
có năng lực ở domain đó. người — chính tiêu chí đang hỏng.
Đã chạm điểm trần với model này.
Vấn đề là model capacity — không Đo trần người-người trước — bất
phải prompt. đồng cao giữa người là lỗi đặc tả
rubric, không phải cơ hội tự động
hoá.
Vấn đề không còn nằm ở cách viết prompt — mà ở giới hạn của chính model hoặc tiêu chí đang được đánh giá.

## s57 — Khi automation không chạm quality bar

Phân vai rõ giữa ba lớp — không bỏ đo lường.
LỚP 1 — LUÔN BẬT LỚP 2 — ĐÃ CALIBRATE LỚP 3 — FALLBACK
Code-based Evals LLM Judge Human review
Structure, format, safety checks — Tiêu chí đã calibrate đủ tốt — Final gate cho dimension
automation đo tốt. Chạy trên mọi semantic quality ở quy mô lớn. automation chưa chạm. Sample
thay đổi. có chủ đích: output cao nhất và
relevance grounding quality
thấp nhất.
format schema safety
Fallback tạm thời — mục tiêu dài
hạn là judge tốt hơn hoặc tiêu chí
đơn giản hơn.
1 · Sample có chủ đích — đừng review tất cả 2 · Đặt threshold rõ ràng
Review toàn bộ sẽ quá tải. Lấy mẫu đúng chỗ đáng quan tâm: Human review cũng là hệ thống ra quyết định: bao nhiêu
output chấm cao nhất và thấp nhất. reviewers · review bao nhiêu outputs · bao nhiêu % phải đạt.
CHI PHÍ QU YẾT ĐỊNH TẦN SUẤT L1 Code evals — chạy liên tục L2 Human & judge — định kỳ
L3 A/B testing — sau thay đổi lớn Hamel Husain

## s58 — Đưa expert vào loop

Bằng chứng thay điểm số · Remove friction · Label là tài sản

## s59 — Cho expert xem bằng chứng, đừng đưa sẵn điểm số

MÁY XUẤT ĐIỂM SỐ MÁY XUẤT BẰNG CHỨNG
KHI MÁY GỢI Ý SẴN KẾT LUẬN
Tăng chi phí bất đồng — muốn phản Giảm chi phí kiểm tra — chỉ cần liếc
+2.9 điểm chính xác khi AI gợi ý
đúng
bác phải tự dựng lập luận.
“Độ tin cậy: 0.86” → trượt
đoạn được trích.
“Trích chính sách, mục 4.2: hoàn nếu
trễ > 3 ngày” → đạt
−11.3 điểm khi AI gợi ý lệch —
người bị kéo sai theo Phép thử thiết kế: “Output này có giúp expert xác nhận hay bác bỏ nhanh hơn
so với không có nó không?”
Downside gấp ~4 lần upside — điểm
số gợi ý sẵn là can thiệp rủi ro cao.
THỨ TỰ MÀN HÌNH CHỐNG LỆCH Bằng chứng → Người phán đoán →
Jabbour 2023 · RCT, 457 bác sĩ
Mới hiện điểm máy Fogliato 2022

## s60 — “Remove ALL friction” — để expert nhìn data không tốn sức

Review một trace phải mở 4 tab → không ai review đủ nhiều → không ai biết hệ thống fail kiểu gì.
1 Một màn hình đủ ngữ cảnh Review Tool — case 38 / 120
Trace, dữ liệu liên quan, chính sách — gom về một chỗ,
không bắt mở tab. KHÁCH HỎI
“Tôi muốn hoàn tiền đơn #4521, giao trễ 5 ngày rồi.”
2 Ngôn ngữ domain, giấu jargon AI
AI TRẢ LỜI
Expert không cần biết trace, span, tool call là gì để chấm
“Đơn của bạn đủ điều kiện hoàn tiền. Tôi đã tạo yêu cầu, tiền
được.
về trong 3–5 ngày.”
3 Một quyết định nhị phân Đơn #4521 — giao trễ 5 ngày
Đạt / Không đạt — thang điểm chi tiết chậm hơn và khó
Chính sách: hoàn nếu trễ > 3 ngày
quản lý hơn nhiều.
4 Build trong ~1 ngày ✓ Đạt ✕ Không đạt
Đây không phải dự án hạ tầng — một tool nội bộ nhỏ, PM yêu
Phím G / B — một quyết định mỗi màn hình
cầu được ngay.

## s61 — Label của expert là tài sản — dùng lại được ba lần

→ Đo chất lượng thật của hệ thống
Baseline đáng tin trước khi tối ưu bất cứ thứ gì.
ĐẦU VÀO
Vài trăm case expert đã chấm Calibrate LLM judge
Đạt / Không đạt → Bộ chuẩn vàng để biết judge lệch ở đâu — như spreadsheet ở slide
trước.
Thu được rất nhanh khi tool review không còn
friction.
Curate dataset
→ Case fail thành regression test và data huấn luyện cho vòng sau.
“Một giờ review của expert — nếu được thiết kế đúng — là tài sản dùng lại ba lần.”

## s62 — Thứ tự triển khai: code trước, human

định nghĩa, rồi mới scale bằng judge
1 Human review — định nghĩa “good”
Đọc 10–30 trace đa Ghi failure mode, Chọn golden outputs làm
dạng, gắn nhãn ✓ / ~ / ✕ severity, expected chuẩn
CHẠY S ONG S ONG, ĐỘC LẬP
behavior
Codebase ↓ Output: labeled cases + failure patterns
Schema, enum, format
Permission, DB match
2 Tạo rubric và calibration set
Regex: UUID, PII, token
Viết tiêu chí pass/fail rõ Tạo calibration set 50– Bước bắt buộc trước khi
Latency, cost, CI regression ràng, có ví dụ tốt và xấu 100 case có human label dùng LLM judge
Chạy đầu tiên và không cần rubric
↓ Điều kiện: rubric ổn định + human labels
hay human. Bắt lỗi chắc chắn trước
khi chuyển sang hai lớp kia.
3 LLM judge — scale những gì human đã định nghĩa
Đưa rubric và examples Đo precision/recall theo Audit định kỳ với human
vào judge prompt từng failure mode — không set-and-forget
✕ Không dùng LLM judge khi chưa có ✕ Không bỏ human hoàn toàn ở high- ✕ Không dùng code để chấm
rubric stakes judgment

## s63 — Tổng kết

Đo công việc AI làm ra — PM là người định Tự động hoá đúng thứ đáng tự động hoá
nghĩa “tốt” Code là mặc định — judge cho sắc thái, và chỉ
Đọc trace là user research mới — đừng tin lời tin judge sau khi calibrate
agent nói, kiểm trạng thái cuối Judge dễ dãi hơn bạn tưởng — so với trần
Thu hẹp scope đến khi viết được rubric nhị người-người, không so với 1.0
phân cả team chấm giống nhau Expert vào loop: bằng chứng thay điểm số,
Dataset: người cầm coverage, LLM chỉ diễn một nhãn dùng lại ba lần
đạt — phủ độ khó, không phủ tần suất
AI Evals
Model mới ra sáng mai — team bạn có dám ship trong 24 giờ không?
