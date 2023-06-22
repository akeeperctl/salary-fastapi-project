from sqlalchemy import Column, Integer, String

from src.models import Base


class Job(Base):
    __tablename__ = "job"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    salary: int = Column(Integer, index=True, nullable=False, default=15000)
    title: str = Column(String, index=True, unique=True, nullable=False)
    description: str = Column(String, nullable=True)
