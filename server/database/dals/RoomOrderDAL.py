from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Room, RoomOrder

from datetime import datetime, date, time

class RoomOrderDAL:
    """Data Access Layer for operating room orders info"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_roomOrder(
        self,
        paying_client_id: int,
        date_in: datetime.date,
        date_out: datetime.date,
        room_id: int,
    ) -> RoomOrder:
        new_roomOrder = RoomOrder(
            paying_client_id=paying_client_id,
            date_in=date_in,
            date_out=date_out,
            room_id=room_id,
        )
        self.session.add(new_roomOrder)
        await self.session.flush()
        return new_roomOrder

    async def get_roomOrders(
        self, offset: int, limit: int, active_ones: bool = None
    ) -> list[RoomOrder]:
        query = select(RoomOrder).offset(offset).limit(limit)
        res = await self.session.execute(query)
        roomOrders = res.scalars().all()
        return list(roomOrders)