

class CustomerValidator:

    def name_validator(self, name: str) -> str:
        return name

    def cnpj_validator(self, cnpj: str) -> str:
        return cnpj
    
    def phone_validator(self, phone: str) -> str:
        return phone
    
    def email_validator(self, email: str) -> str:
        return email
    
    def id_person_validator(self, id_person: str) -> int:
        return int(id_person)