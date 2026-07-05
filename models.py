from typing import Optional, Literal
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict

# 公共类，统一获取UTC时间
def utc_now() -> datetime:
    return datetime.now(timezone.utc)

# 创建公共基础字段
class TaskBase(BaseModel):
    name: str = Field(None, min_length=1, max_length=100, description="任务名称")
    description: Optional[str] = Field(None, max_length=500, description="任务描述")
    priority: Literal[1,2,3,4,5] = Field(None, ge=1, le=5, description="任务优先级1-5")

# 任务模型
class Task(TaskBase):
    id: int
    created_at: datetime = Field(default_factory=utc_now, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    done: bool = Field(False, description="任务是否完成")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example":{
                "id": 1,
                "name": "学习pydantic模型",
                "description": "建立任务模型，增强对pydantic模型的认识与理解",
                "priority": 4,
                "done": False,
                "created_at": "2026-07-04T12:00:00Z",
                "updated_at": None
            }
        }
    )

# 任务创建模型（前端入参，不需要id、done、created_at）
class TaskCreate(TaskBase):
    name: str = Field(..., min_length=1, max_length=100, description="任务名称（必填）")
    priority: Literal[1,2,3,4,5] = Field(..., ge=1, le=5, description="任务优先级（必填）")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example":{
                "name": "学习建立任务创建模型",
                "description": "学习前端入参有些字段不需要带入，后端自动生成",
                "priority": 4,
            }
        }
    )


#  PATCH局部更新模型：所有字段可选，只传要修改的字段
class TaskUpdate(TaskBase):
    done: Optional[bool] = Field(None, description="任务完成状态")

# PUT全量更新模型，所有字段必填
class TaskFullUpdate(TaskBase):
    name: str = Field(..., min_length=1, max_length=100, description="任务名称")
    description: Optional[str] = Field(..., max_length=500, description="任务描述")
    priority: Literal[1,2,3,4,5] = Field(..., ge=1, le=5, description="任务优先级")
    done: bool = Field(..., description="任务完成状态")
