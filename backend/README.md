# 成绩分析系统 - 后端

## 项目概述

本项目是学校管理系统的后端部分，基于 Flask 框架构建，提供 RESTful API 接口，支持学生成绩管理、数据分析和知识发现功能。

## 技术栈

### 后端技术
- **框架**: Flask 2.3+
- **ORM**: SQLAlchemy 2.0+
- **数据库**: SQLite
- **CORS**: Flask-CORS
- **环境管理**: python-dotenv

### 代码质量工具
- **flake8**: Python代码规范检查

## 项目结构

```
backend/
├── app/                   # 应用代码
│   ├── api/               # API路由
│   │   ├── admin_routes.py      # 管理员路由
│   │   ├── analysis_routes.py   # 分析路由
│   │   ├── auth_routes.py       # 认证路由
│   │   ├── course_routes.py     # 课程路由
│   │   ├── exam_routes.py       # 考试路由
│   │   ├── grade_routes.py      # 成绩路由
│   │   ├── grade_settings_routes.py  # 成绩设置路由
│   │   ├── student_routes.py    # 学生路由
│   │   └── teacher_routes.py    # 教师路由
│   ├── models/            # 数据库模型
│   │   ├── classroom.py         # 教室模型
│   │   ├── course.py            # 课程模型
│   │   ├── course_schedule.py   # 课程表模型
│   │   ├── exam.py              # 考试模型
│   │   ├── grade.py             # 成绩模型
│   │   ├── grade_settings.py    # 成绩设置模型
│   │   ├── student.py           # 学生模型
│   │   ├── student_course.py    # 学生课程模型
│   │   ├── student_status.py    # 学生状态模型
│   │   ├── teacher.py           # 教师模型
│   │   ├── teacher_course.py    # 教师课程模型
│   │   ├── teaching_progress.py # 教学进度模型
│   │   └── user.py              # 用户模型
│   ├── data_access/       # 数据访问层
│   │   ├── grade_data_access.py        # 成绩数据访问
│   │   └── grade_settings_data_access.py # 成绩设置数据访问
│   ├── analysis/          # 数据分析模块
│   │   ├── grade_analyzer.py       # 成绩分析器
│   │   ├── decision_tree.py        # 决策树算法
│   │   ├── statistical_analysis.py # 统计分析
│   │   ├── analysis_explainer.py   # 分析解释器
│   │   ├── analysis_logger.py      # 分析日志
│   │   ├── intermediate_results.py # 中间结果存储
│   │   └── etl_manager.py          # ETL管理器
│   ├── services/          # 服务层
│   │   ├── conflict_service.py     # 冲突处理服务
│   │   └── sync_service.py         # 同步服务
│   ├── dto/               # 数据传输对象
│   │   └── exam_dto.py             # 考试DTO
│   ├── utils/             # 工具类
│   │   └── response.py             # 响应工具
│   └── __init__.py        # 应用初始化
├── migrations/            # 数据库迁移脚本
├── backups/               # 数据库备份
├── .flake8               # flake8配置
├── app.py                # 应用入口
└── database_redesign_report.md  # 数据库设计报告
```

## 核心功能

### 1. 成绩管理 API
- 学生成绩录入和查询
- 班级成绩统计
- 年级成绩汇总

### 2. 数据分析 API
- 学生个人成绩分析
- 班级成绩对比分析
- 年级成绩趋势分析
- 教师教学效果评估

### 3. 知识发现 API
- 决策树分析
- 特征重要性评估
- 多因素影响分析
- 挖掘发现展示

### 4. 数据管理 API
- 学生信息管理
- 教师信息管理
- 课程管理
- 考试管理

## 快速开始

### 环境要求
- Python >= 3.8.0
- pip >= 20.0.0

### 安装步骤

1. **进入后端目录**
```bash
cd backend
```

2. **安装依赖**
```bash
pip install flask flask-cors sqlalchemy python-dotenv flake8
```

3. **启动服务器**
```bash
python app.py
```

4. **访问 API**
- 基础URL: `http://localhost:5000/api`
- 健康检查: `http://localhost:5000/api/health`

### 运行命令

| 命令 | 描述 |
|------|------|
| `python app.py` | 启动开发服务器 |
| `flake8 .` | 代码规范检查 |

## API 接口

### 基础信息
- **基础URL**: `http://localhost:5000/api`
- **认证方式**: 暂无（预留JWT）
- **数据格式**: JSON

### 接口列表

| 模块 | 接口路径 | HTTP方法 | 功能描述 |
|------|----------|----------|----------|
| 学生管理 | `/api/students` | GET | 获取学生列表 |
| 学生管理 | `/api/students` | POST | 创建学生 |
| 学生管理 | `/api/students/<id>` | GET | 获取学生详情 |
| 学生管理 | `/api/students/<id>` | PUT | 更新学生信息 |
| 学生管理 | `/api/students/<id>` | DELETE | 删除学生 |
| 成绩管理 | `/api/grades` | GET | 获取成绩列表 |
| 成绩管理 | `/api/grades` | POST | 录入成绩 |
| 成绩管理 | `/api/grades/analysis` | GET | 成绩分析 |
| 考试管理 | `/api/exams` | GET | 获取考试列表 |
| 考试管理 | `/api/exams` | POST | 创建考试 |
| 分析接口 | `/api/analysis/knowledge-discoveries` | GET | 获取挖掘发现 |
| 分析接口 | `/api/analysis/feature-importance` | GET | 获取特征重要性 |
| 分析接口 | `/api/analysis/decision-tree-path` | POST | 获取决策树路径 |

## 代码规范

### flake8 配置
- 行宽: 100 字符
- 遵循 PEP 8 规范
- 排除目录: `__pycache__`, `migrations`, `.git`

### 代码风格
- 使用 4 空格缩进
- 变量命名使用 snake_case
- 函数命名使用 snake_case
- 类命名使用 PascalCase
- 为公共函数添加文档字符串

## 数据库设计

### 核心表结构

| 表名 | 描述 | 主要字段 |
|------|------|----------|
| students | 学生信息 | student_id, name, gender, class_, grade |
| teachers | 教师信息 | teacher_id, name, gender, title |
| courses | 课程信息 | course_code, course_name, subject |
| exams | 考试信息 | exam_code, exam_name, exam_type, grade |
| student_grades | 学生成绩 | student_id, exam_code, subject, score |
| course_schedules | 课程表 | class_, grade, subject, teacher_id |

## 贡献指南

### 提交规范

```
类型(模块): 简要描述

详细描述（可选）
```

**类型说明**:
- feat: 新增功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式
- refactor: 代码重构
- test: 测试更新
- chore: 构建/工具更新

### 分支策略

- `main`: 主分支，稳定版本
- `develop`: 开发分支
- `feature/*`: 功能分支
- `bugfix/*`: 修复分支

## 许可证

MIT License

## 联系方式

- 作者: 开发团队
- 邮箱: dev@example.com