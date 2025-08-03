# 通用任务链控制器插件 - 部署指南

## 📋 部署概述

本指南详细说明如何在不同环境中部署和配置通用任务链控制器插件，包括本地开发、测试环境和生产环境的部署方案。

## 🏗️ 系统要求

### Python版本要求
- **Python版本**: 3.8 或更高版本
- **内存要求**: 最少 512MB，推荐 1GB+
- **存储空间**: 最少 100MB
- **网络**: 支持HTTPS访问（用于扣子平台通信）

### JavaScript版本要求
- **Node.js版本**: 14.0 或更高版本
- **内存要求**: 最少 256MB，推荐 512MB+
- **存储空间**: 最少 50MB
- **网络**: 支持HTTPS访问（用于扣子平台通信）

### 通用要求
- **操作系统**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **网络延迟**: < 500ms（与扣子平台通信）
- **并发支持**: 根据需求配置，建议支持10-50个并发请求

## 🚀 快速部署

### 方式一：Python版本部署

#### 1. 环境准备

```bash
# 检查Python版本
python --version  # 应该 >= 3.8

# 创建虚拟环境（推荐）
python -m venv taskchain_env

# 激活虚拟环境
# Windows
taskchain_env\Scripts\activate
# macOS/Linux
source taskchain_env/bin/activate
```

#### 2. 安装依赖

```bash
# 进入Python版本目录
cd python_version

# 安装依赖
pip install -r requirements.txt

# 验证安装
python -c "import dataclasses, json, time, uuid; print('依赖安装成功')"
```

#### 3. 配置验证

```bash
# 运行基础测试
python main.py

# 如果看到测试输出，说明部署成功
```

### 方式二：JavaScript版本部署

#### 1. 环境准备

```bash
# 检查Node.js版本
node --version  # 应该 >= 14.0
npm --version
```

#### 2. 安装依赖

```bash
# 进入JavaScript版本目录
cd javascript_version

# 安装依赖
npm install

# 验证安装
npm run test  # 如果配置了测试脚本
```

#### 3. 配置验证

```bash
# 运行基础测试
node index.js

# 如果看到测试输出，说明部署成功
```

## 🔧 扣子平台集成

### 1. 插件上传

#### Python版本上传

1. **准备文件**:
   ```
   python_version/
   ├── main.py          # 主程序文件
   ├── metadata.json    # 插件元数据
   └── requirements.txt # 依赖文件
   ```

2. **压缩文件**:
   ```bash
   # 创建部署包
   zip -r taskchain_controller_python.zip python_version/
   ```

3. **上传到扣子**:
   - 登录扣子开发者平台
   - 选择「插件管理」→「创建插件」
   - 上传 `taskchain_controller_python.zip`
   - 填写插件信息

#### JavaScript版本上传

1. **准备文件**:
   ```
   javascript_version/
   ├── index.js         # 主程序文件
   ├── metadata.json    # 插件元数据
   └── package.json     # 依赖文件
   ```

2. **压缩文件**:
   ```bash
   # 创建部署包
   zip -r taskchain_controller_js.zip javascript_version/
   ```

3. **上传到扣子**:
   - 同Python版本流程

### 2. 插件配置

#### 基础配置

```json
{
  "name": "通用任务链控制器",
  "description": "通过结构化任务链确保AI思考的系统性和完整性",
  "version": "1.0.0",
  "category": "工作流程",
  "tags": ["任务管理", "工作流", "分析工具", "创意助手"]
}
```

#### 权限配置

```json
{
  "permissions": {
    "network": false,      // 不需要网络访问
    "storage": false,      // 不需要持久化存储
    "compute": "medium"    // 中等计算资源
  },
  "timeout": 30,           // 30秒超时
  "memory_limit": "512MB", // 内存限制
  "concurrent_limit": 10   // 并发限制
}
```

### 3. 测试验证

#### 功能测试

```json
{
  "test_cases": [
    {
      "name": "基础分析任务",
      "input": {
        "task_type": "analysis",
        "target": "测试分析目标",
        "config": {"depth": "basic"}
      },
      "expected_success": true
    },
    {
      "name": "错误处理测试",
      "input": {
        "target": "缺少任务类型"
      },
      "expected_success": false
    }
  ]
}
```

## 🏢 生产环境部署

### 1. 容器化部署（推荐）

#### Docker部署 - Python版本

**Dockerfile**:
```dockerfile
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "from main import handler; print('OK')" || exit 1

# 运行应用
CMD ["python", "main.py"]
```

**构建和运行**:
```bash
# 构建镜像
docker build -t taskchain-controller-python .

# 运行容器
docker run -d \
  --name taskchain-controller \
  --memory=1g \
  --cpus=1 \
  -p 8080:8080 \
  taskchain-controller-python
```

#### Docker部署 - JavaScript版本

**Dockerfile**:
```dockerfile
FROM node:16-alpine

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制应用代码
COPY . .

# 创建非root用户
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001
USER nodejs

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "require('./index.js'); console.log('OK')" || exit 1

# 运行应用
CMD ["node", "index.js"]
```

### 2. 云平台部署

#### AWS Lambda部署

**部署包准备**:
```bash
# Python版本
zip -r lambda-deployment.zip python_version/

# JavaScript版本
zip -r lambda-deployment.zip javascript_version/
```

**Lambda配置**:
```json
{
  "FunctionName": "taskchain-controller",
  "Runtime": "python3.9",  // 或 "nodejs16.x"
  "Handler": "main.handler", // 或 "index.handler"
  "MemorySize": 512,
  "Timeout": 30,
  "Environment": {
    "Variables": {
      "LOG_LEVEL": "INFO"
    }
  }
}
```

#### 阿里云函数计算部署

**fun.yml配置**:
```yaml
ROSTemplateFormatVersion: '2015-09-01'
Transform: 'Aliyun::Serverless-2018-04-03'
Resources:
  taskchain-controller:
    Type: 'Aliyun::Serverless::Service'
    Properties:
      Description: '任务链控制器插件'
    taskchain-function:
      Type: 'Aliyun::Serverless::Function'
      Properties:
        Handler: main.handler
        Runtime: python3.9
        CodeUri: './python_version'
        MemorySize: 512
        Timeout: 30
```

### 3. 监控和日志

#### 日志配置

**Python版本日志**:
```python
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('taskchain.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('TaskChainController')

# 在handler中添加日志
def handler(input_data):
    session_id = str(uuid.uuid4())
    logger.info(f"[{session_id}] 任务开始: {input_data.get('task_type', 'unknown')}")
    
    try:
        # 执行任务逻辑
        result = controller.execute_task_chain(input_data)
        logger.info(f"[{session_id}] 任务完成: {result['success']}")
        return result
    except Exception as e:
        logger.error(f"[{session_id}] 任务失败: {str(e)}")
        raise
```

**JavaScript版本日志**:
```javascript
const winston = require('winston');

// 配置日志
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ filename: 'taskchain.log' }),
        new winston.transports.Console()
    ]
});

// 在handler中添加日志
async function handler(inputData) {
    const sessionId = require('crypto').randomUUID();
    logger.info(`[${sessionId}] 任务开始`, { taskType: inputData.task_type });
    
    try {
        const result = await controller.executeTaskChain(inputData);
        logger.info(`[${sessionId}] 任务完成`, { success: result.success });
        return result;
    } catch (error) {
        logger.error(`[${sessionId}] 任务失败`, { error: error.message });
        throw error;
    }
}
```

#### 性能监控

**监控指标**:
```json
{
  "metrics": {
    "execution_time": "任务执行时间",
    "success_rate": "任务成功率",
    "error_rate": "错误率",
    "memory_usage": "内存使用量",
    "concurrent_requests": "并发请求数"
  },
  "alerts": {
    "execution_time_threshold": "10s",
    "error_rate_threshold": "5%",
    "memory_usage_threshold": "80%"
  }
}
```

## 🔒 安全配置

### 1. 输入验证

```python
# Python版本安全配置
def validate_input(input_data):
    """严格的输入验证"""
    
    # 检查必需字段
    required_fields = ['task_type', 'target']
    for field in required_fields:
        if field not in input_data:
            raise ValueError(f"缺少必需字段: {field}")
    
    # 验证任务类型
    valid_task_types = ['analysis', 'creative', 'education', 'research', 'custom']
    if input_data['task_type'] not in valid_task_types:
        raise ValueError(f"无效的任务类型: {input_data['task_type']}")
    
    # 验证目标长度
    if len(input_data['target']) > 1000:
        raise ValueError("目标描述过长")
    
    # 验证自定义任务链
    if input_data['task_type'] == 'custom':
        if 'custom_chain' not in input_data:
            raise ValueError("自定义任务需要提供custom_chain")
        
        if len(input_data['custom_chain']) > 20:
            raise ValueError("自定义任务链步骤过多")
    
    return True
```

### 2. 资源限制

```python
# 资源限制配置
RESOURCE_LIMITS = {
    'max_execution_time': 30,      # 最大执行时间（秒）
    'max_memory_usage': 512,       # 最大内存使用（MB）
    'max_task_chain_length': 20,   # 最大任务链长度
    'max_target_length': 1000,     # 最大目标描述长度
    'max_concurrent_tasks': 10     # 最大并发任务数
}

def check_resource_limits(input_data):
    """检查资源限制"""
    
    # 检查任务链长度
    if input_data.get('task_type') == 'custom':
        chain_length = len(input_data.get('custom_chain', []))
        if chain_length > RESOURCE_LIMITS['max_task_chain_length']:
            raise ValueError(f"任务链长度超限: {chain_length}")
    
    # 检查目标长度
    target_length = len(input_data.get('target', ''))
    if target_length > RESOURCE_LIMITS['max_target_length']:
        raise ValueError(f"目标描述超限: {target_length}")
    
    return True
```

### 3. 错误处理

```python
# 统一错误处理
class TaskChainError(Exception):
    """任务链执行错误"""
    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

def safe_handler(input_data):
    """安全的处理函数"""
    try:
        # 输入验证
        validate_input(input_data)
        check_resource_limits(input_data)
        
        # 执行任务
        result = handler(input_data)
        return result
        
    except ValueError as e:
        return {
            'success': False,
            'error_code': 'VALIDATION_ERROR',
            'error': str(e)
        }
    except TaskChainError as e:
        return {
            'success': False,
            'error_code': e.error_code or 'EXECUTION_ERROR',
            'error': e.message
        }
    except Exception as e:
        return {
            'success': False,
            'error_code': 'INTERNAL_ERROR',
            'error': '内部错误，请联系管理员'
        }
```

## 📊 性能优化

### 1. 缓存策略

```python
# Python版本缓存
from functools import lru_cache
import hashlib

class TaskChainController:
    def __init__(self):
        self.result_cache = {}
        self.cache_ttl = 3600  # 1小时
    
    def get_cache_key(self, input_data):
        """生成缓存键"""
        cache_data = {
            'task_type': input_data.get('task_type'),
            'target': input_data.get('target'),
            'config': input_data.get('config', {})
        }
        return hashlib.md5(str(cache_data).encode()).hexdigest()
    
    @lru_cache(maxsize=100)
    def get_task_chain_template(self, task_type):
        """缓存任务链模板"""
        return self._load_task_chain_template(task_type)
```

### 2. 异步处理

```javascript
// JavaScript版本异步优化
class TaskChainController {
    async executeTaskChain(inputData) {
        const tasks = this.loadTaskChain(inputData);
        const results = [];
        
        // 并行执行独立任务
        const independentTasks = tasks.filter(task => !task.dependencies);
        const independentResults = await Promise.all(
            independentTasks.map(task => this.executeTask(task, inputData))
        );
        
        results.push(...independentResults);
        
        // 串行执行依赖任务
        const dependentTasks = tasks.filter(task => task.dependencies);
        for (const task of dependentTasks) {
            const result = await this.executeTask(task, inputData, results);
            results.push(result);
        }
        
        return this.generateFinalReport(inputData, results);
    }
}
```

## 🔄 维护和更新

### 1. 版本管理

```json
{
  "version_strategy": {
    "major": "重大功能变更或不兼容更新",
    "minor": "新功能添加，向后兼容",
    "patch": "错误修复和小幅改进"
  },
  "update_process": {
    "1": "开发环境测试",
    "2": "预发布环境验证",
    "3": "生产环境灰度发布",
    "4": "全量发布"
  }
}
```

### 2. 备份策略

```bash
#!/bin/bash
# 备份脚本

BACKUP_DIR="/backup/taskchain-controller"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份代码
tar -czf $BACKUP_DIR/code_$DATE.tar.gz python_version/ javascript_version/

# 备份配置
cp metadata.json $BACKUP_DIR/metadata_$DATE.json

# 清理旧备份（保留30天）
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.json" -mtime +30 -delete

echo "备份完成: $DATE"
```

### 3. 健康检查

```python
# 健康检查端点
def health_check():
    """系统健康检查"""
    checks = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'checks': {
            'memory': check_memory_usage(),
            'capabilities': check_capabilities(),
            'dependencies': check_dependencies()
        }
    }
    
    # 检查是否有失败项
    failed_checks = [k for k, v in checks['checks'].items() if not v['healthy']]
    if failed_checks:
        checks['status'] = 'unhealthy'
        checks['failed_checks'] = failed_checks
    
    return checks

def check_memory_usage():
    """检查内存使用"""
    import psutil
    memory = psutil.virtual_memory()
    return {
        'healthy': memory.percent < 80,
        'usage_percent': memory.percent,
        'available_mb': memory.available // 1024 // 1024
    }

def check_capabilities():
    """检查能力模块"""
    try:
        registry = CapabilityRegistry()
        capabilities = registry.list_capabilities()
        return {
            'healthy': len(capabilities) >= 10,
            'count': len(capabilities),
            'capabilities': list(capabilities.keys())
        }
    except Exception as e:
        return {
            'healthy': False,
            'error': str(e)
        }
```

## 📞 故障排除

### 常见问题和解决方案

#### 1. 部署失败

**问题**: 依赖安装失败
```bash
# 解决方案
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir

# 或者使用conda
conda create -n taskchain python=3.9
conda activate taskchain
pip install -r requirements.txt
```

**问题**: 权限错误
```bash
# 解决方案
sudo chown -R $USER:$USER /path/to/project
chmod +x main.py
```

#### 2. 运行时错误

**问题**: 内存不足
```python
# 解决方案：优化内存使用
def optimize_memory():
    import gc
    gc.collect()  # 强制垃圾回收
    
    # 限制任务链长度
    MAX_CHAIN_LENGTH = 10
    
    # 使用生成器减少内存占用
    def process_tasks_generator(tasks):
        for task in tasks:
            yield process_task(task)
            gc.collect()
```

**问题**: 超时错误
```python
# 解决方案：添加超时控制
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("任务执行超时")

def execute_with_timeout(func, timeout=30):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        result = func()
        signal.alarm(0)  # 取消超时
        return result
    except TimeoutError:
        return {'success': False, 'error': '任务执行超时'}
```

#### 3. 性能问题

**问题**: 响应时间过长
```python
# 解决方案：性能分析和优化
import cProfile
import pstats

def profile_execution(input_data):
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = handler(input_data)
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # 显示前10个最耗时的函数
    
    return result
```

### 联系支持

如果遇到无法解决的问题，请联系技术支持：

- **邮箱**: support@example.com
- **文档**: https://docs.example.com/taskchain-controller
- **GitHub**: https://github.com/example/taskchain-controller
- **社区论坛**: https://community.example.com

---

**部署指南版本**: 1.0.0  
**最后更新**: 2025-08-03  
**维护团队**: 字伯升 (vx: zibosheng88)