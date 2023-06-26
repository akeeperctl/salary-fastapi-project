from pprint import pprint

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import insert, select

from src.auth.auth import auth_backend, REDIS_INSTANCE
from src.config import CREATE_PLUG_JOB
from src.database import async_session_maker
from src.job.models import Job
from src.job.routers import job_router
from src.job.schemas import JobRead
from src.main_users import app_users
from src.user_employee.routers import employees_router
from src.user_employee.schemas import UserEmployeeRead, UserEmployeeCreate

app = FastAPI(title="Shift Python Project")

app.include_router(
    app_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    app_users.get_register_router(UserEmployeeRead, UserEmployeeCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    app_users.get_users_router(UserEmployeeRead, UserEmployeeCreate),
    prefix="/employees",
    tags=["employees"],
)
app.include_router(
    app_users.get_verify_router(UserEmployeeRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(job_router)
app.include_router(employees_router)


# @app.get(path="/hardword/")
# @cache(expire=60, coder=JsonCoder)
# async def do_work():
#     time.sleep(2)
#     return "Work done"


@app.on_event("startup")
async def on_app_start():
    FastAPICache.init(RedisBackend(REDIS_INSTANCE), prefix="fastapi-cache")

    if CREATE_PLUG_JOB == "True":
        try:
            async with async_session_maker() as session:
                title = "заглушка"
                # check
                query = select(Job).where(Job.title == title)
                result = await session.execute(query)
                await session.commit()

                stored_model: JobRead = result.scalar()
                stored_job: dict = jsonable_encoder(stored_model)

                if stored_job is None:
                    stmt = insert(Job).values(salary=15000, title=title, description="заглушка")
                    await session.execute(stmt)
                    await session.commit()
        except Exception as e:
            pprint("Plug job can not be created. Database not connected")
    #
    # # get
    # query = select(Job).where(Job.title == title)
    # result = await session.execute(query)
    # await session.commit()
    #
    # stored_model: JobRead = result.scalar()
    # stored_job: dict = jsonable_encoder(stored_model)
    #
    # if stored_job is not None:
    #     stmt = insert(UserEmployee).values(
    #         job_id=stored_job.get("id"),
    #         username="superuser",
    #         firstname="superuser",
    #         lastname="superuser",
    #         signed_at_utc=,
    #         last_promotion_utc=,
    #         next_promotion_utc=,
    #         email=,
    #         password=
    #     )
