# The Skill Design Book

### How to Write SKILL.md Files for Long-Running AI Agents That Tackle Hard Tasks

*April 2026*

---

## Table of Contents

### Preface
- [Preface — Who This Book Is For](00-preface.md)

### Part I: Foundations — What Skills Are
- [Chapter 1: The Skill Layer — Why Agents Need More Than Prompts and Tools](01-the-skill-layer.md)
- [Chapter 2: Anatomy of a Skill — The SKILL.md Specification](02-anatomy-of-a-skill.md)

### Part II: The Craft of Writing SKILL.md *(core of the book)*
- [**Chapter 20: Writing the Description** — The Most Important Line in Your Skill](20-writing-the-description.md)
  - The three questions · Production description anatomy · Before/after examples · Skip condition pattern · Testing your description · Rules of thumb
- [**Chapter 21: Writing the Body** — Instruction Craft for LLMs](21-writing-the-body.md)
  - Section ordering (primacy/recency) · Imperative style · Quick Start pattern · Decision trees (if/then, matrices, surface categories) · Input/output contracts · Report-first-act-after-approval · Scripts vs prose · Constraint writing (ALWAYS/NEVER) · Line budget · Anti-patterns · Body template
- [**Chapter 22: Skill Patterns** — Archetypes from Production](22-skill-patterns.md)
  - 9 patterns with real production code: Gate-keeper · Report-first · Decision gate · Think-before-act · Handoff automation · Debug-and-fix · Multi-axis review · Prompt augmentation · Empirical probe · Pattern selection guide

### Part III: How the Industry Writes Skills
- [Chapter 6: Industry Practice — How the Leaders Design Skills](06-industry-practice.md)
- [Chapter 6A: Deep Dive — Anatomy of Top-Tier Production Skills](06a-deep-dive-production-skills.md)
  - OpenAI's skills dissected · Anthropic's ACI tool design · Cursor's dynamic context · Manus's event loop · Devin's planning mode · Community skills

### Part IV: Advanced Topics
- [Chapter 3: Progressive Disclosure — Token Efficiency for Skill Authors](03-progressive-disclosure.md)
- [Chapter 4: Activation Accuracy — Getting the Right Skill at the Right Time](04-activation-and-routing.md)
- [Chapter 5: Context Engineering for Skills](05-context-engineering.md)
- [Chapter 7: Error Recovery and Resilience](07-error-recovery-and-resilience.md)
- [Chapter 8: Memory and Learning](08-memory-and-learning.md)
- [Chapter 9: Multi-Agent Composition](09-multi-agent-composition.md)
- [Chapter 10: Security](10-security.md)
- [Chapter 11: Evaluation and Benchmarks](11-evaluation-and-benchmarks.md)
- [Chapter 12: Open Problems](12-open-problems.md)

### Part V: Reference
- [Chapter 15: Practitioner's Handbook — Full Annotated Production Skills](15-practitioners-handbook.md)
- [Appendix A–E: Checklists, Examples, Platform Guide, Glossary](13-appendix.md)
- [**Source Catalog — 100+ Hyperlinked References**](14-source-catalog.md)

---

## Quick Start

**"I want to write my first SKILL.md":**
→ Ch 20 (description) → Ch 21 (body) → Ch 22 (pick a pattern) → Appendix A (checklist)

**"I want to see what production skills look like":**
→ Ch 15 (full annotated texts) → Ch 6A (deep dives)

**"I want to look up a source":**
→ [Source Catalog](14-source-catalog.md)

---

## What's in Each Core Chapter

| Chapter | What You'll Learn | Lines of Real Code |
|---------|------------------|--------------------|
| **Ch 20: Writing the Description** | How to write the 1-1024 char routing boundary. Before/after examples. Testing methodology. | 6 production descriptions annotated |
| **Ch 21: Writing the Body** | Section ordering, imperative style, decision trees, I/O contracts, output templates, script integration. | 15+ code blocks from OpenAI, Anthropic, Osmani |
| **Ch 22: Skill Patterns** | 9 structural archetypes. When to use each. Templates for each. | 9 production skills as pattern exemplars |
| **Ch 15: Practitioner's Handbook** | Full unabridged production skills with line-by-line annotations. | 5 complete skills (500+ lines) |

## Sources

Every claim links to a primary source. See the [Source Catalog](14-source-catalog.md) for 100+ hyperlinked references organized by: Official Specs · OpenAI (16 links) · Anthropic (10) · Google (4) · Cursor (7) · Devin (6) · Manus (6) · Frameworks (5) · Community (4) · Papers (11) · Security (5) · Patterns (10) · Benchmarks (4).
