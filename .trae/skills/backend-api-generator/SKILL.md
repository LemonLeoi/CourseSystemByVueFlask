---
name: "backend-api-generator"
description: "为学校管理系统生成Flask API路由和数据库模型。当为新实体创建后端API端点或扩展现有端点时调用。"
---

# 后端API生成器

此技能为学校管理系统项目生成Flask API路由、数据库模型和相关文件。它创建具有适当错误处理的RESTful API端点，并遵循项目现有的目录结构和编码规范。

## 功能特性

- 生成带有RESTful端点的Flask API蓝图
- 创建具有适当关系的SQLAlchemy数据库模型
- 包含错误处理和响应格式化
- 遵循项目现有的目录结构
- 为API端点生成测试文件
- 支持常见的字段类型和关系

## 使用方法

### 基本使用

要为新实体生成API端点和数据库模型：

1. 指定实体名称（例如："Classroom"）
2. 定义实体的字段，包括类型和关系
3. 指定API端点前缀（例如："/api/classrooms"）
4. 选择其他功能（认证、分页等）

### 生成的文件

该技能将生成以下文件：

- **API路由**：`app/api/{entity}_routes.py`
- **数据库模型**：`app/models/{entity}.py`
- **测试文件**：`tests/test_{entity}_api.py`
- **蓝图注册**：更新 `app.py` 以注册蓝图

### 示例

对于"Classroom"实体：

```python
# 生成的数据库模型 (classroom.py)
from app import db

class Classroom(db.Model):
    __tablename__ = 'classrooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    
    # 关系
    # ...

# 生成的API路由 (classroom_routes.py)
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

### 实体配置

- **实体名称**：实体的单数名称（例如："Classroom"）
- **复数名称**：用于命名一致性的复数形式（例如："Classrooms"）
- **API端点前缀**：API路由的前缀（例如："/api/classrooms"）

### 字段配置

对于每个字段，指定：

- **名称**：字段名称（例如："name"）
- **类型**：字段类型（例如："String"、"Integer"、"Boolean"）
- **可为空**：字段是否可以为null
- **默认值**：可选的默认值
- **唯一**：字段值是否必须唯一
- **关系**：与其他实体的可选关系

### 关系类型

- **一对一**：此实体中的一条记录与另一个实体中的一条记录相关
- **一对多**：此实体中的一条记录与另一个实体中的多条记录相关
- **多对多**：此实体中的多条记录与另一个实体中的多条记录相关

### 功能选项

- **认证**：启用/禁用API端点的认证
- **分页**：启用/禁用GET请求的分页
- **验证**：启用/禁用请求体验证
- **错误处理**：启用/禁用标准化错误处理
- **测试**：为API端点生成测试文件

## 最佳实践

1. **遵循RESTful约定**：使用适当的HTTP方法和状态码
2. **数据库设计**：规范化数据库模式并使用适当的字段类型
3. **错误处理**：返回具有适当状态码的一致错误响应
4. **验证**：在处理前验证所有用户输入
5. **文档**：为API端点和模型包含文档字符串
6. **测试**：为API端点编写全面的测试

## 故障排除

### 常见问题

- **数据库迁移错误**：检查模型定义和关系
- **API路由冲突**：确保端点路径唯一
- **导入错误**：验证模块导入和循环依赖
- **认证问题**：检查认证中间件配置
- **CORS错误**：确保为API端点正确配置了CORS

### 解决步骤

1. 验证生成的文件是否匹配项目结构
2. 检查生成代码中的语法错误
3. 使用Postman或类似工具测试API端点
4. 确保数据库迁移已正确应用
5. 验证跨域请求的CORS配置

## 与前端集成

此技能与`frontend-crud-generator`技能生成的前端CRUD页面无缝配合。确保前端API调用与生成的后端端点匹配，以实现最佳集成。