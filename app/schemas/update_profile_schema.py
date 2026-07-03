from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class UpdateProfileSchema(BaseModel):
    """
    Schema responsável por validar
    os dados recebidos na atualização de perfil.
    """

    name: Optional[str] = Field(None, min_length=3, max_length=100, description="Nome do usuário")
    email: Optional[EmailStr] = Field(None, description="Novo email do usuário")

    @field_validator('name')
    @classmethod
    def validate_name(cls, value):
        if value is not None and not value.replace(" ", "").isalpha():
            raise ValueError('O nome deve conter apenas letras e espaços.')
        return value
