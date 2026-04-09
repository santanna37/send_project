from src.presentation.validator.validator_person import PersonValidator
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_case.case_person.use_case_person_interface import UseCasePersonInterface
from src.presentation.interfaces.controller_person_interface import PersonControllerInterface
from src.presentation.dto.dto_person import DTOPerson
from src.infra.db.mappers.mapper import DataMapper
from src.presentation.http_types.status_code import HTTPStatus


class  PersonController(PersonControllerInterface):


    def __init__(self, use_case: UseCasePersonInterface, dto: DTOPerson):
        self._use_case = use_case
        self._dto = dto

    def create(self, http_request: HttpRequest) -> HttpResponse:

        try:
            person_model = self._dto.dto_person_create(person_dict= http_request.body)
            result = self._use_case.create(person= person_model)
            result = self._dto.dto_person_response(person_model= result)
            
            return HttpResponse(status_code = HTTPStatus.CREATED, body = result)

        except ValueError as error:
            return HttpResponse(status_code = HTTPStatus.BAD_REQUEST,
                                body= { 'error': str(error)})

    def login(self,http_request: HttpRequest) -> HttpResponse:

        try:
            data_person = self._dto.dto_person_login(
                email= http_request.body.get("email"),
                password= http_request.body.get("password")
            )

            result = self._use_case.login(email= data_person.get("email"), password= data_person.get("password"))
            
            return HttpResponse(status_code= HTTPStatus.ACCEPTED, body = result) 
        except Exception as exception:
            return HttpResponse(status_code=HTTPStatus.BAD_REQUEST, body= f"falha no login {exception}")