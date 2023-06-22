from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends

from src.database import get_async_session
from src.job.models import Job as JobModel
from src.job.schemas import JobCreate, JobUpdate

job_router = APIRouter(
    prefix="/job",
    tags=["job"]
)


@job_router.post(path="/add")
async def create_job(job: JobCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(JobModel).values(salary=job.salary, title=job.title, description=job.description)
    await session.execute(stmt)
    await session.commit()

    query = select(JobModel).where(JobModel.title == job.title)
    result = await session.execute(query)
    new_job: JobModel = result.scalar()

    if new_job.title == job.title:
        return {
            "status": "success",
            "description": None,
            "data": new_job
        }
    else:
        return {
            "status": "error",
            "description": None,
            "data": None
        }


@job_router.post(path="/{job_id}/update")
async def update_role(job: JobUpdate, job_id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = update(JobModel). \
        where(JobModel.id == job_id). \
        values(**job.dict())

    await session.execute(stmt)
    await session.commit()

    query = select(JobModel).where(JobModel.id == job_id)
    result = await session.execute(query)
    updated_job: JobUpdate = result.scalar()

    if updated_job.title == job.title and \
            updated_job.description == job.description and \
            updated_job.salary == job.salary:
        return {
            "status": "success",
            "description": None,
            "data": updated_job
        }
    else:
        return {
            "status": "error",
            "description": None,
            "data": None
        }
