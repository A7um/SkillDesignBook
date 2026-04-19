# Part II, Chapter 4: Skill Patterns — Recurring Structures Across 50+ Production Skills

A pattern must appear in **at least 5 independently-authored skills**, unless it is a pioneering pattern from a top-tier skill that others are copying. Every pattern is structured as **What** / **Why** / **How**, and every claim cites the skill by name with a link.

### Skills Corpus

| Source | Count | Link |
|--------|-------|------|
| OpenAI Agents SDK | 9 | [github](https://github.com/openai/openai-agents-python/tree/main/.agents/skills) |
| OpenAI curated catalog | 5 | [github](https://github.com/openai/skills/tree/main/skills/.curated) |
| Addy Osmani | 19 | [github](https://github.com/addyosmani/agent-skills) |
| ClawHub / OpenClaw | 10 | [clawhub.ai](https://clawhub.ai/skills?sort=downloads), [github](https://github.com/openclaw/skills) |
| Anthropic official | 6 | [VoltAgent list](https://github.com/VoltAgent/awesome-agent-skills) |

---

## Pattern 1: When to Use / When NOT to Use (30+/50)

**What**: The description field includes both positive triggers ("Use when...") and negative boundaries ("Don't use when..." or "NOT for...").

**Why**: Without negative triggers, skills collide. The agent cannot distinguish "review code" from "fix code" from "test code." Negative triggers draw the decision boundary between this skill and its neighbors. OpenAI found that making skills available can initially *reduce* correct triggering — negative examples fix this ([source](https://developers.openai.com/blog/skills-shell-tips)).

**How**: Combine three components: (1) what it does, (2) when to trigger, (3) when NOT to trigger or redirect.

**Skills demonstrating this:**

- [implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md): "Use when a task changes exported APIs, runtime behavior, serialized state, tests, or docs"
- [pr-draft-summary](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md): "skip only for trivial or conversation-only tasks, repo-meta/doc-only tasks without behavior impact"
- [docs-sync](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md): "Only update English docs... never touch translated docs"
- [github](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/github/SKILL.md): ✅ "USE this skill when: Checking PR status..." / ❌ "DON'T use: Local git operations → use git directly"
- [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): "Use before merging any change"
- [review-code](https://clawhub.ai/skills/review-code): "code review, PR review, merge-readiness check, or bug-risk audit before shipping"
- [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md): "Use when evaluating a skill before publishing, reviewing someone else's skill, scoring skill quality"
- All 19 Osmani skills, all 9 OpenAI SDK skills

---

## Pattern 2: Numbered Step-by-Step Workflow (25+/50)

**What**: The body is a numbered, imperative sequence — each step starts with a verb, not a description.

**Why**: LLMs execute numbered sequences more reliably than prose. They track position in the sequence and know what comes next. Research shows imperative instructions are followed more consistently than declarative descriptions ([source](https://agent-layer.dev/skill-design/)).

**How**: Number every step. Start each with a verb (Run, Identify, Confirm, Check, Report, Ask). Include exact commands inline. Add if/then for branches.

**Skills demonstrating this:**

- [docs-sync](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/github/SKILL.md): 7-step workflow (Confirm scope → Build inventory → Doc-first pass → Code-first pass → Detect gaps → Report → Apply if approved)
- [gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md): 8-step workflow (Verify auth → Resolve PR → Inspect checks → Scope → Summarize → Plan → Implement → Recheck)
- [gh-issues](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/gh-issues/SKILL.md): 6 numbered phases (Parse → Fetch → Present → Pre-flight → Spawn → Monitor)
- [test-coverage-improver](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md): 6-step Quick Start
- [solo-review](https://clawhub.ai/skills/solo-review): 12 numbered "Review Dimensions" each with sub-steps
- [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md): 5-step review process
- All 19 Osmani skills, all 9 OpenAI SDK skills

---

## Pattern 3: Structured Output Template (20+/50)

**What**: The skill specifies the exact shape of its output — field names, structure, and often example values.

**Why**: Without a template, the agent produces a different format every run. With one, output is consistent, parseable, and comparable across runs. The template also constrains the agent's reasoning — it must fill every field, which prevents skipping important aspects.

**How**: Define the exact output structure with placeholder field names. Use emoji for visual scanning. Require specific fields like "Evidence" and "Action" to force concreteness.

**Skills demonstrating this:**

- [final-release-review](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md): Full report template — `### Release call: **<🟢 GREEN LIGHT | 🔴 BLOCKED>** <rationale>` → Risk assessment with `Risk:`, `Evidence:`, `Files:`, `Action:` per finding → Unblock checklist with exit criteria
- [pr-draft-summary](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md): Paste-ready PR block — `## Branch name suggestion` / `## Title` / `## Description`
- [docs-sync](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md): Categorized report — Doc-first findings / Code-first gaps / Incorrect-outdated / Structural suggestions / Proposed edits
- [implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md): One-liner — `Compatibility boundary: latest release tag v0.x.y; branch-local rewrite, no shim needed.`
- [solo-review](https://clawhub.ai/skills/solo-review): 12-section report with per-dimension `Status: {PASS / WARN / FAIL}` → `Verdict: {SHIP / FIX FIRST / BLOCK}`
- [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md): `SKILL REVIEW SCORECARD` with Category/Score/Max table → TOTAL/53 → RATING → VERDICT
- [review-code](https://clawhub.ai/skills/review-code): Findings with severity + confidence + evidence + fix path
- [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): Review checklist template with category checkboxes → Verdict

---

## Pattern 4: Report-Then-Ask-Approval Gate (15+/50)

**What**: The skill separates analysis from action with an explicit pause: "Report findings, then ask user for approval before modifying anything."

**Why**: Skills that modify files or state are dangerous without a checkpoint. The gate makes the skill testable in two phases (analysis quality, then action quality). It also builds trust — users review before irreversible changes.

**How**: Insert a "Report" step and an "Ask" step between analysis and action. Use words like "pause", "ask for approval", "wait for confirmation."

**Skills demonstrating this:**

- [docs-sync](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md): "Provide a report and ask for approval before editing docs."
- [test-coverage-improver](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md): "Ask the user for approval to implement the proposed tests; pause until they agree."
- [gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md): "Create a plan... Implement after approval."
- [review-code](https://clawhub.ai/skills/review-code): "Before creating or changing local files, present the planned write and ask for user confirmation."
- [gh-issues](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/gh-issues/SKILL.md): Phase 3 — "Ask the user to confirm which issues to process"
- [implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md): "When to stop and confirm" section listing escalation triggers
- [solo-review](https://clawhub.ai/skills/solo-review): Reports verdict then signals pipeline (never auto-fixes code — "Review only modifies plan.md, never source code")

---

## Pattern 5: Quick Start / Fast Path (12+/50)

**What**: A compressed 4-6 step version of the full workflow, placed before the detailed instructions.

**Why**: Strong models may only need the fast path for straightforward cases. The Quick Start is the "table of contents" for the full workflow — it shows the overall shape before diving into details. This also helps with context: if the model's context is compacted, the Quick Start survives better than detailed steps.

**How**: Place a `## Quick start` section after Overview with 4-6 numbered steps covering the happy path. Follow it with the detailed `## Workflow` section.

**Skills demonstrating this:**

- [implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md): 5-step Quick Start (Identify surface → Determine release tag → Judge risk → Prefer simplest → Add compat only if needed)
- [test-coverage-improver](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md): 6-step Quick Start
- [final-release-review](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md): Quick Start with tag + diff commands
- [gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md): Quick Start with single script command
- All 5 OpenAI curated skills ([imagegen](https://github.com/openai/skills/blob/main/skills/.curated/imagegen/SKILL.md), [sora](https://github.com/openai/skills/blob/main/skills/.curated/sora/SKILL.md), [speech](https://github.com/openai/skills/blob/main/skills/.curated/speech/SKILL.md), [doc](https://github.com/openai/skills/blob/main/skills/.curated/doc/SKILL.md), gh-fix-ci)

---

## Pattern 6: Script-Backed Determinism (12+/50)

**What**: Critical operations run via scripts (`scripts/run.sh`, `scripts/inspect.py`) rather than prose instructions.

**Why**: The agent cannot improvise the verification sequence or API call format when it runs a script. Scripts handle failure modes (field drift, fallbacks, error formatting) that prose instructions handle unreliably. A single script eliminates an entire class of agent improvisation errors.

**How**: Place executable scripts in `scripts/`. Reference them from SKILL.md with exact invocation syntax. Provide a manual fallback in case the script is unavailable.

**Skills demonstrating this:**

- [code-change-verification](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification): `scripts/run.sh` (fail-fast format→lint→mypy→tests)
- [gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md): `scripts/inspect_pr_checks.py` (GitHub API with field-drift fallbacks)
- [final-release-review](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md): `scripts/find_latest_release_tag.sh` (tag lookup from remote)
- [imagegen](https://github.com/openai/skills/blob/main/skills/.curated/imagegen/SKILL.md): `scripts/image_gen.py` (API wrapper)
- [sora](https://github.com/openai/skills/blob/main/skills/.curated/sora/SKILL.md): `scripts/sora.py` (video generation CLI)
- [speech](https://github.com/openai/skills/blob/main/skills/.curated/speech/SKILL.md): `scripts/text_to_speech.py`
- [doc](https://github.com/openai/skills/blob/main/skills/.curated/doc/SKILL.md): `scripts/render_docx.py`
- [pr-commit-workflow](https://github.com/openclaw/skills/tree/main/skills/joshp123/pr-commit-workflow/SKILL.md): `scripts/build_pr_body.sh`
- [review-pr](https://playbooks.com/skills/openclaw/openclaw/review-pr): `scripts/pr-review`, `scripts/pr review-checkout-main`

---

## Pattern 7: Decision Table (Category → Action) (8+/50)

**What**: When the workflow involves classification, the skill provides a lookup table where each row maps a category to a prescribed action. Critically, it includes what does NOT qualify alongside what does.

**Why**: Prose classification is unreliable — agents interpret ambiguous text differently on each run. A lookup table makes classification deterministic. The "non-qualifying" rows are as important as the qualifying ones — without them, agents default to the most conservative interpretation.

**How**: Create a table or bullet list where each row is `[Category]: [Action]`. Add a separate list for non-qualifying categories. Use concrete examples, not abstract descriptions.

**Skills demonstrating this:**

- [implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md): 5-row compatibility table — "Released public API → preserve" / "Branch-local changes → rewrite directly" / "Internal helpers → update directly"
- [final-release-review](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md): Blocking triggers (4 conditions) + Non-blocking list (3 conditions that look scary but aren't blocking)
- [imagegen](https://github.com/openai/skills/blob/main/skills/.curated/imagegen/SKILL.md): Image type taxonomy — photorealistic-natural / product-mockup / etc. → each maps to specific composition constraints
- [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): 5-axis review (correctness / readability / architecture / security / performance)
- [solo-review](https://clawhub.ai/skills/solo-review): Verdict logic — SHIP when [all conditions] / FIX FIRST when [conditions] / BLOCK when [conditions]
- [review-code](https://clawhub.ai/skills/review-code): Severity + confidence calibration table
- [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md): Score thresholds — 45+ Excellent / 35-44 Good / 25-34 Fair / <25 Poor → PUBLISH / REVISE / REWORK
- [shipping-and-launch](https://github.com/addyosmani/agent-skills/blob/main/skills/shipping-and-launch/SKILL.md): Staged rollout strategy table

---

## Pattern 8: Exact Input Collection Commands (8+/50)

**What**: The skill specifies exact shell commands to gather inputs, often with "(do not ask the user)."

**Why**: Without exact commands, agents either ask the user for information they could gather themselves, or they improvise unreliable alternatives. The "(do not ask)" directive is critical — without it, agents default to prompting.

**How**: List each input with its exact command. Include fallbacks for when the primary command fails. Add "(do not ask the user)" when inputs should be auto-gathered.

**Skills demonstrating this:**

- [pr-draft-summary](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md): 8 exact commands — `git rev-parse --abbrev-ref HEAD`, `git status -sb`, `git diff --name-only`, etc. Header: "Inputs to Collect Automatically (do not ask the user)"
- [final-release-review](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md): `git diff --stat`, `git log --oneline --reverse`, `git diff --name-status`
- [implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md): Tag lookup with fallback — `$(.agents/skills/final-release-review/scripts/find_latest_release_tag.sh origin 'v*' 2>/dev/null || git tag -l 'v*' --sort=-v:refname | head -n1)`
- [docs-sync](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md): Targeted search — `rg "Settings"`, `rg "Config"`, `rg "os.environ"`, `rg "OPENAI_"`
- [gh-issues](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/gh-issues/SKILL.md): `git remote get-url origin` with HTTPS/SSH parsing, `curl -s -H "Authorization: Bearer $GH_TOKEN"` for API calls
- [solo-review](https://clawhub.ai/skills/solo-review): Per-stack commands — `npm test -- --coverage`, `uv run pytest`, `swift test`
- [test-coverage-improver](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md): `make coverage`, `coverage report -m`
- [gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md): `gh auth status`, `gh pr view --json`, `gh run view --log`

---

## Pattern 9: Reference File Architecture (10+/50)

**What**: Large skills split into a lean SKILL.md (navigation + workflow) and reference files (depth). SKILL.md tells the agent *at which step* to read each reference.

**Why**: SKILL.md loads entirely into context on activation. If it's 1000 lines, that's ~5000 tokens competing with everything else. Reference files load only when explicitly read — zero cost until needed. This lets skills carry deep expertise without paying the context cost upfront.

**How**: Keep SKILL.md under 500 lines. Move detailed checklists, API docs, sample prompts, and templates to `references/`. In SKILL.md, reference files at the specific workflow step: "Walk through the categories in `references/checklist.md` when analyzing risk."

**Skills demonstrating this:**

- [review-code](https://clawhub.ai/skills/review-code): **8 reference files** — `setup.md`, `memory-template.md`, `review-workflow.md`, `severity-and-confidence.md`, `language-risk-checklists.md`, `test-impact-playbook.md`, `comment-templates.md`, `patch-strategy.md`
- [imagegen](https://github.com/openai/skills/blob/main/skills/.curated/imagegen/SKILL.md): 5 refs — `cli.md`, `image-api.md`, `prompting.md`, `sample-prompts.md`, `codex-network.md`
- [sora](https://github.com/openai/skills/blob/main/skills/.curated/sora/SKILL.md): 5 refs — `cli.md`, `video-api.md`, `prompting.md`, `sample-prompts.md`, `troubleshooting.md`
- [speech](https://github.com/openai/skills/blob/main/skills/.curated/speech/SKILL.md): 5 refs — `cli.md`, `audio-api.md`, `voice-directions.md`, `prompting.md`, `sample-prompts.md`
- [runtime-behavior-probe](https://github.com/openai/openai-agents-python/blob/main/.agents/skills/runtime-behavior-probe/SKILL.md): 4 refs — `validation-matrix.md`, `error-cases.md`, `openai-runtime-patterns.md`, `reporting-format.md`
- [final-release-review](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md): 1 ref — `references/review-checklist.md`
- [docs-sync](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md): 1 ref — `references/doc-coverage-checklist.md`

---

## Pattern 10: Severity / Confidence Labeling (7+/50)

**What**: Each finding gets a severity label, and often a confidence score. The labels have explicit definitions.

**Why**: Without labels, agents treat all findings as equally important. Users waste time on optional suggestions while missing critical issues. The labeling system creates a triage protocol inside the skill.

**How**: Define 3-5 severity levels with one-line definitions. Optionally add confidence (high/medium/low). Require that every finding carries a label.

**Skills demonstrating this:**

- [final-release-review](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md): **🟢 LOW** / **🟡 MODERATE** / **🔴 HIGH** with definitions — LOW: "low blast radius, clearly covered", MODERATE: "plausible regression, needs validation", HIGH: "confirmed release-blocking"
- [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): (no prefix)=required, `Critical:`=blocks, `Nit:`=optional, `Optional:`/`Consider:`=suggestion, `FYI`=informational
- [solo-review](https://clawhub.ai/skills/solo-review): Per-dimension PASS/WARN/FAIL → overall SHIP/FIX FIRST/BLOCK
- [review-code](https://clawhub.ai/skills/review-code): Severity + confidence calibration with rules in `references/severity-and-confidence.md`
- [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md): Defects categorized as Critical (blocks publishing) / Major (should fix) / Minor (nice to fix)
- [review-pr](https://playbooks.com/skills/openclaw/openclaw/review-pr): Structured JSON findings with severity levels
- Devin 2.1 confidence ratings: 🟢🟡🔴 ([source](https://cognition.ai/blog/devin-2-1))

---

## Pattern 11: Anti-Sycophancy / Anti-Rationalization Clauses (5+/50, pioneering)

**What**: Explicit instructions counteracting known LLM failure modes — agreeing too easily, softening criticism, claiming success without evidence.

**Why**: LLMs are trained on helpful, agreeable text and default to rationalizing problems away. Without counter-instructions, review skills rubber-stamp, gate skills green-light everything, and verification skills declare success prematurely. This pattern names the failure mode and pre-programs the correct response.

**How**: Add a "Common Traps" or "Rationalizations" section. Each row: a thought the agent might have → the correct reality. Place near the bottom (recency bias helps it stick).

**Skills demonstrating this:**

- [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): "Don't rubber-stamp. 'LGTM' without evidence helps no one." / "Don't soften real issues. Sycophancy is a failure mode." / "Push back on approaches with clear problems."
- [solo-review](https://clawhub.ai/skills/solo-review): Rationalizations Catalog — `"Tests were passing earlier" → Run them NOW` / `"Good enough to ship" → Quantify. Show the numbers.` / `"I already checked this" → Fresh evidence only.`
- [review-code](https://clawhub.ai/skills/review-code): "Reporting opinions as facts → credibility drops" / "Calling something 'probably fine' without tests → silent regressions"
- [implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md): "Do not preserve a confusing abstraction just because it exists" / "If review feedback claims breaking, verify against release tag before accepting"
- [final-release-review](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md): "never produce a BLOCKED call without concrete evidence" / "If evidence is incomplete, issue GREEN LIGHT with follow-ups instead of BLOCKED"

---

## Pattern 12: Post-Action Verification (10+/50)

**What**: After the skill acts, it re-runs a check to verify the action succeeded.

**Why**: Actions fail silently. Without verification, the agent declares success on a broken state. The verification step closes the loop.

**How**: After the action step, add: "Run [verification command]. Compare output to expected result. If fails, return to step N. After 3 failed attempts, report and stop."

**Skills demonstrating this:**

- [code-change-verification](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification): The entire skill IS the verification step
- [test-coverage-improver](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md): "After implementation: Rerun coverage, report the updated summary."
- [docs-sync](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md): "Build docs with `make build-docs` after edits to verify the docs site still builds."
- [gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md): "After changes, suggest re-running the relevant tests and `gh pr checks` to confirm."
- [solo-review](https://clawhub.ai/skills/solo-review): "Verification Gate: No verdict without fresh evidence. Run actual test/build/lint commands. Read full output. Confirm output matches your claim. Only then write the verdict."
- [gh-issues](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/gh-issues/SKILL.md): Sub-agent must "TEST — Run the relevant tests. If tests fail, attempt ONE retry."

---

## Pattern 13: Scoring Rubric with Numeric Grades (5+/50, pioneering)

**What**: The skill defines a numeric scoring system so the agent grades findings consistently across runs.

**Why**: "Is this good?" produces different answers every run. "Score this 0-8 on these criteria" produces consistent results. Rubrics make evaluation deterministic and comparable over time.

**How**: Define scoring criteria as `[N points] condition`. Provide GOOD/BAD examples for each. Sum to a total with threshold verdicts.

**Skills demonstrating this:**

- [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md): **53-point rubric** across 8 categories — Description/8 (e.g., "[2] Starts with active verb, GOOD: 'Write Makefiles...' BAD: 'This skill covers...'"), Metadata/4, Example density/3, Organization/6, Actionability/10, Tips/8. Thresholds: 45+ Excellent → PUBLISH, 35-44 Good → REVISE, <25 Poor → REWORK
- [solo-review](https://clawhub.ai/skills/solo-review): Per-dimension status → three-level verdict
- [review-code](https://clawhub.ai/skills/review-code): Calibrated severity + confidence scoring in `references/severity-and-confidence.md`
- [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): Implicit scoring — 5-axis pass/fail with severity labels
- Devin 2.1 confidence scores (1-10 internal) → 🟢🟡🔴 external ([source](https://cognition.ai/blog/devin-2-1))

---

## Pattern 14: Checklist as Structural Backbone (8+/50)

**What**: The workflow is organized as a checklist of binary checks. Each item is pass/fail.

**Why**: Checklists convert judgment into verification. The agent doesn't decide "is this good?" — it checks each condition. This is more reliable than open-ended evaluation and produces reproducible results.

**How**: Use `[ ]` checkbox items. Each item is a specific, verifiable condition. Group into categories.

**Skills demonstrating this:**

- [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md): `STRUCTURAL CHECKLIST` — `[ ] Valid YAML frontmatter` / `[ ] name field present` / `[ ] "When to Use" section present` / etc. (11 items)
- [solo-review](https://clawhub.ai/skills/solo-review): 12 dimensions, each a checklist of verifiable conditions
- [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): `## The Review Checklist` template — `[ ] I understand what this change does` / `[ ] Edge cases handled` / `[ ] No injection vulnerabilities` / etc.
- [final-release-review](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md): `references/review-checklist.md` — detailed signals organized by category
- [gh-issues](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/gh-issues/SKILL.md): Pre-flight checks (6 sequential verifications)
- [openclaw-pr-maintainer](https://github.com/openclaw/openclaw/blob/main/.agents/skills/openclaw-pr-maintainer/SKILL.md): PR triage checklist
- [shipping-and-launch](https://github.com/addyosmani/agent-skills/blob/main/skills/shipping-and-launch/SKILL.md): Pre-launch checklist
- [security-and-hardening](https://github.com/addyosmani/agent-skills/blob/main/skills/security-and-hardening/SKILL.md): Security review checklist

---

## Pattern 15: Common Traps / Rationalizations Table (5+/50, pioneering)

**What**: A two-column table pairing a tempting shortcut or rationalization with the correct reality. Placed near the bottom of the skill (recency bias).

**Why**: This is distinct from Pattern 11 (anti-sycophancy). Pattern 11 is about the agent being too agreeable. This pattern is about the agent taking shortcuts — skipping tests, accepting stale data, conflating "works" with "good." The table format is copy-paste-able and scannable.

**How**: Create a table: `| Rationalization | Reality |`. Each row names a specific tempting thought and its correction.

**Skills demonstrating this:**

- [solo-review](https://clawhub.ai/skills/solo-review): 6-row table including `"Tests were passing earlier" → "Run them NOW. Code changed since then."` and `"It's just a warning" → "Warnings become bugs. Report them."`
- [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): 5-row table including `"It works, that's good enough" → "Working unreadable code creates debt"` and `"AI-generated code is probably fine" → "AI code needs more scrutiny, not less"`
- [review-code](https://clawhub.ai/skills/review-code): "Common Traps" section with 6 anti-patterns
- [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md): "Common Defects" catalog — Critical / Major / Minor with DETECT/FIX pairs
- [implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md): "Default implementation stance" countering the urge to add unnecessary shims

---

## Pattern 16: Per-Stack Command Variants (6+/50)

**What**: When a skill applies to multiple technology stacks, it provides the exact command for each stack.

**Why**: "Run your tests" doesn't help an agent — it doesn't know whether to use `npm test`, `pytest`, `swift test`, or `cargo test`. Per-stack commands with exact syntax eliminate guesswork and make the skill work across diverse codebases.

**How**: Use if/then or tabular format. Each stack gets its own command block. Include a Makefile fallback where applicable.

**Skills demonstrating this:**

- [solo-review](https://clawhub.ai/skills/solo-review): 4+ stacks for each dimension — Tests: `npm test --coverage` / `uv run pytest` / `swift test`; Lint: `pnpm lint` / `uv run ruff check .` / `swiftlint` / `./gradlew detekt`; Build: `npm run build` / `uv run python -m py_compile`; Logs: `vercel logs` / `wrangler tail` / `fly logs`
- [github](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/github/SKILL.md): Install via `brew` or `apt`
- [gh-issues](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/gh-issues/SKILL.md): HTTPS vs SSH URL parsing; `jq` vs `node -e` for JSON parsing
- [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md): Cross-platform accuracy checklist — macOS `sed -i ''` vs Linux `sed -i`, brew vs apt vs pacman
- [doc](https://github.com/openai/skills/blob/main/skills/.curated/doc/SKILL.md): `soffice` for DOCX→PDF, `pdftoppm` for PDF→PNG, Python fallback
- [code-change-verification](https://playbooks.com/skills/openai/openai-agents-js/code-change-verification): `scripts/run.sh` (Unix) + `scripts/run.ps1` (Windows)

---

## Pattern Summary Table

| # | Pattern | Freq | What | Why | Exemplar |
|---|---------|------|------|-----|----------|
| 1 | When to Use / NOT | 30+ | Positive + negative triggers in description | Prevents skill collision | [github](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/github/SKILL.md) |
| 2 | Numbered Workflow | 25+ | Imperative numbered steps | LLMs execute sequences reliably | [gh-issues](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/gh-issues/SKILL.md) |
| 3 | Output Template | 20+ | Exact output format with field names | Eliminates per-run variance | [final-release-review](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md) |
| 4 | Report-Then-Approve | 15+ | Analysis → report → ask → act | Safety gate + testable phases | [docs-sync](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md) |
| 5 | Quick Start | 12+ | Compressed fast path before details | Strong models skip detail | [implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) |
| 6 | Script-Backed | 12+ | Scripts for deterministic operations | Prevents improvisation errors | [code-change-verification](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification) |
| 7 | Decision Table | 8+ | Category → action lookup | Deterministic classification | [implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) |
| 8 | Exact Input Commands | 8+ | Shell commands to gather inputs | Prevents asking user + improvisation | [pr-draft-summary](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md) |
| 9 | Reference Files | 10+ | Depth in `references/`, nav in SKILL.md | Context budget efficiency | [review-code](https://clawhub.ai/skills/review-code) |
| 10 | Severity Labels | 7+ | Graded finding severity | Triage protocol | [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) |
| 11 | Anti-Sycophancy | 5+★ | Counter agreeable defaults | LLMs rationalize problems | [solo-review](https://clawhub.ai/skills/solo-review) |
| 12 | Post-Action Verify | 10+ | Re-check after acting | Catch silent failures | [test-coverage-improver](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md) |
| 13 | Scoring Rubric | 5+★ | Numeric grades per criteria | Deterministic evaluation | [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md) |
| 14 | Checklist Backbone | 8+ | Binary pass/fail checks | Converts judgment to verification | [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md) |
| 15 | Traps Table | 5+★ | Rationalization → reality rows | Inoculates against shortcuts | [solo-review](https://clawhub.ai/skills/solo-review) |
| 16 | Per-Stack Commands | 6+ | Exact commands per technology | Eliminates guesswork | [solo-review](https://clawhub.ai/skills/solo-review) |

★ = pioneering pattern

---

*The following patterns were discovered by analyzing an additional 70+ skills from ClawHub community (code, git, docker, memory, python, react, nextjs, linux, deploy, ci-cd, plan, self-improving-agent, etc.), Anthropic official (docx, algorithmic-art, frontend-design), Vercel (react-best-practices, web-design-guidelines), Stripe (stripe-best-practices), Sentry (sentry-fix-issues), Trail of Bits (agentic-actions-auditor), and the full addyosmani/agent-skills pack (19 skills).*

---

## Pattern 17: Common Traps / Gotchas as Primary Content (20+/50)

**What**: A dedicated section (often the longest) listing domain-specific pitfalls, each as a one-liner pairing the trap with its fix, using an em-dash separator.

**Why**: For reference/advisory skills (git, docker, linux, typescript), traps ARE the value. Developers don't need a workflow — they need to know what will bite them. Structuring content as traps is more useful than structuring it as tutorials, because agents encounter problems mid-task and need the specific fix.

**How**: Create sections named "Common Traps", "Gotchas", or "\<Domain\> Traps". Each bullet: `Trap description — Fix or correct approach`. Group traps by subcategory.

**Skills demonstrating this:**

- [docker](https://clawhub.ai/skills/docker): **6 trap categories** — Image Traps, Runtime Traps, Networking Traps, Compose Traps, Volume Traps, Resource Leaks. E.g.: "Running as root in container — Add `USER nonroot` in Dockerfile"
- [git](https://clawhub.ai/skills/git): "Common Traps" section + "Recovery Commands" section. E.g.: "Force-pushing shared branches — Use `--force-with-lease` instead"
- [linux](https://clawhub.ai/skills/linux): ENTIRE skill is traps — Permission Traps, Process Gotchas, Filesystem Traps, SSH Traps, Commands That Lie
- [typescript](https://clawhub.ai/skills/typescript): Stop Using `any`, Narrowing Failures, Literal Type Traps, Inference Limits
- [python](https://clawhub.ai/skills/python): Anti-patterns to Avoid section with ✅/❌ code pairs
- [react](https://clawhub.ai/skills/react): Common Traps (Rendering / Hooks / Data Fetching subsections)
- [nextjs](https://clawhub.ai/skills/nextjs): Common Traps table (trap → fix)
- [devops](https://clawhub.ai/skills/devops): Common Mistakes section
- [ci-cd](https://clawhub.ai/skills/ci-cd): Common Pipeline Pitfalls table (mistake → impact → fix)
- [deploy](https://clawhub.ai/skills/deploy): Common Mistakes section

---

## Pattern 18: ✅/❌ Code Contrast Pairs (10+/50)

**What**: Showing the wrong way and right way as adjacent code blocks, marked with ✅ and ❌.

**Why**: Models learn by contrast. Showing ONLY the correct way leaves the agent uncertain about what to avoid. Showing both — with visual markers — creates a clear boundary. Research on instruction-following confirms that negative examples reduce misfires.

**How**: Place bad example (❌) first, then good example (✅) immediately after. Use the same scenario for both so the contrast is clear.

**Skills demonstrating this:**

- [python](https://clawhub.ai/skills/python): ✅/❌ for PEP 8 patterns, import style, type hints
- [react](https://clawhub.ai/skills/react): ✅/❌ for component patterns, hooks usage, state management
- [typescript](https://clawhub.ai/skills/typescript): ✅/❌ for type narrowing, inference, strict mode
- [github](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/github/SKILL.md): ✅ "USE this skill when..." / ❌ "DON'T use this skill when..."
- [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md): GOOD/BAD example pairs for descriptions — `GOOD: "Write Makefiles for any project type." BAD: "This skill covers Makefiles."`
- [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): Bad/good comparison for change descriptions
- All 19 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills): Bad → Good contrast in verification sections

---

## Pattern 19: Rationalizations-to-Reject Table (12+/50)

**What**: A two-column table of `Excuse | Reality` that names specific rationalizations the agent (or human) might use to skip important steps.

**Why**: This is distinct from Pattern 15 (Traps Table) which focuses on *domain* traps. This pattern targets *process* traps — the temptation to skip testing, rubber-stamp reviews, or declare done prematurely. Found in 17/19 Osmani skills, making it one of the most consistent patterns in the most-starred skill pack.

**How**: Table with `| Rationalization | Reality |`. Place near the end (recency bias helps it stick). Target the specific temptations of the skill's domain.

**Skills demonstrating this:**

- All 17 of 19 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — each has a "Common Rationalizations" section. Examples from [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md):
  - `"It works, that's good enough" → "Working unreadable code creates compound debt"`
  - `"AI-generated code is probably fine" → "AI code needs MORE scrutiny, not less"`
  - `"We'll clean it up later" → "Later never comes. Require cleanup now."`
- [solo-review](https://clawhub.ai/skills/solo-review): 6-row table
- [review-code](https://clawhub.ai/skills/review-code): "Common Traps" framed as rationalizations

---

## Pattern 20: Red Flags Section (8+/50)

**What**: A list of observable warning signs (gerund-phrased behaviors) that indicate process failure, separate from the rationalizations table.

**Why**: While rationalizations are internal thoughts, red flags are observable behaviors that can be detected. An agent can check for red flags in its own behavior or in the codebase it's reviewing. The gerund phrasing ("Skipping...", "Starting...") makes them pattern-matchable.

**How**: List of `- [gerund phrase] [consequence]`. Placed after the main workflow, before or after rationalizations.

**Skills demonstrating this:**

- All 19 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) have a "Red Flags" section. From [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): "PRs merged without any review" / "LGTM without evidence of actual review" / "Large PRs that are too big to review properly (split them)" / "No regression tests with bug fix PRs"
- [solo-review](https://clawhub.ai/skills/solo-review): Implicit red flags in verdict logic (security issue = BLOCK, failing tests = BLOCK)
- [review-code](https://clawhub.ai/skills/review-code): "Missing migration and backward-compatibility checks → runtime failures after deploy"

---

## Pattern 21: Local Memory / State Directory (8+/50)

**What**: The skill declares a local directory (typically `~/skillname/`) for persisting preferences, findings, and session history across runs.

**Why**: Skills that learn from past runs (coding style, review preferences, decision patterns) need persistent storage. Declaring the path explicitly makes storage transparent, auditable, and cleanable. It also enables skills to build up domain knowledge over time.

**How**: Declare the path in an "Architecture" or "Data Storage" section. Define the file structure. Always require user confirmation before creating or modifying files.

**Skills demonstrating this:**

- [code](https://clawhub.ai/skills/code): `~/code/` — memory.md (preferences), findings/ (per-review logs)
- [coding](https://clawhub.ai/skills/coding): Coding style memory that "adapts to your preferences, conventions, and patterns"
- [memory](https://clawhub.ai/skills/memory): `~/memory/` — INDEX.md, categorized storage files. Most comprehensive memory architecture on ClawHub (9.7K downloads)
- [review-code](https://clawhub.ai/skills/review-code): `~/review-code/` — memory.md, findings/, baselines/, sessions/
- [decide](https://clawhub.ai/skills/decide): Decision pattern storage with promotion gates
- [nextjs](https://clawhub.ai/skills/nextjs): `~/nextjs/` for framework-specific preferences
- [plan](https://clawhub.ai/skills/plan): Outcome tracking with strategy learning
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent): Logging format with entry types, ID generation, promotion to project memory (399K downloads, highest on ClawHub)

---

## Pattern 22: Related Skills Cross-References (15+/50)

**What**: A "Related Skills" section listing complementary skills with install commands.

**Why**: Skills work better in ecosystems. A code review skill pairs with a git skill, a testing skill, and a CI/CD skill. Cross-references help users build complete workflows and help agents know which other skills to suggest.

**How**: List skill names with one-line descriptions and install commands. Place at the end of the skill.

**Skills demonstrating this:**

- [review-code](https://clawhub.ai/skills/review-code): "code — implementation workflow" / "git — branch, diff, commit handling" / "typescript — typing and runtime safety" / "ci-cd — release-gate checks" / "devops — production risk"
- [docker](https://clawhub.ai/skills/docker): Related to devops, deploy, linux
- [git](https://clawhub.ai/skills/git): Related to github, deploy, ci-cd
- [code](https://clawhub.ai/skills/code): Related to review-code, git, typescript, ci-cd
- [react](https://clawhub.ai/skills/react): Related to typescript, nextjs, frontend
- [nextjs](https://clawhub.ai/skills/nextjs): Related to react, typescript, deploy
- [github-actions](https://clawhub.ai/skills/github-actions): Related to ci-cd, deploy, git
- All 19 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills): Cross-reference by name (e.g., "For detailed security guidance, see `security-and-hardening`")
- [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md): "When comparing skills in the same category" — comparative review template

---

## Pattern 23: Security & Privacy Declaration (10+/50)

**What**: An explicit section declaring what data the skill sends externally, what it stores locally, and what it does NOT do.

**Why**: Users and security teams need to audit skill behavior. Post-ClawHavoc (January 2026, 341 malicious skills), transparency declarations became standard on ClawHub. ClawHub's security scan checks whether declared behavior matches actual behavior.

**How**: Three-part structure: "Data that leaves your machine" / "Data stored locally" / "This skill does NOT:" followed by explicit denials.

**Skills demonstrating this:**

- [review-code](https://clawhub.ai/skills/review-code): "Data that leaves: Nothing by default" / "Data stored locally: Review preferences in ~/review-code/" / "This skill does NOT: auto-approve code, make network calls, store credentials, modify its own instructions"
- [code](https://clawhub.ai/skills/code): External Endpoints table (Endpoint / Data Sent / Purpose) — "None | None | N/A"
- [github-actions](https://clawhub.ai/skills/github-actions): External Endpoints + Trust section
- [coding](https://clawhub.ai/skills/coding): Security & Privacy section
- [memory](https://clawhub.ai/skills/memory): Security & Privacy section
- [decide](https://clawhub.ai/skills/decide): Security & Privacy section
- [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md): Includes "Trust" assessment as part of review framework
- [agentic-actions-auditor](https://github.com/trailofbits/skills) (Trail of Bits): Security auditing skill — security is the core content
- [stripe-best-practices](https://github.com/stripe/ai) (Stripe): Secret handling constraints

---

## Pattern 24: AI-Mistakes-to-Avoid Section (5+/50, pioneering)

**What**: A section explicitly targeting mistakes that AI agents (not humans) commonly make, addressing the agent as "you."

**Why**: LLMs have known failure modes that differ from human mistakes: they hallucinate API parameters, use deprecated syntax, over-engineer simple tasks, and struggle with specific technical patterns (e.g., React hook dependency arrays). Naming these AI-specific mistakes directly reduces their frequency.

**How**: Table or list of `AI Mistake → Correct Approach`, written addressing the agent: "You will be tempted to..." / "AI assistants commonly..."

**Skills demonstrating this:**

- [react](https://clawhub.ai/skills/react): "AI Mistakes to Avoid" — dedicated table of React patterns that AI agents specifically get wrong
- [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md): "AI-generated code needs more scrutiny, not less"
- [solo-review](https://clawhub.ai/skills/solo-review): "Never write 'tests should pass' — run them and show the output"
- [coding](https://clawhub.ai/skills/coding): "Never infer from silence" — explicitly targets AI inference tendency
- [AGI skill](https://clawhub.ai/skills/agi) (ClawHub): Meta-cognitive self-check — "Would a thoughtful human senior colleague respond this way?"

---

## Pattern 25: Em-Dash Rationale Style (15+/50)

**What**: Each rule or bullet point includes a brief rationale after an em-dash (`—`), on the same line.

**Why**: Without rationale, rules feel arbitrary and agents may deprioritize them. With rationale, the agent understands *why* the rule exists and can apply it correctly to edge cases not explicitly covered. The em-dash format keeps it compact (one line per rule+reason).

**How**: `Rule statement — one-line rationale why`. Keep the rationale to 5-15 words.

**Skills demonstrating this:**

- [docker](https://clawhub.ai/skills/docker): "Always pin image tags — `latest` changes without warning"
- [git](https://clawhub.ai/skills/git): "Never force-push shared branches — rewrites others' history"
- [devops](https://clawhub.ai/skills/devops): Every bullet uses this format
- [linux](https://clawhub.ai/skills/linux): Every pitfall uses this format
- [code](https://clawhub.ai/skills/code): Core Rules use this format
- [memory](https://clawhub.ai/skills/memory): Core Rules use this format
- [coding](https://clawhub.ai/skills/coding): Core Rules use this format
- [deploy](https://clawhub.ai/skills/deploy): Strategy descriptions use this format

---

## Updated Pattern Summary Table

| # | Pattern | Freq | What | Why | Exemplar |
|---|---------|------|------|-----|----------|
| 1 | When to Use / NOT | 30+ | +/- triggers in description | Prevent collision | [github](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/github/SKILL.md) |
| 2 | Numbered Workflow | 25+ | Imperative numbered steps | Reliable execution | [gh-issues](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/gh-issues/SKILL.md) |
| 3 | Output Template | 20+ | Exact output format | Eliminate variance | [final-release-review](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md) |
| 4 | Report-Then-Approve | 15+ | Analysis → report → ask → act | Safety gate | [docs-sync](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md) |
| 5 | Quick Start | 12+ | Compressed fast path | Strong models skip detail | [implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) |
| 6 | Script-Backed | 12+ | Scripts for determinism | Prevent improvisation | [code-change-verification](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification) |
| 7 | Decision Table | 8+ | Category → action lookup | Deterministic classification | [implementation-strategy](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) |
| 8 | Exact Input Commands | 8+ | Shell commands for inputs | Prevent asking/improvising | [pr-draft-summary](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md) |
| 9 | Reference Files | 10+ | Depth in `references/` | Context budget | [review-code](https://clawhub.ai/skills/review-code) |
| 10 | Severity Labels | 7+ | Graded finding severity | Triage protocol | [code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) |
| 11 | Anti-Sycophancy | 5+★ | Counter agreeable defaults | LLMs rationalize | [solo-review](https://clawhub.ai/skills/solo-review) |
| 12 | Post-Action Verify | 10+ | Re-check after acting | Catch silent failures | [test-coverage-improver](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md) |
| 13 | Scoring Rubric | 5+★ | Numeric grades | Deterministic eval | [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md) |
| 14 | Checklist Backbone | 8+ | Binary pass/fail checks | Judgment → verification | [skill-reviewer](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md) |
| 15 | Traps Table | 5+★ | Rationalization → reality | Inoculate shortcuts | [solo-review](https://clawhub.ai/skills/solo-review) |
| 16 | Per-Stack Commands | 6+ | Exact per-technology cmds | Eliminate guesswork | [solo-review](https://clawhub.ai/skills/solo-review) |
| **17** | **Domain Traps as Content** | **20+** | **Pitfall + fix as primary content** | **Traps ARE the value** | **[docker](https://clawhub.ai/skills/docker)** |
| **18** | **✅/❌ Code Contrast** | **10+** | **Bad/good code side-by-side** | **Models learn by contrast** | **[python](https://clawhub.ai/skills/python)** |
| **19** | **Rationalizations Table** | **12+** | **Excuse → Reality for process traps** | **17/19 Osmani skills** | **[code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md)** |
| **20** | **Red Flags Section** | **8+** | **Observable warning signs** | **Pattern-matchable** | **[addyosmani all 19](https://github.com/addyosmani/agent-skills)** |
| **21** | **Local Memory Directory** | **8+** | **~/skillname/ for persistence** | **Cross-session learning** | **[memory](https://clawhub.ai/skills/memory)** |
| **22** | **Related Skills Cross-Refs** | **15+** | **Complementary skill links** | **Ecosystem building** | **[review-code](https://clawhub.ai/skills/review-code)** |
| **23** | **Security & Privacy Decl.** | **10+** | **Data flow transparency** | **Post-ClawHavoc trust** | **[review-code](https://clawhub.ai/skills/review-code)** |
| **24** | **AI-Mistakes-to-Avoid** | **5+★** | **Agent-specific failure modes** | **LLMs ≠ humans** | **[react](https://clawhub.ai/skills/react)** |
| **25** | **Em-Dash Rationale** | **15+** | **Rule — reason in one line** | **Rules without reason feel arbitrary** | **[docker](https://clawhub.ai/skills/docker)** |
