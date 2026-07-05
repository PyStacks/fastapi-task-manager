# 任务管理系统 API

## 项目简介
这是我学习FastAPI的第一个项目，实现了任务的增删改查功能。

## 技术栈
- FastAPI 0.100+
- Python 3.10+
- Pydantic 2.0+
- Uvicorn

## 快速开始

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
pip install fastapi uvicorn
```

### 4. 运行服务
```bash
uvicorn main:app --reload
```

### 5. 访问文档
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /tasks | 获取任务列表（支持分页和筛选） |
| GET | /tasks/{id} | 获取单个任务 |
| POST | /tasks | 创建任务 |
| PUT | /tasks/{id} | 更新任务 |
| DELETE | /tasks/{id} | 删除任务 |
| GET | /tasks/search | 搜索任务 |
| POST | /tasks/batch | 批量创建 |

## 项目结构
```
.
├── main.py          # 主程序
├── models.py        # 数据模型（如有拆分）
├── docs/
│   └── postman_collection.json  # Postman测试集合
├── README.md
└── .gitignore
```

## 学习笔记
本周学习了：
- FastAPI路由（路径参数、查询参数）
- Pydantic数据验证
- HTTP状态码规范
- CRUD操作实现
