# 📝 任务管理系统 API

![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)

## 📖 项目简介

这是一个基于FastAPI开发的任务管理系统后端API，作为我从项目管理转Python开发的**第一个实战项目**。

### ✨ 核心功能
- ✅ 用户注册/登录（JWT认证）
- ✅ 任务的增删改查
- ✅ 任务分类管理
- ✅ 按状态/分类筛选任务
- ✅ 用户数据隔离（只能操作自己的数据）
    
## 🛠 技术栈

| 技术 | 用途 |
|------|------|
| FastAPI | Web框架 |
| SQLAlchemy | ORM数据库操作 |
| SQLite | 数据库（可轻松切换PostgreSQL） |
| Pydantic | 数据验证 |
| JWT (python-jose) | 用户认证 |
| Passlib (bcrypt) | 密码加密 |

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/fastapi-task-manager.git
cd fastapi-task-manager
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 运行服务
```bash
uvicorn main:app --reload
```

### 5. 访问文档
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API 端点
### 认证
| 方法     | 路径 | 说明 |
|--------|------|------|
| POST   | /users/register | 用户注册 |
| POST    | /login | 用户登录（返回JWT） |
| GET   | /users/me | 获取当前用户信息 |
### 任务管理
| 方法     | 路径 | 说明 |
|--------|------|------|
| GET   | /tasks | 获取任务列表（支持分页、状态筛选、分类筛选） |
| GET    | /tasks/{id} | 获取单个任务 |
| POST   | /tasks | 创建任务 |
| PUT   | /tasks/{id} | 更新任务 |
| DELETE   | /tasks/{id} | 删除任务 |
### 分类管理
| 方法     | 路径 | 说明 |
|--------|------|------|
| GET   | /categories | 获取分类列表 |
| POST    | /categories | 创建分类 |
| PUT   | /categories/{id} | 更新分类 |
| DELETE   | /categories/{id} | 删除分类 |
## 项目结构
```
app/
├── main.py           # 应用入口
├── database.py       # 数据库配置
├── models.py         # SQLAlchemy模型
├── schemas.py        # Pydantic模型
├── auth.py           # 认证工具
├── config.py         # 配置管理
└── routers/
    ├── users.py      # 用户路由
    ├── tasks.py      # 任务路由
    └── categories.py # 分类路由
```
## 🧪 测试账号
```
用户名: testuser
密码: test123456
```

## 📝 开发笔记
这个项目我学到了什么
- FastAPI框架：路由、依赖注入、自动文档生成
- SQLAlchemy ORM：模型定义、关系映射、CRUD操作
- 认证授权：JWT令牌生成与验证、bcrypt密码加密
- 工程规范：项目结构设计、Git分支管理、Conventional Commits
- 数据隔离：多用户场景下的权限控制设计

## 后续优化方向
- 添加单元测试（pytest）
- 切换到PostgreSQL数据库
- 添加Redis缓存
- Docker容器化部署

## 👤 作者
- 转行Python开发学习中
- 前项目管理背景，擅长需求分析和流程优化
