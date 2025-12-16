from src.domain.models.model_person import PersonModel
from src.infra.db.entities.entity_person import PersonEntity

from typing import Dict 



class PersonMapper:
    
    @staticmethod
    def domain_to_entity(model: PersonModel) -> PersonEntity:
        return PersonEntity(
            email = model.email,
            name = model.name
        )
    
    @staticmethod
    def entity_to_domain(entity: PersonEntity) -> PersonModel:
        return PersonModel(
            id = entity.id,
            name = entity.name,
            email = entity.email
        )
