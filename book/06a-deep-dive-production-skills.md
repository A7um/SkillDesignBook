# Chapter 6A: Deep Dive — Anatomy of Top-Tier Production Skills

This chapter dissects actual production skills from OpenAI, Anthropic, Cursor, Devin, and Manus—examining what they do, why they're structured the way they are, and what design philosophies they reveal.

## 6A.1 OpenAI's Agents SDK Skills: The "Tiny CLI" Philosophy

OpenAI maintains nine production skills in their Agents SDK Python repository (`.agents/skills/`). These skills are not examples—they are the actual operational skills that maintain the SDK itself, handling 457 merged PRs in a three-month period (December 2025–February 2026).

### The Skill Catalog

| Skill | Purpose | Philosophy |
|-------|---------|-----------|
| `code-change-verification` | Run format, lint, type-check, tests | **Gate-keeper**: nothing ships without passing |
| `docs-sync` | Audit docs against codebase | **Report-first**: gather info, then recommend |
| `implementation-strategy` | Decide compatibility boundary before coding | **Think-before-act**: plan compatibility before implementation |
| `final-release-review` | Compare release tag with current candidate | **Checklist**: systematic release verification |
| `openai-knowledge` | Pull current OpenAI API docs via MCP | **Just-in-time knowledge**: fetch authoritative info on demand |
| `pr-draft-summary` | Generate branch name, PR title, description | **Handoff automation**: consistent PR formatting |
| `test-coverage-improver` | Find coverage gaps, propose high-impact tests | **Report-first**: identify gaps, don't auto-fix |
| `runtime-behavior-probe` | Investigate actual runtime behavior | **Empirical verification**: test, don't assume |
| `examples-auto-run` | Validate example code executes correctly | **Continuous verification**: keep examples working |

### Dissecting `code-change-verification`

This is OpenAI's most-used skill. Here is its actual structure:

```markdown
---
name: code-change-verification
description: Run the mandatory verification stack when changes affect
  runtime code, tests, or build/test behavior in the OpenAI Agents
  Python repository.
---
# Code Change Verification

## Overview
Ensure work is only marked complete after formatting, linting,
type checking, and tests pass.

## When to use
- When changes affect runtime code, tests, or build/test configuration
- Before marking work complete or merging to main

## When to skip
- Docs-only or repository metadata changes
- Unless full verification is explicitly requested

## Execution
- If dependencies changed, run `make sync` first
- Run from repository root in order: `make format`, `make lint`,
  `make mypy`, `make tests`

## Resources
### scripts/run.sh
Executes the full verification sequence with fail-fast semantics.
Prefer this entry point.
```

**What makes this excellent:**

1. **Narrow contract**: One job—run the verification stack. No side quests.
2. **Explicit skip conditions**: "Docs-only or metadata changes" prevents over-triggering.
3. **Ordered execution**: Format → lint → type-check → tests. The order matters and is explicit.
4. **Script-backed determinism**: The actual verification runs via `scripts/run.sh`, not natural-language instructions. The agent can't improvise the sequence.
5. **Fail-fast semantics**: The script stops at the first failure, preventing the agent from continuing with a broken state.

### Dissecting `runtime-behavior-probe`

This skill reveals a deeper philosophy: **empirical verification over code reading**.

```markdown
---
name: runtime-behavior-probe
description: Plan and execute runtime-behavior investigations with
  temporary probe scripts, validation matrices, state controls, and
  findings-first reports. Use only when the user explicitly invokes
  this skill to verify actual runtime behavior, not to restate code.
---
```

Key design elements:

1. **Validation matrix before execution**: The skill requires creating a matrix of test cases (baseline + failure cases) *before* running any probes.
2. **Execution modes**: `single-shot` for deterministic checks, with other modes for non-deterministic behavior.
3. **Temporary artifacts**: Probe scripts are created in temporary locations and cleaned up after. The skill explicitly manages its own artifacts.
4. **Findings-first reporting**: Reports start with unexpected findings, then methodology, then case results. This ensures the most important information is consumed first even if context is compacted.
5. **Explicit invocation only**: The description says "Use only when the user explicitly invokes this skill"—this is not auto-triggered.

**The philosophy**: Don't trust what code *says* it does. Run it and observe. Create a hypothesis, design probes, execute them, and report what actually happened.

### The AGENTS.md Integration Pattern

OpenAI's AGENTS.md for the Agents SDK shows how skills and project guidance work together:

```markdown
## Mandatory Skill Usage

#### `$code-change-verification`
Run before marking work complete when changes affect runtime code,
tests, or build/test behavior.

#### `$implementation-strategy`
Before changing runtime code, exported APIs, external configuration,
persisted schemas, wire protocols, or other user-facing behavior.
Judge breaking changes against the latest release tag.

#### `$pr-draft-summary`
When a task finishes with moderate-or-larger code changes.
```

**The philosophy**: AGENTS.md is the policy layer; skills are the execution layer. AGENTS.md says *when*; skills say *how*. The separation keeps both files focused.

## 6A.2 OpenAI's Curated Skills: The Media Production Pattern

OpenAI's public skills repository (`github.com/openai/skills`) contains curated skills for Codex that reveal a different design pattern: **media production workflows**.

### Dissecting the `imagegen` Skill

The image generation skill demonstrates a pattern for skills that wrap external APIs:

**Workflow structure:**
1. Decide intent (generate vs. edit vs. batch)
2. Collect inputs up front
3. **Augment prompt into structured spec** (this is the key insight)
4. Run the bundled CLI
5. Validate output quality
6. Clean up intermediates

**Prompt augmentation is the core innovation.** The skill doesn't just pass user prompts to the API—it restructures them:

```
Taxonomy classification:
- photorealistic-natural → candid/editorial lifestyle scenes
- product-mockup → product/packaging shots
- ...

Augmentation rules:
- Keep it short; add only details the user already implied
- Always classify into a taxonomy slug
- For edits, explicitly list invariants
  ("change only X; keep Y unchanged")
```

This reveals a design philosophy: **skills are intelligence amplifiers, not just procedure runners**. The skill adds domain knowledge (the taxonomy of image types, the invariant pattern for edits) that the base model wouldn't consistently apply.

### The Reference File Architecture

Every curated skill uses the same reference architecture:

```
imagegen/
├── SKILL.md            # High-level workflow + augmentation rules
├── scripts/
│   └── image_gen.py    # CLI wrapper for deterministic API calls
└── references/
    ├── cli.md          # How to run the CLI
    ├── image-api.md    # API parameter reference
    ├── prompting.md    # Prompt engineering principles
    └── sample-prompts.md  # Copy/paste examples
```

**The reference map in SKILL.md** explicitly tells the agent which file to consult for what:
- `cli.md` → how to *run* operations
- `image-api.md` → what *knobs* exist
- `prompting.md` → *principles* for good prompts
- `sample-prompts.md` → *examples* only, no extra theory

This is **progressive disclosure by function**: the agent navigates to the right reference based on what it needs, rather than loading everything.

## 6A.3 Anthropic's Philosophy: The Agent-Computer Interface (ACI)

Anthropic's deepest contribution to skill design isn't a specific skill—it's the **Agent-Computer Interface (ACI)** concept, which treats tool design as a UX discipline.

### The HCI → ACI Mapping

| HCI Principle | ACI Equivalent | Concrete Example |
|--------------|----------------|-----------------|
| **Affordances** | Tool descriptions and parameter docs | A tool named `search_code` with description stating "returns matching lines with file paths" |
| **Constraints** | Parameter validation and typed schemas | Requiring absolute file paths after observing repeated directory-change errors |
| **Feedback** | Structured, semantic tool responses | Returning "Found 847 results. Please narrow your date range" instead of `ERROR: TOO_MANY_RESULTS` |
| **Error prevention** | Poka-yoke (mistake-proofing) | A 100-line file viewer that prevents context loss from full file dumps |

### The SWE-bench Discovery

Anthropic's team revealed that their SWE-bench performance breakthroughs came primarily from ACI improvements, not model or architecture changes:

> "While building our agent for SWE-bench, we actually spent more time optimizing our tools than on the overall prompt or the agent loop."

Specific ACI design decisions that moved the needle:

1. **Constrained file viewer** (100 lines max): Stopped agents from dumping entire files into context
2. **Search returns filenames only**: Improved downstream tool selection by reducing noise
3. **Syntax-validating linter before edits**: Prevented cascading failures from malformed code
4. **Absolute filepath requirement**: A single parameter constraint eliminated an entire class of directory-change errors
5. **Empty-output messages**: Replaced silent empty returns with explicit "no results found" messages

**The philosophy**: A single constraint change can eliminate an entire failure class. Design tools so the agent can't easily make mistakes, rather than instructing it not to make them.

### Five Principles for Tool Design

Anthropic's September 2025 guide on writing tools distills their production experience:

**1. Choose the right tools to implement**
- Don't wrap every API endpoint. Build tools for how agents think, not how APIs are structured.
- Prefer `search_contacts` over `list_contacts`—agents search, they don't browse.

**2. Namespace tools to define boundaries**
- `asana_search`, `jira_search` not just `search`
- Namespacing by service AND resource: `asana_projects_search`, `asana_users_search`

**3. Return meaningful context**
- Replace UUIDs with human-readable names in responses
- Return semantic information, not raw database output

**4. Optimize for token efficiency**
- Claude Code restricts tool responses to 25,000 tokens by default
- Implement pagination, filtering, and truncation with sensible defaults
- Error messages should guide agents toward better queries: "Found 847 expenses. Please narrow your date range or specify a category filter."

**5. Prompt-engineer tool descriptions**
- Write descriptions like docstrings for a junior developer who will never ask questions
- Include example usage, edge cases, input format requirements, and boundaries from other tools
- Iterate via evaluation: Anthropic found Claude was appending "2025" to search queries, fixed by adjusting the tool description

### Composio's Validation

Composio independently validated these principles, reporting a **10x reduction in tool failures** after applying ACI-style design: snake_case consistency, one-atomic-action per tool, explicit constraint documentation, and strong typing with enums.

## 6A.4 Cursor's Philosophy: Dynamic Context Discovery

Cursor's April 2026 blog on dynamic context discovery reveals their core philosophy: **provide fewer details upfront, make it easier for the agent to pull context on its own**.

### The Shift from Static to Dynamic

Traditional approach:
```
System prompt → [All rules, all tool descriptions, all skill bodies]
                 → Very long static context
                 → Attention dilution
```

Cursor's approach:
```
System prompt → [Minimal metadata, skill names only]
                 → Agent pulls context on demand via tools
                 → Token-efficient, high-signal context
```

### Four Dynamic Context Discovery Techniques

**1. Long tool responses → files**
Instead of truncating long shell outputs (losing data), Cursor writes them to a file. The agent calls `tail` to check the end, then reads more if needed. No data loss, minimal context cost.

**2. Chat history → summarization with references**
When the context window fills, Cursor summarizes but keeps references to the original conversation. The agent can pull in specific earlier context if needed.

**3. Skills → on-demand loading**
Skills are defined by files. The agent gets only names and descriptions in the system prompt. It uses grep, semantic search, and file reading to pull in the full skill when relevant.

**4. MCP tools → synced to folder**
Instead of loading all MCP tool descriptions into the prompt (which can massively bloat context), Cursor syncs tool descriptions to a folder. The agent only sees tool names in the system prompt and looks up the full description when needed. In A/B testing, this reduced total context by ~50% in runs that used MCP tools.

### The Priompt System

Cursor open-sourced **Priompt** (`github.com/anysphere/priompt`)—a prompt management system that compiles prompts as JSX components where each element has a **priority score**. When total context exceeds the model's limit, the lowest-priority elements are dropped first.

This is progressive disclosure taken to the extreme: not just three tiers, but a continuous priority spectrum across every piece of context.

### Cursor's Multi-Agent Research: Lessons on Instructions

Cursor's research on scaling multi-agent systems ("Towards Self-Driving Codebases") revealed hard-won lessons about skill/instruction design for long-running agents:

1. **Spending more time on initial instructions pays off**: Instructions are amplified across all agent runs. A poorly-worded instruction causes repeated failures.
2. **Architecture matters**: Explicitly laying out dependency philosophy and which libraries must not be used changed agent behavior dramatically.
3. **Scope instructions convey intent**: "Generate 20-100 tasks" vs. "Generate 5 tasks" produces fundamentally different agent behavior—not just in quantity but in ambition and approach.
4. **Role separation is critical**: The final design used planners (who never code), subplanners (who own narrow slices), and workers (who only implement). Each role has distinct instructions.

## 6A.5 Manus's Philosophy: The Event-Driven Agent Loop

Manus's leaked system prompt (March 2025) reveals a fundamentally different agent architecture from the others—one built on an **event stream** rather than a conversation history.

### The Event-Driven Architecture

```
Event Stream (chronological):
1. Message: User input
2. Action: Tool use actions and results
3. Observation: Tool execution results
4. Plan: Task planning from Planner module
5. Knowledge: Best practice references from Knowledge module
6. Datasource: Data API documentation
7. System: Miscellaneous events
```

The agent processes this stream iteratively:
1. **Analyze Events**: Understand current state from the stream
2. **Select Tools**: Choose ONE tool call per iteration
3. **Wait for Execution**: Tool runs in sandbox
4. **Iterate**: Repeat until done
5. **Submit Results** or **Enter Standby**

### Key Design Principles from Manus

**1. Tool-only responses**
```
<tool_use_rules>
- Must respond with a tool use (function calling);
  plain text responses are forbidden
</tool_use_rules>
```
The agent NEVER responds with text alone. Every response is an action. This enforces a strict action-oriented loop and prevents the agent from "thinking out loud" without acting.

**2. Information priority hierarchy**
```
Authoritative data from datasource API
  > Web search results
    > Model's internal knowledge
```
This explicit priority prevents the agent from relying on potentially outdated training data when authoritative sources are available.

**3. The todo.md pattern**
```
- Create todo.md file as checklist based on task planning
  from the Planner module
```
Manus uses a physical file (`todo.md`) as the agent's working memory. This survives context compaction and provides a persistent, visible record of progress.

**4. Never calculate mentally**
```
- Use non-interactive `bc` for simple calculations,
  Python for complex math; never calculate mentally
```
This enforces determinism: the agent must use tools for computation rather than attempting mental arithmetic (which LLMs are unreliable at).

### The Sandbox Philosophy

Manus runs in an isolated Ubuntu 22.04 VM with:
- Full sudo access
- Internet connectivity
- Browser, editor, shell, and code execution
- Port exposure for web deployments

This full-sandbox approach means skills can orchestrate real applications, not just manipulate files. A market research skill can browse actual websites, run Python data analysis, and generate real reports—all within a single skill execution.

## 6A.6 Devin's Philosophy: Planning Mode and Confidence

Devin's leaked system prompt reveals a unique two-mode architecture with an emphasis on self-assessment.

### The Two-Mode System

**Planning mode**: The agent gathers information, explores the codebase (read-only), and creates a detailed plan. It cannot make changes.

**Standard mode**: The agent executes the plan using shell, editor, git, and browser tools. It can modify files and run commands.

This enforced separation ensures the agent doesn't start implementing before it understands the problem—a common failure mode in other agents.

### Confidence Ratings

Devin reports confidence using a traffic light system:
- 🟢 High confidence: Proceeds automatically
- 🟡 Medium confidence: Proceeds but flags uncertainty
- 🔴 Low confidence: Waits for user approval

This is correlated with actual success: 🟢 ratings result in **twice the task completion rate** compared to 🔴 ratings.

### The File-as-Memory Pattern

Cognition's blog on rebuilding Devin for Sonnet 4.5 revealed that the model spontaneously started using the filesystem as external memory:

> "The model treats the file system as its memory without prompting. It frequently writes summaries to files."

This behavior—writing intermediate understanding to disk—is now an encouraged pattern. It survives context compaction and provides a persistent record that can be referenced across long-horizon tasks.

### Managed Devins: The Meta-Agent Pattern

Devin can spawn "managed Devins"—child agents running in their own VMs:

```
Main Devin (coordinator)
├── Managed Devin A (VM 1, focused task)
├── Managed Devin B (VM 2, focused task)
└── Managed Devin C (VM 3, focused task)
```

The main Devin scopes work, assigns pieces, monitors progress, resolves conflicts, and compiles results. Each managed Devin gets a clean slate, narrow focus, and its own isolated environment.

**The philosophy**: When context accumulates, focus degrades. Give each subtask a fresh context and a single mission.

## 6A.7 Addy Osmani's Engineering Skills: Process Over Prose

Addy Osmani (Google Chrome engineer) published a production skill pack (`addyosmani/agent-skills`) that encodes Google's engineering culture into 19 skills mapping to the development lifecycle:

```
DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP
```

### Key Design Philosophy

**"Process, not prose"**: Skills are workflows agents follow, not reference docs they read. Each has steps, decision points, and quality gates.

**"Bake in engineering judgment"**: Skills encode *when* to write a spec, *what* to test, *how* to review, and *when* to ship. They embed concepts from Google's engineering culture:
- Hyrum's Law in API design
- The Beyoncé Rule in testing ("if you liked it, you should have put a test on it")
- The "small CLs" principle for incremental implementation

### Example: The Review Pipeline

```
code-review-and-quality → code-simplification →
security-and-hardening → performance-optimization
```

This is not a single monolithic review skill—it's a pipeline of specialized skills, each with a narrow focus. The agent runs them in sequence, with each producing a focused report.

## 6A.8 The `skills-best-practices` Meta-Skill (Minko Gechev)

Minko Gechev (Angular team, Google) published a meta-guide on skill authoring that synthesizes the industry consensus:

### The Validation Loop

1. **Draft** the skill
2. **Test routing**: Give an LLM only the frontmatter and ask it to generate trigger/non-trigger prompts
3. **Test execution**: Run the skill on realistic tasks
4. **Analyze failures**: Use LLMs to review skill transcripts and identify where instructions were ambiguous
5. **Iterate**: Refine based on observed behavior

### Key Rules

- **SKILL.md is for agents, not humans**: Write for LLM consumption patterns
- **Use step-by-step numbering**: Define workflows as strict sequences with decision trees for branches
- **Redundant logic is debt**: If the agent handles something reliably without help, delete the instruction
- **Just-in-time loading**: Files in `references/` are not seen until explicitly read. Use SKILL.md to tell the agent *when* to read them

## Key Takeaways

1. **OpenAI's philosophy**: Skills are tiny CLIs—narrow contracts, deterministic scripts, fail-fast execution. AGENTS.md says *when*; skills say *how*.
2. **Anthropic's philosophy**: Tool design is a UX discipline (ACI). A single parameter constraint can eliminate an entire failure class. Invest more in tools than in prompts.
3. **Cursor's philosophy**: Dynamic context discovery—load less upfront, let the agent pull what it needs. Files are the universal interface for context.
4. **Manus's philosophy**: Event-driven agent loops with tool-only responses. Physical files (todo.md) as persistent working memory. Enforce computation via tools, never mental math.
5. **Devin's philosophy**: Separate planning from execution. Self-assess confidence. Use the filesystem as memory. Spawn fresh agents for focused subtasks.
6. **Community philosophy (Osmani, Gechev)**: Skills encode engineering judgment as process, not prose. Validate skills with LLMs, not just humans. Iterate based on observed agent behavior.
