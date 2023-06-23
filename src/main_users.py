from fastapi_users import FastAPIUsers

from src.auth.auth import auth_backend
from src.auth.user_manager import get_user_manager

app_users = FastAPIUsers(
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend]
)

CURRENT_USER = app_users.current_user()