# 第二部分，第 3 章：编写 Body（正文）

本章涵盖你在编写 SKILL.md 正文时需要做出的每一个结构性决策：章节顺序、指令风格、决策树、输入收集、输出模板、脚本和约束。每种技巧都配有生产级代码示例。

### 来源

| 来源 | URL |
|------|-----|
| 首因/近因效应研究 | [agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/) (ComplexBench NeurIPS 2024, IFScale 2025) |
| Anthropic Skill 编写最佳实践 | [platform.claude.com](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| OpenAI "优先使用指令而非脚本" | [developers.openai.com/codex/skills/create-skill](https://developers.openai.com/codex/skills/create-skill) |
| Gechev "逐步编号法" | [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) |
| 所有 OpenAI Agents SDK Skills | [github.com/openai/openai-agents-python/.agents/skills](https://github.com/openai/openai-agents-python/tree/main/.agents/skills) |
| `implementation-strategy` 全文 | [原始 SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) |
| `final-release-review` 全文 | [原始 SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md) |
| `docs-sync` 全文 | [原始 SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md) |
| `pr-draft-summary` 全文 | [原始 SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md) |
| `test-coverage-improver` 全文 | [原始 SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/test-coverage-improver/SKILL.md) |

---

## 3.1 章节顺序

每个 OpenAI SDK Skill 都遵循相同的章节排列：

```
1. Overview         — 一段话：做什么、为什么
2. Quick Start      — 压缩的 5-6 步快速路径
3. Workflow          — 带分支的完整编号步骤
4. Output Format     — 精确模板
5. Notes/Constraints — 边缘情况、护栏
```

这不是随意安排的。它利用了 LLM 处理指令的特性：

| 位置 | LLM 记忆强度 | 放什么内容 |
|------|-------------|-----------|
| 顶部 | 最强（首因效应） | Overview + 硬性约束 |
| 中上部 | 较好 | Quick Start / 正常路径 |
| 中部 | 最弱 | 详细工作流步骤 |
| 中下部 | 中等 | 输出格式 |
| 底部 | 较强（近因效应） | 边缘情况 + NEVER 规则 |

**Quick Start** 章节是一个关键模式：它为 Agent 提供了处理简单情况的快速路径。强模型可能只读这一部分。下面的完整 Workflow 负责处理边缘情况和复杂场景。

## 3.2 祈使语气

每条指令都应是命令，而不是描述：

```markdown
# ❌ Declarative:
The test suite should be run and results analyzed for regressions.

# ✅ Imperative:
1. Run `make tests` from the repository root.
2. If any test fails, report the failing test name and error.
3. If all tests pass, proceed to step 4.
```

OpenAI 的 `docs-sync` 工作流开头：

```markdown
1. Confirm scope and base branch
   - Identify the current branch and default branch (usually `main`).
   - If the current branch is not `main`, analyze only the diff
     vs `main` to scope doc updates.
```

每一行都以动词开头：Confirm、Identify、Analyze、Capture、Use、Walk、Review、Determine、Note、Detect、Produce、Ask、Edit、Build。

## 3.3 收集输入

顶级 Skill 会指定**精确的命令**来收集输入，并明确注明"(do not ask the user)"（不要询问用户）。

摘自 `pr-draft-summary`：

```markdown
## Inputs to Collect Automatically (do not ask the user)
- Current branch: `git rev-parse --abbrev-ref HEAD`
- Working tree: `git status -sb`
- Untracked files: `git ls-files --others --exclude-standard`
- Changed files: `git diff --name-only` and `git diff --name-only --cached`
- Latest release tag:
  LATEST_RELEASE_TAG=$(.agents/skills/final-release-review/scripts/
    find_latest_release_tag.sh origin 'v*' 2>/dev/null ||
    git tag -l 'v*' --sort=-v:refname | head -n1)
- Base reference:
  BASE_REF=$(git rev-parse --abbrev-ref --symbolic-full-name
    @{upstream} 2>/dev/null || echo origin/main)
```

这是一个关键模式：**为每个输入提供精确的 shell 命令**。不要说"查明你在哪个分支上"——而要说 `git rev-parse --abbrev-ref HEAD`。

摘自 `docs-sync`：

```markdown
- Use targeted search to find option types and feature flags:
  `rg "Settings"`, `rg "Config"`, `rg "os.environ"`, `rg "OPENAI_"`
```

给出具体的搜索命令，而不是"搜索与配置相关的代码"。

## 3.4 决策树

当工作流出现分支时，你必须显式地表达分支。以下是生产中的三种模式：

### 模式 A：If/Then 步骤

摘自 `docs-sync`：

```markdown
1. Confirm scope and base branch
   - If the current branch is not `main`, analyze only the
     diff vs `main` to scope doc updates.
   - Avoid switching branches if it would disrupt local changes;
     use `git show main:<file>` instead.
```

### 模式 B：类别 → 操作 对照表

摘自 `implementation-strategy`：

```markdown
## Compatibility boundary rules
- Released public API: preserve compatibility or migration path.
- Changes on current branch only: rewrite directly.
- Changes on `main` after latest release tag: rewrite directly.
- Internal helpers, private types: update directly.
```

### 模式 C：触发 / 非触发列表

摘自 `final-release-review`：

```markdown
Blocking triggers (at least one required for BLOCKED):
 - Confirmed regression or bug
 - Breaking API change with missing versioning
 - Data-loss or security-impacting change

Non-blocking by itself:
 - Large diff size
 - "Could regress" without evidence
 - Not running tests locally
```

非触发列表和触发列表同样重要。没有它，Agent 会因模糊的顾虑而阻塞流程。

## 3.5 输出模板

最好的 Skill 会定义**精确的输出格式**。

`final-release-review` — 完整的结构化模板：

```markdown
### Release readiness review (<tag> -> TARGET <ref>)
### Release call:
**<🟢 GREEN LIGHT TO SHIP | 🔴 BLOCKED>** <one-line rationale>
### Risk assessment (ordered by impact):
1) **<Finding title>**
   - Risk: **<🟢 LOW | 🟡 MODERATE | 🔴 HIGH>**
   - Evidence: <specific signal>
   - Files: <path(s)>
   - Action: <next step with pass criteria>
### Unblock checklist (required when BLOCKED):
1. [ ] <concrete check/fix>
   - Exit criteria: <what must be true>
```

`implementation-strategy` — 简洁的一行式：

```
Compatibility boundary: latest release tag v0.x.y;
branch-local interface rewrite, no shim needed.
```

`docs-sync` — 分类报告：

```markdown
## Docs Sync Report
- Doc-first findings: Page + missing content → evidence + location
- Code-first gaps: Feature + evidence → suggested doc page
- Incorrect/outdated: Doc file + issue + correct info + evidence
- Structural suggestions: Proposed change + rationale
- Proposed edits: Doc file → concise change summary
- Questions for the user
```

`pr-draft-summary` — 可直接粘贴的 PR 块：

```markdown
# Pull Request Draft
## Branch name suggestion
git checkout -b <suggestion>
## Title
<single-line imperative title>
## Description
<"This pull request resolves/updates/adds ...">
```

规则：**指定每个字段名、类型和示例值**。

## 3.6 审批关卡

对于会修改文件的 Skill，必须包含一个显式的暂停点：

```markdown
# docs-sync:
6. Produce a Docs Sync Report and ask for approval
7. If approved, apply changes (English only)

# test-coverage-improver:
5. Ask the user for approval; pause until they agree.
6. After approval, write the tests.

# gh-fix-ci:
6. Create a plan.
7. Implement after approval.
```

模式：分析步骤 → 报告 → "Ask"/"Pause" → 执行步骤 → 验证。

## 3.7 执行后验证

顶级 Skill 在执行操作后都包含验证步骤：

```markdown
# test-coverage-improver:
"After implementation: Rerun coverage, report the updated summary."

# docs-sync:
"Build docs with `make build-docs` after edits to verify
the docs site still builds."

# code-change-verification:
"Run the full verification sequence... Prefer this entry point."

# gh-fix-ci:
"After changes, suggest re-running the relevant tests
and `gh pr checks` to confirm."
```

## 3.8 使用 `references/` 存放深度内容

将 SKILL.md 控制在 500 行以内。把深度内容移到参考文件中：

```
# In SKILL.md:
"Walk through the categories in references/review-checklist.md"
"See references/cli.md for full command documentation"
"Open references/validation-matrix.md for case templates"
```

Agent 只有执行到对应步骤时才会读取参考文件。`references/` 中的文件在被显式打开之前不消耗任何 token。

OpenAI 的 Skill 目录结构：

```
docs-sync/
├── SKILL.md
├── agents/          # Codex-specific metadata
└── references/
    └── doc-coverage-checklist.md

imagegen/
├── SKILL.md
├── scripts/
│   └── image_gen.py
└── references/
    ├── cli.md
    ├── image-api.md
    ├── prompting.md
    ├── sample-prompts.md
    └── codex-network.md
```

## 3.9 约束语言

能可靠影响 LLM 行为的关键词：

| 关键词 | 强度 | 示例 |
|--------|------|------|
| NEVER / DO NOT | 硬性否定 | "Do not block a release solely because you did not run tests locally" |
| ALWAYS / MUST | 硬性肯定 | "Always use the fixed repository URL" |
| PREFER | 软性肯定 | "Prefer the console output from `coverage report -m`" |
| AVOID | 软性否定 | "Avoid switching branches if it would disrupt local changes" |

摘自 `final-release-review`：
```
"never produce a BLOCKED call without concrete evidence"
"Do not block a release solely because..."
"avoid variance between runs by using explicit gate rules"
```

## 3.10 反模式

| 反模式 | 为什么会失败 | 修复方法 |
|--------|-------------|---------|
| 大段文字 | Agent 无法提取步骤 | 使用编号步骤和标题 |
| "注意 X" | 过于模糊，无法执行 | "DO NOT X. Instead, do Y." |
| 工作流中没有分支 | Agent 在决策点卡住 | 为每个分支写明确的 if/then |
| 未声明输出格式 | 每次运行输出不一致 | 带占位符的精确模板 |
| "收集相关信息" | Agent 自己决定什么相关（往往很差） | 给出精确命令：`git status -sb`、`rg "Config"` |
| 所有内容都放在 SKILL.md 里 | 激活时 token 膨胀 | 详细内容放 `references/`，SKILL.md 只做导航 |
| Description 中没有跳过条件 | 对每个沾边的任务都会触发 | "Skip for docs-only changes" |

## 3.11 完整正文模板

```markdown
# [Skill Name]

## Overview
[One paragraph: what this does and when it matters.]

## Quick start
1. [Essential command with exact syntax]
2. [Key decision or check]
3. [Core action]
4. [Verification step]

## Workflow

### Gather
1. Collect [input A]: `[exact command]`
2. Collect [input B]: `[exact command]`
   - (do not ask the user)

### Analyze
3. [What to examine, organized by category]
4. Decision:
   - If [condition A]: → proceed to step 5
   - If [condition B]: → proceed to step 6
   - If [neither]: → report to user and stop

### Report
5. Output findings using the format below.
6. Ask the user for approval before modifying any files.

### Act (after approval)
7. [Specific action steps]
8. [Post-action verification command]
   - If verification fails: return to step [N]
   - After 3 failed attempts: report and stop

## Output format
[Exact template — every field named, typed, with example]

## Constraints
- NEVER [dangerous action]
- ALWAYS [critical requirement]
- If [edge case], then [specific handling]

## References
- `references/[name].md` — [what it covers and when to read it]
```
