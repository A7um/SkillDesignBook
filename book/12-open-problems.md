# Chapter 12: Open Problems and the Research Frontier

## 12.1 The Seven Open Challenges

The academic literature (Jiang et al., 2026; Xu et al., 2026) identifies seven unresolved challenges that define the frontier of agent skill research:

### Challenge 1: Cross-Platform Skill Portability

While the Agent Skills standard defines a common format, **behavioral portability** remains elusive. The same SKILL.md produces different results across platforms because:
- Models interpret instructions differently
- Tool implementations vary (Cursor's Bash ≠ Claude Code's Bash)
- Context management strategies differ
- Subagent capabilities are not standardized

The gap between format portability and behavioral portability is the biggest practical barrier to "write once, run anywhere" skills.

### Challenge 2: Unsupervised Skill Discovery

Most current systems rely on humans to author skills. The next frontier is **agents that discover and create their own skills** from experience:
- Memento-Skills (April 2026) demonstrates the approach: agents extract reusable skills from successful task completions
- The challenge: automatically determining what constitutes a "reusable procedure" vs. a one-off task
- Quality control: auto-generated skills may encode mistakes or inefficient patterns

### Challenge 3: Skill Composition at Scale

Current platforms limit composition:
- Most support only one active skill at a time
- Meta-skills (skills that invoke other skills) are manually authored
- Dependency resolution is primitive
- Conflict detection between skills is minimal

The goal: **automatic composition**—given a complex task, the system selects and orchestrates multiple skills without manual meta-skill authoring.

### Challenge 4: Capability-Based Permission Models

The current trust model is binary: a skill either has access or doesn't. Production systems need **graduated permissions**:
- Read-only skills that can analyze but not modify
- Time-limited access (skill has write access only during deployment phase)
- Resource-scoped access (skill can modify files in `src/` but not `config/`)
- Capability-based security that matches the skill's actual needs

### Challenge 5: Continual Adaptation Under Non-Stationary Tasks

Real-world task distributions shift over time. Skills that work today may fail tomorrow because:
- Codebases evolve (new frameworks, changed conventions)
- External APIs change (new endpoints, deprecated methods)
- Team practices change (new review standards, deployment procedures)

Skills need **adaptation mechanisms** that detect drift and update procedures accordingly, without human intervention.

### Challenge 6: Agent-Tool Co-Adaptation

Current systems treat agent and tool design as independent. But they co-evolve:
- Better agents need less prescriptive tools
- Better tools enable more autonomous agent behavior
- The optimal tool interface depends on the model's capabilities

The research question: how should tools adapt as models improve? And how should skills evolve to leverage new tool capabilities?

### Challenge 7: Safe Exploration During Self-Improvement

Self-improving agents (like Memento-Skills) need to explore new approaches to discover better strategies. But exploration can:
- Produce errors that affect production systems
- Discover and encode unsafe patterns
- Drift from intended behavior

The tension: **exploration is necessary for improvement but dangerous in production**. Sandbox-based exploration with graduated promotion is the likely solution path.

## 12.2 Emerging Research Directions

### Agentic Context Engineering (ACE)

The Stanford/SambaNova ACE framework challenges the assumption that shorter contexts are always better. Their research shows:
- **+12.5% improvement** on the AppWorld benchmark by growing knowledge within structure
- The context window is not just working memory—it's a knowledge base
- "How do I grow knowledge within structure?" is a better question than "How do I fit within limits?"

### Tool Masking

An emerging pattern that dynamically restricts which tools are visible to the agent based on the current task phase. This prevents:
- The agent calling deployment tools during the analysis phase
- Write tools being available during read-only review
- Network tools being accessible during local-only tasks

Tool masking implements the principle of least privilege at the tool level, dynamically adjusting the agent's capabilities based on context.

### Skill Versioning and Migration

As skills evolve, teams need:
- **Semantic versioning** for skills (breaking changes, new features, patches)
- **Migration paths** between skill versions
- **Rollback capabilities** when a new skill version degrades performance
- **A/B testing** between skill versions

### Federated Skill Libraries

Organizations need to share skills across teams while maintaining local customization:
- Organization-wide "golden" skills that all agents use
- Team-specific overrides for local conventions
- Individual-level skills for personal preferences
- Inheritance hierarchy: global → org → team → project → user

### Skill Generation from Demonstrations

Instead of manually authoring SKILL.md files, future systems may:
1. Watch a human perform a task
2. Record the sequence of actions, decisions, and tool uses
3. Generate a skill that captures the procedure
4. Test the skill against similar tasks
5. Refine based on success/failure

Manus's "Package as Skill" feature is a primitive version of this: completing a task, then instructing the agent to package the workflow.

## 12.3 Predictions for the Next 12-18 Months

Based on current trajectories:

1. **Skill marketplaces will consolidate and add security scanning** as the ClawHavoc-style attacks drive demand for trusted registries.

2. **Auto-generated skills will become common** as models improve at self-reflection and procedure extraction.

3. **Multi-skill composition will mature** with dependency resolution, conflict detection, and automatic orchestration.

4. **The context window constraint will ease but not disappear**. Models with 1M+ token windows are coming, but progressive disclosure will remain valuable for reasoning quality.

5. **Agent Skills will extend beyond coding** to business processes, legal workflows, medical procedures, and scientific research.

6. **Formal verification of skills** will emerge for high-stakes domains (finance, healthcare, safety-critical systems).

7. **The skill authoring experience will improve dramatically**—from manual Markdown writing to assisted creation with testing, linting, and simulation built in.

## 12.4 The Long View

The Agent Skills standard is less than six months old. The industry is in the phase that package managers were in around 2012: the format is standardized, the tooling is primitive, and the ecosystem is growing faster than security practices can keep up.

But the fundamental insight is durable: **agents need procedural knowledge, and that knowledge should be modular, portable, version-controlled, and loaded on demand**. This insight will survive any specific format, platform, or model generation.

The engineers who master skill design today—who understand progressive disclosure, activation accuracy, context engineering, error recovery, and security—will define how autonomous systems work for the next decade.

## Key Takeaways

1. Seven open challenges define the frontier: portability, auto-discovery, composition, permissions, adaptation, co-adaptation, and safe exploration.
2. ACE framework suggests growing context knowledge within structure, not just minimizing it.
3. Tool masking, skill versioning, and federated libraries are emerging patterns to watch.
4. Auto-generated skills from demonstrations will lower the authoring barrier.
5. The fundamental principles (modularity, progressive disclosure, least privilege) are durable across platform changes.
