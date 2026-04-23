# 第一部分：设计哲学 — 顶级 Skill 如何自我定位

本章通过阅读下载量前 1,000 的 Skill 中**明确表述**的立场 — 它们的"核心原则"、"核心哲学"、"方法论"、"为什么存在"章节，以及首段自我描述和"绝不"/"始终"/"把……当作"/"而不是"声明 — 来提炼设计哲学。

以下每条原则都是多个排名靠前的 Skill 明确声明的哲学。每条都直接引自语料库。

---

## 原则 1：改变 Agent 的思考方式，而不仅仅是行为

**通俗解释**：好的 Skill 改变的是 *Agent 在选择方法之前问自己的问题*。告诉 Agent "做第 1 步，然后做第 2 步"给了它一个流程。改变 Agent 试图达成的目标则赋予它判断力 — 这种判断力能够泛化到作者从未预料到的场景。

**证据**：下载量最高的、包含哲学章节的 Skill 描述的是一种 *心智转变*，而非流程。

[proactive-agent](https://clawhub.ai/skills/proactive-agent)（14.5 万次下载）的核心哲学开头写道：

> **心态转变：** 不要问"我应该做什么？"而要问"有什么能真正让用户惊喜的，是他们没想到要求的？"

接着又提供了另一个心态重构：

> **不要等待请求，而要主动提出用户没想到要问的想法。**

[data-analysis](https://clawhub.ai/skills/data-analysis)（2.7 万次下载）开头写道：

> **核心原则**：没有决策的分析只是算术。始终明确：**如果分析结果显示 X 与 Y，分别会改变什么？**

[backtest-expert](https://clawhub.ai/skills/backtest-expert)（9 千次下载）：

> **核心哲学 — 目标**：寻找"最不容易崩溃"的策略，而不是在纸面上"盈利最多"的策略。

[thinking-partner](https://clawhub.ai/skills/thinking-partner)（8 千次下载）：

> 目标不是拥有答案，而是帮助发现答案。

[who-is-actor](https://clawhub.ai/skills/who-is-actor)（1.3 万次下载）：

> 目标是改善团队协作流程和个人工作方法，而不是评判一个人的价值。

**共同点**：它们重新定义了 Agent 问自己的问题。没有一个以"做第 1 步，然后做第 2 步"开头。它们改变了 Agent 在选择方法之前 *试图达成的目标*。

---

## 原则 2：选择一个默认值并解释原因 — 不要提供菜单

**通俗解释**：差的 Skill 列出选项（"你可以用 X 或 Y 或 Z"）。好的 Skill 选择一个（"默认使用 X，因为……"）。提供菜单把选择权交给了 Agent，这会导致不同运行之间的行为不一致。选择一个默认值并附上一句话的理由，给 Agent 一个稳定的起点，同时在理由不适用时仍允许它偏离。

**证据**：顶级 Skill 不提供选项菜单 — 它们选择默认值并说明原因。

[nextjs-expert](https://clawhub.ai/skills/nextjs-expert)（8 千次下载）核心原则：

> 1. **服务端优先**：组件默认是 Server Components。只有在需要 hooks、事件处理器或浏览器 API 时才添加 `'use client'`。
> 2. **将客户端边界下推**：将 `'use client'` 保持在组件树中尽可能低的位置。

[database-operations](https://clawhub.ai/skills/database-operations)（1 万次下载）：

> 1. **先度量** — 在优化之前始终使用 `EXPLAIN ANALYZE`
> 2. **策略性建索引** — 基于查询模式，而不是每个列
> 3. **选择性反规范化** — 仅在读取模式证明合理时

[security-auditor](https://clawhub.ai/skills/security-auditor)（2.1 万次下载）：

> - 应用纵深防御，设置多层安全层
> - 对所有访问控制遵循最小权限原则
> - 永远不信任用户输入 — 严格验证一切

**模式**：鲜明立场 + 简短理由，重复 4-6 个要点。不是"考虑 X 或 Y" — 而是"优先选择 X，因为 Y。"

---

## 原则 3：用"是什么"来定义 Skill，包括"不是什么"

**通俗解释**：顶级 Skill 有清晰的身份。它们不只说"这个 Skill 做 X" — 当用户常常把它们误认为 Y 时，它们经常补充"这个 Skill **不是** Y"。说明 Skill 不是什么，不是免责声明或责任盾牌；它是一个定位声明，帮助 Agent（和用户）知道什么时候该用它，什么时候该用别的。

**证据**：顶级 Skill 通过声明自己是什么来定义自己 — 即使这意味着拒绝常见的期望。

[who-is-actor](https://clawhub.ai/skills/who-is-actor)（1.3 万次下载）：

> **不安装任何东西，不运行任何脚本。** 所有数据收集完全通过原生 git 命令（`git log`、`git shortlog`、`git diff --stat` 等）完成。AI 负责解释和评估。

[academic-deep-research](https://clawhub.ai/skills/academic-deep-research)（1.7 万次下载）声明：

> 这是一个调查框架，**不是黑盒 API 封装器**。

[proactivity](https://clawhub.ai/skills/proactivity)（1.6 万次下载）：

> **不是 Prompt 执行者** — 注意下一步可能重要的事。

[data-analysis](https://clawhub.ai/skills/data-analysis)（2.7 万次下载）：

> 本 Skill 不需要本地文件夹、持久内存或初始化状态。

[agent-team-orchestration](https://clawhub.ai/skills/agent-team-orchestration)（2 万次下载）：

> 本 Skill 适用于多次交接的持续性工作流。

**模式**：顶级 Skill 有清晰的身份。"不是……"这种表述出现在 32 个 Skill 中（44 个实例）— 通过对比来强化身份。声明 Skill 不是什么，帮助 Agent 知道何时该使用它。

---

## 原则 4：用"把 X 当作 Y，而不是 Z"来纠正 Agent 的心智模型

**通俗解释**：模型对事物常常有错误的心智图像。一个 `.docx` 文件看起来像文本文档；实际上它是一个 XML 的 ZIP 包。一个 CSV 看起来像 Excel 文件；它不是。当模型的心智模型有误时，再多的步骤说明都无法修复下游错误。顶级 Skill 用"把 X 当作 Y，而不是 Z"这个短语直接修复心智模型 — 强制 Agent 在开始工作之前重新归类这个事物。

**证据**：23 个 Skill 中的 30 个实例使用了"把 X 当作 Y，而不是 Z"的表述 — 强制进行心智模型重置。

[word-docx](https://clawhub.ai/skills/word-docx)（6.2 万次下载）：

> **把 DOCX 当作 OOXML，而不是纯文本** — `.docx` 文件是 XML 部件的 ZIP 包，所以结构与可见文本同样重要。

[excel-xlsx](https://clawhub.ai/skills/excel-xlsx)（5.6 万次下载）：

> **把 CSV 当作纯数据交换格式，而不是 Excel 功能完整的格式。**

[playwright](https://clawhub.ai/skills/playwright)（2.8 万次下载）：

> **把渲染页面提取当作次要用途，而不是默认身份。**

[bilibili-all-in-one](https://clawhub.ai/skills/bilibili-all-in-one)（1.5 万次下载）：

> **像对待账号密码一样小心对待它们。**

**模式**："把 X 当作 Y，而不是 Z"这种表述迫使 Agent 切换推理框架。顶级 Skill 不是说"以下是如何处理 Excel 文件"，而是告诉 Agent "你的心智模型是错的 — 当涉及 CSV 时，不要把 Excel 当作功能完整的电子表格格式。"这种重构比任何规则列表都更持久。

---

## 原则 5：明确命名 Agent 会失败的具体方式 — 这是核心教学，不是边缘案例

**通俗解释**：每个领域都有一些模型 *持续犯的* 错误 — 不是罕见的边缘案例，而是在这个特定领域中会失败的默认行为。顶级 Skill 把这些放在最前面，作为"绝不……"和"不要……"声明。它们不是脚注或警告；它们是 Skill 的承重教学。一个没有"绝不"声明的 Skill 要么还没在生产中使用过，要么其作者还没有识别出失败模式。

**证据**："绝不……"在 96 个顶级 Skill 中出现了 131 次。"不要……"在 133 个 Skill 中出现了 250 次。这些不是边缘案例警告 — 它们是核心教学。

[self-improving-agent](https://clawhub.ai/skills/self-improving-agent)（#1，39.8 万次下载）：

> **绝不覆盖已有文件。**
> **优先使用简短摘要或脱敏摘录，而非原始命令输出或完整记录。**

[skill-vetter](https://clawhub.ai/skills/skill-vetter)（#2，21.3 万次下载）：

> **绝不在审查之前安装 Skill。** 偏执是一种特性。

[self-improving](https://clawhub.ai/skills/self-improving)（16.7 万次下载）：

> **绝不仅从沉默中推断** — 在 3 次相同经验教训后 → 要求确认为规则。

[humanizer](https://clawhub.ai/skills/humanizer)（9.2 万次下载）：

> **不要只是移除不良模式；要注入真正的个性。** 避免 AI 模式只是工作的一半。

**模式**："绝不/不要"声明指向模型持续掉入的特定失败模式。这不是防御性的 — 它是 Skill 最承重的教学。一个没有"绝不"声明的 Skill 可能还没遇到过失败。

---

## 原则 6：让 Skill 产出人们据以行动的决策，而非看起来漂亮的报告

**通俗解释**：构建一个产出精致、全面输出的 Skill 很容易 — 长篇分析、详细报告、全面总结。但如果没有人因为读了它而改变行为，这个 Skill 就没做任何有用的事。顶级 Skill 将"成功"定义为 *有人因为输出做出了不同的决策*，而不是 *输出看起来很完整*。这种导向改变了 Skill 的一切 — 收集什么数据、强调什么、何时停止。

股票分析 Skill 在你买入或卖出时才算成功。代码审查 Skill 在作者修改代码时才算成功。研究 Skill 在用户选择方向时才算成功。如果输出没有推动决策，Skill 就是在生成算术。

**证据**：多个顶级 Skill 明确拒绝理论性输出，转而支持可操作的决策。

[data-analysis](https://clawhub.ai/skills/data-analysis)（2.7 万次下载）：

> 没有决策的分析只是算术。始终明确：**如果分析结果显示 X 与 Y，分别会改变什么？**

[backtest-expert](https://clawhub.ai/skills/backtest-expert)：

> 寻找"最不容易崩溃"的策略，而不是在纸面上"盈利最多"的策略。

[automation-workflows](https://clawhub.ai/skills/automation-workflows)（6.7 万次下载）：

> 目标很简单：**自动化你每周做两次以上但不需要创造性思维的任何事情。**

[base-trader](https://clawhub.ai/skills/base-trader)（7 千次下载）：

> 目标不是每笔交易都赚钱。

**模式**：顶级 Skill 有一个判断输出是否 *有用* 的标准，而不仅仅是输出是否 *正确*。"这个分析可操作吗？"比"这个分析完整吗？"更重要。这将 Skill 的行为约束在真正重要的结果上。

---

## 原则 7：预先阻止 Agent 的默认错误，不要依赖它记住

**通俗解释**：LLM 有默认行为 — 有些好，有些危险。它们会记录详细错误（这可能泄露密钥）。它们在被要求时会自动批准"安全改进"（这可能破坏东西）。它们安装包来解决问题（这可能引入供应链风险）。这些默认行为是烘焙进模型的；你无法通过训练 Agent 一次来消除它们。每次新会话，默认行为都会回来。

顶级 Skill 通过在 Agent 读取 Skill 的那一刻明确 *阻止* 特定默认错误来预防这一点。不是"注意保密" — 而是"不要记录密钥、令牌、私钥、环境变量或完整源/配置文件，除非用户明确要求这种详细程度。"具体默认行为，具体阻止。

**证据**：顶级 Skill 命名模型的具体偏差并阻止它们。

[self-improving-agent](https://clawhub.ai/skills/self-improving-agent)：

> 不要记录密钥、令牌、私钥、环境变量或完整源/配置文件，除非用户明确要求这种详细程度。

[skill-vetter](https://clawhub.ai/skills/skill-vetter) 有一个专门的"危险信号"部分，列出了 14 种应立即拒绝的特定行为：

> **如果看到以下行为立即拒绝：** curl/wget 到未知 URL、向外部服务器发送数据、请求凭证/令牌/API 密钥、读取 ~/.ssh、~/.aws、~/.config 且无明确原因、对任何内容使用 base64 解码、对外部输入使用 eval() 或 exec()、混淆代码、对 IP 而非域名发起网络调用……

[proactive-agent](https://clawhub.ai/skills/proactive-agent)：

> 绝不在没有人工审批的情况下实施"安全改进"。

**模式**：顶级 Skill 不信任模型会默认采取安全行为。它们命名具体的不安全默认行为（记录密钥、安装未审查的 Skill、自动批准变更）并明确阻止它们。

---

## 原则 8：先说"为什么"，再说"怎么做"

**通俗解释**：顶级 Skill 的前 5-15 行告诉 Agent *这个 Skill 的用途以及如何思考它*。只有在那之后 Skill 才进入命令、设置和流程。这与参考文档相反，参考文档通常以"安装"或"快速开始"开头，把"哲学"（如果有的话）留到最后。Skill 之所以颠倒顺序，是因为 Agent 的首次阅读会影响后续每个决策 — 如果你以命令开头，Agent 会把 Skill 看作命令列表。如果你以哲学开头，Agent 会看到一种心态加上支持性事实。

**证据**：从阅读前 20 名 Skill 来看，存在一致的结构：

- **标题 + 标语**（1-2 行）
- **核心哲学或心态**（3-7 行，通常在 `Core Principle` 部分）
- **命令 / 工作流 / 事实**（其余部分）

短的顶级 Skill 在 <50 行内完成这个结构。长的顶级 Skill（[self-improving-agent](https://clawhub.ai/skills/self-improving-agent) 645 行，[proactive-agent](https://clawhub.ai/skills/proactive-agent) 633 行）仍然前置哲学。

来自 [proactive-agent](https://clawhub.ai/skills/proactive-agent) 的开头：

> **一个面向你的 AI Agent 的主动、自我改进架构。** 大多数 Agent 只是等待。这个会预判你的需求 — 并且随时间变得更好。

然后是三大支柱框架。只有在那之后命令和设置才出现。

来自 [pollyreach](https://clawhub.ai/skills/pollyreach)：

> PollyReach 为每个 AI Agent 提供一个电话号码和通过电话完成事务的能力 — 查找联系人、拨打电话、完成任务。

身份优先。设置其次。

**模式**：顶级 Skill 的前 5-15 行是哲学：这个 Skill 为什么存在，适用什么心态。剩余 95% 是事实和命令。这个比例与文档相反；一个 Skill 是 5% 的哲学加 95% 的事实 — 但那 5% 排在最前面，影响了后面的一切。

---

## 原则 9：只从用户实际说过或做过的事中学习 — 不要猜测

**通俗解释**：跨会话积累记忆的 Skill 面临一种诱惑：从模式中外推。用户从未提到过风格 X，所以他们一定偏好风格 Y。三个任务用了工具 Z，所以 Z 现在是首选工具。这种猜测会随时间腐蚀记忆，因为模型不断在推断之上做推断，最终"记忆"充满了用户从未实际表达过的信念。

顶级记忆 Skill 拒绝这一点。它们只从**明确信号**中学习：用户的直接纠正（"不，那是错的"）、声明的偏好（"我偏好 X"）、记录在案的成功结果、以及重复的相同模式（不是相似的，是相同的）。其他一切都是噪音。

**证据**：记忆和学习类 Skill 都收敛于一条规则。

[self-improving](https://clawhub.ai/skills/self-improving)（16.7 万次下载）：

> **绝不从沉默中推断** — 不要从数据缺失中得出任何结论。

[self-improving-proactive-agent](https://clawhub.ai/skills/self-improving-proactive-agent)：

> 学习来源：用户的直接纠正、明确偏好、重复的成功工作流、有意义工作后的自我反思。

[self-improving-agent](https://clawhub.ai/skills/self-improving-agent)：

> 当用户明确纠正你（"不，那是错的"、"实际上……"）→ 记录到 `.learnings/LEARNINGS.md`，类别为 `correction`。

[who-is-actor](https://clawhub.ai/skills/who-is-actor)：

> AI 负责解释和评估。所有数据收集完全通过原生 git 命令完成。

**模式**：当 Skill 随时间积累知识时，它只从**明确信号**中学习 — 用户纠正、明确偏好、记录在案的结果。它明确禁止从噪音、沉默或单次出现中推断模式。这是对模型自然倾向过度泛化的有力反制。

---

## 原则 10：围绕你要预防的失败来设计，而不是你要执行的任务

**通俗解释**：问 Skill 作者"你的 Skill 做什么？"他们会描述任务（"它审查代码"、"它审计安全"、"它获取股票数据"）。问"你的 Skill 存在是为了预防什么失败？"你会得到更锋利的答案（"通过审查但实际存在 bug 因为审查者只检查了测试"、"安装恶意 Skill"、"基于过拟合回测进行交易"）。第二种框架对每个设计决策都更有用。当你知道失败模式时，你就知道该设定哪些默认值、主张哪些规则、强调哪些输出、以及 Skill 何时真正成功了。

**证据**：顶级 Skill 通过它们失败时会发生什么来框定工作 — 而不是它们机械地做什么。

[skill-vetter](https://clawhub.ai/skills/skill-vetter)："**偏执是一种特性。**" — 风险是：安装恶意 Skill。

[proactive-agent](https://clawhub.ai/skills/proactive-agent)："**大多数 Agent 只是等待。这个会预判。**" — 风险是：错过了重要的事。

[security-auditor](https://clawhub.ai/skills/security-auditor)："**永远不信任用户输入 — 严格验证一切。**" — 风险是：注入攻击。

[backtest-expert](https://clawhub.ai/skills/backtest-expert)："**寻找最不容易崩溃的策略，而不是盈利最多的。**" — 风险是：过拟合。

[humanizer](https://clawhub.ai/skills/humanizer)："**不要只是移除不良模式；要注入真正的个性。**" — 风险是：AI 清洗过的文本听起来仍然了无生气。

[ai-persona-os](https://clawhub.ai/skills/ai-persona-os)：

> **为什么存在** — 我已经训练了数千人通过 AI Persona Method 构建 AI 人设。我看到的第一大问题是：[Skill 要解决的风险]。

**模式**：顶级 Skill 围绕它们存在是为了预防的特定失败来定位。这不是一个"为什么"章节 — 它是审视 Skill 中每个决策的镜头。理解失败模式使得 Skill 的默认值、规则和结构感觉是必然的，而非随意的。

---

## 元原则：Skill 做出主张；文档描述事物

**通俗解释**：综观以上 10 条原则，有一个理念贯穿始终：

- **文档** 描述事物是什么。它是中立的、完整的、安全的 — 旨在不误导任何人。
- **Skill** 不同。Skill 做出主张。它说"这是正确的默认值"、"这是不该做的"、"这是应该怎么思考的"。作者基于经验采取了立场。

这就是为什么措辞中立、面面俱到的 Skill 通常比有态度、有选择性的 Skill 更差。中立性消除了重新引导模型行为的力量。Skill 变成了工具的第二份描述，而模型并不需要 — 它已经知道这个工具了。

[proactive-agent](https://clawhub.ai/skills/proactive-agent) 主张 Agent 不应该等待。[skill-vetter](https://clawhub.ai/skills/skill-vetter) 主张你绝不应在审查之前安装。[data-analysis](https://clawhub.ai/skills/data-analysis) 主张没有决策的分析是算术。[word-docx](https://clawhub.ai/skills/word-docx) 主张 DOCX 不是纯文本。

这些是**作者通过经验获得的观点**。从 Skill 中剥离观点 — 使其"中立" — 会使它变差，因为它消除了重新引导模型行为的力量。

排名靠前的 Skill 都是有态度的。排名机制奖励这一点。

---

## 总结

| # | 原则 | 一句话总结 | 证据来源 |
|---|------|----------|---------|
| 1 | 改变 Agent 的思考方式，而不仅仅是行为 | Skill 重构问题；流程不会 | [proactive-agent](https://clawhub.ai/skills/proactive-agent)、[data-analysis](https://clawhub.ai/skills/data-analysis)、[backtest-expert](https://clawhub.ai/skills/backtest-expert) |
| 2 | 选择默认值并解释原因 | 菜单制造不一致；带理由的默认值稳定行为 | [nextjs-expert](https://clawhub.ai/skills/nextjs-expert)、[database-operations](https://clawhub.ai/skills/database-operations)、[security-auditor](https://clawhub.ai/skills/security-auditor) |
| 3 | 用"是什么"定义 Skill，包括"不是什么" | 身份 + 边界，不只是描述 | [who-is-actor](https://clawhub.ai/skills/who-is-actor)、[academic-deep-research](https://clawhub.ai/skills/academic-deep-research)、[proactivity](https://clawhub.ai/skills/proactivity) |
| 4 | 用"把 X 当作 Y，不是 Z"纠正心智模型 | 模型对 X 的默认分类有误 — 先修正它 | [word-docx](https://clawhub.ai/skills/word-docx)、[excel-xlsx](https://clawhub.ai/skills/excel-xlsx)、[playwright](https://clawhub.ai/skills/playwright) — 23 个 Skill |
| 5 | 命名具体失败模式 — 它们是核心教学 | 模型持续犯的错误，被明确命名 | [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)、[skill-vetter](https://clawhub.ai/skills/skill-vetter)、[humanizer](https://clawhub.ai/skills/humanizer) — 96 个 Skill |
| 6 | 产出人们据以行动的决策，而非漂亮的报告 | 成功 = 有人因输出做出不同决策 | [data-analysis](https://clawhub.ai/skills/data-analysis)、[backtest-expert](https://clawhub.ai/skills/backtest-expert)、[automation-workflows](https://clawhub.ai/skills/automation-workflows) |
| 7 | 预先阻止默认错误 | 具体默认行为 + 具体阻止，不是"小心点" | [self-improving-agent](https://clawhub.ai/skills/self-improving-agent)、[skill-vetter](https://clawhub.ai/skills/skill-vetter)、[proactive-agent](https://clawhub.ai/skills/proactive-agent) |
| 8 | 先说"为什么"，再说"怎么做" | 首次阅读为后续一切设定心态 | 下载量前 20 的 Skill |
| 9 | 只从用户实际说过或做过的事中学习 | 不猜测，不外推 — 仅明确信号 | [self-improving](https://clawhub.ai/skills/self-improving)、[self-improving-agent](https://clawhub.ai/skills/self-improving-agent)、[who-is-actor](https://clawhub.ai/skills/who-is-actor) |
| 10 | 围绕你要预防的失败来设计，而非执行的任务 | 以失败模式为框架，使每个设计决策更锋利 | [skill-vetter](https://clawhub.ai/skills/skill-vetter)、[backtest-expert](https://clawhub.ai/skills/backtest-expert)、[ai-persona-os](https://clawhub.ai/skills/ai-persona-os) |
