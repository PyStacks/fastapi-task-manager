from app.database import SessionLocal, init_db
from app.models import User, Tasks
from sqlalchemy.orm import joinedload

init_db()
db = SessionLocal()

# 实验1：普通查询
user = db.query(User).filter(User.id == 1).first()
print(f"用户对象:{user}")
print(f"此时还没有查询tasks")

# 实验2：访问关联属性触发懒加载
print("\n=== 实验2：访问user.tasks ===")
print(f"用户的tasks:{user.tasks}")
print("注意：上面这行才真正执行了SQL查询")

# 实验3：N+1问题演示
print("\n=== 实验3：N+1问题 ===")
users = db.query(User).limit(3).all()
for u in users:
    print(f"{u.username}有{len(u.tasks)}条任务")

# 解决方案：预加载
print("\n=== 解决方案：joinedload ===")
users = db.query(User).options(joinedload(User.tasks)).limit(3).all()
for u in users:
    print(f"{u.username} 有 {len(u.tasks)} 个任务")  # 0条额外SQL