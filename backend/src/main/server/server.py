from fastapi import FastAPI
from src.main.routers.route_person import  router as person_router



app = FastAPI()

app.include_router(person_router)
