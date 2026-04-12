from src.domain.use_case.case_email.use_case_email_interface import UseCaseEmailInterface
from src.domain.constants.email_constants import EmailTemplateType, get_template
from src.data.interface.repository_customer_interface import CustomerRepositoryInterface
from src.infra.email.email_connection import AdapterEmail
from src.infra.pdf.pdf_reader import AdapterPDF

from typing import Dict, List

type_email = EmailTemplateType

class UseCaseEmail(UseCaseEmailInterface):

    def __init__(self,
                adapter_email: AdapterEmail,
                adapter_dpf: AdapterPDF,
                builder_email: get_template,
                customer_repository: CustomerRepositoryInterface
                ):
        
        self._repository = CustomerRepositoryInterface
        self._adapter_email = adapter_email
        self._adapter_pdf = AdapterPDF
        self._builder_email = get_template
    
    def builder(self, pdf_path: str) -> Dict:
        
        info_pdf = self._adapter_pdf.extrair_dados_darf(pdf_path= pdf_path)
        
        email_data = self._builder_email(
                                            template_type= type_email(info_pdf["tipo_documento"]),
                                            company_name= info_pdf["razao_social"],
                                            attachment_name= info_pdf["tipo_documento"],
                                            attachment_path= pdf_path
                                            )
        email_data["cnpj_extraido"] = info_pdf.get("cnpj")
        return email_data
    
    def send(self, email: str, email_data: Dict) -> Dict:

        try:
            send_email = self._adapter_email.send_email(email= email, email_data= email_data)
            if send_email:
                return {
                    "body": "email enviado"
                }
        except Exception as exception:
            return {"body": "falha no envio do email"}
    
    def quest_customer(self,id_person:int):

        customer_list = self._repository.read_customer(id_person= id_person)
        return email_list

    def trigger_email(self, list_customer: List, list_path: List):


        for path in list_path:
            builder_email = self.builder(pdf_path= path)

            
            sender = self.send(email= email, email_data= builder_email)
