# Chapter 9: Multi-Agent Composition — Skills That Orchestrate

## 9.1 When One Agent Isn't Enough

Single-agent architectures hit limits in three scenarios:

1. **Context overflow**: The task requires more information than fits in one context window
2. **Parallelism**: Multiple independent subtasks can execute simultaneously
3. **Specialization**: Different parts of the task benefit from different tools, models, or expertise

Multi-agent composition addresses all three by distributing work across specialized agents, each with their own context window, tool access, and mission.

## 9.2 The Subagent Pattern

The most widely implemented multi-agent pattern is **parent-child delegation**: a primary agent spawns specialized subagents for specific subtasks.

### Claude Code's Implementation

```
Primary Agent
├── Explore (Haiku, read-only, fast)
│   └── Returns: file paths, code patterns, summaries
├── Plan (inherits parent model)
│   └── Returns: implementation plan, critical files
├── generalPurpose (inherits parent model)
│   └── Returns: task-specific results
└── Custom subagents (.claude/agents/*.md)
    └── Returns: defined by custom instructions
```

**Key constraints:**
- Subagents get a fresh context window (no parent history)
- Subagents cannot spawn more subagents (depth = 1)
- Only summaries return to the parent
- Multiple subagents can run in parallel

### Defining Custom Subagents

```yaml
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Reviews code changes for security vulnerabilities
model: claude-opus-4-6
tools: Read, Grep, Glob
permissionMode: default
---

When asked to review code for security issues:

1. Identify all changed files
2. For each file, check for:
   - SQL injection patterns
   - XSS vulnerabilities
   - Authentication bypasses
   - Exposed credentials
3. Report findings with severity, location, and remediation
```

### When to Use Subagents

| Use Subagents | Stay Single-Agent |
|--------------|-------------------|
| Task produces verbose output you won't reference again | Task needs frequent back-and-forth |
| You want to enforce tool restrictions | You need the full conversation history |
| Work is self-contained and can return a summary | Task is too iterative for delegation |
| Multiple independent subtasks can run in parallel | The overhead of delegation exceeds the benefit |

## 9.3 The Multi-Agent Orchestration Pattern

For complex systems requiring coordination across multiple specialized agents, the orchestration pattern adds a coordinator layer:

```
┌─────────────────────────────────────────────────┐
│  ORCHESTRATOR                                    │
│  Understands the overall task                    │
│  Decomposes into subtasks                        │
│  Routes to specialized agents                    │
│  Synthesizes results                             │
│                                                  │
│  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐   │
│  │Research│  │Code   │  │Test   │  │Deploy │   │
│  │Agent  │  │Agent  │  │Agent  │  │Agent  │   │
│  └───────┘  └───────┘  └───────┘  └───────┘   │
└─────────────────────────────────────────────────┘
```

### LangGraph's Implementation

LangGraph (the dominant open-source orchestration framework as of 2026) represents workflows as **directed cyclic graphs**:

```python
from langgraph.graph import StateGraph

graph = StateGraph(AgentState)
graph.add_node("planner", planner_node)
graph.add_node("executor", executor_node)
graph.add_node("reviewer", reviewer_node)

graph.add_edge("planner", "executor")
graph.add_edge("executor", "reviewer")
graph.add_conditional_edges(
    "reviewer",
    lambda state: "planner" if state["needs_revision"] else "done"
)
```

Key LangGraph patterns:
- **Persistent checkpointing**: State survives across interruptions
- **Human-in-the-loop interrupts**: Pause for approval before critical actions
- **Conditional branching**: Route based on intermediate results
- **Retry with backoff**: Re-attempt failed nodes automatically

### CrewAI's Implementation

CrewAI takes a role-based approach: agents are defined as team members with roles, goals, and backstories:

```python
researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments",
    backstory="Expert researcher with deep domain knowledge",
    tools=[search_tool, read_tool]
)

writer = Agent(
    role="Technical Writer",
    goal="Produce clear, accurate documentation",
    backstory="Experienced tech writer..."
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential
)
```

CrewAI strengths:
- Fastest path to a working multi-agent prototype (2-4 hours)
- 30-60% faster than AutoGen on structured tasks
- 33% fewer tokens through role-based pipeline design

## 9.4 Agent-to-Agent Communication (A2A)

Google's A2A protocol (April 2025) standardizes how agents discover and communicate with each other across organizational boundaries:

### Agent Cards

Each A2A agent publishes a discovery document:

```json
{
  "name": "research-agent",
  "description": "Searches web and databases for information",
  "capabilities": ["web-search", "database-query"],
  "endpoint": "https://research-agent.example.com/a2a",
  "auth": { "type": "bearer" }
}
```

### Communication Protocol

A2A uses JSON-RPC 2.0 with five core methods:

| Method | Purpose |
|--------|---------|
| `tasks/send` | Send a task to an agent |
| `tasks/get` | Check task status |
| `tasks/cancel` | Cancel a running task |
| `tasks/subscribe` | Subscribe to task updates |
| `agent/card` | Get agent capabilities |

### When to Use A2A vs. Subagents

| A2A | Subagents |
|-----|-----------|
| Agents from different teams/orgs | Agents within one system |
| Agents deployed as separate services | Agents sharing a runtime |
| Loose coupling (agents can be replaced) | Tight coupling (parent controls child) |
| Dynamic discovery | Static configuration |

## 9.5 Skill Composition Patterns

### Sequential Composition

Skills execute one after another, with each skill's output feeding the next:

```markdown
# Full Stack Feature Skill (Meta-Skill)

1. Invoke $design-review to validate the architecture
2. Invoke $code-implementation to write the code
3. Invoke $test-suite to verify correctness
4. Invoke $code-review to check quality
5. Invoke $deploy-staging to push to staging
```

### Parallel Composition

Independent skills execute simultaneously:

```markdown
# Release Preparation (Meta-Skill)

Run in parallel:
- $security-audit on all changed files
- $performance-benchmark on critical paths
- $docs-sync to update documentation

Wait for all to complete, then:
- $release-notes to generate changelog
- $final-review for sign-off
```

### Conditional Composition

Skills activate based on conditions:

```markdown
# Code Change Verification

1. Detect what changed: code, tests, docs, or config
2. If code changed → run $lint-check and $type-check
3. If tests changed → run $test-suite
4. If docs changed → run $docs-validation
5. If config changed → run $config-review
6. Always → run $commit-message-check
```

## 9.6 The Dependency Graph

Complex skill systems require dependency management. The Manus Skills architecture implements this via a central registry:

```json
{
  "skills": {
    "deploy-production": {
      "depends_on": ["test-suite", "security-audit", "config-review"],
      "conflicts_with": ["deploy-staging"]
    }
  }
}
```

The dependency graph ensures:
- Prerequisites run before dependent skills
- Conflicting skills don't run simultaneously
- Missing dependencies are detected at skill discovery time

## 9.7 Current Limitations

1. **Only one skill at a time**: Most platforms (Devin, Manus) currently support only one active skill per session. Composition requires meta-skills that reference sub-skills.
2. **No cross-agent memory**: Subagents don't share memory with each other, only with the parent.
3. **Depth limits**: Most implementations limit subagent depth to 1 (no subagent-of-subagent).
4. **Composition overhead**: Each agent delegation adds latency and token cost.

## Key Takeaways

1. Multi-agent composition solves context overflow, parallelism, and specialization needs.
2. Subagents provide context isolation: verbose work stays in the child, summaries return to the parent.
3. LangGraph dominates orchestration for complex stateful workflows; CrewAI leads for rapid prototyping.
4. Google's A2A protocol enables cross-boundary agent-to-agent communication.
5. Skills compose sequentially, in parallel, or conditionally via meta-skills.
6. Current limitations (single active skill, depth-1 subagents) will likely relax as platforms mature.
