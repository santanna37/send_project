from abc import ABC, abstractmethod
from typing import Dict, Optional



class AdapterPDFInterface(ABC):
    """
    Adaptador para leitura e extração de dados de PDFs
    """
    @abstractmethod
    def extrair_dados_darf(self, pdf_path: str) -> Dict: pass
    
    @abstractmethod
    def _extrair_cnpj(self, texto: str) -> Optional[str]: pas
    
    @abstractmethod
    def _extrair_razao_social(self, texto: str) -> Optional[str]: pass
    
    @abstractmethod
    def _identificar_tipo_documento(self, texto: str) -> str: pass
    
    @abstractmethod
    def _extrair_periodo(self, texto: str) -> Optional[str]: pass
    
    @abstractmethod
    def _extrair_vencimento(self, texto: str) -> Optional[str]: pass
    
    @abstractmethod
    def _extrair_valor_total(self, texto: str) -> Optional[str]: pass