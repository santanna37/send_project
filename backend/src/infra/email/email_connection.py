
import os
import requests
import logging
from typing import Dict
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Carrega .env
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class AdapterEmail:

    def __init__(self):
        self._api_key = os.getenv("BREVO_API_KEY")
        self._host = os.getenv("EMAIL_HOST")
        self._url = os.getenv("BREVO_URL", "https://api.brevo.com/v3/smtp/email")
        
        if not self._api_key:
            raise ValueError("BREVO_API_KEY não configurada no .env")
        
        logger.info(f"[AdapterEmail] API: {'✅' if self._api_key else '❌'}")

    def send_email(self, email: str, email_data: Dict) -> bool:
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
        # Monta payload base
        payload = {
            "sender": {
                "name": email_data.get("sender", {}).get("name", "Sistema Send"),
                "email": self._host
            },
            "to": [{"email": email}],
            "subject": email_data.get("subject", "Sem assunto"),
            "htmlContent": email_data.get("body", "")  # ✅ API Brevo espera htmlContent
        }
        
        # ========================================
        # ADICIONA ANEXOS (se existirem)
        # ========================================
        attachments = email_data.get("attachments", [])
        if attachments:
            payload["attachment"] = []  # ✅ API Brevo usa "attachment" (singular)
            
            for att in attachments:
                payload["attachment"].append({
                    "content": att["content"],  # Base64 já vem do template
                    "name": att["name"]
                })
            
            logger.info(f"[AdapterEmail] 📎 Anexos: {len(attachments)}")
        
        logger.info(f"[AdapterEmail] 📧 Enviando para: {email}")
        logger.info(f"[AdapterEmail] 📝 Assunto: {email_data.get('subject')}")
        
        # Headers
        headers = {
            "accept": "application/json",
            "api-key": self._api_key,
            "content-type": "application/json"
        }
        
        try:
            response = requests.post(self._url, json=payload, headers=headers)
            
            logger.info(f"[AdapterEmail] Status: {response.status_code}")
            
            if response.status_code >= 400:
                logger.error(f"[AdapterEmail] ❌ Erro Brevo: {response.text}")
                return False
            
            logger.info(f"[AdapterEmail] ✅ Email enviado!")
            return True

        except Exception as exception:
            logger.error(f"[AdapterEmail] ❌ Exceção: {exception}")
            return False