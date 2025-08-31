#!/usr/bin/env python3
"""
高级数据分析工具 - 支持丰富的报表类型

使用方法:
python analyze_advanced.py <文件路径> [报表类型]

报表类型:
- basic: 基础分析报表
- quality: 数据质量评估报告  
- business: 商业智能仪表板
- statistical: 统计分析报表
- predictive: 预测性分析报告
- correlation: 相关性分析报表
- anomaly: 异常值检测报告
- custom: 自定义分析问题

示例:
python analyze_advanced.py data.csv quality
python analyze_advanced.py data.csv business
python analyze_advanced.py data.csv custom "分析销售趋势" "预测下月收入"
"""
import sys
import os
import pandas as pd
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smart_file_analyzer import FileDataAnalyzer

# 预定义报表模板
REPORT_TEMPLATES = {
    'basic': [
        "请分析这个数据集的基本统计信息",
        "数据中有哪些主要的趋势和模式？",
        "有什么异常值或需要注意的数据质量问题吗？",
        "基于这些数据，你有什么业务洞察和建议？"
    ],
    
    'quality': [
        "生成完整的数据质量评估报告，包括数据完整性、一致性、准确性分析",
        "检测和报告所有数据质量问题：缺失值、重复值、异常值、格式错误",
        "评估数据的可信度和可用性，提供数据清洗建议",
        "分析数据源的稳定性和数据收集过程中的潜在问题"
    ],
    
    'business': [
        "创建商业智能仪表板，展示关键业务指标和KPI",
        "分析业务趋势，识别增长机会和风险点",
        "提供可执行的业务洞察和战略建议",
        "生成面向管理层的数据驱动决策支持报告"
    ],
    
    'statistical': [
        "生成详细的描述性统计分析，包含均值、中位数、标准差、分位数",
        "进行数据分布分析，包括正态性检验、偏度和峰度分析",
        "执行假设检验，验证数据的统计显著性",
        "创建置信区间分析和统计推断报告"
    ],
    
    'predictive': [
        "基于历史数据进行趋势预测和未来值估算",
        "识别数据中的季节性模式和周期性变化",
        "建立预测模型并评估预测准确性",
        "提供风险评估和不确定性分析"
    ],
    
    'correlation': [
        "创建全面的相关性分析矩阵，发现变量间的关联关系",
        "识别强相关和弱相关的变量对，分析因果关系",
        "进行多变量分析，探索复杂的交互效应",
        "提供基于相关性的特征选择和降维建议"
    ],
    
    'anomaly': [
        "使用多种统计方法检测数据中的异常值和离群点",
        "分析异常值的分布特征和可能的产生原因",
        "评估异常值对整体分析结果的影响",
        "提供异常值处理策略和数据清洗方案"
    ],
    
    'comprehensive': [
        "生成全面的数据科学报告，涵盖数据质量、统计分析、业务洞察",
        "创建多维度数据探索，包括单变量、双变量、多变量分析",
        "提供完整的数据故事，从原始数据到可执行的见解",
        "建立数据分析流水线，支持持续的数据监控和分析"
    ]
}

def print_help():
    """打印帮助信息"""
    print("🎯 高级数据分析工具")
    print("=" * 60)
    print("\n📋 使用方法:")
    print(f"python {sys.argv[0]} <文件路径> [报表类型] [自定义问题...]")
    
    print("\n📊 可用报表类型:")
    for report_type, questions in REPORT_TEMPLATES.items():
        print(f"\n🔹 {report_type}:")
        print(f"   {questions[0]}")
    
    print("\n📝 使用示例:")
    print(f"python {sys.argv[0]} data.csv quality")
    print(f"python {sys.argv[0]} data.csv business") 
    print(f"python {sys.argv[0]} data.csv custom '分析销售趋势' '预测收入增长'")
    print(f"python {sys.argv[0]} data.csv comprehensive")

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    if sys.argv[1] in ['-h', '--help', 'help']:
        print_help()
        return
    
    file_path = sys.argv[1]
    
    # 确定报表类型
    if len(sys.argv) >= 3:
        report_type = sys.argv[2].lower()
        if report_type == 'custom':
            # 自定义问题
            custom_questions = sys.argv[3:] if len(sys.argv) > 3 else None
            if not custom_questions:
                print("❌ 使用 custom 类型时需要提供自定义问题")
                print("示例: python analyze_advanced.py data.csv custom '问题1' '问题2'")
                return
            questions = custom_questions
        elif report_type in REPORT_TEMPLATES:
            questions = REPORT_TEMPLATES[report_type]
        else:
            print(f"❌ 未知的报表类型: {report_type}")
            print("可用类型:", list(REPORT_TEMPLATES.keys()))
            return
    else:
        # 默认使用综合报表
        report_type = 'comprehensive'
        questions = REPORT_TEMPLATES[report_type]
    
    print(f"🎯 分析文件: {file_path}")
    print(f"📊 报表类型: {report_type}")
    print("=" * 60)
    
    analyzer = FileDataAnalyzer()
    
    # 检查Ollama服务
    import requests
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code != 200:
            print("❌ Ollama服务未运行，请先启动: ollama serve")
            return
        
        models = response.json().get("models", [])
        if not models:
            print("❌ 未找到Ollama模型，请先下载模型")
            return
            
    except:
        print("❌ 无法连接到Ollama服务")
        return
    
    # 执行分析
    result = analyzer.analyze_file(file_path, questions)
    
    if "error" in result:
        print(f"❌ 分析失败: {result['error']}")
    else:
        print(f"\n🎉 {report_type.upper()} 报表分析完成！")
        if "chart_path" in result and result["chart_path"]:
            print(f"📊 高级图表已保存: {result['chart_path']}")
        
        # 保存详细结果到文件
        if result.get("analyses"):
            output_filename = f"report_{report_type}_{os.path.basename(file_path).split('.')[0]}.txt"
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(f"# {report_type.upper()} 数据分析报告\n")
                f.write(f"文件: {file_path}\n")
                f.write(f"生成时间: {pd.Timestamp.now()}\n")
                f.write("=" * 60 + "\n\n")
                
                for i, analysis in enumerate(result["analyses"], 1):
                    f.write(f"## 分析 {i}: {analysis['question']}\n\n")
                    f.write(f"{analysis['answer']}\n\n")
                    f.write("-" * 40 + "\n\n")
            
            print(f"📝 详细报告已保存: {output_filename}")

if __name__ == "__main__":
    main()