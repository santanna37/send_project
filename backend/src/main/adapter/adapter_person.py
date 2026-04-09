from fastapi import Request
from fastapi.responses import JSONResponse
from src.presentation.http_types.http_request import HttpRequest
from src.main.composers.composer_person import PersonCompose

composer = PersonCompose()


async def person_adapter_create(request: Request):
    
    body = await request.json()

    http_request = HttpRequest(body= body)

    handler = composer.person_register()

    http_response = handler(http_request= http_request)

    return JSONResponse(status_code= http_response.status_code,
                        content= http_response.body)


async def person_adapter_login(request: Request):
    body = await request.json()

    http_request = HttpRequest(body= body)

    handler = composer.person_login()

    http_response = handler(http_request= http_request)

    return JSONResponse(status_code= http_response.status_code,
                        content= http_response.body)
