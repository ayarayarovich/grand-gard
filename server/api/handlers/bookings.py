from typing import Annotated

from fastapi import APIRouter, Depends

from api.schemes import BookingShow, BookingCreate
from database.dals import BookingDAL
from database.session import AsyncSession, get_db_session
from shared import create_http_exception
bookings_router = APIRouter()


@bookings_router.post("/", response_model=BookingShow)
async def create_booking(
    booking: BookingCreate, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        booking_dal = BookingDAL(session)

        if booking_dal.is_room_booked(booking.room_id, booking.date_in, booking.date_out):
            raise create_http_exception(
                status_code=403,
                reason="This room is already booked",
            )

        new_booking = await booking_dal.create_booking(
            room_id=booking.room_id,
            client_id=booking. client_id,
            date_in=booking.date_in,
            date_out=booking.date_out,
            number_of_guests=booking.number_of_guests,)

        return new_booking

@bookings_router.get("/{id}", response_model=BookingShow)  # предоставление информации
async def get_booking_by_id(
        id: int, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        booking_dal = BookingDAL(session)

        booking = await booking_dal.get_booking(id)
        if booking is None:
            raise create_http_exception(
                status_code=404, reason="Booking with provided id does not exist"
            )
        return booking