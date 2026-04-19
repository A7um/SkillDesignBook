# The Skill Design Book

**How to Write SKILL.md** — philosophy, methodology, and patterns extracted empirically from the **top 1,000 most-downloaded skills on ClawHub** (12.5M total downloads).

---

## What This Book Is

A practical, data-backed guide to writing SKILL.md files for long-running AI agents. Every principle and pattern in this book is grounded in direct analysis of production skills from:

- **OpenAI** — 14 skills (Agents SDK + curated catalog)
- **Anthropic, Vercel, Stripe, Sentry, Trail of Bits** — 18 official company skills
- **Addy Osmani** — 19 lifecycle engineering skills
- **ClawHub community** — top 1,000 by download (12.5M downloads, 990 matched SKILL.md files, 889 analyzed scripts)
- **Full corpus** — 58,593 skills analyzed programmatically

## How It's Organized

**Part I — Philosophy** opens the book with 10 design principles mined from the skills' own "Core Philosophy" / "Core Principle" sections, plus their explicit "Never..." / "Treat X as Y, not Z" / "Not a..." declarations. Every principle is quoted directly from specific top skills.

**Part II — Methodology** walks through the craft of writing each part of a SKILL.md file: the description (the routing boundary), the body (section ordering, instruction style, decision trees, output templates, scripts vs prose, constraint language), skill patterns (16 structural archetypes A–P discovered from corpus analysis), and file architecture (directory structure, scripts, references, testing).

**Part III — Empirical Analysis** presents the data: top 20 downloaded skills, aggregate statistics, pattern frequency in the top 1,000 vs the full corpus, script analysis (Python 56%, Bash 32%, JS/TS 12%), and a case study of `self-improving-agent` (398K downloads — the #1 skill on ClawHub).

**Reference** — a source catalog with 110+ hyperlinked references to every skill, blog post, and paper cited.

## Reading Paths

- **"I want to write my first skill"** → Chapter 1 (philosophy) → Chapter 2 (description) → Chapter 3 (body) → Chapter 4 (pick a pattern) → Chapter 5 (files and testing)
- **"I want to understand the design principles"** → Chapter 1 only
- **"I want to see patterns from real skills"** → Chapter 4 (patterns A–P) + Chapter 6 (data analysis)
- **"I want to look up a specific skill"** → [Source Catalog](14-source-catalog.md)

## The Meta-Principle

> A skill is not documentation. Documentation describes what something is; a skill makes claims. It asserts defaults, rejects alternatives, names failure modes, and corrects the model's mental model. The top-ranked skills are opinionated — the ranking rewards that.

---

*By [Atum](https://atum.li) — Source: [github.com/A7um/SkillDesignBook](https://github.com/A7um/SkillDesignBook)*
