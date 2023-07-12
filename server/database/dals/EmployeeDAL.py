from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.dals import PostDAL
from database.models import PermissionsEnum, Employee, Post


class EmployeeDAL:
    """Data Access Layer for operating rooms info"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_employee(
        self,
        post_name: str,
        post_permissions: list[PermissionsEnum],
        username,
        hashed_password,
        is_active,
    ):
        res = await self.session.execute(select(Post).where(Post.name == post_name))
        post = res.scalar_one_or_none()

        if post is None:
            post = Post(
                name=post_name,
                permissions=[p.value for p in post_permissions]
                if post_permissions is not None
                else [],
            )

        new_employee = Employee(
            username=username,
            hashed_password=hashed_password,
            is_active=is_active,
            post=post,
        )

        self.session.add_all([new_employee, post])
        await self.session.flush()
        return new_employee

    async def delete_employee(self, employee_id: int) -> int | None:
        query = (
            update(Employee)
            .where(Employee.id == employee_id & Employee.is_active == True)
            .values(is_active=False)
            .returning(Employee.id)
        )
        res = await self.session.execute(query)
        deleted_employee_id = res.scalar_one_or_none()
        return deleted_employee_id

    async def get_employee_by_id(self, employee_id: int) -> Employee | None:
        query = (
            select(Employee)
            .where(Employee.id == employee_id)
            .options(joinedload(Employee.post))
        )

        res = await self.session.execute(query)
        employee = res.scalars().unique().one_or_none()

        return employee

    async def get_employee_by_username(self, employee_username: str) -> Employee | None:
        query = (
            select(Employee)
            .where(Employee.username == employee_username)
            .options(joinedload(Employee.post))
        )

        res = await self.session.execute(query)
        employee = res.scalars().unique().one_or_none()

        return employee

    async def get_employees(self, offset: int, limit: int) -> list[Employee]:
        query = (
            select(Employee)
            .options(joinedload(Employee.post))
            .offset(offset)
            .limit(limit)
        )

        res = await self.session.execute(query)
        employees = res.scalars().unique().all()

        return list(employees)

    async def assign_post(
        self, employee_id: int, post_name: str = None, post_id: int = None
    ):
        post_dal = PostDAL(self.session)
        employee = await self.get_employee_by_id(employee_id)
        if post_name is not None and post_id is not None:
            raise Exception(
                "Only one post selection parameter has to be provided. It's either post_name or post_id!"
            )
        elif post_name is not None:
            post = await post_dal.get_post_by_name(post_name=post_name)
        elif post_id is not None:
            post = await post_dal.get_post_by_id(post_id=post_id)
        else:
            raise Exception("Either post_name or post_id arguments have to be provided")
        employee.post = post
        await self.session.flush()
        return employee
