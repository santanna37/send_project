from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict




class CustomerModel(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    name: str = Field(
        ...,
        min_length= 3,
        max_length= 100,
        description="Nome completo"
    )
    cnpj: str = Field(
        ...,
        description="CNPJ somente números"
    )
    phone: str = Field(
        ...,
        min_length=10,
        description="Telefone com DDD"
    )
    email: str = Field(
        ...,
        description="email mais usado"
    )
    id_person: int = Field(
        None,
        description="ID do person"
    )
    id: int = Field(
        None,
        description="ID unico da empresa"
    )
