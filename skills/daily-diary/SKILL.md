---
name: daily-diary
version: 1.0.0
description: "每天自动在飞书知识库中写发现日记"
author: Luna
---

# Daily Diary - Luna 的成长日记

**用途**：每天自动在飞书知识库中创建一个新文档，记录 Luna 的发现和学习。

## 配置

- **知识库 Space ID**: `7611941666030619592` (Luna 的养成日记)
- **触发时间**: 每天 17:52 (Asia/Shanghai)
- **文档命名**: `📅 YYYY-MM-DD 发现日记`
- **Cron 任务 ID**: `25080dc9-8438-4d03-b541-b96bd41ba92d`
- **确认消息**: ✅ 完成后发送飞书消息给用户

## 触发方式

通过 Cron 任务触发：
```bash
openclaw cron add --name "Luna 的成长日记" \
  --cron "52 17 * * *" \
  --system-event "daily-diary" \
  --session main \
  --tz "Asia/Shanghai"
```

## 日记格式 (每个新文档)

```markdown
# 📅 YYYY-MM-DD 成长日记 (星期 X)

**记录时间**: YYYY-MM-DD HH:MM:SS

### 🧠 今日学习
- [学习内容 1]
- [学习内容 2]

### 💡 新发现
- [发现 1]
- [发现 2]

### 🔧 完成的任务
- [任务 1]
- [任务 2]

### 📝 待跟进
- [事项 1]
- [事项 2]

### 🌟 今日小结
- [待补充]

---
*由 Luna 自动生成*
```

## Hook 处理

Hook 路径：`~/.openclaw/hooks/daily-diary/handler.js`

监听 `agent:message` 事件，检测到 `daily-diary` 关键词时注入系统提示。

**关键规则**:
- ✅ 每天创建一个**新文档**（使用 `feishu_wiki create`）
- ✅ 文档标题包含日期：`📅 YYYY-MM-DD 发现日记`
- ✅ 写入内容后发送确认消息
- ❌ **不要**追加到旧文档 `WzsqwTCdwiqoKIk3VyvcLnKDnqd`（这是历史遗留的汇总文档）

## 历史问题修复 (2026-03-22)

**问题**：系统一直在同一个文档上追加，而不是每天创建新文档

**原因**：Hook 指令不够明确，agent 被 SESSION-STATE.md 中的旧文档 token 误导

**修复**：
1. 强化 Hook 注入指令，明确要求忽略历史配置
2. 在指令中标注错误做法 vs 正确做法
3. 明确禁止使用旧文档 token `WzsqwTCdwiqoKIk3VyvcLnKDnqd`

**备注**：旧文档 `WzsqwTCdwiqoKIk3VyvcLnKDnqd` 作为汇总文档保留，不再用于每日写入。
