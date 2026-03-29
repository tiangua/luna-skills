#!/usr/bin/env python3
"""
News Analyzer — AI 新闻分析思考生成器
在 AI 新闻晨报后自动生成分析思考
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# 分析维度
ANALYSIS_DIMENSIONS = [
    "技术趋势",
    "产品动态",
    "研究突破",
    "行业影响",
    "可应用点",
]

def analyze_news(news_data, limit=50):
    """
    分析新闻数据，生成思考
    
    Args:
        news_data: 新闻列表（来自 rss_aggregator.py）
        limit: 分析前 N 条新闻
    
    Returns:
        dict: 分析结果
    """
    if isinstance(news_data, list):
        articles = news_data[:limit]
    else:
        articles = news_data.get("articles", [])[:limit]
    
    # 过滤空数据
    articles = [a for a in articles if a.get("title") and a.get("url")]
    
    # 分类统计
    sources = {}
    categories = {
        "company": [],  # 大厂动态
        "research": [],  # 研究突破
        "product": [],  # 产品发布
        "tool": [],  # 工具/框架
        "industry": [],  # 行业趋势
    }
    
    for article in articles:
        source = article.get("source", "Unknown")
        sources[source] = sources.get(source, 0) + 1
        
        title = article.get("title", "").lower()
        desc = article.get("desc", "").lower()
        content = title + " " + desc
        
        # 简单分类
        if any(kw in content for kw in ["release", "launch", "update", "new", "发布", "更新"]):
            categories["product"].append(article)
        elif any(kw in content for kw in ["research", "study", "paper", "model", "研究", "论文", "模型"]):
            categories["research"].append(article)
        elif any(kw in content for kw in ["tool", "framework", "library", "sdk", "api", "工具", "框架"]):
            categories["tool"].append(article)
        elif any(kw in content for kw in ["company", "business", "funding", "ipo", "收购", "融资", "公司"]):
            categories["company"].append(article)
        else:
            categories["industry"].append(article)
    
    # 生成分析思考
    analysis = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "summary": {
            "total_articles": len(articles),
            "total_sources": len(sources),
            "top_sources": sorted(sources.items(), key=lambda x: x[1], reverse=True)[:5],
        },
        "categories": {k: len(v) for k, v in categories.items()},
        "key_insights": [],
        "actionable_items": [],
        "trends": [],
    }
    
    # 提取关键洞察
    for cat_name, cat_articles in categories.items():
        if cat_articles:
            top_article = cat_articles[0]
            analysis["key_insights"].append({
                "category": cat_name,
                "title": top_article.get("title"),
                "source": top_article.get("source"),
                "url": top_article.get("url"),
            })
    
    # 提取可行动项（针对技术工具类）
    for article in categories["tool"][:3]:
        analysis["actionable_items"].append({
            "title": article.get("title"),
            "reason": "技术工具，可评估集成到 OpenClaw",
            "priority": "中" if "github" in article.get("url", "") else "低",
        })
    
    # 识别趋势
    trend_keywords = ["agent", "cli", "evaluation", "memory", "local", "rust", "real-time"]
    trend_counts = {}
    for article in articles:
        content = (article.get("title", "") + " " + article.get("desc", "")).lower()
        for kw in trend_keywords:
            if kw in content:
                trend_counts[kw] = trend_counts.get(kw, 0) + 1
    
    analysis["trends"] = [
        {"keyword": k, "count": v}
        for k, v in sorted(trend_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    ]
    
    return analysis

def generate_markdown_report(analysis):
    """生成 Markdown 格式的分析报告"""
    md = f"""# 📰 AI 新闻分析思考

**日期**: {analysis['date']}
**分析范围**: {analysis['summary']['total_articles']} 条新闻 / {analysis['summary']['total_sources']} 个源

---

## 📊 今日概览

| 分类 | 数量 |
|------|------|
| 大厂动态 | {analysis['categories'].get('company', 0)} |
| 研究突破 | {analysis['categories'].get('research', 0)} |
| 产品发布 | {analysis['categories'].get('product', 0)} |
| 工具/框架 | {analysis['categories'].get('tool', 0)} |
| 行业趋势 | {analysis['categories'].get('industry', 0)} |

**热门来源**: {', '.join([f"{s[0]}({s[1]})" for s in analysis['summary']['top_sources']])}

---

## 💡 关键洞察

"""
    
    for insight in analysis["key_insights"]:
        md += f"""### {insight['category'].title()}
- **{insight['title']}**
- 来源：{insight['source']}
- [链接]({insight['url']})

"""
    
    md += """---

## 🛠️ 可行动项

"""
    
    if analysis["actionable_items"]:
        for item in analysis["actionable_items"]:
            priority_icon = {"高": "🔴", "中": "🟡", "低": "🟢"}.get(item["priority"], "⚪")
            md += f"""{priority_icon} **{item['title']}**
- 理由：{item['reason']}
- 优先级：{item['priority']}

"""
    else:
        md += "今日暂无明确可行动项。\n"
    
    md += """---

## 📈 趋势观察

"""
    
    if analysis["trends"]:
        for trend in analysis["trends"]:
            md += f"- **{trend['keyword']}**: {trend['count']} 次提及\n"
    else:
        md += "今日无明显技术趋势。\n"
    
    md += """
---

## 🤔 Luna 的思考

"""
    
    # 生成个性化思考
    if analysis["categories"].get("tool", 0) >= 3:
        md += "- 今天工具/框架类新闻较多，值得花时间评估是否有可集成到 OpenClaw 的新能力。\n"
    
    if analysis["categories"].get("research", 0) >= 2:
        md += "- 研究突破类新闻值得关注，可能是下一代 Agent 能力的方向。\n"
    
    if any(t["keyword"] == "agent" for t in analysis["trends"]):
        md += "- 「Agent」是今日高频词，Agent 工程化仍是行业焦点。\n"
    
    if any(t["keyword"] == "evaluation" for t in analysis["trends"]):
        md += "- 「Evaluation」被多次提及，Agent 评估标准化是生产落地的关键。\n"
    
    md += """
---

*由 agent-evaluator 自动生成*
"""
    
    return md

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 新闻分析思考生成器")
    parser.add_argument("--input", type=str, required=True, help="输入新闻 JSON 文件路径")
    parser.add_argument("--output", type=str, help="输出 Markdown 文件路径")
    parser.add_argument("--limit", type=int, default=50, help="分析前 N 条新闻")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    # 加载新闻数据
    with open(args.input) as f:
        news_data = json.load(f)
    
    # 执行分析
    analysis = analyze_news(news_data, limit=args.limit)
    
    # 输出结果
    if args.json:
        print(json.dumps(analysis, ensure_ascii=False, indent=2))
    else:
        md_report = generate_markdown_report(analysis)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(md_report)
            print(f"分析报告已保存至：{args.output}")
        else:
            print(md_report)

if __name__ == "__main__":
    main()
