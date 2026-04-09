from src.infra.db.repositores.repository_person import PersonRepository
from src.infra.db.entities.entity_person import PersonEntity
from src.domain.models.model_person import PersonModel
from src.infra.db.mappers.mapper import DataMapper



user_test = PersonModel(
    name= 'person_repo',
    cpf = '14062416794',
    cnpj = '12345678000199',
    phone = '21988621364',
    email= 'person_repo@test.com',
    password = '123'
    
    )

# user_test2 = PersonModel(
#     name= 'new_person',
#     email= None
# )


# def test_repo_create_person():
#     repo = PersonRepository(mapper=DataMapper)
#     print(repo.create_person(person= user_test))
#     print('passou_create_test')


# def test_repo_list_person():
#     repo = PersonRepository(mapper= DataMapper)
#     lista = repo.read_person(email =  user_test.email)
#     print(f'read_passou_test = {lista}')


# def test_repo_update_person():
#     repo = PersonRepository()
#     lista = repo.update_person(name= user_test.name, new_data= user_test2)
#     print(lista)
#     print('passou_update_test')