---
doc_id: "ai-evals-m12"
title: "Module 12: Evaluating Complex Agents"
author: "AI Evals course (external reference)"
type: "course-reference"
source_url: "local: day20/research/evaluation/02-course-ai-evals/module-12-evaluating-complex-agents.md"
retrieved: "2026-08-20"
lang: "en"
---
# Module 12: Evaluating Complex Agents

## Course Outline

- Intro
- Three Places Quality Breaks in Agentic Systems
- Cascading Failures in Long Agentic Traces
- Simulation: Testing What Static Inputs Can't
- Recap and Further Learning

---

## Intro

Real-world agentic products can be far more complex than the examples we have used to date.

The Support Triage Agent is a single-step system: one input, one classification, one response. Most production agents are not this simple.

- A research agent retrieves documents, synthesizes findings, and generates a report.
- A customer service agent routes to specialized sub-agents, calls APIs, and composes a multi-part resolution.
- An analytics agent interprets a natural-language question, generates SQL, executes it, and summarizes the results.

Single-turn evaluations don't directly scale to these production agentic systems with routing, tool calls, intermediate reasoning, and multi-step pipelines.

These systems break in ways that single-step evals can't diagnose. This chapter teaches **architectural decomposition**: breaking your system into evaluable components so you can pinpoint exactly where quality breaks, instead of staring at a headline success rate that tells you something is wrong but not what.

### Architectural Decomposition

The key principle: instead of evaluating the system as a black box, break it into its major components and evaluate each independently. A complex agent that scores 55% on an end-to-end success rate is not a 55% agent. It's a system where some components work at 95% and one component works at 76%, and that latter step drags the entire pipeline down.

Decomposition gives you precision. "The agent fails 45% of the time" is not actionable. "The routing layer misclassifies 8% of requests, the SQL generation step produces invalid queries 24% of the time, and the summarization step misses key findings 6% of the time" tells you exactly where to focus.

The decomposition typically produces three layers, each with its own evaluation strategy:
1. **Orchestration and routing** — did the system understand the request and choose the right path?
2. **Individual skills** — did each component do its job?
3. **Full-path outcomes** — did the user's goal get accomplished?

### Two Architectures, Two Evaluation Strategies

**Multi-agent systems for parallel orchestration:**

In a multi-agent system, a lead orchestrator receives the user's request and delegates to specialized sub-agents working simultaneously. For example, a customer support orchestrator might dispatch a billing agent, a technical agent, and a sentiment analysis agent in parallel, then synthesize their outputs into a unified response.

Eval strategy — Evaluate three things independently:
1. Routing correctness: did the orchestrator delegate to the right sub-agents?
2. Each sub-agent in isolation: given reasonable inputs, does each sub-agent produce quality outputs?
3. Orchestrator synthesis: does the final composed response accurately reflect what the sub-agents produced, without dropping or distorting information?

Treating a multi-agent system as a black box produces evals that can't distinguish routing failures from sub-agent failures from synthesis failures.

**Multi-step pipelines for sequential processing:**

In a multi-step pipeline, each step's output becomes the next step's input. One failure breaks the chain. A text-to-SQL agent might follow this sequence: understand the user's intent → identify the right tables → select the right columns → construct JOIN logic → build WHERE clauses → compile the query → execute it.

Eval strategy — Prioritize cascading failure analysis and end-to-end success rate. The critical insight is that a 3% failure rate in Step 1 propagates to every downstream metric. If the intent understanding step misinterprets the question, no amount of SQL generation quality will save the output.

**Highest-leverage evals target the earliest steps.** In sequential pipelines, improving the first failing step always produces a larger end-to-end gain than improving a later step with the same failure rate.

---

## Lesson 1: Three Places Quality Breaks in Agentic Systems

### A. Orchestration and routing

Did the system interpret user intent correctly? Did it extract the right parameters from underspecified requests? Did it choose a valid capability rather than hallucinating one or defaulting to a generic response?

**Eval approach:** Code-based evals on routing decisions. Build a labeled dataset of user intents mapped to expected routes. Pass/Fail on each routing decision. This is often the cheapest eval to build and the highest-leverage problem to fix, because every routing error guarantees a downstream failure.

**Example:** A financial analytics agent receives "show me revenue by region for Q3." The routing eval checks: did the agent correctly identify this as a SQL query task (not a document search or a calculation)? Did it extract the parameters: metric = revenue, dimension = region, time period = Q3? Routing errors at this level are invisible if you only evaluate the final output.

### B. Individual agent skills

Evaluate each skill in isolation with controlled inputs. Can this capability perform its job when given reasonable inputs? Where does it break: edge cases, scale, ambiguity, missing context?

**Eval approach:** A dedicated eval suite per skill, using the same code eval plus LLM judge methodology from modules 6 and 7, but scoped to the skill's specific quality criteria. The SQL generation skill has different evals from the summarization skill. Each skill's eval suite runs independently, and failures are attributed to the specific skill, not the system.

**Example:** The SQL generation skill is tested with a set of known-good intent/parameter pairs. The eval checks: is the generated SQL syntactically valid? Does it reference the correct tables and columns? Does it execute without errors? These evals run without the routing layer in the loop, isolating SQL quality from routing quality.

### C. Full-path outcomes

Full-path evals address two questions: Did the agent ultimately accomplish the user's goal (effectiveness)? Did it take a reasonable path to get there (efficiency)?

Full-path evaluation is the hardest, especially for long-running agents where multiple approaches are valid. A research agent might find the answer through three different retrieval paths, all equally valid. An efficiency eval needs to define what "reasonable" means without being so rigid that it penalizes legitimate alternative approaches.

**Eval approach:** End-to-end success criteria per task type. LLM judges or human review for subjective quality assessment. Efficiency metrics: step count, total latency, token cost. For tasks with clear correct answers (e.g., SQL queries that should return specific results), code evals on the final output. For open-ended tasks (e.g., research summaries), reference-based LLM judges or human review.

### Evaluating Tool Calls

Complex agents are defined by their tool use. Every tool call is a decision point where quality can break, and most teams don't evaluate tool calls independently. This is a mistake.

According to Anthropic's research on agent evaluation, each tool call involves three distinct failure modes:
- **A: selecting the wrong tool**
- **B: passing incorrect parameters**
- **C: mishandling the response**

Evaluating only the final output conflates all three into a single pass/fail, making it impossible to diagnose which part of the tool interaction broke.

### A: Tool selection accuracy

Did the agent choose the right tool for the task? This is a classification problem, and you can evaluate it like one.

Build a labeled dataset of user requests mapped to expected tool calls. "What was our revenue last quarter?" should trigger `query_database`, not `search_documents`. The eval is a simple code check: expected tool versus actual tool, pass or fail.

Tool selection errors are binary and high-impact. If the agent picks the wrong tool, everything downstream is guaranteed to fail.

In practice, tool selection accuracy above 95% is table stakes for production. Below that, users experience a system that feels random.

Watch for **hallucinated tools**. Agents sometimes attempt to call tools that don't exist in their toolkit, especially when the user's request doesn't map cleanly to an available capability.

### B: Parameter extraction

The agent picked the right tool. Did it pass the right parameters? Parameters have three failure modes: missing, incorrect, and malformed. Examples for a SQL agent:

- **Missing:** the agent calls `query_database` but omits the time range, returning all-time data when the user asked for Q3
- **Incorrect:** the agent passes `region = "APAC"` when the user said "Asia-Pacific" and the database uses `region = "Asia Pacific"`
- **Malformed:** the agent constructs a date filter as "2025-Q3" when the API expects "2025-07-01"

**Eval approach:** For each tool in the agent's toolkit, define the expected parameter schema and build test cases that cover normal inputs, edge cases, and adversarial inputs. Code evals handle exact-match parameters (dates, IDs, enums). LLM judges handle fuzzy parameters where multiple formulations are acceptable.

**Example:** An analytics agent receives "show me weekly signups for the enterprise plan since January." The parameter eval checks: did it extract metric = signups, granularity = weekly, plan = enterprise, start_date = 2026-01-01? A common failure: the agent extracts the metric and plan correctly, but defaults granularity to "daily" because the prompt doesn't emphasize temporal granularity. This failure is invisible in end-to-end evals if the query happens to return plausible-looking data at the wrong granularity.

### C: Response handling

The tool returned a result. Did the agent use it correctly? Three patterns to evaluate:

1. **Faithful interpretation:** Does the agent accurately represent what the tool returned, without hallucinating additional data or dropping key results?
2. **Error handling:** When the tool returns an error or empty result, does the agent surface it clearly or paper over it with a fabricated answer?
3. **Multi-tool synthesis:** When multiple tools return results, does the agent combine them correctly?

Faithful interpretation is best evaluated with an LLM judge that compares the tool's raw output against the agent's response.

Error handling deserves its own eval. Build test cases where tools return errors, empty results, partial data, and timeouts. A common and dangerous failure mode: the agent receives an empty result from a database query and responds "There were no signups in Q3" when the correct response is "The query returned no results, which may indicate a data issue."

---

## Lesson 2: Cascading Failures in Long Agentic Traces

One error in Step 1 can corrupt everything downstream. Reading the trace without this in mind produces a misleading picture. You see failures at Steps 3, 5, and 7 and conclude the system has three independent problems. In reality, it has one: Step 1 set the wrong context, and every subsequent step worked correctly on bad inputs.

**Example:** A research agent misinterprets "recent" as "within the last year" when the user meant "within the last week." The agent retrieves outdated data (Step 2, working correctly on the wrong timeframe). It analyzes the data correctly (Step 3). It produces a well-written summary (Step 4) of information the user didn't ask for. The root cause is Step 1. The summary eval might even pass, because the summary is well-written. Only the end-to-end eval catches that the answer is wrong.

### Diagnostic strategy: work backwards

Find the last step that was correct, then examine the step immediately after it. That boundary is where the cascade started.

Distinguish between **primary failures** (root cause) and **secondary failures** (downstream noise). When sizing problems and selecting which evals to build, count only primary failures. If Step 1 fails on 10 traces and Steps 3 through 7 show failures on those same 10 traces, the problem is 10 Step 1 failures, not 50 failures across 5 steps.

Once you've identified the cascade origin, you can use a transition failure matrix (detailed in module 13) to map the last successful step against the first failing step across all traces.

### Evaluating Error Recovery and Self-Correction

Most agent evals measure whether the agent got it right on the first try. Production agents rarely get one shot.

A SQL query fails, and the agent needs to read the error message, diagnose the problem, and retry with a corrected query. A tool called returns unexpected data, and the agent needs to ask for clarification rather than bulldozing forward with bad assumptions.

**The ability to recover from errors is what separates agents that work in demos from agents that work in production.**

A text-to-SQL agent with 80% first-attempt accuracy and strong error recovery will outperform one with 90% first-attempt accuracy that freezes or hallucinates when a query fails.

Yet most eval suites only measure the happy path. They never test what happens when the tool returns an error, the database schema changes, or the user's question is ambiguous in a way the agent didn't anticipate.

**Three recovery capabilities to evaluate:**

**1. Error detection:** Does the agent recognize when something went wrong? Many agents treat tool errors as valid responses. Example: A SQL agent receives `ERROR: column "revenue" does not exist` and responds to the user with "Your revenue data is not available" instead of recognizing that it referenced the wrong column name. The eval should check: given a tool error, does the agent's next action indicate it recognized the failure?

**2. Diagnostic reasoning:** Does the agent correctly identify why it failed? After detecting an error, the agent needs to distinguish between "I used the wrong column name," "the database is down," and "the user's question is ambiguous." Each diagnosis leads to a different recovery action.

**3. Adaptive retry:** Does the agent take an effective corrective action? Retrying with the exact same parameters is not recovery. Effective recovery means changing the approach based on the diagnosis: trying a different column name, asking the user for clarification, or falling back to a simpler query strategy.

**Building recovery evals — inject failures deliberately.** Create test cases where tools return errors, unexpected schemas, partial results, or timeouts:

| Failure scenario | Expected recovery |
|---|---|
| Tool returns column not found error | Inspect available columns and retry with correct column name |
| Query returns zero rows when results are expected | Verify table/filter logic rather than reporting "no data" |
| Query times out | Simplify the query (reduce JOINs, narrow date range) and retry |
| User question is ambiguous ("show me performance") | Ask a clarifying question rather than guessing |

**Score recovery on three dimensions:**
1. Did the agent detect the error? (Binary)
2. Did it diagnose correctly? (LLM judge on the reasoning trace)
3. Did it ultimately succeed? (Code eval on the final output)

**Track recovery rate alongside first-attempt accuracy.** If first-attempt accuracy is 82% and recovery brings the success rate to 93%, you know recovery is adding 11 points of value. If recovery only adds 2 points, the agent is retrying without meaningfully changing its approach.

### Case Study: Evaluating a Text-to-SQL Analytics Agent

The text-to-SQL analytics agent converts natural-language questions into SQL queries, executes them, and summarizes the results. Users ask things like "What was our weekly signup rate for enterprise accounts in Q1?" This is a high-stakes system — wrong numbers can drive bad product decisions.

**Step 1: Decompose the pipeline**

| Step | What it does |
|---|---|
| Intent parsing | Identify metric, dimensions, time range, and filters |
| Schema mapping | Match parsed intent to correct database tables and columns |
| SQL generation | Construct syntactically valid query with correct logic |
| SQL execution | Run against data warehouse, capture errors/timeouts |
| Result interpretation | Transform raw results into meaningful answer |
| Summary generation | Produce natural-language response to user's question |

**Step 2: Build layered evals**

- **Intent parsing (code eval):** Extract structured intent, compare against labeled ground truth. Fields checked: metric name, dimension(s), time range, filters.
- **Schema mapping (code eval):** Check that the agent selected the correct tables and columns.
- **SQL generation (code eval + execution test):** Two checks — syntactic validity, then execution accuracy against a test database with known data.
- **SQL execution (code eval):** Did the query run? Track error rate, timeout rate, and recovery success rate separately.
- **Result interpretation (LLM judge):** Does the interpretation accurately represent the data? Check numerical accuracy, completeness, and honesty (does it flag caveats?).
- **Summary generation (LLM judge):** Does the final response answer the user's original question? Is it clear, concise, and actionable?

**Step 3: Visualize failures and iterate**

Run the eval suite on ~200 production traces. Build the transition failure matrix and failure funnel (from module 13) to identify where failures concentrate. The matrix immediately reveals that Schema Mapping → SQL Generation is the dominant hotspot, accounting for nearly half of all failures.

From here, apply the iteration loop from module 10 to the SQL generation step: prompt fixes for JOIN patterns, a schema-aware validation layer, and eventually a model upgrade with error recovery.

---

## Lesson 3: Simulation — Testing What Static Inputs Can't

Static datasets can't test multi-turn branching, recovery from mistakes, or context management over long conversations. A reference dataset row is typically a single input/output pair. A real user conversation is 8–12 turns where the user asks a follow-up, corrects a misunderstanding, changes direction, and circles back to an earlier point.

**Simulation uses an LLM playing a realistic user** with a defined goal, persona, and constraints. The simulated user interacts with your agent over multiple turns, creating the kind of dynamic, branching conversation that static evals can't replicate.

### How to design simulations

Define user personas with specific goals, communication styles, and frustration triggers. A simulation persona might be: "Enterprise finance analyst. Goal: get a quarterly revenue breakdown by region. Communication style: direct, expects precise numbers. Frustration trigger: vague or hedged answers."

Let the simulated user respond naturally — ask follow-ups when the answer is incomplete, correct the agent when it misinterprets, change course mid-conversation, and escalate frustration when the agent fails repeatedly.

**Score the full conversation:** Did the agent achieve the user's goal? Did it take a reasonable number of steps? Did it handle interruptions and corrections gracefully? Did context degrade over the conversation?

### Simulation limitations

Simulated users are not real users. They tend to be more cooperative, more predictable, and less creative in their requests.

Use simulation for regression testing and coverage of long-running scenarios. It's excellent for checking that a prompt change didn't break multi-turn context management. It's poor as your only multi-turn test.

Always validate simulation results against real production traces. If the simulation shows 90% goal completion but production monitoring shows 70%, the simulation personas don't represent real users. Update them.

### Practical Eval Design for Complex Systems: Start simple, add layers

1. Define binary success criteria for routing, each skill, and the full path
2. Build code evals for routing and skill-level checks first — cheapest and fastest to implement
3. Add LLM judges for full-path quality assessment once the component evals are stable
4. Add simulation for multi-turn and long-horizon testing once you have a baseline of component-level evals

Don't build all four layers at once. Start with the layer where failures are most visible and work outward.

**When to invest in each layer:**
- If most failures come from routing, invest in routing evals
- If routing is fine but individual skills underperform, invest in skill-level evals
- If components work individually but the composed system fails, invest in full-path and simulation evals

---

## Lesson 4: Recap and Further Learning

### Key takeaways and definitions

- **Decompose before evaluating.** Break complex systems into routing, skills, and full-path outcomes. Evaluate each independently to isolate failure sources. A headline success rate tells you something is wrong. Decomposition tells you what.
- **Evaluate tool calls at three levels.** Tool selection (did it pick the right tool?), parameter extraction (did it pass the right inputs?), and response handling (did it use the output correctly?). Each is a distinct failure mode that needs its own eval.
- **Fix upstream first.** In multi-step pipelines, one early failure cascades everywhere. Prioritize evals and fixes at the top of the pipeline. Improving Step 1 always yields more end-to-end gain than improving Step 5.
- **Evaluate recovery, not just accuracy.** Agents that can detect errors, diagnose root causes, and retry effectively outperform agents with higher first-attempt accuracy but no recovery capability. Track recovery rate alongside first-attempt accuracy.
- **Simulation fills gaps.** Use LLM-simulated users to test multi-turn, long-horizon scenarios that static datasets can't cover. But always validate against real production traces.
- **Start simple, add layers.** Build routing and skill-level code evals first. Add full-path judges. Add simulation last.

**Architectural decomposition** — Breaking a complex AI system into its major components (routing, skills, full-path) and evaluating each independently to isolate where failures originate.

**Tool call evaluation** — Independently assessing three aspects of an agent's tool use: selecting the correct tool, extracting accurate parameters, and handling the tool's response faithfully.

**Error recovery** — An agent's ability to detect failures, diagnose root causes, and take corrective action (retry with different parameters, ask for clarification, or fall back to a simpler approach) rather than failing silently or hallucinating.

**Cascading failure** — An error in an early step of a multi-step pipeline that propagates through all downstream steps, making the system appear to have many independent failures when it has one root cause.

**Simulation-based evaluation** — Testing multi-turn agent behavior using an LLM that plays the role of a realistic user with defined goals, personas, and constraints.

In the next module, we will learn how to visualize multi-step eval results using failure funnels, making cascading failures visible and actionable.
