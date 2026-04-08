from src.data.interface.token_data_interface import TokenAuthInterface
from src.domain.models.model_person import PersonModel
from typing import List, Dict
import jwt
from datetime import datetime, timedelta, timezone


KEY="luizfelipedemenezesbernardo_27.09.90/37"



class TokenAuth(TokenAuthInterface):

    def authenticate(self, person: PersonModel) -> Dict:
        token_data = {
            "sub": person.id,
            "exp": datetime.now(timezone.utc) + timedelta(hours=24)
        }

        token = jwt.encode(token_data, KEY, algorithm="HS256")

        return {'success': True, "access_token": token}
