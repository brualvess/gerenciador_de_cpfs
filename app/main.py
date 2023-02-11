from .database.database import engine
from .database import models
from fastapi import FastAPI
from .routers import cpf

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(cpf.router)


