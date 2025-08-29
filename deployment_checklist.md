# PandasAI 部署检查清单

## 🔍 部署前检查

### 系统要求检查
- [ ] Python 3.8+ < 3.12 ✅
- [ ] 可用内存 >= 4GB
- [ ] 磁盘空间 >= 2GB
- [ ] 网络连接正常（用于下载依赖）

### API密钥准备
- [ ] OpenAI API密钥（必需）
- [ ] 其他LLM提供商密钥（可选）
- [ ] 企业级服务密钥（可选）

## 🚀 部署方式选择

### 方式1: 快速体验 (推荐初学者)
```bash
# 运行自动部署脚本
./deploy.sh
# 选择选项 1
```

**适用场景:**
- 个人学习和体验
- 快速原型开发
- 简单数据分析任务

**安装内容:**
- pandasai 核心库
- pandasai-openai 扩展
- 基础示例代码

### 方式2: 开发环境 (推荐开发者)
```bash
# 运行自动部署脚本
./deploy.sh
# 选择选项 2
```

**适用场景:**
- 参与项目开发
- 自定义扩展开发
- 深度定制需求

**安装内容:**
- 完整源代码
- 开发依赖工具
- 测试框架
- 文档生成工具

### 方式3: 生产环境 (推荐企业)
```bash
# Docker单机部署
docker-compose -f docker-compose.production.yml up -d

# 或Kubernetes部署
kubectl apply -f k8s/
```

**适用场景:**
- 生产环境部署
- 多用户服务
- 高可用要求

**包含组件:**
- PandasAI应用容器
- ChromaDB向量数据库
- Redis缓存
- Jupyter Lab（可选）

## 🔧 环境配置

### 环境变量配置
```bash
# 复制模板文件
cp .env.template .env

# 编辑配置文件
nano .env
```

**必需变量:**
```bash
OPENAI_API_KEY=sk-your-key-here
```

**可选变量:**
```bash
# 其他LLM
ANTHROPIC_API_KEY=your-key
GOOGLE_API_KEY=your-key

# 企业功能
PINECONE_API_KEY=your-key
CHROMADB_HOST=localhost:8001

# 应用配置
PANDASAI_SAVE_LOGS=true
PANDASAI_VERBOSE=false
PANDASAI_MAX_RETRIES=3
```

### 数据目录准备
```bash
# 创建必要目录
mkdir -p data logs notebooks

# 设置权限
chmod 755 data logs notebooks
```

## ✅ 部署后验证

### 基础功能测试
```bash
# 运行示例代码
python3 example_usage.py

# 或交互式测试
python3 -c "
import pandasai as pai
from pandasai_openai.openai import OpenAI
llm = OpenAI('your-api-key')
pai.config.set({'llm': llm})
df = pai.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
print(df.chat('计算a列的平均值'))
"
```

### Docker部署验证
```bash
# 检查容器状态
docker-compose -f docker-compose.production.yml ps

# 查看日志
docker-compose -f docker-compose.production.yml logs pandasai

# 测试服务
curl http://localhost:8000/health
```

### 性能测试
```bash
# 内存使用检查
ps aux | grep python

# Docker资源使用
docker stats
```

## 🛠️ 故障排除

### 常见问题

#### 1. Python版本不兼容
**症状:** `ImportError` 或版本警告
**解决方案:**
```bash
# 检查版本
python3 --version

# 使用pyenv切换版本
pyenv install 3.11
pyenv local 3.11
```

#### 2. API密钥问题
**症状:** `Authentication failed` 或 `API key not found`
**解决方案:**
```bash
# 检查环境变量
echo $OPENAI_API_KEY

# 设置环境变量
export OPENAI_API_KEY="your-key-here"

# 验证密钥有效性
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### 3. 依赖安装失败
**症状:** `ModuleNotFoundError` 或安装错误
**解决方案:**
```bash
# 清理pip缓存
pip cache purge

# 升级pip
pip install --upgrade pip

# 强制重新安装
pip install --force-reinstall pandasai
```

#### 4. Docker问题
**症状:** 容器启动失败或服务不可用
**解决方案:**
```bash
# 检查Docker服务
docker --version
systemctl status docker

# 重建镜像
docker-compose -f docker-compose.production.yml build --no-cache

# 检查端口占用
netstat -tlnp | grep :8000
```

#### 5. 内存不足
**症状:** `MemoryError` 或处理缓慢
**解决方案:**
```bash
# 增加Docker内存限制
# 在docker-compose.yml中添加:
# deploy:
#   resources:
#     limits:
#       memory: 4G

# 或优化数据处理
df = df.sample(n=1000)  # 采样减少数据量
```

### 调试技巧

#### 启用详细日志
```python
import pandasai as pai

pai.config.set({
    "verbose": True,
    "save_logs": True
})
```

#### 检查生成的代码
```python
agent = pai.Agent([df])
agent.chat("your question")
print("Generated code:", agent.last_code_generated)
```

#### 沙箱调试
```python
from pandasai_docker import DockerSandbox

sandbox = DockerSandbox()
sandbox.start()

# 在沙箱中调试
result = sandbox.execute("print('Hello from sandbox')")
print(result)

sandbox.stop()
```

## 🔄 升级和维护

### 版本升级
```bash
# 升级库版本
pip install --upgrade pandasai

# Poetry环境升级
poetry update

# Docker镜像更新
docker-compose pull
docker-compose up -d
```

### 数据备份
```bash
# 备份配置和数据
tar -czf pandasai-backup.tar.gz \
  .env data/ logs/ notebooks/

# 恢复备份
tar -xzf pandasai-backup.tar.gz
```

### 性能监控
```bash
# 安装监控工具
pip install psutil

# 监控脚本
python3 -c "
import psutil
print(f'CPU: {psutil.cpu_percent()}%')
print(f'内存: {psutil.virtual_memory().percent}%')
"
```

## 📞 获取帮助

- **官方文档**: https://pandas-ai.readthedocs.io/
- **GitHub仓库**: https://github.com/sinaptik-ai/pandas-ai
- **Discord社区**: https://discord.gg/KYKj9F2FRH
- **问题报告**: https://github.com/sinaptik-ai/pandas-ai/issues