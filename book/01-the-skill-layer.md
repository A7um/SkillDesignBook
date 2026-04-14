# Chapter 1: The Skill Layer — Why Agents Need More Than Prompts and Tools

## 1.1 From Prompt Engineering to Context Engineering

For the first two years of the LLM era (2023–2024), the dominant practice was **prompt engineering**: crafting the right words and phrases to elicit desired model behavior. Teams poured effort into system prompts, few-shot examples, and chain-of-thought instructions. The results were impressive for single-turn tasks but brittle for anything requiring sustained, multi-step execution.

By mid-2025, a new term gained prominence: **context engineering**. Popularized by Shopify CEO Tobi Lütke and endorsed by Andrej Karpathy, context engineering refers to the broader discipline of curating the *entire information environment* an AI agent operates within—not just the prompt, but the tools, retrieved documents, conversation history, memory state, and procedural knowledge.

Anthropic's September 2025 engineering blog crystallized the shift:

> "Building with language models is becoming less about finding the right words and phrases for your prompt and more about answering the question: What configuration of context is most likely to generate our model's desired behavior?"

This reframing—from *writing prompts* to *curating context*—is the conceptual foundation of skill design.

## 1.2 The Three-Layer Architecture

Modern agent systems operate across three distinct layers, each with different characteristics:

```
┌─────────────────────────────────────────────────────┐
│  SYSTEM PROMPT                                       │
│  Always loaded. Global behavior. ~2-10K tokens.      │
│  "You are a careful engineer. Follow conventions."   │
├─────────────────────────────────────────────────────┤
│  SKILLS                                              │
│  Loaded on demand. Procedural workflows.             │
│  "When deploying, run tests, then lint, then..."     │
├─────────────────────────────────────────────────────┤
│  TOOLS                                               │
│  Always available. Atomic capabilities.              │
│  read_file(), run_shell(), search_web()              │
└─────────────────────────────────────────────────────┘
```

**System prompts** are always-on behavioral constraints. They define personality, safety guardrails, and universal conventions. They should be small, stable, and high-signal.

**Tools** are atomic capabilities—individual functions the agent can call. A tool reads a file, executes a shell command, or calls an API. Tools have strict input/output schemas and are stateless.

**Skills** occupy the middle layer. They are *procedural*—they encode multi-step workflows with branching logic, validation criteria, and domain expertise. Unlike system prompts, skills load only when relevant. Unlike tools, skills carry rich natural-language instructions that guide the agent through complex processes.

This three-layer separation is not merely organizational. It is an architectural response to a fundamental constraint: the context window is finite, and performance degrades as it fills.

## 1.3 The Formalization of Skills

The concept of "teaching agents procedures" existed informally before 2025—in long system prompts, in RAG pipelines that retrieved relevant documentation, and in manually-crafted tool descriptions. What changed was the **formalization** into a portable, versioned, discoverable standard.

The timeline:

| Date | Event |
|------|-------|
| **Oct 2025** | Anthropic launches Agent Skills in Claude Code |
| **Dec 2025** | Agent Skills released as open standard at agentskills.io |
| **Jan 2026** | Manus AI fully integrates Agent Skills |
| **Jan 2026** | Cursor 2.4 ships Skills support |
| **Feb 2026** | OpenAI Codex adopts SKILL.md format |
| **Feb 2026** | Devin adds Skills support |
| **Mar 2026** | Google Gemini CLI adds Skills support |
| **Apr 2026** | OWASP publishes Agentic Skills Top 10 security risks |

By April 2026, the same skill file works across Claude Code, Cursor, Codex, Gemini CLI, Devin, Manus, and Junie—a level of interoperability unprecedented in AI tooling.

## 1.4 Skills as the Missing Middle

The reason skills matter is not abstraction for its own sake. They solve three concrete problems that neither prompts nor tools address:

### Problem 1: Context Bloat
Long system prompts filled with procedural instructions waste tokens on every turn, even when 90% of the procedures are irrelevant to the current task. Skills solve this with **progressive disclosure**: only metadata loads at startup; full instructions load on activation.

### Problem 2: Drift
When procedures live in system prompts, they drift as teams copy-paste and modify them across projects. Skills are **version-controlled files** that travel with the repository, can be code-reviewed, and evolve alongside the codebase they serve.

### Problem 3: Reusability
A deployment procedure hardcoded into a system prompt cannot be shared across agents, teams, or platforms. Skills are **portable packages** that work identically across any compliant agent.

## 1.5 The Formal Definition

Drawing on the academic systematization by Jiang et al. (2026, "SoK: Agentic Skills"), we can define a skill formally:

> **S = (C, π, T, R)**
>
> Where:
> - **C** = applicability conditions (when the skill should trigger)
> - **π** = policy (the procedural instructions)
> - **T** = tool requirements (which tools the skill needs)
> - **R** = success criteria (how to know the skill completed correctly)

This formalization captures what production systems have converged on: a skill must specify *when* to activate, *what* to do, *what tools it needs*, and *what success looks like*.

## Key Takeaways

1. Context engineering supersedes prompt engineering as the core discipline for building agents.
2. The three-layer architecture (system prompt → skills → tools) separates always-on behavior from on-demand expertise from atomic capabilities.
3. Skills solve context bloat through progressive disclosure, drift through version control, and reuse through portability.
4. The Agent Skills open standard (December 2025) unified the industry around a single format: SKILL.md.
5. A skill is formally defined as (applicability conditions, policy, tool requirements, success criteria).

---

### Sources for This Chapter

| Topic | Source |
|-------|--------|
| "Context engineering" concept | [Anthropic: Context Engineering for Agents (Sep 2025)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) |
| Agent Skills open standard | [agentskills.io/specification](https://agentskills.io/specification) |
| Skill formalization S=(C,π,T,R) | [SoK: Agentic Skills (arXiv:2602.20867)](https://arxiv.org/html/2602.20867v1) |
| Anthropic's original Skills launch | [Manus blog on open standard adoption (Jan 2026)](https://manus.im/blog/manus-skills) |
| Cursor 2.4 Skills support | [Cursor changelog 2.4 (Jan 2026)](https://www.cursor.so/changelog/2-4) |
| "Stop Engineering Prompts" | [Medium: Context Engineering Guide](https://medium.com/@muhammad.shafat/stop-engineering-prompts-start-engineering-context-a-guide-to-the-agent-skills-standard-bc8e2056f40a) |
