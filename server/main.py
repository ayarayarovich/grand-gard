from fastapi import FastAPI

from api.handlers import clients_router, employees_router


app = FastAPI()

app.include_router(clients_router, prefix="/clients", tags=["clients"])
app.include_router(employees_router, prefix="/employees", tags=["employees"])
