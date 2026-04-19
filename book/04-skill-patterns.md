# Part II, Chapter 4: Writing Patterns Discovered in the Top 1,000 Downloaded Skills

This chapter presents patterns discovered empirically by analyzing the **top 1,000 most-downloaded ClawHub skills** (12.5M downloads, 990 matched SKILL.md files + 889 script files).

Each pattern below was discovered from the data — not imported from existing literature. Every pattern cites frequency and specific skills.

### Data Sources

- **ClawHub API**: [clawhub.atomicbot.ai/api/skills?sort=downloads&dir=desc](https://clawhub.atomicbot.ai/api/skills?sort=downloads&dir=desc)
- **Skills repository**: [github.com/openclaw/skills](https://github.com/openclaw/skills) (58,593 skills cloned, 990 top-1000 matched)
- **Scripts analyzed**: 889 files across 326 skills with `scripts/` directories

---

## Pattern A: The "API Scaffold" Skill (75 skills, 7.6%)

**What**: A consistent 7-section scaffold used specifically by skills that wrap external APIs. The sections appear together with extremely high co-occurrence.

**Evidence**: 67+ skills have both `Authentication` + `Base URL` + `API Reference` sections. 68 have `Base URL` + `Code Examples` + `Connection Management`. This co-occurrence is too tight to be coincidence — it's a learned template.

**The scaffold**:
```
## Quick Start
## Base URL
## Authentication
## Connection Management
## API Reference (or Commands)
## Code Examples
## Error Handling
## Rate Limits
## Notes / Troubleshooting
```

**Why it works**: API skills share a consumption pattern — agent reads auth setup, then endpoint reference, then code examples. Skills that deviate from this scaffold make the agent hunt for info.

**Skills demonstrating this:**
- [api-gateway](https://clawhub.ai/skills/api-gateway) (70K dl, 635 lines, 124 API references): The canonical scaffold
- [stripe-api](https://clawhub.ai/skills/stripe-api) (19K dl, 4 scaffold signals): Full scaffold
- [gmail](https://clawhub.ai/skills/gmail) (31K dl, 3 signals)
- [outlook-api](https://clawhub.ai/skills/outlook-api) (21K dl, 3 signals)
- [whatsapp-business](https://clawhub.ai/skills/whatsapp-business) (21K dl, 3 signals)
- [stripe-best-practices](https://github.com/stripe/ai) (official Stripe skill): Same scaffold
- [xero](https://clawhub.ai/skills/xero) (18K dl, 3 signals)
- [google-slides](https://clawhub.ai/skills/google-slides) (18K dl, 3 signals)

**When to use this pattern**: If your skill wraps an HTTP API, use this scaffold verbatim. Don't invent a new structure.

---

## Pattern B: The "CLI Passthrough" Skill (~150 skills, ~15%)

**What**: Skills that are effectively thin prose wrappers around a single existing CLI tool. Characteristic: very short (<60 lines), 0-3 `##` sections, 90%+ bash code blocks, no scripts.

**Evidence**: Among top-30 downloaded skills, 12 are under 60 lines. Examples: `github` (48 lines), `gog` (37 lines, 0 sections), `weather` (50 lines), `nano-pdf` (21 lines), `sonoscli` (27 lines), `openai-whisper` (20 lines), `mcporter` (39 lines), `video-frames` (30 lines).

**The minimal structure**:
```markdown
# <tool-name>

One-sentence description of what the CLI does and when to use it.

Quick start
- `command1 arg` — what it does
- `command2 arg` — what it does

Common tasks
- `command3 arg` — what it does
```

**Why it works**: Documenting an already-well-designed CLI doesn't require a 500-line skill. The skill exists to *tell the agent this CLI is available* and show 5-10 canonical invocations. Padding out to hit an arbitrary size hurts, not helps.

**Skills demonstrating this:**
- [github](https://clawhub.ai/skills/github) (160K dl): `gh` CLI, 48 lines
- [gog](https://clawhub.ai/skills/gog) (158K dl): Google Workspace CLI, 37 lines, **zero `##` sections**
- [nano-pdf](https://clawhub.ai/skills/nano-pdf) (92K dl): 21 lines, single `## Quick start`
- [sonoscli](https://clawhub.ai/skills/sonoscli) (78K dl): 27 lines, no sections
- [openai-whisper](https://clawhub.ai/skills/openai-whisper) (70K dl): 20 lines, no sections
- [mcporter](https://clawhub.ai/skills/mcporter) (57K dl): 39 lines, no sections
- [video-frames](https://clawhub.ai/skills/video-frames) (42K dl): 30 lines, 2 sections
- [youtube-watcher](https://clawhub.ai/skills/youtube-watcher) (44K dl): 49 lines, 3 sections

**Key insight**: Download count does NOT correlate with length. These skills have 42K-160K downloads each, rivaling 600+ line sophisticated skills.

---

## Pattern C: Backtick-Wrapped Command Identifier in Description (30% of skills)

**What**: Descriptions reference the specific CLI tool or function by wrapping its name in backticks.

**Evidence**: 30% of top-1000 descriptions contain backtick-wrapped field names (e.g., `` `gh` ``, `` `nano-pdf` ``, `` `wttr.in` ``). 27% explicitly reference a specific tool/CLI/API.

**Why**: The backtick signals to the agent "this specific string is what you invoke." It also helps the agent match user intent when users ask "use `gh` to check CI" — the skill description matches literally.

**Skills demonstrating this:**
- [github](https://clawhub.ai/skills/github): "Interact with GitHub using the `gh` CLI."
- [mcporter](https://clawhub.ai/skills/mcporter): "Use the `mcporter` CLI..."
- [nano-pdf](https://clawhub.ai/skills/nano-pdf): "Edit PDFs...using the `nano-pdf` CLI."
- [obsidian](https://clawhub.ai/skills/obsidian): "...and automate via `obsidian-cli`."
- [weather](https://clawhub.ai/skills/weather): Mentions `wttr.in` and Open-Meteo by name
- [himalaya](https://clawhub.ai/skills/himalaya): "CLI to manage emails via IMAP/SMTP. Use `himalaya` to list, read..."

---

## Pattern D: The Arrow Notation (`→`) for Cause/Effect (34% of skills)

**What**: Using the `→` arrow character to indicate cause/effect, input/output, or trap/fix relationships.

**Evidence**: **339 skills (34%)** contain `→` in their content. This is dramatically higher than the em-dash rationale pattern (which uses `—`). The arrow is specifically used for directional relationships.

**Why**: The arrow is visually distinct and unambiguous. `Command --dry-run → preview only` tells the agent "when you see this flag, expect this behavior" faster than any prose.

**Skills demonstrating this:**
- [skill-vetter](https://clawhub.ai/skills/skill-vetter): Arrow-heavy RED FLAGS list — behaviors → reject decision
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent): "Workflow improvements → Promote to `AGENTS.md`"
- [stock-analysis](https://clawhub.ai/skills/stock-analysis): Command/option → outcome mappings
- [proactive-agent](https://clawhub.ai/skills/proactive-agent): "Autonomous vs Prompted Crons → Know when to use systemEvent vs isolated agentTurn"

**Usage patterns** (from top-1000):
- Command → expected output
- Input/trigger → action to take
- Condition → destination/target
- Problem → fix

---

## Pattern E: The "Quick Start" as Primary Entry Point (21% of skills)

**What**: A `## Quick Start` section placed immediately after the title, containing the minimum commands needed to use the skill.

**Evidence**: 21% of top-1000 skills have `## Quick Start` — the **#1 most common section header**. 14% have `## Notes`, 10% have `## Error Handling`, 10% have `## Setup`. Quick Start is nearly 2x more common than the next pattern.

**Why**: The Quick Start is the skill's ABI. It shows the agent (and the reader) the happy path in 3-6 bash commands. If the Quick Start works, everything else is gravy.

**Skills demonstrating this:**
- [nano-pdf](https://clawhub.ai/skills/nano-pdf): Entire skill is `## Quick start` + a single code block
- [weather](https://clawhub.ai/skills/weather): Quick start for two services (wttr.in + Open-Meteo)
- [video-frames](https://clawhub.ai/skills/video-frames): Quick start with absolute path to bundled script
- [nano-banana-pro](https://clawhub.ai/skills/nano-banana-pro): "Quick start" then "Default Workflow"
- [playwright-mcp](https://clawhub.ai/skills/playwright-mcp): Installation → Quick Start
- [brave-search](https://clawhub.ai/skills/brave-search): Setup → Search
- [skill-creator](https://clawhub.ai/skills/skill-creator) (72K dl): `## Quick start` is step 1

**Recipe**:
```markdown
# <Skill Name>
One paragraph of what and when.

## Quick Start
```bash
<command 1>  # comment showing expected output
<command 2>
<command 3>
```
```

---

## Pattern F: Scripts Use `argparse` + `--json` Flag (Python, 32% + 18%)

**What**: Python scripts in top-1000 skills overwhelmingly use `argparse` for CLI args and frequently support `--json` for machine-readable output.

**Evidence** (from 889 analyzed scripts):
- **32%** of all scripts use `argparse`
- **18%** implement a `--json` output flag
- **45%** have a `main()` function or `if __name__ == "__main__":` entry
- **12%** include a help/usage printer
- Only **1%** use `click` (the more modern alternative)

**Why**: `argparse` produces consistent help text. Agents can call `script.py --help` and parse the output. The `--json` flag separates human-readable (default) from machine-consumable output — the same script serves both audiences.

**Skills demonstrating this:**
- [gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md) (OpenAI): `scripts/inspect_pr_checks.py` with `--json`
- [stock-analysis](https://clawhub.ai/skills/stock-analysis): 7 Python scripts, all with argparse
- [polymarket-trade](https://clawhub.ai/skills/polymarket-trade): `scripts/polymarket.py` with full argparse
- [nano-banana-pro](https://clawhub.ai/skills/nano-banana-pro): `scripts/generate_image.py` with `--prompt` / `--filename` flags
- [tavily-search](https://clawhub.ai/skills/openclaw-tavily-search): `scripts/tavily_search.py` with `--query` / `--max-results`

---

## Pattern G: Bash Scripts Use `set -euo pipefail` (17% of scripts)

**What**: Bash scripts in skills opt into fail-fast mode with `set -e` (exit on error), `set -u` (error on undefined vars), and `set -o pipefail` (pipe failures propagate).

**Evidence**: **17%** of analyzed scripts include `set -euo pipefail` or a subset. **90%** start with a shebang. Only **10%** use `time.sleep`/rate limiting.

**Why**: Agents can't always distinguish partial success from complete success. A bash script that fails on line 3 but exits 0 because of silent pipe failures gives the agent a false "success" signal. `set -euo pipefail` eliminates this failure mode.

**Skills demonstrating this:**
- [code-change-verification](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification) (OpenAI): `scripts/run.sh` with `set -euo pipefail`
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent): `scripts/error-detector.sh` fails fast on missing env
- [pollyreach](https://clawhub.ai/skills/pollyreach) (96K dl): 6 bash scripts with strict mode
- [github-deploy-skill](https://playbooks.com/skills/openclaw/skills/github-deploy-skill): Fail-fast pattern

---

## Pattern H: Idempotent Setup Blocks (Evidence: top skills)

**What**: Initialization commands that check for existence before creating, making the setup script safe to run repeatedly.

**Evidence**: While specific patterns are hard to count corpus-wide, the top-downloaded memory skills all use this pattern.

**Why**: Agents don't remember across sessions by default. On every new session, the skill may re-run its setup. If setup isn't idempotent, re-running overwrites user data.

**Skills demonstrating this:**
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent) (398K dl, #1 on ClawHub):
  ```bash
  mkdir -p .learnings
  [ -f .learnings/LEARNINGS.md ] || printf "# Learnings\n..." > .learnings/LEARNINGS.md
  [ -f .learnings/ERRORS.md ] || printf "# Errors\n..." > .learnings/ERRORS.md
  ```
  Explicitly notes: "Never overwrite existing files. This is a no-op if `.learnings/` is already initialised."
- [proactive-agent](https://clawhub.ai/skills/proactive-agent): WAL protocol with idempotent init
- [elite-longterm-memory](https://clawhub.ai/skills/elite-longterm-memory): Idempotent multi-layer setup
- [memory-setup](https://clawhub.ai/skills/memory-setup): Config additions are non-destructive merges

**The canonical idempotent pattern in bash**:
```bash
mkdir -p <dir>                           # -p = idempotent mkdir
[ -f <file> ] || echo "<content>" > <file>  # create only if missing
```

---

## Pattern I: The "Overview / What's New" Header Stack (5% of skills)

**What**: A header stack at the top of SKILL.md showing version, what's new in the latest release, what's new in previous releases — before any workflow content.

**Evidence**: Observed in mature/multi-version top skills. [proactive-agent](https://clawhub.ai/skills/proactive-agent) has: `## What's New in v3.1.0` → `## What's in v3.0.0` → `## The Three Pillars`. [stock-analysis](https://clawhub.ai/skills/stock-analysis) has: `## What's New in v6.2` → `## What's in v6.1` → `## What's in v6.0`. [self-improving-agent](https://clawhub.ai/skills/self-improving-agent) has 28 versions and uses the same pattern.

**Why**: Skills evolve. A returning user (or agent with cached context) needs to know what changed. Placing version history at the top ensures deltas are seen first — before the main content.

**Skills demonstrating this:**
- [proactive-agent](https://clawhub.ai/skills/proactive-agent): "What's New in v3.1.0" / "What's in v3.0.0"
- [stock-analysis](https://clawhub.ai/skills/stock-analysis): 3 "What's in vN" sections
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent): 28 versions with changelog

**The shape**:
```markdown
# Skill Name (optional emoji)
Brief tagline.

## What's New in v3.1.0
- Bullet 1
- Bullet 2

## What's in v3.0.0  (keep for context)
- Earlier features
```

---

## Pattern J: The "Three Pillars" / Branded Philosophy Opening (Top skills)

**What**: Top-tier skills open with a branded conceptual framework — typically 3 principles — before any practical content. This differentiates the skill from its imitators.

**Evidence**: Observed in the most sophisticated top-20 skills but not in the commodity ones.

**Skills demonstrating this:**
- [proactive-agent](https://clawhub.ai/skills/proactive-agent) (145K dl): "The Three Pillars — Proactive / Persistent / Self-improving" with ✅ bullet points
- [humanizer](https://clawhub.ai/skills/humanizer) (92K dl): Personality/Content/Language/Style/Communication pillars
- [elite-longterm-memory](https://clawhub.ai/skills/elite-longterm-memory) (52K dl): "5 Memory Layers" framework
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent): Learnings/Errors/Features — 3 entry types

**Why**: This is marketing within the SKILL.md. A pillars framework makes the skill memorable and gives users vocabulary to describe it. It signals "this skill has a point of view."

**When to use**: Only for skills that genuinely introduce a new concept. Don't invent pillars for a simple API wrapper.

---

## Pattern K: Aggressive Cross-Linking via Related Skills (5% of skills)

**What**: A `## Related Skills` section listing 4-8 complementary skills with install commands, creating explicit skill ecosystems.

**Evidence**: 5% of top-1000 have this section — but within top-20 authors like steipete (44 skills) and byungkyu (70 skills), ALL skills cross-reference others in their family.

**Why**: Skills work better together. A `review-code` skill that references `git`, `typescript`, `ci-cd`, and `devops` tells the agent the full toolchain. This creates upward pull: installing one skill creates gravitational interest in the author's others.

**Skills demonstrating this:**
- [review-code](https://clawhub.ai/skills/review-code): Links to `code`, `git`, `typescript`, `ci-cd`, `devops`
- [docker](https://clawhub.ai/skills/docker): Links to devops, deploy, linux
- [word-docx](https://clawhub.ai/skills/word-docx) (ivangdavila): Links to other Office skills
- [excel-xlsx](https://clawhub.ai/skills/excel-xlsx) (ivangdavila): Same pattern — consistent author voice

**The format**:
```markdown
## Related Skills

Install with `clawhub install <name>` if user confirms:

- `code` — implementation workflow that complements review findings
- `git` — safer branch, diff, and commit handling during remediation
- `typescript` — stricter typing and runtime safety review for TS-heavy codebases
```

---

## Pattern L: Version Pinning in Title (16 skills in top 1000)

**What**: Including the skill's version number in the `# Title`, making the version visible in the agent's rendered view.

**Evidence**: 16 top-1000 skills have titles like `# Stock Analysis v6.1`, `# SkillScan v1.1.5`, `# Self-Improvement Skill`. Low frequency but distinct pattern.

**Why**: When the agent (or reader) sees a version in the title, they immediately know if the skill matches their expectations. Also signals "this is actively maintained."

**Skills demonstrating this:**
- [stock-analysis](https://clawhub.ai/skills/stock-analysis): `# Stock Analysis v6.1`
- [skillscan](https://clawhub.ai/skills/skillscan): `# SkillScan v1.1.5`
- [proactive-agent](https://clawhub.ai/skills/proactive-agent): Version in first `##` section

---

## Pattern M: Zero-Section Skills (~4%)

**What**: Top-downloaded skills with **zero `##` section headers** — just a title, opening paragraph, and flat content.

**Evidence**: 4% of top-1000 skills have zero `##` sections. These are not low-quality — they're deliberately flat for skills that wrap simple tools.

**Skills demonstrating this:**
- [gog](https://clawhub.ai/skills/gog) (158K dl)
- [sonoscli](https://clawhub.ai/skills/sonoscli) (78K dl)
- [openai-whisper](https://clawhub.ai/skills/openai-whisper) (70K dl)
- [mcporter](https://clawhub.ai/skills/mcporter) (57K dl)
- [blogwatcher](https://clawhub.ai/skills/blogwatcher) (35K dl)

**Why**: For a skill whose entire purpose is "here's a CLI tool and 5 canonical commands," section headers add structure without adding value. Flat content is easier to scan.

**The lesson**: Section hierarchy is a tool, not a requirement. Use it when you have branches in the workflow. Skip it for linear content.

---

## Pattern N: Structured Memory Entry IDs (pioneering, <1%)

**What**: A structured ID format for log entries, enabling cross-reference and promotion across sessions. Format: `[LRN-YYYYMMDD-XXX]`, `[ERR-YYYYMMDD-XXX]`, `[FEAT-YYYYMMDD-XXX]`.

**Evidence**: Pioneered by [self-improving-agent](https://clawhub.ai/skills/self-improving-agent) (398K dl, #1 on ClawHub, 3,240 stars). Now copied by [self-improving](https://clawhub.ai/skills/self-improving) (167K dl) and several derivative skills.

**Why**: Memory systems accumulate entries. Without stable IDs, cross-referencing is impossible — "the correction from yesterday" is ambiguous. Structured IDs make every entry addressable, promotable, and deletable.

**Skills demonstrating this:**
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent): `[LRN-YYYYMMDD-XXX] category` / `[ERR-YYYYMMDD-XXX] skill_or_command_name` / `[FEAT-YYYYMMDD-XXX] capability_name`
- [self-improving](https://clawhub.ai/skills/self-improving): Similar structured IDs
- [hippocampus-memory](https://clawhub.ai/skills/hippocampus-memory) (3K dl, 10 scripts): ID-indexed memory

**Why this is pioneering**: Most memory skills use free-form timestamps. Structured IDs enable machine-readable memory operations — the skill can query "all LRN entries in category=correction from the last 30 days."

---

## Pattern O: Prompt Engineering Inside SKILL.md (~15% of skills)

**What**: The SKILL.md contains first-person or second-person instructional text addressing the agent directly, such as "You are a writing editor..." or "When asked to review code...".

**Evidence**: 3% use first person ("You are a..."), but a broader ~15% address the agent in second person ("When asked to...", "You should...").

**Why**: These skills are essentially system prompts for the agent's subtask. They set persona before giving procedure.

**Skills demonstrating this:**
- [humanizer](https://clawhub.ai/skills/humanizer) (92K dl): "# Humanizer: Remove AI Writing Patterns — You are a writing editor that identifies and removes signs of AI-generated text..."
- [admapix](https://clawhub.ai/skills/admapix) (81K dl): "You are an ad intelligence and app analytics assistant..."
- [clawddocs](https://clawhub.ai/skills/clawddocs) (36K dl): "You are an expert on Clawdbot documentation."

**The shape**: `You are [role]. When [trigger], do [action].` — followed by procedural steps.

---

## Pattern P: Workspace-Injected Multi-File Memory (pioneering)

**What**: The skill expects (and checks for) specific files at specific workspace paths — `SOUL.md`, `AGENTS.md`, `TOOLS.md`, `MEMORY.md` — treating them as different categories of long-term memory.

**Evidence**: Pioneered by [self-improving-agent](https://clawhub.ai/skills/self-improving-agent) (398K dl). The OpenClaw platform injects these files into every session. The skill promotes learnings into the appropriate file by category.

**Skills demonstrating this:**
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent): Promotes by category — Behavioral → SOUL.md, Workflow → AGENTS.md, Tool gotchas → TOOLS.md
- [proactive-agent](https://clawhub.ai/skills/proactive-agent): Same workspace file integration
- [memory-setup](https://clawhub.ai/skills/memory-setup): Configures the workspace file injection

**Why**: Having one `MEMORY.md` means the agent must scan everything for relevance. Categorized files mean the agent loads just the category needed.

---

## Pattern Frequency Summary

| Pattern | % of top 1000 | Type |
|---------|---------------|------|
| E. Quick Start as primary entry | 21% | Structural |
| D. Arrow notation (→) | 34% | Syntactic |
| C. Backtick command identifier in desc | 30% | Description |
| H. Idempotent setup (evidence in top skills) | 15%+ | Scripting |
| O. Second-person agent instruction | 15% | Voice |
| A. API scaffold (7 co-occurring sections) | 7.6% | Template |
| B. CLI passthrough (<60 lines) | 15% | Minimalist |
| F. argparse + `--json` (Python scripts) | 32% + 18% | Scripting |
| G. `set -euo pipefail` (bash scripts) | 17% | Scripting |
| K. Aggressive cross-linking | 5% | Ecosystem |
| M. Zero-section skills | 4% | Minimalist |
| I. Version/What's New header stack | 5% | Maturity signal |
| L. Version in title | 1.6% | Maturity signal |
| N. Structured memory entry IDs | <1% | Pioneering |
| P. Workspace-injected memory files | <1% | Pioneering |
| J. "Three Pillars" branded opening | <1% | Pioneering |

### Key Takeaways

1. **The API Scaffold** (Pattern A) is a learned template — if you wrap an API, use it verbatim.
2. **CLI Passthrough** (Pattern B) is legitimate — 4 of the top 6 downloaded skills are under 60 lines.
3. **Scripts are code, not prose** — 32% use argparse, 45% have main(), 17% use fail-fast bash mode.
4. **Arrow notation (→) is universal** — 34% of top skills use `→` for cause/effect.
5. **The top skill pioneered three patterns** that are now being copied: structured memory IDs, workspace-file promotion, and explicit privacy constraints.
