# 第 6 章：下载量前 1,000 的 Skill，数据里能看出什么

这一章把 **ClawHub 上按下载量排的前 1,000 个 Skill** 摊开看（排序数据来自 [ClawHub API](https://clawhub.atomicbot.ai/api/skills?sort=downloads&dir=desc)），再和 [openclaw/skills](https://github.com/openclaw/skills) 仓库里的 SKILL.md 对上号（全库一共 58,593 个 Skill）。

### 我们怎么做的

1. 用 ClawHub API 拉出下载量前 1,000 的列表  
2. 在本地克隆好的 `openclaw/skills` 里，给每个 Skill 找对应的 SKILL.md  
3. 对成功对上的 990 个跑了一遍脚本统计（有 10 个在仓库里没找到）  
4. 再人工细读了下载量前 20，看结构和写法  

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

**值得记住的一点**：下载量不等于质量。第 1 名的 `self-improving-agent`（约 39.8 万次下载，645 行，25 节，3 个脚本）写得很厚；但第 13 名的 `nano-pdf`（约 9.2 万次下载，才 21 行）和第 20 名的 `sonoscli`（约 7.8 万次下载，27 行、几乎没分节）也可以很「薄」却照样火。高下载往往和先发、传播有关，别把它当成质量认证章。

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

和全库平均比，前 1,000 这批 **平均多写约六成行数**、**章节多约六成**、**代码块多约七成**。看得出大家更愿意在「长得更像一本小手册」的 Skill 上花时间，但这是不是下载高的原因，这里不下结论。

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

**Top 1,000 里明显比全库更常见的写法**：
- **前置条件 / 环境搭建**（+25 个百分点）— 先把「开工前要有什么」说清楚
- **编号步骤**（+23 个百分点）— 偏流程，少空泛描述
- **决策表**（+21 个百分点）— 爱用表格做分类、对照
- **快速入门**（+19 个百分点）— 给一条能马上跑通的路径
- **故障排除**（+19 个百分点）— 会提前写「挂了怎么办」
- **安全与信任**（+10 个百分点）— 会交代数据怎么流、本地留什么
- **核心规则**（+6 个百分点）— 单独开一节把底线写死

---

## 6.4 脚本到底在干什么（结合头部 Skill 的阅读）

**Top 1,000 中有 327 个 Skill（33%）包含 `scripts/` 目录。** 在包含脚本的 Skill 中，平均每个 Skill 有 2.9 个脚本。

### 脚本语言分布

| 语言 | 数量 | 占含脚本 Skill 的百分比 |
|------|------|------------------------|
| Python | 183 | 56% |
| Bash/Shell | 105 | 32% |
| JavaScript/TypeScript | 39 | 12% |

### 脚本常见分工（来自对头部 Skill 的细读）

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

**为什么**：Top 1,000 里有 11.3% 写了安全/信任相关的话，是全库平均（1.5%）的 **7.5 倍**。ClawHavoc 之后，大家更习惯用「我怎么处理数据、我不干什么」来给自己背书。[skill-vetter](https://clawhub.ai/skills/skill-vetter)（约 21.2 万次下载，ClawHub 第 2）干脆整篇就是安全审查清单。

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

## 6.7 给 Skill 作者的几条实在话

对着 Top 1,000 这批数据，可以这么记：

1. **结构比篇幅更要紧**：平均是比全库长约六成，但章节数平均多六成这件事更说明问题——有条理，好过一堵字墙。

2. **能编号就编号**（62.7%）：只要有一串操作，就给步骤编号，Agent 跟起来省劲。

3. **表格很吃香**（51.3%）：至少放一张表，用来做分类或并排对比，很常见。

4. **前置条件别藏后面**（44.8%）：开头就把依赖、凭证、环境写清，能少烧一半「报错再救」的 token。

5. **脚本让 Skill 真能落地**：三分之一带 `scripts/`，其中 Python 约占六成、Bash 约占三成。

6. **安全/信任写一句，很加分**：头部样本里 11.3% 有这类段落，全库只有约 1.5%。社区被安全事件教育过之后，这几乎成了「像那么回事」的信号灯。

7. **下载量还是不等于质量**：前 20 里既有 600 多行的重器，也有二十来行、几乎没分节的「薄」Skill。

8. **「什么时候别用」是大片空白**：只有约 4.6% 写了负向触发。多数 Skill 若只改一处，往往就改这里，性价比最高。
