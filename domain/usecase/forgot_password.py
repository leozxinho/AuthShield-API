from datetime import timedelta

from infrastructure.repositories.users_repository import UserRepository
from infrastructure.security.jwt_security import create_access_token
from infrastructure.email.email_service import send_password_reset_email


class ForgotPasswordUseCase:

    @staticmethod
    async def execute(email: str) -> dict:
        repository = UserRepository()

        user = await repository.find_by_email(email)
        if user:
            token = await create_access_token(
                {"sub": str(user.id), "type": "password_reset"},
                expires_delta=timedelta(hours=1),
            )
            await send_password_reset_email(user.email, token)

        # Sempre retorna sucesso para não revelar se o email existe
        return {"message": "Se o email estiver cadastrado, você receberá um link de redefinição de senha"}
