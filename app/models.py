from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

# User模型
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
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

    # 外键，关联users表
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    # 建立与User的关系
    owner = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, priority={self.priority}, done={self.done})>"

# 定义分类模型
class Category(Base):

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    color = Column(String(7), default="#808080")
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User")
    tasks = relationship("Tasks", back_populates="category")
