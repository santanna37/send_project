import fitz  # PyMuPDF
import re
import logging
from typing import Dict, Optional



logger = logging.getLogger(__name__)



class AdapterPDF:
    """
    Adaptador para leitura e extração de dados de PDFs
    """
    
    def extrair_dados_darf(self, pdf_path: str) -> Dict:
        """
        Extrai dados do PDF de DARF/INSS/Simples
        
        Args:
            pdf_path: Caminho do arquivo PDF
        
        Returns:
            {
                "cnpj": "12.345.678/0001-90",
                "razao_social": "Empresa XYZ LTDA",
                "tipo_documento": "inss" ou "simples",
                "periodo": "01/2024",
                "vencimento": "20/02/2024",
                "valor_total": "1.234,56"
            }
        """
        try:
            logger.info(f"[AdapterPDF] Lendo PDF: {pdf_path}")
            
            with fitz.open(pdf_path) as pdf:
                # Extrai texto da primeira página
                texto = pdf[0].get_text()
            
            logger.debug(f"[AdapterPDF] Texto extraído (primeiros 200 chars): {texto[:200]}")
            
            # Extrai campos específicos
            dados = {
                'cnpj': self._extrair_cnpj(texto),
                'razao_social': self._extrair_razao_social(texto),
                'tipo_documento': self._identificar_tipo_documento(texto),
                'periodo': self._extrair_periodo(texto),
                'vencimento': self._extrair_vencimento(texto),
                'valor_total': self._extrair_valor_total(texto)
            }
            
            logger.info(f"[AdapterPDF] Dados extraídos: CNPJ={dados['cnpj']}, Tipo={dados['tipo_documento']}")
            
            return dados
            
        except Exception as error:
            logger.error(f"[AdapterPDF] Erro ao ler PDF: {error}")
            raise Exception(f"Erro ao processar PDF: {str(error)}")
    
    def _extrair_cnpj(self, texto: str) -> Optional[str]:
        """Extrai CNPJ do texto"""
        match = re.search(r'(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})', texto)
        return match.group(1) if match else None
    
    def _extrair_razao_social(self, texto: str) -> Optional[str]:
        """Extrai razão social"""
        match = re.search(
            r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\s+([A-Z\s\.]+?)(?:Período|CNPJ|$)', 
            texto, 
            re.IGNORECASE
        )
        if match:
            razao = match.group(1).strip()
            # Remove espaços múltiplos
            razao = re.sub(r'\s+', ' ', razao)
            return razao
        return None
    
    def _identificar_tipo_documento(self, texto: str) -> str:
        """Identifica se é INSS ou Simples Nacional"""
        texto_upper = texto.upper()
        
        if 'INSS' in texto_upper or 'PREVIDÊNCIA' in texto_upper:
            return 'inss'
        elif 'SIMPLES' in texto_upper or 'DAS' in texto_upper:
            return 'simples'
        else:
            return 'custom'
    
    def _extrair_periodo(self, texto: str) -> Optional[str]:
        """Extrai período de apuração"""
        match = re.search(r'Período.*?Apuração\s*([A-Za-z0-9/]+)', texto, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _extrair_vencimento(self, texto: str) -> Optional[str]:
        """Extrai data de vencimento"""
        match = re.search(r'Vencimento\s*([0-9]{2}/[0-9]{2}/[0-9]{4})', texto)
        return match.group(1) if match else None
    
    def _extrair_valor_total(self, texto: str) -> Optional[str]:
        """Extrai valor total"""
        match = re.search(r'Valor Total.*?\s*([0-9,\.]+)', texto)
        return match.group(1) if match else None