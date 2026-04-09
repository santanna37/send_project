from src.infra.db.repositores.repository_person import PersonRepository
from src.data.use_case.case_person.use_case_person import UseCasePerson
from src.presentation.controllers.controller_person import PersonController
from src.presentation.dto.dto_person import DTOPerson
from src.presentation.validator.validator_person import PersonValidator
from src.infra.db.mappers.mapper import DataMapper
from src.infra.auth.token_data import Token
from src.infra.crypto.hash_data import CryptoHash

class PersonCompose:

    def __init__(self):
        self._validator = PersonValidator()
        self._dto = DTOPerson(validator= self._validator)
        
        self._mapper = DataMapper()
        self._repository = PersonRepository(mapper=self._mapper)
        
        self.__token = Token()
        self._hash = CryptoHash()
        self._use_case = UseCasePerson(repository= self._repository,
                                        hash_person= self._hash,
                                        token= self.__token
        )


    def person_register(self):
        controller = PersonController(use_case= self._use_case, dto= self._dto)
        
        return controller.create 

    def person_login(self):
        controller = PersonController(use_case= self._use_case, dto= self._dto)

        return controller.login