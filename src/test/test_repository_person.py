from src.infra.db.repositores.repository_person import PersonRepository
from src.infra.db.entities.entity_person import PersonEntity
from src.domain.models.model_person import PersonModel



user_test = PersonModel(
    name= 'person_repo',
    email= 'person_repo@test.com')

user_test2 = PersonModel(
    name= 'new_person',
    email= None
)


def test_repo_create_person():
    repo = PersonRepository()
    repo.create_person(person= user_test)
    print('passou_create_test')


def test_repo_list_person():
    repo = PersonRepository()
    lista = repo.read_person(name = user_test.name)
    print(f'read_passou_test = {lista}')


def test_repo_update_person():
    repo = PersonRepository()
    lista = repo.update_person(name= user_test.name, new_data= user_test2)
    print(lista)
    print('passou_update_test')