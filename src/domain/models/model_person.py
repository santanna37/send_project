from dataclasses import dataclass
from typing import Optional

@dataclass
class PersonModel:
    name: str
    id: int |None = None
    email: str
