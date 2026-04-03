from typing import TypeVar, Type, Any
from pydantic import BaseModel
from src.infra.db.settings.base import Base


# models
M = TypeVar("M", bound = BaseModel)
# entities
E = TypeVar("E", bound = Base)


class DataMapper:

    @staticmethod
    def model_to_entity(model: M, entity_cls: Type[E]) -> E:
        entity_cls = entity_cls(**model.model_dump())
        return entity_cls

    @staticmethod
    def entity_to_model(entity: E, model_cls: Type[M]) -> M:
        if not entity:
            return None
        data ={
            column.name: getattr(entity, column.name)
            for column in entity.__table__.columns
        }
        return model_cls(**data)

    # @staticmethod
    # def dict_to_domain(data: Dict) -> PersonModel:
    #     return PersonModel(
    #         id=data.get("id"),
    #         name=data.get("name"),
    #         email=data.get("email")
    #     )

    # @staticmethod
    # def domain_to_dict(model: PersonModel) -> Dict:
    #     return {
    #         "id": model.id,
    #         "name": model.name,
    #         "email": model.email
    #     }
