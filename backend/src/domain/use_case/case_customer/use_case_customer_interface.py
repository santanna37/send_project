from src.domain.models.model_customer import CustomerModel
from abc import ABC, abstractmethod
from typing import Dict



class UseCaseCustomerInterface(ABC):

    @abstractmethod
    def create(self, model: CustomerModel) -> CustomerModel: pass 

    @abstractmethod
    def reader(self, cnpj: str, id_person: int) -> Dict: pass 
