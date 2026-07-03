from datetime import datetime
from jose import jwt, JWTError
from infrastructure.repositories.token_repository import add_to_blacklist
from infrastructure.config.settings import get_settings


class LogoutUserUseCase:

    @staticmethod
    async def execute(authorization: str) -> dict:
        if not authorization.startswith("Bearer "):
            raise ValueError("Token inválido ou ausente")

        token = authorization.replace("Bearer ", "", 1)
        settings = get_settings()

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except JWTError:
            raise ValueError("Token inválido ou expirado")

        exp_timestamp = payload.get("exp")
        if exp_timestamp is None:
            raise ValueError("Token sem campo de expiração")

        expires_at = datetime.utcfromtimestamp(exp_timestamp)

        await add_to_blacklist(token, expires_at)

        return {"detail": "Logout realizado com sucesso"}
