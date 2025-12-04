from sqlalchemy import Column, Integer, String
from src.infra.db.settings.base import Base



class PersonEntity(Base):
    __tablename__ = "person"

    id = Column(Integer, primary_key= True, autoincrement= True)
    name = Column(String(100))
    email = Column(String(100))

    def __repr__(self):
        return f"Person [id= {self.id}, name= {self.name}]"