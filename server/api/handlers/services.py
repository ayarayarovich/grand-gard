from typing import Annotated
from fastapi import APIRouter, Depends
from api.schemes import ServiceShow, ServiceCreate, ServiceUpdate
from database.dals import ServiceDAL
from database.session import AsyncSession, get_db_session
from shared import create_http_exception

services_router = APIRouter()
@services_router.post("/")
async def create_service(
    service: ServiceCreate, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        service_dal = ServiceDAL(session)

        new_service = await service_dal.create_service(
        name=service.name,
        price=service.price,
        is_active=True,
        )

        return new_service

@services_router.get("/{id}", response_model=ServiceShow) #предоставление информации
async def get_service_by_id(
    id: int, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        service_dal = ServiceDAL(session)

        service = await service_dal.get_service_by_id(id)
        if service is None:
            raise create_http_exception(
                status_code=404, reason="service with provided id does not exist", id=id
            )
        return service



@services_router.put("/{id}", response_model=ServiceShow) #обновление
async def update_service(
    id: int,
    values_to_update: ServiceUpdate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    async with session.begin():
        service_dal = ServiceDAL(session)
        updated_service = await service_dal.update_service(
            id, **values_to_update.dict(exclude_unset=True)
        )

        service = await service_dal.get_service_by_id(id)
        if service is None:
            raise create_http_exception(
                status_code=404, reason="service with provided id does not exist", id=id
            )
        return updated_service



#----------------------

@services_router.get("/", response_model=list[ServiceShow])
async def get_services(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    offset: int = 0,
    limit: int = 10,
):
    async with session.begin():
         service_dal = ServiceDAL(session)
         service = await service_dal.get_sr(offset, limit)
         if limit > 10:
             raise create_http_exception(
                 status_code=416, reason="you cannot output more than 10 services ", id=id
             )
         return service



@services_router.delete("/{id}")
async def delete_service(id: int, session: Annotated[AsyncSession, Depends(get_db_session)]):

    async with session.begin():
        service_dal = ServiceDAL(session)

        service = await service_dal.get_service_by_id(id)
        if service is None:
            raise create_http_exception(
                status_code=404, reason="service with provided id does not exist", id=id
            )
        deleted_service_id=await service_dal.delete_service(id)
        return {deleted_service_id: "is deleted"}