from fastapi import FastAPI
from src.main.routers.route_person import  router as person_router
from src.main.routers.route_customer import router as customer_router
from src.main.routers.route_email import router as email_router
import os 


app = FastAPI()



if os.getenv("AMBIENTE") == "LOCAL":

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(person_router)
    app.include_router(log_router)

elif os.getenv("AMBIENTE") == "ONLINE":

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://send-project-one.vercel.app"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(person_router)
app.include_router(customer_router)
app.include_router(email_router)
