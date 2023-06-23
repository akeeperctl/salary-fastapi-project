from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_cache import FastAPICache

from src.main_users import app_users
from src.user_employee.schemas import UserEmployeeRead, UserEmployeeCreate
from src.role.routers import role_router
from src.user_employee.routers import employees_router
from src.auth.auth import auth_backend
from src.auth.user_manager import get_user_manager

from src.job.routers import job_router

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
app.include_router(role_router)
app.include_router(employees_router)

# @app.on_event("startup")
# async def on_startup():
#     app_cache.init()
