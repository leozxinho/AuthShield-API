from domain.entities.users import User
from infrastructure.repositories.users_repository import UserRepository
from infrastructure.repositories.password_history_repository import PasswordHistoryRepository
from infrastructure.security.hash_secutiry import Hash


class ChangePasswordUseCase:

    @staticmethod
    async def execute(user: User, current_password: str, new_password: str) -> dict:
        # 1. Verificar senha atual
        if not Hash.verify(current_password, user.password_hash):
            raise ValueError("Senha atual incorreta")

        # 2. Verificar se a nova senha é igual à atual
        if Hash.verify(new_password, user.password_hash):
            raise ValueError("A nova senha não pode ser igual à senha atual")

        # 3. Verificar histórico de senhas (últimas 5)
        history_repository = PasswordHistoryRepository()
        last_passwords = await history_repository.get_last_passwords(user.id, limit=5)
        for old_hash in last_passwords:
            if Hash.verify(new_password, old_hash):
                raise ValueError("A nova senha não pode ser igual a uma das últimas 5 senhas utilizadas")

        # 4. Fazer hash da nova senha
        hashed = Hash.hash(new_password)

        # 5. Salvar senha atual no histórico
        await history_repository.save(user_id=user.id, password_hash=user.password_hash)

        # 6. Atualizar senha no banco
        user_repository = UserRepository()
        await user_repository.update_password(user_id=user.id, password_hash=hashed)

        return {"message": "Senha alterada com sucesso"}
