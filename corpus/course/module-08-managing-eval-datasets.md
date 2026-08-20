---
doc_id: "ai-evals-m08"
title: "Module 8: Managing Eval Datasets"
author: "AI Evals course (external reference)"
type: "course-reference"
source_url: "local: day20/research/evaluation/02-course-ai-evals/module-08-managing-eval-datasets.md"
retrieved: "2026-08-20"
lang: "en"
---
# Module 8: Managing Eval Datasets

## Course Outline

- Intro
- Growing Your Dataset from Production
- Dataset Versioning and Governance
- Recap and Further Learning

---

## Intro

Your evals are only as good as the data you run them on. Automated evals require a dataset of representative traces to produce meaningful results. This module covers how to structure your dataset from day one, what goes into each row, how to grow it from production, and how to prevent contamination that inflates your confidence.

### Your eval suite is only as good as your dataset

The dataset is the single most underinvested part of most eval systems: teams build judges and code evals but feed them stale, unrepresentative data. A typical team will build a few well-designed evals, run them on a dataset of 30 traces that were hand-picked during prototyping, and treat the pass rates as authoritative. The dataset was never representative of real production traffic. It didn't emphasize failure modes.

The pass rates are meaningless because they measure performance on easy, well-formatted inputs that look nothing like the more tricky messages that users might actually send. The 3 mistakes to avoid are as follows:

1. If the dataset doesn't represent the distribution of inputs your agent handles poorly in production, every number you compute on it is suspect.
2. If it isn't labeled correctly, your LLM judge will be calibrated against noise, not signal.
3. If it never gets refreshed, your evals will gradually measure a version of the product that no longer exists.

### Building the Initial Dataset

The source of your traces depends on where you are in the product lifecycle. Before launch, you're working with synthetic and prototype data:

- The AI PRD (which we covered in module 3) defines the user intents and edge cases your agent must handle. Those become your first inputs.
- Run the agent on them, collect the outputs, and you have traces.
- The golden outputs from module 2's vibe-check process are also traces: they represent what "good" looks like for a specific set of inputs.

This gives you a starting dataset of 20 to 50 traces that covers the happy path and the known edge cases.

After launch, production traffic becomes the primary source:
- Real users send inputs you never anticipated: malformed queries, multi-part requests, edge cases from industries or workflows you didn't design for
- Sample production traffic systematically. Don't cherry-pick simple examples. Add bias towards failure cases.
- Use sampling strategically to ensure your dataset includes the full distribution of input types, complexity levels, and user segments.

The transition from synthetic to production data is the most important dataset event. Teams that never make this transition are running evals against a fantasy version of their product.

The internal dataset is clean, well-formatted, and represents the use cases the team was already thinking about. Production data is messy, surprising, and humbling. Plan for this transition from day one.

### Anatomy of a dataset row

Every row in your reference dataset should contain the same core fields. Consistency here makes it possible to run evals programmatically and compare results across experiments. The fields that matter are as follows:

| Field | Description |
|---|---|
| User input | The original query, ticket, or request that triggered the agent |
| Agent output | The full response, including any structured fields, tool calls, or intermediate reasoning |
| Reference/ground truth | For reference-based judges, include the retrieved context or the golden output the judge will compare against |
| Human label (Pass/Fail) | One label per evaluation criterion/trace code |
| Notes field | Free-text annotation for borderline cases, labeler reasoning, or context that future reviewers will need |

### How many traces you need (and when)

There's no universal right number, but there are useful minimums.

- **Start with 30 to 50 labeled examples** from vibe checks and trace analysis (modules 1–4). These seed the dataset with the happy path and the failure modes you already know about.
- **Expand to 100+** for meaningful offline eval pass rates. At this size, you can calculate pass rates that are stable enough to compare across prompt versions. Below 50, a single trace flipping from fail to pass swings the rate by 2 percentage points.
- **200+ for reliable judge calibration** (next module). You need enough labeled data to split into train, dev, and test buckets and still have enough traces in each to calculate reliable TPR and TNR. With fewer than 100, the confidence intervals on your calibration metrics are too wide to be actionable.

**Quality over quantity:** 50 diverse, well-labeled examples beat 500 that oversample easy cases. The marginal value of your 501st routine billing ticket is near zero. The marginal value of your first scanned PDF with handwriting is high.

### Balancing the dataset

Avoid oversampling "happy path" inputs. Your dataset should mirror the difficulty distribution of production, not the frequency distribution.

If 80% of production tickets are straightforward billing questions and 5% are ambiguous multi-issue tickets, your dataset should not be 80% billing. The billing question tickets are easy. The agent handles them well. You already know that.

Intentionally overrepresent the hard cases: edge cases, ambiguous inputs, multi-intent queries, adversarial inputs, and examples from each trace code category identified in module 4.

Track coverage by dimension using the User Input Grid from module 4 to identify gaps. If your UIG has 12 cells and your dataset only covers 7 of them, you know exactly which input types are missing.

### What to Label

Not every trace needs the same labels. What you label depends on what your evals measure.

For code-based evals, you usually don't need manual labels at all. The eval function itself determines pass or fail based on the trace content.

For LLM judges, you need human labels on the specific criterion that the judge evaluates. **Label the criterion, not the trace.** A labeler who's told "rate this response" will apply their own implicit criteria, which may not match the judge's.

A single trace can have multiple labels for different judges. Trace #42 might be labeled Pass for empathy, Fail for actionability, and Pass for factual grounding. Each label corresponds to one eval criterion.

### Dataset Hygiene: Train, Dev, and Test Splits

To maintain a high-quality calibration process, organize labeled data into three distinct buckets with no overlap. This prevents the judge from "cheating" on inputs it has already seen.

| Split | Size (100 traces) | Purpose |
|---|---|---|
| Train set | ~10 traces | Provide a few-shot examples inside the judge prompt |
| Dev set | ~30 traces | Iterate and debug the judge prompt |
| Test set | ~60 traces | Final "blind" validation of accuracy |

**Train set:** Include clear passes, clear fails, and 2–3 edge cases that teach the boundary. Only run against this set for final mathematical validation (TPR/TNR calculation).

**Dev set:** Run the judge against these, review disagreements, and refine the prompt. You can look at these during development without biasing your final validation.

**Test set:** Only run against this set for final mathematical validation (TPR/TNR calculation). **Critical rule: Never look at test set disagreements to refine the prompt. That's what the dev set is for.**

The 10/30/60 split is a starting point for small datasets. As your dataset grows past 200 traces, the proportions can shift (fewer train, more test) because you don't need many more than 10 examples in the judge prompt, but you benefit from a larger test set for tighter confidence intervals on your metrics.

### Why splits matter: contamination risk

Imagine you accidentally include a test set example in your judge prompt. When you calculate TPR/TNR on the test set, the judge sees an example that it's already been trained on. This inflates accuracy metrics because your judge appears to work better than it actually does.

Contamination is subtle. If you read test set failures and then refine the judge prompt to address those specific patterns, you've also contaminated the test set. This is exactly why the dev set exists: iterate there, validate once on the test set.

**Practical rule:** One person manages the test set. Another iterates on the judge prompt using only the dev set. This separation of responsibilities prevents accidental contamination even in small teams.

---

## Lesson 1: Growing Your Dataset from Production

Once your agent is in production, the pipeline for growing your dataset follows five steps:

**Step 1: Sample production traces.** Use a combination of random and signal-based sampling (detailed below). The goal is both breadth (what does typical traffic look like?) and depth (where is the agent struggling?).

**Step 2: Route samples to human review.** The PM, designer, a subject matter expert, or a dedicated labeling team reviews the sampled traces. Keep the review queue manageable: 10 to 20 traces per week is sustainable. 200 at once is not.

**Step 3: Label with Pass/Fail, trace code, and notes.** Apply the annotation rubric for each criterion. Record the trace code category and any annotator notes for borderline cases.

**Step 4: Add labeled examples to the appropriate bucket.** New traces go into the dev set or the test set. The train set should remain small and stable unless you're deliberately updating the judge prompt's few-shot examples.

**Step 5: Periodically refresh the train set with new boundary examples.** As you accumulate more labeled data and discover new edge cases, replace one or two train set examples with traces that better represent the current boundary.

### Smart sampling strategies

Not all production traces are equally useful for growing the dataset. Five sampling strategies, used in combination, give you the best coverage:

- **Random sampling:** catches unknown unknowns. It's the baseline. Start here.
- **Failure-signal sampling:** Prioritize traces flagged by existing evals, traces with low confidence scores, user complaints, or support ticket escalations. These are the traces most likely to expose failure modes your dataset doesn't yet cover.
- **Outlier sampling:** Sort traces by latency, token count, or response length. Review the extremes. Unusually long or short responses often reveal failure patterns.
- **Stratified sampling:** Group traces by user segment, intent type, or product feature. Sample from each group proportionally, but oversample small or rare groups.

### Cadence: how often to refresh datasets

- **Weekly:** Review 10 to 20 traces (outliers and failure signals). This takes 30 to 60 minutes and keeps you connected to what the agent is actually doing in production.
- **Every 2 to 4 weeks:** Full error analysis cycle on 100+ fresh traces. Label them, run your evals, and compare results to the reference dataset.
- **After every major change:** New model, significant prompt revision, new feature, or production incident.
- **After EAP rounds:** Incorporate all labeled examples from the program immediately.

### Early Access Programs as Edge-Case Discovery

The standard Early Access Program answers one question: Does this feature work? The answer is almost always "yes, mostly," because the EAP participants were selected for friendliness, not diversity, and your internal eval dataset was built from clean internal data.

**The eval-first EAP answers a different question: where does this break?**

The IT Service team at a public SaaS company we worked with learned this the hard way. Their internal evals showed 87% task success because their internal docs were well-structured. EAP customers had scanned PDFs, contradictory policies across tools, and domain jargon not in their documentation. Real-world performance was 60%. The gap was entirely in the dataset, not the model.

**Running an eval-first EAP:**

The selection criteria change first. Pick customers who represent maximum diversity: different industries, different data formats (clean vs. messy, digital vs. scanned), different communication styles, different workflow complexity.

The engagement model runs in three phases:

- **Week 1:** Run live screen-sharing sessions. Watch customers use their actual data. Note failures in real time.
- **Week 2:** Shift to structured data collection. Ask each customer to submit 20 representative queries and label the outputs: acceptable, needs edits, or unacceptable.
- **Week 3:** Show customers what you fixed based on their feedback and re-test on their specific edge cases.

**The deliverable: a dataset, not a testimonial.** At the end of an eval-first EAP, you should have 100+ new labeled examples from real usage, 15 to 20 new edge cases added to your reference dataset, and documented failure modes you didn't know existed.

---

## Lesson 2: Dataset Versioning and Governance

Every dataset change should be tracked: what was added, removed, or relabeled, and why. Use Git or a dataset management tool. Timestamp every version.

This matters for reproducibility. When you compare eval results across experiments and one used dataset v3.2 while another used v4.0, you need to know what changed between them. A pass rate drop from 88% to 79% might be a real regression, or it might be that v4.0 added 30 harder traces. Without version tracking, you can't tell the difference.

### Governance policies

**Who can add rows? Who can relabel? Who owns the test set?**

In small teams, these questions feel unnecessary. In practice, even two-person teams benefit from documented answers, because the alternative is discovering six months later that someone relabeled 15 test set traces during a debugging session and your calibration numbers are now untrustworthy.

**Document the labeling rubric alongside the dataset.** When the rubric changes, relabel the affected rows. Old labels that were correct under the old rubric may be wrong under the new one.

**Retire examples that no longer reflect the product.** Deprecated features, architectural fixes that eliminated certain failure modes, and old edge cases from a user segment you no longer serve. Dead examples dilute your pass rates and waste labeling effort. Move them to an archive, don't delete them. You may need them to understand historical eval trends.

### Case Study: Building the Support Triage Dataset

**Phase 1: The prototype dataset (20 traces).**

During the vibe-check stage, the team wrote 20 representative support tickets covering the three categories (Technical, Billing, Feature Request) at varying severity levels. They ran the agent and manually assessed each output. These 20 traces became the golden outputs: the first definition of what "good" looks like.

**Phase 2: The pre-launch dataset (50 traces).**

Trace analysis revealed failure patterns that the original 20 didn't cover: tickets with ambiguous categories, tickets referencing multiple issues, and tickets in non-standard formats. The team generated 30 additional inputs targeting these gaps. The full 50-trace dataset now covers the happy path plus the known failure modes. Code evals established baseline pass rates.

**Phase 3: The calibration dataset (100 traces).**

To calibrate the LLM judges, the team needed labeled data. A support team lead labeled all 50 existing traces on three criteria: empathetic acknowledgment, actionability, and factual grounding. Then the team sampled 50 additional traces from a beta deployment and labeled those, too. The 100-trace dataset was split: 10 train, 30 dev, 60 test. Three rounds of judge calibration on the dev set brought TPR and TNR above 85% for the empathy and actionability judges.

**Phase 4: The production dataset (ongoing).**

After launch, the team samples 20 new traces per week from production, stratified by category and severity. Every month, a support lead labels a batch of 40 to 50 new traces. After three months, the dataset stands at 280 traces, and the distribution has shifted noticeably: 15% of production tickets don't fit cleanly into the three original categories, which triggered a prompt update and new eval criteria.

---

## Lesson 3: Recap and Further Learning

### Key takeaways and definitions

- **The dataset is the foundation.** Every eval result is only as trustworthy as the dataset it runs on. A dataset that doesn't reflect production traffic produces metrics that look good and mean nothing.
- **Three-bucket discipline.** Maintain strict train/dev/test separation with no overlap. Never use test set results to iterate on judge prompts. One person manages the test set, another iterates on the prompt.
- **Quality over quantity.** A diverse, well-labeled 50-row dataset beats a 500-row dataset that oversamples easy cases. Balance difficulty distribution, not frequency distribution.
- **Label the criterion, not the trace.** A single trace should carry separate labels for each eval criterion. A single "good/bad" label throws away the diagnostic value of having multiple judges.
- **Production is your best data source.** Build a pipeline to sample, label, and incorporate production traces into your reference dataset on a regular cadence.
- **EAPs discover edges.** Select for diversity, not customer friendliness. The deliverable is a labeled dataset with new failure modes, not a testimonial.
- **Version everything.** Track every dataset change with the same rigor you'd apply to code changes. Retire examples that no longer reflect the product.

**Eval dataset** — A curated collection of representative traces, labeled with ground-truth verdicts for specific quality criteria, used to measure the performance of code evals and LLM judges.

**Train/Dev/Test split** — The practice of dividing a labeled dataset into three non-overlapping buckets: a small train set for few-shot examples in the judge prompt, a dev set for iteration and debugging, and a held-out test set for final blind validation.

**Dataset contamination** — When information from the test set leaks into the judge prompt or calibration process, inflating accuracy metrics beyond what the judge achieves on genuinely unseen data.

**Dataset versioning** — The practice of tracking every addition, removal, and relabeling in your reference dataset over time, enabling reproducible evaluation and comparison across experiments.

**Eval-first EAP** — An Early Access Program structured around edge-case discovery and dataset building rather than feature validation. Selects participants for diversity, runs structured data collection phases, and produces labeled examples and documented failure modes as its primary deliverable.

In the next module, we will learn how to mathematically validate your LLM judges against human judgment using the confusion matrix method, and what to do when judges hit their ceiling.
