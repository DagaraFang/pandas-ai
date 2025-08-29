"""
免费AI API使用示例

这个示例展示如何使用免费的AI API来分析数据
"""
import pandas as pd
import os

# 导入我们的免费AI配置
from free_ai_config import get_free_llm, create_agent_with_free_llm

def demo_with_sample_data():
    """
    使用示例数据演示免费AI API的功能
    """
    print("🚀 开始免费AI数据分析演示...")
    
    # 创建示例数据
    data = {
        '销售员': ['张三', '李四', '王五', '赵六', '钱七'],
        '销售额': [10000, 15000, 8000, 12000, 9000],
        '地区': ['北京', '上海', '广州', '深圳', '杭州'],
        '产品': ['笔记本', '台式机', '平板', '手机', '耳机']
    }
    
    df = pd.DataFrame(data)
    print("📊 示例数据：")
    print(df)
    print()
    
    # 尝试创建Agent
    agent = create_agent_with_free_llm(df)
    
    if agent:
        print("✅ Agent创建成功！可以开始提问了...")
        print("\n💡 示例问题：")
        print("- '哪个销售员的销售额最高？'")
        print("- '不同地区的平均销售额是多少？'")
        print("- '生成一个销售额的柱状图'")
        
        # 如果有可用的LLM，可以尝试一个简单的问题
        try:
            result = agent.chat("哪个销售员的销售额最高？")
            print(f"\n🤖 AI回答: {result}")
        except Exception as e:
            print(f"\n⚠️  查询失败: {e}")
            print("这可能是因为模型仍在下载中或配置问题")
    
    return agent

def demo_with_openai():
    """
    专门演示OpenAI API的使用方法
    """
    print("\n=== OpenAI API 使用示例 ===")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("请先设置OpenAI API Key：")
        print("1. 访问 https://platform.openai.com")
        print("2. 注册并获取API Key")
        print("3. 运行: export OPENAI_API_KEY='your_key_here'")
        return
    
    from pandasai.llm import OpenAI
    from pandasai import Agent
    
    # 创建示例数据
    df = pd.DataFrame({
        '月份': ['1月', '2月', '3月', '4月', '5月'],
        '收入': [50000, 60000, 55000, 70000, 65000],
        '支出': [30000, 35000, 32000, 45000, 40000]
    })
    
    # 配置OpenAI
    llm = OpenAI(api_token=api_key)
    agent = Agent(df, config={"llm": llm})
    
    print("📊 财务数据：")
    print(df)
    
    # 示例查询
    questions = [
        "哪个月的净利润最高？",
        "计算每个月的净利润",
        "生成收入和支出的对比图"
    ]
    
    for question in questions:
        try:
            print(f"\n❓ 问题: {question}")
            result = agent.chat(question)
            print(f"🤖 回答: {result}")
        except Exception as e:
            print(f"❌ 错误: {e}")

def demo_with_ollama():
    """
    专门演示Ollama本地模型的使用
    """
    print("\n=== Ollama 本地模型使用示例 ===")
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code != 200:
            print("❌ Ollama服务未运行，请先启动：")
            print("ollama serve")
            return
        
        models = response.json().get("models", [])
        if not models:
            print("❌ 未找到模型，请先下载：")
            print("ollama pull codellama:7b")
            return
        
        print(f"✅ 可用模型: {[m['name'] for m in models]}")
        
        # 使用Ollama
        from pandasai.llm import Ollama
        from pandasai import Agent
        
        llm = Ollama(model=models[0]['name'])
        df = pd.DataFrame({
            '学生': ['小明', '小红', '小刚', '小丽'],
            '数学': [85, 92, 78, 96],
            '语文': [88, 85, 90, 94],
            '英语': [82, 94, 76, 98]
        })
        
        agent = Agent(df, config={"llm": llm})
        
        print("📊 学生成绩数据：")
        print(df)
        
        # 简单查询
        result = agent.chat("哪个学生的总分最高？")
        print(f"\n🤖 AI回答: {result}")
        
    except Exception as e:
        print(f"❌ Ollama配置失败: {e}")

if __name__ == "__main__":
    print("🎯 免费AI API演示程序")
    print("=" * 50)
    
    # 基础演示
    demo_with_sample_data()
    
    # 根据环境选择演示
    if os.getenv("OPENAI_API_KEY"):
        demo_with_openai()
    
    # 检查Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            demo_with_ollama()
    except:
        print("\n💡 提示：Ollama模型下载完成后，可以运行本地免费AI分析")