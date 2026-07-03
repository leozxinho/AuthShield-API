from infrastructure.repositories.users_repository import UserRepository
from infrastructure.security.hash_secutiry import Hash
from infrastructure.security.jwt_security import verify_token


class ResetPasswordUseCase:
    @staticmethod
    async def execute(token: str, new_password: str) -> dict:
        try:
            payload = await verify_token(token)
        except Exception:
            raise ValueError("Token inválido ou expirado")
        
        if payload.get("type") != "password_reset":
            raise ValueError("Token inválido para redefinição de senha")

        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token inválido")

        hashed = Hash.hash(new_password)

        repository = UserRepository()
        await repository.update_password(user_id=int(user_id), password_hash=hashed)

        return {"message": "Senha redefinida com sucesso"}
