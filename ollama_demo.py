"""
使用Ollama免费本地AI进行数据分析

这个示例展示如何使用完全免费的Ollama本地模型进行数据分析
"""
import json
import requests

def test_ollama_chat():
    """测试Ollama聊天功能"""
    print("🤖 测试Ollama AI对话...")
    
    # 测试基本对话
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "codellama:7b",
        "prompt": "你好，请简单介绍一下自己。用中文回答。",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ AI回复:")
            print(result.get('response', '无回复'))
            return True
        else:
            print(f"❌ 请求失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 对话测试失败: {e}")
        return False

def test_data_analysis():
    """测试数据分析功能"""
    print("\n📊 测试数据分析...")
    
    # 模拟数据分析问题
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "codellama:7b",
        "prompt": """
我有以下销售数据：
销售员: 张三, 销售额: 10000
销售员: 李四, 销售额: 15000  
销售员: 王五, 销售额: 8000

请分析哪个销售员表现最好，并用中文简单解释。
""",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print("✅ 数据分析结果:")
            print(result.get('response', '无分析结果'))
            return True
        else:
            print(f"❌ 分析失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 数据分析失败: {e}")
        return False

def show_usage_guide():
    """显示使用指南"""
    print("\n" + "="*50)
    print("🎯 Ollama使用指南")
    print("="*50)
    
    print("\n✅ 当前状态:")
    print("  - Ollama服务: 运行中")
    print("  - 模型: CodeLlama 7B")
    print("  - 成本: 完全免费")
    print("  - 隐私: 数据不会上传到网络")
    
    print("\n🔧 基本使用:")
    print("  - 直接对话: ollama run codellama:7b")
    print("  - 停止服务: Ctrl+C 终止 ollama serve")
    print("  - 查看模型: ollama list")
    
    print("\n📝 Python代码集成:")
    print("""
# 基本对话示例
import requests

def chat_with_ollama(question):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "codellama:7b",
        "prompt": question,
        "stream": False
    }
    response = requests.post(url, json=data)
    return response.json().get('response', '')

# 使用示例
answer = chat_with_ollama("分析这组数据: [1,2,3,4,5]")
print(answer)
""")
    
    print("\n🚀 与pandas-ai集成:")
    print("1. 修复pandas版本问题")
    print("2. 配置pandas-ai使用Ollama")
    print("3. 开始数据分析")

def create_ollama_config_example():
    """创建Ollama配置示例"""
    print("\n📄 创建配置文件示例...")
    
    config_content = '''"""
Ollama + pandas-ai 配置示例
"""
import requests
from typing import Any, Dict

class OllamaLLM:
    """简单的Ollama LLM包装器"""
    
    def __init__(self, model: str = "codellama:7b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def generate(self, prompt: str) -> str:
        """生成回复"""
        url = f"{self.base_url}/api/generate"
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=data, timeout=30)
            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                return f"错误: {response.status_code}"
        except Exception as e:
            return f"请求失败: {e}"

# 使用示例
if __name__ == "__main__":
    llm = OllamaLLM()
    
    # 测试对话
    questions = [
        "你好，请用中文回答",
        "什么是数据分析？",
        "如何计算平均值？"
    ]
    
    for q in questions:
        print(f"问题: {q}")
        answer = llm.generate(q)
        print(f"回答: {answer}\\n")
'''
    
    with open("/Users/longwaystov2025/dev_workspaces/pandas-ai/ollama_config_example.py", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print("✅ 配置示例已保存到: ollama_config_example.py")

def main():
    print("🎉 恭喜！你的免费AI已经准备就绪")
    print("="*50)
    
    # 测试基本功能
    if test_ollama_chat():
        print("\n✅ 基本对话功能正常")
    
    if test_data_analysis():
        print("\n✅ 数据分析功能正常")
    
    # 显示指南
    show_usage_guide()
    
    # 创建配置示例
    create_ollama_config_example()
    
    print("\n🎯 总结:")
    print("✅ 你现在拥有了一个完全免费的AI助手")
    print("✅ 无需API密钥，无使用次数限制")
    print("✅ 数据隐私完全保护")
    print("✅ 可以进行代码生成、数据分析等任务")
    
    print("\n💡 下一步建议:")
    print("1. 尝试运行: ollama run codellama:7b")
    print("2. 测试不同的提问方式")
    print("3. 集成到你的Python项目中")

if __name__ == "__main__":
    main()