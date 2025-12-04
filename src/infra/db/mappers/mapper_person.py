from src.domain.models.model_person import PersonModel
from src.infra.db.entities.entity_person import PersonEntity

from typing import Dict 



class PersonMapper:
    
    def domain_to_entity(self,model: PersonModel) -> PersonEntity:
        return PersonEntity(
            id = model.id,
            email = model.email,
            name = model.name
        )

    