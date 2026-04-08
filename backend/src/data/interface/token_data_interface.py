from src.domain.models.model_person import PersonModel
from typing import Dict
from abc import ABC, abstractmethod




class TokenAuthInterface(ABC):

    @abstractmethod
    def authenticate(self, person: PersonModel) -> Dict: pass