# Source Catalog — Hyperlinked References for Every Topic

Every claim in this book links to a primary source. Use this catalog to jump directly to the original material.

---

## Official Specifications & Standards

| Source | URL | Topics |
|--------|-----|--------|
| Agent Skills Specification | [agentskills.io/specification](https://agentskills.io/specification) | SKILL.md format, frontmatter fields, progressive disclosure, directory structure |
| Agent Skills Overview | [skill.md](https://skill.md/) | What skills are, adoption list, ecosystem overview |
| MCP Specification | [modelcontextprotocol.io](https://modelcontextprotocol.io) | Model Context Protocol spec, server/client architecture |
| A2A Protocol Spec | [github.com/google/A2A](https://github.com/google/A2A) | Agent-to-Agent protocol, agent cards, JSON-RPC methods |
| OWASP Agentic Skills Top 10 | [owasp.org/www-project-agentic-skills-top-10](https://owasp.org/www-project-agentic-skills-top-10/) | AST01–AST10 security risks, threat taxonomy |

---

## OpenAI — Skills, Codex, Agents SDK

| Source | URL | Topics |
|--------|-----|--------|
| OpenAI Skills Repository (16K stars) | [github.com/openai/skills](https://github.com/openai/skills) | Curated skills: `imagegen`, `sora`, `speech`, `doc`, `gh-fix-ci` |
| Agents SDK Python Skills (9 skills) | [github.com/openai/openai-agents-python/.agents/skills](https://github.com/openai/openai-agents-python/tree/main/.agents/skills) | `code-change-verification`, `implementation-strategy`, `final-release-review`, `docs-sync`, `runtime-behavior-probe`, `test-coverage-improver`, `pr-draft-summary`, `openai-knowledge`, `examples-auto-run` |
| `implementation-strategy` SKILL.md (full text) | [raw link](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) | Compatibility boundary rules, release-tag judgment, default implementation stance |
| `final-release-review` SKILL.md (full text) | [raw link](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md) | Deterministic gate policy (🟢/🔴), release readiness workflow, output format template |
| `code-change-verification` SKILL.md | [playbooks.com](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification) | Verification stack: format→lint→mypy→tests, fail-fast scripts |
| Agents SDK AGENTS.md | [github.com/openai/openai-agents-python/AGENTS.md](https://github.com/openai/openai-agents-python/blob/main/AGENTS.md) | Mandatory skill usage rules, project structure, compatibility policy |
| Blog: Using Skills to Accelerate OSS Maintenance | [developers.openai.com/blog/skills-agents-sdk](https://developers.openai.com/blog/skills-agents-sdk) | 457 PRs in 3 months, skill catalog, AGENTS.md integration pattern |
| Blog: Shell + Skills + Compaction Tips | [developers.openai.com/blog/skills-shell-tips](https://developers.openai.com/blog/skills-shell-tips) | Description as routing logic, negative examples, long-run design, security containment |
| Skills in OpenAI API (cookbook) | [developers.openai.com/cookbook/examples/skills_in_api](https://developers.openai.com/cookbook/examples/skills_in_api) | API integration, version pinning, operational best practices |
| AGENTS.md Guide | [developers.openai.com/codex/guides/agents-md](https://developers.openai.com/codex/guides/agents-md) | Global/project/nested discovery, 32KiB limit, override mechanism |
| Codex Best Practices | [developers.openai.com/codex/learn/best-practices](https://developers.openai.com/codex/learn/best-practices) | Planning, AGENTS.md, MCP, skill authoring, automation |
| Codex Skill Creation Docs | [developers.openai.com/codex/skills/create-skill](https://developers.openai.com/codex/skills/create-skill) | SKILL.md format, directory layout, `openai.yaml`, invocation modes |

---

## Anthropic — Claude Code, MCP, Context Engineering

| Source | URL | Topics |
|--------|-----|--------|
| Building Effective Agents | [anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents/) | Three principles (simplicity, transparency, ACI), workflows vs. agents, augmented LLM pattern |
| Context Engineering for Agents | [anthropic.com/engineering/effective-context-engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Context as currency, compaction, multi-agent architectures, tool design |
| Writing Tools for Agents | [anthropic.com/engineering/writing-tools-for-agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | 5 principles: tool selection, namespacing, meaningful context, token efficiency, description engineering |
| Code Execution with MCP | [anthropic.com/engineering/code-execution-with-mcp](https://www.anthropic.com/engineering/code-execution-with-mcp) | Code Mode pattern, filesystem-based tool discovery, context reduction |
| Advanced Tool Use | [anthropic.com/engineering/advanced-tool-use](https://www.anthropic.com/engineering/advanced-tool-use) | Tool Search Tool (85% token reduction), Programmatic Tool Calling, Tool Use Examples |
| Introducing MCP | [anthropic.com/index/model-context-protocol](https://www.anthropic.com/index/model-context-protocol) | MCP architecture, ecosystem, pre-built servers |
| MCP Connector API Docs | [docs.anthropic.com/en/docs/agents-and-tools/mcp-connector](https://docs.anthropic.com/en/docs/agents-and-tools/mcp-connector) | API integration, MCPToolset, tool configuration |
| Skill Authoring Best Practices | [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Concise is key, degrees of freedom, progressive disclosure in practice, token budgets, checklist |
| Claude Code Subagents Docs | [docs.anthropic.com/en/docs/claude-code/sdk/subagents](https://docs.anthropic.com/en/docs/claude-code/sdk/subagents) | Agent SDK, built-in tools, subagent definitions, session persistence |
| Claude Code Custom Subagents | [code.claude.com/docs/en/sub-agents.md](https://code.claude.com/docs/en/sub-agents.md) | Custom subagent YAML frontmatter, tool restrictions, permission modes, parallel execution |

---

## Google — ADK, A2A, Gemini

| Source | URL | Topics |
|--------|-----|--------|
| ADK Overview | [cloud.google.com/agent-builder/agent-development-kit/overview](https://cloud.google.com/agent-builder/agent-development-kit/overview) | Framework overview, multi-agent design, deployment targets |
| ADK Launch Blog | [developers.googleblog.com](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/) | LlmAgent, multi-agent patterns, LiteLLM integration, Gemini optimization |
| A2A Protocol Explainer | [dev.to/diven_rastdus](https://dev.to/diven_rastdus_c5af27d68f3/the-a2a-protocol-how-google-wants-ai-agents-to-talk-to-each-other-27e5) | Agent cards, JSON-RPC methods, healthcare system case study, when to use A2A vs MCP |
| ADK `to_a2a()` Tutorial | [medium.com/google-cloud](https://medium.com/google-cloud/surprisingly-simple-a2a-agents-with-adk-using-to-a2a-deploy-to-cloud-run-and-gemini-enterprise-e815bdef4a32) | Single-function A2A conversion, Cloud Run deployment, Gemini Enterprise registration |

---

## Cursor

| Source | URL | Topics |
|--------|-----|--------|
| Agent Best Practices | [cursor.com/blog/agent-best-practices](https://www.cursor.com/blog/agent-best-practices) | Agent harness (instructions+tools+model), planning, rules vs skills, cloud agents |
| Dynamic Context Discovery | [cursor.com/blog/dynamic-context-discovery](https://cursor.com/blog/dynamic-context-discovery) | Long responses→files, skills on-demand loading, MCP tool folder sync, terminal sync |
| Towards Self-Driving Codebases | [cursor.com/blog/self-driving-codebases](https://cursor.com/blog/self-driving-codebases) | Multi-agent research, planner/executor/worker roles, instruction importance |
| Cursor Skills Docs | [cursor.com/docs/context/skills](https://www.cursor.com/docs/context/skills) | Skill directories, SKILL.md format, installation, migration |
| Subagents, Skills, and Image Generation (v2.4) | [cursor.so/changelog/2-4](https://www.cursor.so/changelog/2-4) | Subagent types, skills launch, custom subagents |
| Cursor Architecture Deep Dive | [medium.com/@khayyam.h](https://medium.com/@khayyam.h/designing-high-performance-agentic-systems-an-architectural-case-study-of-the-cursor-agent-ab624e4a0a64) | ReAct loop, 15+ tools, speculative edits, multi-agent design |
| How Cursor Actually Works | [medium.com/@paoloperrone](https://medium.com/@paoloperrone/how-cursor-actually-works-c0702d5d91a9) | Priompt, tree-sitter indexing, speculative decoding, RL retraining loop |

---

## Devin / Cognition

| Source | URL | Topics |
|--------|-----|--------|
| Devin Skills Docs | [docs.devin.ai/product-guides/skills](https://docs.devin.ai/product-guides/skills) | SKILL.md in repos, auto-suggestion, skill discovery, invocation modes |
| Rebuilding Devin for Sonnet 4.5 | [cognition.ai/blog/devin-sonnet-4-5-lessons-and-challenges](https://cognition.ai/blog/devin-sonnet-4-5-lessons-and-challenges) | Context anxiety, filesystem-as-memory, parallel tool calls, subagent delegation |
| How Cognition Uses Devin to Build Devin | [cognition.ai/blog/how-cognition-uses-devin-to-build-devin](https://cognition.ai/blog/how-cognition-uses-devin-to-build-devin) | 659 PRs/week, Playbooks, Devin Review, DANA, managed Devins |
| Devin Can Now Manage Devins | [cognition.ai/blog/devin-can-now-manage-devins](https://cognition.ai/blog/devin-can-now-manage-devins) | Meta-agent pattern, isolated VMs per subtask, coordination |
| Devin 2.1 (Confidence Ratings) | [cognition.ai/blog/devin-2-1](https://cognition.ai/blog/devin-2-1) | 🟢🟡🔴 confidence, codebase intelligence, plan confirmation |
| Devin System Prompt (leaked) | [github.com/hussainasghar/system-prompts](https://github.com/hussainasghar/system-prompts-and-models-of-ai-tools/blob/main/Devin%20AI/devin.txt) | Planning/standard modes, think tool, security rules, command reference |

---

## Manus / Meta

| Source | URL | Topics |
|--------|-----|--------|
| Manus Skills Documentation | [manus.im/docs/features/skills](https://manus.im/docs/features/skills) | Progressive disclosure levels, skill management, tips |
| Manus Agent Skills Feature Page | [manus.im/features/agent-skills](https://manus.im/features/agent-skills) | Sandbox execution, multi-tool synergy, MCP complementarity |
| Manus Skills Blog | [manus.im/blog/manus-skills](https://manus.im/blog/manus-skills) | Open standard integration, progressive disclosure, data source skills |
| Manus System Prompt (leaked) | [leaked-system-prompts.com](https://leaked-system-prompts.com/prompts/manus/manus_20250310) | Agent loop, modules, sandbox environment, tool-use rules |
| Manus System Prompt (gist) | [gist.github.com/renschni](https://gist.github.com/renschni/a6c0157cdcdf2db2fc1e7c3e20bff602) | Full agent_loop, modules, prompt.txt, tools dump |
| Manus Skills Architecture | [github.com/abcnuts/manus-skills/ARCHITECTURE.md](https://github.com/abcnuts/manus-skills/blob/main/ARCHITECTURE.md) | Five-layer architecture, skill registry, dependency graph |

---

## Open-Source Frameworks

| Source | URL | Topics |
|--------|-----|--------|
| LangGraph 2.0 Guide | [dev.to/richard_dillon](https://dev.to/richard_dillon_b9c238186e/langgraph-20-the-definitive-guide-to-building-production-grade-ai-agents-in-2026-4j2b) | StateGraph, checkpointing, MCP/A2A integration, migration |
| LangGraph Tools-First Pattern | [sitepoint.com](https://www.sitepoint.com/implementing-the-tools-first-pattern-in-lang-graph/) | Pydantic schemas, UniversalToolNode, bind_tools, recursion limits |
| Production LangChain Agents (SRAL) | [aakashsharan.com](https://aakashsharan.com/production-langchain-agents-sral-patterns/) | State-first, tool verification, experience store, PostgresSaver |
| Human-in-the-Loop with LangGraph | [towardsdatascience.com](https://towardsdatascience.com/building-human-in-the-loop-agentic-workflows/) | Interrupts, checkpointing, best practices |
| LangGraph 3 Tool Patterns | [medium.com/@abhinavsaxena](https://medium.com/@abhinavsaxena_17855/mastering-llm-tools-in-langgraph-a-guide-to-the-3-core-patterns-a48f31653f11) | Action Tool, Command Tool, Structured Tool (BaseTool) |

---

## Community Skill Libraries

| Source | URL | Topics |
|--------|-----|--------|
| VoltAgent/awesome-agent-skills (15K stars) | [github.com/VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 1000+ curated skills, official Anthropic/Google/Vercel/Stripe skills |
| addyosmani/agent-skills (5K stars) | [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 19 production engineering lifecycle skills (define→plan→build→verify→review→ship) |
| mgechev/skills-best-practices (1.8K stars) | [github.com/mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) | Authoring guide, LLM-driven validation, routing tests, skillgrade eval |
| heilcheng/awesome-agent-skills (3.9K stars) | [github.com/heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) | Community directory, quality standards, MCP server examples |

---

## Academic Papers

| Paper | URL | Key Finding |
|-------|-----|-------------|
| SoK: Agentic Skills — Beyond Tool Use | [arxiv.org/html/2602.20867v1](https://arxiv.org/html/2602.20867v1) | Skill lifecycle taxonomy (7 stages), S=(C,π,T,R) formalization, ClawHavoc analysis |
| Agent Skills for LLMs: Architecture, Acquisition, Security | [arxiv.org/pdf/2602.12430](https://arxiv.org/pdf/2602.12430) | SKILL.md architecture, CUA deployment, Skill Trust Framework, 7 open challenges |
| Adaptation of Agentic AI: Post-Training, Memory, Skills | [arxiv.org/pdf/2512.16301v3](https://arxiv.org/pdf/2512.16301v3) | Four-paradigm framework, agent vs tool adaptation, skill libraries |
| PALADIN: Self-Correcting Agents for Tool Failures | [arxiv.org/html/2509.25238v1](https://arxiv.org/html/2509.25238v1) | 50K+ recovery trajectories, 7 failure patterns, retrieval-based recovery |
| Memento-Skills: Self-Evolving Agent Skills | [venturebeat.com](https://venturebeat.com/orchestration/new-framework-lets-ai-agents-rewrite-their-own-skills-without-retraining-the) | 13.7pp improvement on GAIA, skill router, continual learning |
| Measuring AI Ability to Complete Long Tasks (METR) | [arxiv.org/html/2503.14499v1](https://arxiv.org/html/2503.14499v1) | 50% time horizon doubling every 7 months, 170-task benchmark |
| SWE-Bench Pro: Long-Horizon SWE Tasks | [arxiv.org/html/2509.16941v2](https://arxiv.org/html/2509.16941v2) | 1,865 problems, 41 repos, <45% resolve rate, failure mode clusters |
| Trajectory-Informed Memory Generation | [arxiv.org/html/2603.10600v1](https://arxiv.org/html/2603.10600v1) | Strategy/recovery/optimization tips, adaptive retrieval, decision attribution |
| ComplexBench (NeurIPS 2024) | Referenced in [agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/) | Constraint composition degrades LLM performance |
| IFScale (2025) | Referenced in [agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/) | Three degradation patterns as instruction density increases |
| Same Task, More Tokens (ACL 2024) | Referenced in [agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/) | Accuracy drops 0.92→0.68 with prompt length increase |

---

## Security Research

| Source | URL | Topics |
|--------|-----|--------|
| Snyk ToxicSkills Audit | [snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) | 36% infection rate, 1,467 malicious skills, prompt injection + malware convergence |
| OWASP AST10 | [owasp.org/www-project-agentic-skills-top-10](https://owasp.org/www-project-agentic-skills-top-10/) | 10 risks: malicious skills, supply chain, over-privilege, metadata, deserialization |
| PurpleBox: Hidden Supply Chain Risk | [prplbx.com/blog/agent-skills-supply-chain](https://www.prplbx.com/blog/agent-skills-supply-chain) | ClawHavoc timeline, attack taxonomy, defense checklist |
| Red Hat: Security Threats and Controls | [developers.redhat.com](https://developers.redhat.com/articles/2026/03/10/agent-skills-explore-security-threats-and-controls) | Threat model, sandbox isolation, AppArmor, prompt injection |
| Promptfoo: Supply Chain Attack DB Entry | [promptfoo.dev](https://www.promptfoo.dev/lm-security-db/vuln/agent-skill-supply-chain-attack-f0c66804) | Confused deputy attacks, hybrid NL+code payloads, mitigation steps |

---

## Design Patterns & Deep Dives

| Source | URL | Topics |
|--------|-----|--------|
| Agent-Computer Interface (ACI) | [agentpatterns.ai/tool-engineering/agent-computer-interface](https://agentpatterns.ai/tool-engineering/agent-computer-interface/) | HCI→ACI mapping, poka-yoke, SWE-agent design choices |
| Token-Efficient Tool Design | [agentpatterns.ai/tool-engineering/token-efficient-tool-design](https://agentpatterns.ai/tool-engineering/token-efficient-tool-design/) | Return only next decision's inputs, eliminate overlap, cap toolset size |
| Progressive Disclosure Pattern | [jayminwest.com/.../7-progressive-disclosure](https://www.jayminwest.com/agentic-engineering-book/7-patterns/7-progressive-disclosure) | Three-tier model, token economics table, trade-offs |
| Advanced Context Patterns (ACE) | [jayminwest.com/.../3-context-patterns](https://jayminwest.com/agentic-engineering-book/4-context/3-context-patterns) | Stanford/SambaNova ACE framework, +12.5% on AppWorld |
| Self-Healing AI Agent Pipeline | [dev.to/miso_clawpod](https://dev.to/miso_clawpod/how-to-build-a-self-healing-ai-agent-pipeline-a-complete-guide-95b) | 5 failure categories, Recovery Ledger, circuit breakers, dead letter queues |
| VIGIL Self-Healing Runtime | [zylos.ai/research](https://zylos.ai/research/2026-01-12-ai-agent-error-handling-recovery) | Meta-procedural self-repair, failure taxonomy by module, graceful degradation |
| ActiveMemory (Carnival9) | [dev.to/oldeucryptoboi](https://dev.to/oldeucryptoboi/cross-session-lessons-in-carnival9-how-an-agent-remembers-what-worked-51ji) | Lesson extraction, utility-based eviction, damage-tolerant loading |
| Context Engineering Guide (Anthropic) | [howaiworks.ai/blog](https://howaiworks.ai/blog/anthropic-context-engineering-for-agents) | Six developer takeaways, six organization takeaways |
| Stop Engineering Prompts, Start Engineering Context | [medium.com/@muhammad.shafat](https://medium.com/@muhammad.shafat/stop-engineering-prompts-start-engineering-context-a-guide-to-the-agent-skills-standard-bc8e2056f40a) | Prompt→context shift, drift problem, platform implementations |

---

## Benchmarks & Evaluation

| Source | URL | Topics |
|--------|-----|--------|
| SWE-bench Scores Explained (2026) | [dev.to/rahulxsingh](https://dev.to/rahulxsingh/swe-bench-scores-and-leaderboard-explained-2026-54of) | Leaderboard, scaffolding effect (30%→80%), limitations |
| SWE-bench Pro Leaderboard | [scaleapi.github.io/SWE-bench_Pro-os](https://scaleapi.github.io/SWE-bench_Pro-os/) | Live scores, 730 problems, SWE-Agent scaffold |
| Claude Mythos Preview Benchmarks | [officechai.com](https://officechai.com/ai/claude-mythos-preview-benchmarks-swe-bench-pro/) | 93.9% SWE-bench Verified, 77.8% SWE-bench Pro |
| GLM-5.1 SWE-bench Pro | [officechai.com](https://officechai.com/ai/z-ai-glm-5-1-benchmarks-swe-bench-pro/) | 58.4% SWE-bench Pro (first Chinese model to top leaderboard) |

---

## CLAUDE.md / AGENTS.md Best Practices

| Source | URL | Topics |
|--------|-----|--------|
| CLAUDE.md Best Practices (6 Principles) | [heyuan110.com](https://www.heyuan110.com/posts/ai/2026-03-05-claude-code-claudemd-best-practices/) | Commands not descriptions, emphasis keywords, 7 project-type examples |
| 15 Claude Code Tips from 6 Projects | [aiorg.dev/blog](https://aiorg.dev/blog/claude-code-best-practices) | CLAUDE.md, rules, custom commands, phased execution |
| Claude Code 2026 Guide (Morph) | [morphllm.com](https://www.morphllm.com/claude-code-best-practices) | Templates by stack, delegation spectrum, subagent usage |
| Complete CLAUDE.md Guide | [claudedirectory.org/blog](https://www.claudedirectory.org/blog/claude-md-guide) | Anatomy of great CLAUDE.md, 5 stack templates, common mistakes |
| Claude Code Hooks & Subagents Guide | [dev.to/vibehackers](https://dev.to/vibehackers/claude-code-hooks-subagents-power-features-the-complete-guide-2026-c71) | Hooks lifecycle, custom subagents, memory systems, auto mode |
