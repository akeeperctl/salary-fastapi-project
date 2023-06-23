from typing import AsyncGenerator, Any

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from pydantic import BaseModel
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import DB_USER, DB_PASS, DB_HOST, DB_NAME

from src.models import Base
from src.user_employee.models import UserEmployee

# DATABASE_URL = "postgresql://user:password@postgresserver/db"
# DATABASE_URL = f"postgresql+asyncpg://postgres:postgres@localhost/shift-project-db"
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserEmployee)


async def store_exact_data_from_db(base_model: Base | Any, base_read: BaseModel | Any, row_id: int,
                                   session: AsyncSession) -> dict:
    query = select(base_model).where(base_model.id == row_id)
    result = await session.execute(query)
    await session.commit()
    stored_model: base_read = result.scalar()
    stored_data: dict = jsonable_encoder(stored_model)

    return stored_data


async def store_data_from_db(base_model: Base | Any, base_read: BaseModel | Any,
                             limit: int, offset: int, session: AsyncSession) -> dict:
    query = select(base_model).limit(limit).offset(offset)
    result = await session.execute(query)
    await session.commit()
    stored_model: base_read = result.scalars().all()
    stored_data: dict = jsonable_encoder(stored_model)

    return stored_data
