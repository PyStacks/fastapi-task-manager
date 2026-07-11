from sqlite_model import Tasks, init_db, SessionLocal

# 初始化数据库（如果表不存在则创建）
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 测试CRUD操作
def test_crud():
    db = SessionLocal()

    try:
        print("\n📝 创建任务...")
        task1 = Tasks(name="学习SQLAlchemy", description="掌握ORM基础", priority=5)
        task2 = Tasks(name="写周报", priority=3)
        task3 = Tasks(name="复习FastAPI", done=True)

        db.add(task1)
        db.add_all([task2, task3])
        db.commit()

        db.refresh(task1)
        print(f"任务1创建成功：{task1}")

        print("\n🔍 查询所有任务:")
        all_tasks = db.query(Tasks).all()
        for task in all_tasks:
            print(f"任务列表：{task}")

        print("\n🔍 查询未完成的任务:")
        undone2 = db.query(Tasks).filter(Tasks.done==False).all()
        for task in undone2:
            print(f"未完成的任务2：{task}")

        print("\n🔍 查询优先级>=4的任务:")
        high_priority = db.query(Tasks).filter(Tasks.priority>=4).all()
        for task in high_priority:
            print(f"{task}")

        # 获取单个任务
        first_task = db.query(Tasks).first()
        print(f"第一个任务：{first_task}")

        # ========== UPDATE 更新 ==========
        print("\n✏️ 更新第一个任务...")
        task_to_update = db.query(Tasks).filter(Tasks.id == task1.id).first()
        if task_to_update:
            task_to_update.title = "修改任务标题"
            task_to_update.done = True
            task_to_update.priority = 5
            db.commit()
            db.refresh(task_to_update)
            print(f"更新后的任务：{task_to_update}")

        print("\n🗑️ 删除第三个任务...")
        task_to_delete = db.query(Tasks).filter(Tasks.id == task3.id).first()
        if task_to_delete:
            db.delete(task_to_delete)
            db.commit()
            print(f"已删除{task_to_delete}")

        remaining = db.query(Tasks).count()
        print(f"共有{remaining}条任务")
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    test_crud()