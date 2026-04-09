from src.domain.models.model_person import PersonModel
from typing import Dict
from abc import ABC, abstractmethod




class TokenInterface(ABC):

    @abstractmethod
    def authenticate(self, person: PersonModel) -> Dict: pass

    @abstractmethod
    def decode(self, token: str) -> Dict: pass