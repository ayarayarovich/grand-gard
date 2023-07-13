from typing import Annotated

from fastapi import APIRouter, Depends

from api.schemes import ServiceOrderShow, ServiceOrderCreate
from database.dals import ServiceOrderDAL
from database.session import AsyncSession, get_db_session
from shared import create_http_exception

serviceOrders_router = APIRouter()


@serviceOrders_router.post("/")
async def create_service_order(
        serviceOrder: ServiceOrderCreate, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        service_order_dal = ServiceOrderDAL(session)

        # -----------------
        # old_serviceOrder = await service_order_dal.get_serviceOrder_by_id(serviceOrder.username)
        # if old_serviceOrder:
        #    raise create_http_exception(
        #        status_code=403,
        #        reason="service order with provided service id and date in already exists",
        #        service_id=serviceOrder.service_id,
        #        date_in=serviceOrder.date_in,
        #    )
        # -----------------

        new_service_order = await service_order_dal.create_serviceOrder(
            service_id=serviceOrder.service_id,
            client_id=serviceOrder.client_id,
            room_id=serviceOrder.room_id,
        )

        return new_service_order


@serviceOrders_router.get("/", response_model=list[ServiceOrderShow])
async def get_service_orders(
        session: Annotated[AsyncSession, Depends(get_db_session)],
        offset: int = 0,
        limit: int = 10,
):
    async with session.begin():
        service_order_dal = ServiceOrderDAL(session)
        if limit > 10:
            raise create_http_exception(
                status_code=416, reason="you cannot output more than 10 service orders "
            )
        service_order = await service_order_dal.get_serviceOrders(offset, limit)
        return service_order
