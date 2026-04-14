from pathlib import Path
from functools import lru_cache
from enum import Enum
import base64
import os

# ========================================
# 1. Configurações de Caminho
# ========================================
CURRENT_DIR = Path(__file__).parent.resolve()
MEDIA_DIR = CURRENT_DIR / "media"

# ========================================
# 2. Assets Externos
# ========================================
URL_LOGO = "https://via.placeholder.com/150x60/667eea/ffffff?text=Sistema+Send"  # Substitua pelo seu logo

# ========================================
# 3. Enum de Tipos
# ========================================
class EmailTemplateType(str, Enum):
    INSS = "inss"
    SIMPLES = "simples"
    CUSTOM = "custom"

# ========================================
# 4. Templates com Cache
# ========================================

@lru_cache(maxsize=1)
def get_inss_template():
    """Template para documentação INSS"""
    return {
        'subject': 'Documentação INSS - {company_name}',
        'body': f"""
            <html>
                <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; margin: 0; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e0e0e0;">
                        
                        <!-- Header -->
                        <div style="padding: 30px 20px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                            <img src="{URL_LOGO}" alt="Logo Sistema Send" style="width: 120px; height: auto; margin-bottom: 10px;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 20px;">Documentação INSS</h1>
                        </div>

                        <!-- Corpo -->
                        <div style="padding: 30px 40px;">
                            <p style="font-size: 16px;">
                                Prezado(a) <strong>{{company_name}}</strong>,
                            </p>
                            
                            <p style="font-size: 15px; color: #555;">
                                Segue em anexo a <strong>documentação referente ao INSS</strong> do período atual.
                            </p>

                            <div style="margin: 25px 0; padding: 15px; background-color: #f0f4ff; border-left: 4px solid #667eea; border-radius: 5px;">
                                <p style="margin: 0; font-size: 14px; color: #555;">
                                    📋 <strong>Importante:</strong> Verifique os dados e guias em anexo. 
                                    Em caso de dúvidas, entre em contato.
                                </p>
                            </div>

                            <p style="font-size: 15px; color: #555;">
                                Atenciosamente,<br>
                                <strong>{{sender_name}}</strong>
                            </p>
                        </div>

                        <!-- Footer -->
                        <div style="padding: 20px; text-align: center; background-color: #f8f9fa; border-top: 1px solid #e9ecef; font-size: 12px; color: #6c757d;">
                            <p style="margin: 5px 0;"><strong>Sistema Send</strong> - Gestão Contábil</p>
                            <hr style="border: 0; border-top: 1px solid #dee2e6; margin: 15px 0;">
                            <p style="font-size: 10px; color: #adb5bd;">&copy; {{current_year}} Sistema Send. Todos os direitos reservados.</p>
                        </div>
                    </div>
                </body>
            </html>
        """,
        'images': [],
        'attachments': []
    }

@lru_cache(maxsize=1)
def get_simples_template():
    """Template para Simples Nacional"""
    return {
        'subject': 'Documentação Simples Nacional - {company_name}',
        'body': f"""
            <html>
                <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; margin: 0; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e0e0e0;">
                        
                        <!-- Header -->
                        <div style="padding: 30px 20px; text-align: center; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
                            <img src="{URL_LOGO}" alt="Logo Sistema Send" style="width: 120px; height: auto; margin-bottom: 10px;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 20px;">Simples Nacional</h1>
                        </div>

                        <!-- Corpo -->
                        <div style="padding: 30px 40px;">
                            <p style="font-size: 16px;">
                                Prezado(a) <strong>{{company_name}}</strong>,
                            </p>
                            
                            <p style="font-size: 15px; color: #555;">
                                Segue em anexo a <strong>documentação referente ao Simples Nacional</strong> do período atual.
                            </p>

                            <div style="margin: 25px 0; padding: 15px; background-color: #e8f8f5; border-left: 4px solid #11998e; border-radius: 5px;">
                                <p style="margin: 0; font-size: 14px; color: #555;">
                                    💼 <strong>Atenção:</strong> Confira valores e prazos de vencimento. 
                                    Mantenha seus tributos em dia.
                                </p>
                            </div>

                            <p style="font-size: 15px; color: #555;">
                                Atenciosamente,<br>
                                <strong>{{sender_name}}</strong>
                            </p>
                        </div>

                        <!-- Footer -->
                        <div style="padding: 20px; text-align: center; background-color: #f8f9fa; border-top: 1px solid #e9ecef; font-size: 12px; color: #6c757d;">
                            <p style="margin: 5px 0;"><strong>Sistema Send</strong> - Gestão Contábil</p>
                            <hr style="border: 0; border-top: 1px solid #dee2e6; margin: 15px 0;">
                            <p style="font-size: 10px; color: #adb5bd;">&copy; {{current_year}} Sistema Send. Todos os direitos reservados.</p>
                        </div>
                    </div>
                </body>
            </html>
        """,
        'images': [],
        'attachments': []
    }

@lru_cache(maxsize=1)
def get_custom_template():
    """Template genérico"""
    return {
        'subject': 'Documentação Contábil - {company_name}',
        'body': f"""
            <html>
                <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; background-color: #f4f4f4; margin: 0; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e0e0e0;">
                        
                        <!-- Header -->
                        <div style="padding: 30px 20px; text-align: center; background: linear-gradient(135deg, #3a7bd5 0%, #00d2ff 100%);">
                            <img src="{URL_LOGO}" alt="Logo Sistema Send" style="width: 120px; height: auto; margin-bottom: 10px;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 20px;">Documentação Contábil</h1>
                        </div>

                        <!-- Corpo -->
                        <div style="padding: 30px 40px;">
                            <p style="font-size: 16px;">
                                Prezado(a) <strong>{{company_name}}</strong>,
                            </p>
                            
                            <p style="font-size: 15px; color: #555;">
                                Segue em anexo a <strong>documentação solicitada</strong> para sua análise.
                            </p>

                            <div style="margin: 25px 0; padding: 15px; background-color: #e3f2fd; border-left: 4px solid #3a7bd5; border-radius: 5px;">
                                <p style="margin: 0; font-size: 14px; color: #555;">
                                    📁 <strong>Dica:</strong> Guarde este documento em local seguro 
                                    para futuras consultas.
                                </p>
                            </div>

                            <p style="font-size: 15px; color: #555;">
                                Atenciosamente,<br>
                                <strong>{{sender_name}}</strong>
                            </p>
                        </div>

                        <!-- Footer -->
                        <div style="padding: 20px; text-align: center; background-color: #f8f9fa; border-top: 1px solid #e9ecef; font-size: 12px; color: #6c757d;">
                            <p style="margin: 5px 0;"><strong>Sistema Send</strong> - Gestão Contábil</p>
                            <hr style="border: 0; border-top: 1px solid #dee2e6; margin: 15px 0;">
                            <p style="font-size: 10px; color: #adb5bd;">&copy; {{current_year}} Sistema Send. Todos os direitos reservados.</p>
                        </div>
                    </div>
                </body>
            </html>
        """,
        'images': [],
        'attachments': []
    }

# ========================================
# 5. Variáveis Pré-carregadas (Cache)
# ========================================
TEMPLATE_INSS = get_inss_template()
TEMPLATE_SIMPLES = get_simples_template()
TEMPLATE_CUSTOM = get_custom_template()

# ========================================
# 6. Funções Helper
# ========================================

def _read_file_as_base64(file_path: str) -> str:
    """
    Lê arquivo e converte para base64
    
    Args:
        file_path: Caminho do arquivo (absoluto ou relativo)
    
    Returns:
        String base64 do arquivo
    
    Raises:
        FileNotFoundError: Se arquivo não existir
    """
    if isinstance(file_path, bytes):
        return base64.b64encode(file_path).decode("utf-8")

    if isinstance(file_path, str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    raise TypeError("attachment_path deve ser str ou bytes")
    
    #return base64.b64encode(file_bytes).decode('utf-8')

def get_template(
    template_type: EmailTemplateType, 
    company_name: str, 
    sender_name: str = "Equipe Send",
    attachment_path: str | bytes = None,
    attachment_name: str = None
) -> dict:
    """
    Retorna template formatado com opção de anexo
    
    Args:
        template_type: INSS, SIMPLES ou CUSTOM
        company_name: Nome da empresa destinatária
        sender_name: Nome do remetente
        attachment_path: (OPCIONAL) Caminho do arquivo para anexar
        attachment_name: (OPCIONAL) Nome do arquivo no email (ex: "INSS_Janeiro_2024.pdf")
    
    Returns:
        dict com 'subject', 'body', 'images', 'attachments'
    
    Exemplo:
        # Sem anexo
        template = get_template(
            template_type=EmailTemplateType.INSS,
            company_name="Empresa XYZ",
            sender_name="João Contador"
        )
        
        # Com anexo
        template = get_template(
            template_type=EmailTemplateType.INSS,
            company_name="Empresa XYZ",
            sender_name="João Contador",
            attachment_path="./pdfs/inss_empresa_xyz.pdf",
            attachment_name="INSS_Janeiro_2024.pdf"
        )
    """
    from datetime import datetime
    
    # Seleciona template
    if template_type == EmailTemplateType.INSS:
        template = TEMPLATE_INSS.copy()
    elif template_type == EmailTemplateType.SIMPLES:
        template = TEMPLATE_SIMPLES.copy()
    else:
        template = TEMPLATE_CUSTOM.copy()
    
    # Formata subject
    subject = template['subject'].format(company_name=company_name)
    
    # Formata body (substitui placeholders)
    body = template['body']
    body = body.replace('{{company_name}}', company_name)
    body = body.replace('{{sender_name}}', sender_name)
    body = body.replace('{{current_year}}', str(datetime.now().year))
    
    # Processa anexo (se fornecido)
    attachments = []
    if attachment_path:
        # Lê arquivo e converte para base64
        file_base64 = _read_file_as_base64(attachment_path)
        
        # Define nome do anexo
        final_name = attachment_name or os.path.basename(attachment_path)
        
        attachments.append({
            'content': file_base64,
            'name': final_name
        })
    
    return {
        'subject': subject,
        'body': body,
        'images': template['images'],
        'attachments': attachments
    }