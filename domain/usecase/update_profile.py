from datetime import timedelta

from domain.entities.users import User
from infrastructure.repositories.users_repository import UserRepository
from infrastructure.security.jwt_security import create_access_token
from infrastructure.email.email_service import send_validation_email


class UpdateProfileUseCase:

    @staticmethod
    async def execute(user: User, name: str | None = None, email: str | None = None) -> dict:
        repository = UserRepository()

        if email is not None and email != user.email: # Verifica se o email fornecido é diferente do email atual do usuário
            existing = await repository.find_by_email(email)
            if existing:
                raise ValueError("Este email já está em uso por outro usuário")

            token = await create_access_token(   # Cria um token de acesso para validação do novo email
                {"sub": str(user.id), "type": "email_change", "new_email": email},
                expires_delta=timedelta(hours=24)
            )

            await repository.save_verification_token(user.id, token)

            await send_validation_email(email, token)

        if name is not None and name != user.name:  # Verifica se o nome fornecido é diferente do nome atual do usuário
            await repository.update_profile(user_id=user.id, name=name)

        if email is not None and email != user.email:  #  Verifica se o email fornecido é diferente do email atual do usuário
            await repository.update_profile(user_id=user.id, email=email, is_verified=False)
            return {"message": "Perfil atualizado. Verifique o novo email para confirmar a alteração"}

        return {"message": "Perfil atualizado"}
