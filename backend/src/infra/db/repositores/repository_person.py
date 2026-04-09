from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.mappers.mapper import DataMapper
from src.infra.db.entities.entity_person import PersonEntity
from src.domain.models.model_person import PersonModel
from src.data.interface.repository_person_interface import PersonRepositoryInterface

from typing import List
import logging



logger = logging.getLogger(__name__)



class PersonRepository(PersonRepositoryInterface):

    def __init__(self, mapper: DataMapper):
        self.__mapper = mapper
        self.__entity = PersonEntity
        self.__model = PersonModel

    def create_person(self,person: PersonModel) -> PersonModel:

        new_user = self.__mapper.model_to_entity(model = person, entity_cls= self.__entity)

        with DBConnectionHandler() as database:
            try:
                database.add(new_user)
                database.commit()
                database.refresh(new_user)
                logger.info(f"[LOG_DB] - OK - Usuario: {person.name} cadastrado")
                return person

            except Exception as exception:
                database.rollback()
                logger.exception(f"[LOG_DB] - EXCEPTION - Erro ao salvar usuario {person.name}")
                raise exception

            finally:
                database.close()


    def read_person(self, email: str = None, cpf: str = None) ->PersonModel:

        with DBConnectionHandler() as database:
            try:
                query =  database.query(PersonEntity)
                
                if email is not None:
                    query = query.filter(PersonEntity.email == email)
                
                if cpf is not None:
                    query = query.filter(PersonEntity.cpf == cpf)
                
                print(query)
                response = query.distinct().first()

                print(f"print do response: {response}")
                
                response = self.__mapper.entity_to_model(entity= response, model_cls= self.__model)

                return response
            
            except Exception as exception:
                database.rollback()
                print(exception)
                raise exception

            finally:
                print('read_acabou')
                database.close()


    # def update_person(self, name: str, new_data:PersonModel) -> PersonModel:
    #     with DBConnectionHandler() as database:
    #         try:
    #             quest =(
    #                 database
    #             .query(PersonEntity)
    #             .filter(PersonEntity.name == name)
    #             .first()
    #             )

    #             if not quest:
    #                 return None
                
    #             new_data = new_data.__dict__
                
    #             for key, value in new_data.items():
    #                 if value is not None:
    #                     setattr(quest,key,value)
                
    #             database.commit()
    #             database.refresh(quest)

    #             update_person = PersonMapper.entity_to_domain(quest)
    #             return update_person

    #         except Exception as exception:
    #             database.rollback()
    #             return exception

    #         finally:
    #             print('update_acabou')
    #             database.close()





    #def delete_person(name: str) -> PersonModel:pass 
