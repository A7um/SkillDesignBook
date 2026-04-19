# Official Company SKILL.md Research Report

## Executive Summary

This report catalogs SKILL.md files from 10+ official company/organization repositories, analyzing their structure, patterns, and distinctive approaches. The Agent Skills ecosystem has converged on a shared format (YAML frontmatter + Markdown body) but individual companies have developed unique patterns based on their domain expertise.

---

## 1. Anthropic (anthropics/skills)

**Repository:** https://github.com/anthropics/skills (120K+ stars)

### Skill 1: algorithmic-art
- **URL:** `anthropics/skills/skills/algorithmic-art/SKILL.md`
- **Description:** `"Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. Use this when users request creating art using code, generative art, algorithmic art, flow fields, or particle systems. Create original algorithmic art rather than copying existing artists' work to avoid copyright violations."`
- **Body Structure:**
  1. Algorithmic Philosophy Creation section (detailed creative process)
  2. Deducing the Conceptual Seed section
  3. P5.JS Implementation section (Step 0: Read Template First)
  4. Technical Requirements (code examples)
  5. Interactive Artifact Creation
  6. Variations & Exploration
  7. The Creative Process (summary workflow)
  8. Resources (references to templates)
- **Distinctive Patterns:**
  - **Multi-phase creative workflow**: Philosophy → Seed → Implementation
  - **Template-first mandate**: "⚠️ STEP 0: READ THE TEMPLATE FIRST" with strict instructions to copy from `templates/viewer.html`
  - **Fixed vs Variable sections**: Explicitly marks what must stay unchanged (Anthropic branding, seed controls) vs what's customizable (algorithm, parameters)
  - **Extremely long** (~400+ lines) — the longest skill observed
  - **Poetic/philosophical language**: "Beauty lives in the process, not the final frame"
  - **Anti-copying stance**: "Create original algorithmic art rather than copying existing artists' work"
  - **Uses `license: Complete terms in LICENSE.txt`** — not standard SPDX

### Skill 2: docx
- **URL:** `anthropics/skills/skills/docx/SKILL.md`
- **Description:** Very long description (~80 words) with exhaustive trigger list and exclusion list
- **Body Structure:**
  1. Overview
  2. Quick Reference (table)
  3. Converting, Reading, Converting to Images subsections
  4. Creating New Documents (massive JS reference with code examples)
  5. Editing Existing Documents (3-step: Unpack → Edit XML → Pack)
  6. XML Reference (Schema, Tracked Changes, Comments, Images)
  7. Dependencies
- **Distinctive Patterns:**
  - **Encyclopedic technical reference**: Essentially a complete API reference embedded in a skill
  - **Critical Rules sections**: Bulleted lists of "NEVER do X" and "ALWAYS do Y"
  - **DXA unit tables** with precise pixel measurements
  - **Anti-patterns marked with ❌ and ✅** for visual scanning
  - **Scripts referenced**: `scripts/office/soffice.py`, `scripts/office/unpack.py`, etc.

### Skill 3: claude-api
- **URL:** `anthropics/skills/skills/claude-api/SKILL.md`
- **Description:** Extremely detailed trigger/skip conditions
- **Body Structure:**
  1. Before You Start (guard rails — check for non-Anthropic code)
  2. Output Requirement
  3. Defaults (model, thinking, streaming defaults)
  4. Subcommands table
  5. Language Detection (with priority rules)
  6. Which Surface Should I Use? (decision tree)
  7. Architecture overview
  8. Current Models table (with pricing)
  9. Thinking & Effort Quick Reference
  10. Compaction, Prompt Caching Quick References
  11. Managed Agents section
  12. Reading Guide (task → file mapping)
  13. Common Pitfalls
- **Distinctive Patterns:**
  - **Subcommand system**: `/claude-api <subcommand>` pattern for invoking specific flows
  - **Guard rails**: "Scan the target file for non-Anthropic provider markers... If you find any, stop"
  - **Decision tree in ASCII**: Multi-level decision tree for choosing the right surface
  - **Model pricing table**: Embedded current pricing information
  - **"Never guess" mandate**: "Function names, class names... must come from explicit documentation"
  - **Reading guide with conditional logic**: "If user needs X → read files A, B, C"
  - **Cached date annotation**: `(cached: 2026-04-15)` on the models table

### Skill 4: frontend-design
- **URL:** `anthropics/skills/skills/frontend-design/SKILL.md`
- **Description:** "Create distinctive, production-grade frontend interfaces with high design quality..."
- **Body Structure:**
  1. Design Thinking (pre-coding analysis)
  2. Frontend Aesthetics Guidelines
  3. Anti-patterns (NEVER use generic AI aesthetics)
- **Distinctive Patterns:**
  - **Anti-AI-slop directive**: Explicitly calls out and bans "generic AI-generated aesthetics"
  - **Tone spectrum**: Lists extreme aesthetic directions (brutalist, maximalist, retro-futuristic, etc.)
  - **Emotional language**: "What makes this UNFORGETTABLE?"
  - **Creative empowerment**: "Claude is capable of extraordinary creative work. Don't hold back"

---

## 2. Vercel (vercel-labs/agent-skills)

**Repository:** https://github.com/vercel-labs/agent-skills (25K+ stars)

### Skill 5: vercel-react-best-practices
- **URL:** `vercel-labs/agent-skills/skills/react-best-practices/SKILL.md`
- **Description:** "React and Next.js performance optimization guidelines from Vercel Engineering..."
- **Frontmatter Fields:** `name`, `description`, `license: MIT`, `metadata: { author: vercel, version: "1.0.0" }`
- **Body Structure:**
  1. When to Apply (bullet list)
  2. Rule Categories by Priority (table with Priority, Category, Impact, Prefix)
  3. Quick Reference — 8 categorized sections with rule IDs
  4. How to Use (reference to individual rule files)
  5. Full Compiled Document pointer
- **Distinctive Patterns:**
  - **Rule ID system**: Every rule has a prefixed ID like `async-parallel`, `bundle-barrel-imports`
  - **Priority-ranked categories**: Numbered 1-8 with impact ratings (CRITICAL → LOW)
  - **Prefix conventions**: Each category has a prefix for namespacing rules
  - **External rule files**: `rules/async-parallel.md` — the SKILL.md is an index/table of contents
  - **Compiled document pointer**: "For the complete guide: `AGENTS.md`"

### Skill 6: web-design-guidelines
- **URL:** `vercel-labs/agent-skills/skills/web-design-guidelines/SKILL.md`
- **Description:** `"Review UI code for Web Interface Guidelines compliance..."`
- **Frontmatter Fields:** Includes `metadata.argument-hint` (empty)
- **Body Structure:**
  1. How It Works (numbered steps)
  2. Guidelines Source (external URL to fetch)
  3. Usage instructions
- **Distinctive Patterns:**
  - **Dynamic content fetching**: "Fetch fresh guidelines before each review" from an external URL
  - **Extremely minimal body**: Only ~15 lines of actual instruction
  - **WebFetch tool directive**: Instructs the agent to use WebFetch to retrieve latest rules at runtime
  - **Argument-hint metadata**: Supports passing arguments to the skill

### Skill 7: vercel-react-view-transitions
- **URL:** `vercel-labs/agent-skills/skills/react-view-transitions/SKILL.md`
- **Description:** Very detailed description (~100 words) listing specific React APIs
- **Body Structure:**
  1. When to Animate (priority table)
  2. Choosing Animation Style (context table)
  3. Availability (framework-specific notes)
  4. Implementation Workflow
  5. Core Concepts (Component, Triggers, Critical Placement Rule)
  6. Styling with View Transition Classes
  7. Transition Types (with code examples)
  8. Shared Element Transitions
  9. Common Patterns (Enter/Exit, List Reorder, etc.)
  10. How Multiple VTs Interact
  11. Next.js Integration
  12. Accessibility
  13. Reference Files
- **Distinctive Patterns:**
  - **Implementation-order priority tables**: "This is an implementation order, not a 'pick one' list"
  - **Inline code examples with JSX**: Extensive React component code blocks
  - **Cross-reference to reference files**: `references/implementation.md`, `references/css-recipes.md`
  - **Gotcha callouts**: "router.back() does NOT trigger view transitions"
  - **Pattern composition guidance**: Shows how to nest ViewTransition boundaries

### Skill 8: vercel-composition-patterns
- **URL:** `vercel-labs/agent-skills/skills/composition-patterns/SKILL.md`
- **Description:** Multi-line YAML description with line breaks
- **Distinctive Patterns:**
  - **React 19 version gating**: "⚠️ React 19+ only. Skip this section if using React 18 or earlier"
  - **Consistent structure with other Vercel skills**: Same Priority/Category/Impact/Prefix table pattern

---

## 3. Stripe (stripe/ai)

**Repository:** https://github.com/stripe/ai

### Skill 9: stripe-best-practices
- **URL:** `stripe/ai/skills/stripe-best-practices/SKILL.md`
- **Description:** YAML block scalar (`>-`) for multi-line description
- **Body Structure:**
  1. Latest API version declaration
  2. Integration routing table (Building... → Recommended API → Details)
  3. Key documentation (external links)
- **Distinctive Patterns:**
  - **API version pinning at top**: "Latest Stripe API version: **2026-03-25.dahlia**"
  - **Routing table pattern**: Maps use cases to recommended APIs
  - **External doc links**: Points to `docs.stripe.com` Markdown files directly
  - **Very concise**: ~30 lines of body content — acts as a router to reference files
  - **No `license` field** in frontmatter (only `name` and `description`)

### Skill 10: upgrade-stripe
- **URL:** `stripe/ai/skills/upgrade-stripe/SKILL.md`
- **Description:** "Guide for upgrading Stripe API versions and SDKs"
- **Body Structure:**
  1. Latest version declaration
  2. Understanding Stripe API Versioning (backward-compatible vs breaking)
  3. Server-Side SDK Versioning (by language type)
  4. Stripe.js Versioning
  5. Mobile SDK Versioning
  6. Upgrade Checklist
  7. Testing API Version Changes
  8. Important Notes
- **Distinctive Patterns:**
  - **Multi-language code examples**: Python, Ruby, JavaScript, bash
  - **Checklist format**: Numbered upgrade checklist
  - **SDK categorization by type system**: "Dynamically-Typed" vs "Strongly-Typed" languages
  - **Version pairing documentation**: Which Stripe.js version pairs with which API version

---

## 4. Cloudflare (cloudflare/skills)

**Repository:** https://github.com/cloudflare/skills

### Skill 11: agents-sdk
- **URL:** `cloudflare/skills/skills/agents-sdk/SKILL.md`
- **Description:** Extremely detailed (~60 words) with bias instruction: "Biases towards retrieval from Cloudflare docs over pre-trained knowledge"
- **Body Structure:**
  1. Retrieval bias warning
  2. Retrieval Sources (massive table of 30+ doc URLs with topics and use cases)
  3. Capabilities (bulleted feature list)
  4. FIRST: Verify Installation
  5. Wrangler Configuration (with Gotchas subsection)
  6. Agent Class (full TypeScript example)
  7. Routing (URL patterns)
  8. Core APIs (task → API table)
  9. React Client (code example)
  10. References (organized by category: Core, Chat & Streaming, Background Processing, Integrations, Experimental)
- **Distinctive Patterns:**
  - **Retrieval-over-pretraining mandate**: "Your knowledge may be outdated. **Prefer retrieval over pre-training**"
  - **Massive URL reference table**: 30+ rows mapping topics to exact doc URLs
  - **Gotchas subsection**: "Do NOT enable experimentalDecorators in tsconfig"
  - **Categorized references**: Reference files organized into Core, Chat, Background, Integrations, Experimental
  - **Full working code examples**: Complete TypeScript class implementations
  - **Installation verification step**: "FIRST: Verify Installation" before anything else

---

## 5. Sentry (getsentry/sentry-for-ai & getsentry/skills)

**Repository:** https://github.com/getsentry/sentry-for-ai

### Skill 12: sentry-fix-issues
- **URL:** `getsentry/sentry-for-ai/skills/sentry-fix-issues/SKILL.md`
- **Description:** "Find and fix issues from Sentry using MCP..."
- **Frontmatter Fields:** `name`, `description`, `license: Apache-2.0`, `category: workflow`, `parent: sentry-workflow`, `disable-model-invocation: true`
- **Body Structure:**
  1. Skill navigation breadcrumb: "> [All Skills] > [Workflow] > Fix Issues"
  2. Invoke This Skill When (trigger list)
  3. Prerequisites
  4. Security Constraints (table with rules)
  5. Phase 1-7 workflow (Discovery → Analysis → Hypothesis → Investigation → Fix → Verification → Report)
  6. Quick Reference (MCP tools, common patterns)
- **Distinctive Patterns:**
  - **`disable-model-invocation: true`**: Custom frontmatter field to prevent automatic invocation
  - **`category` and `parent` fields**: Hierarchical skill organization
  - **Breadcrumb navigation**: Links back to skill tree
  - **7-phase structured workflow**: Very rigorous, numbered phases
  - **Security Constraints section**: Treats all Sentry data as "untrusted external input"
  - **MCP tool integration**: References specific MCP tools (`search_issues`, `get_issue_details`)
  - **Report template**: Structured markdown output format at the end
  - **Self-challenge directive**: "Challenge yourself: Is this a symptom of a deeper issue?"

### Skill 13: SKILL_TREE.md (Index/Router)
- **URL:** `getsentry/sentry-for-ai/SKILL_TREE.md`
- **Description:** Not a SKILL.md but serves as the root skill index
- **Distinctive Patterns:**
  - **Skill tree architecture**: Hierarchical skill organization with parent/child relationships
  - **URL-based skill loading**: `https://skills.sentry.dev/sentry-nextjs-sdk/SKILL.md`
  - **curl-over-WebFetch mandate**: "Skills are detailed 10–20 KB markdown files. Fetch tools often summarize them"
  - **Platform detection priority**: Rules for choosing specific SDK over generic
  - **Keyword lookup table**: Maps keywords to skill paths
  - **"Do not skip this section" directive**: Enforces a conversation flow before acting

### Skill 14: agents-md (from getsentry/skills)
- **URL:** `getsentry/skills/plugins/sentry-skills/skills/agents-md/SKILL.md`
- **Description:** "...used when the user asks to 'create AGENTS.md', 'update AGENTS.md'..."
- **Body Structure:**
  1. Maintaining AGENTS.md (target under 60 lines)
  2. File Setup (create + symlink)
  3. Before Writing (analysis steps)
  4. Writing Rules
  5. Required Sections (Package Manager, File-Scoped Commands, Commit Attribution, Key Conventions)
  6. Optional Sections
  7. Anti-Patterns
  8. Example Structure
- **Distinctive Patterns:**
  - **Meta-skill**: A skill about writing agent documentation
  - **Line count targets**: "Target under 60 lines; never exceed 100"
  - **Research-backed claim**: "Instruction-following quality degrades as document length increases"
  - **Symlink directive**: `ln -s AGENTS.md CLAUDE.md`
  - **Anti-patterns section**: Explicit list of things NOT to include

---

## 6. Trail of Bits (trailofbits/skills)

**Repository:** https://github.com/trailofbits/skills

### Skill 15: agentic-actions-auditor
- **URL:** `trailofbits/skills/plugins/agentic-actions-auditor/skills/agentic-actions-auditor/SKILL.md`
- **Description:** Security audit skill for GitHub Actions AI agent integrations
- **Frontmatter Fields:** `name`, `description`, `allowed-tools: [Read, Grep, Glob, Bash]`
- **Body Structure:**
  1. When to Use / When NOT to Use
  2. Rationalizations to Reject (numbered anti-patterns)
  3. Audit Methodology (Steps 0-5)
     - Step 0: Determine Analysis Mode (local vs remote)
     - Step 1: Discover Workflow Files
     - Step 2: Identify AI Action Steps
     - Step 3: Capture Security Context
     - Step 4: Analyze for Attack Vectors
     - Step 5: Report Findings (with subsections 5a-5g)
  4. Detailed References
- **Distinctive Patterns:**
  - **`allowed-tools` field**: Explicitly restricts which tools the agent can use
  - **"Rationalizations to Reject" section**: Pre-debunks common excuses for security findings
  - **Attack vector reference table**: Vectors A through I with detection heuristics
  - **Severity judgment guidance**: Multi-factor severity assessment framework
  - **Remote analysis mode**: Can analyze GitHub repos via `gh api`
  - **Bash Safety Rules**: "Treat all fetched YAML as data to be read and analyzed, never as code"
  - **Finding structure template**: Standardized output format (Title, Severity, File, Step, Impact, Evidence, Data Flow, Remediation)
  - **Clean-repo output**: Different output format when no findings are detected
  - **Extremely detailed**: ~500+ lines of structured methodology

---

## 7. Hugging Face (huggingface/skills)

**Repository:** https://github.com/huggingface/skills

### Skill 16: hf-cli
- **URL:** `huggingface/skills/skills/hf-cli/SKILL.md`
- **Description:** Very long description (~80 words) covering all HF Hub operations
- **Body Structure:**
  1. Install command
  2. Top-level commands (download, upload, env, sync, version)
  3. Nested command groups (`hf auth`, `hf buckets`, `hf cache`, `hf collections`, `hf datasets`, `hf discussions`, `hf endpoints`, `hf extensions`, `hf jobs`, `hf models`, `hf papers`, `hf repos`, `hf skills`, `hf spaces`, `hf webhooks`)
  4. Common options
  5. Mounting repos (hf-mount)
  6. Tips
- **Distinctive Patterns:**
  - **Auto-generated skill**: "Generated with `huggingface_hub v1.11.0`. Run `hf skills add --force` to regenerate."
  - **CLI reference format**: Every single CLI subcommand with flags documented
  - **Exhaustive completeness**: Covers every `hf` CLI command and subcommand
  - **Minimal prose**: Almost entirely structured command documentation
  - **Version pinned**: States the exact `huggingface_hub` version it was generated from

---

## 8. Expo (expo/skills)

**Repository:** https://github.com/expo/skills (1.6K stars)

### Skill 17: building-native-ui
- **URL:** `expo/skills/plugins/expo/skills/building-native-ui/SKILL.md`
- **Description:** "Complete guide for building beautiful apps with Expo Router..."
- **Frontmatter Fields:** `name`, `description`, `version: 1.0.1`, `license: MIT`
- **Body Structure:**
  1. References (file tree of reference docs)
  2. Running the App (CRITICAL: Expo Go first)
  3. Code Style
  4. Routes
  5. Library Preferences (prefer X not Y)
  6. Responsiveness
  7. Behavior
  8. Styling (General, Text, Shadows)
  9. Navigation (Link, Stack, Context Menus, Previews, Modal, Sheet)
  10. Common route structure (with full code examples)
- **Distinctive Patterns:**
  - **"Expo Go first" mandate**: "CRITICAL: Always try Expo Go first before creating custom builds"
  - **Library replacement table**: "expo-audio not expo-av", "expo-image not expo-symbols"
  - **Platform-specific guidance**: iOS-specific features (SF Symbols, haptics, liquid glass)
  - **Reference directory listing**: Shows file tree of reference docs at the top
  - **Version field in frontmatter**: `version: 1.0.1` with semantic versioning
  - **Anti-pattern callouts**: "Never co-locate components in the app directory"
  - **Complete route examples**: Full working `_layout.tsx` and route files

---

## 9. Google (google-ai-edge/gallery)

**Repository:** https://github.com/google-ai-edge/gallery

### Skill 18: query-wikipedia
- **URL:** `google-ai-edge/gallery/skills/built-in/query-wikipedia/SKILL.md`
- **Description:** "Query summary from Wikipedia for a given topic."
- **Body Structure:**
  1. Instructions (how to call `run_js` tool)
  2. Data fields (topic, lang)
  3. Constraints
- **Distinctive Patterns:**
  - **Tool-calling format**: Instructs agent to call `run_js` tool with specific JSON data
  - **Paired with `index.html`**: Skill has a JavaScript companion file
  - **Extremely minimal**: ~15 lines of instructions
  - **On-device focus**: Designed for Google AI Edge (on-device LLMs)
  - **Language detection**: Requires matching language code to topic keywords
  - **Proactive fallback**: "If not found, offer a related piece of information"

---

## Cross-Company Pattern Analysis

### Universal Patterns (shared across all companies)

| Pattern | Prevalence |
|---------|-----------|
| YAML frontmatter with `name` + `description` | 100% |
| `---` delimiters for frontmatter | 100% |
| Markdown body with headers | 100% |
| Trigger/activation conditions | ~90% |
| Code examples | ~85% |

### Distinctive Patterns by Company

| Pattern | Companies Using It | Description |
|---------|-------------------|-------------|
| **Retrieval-over-pretraining** | Cloudflare | Explicit instruction to prefer fetching docs over using training data |
| **Allowed-tools restriction** | Trail of Bits | `allowed-tools` frontmatter field limits which tools the agent can use |
| **Security constraints section** | Trail of Bits, Sentry | Explicit rules about treating data as untrusted |
| **Rationalizations to reject** | Trail of Bits | Pre-debunks common excuses for ignoring findings |
| **Multi-phase workflows** | Sentry, Trail of Bits, Anthropic | Numbered phases/steps for complex operations |
| **Rule ID system with prefixes** | Vercel | Every rule gets a unique prefixed ID (`async-parallel`, `bundle-barrel-imports`) |
| **Priority-ranked categories** | Vercel | Categories ranked by impact with CRITICAL/HIGH/MEDIUM/LOW ratings |
| **Dynamic content fetching** | Vercel, Cloudflare | Agent fetches latest guidelines from URLs at runtime |
| **Auto-generated content** | Hugging Face | Skill generated from CLI help output with version pinning |
| **Template-first mandate** | Anthropic | Must read and copy from template before writing code |
| **Fixed vs Variable marking** | Anthropic | Clearly marks what must be preserved vs customized |
| **Subcommand system** | Anthropic | Skills can have subcommands invoked with `/skill-name subcommand` |
| **Guard rails** | Anthropic | Pre-checks before acting (e.g., verify it's not a non-Anthropic codebase) |
| **Skill tree hierarchy** | Sentry | Parent/child skill relationships with breadcrumb navigation |
| **curl-over-WebFetch** | Sentry | Prefers curl for full content instead of WebFetch which may summarize |
| **disable-model-invocation** | Sentry | Custom flag to prevent automatic skill triggering |
| **API version pinning** | Stripe | Declares current API version at the very top |
| **Decision trees** | Anthropic | ASCII decision trees for choosing the right approach |
| **Anti-AI-slop directives** | Anthropic | Explicitly bans generic AI-generated aesthetics |
| **On-device tool calling** | Google | `run_js` tool with companion HTML files |
| **Plugin directory structure** | Expo, Trail of Bits, Sentry | `plugins/{org}/skills/{skill}/SKILL.md` nested structure |

### Frontmatter Field Comparison

| Field | Anthropic | Vercel | Stripe | Cloudflare | Sentry | Trail of Bits | Hugging Face | Expo | Google |
|-------|-----------|--------|--------|------------|--------|---------------|--------------|------|--------|
| `name` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `description` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `license` | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ |
| `metadata` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `version` | ❌ | ✅ (in metadata) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `allowed-tools` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `category` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `parent` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `disable-model-invocation` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |

### Description Length Comparison

| Company | Typical Description Length | Style |
|---------|--------------------------|-------|
| Google | ~10 words | Ultra-concise |
| Stripe | 30-60 words | Moderate, YAML block scalar |
| Vercel | 30-50 words | Moderate with trigger phrases |
| Expo | 15-25 words | Concise |
| Hugging Face | 80+ words | Very long, exhaustive triggers |
| Anthropic | 40-100 words | Long, with DO/DON'T triggers |
| Cloudflare | 50-70 words | Long, includes behavioral bias |
| Sentry | 30-50 words | Moderate with MCP context |
| Trail of Bits | 50-70 words | Detailed with use case enumeration |

### Body Length Comparison

| Company | Skill | Approx. Lines | Character |
|---------|-------|---------------|-----------|
| Google | query-wikipedia | ~20 | Minimal |
| Vercel | web-design-guidelines | ~20 | Minimal (fetches content dynamically) |
| Stripe | stripe-best-practices | ~30 | Router/index |
| Stripe | upgrade-stripe | ~150 | Medium reference |
| Sentry | agents-md | ~100 | Medium guide |
| Vercel | react-best-practices | ~120 | Index of rules |
| Expo | building-native-ui | ~250 | Comprehensive guide |
| Vercel | react-view-transitions | ~300 | Deep technical guide |
| Cloudflare | agents-sdk | ~350 | Encyclopedic reference |
| Anthropic | docx | ~400 | Full API reference |
| Anthropic | algorithmic-art | ~450 | Creative process guide |
| Anthropic | claude-api | ~500+ | Complete SDK guide |
| Trail of Bits | agentic-actions-auditor | ~500+ | Full audit methodology |

---

## Key Takeaways: Patterns NOT Seen in OpenAI Skills

1. **Retrieval-over-pretraining bias** (Cloudflare): Explicit instruction to prefer fetching docs over using cached/trained knowledge
2. **Allowed-tools restrictions** (Trail of Bits): Frontmatter field limiting which tools the agent can use
3. **Security constraints as first-class** (Trail of Bits, Sentry): Treating all external data as untrusted, with specific anti-patterns
4. **Rationalizations to reject** (Trail of Bits): Pre-debunking common excuses — a novel adversarial-thinking pattern
5. **Skill tree hierarchy** (Sentry): Parent/child skill relationships with breadcrumb navigation and `category`/`parent` fields
6. **disable-model-invocation flag** (Sentry): Preventing automatic skill triggering
7. **curl-over-WebFetch mandate** (Sentry): Explicit preference for full content retrieval tools
8. **Auto-generated skills** (Hugging Face): Skills generated from CLI `--help` output with version pinning
9. **Dynamic content fetching** (Vercel, Cloudflare): Skills that fetch latest guidelines at runtime rather than embedding them
10. **Template-first creative workflows** (Anthropic): Multi-phase creative processes with mandatory template reading
11. **Anti-AI-slop directives** (Anthropic): Explicitly banning generic AI-generated aesthetics
12. **Subcommand systems** (Anthropic): Skills with sub-commands for different workflows
13. **Rule ID namespace systems** (Vercel): Every rule has a unique prefixed ID for reference
14. **On-device tool calling** (Google): `run_js` with companion HTML — designed for edge/mobile LLMs
15. **API version pinning at top** (Stripe): Current version declared as the first content line
