# Part II, Chapter 4: Skill Patterns — Structural Archetypes

Every production skill fits one of a few recurring structural patterns. This chapter names them, shows the real skill that exemplifies each, and provides a template so you can write your own.

### Sources

| Pattern | Exemplar Skill | Full Text |
|---------|---------------|-----------|
| Gate-keeper | OpenAI `code-change-verification` | [playbooks.com](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification) |
| Report-first | OpenAI `docs-sync` | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md) |
| Report-first | OpenAI `test-coverage-improver` | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md) |
| Decision gate | OpenAI `final-release-review` | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md) |
| Think-before-act | OpenAI `implementation-strategy` | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) |
| Handoff automation | OpenAI `pr-draft-summary` | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md) |
| Debug-and-fix | OpenAI `gh-fix-ci` | [raw SKILL.md](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md) |
| Multi-axis review | Osmani `code-review-and-quality` | [GitHub](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) |
| Prompt augmentation | OpenAI `imagegen` | [GitHub](https://github.com/openai/skills/blob/main/skills/.curated/imagegen/SKILL.md) |

---

## Pattern 1: Gate-Keeper

**Shape**: Run checks → fail-fast on error → report result.

**Exemplar**: OpenAI `code-change-verification`

```
Trigger → make sync (if needed) → make format → make lint →
  make mypy → make tests → done OR fail-report
```

**Key trait**: Strict ordering. Script-backed. The agent cannot improvise the sequence.

**When to use**: Pre-merge verification, pre-deploy validation, pre-release checks.

**Template**:
```markdown
---
name: [check-name]
description: Run [checks] when [trigger]. Skip for [exceptions].
---
# [Check Name]
## Execution
- Prerequisites: [sync/install command if needed]
- Run in order: [cmd1], [cmd2], [cmd3]
- If any step fails, stop and report the failure.
## Resources
### scripts/run.sh
```

---

## Pattern 2: Report-First

**Shape**: Gather → analyze → report → ask approval → act if approved → verify.

**Exemplar**: OpenAI `docs-sync`

```
Confirm scope → Build feature inventory → Doc-first pass →
  Code-first pass → Detect gaps → Report → Ask approval →
  Apply changes → Build docs to verify
```

**Key trait**: The skill produces a structured report and **pauses** before modifying anything.

**When to use**: Audits, coverage analysis, documentation sync, dependency review.

**Template**:
```markdown
---
name: [audit-name]
description: Analyze [target] to find [issues]. Provide a report
  and ask for approval before [action].
---
# [Audit Name]
## Workflow
1. [Gather: commands to collect data]
2. [Analyze: categories to check]
3. Report using output format below
4. Ask user for approval
5. If approved: [apply changes]
6. [Verify: re-run analysis to confirm]
## Output format
[Categorized template: gaps, errors, suggestions, proposed edits]
```

---

## Pattern 3: Decision Gate

**Shape**: Gather evidence → check against criteria → binary decision → structured output.

**Exemplar**: OpenAI `final-release-review`

```
Fetch tags → Diff → Analyze risk → Gate decision
  (🟢 ship / 🔴 blocked) → Structured report
```

**Key trait**: Explicit default bias (GREEN), exhaustive blocking triggers, exhaustive non-blocking list, evidence requirement for any block.

**When to use**: Release readiness, migration approval, security sign-off.

**Template**:
```markdown
---
name: [gate-name]
description: [Make decision] by [analyzing what]. Use before [action].
---
# [Gate Name]
## Gate policy
- Default to [PASS] unless a blocking trigger is satisfied.
- [BLOCK] only with concrete evidence and actionable unblock steps.

Blocking triggers (at least one required):
 - [Condition 1]
 - [Condition 2]

Non-blocking by itself:
 - [Condition that looks scary but isn't blocking]
 - [Another false-positive case]

## Output format
[Binary decision with evidence and unblock checklist]
```

---

## Pattern 4: Think-Before-Act

**Shape**: Classify change → apply decision rules → state the decision → then code.

**Exemplar**: OpenAI `implementation-strategy`

```
Identify surface → Determine release boundary → Apply
  compatibility rules → Output decision statement
```

**Key trait**: The entire skill is a decision procedure. No code is modified. The output is a one-line decision that guides subsequent work.

**When to use**: Architecture decisions, compatibility analysis, approach selection.

**Template**:
```markdown
---
name: [strategy-name]
description: Decide [what] before [action]. Use when [trigger].
---
# [Strategy Name]
## Quick start
1. Classify what you're changing: [categories]
2. Determine the baseline: [command]
3. Apply the rules below
4. State your decision

## Rules
- [Category A]: [prescribed action]
- [Category B]: [prescribed action]
- [Category C]: [prescribed action]

## Default stance
- Prefer [simpler approach] over [complex approach] when [condition].

## When to stop and confirm
- [Escalation trigger 1]
- [Escalation trigger 2]

## Output
[One-liner format with decision and rationale]
```

---

## Pattern 5: Handoff Automation

**Shape**: Auto-gather context → classify → generate structured artifact.

**Exemplar**: OpenAI `pr-draft-summary`

```
Collect git state (auto, no user input) → Detect change type
  from paths → Choose lead verb → Generate PR block
```

**Key trait**: All inputs are collected automatically ("do not ask the user"). The output is a structured artifact ready to paste.

**When to use**: PR descriptions, commit messages, release notes, handoff documents.

**Template**:
```markdown
---
name: [artifact-name]
description: Generate [artifact] after [trigger]. Skip for [exceptions].
---
# [Artifact Name]
## Inputs to Collect Automatically (do not ask the user)
- [Input A]: `[exact command]`
- [Input B]: `[exact command]`

## Workflow
1. Run input commands without asking
2. If no changes detected, skip
3. Classify from [signals]
4. Generate output using template below

## Output format
[Paste-ready template with field names]
```

---

## Pattern 6: Debug-and-Fix

**Shape**: Authenticate → fetch logs → extract failure → summarize → plan → get approval → implement → recheck.

**Exemplar**: OpenAI `gh-fix-ci`

```
Auth check → Resolve PR → Inspect failing checks (script) →
  Scope (GH Actions only) → Summarize → Plan → Approval →
  Implement → Recheck
```

**Key trait**: Scope boundaries ("GitHub Actions only; external providers are out of scope"). Script with fallback. Plan-before-implement gate.

**When to use**: CI debugging, error investigation, incident response.

**Template**:
```markdown
---
name: [debug-name]
description: Debug [what]. Use when [trigger]. [Scope boundaries].
---
# [Debug Name]
## Workflow
1. Verify auth / prerequisites
2. Identify the failing [thing]
3. Fetch logs: [preferred script] or [manual fallback]
4. Scope: [what's in scope] / [what's out of scope]
5. Summarize: [name, URL, log snippet for each failure]
6. Plan the fix
7. Ask for approval
8. Implement
9. Re-run checks to verify
## Resources
### scripts/[inspector].py
```

---

## Pattern 7: Multi-Axis Review

**Shape**: Understand context → review tests → evaluate each axis → label findings → verdict.

**Exemplar**: Osmani `code-review-and-quality` (525 lines — [source](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md))

Five axes: Correctness, Readability, Architecture, Security, Performance.

Finding severity: (no prefix)=required, `Critical:`=blocks, `Nit:`=optional, `FYI`=informational.

**Key trait**: The severity labeling system. Without it, agents treat all comments as equally important. With it, authors know what's required vs. optional.

Also notable: the "approval standard" at the top:
```
Approve when it definitely improves overall code health,
even if it isn't perfect. Perfect code doesn't exist.
```

This prevents a known agent failure mode: blocking everything that isn't flawless.

**When to use**: Code review, design review, security audit.

---

## Pattern 8: Prompt Augmentation

**Shape**: Collect user intent → classify into taxonomy → apply augmentation rules → call API via script.

**Exemplar**: OpenAI `imagegen` ([source](https://github.com/openai/skills/blob/main/skills/.curated/imagegen/SKILL.md))

```
User says "make a hero image for my website" →
  Classify: website-asset →
  Augment: add composition/quality constraints →
  Run scripts/image_gen.py with structured prompt
```

**Key trait**: The skill adds domain expertise (taxonomy, invariant pattern) that the model wouldn't consistently apply. The rule "do not invent new requirements" prevents over-augmentation.

**When to use**: Any skill that wraps a generative API (image, video, speech, document).

---

## Choosing the Right Pattern

| Your task... | Pattern |
|---|---|
| "Run checks before shipping" | Gate-keeper |
| "Analyze X, tell me what's wrong, then fix" | Report-first |
| "Should we ship/approve this?" | Decision gate |
| "How should we approach this?" | Think-before-act |
| "Generate the PR description" | Handoff automation |
| "Fix this CI failure" | Debug-and-fix |
| "Review this code" | Multi-axis review |
| "Generate an image/video/document" | Prompt augmentation |

Most real skills combine two patterns:
- `docs-sync` = Report-first + Gate-keeper (report → approve → act → verify)
- `gh-fix-ci` = Debug-and-fix + Report-first (diagnose → report → approve → fix)
- `final-release-review` = Decision gate + Report-first (analyze → report → gate)
