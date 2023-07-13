from fastapi import FastAPI

from api.handlers import clients_router, employees_router, rooms_router, services_router,posts_router, roomOrders_router, bookings_router


app = FastAPI()

app.include_router(clients_router, prefix="/clients", tags=["clients"])
app.include_router(employees_router, prefix="/employees", tags=["employees"])
app.include_router(rooms_router, prefix="/rooms", tags=["rooms"])
app.include_router(services_router, prefix="/services", tags=["services"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])
app.include_router(roomOrders_router, prefix="/roomOrders", tags=["roomOrders"])
app.include_router(bookings_router, prefix="/bookings", tags=["bookings"])