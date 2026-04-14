from fastapi import FastAPI
from src.main.routers.route_person import  router as person_router
from src.main.routers.route_customer import router as customer_router
from src.main.routers.route_email import router as email_router



app = FastAPI()

app.include_router(person_router)
app.include_router(customer_router)
app.include_router(email_router)
