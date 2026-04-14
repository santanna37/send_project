from src.presentation.validator.validator_customer import CustomerValidator
from src.domain.models.model_customer import CustomerModel
from typing import List, Dict, Type, TypeVar



class DTOEmail:

    def __init__(self, validator: CustomerValidator) -> None:
        self._validator = validator

    def dto_email_sender(self, id_person: str) -> Dict:
        id_person = self._validator.id_person_validator(id_person= id_person)
        return id_person

