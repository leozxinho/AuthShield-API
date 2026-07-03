from pydantic import BaseModel, EmailStr


class ForgotPasswordSchema(BaseModel):
    """
    Schema responsável por validar
    os dados recebidos na solicitação de redefinição de senha.
    """

    email: EmailStr
