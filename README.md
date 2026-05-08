# 学校管理系统

## 项目概述

本项目是一个基于 Vue 3 + Flask 技术栈的学校管理系统，旨在为学校提供全面的信息化管理解决方案。系统涵盖学生管理、教师管理、课程管理、考试管理、教学进度管理和成绩分析等核心功能，通过前后端分离的架构实现高效、直观的管理体验。

## 技术栈

### 前端技术
- **框架**: Vue 3.5+
- **TypeScript**: 5.9+
- **状态管理**: Pinia 3.0+
- **路由**: Vue Router 5.0+
- **构建工具**: Vite 7.2+
- **UI组件**: Element Plus 2.13+
- **图表库**: ECharts 6.0+
- **样式**: CSS 3 + SCSS

### 后端技术
- **框架**: Flask 2.3+
- **数据库**: SQLite
- **ORM**: SQLAlchemy 2.0+
- **CORS**: Flask-CORS
- **环境管理**: python-dotenv

### 代码质量工具
- **前端**: ESLint + Prettier
- **后端**: flake8

## 项目结构

```
A_Course/
├── backend/                # 后端代码
│   ├── app/               # 应用代码
│   │   ├── api/           # API路由
│   │   ├── models/        # 数据库模型
│   │   ├── services/      # 服务层
│   │   ├── data_access/   # 数据访问层
│   │   └── analysis/      # 数据分析模块
│   ├── migrations/        # 数据库迁移
│   ├── app.py             # 应用入口
│   └── .flake8            # flake8配置
├── frontend/              # 前端代码
│   ├── src/               # 源代码
│   ├── public/            # 静态资源
│   ├── .eslintrc.js       # ESLint配置
│   ├── .prettierrc        # Prettier配置
│   └── package.json       # 依赖配置
├── docs/                  # 文档目录
│   └── DOCUMENTATION_STANDARD.md  # 文档格式标准
└── README.md              # 项目说明
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
- 成绩分析报告

### 6. 数据分析
- 学生个人成绩分析
- 班级成绩对比
- 年级成绩统计
- 知识发现与挖掘

## 快速开始

### 环境要求
- Node.js >= 18.0.0
- Python >= 3.8.0

### 启动后端服务

```bash
cd backend
pip install flask flask-cors sqlalchemy python-dotenv flake8
python app.py
```
- 访问地址: `http://localhost:5000`

### 启动前端服务

```bash
cd frontend
npm install
npm run dev
```
- 访问地址: `http://localhost:5173`

### 运行命令

#### 前端命令

| 命令 | 描述 |
|------|------|
| `npm run dev` | 启动开发服务器 |
| `npm run build` | 构建生产版本 |
| `npm run preview` | 预览生产版本 |
| `npm run lint` | 代码检查和自动修复 |

#### 后端命令

| 命令 | 描述 |
|------|------|
| `python app.py` | 启动开发服务器 |
| `flake8 .` | 代码规范检查 |

## 代码规范

### 前端规范
- **ESLint**: 代码质量检查
- **Prettier**: 代码格式化
- 行宽: 100 字符
- 缩进: 2 空格
- 单引号: true

### 后端规范
- **flake8**: Python代码规范检查
- 行宽: 100 字符
- 遵循 PEP 8 规范

## 文档规范

项目文档应遵循 `docs/DOCUMENTATION_STANDARD.md` 中定义的格式标准，包括：
- Markdown 文件命名规则
- 标题层级规范
- 代码块规范
- 表格规范
- README 文件结构模板

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
- `develop`: 开发分支，功能集成
- `feature/*`: 功能分支，开发新功能
- `bugfix/*`: 修复分支，修复bug
- `release/*`: 发布分支，准备发布

## 许可证

MIT License

## 联系方式

- 作者: 开发团队
- 邮箱: dev@example.com