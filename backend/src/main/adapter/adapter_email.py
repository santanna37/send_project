from fastapi import Request, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from src.presentation.http_types.http_request import HttpRequest
from src.main.composers.composer_email import EmailCompose
from typing import Dict, List

composer = EmailCompose()

async def email_adapter_multi_sender(
    files: List[UploadFile],
    token_data: Dict
):
    # lê todos os PDFs em memória — sem salvar no disco
    list_pdfs = []
    for file in files:
        pdf_bytes = await file.read()
        list_pdfs.append({
            "bytes": pdf_bytes,
            "name": file.filename
        })

    http_request = HttpRequest(
        body={"pdfs": list_pdfs},
        token_data=token_data
    )

    handler = composer.email_multi_sender()
    http_response = handler(http_request=http_request)

    return JSONResponse(
        status_code=http_response.status_code,
        content=http_response.body
    )