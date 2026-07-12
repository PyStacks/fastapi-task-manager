from sqlalchemy import create_engine, MetaData
from app.config import settings
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# 获取引擎，check_same_thread针对SQLite专属参数
engine = create_engine(settings.DATABASE_URL,
                       connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})

# session工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

global_metadata = MetaData()

# 创建基类
class Base(DeclarativeBase):
    metadata = global_metadata


# 获取会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 初始化
def init_db():
    Base.metadata.create_all(engine)
    print('数据库初始化成功')