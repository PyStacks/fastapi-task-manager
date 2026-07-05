from typing import List, Optional, Literal
from fastapi import FastAPI, HTTPException, status, Query, Body
from models import Task, TaskUpdate, TaskCreate, TaskFullUpdate, utc_now

app = FastAPI(
    title="任务管理系统API",
    description="基于FastAPI + Pydantic实现的任务CRUD接口，区分PATCH局部更新/PUT全量更新",
    version="0.0.1",
)

task_counter = 4

tasks_db = {
    1: {"id": 1, "name":"第一天学习任务", "description": "获取单个任务，开始行动","priority":3, "done": False,"created_at": utc_now(),"updated_at": None},
    2: {"id": 2, "name":"第二天学习任务","description": "学习使用路径参数和查询参数","priority":3, "done": False,"created_at": utc_now(), "updated_at": None},
    3: {"id": 3, "name":"第三天学习任务", "description": "批量获取多个任务", "priority":3, "done": True,"created_at": utc_now(), "updated_at": None}
}

def get_next_task_id() -> int:
    global task_counter
    current_task_id = task_counter
    task_counter += 1
    return current_task_id

@app.get("/")
def read_root():
    return {"msg": "欢迎进入任务管理系统！", "docs": "/docs"}

# -------------------------- 查询接口 --------------------------
@app.get("/tasks/search", response_model=List[Task], status_code=status.HTTP_200_OK)
def search_task(name: str):
    """
    模糊搜索接口，根据名称进行查询
    :param name:  任务名称
    :return:  任务列表
    """
    tasks = [task for task in tasks_db.values() if name.lower() in task['name'].lower()]
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return tasks


@app.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    """
    根据任务ID查询单条任务详情
    :param task_id: 任务id
    :return: 任务
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return tasks_db[task_id]


@app.get("/tasks", response_model=List[Task], status_code=status.HTTP_200_OK)
def get_tasks(
        skip: int = Query(0, ge=0, description="跳过条数"),
        limit: int = Query(2, ge=1, le=20, description="每页最大20条"),
        done: Optional[bool] = Query(None, description="根据状态进行筛选"),
        priority: Optional[Literal[1,2,3,4,5]] = Query(None, description="根据优先级进行筛选")
):
    """
    分页查询任务列表，支持状态、优先级过滤
    :param skip: 跳过条数
    :param limit: 每页最大20条
    :param done: 状态
    :param priority: 优先级
    :return: 任务列表
    """
    tasks = list(tasks_db.values())

    if done is not None:
        tasks = [task for task in tasks if task["done"] == done]
    if priority is not None:
        tasks = [task for task in tasks if task["priority"] == priority]

    # 返回指定区间内的任务
    return tasks[skip:skip + limit]

@app.get("/users/{user_id}/tasks", status_code=status.HTTP_200_OK)
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

# -------------------------- 创建接口 --------------------------
@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    """
        创建新任务
       -请求体需要符合TaskCreate模型
       -返回完整的Task对象（包含自动生成的ID）
    :param task:
    :return:
    """
    new_id = get_next_task_id()

    new_task = Task(
        id=new_id,
        name=task.name,
        description=task.description,
        priority=task.priority,
        done=False
    )

    tasks_db[new_id] = new_task.model_dump()
    return new_task

@app.post("/tasks/batch", response_model=List[Task], status_code=status.HTTP_201_CREATED)
def batch_create_task(tasks: List[TaskCreate] = Body(..., max_length=10, description="单次最多批量创建10条任务")):
    """批量创建多条任务"""
    new_tasks = []
    for task in tasks:
        new_task = create_task(task)
        new_tasks.append(new_task)
    return new_tasks

# -------------------------- 更新接口 --------------------------
# patch 增量局部更新， put 全量更新 标准语义
@app.patch("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_update: TaskUpdate):
    """
    局部更新任务（PATCH标准语义，仅更新传入字段）
    - 不传的字段保持原有值
    - 自动刷新updated_at更新时间
    :param task_id: 任务ID
    :param task_update: 任务修改模型对象
    :return: 任务对象
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task_data = tasks_db[task_id]
    # 只更新传入的字段（排除None）
    update_data = task_update.model_dump(exclude_unset=True)
    task_data.update(update_data)
    task_data['updated_at'] = utc_now()

    return task_data

@app.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_full_task(task_id: int, full_task: TaskFullUpdate):
    """
    PUT 全量覆盖更新（标准REST语义）
    前端必须传入所有必填字段，缺失字段会被清空；仅保留原有ID、创建时间
    :param task_id:
    :param full_task:
    :return:
    """
    if task_id not in tasks_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    full_dict = full_task.model_dump()
    full_dict['id'] = task_id
    full_dict['updated_at'] = utc_now()
    full_dict['created_at'] = tasks_db[task_id]['created_at']

    tasks_db[task_id] = full_dict
    return tasks_db[task_id]

# -------------------------- 删除接口 --------------------------
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    # 204响应不返回任何内容
    del tasks_db[task_id]


