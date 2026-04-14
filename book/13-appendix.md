# Appendix A: Skill Authoring Checklist

## Before Writing

- [ ] Is this task actually repeatable enough to warrant a skill?
- [ ] Does a similar skill already exist in the project or marketplace?
- [ ] What is the one primary job this skill does?
- [ ] What does success look like?

## Frontmatter

- [ ] `name` uses lowercase-hyphenated format and matches the directory name
- [ ] `description` clearly states what the skill does
- [ ] `description` includes "Use when..." positive triggers
- [ ] `description` includes "Don't use when..." negative triggers
- [ ] `description` includes concrete trigger terms (not abstract language)
- [ ] `allowed-tools` specifies minimum required tools (least privilege)
- [ ] Optional: `disable-model-invocation: true` for high-stakes operations

## Body

- [ ] Body is under 500 lines
- [ ] Hard constraints and defaults appear at the top (primacy effect)
- [ ] Instructions are imperative ("Run X", not "X should be run")
- [ ] Inputs and outputs are explicitly defined
- [ ] Success criteria are concrete and verifiable
- [ ] Each step produces a verifiable intermediate result
- [ ] Guardrails and edge cases appear at the end (recency effect)
- [ ] No time-sensitive information that will become stale

## Error Handling

- [ ] Each major step has explicit failure recovery instructions
- [ ] Convergence criteria define what "done" looks like
- [ ] Exit conditions prevent infinite loops
- [ ] Maximum retry counts are specified for iterative steps
- [ ] Human escalation path exists for unrecoverable failures

## Scripts (if any)

- [ ] Scripts are non-interactive (no prompts, no TTY input)
- [ ] Scripts have documented inputs and outputs
- [ ] Scripts are idempotent (safe to re-run)
- [ ] Scripts contain no embedded secrets
- [ ] Scripts use absolute paths to prevent manipulation

## References

- [ ] SKILL.md serves as table of contents, not comprehensive manual
- [ ] Detailed reference material is in `references/` directory
- [ ] File references are one level deep (no deep nesting)
- [ ] Large templates are in `assets/` directory

## Testing

- [ ] 5-10 positive trigger prompts defined
- [ ] 5-10 negative trigger prompts defined
- [ ] Boundary cases identified and tested
- [ ] Routing accuracy verified before testing body
- [ ] Skill tested on at least 3 representative real-world tasks

## Security

- [ ] No embedded credentials, API keys, or secrets
- [ ] `allowed-tools` restricts to minimum necessary
- [ ] All external URLs are verified and necessary
- [ ] Scripts inspected for obfuscation or suspicious patterns
- [ ] Network access is justified and documented

---

# Appendix B: Reference Skill Examples

## Example 1: Test Before PR (Minimal)

```markdown
---
name: test-before-pr
description: >
  Run the full test suite and linter before opening a pull request.
  Use when the user is about to create a PR or asks to verify 
  code before submission. Don't use for mid-development test runs 
  or debugging individual test failures.
---

# Test Before PR

1. Identify the test command from package.json, Makefile, or AGENTS.md
2. Run the full test suite
3. Run the linter
4. If any failures exist, report them clearly with file and line numbers
5. If all pass, confirm readiness for PR

## Success Criteria
- All tests pass (zero failures)
- Linter reports zero errors (warnings are acceptable)
- Report is clear and actionable
```

## Example 2: Code Review (With Scripts)

```markdown
---
name: code-review
description: >
  Review code changes for bugs, security issues, and best practices.
  Use when the user asks for a code review, mentions reviewing changes,
  or wants feedback on a PR. Don't use for style-only formatting 
  (use format-check skill). Don't use for performance analysis 
  (use perf-review skill).
allowed-tools: Read Grep Glob Bash(git:*)
---

# Code Review

## Step 1: Gather Changes
Run `scripts/gather-changes.sh` to collect the diff.

## Step 2: Security Scan
For each changed file, check for:
- SQL injection patterns (string concatenation in queries)
- XSS vulnerabilities (unsanitized user input in HTML)
- Authentication gaps (missing auth checks on endpoints)
- Exposed secrets (hardcoded keys, tokens, passwords)

## Step 3: Logic Review
- Verify edge cases (null inputs, empty collections, boundary values)
- Check error handling (are all error paths covered?)
- Validate state management (race conditions, stale data)

## Step 4: Report
See references/report-template.md for the output format.
Organize by severity: Critical → Warning → Suggestion.

## When to Escalate
If you find a Critical security issue, recommend blocking the PR 
and notifying the security team immediately.
```

## Example 3: Deploy Staging (With Explicit Recovery)

```markdown
---
name: deploy-staging
description: >
  Deploy the current branch to the staging environment.
  Use when the user asks to deploy to staging, push to staging,
  or test in staging. Don't use for production deployments 
  (use deploy-production skill). Don't use for local testing.
disable-model-invocation: true
---

# Deploy to Staging

## Prerequisites
- All tests must pass (run test-before-pr skill first if unsure)
- Branch must be pushed to remote

## Phase 1: Build (safe to re-run)
1. Run `npm run build`
2. Verify build output exists in `dist/`
3. If build fails → report error and stop

## Phase 2: Deploy (safe to re-run)
1. Run `scripts/deploy.sh staging`
2. Wait for deployment to complete (max 5 minutes)
3. If deployment fails:
   - Check if it's a timeout → retry once
   - Check if it's a config error → report the specific error
   - Check if staging is down → report infrastructure issue

## Phase 3: Verify
1. Run `scripts/smoke-test.sh staging`
2. Verify HTTP 200 from staging URL
3. If smoke tests fail:
   - Check if it's a known flaky test → note and proceed
   - Check if it's a real failure → report and recommend rollback

## Success Criteria
- Build completes without errors
- Deployment succeeds
- Staging URL returns HTTP 200
- Smoke tests pass (or flaky tests are noted)
```

---

# Appendix C: Platform Quick Reference

## Skill Directories by Platform

| Platform | Primary Path | Compatibility Paths |
|----------|-------------|-------------------|
| Claude Code | `.claude/skills/` | `.agents/skills/` |
| Cursor | `.cursor/skills/` | `.agents/skills/` |
| Codex | `.agents/skills/` | `.codex/skills/` |
| Devin | `.agents/skills/` | `.cognition/skills/`, `.cursor/skills/`, `.claude/skills/`, `.codex/skills/`, `.github/skills/` |
| Gemini CLI | `.agents/skills/` | — |
| Manus | Via UI or `.agents/skills/` | — |

**Universal path**: `.agents/skills/` works across all platforms.

## Related Configuration Files

| File | Purpose | Scope |
|------|---------|-------|
| `AGENTS.md` | Always-on project guidance | Cross-platform |
| `CLAUDE.md` | Claude Code project memory | Claude Code |
| `.cursor/rules/` | Always-on Cursor rules | Cursor |
| `agents/openai.yaml` | Codex UI metadata and policies | Codex |

## Validation Tools

- `skills-ref validate ./my-skill` — Validates SKILL.md frontmatter
- `npx skills init [name]` — Scaffolds a new skill directory
- `mcp-scan` — Scans skills for security issues (Snyk)
- `/migrate-to-skills` — Converts Cursor rules to skills (Cursor 2.4+)

---

# Appendix D: Glossary

**A2A (Agent-to-Agent)**: Google's protocol for agent discovery and task delegation. Complements MCP.

**Activation accuracy**: The probability that the correct skill fires for a given task.

**AGENTS.md**: A cross-platform file for always-on project guidance, loaded before every agent task.

**Agent Skills**: The open standard (agentskills.io) for portable, versioned agent capabilities.

**Compaction**: Summarizing older conversation turns to free context window space for new work.

**Context engineering**: The discipline of curating the optimal set of tokens for LLM inference.

**Context window**: The fixed-size token budget available for all input and output in a single inference.

**MCP (Model Context Protocol)**: Anthropic's open protocol for connecting agents to external tools and data sources.

**Meta-skill**: A skill that orchestrates other skills in sequence, parallel, or conditional patterns.

**Progressive disclosure**: Loading information in tiers based on relevance—metadata first, full instructions on activation, resources on demand.

**SKILL.md**: The manifest file for an Agent Skill, containing YAML frontmatter and Markdown instructions.

**Subagent**: A child agent spawned by a parent agent with its own context window, tool access, and mission.

**Tool Search Tool**: Anthropic's mechanism for dynamic tool discovery, loading tool definitions on demand rather than upfront.

---

# Appendix E: Further Reading

## Primary Sources

- **Agent Skills Specification**: https://agentskills.io/specification
- **Anthropic: Building Effective Agents** (Dec 2024): https://anthropic.com/engineering/building-effective-agents
- **Anthropic: Context Engineering for Agents** (Sep 2025): https://anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **Anthropic: Code Execution with MCP** (Nov 2025): https://anthropic.com/engineering/code-execution-with-mcp
- **Anthropic: Advanced Tool Use** (Nov 2025): https://anthropic.com/engineering/advanced-tool-use
- **OpenAI: Skills + Shell + Compaction Tips**: https://developers.openai.com/blog/skills-shell-tips
- **OpenAI: Using Skills to Accelerate OSS Maintenance**: https://developers.openai.com/blog/skills-agents-sdk
- **OpenAI: AGENTS.md Guide**: https://developers.openai.com/codex/guides/agents-md
- **Google ADK Overview**: https://cloud.google.com/agent-builder/agent-development-kit/overview
- **Cursor Agent Best Practices**: https://cursor.com/blog/agent-best-practices
- **OWASP Agentic Skills Top 10**: https://owasp.org/www-project-agentic-skills-top-10/

## Academic Papers

- Jiang et al. (2026). "SoK: Agentic Skills — Beyond Tool Use in LLM Agents." arXiv:2602.20867
- Xu et al. (2026). "Agent Skills for LLMs: Architecture, Acquisition, Security, and the Path Forward." arXiv:2602.12430
- "Adaptation of Agentic AI: A Survey of Post-Training, Memory, and Skills." arXiv:2512.16301
- "Measuring AI Ability to Complete Long Tasks." arXiv:2503.14499
- "PALADIN: Self-Correcting Language Model Agents to Cure Tool-Failure Cases." arXiv:2509.25238
- "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?" arXiv:2509.16941
- "Trajectory-Informed Memory Generation for Self-Improving Agent Systems." arXiv:2603.10600
- ComplexBench (NeurIPS 2024): Constraint composition degrades performance
- IFScale (2025): Three degradation patterns as instruction density increases
- "Same Task, More Tokens" (ACL 2024): Accuracy drops from 0.92 to 0.68 with prompt length

## Community Resources

- Agent Skills GitHub: https://github.com/agentskills/agentskills
- OpenAI Skills Repository: https://github.com/openai/skills
- Manus Skills Architecture: https://github.com/abcnuts/manus-skills
- Snyk ToxicSkills Report: https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub
