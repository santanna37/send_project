from src.data.interface.repository_person_interface import PersonRepositoryInterface
from src.domain.models.model_person import PersonModel
from src.domain.use_case.case_person.use_case_person_interface import UseCasePersonInterface
from typing import List, Dict
from src.infra.db.mappers.mapper_person import PersonMapper




class UseCasePerson(UseCasePersonInterface):

    def __init__(self, repository: PersonRepositoryInterface):
        self.__repository = repository

    def create(self, person: PersonModel) -> Dict:
        new_person = self.__repository.create_person(person= person)

        return PersonMapper.domain_to_dict(new_person)

    def read(self, name:str) -> List:
        list_person = self.__repository.read_person(name= name)

        return list_person

    def update(self, name:str, new_data:PersonModel) -> str:
        up_person = self.__repository.update_person(name= name, new_data= new_data)

        return up_person