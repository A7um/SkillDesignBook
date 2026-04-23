# 第二部分 · 第 5 章：目录怎么摆、脚本怎么写、Skill 怎么测

### 参考来源

| 来源 | 链接 |
|------|------|
| Agent Skills 规范（目录结构） | [agentskills.io/specification](https://agentskills.io/specification) |
| Anthropic：控制在 500 行以内 | [platform.claude.com best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| Gechev：验证方法论 | [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) |
| OpenAI：Skill 目录 | [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills/) |
| 跨平台路径 | [Devin skill discovery](https://docs.devin.ai/product-guides/skills) |

---

## 5.1 目录结构

```
skill-name/
├── SKILL.md              # 必需：frontmatter + 正文
├── scripts/              # 可选：可执行代码
│   ├── run.sh            # 快速失败验证
│   └── inspect.py        # 数据采集 / API 调用
├── references/           # 可选：深度文档
│   ├── checklist.md      # 详细检查清单
│   ├── api-reference.md  # API 参数文档
│   └── examples.md       # 可直接复制使用的示例
└── assets/               # 可选：模板、配置
    └── template.md       # 输出模板
```

### OpenAI 如何组织他们的 Skill

简单 Skill（单个脚本）：
```
code-change-verification/
├── SKILL.md
└── scripts/
    ├── run.sh         # Unix
    └── run.ps1        # Windows
```

复杂 Skill（脚本 + 参考文件）：
```
docs-sync/
├── SKILL.md
├── agents/
│   └── openai.yaml    # Codex 专用元数据
└── references/
    └── doc-coverage-checklist.md
```

富媒体 Skill（脚本 + 大量参考文件）：
```
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

## 5.2 编写脚本

脚本负责处理确定性操作。编写规则：

1. **非交互式**：不允许有提示输入、菜单选择或 TTY 输入
2. **幂等性**：多次运行必须安全无副作用
3. **快速失败**：遇到第一个错误即退出（bash 中使用 `set -euo pipefail`）
4. **禁止内嵌密钥**：通过环境变量传递
5. **输入输出有文档**：清楚说明输入什么、输出什么

OpenAI 的 `code-change-verification/scripts/run.sh`，一整条验证链路都写死在脚本里：

```bash
#!/usr/bin/env bash
set -euo pipefail
# Fail-fast verification: format → lint → type-check → test
make format
make lint
make mypy
make tests
```

`gh-fix-ci/scripts/inspect_pr_checks.py` 里，顺带把 API 变了怎么办也考虑进去：

```bash
# Usage:
python scripts/inspect_pr_checks.py --repo "." --pr "123"
python scripts/inspect_pr_checks.py --repo "." --pr "123" --json
```

`--json` 这种「给人看默认输出、给程序看加开关」的写法，很值得抄：别的工具也能直接吃脚本结果。

### 跨 Skill 引用

Skill 之间可以调用其他 Skill 目录下的脚本：

```bash
BASE_TAG="$(.agents/skills/final-release-review/scripts/
  find_latest_release_tag.sh origin 'v*')"
```

这样做避免了重复编写共享逻辑。当标签格式发生变化时，只需更新一个脚本即可。

## 5.3 编写参考文件

参考文件用于承载那些会使 SKILL.md 变得臃肿的深度内容。它们按需加载（在被读取之前不消耗任何 token）。

### 如何在 SKILL.md 中引用参考文件

```markdown
# Good: tells the agent WHEN to read the file
"Walk through the categories in references/review-checklist.md
when analyzing risk."

"Open references/validation-matrix.md when you need to design
the case matrix."

# Bad: agent might read it eagerly
"See references/checklist.md for more details."
```

关键在于：告诉 Agent *在工作流的哪个步骤*去读取文件，而不是仅仅告诉它文件存在。

### 哪些内容放在 references 中，哪些放在 SKILL.md 中

| 放在 SKILL.md 中 | 放在 references/ 中 |
|---|---|
| 工作流步骤 | 每个步骤的详细检查清单 |
| "将提示词分类到某个分类体系" | 包含所有类别的完整分类体系 |
| "使用审查检查清单" | 50 条审查项的完整清单 |
| "遵循提示词最佳实践" | 完整的提示词编写指南 |
| 输出模板（简要版） | 丰富的示例输出 |

## 5.4 Skill 文件的存放位置（跨平台）

适用于所有平台的通用路径：
```
.agents/skills/your-skill/SKILL.md
```

各平台特定路径（均会被扫描）：

| 平台 | 扫描路径 |
|------|---------|
| Claude Code | `.claude/skills/`, `.agents/skills/` |
| Cursor | `.cursor/skills/`, `.agents/skills/` |
| Codex | `.agents/skills/`, `.codex/skills/` |
| Devin | `.agents/skills/`, `.github/skills/`, `.cognition/skills/`, `.cursor/skills/`, `.claude/skills/`, `.codex/skills/` |
| Gemini CLI | `.agents/skills/` |

来源：[Devin skills docs](https://docs.devin.ai/product-guides/skills)

## 5.5 AGENTS.md 集成

Skill 定义的是*如何*做一件事。AGENTS.md 定义的是*何时*去做。将强制触发 Skill 的规则放在 AGENTS.md 中：

```markdown
# AGENTS.md (from OpenAI Agents SDK)

## Mandatory skill usage
- Run `$code-change-verification` when runtime code, tests,
  examples, or build/test behavior changes.
- Use `$implementation-strategy` before editing runtime or
  API changes that may affect compatibility boundaries.
- Use `$pr-draft-summary` when a task finishes with
  moderate-or-larger code changes.
```

来源：[AGENTS.md](https://github.com/openai/openai-agents-python/blob/main/AGENTS.md)

## 5.6 测试你的 Skill

### 第一步：测试描述（路由）

只将 frontmatter 提供给 LLM，让它生成触发和非触发提示词。如果它生成了错误的触发条件，先重写描述，再去修改正文。

完整的提示词模板请参见[第二章 §2.5](02-writing-the-description.md#25-testing-your-description)。

### 第二步：测试正文（执行）

用实际工作中的 3 到 5 个代表性任务来运行 Skill。记录以下内容：

- Agent 是否正确遵循了工作流？
- 它产出的结果是否符合模板要求？
- 它是否正确处理了决策分支？
- 它是否在审批关卡处停下来了？
- 它是否在执行操作后进行了验证？

### 第三步：分析失败记录

将对话记录反馈给 LLM：

```
Review this agent transcript where it used the skill.
Identify:
- Where the instructions were ambiguous
- Where the agent deviated from the workflow
- Where additional guidance would help
- Where the agent followed instructions but the
  instructions led to a wrong outcome
```

### 第四步：迭代与回归测试

根据观察到的失败情况修复 Skill，然后重新运行同样的 3 到 5 个任务，确认修复没有破坏之前已经正常工作的场景。

关于自动化回归测试，请参见 [skillgrade](https://github.com/mgechev/skillgrade)。

来源：[mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices)

## 5.7 发布前检查清单

发布 Skill 之前，请逐项确认：

**Frontmatter：**
- [ ] `name` 使用小写加连字符格式，且与目录名一致
- [ ] `description` 回答了：做什么、何时使用、何时不用
- [ ] 描述已通过路由提示词测试

**正文：**
- [ ] 不超过 500 行
- [ ] 硬性约束放在最前面
- [ ] 包含快速入门部分
- [ ] 工作流步骤使用编号 + 祈使动词
- [ ] 所有决策分支均已明确列出（if/then）
- [ ] 输入收集使用精确的命令
- [ ] 输出格式是包含字段名称的模板
- [ ] 在修改文件前设置审批关卡
- [ ] 在修改后设置验证步骤

**脚本：**
- [ ] 非交互式、幂等、快速失败
- [ ] 未内嵌密钥

**参考文件：**
- [ ] SKILL.md 明确说明了何时读取每个参考文件
- [ ] 细节内容放在 references 中，而非塞进 SKILL.md

**测试：**
- [ ] 描述路由已测试（至少 3 个触发 + 3 个非触发）
- [ ] 正文执行已在 3 个以上真实任务中测试
- [ ] 已分析失败记录
