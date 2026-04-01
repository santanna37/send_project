from src.infra.db.repositores.repository_person import PersonRepository
from src.data.use_case.case_person.use_case_person import UseCasePerson
from src.presentation.controllers.controller_person import PersonController
from src.presentation.dto.dto_person import DTOPerson
from src.presentation.validator.validator_person import PersonValidator

class PersonCompose:

    @staticmethod
    def person_register():

        validator = PersonValidator()
        dto = DTOPerson(validator= validator)

        repository = PersonRepository()
        use_case = UseCasePerson(repository= repository)
        controller = PersonController(use_case= use_case,dto= dto)

        return controller.handler
