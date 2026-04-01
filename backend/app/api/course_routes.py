from flask import Blueprint, request, jsonify
from app import db
from app.models import Course, StudentCourse, TeacherCourse, TeachingProgress, Classroom

# 创建Blueprint
bp = Blueprint('courses', __name__)

# 年级到代码的映射
GRADE_CODES = {
    '高一': '10',
    '高二': '20',
    '高三': '30'
}

# 特殊科目年级代码映射
SPECIAL_GRADE_SUBJECT_CODES = {
    ('高一', '体育'): '11',
    ('高二', '体育'): '21',
    ('高三', '体育'): '31',
    ('高一', '美术'): '12',
    ('高二', '美术'): '22',
    ('高三', '美术'): '32'
}

# 科目到代码的映射
SUBJECT_CODES = {
    '语文': '01',
    '数学': '02',
    '英语': '03',
    '物理': '14',
    '化学': '15',
    '生物': '16',
    '历史': '24',
    '政治': '25',
    '地理': '26'
}

# 课程管理API
@bp.route('/', methods=['GET'])
def get_courses():
    """获取所有课程数据，支持搜索和筛选"""
    # 获取查询参数
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    semester = request.args.get('semester', '')
    year = request.args.get('year', '')
    teacher_id = request.args.get('teacher_id', '')
    
    # 构建查询
    query = Course.query
    
    # 应用筛选条件
    if search:
        query = query.filter(
            (Course.course_name.ilike(f'%{search}%')) |
            (Course.course_code.ilike(f'%{search}%'))
        )
    
    if status:
        query = query.filter(Course.status == status)
    
    if semester:
        query = query.filter(Course.semester == semester)
    
    if year:
        try:
            query = query.filter(Course.year == int(year))
        except ValueError:
            pass
    
    if teacher_id:
        query = query.filter(Course.teacher_id == teacher_id)
    
    # 执行查询
    courses = query.all()
    
    # 返回结果
    return jsonify([course.to_dict() for course in courses])

@bp.route('/<int:id>', methods=['GET'])
def get_course(id):
    """获取单个课程数据"""
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    return jsonify(course.to_dict())

@bp.route('/', methods=['POST'])
def create_course():
    """创建新课程"""
    data = request.get_json()
    
    # 验证数据
    required_fields = ['course_name', 'teacher_id', 'subject', 'grade', 'semester', 'year']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    # 生成课程代码
    grade = data['grade']
    subject = data['subject']
    
    # 检查年级是否有效
    if grade not in GRADE_CODES:
        return jsonify({'error': '无效的年级'}), 400
    
    # 检查科目是否有效
    if subject not in SUBJECT_CODES and subject not in ['体育', '美术']:
        return jsonify({'error': '无效的科目'}), 400
    
    # 生成前两位代码
    if (grade, subject) in SPECIAL_GRADE_SUBJECT_CODES:
        # 特殊科目（体育、美术）
        first_two = SPECIAL_GRADE_SUBJECT_CODES[(grade, subject)]
        # 特殊科目不需要后两位代码
        course_code = first_two
    else:
        # 普通科目
        first_two = GRADE_CODES[grade]
        second_two = SUBJECT_CODES.get(subject, '')
        if not second_two:
            return jsonify({'error': '无效的科目'}), 400
        course_code = first_two + second_two
    
    # 检查课程代码是否已存在
    existing_course = Course.query.filter_by(course_code=course_code).first()
    if existing_course:
        return jsonify({'error': '课程代码已存在'}), 400
    
    # 创建课程
    new_course = Course(
        course_name=data['course_name'],
        course_code=course_code,
        teacher_id=data['teacher_id'],
        subject=data['subject'],
        grade=data['grade'],
        semester=data['semester'],
        year=data['year']
    )
    
    # 保存到数据库
    db.session.add(new_course)
    db.session.commit()
    
    # 重新查询以获取关联数据
    new_course = Course.query.get(new_course.id)
    
    return jsonify(new_course.to_dict()), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_course(id):
    """更新课程数据"""
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    
    data = request.get_json()
    
    # 更新字段
    if 'course_name' in data:
        course.course_name = data['course_name']
    if 'course_code' in data:
        course.course_code = data['course_code']
    if 'teacher_id' in data:
        course.teacher_id = data['teacher_id']
    if 'subject' in data:
        course.subject = data['subject']
    if 'grade' in data:
        course.grade = data['grade']
    if 'semester' in data:
        course.semester = data['semester']
    if 'year' in data:
        course.year = data['year']
    
    # 保存更改
    db.session.commit()
    
    # 重新查询以获取关联数据
    course = Course.query.get(id)
    
    return jsonify(course.to_dict())

@bp.route('/<int:id>', methods=['DELETE'])
def delete_course(id):
    """删除课程"""
    course = Course.query.get(id)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    
    # 从数据库中删除
    db.session.delete(course)
    db.session.commit()
    
    return jsonify({'message': '课程删除成功'})

# 学生课程表API
@bp.route('/student-courses', methods=['GET'])
def get_student_courses():
    """获取学生课程表数据"""
    # 获取查询参数
    grade = request.args.get('grade', '')
    class_name = request.args.get('class', '')
    
    # 构建查询
    query = StudentCourse.query
    
    # 应用筛选条件
    if class_name:
        query = query.filter(StudentCourse.class_ == class_name)
    
    if grade:
        query = query.filter(StudentCourse.grade == grade)
    
    # 执行查询
    courses = query.all()
    
    # 返回结果
    return jsonify([course.to_dict() for course in courses])

@bp.route('/student-courses/<int:id>', methods=['GET'])
def get_student_course(id):
    """获取单个学生课程数据"""
    course = StudentCourse.query.get(id)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    return jsonify(course.to_dict())

@bp.route('/student-courses', methods=['POST'])
def create_student_course():
    """创建新学生课程"""
    data = request.get_json()
    
    # 验证数据
    required_fields = ['name', 'teacher_id', 'day_of_week', 'period', 'room_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    # 处理className字段，从其中提取年级和班级
    grade = data.get('grade')
    class_ = data.get('class')
    
    # 如果提供了className，则从其中提取年级和班级
    if 'className' in data:
        class_name = data['className']
        # 提取年级（如“高一”、“高二”、“高三”）
        if '高一' in class_name:
            grade = '高一'
            class_ = class_name.replace('高一', '')
        elif '高二' in class_name:
            grade = '高二'
            class_ = class_name.replace('高二', '')
        elif '高三' in class_name:
            grade = '高三'
            class_ = class_name.replace('高三', '')
    
    # 验证年级和班级
    if not grade:
        return jsonify({'error': '缺少必填字段: grade'}), 400
    if not class_:
        return jsonify({'error': '缺少必填字段: class'}), 400
    
    # 验证room_id是否存在
    room = db.session.query(Classroom).filter_by(room_id=data['room_id']).first()
    if not room:
        return jsonify({'error': '教室ID不存在'}), 400
    
    # 创建学生课程
    new_course = StudentCourse(
        grade=grade,
        class_=class_,
        course_code=data.get('course_code'),
        teacher_id=data['teacher_id'],
        day_of_week=data['day_of_week'],
        period=data['period'],
        classroom=room.room_id,  # 使用room_id作为classroom字段的值
        room_id=data['room_id'],  # 设置新的room_id字段
        status=data.get('status', 'active')
    )
    
    # 保存到数据库
    db.session.add(new_course)
    db.session.commit()
    
    return jsonify(new_course.to_dict()), 201

@bp.route('/student-courses/<int:id>', methods=['PUT'])
def update_student_course(id):
    """更新学生课程数据"""
    course = StudentCourse.query.get(id)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    
    data = request.get_json()
    
    # 更新字段
    if 'grade' in data:
        course.grade = data['grade']
    if 'class' in data:
        course.class_ = data['class']
    if 'course_code' in data:
        course.course_code = data['course_code']
    if 'teacher_id' in data:
        course.teacher_id = data['teacher_id']
    if 'day_of_week' in data:
        course.day_of_week = data['day_of_week']
    if 'period' in data:
        course.period = data['period']
    if 'room_id' in data:
        # 验证room_id是否存在
        room = db.session.query(Classroom).filter_by(room_id=data['room_id']).first()
        if not room:
            return jsonify({'error': '教室ID不存在'}), 400
        course.room_id = data['room_id']
        course.classroom = room.room_id  # 更新classroom字段为room_id
    if 'status' in data:
        course.status = data['status']
    
    # 保存更改
    db.session.commit()
    
    return jsonify(course.to_dict())

@bp.route('/student-courses/<int:id>', methods=['DELETE'])
def delete_student_course(id):
    """删除学生课程"""
    course = StudentCourse.query.get(id)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    
    # 从数据库中删除
    db.session.delete(course)
    db.session.commit()
    
    return jsonify({'message': '课程删除成功'})

# 教师课程表API
@bp.route('/teacher-courses', methods=['GET'])
def get_teacher_courses():
    """获取教师课程表数据"""
    # 获取查询参数
    teacher_id = request.args.get('teacher_id', '')
    
    # 构建查询
    query = TeacherCourse.query
    
    # 应用筛选条件
    if teacher_id:
        query = query.filter(TeacherCourse.teacher_id == teacher_id)
    
    # 执行查询
    courses = query.all()
    
    # 返回结果
    return jsonify([course.to_dict() for course in courses])

@bp.route('/teacher-courses/<int:id>', methods=['GET'])
def get_teacher_course(id):
    """获取单个教师课程数据"""
    course = TeacherCourse.query.get(id)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    return jsonify(course.to_dict())

@bp.route('/teacher-courses', methods=['POST'])
def create_teacher_course():
    """创建新教师课程"""
    data = request.get_json()
    
    # 验证数据
    required_fields = ['teacher', 'day_of_week', 'period', 'classroom', 'className']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    # 处理className字段，从其中提取年级和班级
    class_name = data['className']
    grade = ''
    class_ = ''
    
    # 提取年级（如“高一”、“高二”、“高三”）
    if '高一' in class_name:
        grade = '高一'
        class_ = class_name.replace('高一', '')
    elif '高二' in class_name:
        grade = '高二'
        class_ = class_name.replace('高二', '')
    elif '高三' in class_name:
        grade = '高三'
        class_ = class_name.replace('高三', '')
    
    # 验证年级和班级
    if not grade:
        return jsonify({'error': '缺少必填字段: grade'}), 400
    if not class_:
        return jsonify({'error': '缺少必填字段: class'}), 400
    
    # 创建教师课程
    new_course = TeacherCourse(
        teacher_id=data['teacher'],
        course_code=data.get('course_code'),
        grade=grade,
        class_=class_,
        day_of_week=data['day_of_week'],
        period=data['period'],
        classroom=data['classroom'],
        status=data.get('status', 'active')
    )
    
    # 保存到数据库
    db.session.add(new_course)
    db.session.commit()
    
    return jsonify(new_course.to_dict()), 201

@bp.route('/teacher-courses/<int:id>', methods=['PUT'])
def update_teacher_course(id):
    """更新教师课程数据"""
    course = TeacherCourse.query.get(id)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    
    data = request.get_json()
    
    # 更新字段
    if 'teacher_id' in data:
        course.teacher_id = data['teacher_id']
    if 'course_code' in data:
        course.course_code = data['course_code']
    if 'grade' in data:
        course.grade = data['grade']
    if 'class' in data:
        course.class_ = data['class']
    if 'day_of_week' in data:
        course.day_of_week = data['day_of_week']
    if 'period' in data:
        course.period = data['period']
    if 'classroom' in data:
        course.classroom = data['classroom']
    if 'status' in data:
        course.status = data['status']
    
    # 保存更改
    db.session.commit()
    
    return jsonify(course.to_dict())

@bp.route('/teacher-courses/<int:id>', methods=['DELETE'])
def delete_teacher_course(id):
    """删除教师课程"""
    course = TeacherCourse.query.get(id)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    
    # 从数据库中删除
    db.session.delete(course)
    db.session.commit()
    
    return jsonify({'message': '课程删除成功'})

# 教室API
@bp.route('/classrooms', methods=['GET'])
def get_classrooms():
    """获取教室列表数据"""
    # 构建查询
    query = Classroom.query
    
    # 执行查询
    classrooms = query.all()
    
    # 返回结果
    return jsonify([classroom.to_dict() for classroom in classrooms])

# 科目API
@bp.route('/subjects', methods=['GET'])
def get_subjects():
    """获取所有唯一的科目列表"""
    # 查询所有不同的科目
    subjects = db.session.query(Course.subject).distinct().all()
    # 提取科目名称
    subject_list = [subject[0] for subject in subjects]
    return jsonify(subject_list)

# 教学进度API
@bp.route('/teaching-progress', methods=['GET'])
def get_teaching_progress():
    """获取教学进度数据"""
    # 获取查询参数
    course_id = request.args.get('course_id', '')
    subject = request.args.get('subject', '')
    grade = request.args.get('grade', '')
    
    # 构建查询
    query = TeachingProgress.query
    
    # 应用筛选条件
    if course_id:
        try:
            query = query.filter(TeachingProgress.course_id == int(course_id))
        except ValueError:
            pass
    elif subject or grade:
        # 通过科目和年级筛选
        course_query = Course.query
        if subject:
            course_query = course_query.filter(Course.subject == subject)
        if grade:
            course_query = course_query.filter(Course.grade == grade)
        
        # 获取符合条件的课程ID列表
        course_ids = [course.id for course in course_query.all()]
        if course_ids:
            query = query.filter(TeachingProgress.course_id.in_(course_ids))
    
    # 执行查询
    progress = query.all()
    
    # 返回结果
    return jsonify([p.to_dict() for p in progress])

@bp.route('/teaching-progress/<int:id>', methods=['GET'])
def get_teaching_progress_item(id):
    """获取单个教学进度数据"""
    progress = TeachingProgress.query.get(id)
    if not progress:
        return jsonify({'error': '进度不存在'}), 404
    return jsonify(progress.to_dict())

@bp.route('/teaching-progress', methods=['POST'])
def create_teaching_progress():
    """创建新教学进度"""
    data = request.get_json()
    
    # 验证数据
    required_fields = ['course_id', 'chapter', 'hours', 'objective', 'progress', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    # 创建教学进度
    new_progress = TeachingProgress(
        course_id=data['course_id'],
        chapter=data['chapter'],
        hours=data['hours'],
        objective=data['objective'],
        progress=data['progress'],
        status=data['status']
    )
    
    # 保存到数据库
    db.session.add(new_progress)
    db.session.commit()
    
    return jsonify(new_progress.to_dict()), 201

@bp.route('/teaching-progress/<int:id>', methods=['PUT'])
def update_teaching_progress(id):
    """更新教学进度数据"""
    progress = TeachingProgress.query.get(id)
    if not progress:
        return jsonify({'error': '进度不存在'}), 404
    
    data = request.get_json()
    
    # 更新字段
    if 'chapter' in data:
        progress.chapter = data['chapter']
    if 'hours' in data:
        progress.hours = data['hours']
    if 'objective' in data:
        progress.objective = data['objective']
    if 'progress' in data:
        progress.progress = data['progress']
    if 'status' in data:
        progress.status = data['status']
    
    # 保存更改
    db.session.commit()
    
    return jsonify(progress.to_dict())

@bp.route('/teaching-progress/<int:id>', methods=['DELETE'])
def delete_teaching_progress(id):
    """删除教学进度"""
    progress = TeachingProgress.query.get(id)
    if not progress:
        return jsonify({'error': '进度不存在'}), 404
    
    # 从数据库中删除
    db.session.delete(progress)
    db.session.commit()
    
    return jsonify({'message': '进度删除成功'})
