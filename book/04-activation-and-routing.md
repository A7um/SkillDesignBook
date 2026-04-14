# Chapter 4: Activation Accuracy — Getting the Right Skill at the Right Time

## 4.1 The Routing Problem

A skill that does not trigger reliably is broken, even if its body is excellent. Activation accuracy—the probability that the correct skill fires for a given task—is the single most important quality metric for a skill system.

The routing problem has two failure modes:

- **False negative**: The skill should have triggered but didn't. The agent proceeds without the relevant expertise, producing inferior results.
- **False positive**: The skill triggered when it shouldn't have. The agent loads irrelevant instructions, wasting context and potentially following incorrect procedures.

OpenAI's experience with Codex revealed a counterintuitive finding: **making skills available can initially reduce correct triggering**. Adding a new skill can confuse the routing model about when existing skills should (or shouldn't) fire. The solution is not fewer skills—it's better descriptions.

## 4.2 Writing Routing-Effective Descriptions

The description field is the routing contract. OpenAI's skill design guide and Anthropic's best practices converge on the same structure:

### The "Use When / Don't Use When" Pattern

```yaml
description: >
  Generate and run database migrations for schema changes. 
  Use when adding, modifying, or removing database tables or columns.
  Use when the user mentions "migration", "schema change", or "alter table".
  Don't use for query optimization (use query-optimizer skill).
  Don't use for seed data (use data-seeding skill).
```

This pattern works because it:
1. States the positive trigger clearly
2. Includes concrete trigger terms the model can match
3. Explicitly redirects to alternative skills for confusable tasks

### Negative Examples Prevent Misfires

OpenAI found that negative examples are the most effective tool for improving routing accuracy:

```yaml
description: >
  Refactor JavaScript code for readability and maintainability.
  Use when asked to clean up, simplify, or restructure JS/TS code.
  Don't use when:
  - The request is about fixing a bug (use debug skill)
  - The request is about performance optimization (use perf-optimizer)
  - The code is in a language other than JavaScript/TypeScript
```

The negative examples create a **decision boundary**: the model can see not just where this skill applies, but where its territory ends and another skill's begins.

### Concrete Trigger Terms Over Abstract Descriptions

```yaml
# Bad: Abstract
description: Assists with infrastructure management.

# Good: Concrete trigger terms
description: >
  Provision and configure AWS resources using Terraform.
  Use when the user mentions: Terraform, infrastructure as code, 
  AWS resource provisioning, EC2, S3, RDS, Lambda deployment.
  Don't use for Kubernetes/container orchestration (use k8s-deploy skill).
```

## 4.3 Testing Activation

Skill routing must be tested as deliberately as code logic. The recommended approach:

### 1. Define Positive Trigger Prompts
Write 5-10 prompts that should activate the skill:
- "Review the auth changes in this PR"
- "Check this code for security issues"
- "Do a code review of the latest commit"

### 2. Define Negative Trigger Prompts
Write 5-10 prompts that should NOT activate the skill:
- "Fix the formatting in this file" (formatting, not review)
- "Add a new feature to the auth module" (development, not review)
- "Run the test suite" (testing, not review)

### 3. Test Boundary Cases
Write prompts that are deliberately ambiguous:
- "Look at this code" (too vague—should the agent ask for clarification or activate?)
- "Check this PR" (could be review or CI/CD—depends on context)

### 4. Iterate on Description, Not Body
If routing is wrong, fix the description first. OpenAI's guidance: "If routing feels inconsistent, iterate on name, description, and examples before changing code."

## 4.4 Implicit vs. Explicit Invocation

Skills can be activated in two ways:

**Implicit invocation**: The agent autonomously decides to use the skill based on task-description matching. This is the default behavior.

**Explicit invocation**: The user directly names the skill (e.g., `$code-review` in Codex, `/code-review` in Cursor, `@skills:code-review` in Devin).

For high-stakes workflows where you need deterministic activation, the spec supports disabling implicit invocation:

```yaml
---
name: production-deploy
description: Deploy to production environment. ONLY use when explicitly requested.
disable-model-invocation: true
---
```

With `disable-model-invocation: true` (or `allow_implicit_invocation: false` in Codex's `openai.yaml`), the skill only fires on explicit user request. This is the right choice for:
- Destructive operations (database migrations, production deploys)
- High-cost workflows (full regression suites)
- Sensitive operations (security audits, compliance checks)

## 4.5 Skill Discovery Across Platforms

Each platform discovers skills from specific directories:

| Platform | Primary Location | Additional Locations |
|----------|-----------------|---------------------|
| **Claude Code** | `.claude/skills/` | `.agents/skills/`, `~/.claude/skills/` |
| **Cursor** | `.cursor/skills/` | `.agents/skills/`, `~/.cursor/skills/` |
| **Codex** | `.agents/skills/` | `~/.codex/skills/`, admin/system paths |
| **Devin** | `.agents/skills/` | `.github/skills/`, `.cognition/skills/`, 5 more paths |
| **Gemini CLI** | `.agents/skills/` | — |
| **Manus** | Skills tab in UI | Upload, marketplace, or "Package as Skill" |

The `.agents/skills/` directory is the universal path. If you write one skill, put it there for maximum portability across platforms.

## 4.6 The Routing Architecture

At a system level, skill routing is a classification problem. The agent must:

1. Parse the user's request
2. Compare it against all skill descriptions (Tier 1 metadata)
3. Select zero, one, or multiple matching skills
4. Load the selected skill(s) into context (Tier 2)
5. Execute the skill's instructions

Anthropic's routing recommendation: classify inputs and direct them to specialized handlers with **clearly distinct trigger conditions**. This is the same pattern used in customer service routing, API gateway design, and microservice architecture—applied to LLM context.

The implication for skill designers: **skills in the same domain must have clearly distinct trigger conditions**. If two skills might both match "help with the database," the descriptions must specify exactly which one handles which sub-domain.

## 4.7 Mandatory vs. Suggested Skills

OpenAI's Agents SDK repos demonstrate a pattern for ensuring critical skills always run: **mandatory skill rules in AGENTS.md**.

```markdown
# AGENTS.md

## Mandatory skill usage
- Use `$implementation-strategy` before editing runtime or API changes
  that may affect compatibility boundaries.
- Run `$code-change-verification` when runtime code, tests, examples,
  or build/test behavior changes.
- Use `$final-release-review` before any release.
```

This pattern uses AGENTS.md (always-loaded project guidance) to encode conditional triggers for skills. The skill's own description handles general routing; the AGENTS.md rule handles project-specific enforcement.

## Key Takeaways

1. Activation accuracy is the most important skill quality metric—a well-written body with a bad description is useless.
2. Use the "Use when / Don't use when" pattern with concrete trigger terms and negative examples.
3. Test routing with positive, negative, and boundary prompts before testing the skill body.
4. Put skills in `.agents/skills/` for maximum cross-platform portability.
5. Use `disable-model-invocation` for high-stakes operations that should only run on explicit request.
6. Encode mandatory skill usage in AGENTS.md for project-wide enforcement.
