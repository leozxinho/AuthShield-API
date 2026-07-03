from pydantic import BaseModel, EmailStr, Field, field_validator

class RegisterSchema(BaseModel):
    """
    Schema responsável por validar
    os dados recebidos no registro.
    """

    email: EmailStr
    name: str = Field(min_length=3, max_length=100, description="Nome do usuário") # Exige no mínimo 3 caracteres
    password: str = Field(
        min_length=8,
        max_length=100,
        description="Senha do usuário"
    )
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if not any(c.isupper() for c in value):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula.')
        if not any(c.isdigit() for c in value):
            raise ValueError('A senha deve conter pelo menos um número.')
        if not any(c in "!@#$%^&*()-_=+[{]}\|;:'\",<.>/?`~" for c in value):
            raise ValueError('A senha deve conter pelo menos um caractere especial.')
        return value
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError('O nome deve conter apenas letras e espaços.')
        return value