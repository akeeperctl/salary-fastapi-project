from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, InvalidPasswordException

from src.auth.schemas import EmployeeCreate
from src.config import SECRET, TOKEN_RESET_PASSWORD_LIFETIME, TOKEN_VERIFICATION_LIFETIME
from src.database import get_user_db
from src.auth.models import Employee


class UserManager(IntegerIDMixin, BaseUserManager[Employee, int]):
    reset_password_token_secret = SECRET
    reset_password_token_lifetime_seconds = TOKEN_RESET_PASSWORD_LIFETIME
    verification_token_secret = SECRET
    verification_token_lifetime_seconds = TOKEN_VERIFICATION_LIFETIME

    async def validate_password(
            self,
            password: str,
            user: Union[EmployeeCreate, Employee],
    ) -> None:
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password should not contain e-mail"
            )
        if (user.username in password) or (user.firstname in password) or (user.lastname in password):
            raise InvalidPasswordException(
                reason="Password should not contain username/firstname/lastname"
            )

    async def on_after_register(self, user: Employee, request: Optional[Request] = None):
        print(f"SERVER: User {user.id} has registered.")

        # todo: сюда добавить значения в БД: signed_at, last_promotion, next_promotion

    async def on_after_forgot_password(
            self, user: Employee, token: str, request: Optional[Request] = None
    ):
        print(f"SERVER: User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: Employee, token: str, request: Optional[Request] = None
    ):
        print(f"SERVER: Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
