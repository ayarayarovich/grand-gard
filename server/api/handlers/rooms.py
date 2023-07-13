from typing import Annotated
from fastapi import APIRouter, Depends
from api.schemes import RoomShow, RoomCreate, RoomUpdate
from database.dals import RoomDAL
from database.session import AsyncSession, get_db_session
from shared import create_http_exception


from api.schemes import RoomOrderShow


rooms_router = APIRouter()
@rooms_router.post("/")
async def create_room(
    rooms: RoomCreate, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        room_dal = RoomDAL(session)

        new_room = await room_dal.create_room(
        type_room=rooms.type_room,
        price=rooms.price,
        area=rooms.area,
        max_quest=rooms.max_quest,
        is_active=True
        )

        return new_room

@rooms_router.get("/{id}",response_model=RoomShow) #предоставление информации
async def get_room_by_id(
    id: int, session: Annotated[AsyncSession, Depends(get_db_session)]
):
    async with session.begin():
        room_dal = RoomDAL(session)



        room = await room_dal.get_room_by_id(id)
        if room is None:
            raise create_http_exception(
                status_code=404, reason="room with provided id does not exist", id=id
            )
        return room



@rooms_router.put("/{id}", response_model=RoomShow) #обновление
async def update_room(
    id: int,

    values_to_update: RoomUpdate,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    async with session.begin():
        room_dal = RoomDAL(session)
        updated_room = await room_dal.update_room(
            id, **values_to_update.dict(exclude_unset=True)
        )

        room = await room_dal.get_room_by_id(id)
        if room is None:
            raise create_http_exception(
                status_code=404, reason="room with provided id does not exist", id=id
            )

        return updated_room



#----------------------

@rooms_router.get("/", response_model=list[RoomShow])
async def get_rooms(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    offset: int = 0,
    limit: int = 10,
):
    async with session.begin():
         room_dal = RoomDAL(session)
         rooms = await room_dal.get_rooms(offset, limit)
         if limit > 10:
             raise create_http_exception(
                 status_code=416, reason="you cannot output more than 10 rooms ", id=id
             )
         return rooms



@rooms_router.delete("/{id}")
async def delete_room(id: int, session: Annotated[AsyncSession, Depends(get_db_session)]):

    async with session.begin():
        room_dal = RoomDAL(session)

        room = await room_dal.get_room_by_id(id)
        if room is None:
            raise create_http_exception(
                status_code=404, reason="room with provided id does not exist", id=id
            )
        deleted_room_id=await room_dal.delete_room(id)
        return {deleted_room_id: "is deleted"}









#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



@rooms_router.get("/", response_model=list[RoomOrderShow])
async def get_rooms_order(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    offset: int = 0,
    limit: int = 10,
):
    async with session.begin():
         room_dal = RoomDAL(session)
         rooms = await room_dal.get_rooms(offset, limit)
         return rooms
