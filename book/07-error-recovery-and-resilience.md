# Chapter 7: Error Recovery and Resilience — Skills That Survive Failure

## 7.1 Failure Is the Default

Long-running agents fail. Not occasionally—**systematically**. API calls time out. Rate limits hit. Tool outputs are malformed. The agent misinterprets instructions. External services go down. Files change between reads. Tests break for reasons unrelated to the agent's changes.

The question is not whether your skill will encounter failure, but whether it can recover. Skills designed for long-horizon tasks must treat error handling as a first-class architectural concern, not an afterthought.

## 7.2 The Five Failure Categories

ClawPod's production experience (scaling hundreds of agent runs per day) identified five fundamental failure categories:

| Category | Example | Correct Response |
|----------|---------|-----------------|
| **Transient** | Network timeout, 503 error | Retry with exponential backoff |
| **Rate limit** | 429 Too Many Requests | Wait for rate limit window, then retry |
| **Malformed output** | Agent produces invalid JSON, truncated response | Re-prompt with explicit format instructions |
| **Logic error** | Agent takes wrong branch, misinterprets task | Re-plan from current state |
| **Unrecoverable** | Missing credentials, permission denied, service down | Escalate to human with clear error description |

The critical insight: **not all failures are equal. Retrying a rate limit error is correct; retrying a logic error with the same approach is insanity.** Skills must classify failures before choosing recovery strategies.

## 7.3 Designing Skills for Recovery

### Pattern 1: Checkpoint-Based Recovery

Break the skill into phases that can be re-run independently:

```markdown
# Deployment Skill

## Phase 1: Validation
Run tests and linting. If this phase fails, stop and report.
This phase is safe to re-run at any time.

## Phase 2: Build
Create the production bundle. If this fails, re-run from Phase 1.

## Phase 3: Deploy
Push to staging. If this fails, the build is still valid—
re-run only this phase.

## Phase 4: Verify
Run smoke tests against staging. If this fails, 
check whether the failure is in deployment or in the code.
```

Each phase produces a verifiable intermediate result. If the agent's context is compacted mid-skill, it can determine which phase to resume from by examining the current state.

### Pattern 2: Explicit Failure Branching

```markdown
## Step 3: Run the test suite

Execute: `npm test`

If ALL tests pass:
  → Proceed to Step 4

If tests fail with COMPILATION errors:
  → The code has syntax errors. Fix them and re-run from Step 2.

If tests fail with RUNTIME errors:
  → Examine the failing test. If the failure is in your changed code,
    fix it and re-run. If the failure is in unrelated code, note it
    and proceed to Step 4.

If the test command itself fails (e.g., "command not found"):
  → Check that dependencies are installed. Run `npm install` 
    and retry once.
```

This pattern makes failure handling **explicit in the skill instructions**, not implicit in the agent's general reasoning.

### Pattern 3: Convergence Criteria

For iterative workflows, define what "done" looks like and what triggers exit:

```markdown
## Convergence Criteria

The refactoring is complete when:
1. All tests pass (zero failures)
2. The linter reports zero new warnings
3. Code coverage has not decreased
4. No function exceeds 50 lines

## Exit Conditions

Stop and report if:
- You have attempted the same fix 3 times without improvement
- Total execution time exceeds 30 minutes
- You encounter a dependency that cannot be resolved without
  human intervention
```

Without explicit convergence criteria, agents can loop indefinitely. Without exit conditions, they can burn tokens on unrecoverable situations.

## 7.4 The Self-Healing Pipeline

Production systems implement self-healing at the pipeline level, wrapping agent execution in recovery infrastructure:

```
┌────────────────────────────────────────────────────┐
│  SELF-HEALING PIPELINE                             │
│                                                    │
│  Task → Context Manager → Agent Execution          │
│                              ↓                     │
│                        Output Validator            │
│                              ↓                     │
│                    ┌── Pass → Deliver              │
│                    │                               │
│                    └── Fail → Classify Error        │
│                                   ↓                │
│                          ┌── Transient → Retry     │
│                          ├── Logic → Re-plan       │
│                          └── Fatal → Escalate      │
│                                                    │
│  Recovery Ledger: tracks what worked per error type │
└────────────────────────────────────────────────────┘
```

### The Recovery Ledger

The most powerful component is **memory of past failures**. A recovery ledger tracks:
- Which agent encountered which error type
- What resolution was attempted
- Whether the resolution succeeded

Over time, the pipeline learns: "When the developer agent hits a dependency conflict, the most successful resolution is to clear the cache and reinstall, not to modify the lockfile."

## 7.5 The PALADIN Framework

Academic research has formalized error recovery for tool-augmented agents. The PALADIN framework (2025) provides a systematic approach:

1. **Failure Taxonomy**: Seven recurring error patterns in tool use:
   - Tool hallucination (calling a tool that doesn't exist)
   - Argument hallucination (wrong parameter types or values)
   - Invalid tool invocation (calling tools out of sequence)
   - Partial tool execution (incomplete tool calls)
   - Tool output hallucination (misinterpreting results)
   - Invalid intermediate reasoning (wrong conclusions from correct data)
   - Re-entrant error handling failures (errors in error handling)

2. **Recovery-Annotated Training**: Training agents on 50,000+ trajectories that include failures and successful recoveries

3. **Retrieval-Based Recovery**: At runtime, matching current failures to similar past recovery examples

The key insight from PALADIN: **recovery capability can be systematically taught, not just engineered around**. Agents trained on failure trajectories develop robust recovery instincts.

## 7.6 The VIGIL Self-Healing Runtime

The VIGIL framework (December 2025) represents the state of the art in self-healing agent systems:

```
┌─────────────────────────────────────────────────┐
│                 VIGIL Runtime                    │
│  Log Ingestion → Appraisal → Decay → Diagnosis  │
│                                  ↓               │
│           Strategy Engine: Updates + Proposals   │
│                                  ↓               │
│                          Target Agent            │
└─────────────────────────────────────────────────┘
```

VIGIL's key innovation is **meta-procedural self-repair**: it can fix not just the target agent, but itself. When its own diagnostic tool fails, it surfaces the error, issues a fallback diagnosis, and emits a remediation plan.

Results in controlled environments:
- Premature success notifications: 100% → 0%
- Successful recovery from novel failure modes: significant improvement

## 7.7 Module-Specific Failure Taxonomy

Understanding where failures occur in the agent architecture enables targeted recovery:

| Module | Failure Type | Recovery Strategy |
|--------|-------------|-------------------|
| **Memory** | Hallucination (generates false info) | Re-query with explicit context |
| **Memory** | Retrieval failure (can't access stored info) | Fallback to explicit re-observation |
| **Planning** | Goal decomposition error | Re-plan with simpler subtasks |
| **Planning** | Step ordering error | Re-plan with explicit dependency graph |
| **Action** | Tool selection error (wrong tool) | Provide tool descriptions in retry prompt |
| **Action** | Tool execution error (right tool, wrong params) | Validate params against schema and retry |
| **Output** | Format error (invalid structure) | Re-prompt with explicit format example |
| **Output** | Completeness error (missing required content) | Re-prompt with checklist of required elements |

## 7.8 Practical Error Recovery Checklist for Skills

When authoring a skill for long-horizon tasks:

- [ ] Define explicit failure modes for each step
- [ ] Include recovery instructions for each failure mode
- [ ] Set convergence criteria (what "done" looks like)
- [ ] Set exit conditions (when to stop trying)
- [ ] Design phases that can be re-run independently
- [ ] Write state to files/tools, not just conversation history
- [ ] Include a maximum retry count for iterative steps
- [ ] Provide human escalation instructions for unrecoverable failures

---

### Sources for This Chapter

| Topic | Source |
|-------|--------|
| Self-healing pipeline (5 failure categories) | [dev.to: Self-Healing AI Agent Pipeline](https://dev.to/miso_clawpod/how-to-build-a-self-healing-ai-agent-pipeline-a-complete-guide-95b) |
| PALADIN framework (50K recovery trajectories) | [arXiv:2509.25238 (PALADIN)](https://arxiv.org/html/2509.25238v1) |
| VIGIL self-healing runtime | [zylos.ai: Error Handling & Recovery](https://zylos.ai/research/2026-01-12-ai-agent-error-handling-recovery) |
| Module-specific failure taxonomy | [zylos.ai: AgentErrorTaxonomy](https://zylos.ai/research/2026-01-12-ai-agent-error-handling-recovery) |
| OpenAI final-release-review gate policy | [raw SKILL.md](https://raw.githubusercontent.com/openai/openai-agents-python/main/.agents/skills/final-release-review/SKILL.md) |

## Key Takeaways

1. Long-running agents fail systematically. Skills must classify failures and respond appropriately.
2. The five failure categories (transient, rate limit, malformed output, logic error, unrecoverable) require five different responses.
3. Design skills with checkpoint-based recovery: independent phases with verifiable intermediate results.
4. Include explicit convergence criteria and exit conditions to prevent infinite loops.
5. Recovery capability can be trained (PALADIN) and automated (VIGIL), not just engineered.
6. Write critical state to persistent storage, not conversation history.
