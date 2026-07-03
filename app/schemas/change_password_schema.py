from pydantic import BaseModel, Field, field_validator


class ChangePasswordSchema(BaseModel):
    """
    Schema responsável por validar
    os dados recebidos na alteração de senha.
    """

    current_password: str = Field(
        min_length=1,
        description="Senha atual do usuário"
    )
    new_password: str = Field(
        min_length=8,
        max_length=100,
        description="Nova senha do usuário"
    )

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, value):
        if not any(c.isupper() for c in value):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula.')
        if not any(c.isdigit() for c in value):
            raise ValueError('A senha deve conter pelo menos um número.')
        if not any(c in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for c in value):
            raise ValueError('A senha deve conter pelo menos um caractere especial.')
        return value
