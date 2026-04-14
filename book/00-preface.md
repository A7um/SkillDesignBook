# Preface

## Who This Book Is For

This book is for engineers, technical leads, and AI practitioners who design **skills for long-running AI agents that tackle hard, multi-step tasks**. If you are building autonomous systems that must plan, execute, recover from errors, and deliver results over extended horizons—hours, not seconds—this book is your field guide.

You will not find toy examples here. Every principle, pattern, and case study is drawn from production systems at companies shipping agent products to millions of users: OpenAI's Codex, Anthropic's Claude Code, Google's Agent Development Kit, Cursor, Manus (now Meta), Devin, and the leading open-source frameworks (LangGraph, CrewAI, AutoGen). Where production details are not public, we draw on the best available academic research from labs at Princeton, Stanford, NeurIPS, and ACL.

## What "Skill Design" Means

A **skill** is a reusable unit of procedural knowledge that an AI agent can discover, load, execute, and retire. Skills are not prompts. They are not tools. They sit between the two:

| Layer | What It Does | Persistence |
|-------|-------------|-------------|
| **System prompt** | Global behavioral constraints | Always loaded |
| **Skill** | Procedural workflow for a specific task | Loaded on demand |
| **Tool** | Atomic capability (read file, call API) | Always available |

Prompts define *who the agent is*. Tools define *what the agent can do*. Skills define *how the agent should work*—the step-by-step procedures, branching logic, validation criteria, and domain expertise that turn a capable model into a reliable specialist.

The formalization of this layer—first by Anthropic in October 2025, then as an open standard adopted across the industry by early 2026—represents the most significant architectural shift in applied AI since the introduction of tool use.

## How This Book Is Organized

The book progresses from foundations to advanced practice:

- **Part I: Foundations** covers the conceptual framework, the anatomy of skills, and the open standard that unifies them.
- **Part II: Design Principles** dives into the core engineering principles: progressive disclosure, context engineering, activation accuracy, and composability.
- **Part III: Industry Practice** examines how each major player designs skills, with architecture diagrams and concrete examples.
- **Part IV: Patterns for Hard Tasks** addresses the patterns that matter most for long-horizon agents: error recovery, memory, multi-agent coordination, and security.
- **Part V: Evaluation and the Future** covers benchmarks, testing, and the open research frontier.

Each chapter ends with actionable takeaways. The Appendix includes a complete skill authoring checklist and reference implementations.

## A Note on Timing

This book is written as of April 2026. The Agent Skills open standard is less than six months old. Production systems are evolving weekly. The principles in this book—progressive disclosure, context as currency, activation accuracy, composability—are durable. The specific APIs and tool names will change. Read for the architecture, not the syntax.

---

*"The best way to predict the future is to build it, and the best way to build agents is to give them the right skills at the right time."*
