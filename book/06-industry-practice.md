# Chapter 6: Industry Practice — How the Leaders Design Skills

## 6.1 OpenAI: Skills as Reusable Procedures

### Architecture

OpenAI's approach, implemented in Codex, treats skills as **tiny CLIs**: self-contained, versioned procedures with clear inputs and outputs. The system has three layers:

1. **AGENTS.md**: Repository-level instructions loaded before every task. Short if/then rules that trigger mandatory skills.
2. **Skills**: Directories in `.agents/skills/` with `SKILL.md` + optional scripts/references. Progressive disclosure via metadata-first loading.
3. **MCP**: External tool connections declared as skill dependencies in `agents/openai.yaml`.

### Key Design Decisions

**Skills + Shell + Compaction**: OpenAI's production pattern combines reusable skill instructions with shell execution environments and context compaction for long runs. This "trifecta" creates durable workflows: skills provide the procedure, shell provides execution, compaction provides continuity.

**The Agents SDK Repo Pattern**: OpenAI uses skills in their own Agents SDK repositories. The pattern reveals their philosophy:
- `code-change-verification`: Runs formatting, lint, type-checking, and tests when code changes
- `docs-sync`: Audits docs against codebase, finding missing or outdated documentation
- `implementation-strategy`: Decides compatibility boundary and approach before editing runtime code
- `final-release-review`: Compares previous release tag with current release candidate

Each skill has a narrow contract, a clear trigger, and a concrete success criterion. They are **report-first workflows**: the skill gathers information and presents findings, then the agent or human decides on action.

**Description as Routing Logic**: OpenAI emphasizes that the `description` field is structural, not stylistic. They recommend including "Use when vs. don't use when" blocks and testing routing before testing the skill body.

### Lessons

- Keep each skill focused on one job
- Prefer instructions over scripts unless determinism is required
- Write imperative steps with explicit inputs and outputs
- Test routing first, body second
- Pin skill versions in production for reproducibility

## 6.2 Anthropic: Context Engineering and the Agent-Computer Interface

### Architecture

Anthropic's approach is built on three pillars:

1. **Model Context Protocol (MCP)**: The universal connector between agents and external tools/data
2. **Agent Skills**: The open standard for procedural knowledge
3. **Context Engineering**: The discipline of curating optimal context

Claude Code's agent architecture is remarkably simple: a `while(tool_call)` loop with 8 core tools (Bash, Read, Edit, Write, Grep, Glob, Task, TodoWrite). The model decides when to call tools, which to call, and when it's done. No DAGs, no classifiers, no RAG pipeline—just a capable model with well-designed tools in a loop.

### Key Design Decisions

**Simplicity First**: Anthropic's most consistent advice is "do the simplest thing that works." Their December 2024 guide on building effective agents explicitly warns against unnecessary complexity: "Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short."

**The Agent-Computer Interface (ACI)**: Anthropic coined this term to describe the tool layer as a first-class design surface—analogous to UI/UX for humans. Tool descriptions deserve as much prompt engineering as the system prompt itself. Each tool should have:
- Clear, precise descriptions
- Well-defined parameter schemas
- Examples of correct usage
- Guidance on when NOT to use the tool

**Subagent Isolation**: Claude Code pioneered the subagent pattern: spawning independent agents with their own context window, restricted tool access, and specific missions. The Explore subagent (Haiku model, read-only tools) is a canonical example—it searches codebases without polluting the parent's context.

**MCP as the Tool Layer**: Rather than building custom tool integrations, Anthropic standardized on MCP—an open protocol that any agent can use to connect to any MCP-compatible server. This decouples tool design from agent design, enabling a shared ecosystem.

### Advanced Features (2025-2026)

- **Tool Search Tool**: Dynamic tool discovery for large tool ecosystems
- **Programmatic Tool Calling**: Writing code to orchestrate tool calls, keeping intermediate results out of context
- **Tool Use Examples**: Demonstrating correct tool patterns within skills
- **Memory Tool**: File-based persistent memory across sessions

### Lessons

- Start simple, add complexity only when it demonstrably improves outcomes
- Treat tool descriptions as first-class prompt engineering
- Use subagents for context isolation, not just parallelism
- Design tools to promote good agent behaviors (clear error messages, structured outputs)

## 6.3 Google: Multi-Agent Systems and the A2A Protocol

### Architecture

Google's approach, implemented in the Agent Development Kit (ADK), is distinguished by its focus on **multi-agent systems** from the ground up:

1. **ADK**: Open-source Python/Go/Java framework for building agents
2. **A2A Protocol**: Agent-to-Agent communication standard (JSON-RPC 2.0 over HTTP)
3. **Vertex AI Agent Engine**: Managed deployment platform

Where Anthropic's MCP connects agents to tools, Google's A2A connects agents to other agents. The two protocols are complementary:

```
MCP = Agent ↔ Tool   ("the hands")
A2A = Agent ↔ Agent  ("the mouth")
```

### Key Design Decisions

**Agent Cards for Discovery**: In A2A, each agent publishes an "agent card" describing its capabilities—similar to a skill's description, but for entire agents. Orchestrator agents discover worker agents by reading their cards and delegate tasks based on capability matching.

**The `to_a2a()` Pattern**: ADK provides a single-function wrapper that converts any ADK agent into an A2A-compatible service:

```python
from google.adk.agents.llm_agent import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="An agent that provides weather information",
    tools=[get_weather]
)

a2a_agent = to_a2a(root_agent)
```

**Skills in the Gemini CLI**: Google adopted the Agent Skills standard for Gemini CLI, loading skills from `.agents/skills/`. The pattern is identical to Codex and Claude Code: progressive disclosure with metadata-first loading.

### Lessons

- When agents need to collaborate across organizational boundaries, A2A provides the standard
- Agent discovery (via agent cards) is the multi-agent analog of skill routing (via descriptions)
- MCP and A2A are complementary, not competing: use MCP for tools, A2A for agent-to-agent

## 6.4 Cursor: The IDE as Agent Harness

### Architecture

Cursor treats the IDE itself as an **agent harness** built on three components:

1. **Instructions**: System prompts and rules that guide agent behavior
2. **Tools**: File operations, terminal, browser, MCP connections
3. **Models**: Multiple models tuned for different tasks

### Key Design Decisions

**Rules vs. Skills**: Cursor distinguishes between:
- **Rules** (`.cursor/rules/`): Always-on context that applies to every conversation. Think of them as the AGENTS.md equivalent.
- **Skills** (`.cursor/skills/`): On-demand capabilities loaded when relevant. Procedural "how-to" instructions.

**Subagents for Specialization**: Cursor 2.4 (January 2026) introduced built-in subagents for codebase exploration, terminal commands, and parallel work. Custom subagents can be defined with specific prompts, tool access, and model selection.

**Cloud Agents**: For long-running tasks, Cursor provides cloud agents that run in remote sandboxes. Users can close their laptop and check results later. Cloud agents create branches, run tests, and produce PRs autonomously.

**Plan Before Code**: Cursor's most impactful recommendation: plan before coding. Start conversations with a plan, let the agent propose an approach, then iterate. The agent's success rate improves significantly with specific instructions.

### Lessons

- The agent harness (instructions + tools + model) matters as much as any individual component
- Separate always-on rules from on-demand skills
- Cloud agents enable long-horizon tasks that exceed a single session
- Planning before execution dramatically improves agent performance

## 6.5 Devin (Cognition): The Planner-Critic Architecture

### Architecture

Devin's architecture is the most specialized for long-horizon coding tasks:

1. **Planner Model**: High-reasoning model (comparable to GPT-6 class) that constructs multi-step plans and dynamically re-plans on failure
2. **Critic Model**: Pattern recognition model that reviews changes for logic errors, vulnerabilities, and regressions
3. **Sandbox**: Secure VM with terminal, editor, and browser

### Key Design Decisions

**Plan → Execute → Critique → Re-plan Loop**: Devin's core loop is iterative by design. The Planner generates a plan, the agent executes it in the sandbox, the Critic reviews the results, and the Planner re-plans based on feedback. This loop continues until the task succeeds or the agent reports a blocker.

**Large-Context Repository Ingestion**: Devin ingests entire repositories at 10M+ token scale, enabling coordinated multi-file, multi-repo analysis without losing context on distant dependencies.

**Auto-Suggested Skills**: Devin can automatically suggest skills after testing your application or learning something new about your codebase. This turns the skill creation process from manual authoring to agent-assisted capture of successful workflows.

**Self-Healing Test Loops**: Tests run in the sandbox; failures feed back to the Planner/Critic for automated diagnosis and fix. This creates a tight feedback loop between execution and learning.

### Lessons from Rebuilding for Sonnet 4.5

Cognition's blog (September 2025) on rebuilding Devin for Claude Sonnet 4.5 reveals deep insights:

- Models respond differently to the same prompts; the agent architecture must adapt to each model's strengths
- Newer models are more proactive about writing tests and creating feedback loops
- Context-aware tool calls (the model adjusting behavior based on remaining context budget) are an emerging capability
- Subagent delegation works better when the model can judge which tasks benefit from isolation

## 6.6 Manus (Meta): Skills in the Sandbox

### Architecture

Manus's distinguishing characteristic is **full sandbox execution**: every skill runs in an isolated Ubuntu VM with browser, code execution, and file system access.

### Key Design Decisions

**"Package as Skill"**: Users can complete a task conversationally, then say "Package this workflow as a Skill." Manus auto-generates the SKILL.md and bundles scripts.

**Multi-Tool Synergy**: A single skill can orchestrate browser automation, code execution, and file operations seamlessly. A market research skill can browse websites, analyze data with Python, and generate reports—all within one workflow.

**Five-Layer Architecture**: Community skill libraries (like the Manus Skills Unified Arsenal) organize skills across layers:
1. Foundation (standards and patterns)
2. Shared utilities (common helpers)
3. Individual skills (55+ across 12 categories)
4. Discovery and dependency system (registry, dependency graph)
5. Meta-skills (orchestrate multiple skills into workflows)

### Lessons

- Full sandbox execution removes the gap between skill instructions and actual execution
- Auto-generating skills from successful workflows lowers the authoring barrier
- Multi-tool synergy within skills enables complex real-world workflows

## Key Takeaways

1. All major platforms have converged on the SKILL.md format and progressive disclosure.
2. OpenAI emphasizes skills as tiny CLIs with routing-first design.
3. Anthropic emphasizes simplicity, context engineering, and the agent-computer interface.
4. Google extends skill concepts to multi-agent systems via A2A.
5. Cursor integrates skills into the IDE harness with rules/skills separation.
6. Devin adds Planner/Critic architecture for iterative long-horizon tasks.
7. Manus demonstrates full sandbox execution with auto-skill generation.
