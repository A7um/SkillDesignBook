# Part I: Philosophy — What the Top 1,000 Downloaded Skills Reveal

This chapter extracts design philosophy from the **actual top 1,000 most-downloaded skills on ClawHub** (12.5M total downloads, range 3,835–398,524). Data comes from programmatic analysis of 990 matched SKILL.md files plus deep reading of the top 50.

Every principle below is backed by empirical frequency across the corpus, not intuition.

---

## Principle 1: Description Starts with an Action Verb or Tool Reference

**Evidence**: 23% of top-1000 descriptions start with an action verb (Create, Build, Generate, Analyze, Search, Run, Manage, Fetch, Extract, Write, Edit, etc.). Another 27% reference a specific tool/CLI/API by backtick name. The average description length is **155 characters**.

**Why**: The description is the only text the agent reads at startup for every installed skill. An action verb lets the agent immediately determine *what this does*. A tool reference lets the agent match the user's intent (e.g., "use `gh`") directly to the skill.

**Skills demonstrating this:**
- [weather](https://clawhub.ai/skills/weather) (136K dl): "Get current weather and forecasts (no API key required)."
- [nano-pdf](https://clawhub.ai/skills/nano-pdf) (92K dl): "Edit PDFs with natural-language instructions using the `nano-pdf` CLI."
- [github](https://clawhub.ai/skills/github) (160K dl): "Interact with GitHub using the `gh` CLI."
- [video-frames](https://clawhub.ai/skills/video-frames) (42K dl): "Extract frames or short clips from videos using ffmpeg."
- [mcporter](https://clawhub.ai/skills/mcporter) (57K dl): "Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly..."

**What "Use when:" tells us**: 31% of descriptions include "Use when" — the second most common phrase after the initial verb. But only 0.4% include explicit "Don't use" or "NOT for" — a massive quality gap.

---

## Principle 2: A Title Heading Is Mandatory; Everything Else Is Optional

**Evidence**: **93% of top-1000 skills open with a `# Title` heading** immediately after frontmatter. Only 4% open with `##` directly. This is the most universal formatting convention in the corpus.

**Why**: The title heading gives the skill a visible identity in tools that render Markdown, and serves as an anchor for the agent to know "this is where the skill begins."

**Skills demonstrating this:**
- Every top-20 skill starts with `# <Skill Name>` (often with emoji) followed by one paragraph of context.

**Counter-examples (4 skills in top 30 with NO `##` sections at all):**
- [gog](https://clawhub.ai/skills/gog) (158K dl, 37 lines): Just a title + bullet list
- [sonoscli](https://clawhub.ai/skills/sonoscli) (78K dl, 27 lines): Title + flat bullet list
- [openai-whisper](https://clawhub.ai/skills/openai-whisper) (70K dl, 20 lines): Title + quick start code block
- [mcporter](https://clawhub.ai/skills/mcporter) (57K dl, 39 lines): Title + 3 bullet lists

**The philosophy**: Structure is optional for simple CLI-wrapping skills. A 20-line skill wrapping a single CLI tool doesn't need sections — it needs copy-pasteable commands.

---

## Principle 3: Bash Code Blocks Are the Dominant Teaching Mechanism

**Evidence**: 66% of top-1000 skills contain bash/shell code blocks. 78% of all skills contain SOME kind of code block (`` ``` ``). 56% contain markdown tables. In aggregate, **top-1000 skills average 10.6 code blocks each** — roughly one code block per 23 lines.

**Why**: Skills aren't documentation; they're procedures. Executable commands are the unit of transfer. Prose describing what `gh pr checks` does is useless — the exact command `gh pr checks 55 --repo owner/repo` is the value.

**Skills demonstrating this:**
- [github](https://clawhub.ai/skills/github) (48 lines total): 6 bash code blocks. That's 1 code block per 8 lines.
- [weather](https://clawhub.ai/skills/weather) (50 lines): 4 code blocks covering `curl` invocations.
- [nano-pdf](https://clawhub.ai/skills/nano-pdf) (21 lines): 1 code block — that IS the skill.
- [mcporter](https://clawhub.ai/skills/mcporter) (39 lines): 0 code blocks, pure bullet list. Exception, not rule.

**Implication**: If your skill has fewer than 1 code block per 25 lines, it's probably too abstract. Either add concrete examples or cut the prose.

---

## Principle 4: Hard Emphasis Keywords Carry Real Weight

**Evidence**: 
- **41%** of top-1000 skills use `ALWAYS` or `MUST` (hard positive)
- **33%** use `IMPORTANT`, `CRITICAL`, or `WARNING`
- **28%** use `NEVER`, `DO NOT`, or `MUST NOT` (hard negative)
- Combined: **~60% of top-1000 skills use emphasis keywords**

**Why**: LLMs respond differently to "prefer X" vs "ALWAYS X" vs "**ALWAYS X**". Emphasis keywords signal priority at the attention layer. Without them, every instruction has equal weight.

**Skills demonstrating this:**
- [skill-vetter](https://clawhub.ai/skills/skill-vetter) (213K dl): `**Never install a skill without vetting it first.**`
- [stock-analysis](https://clawhub.ai/skills/stock-analysis) (45K dl, 249 lines): Uses `IMPORTANT` and `CRITICAL` for risk warnings
- [proactive-agent](https://clawhub.ai/skills/proactive-agent) (145K dl): Multiple `⭐ NEW` markers + hard constraints
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent) (398K dl): "Never overwrite existing files" / "Do not log secrets, tokens..."

**But**: Only **1%** wrap these in bold all-caps (`**NEVER**`). Most use plain caps. The visual noise of bold caps doesn't help — the keyword alone is sufficient.

---

## Principle 5: The "Concise/Compact" Self-Instruction

**Evidence**: 32% of top-1000 skills include the words `concise`, `compact`, `brief`, `terse`, `short`, or `minimal` — usually as self-instructions to the agent about output length.

**Why**: LLMs default to verbose output. Without explicit counter-instructions, agents write essays when users want a status line. Top skills actively constrain output verbosity.

**Skills demonstrating this:**
- [github](https://clawhub.ai/skills/github): `# Output: London: ⛅️ +8°C` — single-line expected outputs
- [weather](https://clawhub.ai/skills/weather): Documents compact format codes (`%c` for condition, `%t` for temp)
- [skill-creator](https://clawhub.ai/skills/skill-creator) (72K dl): "Keep descriptions concise"

**The pattern**: Top skills don't just show what to do — they constrain how to present results.

---

## Principle 6: Memory Lives in Known Paths

**Evidence**: 21% of top-1000 skills reference literal file paths like `~/.something/`. 18% include patterns for memory/state persistence (`.learnings/`, `memory.md`, `~/<skillname>/`).

**Why**: Skills that learn across sessions need persistent storage. Rather than invent path conventions per skill, top skills use a shared convention: `~/<skill-name>/` or `~/.openclaw/workspace/`. Predictable paths enable cross-skill memory sharing.

**Skills demonstrating this:**
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent) (398K dl): `~/.openclaw/workspace/.learnings/`
- [self-improving](https://clawhub.ai/skills/self-improving) (167K dl): `~/self-improving/` with tiered structure
- [elite-longterm-memory](https://clawhub.ai/skills/elite-longterm-memory) (52K dl): Multi-layer memory architecture
- [ontology](https://clawhub.ai/skills/ontology) (167K dl): Typed entity storage with validation
- [memory-setup](https://clawhub.ai/skills/memory-setup) (36K dl): Configures `memorySearch` with shared path conventions
- [review-code](https://clawhub.ai/skills/review-code): `~/review-code/` for findings and preferences

**The convention**: Most top memory skills use `~/<skill-slug>/memory.md` + optional subdirectories (`findings/`, `sessions/`, `baselines/`).

---

## Principle 7: Scripts Carry 3x More Lines Than SKILL.md

**Evidence**: Of the 326 top-1000 skills with a `scripts/` directory, the total script code is **211,969 lines** vs **65,783 lines** of SKILL.md content — a **3.22x ratio**.

**Why**: SKILL.md is the agent's entry point. Scripts are the implementation. For skills that wrap APIs or automate tools, 80% of the engineering work lives in `scripts/`, not in the prose. The prose exists to route the agent to the right script with the right arguments.

**Skills demonstrating this:**
- [windows-control](https://clawhub.ai/skills/windows-control) (7K dl): 23 Python scripts
- [email-to-calendar](https://clawhub.ai/skills/email-to-calendar) (5K dl): 23 bash scripts
- [automate-excel](https://clawhub.ai/skills/automate-excel) (5K dl): 18 Python scripts
- [computer-use](https://clawhub.ai/skills/computer-use) (12K dl): 17 bash scripts
- [stock-watcher](https://clawhub.ai/skills/stock-watcher) (28K dl): 8 scripts (Python + Bash)

**Script languages**: Python 51%, Bash 30%, JavaScript 12%, Node variants 7%.

**Implication**: For complex skills, the SKILL.md is a façade. Author scripts with the same care you'd give production code — they're the actual product.

---

## Principle 8: Scripts Must Self-Document for the Agent

**Evidence in scripts**:
- **90%** start with a shebang (`#!/usr/bin/env python3` or `#!/bin/bash`)
- **45%** have a `main()` function or `if __name__ == "__main__":` entry point (Python)
- **32%** use `argparse` for structured CLI args (Python)
- **18%** support a `--json` flag for machine-readable output
- **12%** include a help/usage text printer
- **17%** use `set -euo pipefail` (fail-fast, bash)

**Why**: Scripts are called by agents, not humans. Agents parse `--help` output, check exit codes, and react to structured JSON. A script that silently fails or produces inconsistent output breaks the skill.

**Skills demonstrating this:**
- [gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md) (OpenAI): `scripts/inspect_pr_checks.py` with `--json` flag for machine output
- [polymarket-trade](https://clawhub.ai/skills/polymarket-trade) (122K dl): `scripts/polymarket.py` with argparse + structured JSON output
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent): `scripts/error-detector.sh`, `scripts/activator.sh`, `scripts/extract-skill.sh` — each script has a single job
- [code-change-verification](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification) (OpenAI): `scripts/run.sh` with `set -euo pipefail` for fail-fast verification
- [stock-analysis](https://clawhub.ai/skills/stock-analysis) (45K dl): 7 scripts, each with argparse and descriptive help text

**Anti-pattern**: 55% of scripts have error handling (`try/except` or `try/catch`), but only **14%** implement retry logic. Top skills lean on fail-fast + structured errors, not silent retries.

---

## Principle 9: Naming Follows the `short-hyphen-case` Convention

**Evidence**: 47% of top-1000 skills use 2-word hyphenated names (e.g., `nano-pdf`, `brave-search`). 25% use 3 words. 22% are single-word. Only 3% use 4+ words.

**Why**: Short names are invokable. Agents see `$skill-name` in system prompts; short names are memorable and distinguishable. Names longer than 3 words suggest the skill is trying to do too much (Pattern: One skill, one job).

**Skills demonstrating this:**
- Steipete (a prolific top author) uses single-word skills: `github`, `gog`, `weather`, `obsidian`, `slack`, `notion`, `mcporter`, `sonoscli`, `brave-search`
- Most-downloaded: `self-improving-agent` (3 words), `skill-vetter` (2), `ontology` (1), `proactive-agent` (2), `nano-pdf` (2)

**Counter-example**: [openclaw-tavily-search](https://clawhub.ai/skills/openclaw-tavily-search) (83K dl) — 3 words including a redundant `openclaw-` prefix. The skill works despite the clunky name.

---

## Principle 10: Authorship Concentrates

**Evidence**: The top 15 authors account for **272 skills** (27% of top-1000) with **3.78M downloads** (30% of total). One author alone — **steipete** — has 44 skills with **1.77M combined downloads**.

**Why**: Skill authoring is a craft. Top authors develop a consistent voice and re-apply patterns across their catalog. Their skills cross-reference each other (`Related Skills: see my `github` skill`), creating ecosystems.

**Top authors and their patterns:**
- **steipete** (44 skills, 1.77M dl): Single-word names, minimal sections, bash-heavy examples. Skills: `github`, `gog`, `weather`, `obsidian`, `slack`, `notion`, `nano-pdf`, `sonoscli`, `mcporter`, `brave-search`, `video-frames`, `youtube-watcher`, `openai-whisper`
- **byungkyu** (70 skills, 840K dl): API-scaffold skills (authentication → base URL → api reference → rate limits → pagination). Skills: `api-gateway`, `gmail`, `stripe-api`, `slack`, dozens more
- **ivangdavila** (50 skills, 737K dl): Word/Excel/PDF document skills with consistent "Core Rules → Common Traps → Related Skills" structure

**The lesson for authors**: Pick a niche. Build a family of skills that share vocabulary, conventions, and cross-references. Individual skills benefit from being part of a family.

---

## Summary of the 10 Principles

| # | Principle | Evidence |
|---|-----------|----------|
| 1 | Description starts with action verb or tool reference | 23% verb + 27% tool = 50% of top-1000 |
| 2 | Title heading mandatory, sections optional | 93% start with `# Title` |
| 3 | Bash code blocks are the teaching mechanism | 66% use bash blocks, avg 10.6 code blocks/skill |
| 4 | Hard emphasis keywords carry weight | 60%+ use ALWAYS/NEVER/MUST/IMPORTANT |
| 5 | "Concise/compact" self-instruction | 32% include conciseness directives |
| 6 | Memory lives in predictable paths | 21% reference `~/<skill-name>/` or workspace paths |
| 7 | Scripts carry 3x more lines than SKILL.md | 211K script lines vs 66K SKILL.md lines |
| 8 | Scripts must self-document | 90% shebang, 32% argparse, 18% `--json` |
| 9 | Names use `short-hyphen-case` | 47% 2-word, 22% 1-word, only 3% 4+ words |
| 10 | Authorship concentrates | Top 15 authors = 27% of top-1000 |

---

### Source

All evidence in this chapter is derived from:

- **ClawHub API** for download counts: https://clawhub.atomicbot.ai/api/skills?sort=downloads&dir=desc
- **openclaw/skills repository** for SKILL.md files: https://github.com/openclaw/skills (cloned, 58,593 skills)
- Top 1,000 by downloads → 990 matched SKILL.md files → programmatic pattern detection + deep read of top 50
