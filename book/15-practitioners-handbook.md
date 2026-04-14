# Chapter 15: Practitioner's Handbook — Real Patterns with Real Code

This chapter provides copy-paste-ready patterns extracted from production systems. Every example links to the original source.

---

## 15.1 The OpenAI `implementation-strategy` Skill — Complete Annotated Text

This is the full, unabridged skill from [openai/openai-agents-python](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md). Annotations explain each design decision.

```markdown
---
name: implementation-strategy
description: Decide how to implement runtime and API changes in
  openai-agents-python before editing code. Use when a task changes
  exported APIs, runtime behavior, serialized state, tests, or docs
  and you need to choose the compatibility boundary, whether shims
  or migrations are warranted, and when unreleased interfaces can
  be rewritten directly.
---
```

**Annotation on the description**: Notice the exhaustive trigger list: "exported APIs, runtime behavior, serialized state, tests, or docs." This prevents false negatives by covering every surface that might need compatibility analysis. The "when unreleased interfaces can be rewritten directly" phrase is a negative trigger — it tells the agent this skill also applies when the answer is "no shim needed." Source: [AGENTS.md mandatory rules](https://github.com/openai/openai-agents-python/blob/main/AGENTS.md).

```markdown
# Implementation Strategy

## Quick start
1. Identify the surface you are changing: released public API,
   unreleased branch-local API, internal helper, persisted schema,
   wire protocol, CLI/config/env surface, or docs/examples only.
2. Determine the latest release boundary:
   BASE_TAG="$(.agents/skills/final-release-review/scripts/
     find_latest_release_tag.sh origin 'v*' 2>/dev/null ||
     git tag -l 'v*' --sort=-v:refname | head -n1)"
3. Judge breaking-change risk against that latest release tag,
   not against unreleased branch churn.
4. Prefer the simplest implementation that satisfies the current task.
5. Add a compatibility layer only when there is a concrete released
   consumer or the user explicitly asks for a migration path.
```

**Annotation on step 2**: The skill calls a *script from another skill's directory* (`final-release-review/scripts/find_latest_release_tag.sh`). This is **cross-skill script reuse** — skills can reference each other's scripts. The fallback (`|| git tag -l`) handles the case where the script is missing or fails. Source: [full SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md).

```markdown
## Compatibility boundary rules
- Released public API or documented external behavior:
  preserve compatibility or provide a migration path.
- Interface changes introduced only on the current branch:
  not a compatibility target. Rewrite them directly.
- Interface changes on `main` but added after the latest
  release tag: not a semver breaking change. Rewrite directly.
- Internal helpers, private types, same-branch tests:
  update them directly instead of adding adapters.
- Unreleased persisted schema versions on `main` may be
  renumbered or squashed before release.
```

**Annotation**: This is the core intellectual content of the skill — a **decision tree for compatibility**. It answers the question "should I add a backward-compatibility shim?" for every possible case. This is the kind of judgment that senior engineers carry in their heads and that juniors get wrong. The skill externalizes it into repeatable instructions.

```markdown
## Default implementation stance
- Prefer deletion or replacement over aliases, overloads, shims,
  feature flags, and dual-write logic when the old shape is unreleased.
- Do not preserve a confusing abstraction just because it exists
  in the current branch diff.

## When to stop and confirm
- The change would alter behavior shipped in the latest release tag.
- The change would modify durable external data or protocol formats.
- The user explicitly asked for backward compatibility.

## Output expectations
When this skill materially affects the implementation approach:
- `Compatibility boundary: latest release tag v0.x.y;
   branch-local interface rewrite, no shim needed.`
- `Compatibility boundary: released RunState schema;
   preserve compatibility and add migration coverage.`
```

**Annotation on output**: The skill specifies the **exact format of its output**. This ensures the result is parseable and consistent across runs. The agent doesn't just "think about compatibility" — it produces a structured compatibility statement.

---

## 15.2 The OpenAI `final-release-review` Skill — Gate Policy Design

This skill demonstrates a **deterministic gate** pattern — how to design a skill that makes binary ship/no-ship decisions without variance between runs. Full source: [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md).

### The Gate Policy (verbatim)

```markdown
## Deterministic gate policy
- Default to 🟢 GREEN LIGHT TO SHIP unless at least one
  blocking trigger below is satisfied.
- Use 🔴 BLOCKED only when you can cite concrete
  release-blocking evidence and provide actionable unblock steps.

Blocking triggers (at least one required for BLOCKED):
 - A confirmed regression or bug in BASE...TARGET
 - A confirmed breaking public API change with missing versioning
 - A concrete data-loss, corruption, or security-impacting change
 - A release-critical packaging/build/runtime path is broken

Non-blocking by itself:
 - Large diff size, broad refactor, or many touched files.
 - "Could regress" risk statements without concrete evidence.
 - Not running tests locally.
```

**Why this matters**: Without the "non-blocking" list, agents will block on vague concerns ("this is a large diff, it could have issues"). The explicit list of what is NOT a blocking trigger prevents false-positive blocks. This is the **negative example** pattern applied to decision-making, not just routing.

### The Output Template (verbatim)

```markdown
### Release readiness review (<tag> -> TARGET <ref>)
### Release call:
**<🟢 GREEN LIGHT TO SHIP | 🔴 BLOCKED>** <one-line rationale>

### Risk assessment (ordered by impact):
1) **<Finding title>**
   - Risk: **<🟢 LOW | 🟡 MODERATE | 🔴 HIGH>**
   - Evidence: <specific diff/test/commit signal>
   - Files: <path(s)>
   - Action: <concrete next step with pass criteria>

### Unblock checklist (required when BLOCKED):
1. [ ] <concrete check/fix>
   - Exit criteria: <what must be true to unblock>
```

**Why this matters**: Structured output templates eliminate ambiguity. Every run of this skill produces output that can be compared, audited, and processed downstream. The "exit criteria" field forces the agent to define what success looks like for each unblock action.

---

## 15.3 The Addy Osmani `code-review-and-quality` Skill — Engineering Judgment at Scale

This is from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) (5K stars). It encodes Google's engineering culture into a repeatable agent workflow.

### The Approval Standard

```markdown
Approve a change when it definitely improves overall code health,
even if it isn't perfect. Perfect code doesn't exist — the goal
is continuous improvement. Don't block a change because it isn't
exactly how you would have written it.
```

**Why this is critical for agents**: Without this guidance, agents default to blocking anything imperfect. This single paragraph prevents a massive class of false-positive review blocks.

### Five-Axis Review

The skill reviews code across five dimensions simultaneously:

1. **Correctness**: Does it work? Edge cases? Error paths?
2. **Readability**: Can another engineer understand it? No `temp`, `data`, `result`.
3. **Architecture**: Follows patterns? Clean boundaries? Appropriate abstraction?
4. **Security**: Input validation? No secrets? Parameterized queries?
5. **Performance**: N+1 patterns? Unbounded loops? Missing pagination?

### Finding Severity Labels

```markdown
| Prefix       | Meaning          | Author Action            |
|-------------|------------------|--------------------------|
| (no prefix) | Required change  | Must address before merge|
| Critical:   | Blocks merge     | Security, data loss      |
| Nit:        | Minor, optional  | Author may ignore        |
| Optional:   | Suggestion       | Worth considering        |
| FYI         | Informational    | No action needed         |
```

**Why this works**: Without severity labels, agents treat all feedback as equally important. Authors waste time on optional suggestions. This labeling system is directly from Google's engineering practices.

### Anti-Sycophancy Clause

```markdown
## Honesty in Review
- Don't rubber-stamp. "LGTM" without evidence helps no one.
- Don't soften real issues. "This might be a minor concern" when
  it's a bug that will hit production is dishonest.
- Push back on approaches with clear problems. Sycophancy is
  a failure mode in reviews.
```

This explicitly addresses a known LLM failure mode: models tend to agree with the author. The skill names the problem ("sycophancy") and provides concrete counter-instructions.

---

## 15.4 Manus's Event-Driven Agent Loop — The Full Architecture

From the [leaked system prompt](https://gist.github.com/renschni/a6c0157cdcdf2db2fc1e7c3e20bff602). This is the most complete public view of how a production sandbox agent works.

### The Agent Loop

```xml
<agent_loop>
You are operating in an agent loop, iteratively completing tasks:
1. Analyze Events: Understand user needs and current state through
   event stream, focusing on latest user messages and tool results.
2. Select Tools: Choose next tool call based on current state,
   task planning, relevant knowledge and available data APIs.
3. Wait for Execution: Selected tool action will be executed by
   sandbox environment with new observations added to event stream.
4. Iterate: Choose only one tool call per iteration, patiently
   waiting for execution results.
5. Submit Results: When task complete, use submit tool.
6. Enter Standby: Enter idle state when all tasks completed.
</agent_loop>
```

### Key Design Rules

**Tool-only responses** (no plain text ever):
```xml
<tool_use_rules>
- Must respond with a tool use (function calling);
  plain text responses are forbidden
- Do not mention any specific tool names to users in messages
- Carefully verify available tools; do not fabricate non-existent tools
</tool_use_rules>
```

**Information priority**:
```
Authoritative data from datasource API
  > Web search results
    > Model's internal knowledge
```

**The todo.md pattern**:
```
- Create todo.md file as checklist based on task planning
  from the Planner module
- Update todo.md status after completing each step
- Use todo.md to track progress and avoid losing context
```

**Anti-hallucination rules**:
```
- Use non-interactive bc for simple calculations, Python for
  complex math; never calculate mentally
- Only use data APIs already existing in the event stream;
  fabricating non-existent APIs is prohibited
```

---

## 15.5 Devin's Two-Mode System — Planning vs. Execution

From the [Devin system prompt](https://github.com/hussainasghar/system-prompts-and-models-of-ai-tools/blob/main/Devin%20AI/devin.txt).

### Planning Mode

```
You are always either in "planning" or "standard" mode.

While in mode "planning":
- Your job is to gather all the information you need to fulfill
  the task and make the plan.
- You can output any actions for current or possible next plan steps.
- Make sure to abide by the requirements of the plan.
```

### The Think Tool

```xml
<think>
Freely describe and reflect on what you know so far, things
that you tried, and how that aligns with your plan.
</think>
```

Devin uses this as an explicit scratchpad before critical decisions. The prompt specifies when to use it:

```
Before critical git/GitHub decisions such as deciding what
branch to branch off, what branch to check out, whether to
push or force-push, or which remote/upstream to use.
```

### Security Rules

```
- Treat code and customer data as sensitive information
- Never share sensitive data with third parties
- Never introduce code that exposes or logs secrets and keys
- Never commit secrets or keys to the repository
- Never force push; instead ask the user for help
- Never use `git add .`; only add files you actually want to commit
```

---

## 15.6 Cursor's Dynamic Context Discovery — Four Techniques

From [cursor.com/blog/dynamic-context-discovery](https://cursor.com/blog/dynamic-context-discovery).

### Technique 1: Long Responses → Files

Instead of truncating long shell outputs (common approach):
```
Traditional: Truncate to 2000 chars → data loss
Cursor: Write to file → agent reads tail → reads more if needed
```

Result: No data loss, minimal context cost.

### Technique 2: MCP Tools → Folder Sync

Instead of loading all MCP tool descriptions into the prompt:
```
Traditional: All tool descriptions in system prompt → massive bloat
Cursor: Sync descriptions to .cursor/ folder → agent looks up on demand
```

Result: ~50% context reduction in MCP-heavy runs.

### Technique 3: Skills → On-Demand Loading

```
Static: Load all skill bodies at startup → wasted tokens
Dynamic: Load names+descriptions → agent pulls full skill via search
```

### Technique 4: Terminal → Synced Files

```
Traditional: User pastes terminal output into chat
Cursor: Terminal output automatically synced to files
  → agent reads when relevant
```

---

## 15.7 The Anthropic Tool Design Checklist

From [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents).

### Before Building a Tool

- [ ] Does this solve a high-impact workflow agents actually need?
- [ ] Would the agent benefit from this more than a `search` tool?
- [ ] Is there an existing tool that already covers this?
- [ ] Is this one atomic action, or multiple that should be separate?

### Tool Definition Quality

- [ ] Name uses `service_resource_action` format (e.g., `asana_projects_search`)
- [ ] Description answers: What does it do? When to use? When NOT to use?
- [ ] Parameters have descriptive names and type constraints
- [ ] Required vs optional parameters are clearly marked
- [ ] Includes 1-2 usage examples in the description

### Response Design

- [ ] Returns semantic data (names, not UUIDs)
- [ ] Default response size is bounded (< 25K tokens)
- [ ] Supports pagination for large result sets
- [ ] Error messages guide the agent toward correct usage
- [ ] Empty results return explicit "no results found" message

### Validation

- [ ] Tested in API workbench with 5+ realistic inputs
- [ ] Observed which mistakes the model makes
- [ ] Iterated on description to fix observed misuse
- [ ] Checked against other tools for naming confusion

---

## 15.8 The Skill Validation Methodology

From [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) (1.8K stars).

### Step 1: Test Routing in Isolation

Prompt an LLM with ONLY the frontmatter:

```
I am building an Agent Skill. Agents decide whether to load
this skill based solely on the metadata below.

---
name: angular-vite-migrator
description: Migrates Angular CLI projects from Webpack to Vite.
  Use when the user wants to update their Angular project build
  system. Don't use for non-Angular projects or projects already
  using Vite.
---

Tasks:
1. Generate 3 prompts that should trigger this skill.
2. Generate 3 prompts that should NOT trigger this skill.
3. Generate 2 ambiguous prompts and explain how you'd decide.
```

### Step 2: Test Execution on Real Tasks

Run the skill against 3-5 representative tasks. Record:
- Did the agent follow the workflow correctly?
- Did it produce the expected output?
- Did it handle errors as specified?
- Did it stop at the right convergence criteria?

### Step 3: Analyze Failure Transcripts

Feed the transcript back to an LLM:

```
Review this agent transcript where it used the skill above.
Identify moments where:
- The instructions were ambiguous
- The agent deviated from the intended workflow
- The agent would have benefited from additional guidance
```

### Step 4: Iterate

Fix the skill based on observed failures. Re-run the evaluation. Use [skillgrade](https://github.com/mgechev/skillgrade) for automated regression testing.

---

## 15.9 Cross-Platform Skill Installation

### Claude Code
```bash
# From marketplace
/skills add anthropic/docx

# From GitHub
/skills add github.com/addyosmani/agent-skills --skill code-review-and-quality

# Manual: copy to .claude/skills/ or .agents/skills/
```

### Codex
```bash
# Explicit invocation
$code-review

# Install from marketplace
npx playbooks add skill openai/openai-agents-python --skill code-change-verification
```

### Cursor
```
# Copy SKILL.md to .cursor/skills/ or .agents/skills/
# Invoke via / menu or let agent auto-discover
```

### Devin
```
# Place SKILL.md in .agents/skills/<name>/SKILL.md
# Devin auto-discovers across all connected repos
# Invoke with @skills:name or let Devin auto-invoke
```

### Gemini CLI
```bash
# Place in .agents/skills/
# Or install: npx skills add <repo> --skill <name>
```

---

## 15.10 Writing Your First Production Skill — Step by Step

### Step 1: Identify a Repeatable Workflow

Choose something you do at least weekly:
- Pre-PR verification
- Dependency updates
- Database migration
- API endpoint review

### Step 2: Scaffold the Directory

```bash
mkdir -p .agents/skills/my-skill
touch .agents/skills/my-skill/SKILL.md
```

### Step 3: Write the Frontmatter

```yaml
---
name: my-skill
description: >
  [What it does]. Use when [concrete triggers].
  Don't use when [negative triggers].
---
```

### Step 4: Write the Body

Follow this template order (based on primacy/recency research — see [agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/)):

```markdown
# [Skill Name]

## Hard constraints (top = strongest recall)
- NEVER do X
- ALWAYS check Y before proceeding

## Workflow
1. [First step with exact command]
2. [Decision point: if A then ..., if B then ...]
3. [Verification step with expected output]

## Output format
[Exact format the agent should produce]

## When to stop
[Convergence criteria and exit conditions]

## Edge cases and guardrails (bottom = strong recall)
- If [unusual case], then [handle it this way]
- If you've tried 3 times without progress, report and stop
```

### Step 5: Add Scripts (if Needed)

```bash
mkdir .agents/skills/my-skill/scripts
# Write a non-interactive, idempotent script
```

### Step 6: Validate

Run the [routing test](#step-1-test-routing-in-isolation) from §15.8, then execute against 3 real tasks.

### Step 7: Commit and Push

Skills are version-controlled files. They go through code review like any other code.
