import datetime
from decimal import Decimal
from enum import Enum

import sqlalchemy as sa
import sqlalchemy.orm as so


class PermissionsEnum(Enum):
    EMPLOYEES_CREATE = "employees:create"
    EMPLOYEES_READ = "employees:read"
    EMPLOYEES_UPDATE = "employees:update"
    EMPLOYEES_DELETE = "employees:delete"

    CLIENTS_CREATE = "clients:create"
    CLIENTS_READ = "clients:read"
    CLIENTS_UPDATE = "clients:update"
    CLIENTS_DELETE = "clients:delete"

    BOOKING_CREATE = "booking:create"
    BOOKING_READ = "booking:read"
    BOOKING_UPDATE = "booking:update"
    BOOKING_DELETE = "booking:delete"

    SERVICES_CREATE = "services:create"
    SERVICES_READ = "services:read"
    SERVICES_UPDATE = "services:update"
    SERVICES_DELETE = "services:delete"

    ROOMS_CREATE = "rooms:create"
    ROOMS_READ = "rooms:read"
    ROOMS_UPDATE = "rooms:update"
    ROOMS_DELETE = "rooms:delete"

    SERVICE_ORDERS_CREATE = "service_orders:create"
    SERVICE_ORDERS_READ = "service_orders:read"
    SERVICE_ORDERS_UPDATE = "service_orders:update"
    SERVICE_ORDERS_DELETE = "service_orders:delete"


class Base(so.DeclarativeBase):
    pass


class ClientRoomOrderSecondary(Base):
    __tablename__ = "client_room_order_secondary"

    room_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("room_order.id"), primary_key=True
    )
    client_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("client.id"), primary_key=True
    )


class Client(Base):
    __tablename__ = "client"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    room_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("room.id"), nullable=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(75), nullable=False)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(75), nullable=False)
    middle_name: so.Mapped[str] = so.mapped_column(sa.String(75), nullable=False)
    phone: so.Mapped[str] = so.mapped_column(sa.String(20), nullable=False)
    email: so.Mapped[str] = so.mapped_column(
        sa.String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: so.Mapped[str] = so.mapped_column(
        sa.String(length=1024), nullable=False
    )
    is_active: so.Mapped[bool] = so.mapped_column(nullable=False)

    room_orders: so.Mapped[list["RoomOrder"]] = so.relationship(
        secondary="client_room_order_secondary", back_populates="clients"
    )
    bookings: so.Mapped[list["Booking"]] = so.relationship(back_populates="client")


class Room(Base):
    __tablename__ = "room"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    type_room: so.Mapped[str] = so.mapped_column(sa.String(50), nullable=False)
    price: so.Mapped[Decimal] = so.mapped_column(sa.DECIMAL(10, 2), nullable=False)
    area: so.Mapped[int] = so.mapped_column(nullable=False)
    max_quest: so.Mapped[int] = so.mapped_column(nullable=False)
    is_active: so.Mapped[bool] = so.mapped_column(nullable=False, default=True)


class Employee(Base):
    __tablename__ = "employee"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    post_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("post.id", ondelete="SET NULL"), nullable=True
    )
    post: so.Mapped["Post"] = so.relationship()
    username: so.Mapped[str] = so.mapped_column(
        sa.String(50), unique=True, nullable=False
    )
    hashed_password: so.Mapped[str] = so.mapped_column(
        sa.String(length=1024), nullable=False
    )
    is_active: so.Mapped[bool] = so.mapped_column(nullable=False)


class Post(Base):
    __tablename__ = "post"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(50), unique=True, nullable=False)
    permissions: so.Mapped[list[PermissionsEnum]] = so.mapped_column(
        sa.ARRAY(sa.String(30)), nullable=True
    )

    employees: so.Mapped[list[Employee]] = so.relationship(back_populates="post")


class Service(Base):
    __tablename__ = "service"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False)
    price: so.Mapped[Decimal] = so.mapped_column(sa.DECIMAL(10, 2), nullable=False)
    is_active: so.Mapped[bool] = so.mapped_column(nullable=False, default=True)


class ServiceOrderStatusEnum(Enum):
    fulfilled = 1
    canceled = 2
    in_process = 3
    accepted = 4


class ServiceOrder(Base):
    __tablename__ = "service_order"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)

    service_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("service.id"), nullable=False
    )
    service: so.Mapped[Service] = so.relationship()

    client_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("client.id"), nullable=False
    )
    client: so.Mapped[Client] = so.relationship()

    room_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("room.id"), nullable=False)
    room: so.Mapped[Room] = so.relationship()

    status: so.Mapped[ServiceOrderStatusEnum] = so.mapped_column(
        sa.Enum(ServiceOrderStatusEnum),
        nullable=False,
        default=ServiceOrderStatusEnum.accepted,
    )
    created_at: so.Mapped[datetime.datetime] = so.mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now()
    )


class RoomOrder(Base):
    __tablename__ = "room_order"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)

    room_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("room.id"), nullable=False)
    room: so.Mapped[Room] = so.relationship()

    paying_client_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("client.id"), nullable=False
    )
    paying_client: so.Mapped[Client] = so.relationship()

    date_in: so.Mapped[datetime.date] = so.mapped_column(sa.Date, nullable=False)
    date_out: so.Mapped[datetime.date] = so.mapped_column(sa.Date, nullable=False)

    clients: so.Mapped[list[Client]] = so.relationship(
        secondary="client_room_order_secondary", back_populates="room_orders"
    )
    created_at: so.Mapped[datetime.datetime] = so.mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now()
    )


class BookingStatusEnum(Enum):
    active = 1
    canceled = 2


class Booking(Base):
    __tablename__ = "booking"

    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)

    room_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("room.id"), nullable=False)
    room: so.Mapped[Room] = so.relationship()

    client_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey("client.id"), nullable=False
    )
    client: so.Mapped[Client] = so.relationship()

    date_in: so.Mapped[datetime.date] = so.mapped_column(sa.Date, nullable=False)
    date_out: so.Mapped[datetime.date] = so.mapped_column(sa.Date, nullable=False)

    status: so.Mapped[BookingStatusEnum] = so.mapped_column(
        sa.Enum(BookingStatusEnum), nullable=False
    )
    number_of_guests: so.Mapped[int] = so.mapped_column(nullable=False)

    created_at: so.Mapped[datetime.datetime] = so.mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now()
    )
