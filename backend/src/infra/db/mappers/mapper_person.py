from typing import Dict
from src.domain.models.model_person import PersonModel
from src.infra.db.entities.entity_person import PersonEntity


class PersonMapper:

    @staticmethod
    def domain_to_entity(model: PersonModel) -> PersonEntity:
        return PersonEntity(
            name=model.name,
            email=model.email
        )

    @staticmethod
    def entity_to_domain(entity: PersonEntity) -> PersonModel:
        return PersonModel(
            id=entity.id,
            name=entity.name,
            email=entity.email
        )

    @staticmethod
    def dict_to_domain(data: Dict) -> PersonModel:
        return PersonModel(
            id=data.get("id"),
            name=data.get("name"),
            email=data.get("email")
        )

    @staticmethod
    def domain_to_dict(model: PersonModel) -> Dict:
        return {
            "id": model.id,
            "name": model.name,
            "email": model.email
        }
