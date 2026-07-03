from domain.entities.users import User
from infrastructure.repositories.users_repository import UserRepository
from infrastructure.repositories.reflesh_tokens_repository import RefreshTokensRepository


class DeleteAccountUseCase:

    @staticmethod
    async def execute(user: User) -> dict:
        user_repository = UserRepository() 
        await user_repository.deactivate_user(user.id)  # Desativa a conta do usuário no banco de dados

        refresh_repository = RefreshTokensRepository() 
        await refresh_repository.revoke_all_by_user_id(user.id) # Revoga todos os tokens de atualização associados ao usuário

        return {"message": "Conta desativada com sucesso"}
