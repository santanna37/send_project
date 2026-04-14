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
    # @abstractmethod
    # def get_path_list(self, list_pdf:List) -> List: pass

    @abstractmethod
    def get_email_list(self, id_person:int, cnpj: str = None) -> List: pass
    
    @abstractmethod
    def builder(self, pdf_bytes: bytes, pdf_name: str) -> Dict: pass

    @abstractmethod
    def send(self, email: str, email_data: Dict) -> Dict: pass

    @abstractmethod
    def get_email_list(self, id_person: int, cnpj: str = None) -> List: pass

    @abstractmethod
    def trigger_email(self, list_email: List, list_pdf: List[Dict]) -> Dict: pass