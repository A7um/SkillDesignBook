# 第六章：Top 1,000 下载量 Skill 的实证分析

本章呈现了对 **ClawHub 上实际下载量排名前 1,000 的 Skill** 的分析成果（按下载次数排序，数据来自 [ClawHub API](https://clawhub.atomicbot.ai/api/skills?sort=downloads&dir=desc)），并与 [openclaw/skills](https://github.com/openclaw/skills) 仓库中的 SKILL.md 文件进行了交叉比对（共 58,593 个 Skill）。

### 方法论

1. 通过 ClawHub API 查询下载量排名前 1,000 的 Skill
2. 将每个 Skill 匹配到已克隆的 `openclaw/skills` 仓库中对应的 SKILL.md 文件
3. 对 990 个匹配到的 Skill 执行程序化模式检测（10 个未在仓库中找到）
4. 对下载量前 20 的 Skill 进行人工深度阅读，分析其结构

---

## 6.1 下载量前 20 的 Skill

| 排名 | Skill | 下载量 | 行数 | 章节数 | 代码块 | 脚本 | 引用 |
|------|-------|--------|------|--------|--------|------|------|
| 1 | [self-improving-agent](https://clawhub.ai/skills/self-improving-agent) | 398,524 | 645 | 25 | 21 | 3 | 3 |
| 2 | [skill-vetter](https://clawhub.ai/skills/skill-vetter) | 212,949 | 139 | 6 | 5 | 0 | 0 |
| 3 | [ontology](https://clawhub.ai/skills/ontology) | 167,234 | 233 | 12 | 13 | 1 | 2 |
| 4 | [self-improving](https://clawhub.ai/skills/self-improving) | 166,829 | 251 | 14 | 4 | 0 | 0 |
| 5 | [github](https://clawhub.ai/skills/github) | 160,019 | 48 | 3 | 6 | 0 | 0 |
| 6 | [gog](https://clawhub.ai/skills/gog) | 158,020 | 37 | 0 | 0 | 0 | 0 |
| 7 | [proactive-agent](https://clawhub.ai/skills/proactive-agent) | 145,053 | 633 | 32 | 9 | 1 | 2 |
| 8 | [weather](https://clawhub.ai/skills/weather) | 136,298 | 50 | 2 | 4 | 0 | 0 |
| 9 | [multi-search-engine](https://clawhub.ai/skills/multi-search-engine) | 122,353 | 155 | 11 | 1 | 0 | 2 |
| 10 | [polymarket-trade](https://clawhub.ai/skills/polymarket-trade) | 121,966 | 252 | 9 | 15 | 1 | 0 |
| 11 | [pollyreach](https://clawhub.ai/skills/pollyreach) | 95,510 | 547 | 11 | 14 | 6 | 0 |
| 12 | [humanizer](https://clawhub.ai/skills/humanizer) | 92,489 | 438 | 11 | 0 | 0 | 0 |
| 13 | [nano-pdf](https://clawhub.ai/skills/nano-pdf) | 92,486 | 21 | 1 | 1 | 0 | 0 |
| 14 | [agent-browser](https://clawhub.ai/skills/agent-browser-clawdbot) | 91,547 | 207 | 9 | 17 | 0 | 0 |
| 15 | [nano-banana-pro](https://clawhub.ai/skills/nano-banana-pro) | 87,867 | 131 | 11 | 4 | 1 | 0 |
| 16 | [tavily-search](https://clawhub.ai/skills/openclaw-tavily-search) | 83,383 | 49 | 4 | 1 | 1 | 0 |
| 17 | [obsidian](https://clawhub.ai/skills/obsidian) | 83,200 | 56 | 2 | 0 | 0 | 0 |
| 18 | [admapix](https://clawhub.ai/skills/admapix) | 81,113 | 480 | 11 | 13 | 0 | 7 |
| 19 | [baidu-search](https://clawhub.ai/skills/baidu-search) | 79,770 | 64 | 5 | 2 | 1 | 1 |
| 20 | [sonoscli](https://clawhub.ai/skills/sonoscli) | 78,572 | 27 | 0 | 0 | 0 | 0 |

**关键发现**：下载量与 Skill 质量并不相关。排名第 1 的 `self-improving-agent`（39.8 万次下载，645 行，25 个章节，3 个脚本）结构精深。但排名第 13 的 `nano-pdf`（9.2 万次下载，21 行）和排名第 20 的 `sonoscli`（7.8 万次下载，27 行，零章节）内容极其简薄。高下载量往往反映的是发布时间早或病毒式传播，而非质量。

---

## 6.2 汇总统计

| 指标 | 下载量 Top 1,000 | 全量语料库（58,593） |
|------|------------------|---------------------|
| 总下载量 | 12,502,864 | — |
| 平均下载量 | 12,629 | — |
| 下载量区间 | 3,835 – 398,524 | — |
| 平均行数 | 240 | ~150 |
| 平均章节数（## 标题） | 8.2 | ~5 |
| 平均代码块数 | 10.6 | ~6 |
| 包含 `scripts/` 的 Skill | 327（33%） | 18,204（31%） |
| 包含 `references/` 的 Skill | 204（20%） | 12,591（22%） |

Top 1,000 的 Skill 平均**长 60%**，**章节多 64%**，**代码块多 77%**。在结构上的投入与下载量正相关（尽管因果关系尚不明确）。

---

## 6.3 Top 1,000 下载量 Skill 中的模式频率

| 模式 | 数量 | 占 990 的百分比 | 语料库占比（58,593） | 差值 |
|------|------|----------------|---------------------|------|
| 编号步骤 | 621 | 62.7% | ~40% | +23 |
| 决策表 | 508 | 51.3% | ~30% | +21 |
| 前置条件 / 环境搭建 | 444 | 44.8% | ~20% | +25 |
| 快速入门 / 快速参考 | 358 | 36.2% | 17.3% | +19 |
| 故障排除 | 275 | 27.8% | 9.0% | +19 |
| 正文中引用脚本 | 258 | 26.1% | — | — |
| 破折号式理由说明（4 处以上） | 228 | 23.0% | 36.6% | -14 |
| 错误处理 | 210 | 21.2% | 14.3% | +7 |
| ✅/❌ 代码对比 | 201 | 20.3% | 19.8% | +0.5 |
| 何时使用 | 171 | 17.3% | 13.2% | +4 |
| 输出格式 / 模板 | 141 | 14.2% | 9.7% | +5 |
| 最佳实践章节 | 124 | 12.5% | 11.8% | +1 |
| 安全与信任 | 112 | 11.3% | 1.5% | **+10** |
| 工作流章节 | 110 | 11.1% | 9.4% | +2 |
| 示例章节 | 97 | 9.8% | 4.6% | +5 |
| 常见陷阱 / 踩坑点 | 94 | 9.5% | 3.9% | +6 |
| AI 特有的常见错误 | 85 | 8.6% | — | 新增 |
| 清单项 `[ ]` | 78 | 7.9% | 6.3% | +2 |
| 核心规则章节 | 71 | 7.2% | 1.4% | **+6** |
| 关联 Skill | 60 | 6.1% | 2.9% | +3 |
| 记忆目录（`~/name/`） | 52 | 5.3% | 3.6% | +2 |
| 何时不使用 | 46 | 4.6% | 4.9% | -0.3 |
| 审批关卡 | 43 | 4.3% | 3.1% | +1 |
| 危险信号 | 22 | 2.2% | — | — |

**Top 1,000 显著高于语料库平均水平的模式**：
- **前置条件 / 环境搭建**（+25 个百分点）— 顶级 Skill 会告知你开始之前需要准备什么
- **编号步骤**（+23 个百分点）— 顶级 Skill 以流程为导向，而非纯描述性
- **决策表**（+21 个百分点）— 顶级 Skill 包含用于分类的表格
- **快速入门**（+19 个百分点）— 顶级 Skill 提供快速上手路径
- **故障排除**（+19 个百分点）— 顶级 Skill 预见并处理故障
- **安全与信任**（+10 个百分点）— 顶级 Skill 声明其数据处理方式
- **核心规则**（+6 个百分点）— 顶级 Skill 设有专门的"核心规则"章节

---

## 6.4 脚本分析 — 顶级 Skill 实际执行了什么

**Top 1,000 中有 327 个 Skill（33%）包含 `scripts/` 目录。** 在包含脚本的 Skill 中，平均每个 Skill 有 2.9 个脚本。

### 脚本语言分布

| 语言 | 数量 | 占含脚本 Skill 的百分比 |
|------|------|------------------------|
| Python | 183 | 56% |
| Bash/Shell | 105 | 32% |
| JavaScript/TypeScript | 39 | 12% |

### 脚本用途（基于对顶级 Skill 的深度阅读）

| 脚本类型 | 功能 | 示例 Skill |
|----------|------|-----------|
| **API 封装** | 将外部 API 封装为结构化输入输出 | [polymarket-trade](https://clawhub.ai/skills/polymarket-trade)、[stock-watcher](https://clawhub.ai/skills/stock-watcher)、[crypto-market-data](https://clawhub.ai/skills/crypto-market-data) |
| **验证运行器** | 按严格顺序执行检查，快速失败 | [code-change-verification](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification)（OpenAI） |
| **数据获取器** | 获取并解析外部数据 | [baidu-search](https://clawhub.ai/skills/baidu-search)、[multi-search-engine](https://clawhub.ai/skills/multi-search-engine)、[tech-news-digest](https://clawhub.ai/skills/tech-news-digest) |
| **文件处理器** | 转换文件（PDF、Excel、图片） | [automate-excel](https://clawhub.ai/skills/automate-excel)、[nano-banana-pro](https://clawhub.ai/skills/nano-banana-pro) |
| **系统自动化** | 控制操作系统/硬件 | [windows-control](https://clawhub.ai/skills/windows-control)（23 个脚本！）、[computer-use](https://clawhub.ai/skills/computer-use)（17 个脚本） |
| **记忆/状态管理器** | 读写持久化状态文件 | [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)、[session-memory](https://clawhub.ai/skills/session-memory)、[hippocampus-memory](https://clawhub.ai/skills/hippocampus-memory) |

### 关键脚本模式

**模式 A：SKILL.md 按场景路由到脚本**

来自 [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)（39.8 万次下载）：
```
| Situation                | Action                                    |
|--------------------------|-------------------------------------------|
| Command/operation fails  | Log to `.learnings/ERRORS.md`             |
| User corrects you        | Log to `.learnings/LEARNINGS.md`          |
| Found better approach    | Log with category `best_practice`         |
| Broadly applicable       | Promote to `CLAUDE.md` or `AGENTS.md`     |
```

SKILL.md 是一张路由表，每条路由指向一个文件或脚本。

**模式 B：脚本支持 `--json` 标志以输出机器可读格式**

来自 OpenAI [gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md)：
```bash
python scripts/inspect_pr_checks.py --repo "." --pr "123" --json
```

双重输出：默认人类可读，`--json` 用于 Agent 需要结构化数据的场景。

**模式 C：跨平台脚本变体**

来自 OpenAI [code-change-verification](https://playbooks.com/skills/openai/openai-agents-js/code-change-verification)：
```
scripts/
├── run.sh    # Unix
└── run.ps1   # Windows
```

**模式 D：创建目录结构的初始化脚本**

来自 [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)：
```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Learnings\n..." > .learnings/LEARNINGS.md
[ -f .learnings/ERRORS.md ] || printf "# Errors\n..." > .learnings/ERRORS.md
```

该脚本是幂等的 — 可以安全地重复运行。它只在文件不存在时才创建。

---

## 6.5 从 Top 1,000 分析中发现的新模式

### 模式 28：前置条件 / 环境搭建章节（444/990 = 44.8%）

**是什么**：列出 Skill 运行前所需的工具、凭证和环境配置的章节。

**为什么**：44.8% 的 Top 1,000 Skill 包含此模式 — 仅次于编号步骤和决策表，排名第三。如果没有前置条件说明，Agent 会在执行过程中才发现缺少依赖项，浪费 token 在错误恢复上。提前列出前置条件可以在一开始就快速失败。

**怎么做**：创建 `## Prerequisites` 或 `## Setup` 章节，包含精确的安装命令和验证步骤。

**示例 Skill：**
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)：包含"First-Use Initialisation"章节，提供创建目录结构的 bash 命令
- [github](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/github/SKILL.md)：包含"Setup"章节，使用 `gh auth login` 和 `gh auth status`
- [gh-issues](https://raw.githubusercontent.com/openclaw/openclaw/main/skills/gh-issues/SKILL.md)：Token 解析序列，提供 3 条降级路径
- [polymarket-trade](https://clawhub.ai/skills/polymarket-trade)：API 密钥配置、钱包配置
- [skill-vetter](https://clawhub.ai/skills/skill-vetter)：将"Source Check"作为审查的前置条件

### 模式 29：安全审查清单（112/990 = 11.3%）

**是什么**：在信任 Skill 的输出或安装依赖之前，需要检查的安全危险信号清单。

**为什么**：11.3% 的 Top 1,000 Skill 包含安全/信任声明 — 是语料库平均水平（1.5%）的 **7.5 倍**。在 ClawHavoc 事件之后，顶级 Skill 通过信任声明来展示可靠性。[skill-vetter](https://clawhub.ai/skills/skill-vetter)（21.2 万次下载，ClawHub 排名第 2）本身就是一份完整的安全审查清单。

**怎么做**：包含 `## Security & Privacy` 或 `## Trust` 章节。声明：哪些数据会外传、哪些数据保存在本地、Skill 不会做什么。

**示例 Skill：**
- [skill-vetter](https://clawhub.ai/skills/skill-vetter)（21.2 万次下载）：完整的审查协议，包含危险信号清单、风险分级（🟢/🟡/🔴/⛔）和结构化审查报告
- [proactive-agent](https://clawhub.ai/skills/proactive-agent)（14.5 万次下载）："Security Hardening — Skill 安装审查、Agent 网络告警、上下文泄露防护"
- [review-code](https://clawhub.ai/skills/review-code)：外部端点表 + Security & Privacy 声明
- [github-actions](https://clawhub.ai/skills/github-actions)：外部端点 + Trust 章节

### 模式 30：提升 / 升级规则（52/990 = 5.3%）

**是什么**：定义何时将经验教训或发现从 Skill 本地存储"提升"到项目级或工作区级文件的规则。

**为什么**：由 [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)（39.8 万次下载，ClawHub 排名第 1）首创。核心思路：经验教训从本地开始积累，如果被证明具有广泛适用性，则提升到 CLAUDE.md、AGENTS.md 或其他项目文件中。这样就建立了一个学习层级体系。

**怎么做**：定义提升标准（例如"30 天内在 2 个以上任务中出现 3 次以上"）和提升目标。

**示例 Skill：**
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)：提升表 — 行为模式 → `SOUL.md`，工作流改进 → `AGENTS.md`，工具踩坑点 → `TOOLS.md`
- [proactive-agent](https://clawhub.ai/skills/proactive-agent)："Self-Improvement Guardrails — 通过 ADL/VFM 协议实现安全演化"
- [self-improving](https://clawhub.ai/skills/self-improving)（16.6 万次下载）：类似的提升模式
- [coding](https://clawhub.ai/skills/coding)：代码风格记忆，仅在明确指示时学习
- [decide](https://clawhub.ai/skills/decide)：决策模式，带有提升关卡

---

## 6.6 self-improving-agent 案例研究

ClawHub 上排名第 1 的 Skill（398,524 次下载，3,240 个 star，28 个版本）值得深入研究，因为它开创了多种如今被广泛模仿的模式。

### 结构

```
self-improving-agent/
├── SKILL.md (645 lines, 25 sections)
├── scripts/
│   ├── init.sh
│   ├── review.sh
│   └── promote.sh
└── references/
    ├── logging-format.md
    ├── detection-triggers.md
    └── hook-integration.md
```

### 源自此 Skill 的关键模式

1. **信号检测触发器**：该 Skill 定义了触发日志记录的自然语言模式 — "No, that's not right..."、"Actually..."、"A better approach..." — 并将每种映射到一个日志类别（correction、insight、knowledge_gap、best_practice）。

2. **结构化日志格式**：三种条目类型（`[lrn-YYYYMMDD-XXX]`、`[err-YYYYMMDD-XXX]`、`[feat-YYYYMMDD-XXX]`），每种类型有特定字段。

3. **提升层级体系**：`.learnings/`（本地）→ `CLAUDE.md` / `AGENTS.md` / `SOUL.md`（工作区级）→ 项目记忆。

4. **Hook 集成**：可选启用的 Hook（`PostToolUse`、`PreCompact`），无需手动调用即可自动触发日志记录。

5. **幂等初始化**：初始化脚本仅在目录结构不存在时才创建 — 在每次会话开始时运行都是安全的。

6. **隐私约束前置**："Do not log secrets, tokens, private keys... Prefer short summaries over raw output." — 放在初始化章节中，确保在任何日志记录之前被读取。

---

## 6.7 给 Skill 作者的核心启示

基于 Top 1,000 分析：

1. **结构比长度更重要**：顶级 Skill 比平均水平长 60%，但更关键的是它们的章节数多 64%。组织良好的内容 > 一堵文字墙。

2. **编号步骤是最常见的模式**（62.7%）：如果你的 Skill 包含操作流程，请为步骤编号。

3. **决策表是第二常见的模式**（51.3%）：顶级 Skill 至少包含一张用于分类或比较的表格。

4. **前置条件节省 token**：44.8% 的顶级 Skill 在开头列出前置条件。在开始时快速失败，而非在执行中途才发现问题。

5. **脚本让 Skill 具备可操作性**：33% 的 Skill 包含脚本。Python 是主流（占含脚本 Skill 的 56%），其次是 Bash（32%）。

6. **安全声明是顶级 Skill 的差异化因素**：顶级 Skill 中 11.3% vs 语料库平均 1.5%。ClawHavoc 事件之后，信任声明是质量的信号。

7. **下载量 ≠ 质量**：前 20 名中既有 ClawHub 上最精密的 Skill（self-improving-agent，645 行），也有近乎空壳的 Skill（sonoscli，27 行，零章节）。

8. **"何时不使用"的缺口**：仅 4.6% 的顶级 Skill 包含负向触发器 — 这是一个巨大的质量差距。添加负向触发器是大多数 Skill 最具杠杆效应的改进。
