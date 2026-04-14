# Chapter 2: Anatomy of a Skill — The SKILL.md Specification

## 2.1 The File Format

A skill is a directory containing, at minimum, a `SKILL.md` file:

```
skill-name/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── agents/
    └── openai.yaml   # Optional: platform-specific metadata
```

The `SKILL.md` file uses YAML frontmatter followed by a Markdown body:

```markdown
---
name: code-review
description: >
  Reviews code changes for bugs, security issues, and best practices.
  Use when the user asks for a code review or mentions reviewing changes.
  Don't use for simple formatting or style-only checks.
license: Apache-2.0
metadata:
  author: engineering-team
  version: "1.2"
allowed-tools: Read Grep Glob Bash(git:*)
---

# Code Review

When asked to review code, follow these steps:

## Step 1: Gather Context
Read the changed files and understand the scope of the change.

## Step 2: Security Analysis
Check for:
- SQL injection vulnerabilities
- XSS attack vectors
- Authentication/authorization gaps
- Exposed secrets or credentials

## Step 3: Logic Review
- Verify edge cases are handled
- Check error handling completeness
- Validate state management

## Step 4: Output
Organize findings by severity: Critical → Warning → Suggestion.
For each finding, include: file, line, issue description, and proposed fix.
```

## 2.2 Frontmatter Fields

The frontmatter is the skill's **routing contract**—the information agents use to decide whether to activate the skill.

### Required Fields

| Field | Constraints | Purpose |
|-------|------------|---------|
| `name` | 1-64 chars, lowercase `a-z0-9-`, no consecutive hyphens, must match parent directory | Unique identifier for discovery and invocation |
| `description` | 1-1024 chars, non-empty | The routing signal. Tells the agent when to use (and not use) this skill |

### Optional Fields

| Field | Purpose |
|-------|---------|
| `license` | SPDX license identifier |
| `compatibility` | Environment requirements (max 500 chars) |
| `metadata` | Arbitrary key-value map (author, version, tags) |
| `allowed-tools` | Space-separated list of pre-approved tools |
| `disable-model-invocation` | When `true`, skill only activates via explicit invocation |

### The `name` Field

The name is the skill's identity. It must match the parent directory name exactly. This constraint ensures filesystem consistency and prevents name collisions.

**Good names:**
- `code-review`
- `deploy-staging`
- `test-before-pr`

**Bad names:**
- `CodeReview` (uppercase not allowed)
- `my--skill` (consecutive hyphens)
- `-leading` (starts with hyphen)

### The `description` Field — The Most Important Line You'll Write

The description is not documentation. It is the **decision boundary** the model uses to route tasks to skills. At startup, the agent sees only names and descriptions for all installed skills. The quality of your description determines whether the right skill activates at the right time.

**Principles for effective descriptions:**

1. **Say what the skill does and when to trigger it**
2. **Include negative examples** ("Don't use when...")
3. **Use concrete trigger terms**, not marketing language
4. **Keep it under 200 tokens** for efficient routing

**Poor description:**
```yaml
description: Helps with PDFs.
```

**Good description:**
```yaml
description: >
  Extract text and tables from PDF files, fill PDF forms, and merge 
  multiple PDFs into one document. Use when the user asks about PDF 
  processing, text extraction from documents, or form filling.
  Don't use for image-only PDFs (use OCR skill instead) or for 
  creating new PDFs from scratch (use document-generation skill).
```

## 2.3 The Body — Instructions That Drive Execution

The Markdown body contains the actual procedural instructions. There are no format restrictions, but the body is loaded into the agent's context window when the skill activates, so every token counts.

### Recommended Structure

Based on research into primacy and recency effects in LLM instruction-following (documented by ComplexBench, NeurIPS 2024, and IFScale 2025):

| Section | Purpose | Placement Rationale |
|---------|---------|-------------------|
| Defaults and hard constraints | What must always/never happen | Top (primacy effect — strongest recall) |
| Step-by-step workflow | The core procedure | Middle (sequential processing) |
| Output format and artifacts | What success looks like | Near end |
| Edge cases and guardrails | Negative constraints | End (recency effect — strong recall) |

### Writing Effective Instructions

**Be imperative, not declarative.** Write steps as commands the agent should execute, not descriptions of what the skill conceptually does.

```markdown
# Bad: Declarative
This skill handles deployment by checking tests and pushing code.

# Good: Imperative
1. Run the full test suite: `npm test`
2. If any test fails, stop and report the failure.
3. Run the linter: `npm run lint`
4. Build the production bundle: `npm run build`
5. Deploy to staging: `./scripts/deploy.sh staging`
```

**Make inputs and outputs explicit.**

```markdown
## Inputs
- Branch name (from git context)
- Target environment (staging or production)

## Outputs
- Deploy URL
- Test results summary
- Any warnings or errors encountered
```

**Include explicit success criteria.**

```markdown
## Success Criteria
The deployment is successful when:
1. All tests pass with zero failures
2. The linter reports zero errors
3. The staging URL returns HTTP 200
4. Smoke tests pass against the staging endpoint
```

## 2.4 Scripts — Deterministic Execution

The `scripts/` directory contains executable code that the agent can run. Scripts are the bridge between natural-language instructions and deterministic behavior.

**When to use scripts:**
- The procedure requires exact, reproducible steps
- The workflow involves data transformation or computation
- You need deterministic behavior that shouldn't vary between runs

**When to prefer instructions over scripts:**
- The procedure requires judgment or adaptation
- The workflow varies significantly based on context
- The task benefits from model reasoning

```markdown
# In SKILL.md, reference the script:
Run the validation script to check all prerequisites:
scripts/validate-prerequisites.sh

If validation fails, report the specific failures to the user.
```

Scripts should be:
- **Non-interactive**: No prompts, no TTY input, no menus
- **Documented**: Clear inputs/outputs in comments or a companion README
- **Idempotent**: Safe to run multiple times
- **Self-contained**: Minimal external dependencies

## 2.5 References and Assets

The `references/` directory holds documentation the skill may need to consult. The `assets/` directory holds templates, configuration files, or other static resources.

These directories enable a critical pattern: **keeping SKILL.md lean while providing deep expertise on demand**. The agent reads SKILL.md first, then loads specific reference files only when needed.

```markdown
# In SKILL.md:
For the complete API specification, see references/api-spec.md
For response templates, use the templates in assets/templates/
```

This filesystem-based architecture is what makes progressive disclosure practical at scale.

## 2.6 Token Budget Guidelines

The specification recommends:

- **Metadata** (name + description): ~100 tokens per skill
- **SKILL.md body**: Under 5,000 tokens (under 500 lines)
- **Reference files**: Loaded only on demand, no inherent limit

For perspective: with 100 installed skills, the metadata layer costs approximately 10,000 tokens—about 5% of a 200K context window. The same skills loaded eagerly would cost 500,000 tokens—impossible in any current model.

## Key Takeaways

1. A skill is a directory with a required `SKILL.md` file plus optional `scripts/`, `references/`, and `assets/` directories.
2. The `description` field is the single most important line in a skill—it is the routing decision boundary.
3. Write descriptions with positive triggers ("Use when...") and negative triggers ("Don't use when...").
4. Structure the body for primacy/recency: hard constraints first, guardrails last.
5. Use scripts for deterministic behavior, instructions for judgment-requiring tasks.
6. Keep SKILL.md under 500 lines; move detailed references to separate files.

---

### Sources for This Chapter

| Topic | Source |
|-------|--------|
| SKILL.md specification (fields, constraints) | [agentskills.io/specification](https://agentskills.io/specification) |
| Primacy/recency effects on instruction-following | [agent-layer.dev/skill-design](https://agent-layer.dev/skill-design/) (refs ComplexBench, IFScale) |
| Anthropic skill authoring best practices | [platform.claude.com: Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| OpenAI skill creation docs | [developers.openai.com/codex/skills/create-skill](https://developers.openai.com/codex/skills/create-skill) |
| Real SKILL.md examples (imagegen, speech, doc) | [github.com/openai/skills](https://github.com/openai/skills/tree/main/skills/.curated) |
| What Is SKILL.md? Complete Guide | [dev.to: Complete Guide to Agent Skills](https://dev.to/samuel_rose_b30991db2b25b/what-is-skillmd-a-complete-guide-to-ai-agent-skills-2i93) |
