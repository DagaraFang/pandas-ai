#!/bin/bash

# PandasAI 自动部署脚本
echo "🚀 开始部署 PandasAI..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Python版本
echo -e "${YELLOW}📋 检查Python版本...${NC}"
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python版本: $python_version"

if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 1 ]] && [[ $(echo "$python_version < 3.12" | bc -l) -eq 1 ]]; then
    echo -e "${GREEN}✅ Python版本符合要求${NC}"
else
    echo -e "${RED}❌ Python版本不符合要求，需要 3.8 <= version < 3.12${NC}"
    exit 1
fi

# 选择部署方式
echo -e "${YELLOW}📦 选择部署方式:${NC}"
echo "1) 快速安装 (仅安装库)"
echo "2) 开发环境 (完整开发环境)"
echo "3) 带Docker沙箱 (推荐生产环境)"
read -p "请输入选择 (1-3): " choice

case $choice in
    1)
        echo -e "${GREEN}🔧 执行快速安装...${NC}"
        pip3 install --upgrade pip
        pip3 install "pandasai>=3.0.0b2"
        pip3 install pandasai-openai
        echo -e "${GREEN}✅ 快速安装完成${NC}"
        ;;
    2)
        echo -e "${GREEN}🔧 设置开发环境...${NC}"
        
        # 检查Poetry是否安装
        if ! command -v poetry &> /dev/null; then
            echo -e "${YELLOW}📦 安装Poetry...${NC}"
            curl -sSL https://install.python-poetry.org | python3 -
            export PATH="$HOME/.local/bin:$PATH"
        fi
        
        # 安装项目依赖
        echo -e "${YELLOW}📦 安装项目依赖...${NC}"
        poetry install --all-extras --with dev
        
        echo -e "${GREEN}✅ 开发环境设置完成${NC}"
        echo -e "${YELLOW}💡 使用 'poetry shell' 激活虚拟环境${NC}"
        ;;
    3)
        echo -e "${GREEN}🔧 安装带Docker沙箱版本...${NC}"
        
        # 检查Docker是否安装
        if ! command -v docker &> /dev/null; then
            echo -e "${RED}❌ 需要先安装Docker${NC}"
            echo "请访问: https://docs.docker.com/get-docker/"
            exit 1
        fi
        
        pip3 install --upgrade pip
        pip3 install "pandasai>=3.0.0b2"
        pip3 install pandasai-openai
        pip3 install pandasai-docker
        
        echo -e "${GREEN}✅ Docker沙箱版本安装完成${NC}"
        ;;
    *)
        echo -e "${RED}❌ 无效选择${NC}"
        exit 1
        ;;
esac

# 创建示例文件
echo -e "${YELLOW}📝 创建使用示例...${NC}"
cat > example_usage.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PandasAI 使用示例
"""

import pandasai as pai
import os

# 检查是否有OpenAI API密钥
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("⚠️  请设置 OPENAI_API_KEY 环境变量")
    print("export OPENAI_API_KEY='your_api_key_here'")
    exit(1)

try:
    from pandasai_openai.openai import OpenAI
    
    # 配置LLM
    llm = OpenAI(api_key)
    pai.config.set({"llm": llm})
    
    # 创建示例数据
    df = pai.DataFrame({
        "country": ["中国", "美国", "日本", "德国", "英国"],
        "revenue": [7000, 5000, 4500, 4100, 3200],
        "profit": [1400, 1000, 900, 820, 640]
    })
    
    print("🎯 数据加载完成，可以开始提问了！")
    print("\n示例查询:")
    print("1. df.chat('哪个国家收入最高？')")
    print("2. df.chat('绘制收入分布图')")
    print("3. df.chat('计算平均利润')")
    
    # 交互式查询
    while True:
        try:
            query = input("\n💬 请输入您的问题 (输入 'quit' 退出): ")
            if query.lower() == 'quit':
                break
            
            result = df.chat(query)
            print(f"📊 结果: {result}")
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")

except ImportError:
    print("❌ 请先安装 pandasai-openai:")
    print("pip install pandasai-openai")
except Exception as e:
    print(f"❌ 初始化失败: {e}")
EOF

chmod +x example_usage.py

# 创建环境变量模板
cat > .env.template << 'EOF'
# PandasAI 环境变量配置

# OpenAI API密钥 (必需)
OPENAI_API_KEY=your_openai_api_key_here

# 其他LLM提供商 (可选)
# ANTHROPIC_API_KEY=your_anthropic_key
# GOOGLE_API_KEY=your_google_key

# 企业级功能 (可选)
# PINECONE_API_KEY=your_pinecone_key
# CHROMADB_HOST=localhost:8000

# PandasAI 配置
PANDASAI_SAVE_LOGS=true
PANDASAI_VERBOSE=true
PANDASAI_MAX_RETRIES=3
EOF

echo -e "${GREEN}🎉 部署完成！${NC}"
echo -e "${YELLOW}📋 下一步操作:${NC}"
echo "1. 复制 .env.template 为 .env 并填入API密钥"
echo "2. 运行示例: python3 example_usage.py"
echo "3. 查看文档: https://pandas-ai.readthedocs.io/"

if [[ $choice -eq 2 ]]; then
    echo -e "${YELLOW}💡 开发者提示:${NC}"
    echo "- 激活环境: poetry shell"
    echo "- 运行测试: poetry run pytest tests/unit_tests/"
    echo "- 代码格式化: poetry run ruff format ."
fi

echo -e "${GREEN}✨ 享受AI驱动的数据分析！${NC}"