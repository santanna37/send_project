from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.infra.auth.token_data import Token
from src.presentation.http_types.status_code import HTTPStatus
from typing import Dict



class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.__validator = Token()

    async def __call__(self, request: Request) -> Dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if not credentials or credentials.scheme != "Bearer":
            raise HTTPException(status_code=HTTPStatus.BAD_GATEWAY, detail= "token invalido ou ausente")

        try:
            return self.__validator.decode(credentials.credentials)
        except ValueError as error:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error))