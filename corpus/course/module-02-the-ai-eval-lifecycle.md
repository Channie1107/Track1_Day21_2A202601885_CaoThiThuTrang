---
doc_id: "ai-evals-m02"
title: "Module 2: The AI Eval Lifecycle"
author: "AI Evals course (external reference)"
type: "course-reference"
source_url: "local: day20/research/evaluation/02-course-ai-evals/module-02-the-ai-eval-lifecycle.md"
retrieved: "2026-08-20"
lang: "en"
---
# Module 2: The AI Eval Lifecycle

## Course Outline

- Intro
- Case Study: Support Triage Agent
- Stage 1: "Vibe Checks" (Prototype)
- Stage 2: "Offline Evals" (Build)
- Stage 3: "User Monitoring" (Optimize)
- Demo before Memo: On starting with the Vibe Check
- Recap and Further Learning

---

## Intro

In this module, you will understand the three-stage evaluation lifecycle — vibe checks, offline evals, and user monitoring — and how each maps to a distinct phase of AI product development.

Evaluations must span the entire lifecycle of software development, from the earliest prototype to live production experience.

If we think of these as 3 distinct stages — prototype, build, and optimize — we require distinct evaluation methodologies at each stage: vibe checks, offline evals, and user monitoring.

**Pitfall to avoid:** Most teams either stop at vibe checks or just build one offline evaluation for overall correctness with a relatively small dataset (<100 inputs). This is not sufficient. To be able to experiment quickly and have reliable results, we need to be much more systematic.

---

## Lesson 1: Case Study: Support Triage Agent

Throughout these chapters, we'll use a concrete example to ground each stage of evaluation: a **Support Ticket Triage agent**.

**Support Triage Agent Prompt:**

```
# You are a customer support analyst. Your core tasks are:

Categorize incoming tickets into one of three buckets: Technical, Billing, or Feature Request.

Assign a Sentiment to each user query (Positive, Neutral, Frustrated, Angry).

If the score is Frustrated or Angry, flag for human intervention with an Urgency level (High, Critical).

# Examples <sample of triaged tickets>
```

**What it is:** The triage agent runs in the background and automatically classifies incoming support tickets by intent, sentiment, and urgency. The goal is to eliminate the four hours a day support leads spend manually tagging tickets, so specialists see high-priority issues faster.

Traditionally, the first step towards building such a triage app would have been writing a PRD. Instead, for AI development, we recommend starting with a prototype.

**Prototype:** A prototype for this agent would consist of a very simple prompt and some examples with a connector hooking up sample tickets for triage.

---

## Lesson 2: Stage 1 — "Vibe Checks" (Prototype)

A **vibe check** is a manual review using a few dozen diverse inputs. You run it before writing the PRD, during initial prompt exploration, and the goal is to build intuition about what the system can and can't do — and to seed your first dataset with golden outputs.

Vibe checks are casual but systematic. Rigor matters less than coverage. Which use cases does the model handle well? Where does it consistently fail? What surprising behaviors emerge?

**Typical vibe check workflow:**

1. Generate 10–30 test inputs covering different personas and use cases
2. Run each through your prototype
3. Label each output: ✓ (would ship this), ~ (needs minor edits), ✗ (unacceptable)
4. Take notes on why something passed or failed, and your early findings

Take the Support Ticket Triage agent as an example. Before writing a single line of the PRD, a team vibe-checking this prototype would run a batch of real support tickets through it and immediately discover some patterns. It might look like this:

- Very short inputs (for example, "Help!") cause category hallucinations; we need a neutral "clarification needed" mode
- Accuracy of the category identification seems ok to start at 50–70%
- The sentiment analysis isn't good — it can't detect sarcasm
- If there are multiple categories of requests present in a single ticket, it sometimes drops a label

Those aren't edge cases you can anticipate from a requirements doc — they're things you find by watching the model work. This vibe check will end up shaping the PRD, as we will see in the next module.

Because vibe checks happen before a formal spec exists, they also surface candidates for **"golden outputs"** — the ideal responses/outputs that the Triage agent should generate in a diverse set of cases. By learning where the agent struggles, you discover what should belong in your PRD's reference dataset, both for few-shot learning and evaluation.

An ideal dataset also includes **edge cases**: missing information, contradictory instructions, and unclear intent. For example, entries like:

- "Hello"
- "I hate this app, I want to cancel, but can I get a discount for the Pro plan?"

Such ambiguous entries are more challenging for the agent to resolve. More on this in module 4 when we dive into Trace Analysis.

---

## Lesson 3: Stage 2 — "Offline Evals" (Build)

**Offline evals** refer to automated scoring of your AI outputs against a stored (hence offline) dataset. You can use it before each new release to quickly verify that prompt changes or new features are having the intended effect before users get access to the new version.

By this point, you've defined what "good" looks like and captured it in examples. We use those examples to effectively automate trace analysis, turning our understanding into a repeatable check that can scale over larger datasets.

**A typical workflow:**

1. Engineer makes a change (new prompt, model upgrade, tool integration)
2. The system automatically runs the change against your reference dataset
3. Results are compared to baseline (previous version)
4. If quality improves or holds, approve for deployment. If quality regresses, investigate and fix before shipping

Let's revisit our Triage Agent. A basic offline eval for it would be a golden dataset of 50 historical tickets with verified labels, which serves as the reference set for every subsequent change.

Baseline eval metrics would start with the success rate of its core tasks. Using the patterns we identified earlier, we may create an eval for categorization accuracy and one for sentiment precision.

When a new model version is available, the team can run it against those 50 tickets and know within hours whether the upgrade helps or hurts — for this product, on this task, not on a generic benchmark. Teams that invest in this infrastructure move faster. We will show you exactly how to design and implement automated offline evals in Modules 2–3, step by step.

A quick rule of thumb: if you can't confidently roll out a new model the same day it's been released, the bottleneck on your team is evaluation. A great example of this is Notion, where the AI team has accelerated 10X thanks to systematic evals, going from fixing 3 to 30 issues every day. When a new model drops, they can ship to prod in <24 hours. AI has accelerated their company growth with over 50% adoption across their customer base for premium features.

---

## Lesson 4: Stage 3 — "User Monitoring" (Optimize)

**Online monitoring** is real-time tracking of production performance, including A/B testing. It runs continuously after launch, and the goal is to capture any possible regressions as well as new edge cases.

Offline evaluation only tests what you already know to look for. Online scoring of real user sessions reveals what you didn't anticipate. You look for:

- Emerging new failure modes
- Shifts in user behavior
- Differences between experimental variants

This difference between your offline evals and your online monitoring scores is known as the **"drift"** in production quality.

Going back to our Support Triage Agent, what would online monitoring look like? Given its nature as a background task, we would probably want to sample some AI-tagged tickets with an evaluator asking, "Is this tag correct?" As ticket language evolves and new issue types appear, the audit surfaces (offline vs online) can drift. Before it becomes a systemic problem, we add new examples from the online monitoring back into the reference dataset.

**A quick rule of thumb:** If offline metrics say quality is improving, but user complaints are rising, you're measuring the wrong thing. We will dive deeper into this in the upcoming modules.

---

## Lesson 5: Demo before Memo — On starting with the Vibe Check

Now that you have a high-level overview of the whole eval lifecycle, imagine writing a PRD without prototyping and vibe checks.

Vibe checks on a simple prototype can help identify high-value examples for the AI PRD and seed datasets for building offline evals. With AI features:

**The PRD is no longer the first step; it's the second or third step.**

The first step instead is a prompt prototype and dataset collection. The PRD should then be focused on expectations for the AI, not a feature burndown list.

---

## Lesson 6: Recap and Further Learning

### Key takeaways and definitions

- **Look at the Data:** Evaluations must span the entire AI product lifecycle, covering prototype (Vibe Checks), build (Offline Evals), and optimize (User Monitoring).
- **Demo before Memo:** The PRD for AI features should follow the initial Vibe Check, focusing on expectations for the AI rather than being the first step in the development process.

**Vibe Checks** — Manual reviews of a prototype using a small but diverse dataset to build a sense for the agent's strengths and weaknesses before building a formal PRD. It can be casual but still systematic.

**Offline Evaluation** — Automated scoring of AI outputs against a stored (offline) dataset, used before each new release to quickly verify that prompt changes or new features are having the intended effect.

**User monitoring** — Real-time tracking or online evaluation of production user experience, which runs continuously after launch to capture performance, regressions, and edge cases. This is often done on a 1–10% sample of all user sessions.

### Recommended articles

- Demystifying evals for AI agents by Anthropic
- Your AI agent needs Evals by Hamel

In the next module, we will learn how to encode quality criteria directly into your AI PRD so that every engineer on the team knows exactly what "good" looks like before building begins.
