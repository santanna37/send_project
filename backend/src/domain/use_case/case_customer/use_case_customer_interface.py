from src.domain.models.model_customer import CustomerModel
from abc import ABC, abstractmethod



class UseCaseCustomerInterface(ABC):

    @abstractmethod
    def create(self, model: CustomerModel) -> CustomerModel: pass 

    @abstractmethod
    def reader(self, cnpj: str, id_person: int): pass 