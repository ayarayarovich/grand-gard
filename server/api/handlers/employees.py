from typing import Annotated

from fastapi import APIRouter, Depends

from api.schemes import EmployeeShow, EmployeeCreate, EmployeeUpdate
from database.dals import EmployeeDAL
from database.session import AsyncSession, get_db_session
from shared import create_http_exception
employees_router = APIRouter()


@employees_router.post("/")
async def create_employee(
    employee: EmployeeCreate, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        employee_dal = EmployeeDAL(session)

        #-----------------
        old_employee = await employee_dal.get_employee_by_username(employee.username)
        if old_employee:
            raise create_http_exception(
                status_code=403,
                reason="employee with provided username already exists",
                username=employee.username,
            )
        # -----------------

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

        # ------------------
        employee = await employee_dal.get_employee_by_id(id)
        if employee is None:
            raise create_http_exception(
                status_code=404, reason="employee with provided id does not exist", id=id
            )
        # ------------



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
        #------------------
        if employee is None:
            raise create_http_exception(
                status_code=404, reason="employee with provided id does not exist", id=id
            )
        #------------
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
        if limit > 10:
            raise create_http_exception(
                status_code=416, reason="you cannot output more than 10 posts ", id=id
            )
        return employees

@employees_router.delete("/{id}")
async def delete_employee(id: int, session: Annotated[AsyncSession, Depends(get_db_session)]):

    async with session.begin():
        employees_dal = EmployeeDAL(session)

        room = await employees_dal.get_employee_by_id(id)
        if room is None:
            raise create_http_exception(
                status_code=404, reason="employee with provided id does not exist", id=id
            )
        deleted_employees_id = await employees_dal.delete_employee(id)
        return {deleted_employees_id: "is deleted"}