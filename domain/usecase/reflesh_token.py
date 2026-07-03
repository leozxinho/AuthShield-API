from datetime import timedelta
from infrastructure.repositories.reflesh_tokens_repository import RefreshTokensRepository
from infrastructure.security.jwt_security import (
    create_access_token,
    refresh_access_token,
    verify_token
)


class RefreshTokenUseCase:

    @staticmethod
    async def execute(refresh_token: str) -> dict:
        repository = RefreshTokensRepository()

        # 1. Verifica se o token existe e não está revogado
        token_record = await repository.find_valid(refresh_token)
        if not token_record:
            raise ValueError("Token inválido")

        # 2. Decodifica o JWT para extrair o user_id
        try:
            payload = await verify_token(refresh_token)
        except Exception:
            raise ValueError("Token inválido")

        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token inválido")

        # 3. Revoga o token atual (uso único)
        await repository.revoke(refresh_token)

        # 4. Gera novo par de tokens
        new_access_token = await create_access_token(
            {"sub": str(user_id), "type": "access"},
            expires_delta=timedelta(minutes=15)
        )
        new_refresh_token = await refresh_access_token(
            {"sub": str(user_id), "type": "refresh"}
        )

        # 5. Salva o novo refresh token no banco
        await repository.save(user_id=int(user_id), token=new_refresh_token)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
