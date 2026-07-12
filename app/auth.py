from passlib.context import CryptContext
from datetime import  timedelta
from jose import JWTError, jwt
from typing import Optional
from utils.time_util import utc_now
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
import hashlib

# JWT配置
SECRET_KEY = '123456789'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2配置
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def _pre_hash(raw_pwd: str) -> str:
    # 任意长度密码统一压缩为固定256bit摘要，字节永远小于72
    return hashlib.sha256(raw_pwd.encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    :param plain_password:
    :param hashed_password:
    :return:
    """
    fixed_len_pwd = _pre_hash(plain_password)
    return pwd_context.verify(fixed_len_pwd, hashed_password)

def get_password_hash(password: str) -> str:
    """
    生成哈希密码
    :param password:
    :return:
    """
    print("待加密明文：", password, "字节长度：", len(password.encode("utf8")))
    fixed_len_pwd = _pre_hash(password)
    print(fixed_len_pwd)
    print(len(fixed_len_pwd.encode("utf8")))
    return pwd_context.hash(fixed_len_pwd)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    生成JWT令牌
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = utc_now() + expires_delta
    else:
        expire = utc_now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """
    验证JWT令牌
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    从token中解析当前用户
    :param token:
    :param db:
    :return:
    """
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="无效的认证凭据",
                            headers={"WWW-Authenticate": "Bearer"})
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="无效的token")

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="用户不存在")

    return user
