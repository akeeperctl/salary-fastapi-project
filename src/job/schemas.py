from typing import Optional

from pydantic import BaseModel, Field


class JobRead(BaseModel):
    id: Optional[int]
    salary: Optional[int]
    title: Optional[str]
    description: Optional[str]


class JobCreate(BaseModel):
    salary: int = Field(ge=15000)
    title: str = Field(min_length=4, max_length=15)
    description: str = Field(max_length=64)


class JobUpdate(BaseModel):
    salary: Optional[int] = Field(ge=15000)
    title: Optional[str]
    description: Optional[str]
