from src.infra.email.email_connection import AdapterEmail
from src.infra.pdf.pdf_reader import AdapterPDF
from src.domain.constants.email_constants import get_template
from src.infra.db.repositores.repository_customer import CustomerRepository
from src.infra.db.mappers.mapper import DataMapper
from src.data.use_case.case_email.use_case_email import UseCaseEmail
from src.presentation.controllers.controller_email import EmailController
from src.presentation.dto.dto_email import DTOEmail
from src.presentation.validator.validator_customer import CustomerValidator


class EmailCompose:

    def __init__(self):
        self._adapter_email = AdapterEmail()
        self._adapter_pdf = AdapterPDF()
        self._repository = CustomerRepository(mapper=DataMapper())
        self._dto = DTOEmail(validator=CustomerValidator())

    def email_multi_sender(self):
        use_case = UseCaseEmail(
            adapter_email=self._adapter_email,
            adapter_pdf=self._adapter_pdf,
            builder_email=get_template,
            customer_repository=self._repository
        )
        controller = EmailController(use_case=use_case, dto=self._dto)
        return controller.multi_sender