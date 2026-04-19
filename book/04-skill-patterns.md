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
