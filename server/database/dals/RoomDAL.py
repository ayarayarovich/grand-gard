from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Room, RoomOrder


class RoomDAL:
    """Data Access Layer for operating rooms info"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_room(
        self,
        type_room: str,
        price: float,
        area: int,
        max_quest: int,
        is_active: bool = True,
    ) -> Room:
        new_room = Room(
            type_room=type_room,
            price=price,
            area=area,
            max_quest=max_quest,
            is_active=is_active,
        )
        self.session.add(new_room)
        await self.session.flush()
        return new_room

    async def delete_room(self, room_id: int) -> int | None:
        query = (
            update(Room)
            .where(Room.id == room_id)
            .values(is_active=False)
            .returning(Room.id)
        )
        res = await self.session.execute(query)
        deleted_room_id = res.scalar_one_or_none()
        return deleted_room_id

    async def get_room_by_id(self, room_id: int) -> Room | None:
        query = select(Room).where(Room.id == room_id)
        res = await self.session.execute(query)
        room = res.scalar_one_or_none()
        return room

    async def update_room(self, room_id: int, **kwargs):
        query = update(Room).where(Room.id == room_id).values(kwargs).returning(Room.id)
        res = await self.session.execute(query)
        updated_room_id = res.scalar_one_or_none()
        return updated_room_id

    async def get_room_orders(
        self, room_id: int, offset: int = 0, limit: int = 10
    ) -> list[RoomOrder]:
        query = (
            select(RoomOrder)
            .where(RoomOrder.room_id == room_id)
            .offset(offset)
            .limit(limit)
        )
        res = await self.session.execute(query)
        room_orders = res.scalars()
        return list(room_orders)

    async def get_rooms(
        self, offset: int, limit: int, active_ones: bool = None
    ) -> list[Room]:
        query = select(Room).offset(offset).limit(limit)
        if active_ones is not None:
            query.where(Room.is_active == active_ones)
        res = await self.session.execute(query)
        rooms = res.scalars()
        return list(rooms)
