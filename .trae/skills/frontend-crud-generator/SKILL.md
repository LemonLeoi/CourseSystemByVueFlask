---
name: "frontend-crud-generator"
description: "生成带有TypeScript、Pinia和API集成的Vue 3 CRUD页面。当为项目创建新的基于CRUD的管理页面时调用。"
---

# 前端CRUD生成器

此技能为学校管理系统项目生成完整的Vue 3 CRUD页面，支持TypeScript、Pinia状态管理和API集成。

## 功能特性

- 生成带有TypeScript setup的Vue 3单文件组件
- 包含用于状态管理的Pinia store
- 提供API服务集成
- 遵循项目现有的目录结构和编码规范
- 包含搜索、分页和模态框等常见组件
- 生成用于类型安全的TypeScript接口

## 使用方法

### 基本使用

要为新实体生成CRUD页面：

1. 指定实体名称（例如："Classroom"）
2. 定义实体的字段
3. 指定API端点
4. 选择其他功能（搜索、分页等）

### 生成的文件

该技能将生成以下文件：

- **视图组件**：`src/views/{entity}/Manage{Entity}.vue`
- **类型定义**：`src/types/{entity}.ts`
- **Pinia状态管理**：`src/stores/{entity}s.ts`
- **API服务**：`src/services/{entity}Service.ts`
- **可组合函数**：`src/composables/{entity}/use{Entity}Manage.ts`

### 示例

对于"Classroom"实体：

```typescript
// 生成的类型定义 (classroom.ts)
export interface Classroom {
  id: number;
  name: string;
  capacity: number;
  location: string;
}

// 生成的store (classrooms.ts)
export const useClassroomsStore = defineStore('classrooms', {
  state: () => ({
    classrooms: [] as Classroom[],
    loading: false,
    error: null as string | null
  }),
  // ... CRUD操作的actions
});

// 生成的视图组件 (ManageClassroom.vue)
<template>
  <Layout activePath="/classrooms">
    <BaseManagePage 
      title="Classroom Management"
      :totalItems="classrooms.length"
      :showAddButton="true"
      @add="openAddModal"
    >
      <!-- 生成的内容 -->
    </BaseManagePage>
  </Layout>
</template>
```

## 配置选项

### 实体配置

- **实体名称**：实体的单数名称（例如："Classroom"）
- **复数名称**：用于命名一致性的复数形式（例如："Classrooms"）
- **API端点**：后端API端点（例如："/api/classrooms"）

### 字段配置

对于每个字段，指定：

- **名称**：字段名称（例如："name"）
- **类型**：字段类型（例如："string"、"number"、"boolean"）
- **标签**：显示标签（例如："Classroom Name"）
- **必填**：字段是否必填
- **验证**：可选的验证规则

### 功能选项

- **搜索**：启用/禁用搜索功能
- **分页**：启用/禁用分页
- **排序**：启用/禁用列排序
- **过滤**：启用/禁用高级过滤
- **导出**：启用/禁用数据导出

## 最佳实践

1. **遵循命名约定**：组件使用PascalCase，变量使用camelCase
2. **类型安全**：始终为实体定义TypeScript接口
3. **状态管理**：使用Pinia store管理复杂状态
4. **API集成**：在服务文件中集中API调用
5. **组件重用**：尽可能利用现有的基础组件
6. **响应式设计**：确保页面在不同屏幕尺寸上正常工作

## 故障排除

### 常见问题

- **API集成错误**：检查API端点和CORS配置
- **类型错误**：确保TypeScript接口与后端数据结构匹配
- **状态管理问题**：验证Pinia store设置和actions
- **组件渲染问题**：检查Vue模板语法和组件属性

### 解决步骤

1. 验证生成的文件是否匹配项目结构
2. 检查TypeScript编译错误
3. 使用Postman或类似工具测试API端点
4. 确保Pinia store已正确注册
5. 验证组件属性和事件处理

## 与后端集成

此技能与`backend-api-generator`技能生成的后端API结构无缝配合。确保后端端点遵循RESTful约定以实现最佳集成。