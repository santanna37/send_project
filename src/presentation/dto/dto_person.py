from src.presentation.validator.validator_person import PersonValidator
from src.domain.models.model_person import PersonModel
from typing import Dict


class DTOPerson:

    def __init__(self, validator: PersonValidator) -> None:

        self._validator = validator
    
    
    def dto_person_create(self, person_dict: Dict) -> Dict:
        name = person_dict.get("name")
        email = person_dict.get("email")
        name_person = self._validator.name_validator(name = name)
        email_person = self._validator.email_validador(email_person = email)

        body_person = PersonModel(
                                name= name_person,
                                email= email_person
        )

        return body_person
