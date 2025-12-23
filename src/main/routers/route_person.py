from fastapi import APIRouter, Request
from  src.main.adapter.adapter_person import person_adapter_create


router = APIRouter(prefix="/person", tags=["Person"])



@router.post("/")
async def create_person_router(request: Request):
    return await person_adapter_create(request=request)
    
