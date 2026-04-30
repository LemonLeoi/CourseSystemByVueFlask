from flask import Blueprint, request
from app import db
from app.models import Exam, Student, Grade
from app.utils.response import ResponseUtil
from app.dto.exam_dto import ExamCreateDTO, ExamUpdateDTO, ExamResponseDTO, StudentExamInfoDTO
from datetime import datetime
import re

bp = Blueprint('exams', __name__)

# 学生ID格式验证正则表达式
STUDENT_ID_PATTERN = re.compile(r'^STU\d{9}$|^\d{10}$')

def validate_student_id(student_id: str) -> bool:
    """验证学生ID格式"""
    if not student_id:
        return False
    return bool(STUDENT_ID_PATTERN.match(student_id))

def validate_exam_code(exam_code: str) -> bool:
    """验证考试代码格式"""
    if not exam_code:
        return False
    return len(exam_code) >= 5 and len(exam_code) <= 20

@bp.route('/', methods=['GET'])
def get_exams():
    """获取所有考试数据，支持搜索和筛选"""
    search = request.args.get('search', '')
    exam_type = request.args.get('type', '')
    grade = request.args.get('grade', '')

    query = Exam.query

    if search:
        query = query.filter(
            (Exam.exam_name.ilike(f'%{search}%')) |
            (Exam.exam_code.ilike(f'%{search}%'))
        )

    if exam_type:
        query = query.filter(Exam.exam_type == exam_type)

    if grade:
        query = query.filter(Exam.grade == grade)

    exams = query.order_by(Exam.start_date.desc()).all()
    exam_dtos = [ExamResponseDTO.from_model(exam).to_dict() for exam in exams]

    return ResponseUtil.success(data=exam_dtos, message="获取考试列表成功")

@bp.route('/student-exams', methods=['GET'])
def get_student_exams():
    """
    获取学生参与的所有考试信息

    Query Parameters:
        student_id: 学生ID (必填)
        exam_code: 考试代码 (可选，用于筛选特定考试)

    Returns:
        200: 成功获取学生考试信息
        400: 请求参数错误
        404: 学生不存在或未找到匹配的考试
        500: 服务器内部错误
    """
    try:
        # 获取查询参数
        student_id = request.args.get('student_id', '').strip()
        exam_code = request.args.get('exam_code', '').strip()

        # 请求验证
        if not student_id:
            return ResponseUtil.bad_request(message='学生ID不能为空')

        if not validate_student_id(student_id):
            return ResponseUtil.bad_request(
                message='学生ID格式不正确，应为STU开头的9位数字或10位数字'
            )

        if exam_code and not validate_exam_code(exam_code):
            return ResponseUtil.bad_request(message='考试代码格式不正确')

        # 查询学生是否存在
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return ResponseUtil.not_found(message=f'学生ID {student_id} 不存在')

        # 构建查询 - 使用JOIN优化查询性能
        query = db.session.query(Exam).join(
            Grade, Exam.exam_code == Grade.exam_code
        ).filter(
            Grade.student_id == student_id
        )

        # 如果指定了考试代码，进一步筛选
        if exam_code:
            query = query.filter(Exam.exam_code == exam_code)

        # 按考试日期降序排列
        exams = query.order_by(Exam.start_date.desc()).all()

        if not exams:
            return ResponseUtil.not_found(
                message=f'学生 {student_id} 未找到匹配的考试信息'
            )

        # 构建响应数据
        student_exam_list = []
        for exam in exams:
            # 获取学生该考试的所有科目成绩
            grades = Grade.query.filter_by(
                student_id=student_id,
                exam_code=exam.exam_code
            ).all()

            subjects = [grade.subject for grade in grades]
            scores = [grade.score for grade in grades]
            average_score = round(sum(scores) / len(scores), 2) if scores else None

            # 生成特殊说明
            special_notes = []
            if average_score:
                if average_score >= 90:
                    special_notes.append('整体表现优秀')
                elif average_score >= 80:
                    special_notes.append('整体表现良好')
                elif average_score >= 60:
                    special_notes.append('整体表现一般，需继续努力')
                else:
                    special_notes.append('整体表现较差，建议加强学习')

            # 检查是否有不及格科目
            failing_subjects = [g.subject for g in grades if g.score < 60]
            if failing_subjects:
                special_notes.append(f'以下科目不及格: {", ".join(failing_subjects)}')

            exam_dto = StudentExamInfoDTO.from_model(
                exam=exam,
                subjects=subjects,
                average_score=average_score,
                total_subjects=len(subjects),
                exam_location='本校',  # 默认地点，可根据实际业务扩展
                special_notes='; '.join(special_notes) if special_notes else '无'
            )
            student_exam_list.append(exam_dto.to_dict())

        return ResponseUtil.success(
            data={
                'studentId': student_id,
                'studentName': student.name,
                'studentClass': student.class_,
                'grade': student.grade,
                'exams': student_exam_list,
                'totalExams': len(student_exam_list)
            },
            message=f'成功获取学生 {student_id} 的 {len(student_exam_list)} 条考试信息'
        )

    except db.exc.SQLAlchemyError as e:
        db.session.rollback()
        return ResponseUtil.internal_error(
            message=f'数据库查询错误: {str(e)}'
        )
    except Exception as e:
        return ResponseUtil.internal_error(
            message=f'服务器内部错误: {str(e)}'
        )

@bp.route('/student-exams/detail', methods=['GET'])
def get_student_exam_detail():
    """
    获取学生特定考试的详细成绩信息

    Query Parameters:
        student_id: 学生ID (必填)
        exam_code: 考试代码 (必填)

    Returns:
        200: 成功获取考试详情
        400: 请求参数错误
        404: 未找到匹配的考试信息
        500: 服务器内部错误
    """
    try:
        student_id = request.args.get('student_id', '').strip()
        exam_code = request.args.get('exam_code', '').strip()

        # 请求验证
        if not student_id:
            return ResponseUtil.bad_request(message='学生ID不能为空')

        if not validate_student_id(student_id):
            return ResponseUtil.bad_request(
                message='学生ID格式不正确，应为STU开头的9位数字或10位数字'
            )

        if not exam_code:
            return ResponseUtil.bad_request(message='考试代码不能为空')

        if not validate_exam_code(exam_code):
            return ResponseUtil.bad_request(message='考试代码格式不正确')

        # 查询学生
        student = Student.query.filter_by(student_id=student_id).first()
        if not student:
            return ResponseUtil.not_found(message=f'学生ID {student_id} 不存在')

        # 查询考试
        exam = Exam.query.filter_by(exam_code=exam_code).first()
        if not exam:
            return ResponseUtil.not_found(message=f'考试代码 {exam_code} 不存在')

        # 查询学生该考试的所有成绩
        grades = Grade.query.filter_by(
            student_id=student_id,
            exam_code=exam_code
        ).all()

        if not grades:
            return ResponseUtil.not_found(
                message=f'学生 {student_id} 在考试 {exam_code} 中没有成绩记录'
            )

        # 构建成绩详情
        grade_details = []
        for grade in grades:
            grade_details.append({
                'subject': grade.subject,
                'score': grade.score,
                'gradeLevel': grade.grade_level,
                'pass': grade.score >= 60,
                'excellent': grade.score >= 90
            })

        # 计算统计信息
        scores = [g.score for g in grades]
        average_score = round(sum(scores) / len(scores), 2)
        max_score = max(scores)
        min_score = min(scores)
        pass_count = len([s for s in scores if s >= 60])
        excellent_count = len([s for s in scores if s >= 90])

        return ResponseUtil.success(
            data={
                'studentId': student_id,
                'studentName': student.name,
                'studentClass': student.class_,
                'exam': {
                    'examCode': exam.exam_code,
                    'examName': exam.exam_name,
                    'academicYear': exam.academic_year,
                    'semester': exam.semester,
                    'grade': exam.grade,
                    'examType': exam.exam_type,
                    'startDate': exam.start_date.isoformat() if exam.start_date else None,
                    'endDate': exam.end_date.isoformat() if exam.end_date else None,
                    'status': exam.status
                },
                'grades': grade_details,
                'statistics': {
                    'totalSubjects': len(grades),
                    'averageScore': average_score,
                    'maxScore': max_score,
                    'minScore': min_score,
                    'passRate': round(pass_count / len(grades) * 100, 2),
                    'excellentRate': round(excellent_count / len(grades) * 100, 2),
                    'passCount': pass_count,
                    'excellentCount': excellent_count
                }
            },
            message='成功获取考试详情'
        )

    except db.exc.SQLAlchemyError as e:
        db.session.rollback()
        return ResponseUtil.internal_error(
            message=f'数据库查询错误: {str(e)}'
        )
    except Exception as e:
        return ResponseUtil.internal_error(
            message=f'服务器内部错误: {str(e)}'
        )

@bp.route('/', methods=['POST'])
def create_exam():
    """创建新考试"""
    data = request.get_json()

    required_fields = ['code', 'name', 'grade', 'type', 'startDate', 'endDate', 'status']
    for field in required_fields:
        if field not in data:
            return ResponseUtil.bad_request(message=f'缺少必填字段: {field}')
        if not data[field]:
            return ResponseUtil.bad_request(message=f'字段 {field} 不能为空')

    existing_exam = Exam.query.filter_by(exam_code=data['code']).first()
    if existing_exam:
        return ResponseUtil.bad_request(message='考试代码已存在')

    try:
        start_date = datetime.strptime(data['startDate'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['endDate'], '%Y-%m-%d').date()
    except ValueError:
        return ResponseUtil.bad_request(message='日期格式不正确，请使用 YYYY-MM-DD 格式')

    exam_dto = ExamCreateDTO.from_dict(data)

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

    db.session.add(new_exam)
    db.session.commit()

    response_dto = ExamResponseDTO.from_model(new_exam)

    return ResponseUtil.success(data=response_dto.to_dict(), message="考试创建成功"), 201

@bp.route('/<string:exam_code>', methods=['GET'])
def get_exam(exam_code):
    """获取单个考试数据"""
    exam = Exam.query.filter_by(exam_code=exam_code).first()
    if not exam:
        return ResponseUtil.not_found(message='考试不存在')

    exam_dto = ExamResponseDTO.from_model(exam)

    return ResponseUtil.success(data=exam_dto.to_dict(), message="获取考试成功")

@bp.route('/<string:exam_code>', methods=['PUT'])
def update_exam(exam_code):
    """更新考试数据"""
    exam = Exam.query.filter_by(exam_code=exam_code).first()
    if not exam:
        return ResponseUtil.not_found(message='考试不存在')

    data = request.get_json()

    exam_dto = ExamUpdateDTO.from_dict(data)

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

    db.session.commit()

    response_dto = ExamResponseDTO.from_model(exam)

    return ResponseUtil.success(data=response_dto.to_dict(), message="考试更新成功")

@bp.route('/<string:exam_code>', methods=['DELETE'])
def delete_exam(exam_code):
    """删除考试"""
    exam = Exam.query.filter_by(exam_code=exam_code).first()
    if not exam:
        return ResponseUtil.not_found(message='考试不存在')

    db.session.delete(exam)
    db.session.commit()

    return ResponseUtil.success(message='考试删除成功')
