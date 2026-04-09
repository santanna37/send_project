from src.domain.models.model_customer import CustomerModel


from abc import ABC, abstractmethod
from typing import List, Dict



class CustomerRepositoryInterface(ABC):

    @abstractmethod
    def create_customer(self, model_customer: CustomerModel) -> CustomerModel: pass

    @abstractmethod
    def read_customer(self, id_person: int = None, cnpj: str = None) ->List: pass 