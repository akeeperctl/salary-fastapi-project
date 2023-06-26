from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends
from fastapi_cache import JsonCoder
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database import get_async_session, store_exact_data_from_db, store_data_from_db
from src.exceptions import ShiftHTTPException
from src.job.models import Job as JobModel
from src.job.schemas import JobCreate, JobUpdate, JobRead
from src.main_users import CURRENT_USER_SUPERUSER
from src.user_employee.models import UserEmployee

job_router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@job_router.post(path="/add", description="Add new job to database. Only for **superuser**")
async def create_job(job: JobCreate, session: AsyncSession = Depends(get_async_session),
                     current_user: UserEmployee = Depends(CURRENT_USER_SUPERUSER)):

    job_title = job.title.lower()
    job_desc = job.description.lower()

    try:
        stmt = insert(JobModel).values(salary=job.salary, title=job_title, description=job_desc)
        await session.execute(stmt)
        await session.commit()
    except (IntegrityError, UniqueViolationError):
        raise ShiftHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=None,
            sh_status="error",
            sh_desc=f"job with title: {job_title} already created"
        )

    query = select(JobModel).where(JobModel.title == job_title)
    result = await session.execute(query)
    new_job: JobModel = result.scalar()

    if new_job.title.lower() == job_title:
        raise ShiftHTTPException(
            status_code=status.HTTP_201_CREATED,
            detail=new_job,
            sh_status="success",
            sh_desc="job add completed"
        )
    else:
        raise ShiftHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=None,
            sh_status="error",
            sh_desc="job add uncompleted"
        )


@job_router.patch(path="/{job_id}", description="Update a stored job in database. Only for **superuser**")
async def update_job(job: JobUpdate, job_id: int, session: AsyncSession = Depends(get_async_session),
                     current_user: UserEmployee = Depends(CURRENT_USER_SUPERUSER)):
    # query = select(JobModel).where(JobModel.id == job_id)
    # result = await session.execute(query)
    # await session.commit()
    # stored_job: JobRead = result.scalar()
    # stored_data: dict = jsonable_encoder(stored_job)

    stored_data = await store_exact_data_from_db(
        base_model=JobModel,
        base_read=JobRead,
        row_id=job_id,
        session=session
    )

    if stored_data is None:
        raise ShiftHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=None,
            sh_status="error",
            sh_desc=f"job with id: {job_id} not found"
        )

    stmt = update(JobModel). \
        where(JobModel.id == job_id). \
        values(**job.dict(exclude_unset=True))

    await session.execute(stmt)
    await session.commit()

    # query = select(JobModel).where(JobModel.id == job_id)
    # result = await session.execute(query)
    # updated_job: JobRead = result.scalar()
    # updated_data: dict = jsonable_encoder(updated_job)

    updated_data = await store_exact_data_from_db(
        base_model=JobModel,
        base_read=JobRead,
        row_id=job_id,
        session=session
    )

    if not stored_data == updated_data:
        raise ShiftHTTPException(
            status_code=status.HTTP_200_OK,
            detail=updated_data,
            sh_status="success",
            sh_desc="update complete"
        )
    else:
        raise ShiftHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=None,
            sh_status="error",
            sh_desc="update not completed"
        )

    # debug info
    # print(stored_data)
    # print(updated_data)
    #
    # return {
    #     "stored_data": stored_data,
    #     "new_dict": job.dict(),
    #     "updated_data": updated_data
    # }


@job_router.delete(path="/{job_id}", description="Delete stored job from database. Only for **superuser**")
async def delete_job(job_id: int, session: AsyncSession = Depends(get_async_session),
                     current_user: UserEmployee = Depends(CURRENT_USER_SUPERUSER)):
    pre_delete_data = await store_exact_data_from_db(
        row_id=job_id,
        base_model=JobModel,
        base_read=JobRead,
        session=session
    )

    if pre_delete_data is None:
        raise ShiftHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=None,
            sh_status="error",
            sh_desc=f"job with id: {job_id} not found"
        )

    stmt = delete(JobModel).where(JobModel.id == job_id)
    await session.execute(stmt)
    await session.commit()

    stored_data = await store_exact_data_from_db(
        row_id=job_id,
        base_model=JobModel,
        base_read=JobRead,
        session=session
    )

    if stored_data is None:
        raise ShiftHTTPException(
            status_code=status.HTTP_200_OK,
            detail=None,
            sh_status="success",
            sh_desc=f"job with id: {job_id} deleted"
        )
    else:
        raise ShiftHTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail=None,
            sh_status="error",
            sh_desc=f"job with id: {job_id} not deleted"
        )


@job_router.get(path="/all/", description="Get a list of stored jobs from the database. Only for **superuser**")
@cache(expire=60, coder=JsonCoder)
async def get_jobs(limit: int, offset: int, session: AsyncSession = Depends(get_async_session),
                   current_user: UserEmployee = Depends(CURRENT_USER_SUPERUSER)):
    stored_data = await store_data_from_db(
        limit=limit,
        offset=offset,
        base_model=JobModel,
        base_read=JobRead,
        session=session
    )

    raise ShiftHTTPException(
        status_code=status.HTTP_200_OK,
        detail=stored_data,
        sh_status="success",
        sh_desc=None
    )


@job_router.get(path="/{job_id}", description="Get stored job from database. Only for **superuser**")
@cache(expire=60, coder=JsonCoder)
async def get_job(job_id: int, session: AsyncSession = Depends(get_async_session),
                  current_user: UserEmployee = Depends(CURRENT_USER_SUPERUSER)):
    stored_data = await store_exact_data_from_db(
        row_id=job_id,
        base_model=JobModel,
        base_read=JobRead,
        session=session
    )

    if stored_data is None:
        raise ShiftHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=None,
            sh_status="error",
            sh_desc=f"job with id: {job_id} not found"
        )

    raise ShiftHTTPException(
        status_code=status.HTTP_200_OK,
        detail=stored_data,
        sh_status="success",
        sh_desc=None
    )
