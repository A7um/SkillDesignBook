# Part II, Chapter 5: File Architecture, Scripts, and Testing Your Skill

### Sources

| Source | URL |
|--------|-----|
| Agent Skills spec (directory structure) | [agentskills.io/specification](https://agentskills.io/specification) |
| Anthropic: keep under 500 lines | [platform.claude.com best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) |
| Gechev: validation methodology | [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices) |
| OpenAI: skill directories | [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills/) |
| Cross-platform paths | [Devin skill discovery](https://docs.devin.ai/product-guides/skills) |

---

## 5.1 Directory Structure

```
skill-name/
├── SKILL.md              # Required: frontmatter + body
├── scripts/              # Optional: executable code
│   ├── run.sh            # Fail-fast verification
│   └── inspect.py        # Data gathering / API calls
├── references/           # Optional: deep documentation
│   ├── checklist.md      # Detailed checklists
│   ├── api-reference.md  # API parameter docs
│   └── examples.md       # Copy-paste examples
└── assets/               # Optional: templates, config
    └── template.md       # Output template
```

### How OpenAI organizes their skills

Simple skill (one script):
```
code-change-verification/
├── SKILL.md
└── scripts/
    ├── run.sh         # Unix
    └── run.ps1        # Windows
```

Complex skill (script + references):
```
docs-sync/
├── SKILL.md
├── agents/
│   └── openai.yaml    # Codex-specific metadata
└── references/
    └── doc-coverage-checklist.md
```

Rich media skill (script + many references):
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

## 5.2 Writing Scripts

Scripts handle deterministic operations. Rules:

1. **Non-interactive**: No prompts, no menus, no TTY input
2. **Idempotent**: Safe to run multiple times
3. **Fail-fast**: Exit on first error (`set -euo pipefail` in bash)
4. **No embedded secrets**: Use environment variables
5. **Documented I/O**: Clear what goes in, what comes out

From OpenAI `code-change-verification/scripts/run.sh` — the script runs the exact verification sequence:

```bash
#!/usr/bin/env bash
set -euo pipefail
# Fail-fast verification: format → lint → type-check → test
make format
make lint
make mypy
make tests
```

From `gh-fix-ci/scripts/inspect_pr_checks.py` — handles API drift:

```bash
# Usage:
python scripts/inspect_pr_checks.py --repo "." --pr "123"
python scripts/inspect_pr_checks.py --repo "." --pr "123" --json
```

The `--json` flag for machine-friendly output is a pattern worth copying — it lets other tools consume the script's output.

### Cross-skill references

Skills can call scripts from other skill directories:

```bash
BASE_TAG="$(.agents/skills/final-release-review/scripts/
  find_latest_release_tag.sh origin 'v*')"
```

This avoids duplicating shared logic. When the tag format changes, only one script updates.

## 5.3 Writing Reference Files

Reference files hold depth that would bloat SKILL.md. They load on demand (zero tokens until read).

### How to reference them from SKILL.md

```markdown
# Good: tells the agent WHEN to read the file
"Walk through the categories in references/review-checklist.md
when analyzing risk."

"Open references/validation-matrix.md when you need to design
the case matrix."

# Bad: agent might read it eagerly
"See references/checklist.md for more details."
```

The key: tell the agent *at which workflow step* to read the file, not just that it exists.

### What goes in references vs. SKILL.md

| In SKILL.md | In references/ |
|---|---|
| The workflow steps | Detailed checklists per step |
| "Classify the prompt into a taxonomy" | The full taxonomy with all categories |
| "Use the review checklist" | The 50-item checklist |
| "Follow prompting best practices" | The complete prompting guide |
| The output template (brief) | Extensive sample outputs |

## 5.4 Where to Put Skills (Cross-Platform)

Universal path that works everywhere:
```
.agents/skills/your-skill/SKILL.md
```

Platform-specific paths (all also scanned):

| Platform | Paths Scanned |
|----------|--------------|
| Claude Code | `.claude/skills/`, `.agents/skills/` |
| Cursor | `.cursor/skills/`, `.agents/skills/` |
| Codex | `.agents/skills/`, `.codex/skills/` |
| Devin | `.agents/skills/`, `.github/skills/`, `.cognition/skills/`, `.cursor/skills/`, `.claude/skills/`, `.codex/skills/` |
| Gemini CLI | `.agents/skills/` |

Source: [Devin skills docs](https://docs.devin.ai/product-guides/skills)

## 5.5 AGENTS.md Integration

Skills define *how* to do things. AGENTS.md defines *when* to do them. Put mandatory skill triggers in AGENTS.md:

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

Source: [AGENTS.md](https://github.com/openai/openai-agents-python/blob/main/AGENTS.md)

## 5.6 Testing Your Skill

### Step 1: Test the description (routing)

Prompt an LLM with ONLY the frontmatter. Ask it to generate trigger and non-trigger prompts. If it generates wrong triggers, rewrite the description before touching the body.

See [Chapter 2 §2.5](02-writing-the-description.md#25-testing-your-description) for the full prompt template.

### Step 2: Test the body (execution)

Run the skill against 3-5 representative tasks from your actual workflow. Record:

- Did the agent follow the workflow correctly?
- Did it produce output matching the template?
- Did it handle the decision branches correctly?
- Did it stop at the approval gate?
- Did it run verification after acting?

### Step 3: Analyze failure transcripts

Feed the transcript back to an LLM:

```
Review this agent transcript where it used the skill.
Identify:
- Where the instructions were ambiguous
- Where the agent deviated from the workflow
- Where additional guidance would help
- Where the agent followed instructions but the
  instructions led to a wrong outcome
```

### Step 4: Iterate and regression-test

Fix the skill based on observed failures. Re-run the same 3-5 tasks. Check that the fixes didn't break previously-working cases.

For automated regression testing, see [skillgrade](https://github.com/mgechev/skillgrade).

Source: [mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices)

## 5.7 Authoring Checklist

Before shipping a skill:

**Frontmatter:**
- [ ] `name` is lowercase-hyphenated and matches directory name
- [ ] `description` answers: what, when to use, when NOT to use
- [ ] Description tested with routing prompts

**Body:**
- [ ] Under 500 lines
- [ ] Hard constraints at top
- [ ] Quick start section
- [ ] Numbered workflow steps with imperative verbs
- [ ] All decision branches explicit (if/then)
- [ ] Input collection uses exact commands
- [ ] Output format is a template with field names
- [ ] Approval gate before any file modifications
- [ ] Verification step after modifications

**Scripts:**
- [ ] Non-interactive, idempotent, fail-fast
- [ ] No embedded secrets

**References:**
- [ ] SKILL.md says WHEN to read each reference file
- [ ] Detail is in references, not stuffed into SKILL.md

**Testing:**
- [ ] Description routing tested (3+ trigger, 3+ non-trigger)
- [ ] Body execution tested on 3+ real tasks
- [ ] Failure transcripts analyzed
