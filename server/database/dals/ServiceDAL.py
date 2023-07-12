from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import Service, ServiceOrder, ServiceOrderStatusEnum


class ServiceDAL:
    """Data Access Layer for operating service info"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_service(
        self, name: str, price: float, is_active: bool = True
    ) -> Service:
        new_service = Service(name=name, price=price, is_active=is_active)
        self.session.add(new_service)
        await self.session.flush()
        return new_service

    async def delete_service(self, service_id: int) -> int | None:
        query = (
            update(Service)
            .where(Service.id == service_id)
            .values(is_active=False)
            .returning(Service.id)
        )
        res = await self.session.execute(query)
        deleted_service_id = res.scalar_one_or_none()
        return deleted_service_id

    async def get_service_by_id(self, service_id: int) -> Service | None:
        query = select(Service).where(Service.id == service_id)
        res = await self.session.execute(query)
        service = res.scalar_one_or_none()
        return service

    async def update_service(self, service_id: int, **kwargs):
        query = (
            update(Service)
            .where(Service.id == service_id)
            .values(kwargs)
            .returning(Service.id)
        )
        res = await self.session.execute(query)
        updated_service_id = res.scalar_one_or_none()
        return updated_service_id

    async def get_service_orders_from_room(
        self,
        room_id: int,
        eligible_statuses: list[ServiceOrderStatusEnum] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[ServiceOrder]:
        query = (
            select(ServiceOrder)
            .where(ServiceOrder.room_id == room_id)
            .options(joinedload(ServiceOrder.service))
            .offset(offset)
            .limit(limit)
        )
        if eligible_statuses is not None:
            query.where(ServiceOrder.status.in_(eligible_statuses))
        res = await self.session.execute(query)
        service_orders = res.scalars()
        return list(service_orders)

    async def get_orders_on_service(
        self,
        service_id: int,
        eligible_statuses: list[ServiceOrderStatusEnum] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> list[ServiceOrder]:
        query = (
            select(ServiceOrder)
            .where(ServiceOrder.service_id == service_id)
            .options(joinedload(ServiceOrder.service))
            .offset(offset)
            .limit(limit)
        )
        if eligible_statuses is not None:
            query.where(ServiceOrder.status.in_(eligible_statuses))
        res = await self.session.execute(query)
        service_orders = res.scalars()
        return list(service_orders)
