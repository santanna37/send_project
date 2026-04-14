from abc import ABC, abstractmethod
from typing import Dict

class AdapterEmail(ABC):

    @abstractmethod
    def send_email(self, email: str, email_data: Dict) -> bool: pass
"""
        Envia email via Brevo
        
        Args:
            email: Email destinatário
            email_data: {
                "sender": {"name": "Nome"},
                "subject": "Assunto",
                "html": "corpo HTML",  # ← será convertido para htmlContent
                "attachments": [{"content": "base64", "name": "arquivo.pdf"}]  # ← NOVO
            }
"""
