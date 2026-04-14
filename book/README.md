# The Skill Design Book

### How to Write SKILL.md — Philosophy, Methodology, and Practice from Top-Tier Skills

*April 2026*

Everything in this book was learned by inspecting production skills from OpenAI, Anthropic, Cursor, Manus, Devin, and leading open-source projects. Every principle links to the skill it was extracted from.

---

## Table of Contents

### Part I: Philosophy — What the Best Skills Teach Us
- [**Chapter 1: 10 Principles of Skill Design**](01-philosophy.md) — extracted by inspecting OpenAI's 9 SDK skills, their curated catalog, Osmani's 19 engineering skills, and Anthropic/Cursor/Devin/Manus system prompts

### Part II: Methodology — How to Write Each Part
- [**Chapter 2: Writing the Description**](02-writing-the-description.md) — the 1-1024 char routing boundary, 6 production descriptions dissected component-by-component, before/after rewrites, testing methodology
- [**Chapter 3: Writing the Body**](03-writing-the-body.md) — section ordering, imperative style, input collection with exact commands, 3 decision tree patterns, output templates, approval gates, verification steps, constraint language, anti-patterns, complete body template
- [**Chapter 4: Skill Patterns**](04-skill-patterns.md) — 8 structural archetypes from production (Gate-keeper, Report-first, Decision gate, Think-before-act, Handoff automation, Debug-and-fix, Multi-axis review, Prompt augmentation), each with exemplar skill, structural analysis, and reusable template
- [**Chapter 5: File Architecture and Testing**](05-file-architecture-and-testing.md) — directory structure, scripts (when/how), reference files (when/how), cross-platform paths, AGENTS.md integration, 4-step testing methodology, authoring checklist

### Reference
- [**Source Catalog**](14-source-catalog.md) — 100+ hyperlinked references to every primary source

---

## Reading Paths

**"I want to write my first skill":**
Ch 1 (principles) → Ch 2 (description) → Ch 3 (body) → Ch 4 (pick a pattern) → Ch 5 (file structure + checklist)

**"I want to understand the philosophy":**
Ch 1 (all 10 principles with production evidence)

**"I want to see what real skills look like":**
Every chapter links to the full text of the production skills it analyzes. Start with Ch 4 (patterns) for the broadest view.

**"I want to look up a specific source":**
[Source Catalog](14-source-catalog.md) — organized by company, topic, and type

---

## Production Skills Referenced

| Skill | Author | Pattern | Full Text |
|-------|--------|---------|-----------|
| `code-change-verification` | OpenAI | Gate-keeper | [source](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification) |
| `implementation-strategy` | OpenAI | Think-before-act | [source](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) |
| `final-release-review` | OpenAI | Decision gate | [source](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md) |
| `docs-sync` | OpenAI | Report-first | [source](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md) |
| `test-coverage-improver` | OpenAI | Report-first | [source](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md) |
| `pr-draft-summary` | OpenAI | Handoff automation | [source](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md) |
| `gh-fix-ci` | OpenAI | Debug-and-fix | [source](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md) |
| `imagegen` | OpenAI | Prompt augmentation | [source](https://github.com/openai/skills/blob/main/skills/.curated/imagegen/SKILL.md) |
| `runtime-behavior-probe` | OpenAI | Empirical probe | [source](https://github.com/openai/openai-agents-python/blob/main/.agents/skills/runtime-behavior-probe/SKILL.md) |
| `code-review-and-quality` | Addy Osmani | Multi-axis review | [source](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) |
