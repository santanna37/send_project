from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from abc import ABC, abstractmethod
from typing import Dict, List



class EmailControllerInterface(ABC):

#    @abstractmethod
#    def single_sender(self, http_request: HttpRequest) -> HttpResponse: pass

    @abstractmethod
    def  multi_sender(self, http_request: HttpRequest) -> HttpResponse: pass
