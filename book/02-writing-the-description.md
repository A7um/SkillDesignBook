# Part II, Chapter 2: Writing the Description

The description is the only text the agent sees at startup for every installed skill. It is the routing decision boundary. This chapter shows how to write it, with production examples dissected.

### Sources

| Source | URL |
|--------|-----|
| Agent Skills specification (field constraints) | [agentskills.io/specification](https://agentskills.io/specification) |
| OpenAI: "Description is routing logic" | [developers.openai.com/blog/skills-shell-tips](https://developers.openai.com/blog/skills-shell-tips) |
| OpenAI `implementation-strategy` | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/implementation-strategy/SKILL.md) |
| OpenAI `docs-sync` | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/docs-sync/SKILL.md) |
| OpenAI `pr-draft-summary` | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/pr-draft-summary/SKILL.md) |
| OpenAI `code-change-verification` | [playbooks.com](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification) |
| Osmani `code-review-and-quality` | [GitHub](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md) |
| Gechev: routing test methodology | [github.com/mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) |

---

## 2.1 Constraints

- 1-1024 characters, non-empty
- Loaded at startup for ALL installed skills (~100 tokens each)
- This is the ONLY thing the agent reads before deciding to activate

## 2.2 Structure of a Production Description

Every top-tier description contains these components:

### Component 1: What it does (one sentence)

```
"Run the mandatory verification stack..."
"Decide how to implement runtime and API changes..."
"Analyze main branch implementation to find missing documentation..."
"Create the required PR-ready summary block..."
```

### Component 2: Positive triggers ("Use when...")

```
"Use when a task changes exported APIs, runtime behavior,
serialized state, tests, or docs..."

"Use when asked to audit doc coverage, sync docs with code,
or propose doc updates/structure changes."

"Use in the final handoff after moderate-or-larger changes
to runtime code, tests, examples, build/test configuration,
or docs with behavior impact"
```

### Component 3: Negative triggers / boundaries

Two sub-patterns:

**Explicit skip conditions:**
```
"skip only for trivial or conversation-only tasks,
repo-meta/doc-only tasks without behavior impact,
or when the user explicitly says not to"
```

**Scope boundaries:**
```
"Only update English docs under docs/** and never touch
translated docs under docs/ja, docs/ko, or docs/zh."
```

**Redirects to other skills:**
```
"Don't use for production deployments (use deploy-production).
Don't use for query optimization (use query-optimizer skill)."
```

## 2.3 The Six Production Descriptions, Annotated

### 1. `code-change-verification`

```yaml
description: >
  Run the mandatory verification stack when changes affect runtime
  code, tests, or build/test behavior in the OpenAI Agents Python
  repository.
```

- **What**: Run verification stack
- **When**: Changes affect runtime code, tests, or build/test behavior
- **Where**: In the OpenAI Agents Python repository (scoped to one repo)
- **Skip**: Implied — "when changes affect" means "skip when they don't"
- Length: 149 chars. Short, precise.

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

- **What**: Decide implementation approach before editing code
- **When**: Task changes APIs, runtime, serialized state, tests, or docs
- **Specific value**: "choose the compatibility boundary" — names the decision
- **Also triggers when**: "unreleased interfaces can be rewritten directly" — the answer might be "no shim needed," and the skill still triggers
- Length: 396 chars. Longer because the decision space is complex.

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

- **What**: Find missing/incorrect/outdated docs
- **When**: Asked to audit, sync, or propose doc changes
- **Boundary**: English only, never translated
- **Contract**: Report first, ask before editing
- Length: 397 chars. Includes behavioral contract in the description.

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

- **What**: Generate PR summary block
- **When**: Final handoff after moderate+ changes
- **Default**: ON by default — explicit "skip only for" list
- **Skip conditions**: Three specific cases enumerated
- Length: 454 chars. The skip-condition list is unusually detailed.

### 5. `test-coverage-improver`

```yaml
description: >
  Improve test coverage in the OpenAI Agents Python repository:
  run `make coverage`, inspect coverage artifacts, identify
  low-coverage files, propose high-impact tests, and confirm
  with the user before writing tests.
```

- **What**: Improve test coverage
- **How** (summarized in description): run coverage → inspect → identify → propose → confirm
- **Contract**: "confirm with the user before writing tests"
- Length: 227 chars. The workflow summary in the description helps routing.

### 6. Osmani `code-review-and-quality`

```yaml
description: >
  Conducts multi-axis code review. Use before merging any change.
  Use when reviewing code written by yourself, another agent, or
  a human. Use when you need to assess code quality across multiple
  dimensions before it enters the main branch.
```

- **What**: Multi-axis code review
- **When**: Before merging (any change, any author, any source)
- **Scope**: Multiple dimensions (elaborated in body)
- Length: 272 chars.

## 2.4 Before/After Rewrites

### Vague → Specific

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

### Too broad → Scoped

```yaml
# ❌ 
description: Reviews code for quality.

# ✅ 
description: >
  Conducts multi-axis code review covering correctness, readability,
  architecture, security, and performance. Use before merging any
  change. Don't use for formatting-only checks (use format-check).
```

### Abstract → Concrete trigger terms

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

### Missing contract → With behavioral contract

```yaml
# ❌ 
description: Finds documentation gaps.

# ✅ 
description: >
  Analyze codebase to find missing or outdated documentation.
  Provide a report and ask for approval before editing docs.
```

## 2.5 Testing Your Description

From [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices):

Prompt an LLM with ONLY the frontmatter:

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

If the LLM generates wrong triggers or can't distinguish from similar skills, rewrite.

## 2.6 Rules

1. Lead with what it does, not what it is
2. Include the concrete words users say ("deploy to staging", "audit doc coverage")
3. Add skip conditions when the skill is on-by-default
4. Add redirects when sister skills exist ("Don't use for X, use Y")
5. Include behavioral contracts when the skill modifies state ("report first, ask before editing")
6. Stay under 200 tokens — the description loads for every skill
7. Test routing before testing the body
