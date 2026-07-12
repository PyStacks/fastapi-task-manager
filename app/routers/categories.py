from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.schemas import CategoryResponse, CategoryCreate, CategoryUpdate
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Category
from app.auth import get_current_user


router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[CategoryResponse])
def get_categories(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    获取当前用户的所有分类
    :param db:
    :param current_user:
    :return:
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
    :param category_data: 
    :param db: 
    :param current_user: 
    :return: 
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
    :param category_id: 
    :param category_data: 
    :param db: 
    :param current_user: 
    :return: 
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
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(category)
    db.commit()