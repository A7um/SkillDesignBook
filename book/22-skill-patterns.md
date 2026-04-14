# Chapter 22: Skill Patterns — Archetypes from Production

This chapter catalogs the recurring structural patterns found in production skills. Each pattern has a specific shape, and understanding the archetype helps you write new skills faster.

### Sources for This Chapter

| Pattern | Primary Source |
|---------|---------------|
| Gate-keeper | [openai code-change-verification](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification) |
| Report-first | [openai docs-sync](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md), [openai test-coverage-improver](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md) |
| Decision gate | [openai final-release-review](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md) |
| Think-before-act | [openai implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) |
| Handoff automation | [openai pr-draft-summary](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md) |
| Debug-and-fix | [openai gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md) |
| Multi-axis review | [addyosmani code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) |
| Prompt augmentation | [openai imagegen](https://github.com/openai/skills/blob/main/skills/.curated/imagegen/SKILL.md) |
| Empirical probe | [openai runtime-behavior-probe](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/runtime-behavior-probe/SKILL.md) |

---

## Pattern 1: The Gate-Keeper

**Purpose**: Ensure a set of quality checks pass before work is marked complete.

**Shape**:
```
Trigger → Run checks in strict order → Fail-fast on first error → Report
```

**When to use**: Pre-merge verification, pre-deploy validation, pre-release checks.

**Real example**: OpenAI `code-change-verification`

```markdown
---
name: code-change-verification
description: Run the mandatory verification stack when changes affect
  runtime code, tests, or build/test behavior.
---
# Code Change Verification
## Overview
Ensure work is only marked complete after formatting, linting,
type checking, and tests pass.

## Execution
- If dependencies changed, run `make sync` first.
- Run from repository root in this order:
  `make format`, `make lint`, `make mypy`, `make tests`

## Resources
### scripts/run.sh
Executes the full verification sequence with fail-fast semantics.
```

**Key structural elements**:
- Strict ordering (format → lint → type → test)
- Fail-fast: stop at first failure, don't continue
- Script-backed: `scripts/run.sh` ensures determinism
- Skip conditions in description ("skip for docs-only changes")

**Template**:
```markdown
---
name: [check-name]
description: Run [what checks] when [trigger]. Skip for [skip conditions].
---
# [Check Name]
## Execution
- Prerequisites: [dependency sync command]
- Run in order: [cmd1], [cmd2], [cmd3]
- If any step fails, stop and report the failure.
## Resources
### scripts/run.sh
[Fail-fast script wrapping the commands above]
```

---

## Pattern 2: The Report-First

**Purpose**: Analyze a situation and present findings *before* making changes. Human or agent reviews the report, then decides to act.

**Shape**:
```
Trigger → Gather info → Analyze → Report findings → Ask approval → Act if approved
```

**When to use**: Documentation audits, coverage analysis, dependency review, refactoring proposals.

**Real example**: OpenAI `docs-sync`

```markdown
## Workflow
1. Confirm scope and base branch
2. Build a feature inventory from the selected scope
3. Doc-first pass: review existing pages
4. Code-first pass: map features to docs
5. Detect gaps and inaccuracies
6. Produce a Docs Sync Report and ask for approval
7. If approved, apply changes (English only)
```

**Key structural elements**:
- Two analysis passes (doc-first + code-first) before any conclusions
- Explicit report template with categories (Missing, Incorrect, Structural)
- Hard gate at step 6: "ask for approval"
- Scope constraints ("English only", "never touch translated docs")

**Also**: OpenAI `test-coverage-improver`:

```markdown
## Quick Start
1. Run `make coverage`
2. Collect artifacts
3. Summarize coverage: total percentages, lowest files, uncovered lines
4. Draft test ideas per file
5. Ask the user for approval to implement proposed tests; pause
6. After approval, write tests, rerun coverage
```

**Template**:
```markdown
---
name: [audit-name]
description: Analyze [what] and report [findings]. Use when [trigger].
  Provide a report and ask for approval before [action].
---
# [Audit Name]
## Workflow
1. [Gather: specific commands to collect data]
2. [Analyze: what to look for, organized by category]
3. [Report: exact template with categories]
4. Ask user for approval before proceeding
5. [Act: implement approved changes only]
6. [Verify: re-run analysis to confirm improvements]
## Output format
[Report template with categories and evidence fields]
```

---

## Pattern 3: The Decision Gate

**Purpose**: Make a binary decision (proceed/block, approve/reject) with explicit criteria and evidence requirements.

**Shape**:
```
Trigger → Gather evidence → Check against criteria → Decision → Structured output
```

**When to use**: Release readiness, security review, migration approval, production deployment.

**Real example**: OpenAI `final-release-review`

```markdown
## Deterministic gate policy
- Default to 🟢 GREEN LIGHT TO SHIP unless a blocking trigger is met.
- Use 🔴 BLOCKED only with concrete evidence and actionable unblock steps.

Blocking triggers (at least one required):
 - Confirmed regression or bug
 - Breaking public API change with missing versioning
 - Data-loss, corruption, or security-impacting change
 - Release-critical build path is broken

Non-blocking by itself:
 - Large diff size
 - "Could regress" risk statements without evidence
 - Not running tests locally
```

**Key structural elements**:
- **Default bias**: GREEN by default. Requires positive evidence to block.
- **Blocking triggers**: Exhaustive list of what CAN block.
- **Non-blocking list**: Exhaustive list of what CANNOT block (prevents false positives).
- **Evidence requirement**: "cite concrete release-blocking evidence"
- **Unblock checklist**: Required whenever blocked, with exit criteria per item.
- **Severity calibration**: 🟢 LOW / 🟡 MODERATE / 🔴 HIGH with definitions.

---

## Pattern 4: The Think-Before-Act

**Purpose**: Force the agent to make a strategic decision *before* writing any code.

**Shape**:
```
Trigger → Classify the change → Apply decision rules → State the decision → Then code
```

**When to use**: Architecture decisions, compatibility analysis, approach selection.

**Real example**: OpenAI `implementation-strategy`

The skill classifies the change into one of seven surface categories, then applies category-specific rules to decide the compatibility boundary. The output is a one-line decision statement:

```
Compatibility boundary: latest release tag v0.x.y;
branch-local interface rewrite, no shim needed.
```

**Key structural elements**:
- **Surface classification**: The agent must first identify what kind of change this is
- **Rule table**: Each surface type maps to a specific compatibility rule
- **Default stance**: "Prefer deletion over shims when the old shape is unreleased"
- **Escalation triggers**: "Stop and confirm" when certain thresholds are crossed
- **Output format**: Structured one-liner that documents the decision for future reference

---

## Pattern 5: The Handoff Automation

**Purpose**: Generate a structured artifact at the end of a workflow (PR description, release notes, summary).

**Shape**:
```
Trigger (work is done) → Auto-gather context → Classify → Generate structured output
```

**When to use**: PR descriptions, commit messages, release notes, handoff documents.

**Real example**: OpenAI `pr-draft-summary`

```markdown
## Inputs to Collect Automatically (do not ask the user)
- Current branch: `git rev-parse --abbrev-ref HEAD`
- Changed files: `git diff --name-only`
- Latest release tag: [script call]
- Category signals: runtime, tests, examples, docs, build config

## Workflow
1. Run commands without asking the user
2. If no changes detected, skip
3. Infer change type from touched paths
4. Summarize changes in 1-3 sentences
5. Choose lead verb: feature→"adds", fix→"fixes", refactor→"improves"
6. Draft PR title and description using template
```

**Key structural elements**:
- All inputs are auto-gathered (no user prompts)
- Change categorization from file paths (not guessing from content)
- Lead verb selection from a finite list
- Structured output template

---

## Pattern 6: The Debug-and-Fix

**Purpose**: Diagnose a failing CI check or runtime error, then propose and implement a fix.

**Shape**:
```
Trigger → Authenticate → Fetch logs → Extract failure → Summarize → Plan fix → Get approval → Implement → Recheck
```

**Real example**: OpenAI `gh-fix-ci`

```markdown
## Workflow
1. Verify gh authentication
2. Resolve the PR
3. Inspect failing checks (GitHub Actions only)
   - Preferred: run bundled script
   - Manual fallback: `gh pr checks --json ...`
4. Scope non-GitHub Actions checks
   - External providers: report URL only, do not attempt
5. Summarize failures: check name, run URL, log snippet
6. Create a plan
7. Implement after approval
8. Recheck status
```

**Key structural elements**:
- Authentication check first (prevents cascading failures)
- Scope boundaries ("GitHub Actions only; external providers are out of scope")
- Script with fallback (bundled script preferred, manual commands if needed)
- Plan-before-implement gate

---

## Pattern 7: The Multi-Axis Review

**Purpose**: Evaluate work across multiple independent dimensions with severity labeling.

**Shape**:
```
Trigger → Understand context → Review tests → Review each axis → Label findings → Verdict
```

**Real example**: Osmani `code-review-and-quality` (525 lines)

Five review axes with specific questions under each:
1. Correctness (edge cases, error paths, off-by-one)
2. Readability ("Could this be done in fewer lines?")
3. Architecture (patterns, boundaries, duplication)
4. Security (injection, secrets, auth, sanitization)
5. Performance (N+1, unbounded loops, pagination)

Finding labels: (no prefix)=required, Critical:=blocks, Nit:=optional, FYI=informational.

**Key structural element**: The severity labeling system prevents authors from treating all feedback as mandatory.

---

## Pattern 8: The Prompt Augmentation

**Purpose**: Transform a user's raw request into a structured, production-quality prompt before calling an API.

**Shape**:
```
Trigger → Collect user intent → Classify into taxonomy → Apply augmentation rules → Call API
```

**Real example**: OpenAI `imagegen`

```markdown
## Prompt augmentation
Reformat user prompts into a structured spec. Only make implicit
details explicit; do not invent new requirements.

Taxonomy:
- photorealistic-natural → candid/editorial scenes
- product-mockup → product/packaging shots
- ...

Augmentation rules:
- Keep it short; add only details the user already implied
- Always classify into a taxonomy slug
- For edits, explicitly list invariants
```

**Key structural element**: The skill adds domain expertise (taxonomy, invariant pattern) that the base model wouldn't consistently apply. The rule "do not invent new requirements" prevents the agent from over-augmenting.

---

## Pattern 9: The Empirical Probe

**Purpose**: Investigate actual runtime behavior through controlled experiments, not code reading.

**Shape**:
```
Trigger → Define hypothesis → Design validation matrix → Build probe scripts → Execute → Report findings first
```

**Real example**: OpenAI `runtime-behavior-probe`

**Key structural elements**:
- Validation matrix required BEFORE execution
- Execution modes declared per case (single-shot vs. repeated)
- Temporary artifacts (probe scripts in temp dirs, cleaned up after)
- Findings-first reporting (unexpected results before methodology)
- NOT auto-triggered — explicit invocation only

---

## Choosing the Right Pattern

| Your task looks like... | Use this pattern |
|------------------------|-----------------|
| "Run checks before shipping" | Gate-keeper |
| "Analyze X and tell me what's wrong" | Report-first |
| "Should we ship this?" | Decision gate |
| "How should we implement this?" | Think-before-act |
| "Generate the PR description" | Handoff automation |
| "Fix this CI failure" | Debug-and-fix |
| "Review this code" | Multi-axis review |
| "Generate an image/video/document" | Prompt augmentation |
| "Is this actually behaving correctly at runtime?" | Empirical probe |

Most real-world skills combine two patterns. For example:
- `docs-sync` = Report-first + Gate-keeper (report first, then apply approved changes, then verify)
- `final-release-review` = Decision gate + Report-first (analyze, report, then gate)
- `gh-fix-ci` = Debug-and-fix + Report-first (diagnose, report, get approval, fix)
