---
name: "Agent Evaluator"
slug: agent-evaluator
version: "1.0.0"
homepage: https://github.com/openclaw/openclaw
description: "Agent 能力评估系统 — 6 维度评估 AI Agent 任务执行质量，支持自我改进追踪"
changelog: "v1.0: 初始版本，基于 LangChain 评估框架设计"
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
---

# Agent Evaluator — AI Agent 能力评估系统

基于 LangChain 评估框架和 Anthropic 经济指数研究设计，6 维度评估 Agent 任务执行质量。

## Setup

无需额外依赖，使用 Python 3.8+ 标准库。

## When to Use

在以下场景使用此 Skill：
- 完成重要任务后自我评估
- 用户更正后记录学习点
- 定期（每周）生成能力进化报告
- 对比不同模型/配置的表现

触发关键词：
- "评估这次任务"、"自我评估"
- "能力报告"、"进化追踪"
- "哪里可以改进"、"表现如何"

## Architecture

```
agent-evaluator/
├── scripts/
│   ├── evaluator.py           # 核心评估引擎
│   ├── metrics.py             # 6 维度指标定义
│   ├── report_generator.py    # 报告生成器
│   └── history_tracker.py     # 历史追踪
├── examples/
│   └── sample_eval.json       # 评估样例
└── SKILL.md                   # 本文件
```

## 6 维评估指标

| 维度 | 说明 | 评分标准 |
|------|------|---------|
| **准确性** | 结果是否正确、无幻觉 | 0-5 分（5=完全准确） |
| **完整性** | 是否覆盖所有需求 | 0-5 分（5=完整覆盖） |
| **效率** | 执行时间/步骤是否合理 | 0-5 分（5=最优） |
| **可解释性** | 推理过程是否清晰 | 0-5 分（5=完全可解释） |
| **鲁棒性** | 面对错误的恢复能力 | 0-5 分（5=优雅降级） |
| **学习性** | 是否从历史中改进 | 0-5 分（5=明显进步） |

## Core Commands

### 单次评估
```bash
# 评估最近一次任务
python3 skills/agent-evaluator/scripts/evaluator.py --task-id latest

# 评估指定任务
python3 skills/agent-evaluator/scripts/evaluator.py --task-id <task_id> --score-file /tmp/eval.json
```

### 生成报告
```bash
# 生成日报
python3 skills/agent-evaluator/scripts/report_generator.py --period daily --output /tmp/daily_report.md

# 生成周报
python3 skills/agent-evaluator/scripts/report_generator.py --period weekly --output /tmp/weekly_report.md

# 生成能力进化曲线
python3 skills/agent-evaluator/scripts/report_generator.py --period all --trend --output /tmp/evolution.md
```

### 历史追踪
```bash
# 查看所有评估记录
python3 skills/agent-evaluator/scripts/history_tracker.py --list

# 查看特定维度的进步曲线
python3 skills/agent-evaluator/scripts/history_tracker.py --metric accuracy --plot

# 导出为 JSON
python3 skills/agent-evaluator/scripts/history_tracker.py --export json --output /tmp/history.json
```

## Integration with OpenClaw

### 1. 自动评估 Hook

创建 `~/.openclaw/hooks/auto-evaluate/HOOK.md`:

```markdown
---
name: auto-evaluate
description: "任务完成后自动评估 Agent 表现"
metadata: {"openclaw":{"emoji":"📊","events":["agent:task-complete"]}}
---

触发时执行：
```bash
python3 ~/.openclaw/skills/agent-evaluator/scripts/evaluator.py --task-id $TASK_ID --auto
```

评估结果写入：`~/.openclaw/workspace/memory/evaluations/YYYY-MM-DD.md`
```

### 2. 新闻晨报分析集成

在 `ai-news-digest` Hook 末尾添加：

```bash
# 生成新闻分析
python3 ~/.openclaw/skills/agent-evaluator/scripts/news_analyzer.py \
  --input /tmp/ai_news.json \
  --output /tmp/news_analysis.md
```

## Output Format

### 评估结果 JSON
```json
{
  "task_id": "task_20260329_001",
  "timestamp": "2026-03-29T20:00:00+08:00",
  "scores": {
    "accuracy": 4.5,
    "completeness": 5.0,
    "efficiency": 4.0,
    "explainability": 5.0,
    "robustness": 4.5,
    "learning": 4.0
  },
  "overall": 4.5,
  "highlights": ["准确引用来源", "覆盖所有需求点"],
  "improvements": ["可进一步优化执行时间"],
  "user_feedback": null
}
```

### 能力进化报告 Markdown
```markdown
# Agent 能力进化报告

**周期**: 2026-03-01 ~ 2026-03-29
**评估次数**: 47

## 总体趋势
- 平均分：4.2 → 4.5 (+7.1%)
- 最佳维度：完整性 (4.8)
- 待改进：效率 (3.9)

## 维度曲线
[图表：6 维度随时间变化]

## 关键学习点
1. 技术文档分析能力提升 (+15%)
2. 代码生成准确性提升 (+12%)
3. 多步骤任务规划稳定 (持平)
```

## Core Rules

### 1. 评估时机
- **自动**: 重要任务完成后（通过 Hook）
- **手动**: 用户请求时
- **定期**: 每周日生成周报

### 2. 评分原则
- 基于客观指标（非主观感受）
- 用户反馈权重 > 自评估
- 连续 3 次低分触发改进建议

### 3. 数据持久化
- 评估记录写入 `memory/evaluations/`
- 历史数据用于趋势分析
- 支持导出/备份

## Configuration

编辑 `scripts/config.json` 调整权重：
```json
{
  "weights": {
    "accuracy": 1.5,
    "completeness": 1.2,
    "efficiency": 1.0,
    "explainability": 1.0,
    "robustness": 1.3,
    "learning": 1.5
  },
  "thresholds": {
    "excellent": 4.5,
    "good": 4.0,
    "needs_improvement": 3.0
  }
}
```

## Related Skills

- `self-improvement` — 记录学习点
- `ai-news-aggregator` — 新闻分析输入
- `daily-diary` — 能力报告归档

---

*评估不是为了完美，而是为了持续进步*
