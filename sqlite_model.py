from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declarative_base
from sqlalchemy import select


SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

# 获取引擎，check_same_thread针对SQLite专属参数
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

# session工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

global_metadata = MetaData()

# 创建基类
class Base(DeclarativeBase):
    metadata = global_metadata

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

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, priority={self.priority}, done={self.done})>"

# 初始化
def init_db():
    Base.metadata.create_all(engine)
    print('数据库初始化成功')

if __name__ == '__main__':
    try:
        db = SessionLocal()
        stmt = select(Tasks).where(Tasks.done==False)
        result = db.execute(stmt).all()
        result1 = db.execute(stmt).scalars().all()
        print(f"result1: {result1}")
        print(f"result2: {result}")
    finally:
        db.close()
