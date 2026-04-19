# Chapter 6: Empirical Analysis of the Top 1,000 Downloaded Skills

This chapter presents findings from analyzing the **actual top 1,000 most-downloaded skills on ClawHub** (by download count from the [ClawHub API](https://clawhub.atomicbot.ai/api/skills?sort=downloads&dir=desc)), cross-referenced with their SKILL.md files in the [openclaw/skills](https://github.com/openclaw/skills) repository (58,593 skills total).

### Methodology

1. Queried the ClawHub API for the top 1,000 skills sorted by download count
2. Matched each to its SKILL.md file in the cloned `openclaw/skills` repository
3. Ran programmatic pattern detection on all 990 matched skills (10 not found in repo)
4. Deep-read the top 20 skills manually for structural analysis

---

## 6.1 The Top 20 Skills by Downloads

| Rank | Skill | Downloads | Lines | Sections | Code Blocks | Scripts | Refs |
|------|-------|-----------|-------|----------|-------------|---------|------|
| 1 | [self-improving-agent](https://clawhub.ai/skills/self-improving-agent) | 398,524 | 645 | 25 | 21 | 3 | 3 |
| 2 | [skill-vetter](https://clawhub.ai/skills/skill-vetter) | 212,949 | 139 | 6 | 5 | 0 | 0 |
| 3 | [ontology](https://clawhub.ai/skills/ontology) | 167,234 | 233 | 12 | 13 | 1 | 2 |
| 4 | [self-improving](https://clawhub.ai/skills/self-improving) | 166,829 | 251 | 14 | 4 | 0 | 0 |
| 5 | [github](https://clawhub.ai/skills/github) | 160,019 | 48 | 3 | 6 | 0 | 0 |
| 6 | [gog](https://clawhub.ai/skills/gog) | 158,020 | 37 | 0 | 0 | 0 | 0 |
| 7 | [proactive-agent](https://clawhub.ai/skills/proactive-agent) | 145,053 | 633 | 32 | 9 | 1 | 2 |
| 8 | [weather](https://clawhub.ai/skills/weather) | 136,298 | 50 | 2 | 4 | 0 | 0 |
| 9 | [multi-search-engine](https://clawhub.ai/skills/multi-search-engine) | 122,353 | 155 | 11 | 1 | 0 | 2 |
| 10 | [polymarket-trade](https://clawhub.ai/skills/polymarket-trade) | 121,966 | 252 | 9 | 15 | 1 | 0 |
| 11 | [pollyreach](https://clawhub.ai/skills/pollyreach) | 95,510 | 547 | 11 | 14 | 6 | 0 |
| 12 | [humanizer](https://clawhub.ai/skills/humanizer) | 92,489 | 438 | 11 | 0 | 0 | 0 |
| 13 | [nano-pdf](https://clawhub.ai/skills/nano-pdf) | 92,486 | 21 | 1 | 1 | 0 | 0 |
| 14 | [agent-browser](https://clawhub.ai/skills/agent-browser-clawdbot) | 91,547 | 207 | 9 | 17 | 0 | 0 |
| 15 | [nano-banana-pro](https://clawhub.ai/skills/nano-banana-pro) | 87,867 | 131 | 11 | 4 | 1 | 0 |
| 16 | [tavily-search](https://clawhub.ai/skills/openclaw-tavily-search) | 83,383 | 49 | 4 | 1 | 1 | 0 |
| 17 | [obsidian](https://clawhub.ai/skills/obsidian) | 83,200 | 56 | 2 | 0 | 0 | 0 |
| 18 | [admapix](https://clawhub.ai/skills/admapix) | 81,113 | 480 | 11 | 13 | 0 | 7 |
| 19 | [baidu-search](https://clawhub.ai/skills/baidu-search) | 79,770 | 64 | 5 | 2 | 1 | 1 |
| 20 | [sonoscli](https://clawhub.ai/skills/sonoscli) | 78,572 | 27 | 0 | 0 | 0 | 0 |

**Key observation**: Download count does NOT correlate with skill quality. The #1 skill (`self-improving-agent`, 398K downloads, 645 lines, 25 sections, 3 scripts) is deeply structured. But #13 (`nano-pdf`, 92K downloads, 21 lines) and #20 (`sonoscli`, 78K downloads, 27 lines, zero sections) are minimal. High downloads often reflect early publication or viral sharing, not quality.

---

## 6.2 Aggregate Statistics

| Metric | Top 1,000 Downloaded | Full Corpus (58,593) |
|--------|---------------------|---------------------|
| Total downloads | 12,502,864 | — |
| Avg downloads | 12,629 | — |
| Download range | 3,835 – 398,524 | — |
| Avg lines | 240 | ~150 |
| Avg sections (## headers) | 8.2 | ~5 |
| Avg code blocks | 10.6 | ~6 |
| Skills with `scripts/` | 327 (33%) | 18,204 (31%) |
| Skills with `references/` | 204 (20%) | 12,591 (22%) |

The top 1,000 skills are **60% longer**, have **64% more sections**, and **77% more code blocks** than the average skill. Investment in structure correlates with downloads (though causation is unclear).

---

## 6.3 Pattern Frequency in Top 1,000 Downloaded Skills

| Pattern | Count | % of 990 | Corpus % (58,593) | Delta |
|---------|-------|----------|-------------------|-------|
| Numbered steps | 621 | 62.7% | ~40% | +23 |
| Decision tables | 508 | 51.3% | ~30% | +21 |
| Prerequisites / Setup | 444 | 44.8% | ~20% | +25 |
| Quick Start / Quick Reference | 358 | 36.2% | 17.3% | +19 |
| Troubleshooting | 275 | 27.8% | 9.0% | +19 |
| Script referenced in body | 258 | 26.1% | — | — |
| Em-dash rationale (4+) | 228 | 23.0% | 36.6% | -14 |
| Error handling | 210 | 21.2% | 14.3% | +7 |
| ✅/❌ code contrast | 201 | 20.3% | 19.8% | +0.5 |
| When to Use | 171 | 17.3% | 13.2% | +4 |
| Output format / template | 141 | 14.2% | 9.7% | +5 |
| Best practices section | 124 | 12.5% | 11.8% | +1 |
| Security & trust | 112 | 11.3% | 1.5% | **+10** |
| Workflow section | 110 | 11.1% | 9.4% | +2 |
| Examples section | 97 | 9.8% | 4.6% | +5 |
| Common traps / gotchas | 94 | 9.5% | 3.9% | +6 |
| AI-specific mistakes | 85 | 8.6% | — | new |
| Checklist items `[ ]` | 78 | 7.9% | 6.3% | +2 |
| Core rules section | 71 | 7.2% | 1.4% | **+6** |
| Related skills | 60 | 6.1% | 2.9% | +3 |
| Memory directory (`~/name/`) | 52 | 5.3% | 3.6% | +2 |
| When NOT to use | 46 | 4.6% | 4.9% | -0.3 |
| Approval gate | 43 | 4.3% | 3.1% | +1 |
| Red flags | 22 | 2.2% | — | — |

**What the top 1,000 over-index on** (much more than corpus average):
- **Prerequisites / Setup** (+25pp) — top skills tell you what you need before starting
- **Numbered steps** (+23pp) — top skills are procedural, not descriptive
- **Decision tables** (+21pp) — top skills include tables for classification
- **Quick Start** (+19pp) — top skills provide a fast path
- **Troubleshooting** (+19pp) — top skills anticipate failures
- **Security & trust** (+10pp) — top skills declare their data practices
- **Core rules** (+6pp) — top skills have a named "Core Rules" section

---

## 6.4 Script Analysis — What Top Skills Actually Execute

**327 of the top 1,000 skills (33%) include a `scripts/` directory.** Average: 2.9 scripts per skill when present.

### Script Languages

| Language | Count | % of scripted skills |
|----------|-------|---------------------|
| Python | 183 | 56% |
| Bash/Shell | 105 | 32% |
| JavaScript/TypeScript | 39 | 12% |

### What Scripts Do (from deep reading top skills)

| Script Type | What It Does | Example Skills |
|-------------|-------------|---------------|
| **API wrapper** | Wraps an external API with structured I/O | [polymarket-trade](https://clawhub.ai/skills/polymarket-trade), [stock-watcher](https://clawhub.ai/skills/stock-watcher), [crypto-market-data](https://clawhub.ai/skills/crypto-market-data) |
| **Verification runner** | Runs checks in strict order with fail-fast | [code-change-verification](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification) (OpenAI) |
| **Data fetcher** | Fetches and parses external data | [baidu-search](https://clawhub.ai/skills/baidu-search), [multi-search-engine](https://clawhub.ai/skills/multi-search-engine), [tech-news-digest](https://clawhub.ai/skills/tech-news-digest) |
| **File processor** | Transforms files (PDF, Excel, images) | [automate-excel](https://clawhub.ai/skills/automate-excel), [nano-banana-pro](https://clawhub.ai/skills/nano-banana-pro) |
| **System automation** | Controls OS/hardware | [windows-control](https://clawhub.ai/skills/windows-control) (23 scripts!), [computer-use](https://clawhub.ai/skills/computer-use) (17 scripts) |
| **Memory/state manager** | Reads/writes persistent state files | [self-improving-agent](https://clawhub.ai/skills/self-improving-agent), [session-memory](https://clawhub.ai/skills/session-memory), [hippocampus-memory](https://clawhub.ai/skills/hippocampus-memory) |

### Key Script Patterns

**Pattern A: SKILL.md routes to scripts by scenario**

From [self-improving-agent](https://clawhub.ai/skills/self-improving-agent) (398K downloads):
```
| Situation                | Action                                    |
|--------------------------|-------------------------------------------|
| Command/operation fails  | Log to `.learnings/ERRORS.md`             |
| User corrects you        | Log to `.learnings/LEARNINGS.md`          |
| Found better approach    | Log with category `best_practice`         |
| Broadly applicable       | Promote to `CLAUDE.md` or `AGENTS.md`     |
```

The SKILL.md is a routing table; each route points to a file or script.

**Pattern B: Script with `--json` flag for machine-readable output**

From OpenAI [gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md):
```bash
python scripts/inspect_pr_checks.py --repo "." --pr "123" --json
```

Dual output: human-readable by default, `--json` for when the agent needs structured data.

**Pattern C: Scripts with cross-platform variants**

From OpenAI [code-change-verification](https://playbooks.com/skills/openai/openai-agents-js/code-change-verification):
```
scripts/
├── run.sh    # Unix
└── run.ps1   # Windows
```

**Pattern D: Initialization scripts that create directory structure**

From [self-improving-agent](https://clawhub.ai/skills/self-improving-agent):
```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Learnings\n..." > .learnings/LEARNINGS.md
[ -f .learnings/ERRORS.md ] || printf "# Errors\n..." > .learnings/ERRORS.md
```

The script is idempotent — safe to re-run. It creates files only if they don't exist.

---

## 6.5 New Patterns Discovered from Top-1,000 Analysis

### Pattern 28: Prerequisites / Setup Section (444/990 = 44.8%)

**What**: A section listing exact tools, credentials, and environment setup needed before the skill can run.

**Why**: 44.8% of top-1,000 skills include this — the 3rd most common pattern after numbered steps and decision tables. Without prerequisites, the agent discovers missing dependencies mid-execution, wasting tokens on error recovery. Listing prerequisites upfront allows fail-fast at the start.

**How**: Create a `## Prerequisites` or `## Setup` section with exact install commands and verification steps.

**Skills demonstrating this:**
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent): "First-Use Initialisation" with exact bash commands to create directory structure
- [github](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/github/SKILL.md): "Setup" with `gh auth login` and `gh auth status`
- [gh-issues](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/gh-issues/SKILL.md): Token resolution sequence with 3 fallback paths
- [polymarket-trade](https://clawhub.ai/skills/polymarket-trade): API key setup, wallet configuration
- [skill-vetter](https://clawhub.ai/skills/skill-vetter): "Source Check" as prerequisite to vetting

### Pattern 29: Security Vetting Checklist (112/990 = 11.3%)

**What**: A checklist of security red flags to check before trusting a skill's output or installing a dependency.

**Why**: 11.3% of top-1,000 skills include security/trust declarations — **7.5x higher than the corpus average** (1.5%). Post-ClawHavoc, top skills signal trustworthiness. The [skill-vetter](https://clawhub.ai/skills/skill-vetter) (212K downloads, #2 on ClawHub) is entirely a security checklist.

**How**: Include `## Security & Privacy` or `## Trust` section. Declare: what data leaves, what's stored locally, what the skill does NOT do.

**Skills demonstrating this:**
- [skill-vetter](https://clawhub.ai/skills/skill-vetter) (212K dl): Complete vetting protocol with RED FLAGS checklist, risk classification (🟢/🟡/🔴/⛔), and structured vetting report
- [proactive-agent](https://clawhub.ai/skills/proactive-agent) (145K dl): "Security Hardening — Skill installation vetting, agent network warnings, context leakage prevention"
- [review-code](https://clawhub.ai/skills/review-code): External Endpoints table + Security & Privacy declaration
- [github-actions](https://clawhub.ai/skills/github-actions): External Endpoints + Trust section

### Pattern 30: Promotion / Escalation Rules (52/990 = 5.3%)

**What**: Rules for when learnings or findings should be "promoted" from the skill's local storage to project-level or workspace-level files.

**Why**: Pioneered by [self-improving-agent](https://clawhub.ai/skills/self-improving-agent) (398K downloads, #1 on all of ClawHub). The idea: learnings start local, and if they prove broadly applicable, they get promoted to CLAUDE.md, AGENTS.md, or other project files. This creates a learning hierarchy.

**How**: Define promotion criteria (e.g., "3x occurrences across 2+ tasks in 30 days") and promotion targets.

**Skills demonstrating this:**
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent): Promotion table — behavioral patterns → `SOUL.md`, workflow improvements → `AGENTS.md`, tool gotchas → `TOOLS.md`
- [proactive-agent](https://clawhub.ai/skills/proactive-agent): "Self-Improvement Guardrails — Safe evolution with ADL/VFM protocols"
- [self-improving](https://clawhub.ai/skills/self-improving) (166K dl): Similar promotion pattern
- [coding](https://clawhub.ai/skills/coding): Style memory with explicit-only learning
- [decide](https://clawhub.ai/skills/decide): Decision patterns with promotion gates

---

## 6.6 The Self-Improving-Agent Case Study

The #1 skill on all of ClawHub (398,524 downloads, 3,240 stars, 28 versions) deserves deep study because it pioneered several patterns now widely copied.

### Structure

```
self-improving-agent/
├── SKILL.md (645 lines, 25 sections)
├── scripts/
│   ├── init.sh
│   ├── review.sh
│   └── promote.sh
└── references/
    ├── logging-format.md
    ├── detection-triggers.md
    └── hook-integration.md
```

### Key Patterns Originated Here

1. **Signal Detection Triggers**: The skill defines natural-language patterns that trigger logging — "No, that's not right...", "Actually...", "A better approach..." — and maps each to a logging category (correction, insight, knowledge_gap, best_practice).

2. **Structured Logging Format**: Three entry types (`[lrn-YYYYMMDD-XXX]`, `[err-YYYYMMDD-XXX]`, `[feat-YYYYMMDD-XXX]`) with specific fields per type.

3. **Promotion Hierarchy**: `.learnings/` (local) → `CLAUDE.md` / `AGENTS.md` / `SOUL.md` (workspace) → project memory.

4. **Hook Integration**: Opt-in hooks (`PostToolUse`, `PreCompact`) that trigger logging automatically without manual invocation.

5. **Idempotent Initialization**: The init script creates directory structure only if it doesn't exist — safe to run on every session start.

6. **Privacy Constraint at the Top**: "Do not log secrets, tokens, private keys... Prefer short summaries over raw output." — placed in the initialization section, ensuring it's read before any logging.

---

## 6.7 Key Takeaways for Skill Authors

Based on the top-1,000 analysis:

1. **Structure matters more than length**: The top skills are 60% longer than average, but more importantly they have 64% more sections. Well-organized content > wall of text.

2. **Numbered steps are the #1 pattern** (62.7%): If your skill has a procedure, number the steps.

3. **Decision tables are the #2 pattern** (51.3%): Top skills include at least one table for classification or comparison.

4. **Prerequisites save tokens**: 44.8% of top skills list prerequisites upfront. Fail-fast at the start, not mid-execution.

5. **Scripts make skills actionable**: 33% include scripts. Python is dominant (56% of scripted skills), followed by Bash (32%).

6. **Security is a top-skill differentiator**: 11.3% of top skills vs 1.5% corpus average. Post-ClawHavoc, trust declarations signal quality.

7. **Download count ≠ quality**: The top 20 includes both the most sophisticated skill on ClawHub (self-improving-agent, 645 lines) and near-empty shells (sonoscli, 27 lines, zero sections).

8. **The "When NOT to Use" gap**: Only 4.6% of top skills include negative triggers — a massive quality gap. Adding negative triggers is the highest-leverage improvement for most skills.
