from src.presentation.validator.validator_person import PersonValidator
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_case.case_person.use_case_person_interface import UseCasePersonInterface
from abc import ABC, abstractmethod



class PersonControllerInterface(ABC):

    @abstractmethod
    def handler(self, http_request: HttpRequest) -> HttpResponse: pass
