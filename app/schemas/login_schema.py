# Importações do Pydantic
from pydantic import BaseModel, EmailStr, Field


class LoginSchema(BaseModel):
    """
    Schema responsável por validar
    os dados recebidos no login.
    """

    # Valida formato de email
    email: EmailStr

    # Exige no mínimo 6 caracteres
    password: str = Field(
        min_length=6,
        max_length=100,
        description="Senha do usuário"
    )