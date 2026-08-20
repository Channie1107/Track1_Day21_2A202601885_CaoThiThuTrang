---
doc_id: "ai-evals-m04"
title: "Module 4: Principles of Trace Analysis"
author: "AI Evals course (external reference)"
type: "course-reference"
source_url: "local: day20/research/evaluation/02-course-ai-evals/module-04-principles-of-trace-analysis.md"
retrieved: "2026-08-20"
lang: "en"
---
# Module 4: Principles of Trace Analysis

## Course Outline

- Intro
- What is a Trace
- The Trace Analysis Workflow: Generating Codes
- Sourcing a Diverse Dataset: the User Input Grid
- Collaboration: Make Trace Analysis a Team Sport
- Recap and Further Learning

---

## Intro

In this module, you will develop a repeatable workflow for reading agent traces — sourcing diverse inputs, reviewing outputs free-form, and clustering patterns into structured trace codes.

Before you can automate evaluation, you need to understand how your system actually behaves.

We start that journey with trace analysis. Trace analysis is how teams move from abstract quality goals to concrete insight. It is the AI equivalent of UX research: instead of interviews and session replays, you study real inputs and outputs to understand success and failure.

New features, unexpected behavior, or user complaints all surface first in real traces. You review them manually to understand what actually happened, not what you hoped would happen. This is where failure modes are named, and reference examples are created.

**Pitfall to avoid:** Most teams try to skip this step. They jump straight to dashboards, benchmarks, or automated scoring. The result is predictable: metrics that look rigorous but don't reflect what users experience.

This section teaches a lightweight, repeatable way to do trace analysis without turning it into an academic exercise.

---

## Lesson 1: What is a Trace

Before you can analyze traces, your team needs a shared vocabulary for LLM instrumentation. These terms define the atomic units of AI requests.

**Trace** — A trace is the complete record of everything that happened inside a single AI request. It captures all user inputs, all model outputs (including intermediate steps), and relevant metadata such as timestamps, token counts, and model versions.

Traces can be single or multi-turn, where every turn represents fresh external input for the LLM. We recommend recording all the AI vs user back and forth in a single session as a single Trace. When you do trace analysis, you are reviewing not just final outputs, but the full sequence of work the system performed.

### Example 1: AI Slide Tool

A user signs up for an AI presentation tool like Gamma and takes these actions:

- Creates a new presentation from a template
- Uploads an outline to generate slides
- Opens individual slides and edits them
- Asks the AI to rewrite a slide
- Iterates on that rewrite through multiple back-and-forth instructions

To the user, this feels like a single continuous workflow. Under the hood, it might produce multiple traces based on how the agents are structured. Essentially, each task performed with a distinct agent is its own trace.

**Trace 1 — Slide generation workflow: Outline → Slides**

- User uploads an outline
- AI generates a full slide deck from that outline
- Output is a structured set of slides

This trace contains: the uploaded outline and prompt used to generate slides, the generated content, any intermediate reasoning or formatting steps, all the metadata on the interaction (including tokens, latency, etc).

**Trace 2 — Slide rewrite workflow**

- User selects a specific slide
- Asks AI to rewrite it through multiple iterations
- Output is a revised slide

This can be a separate group of traces because it represents collaborative work with a different part of the AI Slide app.

### Example 2: Customer Support Agent

Below is a simplified JSON representation of an LLM Trace, which captures a Retrieval-Augmented Generation (RAG) operation from a CSM agent where a user asks about a return policy.

```json
{
  "trace_id": "trace_abc123",
  "timestamp": "2025-01-15T10:30:00Z",
  "user_input": "What is your return policy for electronics?",
  "retrieved_context": [
    "Electronics can be returned within 30 days of purchase...",
    "Items must be in original packaging..."
  ],
  "model_output": "Our return policy for electronics allows returns within 30 days...",
  "metadata": {
    "model": "claude-sonnet-4-6",
    "tokens_used": 450,
    "latency_ms": 1200
  }
}
```

---

## Lesson 2: The Trace Analysis Workflow — Generating Codes

Here's the systematic process for moving from raw traces to structured evaluation categories.

### Step 1: Source inputs

You start by assembling a small but diverse set of inputs to run through the system. These inputs can come from:

- Early design partners or internal users
- Support tickets or example use cases
- Synthetic inputs generated with prompts

At this stage, perfection doesn't matter. Coverage does. You are trying to see the range: different personas, intents, ambiguity levels, and edge cases.

For early products, synthetic inputs are often the fastest way to explore the solution space. The goal is not realism for its own sake, but stress-testing the system across plausible scenarios.

### Step 2: Review Outputs (Free-Form)

Next, you review traces manually. This is an intentionally open-ended pass. You are not scoring or judging yet. You are observing. As you review each trace:

- Take generous notes and write down anything that surprises you
- Capture both failures and moments where the system is impressive

Three kinds of signals usually emerge: **hard performance failures**, **soft quality issues**, and **emergent behavior** that differentiates your product.

Early on, resist the urge to formalize. Patterns appear through repetition, not through over-structuring the first ten traces.

### Step 3: Cluster Into Trace Codes

After reviewing 30–50 traces, repetition sets in. This is where structure emerges. You now cluster your notes into **trace codes**:

- Groups of similar success or failure patterns
- Each category represents a recurring behavior worth tracking

A strong trace code has:
- A short, concrete name
- A one-sentence definition
- Clear Yes/No criteria
- Two or three representative examples

**Example 3: Market Research Agent**

Consider a market research agent that searches the web to respond to user questions about competition and general company information. Examples of trace codes for an agent conducting market research might be:

- **Unsupported claims** — Makes assertions without citing sources
- **Over-generalization** — Treats niche markets as homogeneous
- **Missed ambiguity** — Assumes metrics like "market size" without clarification
- **Strong synthesis** — Connects multiple weak signals into a coherent insight

Keeping these codes binary (Yes/No) matters. They force clarity. If two reviewers can't agree whether something passes, the code isn't ready for automated labelling.

Over time, these codes become the foundation for rubrics, datasets, and automation.

---

## Lesson 3: Sourcing a Diverse Dataset — the User Input Grid

Simply asking an LLM to "generate test queries" produces generic inputs that fail to surface critical edge cases. A **user input grid (UIG)** mapped to different user intents is how you bring order to probabilistic complexity by creating a structured grid of query dimensions that mirrors production diversity.

### The UIG Methodology

**Step 1: Define 3–5 Key Dimensions**

Identify the variables that create meaningful diversity in your product. Common dimensions include:

- **Ideal Customer Profile (ICP):** Enterprise, Mid-market, SMB
- **Persona:** End user role (Engineer, Manager, Executive)
- **User Intent:** What task they're trying to accomplish
- **Context Richness:** Complete information vs. missing details
- **Ambiguity Level:** Clear instructions vs. vague requests

**Step 2: Generate Realistic Examples**

Create 2–3 concrete examples for each dimension, grounded in real-world constraints:

ICP Examples:
- Public SaaS: Companies with publicly available financial data
- Private B2B: Limited public information, must infer from news/funding
- Healthcare: HIPAA compliance constraints, specialized terminology

User Intent Examples for our Market Research Agent might include:
- Competitive analysis: "Who are our direct competitors and what's their positioning?"
- Market sizing: "What's the TAM for vertical SaaS in manufacturing?"
- Customer research: "What pain points do customers mention most in G2 reviews?"

**Step 3: Create Combinations**

Form a grid by combining dimensions. For 4 ICPs × 4 Personas × 4 JTBDs = 64 possible combinations. Remove implausible ones (e.g., "Executive researching low-level technical details"), leaving 15–20 realistic scenarios.

Example Combination:
- ICP: Public SaaS
- Persona: Product Marketing Manager
- JTBD: Competitive landscape
- Context: Q4 2024 data needed

**Step 4: Add Real-World Constraints**

Enhance combinations with realistic complications:
- Missing context: User doesn't specify which market/geography
- Ambiguous terms: "Best" could mean revenue, growth rate, or customer satisfaction
- Time sensitivity: "Recent" could mean last month or last year
- Conflicting requirements: "Comprehensive but concise."
- Business rules: "Must comply with data privacy regulations."

**Step 5: Formulate Natural Language Queries**

Use an LLM to transform combinations into natural user queries. Provide the combination as structured input, ask for 2–3 variations.

Generated Queries could include:
- "Which US SaaS companies have the highest customer satisfaction scores in Gartner's 2025 reports?"
- "Who are the leading CRM platforms by market share, and what are their key differentiators?"

Notice these inputs have realistic ambiguity (leading = satisfaction or market share?) and missing context (US assumed but not stated in query 2).

### Example 4: Legal Contract Analyzer

Below is what a user input grid for a legal analysis agent might look like:

| Dimension | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| Document Type | Employment agreement | NDA | Service contract |
| User Persona | In-house counsel | Outside counsel | Business executive |
| Task | Risk assessment | Clause extraction | Comparison |
| Context | Complete contract | Partial document | Multiple versions |

**Sample Combination:** Employment agreement + In-house counsel + Risk assessment + Complete contract

**Sample Generated Query:** "Review this employment agreement for non-standard termination clauses that could expose us to litigation in California. Flag any provisions that deviate from our standard template."

---

## Lesson 4: Collaboration — Make Trace Analysis a Team Sport

Trace analysis is most effective as a cross-functional team effort. It turns subjective "product taste" into trusted, repeatable standards the entire team can align on. Different roles reveal distinct failure modes:

- **PMs** catch violations of the product promise and user intent
- **Engineers** identify fragility in tool execution and architectural issues
- **Designers** surface UX issues and formatting problems
- **Subject Matter Experts (SMEs)** catch domain-specific mistakes others might miss

**The collaborative workflow:**

1. Independent labeling: 3–4 team members each label the same 20 traces individually
2. Comparison meeting: Compare labels, discuss disagreements
3. Refinement: Tighten category definitions based on where people disagreed
4. Standardization: Update the rubric, re-label disagreements
5. Repeat: Continue until the team achieves >90% agreement

### Knowing When to Stop: The Saturation Rate

A common question: how much data is "enough"? You don't need thousands of traces. You stop when you reach **saturation**:

- You review ten consecutive traces of different kinds
- No new categories emerge
- Existing categories keep repeating

That's your signal to move on. At that point, more reviews add diminishing returns. The work shifts from discovery to formalization.

Note: saturation is per-dimension. You might reach saturation on "tone" after 50 traces, but you need 150 traces to understand "factual accuracy" failure modes. Track saturation separately for each quality criterion you're evaluating.

### Playing Offense, Not Just Defense

Trace analysis isn't only about catching errors. You should actively look for affirmative patterns and double down on the strategy behind them:

- Outputs users accept immediately
- Moments where the agent anticipates the next question
- Responses that reduce follow-up work

These are signals of product taste. Capturing them ensures you don't just eliminate bad behavior but reinforce what's great.

---

## Lesson 5: Recap and Further Learning

### Key takeaways and definitions

- **Trace Analysis as UX Research:** Trace analysis is the AI equivalent of UX research, moving teams from abstract quality goals to concrete insights by manually studying real inputs and outputs
- **Source Diversity with UIGs:** The User Input Grid (UIG) methodology structures test data creation (or sourcing) by defining key dimensions (like ICP and User Intent) and generating realistic, constrained, and ambiguous queries
- **Collaboration and Standardization:** Trace analysis is a cross-functional effort, and a Trace Code is only ready for automation when reviewers achieve high inter-rater agreement (>90%)
- **Knowing When to Stop:** Stop manual review when you reach the Saturation Rate—when no new failure or success categories are emerging
- **Playing Offense:** Actively look for successful patterns and product differentiators, not just failures, to reinforce effective product behavior

**Trace** — The complete record of everything that happened inside a single AI request, including all user inputs, model outputs (including intermediate steps), and metadata.

**Trace Codes** — Short, concrete names representing recurring success or failure patterns, which are clustered from free-form review notes and form the foundation for automated rubrics and datasets.

**User Input Grid (UIG)** — A structured methodology used to generate a diverse and realistic set of user queries by defining and combining variables such as Customer Profile, Persona, and Ambiguity Level.

**Saturation Rate** — The point at which manual review of diverse traces stops yielding new categories, signaling that the discovery phase is complete.

### Recommended articles

- The AI PM Craft: Evolving Product Leadership
- Evals, Error Analysis, and Better Prompts
- Why AI Agents Break: A Field Analysis of Production Failures

In the next module, we will learn the principles that determine when to automate evaluation, which method to choose, and the common mistakes that make eval suites unreliable.
