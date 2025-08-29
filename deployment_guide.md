# PandasAI 部署指南

## 方案A: 个人/学习使用

### 1. 环境准备
```bash
# 检查Python版本
python3 --version  # 需要 3.8+ < 3.12

# 创建虚拟环境
python3 -m venv pandasai_env
source pandasai_env/bin/activate  # Linux/macOS
# pandasai_env\Scripts\activate  # Windows
```

### 2. 快速安装
```bash
# 基础安装
pip install "pandasai>=3.0.0b2"

# 安装OpenAI支持
pip install pandasai-openai

# 安装其他常用库
pip install jupyter notebook
```

### 3. 基础使用示例
```python
import pandasai as pai
from pandasai_openai.openai import OpenAI

# 配置LLM
llm = OpenAI("YOUR_OPENAI_API_KEY")
pai.config.set({"llm": llm})

# 创建数据框
df = pai.DataFrame({
    "country": ["China", "USA", "Japan", "Germany", "UK"],
    "revenue": [7000, 5000, 4500, 4100, 3200]
})

# 自然语言查询
result = df.chat('哪个国家收入最高？')
print(result)
```

## 方案B: 开发环境

### 1. 克隆项目
```bash
git clone https://github.com/sinaptik-ai/pandas-ai.git
cd pandas-ai
```

### 2. 安装Poetry
```bash
# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows PowerShell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python3 -
```

### 3. 安装依赖
```bash
# 安装核心依赖
poetry install --all-extras --with dev

# 安装扩展依赖
make install_extension_deps

# 激活环境
poetry shell
```

### 4. 运行测试
```bash
# 运行核心测试
make test_core

# 运行所有测试
make test_all

# 代码格式化
make format
```

## 方案C: 生产部署

### 1. Docker部署
```bash
# 构建Docker镜像
docker build -t pandasai-app .

# 运行容器
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  pandasai-app
```

### 2. 使用Docker沙箱
```python
from pandasai_docker import DockerSandbox

# 启动沙箱
sandbox = DockerSandbox()
sandbox.start()

# 在沙箱中执行查询
result = pai.chat("分析数据", df, sandbox=sandbox)

# 关闭沙箱
sandbox.stop()
```

## 环境变量配置

### 必需的API密钥
```bash
# OpenAI
export OPENAI_API_KEY="your_openai_api_key"

# 其他LLM提供商（可选）
export ANTHROPIC_API_KEY="your_anthropic_key"
export GOOGLE_API_KEY="your_google_key"

# 企业级功能（可选）
export PINECONE_API_KEY="your_pinecone_key"
export CHROMADB_HOST="localhost:8000"
```

### 配置文件示例
```python
# config.py
import pandasai as pai

pai.config.set({
    "llm": llm,
    "save_logs": True,
    "verbose": True,
    "max_retries": 3,
})
```

## 扩展安装选项

### LLM扩展
```bash
# OpenAI
pip install pandasai-openai

# LiteLLM (支持多种LLM)
pip install pandasai-litellm
```

### 连接器扩展
```bash
# SQL连接器
pip install pandasai-sql

# Yahoo Finance
pip install pandasai-yfinance
```

### 企业级扩展
```bash
# 向量数据库
pip install pandasai-chromadb
pip install pandasai-pinecone

# 企业数据库
pip install pandasai-bigquery
pip install pandasai-snowflake
```

## 常见问题

### Q: Python版本兼容性
A: 必须使用 Python 3.8+ < 3.12，不支持 3.12+

### Q: 内存要求
A: 建议至少 4GB RAM，大数据集需要更多内存

### Q: API密钥安全
A: 生产环境请使用环境变量，不要硬编码在代码中

### Q: 沙箱执行
A: 生产环境强烈建议使用Docker沙箱确保安全性