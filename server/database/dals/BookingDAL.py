from datetime import date

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import Client, Booking, BookingStatusEnum


class BookingDAL:
    """Data Access Layer for operating clients info"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_booking(
        self,
        client_id: int,
        room_id: int,
        date_in: date,
        date_out: date,
        number_of_guests: int,
        status: BookingStatusEnum = BookingStatusEnum.active,
    ) -> Booking:
        """Создает запись, в таблице бронирований. Возвращает созданную запись."""
        new_booking = Booking(
            client_id=client_id,
            date_in=date_in,
            date_out=date_out,
            number_of_guests=number_of_guests,
            status=status,
            room_id=room_id,
        )
        self.session.add(new_booking)
        await self.session.flush()
        return new_booking

    async def cancel_booking(self, booking_id: int) -> int | None:
        """Отмена брони"""
        query = (
            update(Booking)
            .where(
                Booking.id == booking_id & Booking.status == BookingStatusEnum.active
            )
            .values(status=BookingStatusEnum.canceled)
            .returning(Booking.id)
        )
        res = await self.session.execute(query)
        canceled_booking_id = res.scalar_one_or_none()
        return canceled_booking_id

    async def get_booking(self, booking_id: int) -> Booking | None:
        query = select(Booking).where(Booking.id == booking_id)

        res = await self.session.execute(query)
        booking = res.scalar_one_or_none()
        return booking

    async def get_bookings(
        self,
        offset: int,
        limit: int,
        status: BookingStatusEnum = BookingStatusEnum.active,
    ) -> list[Client]:
        query = (
            select(Booking)
            .where(Booking.status == status)
            .options(joinedload(Booking.room), joinedload(Booking.client))
            .offset(offset)
            .limit(limit)
        )

        res = await self.session.execute(query)
        bookings = res.scalars().unique()

        return list(bookings)

    async def get_clients_bookings(self, client_id: int) -> list[Booking]:
        query = (
            select(Client.bookings)
            .where(Client.id == client_id)
            .options(joinedload(Client.bookings))
        )

        res = await self.session.execute(query)
        his_bookings = res.scalar_one_or_none()
        return list(his_bookings)
