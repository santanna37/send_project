from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base



class PersonEntity(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key= True, autoincrement= True)
    name = Column(String(100))
    cpf = Column(String(11))
    cnpj = Column(String(14))
    phone = Column(String(20))
    email = Column(String(100))
    password = Column(String(100))

    customer = relationship("CustomerEntity", back_populates = "person")

    def __repr__(self):
        return f"Person [name = {self.name}, email = {self.email}]"


