from fastapi import APIRouter, Request
from  src.main.adapter.adapter_person import person_adapter_create, person_adapter_login


router = APIRouter(prefix="/person", tags=["Person"])



@router.post("/register")
async def create_person_router(request: Request):
    return await person_adapter_create(request=request)


@router.post("/login")
async def login_person_router(request: Request):
    return await person_adapter_login(request= request)