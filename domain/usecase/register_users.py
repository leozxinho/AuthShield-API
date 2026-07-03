from datetime import timedelta

from infrastructure.repositories.users_repository import UserRepository
from infrastructure.security.hash_secutiry import Hash
from infrastructure.security.jwt_security import create_access_token
from infrastructure.email.email_service import send_validation_email


class RegisterUserUseCase:

    @staticmethod
    async def execute(name: str, email: str, password: str) -> dict:
        repository = UserRepository()

        existing = await repository.find_by_email(email)
        if existing:
            raise ValueError("Email já cadastrado")

        hashed = Hash.hash(password)
        user_id = await repository.create(name=name, email=email, password_hash=hashed)

        # Gerar token de verificação de email
        token = await create_access_token(
            {"sub": str(user_id), "type": "email_verification"},
            expires_delta=timedelta(hours=24)
        )

        # Salvar token no banco
        await repository.save_verification_token(user_id, token)

        # Enviar email de verificação
        await send_validation_email(email, token)

        return {"message": "Registro realizado. Verifique seu email para ativar a conta"}
