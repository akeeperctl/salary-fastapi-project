from pprint import pprint

from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.job.models import Job
from src.job.schemas import JobRead
from tests.conftest import async_session_maker_test, TEST_VALUE_SAVER

CREATED_JOB = {}
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
ACCESS_TOKEN: str = ""


async def test_create_job():
    async with async_session_maker_test() as session:
        global CREATED_JOB

        session: AsyncSession = session

        job_title = "разработчик ml"
        job_desc = "Занимается разработкой и внедрением ML"

        stmt = insert(Job). \
            values(
            salary=70000,
            title=job_title.lower(),
            description=job_desc.lower())

        await session.execute(stmt)
        await session.commit()

        query = select(Job).where(Job.title == job_title)
        result = await session.execute(query)
        await session.commit()
        stored_model: JobRead = result.scalar()
        stored_data: dict = jsonable_encoder(stored_model)

        assert stored_data is not None
        assert stored_data.get("title") == job_title + "", "Вид деятельности не был добавлен"

        CREATED_JOB = stored_data
        TEST_VALUE_SAVER.values["CREATED_JOB"] = CREATED_JOB


async def test_register_user(ac: AsyncClient):
    global CREATED_JOB
    global CREATED_USER

    CREATED_USER["job_id"] = CREATED_JOB.get("id")

    response = await ac.post(
        url="auth/register",
        json=CREATED_USER
    )

    assert response.status_code == 201, "Юзер не зареган"

    TEST_VALUE_SAVER.values["CREATED_USER"] = CREATED_USER

    # query = select(UserEmployee).where(UserEmployee.username == CREATED_USER.get("username"))
    # result = await session.execute(query)
    # await session.commit()
    # stored_model: UserEmployeeRead = result.scalar()
    # stored_user: dict = jsonable_encoder(stored_model)
    #
    # CREATED_USER = stored_user


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

    assert response.status_code == 200, f"Войти не получилось"
