from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, TIMESTAMP

from src.job.models import Job
from src.role.models import Role
from src.models import Base


class UserEmployee(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "employee"

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    # Может содержать: Уборщик, программист и т.д
    job_id: int = Column(Integer, ForeignKey(Job.id), index=True, nullable=False)

    # Может содержать: Админ, пользователь и т.д
    # role_id: int = Column(Integer, ForeignKey(Role.id), index=True, nullable=False)

    username: str = Column(String, index=True, nullable=False)
    firstname: str = Column(String, index=True, nullable=False)
    lastname: str = Column(String, index=True, nullable=False)

    signed_at_utc: datetime = Column(TIMESTAMP, index=True, nullable=True)
    last_promotion_utc: datetime = Column(TIMESTAMP, nullable=True)
    next_promotion_utc: datetime = Column(TIMESTAMP, nullable=True)

    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
