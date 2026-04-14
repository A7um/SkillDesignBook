# Chapter 3: Progressive Disclosure — The Architecture of Attention

## 3.1 The Core Insight

The most important architectural principle in skill design comes from an unlikely source: user interface design. **Progressive disclosure**—the practice of revealing information only when the user needs it—was formalized in HCI research decades ago. Applied to AI agents, it becomes the key to scaling capabilities within fixed context budgets.

The insight is deceptively simple: **agents get dumber when you give them too much information upfront**.

This is not intuition—it is empirically demonstrated. The "Same Task, More Tokens" study (ACL 2024) showed that aggregate reasoning accuracy drops from 0.92 to 0.68 as prompt length increases, even when the additional tokens are relevant. The performance degradation comes from the attention mechanism itself: every token competes with every other token for the model's limited computational attention.

## 3.2 The Three-Tier Model

Progressive disclosure in agent systems operates across three tiers:

```
┌──────────────────────────────────────────────────────┐
│  Tier 1: METADATA INDEX                              │
│  Loaded: At startup, for ALL skills                  │
│  Content: name + description (~100 tokens each)      │
│  Context cost: 1-5% of budget                        │
│  Purpose: Semantic awareness of available expertise   │
├──────────────────────────────────────────────────────┤
│  Tier 2: FULL INSTRUCTIONS                           │
│  Loaded: When skill is activated                     │
│  Content: SKILL.md body (<5,000 tokens)              │
│  Context cost: 10-30% of budget per active skill     │
│  Purpose: Step-by-step procedural guidance            │
├──────────────────────────────────────────────────────┤
│  Tier 3: REFERENCE RESOURCES                         │
│  Loaded: On demand, during skill execution           │
│  Content: scripts/, references/, assets/             │
│  Context cost: Variable, as needed                   │
│  Purpose: Deep expertise for specific sub-tasks      │
└──────────────────────────────────────────────────────┘
```

### Token Economics

The scaling advantage is dramatic:

| Approach | 10 Skills | 100 Skills | 1,000 Skills |
|----------|-----------|------------|--------------|
| **Eager loading** | 50K tokens | 500K tokens | 5M tokens (impossible) |
| **Progressive disclosure** | ~6K tokens | ~7K tokens | ~8K tokens |

Progressive disclosure scales logarithmically. Eager loading scales linearly. At 100 skills, progressive disclosure uses **98.6% fewer tokens** than eager loading.

## 3.3 Why Less Context Means Better Reasoning

The intuition that "more information helps" is dangerously wrong for LLMs. Three mechanisms explain why:

### Attention Dilution
The transformer attention mechanism distributes computational budget across all tokens in the context. Irrelevant tokens don't just waste space—they actively compete for attention that should go to relevant information. The IFScale study (2025) identified three distinct degradation patterns as instruction density increases, affecting even the strongest models.

### Decision Complexity
When an agent must choose among 100 fully-loaded tools, the selection space is enormous. When it must choose among 100 names and descriptions, then load the selected tool's details, the decision is dramatically simpler.

### Context Pollution
Tool results, intermediate outputs, and verbose instructions from one skill can pollute the context for subsequent skills. Progressive disclosure, combined with subagent isolation, prevents cross-skill contamination.

## 3.4 Implementation in Production Systems

### Claude Code (Anthropic)

Claude Code implements progressive disclosure through its Skills and subagent architecture:

1. **Startup**: Load all skill names + descriptions into context
2. **Task routing**: Model evaluates which skill (if any) matches the current task
3. **Activation**: Selected skill's full SKILL.md loads into context
4. **Execution**: Agent reads reference files on demand via tool calls
5. **Isolation**: Subagents (spawned via the Task tool) execute in their own context, returning only summaries

The Explore subagent exemplifies this pattern: it runs on the fast Haiku model with read-only tools, processes verbose search results in its own context, and returns a concise summary to the parent agent.

### OpenAI Codex

Codex implements a nearly identical pattern:

1. **Metadata at startup**: Each skill's `name`, `description`, file path, and optional `agents/openai.yaml` metadata
2. **Progressive loading**: Full `SKILL.md` body loaded only when the skill is activated
3. **Explicit invocation**: Users can force-activate with `$skill-name`
4. **Implicit invocation**: Codex matches task to skill descriptions automatically

### Cursor

Cursor loads skills from `.agents/skills/`, `.cursor/skills/`, and user-level `~/.cursor/skills/`. The agent is presented with available skills and decides when they are relevant based on context. Skills can also be manually invoked via the `/` slash command menu.

### Manus (Meta)

Manus structures progressive disclosure across explicit levels:

| Level | Content | Load Time | Context Cost |
|-------|---------|-----------|--------------|
| Level 1: Metadata | Name + description | At startup | ~100 tokens/skill |
| Level 2: Instructions | Full SKILL.md | On trigger | <5K tokens |
| Level 3: Resources | Scripts, references, assets | On demand | Variable |

## 3.5 The Code Execution Pattern

When skills need to interact with many external tools, an advanced form of progressive disclosure emerges: **code execution with MCP**.

Anthropic's engineering team documented this pattern in November 2025. Instead of loading all tool definitions into context (which can consume 50,000+ tokens for a rich tool ecosystem), the agent is presented with tools as a code API:

```
servers/
├── google-drive/
│   ├── getDocument.ts
│   ├── listFiles.ts
│   └── index.ts
├── salesforce/
│   ├── createLead.ts
│   └── index.ts
```

The agent discovers tools by exploring the filesystem—listing directories, reading specific function signatures on demand—and writes code to invoke them. This approach reduces the tool context from potentially millions of tokens to a fixed ~1,000-token footprint regardless of the number of available tools.

Cloudflare independently arrived at the same pattern (February 2026), calling it "Code Mode": exposing only two tools (`search()` to explore the API spec and `execute()` to run requests) keeps the token footprint constant at ~1,000 tokens even for APIs with 2,500+ endpoints.

## 3.6 Designing for Progressive Disclosure

### Principle 1: Metadata Is Routing Logic

Treat the `description` field as a router, not documentation. It should answer three questions:
1. When should the agent activate this skill?
2. When should it *not* activate this skill?
3. What are the expected outputs?

### Principle 2: SKILL.md Is a Table of Contents

The body of SKILL.md should serve as an overview that points to detailed materials. Keep it under 500 lines. Move comprehensive reference material to separate files.

### Principle 3: Reference Files Are Free Until Read

Files in `references/` and `assets/` consume zero context tokens until the agent explicitly reads them. This means you can bundle extensive documentation—complete API specs, large template libraries, detailed examples—without any context cost.

### Principle 4: Depth Should Not Exceed Three Tiers

UX research shows that progressive disclosure beyond 2-3 layers causes user frustration. The same applies to agents: deeply nested reference chains cause partial loads and context fragmentation. Keep your disclosure hierarchy flat.

## 3.7 Anti-Patterns

| Anti-Pattern | Why It Fails |
|--------------|-------------|
| Stuffing everything into SKILL.md | Exceeds 5K-token budget; dilutes attention on every activation |
| Vague descriptions ("Helps with data") | Routing failures—skill either triggers too often or not at all |
| No negative examples | The agent can't distinguish this skill from similar ones |
| Eager-loading reference files in SKILL.md | Wastes tokens on content that may never be needed |
| Deeply nested file references | Causes context fragmentation and partial loads |

## Key Takeaways

1. Progressive disclosure is the defining architectural pattern for scalable skill systems.
2. Three tiers: metadata (~100 tokens/skill at startup) → instructions (<5K tokens on activation) → resources (on demand).
3. The pattern enables 98%+ token savings compared to eager loading at 100+ skills.
4. Agents perform *worse* with more irrelevant context—this is empirically demonstrated, not intuition.
5. Design descriptions as routing logic, SKILL.md as a table of contents, and reference files as free-until-read deep expertise.
