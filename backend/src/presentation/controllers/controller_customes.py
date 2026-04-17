from src.presentation.validator.validator_customer import CustomerValidator
from src.presentation.http_types.http_request import HttpRequest
from src.presentation.http_types.http_response import HttpResponse
from src.domain.use_case.case_customer.use_case_customer_interface import UseCaseCustomerInterface
from src.presentation.interfaces.controller_customer_interface import CustomerControllerInterface 
from src.presentation.dto.dto_customer import DTOCustomer
from src.infra.db.mappers.mapper import DataMapper
from src.presentation.http_types.status_code import HTTPStatus


class  CustomerController(CustomerControllerInterface):

    def __init__(self, use_case: UseCaseCustomerInterface, dto: DTOCustomer):
        self._use_case = use_case
        self._dto = dto

    def create(self, http_request: HttpRequest) -> HttpResponse:
        try:
            customer_model = self._dto.dto_customer_create(customer_dict= http_request.body,id_person= http_request.token_data.get("sub"))
            result = self._use_case.create(model= customer_model)
            
            return HttpResponse(status_code= HTTPStatus.CREATED, body = result)
        
        except Exception as exception:
            return HttpResponse(status_code= HTTPStatus.BAD_REQUEST, body= {"erro": exception})
    
    def read(self, http_request: HttpRequest) -> HttpResponse:
        try:
            query_params = http_request.query_params
            data_share = self._dto.dto_customer_reader(cnpj= query_params.get("cnpj"), id_person= http_request.token_data.get("sub"))
            print(f" data -> {data_share}")
            result = self._use_case.reader(cnpj= data_share.get("cnpj"), id_person= data_share.get("id_person"))

            return HttpResponse(status_code= HTTPStatus.OK, body= {
                "list_customer": result.get("list_customer"),
                "count_customers": result.get("count_customers")
            })
        except Exception as exception:
            return HttpResponse(status_code= HTTPStatus.BAD_REQUEST, body= {"error": exception})