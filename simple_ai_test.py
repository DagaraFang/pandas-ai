"""
简化的免费AI配置测试

测试各种免费AI API的可用性
"""
import os
import requests

def test_openai_config():
    """测试OpenAI API配置"""
    print("=== OpenAI API 测试 ===")
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ 找到OpenAI API Key: {api_key[:8]}...")
        return True
    else:
        print("❌ 未设置 OPENAI_API_KEY")
        print("获取方式：")
        print("1. 访问 https://platform.openai.com")
        print("2. 注册账户并获取API Key (新用户有$5-18免费额度)")
        print("3. 运行: export OPENAI_API_KEY='your_key_here'")
        return False

def test_ollama_config():
    """测试Ollama本地服务"""
    print("\n=== Ollama 本地模型测试 ===")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print("✅ Ollama服务正在运行")
                print(f"✅ 可用模型: {[m['name'] for m in models]}")
                return True
            else:
                print("⚠️  Ollama服务运行中，但无可用模型")
                print("下载模型: ollama pull codellama:7b")
                return False
        else:
            print("❌ Ollama服务响应异常")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Ollama服务")
        print("启动方法: ollama serve")
        return False
    except Exception as e:
        print(f"❌ Ollama测试失败: {e}")
        return False

def test_huggingface_config():
    """测试Hugging Face配置"""
    print("\n=== Hugging Face API 测试 ===")
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    if hf_token:
        print(f"✅ 找到Hugging Face Token: {hf_token[:8]}...")
        return True
    else:
        print("❌ 未设置 HUGGINGFACE_API_TOKEN")
        print("获取方式：")
        print("1. 访问 https://huggingface.co")
        print("2. 注册账户")
        print("3. 在 Settings > Access Tokens 创建token")
        print("4. 运行: export HUGGINGFACE_API_TOKEN='your_token'")
        return False

def show_recommendations():
    """显示推荐方案"""
    print("\n" + "="*50)
    print("🎯 推荐的免费AI方案:")
    print("="*50)
    
    print("\n💰 方案1: OpenAI (推荐新手)")
    print("  优势: 性能最好，集成简单")
    print("  免费额度: 新用户$5-18")
    print("  设置: export OPENAI_API_KEY='your_key'")
    
    print("\n🏠 方案2: Ollama (推荐开发者)")
    print("  优势: 完全免费，本地运行，隐私保护")
    print("  要求: 需要下载模型(3.8GB)")
    print("  状态: 正在为你下载CodeLlama模型...")
    
    print("\n🤖 方案3: Hugging Face")
    print("  优势: 开源模型丰富")
    print("  限制: 免费额度有限")
    print("  适合: 实验和学习")

def check_ollama_download_progress():
    """检查Ollama模型下载进度"""
    print("\n=== 检查CodeLlama下载进度 ===")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            models = response.json().get("models", [])
            codellama_models = [m for m in models if 'codellama' in m['name'].lower()]
            if codellama_models:
                print("✅ CodeLlama模型下载完成！")
                print(f"可用模型: {[m['name'] for m in codellama_models]}")
                print("\n🎉 现在你可以使用完全免费的本地AI了！")
                return True
            else:
                print("⏳ CodeLlama模型仍在下载中...")
                print("💡 下载完成后，你将拥有完全免费的本地AI助手")
                return False
    except:
        print("⏳ Ollama服务准备中...")
        return False

def main():
    print("🔍 免费AI API配置检查")
    print("="*40)
    
    # 测试各种配置
    has_openai = test_openai_config()
    has_ollama = test_ollama_config()
    has_hf = test_huggingface_config()
    
    # 检查Ollama下载进度
    ollama_ready = check_ollama_download_progress()
    
    # 总结
    print("\n" + "="*40)
    print("📊 配置状态总结:")
    print("="*40)
    
    available_count = sum([has_openai, has_ollama, has_hf])
    
    if available_count == 0:
        print("❌ 暂无可用的AI API配置")
        if ollama_ready:
            print("✅ 但是Ollama本地模型已就绪！")
        show_recommendations()
    else:
        print(f"✅ 找到 {available_count} 个可用配置")
        if has_openai:
            print("  - OpenAI API ✓")
        if has_ollama:
            print("  - Ollama本地模型 ✓") 
        if has_hf:
            print("  - Hugging Face ✓")
    
    # 下一步指导
    print("\n🚀 下一步:")
    if has_openai or has_ollama or has_hf:
        print("你已经可以开始使用pandas-ai进行数据分析了！")
        print("运行示例: python demo_free_ai.py")
    else:
        print("请先配置至少一个AI API，推荐从OpenAI开始")

if __name__ == "__main__":
    main()