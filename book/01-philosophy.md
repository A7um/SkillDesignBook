# Part I: Philosophy — What the Best Skills Teach Us

This part distills the design philosophy behind the best production skills by inspecting them directly. Every principle here was extracted by reading the actual SKILL.md files that ship in OpenAI's Agents SDK, OpenAI's curated skill catalog, Addy Osmani's engineering skills, and the Anthropic/Cursor/Devin/Manus systems — then asking: *what did the author do, and why?*

### Sources Inspected

| Skill Set | Where to Read | Star Count |
|-----------|---------------|------------|
| OpenAI Agents SDK (9 skills) | [github.com/openai/openai-agents-python/.agents/skills](https://github.com/openai/openai-agents-python/tree/main/.agents/skills) | 21K |
| OpenAI curated skills (imagegen, sora, speech, doc, gh-fix-ci) | [github.com/openai/skills](https://github.com/openai/skills/tree/main/skills/.curated) | 16K |
| Addy Osmani's engineering skills (19 skills) | [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 5K |
| Anthropic skill authoring guide | [platform.claude.com: best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | — |
| Minko Gechev's authoring guide | [github.com/mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) | 1.8K |
| Manus system prompt (leaked) | [gist.github.com/renschni](https://gist.github.com/renschni/a6c0157cdcdf2db2fc1e7c3e20bff602) | — |
| Devin system prompt (leaked) | [github.com/hussainasghar](https://github.com/hussainasghar/system-prompts-and-models-of-ai-tools/blob/main/Devin%20AI/devin.txt) | 70 |
| Agent Skills specification | [agentskills.io/specification](https://agentskills.io/specification) | — |

---

## 1.1 A Skill Is a Procedure, Not Documentation

The single most consistent property of every top-tier skill: **it reads like a run-book, not a wiki page**.

Look at OpenAI's `code-change-verification` ([source](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification)):

```markdown
## Execution
- If dependencies changed, run `make sync` first.
- Run from repository root in this order:
  `make format`, `make lint`, `make mypy`, `make tests`
```

Four imperative commands. No background. No explanation of what linting is. No history of why this order was chosen. The agent doesn't need to understand — it needs to execute.

Contrast this with how a junior engineer might write it:

```markdown
## About Verification
The verification process is important to ensure code quality.
Formatting ensures consistent style across the codebase, while
linting catches common errors. Type checking with mypy provides
additional safety. Tests verify that existing functionality is
not broken by new changes.
```

The second version is informative to a human reader but useless to an agent. The agent can't extract "run `make format` first" from a paragraph about what formatting is.

**Principle 1: Write procedures the agent can execute, not documents the agent can read.**

Addy Osmani encodes this explicitly: "**Process, not prose.** Skills are workflows agents follow, not reference docs they read." ([source](https://github.com/addyosmani/agent-skills))

---

## 1.2 One Job Per Skill

Every OpenAI Agents SDK skill does exactly one thing:

| Skill | One Job |
|-------|---------|
| `code-change-verification` | Run the verification stack |
| `implementation-strategy` | Decide compatibility boundary |
| `final-release-review` | Gate the release |
| `docs-sync` | Find doc gaps |
| `pr-draft-summary` | Generate PR description |
| `test-coverage-improver` | Find and propose coverage improvements |
| `gh-fix-ci` | Debug a failing CI check |

No skill tries to do two things. `docs-sync` finds gaps and proposes edits — it doesn't also run the linter. `final-release-review` gates the release — it doesn't also update the changelog.

When OpenAI needs code review AND release gating, they use two separate skills with separate triggers. The AGENTS.md file orchestrates when each one runs:

```markdown
# From AGENTS.md:
- Run `$code-change-verification` when runtime code changes.
- Use `$implementation-strategy` before editing runtime or API changes.
- Use `$final-release-review` before any release.
```

**Principle 2: One skill, one job. Orchestrate via AGENTS.md, not by cramming multiple workflows into one file.**

OpenAI's official guidance: "Keep each skill focused on one job." ([source](https://developers.openai.com/codex/skills/create-skill))

---

## 1.3 The Description Is Routing Logic

In every top-tier skill, the description field is written as **routing logic** — it tells the agent precisely when to activate, not what the skill conceptually does.

OpenAI's `pr-draft-summary` ([source](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md)):

```yaml
description: >
  Create the required PR-ready summary block, branch suggestion,
  title, and draft description for openai-agents-python. Use in
  the final handoff after moderate-or-larger changes to runtime
  code, tests, examples, build/test configuration, or docs with
  behavior impact; skip only for trivial or conversation-only
  tasks, repo-meta/doc-only tasks without behavior impact, or
  when the user explicitly says not to include the PR draft block.
```

This is a decision procedure: IF (moderate-or-larger changes AND touches runtime/tests/examples/config/docs-with-impact) AND NOT (trivial OR conversation-only OR user-says-no) THEN activate.

**Principle 3: Write the description as an if/then activation rule, not a marketing tagline.**

OpenAI's blog: "Your skill's description is effectively the model's decision boundary." ([source](https://developers.openai.com/blog/skills-shell-tips))

---

## 1.4 Scripts for Determinism, Prose for Judgment

OpenAI draws a sharp line between what goes in scripts and what stays in the SKILL.md body.

**Scripts** handle things that must be deterministic:
- `code-change-verification/scripts/run.sh` — the exact command sequence with fail-fast
- `gh-fix-ci/scripts/inspect_pr_checks.py` — GitHub API calls with field-drift fallbacks
- `final-release-review/scripts/find_latest_release_tag.sh` — tag lookup from remote
- `imagegen/scripts/image_gen.py` — API call with structured parameters

**SKILL.md prose** handles things that require judgment:
- Whether a change is a breaking change (requires reading and reasoning)
- Which coverage gaps are highest-priority (requires understanding the codebase)
- Whether a doc is "outdated" (requires comparing docs to code)
- Whether a CI failure is in your code or upstream (requires log analysis)

**Principle 4: Use scripts when the output must be identical every time. Use prose instructions when the agent needs to reason about context.**

OpenAI's guidance: "Prefer instructions over scripts unless you need deterministic behavior or external tooling." ([source](https://developers.openai.com/codex/skills/create-skill))

---

## 1.5 Report First, Act After Approval

Three of OpenAI's nine SDK skills enforce a **report → approval → action** gate:

- `docs-sync`: "Provide a report and ask for approval before editing docs."
- `test-coverage-improver`: "Ask the user for approval to implement the proposed tests; pause until they agree."
- `gh-fix-ci`: "Summarize failures... Create a plan... Implement after approval."

And `implementation-strategy` gates action at the conceptual level: you must decide the compatibility boundary *before* writing any code.

This is not just safety. It's a skill design pattern that **splits analysis from action**, making each phase testable independently. A skill that reports well but acts wrong is easier to debug than one that silently does everything.

**Principle 5: For skills that modify code or state, separate analysis from action with an explicit approval gate.**

---

## 1.6 Hard Constraints at Top and Bottom, Workflow in Middle

Research on LLM instruction-following shows **primacy bias** (instructions at the start are followed most) and **recency bias** (instructions at the end are recalled well). The middle is the weakest position. ([source: agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/), citing ComplexBench NeurIPS 2024, IFScale 2025)

Every OpenAI skill puts its hardest constraints at the top:

```markdown
# docs-sync — top:
"Only update English docs under docs/** and never touch
translated docs under docs/ja, docs/ko, or docs/zh."

# final-release-review — top:
"Default to 🟢 GREEN LIGHT TO SHIP unless at least one
blocking trigger below is satisfied."

# implementation-strategy — top:
"Judge breaking-change risk against the latest release tag,
not against unreleased branch churn."
```

And edge cases / guardrails at the bottom:

```markdown
# implementation-strategy — bottom:
"Do not preserve a confusing abstraction just because it
exists in the current branch diff."

# final-release-review — bottom:
"If you cannot provide a concrete unblock checklist item,
do not use BLOCKED."
```

**Principle 6: Put MUST/NEVER constraints and defaults at the top. Put guardrails and edge cases at the bottom. Put the step-by-step workflow in the middle.**

---

## 1.7 Explicit Output Formats Eliminate Variance

The best skills specify the **exact shape** of their output.

`final-release-review` defines a complete template:

```markdown
### Release readiness review (<tag> -> TARGET <ref>)
### Release call:
**<🟢 GREEN LIGHT TO SHIP | 🔴 BLOCKED>** <one-line rationale>
### Risk assessment (ordered by impact):
1) **<Finding title>**
   - Risk: **<🟢 LOW | 🟡 MODERATE | 🔴 HIGH>**
   - Evidence: <specific diff/test/commit signal>
   - Action: <concrete next step with pass criteria>
```

`implementation-strategy` specifies a one-liner:

```
Compatibility boundary: latest release tag v0.x.y;
branch-local interface rewrite, no shim needed.
```

`pr-draft-summary` provides a full PR block template with exact field names.

Without these templates, the agent improvises a different format every time. With them, output is consistent, parseable, and comparable across runs.

**Principle 7: Define the exact output format. The agent will follow a template faithfully; it will improvise inconsistently.**

---

## 1.8 Decision Tables Over Paragraphs

When a skill involves classification (is this a breaking change? should I block the release?), top skills use explicit **decision tables**, not prose descriptions.

`implementation-strategy` ([source](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md)):

```markdown
## Compatibility boundary rules
- Released public API: preserve compatibility or migration path.
- Interface changes on current branch only: rewrite directly.
- Interface changes on `main` after latest release tag: rewrite directly.
- Internal helpers, private types: update directly.
- Unreleased persisted schema: may be renumbered.
```

`final-release-review` ([source](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md)):

```markdown
Blocking triggers (at least one required):
 - Confirmed regression or bug
 - Breaking API change with missing versioning
 - Data-loss or security-impacting change
 - Release-critical build path broken

Non-blocking by itself:
 - Large diff size
 - "Could regress" risk without evidence
 - Not running tests locally
```

Both are **lookup tables**: the agent identifies which row matches, then follows the prescribed action. No interpretation needed.

**Principle 8: Express classifications as decision tables with category → action rows. Include what does NOT qualify (non-blocking, non-breaking) alongside what does.**

---

## 1.9 Context Budget Awareness

The SKILL.md body loads into the agent's context window alongside everything else — conversation history, tool results, other skills. Every token competes for attention.

The spec recommends: body under 500 lines, under ~5,000 tokens. ([source](https://agentskills.io/specification))

Anthropic's authoring guide: "Once Claude loads [SKILL.md], every token competes with conversation history and your actual request." ([source](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices))

The solution: **keep SKILL.md as a table of contents that points to detail in reference files**.

OpenAI's `runtime-behavior-probe` has 4 reference files:
```
references/validation-matrix.md
references/error-cases.md
references/openai-runtime-patterns.md
references/reporting-format.md
```

OpenAI's `imagegen` has 5:
```
references/cli.md
references/image-api.md
references/prompting.md
references/sample-prompts.md
references/codex-network.md
```

The SKILL.md body tells the agent *when* to read each file. The reference files hold the depth. The agent only loads what it needs, when it needs it.

**Principle 9: Keep SKILL.md lean (<500 lines). Move detailed reference material, examples, and templates to files in `references/`. Load them just-in-time, not all-at-once.**

---

## 1.10 Cross-Skill Script Reuse

Skills can reference scripts from other skills. `implementation-strategy` calls a script from `final-release-review`:

```bash
BASE_TAG="$(.agents/skills/final-release-review/scripts/
  find_latest_release_tag.sh origin 'v*')"
```

This avoids duplicating the tag-lookup logic. When the release tag format changes, only one script updates.

**Principle 10: Factor shared logic into scripts. Reference them by path from any skill that needs them. Don't duplicate.**

---

## Summary of the 10 Principles

| # | Principle | Learned From |
|---|-----------|-------------|
| 1 | Write procedures, not documentation | All OpenAI skills |
| 2 | One job per skill | OpenAI Agents SDK catalog |
| 3 | Description is routing logic (if/then) | OpenAI `pr-draft-summary` |
| 4 | Scripts for determinism, prose for judgment | OpenAI script/instruction split |
| 5 | Report first, act after approval | `docs-sync`, `test-coverage-improver`, `gh-fix-ci` |
| 6 | Hard constraints at top and bottom | Primacy/recency research + all OpenAI skills |
| 7 | Explicit output formats eliminate variance | `final-release-review`, `implementation-strategy` |
| 8 | Decision tables over paragraphs | `implementation-strategy`, `final-release-review` |
| 9 | Keep SKILL.md lean, use reference files | `runtime-behavior-probe`, `imagegen` |
| 10 | Cross-skill script reuse | `implementation-strategy` calling `final-release-review` |
