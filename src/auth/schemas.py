from datetime import datetime, timedelta
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, Field


#utcnow = datetime.utcnow().isoformat(sep='_', timespec='minutes')
utcnow = datetime.utcnow()


class EmployeeRead(schemas.BaseUser[int]):

    id: Optional[int]
    job_id: Optional[int]
    role_id: Optional[int]

    username: Optional[str]
    firstname: Optional[str]
    lastname: Optional[str]

    signed_at: Optional[datetime]
    last_promotion: Optional[datetime]
    next_promotion: Optional[datetime]

    email: Optional[EmailStr]
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]


class EmployeeCreate(schemas.BaseUserCreate):
    # id: int = Field()

    job_id: int
    role_id: int

    username: str = Field(min_length=3, max_length=10)
    firstname: str = Field(min_length=3, max_length=15)
    lastname: str = Field(min_length=3, max_length=15)

    # signed_at: datetime = utcnow
    # last_promotion: datetime = utcnow
    # next_promotion: datetime = utcnow + timedelta(days=365)

    email: EmailStr
    password: str = Field(min_length=8)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    id: int
    job_id: Optional[int]
    role_id: Optional[int]

    username: Optional[str] = Field(min_length=3, max_length=10)
    firstname: Optional[str] = Field(min_length=3, max_length=15)
    lastname: Optional[str] = Field(min_length=3, max_length=15)

    signed_at: Optional[datetime]
    last_promotion: Optional[datetime]
    next_promotion: Optional[datetime]

    email: Optional[EmailStr]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
