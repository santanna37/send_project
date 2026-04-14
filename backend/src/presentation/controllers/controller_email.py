from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.presentation.http_types.status_code import HTTPStatus
from src.presentation.validator.validator_customer import CustomerValidator
from src.domain.use_case.case_email.use_case_email_interface import UseCaseEmailInterface
from src.presentation.interfaces.controller_email_interface import EmailControllerInterface
from src.presentation.dto.dto_email import DTOEmail
from src.infra.db.mappers.mapper import DataMapper
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)



class EmailController(EmailControllerInterface):

    def __init__(self, use_case: UseCaseEmailInterface, dto: DTOEmail):
        self._validator = CustomerValidator
        self._use_case = use_case
        self._dto = dto

    def multi_sender(self, http_request: HttpRequest) -> HttpResponse: 
        try:
            id_person = self._dto.dto_email_sender(id_person= http_request.token_data["sub"])
            pdf_paths = http_request.body.get("pdfs")
            list_customer = self._use_case.get_email_list(id_person= id_person)
            print(f" lista customer => {list_customer}")
                        
            response = self._use_case.trigger_email(list_email= list_customer, list_pdf= pdf_paths)
            return HttpResponse(status_code= HTTPStatus.OK, body= {"response": response})
        
        except Exception as exception:
            return HttpResponse(status_code= HTTPStatus.BAD_REQUEST, body= {"response_error": str(exception)})