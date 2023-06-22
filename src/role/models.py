from typing import List

from sqlalchemy import Column, Integer, String

from src.models import Base


class Role(Base):
    __tablename__ = "role"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String, nullable=False, index=True)
    permissions: List = Column(List, default=[], nullable=False)
