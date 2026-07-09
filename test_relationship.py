from sqlite_demo import description
from sqlite_model import SessionLocal, init_db, User, Tasks

import os

if os.path.exists("database.db"):
    os.remove("database.db")
    print("旧数据库已删除")

init_db()

db = SessionLocal()

user1 = User(username="zhangsan", email="zs@qq.com", hashed_password="123456789")
user2 = User(username="lisi", email="lisi@qq.com", hashed_password="1234567")

db.add_all([user1, user2])
db.commit()

task1 = Tasks(name="任务1", description="任务描述1", priority=1, owner_id=user1.id)
task2 = Tasks(name="任务2",description="任务描述2", priority=2, owner_id=user1.id)
task3 = Tasks(name="任务3",description="任务描述3", priority=3, owner_id=user2.id)
db.add_all([task1, task2, task3])
db.commit()

# 通过用户查询任务
user = db.query(User).filter(User.username == "zhangsan").first()
print(f"用户名:{user.username}")
print(f"用户拥有的任务:{user.tasks}")

task = db.query(Tasks).filter(Tasks.name == '任务1').first()
print(f"任务:{task.name}")
print(f"任务属于:{task.owner.username}")

db.close()
