# Chapter 20: Writing the Description — The Most Important Line in Your Skill

The `description` field determines whether your skill is ever used. It is the **routing decision boundary**: the only text the agent reads at startup to decide if this skill is relevant. A perfect skill body with a bad description is invisible.

This chapter shows exactly how to write descriptions that trigger correctly, with before/after examples drawn from production skills.

### Sources for This Chapter

| Topic | Source |
|-------|--------|
| Description as routing logic | [OpenAI: Shell + Skills + Compaction Tips](https://developers.openai.com/blog/skills-shell-tips) |
| "Use when / Don't use when" pattern | [OpenAI: Codex Skill Creation](https://developers.openai.com/codex/skills/create-skill) |
| Trigger-optimized descriptions | [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) |
| Spec constraints (1-1024 chars) | [agentskills.io/specification](https://agentskills.io/specification) |
| OpenAI real descriptions | [openai/openai-agents-python/.agents/skills](https://github.com/openai/openai-agents-python/tree/main/.agents/skills) |
| Negative examples reduce misfires | [OpenAI blog](https://developers.openai.com/blog/skills-shell-tips) |

---

## 20.1 Constraints

- Maximum 1024 characters
- Non-empty
- Agent sees ONLY name + description at startup (~100 tokens per skill)

## 20.2 The Three Questions

Every description must answer:

1. **What does this skill do?** (one sentence)
2. **When should the agent use it?** (positive triggers)
3. **When should the agent NOT use it?** (negative triggers / redirects)

## 20.3 Anatomy of a Production Description

Here is OpenAI's `implementation-strategy` description, broken into its components:

```yaml
description: >
  Decide how to implement runtime and API changes in
  openai-agents-python before editing code.
  #──── WHAT it does ─────────────────────────────────

  Use when a task changes exported APIs, runtime behavior,
  serialized state, tests, or docs and you need to choose
  the compatibility boundary, whether shims or migrations
  are warranted, and when unreleased interfaces can be
  rewritten directly.
  #──── WHEN to use (positive triggers) ──────────────
```

Notice: no explicit "Don't use when" — but the positive trigger is so specific ("exported APIs, runtime behavior, serialized state") that it implicitly excludes everything else. This works when the trigger surface is well-defined.

Here is OpenAI's `docs-sync` description with explicit boundaries:

```yaml
description: >
  Analyze main branch implementation and configuration to find
  missing, incorrect, or outdated documentation in docs/.

  Use when asked to audit doc coverage, sync docs with code,
  or propose doc updates/structure changes.

  Only update English docs under docs/** and never touch
  translated docs under docs/ja, docs/ko, or docs/zh.

  Provide a report and ask for approval before editing docs.
```

This description has four parts:
1. What it does ("Analyze... to find missing/incorrect/outdated documentation")
2. Positive triggers ("audit doc coverage, sync docs with code, propose doc updates")
3. Scope constraint ("Only English docs... never touch translated docs")
4. Behavioral contract ("report and ask for approval before editing")

## 20.4 Before/After Examples

### Example 1: Vague → Specific

```yaml
# ❌ BAD: Vague, no triggers
description: Helps with deployment.

# ✅ GOOD: Specific triggers, negative boundary, behavioral contract
description: >
  Deploy the current branch to the staging environment via
  scripts/deploy.sh. Use when the user asks to deploy to staging,
  push to staging, or test changes in the staging environment.
  Don't use for production deployments (use deploy-production).
  Don't use for local testing. Runs tests before deploying and
  verifies the staging URL returns HTTP 200 after deployment.
```

### Example 2: Too broad → Scoped

```yaml
# ❌ BAD: Triggers on everything
description: Reviews code for quality and best practices.

# ✅ GOOD: Scoped to multi-axis review before merge
description: >
  Conducts multi-axis code review. Use before merging any change.
  Use when reviewing code written by yourself, another agent, or
  a human. Use when you need to assess code quality across multiple
  dimensions before it enters the main branch.
```
Source: [addyosmani/agent-skills code-review-and-quality](https://github.com/addyosmani/agent-skills/blob/main/skills/code-review-and-quality/SKILL.md)

### Example 3: Missing redirect → With redirect

```yaml
# ❌ BAD: No redirect for confusable tasks
description: >
  Run the test suite and report failures.

# ✅ GOOD: Explicit redirects for similar skills
description: >
  Run the mandatory verification stack when changes affect runtime
  code, tests, or build/test behavior in the OpenAI Agents Python
  repository.
```
Source: [openai/openai-agents-python code-change-verification](https://playbooks.com/skills/openai/openai-agents-python/code-change-verification)

(The AGENTS.md file handles the redirect by specifying *when* each skill triggers.)

### Example 4: Abstract → Concrete trigger terms

```yaml
# ❌ BAD: Abstract language
description: Assists with managing database schema evolution.

# ✅ GOOD: Concrete terms the agent can match
description: >
  Generate and run database migrations for schema changes using
  Alembic. Use when adding, modifying, or removing database tables,
  columns, indexes, or constraints. Use when the user mentions
  "migration", "schema change", "alter table", or "alembic".
  Don't use for query optimization (use query-optimizer skill).
  Don't use for seed data or fixtures (use data-seeding skill).
```

## 20.5 The Skip Condition Pattern

OpenAI's `pr-draft-summary` demonstrates how to specify when a skill should be skipped:

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

This is a "default on, explicit off" pattern: the skill runs by default for any substantial change, and skips only when one of three specific conditions is met.

## 20.6 Testing Your Description

From [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices):

Give an LLM ONLY the frontmatter:

```
I am building an Agent Skill. Agents decide whether to load
this skill based solely on the metadata below.

---
name: deploy-staging
description: [your description here]
---

Tasks:
1. Generate 3 user prompts that SHOULD trigger this skill.
2. Generate 3 user prompts that should NOT trigger this skill.
3. Generate 2 ambiguous prompts. Explain how you'd decide.
4. Is there any overlap with common skills like "test", "lint",
   "review", or "deploy-production"?
```

If the LLM generates wrong triggers or can't distinguish your skill from others, rewrite the description.

## 20.7 Rules of Thumb

1. **Lead with what it does**, not what it is
2. **Include concrete trigger words** that users actually say
3. **Add negative triggers** when there are confusable sister skills
4. **State behavioral contracts** ("reports first, asks before editing")
5. **Stay under 200 tokens** — the description loads for EVERY skill, so brevity matters at scale
6. **Test routing before testing the body** — a skill that doesn't trigger is useless regardless of quality
