from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Service, ServiceOrder

from datetime import datetime, date, time

class ServiceOrderDAL:
    """Data Access Layer for operating room orders info"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_serviceOrder(
        self,
        service_id: int,
        client_id: int,
        room_id: int,
    ) -> ServiceOrder:
        new_serviceOrder = ServiceOrder(
            service_id=service_id,
            client_id=client_id,
            room_id=room_id,
        )
        self.session.add(new_serviceOrder)
        await self.session.flush()
        return new_serviceOrder

    async def get_serviceOrders(
        self, offset: int, limit: int, active_ones: bool = None
    ) -> list[ServiceOrder]:
        query = select(ServiceOrder).offset(offset).limit(limit)
        res = await self.session.execute(query)
        serviceOrders = res.scalars().all()
        return list(serviceOrders)