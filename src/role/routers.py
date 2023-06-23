from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.response import ShiftHTTPException
from src.database import get_async_session, store_exact_data_from_db, store_data_from_db
from src.role.models import Role as RoleModel
from src.role.schemas import RoleCreate as RoleCreateScheme, RoleUpdate, RoleRead

role_router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    deprecated=True
)


@role_router.post(path="/add")
async def create_role(role: RoleCreateScheme, session: AsyncSession = Depends(get_async_session)):

    role_title = role.title.lower()

    try:
        stmt = insert(RoleModel).values(title=role_title, permissions=role.permissions)
        await session.execute(stmt)
        await session.commit()
    except (IntegrityError, UniqueViolationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description=f"role with title: {role_title} already created",
                    data=None
                )
            )
        )

    query = select(RoleModel).where(RoleModel.title == role_title)
    result = await session.execute(query)
    new_role: RoleModel = result.scalar()

    if new_role.title.lower() == role_title:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="success",
                    description=f"role with id: {new_role.id} created",
                    data=jsonable_encoder(new_role)
                )
            )
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description=f"role with id: {new_role.id} not created",
                    data=None
                )
            )
        )


@role_router.patch(path="/{role_id}")
async def update_role(role: RoleUpdate, role_id: int, session: AsyncSession = Depends(get_async_session)):
    stored_data = await store_exact_data_from_db(
        row_id=role_id,
        base_model=RoleModel,
        base_read=RoleRead,
        session=session
    )

    if stored_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description=f"role with id: {role_id} not found",
                    data=None
                )
            )
        )

    # query = select(RoleModel).where(RoleModel.id == role_id)
    # result = await session.execute(query)
    # await session.commit()
    # stored_job: RoleRead = result.scalar()
    # stored_data: dict = jsonable_encoder(stored_job)

    stmt = update(RoleModel). \
        where(RoleModel.id == role_id). \
        values(**role.dict(exclude_unset=True))

    await session.execute(stmt)
    await session.commit()

    # query = select(RoleModel).where(RoleModel.id == role_id)
    # result = await session.execute(query)
    # updated_job: RoleRead = result.scalar()
    # updated_data: dict = jsonable_encoder(updated_job)

    updated_data = await store_exact_data_from_db(
        row_id=role_id,
        base_model=RoleModel,
        base_read=RoleRead,
        session=session
    )

    if not stored_data == updated_data:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="success",
                    description=f"role with id: {role_id} updated",
                    data=None
                )
            )
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description="stored data equal updated data",
                    data=None
                )
            )
        )


@role_router.delete(path="/{role_id}")
async def delete_job(role_id: int, session: AsyncSession = Depends(get_async_session)):
    pre_delete_data = await store_exact_data_from_db(
        row_id=role_id,
        base_model=RoleModel,
        base_read=RoleRead,
        session=session
    )

    if pre_delete_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description=f"role with id: {role_id} not found",
                    data=None
                )
            )
        )

    stmt = delete(RoleModel).where(RoleModel.id == role_id)
    await session.execute(stmt)
    await session.commit()

    stored_data = await store_exact_data_from_db(
        row_id=role_id,
        base_model=RoleModel,
        base_read=RoleRead,
        session=session
    )

    if stored_data is None:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="success",
                    description=f"role with id: {role_id} deleted",
                    data=None
                )
            )
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description=f"role with id: {role_id} not deleted",
                    data=None
                )
            )
        )


@role_router.get(path="/{role_id}")
async def get_role(role_id: int, session: AsyncSession = Depends(get_async_session)):
    stored_data = await store_exact_data_from_db(
        row_id=role_id,
        base_model=RoleModel,
        base_read=RoleRead,
        session=session
    )

    if stored_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description=f"role with id: {role_id} not found",
                    data=None
                )
            )
        )

    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail=jsonable_encoder(
            ShiftAPIResponse(
                status="success",
                description="",
                data=stored_data
            )
        )
    )


@role_router.get(path="/all/")
async def get_roles(limit: int, offset: int, session: AsyncSession = Depends(get_async_session)):
    stored_data = await store_data_from_db(
        limit=limit,
        offset=offset,
        base_model=RoleModel,
        base_read=RoleRead,
        session=session
    )

    raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="success",
                    description="",
                    data=stored_data
                )
            )
        )
