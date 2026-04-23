# 参考资料目录：按主题整理的链接

书里该点出处的地方，尽量都链回一手材料。想顺着某个话题往下挖，可以从这份目录直接跳过去。

---

## 官方规范与标准

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| Agent Skills Specification | [agentskills.io/specification](https://agentskills.io/specification) | SKILL.md 格式、frontmatter 字段、渐进式披露、目录结构 |
| Agent Skills Overview | [skill.md](https://skill.md/) | 什么是 skills、采用列表、生态系统概览 |
| MCP Specification | [modelcontextprotocol.io](https://modelcontextprotocol.io) | Model Context Protocol 规范、服务端/客户端架构 |
| A2A Protocol Spec | [github.com/google/A2A](https://github.com/google/A2A) | Agent-to-Agent 协议、agent cards、JSON-RPC 方法 |
| OWASP Agentic Skills Top 10 | [owasp.org/www-project-agentic-skills-top-10](https://owasp.org/www-project-agentic-skills-top-10/) | AST01–AST10 安全风险、威胁分类体系 |

---

## OpenAI — Skills、Codex、Agents SDK

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| OpenAI Skills Repository（16K stars） | [github.com/openai/skills](https://github.com/openai/skills) | 精选 skills：`imagegen`、`sora`、`speech`、`doc`、`gh-fix-ci` |
| Agents SDK Python Skills（9 个 skills） | [github.com/openai/openai-agents-python/.agents/skills](https://github.com/openai/openai-agents-python/tree/main/.agents/skills) | `code-change-verification`、`implementation-strategy`、`final-release-review`、`docs-sync`、`runtime-behavior-probe`、`test-coverage-improver`、`pr-draft-summary`、`openai-knowledge`、`examples-auto-run` |
| `implementation-strategy` SKILL.md（全文） | [raw link](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) | 兼容性边界规则、release-tag 判断、默认实现立场 |
| `final-release-review` SKILL.md（全文） | [raw link](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md) | 确定性门控策略（🟢/🔴）、发布就绪工作流、输出格式模板 |
| `code-change-verification` SKILL.md | [playbooks.com](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification) | 验证栈：format→lint→mypy→tests，快速失败脚本 |
| Agents SDK AGENTS.md | [github.com/openai/openai-agents-python/AGENTS.md](https://github.com/openai/openai-agents-python/blob/main/AGENTS.md) | 强制 skill 使用规则、项目结构、兼容性策略 |
| 博客：Using Skills to Accelerate OSS Maintenance | [developers.openai.com/blog/skills-agents-sdk](https://developers.openai.com/blog/skills-agents-sdk) | 3 个月内 457 个 PR、skill 目录、AGENTS.md 集成模式 |
| 博客：Shell + Skills + Compaction Tips | [developers.openai.com/blog/skills-shell-tips](https://developers.openai.com/blog/skills-shell-tips) | 描述作为路由逻辑、反面示例、长期运行设计、安全隔离 |
| Skills in OpenAI API（cookbook） | [developers.openai.com/cookbook/examples/skills_in_api](https://developers.openai.com/cookbook/examples/skills_in_api) | API 集成、版本锁定、运维最佳实践 |
| AGENTS.md Guide | [developers.openai.com/codex/guides/agents-md](https://developers.openai.com/codex/guides/agents-md) | 全局/项目/嵌套发现机制、32KiB 限制、覆盖机制 |
| Codex Best Practices | [developers.openai.com/codex/learn/best-practices](https://developers.openai.com/codex/learn/best-practices) | 规划、AGENTS.md、MCP、skill 编写、自动化 |
| Codex Skill Creation Docs | [developers.openai.com/codex/skills/create-skill](https://developers.openai.com/codex/skills/create-skill) | SKILL.md 格式、目录布局、`openai.yaml`、调用模式 |

---

## Anthropic — Claude Code、MCP、Context Engineering

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| Building Effective Agents | [anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents/) | 三项原则（简洁性、透明性、ACI）、工作流与 agents 的对比、增强型 LLM 模式 |
| Context Engineering for Agents | [anthropic.com/engineering/effective-context-engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 上下文即资产、压缩策略、多 agent 架构、工具设计 |
| Writing Tools for Agents | [anthropic.com/engineering/writing-tools-for-agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | 5 项原则：工具选择、命名空间、有意义的上下文、token 效率、描述工程 |
| Code Execution with MCP | [anthropic.com/engineering/code-execution-with-mcp](https://www.anthropic.com/engineering/code-execution-with-mcp) | Code Mode 模式、基于文件系统的工具发现、上下文缩减 |
| Advanced Tool Use | [anthropic.com/engineering/advanced-tool-use](https://www.anthropic.com/engineering/advanced-tool-use) | Tool Search Tool（token 减少 85%）、Programmatic Tool Calling、Tool Use Examples |
| Introducing MCP | [anthropic.com/index/model-context-protocol](https://www.anthropic.com/index/model-context-protocol) | MCP 架构、生态系统、预构建服务器 |
| MCP Connector API Docs | [docs.anthropic.com/en/docs/agents-and-tools/mcp-connector](https://docs.anthropic.com/en/docs/agents-and-tools/mcp-connector) | API 集成、MCPToolset、工具配置 |
| Skill Authoring Best Practices | [platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | 简洁为要、自由度控制、渐进式披露实践、token 预算、检查清单 |
| Claude Code Subagents Docs | [docs.anthropic.com/en/docs/claude-code/sdk/subagents](https://docs.anthropic.com/en/docs/claude-code/sdk/subagents) | Agent SDK、内置工具、subagent 定义、会话持久化 |
| Claude Code Custom Subagents | [code.claude.com/docs/en/sub-agents.md](https://code.claude.com/docs/en/sub-agents.md) | 自定义 subagent YAML frontmatter、工具限制、权限模式、并行执行 |

---

## Google — ADK、A2A、Gemini

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| ADK Overview | [cloud.google.com/agent-builder/agent-development-kit/overview](https://cloud.google.com/agent-builder/agent-development-kit/overview) | 框架概览、多 agent 设计、部署目标 |
| ADK Launch Blog | [developers.googleblog.com](https://developers.googleblog.com/en/agent-development-kit-easy-to-build-multi-agent-applications/) | LlmAgent、多 agent 模式、LiteLLM 集成、Gemini 优化 |
| A2A Protocol Explainer | [dev.to/diven_rastdus](https://dev.to/diven_rastdus_c5af27d68f3/the-a2a-protocol-how-google-wants-ai-agents-to-talk-to-each-other-27e5) | Agent cards、JSON-RPC 方法、医疗系统案例研究、A2A 与 MCP 的使用场景对比 |
| ADK `to_a2a()` Tutorial | [medium.com/google-cloud](https://medium.com/google-cloud/surprisingly-simple-a2a-agents-with-adk-using-to-a2a-deploy-to-cloud-run-and-gemini-enterprise-e815bdef4a32) | 单函数 A2A 转换、Cloud Run 部署、Gemini Enterprise 注册 |

---

## Cursor

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| Agent Best Practices | [cursor.com/blog/agent-best-practices](https://www.cursor.com/blog/agent-best-practices) | Agent 框架（指令+工具+模型）、规划、rules 与 skills 的对比、cloud agents |
| Dynamic Context Discovery | [cursor.com/blog/dynamic-context-discovery](https://cursor.com/blog/dynamic-context-discovery) | 长响应→文件、skills 按需加载、MCP 工具文件夹同步、终端同步 |
| Towards Self-Driving Codebases | [cursor.com/blog/self-driving-codebases](https://cursor.com/blog/self-driving-codebases) | 多 agent 研究、planner/executor/worker 角色、指令重要性 |
| Cursor Skills Docs | [cursor.com/docs/context/skills](https://www.cursor.com/docs/context/skills) | Skill 目录、SKILL.md 格式、安装、迁移 |
| Subagents, Skills, and Image Generation (v2.4) | [cursor.so/changelog/2-4](https://www.cursor.so/changelog/2-4) | Subagent 类型、skills 发布、自定义 subagents |
| Cursor Architecture Deep Dive | [medium.com/@khayyam.h](https://medium.com/@khayyam.h/designing-high-performance-agentic-systems-an-architectural-case-study-of-the-cursor-agent-ab624e4a0a64) | ReAct 循环、15+ 工具、推测性编辑、多 agent 设计 |
| How Cursor Actually Works | [medium.com/@paoloperrone](https://medium.com/@paoloperrone/how-cursor-actually-works-c0702d5d91a9) | Priompt、tree-sitter 索引、推测性解码、RL 重训练循环 |

---

## Devin / Cognition

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| Devin Skills Docs | [docs.devin.ai/product-guides/skills](https://docs.devin.ai/product-guides/skills) | 仓库中的 SKILL.md、自动建议、skill 发现、调用模式 |
| Rebuilding Devin for Sonnet 4.5 | [cognition.ai/blog/devin-sonnet-4-5-lessons-and-challenges](https://cognition.ai/blog/devin-sonnet-4-5-lessons-and-challenges) | 上下文焦虑、文件系统作为记忆、并行工具调用、subagent 委托 |
| How Cognition Uses Devin to Build Devin | [cognition.ai/blog/how-cognition-uses-devin-to-build-devin](https://cognition.ai/blog/how-cognition-uses-devin-to-build-devin) | 每周 659 个 PR、Playbooks、Devin Review、DANA、托管 Devins |
| Devin Can Now Manage Devins | [cognition.ai/blog/devin-can-now-manage-devins](https://cognition.ai/blog/devin-can-now-manage-devins) | 元 agent 模式、每个子任务隔离 VM、协调 |
| Devin 2.1（Confidence Ratings） | [cognition.ai/blog/devin-2-1](https://cognition.ai/blog/devin-2-1) | 🟢🟡🔴 置信度、代码库智能、计划确认 |
| Devin System Prompt（泄露） | [github.com/hussainasghar/system-prompts](https://github.com/hussainasghar/system-prompts-and-models-of-ai-tools/blob/main/Devin%20AI/devin.txt) | 规划/标准模式、think 工具、安全规则、命令参考 |

---

## Manus / Meta

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| Manus Skills Documentation | [manus.im/docs/features/skills](https://manus.im/docs/features/skills) | 渐进式披露层级、skill 管理、技巧 |
| Manus Agent Skills Feature Page | [manus.im/features/agent-skills](https://manus.im/features/agent-skills) | 沙箱执行、多工具协同、MCP 互补性 |
| Manus Skills Blog | [manus.im/blog/manus-skills](https://manus.im/blog/manus-skills) | 开放标准集成、渐进式披露、数据源 skills |
| Manus System Prompt（泄露） | [leaked-system-prompts.com](https://leaked-system-prompts.com/prompts/manus/manus_20250310) | Agent 循环、模块、沙箱环境、工具使用规则 |
| Manus System Prompt（gist） | [gist.github.com/renschni](https://gist.github.com/renschni/a6c0157cdcdf2db2fc1e7c3e20bff602) | 完整 agent_loop、模块、prompt.txt、工具转储 |
| Manus Skills Architecture | [github.com/abcnuts/manus-skills/ARCHITECTURE.md](https://github.com/abcnuts/manus-skills/blob/main/ARCHITECTURE.md) | 五层架构、skill 注册表、依赖图 |

---

## 开源框架

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| LangGraph 2.0 Guide | [dev.to/richard_dillon](https://dev.to/richard_dillon_b9c238186e/langgraph-20-the-definitive-guide-to-building-production-grade-ai-agents-in-2026-4j2b) | StateGraph、检查点、MCP/A2A 集成、迁移 |
| LangGraph Tools-First Pattern | [sitepoint.com](https://www.sitepoint.com/implementing-the-tools-first-pattern-in-lang-graph/) | Pydantic schemas、UniversalToolNode、bind_tools、递归限制 |
| Production LangChain Agents (SRAL) | [aakashsharan.com](https://aakashsharan.com/production-langchain-agents-sral-patterns/) | State-first、工具验证、经验存储、PostgresSaver |
| Human-in-the-Loop with LangGraph | [towardsdatascience.com](https://towardsdatascience.com/building-human-in-the-loop-agentic-workflows/) | 中断机制、检查点、最佳实践 |
| LangGraph 3 Tool Patterns | [medium.com/@abhinavsaxena](https://medium.com/@abhinavsaxena_17855/mastering-llm-tools-in-langgraph-a-guide-to-the-3-core-patterns-a48f31653f11) | Action Tool、Command Tool、Structured Tool (BaseTool) |

---

## 社区 Skill 库

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| VoltAgent/awesome-agent-skills（15K stars） | [github.com/VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 1000+ 精选 skills，含 Anthropic/Google/Vercel/Stripe 官方 skills |
| addyosmani/agent-skills（5K stars） | [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 19 个生产工程生命周期 skills（定义→规划→构建→验证→评审→交付） |
| mgechev/skills-best-practices（1.8K stars） | [github.com/mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) | 编写指南、LLM 驱动的验证、路由测试、skillgrade 评估 |
| heilcheng/awesome-agent-skills（3.9K stars） | [github.com/heilcheng/awesome-agent-skills](https://github.com/heilcheng/awesome-agent-skills) | 社区目录、质量标准、MCP 服务器示例 |

---

## ClawHub 与 OpenClaw Skills

| Skill | 链接 | 模式 / 备注 |
|-------|------|-------------|
| ClawHub Skills Hub（按下载量排序） | [clawhub.ai/skills?sort=downloads](https://clawhub.ai/skills?sort=downloads) | 3,286 个 skills，总下载量超 150 万次 |
| `review-code`（ClawHub，473 次下载） | [clawhub.ai](https://clawhub.ai/skills/review-code)、[raw SKILL.md](https://raw.githubusercontent.com/openclaw/skills/main/skills/review-code/SKILL.md) | 风险优先的代码审查、8 个参考文件、记忆架构、严重性+置信度校准 |
| `solo-review`（ClawHub，645 次下载） | [clawhub.ai](https://clawhub.ai/skills/solo-review) | 12 维质量门控（测试、lint、构建、安全、验收、代码质量、计划、日志、原则、提交、文档、可视化），SHIP/FIX/BLOCK 裁定，合理化目录，按技术栈划分的命令 |
| `skill-reviewer`（ClawHub） | [raw SKILL.md](https://raw.githubusercontent.com/openclaw/skills/main/skills/gitgoodordietrying/skill-reviewer/SKILL.md) | 53 项评分标准、结构检查清单、描述审计、示例密度/质量指标、常见缺陷目录 |
| OpenClaw `github` skill | [raw SKILL.md](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/github/SKILL.md) | ✅/❌ 何时使用/不使用章节，带 JSON 输出的常用命令，PR 审查 + 问题分流模板 |
| OpenClaw `gh-issues` skill | [raw SKILL.md](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/gh-issues/SKILL.md) | 6 阶段编排器、标志参考表、带完整提示模板的 sub-agent 生成、基于声明的去重、fork 模式、cron 模式 |
| OpenClaw `review-pr` skill | [playbooks.com](https://playbooks.com/skills/openclaw/openclaw/review-pr) | 脚本优先的 PR 审查、结构化 JSON 发现 |
| OpenClaw `pr-commit-workflow` | [github.com/openclaw/skills](https://github.com/openclaw/skills/tree/main/skills/joshp123/pr-commit-workflow/SKILL.md) | 提交 + PR 强制执行，要求人工编写的意图说明 |
| OpenClaw `openclaw-pr-maintainer` | [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw/blob/9098e948/.agents/skills/openclaw-pr-maintainer/SKILL.md) | 分流、标记、合入 PR，要求提供 bug 修复证据 |
| Best ClawHub Skills Guide（2026 年 3 月） | [medium.com/@tentenco](https://medium.com/@tentenco/the-best-clawhub-skills-worth-installing-now-a-category-by-category-guide-5221c4850d21) | 分类指南、安全审查、100/3 规则 |
| SkillCompass Analysis of Top 100 | [dev.to/john_spaghetti](https://dev.to/john_spaghetti/i-ran-skillcompass-on-the-top-100-clawhub-skills-heres-what-i-found-18fo) | 对 ClawHub 下载量头部 Skill 的质量分析 |
| Top 5 Downloaded Skills Review | [dev.to/99rebels](https://dev.to/99rebels/i-installed-the-5-most-downloaded-skills-on-clawhub-only-one-did-anything-49e4) | 批判性评测 — 下载与安装比平均为 59:1 |

---

## 学术论文

| 论文 | 链接 | 关键发现 |
|------|------|----------|
| SoK: Agentic Skills — Beyond Tool Use | [arxiv.org/html/2602.20867v1](https://arxiv.org/html/2602.20867v1) | Skill 生命周期分类法（7 个阶段）、S=(C,π,T,R) 形式化、ClawHavoc 分析 |
| Agent Skills for LLMs: Architecture, Acquisition, Security | [arxiv.org/pdf/2602.12430](https://arxiv.org/pdf/2602.12430) | SKILL.md 架构、CUA 部署、Skill Trust Framework、7 个开放挑战 |
| Adaptation of Agentic AI: Post-Training, Memory, Skills | [arxiv.org/pdf/2512.16301v3](https://arxiv.org/pdf/2512.16301v3) | 四范式框架、agent 与工具适配的对比、skill 库 |
| PALADIN: Self-Correcting Agents for Tool Failures | [arxiv.org/html/2509.25238v1](https://arxiv.org/html/2509.25238v1) | 50K+ 恢复轨迹、7 种失败模式、基于检索的恢复 |
| Memento-Skills: Self-Evolving Agent Skills | [venturebeat.com](https://venturebeat.com/orchestration/new-framework-lets-ai-agents-rewrite-their-own-skills-without-retraining-the) | 在 GAIA 上提升 13.7 个百分点、skill 路由器、持续学习 |
| Measuring AI Ability to Complete Long Tasks (METR) | [arxiv.org/html/2503.14499v1](https://arxiv.org/html/2503.14499v1) | 50% 时间范围每 7 个月翻倍、170 个任务的基准测试 |
| SWE-Bench Pro: Long-Horizon SWE Tasks | [arxiv.org/html/2509.16941v2](https://arxiv.org/html/2509.16941v2) | 1,865 个问题、41 个仓库、<45% 解决率、失败模式聚类 |
| Trajectory-Informed Memory Generation | [arxiv.org/html/2603.10600v1](https://arxiv.org/html/2603.10600v1) | 策略/恢复/优化提示、自适应检索、决策归因 |
| ComplexBench (NeurIPS 2024) | 引用自 [agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/) | 约束组合导致 LLM 性能下降 |
| IFScale (2025) | 引用自 [agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/) | 指令密度增加时的三种退化模式 |
| Same Task, More Tokens (ACL 2024) | 引用自 [agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/) | 随着提示长度增加，准确率从 0.92 降至 0.68 |

---

## 安全研究

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| Snyk ToxicSkills Audit | [snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/) | 36% 感染率、1,467 个恶意 skills、提示注入 + 恶意软件融合 |
| OWASP AST10 | [owasp.org/www-project-agentic-skills-top-10](https://owasp.org/www-project-agentic-skills-top-10/) | 10 大风险：恶意 skills、供应链、过度授权、元数据、反序列化 |
| PurpleBox: Hidden Supply Chain Risk | [prplbx.com/blog/agent-skills-supply-chain](https://www.prplbx.com/blog/agent-skills-supply-chain) | ClawHavoc 时间线、攻击分类体系、防御检查清单 |
| Red Hat: Security Threats and Controls | [developers.redhat.com](https://developers.redhat.com/articles/2026/03/10/agent-skills-explore-security-threats-and-controls) | 威胁模型、沙箱隔离、AppArmor、提示注入 |
| Promptfoo: Supply Chain Attack DB Entry | [promptfoo.dev](https://www.promptfoo.dev/lm-security-db/vuln/agent-skill-supply-chain-attack-f0c66804) | 混淆代理攻击、混合自然语言+代码载荷、缓解步骤 |

---

## 设计模式与深度解析

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| Agent-Computer Interface (ACI) | [agentpatterns.ai/tool-engineering/agent-computer-interface](https://agentpatterns.ai/tool-engineering/agent-computer-interface/) | HCI→ACI 映射、防错设计（poka-yoke）、SWE-agent 设计决策 |
| Token-Efficient Tool Design | [agentpatterns.ai/tool-engineering/token-efficient-tool-design](https://agentpatterns.ai/tool-engineering/token-efficient-tool-design/) | 仅返回下一步决策所需的输入、消除重叠、限制工具集规模 |
| Progressive Disclosure Pattern | [jayminwest.com/.../7-progressive-disclosure](https://www.jayminwest.com/agentic-engineering-book/7-patterns/7-progressive-disclosure) | 三层模型、token 经济表、权衡取舍 |
| Advanced Context Patterns (ACE) | [jayminwest.com/.../3-context-patterns](https://jayminwest.com/agentic-engineering-book/4-context/3-context-patterns) | Stanford/SambaNova ACE 框架、在 AppWorld 上提升 +12.5% |
| Self-Healing AI Agent Pipeline | [dev.to/miso_clawpod](https://dev.to/miso_clawpod/how-to-build-a-self-healing-ai-agent-pipeline-a-complete-guide-95b) | 5 类故障、Recovery Ledger、断路器、死信队列 |
| VIGIL Self-Healing Runtime | [zylos.ai/research](https://zylos.ai/research/2026-01-12-ai-agent-error-handling-recovery) | 元程序性自修复、按模块划分的故障分类、优雅降级 |
| ActiveMemory (Carnival9) | [dev.to/oldeucryptoboi](https://dev.to/oldeucryptoboi/cross-session-lessons-in-carnival9-how-an-agent-remembers-what-worked-51ji) | 经验提取、基于效用的淘汰、容错加载 |
| Context Engineering Guide (Anthropic) | [howaiworks.ai/blog](https://howaiworks.ai/blog/anthropic-context-engineering-for-agents) | 面向开发者的六条要点、面向组织的六条要点 |
| Stop Engineering Prompts, Start Engineering Context | [medium.com/@muhammad.shafat](https://medium.com/@muhammad.shafat/stop-engineering-prompts-start-engineering-context-a-guide-to-the-agent-skills-standard-bc8e2056f40a) | 从提示到上下文的转变、漂移问题、平台实现 |

---

## 基准测试与评估

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| SWE-bench Scores Explained (2026) | [dev.to/rahulxsingh](https://dev.to/rahulxsingh/swe-bench-scores-and-leaderboard-explained-2026-54of) | 排行榜、脚手架效应（30%→80%）、局限性 |
| SWE-bench Pro Leaderboard | [scaleapi.github.io/SWE-bench_Pro-os](https://scaleapi.github.io/SWE-bench_Pro-os/) | 实时分数、730 个问题、SWE-Agent 脚手架 |
| Claude Mythos Preview Benchmarks | [officechai.com](https://officechai.com/ai/claude-mythos-preview-benchmarks-swe-bench-pro/) | SWE-bench Verified 93.9%、SWE-bench Pro 77.8% |
| GLM-5.1 SWE-bench Pro | [officechai.com](https://officechai.com/ai/z-ai-glm-5-1-benchmarks-swe-bench-pro/) | SWE-bench Pro 58.4%（首个登顶排行榜的中国模型） |

---

## CLAUDE.md / AGENTS.md 最佳实践

| 来源 | 链接 | 涵盖主题 |
|------|------|----------|
| CLAUDE.md Best Practices（6 项原则） | [heyuan110.com](https://www.heyuan110.com/posts/ai/2026-03-05-claude-code-claudemd-best-practices/) | 命令而非描述、强调关键词、7 个项目类型示例 |
| 15 Claude Code Tips from 6 Projects | [aiorg.dev/blog](https://aiorg.dev/blog/claude-code-best-practices) | CLAUDE.md、rules、自定义命令、分阶段执行 |
| Claude Code 2026 Guide (Morph) | [morphllm.com](https://www.morphllm.com/claude-code-best-practices) | 按技术栈分类的模板、委托光谱、subagent 使用 |
| Complete CLAUDE.md Guide | [claudedirectory.org/blog](https://www.claudedirectory.org/blog/claude-md-guide) | 优秀 CLAUDE.md 的结构剖析、5 个技术栈模板、常见错误 |
| Claude Code Hooks & Subagents Guide | [dev.to/vibehackers](https://dev.to/vibehackers/claude-code-hooks-subagents-power-features-the-complete-guide-2026-c71) | Hooks 生命周期、自定义 subagents、记忆系统、自动模式 |
