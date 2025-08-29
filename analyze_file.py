#!/usr/bin/env python3
"""
简化的文件数据分析工具

使用方法:
python analyze_file.py <文件路径> [问题1] [问题2] ...

示例:
python analyze_file.py data.csv "分析销售趋势" "找出异常值"
"""
import sys
import os
from typing import List, Optional
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from smart_file_analyzer import FileDataAnalyzer

def main():
    if len(sys.argv) < 2:
        print("📋 使用方法:")
        print(f"python {sys.argv[0]} <文件路径> [问题1] [问题2] ...")
        print("\n📝 示例:")
        print(f"python {sys.argv[0]} data.csv '分析销售趋势' '找出异常值'")
        print(f"python {sys.argv[0]} test_data/employee_data.csv")
        return
    
    file_path = sys.argv[1]
    
    # 自定义问题（如果提供）
    custom_questions = sys.argv[2:] if len(sys.argv) > 2 else None
    
    print(f"🎯 分析文件: {file_path}")
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
    if custom_questions:
        result = analyzer.analyze_file(file_path, custom_questions)
    else:
        result = analyzer.analyze_file(file_path)
    
    if "error" in result:
        print(f"❌ 分析失败: {result['error']}")
    else:
        print("\n🎉 分析完成！")
        if "chart_path" in result and result["chart_path"]:
            print(f"📊 图表已保存: {result['chart_path']}")

if __name__ == "__main__":
    main()