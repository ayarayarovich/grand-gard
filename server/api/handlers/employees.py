from typing import Annotated

from fastapi import APIRouter, Depends

from api.schemes import EmployeeShow, EmployeeCreate, EmployeeUpdate
from database.dals import EmployeeDAL
from database.session import AsyncSession, get_db_session

employees_router = APIRouter()


@employees_router.post("/")
async def create_employee(
    employee: EmployeeCreate, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        employee_dal = EmployeeDAL(session)

        new_employee = await employee_dal.create_employee(
            username=employee.username,
            hashed_password=employee.password,
            post_name=employee.post.name,
            post_permissions=employee.post.permissions,
            is_active=True,
        )

        return new_employee


@employees_router.put("/{id}", response_model=EmployeeShow)
async def update_employee(
    id: int,
    values_to_update: EmployeeUpdate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    async with session.begin():
        employee_dal = EmployeeDAL(session)
        updated_employee = await employee_dal.update_employee(
            id, **values_to_update.dict(exclude_unset=True)
        )
        return updated_employee


@employees_router.get("/{id}", response_model=EmployeeShow)
async def get_employee_by_id(
    id: int, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        employee_dal = EmployeeDAL(session)

        employee = await employee_dal.get_employee_by_id(id)
        return employee


@employees_router.get("/", response_model=list[EmployeeShow])
async def get_all_employees(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    offset: int = 0,
    limit: int = 10,
):
    async with session.begin():
        employees_dal = EmployeeDAL(session)
        employees = await employees_dal.get_employees(offset, limit)
        return employees
