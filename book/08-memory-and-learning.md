# Chapter 8: Memory and Learning — Skills That Improve Over Time

## 8.1 The Stateless Problem

By default, every agent session starts fresh. The agent has no memory of previous sessions, no record of successful strategies, and no awareness of past failures. This means:

- The agent makes the same mistakes repeatedly across sessions
- Successful strategies are not reused
- Each session reinvents understanding that was already achieved

For long-horizon tasks that span multiple sessions, or for skills that are used repeatedly across a team, this statelessness is a critical limitation.

## 8.2 Memory Architectures

### Project Memory (CLAUDE.md / AGENTS.md)

The simplest memory mechanism: a file that persists across sessions and is loaded at startup.

**Claude Code** uses `CLAUDE.md`:
- Loaded at session start
- Contains build commands, conventions, known issues
- Can be updated by the agent during the session
- Scoped to project (`.claude/CLAUDE.md`) or user (`~/.claude/CLAUDE.md`)

**Codex** uses `AGENTS.md`:
- Loaded before every task
- Hierarchical: global → project root → nested directories
- Override mechanism: `AGENTS.override.md` takes precedence

These files are the **minimum viable memory**. They capture what the agent needs to know every time, but they don't capture what the agent learned during specific tasks.

### Session Memory and Persistence

Anthropic's Memory Tool (September 2025) adds file-based persistent memory:
- Stores information outside the context window
- Builds knowledge bases over time
- Maintains project state across sessions
- References previous work without keeping everything in context

Claude Code's Agent SDK supports session persistence:
- Capture a `session_id` from the first query
- Resume with full context on subsequent queries
- Fork sessions to explore different approaches

### Skill-Scoped Memory

Custom subagents in Claude Code can maintain their own persistent memory:
```yaml
---
name: code-reviewer
description: Reviews code for quality and security
memory: project  # Scoped to project, user, or local
---
```

This enables skills to accumulate domain-specific knowledge: a code review skill might remember common issues found in this codebase, a deployment skill might remember which configurations work for which environments.

## 8.3 The Memento-Skills Framework

The most sophisticated approach to agent learning comes from the **Memento-Skills** framework (April 2026), developed by researchers across multiple universities.

### Architecture

Memento-Skills creates an **evolving external knowledge base** that functions as the agent's growing muscle memory:

```
┌──────────────────────────────────────────────┐
│  NEW TASK                                     │
│       ↓                                       │
│  SKILL ROUTER → retrieves relevant skills     │
│       ↓                                       │
│  AGENT EXECUTION (with retrieved skills)      │
│       ↓                                       │
│  RESULT EVALUATION                            │
│       ↓                                       │
│  SKILL UPDATE/CREATION                        │
│       ↓                                       │
│  SKILL LIBRARY (persistent, evolving)         │
└──────────────────────────────────────────────┘
```

Each skill artifact contains three core elements:
1. **Declarative specifications**: What the skill is and how it should be used
2. **Procedural knowledge**: Step-by-step instructions derived from successful executions
3. **Executable code**: Helper scripts that the agent runs to solve the task

### Results

On the GAIA benchmark (complex multi-step reasoning): **66.0% accuracy** with Memento-Skills vs. 52.3% with a static skill baseline—a 13.7 percentage point improvement.

The key insight: **actively self-evolving memory vastly outperforms static skill libraries**. Skills that are refined based on execution outcomes become progressively more effective.

## 8.4 Trajectory-Informed Memory

A March 2026 research paper introduced a more nuanced approach to learning from agent execution:

### Three Types of Learned Guidance

1. **Strategy Tips**: Successful patterns from clean executions
   - "When refactoring authentication code, always check for session invalidation edge cases"
   
2. **Recovery Tips**: Failure handling and error correction approaches
   - "When database migrations fail with 'relation already exists', check if a previous migration was partially applied"

3. **Optimization Tips**: Improvements from inefficient-but-successful executions
   - "When searching for function definitions, use Grep before reading full files—it's 10x faster"

### Decision Attribution

The framework distinguishes between:
- **Immediate causes**: The direct action that led to success or failure
- **Proximate causes**: The decision that set up the immediate cause
- **Root causes**: The fundamental reasoning pattern that led to the decision chain

This causal analysis produces higher-quality memories than simple outcome logging.

## 8.5 The ActiveMemory Pattern

The Carnival9 project's `ActiveMemory` implementation provides a practical production model:

### Design Principles

1. **The execution trace is the source of truth.** Memory is derived state—small, distilled, prunable.
2. **Lessons are extracted exactly once per session**, in the `finally` block, after all work is complete.
3. **Eviction is by proven utility**: lessons that were retrieved but never contributed to task success are evicted first.
4. **Memory enters through hardened channels**: the same sanitization and length caps as all other untrusted data.

### Eviction Policy

The store holds at most 100 lessons. When the 101st is added:
1. Sort all lessons by `relevance_count` ascending, then by `created_at` ascending
2. Keep the top 100 (most frequently useful, most recent)
3. Drop the rest

This optimizes for **proven utility**: a lesson that was extracted and then never matched (never contributed to any future task) is the first to go.

### Security Considerations

Memory introduces an attack surface:
- Attacker-controlled state can be re-introduced at startup
- Memory poisoning can cause the agent to follow malicious instructions
- Corrupted memory files can prevent the agent from starting

The mitigation: treat loaded memory with the same suspicion as any untrusted input. Validate format, enforce length limits, and recover silently from corruption.

## 8.6 Cross-Session Learning for Skills

Combining the memory approaches above, a practical pattern for skill improvement:

### After Each Session

1. **Extract outcomes**: Did the skill succeed? What errors occurred? What workarounds were needed?
2. **Distill lessons**: Convert outcomes into concise, actionable guidance
3. **Update skill if warranted**: For significant learnings, update the skill's SKILL.md or reference files
4. **Log to memory**: Store session-specific learnings in the memory system

### At Session Start

1. **Load skill metadata**: Progressive disclosure as usual
2. **Retrieve relevant memories**: Based on the current task, retrieve past learnings
3. **Inject as context**: Add relevant memories alongside the skill instructions

### Over Time

1. **Prune ineffective memories**: Evict memories that are never retrieved or never contribute to success
2. **Promote stable learnings**: Memories that consistently improve outcomes get incorporated into the skill itself
3. **Version the skill**: Major learnings trigger a skill version bump

## 8.7 Practical Memory Checklist

- [ ] Use AGENTS.md/CLAUDE.md for always-needed project knowledge
- [ ] Enable session persistence for multi-turn tasks
- [ ] Implement lesson extraction in the skill's completion phase
- [ ] Define eviction criteria for memory management
- [ ] Treat loaded memory as untrusted input
- [ ] Promote stable learnings into skill instructions
- [ ] Track memory effectiveness (was it retrieved? Did it help?)

## Key Takeaways

1. Stateless agents repeat mistakes and reinvent solutions. Memory breaks this cycle.
2. Memory operates at three levels: project (AGENTS.md), session (persistence), and skill (scoped memory).
3. Memento-Skills demonstrates that self-evolving skill libraries outperform static ones by 13+ percentage points.
4. Trajectory-informed memory produces three types of guidance: strategy, recovery, and optimization tips.
5. Memory management requires eviction policies (prune by utility) and security measures (treat as untrusted input).
6. Stable learnings should be promoted from memory into skill instructions over time.
