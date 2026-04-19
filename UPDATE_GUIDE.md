# SkillDesignBook — Update Guide

> This guide is itself a skill. It follows the book's own principles: opinionated stance, named failure modes, explicit thresholds, and scripts that do the real work. If you find yourself about to violate one of the rules below, the guide is probably right and you're probably being tempted by a rationalization. Re-read the Rationalizations table at the bottom first.

---

## Why This Guide Exists

The book is grounded in measurements: "Pattern X appears in N% of the top-1,000 downloaded skills." Those numbers go stale. Skills drop out of the top 1,000. Citations break. New structural patterns emerge.

This guide exists to prevent **two failure modes**:

- **Staleness** — the book keeps claiming frequency numbers that no longer match reality, cites skills that no longer rank, or misses patterns that have become universal.
- **Churn** — the book gets rewritten every cycle to match the latest top-1 skill, losing the stable principles that were already well-founded.

Staleness erodes credibility. Churn destroys structure. This guide produces changes only when the evidence demands them.

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
# One command; does the whole cycle.
python3 scripts/research.py
```

This fetches the top 1,000 from the ClawHub API, analyzes pattern frequencies against the repo-local skill corpus, diffs against the previous snapshot, validates citations in `book/`, and writes a structured report to `research/reports/<date>.md`.

No changes to the book happen automatically. The report tells you what changed; you decide what to edit.

### Subcommands if you need them

| Command | What it does |
|---|---|
| `research.py fetch` | Snapshot the top 1,000 to `research/snapshots/<date>.json` |
| `research.py analyze` | Print pattern frequencies from the latest snapshot |
| `research.py compare` | Diff the two most recent snapshots, print a report |
| `research.py validate` | List book citations that no longer resolve |
| `research.py` (default) | Run the full pipeline and write a dated report |

---

## Workflow

### 1. Run the pipeline

```bash
python3 scripts/research.py
```

If the SKILL.md corpus isn't cloned locally, clone it once:

```bash
git clone --depth 1 https://github.com/openclaw/skills.git /tmp/clawhub-skills
```

The pipeline looks for SKILL.md files under the path in `$SKILLS_REPO` (defaults to `/tmp/clawhub-skills/skills`). It tolerates missing files — unmatched skills are counted but not pattern-analyzed.

### 2. Read the report

The report has five sections. Act on each in order:

- **Frequency shifts exceeding threshold** → update the numbers in `book/04-skill-patterns.md` and `book/06-top1000-analysis.md`. No other chapters change for this.
- **New entrants into top 20** → scan their SKILL.md files. If their structure uses a pattern the book doesn't name, that's a candidate for Chapter 4. If their structure uses an existing pattern differently, that's a candidate exemplar swap.
- **Pattern candidates** (3–4 hits, not yet at threshold) → append to `research/candidates.md` so you can see which ones are rising over multiple cycles. Do NOT add to the book yet.
- **Broken citations** → fix in place. Either replace with a skill that still ranks and makes the same point, or drop the citation if no replacement exists.
- **Dropped from top 1,000** → only matters if the dropped skills are currently cited. If yes, treat as broken citations.

### 3. Run the pre-flight landscape check

Before touching `book/`, answer these three questions:

1. **Has a new pattern genuinely emerged?** Multi-skill convergence only. Single high-downloaded skills don't count.
2. **Does Chapter 1 (Philosophy) still hold?** Pick two principles and check: are the cited skills still reference-class? Are their quoted lines still intact? If a principle's evidence has eroded, flag for human review — do not auto-edit Chapter 1.
3. **Is Chapter 4's pattern list still complete?** If the report shows a pattern hitting 5+ skills that's not in Chapter 4, the chapter is incomplete. Propose an addition.

### 4. Make the changes

See the per-chapter policy below.

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

---

## File Layout

```
SkillDesignBook/
├── book/                         # The book (mdBook source)
├── scripts/
│   ├── research.py               # Update pipeline — fetch, analyze, compare, validate
│   └── optimize-book.py          # Post-build CI optimizer (unrelated)
├── research/
│   ├── snapshots/<date>.json     # Raw data per cycle, for future diffs
│   ├── reports/<date>.md         # Human-readable report per cycle
│   ├── candidates.md             # Patterns at 3–4 skills, tracked over time
│   └── changelog.md              # Update history
├── UPDATE_GUIDE.md               # This file
├── book.toml
└── README.md
```

---

## The Meta-Principle

This guide is opinionated, just like the skills the book teaches you to write. It picks defaults ("5 skills"), names failure modes ("staleness and churn"), refuses to be "neutral," and tells you what not to do. If you start making the guide more permissive — lowering thresholds, loosening the "what not to do" list, rewriting philosophy chapters casually — the book will drift into churn.

The discipline is the product.
