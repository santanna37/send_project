from src.infra.db.settings.connection import DBConnectionHandler
from src.infra.db.mappers.mapper_person import PersonMapper
from src.infra.db.entities.entity_person import PersonEntity
from src.domain.models.model_person import PersonModel
from src.data.interface.repository_person_interface import PersonRepositoryInterface

from typing import List



class PersonRepository(PersonRepositoryInterface):

    def create_person(self,person: PersonModel) -> str:

        new_user = PersonMapper.domain_to_entity(model = person)

        with DBConnectionHandler() as database:
            try:
                database.add(new_user)
                database.commit()
                print(person)
                return person

            except Exception as exception:
                database.rollback()
                print(exception)
                raise exception

            finally:
                print('acabou')
                database.close()


    def read_person(self, name: str) ->List:
        with DBConnectionHandler() as database:
            try:
                persons =(
                     database
                .query(PersonEntity)
                .filter(PersonEntity.name == name)
                .all()
                )
                lista_person = []

                for person in persons:
                    person = PersonMapper.entity_to_domain(entity= person)
                    lista_person.append(person)
                
                print(lista_person)
                return lista_person
            
            except Exception as exception:
                database.rollback()
                print(exception)
                raise exception

            finally:
                print('read_acabou')
                database.close()


    def update_person(self, name: str, new_data:PersonModel) -> PersonModel:
        with DBConnectionHandler() as database:
            try:
                quest =(
                    database
                .query(PersonEntity)
                .filter(PersonEntity.name == name)
                .first()
                )

                if not quest:
                    return None
                
                new_data = new_data.__dict__
                
                for key, value in new_data.items():
                    if value is not None:
                        setattr(quest,key,value)
                
                database.commit()
                database.refresh(quest)

                update_person = PersonMapper.entity_to_domain(quest)
                return update_person

            except Exception as exception:
                database.rollback()
                return exception

            finally:
                print('update_acabou')
                database.close()





    #def delete_person(name: str) -> PersonModel:pass 
