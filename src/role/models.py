from sqlalchemy import Column, Integer, String, JSON

from src.models import Base


class Role(Base):
    __tablename__ = "role"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String, nullable=False, index=True, unique=True)
    # permissions = Column(JSON, nullable=False,
    #                      comment="example: [perm1, perm2, perm3]. All perm's is string")
