from typing import Annotated

from fastapi import APIRouter, Depends

from api.schemes import RoomOrderShow, RoomOrderCreate
from database.dals import RoomOrderDAL
from database.session import AsyncSession, get_db_session
from shared import create_http_exception

roomOrders_router = APIRouter()


@roomOrders_router.post("/")
async def create_roomOrder(
        roomOrder: RoomOrderCreate, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        roomOrder_dal = RoomOrderDAL(session)

        # -----------------
        # old_roomOrder = await roomOrder_dal.get_roomOrder_by_id(roomOrder.username)
        # if old_roomOrder:
        #    raise create_http_exception(
        #        status_code=403,
        #        reason="room order with provided room id and date in already exists",
        #        room_id=roomOrder.room_id,
        #        date_in=roomOrder.date_in,
        #    )
        # -----------------

        new_roomOrder = await roomOrder_dal.create_roomOrder(
            paying_client_id=roomOrder.paying_client_id,
            date_in=roomOrder.date_in,
            date_out=roomOrder.date_out,
            room_id=roomOrder.room_id,
        )

        return new_roomOrder


@roomOrders_router.get("/", response_model=list[RoomOrderShow])
async def get_roomOrders(
        session: Annotated[AsyncSession, Depends(get_db_session)],
        offset: int = 0,
        limit: int = 10,
):
    async with session.begin():
        room_order_dal = RoomOrderDAL(session)
        if limit > 10:
            raise create_http_exception(
                status_code=416, reason="you cannot output more than 10 room orders "
            )
        room_order = await room_order_dal.get_roomOrders(offset, limit)
        return room_order