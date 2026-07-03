from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="My FastAPI App",
    description="My FastAPI App",
    version="0.0.1",
)

tasks_db = {
    1: {"id": 1, "desc": "获取单个任务，开始行动", "done": False},
    2: {"id": 2, "desc": "学习使用路径参数和查询参数", "done": False},
    3: {"id": 3, "desc": "批量获取多个任务", "done": True}
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