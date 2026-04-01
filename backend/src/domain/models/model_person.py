from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, Field


class PersonModel(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length= 100,
        description="Nome completo"
        )
    cpf: str = Field(
        ...,
        )
    cnpj: str = Field(
        ...,
        description = "CNPJ somente número"
    )
    phone: str = Field(
        ...,
        min_length=10,
        description="Telefone com ddd"
    )
    email: str = Field(
        ...,
        description="Email mais usado"
    )
    password: str = Field(
        ...,
        min_length=3,
        description="utilize uma senha forte"
    )
    id: int = Field(
        None,
        description="ID unico do usuario"
    )



class CustomerModel(BaseModel):
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