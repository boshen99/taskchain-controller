# 通用任务链控制器插件 - 测试示例

## 📋 测试概述

本文档提供了通用任务链控制器插件的全面测试示例，包括功能测试、性能测试、错误处理测试和集成测试。

## 🧪 测试环境准备

### Python版本测试环境

```bash
# 安装依赖
cd python_version
pip install -r requirements.txt

# 运行基础测试
python main.py
```

### JavaScript版本测试环境

```bash
# 安装依赖
cd javascript_version
npm install

# 运行基础测试
node index.js

# 运行单元测试（如果配置了Jest）
npm test
```

## 🔍 功能测试用例

### 1. 基础功能测试

#### 测试用例 1.1: 分析类任务

**测试目标**: 验证分析类任务的完整执行流程

**输入参数**:
```json
{
  "task_type": "analysis",
  "target": "电动汽车市场趋势分析",
  "config": {
    "depth": "detailed",
    "focus_areas": ["技术趋势", "市场规模", "竞争格局"],
    "language": "zh"
  }
}
```

**预期结果**:
- `success`: true
- `execution_results`: 包含4个步骤的执行结果
- `final_report`: 包含完整的分析报告
- `execution_summary.completed_tasks`: 4

#### 测试用例 1.2: 创意类任务

**测试目标**: 验证创意类任务的执行和输出质量

**输入参数**:
```json
{
  "task_type": "creative",
  "target": "智能家居语音助手设计",
  "config": {
    "depth": "comprehensive",
    "focus_areas": ["用户体验", "技术实现", "市场定位"]
  }
}
```

**预期结果**:
- 包含灵感收集、创意生成、方案评估、方案优化四个步骤
- 每个步骤都有相应的能力模块执行结果
- 最终报告包含创意方案和实施建议

#### 测试用例 1.3: 教育类任务

**测试目标**: 验证教育类任务和自定义学习链

**输入参数**:
```json
{
  "task_type": "education",
  "target": "机器学习入门课程设计",
  "learning_chain": [
    {"step": "基础评估", "action": "评估学习者数学和编程基础"},
    {"step": "课程规划", "action": "设计渐进式学习路径"},
    {"step": "内容开发", "action": "开发理论和实践内容"},
    {"step": "效果评估", "action": "设计学习效果评估方法"}
  ],
  "config": {
    "depth": "detailed",
    "language": "zh"
  }
}
```

#### 测试用例 1.4: 研究类任务

**测试目标**: 验证研究类任务的学术性和严谨性

**输入参数**:
```json
{
  "task_type": "research",
  "target": "量子计算在密码学中的应用前景",
  "config": {
    "depth": "comprehensive",
    "focus_areas": ["技术原理", "安全影响", "实用性分析", "发展趋势"]
  }
}
```

#### 测试用例 1.5: 自定义任务链

**测试目标**: 验证完全自定义的任务链执行

**输入参数**:
```json
{
  "task_type": "custom",
  "target": "企业数字化转型咨询方案",
  "custom_chain": [
    {
      "id": "assessment",
      "name": "现状评估",
      "description": "评估企业当前数字化成熟度",
      "required_capabilities": ["理解分析", "信息检索", "数据整理"]
    },
    {
      "id": "gap_analysis",
      "name": "差距分析",
      "description": "分析数字化转型的差距和挑战",
      "required_capabilities": ["逻辑推理", "风险评估"],
      "dependencies": ["assessment"]
    },
    {
      "id": "strategy_design",
      "name": "策略设计",
      "description": "设计数字化转型策略",
      "required_capabilities": ["方案设计", "创意生成"],
      "dependencies": ["gap_analysis"]
    },
    {
      "id": "implementation_plan",
      "name": "实施规划",
      "description": "制定详细的实施计划",
      "required_capabilities": ["方案设计", "质量验证", "结果整合"],
      "dependencies": ["strategy_design"]
    }
  ],
  "continue_on_failure": true
}
```

### 2. 配置参数测试

#### 测试用例 2.1: 不同深度级别

```python
# Python测试代码
def test_depth_levels():
    depths = ["basic", "detailed", "comprehensive"]
    
    for depth in depths:
        input_data = {
            "task_type": "analysis",
            "target": "AI技术发展趋势",
            "config": {"depth": depth}
        }
        
        result = handler(input_data)
        assert result["success"] == True
        print(f"深度级别 {depth} 测试通过")
```

```javascript
// JavaScript测试代码
async function testDepthLevels() {
    const depths = ['basic', 'detailed', 'comprehensive'];
    
    for (const depth of depths) {
        const inputData = {
            task_type: 'analysis',
            target: 'AI技术发展趋势',
            config: { depth }
        };
        
        const result = await handler(inputData);
        console.assert(result.success === true, `深度级别 ${depth} 测试失败`);
        console.log(`深度级别 ${depth} 测试通过`);
    }
}
```

#### 测试用例 2.2: 多语言支持

```json
{
  "task_type": "analysis",
  "target": "Global AI Market Analysis",
  "config": {
    "language": "en",
    "depth": "detailed"
  }
}
```

## ❌ 错误处理测试

### 测试用例 3.1: 缺少必需参数

**输入参数**:
```json
{
  "target": "测试目标"
  // 缺少 task_type
}
```

**预期结果**:
- `success`: false
- `error_code`: "MISSING_REQUIRED_FIELD"
- `error`: 包含具体错误信息

### 测试用例 3.2: 无效任务类型

**输入参数**:
```json
{
  "task_type": "invalid_type",
  "target": "测试目标"
}
```

**预期结果**:
- `success`: false
- `error_code`: "INVALID_TASK_TYPE"

### 测试用例 3.3: 无效自定义任务链

**输入参数**:
```json
{
  "task_type": "custom",
  "target": "测试目标",
  "custom_chain": "invalid_format"
}
```

**预期结果**:
- `success`: false
- `error_code`: "INVALID_CUSTOM_CHAIN"

## 🚀 性能测试

### 测试用例 4.1: 执行时间测试

```python
# Python性能测试
import time

def test_execution_time():
    start_time = time.time()
    
    result = handler({
        "task_type": "analysis",
        "target": "性能测试目标",
        "config": {"depth": "detailed"}
    })
    
    execution_time = time.time() - start_time
    
    assert result["success"] == True
    assert execution_time < 10  # 应在10秒内完成
    
    print(f"执行时间: {execution_time:.2f}秒")
    print(f"报告的执行时间: {result['execution_summary']['total_execution_time']:.2f}秒")
```

```javascript
// JavaScript性能测试
async function testExecutionTime() {
    const startTime = Date.now();
    
    const result = await handler({
        task_type: 'analysis',
        target: '性能测试目标',
        config: { depth: 'detailed' }
    });
    
    const executionTime = (Date.now() - startTime) / 1000;
    
    console.assert(result.success === true, '性能测试失败');
    console.assert(executionTime < 8, '执行时间超出预期'); // JavaScript版本应更快
    
    console.log(`实际执行时间: ${executionTime.toFixed(2)}秒`);
    console.log(`报告的执行时间: ${result.execution_summary.total_execution_time.toFixed(2)}秒`);
}
```

### 测试用例 4.2: 并发执行测试

```javascript
// JavaScript并发测试
async function testConcurrentExecution() {
    const tasks = [];
    const taskCount = 5;
    
    for (let i = 0; i < taskCount; i++) {
        const task = handler({
            task_type: 'analysis',
            target: `并发测试目标${i + 1}`,
            config: { depth: 'basic' }
        });
        tasks.push(task);
    }
    
    const startTime = Date.now();
    const results = await Promise.all(tasks);
    const totalTime = (Date.now() - startTime) / 1000;
    
    // 验证所有任务都成功
    results.forEach((result, index) => {
        console.assert(result.success === true, `并发任务${index + 1}失败`);
    });
    
    console.log(`${taskCount}个并发任务完成，总耗时: ${totalTime.toFixed(2)}秒`);
    console.log(`平均每个任务: ${(totalTime / taskCount).toFixed(2)}秒`);
}
```

### 测试用例 4.3: 大型任务链测试

```json
{
  "task_type": "custom",
  "target": "大型项目管理流程",
  "custom_chain": [
    {"name": "项目启动", "description": "项目启动和团队组建"},
    {"name": "需求分析", "description": "详细需求分析和文档化"},
    {"name": "架构设计", "description": "系统架构和技术选型"},
    {"name": "开发规划", "description": "开发计划和里程碑设定"},
    {"name": "风险评估", "description": "项目风险识别和应对策略"},
    {"name": "资源配置", "description": "人力和物力资源配置"},
    {"name": "质量保证", "description": "质量标准和测试策略"},
    {"name": "进度监控", "description": "项目进度跟踪机制"},
    {"name": "交付准备", "description": "产品交付和部署准备"},
    {"name": "项目总结", "description": "项目复盘和经验总结"}
  ]
}
```

## 🔗 集成测试

### 测试用例 5.1: 扣子Bot集成测试

**测试场景**: 在扣子Bot中使用任务链控制器

**Bot配置示例**:
```
你是一个专业的分析助手，使用任务链控制器来确保分析的系统性和完整性。

当用户提出分析需求时，请：
1. 理解用户的具体需求
2. 选择合适的任务类型
3. 调用任务链控制器插件
4. 解读和展示结果

插件调用示例：
{"task_type": "analysis", "target": "用户需求", "config": {"depth": "detailed"}}
```

**测试对话**:
```
用户: 请帮我分析一下新能源汽车行业的发展前景

Bot: 我将使用系统化的分析方法来为您分析新能源汽车行业的发展前景。

[调用插件]
{
  "task_type": "analysis",
  "target": "新能源汽车行业发展前景",
  "config": {
    "depth": "comprehensive",
    "focus_areas": ["市场规模", "技术趋势", "政策环境", "竞争格局"]
  }
}

[展示结果]
基于系统化分析，我为您提供以下关于新能源汽车行业发展前景的详细分析...
```

## 📊 自动化测试脚本

### Python自动化测试

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务链控制器插件自动化测试脚本
"""

import json
import time
from main import handler

class TaskChainTester:
    def __init__(self):
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def run_test(self, test_name, input_data, expected_success=True):
        """运行单个测试用例"""
        self.total_tests += 1
        print(f"\n🧪 运行测试: {test_name}")
        
        try:
            start_time = time.time()
            result = handler(input_data)
            execution_time = time.time() - start_time
            
            # 验证基本结果
            success = result.get('success', False)
            
            if success == expected_success:
                self.passed_tests += 1
                status = "✅ PASS"
            else:
                status = "❌ FAIL"
                
            self.test_results.append({
                'name': test_name,
                'status': status,
                'execution_time': execution_time,
                'result': result
            })
            
            print(f"状态: {status}")
            print(f"执行时间: {execution_time:.2f}秒")
            
            if not success and expected_success:
                print(f"错误: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            self.test_results.append({
                'name': test_name,
                'status': "❌ ERROR",
                'error': str(e)
            })
            print(f"状态: ❌ ERROR - {str(e)}")
    
    def run_all_tests(self):
        """运行所有测试用例"""
        print("🚀 开始任务链控制器插件测试")
        print("=" * 50)
        
        # 基础功能测试
        self.run_test("分析类任务", {
            "task_type": "analysis",
            "target": "电动汽车市场分析",
            "config": {"depth": "detailed"}
        })
        
        self.run_test("创意类任务", {
            "task_type": "creative",
            "target": "智能手机设计",
            "config": {"depth": "basic"}
        })
        
        self.run_test("教育类任务", {
            "task_type": "education",
            "target": "Python编程教学"
        })
        
        self.run_test("研究类任务", {
            "task_type": "research",
            "target": "AI技术发展研究"
        })
        
        self.run_test("自定义任务链", {
            "task_type": "custom",
            "target": "产品开发流程",
            "custom_chain": [
                {"name": "需求分析", "description": "分析产品需求"},
                {"name": "设计方案", "description": "设计产品方案"}
            ]
        })
        
        # 错误处理测试
        self.run_test("缺少必需参数", {
            "target": "测试目标"
        }, expected_success=False)
        
        self.run_test("无效任务类型", {
            "task_type": "invalid",
            "target": "测试目标"
        }, expected_success=False)
        
        # 配置测试
        self.run_test("英文输出", {
            "task_type": "analysis",
            "target": "Market Analysis",
            "config": {"language": "en"}
        })
        
        self.print_summary()
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "=" * 50)
        print("📊 测试摘要")
        print(f"总测试数: {self.total_tests}")
        print(f"通过测试: {self.passed_tests}")
        print(f"失败测试: {self.total_tests - self.passed_tests}")
        print(f"通过率: {(self.passed_tests / self.total_tests * 100):.1f}%")
        
        # 详细结果
        print("\n📋 详细结果:")
        for result in self.test_results:
            print(f"  {result['status']} {result['name']}")
            if 'execution_time' in result:
                print(f"    执行时间: {result['execution_time']:.2f}秒")

if __name__ == "__main__":
    tester = TaskChainTester()
    tester.run_all_tests()
```

### JavaScript自动化测试

```javascript
#!/usr/bin/env node
/**
 * 任务链控制器插件自动化测试脚本 - JavaScript版本
 */

const { handler } = require('./index.js');

class TaskChainTester {
    constructor() {
        this.testResults = [];
        this.totalTests = 0;
        this.passedTests = 0;
    }
    
    async runTest(testName, inputData, expectedSuccess = true) {
        this.totalTests++;
        console.log(`\n🧪 运行测试: ${testName}`);
        
        try {
            const startTime = Date.now();
            const result = await handler(inputData);
            const executionTime = (Date.now() - startTime) / 1000;
            
            const success = result.success || false;
            
            if (success === expectedSuccess) {
                this.passedTests++;
                var status = "✅ PASS";
            } else {
                var status = "❌ FAIL";
            }
            
            this.testResults.push({
                name: testName,
                status: status,
                executionTime: executionTime,
                result: result
            });
            
            console.log(`状态: ${status}`);
            console.log(`执行时间: ${executionTime.toFixed(2)}秒`);
            
            if (!success && expectedSuccess) {
                console.log(`错误: ${result.error || 'Unknown error'}`);
            }
            
        } catch (error) {
            this.testResults.push({
                name: testName,
                status: "❌ ERROR",
                error: error.message
            });
            console.log(`状态: ❌ ERROR - ${error.message}`);
        }
    }
    
    async runAllTests() {
        console.log("🚀 开始任务链控制器插件测试 (JavaScript版本)");
        console.log("=".repeat(50));
        
        // 基础功能测试
        await this.runTest("分析类任务", {
            task_type: "analysis",
            target: "电动汽车市场分析",
            config: { depth: "detailed" }
        });
        
        await this.runTest("创意类任务", {
            task_type: "creative",
            target: "智能手机设计",
            config: { depth: "basic" }
        });
        
        await this.runTest("教育类任务", {
            task_type: "education",
            target: "Python编程教学"
        });
        
        await this.runTest("研究类任务", {
            task_type: "research",
            target: "AI技术发展研究"
        });
        
        await this.runTest("自定义任务链", {
            task_type: "custom",
            target: "产品开发流程",
            custom_chain: [
                { name: "需求分析", description: "分析产品需求" },
                { name: "设计方案", description: "设计产品方案" }
            ]
        });
        
        // 错误处理测试
        await this.runTest("缺少必需参数", {
            target: "测试目标"
        }, false);
        
        await this.runTest("无效任务类型", {
            task_type: "invalid",
            target: "测试目标"
        }, false);
        
        // 配置测试
        await this.runTest("英文输出", {
            task_type: "analysis",
            target: "Market Analysis",
            config: { language: "en" }
        });
        
        this.printSummary();
    }
    
    printSummary() {
        console.log("\n" + "=".repeat(50));
        console.log("📊 测试摘要");
        console.log(`总测试数: ${this.totalTests}`);
        console.log(`通过测试: ${this.passedTests}`);
        console.log(`失败测试: ${this.totalTests - this.passedTests}`);
        console.log(`通过率: ${(this.passedTests / this.totalTests * 100).toFixed(1)}%`);
        
        console.log("\n📋 详细结果:");
        this.testResults.forEach(result => {
            console.log(`  ${result.status} ${result.name}`);
            if (result.executionTime) {
                console.log(`    执行时间: ${result.executionTime.toFixed(2)}秒`);
            }
        });
    }
}

// 运行测试
if (require.main === module) {
    const tester = new TaskChainTester();
    tester.runAllTests().catch(console.error);
}

module.exports = { TaskChainTester };
```

## 📋 测试报告模板

### 测试执行报告

```markdown
# 任务链控制器插件测试报告

**测试日期**: 2024-01-15
**测试版本**: 1.0.0
**测试环境**: Python 3.8+ / Node.js 14+

## 测试摘要

| 测试类型 | 总数 | 通过 | 失败 | 通过率 |
|---------|------|------|------|--------|
| 功能测试 | 5 | 5 | 0 | 100% |
| 错误处理测试 | 3 | 3 | 0 | 100% |
| 性能测试 | 3 | 3 | 0 | 100% |
| 集成测试 | 2 | 2 | 0 | 100% |
| **总计** | **13** | **13** | **0** | **100%** |

## 性能指标

- **平均执行时间**: 2.3秒 (Python) / 1.8秒 (JavaScript)
- **最大执行时间**: 4.5秒
- **内存使用**: < 50MB
- **并发支持**: ✅ 通过

## 问题和建议

### 发现的问题
1. 无重大问题

### 改进建议
1. 考虑添加任务链缓存机制
2. 优化大型任务链的内存使用
3. 增加更多的能力模块

## 结论

任务链控制器插件功能完整，性能良好，可以投入生产使用。
```

---

**测试完成时间**: 2025-08-03  
**测试负责人**: 字伯升 (vx: zibosheng88)

通过这些全面的测试用例，可以确保任务链控制器插件的稳定性、可靠性和性能表现。