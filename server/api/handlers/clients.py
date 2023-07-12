from typing import Annotated

from fastapi import APIRouter, Depends

from api.schemes import ClientShow, ClientCreate, ClientUpdate
from database.dals import ClientDAL
from database.session import AsyncSession, get_db_session
from shared import create_http_exception

clients_router = APIRouter()


@clients_router.post("/", response_model=ClientShow)
async def create_client(
    client: ClientCreate, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        client_dal = ClientDAL(session)

        old_client = await client_dal.get_client_by_email(client.email)
        if old_client:
            raise create_http_exception(
                status_code=403,
                reason="client with provided email already exists",
                email=client.email,
            )

        new_client = await client_dal.create_client(
            first_name=client.first_name,
            middle_name=client.middle_name,
            last_name=client.last_name,
            phone=client.phone,
            email=client.email,
            hashed_password=client.password,
        )

        return new_client


@clients_router.get("/", response_model=list[ClientShow])
async def get_clients(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    offset: int = 0,
    limit: int = 10,
):
    async with session.begin():
        client_dal = ClientDAL(session)
        clients = await client_dal.get_clients(offset, limit)
        return clients


@clients_router.get("/{id}", response_model=ClientShow)
async def get_client(
    id: int, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        client_dal = ClientDAL(session)
        client = await client_dal.get_client_by_id(id, include_his_room_orders=True)

        if client is None:
            raise create_http_exception(
                status_code=404, reason="client with provided id does not exist", id=id
            )

        return client


@clients_router.put("/{id}")
async def update_client(
    id: int,
    updated_client: ClientUpdate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    async with session.begin():
        client_dal = ClientDAL(session)
        updated_client_id = await client_dal.update_client(
            id, **updated_client.dict(exclude_unset=True)
        )

        return {"id": updated_client_id}
