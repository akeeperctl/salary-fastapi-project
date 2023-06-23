from typing import Optional, List

from pydantic import BaseModel, Field, Json
from sqlalchemy import JSON


class RoleCreate(BaseModel):
    title: str = Field(min_length=4, max_length=15)
    # permissions: List[str] = ["default"]


class RoleUpdate(BaseModel):
    title: Optional[str]
    # permissions: Optional[List[str]]


class RoleRead(BaseModel):
    id: Optional[int]
    title: Optional[str]
    # permissions: Optional[List[str]]
