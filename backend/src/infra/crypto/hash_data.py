from src.data.interface.hash_data_interface import CryptoHashInterface
from typing import List, Dict

import bcrypt



class CryptoHash(CryptoHashInterface):

    def create_hash(self, password: str) -> str:
        #cria o hash
        hash_password =  password.encode('utf-8')
        print(hash_password)
        
        #cria o salt unico
        hashed_bytes = bcrypt.hashpw(hash_password, bcrypt.gensalt())
        print(hashed_bytes)

        # passa pra str
        hashed_decode = hashed_bytes.decode('utf-8')
        print(hashed_decode)
        return hashed_decode


    def check_hash(self, password: str, hash_chec: str) -> bool:
        check_password = bcrypt.checkpw(password= password.encode('utf-8'), hashed_password= hash_chec.encode('utf-8'))
        print(f'comparaçaos: {check_password}')
        return check_password