#!/usr/bin/env python3
"""
Ollama数据分析对话工具

使用方法:
1. python data_chat.py - 启动交互对话
2. python data_chat.py "你的问题" - 单次问答
"""

import sys
import requests
import json
from pathlib import Path

class DataAnalysisChat:
    def __init__(self, model="codellama:7b"):
        self.model = model
        self.base_url = "http://localhost:11434"
        self.session_history = []
    
    def chat(self, question: str) -> str:
        """与AI对话"""
        url = f"{self.base_url}/api/generate"
        
        # 添加数据分析的上下文
        prompt = f"""你是一个数据分析专家助手。请用中文回答问题。

用户问题: {question}

请提供专业的数据分析建议、代码示例或解决方案。"""
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=data, timeout=60)
            if response.status_code == 200:
                result = response.json().get('response', '')
                self.session_history.append({"question": question, "answer": result})
                return result
            else:
                return f"❌ 请求失败: {response.status_code}"
        except Exception as e:
            return f"❌ 连接失败: {e}"
    
    def interactive_mode(self):
        """交互模式"""
        print("🤖 Ollama数据分析助手已启动")
        print("💡 提示：")
        print("   - 输入 'exit' 或 'quit' 退出")
        print("   - 输入 'history' 查看对话历史")
        print("   - 输入 'clear' 清空历史")
        print("   - 直接提问进行数据分析")
        print("-" * 50)
        
        while True:
            try:
                question = input("\n📊 您的问题: ").strip()
                
                if question.lower() in ['exit', 'quit', '退出']:
                    print("👋 再见！")
                    break
                elif question.lower() == 'history':
                    self.show_history()
                elif question.lower() == 'clear':
                    self.session_history.clear()
                    print("✅ 历史记录已清空")
                elif question:
                    print("🤖 AI分析中...")
                    answer = self.chat(question)
                    print(f"\n💡 回答:\n{answer}")
                
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")
    
    def show_history(self):
        """显示对话历史"""
        if not self.session_history:
            print("📝 暂无对话历史")
            return
        
        print("\n📝 对话历史:")
        print("-" * 30)
        for i, item in enumerate(self.session_history, 1):
            print(f"\n{i}. 问题: {item['question']}")
            print(f"   回答: {item['answer'][:100]}...")

def check_ollama_service():
    """检查Ollama服务状态"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    # 检查服务状态
    if not check_ollama_service():
        print("❌ Ollama服务未运行，请先启动:")
        print("ollama serve")
        return
    
    chat = DataAnalysisChat()
    
    # 根据参数决定模式
    if len(sys.argv) > 1:
        # 单次问答模式
        question = " ".join(sys.argv[1:])
        print(f"📊 问题: {question}")
        print("🤖 AI分析中...")
        answer = chat.chat(question)
        print(f"\n💡 回答:\n{answer}")
    else:
        # 交互模式
        chat.interactive_mode()

if __name__ == "__main__":
    main()