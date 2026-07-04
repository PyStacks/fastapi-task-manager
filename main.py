from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

app = FastAPI(
    title="My FastAPI App",
    description="My FastAPI App",
    version="0.0.1",
)

task_counter = 4

class TaskCreate(BaseModel):
    """创建任务时的请求模型"""
    title: str = Field(...,min_length=1, max_length=100, description="任务标题")
    description: Optional[str] = Field(None, max_length=500, description="任务描述")
    priority: int = Field(3, ge=1, le=5, description="优先级")

    model_config = {
        "json_schema_extra":{
            "examples":[
                {
                    "title": "第一周的任务，完成fastapi基础知识学习",
                    "description": "包括查询参数、路径参数、pydantic模型",
                    "priority": 3,
                }
            ]
        }
    }

class TaskUpdate(BaseModel):
    """任务修改模型"""
    title: str = Field(None, min_length=1, max_length=100, description="任务标题")
    description: Optional[str] = Field(None, max_length=500, description="任务描述")
    priority: int = Field(None, ge=1, le=5, description='优先级')
    done: Optional[bool] = None


class Task(BaseModel):
    """完整的任务模型"""
    id: int
    title: str
    description: Optional[str] = None
    priority: int
    done: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

tasks_db = {
    1: {"id": 1, "description": "获取单个任务，开始行动", "done": False,"created_at": datetime.now(timezone.utc)},
    2: {"id": 2, "description": "学习使用路径参数和查询参数", "done": False,"created_at": datetime.now(timezone.utc)},
    3: {"id": 3, "description": "批量获取多个任务", "done": True,"created_at": datetime.now(timezone.utc)}
}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"stats": "ok"}


# 根据ID获取单个任务 - 路径参数
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]

# 获取任务列表 - 查询参数
@app.get("/tasks")
def get_tasks(skip: int = 0, limit: int = 2, done: bool = None):
    tasks = list(tasks_db.values())

    if done is not None:
        tasks = [task for task in tasks if task["done"] == done]

    # 返回指定区间内的任务
    return tasks[skip:skip + limit]

@app.get("/users/{user_id}/tasks")
def get_user_tasks(user_id: int,  done: bool = None, priority: str = "all"):
    """
        获取某用户的任务 - 路径参数+查询参数混合
        这是实际开发中最常见的写法
    """
    return {
        "user_id": user_id,
        "filters": {"done": done, "priority": priority},
        "tasks": []  # 暂时返回空
    }

@app.post("/tasks", response_model=Task, status_code=200)
def create_task(task: TaskCreate):
    """
        创建新任务
       -请求体需要符合TaskCreate模型
       -返回完整的Task对象（包含自动生成的ID）
    :param task:
    :return:
    """
    global task_counter

    new_task = Task(
        id=task_counter,
        title=task.title,
        description=task.description,
        priority=task.priority,
        done=False
    )

    tasks_db[task_counter] = new_task.model_dump()
    task_counter += 1
    return new_task


# patch 增量局部更新， put 全量更新 标准语义
@app.patch("/tasks/{task_id}", response_model=Task, status_code=200)
def update_task(task_id: int, task_update: TaskUpdate):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = tasks_db[task_id]
    # 只更新传入的字段（排除None）
    update_data = task_update.model_dump(exclude_unset=True)
    task_data.update(update_data)

    return task_data

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    # 204响应不返回任何内容
    del tasks_db[task_id]