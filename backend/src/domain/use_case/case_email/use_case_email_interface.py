from src.domain.constants.email_constants import EmailTemplateType
from abc import ABC, abstractmethod
from typing import Dict, List



class UseCaseEmailInterface(ABC):
    """
    id_person
    pdf 
        razao_social
        cnpj
        tipo
        """
    @abstractmethod
    def builder(self, pdf_path: str) -> Dict: pass

    @abstractmethod
    def send(self, email: str, model: Dict) -> Dict: pass

    @abstractmethod
    def quest_customer(self, id_person: int) -> List: pass

    @abstractmethod
    def trigger_email(self, list_customer: List, list_path: List): pass