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
    
    # 检查考试代码是否已存在
    existing_exam = Exam.query.filter_by(exam_code=data['code']).first()
    if existing_exam:
        return jsonify({'error': '考试代码已存在'}), 400
    
    # 创建考试
    new_exam = Exam(
        exam_code=data['code'],
        exam_name=data['name'],
        exam_type=data['type'],
        grade=data['grade'],
        start_date=datetime.strptime(data['startDate'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['endDate'], '%Y-%m-%d').date(),
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
        exam.exam_name = data['name']
    if 'type' in data:
        exam.exam_type = data['type']
    if 'grade' in data:
        exam.grade = data['grade']
    if 'startDate' in data:
        exam.start_date = datetime.strptime(data['startDate'], '%Y-%m-%d').date()
    if 'endDate' in data:
        exam.end_date = datetime.strptime(data['endDate'], '%Y-%m-%d').date()
    if 'status' in data:
        exam.status = data['status']
    
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