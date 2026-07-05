from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 定义tasks模型
class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
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
    init_db()