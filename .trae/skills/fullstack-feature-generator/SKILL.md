---
name: "fullstack-feature-generator"
description: "生成学校管理系统的完整全栈功能模块，包括前端Vue组件和后端Flask API端点。当创建需要前后端同时实现的新功能时调用。"
---

# 全栈功能生成器

此技能为学校管理系统项目生成完整的全栈功能模块，包括前端Vue组件和后端Flask API端点。通过生成一致的数据模型、API端点和前端组件，确保前后端之间的无缝集成。

## 功能特性

- 生成完整的前端Vue 3组件，支持TypeScript
- 创建后端Flask API路由和数据库模型
- 确保前后端之间的数据结构一致性
- 遵循项目现有的目录结构和编码规范
- 生成与数据库模型匹配的TypeScript接口
- 包含具有适当错误处理的API服务集成
- 支持实体之间的常见关系

## 使用方法

### 基本使用

要生成完整的全栈功能模块：

1. 指定功能名称（例如："教室管理"）
2. 定义实体字段，包括类型和关系
3. 指定API端点配置
4. 选择其他功能（认证、分页等）
5. 生成完整的功能模块

### 生成的文件

该技能将生成以下文件：

#### 前端文件

- **视图组件**：`src/views/{entity}/Manage{Entity}.vue`
- **类型定义**：`src/types/{entity}.ts`
- **Pinia状态管理**：`src/stores/{entity}s.ts`
- **API服务**：`src/services/{entity}Service.ts`
- **可组合函数**：`src/composables/{entity}/use{Entity}Manage.ts`
- **路由配置**：更新 `src/router/index.js`

#### 后端文件

- **API路由**：`app/api/{entity}_routes.py`
- **数据库模型**：`app/models/{entity}.py`
- **测试文件**：`tests/test_{entity}_api.py`
- **蓝图注册**：更新 `app.py`

### 示例

对于"教室管理"功能：

#### 前端文件

```typescript
// src/types/classroom.ts
export interface Classroom {
  id: number;
  name: string;
  capacity: number;
  location: string;
}

// src/services/classroomService.ts
import apiService from './apiService';

export const classroomService = {
  getAll: () => apiService.get('/api/classrooms'),
  getById: (id: number) => apiService.get(`/api/classrooms/${id}`),
  create: (classroom: Omit<Classroom, 'id'>) => apiService.post('/api/classrooms', classroom),
  update: (id: number, classroom: Partial<Classroom>) => apiService.put(`/api/classrooms/${id}`, classroom),
  delete: (id: number) => apiService.delete(`/api/classrooms/${id}`)
};
```

#### 后端文件

```python
# app/models/classroom.py
from app import db

class Classroom(db.Model):
    __tablename__ = 'classrooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200), nullable=False)

# app/api/classroom_routes.py
from flask import Blueprint, jsonify, request
from app.models.classroom import Classroom
from app import db

bp = Blueprint('classroom', __name__)

@bp.route('/', methods=['GET'])
def get_classrooms():
    classrooms = Classroom.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'capacity': c.capacity,
        'location': c.location
    } for c in classrooms])

# ... 其他CRUD端点
```

## 配置选项

### 功能配置

- **功能名称**：功能的名称（例如："教室管理"）
- **实体名称**：实体的单数名称（例如："Classroom"）
- **复数名称**：用于命名一致性的复数形式（例如："Classrooms"）
- **API端点前缀**：API路由的前缀（例如："/api/classrooms"）
- **前端路由**：前端导航的路由（例如："/classrooms"）

### 字段配置

对于每个字段，指定：

- **名称**：字段名称（例如："name"）
- **类型**：字段类型（例如："string"、"number"、"boolean"）
- **标签**：前端显示标签（例如："教室名称"）
- **必填**：字段是否必填
- **验证**：可选的验证规则
- **后端类型**：对应的数据库字段类型
- **关系**：与其他实体的可选关系

### 关系配置

- **类型**：一对一、一对多或多对多
- **目标实体**：此关系指向的实体
- **级联选项**：在删除/更新时如何处理相关记录

### 功能选项

#### 前端选项

- **搜索**：启用/禁用搜索功能
- **分页**：启用/禁用分页
- **排序**：启用/禁用列排序
- **过滤**：启用/禁用高级过滤
- **表单验证**：启用/禁用表单验证

#### 后端选项

- **认证**：启用/禁用API端点的认证
- **分页**：启用/禁用GET请求的分页
- **验证**：启用/禁用请求体验证
- **错误处理**：启用/禁用标准化错误处理
- **测试**：为API端点生成测试文件

## 最佳实践

1. **一致命名**：在前后端使用一致的命名约定
2. **数据模型同步**：确保前端接口与后端模型匹配
3. **API设计**：遵循RESTful约定设计API端点
4. **错误处理**：在前后端实现一致的错误处理
5. **验证**：在前后端都验证数据
6. **类型安全**：在前端使用TypeScript接口确保类型安全
7. **测试**：为前后端编写全面的测试

## 故障排除

### 常见问题

- **数据模型不匹配**：确保前端接口与后端模型匹配
- **API端点不一致**：验证API路由与前端服务调用匹配
- **关系配置错误**：检查前后端的关系定义
- **路由配置问题**：确保前端路由已正确注册
- **CORS配置**：验证API端点已启用CORS

### 解决步骤

1. 验证生成的文件是否匹配项目结构
2. 检查前端的TypeScript编译错误
3. 使用Postman或类似工具测试API端点
4. 确保数据库迁移已正确应用
5. 验证前端表单提交和API调用
6. 测试完整的端到端功能

## 与现有功能集成

此技能与项目中的现有功能无缝集成。生成新功能时，它会：

- 尊重现有的数据库模型和关系
- 更新路由配置而不破坏现有路由
- 遵循与现有文件相同的编码约定
- 与现有的认证和错误处理系统集成

## 结论

全栈功能生成器为学校管理系统创建完整功能模块提供了全面的解决方案。通过生成一致的前后端代码，它减少了开发时间，最小化了错误，并确保了无缝的用户体验。