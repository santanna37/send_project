from src.presentation.validator.validator_person import PersonValidator
from src.domain.models.model_person import PersonModel
from typing import Dict, TypeVar, Type



M = TypeVar("M", bound = PersonModel)

class DTOPerson:

    def __init__(self, validator: PersonValidator) -> None:

        self._validator = validator
    
    
    def dto_person_create(self, person_dict: Dict) -> PersonModel:
        new_person = PersonModel(
            name = self._validator.name_validator(name=person_dict.get("name")),
            cpf = self._validator.cpf_validator(cpf = person_dict.get("cpf")),
            cnpj = self._validator.cnpj_validator(cnpj = person_dict.get("cnpj")),
            phone = self._validator.phone_validator(phone = person_dict.get("phone")),
            email = self._validator.email_validador(email_person = person_dict.get("email")),
            password = self._validator.password_validator(password= person_dict.get("password"))
        )
        return new_person

    def dto_person_response(self, person_model: PersonModel) -> Dict:
        new_person = {
            "name": person_model.name,
            "email": person_model.email,
            "cpf": person_model.cpf
        }
        return new_person

    def dto_person_login(self, email: str, password: str) -> Dict:
        email_person = self._validator.email_validador(email_person= email)
        password_person = self._validator.password_validator(password= password)

        return {
            "email": email_person, 
            "password": password_person
                }
