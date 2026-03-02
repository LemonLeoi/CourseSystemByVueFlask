from flask import Blueprint
from .auth_routes import bp as auth_bp
from .student_routes import bp as student_bp
from .teacher_routes import bp as teacher_bp
from .course_routes import bp as course_bp
from .exam_routes import bp as exam_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(student_bp, url_prefix='/api/students')
    app.register_blueprint(teacher_bp, url_prefix='/api/teachers')
    app.register_blueprint(course_bp, url_prefix='/api/courses')
    app.register_blueprint(exam_bp, url_prefix='/api/exams')
