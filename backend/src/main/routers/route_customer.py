from src.main.adapter.adapter_customer import customer_adapter_create, customer_adapter_reader
from src.main.adapter.adapter_jwt_bearer import JWTBearer
from fastapi import APIRouter, Depends, Request
from typing import Dict



router = APIRouter(prefix="/customer", tags=["Customer"])
auth = JWTBearer()


@router.post("/")
async def register_customer(request: Request, token_data: Dict = Depends(auth)):
    return await customer_adapter_create(request= request, token_data= token_data)

@router.get("/")
async def reader_customer(request: Request, token_data: Dict = Depends(auth)):
    print(f" entrada token -> {token_data}")
    return await customer_adapter_reader(request= request, token_data= token_data)