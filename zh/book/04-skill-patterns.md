# 第二部分 · 第 4 章：从前 1,000 个下载量 Skill 里归纳出的写法

这一章里的模式，都是对 **ClawHub 下载量前 1,000 的 Skill** 一条条对出来的（累计约 1,250 万次下载；其中 990 个对上了 SKILL.md，另有 889 个脚本被扫过）。

模式是**从数据里长出来的**，不是从哪本书抄目录。每条都尽量标了频次，并点到具体 Skill，方便你对照原文。

### 数据从哪来

- **ClawHub API**: [clawhub.atomicbot.ai/api/skills?sort=downloads&dir=desc](https://clawhub.atomicbot.ai/api/skills?sort=downloads&dir=desc)
- **Skills 仓库**: [github.com/openclaw/skills](https://github.com/openclaw/skills)（克隆了 58,593 个 Skill，其中 990 个匹配 top-1000）
- **分析的脚本**: 横跨 326 个含 `scripts/` 目录的 Skill，共 889 个文件

---

## 模式 A："API 脚手架" Skill（75 个，7.6%）

**定义**：一种一致的 7 段式结构，专门用于封装外部 API 的 Skill。这些段落以极高的共现率同时出现。

**证据**：67 个以上的 Skill 同时包含 `Authentication` + `Base URL` + `API Reference` 段落。68 个包含 `Base URL` + `Code Examples` + `Connection Management`。共现紧成这样，很难说是巧合，更像是大家互相抄出来的「行业默认骨架」。

**脚手架结构**：
```
## Quick Start
## Base URL
## Authentication
## Connection Management
## API Reference (or Commands)
## Code Examples
## Error Handling
## Rate Limits
## Notes / Troubleshooting
```

**为何有效**：API 类 Skill 有着共同的消费模式——Agent 先读认证设置，再读端点参考，然后看代码示例。偏离这一脚手架的 Skill 会让 Agent 四处寻找信息。

**示例 Skill：**
- [api-gateway](https://clawhub.ai/skills/api-gateway)（7 万次下载，635 行，124 个 API 引用）：标准脚手架
- [stripe-api](https://clawhub.ai/skills/stripe-api)（1.9 万次下载，4 个脚手架信号）：完整脚手架
- [gmail](https://clawhub.ai/skills/gmail)（3.1 万次下载，3 个信号）
- [outlook-api](https://clawhub.ai/skills/outlook-api)（2.1 万次下载，3 个信号）
- [whatsapp-business](https://clawhub.ai/skills/whatsapp-business)（2.1 万次下载，3 个信号）
- [stripe-best-practices](https://github.com/stripe/ai)（Stripe 官方 Skill）：相同脚手架
- [xero](https://clawhub.ai/skills/xero)（1.8 万次下载，3 个信号）
- [google-slides](https://clawhub.ai/skills/google-slides)（1.8 万次下载，3 个信号）

**何时使用此模式**：如果你的 Skill 封装了 HTTP API，请直接使用这个脚手架。不要另起炉灶。

---

## 模式 B："CLI 透传" Skill（约 150 个，约 15%）

**定义**：本质上是围绕某个已有 CLI 工具的薄层文字封装。特征：非常短（少于 60 行），0-3 个 `##` 段落，90% 以上是 bash 代码块，没有脚本。

**证据**：在下载量前 30 的 Skill 中，有 12 个不到 60 行。例如：`github`（48 行）、`gog`（37 行，0 个段落）、`weather`（50 行）、`nano-pdf`（21 行）、`sonoscli`（27 行）、`openai-whisper`（20 行）、`mcporter`（39 行）、`video-frames`（30 行）。

**最小结构**：
```markdown
# <tool-name>

One-sentence description of what the CLI does and when to use it.

Quick start
- `command1 arg` — what it does
- `command2 arg` — what it does

Common tasks
- `command3 arg` — what it does
```

**为何有效**：为一个设计良好的 CLI 写文档，不需要 500 行的 Skill。Skill 存在的意义是*告诉 Agent 这个 CLI 可用*，并展示 5-10 个常用调用方式。刻意填充到某个长度反而有害。

**示例 Skill：**
- [github](https://clawhub.ai/skills/github)（16 万次下载）：`gh` CLI，48 行
- [gog](https://clawhub.ai/skills/gog)（15.8 万次下载）：Google Workspace CLI，37 行，**零个 `##` 段落**
- [nano-pdf](https://clawhub.ai/skills/nano-pdf)（9.2 万次下载）：21 行，仅一个 `## Quick start`
- [sonoscli](https://clawhub.ai/skills/sonoscli)（7.8 万次下载）：27 行，无段落
- [openai-whisper](https://clawhub.ai/skills/openai-whisper)（7 万次下载）：20 行，无段落
- [mcporter](https://clawhub.ai/skills/mcporter)（5.7 万次下载）：39 行，无段落
- [video-frames](https://clawhub.ai/skills/video-frames)（4.2 万次下载）：30 行，2 个段落
- [youtube-watcher](https://clawhub.ai/skills/youtube-watcher)（4.4 万次下载）：49 行，3 个段落

**核心洞察**：下载量与篇幅并不相关。这些 Skill 各有 4.2 万至 16 万次下载，与 600 行以上的复杂 Skill 不相上下。

---

## 模式 C：描述中使用反引号包裹的命令标识符（30% 的 Skill）

**定义**：描述文本中通过反引号来引用具体的 CLI 工具或函数名称。

**证据**：top-1000 中 30% 的描述包含反引号包裹的字段名（例如 `` `gh` ``、`` `nano-pdf` ``、`` `wttr.in` ``）。27% 明确引用了某个特定的工具/CLI/API。

**原因**：反引号向 Agent 传达了"这个字符串就是你需要调用的东西"。当用户说"用 `gh` 检查 CI"时，Skill 描述也能进行字面匹配。

**示例 Skill：**
- [github](https://clawhub.ai/skills/github)："Interact with GitHub using the `gh` CLI."
- [mcporter](https://clawhub.ai/skills/mcporter)："Use the `mcporter` CLI..."
- [nano-pdf](https://clawhub.ai/skills/nano-pdf)："Edit PDFs...using the `nano-pdf` CLI."
- [obsidian](https://clawhub.ai/skills/obsidian)："...and automate via `obsidian-cli`."
- [weather](https://clawhub.ai/skills/weather)：提及 `wttr.in` 和 Open-Meteo
- [himalaya](https://clawhub.ai/skills/himalaya)："CLI to manage emails via IMAP/SMTP. Use `himalaya` to list, read..."

---

## 模式 D：箭头符号（`→`）表示因果关系（34% 的 Skill）

**定义**：使用 `→` 箭头字符来表示因果关系、输入/输出或问题/修复的对应关系。

**证据**：**339 个 Skill（34%）** 的内容中包含 `→`。这一比例远高于使用破折号（`—`）进行解释的模式。箭头专门用于表达方向性关系。

**原因**：箭头在视觉上清晰且含义明确。`Command --dry-run → preview only` 告诉 Agent"看到这个参数时，预期这个行为"，比任何文字叙述都快。

**示例 Skill：**
- [skill-vetter](https://clawhub.ai/skills/skill-vetter)：大量使用箭头的红旗列表——行为 → 拒绝决策
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)："Workflow improvements → Promote to `AGENTS.md`"
- [stock-analysis](https://clawhub.ai/skills/stock-analysis)：命令/选项 → 结果映射
- [proactive-agent](https://clawhub.ai/skills/proactive-agent)："Autonomous vs Prompted Crons → Know when to use systemEvent vs isolated agentTurn"

**使用方式**（来自 top-1000）：
- 命令 → 预期输出
- 输入/触发条件 → 要执行的操作
- 条件 → 目标/目的地
- 问题 → 修复方法

---

## 模式 E："Quick Start" 作为主要入口（21% 的 Skill）

**定义**：在标题之后紧接着放置一个 `## Quick Start` 段落，包含使用该 Skill 所需的最少命令。

**证据**：top-1000 中 21% 的 Skill 含有 `## Quick Start`——这是**出现频率最高的段落标题**。14% 有 `## Notes`，10% 有 `## Error Handling`，10% 有 `## Setup`。Quick Start 的出现频率几乎是第二名的两倍。

**原因**：Quick Start 是 Skill 的 ABI（应用二进制接口）。它用 3-6 条 bash 命令展示快乐路径。如果 Quick Start 能跑通，其他内容都是锦上添花。

**示例 Skill：**
- [nano-pdf](https://clawhub.ai/skills/nano-pdf)：整个 Skill 就是 `## Quick start` 加一个代码块
- [weather](https://clawhub.ai/skills/weather)：为两个服务提供 Quick Start（wttr.in + Open-Meteo）
- [video-frames](https://clawhub.ai/skills/video-frames)：Quick Start 中包含打包脚本的绝对路径
- [nano-banana-pro](https://clawhub.ai/skills/nano-banana-pro)：先"Quick start"再"Default Workflow"
- [playwright-mcp](https://clawhub.ai/skills/playwright-mcp)：Installation → Quick Start
- [brave-search](https://clawhub.ai/skills/brave-search)：Setup → Search
- [skill-creator](https://clawhub.ai/skills/skill-creator)（7.2 万次下载）：`## Quick start` 即第一步

**模板**：
```markdown
# <Skill Name>
One paragraph of what and when.

## Quick Start
```bash
<command 1>  # comment showing expected output
<command 2>
<command 3>
```
```

---

## 模式 F：脚本使用 `argparse` + `--json` 参数（Python，32% + 18%）

**定义**：top-1000 Skill 中的 Python 脚本压倒性地使用 `argparse` 来处理命令行参数，并且经常支持 `--json` 以输出机器可读的结果。

**证据**（来自 889 个分析过的脚本）：
- **32%** 的脚本使用 `argparse`
- **18%** 实现了 `--json` 输出参数
- **45%** 包含 `main()` 函数或 `if __name__ == "__main__":` 入口
- **12%** 包含帮助/用法输出函数
- 仅 **1%** 使用 `click`（更现代的替代方案）

**原因**：`argparse` 能生成一致的帮助文本。Agent 可以调用 `script.py --help` 并解析输出。`--json` 参数将面向人类的可读输出（默认）与机器可消费的输出分离——同一个脚本服务于两种受众。

**示例 Skill：**
- [gh-fix-ci](https://raw.githubusercontent.com/openai/skills/main/skills/.curated/gh-fix-ci/SKILL.md)（OpenAI）：`scripts/inspect_pr_checks.py` 支持 `--json`
- [stock-analysis](https://clawhub.ai/skills/stock-analysis)：7 个 Python 脚本，均使用 argparse
- [polymarket-trade](https://clawhub.ai/skills/polymarket-trade)：`scripts/polymarket.py`，完整的 argparse
- [nano-banana-pro](https://clawhub.ai/skills/nano-banana-pro)：`scripts/generate_image.py`，支持 `--prompt` / `--filename` 参数
- [tavily-search](https://clawhub.ai/skills/openclaw-tavily-search)：`scripts/tavily_search.py`，支持 `--query` / `--max-results`

---

## 模式 G：Bash 脚本使用 `set -euo pipefail`（17% 的脚本）

**定义**：Skill 中的 Bash 脚本采用快速失败模式：`set -e`（出错即退出）、`set -u`（未定义变量报错）和 `set -o pipefail`（管道失败向上传播）。

**证据**：**17%** 的分析脚本包含 `set -euo pipefail` 或其子集。**90%** 以 shebang 开头。仅 **10%** 使用了 `time.sleep`/速率限制。

**原因**：Agent 不总能区分部分成功和完全成功。一个在第 3 行失败但因管道静默失败而返回退出码 0 的 bash 脚本，会给 Agent 一个虚假的"成功"信号。`set -euo pipefail` 消除了这类故障模式。

**示例 Skill：**
- [code-change-verification](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification)（OpenAI）：`scripts/run.sh` 使用 `set -euo pipefail`
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)：`scripts/error-detector.sh` 在缺少环境变量时快速失败
- [pollyreach](https://clawhub.ai/skills/pollyreach)（9.6 万次下载）：6 个 bash 脚本均采用严格模式
- [github-deploy-skill](https://playbooks.com/skills/openclaw/skills/github-deploy-skill)：快速失败模式

---

## 模式 H：幂等初始化代码块（证据来自头部 Skill）

**定义**：初始化命令在创建之前先检查是否已存在，使得安装脚本可以安全地反复执行。

**证据**：虽然难以在整个语料库中精确统计，但下载量最高的记忆类 Skill 全部使用了此模式。

**原因**：Agent 默认不跨会话记忆。每次新会话中，Skill 可能重新执行初始化。如果初始化不是幂等的，重复执行就会覆盖用户数据。

**示例 Skill：**
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)（39.8 万次下载，ClawHub 排名第一）：
  ```bash
  mkdir -p .learnings
  [ -f .learnings/LEARNINGS.md ] || printf "# Learnings\n..." > .learnings/LEARNINGS.md
  [ -f .learnings/ERRORS.md ] || printf "# Errors\n..." > .learnings/ERRORS.md
  ```
  明确说明："Never overwrite existing files. This is a no-op if `.learnings/` is already initialised."
- [proactive-agent](https://clawhub.ai/skills/proactive-agent)：WAL 协议 + 幂等初始化
- [elite-longterm-memory](https://clawhub.ai/skills/elite-longterm-memory)：幂等的多层初始化
- [memory-setup](https://clawhub.ai/skills/memory-setup)：配置添加采用非破坏性合并

**标准的幂等 bash 模式**：
```bash
mkdir -p <dir>                           # -p = idempotent mkdir
[ -f <file> ] || echo "<content>" > <file>  # create only if missing
```

---

## 模式 I："概览/更新日志" 头部堆叠（5% 的 Skill）

**定义**：在 SKILL.md 顶部放置一组头部信息，展示版本号、最新版本的变更内容、前几个版本的变更——出现在任何工作流内容之前。

**证据**：在成熟的多版本头部 Skill 中观察到。[proactive-agent](https://clawhub.ai/skills/proactive-agent) 包含：`## What's New in v3.1.0` → `## What's in v3.0.0` → `## The Three Pillars`。[stock-analysis](https://clawhub.ai/skills/stock-analysis) 包含：`## What's New in v6.2` → `## What's in v6.1` → `## What's in v6.0`。[self-improving-agent](https://clawhub.ai/skills/self-improving-agent) 有 28 个版本，使用相同模式。

**原因**：Skill 会不断演进。回访的用户（或带有缓存上下文的 Agent）需要知道发生了哪些变化。将版本历史置于顶部确保差异内容最先被看到——在正文内容之前。

**示例 Skill：**
- [proactive-agent](https://clawhub.ai/skills/proactive-agent)："What's New in v3.1.0" / "What's in v3.0.0"
- [stock-analysis](https://clawhub.ai/skills/stock-analysis)：3 个 "What's in vN" 段落
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)：28 个版本，附带变更日志

**结构示例**：
```markdown
# Skill Name (optional emoji)
Brief tagline.

## What's New in v3.1.0
- Bullet 1
- Bullet 2

## What's in v3.0.0  (keep for context)
- Earlier features
```

---

## 模式 J："三大支柱" / 品牌化哲学开篇（头部 Skill）

**定义**：有的头部 Skill 一上来先抛一套「品牌感」很强的概念框架——常见是三条原则——实操细节统统往后放。好记，也好跟山寨货拉开距离。

**证据**：在最成熟的 top-20 Skill 中观察到，但在普通 Skill 中未见。

**示例 Skill：**
- [proactive-agent](https://clawhub.ai/skills/proactive-agent)（14.5 万次下载）："The Three Pillars — Proactive / Persistent / Self-improving"，配合 ✅ 符号
- [humanizer](https://clawhub.ai/skills/humanizer)（9.2 万次下载）：Personality/Content/Language/Style/Communication 五大支柱
- [elite-longterm-memory](https://clawhub.ai/skills/elite-longterm-memory)（5.2 万次下载）："5 Memory Layers" 框架
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)：Learnings/Errors/Features——3 种条目类型

**原因**：这其实是 SKILL.md 内部的营销。支柱框架让 Skill 令人印象深刻，并给用户提供了描述它的词汇。它传达的信号是"这个 Skill 有自己的立场"。

**何时使用**：仅适用于真正引入了新概念的 Skill。不要为简单的 API 封装生造支柱。

---

## 模式 K：积极的关联 Skill 交叉链接（5% 的 Skill）

**定义**：一个 `## Related Skills` 段落列出 4-8 个互补 Skill 及其安装命令，形成显式的 Skill 生态系统。

**证据**：top-1000 中 5% 有此段落——但在高产作者如 steipete（44 个 Skill）和 byungkyu（70 个 Skill）中，所有 Skill 都会交叉引用同系列的其他 Skill。

**原因**：Skill 协同使用效果更好。一个 `review-code` Skill 如果引用了 `git`、`typescript`、`ci-cd` 和 `devops`，就告诉了 Agent 完整的工具链。这产生了向上拉力：安装一个 Skill 会对该作者的其他 Skill 产生吸引力。

**示例 Skill：**
- [review-code](https://clawhub.ai/skills/review-code)：链接到 `code`、`git`、`typescript`、`ci-cd`、`devops`
- [docker](https://clawhub.ai/skills/docker)：链接到 devops、deploy、linux
- [word-docx](https://clawhub.ai/skills/word-docx)（ivangdavila）：链接到其他 Office 系列 Skill
- [excel-xlsx](https://clawhub.ai/skills/excel-xlsx)（ivangdavila）：相同模式——一致的作者风格

**格式示例**：
```markdown
## Related Skills

Install with `clawhub install <name>` if user confirms:

- `code` — implementation workflow that complements review findings
- `git` — safer branch, diff, and commit handling during remediation
- `typescript` — stricter typing and runtime safety review for TS-heavy codebases
```

---

## 模式 L：标题中的版本锁定（top-1000 中有 16 个）

**定义**：在 `# 标题` 中包含 Skill 的版本号，使版本在 Agent 的渲染视图中可见。

**证据**：top-1000 中有 16 个 Skill 的标题类似 `# Stock Analysis v6.1`、`# SkillScan v1.1.5`、`# Self-Improvement Skill`。频率较低但模式明确。

**原因**：当 Agent（或读者）在标题中看到版本号时，能立即判断该 Skill 是否符合预期。同时也传达了"这个 Skill 在持续维护"的信号。

**示例 Skill：**
- [stock-analysis](https://clawhub.ai/skills/stock-analysis)：`# Stock Analysis v6.1`
- [skillscan](https://clawhub.ai/skills/skillscan)：`# SkillScan v1.1.5`
- [proactive-agent](https://clawhub.ai/skills/proactive-agent)：版本号在第一个 `##` 段落中

---

## 模式 M：零段落 Skill（约 4%）

**定义**：下载量很高的 Skill 却**没有任何 `##` 段落标题**——只有一个标题、一段开头介绍和平铺的内容。

**证据**：top-1000 中 4% 的 Skill 没有 `##` 段落。这些并非低质量——它们是为封装简单工具而刻意采用的扁平结构。

**示例 Skill：**
- [gog](https://clawhub.ai/skills/gog)（15.8 万次下载）
- [sonoscli](https://clawhub.ai/skills/sonoscli)（7.8 万次下载）
- [openai-whisper](https://clawhub.ai/skills/openai-whisper)（7 万次下载）
- [mcporter](https://clawhub.ai/skills/mcporter)（5.7 万次下载）
- [blogwatcher](https://clawhub.ai/skills/blogwatcher)（3.5 万次下载）

**原因**：对于整个目的就是"这里有一个 CLI 工具和 5 条常用命令"的 Skill 来说，段落标题增加了结构却没有增加价值。扁平内容更易于浏览。

**启示**：段落层级是一种工具，而非硬性要求。当工作流有分支时使用它；对于线性内容则可以跳过。

---

## 模式 N：结构化的记忆条目 ID（先驱性，<1%）

**定义**：一种结构化的日志条目 ID 格式，支持跨会话的交叉引用和提升。格式：`[LRN-YYYYMMDD-XXX]`、`[ERR-YYYYMMDD-XXX]`、`[FEAT-YYYYMMDD-XXX]`。

**证据**：由 [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)（39.8 万次下载，ClawHub 排名第一，3,240 颗星）率先使用。现已被 [self-improving](https://clawhub.ai/skills/self-improving)（16.7 万次下载）及多个衍生 Skill 复用。

**原因**：记忆系统会不断积累条目。没有稳定的 ID，交叉引用就不可能——"昨天的那个修正"含糊不清。结构化 ID 使每条记录都可寻址、可提升、可删除。

**示例 Skill：**
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)：`[LRN-YYYYMMDD-XXX] category` / `[ERR-YYYYMMDD-XXX] skill_or_command_name` / `[FEAT-YYYYMMDD-XXX] capability_name`
- [self-improving](https://clawhub.ai/skills/self-improving)：类似的结构化 ID
- [hippocampus-memory](https://clawhub.ai/skills/hippocampus-memory)（3 千次下载，10 个脚本）：基于 ID 索引的记忆

**为何是先驱**：大多数记忆类 Skill 使用自由格式的时间戳。结构化 ID 使得机器可读的记忆操作成为可能——Skill 可以查询"过去 30 天内 category=correction 的所有 LRN 条目"。

---

## 模式 O：SKILL.md 中的提示词工程（约 15% 的 Skill）

**定义**：SKILL.md 包含以第一人称或第二人称直接向 Agent 发出指令的文本，例如"You are a writing editor..."或"When asked to review code..."。

**证据**：3% 使用第一人称（"You are a..."），但更广泛地看，约 15% 以第二人称对 Agent 说话（"When asked to..."、"You should..."）。

**原因**：这些 Skill 本质上就是 Agent 子任务的系统提示词。它们在给出操作步骤之前先设定角色人设。

**示例 Skill：**
- [humanizer](https://clawhub.ai/skills/humanizer)（9.2 万次下载）："# Humanizer: Remove AI Writing Patterns — You are a writing editor that identifies and removes signs of AI-generated text..."
- [admapix](https://clawhub.ai/skills/admapix)（8.1 万次下载）："You are an ad intelligence and app analytics assistant..."
- [clawddocs](https://clawhub.ai/skills/clawddocs)（3.6 万次下载）："You are an expert on Clawdbot documentation."

**句式结构**：`You are [role]. When [trigger], do [action].`——后接操作步骤。

---

## 模式 P：工作区注入的多文件记忆（先驱性）

**定义**：Skill 期望（并检查）工作区特定路径下的特定文件——`SOUL.md`、`AGENTS.md`、`TOOLS.md`、`MEMORY.md`——将它们视为不同类别的长期记忆。

**证据**：由 [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)（39.8 万次下载）率先使用。OpenClaw 平台在每次会话中注入这些文件。Skill 按类别将学习成果提升到相应文件中。

**示例 Skill：**
- [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)：按类别提升——行为类 → SOUL.md，工作流类 → AGENTS.md，工具注意事项 → TOOLS.md
- [proactive-agent](https://clawhub.ai/skills/proactive-agent)：相同的工作区文件集成
- [memory-setup](https://clawhub.ai/skills/memory-setup)：配置工作区文件注入

**原因**：只有一个 `MEMORY.md` 意味着 Agent 必须扫描所有内容来判断相关性。分类文件意味着 Agent 只需加载所需的类别。

---

## 模式频率汇总

| 模式 | 占 top-1000 比例 | 类型 |
|------|-----------------|------|
| E. Quick Start 作为主要入口 | 21% | 结构性 |
| D. 箭头符号（→） | 34% | 语法性 |
| C. 描述中的反引号命令标识符 | 30% | 描述性 |
| H. 幂等初始化（头部 Skill 中有证据） | 15%+ | 脚本类 |
| O. 第二人称 Agent 指令 | 15% | 语气类 |
| A. API 脚手架（7 个共现段落） | 7.6% | 模板类 |
| B. CLI 透传（<60 行） | 15% | 极简类 |
| F. argparse + `--json`（Python 脚本） | 32% + 18% | 脚本类 |
| G. `set -euo pipefail`（bash 脚本） | 17% | 脚本类 |
| K. 积极的交叉链接 | 5% | 生态类 |
| M. 零段落 Skill | 4% | 极简类 |
| I. 版本/更新日志头部堆叠 | 5% | 成熟度信号 |
| L. 标题中的版本号 | 1.6% | 成熟度信号 |
| N. 结构化记忆条目 ID | <1% | 先驱性 |
| P. 工作区注入的记忆文件 | <1% | 先驱性 |
| J. "三大支柱" 品牌化开篇 | <1% | 先驱性 |

### 核心要点

1. **API 脚手架**（模式 A）是一种习得的模板——如果你封装 API，请直接照搬。
2. **CLI 透传**（模式 B）是合理的做法——下载量前 6 的 Skill 中有 4 个不到 60 行。
3. **脚本是代码，不是散文**——32% 使用 argparse，45% 有 main()，17% 使用 bash 快速失败模式。
4. **箭头符号（→）是通用惯例**——34% 的头部 Skill 使用 `→` 表示因果关系。
5. **排名第一的 Skill 开创了三种模式**，且正在被广泛效仿：结构化记忆 ID、工作区文件提升和显式隐私约束。
