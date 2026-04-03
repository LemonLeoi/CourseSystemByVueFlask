from flask import Blueprint, request
from app import db
from app.models import Exam
from app.utils.response import ResponseUtil
from app.dto.exam_dto import ExamCreateDTO, ExamUpdateDTO, ExamResponseDTO
from datetime import datetime
from flask_restx import Namespace, Resource, fields

# 创建命名空间
exam_ns = Namespace('exams', description='考试管理相关操作')

# 定义请求和响应模型
exam_model = exam_ns.model('Exam', {
    'code': fields.String(required=True, description='考试代码'),
    'name': fields.String(required=True, description='考试名称'),
    'academicYear': fields.String(description='学年'),
    'semester': fields.String(description='学期'),
    'grade': fields.String(required=True, description='年级'),
    'type': fields.String(required=True, description='考试类型'),
    'startDate': fields.String(required=True, description='开始日期'),
    'endDate': fields.String(required=True, description='结束日期'),
    'status': fields.String(required=True, description='状态')
})

exam_response_model = exam_ns.model('ExamResponse', {
    'id': fields.Integer(description='考试ID'),
    'code': fields.String(description='考试代码'),
    'name': fields.String(description='考试名称'),
    'academicYear': fields.String(description='学年'),
    'semester': fields.String(description='学期'),
    'grade': fields.String(description='年级'),
    'type': fields.String(description='考试类型'),
    'startDate': fields.String(description='开始日期'),
    'endDate': fields.String(description='结束日期'),
    'status': fields.String(description='状态')
})

bp = Blueprint('exams', __name__)

@exam_ns.route('/')
class ExamList(Resource):
    @exam_ns.doc('获取所有考试')
    def get(self):
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
        
        # 转换为DTO
        exam_dtos = [ExamResponseDTO.from_model(exam).to_dict() for exam in exams]
        
        # 返回结果
        return ResponseUtil.success(data=exam_dtos, message="获取考试列表成功")
    
    @exam_ns.doc('创建考试')
    @exam_ns.expect(exam_model)
    def post(self):
        """创建新考试"""
        data = request.get_json()
        
        # 验证数据
        required_fields = ['code', 'name', 'grade', 'type', 'startDate', 'endDate', 'status']
        for field in required_fields:
            if field not in data:
                return ResponseUtil.bad_request(message=f'缺少必填字段: {field}')
            if not data[field]:
                return ResponseUtil.bad_request(message=f'字段 {field} 不能为空')
        
        # 检查考试代码是否已存在
        existing_exam = Exam.query.filter_by(exam_code=data['code']).first()
        if existing_exam:
            return ResponseUtil.bad_request(message='考试代码已存在')
        
        # 验证日期格式
        try:
            start_date = datetime.strptime(data['startDate'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['endDate'], '%Y-%m-%d').date()
        except ValueError:
            return ResponseUtil.bad_request(message='日期格式不正确，请使用 YYYY-MM-DD 格式')
        
        # 创建DTO
        exam_dto = ExamCreateDTO.from_dict(data)
        
        # 创建考试
        new_exam = Exam(
            exam_code=exam_dto.code,
            exam_name=exam_dto.name,
            academic_year=exam_dto.academicYear,
            semester=exam_dto.semester,
            grade=exam_dto.grade,
            exam_type=exam_dto.type,
            start_date=start_date,
            end_date=end_date,
            status=exam_dto.status
        )
        
        # 保存到数据库
        db.session.add(new_exam)
        db.session.commit()
        
        # 转换为响应DTO
        response_dto = ExamResponseDTO.from_model(new_exam)
        
        return ResponseUtil.success(data=response_dto.to_dict(), message="考试创建成功"), 201

@exam_ns.route('/<string:exam_code>')
class ExamDetail(Resource):
    @exam_ns.doc('获取单个考试')
    def get(self, exam_code):
        """获取单个考试数据"""
        exam = Exam.query.filter_by(exam_code=exam_code).first()
        if not exam:
            return ResponseUtil.not_found(message='考试不存在')
        
        # 转换为DTO
        exam_dto = ExamResponseDTO.from_model(exam)
        
        return ResponseUtil.success(data=exam_dto.to_dict(), message="获取考试成功")
    
    @exam_ns.doc('更新考试')
    @exam_ns.expect(exam_model)
    def put(self, exam_code):
        """更新考试数据"""
        exam = Exam.query.filter_by(exam_code=exam_code).first()
        if not exam:
            return ResponseUtil.not_found(message='考试不存在')
        
        data = request.get_json()
        
        # 创建DTO
        exam_dto = ExamUpdateDTO.from_dict(data)
        
        # 更新字段
        if exam_dto.name:
            exam.exam_name = exam_dto.name
        if exam_dto.academicYear:
            exam.academic_year = exam_dto.academicYear
        if exam_dto.semester:
            exam.semester = exam_dto.semester
        if exam_dto.type:
            exam.exam_type = exam_dto.type
        if exam_dto.grade:
            exam.grade = exam_dto.grade
        if exam_dto.startDate:
            try:
                exam.start_date = datetime.strptime(exam_dto.startDate, '%Y-%m-%d').date()
            except ValueError:
                return ResponseUtil.bad_request(message='开始日期格式不正确，请使用 YYYY-MM-DD 格式')
        if exam_dto.endDate:
            try:
                exam.end_date = datetime.strptime(exam_dto.endDate, '%Y-%m-%d').date()
            except ValueError:
                return ResponseUtil.bad_request(message='结束日期格式不正确，请使用 YYYY-MM-DD 格式')
        if exam_dto.status:
            exam.status = exam_dto.status
        
        # 保存更改
        db.session.commit()
        
        # 转换为响应DTO
        response_dto = ExamResponseDTO.from_model(exam)
        
        return ResponseUtil.success(data=response_dto.to_dict(), message="考试更新成功")
    
    @exam_ns.doc('删除考试')
    def delete(self, exam_code):
        """删除考试"""
        exam = Exam.query.filter_by(exam_code=exam_code).first()
        if not exam:
            return ResponseUtil.not_found(message='考试不存在')
        
        # 从数据库中删除考试
        db.session.delete(exam)
        db.session.commit()
        
        return ResponseUtil.success(message='考试删除成功')
