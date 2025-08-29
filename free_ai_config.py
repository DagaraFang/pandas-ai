"""
免费 AI API 配置指南

这个文件提供了多种免费AI API的配置选项，你可以根据需要选择使用。
"""
import os
from pandasai import Agent
from pandasai.llm import OpenAI

# ===== 配置选项 1: OpenAI (推荐 - 新用户有免费额度) =====
def setup_openai():
    """
    OpenAI API 配置
    新用户通常有 $5-18 的免费额度
    获取方式：https://platform.openai.com
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("请设置 OPENAI_API_KEY 环境变量")
        print("export OPENAI_API_KEY='your_api_key_here'")
        return None
    
    llm = OpenAI(api_token=api_key)
    print("✅ OpenAI API 配置成功")
    return llm

# ===== 配置选项 2: Ollama (完全免费，本地运行) =====
def setup_ollama():
    """
    Ollama 本地模型配置
    完全免费，无需API密钥
    需要先安装并启动 Ollama 服务
    """
    try:
        from pandasai.llm import Ollama
        
        # 检查 Ollama 服务是否运行
        import requests
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                if models:
                    print(f"✅ 发现 Ollama 模型: {[m['name'] for m in models]}")
                    # 使用第一个可用的模型
                    model_name = models[0]['name']
                    llm = Ollama(model=model_name, base_url="http://localhost:11434")
                    print(f"✅ Ollama 配置成功，使用模型: {model_name}")
                    return llm
                else:
                    print("❌ 未找到已下载的模型，请先下载模型：ollama pull codellama:7b")
            else:
                print("❌ Ollama 服务未运行，请先启动：ollama serve")
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到 Ollama 服务，请检查是否已启动")
        
    except ImportError:
        print("❌ 未安装 Ollama 支持，请安装：pip install ollama")
    
    return None

# ===== 配置选项 3: LiteLLM (支持多种免费API) =====
def setup_litellm():
    """
    LiteLLM 配置 - 支持多种免费模型
    包括 Hugging Face、Cohere 等
    """
    try:
        from pandasai.llm.litellm import LiteLLM
        
        # 示例：使用 Hugging Face 免费API
        hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
        if hf_token:
            llm = LiteLLM(
                model="huggingface/microsoft/DialoGPT-medium",
                api_key=hf_token
            )
            print("✅ LiteLLM (Hugging Face) 配置成功")
            return llm
        else:
            print("请设置 HUGGINGFACE_API_TOKEN 环境变量")
            print("获取方式：https://huggingface.co/settings/tokens")
    
    except ImportError:
        print("❌ 未安装 LiteLLM 支持")
    
    return None

# ===== 主配置函数 =====
def get_free_llm():
    """
    按优先级尝试获取免费的LLM配置
    """
    print("🔍 正在查找可用的免费AI API...")
    
    # 优先级1: 检查OpenAI
    if os.getenv("OPENAI_API_KEY"):
        llm = setup_openai()
        if llm:
            return llm
    
    # 优先级2: 检查Ollama本地服务
    llm = setup_ollama()
    if llm:
        return llm
    
    # 优先级3: 检查其他免费API
    llm = setup_litellm()
    if llm:
        return llm
    
    # 如果都不可用，提供设置指南
    print("\n❌ 未找到可用的免费AI API")
    print("\n推荐设置方案：")
    print("1. OpenAI (最简单)：")
    print("   - 访问 https://platform.openai.com")
    print("   - 创建账户并获取API Key")
    print("   - export OPENAI_API_KEY='your_key'")
    print("\n2. Ollama (完全免费)：")
    print("   - 已为你安装，正在下载模型...")
    print("   - 等待下载完成后即可使用")
    print("\n3. Hugging Face (部分免费)：")
    print("   - 访问 https://huggingface.co")
    print("   - 创建账户并获取token")
    print("   - export HUGGINGFACE_API_TOKEN='your_token'")
    
    return None

# ===== 使用示例 =====
def create_agent_with_free_llm(df):
    """
    使用免费LLM创建pandas-ai Agent
    """
    llm = get_free_llm()
    if llm:
        agent = Agent(df, config={"llm": llm})
        return agent
    else:
        print("无法创建Agent，请先配置AI API")
        return None

if __name__ == "__main__":
    # 测试配置
    get_free_llm()