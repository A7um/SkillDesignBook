# The Skill Design Book

### Designing Skills for Long-Running AI Agents That Tackle Hard Tasks

**A comprehensive guide to the state-of-the-art in agent skill design, drawing from OpenAI, Anthropic, Google, Cursor, Manus, Devin, top open-source frameworks, and leading research labs.**

*April 2026*

---

## Table of Contents

### Preface
- [Preface — Who This Book Is For](00-preface.md)

### Part I: Foundations
- [Chapter 1: The Skill Layer — Why Agents Need More Than Prompts and Tools](01-the-skill-layer.md)
- [Chapter 2: Anatomy of a Skill — The SKILL.md Specification](02-anatomy-of-a-skill.md)

### Part II: Design Principles
- [Chapter 3: Progressive Disclosure — The Architecture of Attention](03-progressive-disclosure.md)
- [Chapter 4: Activation Accuracy — Getting the Right Skill at the Right Time](04-activation-and-routing.md)
- [Chapter 5: Context Engineering for Skills — Managing the Scarcest Resource](05-context-engineering.md)

### Part III: Industry Practice
- [Chapter 6: Industry Practice — How the Leaders Design Skills](06-industry-practice.md)
  - 6.1 OpenAI · 6.2 Anthropic · 6.3 Google · 6.4 Cursor · 6.5 Devin · 6.6 Manus
- [**Chapter 6A: Deep Dive — Anatomy of Top-Tier Production Skills**](06a-deep-dive-production-skills.md)
  - 6A.1 OpenAI's "Tiny CLI" Skills · 6A.2 Media Production Pattern · 6A.3 Anthropic's ACI · 6A.4 Cursor's Dynamic Context · 6A.5 Manus's Event Loop · 6A.6 Devin's Planning Mode · 6A.7 Osmani's Lifecycle Skills · 6A.8 Gechev's Validation

### Part IV: Patterns for Hard Tasks
- [Chapter 7: Error Recovery and Resilience](07-error-recovery-and-resilience.md)
- [Chapter 8: Memory and Learning](08-memory-and-learning.md)
- [Chapter 9: Multi-Agent Composition](09-multi-agent-composition.md)
- [Chapter 10: Security](10-security.md)

### Part V: Evaluation and the Future
- [Chapter 11: Evaluation and Benchmarks](11-evaluation-and-benchmarks.md)
- [Chapter 12: Open Problems and the Research Frontier](12-open-problems.md)

### Part VI: Practice
- [**Chapter 15: Practitioner's Handbook — Real Patterns with Real Code**](15-practitioners-handbook.md)
  - 15.1 OpenAI `implementation-strategy` — complete annotated text
  - 15.2 OpenAI `final-release-review` — deterministic gate policy
  - 15.3 Osmani `code-review-and-quality` — 5-axis review with labels
  - 15.4 Manus event-driven agent loop — full architecture
  - 15.5 Devin two-mode system — planning vs. execution
  - 15.6 Cursor dynamic context discovery — 4 techniques
  - 15.7 Anthropic tool design checklist — build/define/validate
  - 15.8 Skill validation methodology — 4-step with prompts
  - 15.9 Cross-platform skill installation commands
  - 15.10 Writing your first production skill — step by step

### Appendices
- [Appendix A–E: Checklists, Examples, Platform Guide, Glossary, Reading List](13-appendix.md)
- [**Source Catalog — Hyperlinked References for Every Topic**](14-source-catalog.md)
  - Official Specs · OpenAI (16 links) · Anthropic (10 links) · Google (4 links) · Cursor (7 links) · Devin (6 links) · Manus (6 links) · Frameworks (5 links) · Community Libraries (4 links) · Academic Papers (11 links) · Security Research (5 links) · Design Patterns (10 links) · Benchmarks (4 links) · CLAUDE.md Practices (5 links)

---

## Quick Start

**If you want to understand the theory first**: Ch 1 → Ch 3 → Ch 5

**If you want production patterns immediately**: Ch 15 (Practitioner's Handbook) → Ch 6A (Deep Dives)

**If you want to look up a specific source**: [Source Catalog](14-source-catalog.md)

---

## Sources

This book synthesizes research and production practice from:

| Source | What We Drew From |
|--------|------------------|
| **OpenAI** (Codex, Agents SDK) | 9 production skills dissected with full text, AGENTS.md, shell+skills+compaction |
| **Anthropic** (Claude Code, MCP) | ACI tool design, context engineering, 5 tool principles, subagent architecture |
| **Google** (ADK, A2A, Gemini CLI) | Multi-agent orchestration, agent cards, A2A protocol |
| **Cursor** | Dynamic context discovery, Priompt, self-driving codebases research |
| **Manus / Meta** | Leaked system prompt, event-driven agent loop, sandbox execution |
| **Devin / Cognition** | Leaked prompt, two-mode architecture, managed Devins, Sonnet 4.5 rebuild |
| **LangGraph / LangChain** | Graph-based orchestration, tools-first pattern, checkpointing |
| **CrewAI** | Role-based agents, rapid prototyping, pipeline design |
| **Community** | addyosmani/agent-skills (5K★), VoltAgent (15K★), mgechev (1.8K★) |
| **Academic** | 20+ papers from NeurIPS, ACL, arXiv |
| **Security** | OWASP AST10, Snyk ToxicSkills, ClawHavoc |
