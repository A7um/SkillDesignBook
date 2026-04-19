# Part II, Chapter 3: Writing the Body

This chapter covers every structural decision you make when writing the SKILL.md body: section order, instruction style, decision trees, input collection, output templates, scripts, and constraints. Every technique is demonstrated with production code.

### Sources

| Source | URL |
|--------|-----|
| Primacy/recency research | [agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/) (ComplexBench NeurIPS 2024, IFScale 2025) |
| Anthropic skill authoring best practices | [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| OpenAI "prefer instructions over scripts" | [developers.openai.com/codex/skills/create-skill](https://developers.openai.com/codex/skills/create-skill) |
| Gechev "step-by-step numbering" | [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) |
| All OpenAI Agents SDK skills | [github.com/openai/openai-agents-python/.agents/skills](https://github.com/openai/openai-agents-python/tree/main/.agents/skills) |
| `implementation-strategy` full text | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) |
| `final-release-review` full text | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md) |
| `docs-sync` full text | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md) |
| `pr-draft-summary` full text | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md) |
| `test-coverage-improver` full text | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md) |

---

## 3.1 Section Order

Every OpenAI SDK skill follows the same section sequence:

```
1. Overview         — one paragraph: what and why
2. Quick Start      — compressed 5-6 step path
3. Workflow          — full numbered steps with branches
4. Output Format     — exact template
5. Notes/Constraints — edge cases, guardrails
```

This isn't arbitrary. It exploits how LLMs process instructions:

| Position | LLM recall | What goes here |
|----------|-----------|----------------|
| Top | Strongest (primacy) | Overview + hard constraints |
| Upper-middle | Good | Quick start / happy path |
| Middle | Weakest | Detailed workflow steps |
| Lower-middle | Moderate | Output format |
| Bottom | Strong (recency) | Edge cases + NEVER rules |

The **Quick Start** section is a key pattern: it gives the agent a fast path for straightforward cases. Strong models may only read this. The full Workflow below it handles edge cases and complex scenarios.

## 3.2 Imperative Style

Every instruction is a command, not a description:

```markdown
# ❌ Declarative:
The test suite should be run and results analyzed for regressions.

# ✅ Imperative:
1. Run `make tests` from the repository root.
2. If any test fails, report the failing test name and error.
3. If all tests pass, proceed to step 4.
```

OpenAI's `docs-sync` workflow begins:

```markdown
1. Confirm scope and base branch
   - Identify the current branch and default branch (usually `main`).
   - If the current branch is not `main`, analyze only the diff
     vs `main` to scope doc updates.
```

Every line starts with a verb: Confirm, Identify, Analyze, Capture, Use, Walk, Review, Determine, Note, Detect, Produce, Ask, Edit, Build.

## 3.3 Collecting Inputs

Top skills specify the **exact commands** to gather inputs, and explicitly state "(do not ask the user)".

From `pr-draft-summary`:

```markdown
## Inputs to Collect Automatically (do not ask the user)
- Current branch: `git rev-parse --abbrev-ref HEAD`
- Working tree: `git status -sb`
- Untracked files: `git ls-files --others --exclude-standard`
- Changed files: `git diff --name-only` and `git diff --name-only --cached`
- Latest release tag:
  LATEST_RELEASE_TAG=$(.agents/skills/final-release-review/scripts/
    find_latest_release_tag.sh origin 'v*' 2>/dev/null ||
    git tag -l 'v*' --sort=-v:refname | head -n1)
- Base reference:
  BASE_REF=$(git rev-parse --abbrev-ref --symbolic-full-name
    @{upstream} 2>/dev/null || echo origin/main)
```

This is a critical pattern: **give the agent the exact shell command for every input**. Don't say "find out what branch you're on" — say `git rev-parse --abbrev-ref HEAD`.

From `docs-sync`:

```markdown
- Use targeted search to find option types and feature flags:
  `rg "Settings"`, `rg "Config"`, `rg "os.environ"`, `rg "OPENAI_"`
```

Specific search commands, not "search for configuration-related code."

## 3.4 Decision Trees

When the workflow branches, you must express the branch explicitly. Three patterns from production:

### Pattern A: If/Then Steps

From `docs-sync`:

```markdown
1. Confirm scope and base branch
   - If the current branch is not `main`, analyze only the
     diff vs `main` to scope doc updates.
   - Avoid switching branches if it would disrupt local changes;
     use `git show main:<file>` instead.
```

### Pattern B: Category → Action Table

From `implementation-strategy`:

```markdown
## Compatibility boundary rules
- Released public API: preserve compatibility or migration path.
- Changes on current branch only: rewrite directly.
- Changes on `main` after latest release tag: rewrite directly.
- Internal helpers, private types: update directly.
```

### Pattern C: Trigger / Non-Trigger Lists

From `final-release-review`:

```markdown
Blocking triggers (at least one required for BLOCKED):
 - Confirmed regression or bug
 - Breaking API change with missing versioning
 - Data-loss or security-impacting change

Non-blocking by itself:
 - Large diff size
 - "Could regress" without evidence
 - Not running tests locally
```

The non-trigger list is as important as the trigger list. Without it, agents block on vague concerns.

## 3.5 Output Templates

The best skills define the **exact output format**.

`final-release-review` — full structured template:

```markdown
### Release readiness review (<tag> -> TARGET <ref>)
### Release call:
**<🟢 GREEN LIGHT TO SHIP | 🔴 BLOCKED>** <one-line rationale>
### Risk assessment (ordered by impact):
1) **<Finding title>**
   - Risk: **<🟢 LOW | 🟡 MODERATE | 🔴 HIGH>**
   - Evidence: <specific signal>
   - Files: <path(s)>
   - Action: <next step with pass criteria>
### Unblock checklist (required when BLOCKED):
1. [ ] <concrete check/fix>
   - Exit criteria: <what must be true>
```

`implementation-strategy` — concise one-liner:

```
Compatibility boundary: latest release tag v0.x.y;
branch-local interface rewrite, no shim needed.
```

`docs-sync` — categorized report:

```markdown
## Docs Sync Report
- Doc-first findings: Page + missing content → evidence + location
- Code-first gaps: Feature + evidence → suggested doc page
- Incorrect/outdated: Doc file + issue + correct info + evidence
- Structural suggestions: Proposed change + rationale
- Proposed edits: Doc file → concise change summary
- Questions for the user
```

`pr-draft-summary` — paste-ready PR block:

```markdown
# Pull Request Draft
## Branch name suggestion
git checkout -b <suggestion>
## Title
<single-line imperative title>
## Description
<"This pull request resolves/updates/adds ...">
```

Rule: **specify every field name, its type, and an example value**.

## 3.6 The Approval Gate

For skills that modify files, include an explicit pause:

```markdown
# docs-sync:
6. Produce a Docs Sync Report and ask for approval
7. If approved, apply changes (English only)

# test-coverage-improver:
5. Ask the user for approval; pause until they agree.
6. After approval, write the tests.

# gh-fix-ci:
6. Create a plan.
7. Implement after approval.
```

Pattern: Analysis steps → Report → "Ask" / "Pause" → Action steps → Verification.

## 3.7 Post-Action Verification

Top skills include a verification step after acting:

```markdown
# test-coverage-improver:
"After implementation: Rerun coverage, report the updated summary."

# docs-sync:
"Build docs with `make build-docs` after edits to verify
the docs site still builds."

# code-change-verification:
"Run the full verification sequence... Prefer this entry point."

# gh-fix-ci:
"After changes, suggest re-running the relevant tests
and `gh pr checks` to confirm."
```

## 3.8 Using `references/` for Depth

Keep SKILL.md under 500 lines. Move depth to reference files:

```
# In SKILL.md:
"Walk through the categories in references/review-checklist.md"
"See references/cli.md for full command documentation"
"Open references/validation-matrix.md for case templates"
```

The agent reads the reference file only when it reaches that step. Files in `references/` consume zero tokens until explicitly opened.

OpenAI's skill structures:

```
docs-sync/
├── SKILL.md
├── agents/          # Codex-specific metadata
└── references/
    └── doc-coverage-checklist.md

imagegen/
├── SKILL.md
├── scripts/
│   └── image_gen.py
└── references/
    ├── cli.md
    ├── image-api.md
    ├── prompting.md
    ├── sample-prompts.md
    └── codex-network.md
```

## 3.9 Constraint Language

Words that reliably shape LLM behavior:

| Keyword | Strength | Example |
|---------|----------|---------|
| NEVER / DO NOT | Hard negative | "Do not block a release solely because you did not run tests locally" |
| ALWAYS / MUST | Hard positive | "Always use the fixed repository URL" |
| PREFER | Soft positive | "Prefer the console output from `coverage report -m`" |
| AVOID | Soft negative | "Avoid switching branches if it would disrupt local changes" |

From `final-release-review`:
```
"never produce a BLOCKED call without concrete evidence"
"Do not block a release solely because..."
"avoid variance between runs by using explicit gate rules"
```

## 3.10 Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| Wall of text | Agent can't extract steps | Numbered steps with headers |
| "Be careful with X" | Too vague to act on | "DO NOT X. Instead, do Y." |
| No branches in workflow | Agent freezes at decision points | Explicit if/then for every branch |
| Undeclared output format | Inconsistent output every run | Exact template with placeholders |
| "Gather relevant information" | Agent decides what's relevant (badly) | Exact commands: `git status -sb`, `rg "Config"` |
| Everything in SKILL.md | Token bloat on activation | `references/` for detail, SKILL.md for navigation |
| No skip conditions in description | Triggers on every vaguely related task | "Skip for docs-only changes" |

## 3.11 Complete Body Template

```markdown
# [Skill Name]

## Overview
[One paragraph: what this does and when it matters.]

## Quick start
1. [Essential command with exact syntax]
2. [Key decision or check]
3. [Core action]
4. [Verification step]

## Workflow

### Gather
1. Collect [input A]: `[exact command]`
2. Collect [input B]: `[exact command]`
   - (do not ask the user)

### Analyze
3. [What to examine, organized by category]
4. Decision:
   - If [condition A]: → proceed to step 5
   - If [condition B]: → proceed to step 6
   - If [neither]: → report to user and stop

### Report
5. Output findings using the format below.
6. Ask the user for approval before modifying any files.

### Act (after approval)
7. [Specific action steps]
8. [Post-action verification command]
   - If verification fails: return to step [N]
   - After 3 failed attempts: report and stop

## Output format
[Exact template — every field named, typed, with example]

## Constraints
- NEVER [dangerous action]
- ALWAYS [critical requirement]
- If [edge case], then [specific handling]

## References
- `references/[name].md` — [what it covers and when to read it]
```
