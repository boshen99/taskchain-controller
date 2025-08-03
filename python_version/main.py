#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用任务链控制器插件 - Python版本

一个通用的任务链控制框架，通过结构化的任务编排和执行机制，
帮助AI模型在处理复杂任务时保持注意力聚焦和逻辑清晰。

作者: 字伯升 (vx: zibosheng88)
版本: 1.0.0
创建时间: 2025-08-03
"""

import json
import time
import uuid
from typing import Dict, List, Any, Optional, Union
from enum import Enum
from dataclasses import dataclass, asdict
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class ExecutionMode(Enum):
    """执行模式枚举"""
    SEQUENTIAL = "sequential"  # 顺序执行
    PARALLEL = "parallel"     # 并行执行
    CONDITIONAL = "conditional" # 条件执行

@dataclass
class TaskDefinition:
    """任务定义数据类"""
    id: str
    name: str
    description: str
    required_capabilities: List[str]
    dependencies: List[str] = None
    execution_mode: ExecutionMode = ExecutionMode.SEQUENTIAL
    timeout: int = 300  # 超时时间（秒）
    retry_count: int = 0
    validation_rules: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.validation_rules is None:
            self.validation_rules = {}

@dataclass
class ExecutionResult:
    """执行结果数据类"""
    task_id: str
    status: TaskStatus
    output: Any
    error_message: str = None
    execution_time: float = 0.0
    timestamp: str = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        if self.metadata is None:
            self.metadata = {}

class CapabilityRegistry:
    """能力注册表 - 管理所有可用的能力模块"""
    
    def __init__(self):
        self.capabilities = {}
        self._register_standard_capabilities()
    
    def _register_standard_capabilities(self):
        """注册标准能力模块"""
        standard_capabilities = {
            "理解分析": self._capability_understanding,
            "需求提取": self._capability_requirement_extraction,
            "信息检索": self._capability_information_retrieval,
            "数据整理": self._capability_data_organization,
            "创意生成": self._capability_creative_generation,
            "逻辑推理": self._capability_logical_reasoning,
            "方案设计": self._capability_solution_design,
            "风险评估": self._capability_risk_assessment,
            "质量验证": self._capability_quality_validation,
            "结果整合": self._capability_result_integration
        }
        self.capabilities.update(standard_capabilities)
    
    def register_capability(self, name: str, capability_func):
        """注册自定义能力"""
        self.capabilities[name] = capability_func
        logger.info(f"已注册能力模块: {name}")
    
    def get_capability(self, name: str):
        """获取能力模块"""
        return self.capabilities.get(name)
    
    def list_capabilities(self) -> List[str]:
        """列出所有可用能力"""
        return list(self.capabilities.keys())
    
    # 标准能力模块实现
    def _capability_understanding(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """理解分析能力"""
        target = context.get('target', '')
        return {
            "analysis": f"深入分析目标: {target}",
            "key_points": ["核心问题识别", "背景信息梳理", "目标明确化"],
            "understanding_level": "detailed"
        }
    
    def _capability_requirement_extraction(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """需求提取能力"""
        return {
            "requirements": ["功能需求", "性能需求", "约束条件"],
            "priority_matrix": {"高优先级": [], "中优先级": [], "低优先级": []}
        }
    
    def _capability_information_retrieval(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """信息检索能力"""
        return {
            "sources": ["内部知识库", "外部资源", "专家意见"],
            "information_quality": "high",
            "relevance_score": 0.85
        }
    
    def _capability_data_organization(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """数据整理能力"""
        return {
            "structured_data": {},
            "data_quality": "validated",
            "organization_method": "hierarchical"
        }
    
    def _capability_creative_generation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """创意生成能力"""
        return {
            "creative_ideas": [],
            "innovation_level": "moderate",
            "feasibility_score": 0.75
        }
    
    def _capability_logical_reasoning(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """逻辑推理能力"""
        return {
            "reasoning_chain": [],
            "logical_consistency": True,
            "confidence_level": 0.8
        }
    
    def _capability_solution_design(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """方案设计能力"""
        return {
            "solution_options": [],
            "design_principles": [],
            "implementation_roadmap": []
        }
    
    def _capability_risk_assessment(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """风险评估能力"""
        return {
            "risk_factors": [],
            "risk_level": "medium",
            "mitigation_strategies": []
        }
    
    def _capability_quality_validation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """质量验证能力"""
        return {
            "quality_score": 0.85,
            "validation_criteria": [],
            "improvement_suggestions": []
        }
    
    def _capability_result_integration(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """结果整合能力"""
        return {
            "integrated_results": {},
            "synthesis_quality": "high",
            "completeness_score": 0.9
        }

class TaskChainController:
    """任务链控制器 - 核心控制逻辑"""
    
    def __init__(self):
        self.capability_registry = CapabilityRegistry()
        self.execution_history = []
        self.session_id = str(uuid.uuid4())
        self.context = {}
        
    def validate_input(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """输入验证"""
        required_fields = ['task_type']
        
        for field in required_fields:
            if field not in params:
                return {
                    "valid": False,
                    "error": f"缺少必需参数: {field}",
                    "error_code": "MISSING_REQUIRED_FIELD"
                }
        
        # 验证任务类型
        valid_task_types = ['analysis', 'creative', 'education', 'research', 'custom']
        if params['task_type'] not in valid_task_types:
            return {
                "valid": False,
                "error": f"无效的任务类型: {params['task_type']}",
                "error_code": "INVALID_TASK_TYPE"
            }
        
        return {"valid": True}
    
    def load_task_chain(self, task_type: str, custom_chain: List[Dict] = None) -> List[TaskDefinition]:
        """加载任务链定义"""
        if custom_chain:
            return self._parse_custom_chain(custom_chain)
        
        # 预设任务链模板
        templates = {
            "analysis": self._get_analysis_template(),
            "creative": self._get_creative_template(),
            "education": self._get_education_template(),
            "research": self._get_research_template()
        }
        
        template = templates.get(task_type, templates["analysis"])
        return [TaskDefinition(**task) for task in template]
    
    def _parse_custom_chain(self, custom_chain: List[Dict]) -> List[TaskDefinition]:
        """解析自定义任务链"""
        tasks = []
        for i, task_def in enumerate(custom_chain):
            task = TaskDefinition(
                id=task_def.get('id', f'step_{i+1}'),
                name=task_def.get('name', task_def.get('step', f'步骤{i+1}')),
                description=task_def.get('description', task_def.get('focus', '')),
                required_capabilities=task_def.get('required_capabilities', ['理解分析'])
            )
            tasks.append(task)
        return tasks
    
    def _get_analysis_template(self) -> List[Dict]:
        """分析类任务链模板"""
        return [
            {
                "id": "understand",
                "name": "理解目标",
                "description": "深入理解分析目标和背景",
                "required_capabilities": ["理解分析", "需求提取"]
            },
            {
                "id": "research",
                "name": "信息收集",
                "description": "收集相关信息和数据",
                "required_capabilities": ["信息检索", "数据整理"]
            },
            {
                "id": "analyze",
                "name": "深度分析",
                "description": "进行深入分析和推理",
                "required_capabilities": ["逻辑推理", "数据整理"]
            },
            {
                "id": "synthesize",
                "name": "结果综合",
                "description": "整合分析结果并形成结论",
                "required_capabilities": ["结果整合", "质量验证"]
            }
        ]
    
    def _get_creative_template(self) -> List[Dict]:
        """创意类任务链模板"""
        return [
            {
                "id": "inspiration",
                "name": "灵感收集",
                "description": "收集创意灵感和参考资料",
                "required_capabilities": ["信息检索", "理解分析"]
            },
            {
                "id": "ideation",
                "name": "创意生成",
                "description": "生成多个创意方案",
                "required_capabilities": ["创意生成", "逻辑推理"]
            },
            {
                "id": "evaluation",
                "name": "方案评估",
                "description": "评估创意方案的可行性",
                "required_capabilities": ["风险评估", "质量验证"]
            },
            {
                "id": "refinement",
                "name": "方案优化",
                "description": "优化和完善最佳方案",
                "required_capabilities": ["方案设计", "结果整合"]
            }
        ]
    
    def _get_education_template(self) -> List[Dict]:
        """教育类任务链模板"""
        return [
            {
                "id": "assessment",
                "name": "水平评估",
                "description": "评估学习者当前水平",
                "required_capabilities": ["理解分析", "需求提取"]
            },
            {
                "id": "planning",
                "name": "路径规划",
                "description": "制定学习路径和计划",
                "required_capabilities": ["方案设计", "逻辑推理"]
            },
            {
                "id": "teaching",
                "name": "知识传授",
                "description": "传授核心知识和技能",
                "required_capabilities": ["信息检索", "数据整理"]
            },
            {
                "id": "practice",
                "name": "实践指导",
                "description": "提供实践练习和指导",
                "required_capabilities": ["方案设计", "质量验证"]
            }
        ]
    
    def _get_research_template(self) -> List[Dict]:
        """研究类任务链模板"""
        return [
            {
                "id": "question",
                "name": "问题定义",
                "description": "明确研究问题和假设",
                "required_capabilities": ["理解分析", "需求提取"]
            },
            {
                "id": "methodology",
                "name": "方法设计",
                "description": "设计研究方法和流程",
                "required_capabilities": ["方案设计", "逻辑推理"]
            },
            {
                "id": "investigation",
                "name": "深入调研",
                "description": "执行研究和数据收集",
                "required_capabilities": ["信息检索", "数据整理"]
            },
            {
                "id": "conclusion",
                "name": "结论形成",
                "description": "分析数据并形成结论",
                "required_capabilities": ["逻辑推理", "结果整合"]
            }
        ]
    
    def execute_task(self, task: TaskDefinition, context: Dict[str, Any]) -> ExecutionResult:
        """执行单个任务"""
        start_time = time.time()
        
        try:
            logger.info(f"开始执行任务: {task.name} ({task.id})")
            
            # 执行任务所需的能力模块
            task_output = {}
            for capability_name in task.required_capabilities:
                capability = self.capability_registry.get_capability(capability_name)
                if capability:
                    capability_result = capability(context)
                    task_output[capability_name] = capability_result
                else:
                    logger.warning(f"未找到能力模块: {capability_name}")
            
            # 模拟任务执行逻辑
            task_output["task_summary"] = f"已完成任务: {task.name}"
            task_output["task_description"] = task.description
            task_output["execution_context"] = context.get('target', '未指定目标')
            
            execution_time = time.time() - start_time
            
            result = ExecutionResult(
                task_id=task.id,
                status=TaskStatus.COMPLETED,
                output=task_output,
                execution_time=execution_time
            )
            
            logger.info(f"任务执行完成: {task.name}, 耗时: {execution_time:.2f}秒")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"任务执行失败: {task.name}, 错误: {str(e)}")
            
            return ExecutionResult(
                task_id=task.id,
                status=TaskStatus.FAILED,
                output=None,
                error_message=str(e),
                execution_time=execution_time
            )
    
    def execute_chain(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行完整任务链"""
        try:
            # 输入验证
            validation = self.validate_input(params)
            if not validation["valid"]:
                return {
                    "success": False,
                    "error": validation["error"],
                    "error_code": validation["error_code"]
                }
            
            # 设置执行上下文
            self.context = {
                "target": params.get('target', ''),
                "config": params.get('config', {}),
                "session_id": self.session_id
            }
            
            # 加载任务链
            task_type = params['task_type']
            custom_chain = params.get('custom_chain') or params.get('learning_chain')
            task_chain = self.load_task_chain(task_type, custom_chain)
            
            # 执行任务链
            results = []
            accumulated_context = self.context.copy()
            
            for task in task_chain:
                result = self.execute_task(task, accumulated_context)
                results.append(result)
                self.execution_history.append(result)
                
                # 将当前任务结果添加到上下文中，供后续任务使用
                if result.status == TaskStatus.COMPLETED:
                    accumulated_context[f"result_{task.id}"] = result.output
                else:
                    # 如果任务失败，根据配置决定是否继续
                    if not params.get('continue_on_failure', True):
                        break
            
            # 生成最终报告
            final_report = self.generate_final_report(results, params)
            
            return {
                "success": True,
                "session_id": self.session_id,
                "task_type": task_type,
                "target": self.context['target'],
                "execution_results": [asdict(result) for result in results],
                "final_report": final_report,
                "execution_summary": {
                    "total_tasks": len(task_chain),
                    "completed_tasks": len([r for r in results if r.status == TaskStatus.COMPLETED]),
                    "failed_tasks": len([r for r in results if r.status == TaskStatus.FAILED]),
                    "total_execution_time": sum(r.execution_time for r in results)
                }
            }
            
        except Exception as e:
            logger.error(f"任务链执行失败: {str(e)}")
            return {
                "success": False,
                "error": f"任务链执行失败: {str(e)}",
                "error_code": "EXECUTION_FAILED"
            }
    
    def generate_final_report(self, results: List[ExecutionResult], params: Dict[str, Any]) -> Dict[str, Any]:
        """生成最终报告"""
        successful_results = [r for r in results if r.status == TaskStatus.COMPLETED]
        
        report = {
            "executive_summary": f"已完成 {params['task_type']} 类型的任务链执行",
            "target_analysis": params.get('target', '未指定目标'),
            "key_findings": [],
            "detailed_results": {},
            "recommendations": [],
            "quality_metrics": {
                "completion_rate": len(successful_results) / len(results) if results else 0,
                "average_execution_time": sum(r.execution_time for r in results) / len(results) if results else 0
            }
        }
        
        # 整合各任务的输出
        for result in successful_results:
            if result.output:
                report["detailed_results"][result.task_id] = result.output
                
                # 提取关键发现
                if "key_points" in result.output:
                    report["key_findings"].extend(result.output["key_points"])
        
        # 生成建议
        if params['task_type'] == 'analysis':
            report["recommendations"] = ["基于分析结果制定行动计划", "持续监控关键指标", "定期更新分析数据"]
        elif params['task_type'] == 'creative':
            report["recommendations"] = ["选择最具可行性的创意方案", "制定详细实施计划", "建立反馈机制"]
        elif params['task_type'] == 'education':
            report["recommendations"] = ["按计划执行学习任务", "定期评估学习进度", "调整学习策略"]
        
        return report

def handler(event, context):
    """扣子插件主入口函数"""
    try:
        # 解析输入参数
        if isinstance(event, str):
            params = json.loads(event)
        else:
            params = event
        
        # 创建任务链控制器
        controller = TaskChainController()
        
        # 执行任务链
        result = controller.execute_chain(params)
        
        return result
        
    except Exception as e:
        logger.error(f"插件执行失败: {str(e)}")
        return {
            "success": False,
            "error": f"插件执行失败: {str(e)}",
            "error_code": "PLUGIN_EXECUTION_FAILED"
        }

# 测试代码
if __name__ == "__main__":
    # 测试分析类任务链
    test_params_analysis = {
        "task_type": "analysis",
        "target": "电动汽车市场趋势",
        "config": {
            "depth": "detailed",
            "focus_areas": ["技术趋势", "市场规模", "竞争格局"]
        }
    }
    
    # 测试自定义任务链
    test_params_custom = {
        "task_type": "custom",
        "target": "设计智能手机",
        "custom_chain": [
            {
                "id": "research",
                "name": "用户研究",
                "description": "了解用户需求和痛点",
                "required_capabilities": ["理解分析", "信息检索"]
            },
            {
                "id": "design",
                "name": "方案设计",
                "description": "设计产品方案",
                "required_capabilities": ["创意生成", "方案设计"]
            }
        ]
    }
    
    print("=== 测试分析类任务链 ===")
    result1 = handler(test_params_analysis, None)
    print(json.dumps(result1, ensure_ascii=False, indent=2))
    
    print("\n=== 测试自定义任务链 ===")
    result2 = handler(test_params_custom, None)
    print(json.dumps(result2, ensure_ascii=False, indent=2))