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

    customer = relationship("CustomerEntity", back_populates = "customer")




    def __repr__(self):
        return f"Person [name = {self.name}, email = {self.email},]"

class CustomerEntity(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key = True, autoincrement = True)
    razao_social = Column(String(100))
    cnpj = Column(String(100))
    phone = Column(String(20))
    email = Column(string(100))
    id_person = Column(Integer, ForeignKey('person.id'))

    person = relationship("PersonEntity", back_populates = "person")