from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from job.schemas import JobRead
from src.exceptions import ShiftHTTPException
from src.database import get_async_session, store_exact_data_from_db
from src.job.models import Job
from src.main_users import CURRENT_USER
from src.user_employee.models import UserEmployee
from src.user_employee.schemas import EmployeeSalaryRead, UserEmployeeReadAddon

employees_router = APIRouter(
    prefix="/employees",
    tags=["employees"]
)


@employees_router.get(path="/me/salary", summary="Users:Get Salary Info")
async def get_salary_info(user_employee: UserEmployee = Depends(CURRENT_USER),
                          session: AsyncSession = Depends(get_async_session)):
    stored_user_data = await store_exact_data_from_db(
        base_model=UserEmployee,
        base_read=UserEmployeeReadAddon,
        session=session,
        row_id=user_employee.id,
    )

    stored_job_data = await store_exact_data_from_db(
        base_model=Job,
        base_read=JobRead,
        session=session,
        row_id=stored_user_data.get("job_id"),
    )

    result = EmployeeSalaryRead(
        salary=stored_job_data.get("salary"),
        last_promotion_utc=stored_user_data.get("last_promotion_utc"),
        next_promotion_utc=stored_user_data.get("next_promotion_utc")
    )

    raise ShiftHTTPException(
        status_code=status.HTTP_200_OK,
        detail=result,
        sh_status="success",
        sh_desc=None
    )
