from src.data.use_case.case_person.use_case_person import UseCasePerson
from src.infra.db.repositores.repository_person import PersonRepository
from src.domain.models.model_person import PersonModel

user_test = PersonModel(
    name= 'person_use_case',
    email= 'person_use_case@test.com')

user_test2 = PersonModel(
    name= 'new_person_use_case',
    email= 'new_person@use_case.com'
)

def test_use_case_create():

    repo = PersonRepository()
    case = UseCasePerson(repository= repo)

    new = case.create(person= user_test)

    return new

def test_use_case_read():

    repo = PersonRepository()
    case = UseCasePerson(repository= repo)

    list = case.read(name= user_test.name)

    return list

def test_use_case_update():

    repo = PersonRepository()
    case = UseCasePerson(repository= repo)

    new = case.update(name= user_test.name, new_data= user_test2)

    return print(new)
