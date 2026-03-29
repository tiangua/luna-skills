#!/usr/bin/env python3
"""
Report Generator — Agent 能力报告生成器
生成日报、周报、能力进化曲线
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

METRICS_ZH = {
    "accuracy": "准确性",
    "completeness": "完整性",
    "efficiency": "效率",
    "explainability": "可解释性",
    "robustness": "鲁棒性",
    "learning": "学习性",
}

def load_evaluations(start_date=None, end_date=None):
    """加载评估历史"""
    eval_dir = Path(__file__).parent.parent.parent / "workspace" / "memory" / "evaluations"
    
    if not eval_dir.exists():
        return []
    
    evaluations = []
    
    for file in eval_dir.glob("*.jsonl"):
        with open(file, encoding="utf-8") as f:
            for line in f:
                try:
                    eval_data = json.loads(line)
                    eval_date = datetime.fromisoformat(eval_data["timestamp"]).date()
                    
                    if start_date and eval_date < start_date:
                        continue
                    if end_date and eval_date > end_date:
                        continue
                    
                    evaluations.append(eval_data)
                except (json.JSONDecodeError, KeyError):
                    continue
    
    return sorted(evaluations, key=lambda x: x["timestamp"])

def generate_daily_report(date=None):
    """生成日报"""
    if date is None:
        date = datetime.now().date()
    
    evaluations = load_evaluations(start_date=date, end_date=date)
    
    if not evaluations:
        return {
            "date": date.isoformat(),
            "total_tasks": 0,
            "message": "今日暂无评估记录",
        }
    
    # 计算平均分
    avg_scores = defaultdict(list)
    for ev in evaluations:
        for metric, score in ev.get("scores", {}).items():
            avg_scores[metric].append(score)
    
    averages = {k: sum(v) / len(v) for k, v in avg_scores.items()}
    overall_avg = sum(averages.values()) / len(averages) if averages else 0
    
    # 收集亮点和改进点
    all_highlights = []
    all_improvements = []
    for ev in evaluations:
        all_highlights.extend(ev.get("highlights", []))
        all_improvements.extend(ev.get("improvements", []))
    
    return {
        "date": date.isoformat(),
        "total_tasks": len(evaluations),
        "overall_score": round(overall_avg, 2),
        "averages": {k: round(v, 2) for k, v in averages.items()},
        "highlights": list(set(all_highlights))[:5],
        "improvements": list(set(all_improvements))[:5],
    }

def generate_weekly_report(weeks=1):
    """生成周报"""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(weeks=weeks)
    
    evaluations = load_evaluations(start_date=start_date, end_date=end_date)
    
    if not evaluations:
        return {
            "period": f"{start_date.isoformat()} ~ {end_date.isoformat()}",
            "total_tasks": 0,
            "message": "本周暂无评估记录",
        }
    
    # 按天分组
    by_day = defaultdict(list)
    for ev in evaluations:
        day = datetime.fromisoformat(ev["timestamp"]).date()
        by_day[day].append(ev)
    
    # 计算趋势
    daily_scores = []
    for day in sorted(by_day.keys()):
        day_evals = by_day[day]
        avg = sum(ev.get("overall", 0) for ev in day_evals) / len(day_evals)
        daily_scores.append({"date": day.isoformat(), "score": round(avg, 2)})
    
    # 总体统计
    all_scores = [ev.get("overall", 0) for ev in evaluations]
    avg_score = sum(all_scores) / len(all_scores)
    
    # 最佳/最差维度
    metric_totals = defaultdict(list)
    for ev in evaluations:
        for metric, score in ev.get("scores", {}).items():
            metric_totals[metric].append(score)
    
    metric_avgs = {k: sum(v) / len(v) for k, v in metric_totals.items()}
    best_metric = max(metric_avgs, key=metric_avgs.get)
    worst_metric = min(metric_avgs, key=metric_avgs.get)
    
    return {
        "period": f"{start_date.isoformat()} ~ {end_date.isoformat()}",
        "total_tasks": len(evaluations),
        "total_days": len(by_day),
        "overall_score": round(avg_score, 2),
        "trend": daily_scores,
        "best_metric": {"key": best_metric, "name": METRICS_ZH.get(best_metric, best_metric), "score": round(metric_avgs[best_metric], 2)},
        "worst_metric": {"key": worst_metric, "name": METRICS_ZH.get(worst_metric, worst_metric), "score": round(metric_avgs[worst_metric], 2)},
    }

def generate_evolution_report():
    """生成能力进化报告（全量历史）"""
    evaluations = load_evaluations()
    
    if not evaluations:
        return {
            "message": "暂无评估历史",
        }
    
    # 按月分组
    by_month = defaultdict(list)
    for ev in evaluations:
        month = datetime.fromisoformat(ev["timestamp"]).strftime("%Y-%m")
        by_month[month].append(ev)
    
    # 计算月度趋势
    monthly_scores = []
    for month in sorted(by_month.keys()):
        month_evals = by_month[month]
        avg = sum(ev.get("overall", 0) for ev in month_evals) / len(month_evals)
        monthly_scores.append({
            "month": month,
            "score": round(avg, 2),
            "count": len(month_evals),
        })
    
    # 计算进步幅度
    if len(monthly_scores) >= 2:
        first_score = monthly_scores[0]["score"]
        last_score = monthly_scores[-1]["score"]
        improvement = ((last_score - first_score) / first_score) * 100 if first_score > 0 else 0
    else:
        improvement = 0
    
    # 维度趋势
    metric_trends = defaultdict(list)
    for ev in evaluations:
        for metric, score in ev.get("scores", {}).items():
            metric_trends[metric].append(score)
    
    metric_progress = {}
    for metric, scores in metric_trends.items():
        if len(scores) >= 2:
            first_half = sum(scores[:len(scores)//2]) / (len(scores)//2)
            second_half = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)
            progress = ((second_half - first_half) / first_half) * 100 if first_half > 0 else 0
            metric_progress[metric] = {
                "start": round(first_half, 2),
                "end": round(second_half, 2),
                "change": round(progress, 1),
            }
    
    return {
        "total_evaluations": len(evaluations),
        "time_span": f"{monthly_scores[0]['month']} ~ {monthly_scores[-1]['month']}",
        "overall_trend": monthly_scores,
        "improvement_rate": round(improvement, 1),
        "metric_progress": {METRICS_ZH.get(k, k): v for k, v in metric_progress.items()},
    }

def format_markdown_report(report, report_type="daily"):
    """格式化 Markdown 报告"""
    if report_type == "daily":
        md = f"""# 📊 Agent 能力日报

**日期**: {report['date']}

"""
        if report.get("total_tasks", 0) == 0:
            md += "今日暂无评估记录。\n"
        else:
            md += f"""## 总体评分

**综合得分**: {report['overall_score']} / 5.0
**评估任务数**: {report['total_tasks']}

## 维度得分

| 维度 | 得分 |
|------|------|
"""
            for k, v in report.get("averages", {}).items():
                md += f"| {METRICS_ZH.get(k, k)} | {v} |\n"
            
            md += f"""
## 亮点
"""
            for h in report.get("highlights", []):
                md += f"- ✅ {h}\n"
            
            md += f"""
## 改进点
"""
            for i in report.get("improvements", []):
                md += f"- 🔧 {i}\n"
    
    elif report_type == "weekly":
        md = f"""# 📈 Agent 能力周报

**周期**: {report['period']}

"""
        if report.get("total_tasks", 0) == 0:
            md += "本周暂无评估记录。\n"
        else:
            md += f"""## 总体表现

**综合得分**: {report['overall_score']} / 5.0
**评估任务数**: {report['total_tasks']}
**活跃天数**: {report['total_days']}

## 最佳维度

🏆 **{report['best_metric']['name']}**: {report['best_metric']['score']}

## 待改进

📉 **{report['worst_metric']['name']}**: {report['worst_metric']['score']}

## 每日趋势

| 日期 | 得分 |
|------|------|
"""
            for day in report.get("trend", []):
                md += f"| {day['date']} | {day['score']} |\n"
    
    elif report_type == "evolution":
        md = f"""# 🚀 Agent 能力进化报告

**时间跨度**: {report.get('time_span', 'N/A')}
**总评估数**: {report.get('total_evaluations', 0)}
**整体进步**: {report.get('improvement_rate', 0)}%

"""
        if report.get("overall_trend"):
            md += """## 月度趋势

| 月份 | 得分 | 评估数 |
|------|------|--------|
"""
            for m in report["overall_trend"]:
                md += f"| {m['month']} | {m['score']} | {m['count']} |\n"
        
        if report.get("metric_progress"):
            md += """
## 维度进步

| 维度 | 起始 | 当前 | 变化 |
|------|------|------|------|
"""
            for name, data in report["metric_progress"].items():
                change_icon = "📈" if data["change"] > 0 else "📉" if data["change"] < 0 else "➡️"
                md += f"| {name} | {data['start']} | {data['end']} | {change_icon} {data['change']}% |\n"
    
    else:
        md = "# 报告生成失败\n\n未知的报告类型。\n"
    
    md += "\n---\n\n*由 agent-evaluator 自动生成*\n"
    
    return md

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent 能力报告生成器")
    parser.add_argument("--period", type=str, default="daily", choices=["daily", "weekly", "all"], help="报告周期")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--trend", action="store_true", help="包含趋势图表数据")
    
    args = parser.parse_args()
    
    # 生成报告
    if args.period == "daily":
        report = generate_daily_report()
        report_type = "daily"
    elif args.period == "weekly":
        report = generate_weekly_report()
        report_type = "weekly"
    else:
        report = generate_evolution_report()
        report_type = "evolution"
    
    # 输出结果
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        md_report = format_markdown_report(report, report_type)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(md_report)
            print(f"报告已保存至：{args.output}")
        else:
            print(md_report)

if __name__ == "__main__":
    main()
