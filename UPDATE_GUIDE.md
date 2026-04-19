# SkillDesignBook — Update Guide

> This guide is itself a skill. It follows the book's own principles: opinionated stance, named failure modes, explicit thresholds, and a clear split between what machines decide and what agents decide. If you find yourself about to violate one of the rules below, the guide is probably right and you're probably being tempted by a rationalization. Re-read the Rationalizations table at the bottom first.

---

## The Two-Layer Design

**Pattern matching counts. Agents read.**

This is the central discipline of the update process. The script `scripts/research.py` handles what regex is good at — counting occurrences of *known* patterns, detecting 404s, surfacing new top-20 entrants, computing frequency diffs. It never decides what's a new pattern, because regex can't detect patterns it hasn't been taught.

An agent handles what reading is good at — opening actual SKILL.md files, noticing structural moves the detectors don't know about, verifying that a citation's quoted text still appears verbatim, judging whether a new skill's philosophy genuinely extends Chapter 1 or just rephrases an existing principle.

Neither layer can substitute for the other. A regex-only pipeline misses novel patterns. An agent-only pipeline wastes context reading the same 1,000 skills every cycle when most cycles don't need a book change.

The script produces a **worklist**: a small, curated set of skills the agent should actually read. The agent reads them and writes findings. A human reviews the findings before any book edit lands.

## Why This Guide Exists

The book is grounded in measurements: "Pattern X appears in N% of the top-1,000 downloaded skills." Those numbers go stale. Skills drop out of the top 1,000. Citations break. New structural patterns emerge that no existing detector will catch.

This guide exists to prevent **three failure modes**:

- **Staleness** — the book keeps claiming frequency numbers that no longer match reality, cites skills that no longer rank, or misses patterns that have become universal.
- **Churn** — the book gets rewritten every cycle to match the latest top-1 skill, losing the stable principles that were already well-founded.
- **Detector blindness** — the book's pattern list calcifies around what the regex detectors know, and genuinely new structural moves in the corpus go unnoticed because the script never flagged them.

Staleness erodes credibility. Churn destroys structure. Detector blindness is the subtlest: the book looks consistent, the numbers look fresh, but the corpus has moved on in a direction the pipeline can't see.

---

## The Inclusion Bar

A change makes it into the book if and only if one of:

1. **A pattern appears in 5+ independently-authored skills in the current top-1,000.** Evidence: the frequency report from `scripts/research.py`.
2. **A pattern is pioneered by a top-5-downloaded skill** and is structurally novel. Pioneering status allows <5-skill inclusion because the top-5 are reference-class.
3. **A pattern frequency in the book has shifted by ≥5 percentage points.** The new frequency is published; the chapter text updates only if the shift changes what the pattern means.
4. **A cited skill has dropped out of the top 1,000 or 404s.** Replace or remove.

Everything else is noise. Single-skill examples, blog announcements, and personal preferences do not qualify.

---

## Quick Start

```bash
# Step 1: refresh the quantitative layer (~10 seconds)
python3 scripts/research.py

# Step 2: agent reads the worklist and writes findings
#   research/worklists/<date>.md   ← what to read
#   research/findings/<date>.md    ← what you conclude
```

Step 1 fetches the top 1,000 from the ClawHub API, analyzes against the local SKILL.md corpus, diffs against the previous snapshot, validates citations, and writes two outputs:

- `research/reports/<date>.md` — the **quantitative report** (numbers: frequency shifts, broken citations, pattern candidates)
- `research/worklists/<date>.md` — the **agent reading list** (about 40 skills: top 20, new entrants, structural outliers)

Step 2 is manual: an agent opens the worklist, reads each listed SKILL.md, and writes answers to the three questions at the bottom of the worklist into `research/findings/<date>.md`.

No book changes happen until a human reviews the findings.

### Subcommands if you need them

| Command | What it does |
|---|---|
| `research.py fetch` | Snapshot the top 1,000 to `research/snapshots/<date>.json` |
| `research.py analyze` | Print pattern frequencies from the latest snapshot |
| `research.py compare` | Diff the two most recent snapshots, print a report |
| `research.py worklist` | Emit the agent reading list for the latest snapshot |
| `research.py validate` | List book citations that no longer resolve |
| `research.py` (default) | Run the full pipeline: fetch → compare → validate → worklist |

---

## Workflow

### 1. Quantitative layer — run the pipeline

```bash
python3 scripts/research.py
```

If the SKILL.md corpus isn't cloned locally, clone it once:

```bash
git clone --depth 1 https://github.com/openclaw/skills.git /tmp/clawhub-skills
```

The pipeline looks for SKILL.md files under `$SKILLS_REPO` (defaults to `/tmp/clawhub-skills/skills`). It tolerates missing files — unmatched skills are counted but not pattern-analyzed.

Outputs:

- `research/snapshots/<date>.json` — raw data for future diffs
- `research/reports/<date>.md` — quantitative findings
- `research/worklists/<date>.md` — what the agent should read

### 2. Agentic layer — read the worklist

Open `research/worklists/<date>.md`. It's organized into four groups:

- **Top 20 by downloads (reference class)** — read every one. These are the skills users actually use; any structural move they make is high-leverage. Some you'll skim because you already know them; read at least the ones you haven't seen recently.
- **New entrants into top 20** — read carefully. These are the skills breaking in. A new structural move here is the most likely source of a new pattern.
- **Structural outliers** — skills whose shape (lines, sections, scripts, regex hit count) is unusual among the top 1,000 AND whose pattern hits are below average. The combination is the signal: they don't look like their neighbors AND they don't match known patterns. If a new pattern is hiding anywhere, it's most likely hiding here.
- **Pattern candidates (from the regex)** — the script says these known patterns are close to threshold. Verify by reading a few matching skills — the detector might be overcounting.

For each skill, **read the actual SKILL.md body, not just the description or the pattern hit row**. The pattern hits are a hint, not a substitute. The worklist lists download counts, line counts, and section counts — use these to prioritize, not to conclude.

For each skill you read, write a one-line note in `research/findings/<date>.md`. Then answer three questions for the cycle:

1. **Is there a structural pattern here that is NOT in `book/04-skill-patterns.md`?**
   - If you see the same novel structure across 3+ skills → candidate; add to `research/candidates.md`, don't yet add to the book.
   - If 5+ skills → propose a new pattern entry with evidence links.
   - If just 1–2 skills → one-off, not a pattern.

2. **Does this skill declare a design stance worth adding to `book/01-philosophy.md`?**
   - Only if a higher-downloaded skill makes a principle's point better than the current citation.
   - Never propose a principle based on a single skill. Chapter 1 requires multi-skill convergence.

3. **If this skill is cited in the book, are the citation's specifics still accurate?**
   - Check the quoted text still appears in SKILL.md verbatim.
   - Check the download count cited is within ±5% of current.
   - Check any claim about the skill's structure still holds.

### 3. Pre-flight landscape check

Before touching `book/`, with the findings file in front of you, answer:

1. **Has a new pattern genuinely emerged?** Multi-skill convergence only. Single high-downloaded skills don't count.
2. **Does Chapter 1 (Philosophy) still hold?** Pick two principles and check: are the cited skills still reference-class? Are their quoted lines still intact? If a principle's evidence has eroded, flag for human review — do not auto-edit Chapter 1.
3. **Is Chapter 4's pattern list still complete?** If your findings show a pattern hitting 5+ skills that's not in Chapter 4, the chapter is incomplete. Propose an addition.

### 4. Make the changes

See the per-chapter policy below. Agent auto-commit is allowed only for the specific cases listed there; anything else needs human review of the findings file first.

### 5. Commit with a changelog entry

Append a dated block to `research/changelog.md`:

```markdown
## <YYYY-MM-DD>

### Pipeline run
- Fetched: <N> skills, matched <M> to SKILL.md

### Changes made
- <file>: <what and why, with evidence>

### Considered but rejected
- <candidate pattern>: <why not — e.g., only 3 skills, below threshold>

### Notes
- <anything worth flagging for next cycle>
```

A "no changes" cycle is still a valid entry. Record it.

---

## Per-Chapter Update Policy

Different chapters have different volatility budgets. This table is load-bearing — the most common way to corrupt the book is to rewrite stable chapters because a single new skill seems exciting.

| Chapter | When to update | Who decides |
|---|---|---|
| **01 Philosophy** | Only when ≥3 top-ranked skills converge on a framing not captured by existing principles, OR a higher-downloaded skill has a better quote for an existing principle. **Never** based on one skill. | Human review required. |
| **02 Description** | Before/after examples can be swapped for higher-downloaded ones from the same category. Structural advice rarely changes. | Agent may auto-swap examples; structural edits need human review. |
| **03 Body** | Same as Chapter 2. | Same as Chapter 2. |
| **04 Patterns A–P** | Add a pattern when the 5+ skills threshold is met. Refresh frequency numbers every cycle. Swap exemplar skills when higher-downloaded ones appear. | Agent auto-refreshes frequencies; pattern adds/removes need human review. |
| **05 File Architecture** | Rarely. Only when the corpus shifts on a structural norm (e.g., "references/ usage drops from 20% to 5%"). | Human review. |
| **06 Top 1,000 Analysis** | Full refresh every cycle. This is the "living snapshot" chapter. | Agent may auto-commit the refreshed table. |
| **Source Catalog** | Fix broken citations every cycle. Add newly-cited skills as they appear in other chapter edits. | Agent may auto-commit link repairs. |

**Do not rewrite a chapter to rebalance it.** Chapters exist in their current shape because the data supported them. If new data arrives, the chapter's data tables update; its structure does not.

---

## Thresholds (Encoded in the Script)

These are the numeric boundaries above which the tool reports something as significant:

| Threshold | Value | Where it matters |
|---|---:|---|
| Frequency shift reporting | ±5 percentage points | Any smaller shift is noise. |
| Top-20 entry threshold | 20 | New entrants into top 20 are worth investigating; entering top 100 is not. |
| Pattern candidate minimum | 3 skills in top 20 | Below this, a "pattern" is single-author quirk. |
| Pattern addition minimum | 5 independent skills | The book-wide rule for inclusion. |

To change a threshold, edit `scripts/research.py::THRESHOLDS` and document the reason in a changelog entry. Thresholds should be stable across many cycles — frequent adjustment defeats their purpose.

---

## Cadence

| Trigger | Action |
|---|---|
| **Monthly** (calendar) | Run the full pipeline. |
| **A new skill enters top 5 by downloads** | Run immediately; the top 5 are reference-class. |
| **A cited skill gets deprecated, deleted, or renamed** | Run `research.py validate` immediately; fix the citation. |
| **ClawHub API changes shape** | Script health check required before any update (see below). |

Monthly is a ceiling, not a floor. Quarterly is fine if the reports show flat frequencies.

---

## Script Health Check

Before trusting the pipeline output, verify the ClawHub API hasn't silently changed its response shape:

```bash
python3 scripts/research.py fetch
# If the matched count drops to near-zero, the API likely changed.
# Compare one raw response:
curl -H "User-Agent: SkillDesignBook-research/1.0" \
  "https://clawhub.atomicbot.ai/api/skills?sort=downloads&dir=desc&limit=1" | python3 -m json.tool | head -30
```

If the response no longer matches the expected shape (missing `items`, missing `stats.downloads`, etc.), **stop and fix `scripts/research.py` before updating any book content.** A silent API drift that produces plausible-looking but wrong frequencies is the worst possible failure mode. Fix the script; the book can wait.

---

## How This Guide Updates Itself

The guide is versioned with the book and may need to evolve:

- **Thresholds need adjusting** → edit `scripts/research.py::THRESHOLDS`, then document the rationale in `research/changelog.md`.
- **New data source added** (e.g., another skill registry launches) → add a separate collector function in `scripts/research.py` and update this guide to reference it. Do not remove existing sources without migration — keep old snapshots valid.
- **Pattern detectors become stale** → the `PATTERN_DETECTORS` regex dict in the script must stay aligned with the patterns in `book/04-skill-patterns.md`. When a pattern is renamed, split, or merged in the book, update the detector in the same commit.
- **The inclusion bar needs to change** → this is a substantive shift in the book's philosophy. Human review, and a changelog entry explaining why.
- **This guide is wrong about something** → edit it. It's a skill; it should be refined as you learn.

One invariant: this guide and `scripts/research.py` must agree. If you change the thresholds here, change them in the script, or vice-versa. The guide is the spec; the script is the implementation. Skew between them is a bug.

---

## What NOT to Do

- **Don't rewrite philosophy based on a single new top skill.** Ch 1 principles require multi-skill convergence. One new skill with a catchy phrase is not evidence.
- **Don't delete a citation without a replacement.** If a cited skill dropped out, find another skill that makes the same point or rework the paragraph. Don't just remove the citation — that weakens the claim.
- **Don't rewrite chapters that only need data refreshed.** If the only thing that changed is a frequency number, update the number. Leave the prose alone.
- **Don't silently skip a data source on failure.** If the API is down or changed shape, stop the pipeline. Silent skips produce reports that look valid but aren't.
- **Don't add a pattern at 4 skills "because it feels important".** The threshold is 5. If you lower it once for a good reason, you'll lower it again for a worse reason.
- **Don't commit the report as a PR.** The report is a human decision aid, not a diff. Write the actual book edits as separate commits, citing the report date.
- **Don't bump thresholds to make an update easier.** If a pattern doesn't meet the threshold this cycle, maybe it will next cycle. If you move the bar, you're optimizing for a single change, not for the long-term health of the book.

---

## Rationalizations to Reject

| Rationalization | Reality |
|---|---|
| "This skill has 500K downloads, it must be a pattern" | Download count ≠ structural convergence. A pattern is a repeated *shape*, not a single popular file. |
| "Four skills use this section, close enough to five" | The threshold exists to resist noise. Lowering it destroys its purpose. |
| "The report is empty this cycle; I should find something to change" | A flat cycle is a valid cycle. Record it in the changelog and move on. |
| "Let me rewrite the philosophy based on this great new quote" | Philosophy requires multi-skill convergence. Add the quote as a candidate; wait for confirmation from later cycles. |
| "The API returned weird data, but the numbers look roughly right" | No. Stop and verify the API shape. Silently-wrong data corrupts the book permanently. |
| "This cycle I'll also fix the chapter structure" | Structure changes are out of scope for a data-refresh cycle. Propose structural changes in a separate PR with their own justification. |
| "I'll update the script later" | The script is the authoritative source of the numbers. Updating the book without updating the script creates skew. Do both, or neither. |
| "The regex didn't flag anything, so there's nothing new" | The regex only finds what it was taught. Always run the agentic step — skills invent patterns the detectors don't know about. That's the whole reason the worklist exists. |
| "The worklist is long; I'll skip the outliers section" | Outliers are where novel patterns hide. The top-20 rarely contains something unknown to the script because those skills have been seen before. Skip the outliers and you're running a regex-only pipeline. |
| "I'll commit the book edits directly from the findings file" | No. Findings → human review → commit. The agent doesn't commit book changes directly; it proposes them. |

---

## File Layout

```
SkillDesignBook/
├── book/                         # The book (mdBook source)
├── scripts/
│   ├── research.py               # Quantitative pipeline (fetch, analyze, compare, worklist, validate)
│   └── optimize-book.py          # Post-build CI optimizer (unrelated)
├── research/
│   ├── snapshots/<date>.json     # Raw data per cycle, for future diffs
│   ├── reports/<date>.md         # Quantitative report per cycle
│   ├── worklists/<date>.md       # Curated skills for the agent to read
│   ├── findings/<date>.md        # Agent's notes after reading the worklist
│   ├── candidates.md             # Patterns at 3–4 skills, tracked over time
│   └── changelog.md              # Update history
├── UPDATE_GUIDE.md               # This file
├── book.toml
└── README.md
```

## The Division of Labor

| Who | What they do | What they don't do |
|---|---|---|
| **Script** (`research.py`) | Count known patterns, detect top-20 changes, find broken citations, flag outliers, emit a worklist | Decide what's a new pattern, judge whether a citation still "makes the same point," rewrite any book content |
| **Agent** | Read worklist skills carefully, write findings file, propose book edits with evidence | Commit book edits directly, lower thresholds, rewrite philosophy chapters |
| **Human** | Review findings, approve or reject each proposed change, merge | Be consulted on every citation repair or stat refresh (those are auto-safe) |

---

## The Meta-Principle

This guide is opinionated, just like the skills the book teaches you to write. It picks defaults ("5 skills"), names failure modes ("staleness and churn"), refuses to be "neutral," and tells you what not to do. If you start making the guide more permissive — lowering thresholds, loosening the "what not to do" list, rewriting philosophy chapters casually — the book will drift into churn.

The discipline is the product.
