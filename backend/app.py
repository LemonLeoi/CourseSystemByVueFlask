from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask_restx import Api

# 加载环境变量
load_dotenv()

# 创建Flask应用实例
app = Flask(__name__)

# 配置CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# 配置SQLite数据库
import os
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'data', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 导入db实例
from app import db

# 初始化数据库
db.init_app(app)

# 初始化Swagger API
api = Api(
    app,
    version='1.0',
    title='学校管理系统API',
    description='学校管理系统的API接口文档',
    doc='/swagger'
)

# 导入路由
from app.api import auth_routes
from app.api import admin_routes
from app.api import student_routes
from app.api import teacher_routes
from app.api import course_routes
from app.api import grade_routes
from app.api import exam_routes
from app.api import analysis_routes
from app.api import grade_settings_routes

# 注册蓝图
app.register_blueprint(student_routes.bp, url_prefix='/api/students')
app.register_blueprint(teacher_routes.bp, url_prefix='/api/teachers')
app.register_blueprint(course_routes.bp, url_prefix='/api/courses')
app.register_blueprint(grade_routes.bp, url_prefix='/api/grades')
app.register_blueprint(exam_routes.bp, url_prefix='/api/exams')
app.register_blueprint(auth_routes.bp, url_prefix='/api/auth')
app.register_blueprint(admin_routes.bp, url_prefix='/api/admin')
app.register_blueprint(grade_settings_routes.bp, url_prefix='/api/grade-settings')
app.register_blueprint(analysis_routes.analysis_bp)

# 根路由
@app.route('/')
def index():
    return "School Management System API"

# 健康检查路由
@app.route('/health')
def health_check():
    return {"status": "healthy"}

if __name__ == '__main__':
    # 创建数据库表
    with app.app_context():
        db.create_all()
    # 运行应用
    app.run(debug=True, host='0.0.0.0', port=5000)