from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import Client, Booking


class ClientDAL:
    """Data Access Layer for operating clients info"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_client(
        self,
        first_name: str,
        middle_name: str,
        last_name: str,
        phone: str,
        email: str,
        hashed_password: str,
        room_id: int | None = None,
        is_active: bool = True,
    ) -> Client:
        new_client = Client(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            phone=phone,
            email=email,
            hashed_password=hashed_password,
            room_id=room_id,
            is_active=is_active,
        )
        self.session.add(new_client)
        await self.session.flush()
        return new_client

    async def delete_client(self, client_id: int) -> int | None:
        query = (
            update(Client)
            .where(Client.id == client_id & Client.is_active == True)
            .values(is_active=False)
            .returning(Client.id)
        )
        res = await self.session.execute(query)
        deleted_user_id = res.scalar_one_or_none()
        return deleted_user_id

    async def get_client_by_id(
        self, client_id: int, include_his_room_orders: bool = False
    ) -> Client | None:
        query = select(Client).where(Client.id == client_id)

        if include_his_room_orders:
            query.options(joinedload(Client.room_orders))

        res = await self.session.execute(query)
        client = res.scalar_one_or_none()
        return client

    async def get_client_by_email(self, client_email: str) -> Client | None:
        query = select(Client).where(Client.email == client_email)
        res = await self.session.execute(query)
        client = res.scalar_one_or_none()
        return client

    async def get_clients(
        self, offset: int, limit: int, active_ones: bool = None
    ) -> list[Client]:
        query = (
            select(Client)
            .options(joinedload(Client.room_orders))
            .offset(offset)
            .limit(limit)
        )

        if active_ones is not None:
            query.where(Client.is_active == active_ones)

        res = await self.session.execute(query)
        clients = res.scalars().unique()

        return list(clients)

    async def update_client(self, client_id: int, **kwargs):
        query = (
            update(Client)
            .where(Client.id == client_id)
            .values(kwargs)
            .returning(Client.id)
        )
        res = await self.session.execute(query)
        updated_client_id = res.scalar_one_or_none()
        return updated_client_id

    async def get_clients_bookings(
        self, client_id: int, offset: int = 0, limit: int = 0
    ) -> list[Booking]:
        query = (
            select(Booking)
            .where(Booking.client_id == client_id)
            .offset(offset)
            .limit(limit)
        )

        res = await self.session.execute(query)
        his_bookings = res.scalar_one_or_none()
        return list(his_bookings)
