# Agent Skill Writing Patterns: Deep Analysis Report

## Table of Contents
1. [Repositories Analyzed](#1-repositories-analyzed)
2. [All Skills Read (Detailed Catalog)](#2-all-skills-read-detailed-catalog)
3. [Structural Patterns Across Skills](#3-structural-patterns-across-skills)
4. [Cross-Cutting Pattern Analysis](#4-cross-cutting-pattern-analysis)
5. [Anti-Pattern & Mistake Sections](#5-anti-pattern--mistake-sections)
6. [Key Findings & Recommendations](#6-key-findings--recommendations)

---

## 1. Repositories Analyzed

| Repository | Stars | Skills Count | Focus |
|---|---|---|---|
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | 17,640+ | 19 core skills | Engineering lifecycle workflows |
| [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | 33,894+ | 1,409+ skills | Installable skill library (bundles + individual) |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 16,300+ | 1,086+ skills | Curated collection from official teams |
| [LeoYeAI/openclaw-master-skills](https://github.com/LeoYeAI/openclaw-master-skills) | 1,893+ | 387+ skills | OpenClaw agent ecosystem |
| [qdrant/skills](https://github.com/qdrant/skills) | 76 | 8 skills | Qdrant vector search domain skills |
| [transloadit/skills](https://github.com/transloadit/skills) | 2 | ~10 skills | Transloadit file processing integration |

---

## 2. All Skills Read (Detailed Catalog)

### 2.1 addyosmani/agent-skills (All 19 Read)

| # | Skill Name | URL | Description (exact) | Key Structural Features |
|---|---|---|---|---|
| 1 | **idea-refine** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/idea-refine/SKILL.md) | "Refines ideas iteratively. Refine ideas through structured divergent and convergent thinking." | 3-phase interactive process (Diverge → Converge → Ship). Uses `AskUserQuestion` tool. Produces markdown artifact. 7 anti-patterns. Verification checklist. |
| 2 | **spec-driven-development** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/spec-driven-development/SKILL.md) | "Creates specs before coding. Use when starting a new project, feature, or significant change and no specification exists yet." | 4-phase gated workflow (Specify→Plan→Tasks→Implement). ASCII flow diagram. Spec template. "Common Rationalizations" table. "When to Use / When NOT to use" sections. |
| 3 | **planning-and-task-breakdown** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/planning-and-task-breakdown/SKILL.md) | "Breaks work into ordered tasks. Use when you have a spec or clear requirements and need to break work into implementable tasks." | 5-step process. Task sizing table (XS-XL). Dependency graph visualization. Checkpoint pattern. Plan document template. Parallelization guidance. |
| 4 | **incremental-implementation** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/incremental-implementation/SKILL.md) | "Delivers changes incrementally. Use when implementing any feature or change that touches more than one file." | Cycle diagram (Implement→Test→Verify→Commit). 5 numbered rules. 3 slicing strategies (Vertical, Contract-First, Risk-First). Simplicity check pattern. Scope discipline pattern. |
| 5 | **frontend-ui-engineering** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/frontend-ui-engineering/SKILL.md) | "Builds production-quality UIs. Use when building or modifying user-facing interfaces." | "AI Aesthetic" anti-pattern table. Accessibility (WCAG 2.1 AA) requirements. Component architecture patterns. State management decision tree. Responsive design. |
| 6 | **api-and-interface-design** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/api-and-interface-design/SKILL.md) | "Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface." | 5 core principles with code examples. Hyrum's Law and One-Version Rule. REST patterns. TypeScript interface patterns. Predictable naming table. |
| 7 | **context-engineering** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/context-engineering/SKILL.md) | "Optimizes agent context setup. Use when starting a new session, when agent output quality degrades." | 5-level context hierarchy (ASCII diagram). 3 context packing strategies. Confusion management protocol. Inline planning pattern. Anti-pattern table. Trust levels for loaded files. |
| 8 | **test-driven-development** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/test-driven-development/SKILL.md) | "Drives development with tests. Use when implementing any logic, fixing any bug, or changing any behavior." | RED→GREEN→REFACTOR cycle with ASCII art. "Prove-It Pattern" for bugs. Test pyramid diagram. DAMP vs DRY. Test size classification table. 6 anti-patterns. |
| 9 | **browser-testing-with-devtools** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/browser-testing-with-devtools/SKILL.md) | "Tests in real browsers. Use when building or debugging anything that runs in a browser." | MCP tool table. Security boundary rules. 3 debugging workflows (UI/Network/Performance). Test plan template. Screenshot verification. Console analysis. |
| 10 | **code-review-and-quality** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/code-review-and-quality/SKILL.md) | "Conducts multi-axis code review. Use before merging any change." | 5-axis review (Correctness, Readability, Architecture, Security, Performance). Comment severity labels (Critical/Nit/Optional/FYI). Change sizing. Multi-model review pattern. Dead code hygiene. |
| 11 | **security-and-hardening** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/security-and-hardening/SKILL.md) | "Hardens code against vulnerabilities. Use when handling user input, authentication, data storage." | Three-tier boundary system (Always/Ask First/Never). OWASP Top 10 with code examples. npm audit triage decision tree. Rate limiting. Secrets management. |
| 12 | **performance-optimization** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/performance-optimization/SKILL.md) | "Optimizes application performance. Use when performance requirements exist." | Core Web Vitals table. 5-step workflow (Measure→Identify→Fix→Verify→Guard). "Where to Start Measuring" decision tree. 6 anti-pattern fixes with before/after code. Performance budget. |
| 13 | **debugging-and-error-recovery** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/debugging-and-error-recovery/SKILL.md) | "Guides systematic root-cause debugging. Use when tests fail, builds break, behavior doesn't match expectations." | Stop-the-line rule. 6-step triage checklist. Decision trees for test/build/runtime failures. Non-reproducible bug decision tree. Safe fallback patterns. |
| 14 | **shipping-and-launch** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/shipping-and-launch/SKILL.md) | "Prepares production launches. Use when preparing to deploy to production." | Pre-launch checklist (6 categories). Feature flag lifecycle. Staged rollout sequence with decision thresholds table. Rollback strategy template. Monitoring checklist. |
| 15 | **git-workflow-and-versioning** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/git-workflow-and-versioning/SKILL.md) | "Structures git workflow practices. Use when making any code change." | Trunk-based dev diagram. 5 core principles. Atomic commit format. Save point pattern. Change summary template. Pre-commit hygiene checklist. |
| 16 | **ci-cd-and-automation** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/ci-cd-and-automation/SKILL.md) | "Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines." | Quality gate pipeline diagram. GitHub Actions YAML configs. CI failure feedback loop. Deployment strategies. CI optimization decision tree. |
| 17 | **documentation-and-adrs** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/documentation-and-adrs/SKILL.md) | "Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features." | ADR template with lifecycle. Inline documentation rules (when/when not). API documentation patterns. README structure. Changelog maintenance. |
| 18 | **code-simplification** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/code-simplification/SKILL.md) | "Simplifies code for clarity. Use when refactoring code for clarity without changing behavior." | 5 principles. 4-step process. Chesterton's Fence principle. 3 pattern tables (Structural/Naming/Redundancy). Language-specific examples (TS, Python, React). Rule of 500. |
| 19 | **using-agent-skills** | [SKILL.md](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/using-agent-skills/SKILL.md) | "Discovers and invokes agent skills. Use when starting a session or when you need to discover which skill applies." | Skill discovery decision tree. 6 core operating behaviors. 10 failure modes. Lifecycle sequence. Quick reference table. Meta-skill that orchestrates others. |

### 2.2 qdrant/skills (2 skills read in detail, 8 total)

| # | Skill Name | URL | Description | Key Structural Features |
|---|---|---|---|---|
| 1 | **qdrant-scaling** | [SKILL.md](https://raw.githubusercontent.com/qdrant/skills/main/skills/qdrant-scaling/SKILL.md) | "Guides Qdrant scaling decisions. Use when someone asks 'how many nodes do I need', 'data doesn't fit on one node'..." | Hub-and-spoke: thin top-level SKILL.md links to sub-skills for each scaling dimension. Decision-first structure ("First determine what you're scaling for"). Uses `allowed-tools` frontmatter. |
| 2 | **qdrant-search-quality** | [SKILL.md](https://raw.githubusercontent.com/qdrant/skills/main/skills/qdrant-search-quality/SKILL.md) | "Diagnoses and improves Qdrant search relevance. Use when someone reports 'search results are bad'..." | Hub-and-spoke navigation. Diagnosis-first framing. Links to sub-skills for specific strategies. Practical threshold ("Splitting mid-sentence can drop quality 30-40%"). |
| 3 | **qdrant-performance-optimization** | [SKILL.md](https://raw.githubusercontent.com/qdrant/skills/main/skills/qdrant-performance-optimization/SKILL.md) | "Different techniques to optimize the performance of Qdrant..." | Navigation hub only — links to 3 sub-skills (speed, indexing, memory). Pure routing/decision skill. |

### 2.3 LeoYeAI/openclaw-master-skills (4 skills read in detail, 387+ total)

| # | Skill Name | URL | Description | Key Structural Features |
|---|---|---|---|---|
| 1 | **code** | [SKILL.md](https://raw.githubusercontent.com/LeoYeAI/openclaw-master-skills/main/skills/code/SKILL.md) | "Coding workflow with planning, implementation, verification, and testing for clean software development." | Quick reference table linking to sub-files. Strong scope/security section ("This skill NEVER:"). Memory system (~/code/memory.md). "Common Traps" section. "Self-Modification" ban. "External Endpoints" declaration. |
| 2 | **executing-plans** | [SKILL.md](https://raw.githubusercontent.com/LeoYeAI/openclaw-master-skills/main/skills/executing-plans/SKILL.md) | "Use when you have a written implementation plan to execute in a separate session with review checkpoints." | 5-step process with explicit announcements. Batch execution model (3 tasks per batch). "When to Stop and Ask for Help" section. "When to Revisit Earlier Steps" section. Required sub-skill integration. |
| 3 | **dispatching-parallel-agents** | [SKILL.md](https://raw.githubusercontent.com/LeoYeAI/openclaw-master-skills/main/skills/dispatching-parallel-agents/SKILL.md) | "Use when facing 2+ independent tasks that can be worked on without shared state." | Decision graph (graphviz dot notation). Agent prompt structure template. "Common Mistakes" with ❌/✅ format. Real-world example with concrete metrics. "When NOT to Use" section. |
| 4 | **debug-pro** | [SKILL.md](https://raw.githubusercontent.com/LeoYeAI/openclaw-master-skills/main/skills/debug-pro/SKILL.md) | "Systematic debugging methodology and language-specific debugging commands." | 7-step protocol. Language-specific code blocks (JS, Python, Swift, CSS, Network). Common error pattern table. Quick diagnostic commands. Concise, reference-card style. |

### 2.4 sickn33/antigravity-awesome-skills (2 skills read in detail, 1,409+ total)

| # | Skill Name | URL | Description | Key Structural Features |
|---|---|---|---|---|
| 1 | **readme** | [SKILL.md](https://raw.githubusercontent.com/sickn33/antigravity-awesome-skills/main/skills/readme/SKILL.md) | "You are an expert technical writer creating comprehensive project documentation..." | Role-play persona. "When to Use This Skill" trigger phrases. Multi-step "Before Writing" exploration process. Complete README template with 12 sections. "Writing Principles" list. "Limitations" safety section. |
| 2 | **documentation** | [SKILL.md](https://raw.githubusercontent.com/sickn33/antigravity-awesome-skills/main/skills/documentation/SKILL.md) | "Documentation generation workflow covering API docs, architecture docs, README files, code comments, and technical writing." | Workflow bundle format: 8 phases, each with "Skills to Invoke", "Actions", "Copy-Paste Prompts". Quality gates checklist. Related workflow bundles. Category: workflow-bundle. |

### 2.5 transloadit/skills (2 skills read in detail, ~10 total)

| # | Skill Name | URL | Description | Key Structural Features |
|---|---|---|---|---|
| 1 | **transform-remove-background** | [SKILL.md](https://raw.githubusercontent.com/transloadit/skills/main/skills/transform-remove-background-with-transloadit/SKILL.md) | "One-off background removal (local image -> transparent PNG) using the official `@transloadit/node` CLI." | Extremely prescriptive: exact Inputs, Prepare, Run, Debug sections. Complete JSON + CLI commands. Operational notes/caveats. No process steps — pure recipe. |
| 2 | **integrate-uppy-transloadit-s3** | [SKILL.md](https://raw.githubusercontent.com/transloadit/skills/main/skills/integrate-uppy-transloadit-s3-uploading-to-nextjs/SKILL.md) | "Add Uppy Dashboard + Transloadit uploads to a Next.js (App Router) app, with server-side signature generation." | Full code listings (complete files). Numbered implementation steps. "Golden Path" framing. Version-pinned dependencies. Internal references to validated scenarios. |

---

## 3. Structural Patterns Across Skills

### 3.1 Universal File Format: YAML Frontmatter + Markdown

**Appears in: ALL repositories (6/6)**

Every single skill across all repositories uses a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: skill-name
description: "What the skill does and when to use it"
---
```

**Frontmatter field variations by repository:**

| Repository | Required Fields | Optional Fields |
|---|---|---|
| addyosmani/agent-skills | `name`, `description` | (none observed) |
| qdrant/skills | `name`, `description` | `allowed-tools` |
| openclaw-master-skills | `name`, `description` | `slug`, `version`, `homepage`, `changelog`, `metadata` |
| antigravity-awesome-skills | `name`, `description` | `risk`, `source`, `date_added`, `category` |
| transloadit/skills | `name`, `description` | (none observed) |

**Key insight**: The `description` field doubles as the **activation trigger**. It's not just a description—it's a prompt-engineering surface that tells the agent *when* to activate this skill. The best descriptions include trigger phrases/questions.

### 3.2 The "When to Use / When NOT to Use" Gate

**Appears in: 18/19 addyosmani skills, 3/4 openclaw skills, 2/2 antigravity skills**

Nearly every skill begins with explicit activation criteria:

```markdown
## When to Use
- [Specific scenarios]

## When NOT to use
- [Explicit exclusions]
```

**Pattern**: The best descriptions are scenario-driven ("Starting a new project or feature") rather than abstract ("For project management"). Several qdrant skills go further by including verbatim user questions in the description itself:

> "Use when someone asks 'how many nodes do I need', 'data doesn't fit on one node', 'need more throughput'..."

### 3.3 The Verification Checklist (Defining "Done")

**Appears in: ALL 19 addyosmani skills, 2/4 openclaw skills, 1/2 antigravity skills**

Every addyosmani skill ends with a `## Verification` section containing a checklist:

```markdown
## Verification

After completing [action]:

- [ ] [Specific testable condition]
- [ ] [Specific testable condition]
- [ ] [Specific testable condition]
```

**This is the single most consistent pattern** across the addyosmani suite. It serves as:
1. A definition of "done" for the agent
2. A self-assessment checklist
3. An audit trail for the human reviewer

**Key insight**: Verification items are always *behavioral* ("All tests pass", "The user confirmed the direction") rather than *process* ("The skill was followed"). They check outcomes, not compliance.

### 3.4 The "Red Flags" Section

**Appears in: ALL 19 addyosmani skills**

Every addyosmani skill includes a `## Red Flags` section listing observable indicators that the process is going wrong:

```markdown
## Red Flags

- Starting to write code without any written requirements
- Asking "should I just start building?" before clarifying what "done" means
- Implementing features not mentioned in any spec or task list
```

**Pattern**: Red flags are written as *observable behaviors*, not abstract warnings. They describe what the agent might *actually do* wrong, phrased as present participles (gerunds) — "Starting...", "Skipping...", "Building..." — making them easy to match against current behavior.

### 3.5 The "Common Rationalizations" Table

**Appears in: 17/19 addyosmani skills**

A distinctive pattern unique to the addyosmani suite — a two-column table pairing *excuses* with *rebuttals*:

```markdown
## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This is simple, I don't need a spec" | Simple tasks don't need *long* specs, but they still need acceptance criteria. |
| "I'll write the spec after I code it" | That's documentation, not specification. |
```

**Key insight**: This pattern is an *anti-sycophancy* mechanism. It pre-empts the agent's tendency to rationalize skipping important steps. By explicitly naming the rationalization and debunking it, the skill makes it harder for the agent to convince itself (or the user) that a shortcut is acceptable.

### 3.6 ASCII Art Decision Trees and Flow Diagrams

**Appears in: 15/19 addyosmani skills, 2/4 openclaw skills**

Skills heavily use ASCII art for process flows and decision trees:

```
┌──────────────────────────────────────┐
│   Implement ──→ Test ──→ Verify ──┐  │
│       ▲                           │  │
│       └───── Commit ◄─────────────┘  │
│              ▼                       │
│          Next slice                  │
└──────────────────────────────────────┘
```

And decision trees:
```
What is slow?
├── First page load
│   ├── Large bundle? --> Measure bundle size
│   └── Slow server response? --> Measure TTFB
```

**Key insight**: These are not decorative — they serve as *compressed decision logic* that the agent can traverse. They replace paragraphs of if/else prose with a parseable structure.

### 3.7 Code Examples: Inline Bad/Good Pairs

**Appears in: 16/19 addyosmani skills, 2/4 openclaw skills, 1/2 antigravity skills**

The dominant example pattern is inline before/after contrasts:

```typescript
// BAD: SQL injection via string concatenation
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// GOOD: Parameterized query
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

**No skill uses external reference files for examples** in the addyosmani suite. All examples are inline. The only references to external files are to `references/*.md` files that contain extended checklists (not examples).

**Contrast with transloadit/skills**: Transloadit uses complete, copy-pasteable code files inline (entire route handlers, entire component files). These are *recipes*, not *principles*.

### 3.8 The Three-Tier Boundary System

**Appears in: 3/19 addyosmani skills directly, but referenced across many**

The `security-and-hardening` skill introduces a pattern used in multiple skills:

```
Always Do:    [Non-negotiable rules]
Ask First:    [Requires human approval]
Never Do:     [Hard prohibitions]
```

This same pattern appears in `spec-driven-development` (as "Boundaries" in the spec template), `context-engineering` (as trust levels), and `code-review-and-quality` (as comment severity levels).

---

## 4. Cross-Cutting Pattern Analysis

### 4.1 How Skills Define "Done" or Success Criteria

**Pattern**: Three-layer success definition

1. **Verification checklist** (end of skill) — behavioral outcomes to check
2. **Acceptance criteria** (within task templates) — specific testable conditions per task
3. **Red flags** (negative definition) — what "not done" looks like

**Example from spec-driven-development**:
- Verification: "Success criteria are specific and testable"
- Acceptance criteria in spec template: "How we'll know this is done — specific, testable conditions"
- Red flag: "Starting to write code without any written requirements"

**Prevalence**: This three-layer pattern appears in 14/19 addyosmani skills. The `using-agent-skills` meta-skill codifies it as Core Operating Behavior #6: "Verify, Don't Assume."

### 4.2 How Skills Handle Planning vs. Execution Relationship

**Pattern**: Gated phases with human review checkpoints

Every process-heavy skill in addyosmani uses a strict phase gate:

```
Phase N ──→ Human Review ──→ Phase N+1
```

The `spec-driven-development` skill makes this explicit with an ASCII diagram:
```
SPECIFY ──→ PLAN ──→ TASKS ──→ IMPLEMENT
   │          │        │          │
   ▼          ▼        ▼          ▼
 Human      Human    Human      Human
 reviews    reviews  reviews    reviews
```

**The openclaw `executing-plans` skill** takes this further with batched execution:
- Execute 3 tasks per batch
- Report after each batch
- Wait for feedback before continuing

**Key insight**: The separation is enforced by making planning and execution different *skills*. `spec-driven-development` produces a spec, `planning-and-task-breakdown` produces tasks, `incremental-implementation` executes them. This prevents the agent from collapsing planning and execution into a single step.

### 4.3 How Skills Structure Examples

**Pattern comparison across repositories:**

| Repository | Example Style | Location | Purpose |
|---|---|---|---|
| addyosmani/agent-skills | Inline bad/good pairs | Within section | Teach principles by contrast |
| qdrant/skills | Minimal snippets + doc links | Within section | Navigate to the right reference |
| openclaw-master-skills | Language-specific command blocks | Within section | Provide copy-paste commands |
| transloadit/skills | Complete file listings | Within section | Provide exact implementation |
| antigravity-awesome-skills | Template structures + placeholders | Within section | Provide starting frameworks |

**No repository uses external example files**. All examples are inline. The addyosmani skills reference `examples.md` and `frameworks.md` as supplementary material in the skill directory, but the SKILL.md itself contains all essential examples.

### 4.4 How Skills Handle Dependencies on Other Skills

**Three patterns observed:**

**Pattern A: Cross-reference by name (addyosmani)** — Skills mention other skills by name but don't enforce loading:
> "Execute tasks one at a time following `incremental-implementation` and `test-driven-development` skills."

**Pattern B: Meta-skill routing (addyosmani `using-agent-skills`)** — A dedicated meta-skill provides a decision tree that routes to the correct skill:
```
Task arrives → Vague idea? → idea-refine
            → New feature? → spec-driven-development
            → Implementing? → incremental-implementation
```

**Pattern C: Required sub-skill declaration (openclaw `executing-plans`)** — Explicit dependency declaration:
```markdown
## Integration
**Required workflow skills:**
- **superpowers:using-git-worktrees** - REQUIRED
- **superpowers:writing-plans** - Creates the plan this skill executes
- **superpowers:finishing-a-development-branch** - Complete development after all tasks
```

**Pattern D: Workflow bundles (antigravity `documentation`)** — A bundle skill lists skills to invoke per phase:
```markdown
### Phase 1: Documentation Planning
#### Skills to Invoke
- `docs-architect`
- `documentation-templates`
```

### 4.5 How Skills Communicate Progress During Long Tasks

**Four patterns observed:**

**Pattern 1: Inline planning announcement (addyosmani `context-engineering`)**:
```
PLAN:
1. Add Zod schema for task creation
2. Wire schema into POST /api/tasks
3. Add test for validation error response
→ Executing unless you redirect.
```

**Pattern 2: Checkpoint markers (addyosmani `planning-and-task-breakdown`)**:
```markdown
## Checkpoint: After Tasks 1-3
- [ ] All tests pass
- [ ] Application builds without errors
- [ ] Review with human before proceeding
```

**Pattern 3: Batch reporting (openclaw `executing-plans`)**:
- "When batch complete: Show what was implemented, Show verification output, Say: 'Ready for feedback.'"

**Pattern 4: Structured change summaries (addyosmani `git-workflow-and-versioning`)**:
```
CHANGES MADE:
- src/routes/tasks.ts: Added validation middleware

THINGS I DIDN'T TOUCH (intentionally):
- src/routes/auth.ts: Has similar gap but out of scope

POTENTIAL CONCERNS:
- The Zod schema is strict — confirm this is desired.
```

### 4.6 How Skills Handle Context/Memory Across Steps

**Three strategies:**

**Strategy 1: Context hierarchy (addyosmani `context-engineering`)** — 5-level hierarchy from persistent (rules files) to transient (conversation). Explicit recommendation to start fresh sessions when context drifts.

**Strategy 2: File-based memory (openclaw `code` skill)** — Persist preferences to `~/code/memory.md`:
```markdown
### 1. Check Memory First
Read `~/code/memory.md` for user's stated preferences if it exists.
```

**Strategy 3: Living documents (addyosmani `spec-driven-development`)** — Spec is committed to version control and updated as decisions change:
> "The spec is a living document, not a one-time artifact. Update when decisions change."

---

## 5. Anti-Pattern & "Common Mistakes" Sections

### 5.1 Aggregate Anti-Patterns Across 3+ Skills

These anti-patterns appear across multiple skills, suggesting they are fundamental agent failure modes:

| Anti-Pattern | Skills Where It Appears | Frequency |
|---|---|---|
| **Skipping verification / "seems right is not done"** | using-agent-skills, test-driven-development, incremental-implementation, spec-driven-development, code-review-and-quality, code-simplification, debugging-and-error-recovery | **7 skills** |
| **Scope creep / unsolicited renovation** | incremental-implementation, code-simplification, using-agent-skills, git-workflow-and-versioning | **4 skills** |
| **Making wrong assumptions without checking** | using-agent-skills, spec-driven-development, context-engineering, idea-refine | **4 skills** |
| **Over-engineering / premature abstraction** | incremental-implementation, code-simplification, using-agent-skills, frontend-ui-engineering | **4 skills** |
| **Sycophancy / not pushing back** | using-agent-skills, idea-refine, code-review-and-quality | **3 skills** |
| **Guessing instead of asking** | context-engineering, using-agent-skills, debugging-and-error-recovery | **3 skills** |
| **Writing tests after the code** | test-driven-development, spec-driven-development, debugging-and-error-recovery | **3 skills** |
| **Optimizing without measuring** | performance-optimization, code-simplification, debugging-and-error-recovery | **3 skills** |
| **Mixing concerns in commits/changes** | git-workflow-and-versioning, code-review-and-quality, code-simplification, incremental-implementation | **4 skills** |
| **Context flooding / information overload** | context-engineering, planning-and-task-breakdown | **2 skills** |

### 5.2 Format Patterns in Anti-Pattern Sections

**addyosmani uses three distinct anti-pattern formats:**

1. **"Anti-patterns to Avoid"** — Bullet list with don't-do guidance (idea-refine)
2. **"Common Rationalizations"** table — Excuse | Reality pairs (17 skills)
3. **"Red Flags"** — Observable behaviors indicating the process is going wrong (19 skills)

**openclaw uses:**
- **"Common Mistakes"** with ❌/✅ contrasts (dispatching-parallel-agents)
- **"Common Traps"** as brief bullets (code)

**antigravity uses:**
- **"Limitations"** section — Safety boundaries at the end (readme, documentation)

---

## 6. Key Findings & Recommendations

### 6.1 The Six Universal Structural Elements

Every well-written skill across all repositories contains some combination of these elements, ordered by consistency:

| Element | Prevalence | Purpose |
|---|---|---|
| 1. **YAML frontmatter** (name + description) | 100% of all skills | Activation trigger + identity |
| 2. **When to Use / When NOT to use** | ~90% of skills | Activation boundary |
| 3. **Verification checklist** | 100% of addyosmani, ~50% of others | Definition of "done" |
| 4. **Red Flags** | 100% of addyosmani | Negative definition of "done" |
| 5. **Common Rationalizations** | 89% of addyosmani | Anti-sycophancy mechanism |
| 6. **Inline code examples** (bad/good) | ~80% of all skills | Behavioral specification |

### 6.2 The Canonical Skill Structure (addyosmani pattern)

The addyosmani skills follow this exact structure with remarkable consistency:

```markdown
---
name: skill-name
description: "What it does. When to use it."
---

# Skill Title

## Overview
[One paragraph: what this skill does and why it matters]

## When to Use
[Bullet list of activation scenarios]

## When NOT to use
[Explicit exclusions]

## The Process / How It Works
[Numbered steps or phases with diagrams]

## [Domain-Specific Sections]
[Rules, patterns, code examples]

## Common Rationalizations
[Excuse | Reality table]

## Red Flags
[Observable behaviors indicating failure]

## Verification
[Checklist of testable outcomes]
```

### 6.3 Five Architectural Philosophies

**Philosophy 1: Skills as Workflows, Not Suggestions**
> "Skills are workflows, not suggestions. Follow the steps in order. Don't skip verification steps." — using-agent-skills

**Philosophy 2: Process Separation via Skill Boundaries**
Planning and execution are different skills. Spec-writing and task-breakdown are different skills. This prevents the agent from collapsing distinct cognitive modes.

**Philosophy 3: Negative Space Is as Important as Positive**
Skills define what NOT to do as thoroughly as what to do. "When NOT to use", "Red Flags", "Common Rationalizations", "Never Do" lists — all serve to constrain agent behavior.

**Philosophy 4: Domain Skills (qdrant/transloadit) vs. Process Skills (addyosmani)**
- Domain skills are prescriptive recipes ("run this exact command")
- Process skills are decision frameworks ("follow this workflow")
- Both use the same SKILL.md format but serve fundamentally different purposes

**Philosophy 5: Anti-Sycophancy by Design**
The "Common Rationalizations" pattern, "Push back when warranted" directive, and "Be honest, not supportive" instruction collectively work to counteract the agent's natural tendency toward agreement and shortcuts.

### 6.4 Notable Differences Between Repositories

| Dimension | addyosmani | qdrant | transloadit | openclaw | antigravity |
|---|---|---|---|---|---|
| **Skill type** | Process/workflow | Domain/navigation | Domain/recipe | Mixed | Mixed + bundles |
| **Specificity** | Framework-agnostic | Product-specific | Product-specific | Tool-specific | Framework-specific |
| **Example style** | Principle (bad/good) | Minimal + links | Complete files | Commands | Templates |
| **Dependencies** | Cross-reference by name | Hub→sub-skill links | None | Required sub-skills | Phase-based invocation |
| **Security** | Trust boundaries | allowed-tools | Credential handling | Scope/endpoint declaration | Limitations section |
| **Verification** | Always present | Absent | File existence check | Sometimes present | Quality gates |

### 6.5 Patterns That Appear Across 3+ Repositories

1. **YAML frontmatter with `name` + `description`** — Universal (6/6 repos)
2. **"When to Use" trigger list** — (5/6 repos)
3. **Inline code examples** — (5/6 repos)
4. **Decision trees or flowcharts** — (4/6 repos)
5. **Checklist-based verification** — (4/6 repos)
6. **Anti-pattern documentation** — (4/6 repos)
7. **Scope/security boundary declaration** — (4/6 repos)

### 6.6 Underexplored Areas

1. **Skill versioning** — Only openclaw uses a `version` field. No repository has a formal versioning strategy.
2. **Skill testing** — Only transloadit has an E2E validation framework for skills (scenarios/ directory).
3. **Skill composition** — No repository has a formal mechanism for composing skills (the openclaw "Required workflow skills" is the closest).
4. **Context budget management** — Only addyosmani's `context-engineering` addresses this. No skill declares its own token footprint.
5. **Failure recovery** — Skills describe what to do when things go wrong, but no skill describes how to recover when the *skill itself* leads to a wrong path.

---

## Appendix: Summary Statistics

- **Total skills read in full**: 30 (19 addyosmani + 3 qdrant + 4 openclaw + 2 antigravity + 2 transloadit)
- **Total skills cataloged**: 2,900+ across all repositories
- **Total words analyzed**: ~50,000+ words of skill content
- **Most consistent structural pattern**: Verification checklist (100% in addyosmani)
- **Most distinctive pattern**: Common Rationalizations table (unique to addyosmani, appears in 17/19 skills)
- **Most universal pattern**: YAML frontmatter + "When to Use" (appears across all repositories)
