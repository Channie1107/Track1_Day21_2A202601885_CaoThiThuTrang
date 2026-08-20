---
doc_id: "ai-evals-m03"
title: "Module 3: AI-native PRDs"
author: "AI Evals course (external reference)"
type: "course-reference"
source_url: "local: day20/research/evaluation/02-course-ai-evals/module-03-ai-native-prds.md"
retrieved: "2026-08-20"
lang: "en"
---
# Module 3: AI-native PRDs

## Course Outline

- Intro
- Comparing PRD Approaches
- Sample AI PRD: Support Ticket Triage (v1.0)
- When the Agent Should Say "I Don't Know"
- The Solution-space Shift and Trace Analysis
- Recap and Further Learning

---

## Intro

In this module, you will learn how to write an AI-native PRD that defines quality criteria, golden outputs, and an evaluation rubric before your engineering team writes a single line of code.

Traditional PRDs often have a list of features in the form of user stories; their role is to facilitate a backlog of capabilities that can be built and released over time. This tells engineers what to build, but not what good looks like. An AI can generate infinite variations of an email draft. Which ones are great?

AI agents using frontier models come out of the box with most of their core capabilities already present — but performing with low reliability.

Let's consider how Claude Code, a terminal-based coding tool, has evolved over the past year since its February 2025 release. You'll notice that most of the releases (5 of 7) have been performance improvements for the core capabilities that already existed at launch, i.e., agentic coding.

Since v1 of an agentic product already has a lot of its underlying features present, AI PRDs focus significantly on quality definitions and performance scores.

**AI PRDs are not the first step in the development cycle.** They should be written only after initial "vibe checks" (manual prototyping) and prompt testing has been conducted to establish what's possible.

---

## Lesson 1: Comparing PRD Approaches

The core shift is that a traditional PRD describes a system someone will build. An AI-native PRD describes the quality bar a probabilistic system has to meet — and the mechanism for knowing whether it does.

Here's more about 3 vital new components of an AI-native PRD: **golden outputs**, **eval rubrics**, and the **dataset strategy**:

### Golden outputs

These anchor the team's understanding of quality. Every feature should include concrete examples of both strong and weak outputs. Strong examples show what "great" looks like. Weak examples clarify boundaries and failure modes. These examples should include messy cases: incomplete inputs, contradictory instructions, and ambiguous context. Those are the situations where quality decisions matter most.

### Evaluation rubric

Translates intuition into shared standards. At this stage, rubrics are intentionally vibe-oriented. They describe what matters and why, not how measurement will be automated. A good rubric makes clear what accuracy means for your domain, what tradeoffs are acceptable, and which failures are never allowed. Automation comes later; clarity comes first.

In our sample AI PRD coming up below, you will see that the evaluation rubric is explicit: categorization accuracy above 92%, sentiment precision above 85%, latency under two seconds, and hallucination rate at zero.

### Dataset curation strategy

This begins as exploration. Early examples are never sufficient. As real users interact with the system, you will discover variations you did not anticipate. Your spec should include a plan for capturing and labeling these cases to better understand who your users are, how they differ, and where the system struggles. Over time, this exploration produces a dataset that reflects reality rather than assumptions.

Instead of being theoretical, the PRD that your engineering team starts working on should have golden output examples from a diverse set of inputs. This makes it critical for PMs to be able to prototype and vibe check ideas before they write a formal PRD.

---

## Lesson 2: Sample AI PRD — Support Ticket Triage (v1.0)

Below is what a brief but complete AI PRD (written after prototyping and combined with a 50-row golden dataset) for our Support Triage Agent would look like. It has the following sections:

1. Problem & Business Value
2. Prompt Logic & Dataset
3. Tool Specification
4. Evaluation Criteria
5. Edge Cases Handling
6. Prototype & Early Findings
7. Technical Constraints

---

**Sample AI PRD: Support Ticket Triage (v1.0)**

*Owner: [Name] | Status: Prototyping | Default Model: Gemini 3 Flash Preview*

**1. Problem & Business Value**

Support leads spend about 4 hours per day manually tagging tickets. This creates a lag before specialists can see high-priority issues. Our solution is a background agent that autonomously classifies tickets in real time by Intent, Sentiment, and Urgency.

**2. Prompt Logic & Dataset**

*System Instruction Summary:* You are a support analyst. Categorize incoming tickets into one of three buckets: Technical, Billing, or Feature Request. Assign a sentiment (Positive, Neutral, Frustrated, Angry) based on user frustration. If sentiment is Frustrated or Angry, immediately flag for human override, regardless of category.

*Golden Dataset:* Attached: 50 historical tickets with "Gold" labels for few-shot prompting.

**3. Tool Specification**

The agent should have access to the following APIs before making a triage decision:

| Tool Name | Action | Input Param | Purpose |
|---|---|---|---|
| User_Lookup | Query internal database | user_email | Check whether the user is a VIP or Enterprise customer to escalate priority. |
| Subscription_Check | Stripe/Billing API | customer_id | Confirm active paid plan before routing to Priority Tech Support. |
| Jira_Search | Jira API | keyword_string | Check for an existing Active Incident or Known Bug matching the complaint. |
| CRM_Write | Salesforce/HubSpot API | ticket_id, tag | Write final classification and sentiment score to the CRM record. |

**4. Evaluation Criteria**

| Metric | Target | Why It Matters |
|---|---|---|
| Categorization Accuracy | > 92% | Avoid routing Billing issues to Dev teams. |
| Sentiment Precision | > 85% | Avoid false alarms on frustrated users. |
| Latency | < 2s | Must be faster than manual triage. |
| Hallucination Rate | 0% | It should never invent ticket IDs or usernames. |

*Course Note: standard out-of-the-box evals like LLM tone/helpfulness are not primary success metrics for this workflow.*

**5. Edge Cases Handling**

- *Low-confidence fallback:* If model confidence is < 0.7, do not auto-tag. Move ticket to Needs Human Review.
- *Drift monitoring:* Run a weekly manual audit on 5% of AI-tagged tickets.
- *User feedback loop:* Add a support-side prompt: Is this tag correct? [Yes/No].

**6. Prototype & Early Findings**

Link to Internal Demo and Early Findings:

- Very short inputs (for example, "Help!") cause category hallucinations. Add a clarification-needed mode.
- About 20% of tickets contain two issues (for example, "I can't log in and I need to update my billing info"). The current model picks only the first issue, so we need multi-label classification instructions.
- The model struggled with sarcasm. We added 5 sarcastic complaint examples to the Golden dataset for few-shot learning via the system prompt.

**7. Technical Constraints**

- *Data privacy:* Scrub all PII (email addresses, phone numbers) with a regex preprocessor before sending to the LLM API.
- *Cost per ticket:* Keep categorization cost below $0.01 to maintain ROI.

---

## Lesson 3: When the Agent Should Say "I Don't Know"

Most PRDs define what the agent should do when things go well. Fewer define what it should do when it doesn't know. That gap produces hallucinations — not because the model is broken, but because no one told it that admitting uncertainty was an option.

The "I don't know" threshold is a product decision — it belongs in the PRD, and it differs by domain:

- A legal document assistant that fabricates a case citation is a liability.
- A brainstorming tool that hedges on every suggestion is useless.

The right threshold depends on the failure mode you're most afraid of.

**The conservative approach** applies to legal, medical, financial, and compliance-adjacent products. The agent declines to answer:
- If the relevant information isn't in the top retrieved documents
- If retrieved sources contradict each other, or
- If the evidence is ambiguous

"I don't have enough information to answer this accurately" is a success state, not a failure.

**The permissive approach** applies to research, brainstorming, and exploratory tools.

**How to specify this in your PRD:** Define the confidence threshold per query type and the exact language the agent should use when declining. "Your question falls outside what I have reliable information on" is more useful than "I don't know." Also specify what the agent should surface instead:
- A fallback path
- A suggested query reformulation, or
- An escalation

**How to measure it:** Track the "I don't know" rate in production.

A rate above 30% means retrieval is failing and users are hitting dead ends. A rate below 5% in a knowledge-bounded system is a signal that the agent is filling gaps with fabrications rather than admissions. For most enterprise applications, 10–20% is the target range.

---

## Lesson 4: The Solution-space Shift and Trace Analysis

AI product work requires more time defining and refining the solution than traditional PM roles did. You still need to own the primary understanding of the problem, but the heavy lifting is in defining and measuring quality. Spending time prototyping and building an intuition for the failure modes of an agent is very much solution-focused.

This brings us to **Trace Analysis** — reviewing the full record of an interaction between a (user) input and LLM-generated outputs.

As we dive into module 4, we'll see that PMs working on AI products spend significant amounts of time not just testing prompt variations but also:

- Personally reviewing traces to identify patterns
- Writing and iterating on evaluation rubrics
- Labeling datasets to calibrate automated judges

Teams that let ML engineers exclusively own this work discover quickly that "product taste" matters and development is slowed down. An engineer can implement your rubric, but they can't define what "great" means for your users. As a PM, that's your job.
