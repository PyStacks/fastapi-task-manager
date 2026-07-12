from app.models import User
from app.schemas import UserResponse, UserCreate
from app.database import get_db
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, status,Depends
from app.auth import get_password_hash, get_current_user


router = APIRouter(prefix="/users", tags=["用户管理"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册
    :param user_data:
    :param db:
    :return:
    """
    # 检查用户名是否存在
    stmt = select(User).where(User.username==user_data.username)
    existing_user = db.execute(stmt).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    existing_email = db.query(User).filter(User.email==user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    # 创建用户
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = get_password_hash(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: str, db: Session = Depends(get_db)):
    """
    获取单个用户
    :param user_id:
    :param db:
    :return:
    """
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user