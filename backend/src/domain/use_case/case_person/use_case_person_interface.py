from src.data.interface.repository_person_interface import PersonRepositoryInterface
from src.domain.models.model_person import PersonModel

from abc import ABC, abstractmethod
from typing import Dict, List

class UseCasePersonInterface(ABC):

    @abstractmethod
    def create(self, person: PersonModel) -> str: pass

    # @abstractmethod
    # def read(self, name: str) -> List: pass

    # @abstractmethod
    # def update(self, name: str, new_data: PersonModel) -> str: pass

    def create_hash(self, password: str) -> str: pass

    def check_hash(self, password: str, hash_check: str) -> bool: pass