from flask import Blueprint, request, jsonify
from app import db
from app.models import Exam
from datetime import datetime

bp = Blueprint('exams', __name__)

@bp.route('/', methods=['GET'])
def get_exams():
    """获取所有考试数据，支持搜索和筛选"""
    # 获取查询参数
    search = request.args.get('search', '')
    exam_type = request.args.get('type', '')
    grade = request.args.get('grade', '')
    
    # 构建查询
    query = Exam.query
    
    # 应用筛选条件
    if search:
        query = query.filter(
            (Exam.exam_name.ilike(f'%{search}%')) |
            (Exam.exam_code.ilike(f'%{search}%'))
        )
    
    if exam_type:
        query = query.filter(Exam.exam_type == exam_type)
    
    if grade:
        query = query.filter(Exam.grade == grade)
    
    # 执行查询
    exams = query.all()
    
    # 返回结果
    return jsonify([exam.to_dict() for exam in exams])

@bp.route('/<string:exam_code>', methods=['GET'])
def get_exam(exam_code):
    """获取单个考试数据"""
    exam = Exam.query.filter_by(exam_code=exam_code).first()
    if not exam:
        return jsonify({'error': '考试不存在'}), 404
    
    return jsonify(exam.to_dict())

@bp.route('/', methods=['POST'])
def create_exam():
    """创建新考试"""
    data = request.get_json()
    
    # 验证数据
    required_fields = ['code', 'name', 'type', 'grade', 'startDate', 'endDate', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
        if not data[field]:
            return jsonify({'error': f'字段 {field} 不能为空'}), 400
    
    # 检查考试代码是否已存在
    existing_exam = Exam.query.filter_by(exam_code=data['code']).first()
    if existing_exam:
        return jsonify({'error': '考试代码已存在'}), 400
    
    # 验证日期格式
    try:
        start_date = datetime.strptime(data['startDate'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['endDate'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': '日期格式不正确，请使用 YYYY-MM-DD 格式'}), 400
    
    # 创建考试
    new_exam = Exam(
        exam_code=data['code'],
        exam_name=data['name'],
        exam_type=data['type'],
        grade=data['grade'],
        start_date=start_date,
        end_date=end_date,
        status=data['status']
    )
    
    # 保存到数据库
    db.session.add(new_exam)
    db.session.commit()
    
    return jsonify(new_exam.to_dict()), 201

@bp.route('/<string:exam_code>', methods=['PUT'])
def update_exam(exam_code):
    """更新考试数据"""
    exam = Exam.query.filter_by(exam_code=exam_code).first()
    if not exam:
        return jsonify({'error': '考试不存在'}), 404
    
    data = request.get_json()
    
    # 更新字段
    if 'name' in data:
        if data['name']:
            exam.exam_name = data['name']
        else:
            return jsonify({'error': '考试名称不能为空'}), 400
    if 'type' in data:
        if data['type']:
            exam.exam_type = data['type']
        else:
            return jsonify({'error': '考试类型不能为空'}), 400
    if 'grade' in data:
        if data['grade']:
            exam.grade = data['grade']
        else:
            return jsonify({'error': '年级不能为空'}), 400
    if 'startDate' in data:
        if data['startDate']:
            try:
                exam.start_date = datetime.strptime(data['startDate'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': '开始日期格式不正确，请使用 YYYY-MM-DD 格式'}), 400
        else:
            return jsonify({'error': '开始日期不能为空'}), 400
    if 'endDate' in data:
        if data['endDate']:
            try:
                exam.end_date = datetime.strptime(data['endDate'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': '结束日期格式不正确，请使用 YYYY-MM-DD 格式'}), 400
        else:
            return jsonify({'error': '结束日期不能为空'}), 400
    if 'status' in data:
        if data['status']:
            exam.status = data['status']
        else:
            return jsonify({'error': '状态不能为空'}), 400
    
    # 保存更改
    db.session.commit()
    
    return jsonify(exam.to_dict())

@bp.route('/<string:exam_code>', methods=['DELETE'])
def delete_exam(exam_code):
    """删除考试"""
    exam = Exam.query.filter_by(exam_code=exam_code).first()
    if not exam:
        return jsonify({'error': '考试不存在'}), 404
    
    # 从数据库中删除考试
    db.session.delete(exam)
    db.session.commit()
    
    return jsonify({'message': '考试删除成功'})