# Chapter 21: Writing the Body — Instruction Craft for LLMs

The body of SKILL.md is what the agent actually follows. This chapter covers exactly how to write instructions that LLMs execute reliably: section ordering, instruction style, decision trees, input/output contracts, and convergence criteria.

### Sources for This Chapter

| Topic | Source |
|-------|--------|
| Primacy/recency effects on instruction-following | [agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/) |
| IFScale: degradation with instruction density | [agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/) |
| Anthropic: Skill authoring best practices | [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| OpenAI: "Prefer instructions over scripts unless you need determinism" | [developers.openai.com/codex/skills/create-skill](https://developers.openai.com/codex/skills/create-skill) |
| mgechev: "Use step-by-step numbering" | [github.com/mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) |
| All real skills cited below | [openai/openai-agents-python](https://github.com/openai/openai-agents-python/tree/main/.agents/skills) |

---

## 21.1 Section Ordering — Why Position Matters

Research shows LLMs have **primacy bias** (instructions at the top are followed most reliably) and **recency bias** (instructions at the end are recalled well). Instructions in the middle are followed least consistently.

This gives us a template:

```
TOP (strongest recall):
  Hard constraints, defaults, things that must ALWAYS/NEVER happen

MIDDLE (sequential processing):
  Step-by-step workflow

BOTTOM (strong recall):
  Output format, edge cases, guardrails
```

### How OpenAI implements this

Every OpenAI SDK skill follows this exact order:

1. **Overview** — one paragraph saying what the skill does
2. **Quick start** — the minimal sequence of commands (for agents that want to skip details)
3. **Workflow** — numbered steps with decision points
4. **Output format** — exact template for results
5. **Notes/Constraints** — edge cases and guardrails at the bottom

Look at `test-coverage-improver` ([full text](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md)):

```markdown
# Test Coverage Improver

## Overview                    ← What this skill does
## Quick Start                 ← 6-step minimal path
## Workflow Details             ← Deep instructions
## Notes                       ← Constraints at the bottom
```

## 21.2 Imperative Style — Commands, Not Descriptions

LLMs execute commands more reliably than they interpret descriptions.

```markdown
# ❌ Declarative (agent interprets):
The test suite should be run to verify correctness, and the
results should be analyzed for failures that may indicate
regressions in the codebase.

# ✅ Imperative (agent executes):
1. Run `make tests` from the repository root.
2. If any test fails, report the failing test name, file, and
   error message.
3. If all tests pass, proceed to step 4.
```

Every OpenAI production skill uses imperative style. Commands start with verbs: "Run", "Identify", "Confirm", "Draft", "Ask", "Report".

## 21.3 The Quick Start Pattern

OpenAI's skills all include a **Quick Start** section — a compressed version of the full workflow for agents that can handle minimal guidance. This is an optimization: strong models may only need the quick start; weaker models or unusual cases fall through to the detailed workflow.

From `implementation-strategy`:

```markdown
## Quick start
1. Identify the surface you are changing: released public API,
   unreleased branch-local API, internal helper, persisted schema,
   wire protocol, CLI/config/env surface, or docs/examples only.
2. Determine the latest release boundary:
   BASE_TAG="$(.agents/skills/final-release-review/scripts/
     find_latest_release_tag.sh origin 'v*' ...)"
3. Judge breaking-change risk against that latest release tag.
4. Prefer the simplest implementation.
5. Add a compatibility layer only when there is a concrete
   released consumer.
```

**Principle**: Give the agent a fast path (quick start) and a detailed path (full workflow). The quick start is 5 steps; the full workflow expands each step with rules, examples, and edge cases.

## 21.4 Decision Trees — Handling Branches in Workflows

Real workflows branch. Skills must express these branches explicitly, not hope the agent figures them out.

### Pattern A: If/Then in Numbered Steps

From `docs-sync` ([full text](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md)):

```markdown
1. Confirm scope and base branch
   - Identify the current branch and default branch (usually `main`).
   - If the current branch is not `main`, analyze only the diff vs
     `main` to scope doc updates.
   - Avoid switching branches if it would disrupt local changes; use
     `git show main:<file>` or `git worktree add` when needed.
```

The branch is explicit: "If the current branch is not `main`" leads to a specific different action.

### Pattern B: Decision Matrix

From `final-release-review` ([full text](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md)):

```markdown
Blocking triggers (at least one required for BLOCKED):
 - A confirmed regression or bug introduced in BASE...TARGET
 - A confirmed breaking public API change with missing versioning
 - A concrete data-loss, corruption, or security-impacting change
 - A release-critical packaging/build path is broken by the diff

Non-blocking by itself:
 - Large diff size, broad refactor, or many touched files
 - "Could regress" risk statements without concrete evidence
 - Not running tests locally
```

This is a **truth table**: the agent checks each condition and maps to an outcome. The "non-blocking" list is as important as the "blocking" list — it prevents false positives.

### Pattern C: Enumerated Surface Categories

From `implementation-strategy`:

```markdown
## Compatibility boundary rules
- Released public API or documented external behavior:
  preserve compatibility or provide a migration path.
- Interface changes introduced only on the current branch:
  not a compatibility target. Rewrite them directly.
- Interface changes on `main` but added after the latest release tag:
  not a semver breaking change. Rewrite directly.
- Internal helpers, private types, same-branch tests:
  update them directly.
```

Each bullet is a **category → action** mapping. The agent identifies which category the current change falls into, then follows the prescribed action. There is no ambiguity.

## 21.5 Input/Output Contracts

Skills should explicitly define what they receive and what they produce.

### Inputs

From `pr-draft-summary` ([full text](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md)):

```markdown
## Inputs to Collect Automatically (do not ask the user)
- Current branch: `git rev-parse --abbrev-ref HEAD`
- Working tree: `git status -sb`
- Untracked files: `git ls-files --others --exclude-standard`
- Changed files: `git diff --name-only` (unstaged) and
  `git diff --name-only --cached` (staged)
- Latest release tag: `LATEST_RELEASE_TAG=$(.agents/skills/
  final-release-review/scripts/find_latest_release_tag.sh ...)`
- Base reference: `BASE_REF=$(git rev-parse --abbrev-ref
  --symbolic-full-name @{upstream} 2>/dev/null || echo origin/main)`
```

Every input has an **exact command** to obtain it. The agent doesn't decide *how* to gather information — the skill specifies the exact commands.

The "(do not ask the user)" directive is critical — without it, the agent might prompt the user for information it can gather itself.

### Outputs

From `final-release-review`:

```markdown
## Output format (required)
Use the following report structure in every response:

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

Every field is defined. The risk levels use emoji for visual scanning. The "Action" field requires "concrete next step with pass criteria" — not vague suggestions.

From `implementation-strategy`:

```markdown
## Output expectations
When this skill materially affects the implementation approach:
- `Compatibility boundary: latest release tag v0.x.y;
   branch-local interface rewrite, no shim needed.`
- `Compatibility boundary: released RunState schema;
   preserve compatibility and add migration coverage.`
```

Two examples showing the exact format. The agent produces a one-liner in this format.

## 21.6 The "Report First, Act After Approval" Pattern

Multiple OpenAI skills follow this pattern:

```markdown
# docs-sync:
"Provide a report and ask for approval before editing docs."

# test-coverage-improver:
"Draft test ideas per file... Ask the user for approval to
implement the proposed tests; pause until they agree."

# gh-fix-ci:
"Summarize failures for the user... Create a plan...
Implement after approval."
```

**Why this matters for long-running agents**: The pattern creates a checkpoint where a human can review before irreversible changes. This is critical for skills that modify code, deploy artifacts, or alter infrastructure.

### How to write it

```markdown
## Workflow
1-4. [Gather information and analyze]
5. Report findings using the template in "Output format"
6. Ask the user: "Should I proceed with these changes?"
7. If approved, implement the changes
8. After implementation, verify the changes worked
```

The word "pause" or "ask" creates an explicit human-in-the-loop gate.

## 21.7 Scripts vs. Prose — When to Use Each

| Use Scripts When... | Use Prose Instructions When... |
|---------------------|-------------------------------|
| The step must be deterministic (same output every time) | The step requires judgment or adaptation |
| The step involves computation or data transformation | The step involves understanding code and making decisions |
| You want to prevent the agent from improvising | The approach varies based on context |
| The command sequence is long or fragile | The step is a simple tool call |

### How OpenAI uses scripts

From `code-change-verification`:
```markdown
## Resources
### scripts/run.sh
Executes the full verification sequence with fail-fast semantics.
Prefer this entry point to running commands manually.
```

The agent runs one script instead of executing `make format && make lint && make mypy && make tests` manually. The script handles ordering and fail-fast behavior deterministically.

From `gh-fix-ci`:
```markdown
## Quick start
python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number>"
```

The script handles `gh` CLI field drift (when GitHub changes their API field names) and job-log fallbacks — complexity the agent shouldn't manage via prose instructions.

### Cross-skill script references

From `implementation-strategy`:
```markdown
BASE_TAG="$(.agents/skills/final-release-review/scripts/
  find_latest_release_tag.sh origin 'v*' 2>/dev/null || ...)"
```

Skills can call scripts from other skills' directories. This avoids duplicating shared logic.

## 21.8 Constraint Writing — ALWAYS, NEVER, and Emphasis

From [heyuan110.com CLAUDE.md guide](https://www.heyuan110.com/posts/ai/2026-03-05-claude-code-claudemd-best-practices/), confirmed by OpenAI and Anthropic practice:

LLMs respond to emphasis keywords:

| Keyword | Effect | Use For |
|---------|--------|---------|
| `MUST` / `ALWAYS` | Strong positive constraint | Critical requirements |
| `NEVER` / `DO NOT` | Strong negative constraint | Dangerous actions |
| `PREFER` | Soft positive guidance | Default choices |
| `AVOID` | Soft negative guidance | Discouraged patterns |

From `docs-sync`:
```markdown
Only update English docs under docs/** and never touch translated
docs under docs/ja, docs/ko, or docs/zh.
```

From `implementation-strategy`:
```markdown
Do not preserve a confusing abstraction just because it exists
in the current branch diff.
```

From `final-release-review`:
```markdown
Do not block a release solely because you did not run tests locally.
```

These are all at the boundary between instruction and constraint — things the agent would plausibly do wrong without the explicit directive.

## 21.9 Line Budget and Progressive Disclosure

From [agentskills.io/specification](https://agentskills.io/specification):

> Keep your main SKILL.md under 500 lines. Move detailed reference material to separate files.

From [platform.claude.com best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

> Once Claude loads [SKILL.md], every token competes with conversation history and your actual request.

### The reference file pattern

```markdown
# In SKILL.md:
For the full review checklist, see references/review-checklist.md
For common failure patterns, see references/error-cases.md
```

The agent reads SKILL.md (~200 lines), then only reads `references/review-checklist.md` when it reaches the review step. The reference file could be 1000 lines — but it only loads when needed.

OpenAI's `docs-sync` has one reference:
```
references/doc-coverage-checklist.md
```

OpenAI's `runtime-behavior-probe` has four:
```
references/validation-matrix.md
references/error-cases.md
references/openai-runtime-patterns.md
references/reporting-format.md
```

Each reference is loaded only when the corresponding workflow step needs it.

## 21.10 Common Body Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|--------------|-------------|-----|
| Wall of text with no structure | Agent can't extract specific steps | Use numbered steps with headers |
| Declarative instead of imperative | Agent interprets rather than executes | Start each step with a verb |
| No decision branches | Agent freezes or guesses at branch points | Add explicit if/then with each outcome |
| No output format | Agent produces inconsistent results | Specify exact template with field names |
| No convergence criteria | Agent loops forever or stops early | Define "done" explicitly with measurable criteria |
| Instructions buried in middle | Low recall due to lost-in-middle effect | Put critical rules at top and bottom |
| Everything in SKILL.md | Context bloat on activation | Move references to separate files |
| "Be careful" without specifics | Too vague to act on | Replace with specific constraints: "Do NOT force push" |

## 21.11 Putting It All Together — A Body Template

```markdown
# [Skill Name]

## Overview
[One paragraph: what this skill does and when it matters.]

## Quick start
1. [Minimal command or action]
2. [Key decision point]
3. [Verification step]

## Workflow

### Phase 1: Gather
1. [Exact command to collect input A]
2. [Exact command to collect input B]
   - If [condition], use [alternative command]

### Phase 2: Analyze
3. [What to check and how]
4. [Decision: if X then step 5, if Y then step 6]

### Phase 3: Act
5. [Action for case X]
6. [Action for case Y]
   - Report findings using the output format below
   - Ask user for approval before modifying files

### Phase 4: Verify
7. [Run verification command]
8. [Check expected outcome]
   - If verification fails, return to step [N]
   - After 3 failed attempts, report and stop

## Output format
[Exact template with field names and example values]

## Constraints
- NEVER [dangerous action]
- ALWAYS [critical requirement]
- If [edge case], then [specific handling]

## References
- `references/[name].md` for [what it covers]
```
