"""
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
        print(f"回答: {answer}\n")
