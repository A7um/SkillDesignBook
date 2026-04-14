# Chapter 11: Evaluation and Benchmarks — Measuring What Matters

## 11.1 The Evaluation Challenge

How do you know your skill works? Not just that it activates correctly (Chapter 4), but that it produces correct, complete, high-quality results on real tasks?

Agent skill evaluation faces unique challenges:
- Skills operate in open-ended environments where the "correct" answer is not always deterministic
- Long-horizon tasks have many valid solution paths
- The same skill may perform differently with different models, different codebases, or different conversation histories
- Skill quality depends on both the skill design and the underlying model capability

## 11.2 The SWE-bench Ecosystem

The most widely-used benchmark for coding agent skills is **SWE-bench**, created by Princeton researchers. It presents real GitHub issues and measures whether agents can produce correct patches.

### SWE-bench Verified (Curated, Moderate Difficulty)

Top scores as of March 2026:

| Model | Score | Provider |
|-------|-------|----------|
| Claude Mythos Preview | 93.9% | Anthropic |
| Claude Opus 4.5 | 80.9% | Anthropic |
| Claude Opus 4.6 | 80.8% | Anthropic |
| Gemini 3.1 Pro | 80.6% | Google |
| GPT-5.2 | 80.0% | OpenAI |

SWE-bench Verified is **approaching saturation** at the top—the gap between leading models is less than 1 percentage point.

### SWE-bench Pro (Hard, Long-Horizon)

Designed for enterprise-level problems that require hours to days for professional engineers:

| Model | Score | Provider |
|-------|-------|----------|
| GLM-5.1 | 58.4% | Z.AI |
| GPT-5.4 | 57.7% | OpenAI |
| Claude Opus 4.6 | 57.3% | Anthropic |
| Gemini 3.1 Pro | 54.2% | Google |

SWE-bench Pro remains **far from saturated**, with even the best models resolving fewer than 60% of tasks.

### The Scaffolding Effect

The most underappreciated finding from SWE-bench: **the agent framework matters as much as the model**:

- A bare model with a simple prompt: ~30% on Verified
- The same model with SWE-Agent scaffolding: ~60%
- The same model with optimized production scaffolding: ~80%

This means skill design (which is a form of scaffolding) can contribute 20-50 percentage points of improvement. The model provides raw capability; the skill provides the structure to apply it effectively.

### What SWE-bench Does NOT Measure

- Architecture and design decisions
- Multi-repository reasoning
- Creative problem-solving (novel solutions)
- Collaboration with human developers
- Security awareness
- Performance under production pressure

## 11.3 Time Horizon as a Metric

The METR research group (March 2025) proposed a complementary metric: **50%-task-completion time horizon**—the duration of tasks that models can complete with 50% success rate.

Key findings:
- Frontier AI time horizon has been **doubling approximately every 7 months** since 2019
- Current frontier models can handle tasks that take skilled humans 1-2 hours
- Extrapolation predicts 1-month time horizons between late 2028 and early 2031

For skill designers, the implication: **the tasks your skills need to handle will get progressively longer and more complex**. Skills designed for 30-minute tasks today will need to support multi-hour tasks within a year.

## 11.4 Skill-Specific Evaluation

Beyond general benchmarks, skills should be evaluated on skill-specific criteria:

### Activation Accuracy

Test with positive, negative, and boundary prompts:

```
Activation accuracy = (true positives + true negatives) / total test cases

Target: >95% for production skills
```

### Execution Success Rate

For each activated skill:

```
Success rate = successful completions / total activations

Target: >80% for mature skills, >60% for new skills
```

### Token Efficiency

```
Token efficiency = task completion quality / tokens consumed

Compare: same task with skill vs. without skill
Target: Equal or better quality at fewer tokens
```

### Recovery Rate

For skills handling error-prone workflows:

```
Recovery rate = (errors encountered - errors recovered) / errors encountered

Target: >70% recovery for transient errors
```

## 11.5 Evaluation Methodologies

### Method 1: Deterministic Evaluation

For skills with deterministic outputs (deployment procedures, formatting workflows):
- Define expected outputs for given inputs
- Run the skill on test inputs
- Compare outputs against expectations
- Report pass/fail for each test case

### Method 2: LLM-as-Judge

For skills with non-deterministic outputs (code review, analysis):
- Run the skill on a set of test cases
- Have a separate LLM evaluate the quality of outputs against rubrics
- Aggregate scores across test cases

### Method 3: Human Evaluation

For skills where quality is subjective (creative tasks, complex analysis):
- Run the skill on representative tasks
- Have domain experts rate outputs on defined criteria
- Track inter-rater agreement to ensure evaluation consistency

### Method 4: A/B Comparison

For measuring skill improvement:
- Run the same tasks with the old and new skill versions
- Compare outputs on quality, efficiency, and accuracy
- Measure statistical significance of differences

## 11.6 The Eval-Skills Methodology

OpenAI's eval-skills guide recommends:

1. **Define success criteria in the skill itself**: Every skill should specify what "done" looks like
2. **Include verification steps**: The skill's instructions should include steps for the agent to verify its own work
3. **Test routing first**: Before testing the skill body, verify that the description triggers correctly
4. **Use real-world task distributions**: Test with the actual tasks users will bring, not synthetic examples
5. **Measure both positive and negative**: Test that the skill produces correct results AND that it doesn't produce incorrect results

## 11.7 Continuous Skill Monitoring

For skills in production:

| Metric | What It Measures | Alert Threshold |
|--------|-----------------|-----------------|
| Activation rate | How often the skill triggers | Significant change (±30%) from baseline |
| Success rate | How often activated skills complete successfully | Drop below 70% |
| Token consumption | Average tokens per skill execution | Increase >50% from baseline |
| User overrides | How often users manually correct skill behavior | Increase >20% |
| Recovery rate | How often the skill recovers from errors | Drop below 50% |

## 11.8 Building an Evaluation Suite

A practical approach for teams:

1. **Start with 10-20 representative tasks** that the skill should handle
2. **Add 5-10 boundary cases** where the skill should explicitly NOT activate
3. **Include 3-5 failure scenarios** to test error recovery
4. **Run the suite on every skill version change**
5. **Track results over time** to detect regression
6. **Add new test cases** when you discover failure modes in production

## Key Takeaways

1. SWE-bench Verified is approaching saturation; SWE-bench Pro (long-horizon tasks) remains the frontier.
2. The scaffolding (skill design) contributes 20-50 percentage points of improvement over raw model capability.
3. Agent time horizons are doubling every 7 months—design skills for progressively longer tasks.
4. Evaluate skills on four dimensions: activation accuracy, execution success, token efficiency, and recovery rate.
5. Test routing before testing the skill body.
6. Monitor production skills continuously and add test cases when you discover new failure modes.
