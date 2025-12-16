from src.data.interface.repository_person_interface import PersonRepositoryInterface
from src.infra.db.mappers.mapper_person import PersonMapper
from src.domain.models.model_person import PersonModel

from abc import ABC, abstractstaticmethod
from typing import Dict, List

class UseCasePersonInterface(ABC):

    @abstractstaticmethod
    def create(self, person: PersonModel) -> str: pass

    @abstractstaticmethod
    def read(self, name: str) -> List: pass

    @abstractstaticmethod
    def update(self, name: str, new_data: PersonModel) -> str: pass
