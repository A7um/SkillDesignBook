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
  - 6.1 OpenAI: Skills as Reusable Procedures
  - 6.2 Anthropic: Context Engineering and the Agent-Computer Interface
  - 6.3 Google: Multi-Agent Systems and the A2A Protocol
  - 6.4 Cursor: The IDE as Agent Harness
  - 6.5 Devin (Cognition): The Planner-Critic Architecture
  - 6.6 Manus (Meta): Skills in the Sandbox
- [Chapter 6A: Deep Dive — Anatomy of Top-Tier Production Skills](06a-deep-dive-production-skills.md)
  - 6A.1 OpenAI's Agents SDK Skills: The "Tiny CLI" Philosophy
  - 6A.2 OpenAI's Curated Skills: The Media Production Pattern
  - 6A.3 Anthropic's Philosophy: The Agent-Computer Interface (ACI)
  - 6A.4 Cursor's Philosophy: Dynamic Context Discovery
  - 6A.5 Manus's Philosophy: The Event-Driven Agent Loop
  - 6A.6 Devin's Philosophy: Planning Mode and Confidence
  - 6A.7 Addy Osmani's Engineering Skills: Process Over Prose
  - 6A.8 The `skills-best-practices` Meta-Skill

### Part IV: Patterns for Hard Tasks
- [Chapter 7: Error Recovery and Resilience — Skills That Survive Failure](07-error-recovery-and-resilience.md)
- [Chapter 8: Memory and Learning — Skills That Improve Over Time](08-memory-and-learning.md)
- [Chapter 9: Multi-Agent Composition — Skills That Orchestrate](09-multi-agent-composition.md)
- [Chapter 10: Security — The Supply Chain Risk You Can't Ignore](10-security.md)

### Part V: Evaluation and the Future
- [Chapter 11: Evaluation and Benchmarks — Measuring What Matters](11-evaluation-and-benchmarks.md)
- [Chapter 12: Open Problems and the Research Frontier](12-open-problems.md)

### Appendices
- [Appendix A: Skill Authoring Checklist](13-appendix.md#appendix-a-skill-authoring-checklist)
- [Appendix B: Reference Skill Examples](13-appendix.md#appendix-b-reference-skill-examples)
- [Appendix C: Platform Quick Reference](13-appendix.md#appendix-c-platform-quick-reference)
- [Appendix D: Glossary](13-appendix.md#appendix-d-glossary)
- [Appendix E: Further Reading](13-appendix.md#appendix-e-further-reading)

---

## Quick Start

If you're short on time, read these chapters first:
1. **Chapter 1** for the conceptual foundation
2. **Chapter 2** for the practical format
3. **Chapter 3** for the most important design principle
4. **Chapter 6A** for deep dives into actual production skills with code
5. **Appendix A** for the authoring checklist

## Sources

This book synthesizes research and production practice from:

| Source | What We Drew From |
|--------|------------------|
| **OpenAI** (Codex, Agents SDK) | SKILL.md format, AGENTS.md patterns, routing design, shell+skills+compaction |
| **Anthropic** (Claude Code, MCP) | Context engineering, progressive disclosure, subagent isolation, tool design |
| **Google** (ADK, A2A, Gemini CLI) | Multi-agent orchestration, agent cards, A2A protocol |
| **Cursor** | IDE-as-harness, rules vs. skills separation, cloud agents |
| **Manus / Meta** | Sandbox execution, auto-skill generation, five-layer architecture |
| **Devin / Cognition** | Planner-critic loop, large-context ingestion, self-healing test loops |
| **LangGraph / LangChain** | Graph-based orchestration, tools-first pattern, checkpointing |
| **CrewAI** | Role-based agents, rapid prototyping, pipeline design |
| **Agent Skills Standard** | Open specification (agentskills.io) |
| **Academic Research** | SoK surveys, PALADIN, Memento-Skills, VIGIL, SWE-bench, METR |
| **OWASP** | Agentic Skills Top 10 security risks |
| **Snyk** | ToxicSkills supply chain audit |

## License

This work is provided as-is for educational purposes.
