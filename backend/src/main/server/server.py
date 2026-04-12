from fastapi import FastAPI
from src.main.routers.route_person import  router as person_router
from src.main.routers.route_customer import router as customer_customer



app = FastAPI()

app.include_router(person_router)
app.include_router(customer_customer)
