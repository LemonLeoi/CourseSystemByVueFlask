from flask import Blueprint, request, jsonify
from app import db
from app.models import Teacher, VALID_SUBJECTS, VALID_TITLES, VALID_FULL_CLASSES

bp = Blueprint('teachers', __name__)

@bp.route('/', methods=['GET'])
def get_teachers():
    """获取所有教师数据，支持搜索和筛选"""
    # 获取查询参数
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    department = request.args.get('department', '')
    
    # 构建查询
    query = Teacher.query
    
    # 应用筛选条件
    if search:
        query = query.filter(
            (Teacher.name.ilike(f'%{search}%')) |
            (Teacher.teacher_id.ilike(f'%{search}%')) |
            (Teacher.department.ilike(f'%{search}%'))
        )
    
    if status:
        query = query.filter(Teacher.status == status)
    
    if department:
        query = query.filter(Teacher.department == department)
    
    # 执行查询
    teachers = query.all()
    
    # 返回结果
    return jsonify([teacher.to_dict() for teacher in teachers])

@bp.route('/<string:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    """获取单个教师数据"""
    teacher = Teacher.query.filter_by(teacher_id=teacher_id).first()
    if not teacher:
        return jsonify({'error': '教师不存在'}), 404
    return jsonify(teacher.to_dict())

@bp.route('/', methods=['POST'])
def create_teacher():
    """创建新教师"""
    data = request.get_json()
    
    # 验证数据
    required_fields = ['name', 'teacher_id', 'gender', 'age', 'title', 'department']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'缺少必填字段: {field}'}), 400
    
    # 验证学科、职称是否有效
    if 'subject' in data and data['subject'] not in VALID_SUBJECTS:
        return jsonify({'error': f'无效的学科: {data["subject"]}'}), 400
    
    if data['title'] not in VALID_TITLES:
        return jsonify({'error': f'无效的职称: {data["title"]}'}), 400
    
    # 验证任教班级是否有效
    if 'teaching_classes' in data:
        for class_name in data['teaching_classes']:
            if class_name and class_name not in VALID_FULL_CLASSES:
                return jsonify({'error': f'无效的班级: {class_name}'}), 400
    
    # 验证班主任班级是否有效
    if data.get('is_homeroom_teacher') and data.get('homeroom_class'):
        if data['homeroom_class'] not in VALID_FULL_CLASSES:
            return jsonify({'error': f'无效的班主任班级: {data["homeroom_class"]}'}), 400
    
    # 检查教师ID是否已存在
    existing_teacher = Teacher.query.filter_by(teacher_id=data['teacher_id']).first()
    if existing_teacher:
        return jsonify({'error': '教师ID已存在'}), 400
    
    # 创建教师
    new_teacher = Teacher(
        name=data['name'],
        teacher_id=data['teacher_id'],
        gender=data['gender'],
        age=data['age'],
        title=data['title'],
        department=data['department'],
        contact=data.get('contact'),
        status=data.get('status', 'active')
    )
    
    # 保存到数据库
    db.session.add(new_teacher)
    db.session.commit()
    
    # 处理任教班级
    if 'teaching_classes' in data:
        from app.models import TeacherClass
        for class_name in data['teaching_classes']:
            if class_name:
                # 提取年级和班级信息
                if len(class_name) >= 3:
                    grade = class_name[:2]
                    class_ = class_name[2:].replace("班", "")
                else:
                    grade = "未知"
                    class_ = class_name
                new_class = TeacherClass(teacher_id=data['teacher_id'], grade=grade, class_=class_)
                db.session.add(new_class)
    
    # 处理班主任状态
    if data.get('is_homeroom_teacher') and data.get('homeroom_class'):
        from app.models import HomeroomTeacher
        class_name = data['homeroom_class']
        # 提取年级和班级信息
        if len(class_name) >= 3:
            grade = class_name[:2]
            class_ = class_name[2:].replace("班", "")
        else:
            grade = "未知"
            class_ = class_name
        # 检查班级是否已有班主任
        existing_homeroom = HomeroomTeacher.query.filter_by(grade=grade, class_=class_).first()
        if existing_homeroom:
            # 如果有，更新为当前教师
            existing_homeroom.teacher_id = data['teacher_id']
        else:
            # 如果没有，创建新的班主任关联
            new_homeroom = HomeroomTeacher(teacher_id=data['teacher_id'], grade=grade, class_=class_)
            db.session.add(new_homeroom)
    
    # 保存更改
    db.session.commit()
    
    return jsonify(new_teacher.to_dict()), 201

@bp.route('/<string:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    """更新教师数据"""
    teacher = Teacher.query.filter_by(teacher_id=teacher_id).first()
    if not teacher:
        return jsonify({'error': '教师不存在'}), 404
    
    data = request.get_json()
    
    # 更新字段并验证
    if 'name' in data:
        teacher.name = data['name']
    if 'gender' in data:
        teacher.gender = data['gender']
    if 'age' in data:
        teacher.age = data['age']
    if 'subject' in data:
        if data['subject'] not in VALID_SUBJECTS:
            return jsonify({'error': f'无效的学科: {data["subject"]}'}), 400
        teacher.subject = data['subject']
    if 'title' in data:
        if data['title'] not in VALID_TITLES:
            return jsonify({'error': f'无效的职称: {data["title"]}'}), 400
        teacher.title = data['title']
    if 'department' in data:
        teacher.department = data['department']
    if 'contact' in data:
        teacher.contact = data['contact']
    if 'status' in data:
        teacher.status = data['status']
    
    # 处理任教班级
    if 'teaching_classes' in data:
        # 验证任教班级是否有效
        for class_name in data['teaching_classes']:
            if class_name and class_name not in VALID_FULL_CLASSES:
                return jsonify({'error': f'无效的班级: {class_name}'}), 400
        
        # 删除现有班级关联
        from app.models import TeacherClass
        TeacherClass.query.filter_by(teacher_id=teacher_id).delete()
        
        # 添加新班级关联
        for class_name in data['teaching_classes']:
            if class_name:
                # 提取年级和班级信息
                if len(class_name) >= 3:
                    grade = class_name[:2]
                    class_ = class_name[2:].replace("班", "")
                else:
                    grade = "未知"
                    class_ = class_name
                new_class = TeacherClass(teacher_id=teacher_id, grade=grade, class_=class_)
                db.session.add(new_class)
    
    # 处理班主任状态
    if 'is_homeroom_teacher' in data and 'homeroom_class' in data:
        # 验证班主任班级是否有效
        if data['is_homeroom_teacher'] and data['homeroom_class']:
            if data['homeroom_class'] not in VALID_FULL_CLASSES:
                return jsonify({'error': f'无效的班主任班级: {data["homeroom_class"]}'}), 400
        
        from app.models import HomeroomTeacher
        # 先删除现有班主任关联
        HomeroomTeacher.query.filter_by(teacher_id=teacher_id).delete()
        
        # 如果是班主任且指定了班级，添加新的班主任关联
        if data['is_homeroom_teacher'] and data['homeroom_class']:
            class_name = data['homeroom_class']
            # 提取年级和班级信息
            if len(class_name) >= 3:
                grade = class_name[:2]
                class_ = class_name[2:].replace("班", "")
            else:
                grade = "未知"
                class_ = class_name
            # 检查班级是否已有班主任
            existing_homeroom = HomeroomTeacher.query.filter_by(grade=grade, class_=class_).first()
            if existing_homeroom:
                # 如果有，更新为当前教师
                existing_homeroom.teacher_id = teacher_id
            else:
                # 如果没有，创建新的班主任关联
                new_homeroom = HomeroomTeacher(teacher_id=teacher_id, grade=grade, class_=class_)
                db.session.add(new_homeroom)
    
    # 保存更改
    db.session.commit()
    
    return jsonify(teacher.to_dict())

@bp.route('/<string:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    """删除教师"""
    teacher = Teacher.query.filter_by(teacher_id=teacher_id).first()
    if not teacher:
        return jsonify({'error': '教师不存在'}), 404
    
    # 删除关联数据
    from app.models import TeacherClass, HomeroomTeacher, Course
    
    # 删除教师班级关联
    TeacherClass.query.filter_by(teacher_id=teacher_id).delete()
    
    # 删除班主任关联
    HomeroomTeacher.query.filter_by(teacher_id=teacher_id).delete()
    
    # 处理课程关联（将课程的教师设置为空字符串，避免NOT NULL约束错误）
    courses = Course.query.filter_by(teacher_id=teacher_id).all()
    for course in courses:
        course.teacher_id = ''
    
    # 从数据库中删除教师
    db.session.delete(teacher)
    db.session.commit()
    
    return jsonify({'message': '教师删除成功'})

@bp.route('/options', methods=['GET'])
def get_teacher_options():
    """获取教师相关的所有有效选项列表"""
    # 从数据库中获取实际存在的部门/学科列表
    actual_departments = set()
    teachers = Teacher.query.all()
    for teacher in teachers:
        if teacher.department:
            actual_departments.add(teacher.department)
    
    # 合并预定义的学科列表和实际存在的部门列表，确保不重复
    all_subjects = list(set(VALID_SUBJECTS + list(actual_departments)))
    all_subjects.sort()  # 排序，确保顺序一致
    
    return jsonify({
        'subjects': all_subjects,
        'titles': VALID_TITLES,
        'fullClasses': VALID_FULL_CLASSES
    })