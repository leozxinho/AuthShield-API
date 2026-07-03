from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from infrastructure.security.jwt_security import verify_token
from infrastructure.repositories.users_repository import UserRepository

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependência que extrai e valida o usuário a partir do token JWT.
    Pode ser usada em qualquer endpoint protegido.
    """
    token = credentials.credentials
    try:
        payload = await verify_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = await UserRepository().find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return user
