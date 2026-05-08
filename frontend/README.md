# 成绩分析系统 - 前端

## 项目概述

本项目是学校管理系统的前端部分，基于 Vue 3 + TypeScript 构建，提供学生成绩管理、数据分析和可视化展示功能。

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

### 代码质量工具
- **ESLint**: 代码规范检查
- **Prettier**: 代码格式化

## 项目结构

```
frontend/
├── public/                # 静态资源
│   ├── static/            # 静态文件
│   └── index.html         # HTML入口
├── src/
│   ├── assets/            # 资源文件
│   ├── components/        # 组件
│   │   ├── business/      # 业务组件
│   │   ├── common/        # 通用组件
│   │   ├── course/        # 课程相关组件
│   │   ├── dashboard/     # 仪表盘组件
│   │   ├── grade/         # 成绩分析组件
│   │   └── layout/        # 布局组件
│   ├── composables/       # 组合式函数
│   │   ├── api/           # API操作
│   │   ├── common/        # 通用函数
│   │   ├── course/        # 课程相关
│   │   ├── exam/          # 考试相关
│   │   ├── grade/         # 成绩相关
│   │   └── layout/        # 布局相关
│   ├── router/            # 路由配置
│   ├── services/          # 服务层
│   │   ├── api/           # API服务
│   │   ├── data/          # 数据服务
│   │   └── ui/            # UI服务
│   ├── stores/            # 状态管理
│   ├── styles/            # 样式文件
│   ├── types/             # TypeScript类型定义
│   ├── views/             # 页面视图
│   ├── App.vue            # 根组件
│   ├── main.js            # 入口文件
│   └── style.css          # 全局样式
├── .eslintrc.js           # ESLint配置
├── .prettierrc            # Prettier配置
├── package.json           # 依赖配置
├── tsconfig.json          # TypeScript配置
└── vite.config.js         # Vite配置
```

## 核心功能

### 1. 成绩分析
- 学生个人成绩分析
- 班级成绩对比
- 年级成绩统计
- 学科成绩分析

### 2. 知识发现
- 决策树分析
- 特征重要性评估
- 多因素影响分析
- 数据挖掘发现展示

### 3. 可视化展示
- 成绩趋势图表
- 学科对比图表
- 决策树可视化
- 统计数据面板

### 4. 数据管理
- 学生信息管理
- 教师信息管理
- 课程管理
- 考试管理

## 快速开始

### 环境要求
- Node.js >= 18.0.0
- npm >= 9.0.0

### 安装步骤

1. **克隆仓库**
```bash
git clone <仓库地址>
cd A_Course/frontend
```

2. **安装依赖**
```bash
npm install
```

3. **启动开发服务器**
```bash
npm run dev
```

4. **访问应用**
- 开发环境: `http://localhost:5173`
- 后端API: `http://localhost:5000/api`

### 运行命令

| 命令 | 描述 |
|------|------|
| `npm run dev` | 启动开发服务器 |
| `npm run build` | 构建生产版本 |
| `npm run preview` | 预览生产版本 |
| `npm run lint` | 代码检查和自动修复 |

## 代码规范

### ESLint 规则
- 基于 `eslint:recommended`
- 集成 Vue 3 规则
- 集成 TypeScript 规则
- 集成 Prettier 规则

### Prettier 配置
- 行宽: 100 字符
- 缩进: 2 空格
- 单引号: true
- 尾随逗号: es5

## 开发规范

### 组件命名
- 使用 PascalCase 命名组件
- 组件名应描述其功能，如 `GradeChart.vue`

### 文件命名
- 使用 kebab-case 命名文件
- 组件文件使用 `.vue` 后缀
- 工具函数使用 `.ts` 后缀

### 代码注释
- 为复杂逻辑添加注释
- 为公共函数添加 JSDoc 注释
- 保持注释与代码同步

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