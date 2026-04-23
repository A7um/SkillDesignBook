# 第二部分，第 2 章：编写 Description（描述）

Description 是 Agent 启动时对每个已安装 Skill 唯一能看到的文本。它是路由决策边界。本章展示如何编写它，附带生产案例的拆解。

### 来源

| 来源 | URL |
|------|-----|
| Agent Skills 规范（字段约束） | [agentskills.io/specification](https://agentskills.io/specification) |
| OpenAI："Description 是路由逻辑" | [developers.openai.com/blog/skills-shell-tips](https://developers.openai.com/blog/skills-shell-tips) |
| OpenAI `implementation-strategy` | [原始 SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) |
| OpenAI `docs-sync` | [原始 SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md) |
| OpenAI `pr-draft-summary` | [原始 SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md) |
| OpenAI `code-change-verification` | [playbooks.com](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification) |
| Osmani `code-review-and-quality` | [GitHub](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) |
| Gechev：路由测试方法论 | [github.com/mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) |

---

## 2.1 约束条件

- 1-1024 个字符，非空
- 启动时为所有已安装 Skill 加载（每个约 100 token）
- 这是 Agent 在决定激活之前读到的 **唯一内容**

## 2.2 生产级 Description 的结构

每个顶级 Description 包含以下组件：

### 组件 1：做什么（一句话）

```
"Run the mandatory verification stack..."
"Decide how to implement runtime and API changes..."
"Analyze main branch implementation to find missing documentation..."
"Create the required PR-ready summary block..."
```

### 组件 2：正向触发器（"在……时使用"）

```
"Use when a task changes exported APIs, runtime behavior,
serialized state, tests, or docs..."

"Use when asked to audit doc coverage, sync docs with code,
or propose doc updates/structure changes."

"Use in the final handoff after moderate-or-larger changes
to runtime code, tests, examples, build/test configuration,
or docs with behavior impact"
```

### 组件 3：负向触发器 / 边界

两种子模式：

**明确的跳过条件：**
```
"skip only for trivial or conversation-only tasks,
repo-meta/doc-only tasks without behavior impact,
or when the user explicitly says not to"
```

**范围边界：**
```
"Only update English docs under docs/** and never touch
translated docs under docs/ja, docs/ko, or docs/zh."
```

**重定向到其他 Skill：**
```
"Don't use for production deployments (use deploy-production).
Don't use for query optimization (use query-optimizer skill)."
```

## 2.3 六个生产级 Description 注解

### 1. `code-change-verification`

```yaml
description: >
  Run the mandatory verification stack when changes affect runtime
  code, tests, or build/test behavior in the OpenAI Agents Python
  repository.
```

- **做什么**：运行验证栈
- **何时**：变更影响运行时代码、测试或构建/测试行为时
- **哪里**：在 OpenAI Agents Python 仓库中（限定在一个仓库内）
- **跳过**：暗含的 — "当变更影响……"意味着"不影响时跳过"
- 长度：149 字符。简短、精确。

### 2. `implementation-strategy`

```yaml
description: >
  Decide how to implement runtime and API changes in
  openai-agents-python before editing code. Use when a task changes
  exported APIs, runtime behavior, serialized state, tests, or docs
  and you need to choose the compatibility boundary, whether shims
  or migrations are warranted, and when unreleased interfaces can
  be rewritten directly.
```

- **做什么**：在编辑代码之前决定实现方式
- **何时**：任务变更 API、运行时、序列化状态、测试或文档时
- **具体价值**："choose the compatibility boundary" — 命名了决策
- **也触发**："unreleased interfaces can be rewritten directly" — 答案可能是"不需要 shim"，但 Skill 仍然触发
- 长度：396 字符。更长是因为决策空间更复杂。

### 3. `docs-sync`

```yaml
description: >
  Analyze main branch implementation and configuration to find
  missing, incorrect, or outdated documentation in docs/. Use when
  asked to audit doc coverage, sync docs with code, or propose doc
  updates/structure changes. Only update English docs under docs/**
  and never touch translated docs under docs/ja, docs/ko, or
  docs/zh. Provide a report and ask for approval before editing docs.
```

- **做什么**：查找缺失/错误/过时的文档
- **何时**：被要求审计、同步或提议文档变更时
- **边界**：仅英文，从不触碰翻译文档
- **契约**：先报告，编辑前征求批准
- 长度：397 字符。在 Description 中包含了行为契约。

### 4. `pr-draft-summary`

```yaml
description: >
  Create the required PR-ready summary block, branch suggestion,
  title, and draft description for openai-agents-python. Use in
  the final handoff after moderate-or-larger changes to runtime
  code, tests, examples, build/test configuration, or docs with
  behavior impact; skip only for trivial or conversation-only
  tasks, repo-meta/doc-only tasks without behavior impact, or
  when the user explicitly says not to include the PR draft block.
```

- **做什么**：生成 PR 摘要块
- **何时**：中等及以上变更后的最终交接
- **默认**：默认开启 — 明确的"仅跳过"列表
- **跳过条件**：枚举了三种具体情况
- 长度：454 字符。跳过条件列表异常详细。

### 5. `test-coverage-improver`

```yaml
description: >
  Improve test coverage in the OpenAI Agents Python repository:
  run `make coverage`, inspect coverage artifacts, identify
  low-coverage files, propose high-impact tests, and confirm
  with the user before writing tests.
```

- **做什么**：提高测试覆盖率
- **怎么做**（在 Description 中概括）：运行覆盖率 → 检查 → 识别 → 提议 → 确认
- **契约**："confirm with the user before writing tests"
- 长度：227 字符。Description 中的工作流概要有助于路由。

### 6. Osmani `code-review-and-quality`

```yaml
description: >
  Conducts multi-axis code review. Use before merging any change.
  Use when reviewing code written by yourself, another agent, or
  a human. Use when you need to assess code quality across multiple
  dimensions before it enters the main branch.
```

- **做什么**：多维度代码审查
- **何时**：合并前（任何变更、任何作者、任何来源）
- **范围**：多个维度（在 Body 中详述）
- 长度：272 字符。

## 2.4 改写前后对比

### 模糊 → 具体

```yaml
# ❌
description: Helps with deployment.

# ✅
description: >
  Deploy the current branch to staging via scripts/deploy.sh.
  Use when the user asks to deploy to staging, push to staging,
  or test changes in the staging environment. Don't use for
  production deployments (use deploy-production skill).
```

### 过宽 → 有范围

```yaml
# ❌
description: Reviews code for quality.

# ✅
description: >
  Conducts multi-axis code review covering correctness, readability,
  architecture, security, and performance. Use before merging any
  change. Don't use for formatting-only checks (use format-check).
```

### 抽象 → 具体触发词

```yaml
# ❌
description: Assists with database schema evolution.

# ✅
description: >
  Generate and run Alembic migrations for schema changes.
  Use when adding, removing, or modifying tables, columns,
  indexes, or constraints. Don't use for query optimization
  (use query-optimizer) or seed data (use data-seeding).
```

### 缺少契约 → 包含行为契约

```yaml
# ❌
description: Finds documentation gaps.

# ✅
description: >
  Analyze codebase to find missing or outdated documentation.
  Provide a report and ask for approval before editing docs.
```

## 2.5 测试你的 Description

来自 [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices)：

用 **仅 frontmatter** 来提示 LLM：

```
I'm building an Agent Skill. The agent decides whether to load
this skill based solely on the metadata below.

---
name: deploy-staging
description: [your description]
---

1. Generate 3 user prompts that SHOULD trigger this skill.
2. Generate 3 user prompts that should NOT trigger this skill.
3. Generate 2 ambiguous prompts and explain your decision.
4. Does this overlap with "deploy-production", "test", or "lint"?
```

如果 LLM 生成了错误的触发器或无法区分类似的 Skill，请重写。

## 2.6 规则

1. 以它做什么开头，而不是它是什么
2. 包含用户会说的具体词语（"deploy to staging"、"audit doc coverage"）
3. 当 Skill 默认开启时添加跳过条件
4. 当存在姐妹 Skill 时添加重定向（"不要用于 X，使用 Y"）
5. 当 Skill 修改状态时包含行为契约（"先报告，编辑前征求批准"）
6. 保持在 200 token 以下 — Description 为每个 Skill 加载
7. 在测试 Body 之前先测试路由
