# SkillDesignBook

**The Skill Design Book**: A comprehensive guide to designing skills for long-running AI agents that tackle hard tasks.

This book covers the state-of-the-art in agent skill design philosophy, methodology, and practice from top-tier AI companies (OpenAI, Anthropic, Google, Cursor, Manus/Meta, Devin/Cognition), leading open-source frameworks (LangGraph, CrewAI, AutoGen), and academic research labs.

## Read the Book

Start here: **[book/README.md](book/README.md)**

## What You'll Learn

- The **three-layer architecture** (system prompts → skills → tools) that all major platforms have converged on
- **Progressive disclosure**: how to scale agent capabilities within fixed context budgets
- **Activation accuracy**: writing descriptions that route tasks to the right skill every time
- **Context engineering**: managing the scarcest resource in agent design
- How **OpenAI, Anthropic, Google, Cursor, Manus, and Devin** each approach skill design
- **Error recovery patterns** for skills that survive failure in long-horizon tasks
- **Memory and learning**: building skills that improve over time
- **Multi-agent composition**: orchestrating skills across subagents and services
- **Security**: defending against the emerging supply chain attacks on skill ecosystems
- **Evaluation**: measuring skill quality with benchmarks and production metrics

## Who This Book Is For

Engineers, technical leads, and AI practitioners who design skills for autonomous agents that must plan, execute, recover from errors, and deliver results over extended time horizons.

## Structure

```
book/
├── README.md                          # Table of Contents
├── 00-preface.md                      # Preface
├── 01-the-skill-layer.md              # Part I: Foundations
├── 02-anatomy-of-a-skill.md
├── 03-progressive-disclosure.md       # Part II: Design Principles
├── 04-activation-and-routing.md
├── 05-context-engineering.md
├── 06-industry-practice.md            # Part III: Industry Practice
├── 06a-deep-dive-production-skills.md # Deep Dive: actual production skills dissected
├── 07-error-recovery-and-resilience.md # Part IV: Patterns for Hard Tasks
├── 08-memory-and-learning.md
├── 09-multi-agent-composition.md
├── 10-security.md
├── 11-evaluation-and-benchmarks.md    # Part V: Evaluation & Future
├── 12-open-problems.md
├── 13-appendix.md                     # Appendices A-E
├── 14-source-catalog.md               # Hyperlinked references (100+ links)
└── 15-practitioners-handbook.md       # Real production patterns with real code
```
