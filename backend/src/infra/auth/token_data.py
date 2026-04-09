from src.data.interface.token_data_interface import TokenInterface
from src.domain.models.model_person import PersonModel
from typing import List, Dict
import jwt
from datetime import datetime, timedelta, timezone


KEY="luizfelipedemenezesbernardo_27.09.90/37"



class Token(TokenInterface):

    def authenticate(self, person: PersonModel) -> Dict:
        token_data = {
            "sub": person.id,
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        }

        token = jwt.encode(token_data, KEY, algorithm="HS256")

        return {'success': True, "access_token": token}

    def decode(self, token: str) -> Dict:
        try:
            return jwt.decode(token,KEY,algorithms=["HS256"])
        
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError:
            raise ValueError("Token Invalido")