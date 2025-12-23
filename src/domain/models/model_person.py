from dataclasses import dataclass
from typing import Optional

@dataclass
class PersonModel:
    name: str
    email: str
    id: int |None = None
