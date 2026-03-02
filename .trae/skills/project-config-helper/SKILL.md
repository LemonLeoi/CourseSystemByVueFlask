---
name: "project-config-helper"
description: "简化项目配置和环境设置，包括依赖安装、开发环境配置和项目结构管理。当需要快速搭建开发环境或配置项目设置时调用。"
---

# 项目配置助手

此技能帮助简化学校管理系统项目的开发环境配置和项目设置，减少重复的配置工作，提高开发效率。

## 功能特性

- 开发环境搭建：自动生成开发环境配置文件
- 依赖管理：统一管理项目依赖版本
- 项目结构：生成符合项目风格的目录结构
- 配置文件生成：为不同环境生成配置文件

## 使用方法

### 配置开发环境

1. 确保已安装Python 3.10+
2. 确保已安装Node.js 16+

### 配置步骤

1. 选择配置类型：
   - 前端开发环境配置
   - 后端开发环境配置
   - 全栈环境配置

2. 选择具体环境：
   - 开发环境
   - 测试环境
   - 生产环境

3. 配置详细信息：
   - 数据库类型：SQLite / MySQL / PostgreSQL
   - 端口配置
   - 依赖管理

## 配置文件生成

根据选择的环境类型，自动生成对应配置文件：

### 前端配置文件

```bash
# 前端开发环境配置
# 生成vite.config.js
# 生成package.json
```

### 后端配置文件

```bash
# 后端开发环境配置
# 生成requirements.txt
# 数据库配置
```

## 项目结构

```
project-root/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   └── stores/
│   ├── public/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   └── services/
│   ├── main.py
│   ├── requirements.txt
│   └── config.py
└── README.md
```

## 配置流程

1. 选择配置类型
2. 填写配置信息
3. 生成配置文件
4. 验证配置结果

## 注意事项

- 确保路径正确
- 环境变量配置正确
- 依赖版本兼容

## 故障排除

- 路径错误：检查配置路径是否正确
- 依赖冲突：解决依赖版本冲突
- 权限问题：确保有足够权限

## 示例

### 前端环境配置

```bash
# 安装前端依赖
cd frontend
npm install

# 启动开发服务器
npm run dev
```

### 后端环境配置

```bash
# 安装后端依赖
cd backend
pip install -r requirements.txt

# 启动后端服务
python app.py
```

## 总结

此技能可显著简化项目配置流程，减少重复工作，提高开发效率，让开发者专注于业务逻辑实现而非环境配置。