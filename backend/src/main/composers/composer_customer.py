from src.infra.db.repositores.repository_customer import CustomerRepository
from src.data.use_case.case_customer.use_case_customer import UseCaseCustomer
from src.presentation.controllers.controller_customes import CustomerController
from src.presentation.dto.dto_customer import DTOCustomer
from src.presentation.validator.validator_customer import CustomerValidator
from src.infra.db.mappers.mapper import DataMapper
from src.infra.auth.token_data import Token
from src.infra.crypto.hash_data import CryptoHash



class CustomerCompose:

    def __init__(self):
        self._validator = CustomerValidator()
        self._dto = DTOCustomer(validator= self._validator)

        self._mapper = DataMapper()
        self._repository = CustomerRepository(mapper= self._mapper)
        self._use_case = UseCaseCustomer(repository= self._repository)
    
    def customer_create(self):
        controller = CustomerController(use_case= self._use_case, dto= self._dto)
        return controller.create

    def customer_reader(self):
        controller = CustomerController(use_case= self._use_case, dto= self._dto)
        return controller.read