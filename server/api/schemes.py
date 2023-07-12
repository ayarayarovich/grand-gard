import datetime

from pydantic import BaseModel, EmailStr

from database.models import PermissionsEnum, BookingStatusEnum, ServiceOrderStatusEnum


class Token(BaseModel):
    access_token: str
    token_type: str


class ShowModel(BaseModel):
    class Config:
        orm_mode = True


class ClientCreate(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    email: EmailStr
    password: str


class ClientShow(ShowModel):
    id: int
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    email: EmailStr
    is_active: bool


class ClientUpdate(BaseModel):
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    phone: str | None


class RoomShow(ShowModel):
    id: int
    type_room: str
    price: float
    area: int
    max_quest: int
    is_active: bool


class RoomCreate(BaseModel):
    type_room: str
    price: float
    area: int
    max_quest: int
    is_active: bool


class RoomUpdate(BaseModel):
    type_room: str | None
    price: float | None
    area: int | None
    max_quest: int | None
    is_active: bool | None


class PostShow(ShowModel):
    id: int
    name: str
    permissions: list[PermissionsEnum]


class PostCreate(BaseModel):
    name: str
    permissions: list[PermissionsEnum] | None


class PostUpdate(BaseModel):
    name: str | None
    permissions: list[PermissionsEnum] | None


class EmployeeShow(ShowModel):
    id: int
    username: str
    post: PostShow
    is_active: bool


class EmployeeCreate(BaseModel):
    username: str
    password: str
    post: PostCreate


class EmployeeUpdate(BaseModel):
    username: str | None
    password: str | None
    post_id: int | None


class RoomOrderShow(ShowModel):
    id: int
    paying_client: ClientShow
    date_in: datetime.date
    date_out: datetime.date
    room: RoomShow


class RoomOrderCreate(BaseModel):
    paying_client_id: int
    date_in: datetime.date
    date_out: datetime.date
    room_id: int


class ServiceShow(ShowModel):
    id: int
    name: str
    price: float
    is_active: bool


class ServiceCreate(BaseModel):
    name: str
    price: float
    is_active: bool


class ServiceUpdate(BaseModel):
    name: str | None
    price: float | None
    is_active: bool | None


class ServiceOrderShow(ShowModel):
    id: int
    service: ServiceShow
    client: ClientShow
    room: RoomShow
    status: ServiceOrderStatusEnum
    created_at: datetime.datetime


class ServiceOrderCreate(BaseModel):
    service_id: int
    client_id: int
    room_id: int


class BookingShow(ShowModel):
    id: int
    room: RoomShow
    client: ClientShow
    date_in: datetime.date
    date_out: datetime.date
    status: BookingStatusEnum
    number_of_guests: int
    created_at: datetime.datetime


class BookingCreate(BaseModel):
    room_id: int
    client_id: int
    date_in: datetime.date
    date_out: datetime.date
    number_of_guests: int

