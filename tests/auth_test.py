from datetime import datetime, timedelta
from pprint import pprint

from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.job.models import Job
from src.job.schemas import JobRead
from tests.conftest import async_session_maker_test, TEST_VALUE_SAVER
from src.user_employee.models import UserEmployee
from src.user_employee.schemas import UserEmployeeRead

CREATED_JOB = {
    'salary': 70000,
    'title': "разработчик-молодец",
    'description': "Занимается разработкой и пинает молодых"
}
CREATED_USER = {
    'job_id': 0,
    'username': 'test_name',
    'firstname': 'test_first',
    'lastname': 'test_last',
    'email': 'test@example.com',
    'password': '123456789',
    'is_active': True,
    'is_superuser': False,
    'is_verified': False
}
CREATED_USER2 = {
    'job_id': 0,
    'username': 'abiba_boba',
    'firstname': 'test_first',
    'lastname': 'test_last',
    'email': 'biba@bobamail.com',
    'password': '123456789',
    'is_active': True,
    'is_superuser': False,
    'is_verified': False
}

ACCESS_TOKEN: str = ""


async def test_server_create_job():
    async with async_session_maker_test() as session:
        global CREATED_JOB

        session: AsyncSession = session

        stmt = insert(Job). \
            values(**CREATED_JOB)

        await session.execute(stmt)
        # await session.commit()

        query = select(Job).where(Job.title == CREATED_JOB["title"])
        result = await session.execute(query)
        await session.commit()

        stored_model: JobRead = result.scalar()
        stored_data: dict = jsonable_encoder(stored_model)

        assert stored_data is not None
        assert stored_data.get("title") == CREATED_JOB["title"], "Вид деятельности не был добавлен"

        CREATED_JOB = stored_data
        TEST_VALUE_SAVER.values["CREATED_JOB"] = CREATED_JOB


async def test_register_user(ac: AsyncClient, is_super_user):
    global CREATED_JOB
    global CREATED_USER2
    global CREATED_USER

    # 2‑й нужен для теста на удаление/изменение чужого пользователя
    CREATED_USER2["job_id"] = CREATED_JOB.get("id")
    CREATED_USER["job_id"] = CREATED_JOB.get("id")

    await ac.post(
        url="auth/register",
        json=CREATED_USER2
    )

    response = await ac.post(
        url="auth/register",
        json=CREATED_USER
    )

    async with async_session_maker_test() as session:
        utcnow_time = datetime.utcnow()

        time_format = {
            "sep": ' ',
            "timespec": "minutes"
        }

        signed_at = utcnow_time.isoformat(**time_format)
        last_promotion = utcnow_time.isoformat(**time_format)
        next_promotion = (utcnow_time + timedelta(days=365)).isoformat(**time_format)

        signed_at = datetime.fromisoformat(signed_at)
        last_promotion = datetime.fromisoformat(last_promotion)
        next_promotion = datetime.fromisoformat(next_promotion)

        stmt = update(UserEmployee). \
            where(UserEmployee.username == CREATED_USER.get("username")). \
            values(
            signed_at_utc=signed_at,
            last_promotion_utc=last_promotion,
            next_promotion_utc=next_promotion
        )
        await session.execute(stmt)
        # await session.commit()

        stmt = update(UserEmployee). \
            where(UserEmployee.username == CREATED_USER2.get("username")). \
            values(
            signed_at_utc=signed_at,
            last_promotion_utc=last_promotion,
            next_promotion_utc=next_promotion
        )
        await session.execute(stmt)
        await session.commit()

        if is_super_user:
            # Это нужно чтобы подсказки были
            session: AsyncSession = session

            stmt = update(UserEmployee). \
                where(UserEmployee.username == CREATED_USER.get("username")). \
                values(is_superuser=True)

            await session.execute(stmt)
            # await session.commit()

            query = select(UserEmployee).where(UserEmployee.username == CREATED_USER.get("username"))
            result = await session.execute(query)
            await session.commit()

            stored_model: UserEmployeeRead = result.scalar()
            stored_user: dict = jsonable_encoder(stored_model)

            CREATED_USER["is_superuser"] = stored_user.get("is_superuser")

            assert stored_user.get("is_superuser") is True, "Не супер-пользователь"

    assert response.status_code == 201, "Юзер не зареган"

    TEST_VALUE_SAVER.values["CREATED_USER"] = CREATED_USER


async def test_login_user(ac: AsyncClient):
    global CREATED_JOB
    global CREATED_USER
    global ACCESS_TOKEN

    response = await ac.post(
        url="auth/login",
        data={
            'grant_type': None,
            'username': CREATED_USER.get("email"),
            'password': CREATED_USER.get("password"),
            'scope': None,
            'client_id': None,
            'client_secret': None,
        }
    )

    # {'access_token': 'symbols', 'token_type': 'bearer'}
    response_dict = response.json()

    ACCESS_TOKEN = response_dict.get("access_token")
    TEST_VALUE_SAVER.values["ACCESS_TOKEN"] = ACCESS_TOKEN

    # pprint(CREATED_USER)

    assert response.status_code == 200, f"Войти не получилось"
