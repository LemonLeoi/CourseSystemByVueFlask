# Analysis process visualization API
from flask import Blueprint, request, jsonify
from app.analysis.intermediate_results import storage
from app.analysis.analysis_logger import logger
from app.analysis.analysis_explainer import explainer

analysis_bp = Blueprint('analysis', __name__)

# 模拟数据 - 挖掘发现（包含极端显著性案例）
mock_knowledge_discoveries = [
    {
        "conditions": [
            {"feature": "排课时间", "operator": "位于", "value": "周五下午"},
            {"feature": "课程节次", "operator": "=", "value": "第5-6节"}
        ],
        "result": {
            "target": "该课及格率",
            "effect": "预测显著下降",
            "change": -28
        },
        "insight": "周五下午最后一节课学生注意力明显下降，建议调整课程安排",
        "confidence": 95,
        "isHighlight": True,
        "statisticalSignificance": "p-value < 0.001"
    },
    {
        "conditions": [
            {"feature": "排课时间", "operator": "位于", "value": "周二上午"},
            {"feature": "课程节次", "operator": "=", "value": "第1-2节"}
        ],
        "result": {
            "target": "该课及格率",
            "effect": "预测显著上升",
            "change": 18
        },
        "insight": "周二上午学生精神状态最佳，是安排重要课程的黄金时段",
        "confidence": 92,
        "isHighlight": True,
        "statisticalSignificance": "p-value < 0.01"
    },
    {
        "conditions": [
            {"feature": "教师职称", "operator": "=", "value": "高级教师"},
            {"feature": "班级类型", "operator": "=", "value": "基础薄弱班"}
        ],
        "result": {
            "target": "学生提分率",
            "effect": "比普通教师高出",
            "change": 15
        },
        "insight": "高级教师在基础薄弱班的教学效果更显著，建议优化师资配置",
        "confidence": 88,
        "isHighlight": False,
        "statisticalSignificance": "p-value < 0.05"
    },
    {
        "conditions": [
            {"feature": "前序课程分数", "operator": "<", "value": 75},
            {"feature": "排课时间", "operator": "位于", "value": "周一上午"}
        ],
        "result": {
            "target": "该课及格率",
            "effect": "预测下降",
            "change": -15
        },
        "insight": "基础薄弱学生在周一上午课程表现较差，建议提供课前辅导",
        "confidence": 85,
        "isHighlight": False,
        "statisticalSignificance": "p-value < 0.05"
    },
    {
        "conditions": [
            {"feature": "班级", "operator": "=", "value": "数学A班"},
            {"feature": "教师", "operator": "=", "value": "教师A"}
        ],
        "result": {
            "target": "基础薄弱生提分率",
            "effect": "比教师B高出",
            "change": 12
        },
        "insight": "教师A在数学基础薄弱生的教学方法更有效",
        "confidence": 82,
        "isHighlight": False,
        "statisticalSignificance": "p-value < 0.05"
    }
]

# 模拟数据 - 特征重要性（基于C4.5算法的信息增益比）
mock_feature_importance = [
    {
        "name": "排课时间",
        "value": 0.4521,
        "description": "课程安排的时间段对学生成绩的影响",
        "theoreticalBasis": "基于C4.5算法的信息增益比计算，排课时间是影响成绩的最关键因素。信息增益比考虑了特征的固有信息，避免了偏向于取值较多特征的问题。"
    },
    {
        "name": "教师水平",
        "value": 0.3287,
        "description": "教师职称和教学经验对学生成绩的影响",
        "theoreticalBasis": "教师水平通过信息增益比评估，高级教师与一级教师在教学效果上存在显著差异，信息增益比为0.3287。"
    },
    {
        "name": "前序课程分数",
        "value": 0.1563,
        "description": "学生在前置课程中的表现对当前课程的影响",
        "theoreticalBasis": "前序课程分数反映了学生的知识基础，信息增益比为0.1563，表明其对后续课程成绩有中等程度的预测能力。"
    },
    {
        "name": "班级类型",
        "value": 0.0429,
        "description": "重点班与普通班的差异对成绩的影响",
        "theoreticalBasis": "班级类型的信息增益比较低(0.0429)，说明在本数据集中，班级类型不是影响成绩的主要因素。"
    },
    {
        "name": "学生性别",
        "value": 0.0199,
        "description": "学生性别对成绩的影响",
        "theoreticalBasis": "性别的信息增益比最低(0.0199)，表明在本分析中，性别不是影响成绩的显著因素。"
    }
]

# 模拟数据 - 多路径决策树
mock_decision_tree_paths = [
    {
        "id": "path-1",
        "name": "排课时间影响路径",
        "description": "分析排课时间对学生成绩的影响",
        "confidence": 95,
        "impact": "高",
        "recommendation": "建议避免在周五下午安排重要课程",
        "path": [
            {
                "label": "排课时间",
                "value": "信息增益: 0.4521",
                "isLeaf": False,
                "splitCriteria": "",
                "infoGain": 0.4521,
                "significance": "p < 0.001",
                "branchOptions": [
                    {"value": "周五下午", "nextNodeId": 1},
                    {"value": "周二上午", "nextNodeId": 10},
                    {"value": "其他时间", "nextNodeId": 20}
                ]
            },
            {
                "label": "周五下午?",
                "value": "是",
                "isLeaf": False,
                "splitCriteria": "排课时间 = \"周五下午\"",
                "branchOptions": [
                    {"value": "第5-6节", "nextNodeId": 2},
                    {"value": "第1-2节", "nextNodeId": 5}
                ]
            },
            {
                "label": "课程节次",
                "value": "第5-6节",
                "isLeaf": False,
                "splitCriteria": "课程节次 = \"第5-6节\"",
                "infoGain": 0.3287,
                "significance": "p < 0.01"
            },
            {
                "label": "预测结果",
                "value": "及格率下降28%",
                "isLeaf": True,
                "splitCriteria": "最终判定",
                "significance": "高度显著"
            }
        ]
    },
    {
        "id": "path-2",
        "name": "教师水平影响路径",
        "description": "分析教师职称对学生成绩的影响",
        "confidence": 88,
        "impact": "中高",
        "recommendation": "建议为基础薄弱班配置高级教师",
        "path": [
            {
                "label": "教师职称",
                "value": "信息增益: 0.3287",
                "isLeaf": False,
                "splitCriteria": "",
                "infoGain": 0.3287,
                "significance": "p < 0.01",
                "branchOptions": [
                    {"value": "高级教师", "nextNodeId": 1},
                    {"value": "一级教师", "nextNodeId": 1},
                    {"value": "二级教师", "nextNodeId": 1}
                ]
            },
            {
                "label": "班级类型",
                "value": "基础薄弱班",
                "isLeaf": False,
                "splitCriteria": "班级类型 = \"基础薄弱班\"",
                "branchOptions": [
                    {"value": "基础薄弱班", "nextNodeId": 2},
                    {"value": "普通班", "nextNodeId": 5},
                    {"value": "重点班", "nextNodeId": 6}
                ]
            },
            {
                "label": "提分效果",
                "value": "高级教师 +15%",
                "isLeaf": False,
                "splitCriteria": "教师水平 × 班级类型交互效应",
                "infoGain": 0.1856,
                "significance": "p < 0.05"
            },
            {
                "label": "预测结果",
                "value": "提分率提升15%",
                "isLeaf": True,
                "splitCriteria": "最终判定",
                "significance": "显著"
            }
        ]
    },
    {
        "id": "path-3",
        "name": "前序课程影响路径",
        "description": "分析前序课程成绩对当前课程的影响",
        "confidence": 82,
        "impact": "中等",
        "recommendation": "建议为前序课程成绩较低的学生提供补习",
        "path": [
            {
                "label": "前序课程分数",
                "value": "信息增益: 0.1563",
                "isLeaf": False,
                "splitCriteria": "",
                "infoGain": 0.1563,
                "significance": "p < 0.05",
                "branchOptions": [
                    {"value": "< 75分", "nextNodeId": 1},
                    {"value": "75-85分", "nextNodeId": 1},
                    {"value": "> 85分", "nextNodeId": 1}
                ]
            },
            {
                "label": "当前课程难度",
                "value": "高难度",
                "isLeaf": False,
                "splitCriteria": "课程难度 = \"高\"",
                "branchOptions": [
                    {"value": "高难度", "nextNodeId": 2},
                    {"value": "中难度", "nextNodeId": 5},
                    {"value": "低难度", "nextNodeId": 6}
                ]
            },
            {
                "label": "学习状态",
                "value": "需要额外辅导",
                "isLeaf": False,
                "splitCriteria": "综合评估",
                "infoGain": 0.1245,
                "significance": "p < 0.05"
            },
            {
                "label": "预测结果",
                "value": "及格风险+22%",
                "isLeaf": True,
                "splitCriteria": "最终判定",
                "significance": "中等显著"
            }
        ]
    }
]

# 模拟数据 - 单路径（保持向后兼容）
mock_decision_tree_path = mock_decision_tree_paths[0]["path"]

# 模拟数据 - 影响因素量化评估
mock_factor_impact_analysis = [
    {
        "factor": "排课时间",
        "weight": 0.4521,
        "impactScore": 85,
        "significance": "p < 0.001",
        "positive": False,
        "description": "周五下午课程及格率比周二上午低28%"
    },
    {
        "factor": "教师职称",
        "weight": 0.3287,
        "impactScore": 72,
        "significance": "p < 0.01",
        "positive": True,
        "description": "高级教师授课班级平均提分率高出15%"
    },
    {
        "factor": "前序课程成绩",
        "weight": 0.1563,
        "impactScore": 58,
        "significance": "p < 0.05",
        "positive": True,
        "description": "前序课程分数每提高10分，当前课程及格率提升8%"
    },
    {
        "factor": "班级类型",
        "weight": 0.0429,
        "impactScore": 35,
        "significance": "p = 0.12",
        "positive": True,
        "description": "重点班平均成绩略高于普通班，但差异不显著"
    },
    {
        "factor": "学生性别",
        "weight": 0.0199,
        "impactScore": 18,
        "significance": "p = 0.45",
        "positive": None,
        "description": "性别对成绩无显著影响"
    }
]

@analysis_bp.route('/api/analysis/intermediate-results', methods=['GET'])
def get_intermediate_results():
    """获取中间结果
    
    Query参数:
        analysis_id: 分析ID
        step: 分析步骤（可选）
    """
    try:
        analysis_id = request.args.get('analysis_id')
        step = request.args.get('step')
        
        if not analysis_id:
            return jsonify({'error': '缺少analysis_id参数'}), 400
        
        results = storage.get_results(analysis_id, step)
        return jsonify({'results': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/model-state', methods=['GET'])
def get_model_state():
    """获取模型状态
    
    Query参数:
        analysis_id: 分析ID
        model_name: 模型名称（可选）
    """
    try:
        analysis_id = request.args.get('analysis_id')
        model_name = request.args.get('model_name')
        
        if not analysis_id:
            return jsonify({'error': '缺少analysis_id参数'}), 400
        
        models = storage.get_model_state(analysis_id, model_name)
        return jsonify({'models': models}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/conclusions', methods=['GET'])
def get_conclusions():
    """获取阶段性结论
    
    Query参数:
        analysis_id: 分析ID
        level: 结论级别（可选）
    """
    try:
        analysis_id = request.args.get('analysis_id')
        level = request.args.get('level')
        
        if not analysis_id:
            return jsonify({'error': '缺少analysis_id参数'}), 400
        
        conclusions = storage.get_conclusions(analysis_id, level)
        return jsonify({'conclusions': conclusions}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/logs', methods=['GET'])
def get_analysis_logs():
    """获取分析日志
    
    Query参数:
        analysis_type: 分析类型（可选）
        start_time: 开始时间（可选）
        end_time: 结束时间（可选）
    """
    try:
        analysis_type = request.args.get('analysis_type')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        
        logs = logger.get_logs(analysis_type, start_time, end_time)
        return jsonify({'logs': logs}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/process-visualization', methods=['POST'])
def get_process_visualization():
    """获取分析过程可视化数据
    
    请求体:
        analysis_id: 分析ID
        process_type: 过程类型（如'decision_tree', 'statistical_analysis'）
    """
    try:
        data = request.get_json()
        analysis_id = data.get('analysis_id')
        process_type = data.get('process_type')
        
        if not analysis_id or not process_type:
            return jsonify({'error': '缺少必要参数'}), 400
        
        # 根据过程类型获取可视化数据
        if process_type == 'decision_tree':
            # 从中间结果中获取决策树可视化数据
            results = storage.get_results(analysis_id, 'decision_tree_build')
            if results:
                visualization_data = results[-1].get('data', {})
                return jsonify({'visualization_data': visualization_data}), 200
            else:
                return jsonify({'error': '未找到决策树构建数据'}), 404
        
        elif process_type == 'statistical_analysis':
            # 从中间结果中获取统计分析可视化数据
            results = storage.get_results(analysis_id, 'statistical_analysis')
            if results:
                visualization_data = results[-1].get('data', {})
                return jsonify({'visualization_data': visualization_data}), 200
            else:
                return jsonify({'error': '未找到统计分析数据'}), 404
        
        else:
            return jsonify({'error': '不支持的过程类型'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/history', methods=['GET'])
def get_analysis_history():
    """获取历史分析记录
    
    Query参数:
        analysis_type: 分析类型（可选）
        limit: 返回数量限制（可选）
    """
    try:
        analysis_type = request.args.get('analysis_type')
        limit = request.args.get('limit', 10, type=int)
        
        # 从日志中获取历史分析记录
        logs = logger.get_logs(analysis_type)
        
        # 按分析ID分组，获取每个分析的最新记录
        analysis_history = {}
        for log in logs:
            # 从日志中提取分析ID（假设日志中包含analysis_id字段）
            analysis_id = log.get('params', {}).get('analysis_id')
            if analysis_id:
                if analysis_id not in analysis_history or log['timestamp'] > analysis_history[analysis_id]['timestamp']:
                    analysis_history[analysis_id] = log
        
        # 转换为列表并排序
        history_list = list(analysis_history.values())
        history_list.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # 限制返回数量
        history_list = history_list[:limit]
        
        return jsonify({'history': history_list}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/knowledge-discoveries', methods=['GET'])
def get_knowledge_discoveries():
    """获取挖掘发现列表
    
    Query参数:
        class_name: 班级名称（可选）
        limit: 返回数量限制（可选）
    """
    try:
        class_name = request.args.get('class_name')
        limit = request.args.get('limit', 10, type=int)
        
        # 返回模拟数据（实际项目中应从数据库获取）
        discoveries = mock_knowledge_discoveries[:limit]
        
        return jsonify({
            'discoveries': discoveries,
            'total': len(mock_knowledge_discoveries),
            'algorithm': 'C4.5',
            'method': '信息增益比(Gain Ratio)'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/feature-importance', methods=['GET'])
def get_feature_importance():
    """获取特征重要性分析结果
    
    Query参数:
        analysis_type: 分析类型（可选，如'personal', 'class', 'grade'）
    """
    try:
        analysis_type = request.args.get('analysis_type', 'class')
        
        # 返回模拟数据（实际项目中应从分析结果获取）
        importance_data = mock_feature_importance
        
        # 添加算法说明
        explanation = explainer.explain_feature_importance(
            {item['name']: item['value'] for item in importance_data},
            analysis_type
        )
        
        return jsonify({
            'feature_importance': importance_data,
            'algorithm': 'C4.5',
            'method': '信息增益比(Gain Ratio)',
            'explanation': explanation
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/decision-tree-path', methods=['POST'])
def get_decision_tree_path():
    """获取决策树路径分析结果
    
    请求体:
        class_name: 班级名称（可选）
        student_id: 学生ID（可选）
        analysis_type: 分析类型
    """
    try:
        data = request.get_json()
        class_name = data.get('class_name')
        student_id = data.get('student_id')
        analysis_type = data.get('analysis_type', 'class')
        
        # 返回多路径数据
        return jsonify({
            'paths': mock_decision_tree_paths,
            'class_name': class_name,
            'student_id': student_id,
            'algorithm': 'C4.5',
            'total_paths': len(mock_decision_tree_paths)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analysis_bp.route('/api/analysis/factor-impact', methods=['GET'])
def get_factor_impact():
    """获取影响因素量化评估结果
    
    Query参数:
        analysis_type: 分析类型（可选）
    """
    try:
        analysis_type = request.args.get('analysis_type', 'class')
        
        return jsonify({
            'factor_impact': mock_factor_impact_analysis,
            'algorithm': 'C4.5',
            'method': '信息增益比(Gain Ratio)',
            'analysis_type': analysis_type
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500