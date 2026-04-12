from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse

from abc import ABC, abstractmethod



class CustomerControllerInterface(ABC):

    @abstractmethod
    def create(self, http_request: HttpRequest) -> HttpResponse: pass

    @abstractmethod
    def read(self, http_request: HttpRequest) -> HttpResponse: pass