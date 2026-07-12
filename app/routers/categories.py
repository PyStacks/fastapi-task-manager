# 1. 标准库
from typing import List

# 2. 第三方库（fastapi 在前，sqlalchemy在后，字母排序）
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import exists
from sqlalchemy.orm import Session

# 3. 本地项目导入（按app下路径字母排序）
from app.auth import get_current_user
from app.database import get_db
from app.models import Category, Tasks, User
from app.schemas import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["分类管理"])

@router.get("/", response_model=List[CategoryResponse])
def get_categories(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的所有分类
    :param db: 会话
    :param current_user: 当前用户
    :return: 分类列表
    """
    categories = db.query(Category).filter(Category.user_id == current_user.id).all()
    return categories

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
        category_data: CategoryCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    创建分类
    :param category_data: 传入的分类数据
    :param db: 会话
    :param current_user: 当前用户
    :return: 创建成功的分类数据
    """
    # 检查分类是否存在
    exist_category = db.query(Category).filter(
        Category.name == category_data.name,
        Category.user_id == current_user.id
    ).first()
    if exist_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists")

    new_category = Category(
        name=category_data.name,
        color=category_data.color,
        user_id=current_user.id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

@router.put("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_category(
        category_id: int,
        category_data: CategoryUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    更新分类
    :param category_id: 分类id
    :param category_data: 分类数据
    :param db: 会话
    :param current_user: 会话
    :return: 修改后的分类数据
    """
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    update_dict = category_data.model_dump(exclude_unset=True)
    for k, v in update_dict.items():
        setattr(category, k, v)

    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
        category_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    删除分类，应该校验是否已经使用，只能删除未使用的分类
    :param category_id: 分类id
    :param db: 会话
    :param current_user: 当前用户
    :return: 无返回值 204
    """
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    has_used = db.query(
        exists().where(
            Tasks.category_id == category_id,
            Tasks.owner_id == current_user.id
        )
    ).scalar()

    if has_used:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="分类已被使用，无法删除")

    db.delete(category)
    db.commit()
    return