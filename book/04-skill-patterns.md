# Part II, Chapter 4: Skill Patterns — Recurring Structures Across 30+ Production Skills

This chapter identifies patterns by frequency: a pattern must appear in **at least 5 independently-authored skills**, unless it is a pioneering pattern invented by a top-tier skill that others are now copying. Every pattern cites the skills that demonstrate it.

### Skills Corpus Analyzed

| Source | Skills Inspected | Links |
|--------|-----------------|-------|
| OpenAI Agents SDK | 9 skills | [github](https://github.com/openai/openai-agents-python/tree/main/.agents/skills) |
| OpenAI curated catalog | 5 skills (imagegen, sora, speech, doc, gh-fix-ci) | [github](https://github.com/openai/skills/tree/main/skills/.curated) |
| Addy Osmani | 19 skills | [github](https://github.com/addyosmani/agent-skills) |
| ClawHub top skills | review-code, solo-review, github, gh-issues, gitclaw, pr-commit-workflow, review-pr, requesting-code-review | [clawhub.ai](https://clawhub.ai/skills?sort=downloads) |
| OpenClaw built-in | github, gh-issues, openclaw-pr-maintainer, review-pr | [github](https://github.com/openclaw/openclaw/tree/main/skills) |
| Anthropic official | docx, pptx, xlsx, pdf, canvas-design, slack-gif-creator | [VoltAgent list](https://github.com/VoltAgent/awesome-agent-skills) |

Total: **50+ skills** inspected. Patterns below are ordered by frequency.

---

## Pattern 1: Explicit "When to Use / When NOT to Use" in Description

**Frequency: 30+/50 skills (dominant pattern)**

The most universal pattern. Nearly every well-written skill includes both positive and negative triggers in the description.

**Skills demonstrating this pattern:**

| Skill | Positive Trigger | Negative Trigger |
|-------|-----------------|-----------------|
| OpenAI `code-change-verification` | "when changes affect runtime code, tests, or build/test behavior" | implied: skip for docs-only |
| OpenAI `docs-sync` | "when asked to audit doc coverage, sync docs with code" | "never touch translated docs" |
| OpenAI `pr-draft-summary` | "after moderate-or-larger changes" | "skip only for trivial or conversation-only tasks" |
| OpenAI `implementation-strategy` | "when a task changes exported APIs, runtime behavior, serialized state" | — (scoped by specificity) |
| Osmani `code-review-and-quality` | "before merging any change" | — (universal trigger) |
| Osmani `shipping-and-launch` | "Use when deploying code" | — |
| ClawHub `review-code` | "code review, PR review, merge-readiness check, bug-risk audit" | (implicit in scope) |
| OpenClaw `github` | "PR status, CI checks, issues, API queries" | (scoped to GitHub operations) |
| OpenClaw `gh-issues` | "when working with GitHub issues" | — |

**What this looks like in practice:**

The strongest form combines trigger words + redirect:
```yaml
description: >
  Generate and run Alembic migrations for schema changes.
  Use when adding, modifying, or removing tables, columns,
  indexes, or constraints.
  Don't use for query optimization (use query-optimizer skill).
  Don't use for seed data (use data-seeding skill).
```

**Why it's universal:** Without negative triggers, skills collide. The agent can't distinguish "review code" from "fix code" from "test code" without boundaries.

---

## Pattern 2: Numbered Step-by-Step Workflow

**Frequency: 25+/50 skills**

The body is a numbered, imperative sequence — not paragraphs of explanation.

**Skills demonstrating this pattern:**

- OpenAI `docs-sync` (7 numbered steps)
- OpenAI `test-coverage-improver` (6 numbered steps in Quick Start)
- OpenAI `gh-fix-ci` (8 numbered steps)
- OpenAI `implementation-strategy` (5 numbered Quick Start steps)
- OpenAI `pr-draft-summary` (9 numbered workflow steps)
- Osmani all 19 skills (all use numbered steps)
- ClawHub `review-code` (7 "Core Rules")
- ClawHub `solo-review` (12 "Review Dimensions" each with numbered sub-steps)
- OpenClaw `review-pr` (numbered script calls)
- OpenClaw `pr-commit-workflow` (numbered commit/PR flow)

**The pattern:**
```markdown
## Workflow
1. [Verb] [what to do]
   - If [condition]: [alternative]
2. [Verb] [next step]
3. [Verb] [step with exact command]: `command here`
```

Every step starts with a verb: Confirm, Identify, Run, Collect, Analyze, Report, Ask, Apply, Build, Check.

**Why it works:** LLMs execute numbered sequences more reliably than prose. They track their position in the sequence and know what comes next.

---

## Pattern 3: Structured Output Template

**Frequency: 20+/50 skills**

The skill specifies the exact format of its output — field names, structure, and often example values.

**Skills demonstrating this pattern:**

- OpenAI `final-release-review` — full report template with 🟢/🟡/🔴 risk levels, evidence fields, unblock checklist
- OpenAI `pr-draft-summary` — paste-ready PR block with branch, title, description fields
- OpenAI `docs-sync` — categorized report (doc-first findings, code-first gaps, incorrect/outdated, structural suggestions)
- OpenAI `implementation-strategy` — one-liner format: "Compatibility boundary: ..."
- Osmani `code-review-and-quality` — review checklist with category headers and checkbox items
- ClawHub `solo-review` — 12-dimension report with verdict (SHIP/FIX FIRST/BLOCK), per-dimension status, issues list
- ClawHub `review-code` — findings with severity + confidence + evidence
- OpenClaw `review-pr` — structured JSON findings

**Spectrum of formality:**

| Level | Example | When to use |
|-------|---------|-------------|
| One-liner | `Compatibility boundary: v0.x.y; rewrite, no shim.` | Decision output |
| Categorized list | Doc-first findings / Code-first gaps / Structural suggestions | Audit output |
| Full template | Release call + Risk assessment + Unblock checklist (with emoji and field names) | Gate decisions |
| Multi-section report | 12 dimensions with per-dimension verdicts and final verdict | Comprehensive review |

**Why it matters:** Without a template, the agent produces different output formats every run. With a template, output is consistent, parseable, and comparable.

---

## Pattern 4: Report-Then-Ask-Approval Gate

**Frequency: 15+/50 skills**

The skill separates analysis from action with an explicit "ask before modifying" checkpoint.

**Skills demonstrating this pattern:**

- OpenAI `docs-sync`: "Provide a report and ask for approval before editing docs."
- OpenAI `test-coverage-improver`: "Ask the user for approval to implement the proposed tests; pause until they agree."
- OpenAI `gh-fix-ci`: "Create a plan... Implement after approval."
- OpenAI `implementation-strategy`: "When to stop and confirm" section
- Osmani `code-review-and-quality`: review → verdict → author addresses
- ClawHub `review-code`: "Before creating or changing local files, present the planned write and ask for user confirmation."
- ClawHub `solo-review`: generates report with verdict, then signals pipeline
- OpenClaw `openclaw-pr-maintainer`: triage → label → land only after approval
- OpenClaw `pr-commit-workflow`: "human-written intent requirements" for PRs

**The pattern in code:**
```markdown
## Workflow
1-4. [Gather and analyze]
5. Report findings using the output format above.
6. Ask the user: "Should I proceed with these changes?"
7. If approved, apply changes.
8. After changes, verify with [command].
```

**Why it's so common:** Skills that modify files or state are dangerous without a checkpoint. The gate creates a review boundary and makes the skill testable in two phases (analysis quality, then action quality).

---

## Pattern 5: Quick Start / Fast Path

**Frequency: 12+/50 skills**

A compressed version of the full workflow for strong models or straightforward cases.

**Skills demonstrating this pattern:**

- OpenAI `implementation-strategy`: 5-step Quick Start before the detailed rules
- OpenAI `test-coverage-improver`: 6-step Quick Start
- OpenAI `final-release-review`: Quick Start with tag + diff commands
- OpenAI `gh-fix-ci`: Quick Start with single script command
- All 5 OpenAI curated skills (imagegen, sora, speech, doc, gh-fix-ci): each has Quick Start
- Osmani skills: many have a "quick reference" section

**The pattern:**
```markdown
## Quick start
1. [Essential command]
2. [Key check]
3. [Core action]
4. [Verification]

## Workflow (detailed)
[Full steps with branches, edge cases, error handling]
```

**Why it exists:** Strong models can follow the 4-5 step fast path. The detailed workflow below handles unusual cases. This is **two levels of depth in one file** — the fast path is the "table of contents" for the full workflow.

---

## Pattern 6: Script-Backed Determinism

**Frequency: 12+/50 skills**

Critical operations are handled by scripts (`scripts/run.sh`, `scripts/inspect.py`) rather than prose instructions.

**Skills demonstrating this pattern:**

- OpenAI `code-change-verification`: `scripts/run.sh` (fail-fast verification)
- OpenAI `gh-fix-ci`: `scripts/inspect_pr_checks.py` (API call with fallbacks)
- OpenAI `final-release-review`: `scripts/find_latest_release_tag.sh` (tag lookup)
- OpenAI `imagegen`: `scripts/image_gen.py` (API wrapper)
- OpenAI `sora`: `scripts/sora.py` (video generation CLI)
- OpenAI `speech`: `scripts/text_to_speech.py` (TTS CLI)
- OpenAI `doc`: `scripts/render_docx.py` (document rendering)
- OpenClaw `review-pr`: `scripts/pr-review`, `scripts/pr review-checkout-main`
- OpenClaw `pr-commit-workflow`: `scripts/build_pr_body.sh`

**When to use scripts vs. prose:**

| Scripts | Prose |
|---------|-------|
| Command sequence must be identical every time | Agent needs to reason about context |
| Handles API field drift or format changes | Decision depends on code understanding |
| Involves computation or data transformation | Simple tool call |
| Failure modes need structured handling | Straightforward success/fail |

**Pioneering example** (OpenAI): Cross-skill script references — `implementation-strategy` calls `final-release-review/scripts/find_latest_release_tag.sh`. This is shared infrastructure across skills.

---

## Pattern 7: Decision Table (Category → Action)

**Frequency: 8+/50 skills**

When the workflow involves classification, the skill provides an explicit lookup table rather than prose.

**Skills demonstrating this pattern:**

- OpenAI `implementation-strategy`: 5-row compatibility boundary table (released API → preserve, branch-local → rewrite, internal → update)
- OpenAI `final-release-review`: blocking triggers list + non-blocking list
- OpenAI `imagegen`: taxonomy of image types (photorealistic-natural, product-mockup, etc.)
- Osmani `code-review-and-quality`: 5-axis review (correctness/readability/architecture/security/performance)
- Osmani `shipping-and-launch`: staged rollout strategy table
- ClawHub `solo-review`: verdict logic (SHIP/FIX FIRST/BLOCK) with specific conditions
- ClawHub `review-code`: severity + confidence calibration table
- ClawHub `solo-review`: "Rationalizations Catalog" — thought vs reality table

**The critical innovation:** Including what does NOT qualify alongside what does.

From `final-release-review`:
```markdown
Blocking triggers (at least one required):
 - Confirmed regression
 - Breaking API change with missing versioning

Non-blocking by itself:
 - Large diff size
 - "Could regress" without evidence
```

Without the "non-blocking" list, agents block on vague concerns. The negative list is as important as the positive list.

---

## Pattern 8: Exact Input Collection Commands

**Frequency: 8+/50 skills**

The skill specifies the exact shell commands to gather inputs, often with "(do not ask the user)".

**Skills demonstrating this pattern:**

- OpenAI `pr-draft-summary`: 8 exact git commands for branch, status, files, tags, base ref
- OpenAI `implementation-strategy`: tag-lookup command with fallback
- OpenAI `final-release-review`: `git diff --stat`, `git log --oneline`, `git diff --name-status`
- OpenAI `docs-sync`: `rg "Settings"`, `rg "Config"`, `rg "os.environ"`
- OpenAI `test-coverage-improver`: `make coverage`, `coverage report -m`
- OpenAI `gh-fix-ci`: `gh auth status`, `gh pr view --json`, `gh run view --log`
- ClawHub `solo-review`: exact lint/test/build commands per stack (Next.js, Python, Swift, Kotlin)
- OpenClaw `gh-issues`: curl commands with Bearer tokens

**Why "do not ask the user" matters:** Without this directive, agents default to asking the user for information they could gather themselves. The explicit "(do not ask)" instruction eliminates unnecessary prompts.

---

## Pattern 9: Reference File Architecture

**Frequency: 10+/50 skills**

Large skills split into a lean SKILL.md (navigation) + reference files (depth).

**Skills demonstrating this pattern:**

- OpenAI `imagegen`: 5 reference files (cli.md, image-api.md, prompting.md, sample-prompts.md, codex-network.md)
- OpenAI `sora`: 5 reference files (cli.md, video-api.md, prompting.md, sample-prompts.md, troubleshooting.md)
- OpenAI `speech`: 5 reference files (cli.md, audio-api.md, voice-directions.md, prompting.md, sample-prompts.md)
- OpenAI `runtime-behavior-probe`: 4 reference files (validation-matrix.md, error-cases.md, openai-runtime-patterns.md, reporting-format.md)
- OpenAI `docs-sync`: 1 reference file (doc-coverage-checklist.md)
- OpenAI `final-release-review`: 1 reference file (review-checklist.md)
- ClawHub `review-code`: 8 reference files (setup.md, memory-template.md, review-workflow.md, severity-and-confidence.md, language-risk-checklists.md, test-impact-playbook.md, comment-templates.md, patch-strategy.md)
- Osmani skills: use `references/` for security checklist, performance checklist

**The referencing pattern in SKILL.md:**
```markdown
# Good: tells agent WHEN to read
"Walk through the categories in references/review-checklist.md
when analyzing risk."

# Bad: agent might read eagerly or never
"See references/checklist.md for more details."
```

The key: **trigger the reference read at a specific workflow step**, not as a general pointer.

---

## Pattern 10: Severity / Confidence Labeling System

**Frequency: 7+/50 skills**

When a skill produces findings, each finding gets a severity label and often a confidence score.

**Skills demonstrating this pattern:**

- OpenAI `final-release-review`: 🟢 LOW / 🟡 MODERATE / 🔴 HIGH + evidence requirement
- Osmani `code-review-and-quality`: (no prefix)=required, Critical:=blocks, Nit:=optional, FYI=informational
- ClawHub `solo-review`: SHIP / FIX FIRST / BLOCK verdict + per-dimension PASS/WARN/FAIL
- ClawHub `review-code`: severity + confidence calibration with explicit rules
- OpenClaw `review-pr`: structured JSON findings with severity levels
- Devin: 🟢🟡🔴 confidence ratings (not a SKILL.md but the pattern is adopted)
- OpenClaw `openclaw-pr-maintainer`: bug-fix evidence requirements

**Why it matters for skill authors:** Without severity labels, agents treat all findings as equally important. Users waste time on optional suggestions. The labeling system creates a **triage protocol** inside the skill.

---

## Pattern 11: Anti-Sycophancy / Anti-Rationalization Clauses

**Frequency: 5+/50 skills (pioneering pattern, growing)**

Explicit instructions to counteract known LLM failure modes: agreeing too easily, avoiding hard truths, claiming success without evidence.

**Skills demonstrating this pattern:**

- Osmani `code-review-and-quality`:
  ```
  Don't rubber-stamp. "LGTM" without evidence helps no one.
  Don't soften real issues. Sycophancy is a failure mode in reviews.
  Push back on approaches with clear problems.
  ```

- ClawHub `solo-review`:
  ```
  | "Tests were passing earlier" | Run them NOW. Code changed since then. |
  | "It's just a warning"        | Warnings become bugs. Report them.     |
  | "Good enough to ship"        | Quantify "good enough". Show numbers.  |
  | "I already checked this"     | Fresh evidence only. Stale checks are worthless. |
  ```

- OpenAI `final-release-review`:
  ```
  never produce a BLOCKED call without concrete evidence
  Do not block a release solely because you did not run tests locally
  avoid variance between runs by using explicit gate rules
  ```

- OpenAI `implementation-strategy`:
  ```
  Do not preserve a confusing abstraction just because it exists
  If review feedback claims a change is breaking, verify it against
  the latest release tag before accepting
  ```

- ClawHub `review-code`:
  ```
  Reporting opinions as facts → review credibility drops
  Calling something "probably fine" without tests → silent regressions
  ```

**Why this is a pioneering pattern:** LLMs are trained on helpful, agreeable text. Without explicit counter-instructions, they default to approving, softening criticism, and rationalizing weak evidence. This pattern names the failure mode and provides the opposite instruction.

---

## Pattern 12: Post-Action Verification Step

**Frequency: 10+/50 skills**

After the skill acts, it re-runs a check to verify the action succeeded.

**Skills demonstrating this pattern:**

- OpenAI `code-change-verification`: entire skill IS the verification
- OpenAI `test-coverage-improver`: "After implementation: Rerun coverage, report the updated summary."
- OpenAI `docs-sync`: "Build docs with `make build-docs` after edits to verify."
- OpenAI `gh-fix-ci`: "After changes, suggest re-running tests and `gh pr checks`."
- ClawHub `solo-review`: "Verification Gate: No verdict without fresh evidence. Run actual commands."
- Osmani skills: all review skills include a "Verification" section
- OpenClaw `pr-commit-workflow`: post-push verification

**The pattern:**
```markdown
## After acting
7. Run [verification command]
8. Compare output to expected result
   - If verification fails: return to step [N]
   - After 3 failed attempts: report and stop
```

---

## Pattern Summary Table

| # | Pattern | Frequency | Exemplar |
|---|---------|-----------|----------|
| 1 | When to Use / When NOT to Use | 30+/50 | OpenAI all, Osmani all |
| 2 | Numbered Step-by-Step Workflow | 25+/50 | OpenAI all, Osmani all, solo-review |
| 3 | Structured Output Template | 20+/50 | final-release-review, pr-draft-summary, solo-review |
| 4 | Report-Then-Ask-Approval Gate | 15+/50 | docs-sync, test-coverage-improver, review-code |
| 5 | Quick Start / Fast Path | 12+/50 | implementation-strategy, all OpenAI curated |
| 6 | Script-Backed Determinism | 12+/50 | code-change-verification, all OpenAI curated |
| 7 | Decision Table (Category → Action) | 8+/50 | implementation-strategy, final-release-review |
| 8 | Exact Input Collection Commands | 8+/50 | pr-draft-summary, final-release-review, solo-review |
| 9 | Reference File Architecture | 10+/50 | imagegen, sora, speech, review-code |
| 10 | Severity/Confidence Labeling | 7+/50 | final-release-review, code-review-and-quality, solo-review |
| 11 | Anti-Sycophancy Clauses | 5+/50 (pioneering) | code-review-and-quality, solo-review, final-release-review |
| 12 | Post-Action Verification | 10+/50 | test-coverage-improver, docs-sync, solo-review |
