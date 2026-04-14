# SkillDesignBook

**How to Write SKILL.md Files for Long-Running AI Agents That Tackle Hard Tasks**

A deeply practical guide on writing agent skills, centered on the *craft* of authoring SKILL.md files. Drawn from production skills at OpenAI, Anthropic, Google, Cursor, Manus/Meta, Devin/Cognition, and leading open-source projects.

## Read the Book

Start here: **[book/README.md](book/README.md)**

## Core Content (Start Here)

| Chapter | What It Covers |
|---------|---------------|
| [**Ch 20: Writing the Description**](book/20-writing-the-description.md) | The 1-1024 char routing boundary. Before/after examples. Testing methodology. Production descriptions annotated. |
| [**Ch 21: Writing the Body**](book/21-writing-the-body.md) | Section ordering, imperative style, decision trees, I/O contracts, output templates, scripts vs. prose, constraint writing, anti-patterns. |
| [**Ch 22: Skill Patterns**](book/22-skill-patterns.md) | 9 structural archetypes from production: Gate-keeper, Report-first, Decision gate, Think-before-act, Handoff automation, Debug-and-fix, Multi-axis review, Prompt augmentation, Empirical probe. |
| [**Ch 15: Practitioner's Handbook**](book/15-practitioners-handbook.md) | Full unabridged production skills with line-by-line annotations. |

## Also Included

- Foundations (Ch 1-2): What skills are, the SKILL.md spec
- Industry deep dives (Ch 6, 6A): How OpenAI/Anthropic/Cursor/Manus/Devin write skills
- Advanced topics (Ch 3-5, 7-12): Progressive disclosure, context engineering, error recovery, memory, security, evaluation
- [Source Catalog](book/14-source-catalog.md): 100+ hyperlinked references

## Structure

```
book/
├── README.md                          # Table of Contents
│
│  ── CORE: How to Write SKILL.md ──
├── 20-writing-the-description.md      # Description engineering with before/after
├── 21-writing-the-body.md             # Body craft: ordering, style, trees, I/O, scripts
├── 22-skill-patterns.md               # 9 archetypes from production
├── 15-practitioners-handbook.md       # Full annotated production skills
│
│  ── FOUNDATIONS ──
├── 00-preface.md
├── 01-the-skill-layer.md
├── 02-anatomy-of-a-skill.md
│
│  ── INDUSTRY PRACTICE ──
├── 06-industry-practice.md
├── 06a-deep-dive-production-skills.md
│
│  ── ADVANCED TOPICS ──
├── 03-progressive-disclosure.md
├── 04-activation-and-routing.md
├── 05-context-engineering.md
├── 07-error-recovery-and-resilience.md
├── 08-memory-and-learning.md
├── 09-multi-agent-composition.md
├── 10-security.md
├── 11-evaluation-and-benchmarks.md
├── 12-open-problems.md
│
│  ── REFERENCE ──
├── 13-appendix.md                     # Checklists, examples, platform guide, glossary
└── 14-source-catalog.md               # 100+ hyperlinked references
```
