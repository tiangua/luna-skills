#!/usr/bin/env python3
"""
Agent Evaluator — 核心评估引擎
6 维度评估 AI Agent 任务执行质量
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path

# 6 维评估指标定义
METRICS = {
    "accuracy": {"name": "准确性", "weight": 1.5, "desc": "结果正确性、无幻觉"},
    "completeness": {"name": "完整性", "weight": 1.2, "desc": "覆盖所有需求"},
    "efficiency": {"name": "效率", "weight": 1.0, "desc": "时间/步骤合理性"},
    "explainability": {"name": "可解释性", "weight": 1.0, "desc": "推理过程清晰"},
    "robustness": {"name": "鲁棒性", "weight": 1.3, "desc": "错误恢复能力"},
    "learning": {"name": "学习性", "weight": 1.5, "desc": "从历史改进"},
}

def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent / "config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {
        "weights": {k: v["weight"] for k, v in METRICS.items()},
        "thresholds": {"excellent": 4.5, "good": 4.0, "needs_improvement": 3.0}
    }

def evaluate_task(task_data, auto=False):
    """
    评估单个任务
    
    Args:
        task_data: 任务数据（包含输入、输出、执行时间等）
        auto: 是否自动评估
    
    Returns:
        dict: 评估结果
    """
    scores = {}
    highlights = []
    improvements = []
    
    # 准确性评估
    if task_data.get("has_citations") or task_data.get("verified"):
        scores["accuracy"] = 5.0
        highlights.append("准确引用来源/已验证")
    elif task_data.get("has_errors"):
        scores["accuracy"] = 2.5
        improvements.append("存在事实错误，需要核实")
    else:
        scores["accuracy"] = 4.0
    
    # 完整性评估
    if task_data.get("requirements_met", 0) >= task_data.get("requirements_total", 1):
        scores["completeness"] = 5.0
        highlights.append("覆盖所有需求点")
    else:
        coverage = task_data.get("requirements_met", 0) / max(task_data.get("requirements_total", 1), 1)
        scores["completeness"] = min(5.0, coverage * 5)
        if coverage < 1.0:
            improvements.append("有需求未完全覆盖")
    
    # 效率评估
    exec_time = task_data.get("execution_time", 0)
    if exec_time < 10:
        scores["efficiency"] = 5.0
        highlights.append("执行效率高")
    elif exec_time < 30:
        scores["efficiency"] = 4.0
    elif exec_time < 60:
        scores["efficiency"] = 3.0
        improvements.append("执行时间较长")
    else:
        scores["efficiency"] = 2.0
        improvements.append("需要优化执行效率")
    
    # 可解释性评估
    if task_data.get("has_step_by_step") or task_data.get("has_reasoning"):
        scores["explainability"] = 5.0
        highlights.append("推理过程清晰")
    else:
        scores["explainability"] = 3.5
        improvements.append("可增加推理步骤说明")
    
    # 鲁棒性评估
    if task_data.get("errors_handled", 0) > 0:
        scores["robustness"] = 5.0
        highlights.append("优雅处理错误")
    elif task_data.get("has_fallback"):
        scores["robustness"] = 4.0
    else:
        scores["robustness"] = 3.5
    
    # 学习性评估（需要历史数据）
    if task_data.get("improved_from_history"):
        scores["learning"] = 5.0
        highlights.append("从历史学习中改进")
    else:
        scores["learning"] = 4.0  # 默认中等
    
    # 计算加权总分
    config = load_config()
    weights = config["weights"]
    overall = sum(scores[k] * weights[k] for k in scores) / sum(weights.values())
    
    # 生成评估 ID
    eval_id = f"eval_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    result = {
        "eval_id": eval_id,
        "task_id": task_data.get("task_id", "unknown"),
        "timestamp": datetime.now().isoformat(),
        "scores": scores,
        "overall": round(overall, 2),
        "highlights": highlights,
        "improvements": improvements,
        "user_feedback": task_data.get("user_feedback"),
        "auto_evaluated": auto,
    }
    
    return result

def save_evaluation(result, output_dir=None):
    """保存评估结果"""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / "workspace" / "memory" / "evaluations"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 按日期保存
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"{date_str}.jsonl"
    
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")
    
    return output_file

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent 评估引擎")
    parser.add_argument("--task-id", type=str, default="latest", help="任务 ID")
    parser.add_argument("--score-file", type=str, help="输出评分文件路径")
    parser.add_argument("--auto", action="store_true", help="自动评估模式")
    parser.add_argument("--input", type=str, help="输入任务数据 JSON 文件")
    
    args = parser.parse_args()
    
    # 加载任务数据
    if args.input:
        with open(args.input) as f:
            task_data = json.load(f)
    else:
        # 模拟任务数据（实际应从 OpenClaw 获取）
        task_data = {
            "task_id": args.task_id,
            "has_citations": True,
            "verified": True,
            "requirements_met": 3,
            "requirements_total": 3,
            "execution_time": 15,
            "has_step_by_step": True,
            "has_reasoning": True,
            "errors_handled": 0,
            "has_fallback": False,
            "improved_from_history": False,
        }
    
    # 执行评估
    result = evaluate_task(task_data, auto=args.auto)
    
    # 输出结果
    if args.score_file:
        with open(args.score_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"评估结果已保存至：{args.score_file}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 保存到评估历史
    output_file = save_evaluation(result)
    print(f"评估记录已追加至：{output_file}")
    
    # 返回总体评分（用于 CI/CD 等场景）
    sys.exit(0 if result["overall"] >= 4.0 else 1)

if __name__ == "__main__":
    main()
