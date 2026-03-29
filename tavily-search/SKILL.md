---
name: tavily-search
version: 1.0.0
description: "Search the web using Tavily API with AI-synthesized answers and citations"
author: user
---

# Tavily Search Tool

使用 Tavily API 进行网络搜索，返回 AI 综合答案和引用来源。

## 配置

### 1. 获取 API Key

1. 访问 https://app.tavily.com/settings
2. 创建 API Key
3. 设置环境变量：

```bash
# 临时设置
export TAVILY_API_KEY="tvly-..."

# 永久设置（推荐）
echo 'export TAVILY_API_KEY="tvly-..."' >> ~/.bashrc
source ~/.bashrc

# 或者添加到 OpenClaw 环境
echo 'TAVILY_API_KEY=tvly-...' >> ~/.openclaw/.env
```

### 2. 添加到工具配置

编辑 `~/.openclaw/openclaw.json`：

```json5
{
  "tools": {
    "profile": "full",
    "alsoAllow": ["tavily-search"]
  }
}
```

## 使用方法

### 命令行调用

```bash
# 基本搜索
node /root/.openclaw/workspace/tools/tavily-search.js "搜索关键词"

# 指定结果数量
node /root/.openclaw/workspace/tools/tavily-search.js "搜索关键词" 10
```

### 在 Agent 中调用

```javascript
// 使用 exec 工具调用
const { exec } = require('openclaw-tools');

const result = await exec({
  command: 'node /root/.openclaw/workspace/tools/tavily-search.js "AI Agent 架构" 5',
});

// 解析 JSON 输出
const jsonMatch = result.match(/━━━ JSON 格式 ━━━\n([\s\S]+)/);
if (jsonMatch) {
  const data = JSON.parse(jsonMatch[1]);
  console.log(data.answer); // AI 综合答案
  console.log(data.results); // 搜索结果列表
}
```

## API 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `query` | 搜索关键词 | 必填 |
| `max_results` | 最大结果数 | 5 |
| `search_depth` | 搜索深度 (basic/advanced) | basic |
| `include_answer` | 包含 AI 综合答案 | true |
| `include_raw_content` | 包含原始内容 | false |

## 响应格式

```json
{
  "answer": "AI 综合答案文本",
  "query": "原始搜索词",
  "response_time": 0.5,
  "results": [
    {
      "title": "网页标题",
      "url": "https://...",
      "content": "网页摘要",
      "score": 0.95
    }
  ]
}
```

## 定价

| 计划 | 价格 | 每月搜索次数 |
|------|------|-------------|
| Free | $0 | 1,000 次 |
| Starter | $29 | 100,000 次 |
| Pro | $299 | 1,000,000 次 |

详情：https://tavily.com/pricing

## 故障排除

### 错误：TAVILY_API_KEY 未设置

```bash
export TAVILY_API_KEY="tvly-..."
```

### 错误：API Key 无效

检查 Key 是否正确，确保没有多余空格：

```bash
echo $TAVILY_API_KEY | xxd
```

### 错误：网络超时

检查服务器是否能访问 `api.tavily.com`：

```bash
curl -I https://api.tavily.com
```

## 相关文档

- Tavily 官方文档：https://docs.tavily.com/
- OpenClaw 工具开发：https://docs.openclaw.ai/skills/creating-skills
