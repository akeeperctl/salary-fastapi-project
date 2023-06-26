from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, Field, BaseModel


class EmployeeSalaryRead(BaseModel):
    salary: Optional[int]
    last_promotion_utc: Optional[datetime]
    next_promotion_utc: Optional[datetime]


class UserEmployeeRead(schemas.BaseUser[int]):
    id: Optional[int]

    username: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]

    signed_at_utc: Optional[datetime]

    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]


class UserEmployeeReadAddon(schemas.BaseUser[int]):
    id: Optional[int]
    job_id: Optional[int]

    username: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]

    signed_at_utc: Optional[datetime]
    last_promotion_utc: Optional[datetime]
    next_promotion_utc: Optional[datetime]

    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]


class UserEmployeeCreate(schemas.BaseUserCreate):
    job_id: int = Field(default=1)

    username: str = Field(min_length=3, max_length=10)
    firstname: str = Field(min_length=3, max_length=15)
    lastname: str = Field(min_length=3, max_length=15)

    email: EmailStr
    password: str = Field(min_length=8)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserEmployeeUpdate(schemas.BaseUserUpdate):
    id: int
    job_id: Optional[int]

    username: Optional[str] = Field(min_length=3, max_length=10)
    firstname: Optional[str] = Field(min_length=3, max_length=15)
    lastname: Optional[str] = Field(min_length=3, max_length=15)

    signed_at_utc: Optional[datetime]
    last_promotion_utc: Optional[datetime]
    next_promotion_utc: Optional[datetime]

    email: Optional[EmailStr]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
