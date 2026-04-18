from src.domain.use_case.case_email.use_case_email_interface import UseCaseEmailInterface
from src.domain.constants.email_constants import EmailTemplateType, get_template
from src.data.interface.repository_customer_interface import CustomerRepositoryInterface
from src.infra.email.email_connection import AdapterEmail
from src.infra.pdf.pdf_reader import AdapterPDF
import re

from typing import Dict, List

type_email = EmailTemplateType

class UseCaseEmail(UseCaseEmailInterface):

    def __init__(self,
                adapter_email: AdapterEmail,
                adapter_pdf: AdapterPDF,
                builder_email: get_template,
                customer_repository: CustomerRepositoryInterface
                ):
        self._repository = customer_repository
        self._adapter_email = adapter_email
        self._adapter_pdf = adapter_pdf
        self._builder_email = builder_email

    # def get_path_list(self, list_pdf:List) -> List:
    #     list_path = []
    #     self.list_pdf = list_pdf

    #     for pdf in self.list_pdf:
    #         item = self._adapter_pdf.extrair_dados_darf(pdf_path= pdf)
    #         list_path.append(item)
        
    #     return list_path 


    def get_email_list(self, id_person:int, cnpj: str = None) -> List:
        response = self._repository.read_customer(id_person= id_person, cnpj= cnpj)
        return response
    
    def builder(self, pdf_bytes: bytes, pdf_name: str) -> Dict:
        info_pdf = self._adapter_pdf.extrair_dados_darf(pdf_path= pdf_bytes)
        
        email_data = self._builder_email(
            template_type=EmailTemplateType(info_pdf["tipo_documento"]),
            company_name=info_pdf["razao_social"],
            attachment_name=pdf_name,
            attachment_path=pdf_bytes
        )
        # Importante: Guardar o CNPJ para o "match" no trigger
        email_data["cnpj_extraido"] = info_pdf.get("cnpj")
        return email_data
    
    def send(self, email: str, email_data: Dict) -> Dict:
        try:
            success = self._adapter_email.send_email(email=email, email_data=email_data)
            if success:
                return {"status": "sucesso", "email": email}
            return {"status": "erro", "detalhe": "Adapter retornou falso"}
        except Exception as exception:
            return {"status": "erro", "detalhe": str(exception)}

    def trigger_email(self, list_email: List, list_pdf: List[Dict]) -> Dict:
        # Pega a lista de dentro do dicionário que veio do Controller
        customers = list_email
        relatorio = {}

        for pdf in list_pdf:
            # 1. Gera os dados do email através do PDF
            email_data = self.builder(pdf_bytes= pdf["bytes"], pdf_name= pdf["name"])
            cnpj_do_pdf = email_data.get("cnpj_extraido")

            # 1.1) Primeiro tenta pegar CNPJ com máscara (mais comum)
            m = re.search(r"(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})", cnpj_do_pdf)
            if m:
                cnpj_pdf_tratado = re.sub(r"\D", "", m.group(1))

            # 1.2) Fallback: tenta achar 14 dígitos seguidos
            m2 = re.search(r"\b(\d{14})\b", cnpj_do_pdf)
            if m2:
                cnpj_pdf_tratado = m2.group(1)
            
            cnpj_do_pdf = cnpj_pdf_tratado


            # 2. Busca o cliente correto (Match)
            target_customer = None
            for c in customers:
                if str(c.cnpj) == str(cnpj_do_pdf): # Garantimos que ambos sejam string
                    target_customer = c
                    print(f"customer -> {c} -- name: {c.name}")
                    break

            # 3. Processa o envio e alimenta o relatório
            if target_customer:
                print(f"Enviando {pdf['name']} para {target_customer.email}...")
                resultado = self.send(email=target_customer.email, email_data=email_data)
                
                # Incrementa o resultado com dados do cliente
                resultado["name"] = target_customer.name
                relatorio[pdf["name"]] = resultado
            else:
                relatorio[pdf["name"]] = {
                    "status": "erro",
                    "motivo": f"CNPJ {cnpj_do_pdf} não encontrado no banco",
                    "cliente": "Desconhecido"
                }

        return relatorio