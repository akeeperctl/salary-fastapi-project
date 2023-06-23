import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.config import DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_NAME_TEST
from src.database import get_async_session
from src.main import app
from src.models import Base


class TestValueSaver:
    def __init__(self, values=None):
        if values is None:
            values = {}
        self.values = values


TEST_VALUE_SAVER = TestValueSaver()


DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}/{DB_NAME_TEST}"
engine_test: AsyncEngine = create_async_engine(DATABASE_URL_TEST)
async_session_maker_test = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)

# Связывание тестовых таблиц БД с имеющимися
Base.metadata.bind = engine_test


# Переписывание зависимостей
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker_test() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


# Фикстура подготовки базы данных перед тестом
@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# Настройка асинхронного клиента для тестов
@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    print("\n Call function event_loop...")
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
    print("\n Call function event_loop close")


@pytest.fixture(scope="session")
def is_super_user():
    return 1
