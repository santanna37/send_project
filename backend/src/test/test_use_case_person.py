from src.data.use_case.case_person.use_case_person import UseCasePerson
from src.infra.db.repositores.repository_person import PersonRepository
from src.domain.models.model_person import PersonModel
from src.infra.db.mappers.mapper import DataMapper

user_test = PersonModel(
    name= 'person_use_case',
    cpf = '14062416794',
    cnpj = '12345678000199',
    phone = '21988621364',
    email= 'person_repo@test.com',
    password = '123'
    
    )

user_test2 = PersonModel(
    name= 'person_repo',
    cpf = '14062416794',
    cnpj = '12345678000199',
    phone = '21988621364',
    email= 'person_repo@test.com',
    password = '123'
    
    )

# def test_use_case_create():

#     repo = PersonRepository(mapper=DataMapper)
#     case = UseCasePerson(repository= repo)

#     new = case.create(person= user_test)

#     return print(new)

# def test_hash():
#     repo = PersonRepository(mapper= DataMapper)
#     case = UseCasePerson(repository=repo)

#     new = case.create_hash(user_test.password)
#     return print(f"teste: {new}")

# def test_hash_compare():
#     repo = PersonRepository(mapper= DataMapper)
#     case = UseCasePerson(repository= repo)
#     pass_test = '123'
#     new = case.check_hash(password=user_test.password, hash_chec= case.create_hash(pass_test))
# # def test_use_case_read():

# #     repo = PersonRepository()
# #     case = UseCasePerson(repository= repo)

# #     list = case.read(name= user_test.name)

# #     return list

# def test_use_case_update():

#     repo = PersonRepository()
#     case = UseCasePerson(repository= repo)

#     new = case.update(name= user_test.name, new_data= user_test2)

#     return print(new)
