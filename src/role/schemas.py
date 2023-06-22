from typing import Optional, List

from pydantic import BaseModel, Field, Json
from sqlalchemy import JSON


class RoleCreate(BaseModel):
    title: str = Field(min_length=4, max_length=15)
    permissions: Json[List]


class RoleUpdate(BaseModel):
    id: int
    title: str
    permissions: Json[List]


class RoleRead(BaseModel):
    id: Optional[int]
    title: Optional[str]
    permissions: Optional[Json[List]]
