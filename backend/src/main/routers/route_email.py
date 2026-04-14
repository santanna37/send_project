from fastapi import APIRouter, Depends, UploadFile, File
from src.main.adapter.adapter_jwt_bearer import JWTBearer
from src.main.adapter.adapter_email import email_adapter_multi_sender
from typing import Dict, List



router = APIRouter(prefix="/email", tags=["Email"])
auth = JWTBearer()

@router.post("/multi_send")
async def multi_sender(
    files: List[UploadFile] = File(...),  # recebe vários PDFs
    token_data: Dict = Depends(auth)
):
    return await email_adapter_multi_sender(
        files=files,
        token_data=token_data
    )