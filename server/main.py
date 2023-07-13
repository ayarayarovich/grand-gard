from fastapi import FastAPI

from api.handlers import clients_router, employees_router, rooms_router, services_router,posts_router,bookings_router

app = FastAPI()

app.include_router(clients_router, prefix="/clients", tags=["clients"])
app.include_router(employees_router, prefix="/employees", tags=["employees"])
app.include_router(rooms_router, prefix="/rooms", tags=["rooms"])
app.include_router(services_router, prefix="/services", tags=["services"])
app.include_router(bookings_router, prefix="/bookings", tags=["booking"])
app.include_router(posts_router, prefix="/posts", tags=["posts"])

