from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.response import ShiftAPIResponse
from src.database import get_async_session, store_exact_data_from_db, store_data_from_db
from src.job.models import Job as JobModel
from src.job.schemas import JobCreate, JobUpdate, JobRead

job_router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@job_router.post(path="/add")
async def create_job(job: JobCreate, session: AsyncSession = Depends(get_async_session)):
    job_title = job.title.lower()
    job_desc = job.description.lower()

    try:
        stmt = insert(JobModel).values(salary=job.salary, title=job_title, description=job_desc)
        await session.execute(stmt)
        await session.commit()
    except (IntegrityError, UniqueViolationError) as ie:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description=f"job with title: {job_title} already created",
                    data=None
                )
            )
        )

    query = select(JobModel).where(JobModel.title == job_title)
    result = await session.execute(query)
    new_job: JobModel = result.scalar()

    if new_job.title.lower() == job_title:
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="success",
                    description="job add completed",
                    data=new_job
                )
            )
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description="job add uncompleted",
                    data=None
                )
            )
        )


@job_router.patch(path="/{job_id}")
async def update_Job(job: JobUpdate, job_id: int, session: AsyncSession = Depends(get_async_session)):
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description=f"job with id: {job_id} not found",
                    data=None
                )
            )
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
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="success",
                    description="update complete",
                    data=updated_data
                )
            )
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description="update not completed",
                    data=None
                )
            )
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


@job_router.delete(path="/{job_id}")
async def delete_job(job_id: int, session: AsyncSession = Depends(get_async_session)):
    pre_delete_data = await store_exact_data_from_db(
        row_id=job_id,
        base_model=JobModel,
        base_read=JobRead,
        session=session
    )

    if pre_delete_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description=f"job with id: {job_id} not found",
                    data=None
                )
            )
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
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="success",
                    description=f"job with id: {job_id} deleted",
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
                    description=f"job with id: {job_id} not deleted",
                    data=None
                )
            )
        )


@job_router.get(path="/all/")
async def get_jobs(limit: int, offset: int, session: AsyncSession = Depends(get_async_session)):
    stored_data = await store_data_from_db(
        limit=limit,
        offset=offset,
        base_model=JobModel,
        base_read=JobRead,
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


@job_router.get(path="/{job_id}")
async def get_job(job_id: int, session: AsyncSession = Depends(get_async_session)):
    stored_data = await store_exact_data_from_db(
        row_id=job_id,
        base_model=JobModel,
        base_read=JobRead,
        session=session
    )

    if stored_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=jsonable_encoder(
                ShiftAPIResponse(
                    status="error",
                    description=f"job with id: {job_id} not found",
                    data=None
                )
            )
        )

    raise HTTPException(
        status_code=status.HTTP_200_OK,
        detail=jsonable_encoder(
            ShiftAPIResponse(
                status="success",
                description=None,
                data=stored_data
            )
        )
    )
