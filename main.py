from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Query, Body, Depends
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
from models import Task, TaskUpdate, TaskCreate, TaskFullUpdate, utc_now
from sqlite_model import SessionLocal, init_db, Tasks
import os

app = FastAPI(
    title="任务管理系统API",
    description="基于FastAPI + Pydantic实现的任务CRUD接口，区分PATCH局部更新/PUT全量更新",
    version="0.0.1",
)
if os.path.exists("database.db"):
    os.remove("database.db")
    print("旧数据库已删除")

# 启动时创建表
init_db()

# 获取会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# task_counter = 4

# tasks_db = {
#     1: {"id": 1, "name":"第一天学习任务", "description": "获取单个任务，开始行动","priority":3, "done": False,"created_at": utc_now(),"updated_at": None},
#     2: {"id": 2, "name":"第二天学习任务","description": "学习使用路径参数和查询参数","priority":3, "done": False,"created_at": utc_now(), "updated_at": None},
#     3: {"id": 3, "name":"第三天学习任务", "description": "批量获取多个任务", "priority":3, "done": True,"created_at": utc_now(), "updated_at": None}
# }

# def get_next_task_id() -> int:
#     global task_counter
#     current_task_id = task_counter
#     task_counter += 1
#     return current_task_id

@app.get("/")
def read_root():
    return {"msg": "欢迎进入任务管理系统！", "docs": "/docs"}

# -------------------------- 查询接口 --------------------------
@app.get("/tasks/search", response_model=List[Task], status_code=status.HTTP_200_OK)
def search_task(name: str, db: Session = Depends(get_db)):
    """
    模糊搜索接口，根据名称进行查询
    :param name:  任务名称
    :param db:  会话
    :return:  任务列表
    """
    stmt = select(Tasks).where(Tasks.name.like(f"%{name}%"))
    result = db.execute(stmt).scalars().all()

    return result


@app.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    根据任务ID查询单条任务详情
    :param task_id: 任务id
    :param db: 会话
    :return: 任务
    """
    #stmt = select(Tasks).where(Tasks.id == task_id)
    #result = db.execute(stmt).scalar_one_or_none()
    task = db.get(Tasks, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@app.get("/tasks", response_model=List[Task], status_code=status.HTTP_200_OK)
def get_tasks(
        skip: int = Query(0, ge=0, description="跳过条数"),
        limit: int = Query(2, ge=1, le=20, description="每页最大20条"),
        done: Optional[bool] = Query(None, description="根据状态进行筛选"),
        priority: Optional[int] = Query(None, description="优先级筛选"),
        db: Session = Depends(get_db)
):
    """
    分页查询任务列表，支持状态、优先级过滤
    :param skip: 跳过条数
    :param limit: 每页最大20条
    :param done: 状态
    :param priority: 优先级
    :param db: 会话
    :return: 任务列表
    """
    stmt = select(Tasks)
    if done is not None:
        stmt = stmt.where(Tasks.done == done)
    if priority is not None:
        stmt = stmt.where(Tasks.priority == priority)

    stmt = stmt.offset(skip).limit(limit)
    result = db.execute(stmt).scalars().all()

    # 返回指定区间内的任务
    return result

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
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """
    创建任务
    :param task: 任务创建模型
    :param db: 会话
    :return: orm实例
    """

    # new_id = get_next_task_id()

    new_task = Tasks(**task.model_dump(),done=False)
    # tasks_db[new_id] = new_task.model_dump()
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # db.execute()
    # insert_data = task.model_dump()
    # insert_data['done'] = False
    # stmt = insert(Tasks).values(**insert_data)
    # result = db.execute(stmt)
    # db.commit()
    # task_id = result.inserted_primary_key[0]
    # new_task = db.get(Tasks, task_id)

    return new_task

@app.post("/tasks/batch", response_model=List[Task], status_code=status.HTTP_201_CREATED)
def batch_create_task(
        tasks: List[TaskCreate] = Body(..., max_length=10, description="单次最多批量创建10条任务"),
        db: Session = Depends(get_db)
    ):
    """
    批量创建多条任务
    :param tasks: 创建任务模型列表
    :param db:  会话
    :return: 任务模型列表
    """
    try:
        # 通过db.execute()方法
        # insert_data_list = []
        # new_tasks = []
        # for task in tasks:
        #     data  = task.model_dump()
        #     data["done"] = False  # 补充默认状态
        #     insert_data_list.append(data)
        #
        # stmt = insert(Tasks).values(insert_data_list)
        # results = db.execute(stmt)
        # db.commit()

        orm_list = []
        for item in tasks:
            obj = Tasks(**item.model_dump(),done=False)
            orm_list.append(obj)
        db.add_all(orm_list)
        db.commit()

        for orm in orm_list:
            db.refresh(orm)

        return orm_list
    except Exception as e:
        db.rollback()
        raise

# -------------------------- 更新接口 --------------------------
# patch 增量局部更新， put 全量更新 标准语义
@app.patch("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """
    局部更新任务（PATCH标准语义，仅更新传入字段）
    - 不传的字段保持原有值
    - 自动刷新updated_at更新时间
    :param task_id: 任务ID
    :param task_update: 任务修改模型对象
    :param db: 会话
    :return: 任务对象
    """

    # if task_id not in tasks_db:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    # task_data = tasks_db[task_id]
    # # 只更新传入的字段（排除None）
    # update_data = task_update.model_dump(exclude_unset=True)
    # task_data.update(update_data)
    # task_data['updated_at'] = utc_now()
    try:
        target_task = db.get(Tasks, task_id)
        if not target_task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        update_data = task_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="未传入数据")
        update_data["updated_at"] = utc_now()
        stmt = update(Tasks).where(Tasks.id==task_id).values(**update_data)

        db.execute(stmt)

        # for k, v in update_data.items():
        #     setattr(target_task, k, v)
        # target_task.updated_at = utc_now()

        db.commit()
        # db.refresh(target_task)
        new_task = db.get(Tasks, task_id)

        return new_task
    except Exception as e:
        db.rollback()
        raise e


@app.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_full_task(task_id: int, full_task: TaskFullUpdate, db: Session = Depends(get_db)):
    """
    PUT 全量覆盖更新（标准REST语义）
    前端必须传入所有必填字段，缺失字段会被清空；仅保留原有ID、创建时间
    :param task_id:
    :param full_task:
    :param db:
    :return:
    """
    try:
        task = db.get(Tasks, task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        full_task_update = full_task.model_dump()
        if not full_task_update:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="未传入数据")

        forbidden_fields = {"id", "created_at"}
        for field in forbidden_fields:
            if field in full_task_update:
                del full_task_update[field]

        full_task_update["updated_at"] = utc_now()
        stmt = update(Tasks).where(Tasks.id==task_id).values(**full_task_update)
        db.execute(stmt)

        db.commit()

        new_task = db.get(Tasks, task_id)
        return new_task
    except Exception as e:
        db.rollback()
        raise e
    # if task_id not in tasks_db:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    #
    # full_dict = full_task.model_dump()
    # full_dict['id'] = task_id
    # full_dict['updated_at'] = utc_now()
    # full_dict['created_at'] = tasks_db[task_id]['created_at']
    #
    # tasks_db[task_id] = full_dict
    # return tasks_db[task_id]

# -------------------------- 删除接口 --------------------------
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # if task_id not in tasks_db:
    #     raise HTTPException(status_code=404, detail="Task not found")
    # # 204响应不返回任何内容
    # del tasks_db[task_id]
    try:
        stmt = delete(Tasks).where(Tasks.id==task_id)
        result = db.execute(stmt)
        db.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    except Exception as e:
        db.rollback()
        raise e


    # task = db.get(Tasks, task_id)
    # if not task:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    # db.delete(task)
    # db.commit()

