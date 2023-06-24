from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.auth.auth import auth_backend, REDIS_INSTANCE
from src.job.routers import job_router
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


@app.on_event("startup")
async def on_app_start():
    FastAPICache.init(RedisBackend(REDIS_INSTANCE), prefix="fastapi-cache")
