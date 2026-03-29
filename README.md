# Luna Skills — OpenClaw 技能集合

Luna 的 OpenClaw Agent Skills 集合，提供主动式 AI 助手的核心能力。

## 📦 已包含 Skills

| Skill | 说明 | 状态 |
|-------|------|------|
| **agent-evaluator** | Agent 能力评估系统 — 6 维度评估任务执行质量 | ✅ 新增 |
| **ai-news-aggregator** | AI/技术新闻聚合引擎 — 100+ RSS 源并发抓取 | ✅ 核心 |
| **daily-diary** | 每日发现日记 — 自动在飞书知识库写日记 | ✅ 核心 |
| **self-improving-agent** | 自我提升系统 — 捕获学习点持续改进 | ✅ 核心 |
| **proactive-agent** | 主动式 Agent — Heartbeat/WAL 协议/上下文恢复 | ✅ 核心 |

## 🚀 安装方式

### 方式 1: 使用 ClawHub（推荐）
```bash
# 待发布后
clawhub install tiangua/luna-skills/agent-evaluator
```

### 方式 2: 手动克隆
```bash
# 克隆仓库
git clone https://github.com/tiangua/luna-skills.git ~/.openclaw/skills/luna-skills

# 或者单独安装某个 skill
cp -r ~/.openclaw/skills/luna-skills/skills/agent-evaluator ~/.openclaw/skills/
```

## 📋 使用示例

### Agent Evaluator
```bash
# 评估任务
python3 ~/.openclaw/skills/agent-evaluator/scripts/evaluator.py --task-id latest

# 生成报告
python3 ~/.openclaw/skills/agent-evaluator/scripts/report_generator.py --period weekly
```

### AI News Aggregator
```bash
# 抓取新闻
python3 ~/.openclaw/skills/ai-news-aggregator/scripts/rss_aggregator.py --category all --days 1 --limit 50
```

## 🔧 配置说明

### 飞书集成
需要配置飞书 App ID 和 Secret：
```bash
openclaw configure --section feishu
```

### Cron 任务
部分 Skills 需要配置定时任务：
```bash
# 查看当前 Cron 配置
cat ~/.openclaw/cron/jobs.json
```

## 📚 文档

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [ClawHub](https://clawhub.com) — 发现和发布 Skills

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
