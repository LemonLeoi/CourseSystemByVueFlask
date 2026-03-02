# 可组合函数目录结构

## 概述
本文档描述了前端项目中可组合函数的目录结构，包括它们的组织方式、用途和使用指南。

## 目录结构

```
composables/
├── common/            # 全项目通用的可组合函数
├── api/               # API相关可组合函数
├── state/             # 状态管理可组合函数
├── validation/        # 验证可组合函数
├── course/            # 课程相关可组合函数
├── dashboard/         # 仪表盘相关可组合函数
├── student/           # 学生管理可组合函数
├── teacher/           # 教师管理可组合函数
├── exam/              # 考试管理可组合函数
├── layout/            # 布局相关可组合函数
└── README.md          # 本文档
```

## 目录详情

### common/
全项目通用的可组合函数。这些提供通用工具和辅助函数。

**示例：**
- useLocalStorage.ts
- usePagination.ts
- useSearch.ts
- useModal.ts
- useArchive.ts

**使用：** 在项目中任何需要通用功能的地方使用这些可组合函数。

### api/
与API请求和数据获取相关的可组合函数。

**示例：**
- useCrudOperations.ts

**使用：** 在处理API请求和数据获取时使用这些可组合函数。

### state/
与状态管理相关的可组合函数。

**示例：**
- useState.ts
- useStore.ts

**使用：** 在处理状态管理时使用这些可组合函数。

### validation/
与表单验证和数据验证相关的可组合函数。

**示例：**
- useValidation.ts

**使用：** 在处理表单验证和数据验证时使用这些可组合函数。

### course/
专门与课程管理相关的可组合函数。

**示例：**
- useCourseManage.ts
- useCourseTable.ts
- useStudentCourse.ts
- useTeacherCourse.ts
- useTeachingProgress.ts
- useCourseCommon.ts

**使用：** 仅在课程管理模块中使用这些可组合函数。

### dashboard/
专门与管理仪表盘相关的可组合函数。

**示例：**
- useDashboard.ts

**使用：** 仅在管理仪表盘模块中使用这些可组合函数。

### student/
专门与学生管理相关的可组合函数。

**示例：**
- useStudentManage.ts
- useStudentStatusManage.ts

**使用：** 仅在学生管理模块中使用这些可组合函数。

### teacher/
专门与教师管理相关的可组合函数。

**示例：**
- useTeacherManage.ts

**使用：** 仅在教师管理模块中使用这些可组合函数。

### exam/
专门与考试管理相关的可组合函数。

**示例：**
- useExamManage.ts
- useExamNotice.ts

**使用：** 仅在考试管理模块中使用这些可组合函数。

### layout/
与应用布局相关的可组合函数。

**示例：**
- useLayout.ts

**使用：** 在处理应用布局时使用这些可组合函数。

## 可组合函数分类指南

### 何时将可组合函数放在common/中
- 它是一个通用工具函数
- 它在全项目的多个模块中使用
- 它不包含模块特定的业务逻辑

### 何时将可组合函数放在功能特定目录中（api/、state/、validation/）
- 它与特定功能类型相关
- 它在多个模块中使用，但与特定功能相关
- 它为特定领域提供功能

### 何时将可组合函数放在模块特定目录中
- 它特定于单个业务模块
- 它包含模块特定的业务逻辑
- 它不在其他模块中重用

## 命名规范

### 可组合函数文件
- 可组合函数文件名使用camelCase并带有"use"前缀（例如：`useLocalStorage.ts`、`useCourseManage.ts`）
- 使用描述性名称，反映可组合函数的用途

### 目录名称
- 目录名称使用kebab-case（例如：`common`、`course`、`student-management`）
- 根据内容使用单数或复数形式（例如：`api`用于API相关可组合函数，`students`用于多个学生相关可组合函数）

## 最佳实践

1. **保持可组合函数专注：** 每个可组合函数应该只有一个职责
2. **使用适当的类型：** 为可组合函数的输入和输出定义清晰的TypeScript类型
3. **文档化可组合函数：** 添加注释以解释复杂可组合函数的目的和用法
4. **重用可组合函数：** 在创建新可组合函数之前，寻找重用现有可组合函数的机会
5. **测试可组合函数：** 为关键可组合函数编写测试

## 维护

- 定期审查可组合函数结构，确保其保持组织良好
- 根据需要重构可组合函数，以提高可重用性
- 添加新目录或更改现有目录时更新本文档
