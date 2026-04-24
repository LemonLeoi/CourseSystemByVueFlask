# Analysis process visualization API
from flask import Blueprint, request, jsonify
from app.analysis.intermediate_results import storage
from app.analysis.analysis_logger import logger

analysis_bp = Blueprint('analysis', __name__)

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