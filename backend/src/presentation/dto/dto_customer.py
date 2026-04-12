from src.presentation.validator.validator_customer import CustomerValidator
from src.domain.models.model_customer import CustomerModel
from typing import List, Dict, Type, TypeVar



M = TypeVar("M", bound=CustomerModel)

class DTOCustomer:

    def __init__(self, validator: CustomerValidator) -> None:
        self._validator = validator


    def dto_customer_create(self, customer_dict: Dict, id_person: str) -> CustomerModel:
        id_person = id_person
        new_customer = CustomerModel(
            name = self._validator.name_validator(name= customer_dict.get("name")),
            cnpj = self._validator.cnpj_validator(cnpj= customer_dict.get("cnpj")),
            phone = self._validator.phone_validator(phone = customer_dict.get("phone")),
            email = self._validator.email_validator(email= customer_dict.get("email")),
            id_person = self._validator.id_person_validator(id_person= id_person)
        )
        
        return new_customer

    def dto_customer_reader(self, cnpj: str, id_person: str) -> Dict:
        return {
            "cnpj": self._validator.cnpj_validator(cnpj= cnpj),
            "id_person": self._validator.id_person_validator(id_person= id_person)
        }
