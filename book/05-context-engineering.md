# Chapter 5: Context Engineering for Skills — Managing the Scarcest Resource

## 5.1 Context as Currency

Anthropic's context engineering guide (September 2025) introduced a metaphor that has become the industry's operating framework:

> "Good context engineering means finding the smallest possible set of high-signal tokens that maximize the likelihood of some desired outcome."

Context is not a bucket to be filled. It is a **budget to be allocated**. Every token loaded into a skill competes for attention with the user's request, the conversation history, other loaded skills, and the agent's own reasoning. Treating context as currency changes how you design skills at every level.

## 5.2 The Context Budget

A typical agent session has a context window of 128K–200K tokens. Here's how the budget is typically allocated:

| Component | Typical Allocation | Notes |
|-----------|-------------------|-------|
| System prompt | 2-10K tokens | Always present |
| Skill metadata (all skills) | 5-15K tokens | Scales with number of installed skills |
| Active skill instructions | 2-5K tokens | One or two skills at a time |
| Conversation history | 20-80K tokens | Grows over session |
| Tool results | 10-50K tokens | Varies dramatically |
| Model reasoning buffer | 20-40K tokens | Must be preserved for output generation |

The critical observation: **conversation history and tool results are the largest and most variable consumers**. A single verbose tool result (a large file read, a lengthy test output) can consume 10K+ tokens. This is why skill instructions must be concise—they share the budget with unpredictable runtime content.

## 5.3 Compaction for Long-Horizon Tasks

Long-horizon tasks—those requiring dozens or hundreds of agent turns—inevitably exceed the context window. The solution is **compaction**: summarizing older conversation turns to free space for new work.

### How Compaction Works

1. **Checkpoint creation**: The system identifies a point in the conversation history where a logical unit of work completed
2. **Summarization**: A model generates a concise summary of the completed work (key decisions, file changes, results)
3. **Replacement**: The detailed conversation turns are replaced by the summary
4. **Continuation**: The agent resumes with the summary as context, freeing tokens for new work

### Implications for Skill Design

Skills that run in long-horizon contexts must be designed for compaction resilience:

- **Self-contained steps**: Each step in the skill should produce a meaningful intermediate result that survives compaction
- **Explicit state**: Critical state (which files were changed, which tests passed) should be written to files or tool outputs, not kept only in conversation history
- **Re-derivable context**: The skill should be able to reconstruct its understanding from the current state of files and tools, not depend on remembering earlier conversation turns

OpenAI's guidance on shell + skills + compaction:

> "Long-horizon agents rarely succeed as one-shot prompts. Plan for continuity at the start: design for container reuse and compaction."

## 5.4 Tool Design as Context Engineering

Tools are a major consumer of context tokens. Every tool definition and every tool result occupies space. Anthropic's advanced tool use features (November 2025) introduced three mechanisms to manage this:

### Tool Search Tool

Instead of loading all tool definitions upfront, Claude dynamically discovers tools on demand. In internal testing, this preserved **191,300 tokens** of context compared to 122,800 with traditional eager loading—an 85% reduction.

**When to use Tool Search Tool:**
- Tool definitions consuming >10K tokens total
- Experiencing tool selection accuracy issues
- Agent has access to many tools but uses few per task

### Programmatic Tool Calling

Instead of natural-language tool invocation (which requires a full inference pass per call), Claude writes Python code that orchestrates multiple tool calls. This:
- Reduces the number of inference passes
- Keeps intermediate results in the code execution environment (not in context)
- Enables loops, conditionals, and data transformations without context overhead

### Tool Use Examples

Providing examples of correct tool usage in the skill body dramatically improves tool call accuracy. The key: examples should be concrete and representative, not exhaustive.

```markdown
## Example: Searching for a function definition

Good tool use:
- Use Grep to find the function: `grep -r "def calculate_total" src/`
- Read the file containing the match

Bad tool use:
- Read every file in src/ looking for the function
- Use a shell command to search when Grep is available
```

## 5.5 The AGENTS.md Layer

Skills operate within a broader context hierarchy. The `AGENTS.md` file (or `CLAUDE.md` in Claude Code) provides **always-on project guidance** that shapes how skills execute.

The relationship between AGENTS.md and skills:

| AGENTS.md | Skills |
|-----------|--------|
| Always loaded | Loaded on demand |
| Global project conventions | Task-specific procedures |
| Short, stable rules | Detailed, evolving workflows |
| "What the agent should always know" | "What the agent needs for this specific task" |

**What belongs in AGENTS.md:**
- Repo layout and important directories
- Build, test, and lint commands
- Engineering conventions and coding standards
- Mandatory skill triggers ("Use $X before editing API code")
- Do-not rules and hard constraints

**What belongs in skills:**
- Multi-step deployment procedures
- Review checklists and workflows
- Domain-specific analysis procedures
- Complex testing or verification workflows

The rule of thumb: if a piece of guidance applies to every task, put it in AGENTS.md. If it applies only to specific types of tasks, make it a skill.

## 5.6 Multi-Agent Context Isolation

When tasks are too complex for a single context window, multi-agent architectures provide isolation:

```
┌─────────────────────────────────────────────┐
│  PRIMARY AGENT                              │
│  Context: User request + project state      │
│                                             │
│  ┌────────────┐  ┌────────────┐            │
│  │ Subagent A │  │ Subagent B │            │
│  │ (Explore)  │  │ (Test)     │            │
│  │            │  │            │            │
│  │ Own context│  │ Own context│            │
│  │ Read-only  │  │ Shell      │            │
│  │ tools only │  │ access     │            │
│  └─────┬──────┘  └─────┬──────┘            │
│        │                │                   │
│   Summary only    Summary only              │
└─────────────────────────────────────────────┘
```

Each subagent gets a fresh context window with only the task description. All verbose intermediate work (file contents, search results, test output) stays inside the subagent. Only a concise summary returns to the parent.

This pattern, implemented in Claude Code, Cursor, and Devin, is the primary mechanism for preventing **context pollution**—the degradation that occurs when irrelevant results from one task contaminate the context for subsequent tasks.

## 5.7 Practical Context Budget Worksheet

For a 200K-token context window, plan your skill's context allocation:

```
Total budget:                        200,000 tokens
System prompt:                      -  5,000 tokens
AGENTS.md:                          -  3,000 tokens
Skill metadata (50 skills):         -  5,000 tokens
Active skill body:                  -  4,000 tokens
Conversation history (compacted):   - 30,000 tokens
─────────────────────────────────────────────────
Available for tool results + reasoning: 153,000 tokens
```

If your skill produces verbose tool outputs, plan accordingly:
- A large file read: 5-20K tokens
- A test suite output: 5-30K tokens
- A search result set: 2-10K tokens

## Key Takeaways

1. Context is a finite budget, not a bucket. Every token competes for attention.
2. Design skills for compaction resilience: self-contained steps, explicit state, re-derivable context.
3. Use Tool Search Tool when tool definitions exceed 10K tokens.
4. Put always-on guidance in AGENTS.md; put task-specific procedures in skills.
5. Use subagents for context isolation—verbose intermediate work stays in the subagent, only summaries return.
6. Plan your token budget explicitly, leaving ample room for tool results and model reasoning.

---

### Sources for This Chapter

| Topic | Source |
|-------|--------|
| "Smallest possible set of high-signal tokens" | [Anthropic: Context Engineering (Sep 2025)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) |
| Tool Search Tool (85% token reduction) | [Anthropic: Advanced Tool Use (Nov 2025)](https://www.anthropic.com/engineering/advanced-tool-use) |
| Shell + Skills + Compaction tips | [OpenAI: Long-running agent tips](https://developers.openai.com/blog/skills-shell-tips) |
| AGENTS.md vs Skills separation | [OpenAI: Customization docs](https://developers.openai.com/codex/concepts/customization) |
| Claude Code subagent isolation | [Claude Code: Custom Subagents](https://code.claude.com/docs/en/sub-agents.md) |
| ACE framework (+12.5% on AppWorld) | [jayminwest: Advanced Context Patterns](https://jayminwest.com/agentic-engineering-book/4-context/3-context-patterns) |
