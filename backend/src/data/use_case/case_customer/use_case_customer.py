from src.domain.use_case.case_customer.use_case_customer_interface import UseCaseCustomerInterface
from src.data.interface.repository_customer_interface import CustomerRepositoryInterface
from src.domain.models.model_customer import CustomerModel

from typing import Dict, List




class UseCaseCustomer(UseCaseCustomerInterface):

    def __init__(self, repository: CustomerRepositoryInterface):
        self.__repository = repository

    def create(self, model: CustomerModel) -> CustomerModel:
        new_customer = self.__repository.create_customer(model_customer= model)
        return new_customer


    def reader(self, cnpj: str, id_person: int) -> Dict:
        
        try:
            if cnpj is not None:
                customer_list = self.__repository.read_customer(id_person= id_person, cnpj= cnpj)
            else:
                customer_list = self.__repository.read_customer(id_person= id_person)
            
            return {
                "list_customer": customer_list,
                "count_customers": len(customer_list)
            }
        except Exception as exception:
            return {
                "response":"lista nao encontrada",
                "error": exception
            }


