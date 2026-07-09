from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, MetaData, select, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship


SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

# 获取引擎，check_same_thread针对SQLite专属参数
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

# session工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

global_metadata = MetaData()

# 创建基类
class Base(DeclarativeBase):
    metadata = global_metadata


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    # 建立与Task的关系
    tasks = relationship("Tasks", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

# 定义tasks模型
class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    priority = Column(Integer, default=3)
    done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime)

    # 外键，关联users表
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    # 建立与User的关系
    owner = relationship("User", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, priority={self.priority}, done={self.done})>"

# 初始化
def init_db():
    Base.metadata.create_all(engine)
    print('数据库初始化成功')

# if __name__ == '__main__':
#     try:
#         db = SessionLocal()
#         stmt = select(Tasks).where(Tasks.done==False)
#         result = db.execute(stmt).all()
#         result1 = db.execute(stmt).scalars().all()
#         print(f"result1: {result1}")
#         print(f"result2: {result}")
#     finally:
#         db.close()
