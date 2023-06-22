from typing import Union

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from src.database import get_async_session
from src.role.models import Role as RoleModel
from src.role.schemas import RoleCreate as RoleCreateScheme, RoleUpdate

role_router = APIRouter(
    prefix="/role",
    tags=["role"]
)


@role_router.post(path="/add")
async def create_role(role: RoleCreateScheme, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(RoleModel).values(title=role.title, permissions=role.permissions)
    await session.execute(stmt)
    await session.commit()

    query = select(RoleModel).where(RoleModel.title == role.title)
    result = await session.execute(query)
    new_role: RoleModel = result.scalar()

    if new_role.title == role.title:
        return {
            "status": "success",
            "description": None,
            "data": new_role
        }
    else:
        return {
            "status": "error",
            "description": None,
            "data": None
        }


@role_router.post(path="/{input_role_id}/update")
async def update_role(role: RoleUpdate, input_role_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = update(RoleModel). \
        where(RoleModel.id == input_role_id). \
        values(**role.dict())

    await session.execute(stmt)
    await session.commit()

    query = select(RoleModel).where(RoleModel.id == input_role_id)
    result = await session.execute(query)
    updated_role: RoleUpdate = result.scalar()

    if updated_role.title == role.title and \
            updated_role.permissions == role.permissions:
        return {
            "status": "success",
            "description": None,
            "data": updated_role
        }
    else:
        return {
            "status": "error",
            "description": None,
            "data": None
        }
