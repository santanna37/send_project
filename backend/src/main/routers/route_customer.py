from fastapi import APIRouter, Depends
from typing import Dict
from src.main.adapter.adapter_jwt_bearer import JWTBearer



router = APIRouter(prefix="/customer", tags=["Customer"])
auth = JWTBearer()


@router.post("/")
async def register_customer(body: Dict, token_data: Dict = Depends(auth)):
    pass