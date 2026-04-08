from src.domain.use_case.case_person.use_case_person_interface import UseCasePersonInterface
from src.data.interface.repository_person_interface import PersonRepositoryInterface
from src.data.interface.hash_data_interface import CryptoHashInterface
from src.data.interface.token_data_interface import TokenAuthInterface
from src.domain.models.model_person import PersonModel
from typing import List, Dict
from src.infra.db.mappers.mapper import DataMapper



class UseCasePerson(UseCasePersonInterface):

    def __init__(self,
                repository: PersonRepositoryInterface,
                token: TokenAuthInterface,
                hash_person: CryptoHashInterface):
        self.__repository = repository
        self.__token = token
        self.__hash = hash_person

    # def create_hash(self, password: str) -> str:
    #     hash_password =  password.encode('utf-8')
    #     print(hash_password)
    #     hashed_bytes = bcrypt.hashpw(hash_password, bcrypt.gensalt())
    #     print(hashed_bytes)
    #     hashed_decode = hashed_bytes.decode('utf-8')
    #     print(hashed_decode)
    #     return hashed_decode
    
    # def check_hash(self, password: str, hash_chec: str) -> bool:
    #     check_password = bcrypt.checkpw(password= password.encode('utf-8'), hashed_password= hash_chec.encode('utf-8'))
    #     print(f'comparaçaos: {check_password}')
    #     return check_password

    # def authenticate(self, person: PersonModel) -> Dict:
    #     token_data = {
    #         "sub": person.id,
    #         "exp": datetime.utcnow() + timedelta(hours=24)
    #     }

    #     token = jwt.encode(token_data, KEY, algorithm="HS256")

    #     return {'success': True, "access_token": token}


    def login(self, email: str, password: str):
        person = self.__repository.read_person(email= email)
        if not person:
            raise ValueError("Usuario não encontrado")

        verification = self.__hash.check_hash(password= password, hash_chec= person.password)
        if verification:
            token_access = self.__token.authenticate(person= person)
        
        if not token_access:
            raise ValueError("Erro no token")

        return token_access

    def create(self, person: PersonModel) -> Dict:
        password_hash = self.__hash.create_hash(password= person.password)
        person.password = password_hash
        new_person = self.__repository.create_person(person= person)
        

        return new_person

    # def read(self, name:str) -> List:
    #     list_person = self.__repository.read_person(name= name)

    #     return list_person

    # def update(self, name:str, new_data:PersonModel) -> str:
    #     up_person = self.__repository.update_person(name= name, new_data= new_data)

    #     return up_person