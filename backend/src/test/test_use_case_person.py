from src.data.use_case.case_person.use_case_person import UseCasePerson
from src.infra.db.repositores.repository_person import PersonRepository
from src.infra.crypto.hash_data import CryptoHash  # ← NOVO
from src.infra.auth.token_data import Token   # ← NOVO
from src.domain.models.model_person import PersonModel
from src.infra.db.mappers.mapper import DataMapper


# user_test = PersonModel(
#     name='person_use_case',
#     cpf='14062416794',
#     cnpj='12345678000199',
#     phone='21988621364',
#     email='teste_create@email.com',  # ← email diferente para não duplicar
#     password='123'
# )


# def test_use_case_create():
#     # 1. Monta as dependências
#     repo = PersonRepository(mapper=DataMapper)
#     hash_service = CryptoHash()
#     token_service = TokenAuth()
    
#     # 2. Injeta no use case
#     case = UseCasePerson(
#         repository=repo,
#         token=token_service,
#         hash_person=hash_service
#     )
    
#     # 3. Testa o create
#     new = case.create(person=user_test)
    
#     # 4. Validações
#     assert new is not None
#     assert new.name != 'Person Use Case'  # ← validado pelo validator
#     assert new.email == 'teste_create@email.com'
#     assert new.password != '123'  # ← senha deve estar hasheada
    
# #     print(f"✅ Usuário criado: {new.name}")
# user_test = {
#             "email":"lsantanna.menezes@gmail.com",
#             "password":"1111111111"
#             }   

# def test_use_case_login():
#     # 1. Monta as dependências
#     repo = PersonRepository(mapper=DataMapper)
#     hash_service = CryptoHash()
#     token_service = Token()
    
#     # 2. Injeta no use case
#     case = UseCasePerson(
#         repository=repo,
#         token=token_service,
#         hash_person=hash_service
#     )
    
#     # 3. Testa o create
#     new = case.login(email=user_test["email"],password=user_test["password"])
#     print(new)
    
#     # 4. Validações
#     # assert new is not None
#     # assert new.name != 'Person Use Case'  # ← validado pelo validator
#     # assert new.email == 'teste_create@email.com'
#     # assert new.password != '123'  # ← senha deve estar hasheada
    
#     print(f"✅ teste login: {new}")






# # def test_use_case_create():

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



import uuid

from src.data.use_case.case_person.use_case_person import UseCasePerson
from src.infra.db.repositores.repository_person import PersonRepository
from src.infra.db.mappers.mapper import DataMapper
from src.infra.crypto.hash_data import CryptoHash
from src.infra.auth.token_data import Token
from src.domain.models.model_person import PersonModel


def test_use_case_login():
    repo = PersonRepository(mapper=DataMapper)
    hash_service = CryptoHash()
    token_service = Token()

    case = UseCasePerson(
        repository=repo,
        token=token_service,
        hash_person=hash_service
    )

    unique = str(uuid.uuid4())[:8]
    email = f"teste_{unique}@email.com"
    password = "123456"

    # cria usuário novo
    person = PersonModel(
        name="Teste Login",
        cpf="12345678901",
        cnpj="",
        phone="21999999999",
        email=email,
        password=password
    )

    case.create(person)

    # testa login
    print(f"senha salva -> {person.password} ")
    print(f"senha enviada -> {password}")
    result = case.login(email=email, password=password)


    assert result["success"] is True
    assert "access_token" in result