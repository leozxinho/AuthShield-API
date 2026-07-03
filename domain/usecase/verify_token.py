from infrastructure.repositories.users_repository import UserRepository
from infrastructure.security.jwt_security import verify_token


class VerifyEmailUseCase:

    @staticmethod
    async def execute(verification_token: str) -> dict:
        # Decodifica o token JWT
        try:
            payload = await verify_token(verification_token)
        except Exception:
            raise ValueError("Token de verificação inválido ou expirado")

        token_type = payload.get("type")
        if token_type != "email_verification":
            raise ValueError("Token de verificação inválido")

        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token de verificação inválido")

        repository = UserRepository()
        user = await repository.find_by_id(int(user_id))

        if not user:
            raise ValueError("Usuário não encontrado")

        if user.is_verified:
            raise ValueError("Email já verificado")

        await repository.verify_user(int(user_id))

        return {"message": "Email verificado com sucesso"}
