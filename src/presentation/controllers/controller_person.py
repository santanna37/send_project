from src.presentation.validator.validator_person import PersonValidator
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_case.case_person.use_case_person_interface import UseCasePersonInterface
from src.presentation.interfaces.controller_person_interface import PersonControllerInterface
from src.presentation.dto.dto_person import DTOPerson
from src.infra.db.mappers.mapper_person import PersonMapper
from src.presentation.http_types.status_code import HTTPStatus


class  PersonController(PersonControllerInterface):


    def __init__(self, use_case: UseCasePersonInterface, dto: DTOPerson):
        self._use_case = use_case
        self._dto = dto

    def handler(self, http_request: HttpRequest) -> HttpResponse:

        try:
            person_model = self._dto.dto_person_create(person_dict= http_request.body)

            result = self._use_case.create(person= person_model)


            return HttpResponse(status_code = HTTPStatus.CREATED, body = result)

        except ValueError as error:
            return HttpResponse(status_code = HTTPStatus.BAD_REQUEST,
                                body= { 'error': str(error)})
