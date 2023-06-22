from sqlalchemy import Column, Integer, String

from src.models import Base


class Job(Base):
    __tablename__ = "job"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String, nullable=False, index=True)
    description: str = Column(String, nullable=True)
