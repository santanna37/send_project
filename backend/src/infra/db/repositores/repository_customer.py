from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.mappers.mapper import DataMapper
from src.data.interface.repository_customer_interface import CustomerRepositoryInterface
from src.domain.models.model_customer import CustomerModel
from src.infra.db.entities.entity_customer import CustomerEntity

from typing import List
import logging



logger = logging.getLogger(__name__)


class CustomerRepository(CustomerRepositoryInterface):

    def __init__(self, mapper: DataMapper):
        self.__mapper = mapper
        self.__model = CustomerModel
        self.__entitie = CustomerEntity

    def create_customer(self, model_customer: CustomerModel) -> CustomerModel:
        
        new_customer = self.__mapper.model_to_entity(model= model_customer, entity_cls= self.__entitie)

        with DBConnectionHandler() as database:
            try:
                database.add(new_customer)
                database.commit()
                database.refresh(new_customer)
                new_customer = self.__mapper.entity_to_model(entity= new_customer, model_cls= self.__model)
                return new_customer
            except Exception as exception:
                database.rollback()
                return exception


    def read_customer(self, id_person: int = None, cnpj: str = None) ->List:
        
        customer_list = []
        
        with DBConnectionHandler() as database:
            try:
                query = database.query(self.__entitie)
                query = query.filter(self.__entitie.id_person == id_person)

                if cnpj is not None:
                    query = query.filter(self.__entitie.cnpj == cnpj)
                
                result = query.all()

                for customer in result:
                    customer_list.append(self.__mapper.entity_to_model(entity= customer, model_cls= self.__model))
                
                return customer_list
            
            except Exception as exception:
                return []
            
            finally:
                database.close()


