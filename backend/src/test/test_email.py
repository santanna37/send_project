# backend/teste_email_completo.py

from src.infra.email.email_connection import AdapterEmail 
from src.domain.constants.email_constants import get_template, EmailTemplateType

# 1. Inicializa adapter
adapter = AdapterEmail()
def test_email():
    # 2. Gera template COM anexo
    template = get_template(
        template_type=EmailTemplateType.INSS,
        company_name="Teste LTDA",
        sender_name="Maria Contadora",
        attachment_path="./ADP INSS.pdf",  # Substitua por um PDF real
        attachment_name="INSS_Teste.pdf"
    )

    # 3. Monta email_data
    email_data = {
        'sender': {'name': 'Sistema Send'},
        'subject': template['subject'],
        'html': template['body'],
        'attachments': template['attachments']
    }

    # 4. Envia
    result = adapter.send_email(
        email="contador.leonardo.lima@gmail.com",
        email_data=email_data
    )

    print(f"Resultado: {'✅ Sucesso' if result else '❌ Falhou'}")

test_email()