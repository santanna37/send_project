from src.infra.db.entities.entity_person import PersonEntity
from src.infra.db.mappers.mapper_person import PersonMapper
from src.domain.models.model_person import PersonModel
from abc import ABC, abstractmethod
from typing import List



class PersonRepositoryInterface(ABC):

    @abstractmethod
    def create_person(self, person: PersonModel) -> str: pass  


    @abstractmethod
    def read_person(self, name: str) ->List: pass


    @abstractmethod
    def update_person(self, name: str, new_data: PersonModel) -> PersonModel: pass


    # @abstractmethod
    # def delete_person(self, name: str) -> PersonModel:pass 
