from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, InvalidPasswordException
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from src.config import SECRET, TOKEN_RESET_PASSWORD_LIFETIME, TOKEN_VERIFICATION_LIFETIME
from src.database import get_user_db, get_async_session, store_exact_data_from_db, async_session_maker
from src.user_employee.models import UserEmployee
from src.user_employee.schemas import UserEmployeeCreate, UserEmployeeRead


class UserManager(IntegerIDMixin, BaseUserManager[UserEmployee, int]):
    reset_password_token_secret = SECRET
    reset_password_token_lifetime_seconds = int(TOKEN_RESET_PASSWORD_LIFETIME)
    verification_token_secret = SECRET
    verification_token_lifetime_seconds = int(TOKEN_VERIFICATION_LIFETIME)

    async def validate_password(
            self,
            password: str,
            user: Union[UserEmployeeCreate, UserEmployee],
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

    async def on_after_register(self, user: UserEmployee, request: Optional[Request] = None):
        # TypeError: 'async_generator' object is not an iterator
        # session = await next(get_async_session())

        # AttributeError: 'async_generator' object has no attribute 'execute'
        # session = get_async_session()

        # AttributeError: 'function' object has no attribute 'execute'
        # session = get_async_session

        # AttributeError: 'Depends' object has no attribute 'session'
        # db = Depends(get_user_db)
        # session = db.session

        async with async_session_maker() as session:
            # print(type(session))
            utcnow = datetime.utcnow()

            time_format = {
                "sep": ' ',
                "timespec": "minutes"
            }

            signed_at = utcnow.isoformat(**time_format)
            last_promotion = utcnow.isoformat(**time_format)
            next_promotion = (utcnow + timedelta(days=365)).isoformat(**time_format)

            signed_at = datetime.fromisoformat(signed_at)
            last_promotion = datetime.fromisoformat(last_promotion)
            next_promotion = datetime.fromisoformat(next_promotion)

            stmt = update(UserEmployee). \
                where(UserEmployee.id == user.id). \
                values(
                signed_at_utc=signed_at,
                last_promotion_utc=last_promotion,
                next_promotion_utc=next_promotion
            )

            await session.execute(statement=stmt)
            await session.commit()

            print(f"SERVER: User {user.id} has registered at {utcnow}")

    async def on_after_forgot_password(
            self, user: UserEmployee, token: str, request: Optional[Request] = None
    ):
        print(f"SERVER: User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: UserEmployee, token: str, request: Optional[Request] = None
    ):
        print(f"SERVER: Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_login(
            self,
            user: UserEmployee,
            request: Optional[Request] = None,
            response: Optional[Response] = None,
    ):
        print(f"SERVER: User {user.id} logged in.")
        # print(f"SERVER: Request {request.client.host}")
        # print(f"SERVER: Request {request.client.port}")
        # print(f"SERVER: Request {request.client}")
        # print(f"SERVER: Request {request.url}")
        # print(f"SERVER: Request {request.url.scheme}")
        # print(f"SERVER: Request {request.url.username}")
        # print(f"SERVER: Request {request.url.password}")
        # print(f"SERVER: Request {request.url.path}")
        # print(f"SERVER: Response {response.headers.values()}")
        # print(f"SERVER: Response {response.headers.keys()}")
        # print(f"SERVER: Response {response.headers.items()}")
        # print(f"SERVER: Response {response.headers.mutablecopy()}")
        # print(f"SERVER: Response {response.raw_headers}")
        # print(f"SERVER: Response {response.charset}")
        # print(f"SERVER: Response {response.background}")
        # print(f"SERVER: Response {response.body}")
        # print(f"SERVER: Response {response.media_type}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
