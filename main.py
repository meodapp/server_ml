from fastapi import FastAPI

from api import model

app = FastAPI()
app.include_router(model.router)

