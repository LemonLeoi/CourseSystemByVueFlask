from flask import Blueprint, request, jsonify
from app import db
from app.models import Student, Grade, VALID_CLASSES, VALID_GRADES

bp = Blueprint('students', __name__)

@bp.route('/', methods=['GET'])
def get_students():
    """获取所有学生数据，支持搜索和筛选"""
    # 获取查询参数
    search = request.args.get('search', '')
    grade = request.args.get('grade', '')
    class_name = request.args.get('class', '')
    
    # 构建查询
    query = Student.query
    
    # 应用筛选条件
    if search:
        query = query.filter(
            (Student.name.ilike(f'%{search}%')) |
            (Student.student_id.ilike(f'%{search}%')) |
            (Student.class_.ilike(f'%{search}%'))
        )
    
    if grade:
        query = query.filter(Student.grade == grade)
    
    if class_name:
        query = query.filter(Student.class_ == class_name)
    
    # 执行查询
    students = query.all()
    
    # 构建返回数据，确保每个学生对象都包含scores字段
    students_data = []
    for student in students:
        student_data = student.to_dict()
        # 获取学生成绩
        scores = []
        grade_records = Grade.query.filter_by(student_id=student.student_id).all()
        for grade_record in grade_records:
            scores.append({
                'subject': grade_record.subject,
                'score': grade_record.score,
                'grade': grade_record.grade_level,
                'examType': grade_record.exam_type,
                'semester': grade_record.semester,
                'examDate': grade_record.exam_date.isoformat() if grade_record.exam_date else None,
                'period': grade_record.period
            })
        student_data['scores'] = scores
        students_data.append(student_data)
    
    # 返回结果
    return jsonify(students_data)

@bp.route('/<string:student_id>', methods=['GET'])
def get_student(student_id):
    """获取单个学生数据，包括成绩"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': '学生不存在'}), 404
    
    # 获取学生数据
    student_data = student.to_dict()
    
    # 直接查询Grade表获取学生成绩，确保获取最新数据
    scores = []
    grade_records = Grade.query.filter_by(student_id=student_id).all()
    for grade_record in grade_records:
        scores.append({
            'subject': grade_record.subject,
            'score': grade_record.score,
            'grade': grade_record.grade_level,
            'examType': grade_record.exam_type,
            'semester': grade_record.semester,
            'examDate': grade_record.exam_date.isoformat() if grade_record.exam_date else None,
            'period': grade_record.period
        })
    
    student_data['scores'] = scores
    return jsonify(student_data)

@bp.route('/', methods=['POST'])
def create_student():
    """创建新学生"""
    data = request.get_json()
    
    # 验证数据
    # 支持前端的id字段和后端的student_id字段
    if 'id' in data:
        data['student_id'] = data['id']
    
    required_fields = ['name', 'student_id', 'gender', 'class', 'grade']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    # 验证班级和年级是否有效
    if data['class'] not in VALID_CLASSES:
        return jsonify({'error': f'无效的班级: {data["class"]}'}), 400
    
    if data['grade'] not in VALID_GRADES:
        return jsonify({'error': f'无效的年级: {data["grade"]}'}), 400
    
    # 检查学号是否已存在
    existing_student = Student.query.filter_by(student_id=data['student_id']).first()
    if existing_student:
        return jsonify({'error': '学号已存在'}), 400
    
    # 创建学生
    new_student = Student(
        student_id=data['student_id'],
        name=data['name'],
        gender=data['gender'],
        class_=data['class'],
        grade=data['grade'],
        contact=data.get('contact'),
        status=data.get('status', 'active')
    )
    
    # 保存到数据库
    db.session.add(new_student)
    db.session.commit()
    
    return jsonify(new_student.to_dict()), 201

@bp.route('/<string:student_id>', methods=['PUT'])
def update_student(student_id):
    """更新学生数据"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': '学生不存在'}), 404
    
    data = request.get_json()
    
    # 更新字段并验证
    if 'name' in data:
        student.name = data['name']
    if 'gender' in data:
        student.gender = data['gender']
    if 'class' in data:
        if data['class'] not in VALID_CLASSES:
            return jsonify({'error': f'无效的班级: {data["class"]}'}), 400
        student.class_ = data['class']
    if 'grade' in data:
        if data['grade'] not in VALID_GRADES:
            return jsonify({'error': f'无效的年级: {data["grade"]}'}), 400
        student.grade = data['grade']
    if 'contact' in data:
        student.contact = data['contact']
    if 'status' in data:
        student.status = data['status']
    
    # 保存更改
    db.session.commit()
    
    return jsonify(student.to_dict())

@bp.route('/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """删除学生"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': '学生不存在'}), 404
    
    # 删除学生的所有成绩
    Grade.query.filter_by(student_id=student_id).delete()
    
    # 从数据库中删除学生
    db.session.delete(student)
    db.session.commit()
    
    return jsonify({'message': '学生删除成功'})

@bp.route('/<string:student_id>/archive', methods=['PUT'])
def archive_student(student_id):
    """归档学生（设置为毕业状态）"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': '学生不存在'}), 404
    
    student.status = 'graduated'
    db.session.commit()
    
    return jsonify(student.to_dict())

@bp.route('/<string:student_id>/unarchive', methods=['PUT'])
def unarchive_student(student_id):
    """取消归档学生（设置为在校状态）"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': '学生不存在'}), 404
    
    student.status = 'active'
    db.session.commit()
    
    return jsonify(student.to_dict())

@bp.route('/<string:student_id>/grades', methods=['PUT'])
def update_student_grades(student_id):
    """更新学生成绩"""
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': '学生不存在'}), 404
    
    data = request.get_json()
    if 'scores' not in data:
        return jsonify({'error': '缺少成绩数据'}), 400
    
    scores = data['scores']
    
    # 删除现有成绩
    Grade.query.filter_by(student_id=student_id).delete()
    
    # 添加新成绩
    for score_data in scores:
        # 验证成绩数据
        if 'subject' not in score_data or 'score' not in score_data:
            return jsonify({'error': '成绩数据缺少必填字段'}), 400
        
        # 计算等级
        score = score_data['score']
        if score >= 90:
            grade_level = 'A'
        elif score >= 80:
            grade_level = 'B'
        elif score >= 70:
            grade_level = 'C'
        elif score >= 60:
            grade_level = 'D'
        else:
            grade_level = 'E'
        
        # 获取考试信息
        exam_type = score_data.get('examType', '期中考试')
        semester = score_data.get('semester')
        period = score_data.get('period')
        
        # 处理考试日期
        exam_date = None
        if 'examDate' in score_data:
            try:
                from datetime import datetime
                exam_date = datetime.strptime(score_data['examDate'], '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # 创建成绩记录
        new_grade = Grade(
            student_id=student_id,
            exam_type=exam_type,
            subject=score_data['subject'],
            score=score,
            grade_level=grade_level,
            exam_date=exam_date,
            semester=semester,
            period=period
        )
        
        db.session.add(new_grade)
    
    db.session.commit()
    
    # 更新成功后返回更新后的成绩数据，便于前端直接更新视图
    updated_grades = Grade.query.filter_by(student_id=student_id).all()
    updated_scores = []
    for grade in updated_grades:
        updated_scores.append({
            'subject': grade.subject,
            'score': grade.score,
            'grade': grade.grade_level,
            'examType': grade.exam_type,
            'semester': grade.semester,
            'examDate': grade.exam_date.isoformat() if grade.exam_date else None,
            'period': grade.period
        })
    
    return jsonify({
        'message': '成绩更新成功',
        'scores': updated_scores
    })

@bp.route('/classes', methods=['GET'])
def get_classes():
    """获取所有有效班级和年级列表"""
    return jsonify({
        'classes': VALID_CLASSES,
        'grades': VALID_GRADES
    })