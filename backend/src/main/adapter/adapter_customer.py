from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from  src.presentation.http_types.http_request import HttpRequest
from src.main.composers.composer_customer import CustomerCompose
from typing import Dict



composer = CustomerCompose()


async def customer_adapter_create(request: Request, token_data: Dict):
    
    body = await request.json()

    http_request = HttpRequest(body= body, token_data= token_data)

    handler = composer.customer_create()

    http_response = handler(http_request= http_request)

    return JSONResponse(status_code= http_response.status_code,
                        content= str(http_response.body))


async def customer_adapter_reader(request: Request, token_data: Dict):

    query_params = dict(request.query_params)

    http_request = HttpRequest(query_params = query_params, token_data = token_data)

    handler = composer.customer_reader()

    http_response = handler(http_request= http_request)

    list_customer = http_response.body["list_customer"]

    # ✅ Serializa cada CustomerModel individualmente -> passar para DTO
    serialized_customers = []
    for item in list_customer:
        if hasattr(item, "model_dump"):      # Pydantic v2
            serialized_customers.append(item.model_dump())
        elif hasattr(item, "dict"):          # Pydantic v1
            serialized_customers.append(item.dict())
        elif isinstance(item, dict):         # já é dict
            serialized_customers.append(item)
        else:
            serialized_customers.append(str(item))  # fallback de segurança

    return JSONResponse(
        status_code=http_response.status_code,
        content={
            "list_customer": serialized_customers,
            "count_customers": http_response.body["count_customers"]  # ✅ typo corrigido (era count_customer)
        }
    )