# Agent findings

After the worklist is generated, an agent reads each listed skill and writes findings here.

One file per cycle, named `<YYYY-MM-DD>.md`. Format:

```markdown
# Findings — YYYY-MM-DD

## Skills read
- `<slug>` — one-line note on what the reading revealed
- `<slug>` — one-line note

## Proposed book changes
### `book/04-skill-patterns.md`
- Add pattern "X" — appears in 5+ skills: [a], [b], [c], [d], [e]. Evidence: [quotes]
- Swap exemplar for Pattern B: `<old>` → `<new>` (higher downloads, same structure)

### `book/01-philosophy.md`
- (rarely updated; multi-skill convergence required)

## Proposed `research/candidates.md` additions
- Pattern "Y" — 4 skills in top 20: [a], [b], [c], [d]. Track next cycle.

## Broken citations fixed
- `book/04-skill-patterns.md` line N: `<old>` → `<new>` (same point, current skill)

## Non-findings (for the changelog)
- Nothing rose to book-worthy this cycle; all findings below threshold.
```

Human review happens after this file is written. The agent doesn't commit book changes directly — it writes findings, a human reviews, then the actual edits happen.
