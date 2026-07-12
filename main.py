from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.auth import verify_password, create_access_token
from app.models import User
from app.database import get_db, init_db
from app.routers import users, tasks, categories

app = FastAPI(
    title="任务管理系统API",
    description="FastAPI + SQLAlchemy + JWT认证",
    version="2.0.0"
)

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(categories.router)

# 启动时创建表
init_db()

@app.get("/")
def read_root():
    return {"msg": "欢迎进入任务管理系统！", "docs": "/docs"}

# =========登录接口==========
@app.post("/login", tags=["auth"])
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """
    用户登录
    -使用OAuth2表单格式（username和password字段）
    :param form_data:
    :param db:
    :return:
    """
    # 查找用户
    user = db.query(User).filter(User.username==form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}