# 学校管理系统全栈项目介绍

## 项目概述

本项目是一个基于Vue 3 + Flask技术栈的学校管理系统，旨在为学校提供全面的信息化管理解决方案。系统涵盖学生管理、教师管理、课程管理、考试管理、教学进度管理和成绩管理等核心功能，通过前后端分离的架构实现高效、直观的管理体验。

## 技术栈

### 前端技术
- **框架**：Vue 3 + TypeScript
- **状态管理**：Pinia
- **路由**：Vue Router
- **构建工具**：Vite
- **样式**：CSS + SCSS

### 后端技术
- **框架**：Flask
- **数据库**：SQLite
- **ORM**：SQLAlchemy
- **CORS**：Flask-CORS
- **环境管理**：python-dotenv

## 项目结构

### 前端结构
```
frontend/
├── public/            # 静态资源
├── src/
│   ├── assets/        # 资源文件
│   ├── components/    # 组件
│   │   ├── business/  # 业务组件
│   │   ├── common/    # 通用组件
│   │   ├── course/    # 课程相关组件
│   │   ├── dashboard/ # 仪表盘组件
│   │   └── layout/    # 布局组件
│   ├── composables/   # 组合式函数
│   ├── router/        # 路由配置
│   ├── services/      # 服务层
│   ├── stores/        # 状态管理
│   ├── styles/        # 样式文件
│   ├── types/         # TypeScript类型定义
│   ├── views/         # 页面视图
│   ├── App.vue        # 根组件
│   └── main.js        # 入口文件
├── package.json       # 依赖配置
└── vite.config.js     # Vite配置
```

### 后端结构
```
backend/
├── app/
│   ├── api/           # API路由
│   │   ├── admin_routes.py
│   │   ├── auth_routes.py
│   │   ├── course_routes.py
│   │   ├── exam_routes.py
│   │   ├── student_routes.py
│   │   └── teacher_routes.py
│   ├── models/        # 数据库模型
│   │   ├── classroom.py
│   │   ├── course.py
│   │   ├── exam.py
│   │   ├── grade.py
│   │   ├── student.py
│   │   ├── student_course.py
│   │   ├── teacher.py
│   │   ├── teacher_course.py
│   │   ├── teaching_progress.py
│   │   └── user.py
│   └── __init__.py
├── app.py             # 应用入口
└── 数据库设计详细说明.md
```

## 核心功能

### 1. 学生管理
- 学生信息的增删改查
- 学生状态管理（在校、休学、毕业、退学）
- 学生成绩查询

### 2. 教师管理
- 教师信息的增删改查
- 教师任教班级管理
- 班主任管理

### 3. 课程管理
- 课程信息的增删改查
- 课程表安排（学生课程表、教师课程表）
- 教学进度跟踪

### 4. 考试管理
- 考试信息的增删改查
- 考试状态管理

### 5. 成绩管理
- 学生成绩录入和查询
- 成绩等级管理

### 6. 教室管理
- 教室信息管理
- 教室状态管理

## 项目启动

### 前端启动
1. 进入前端目录：`cd frontend`
2. 安装依赖：`npm install`
3. 启动开发服务器：`npm run dev`
4. 访问：`http://localhost:5173`

### 后端启动
1. 进入后端目录：`cd backend`
2. 安装依赖：`pip install flask flask-cors sqlalchemy python-dotenv`
3. 启动服务器：`python app.py`
4. 访问：`http://localhost:5000`