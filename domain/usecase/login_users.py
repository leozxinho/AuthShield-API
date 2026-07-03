from datetime import datetime, timedelta
from infrastructure.security.jwt_security import create_access_token, refresh_access_token
from infrastructure.repositories.users_repository import UserRepository
from infrastructure.repositories.login_log_repository import LoginLogRepository
from infrastructure.repositories.reflesh_tokens_repository import RefreshTokensRepository
from infrastructure.email.email_service import send_suspicious_login_email
from infrastructure.security.hash_secutiry import Hash


class LoginUserUseCase:

    @staticmethod
    async def execute(email: str, password: str, ip_address: str = "", user_agent: str = "") -> dict:
        repository = UserRepository()
        log_repo = LoginLogRepository()

        user = await repository.find_by_email(email)
        if not user:
            raise ValueError("Usuário não encontrado")

        if not user.is_verified:
            raise ValueError("Usuário não verificado. Por favor, verifique seu email.")

        if not user.is_active:
            raise ValueError("Usuário inativo. Por favor, entre em contato com o suporte.")

        if user.locked_until and user.locked_until > datetime.utcnow():
            raise ValueError("Usuário está temporariamente bloqueado")

        if not Hash.verify(password, user.password_hash):

            await log_repo.create_log(user_id=user.id, ip_address=ip_address, user_agent=user_agent, success=False)

            await repository.increment_failed_login_attempts(user.id)
            if user.failed_login_attempts + 1 >= 5:  # Se o número de tentativas falhas for maior ou igual a 5, bloqueia a conta por 15 minutos
                lock_until = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                await repository.lock_account(user.id, lock_until)

            if user.password_changed_at:
                days_since_change = (datetime.utcnow() - user.password_changed_at).days
                if days_since_change >= 90:
                    raise ValueError("Senha expirada. Por favor, redefina sua senha.")

            raise ValueError("Senha incorreta")

        await log_repo.create_log(user_id=user.id, ip_address=ip_address, user_agent=user_agent, success=True)

        # Verificar se o IP é conhecido
        known_ips = await log_repo.get_known_ips(user.id)
        if ip_address and ip_address not in known_ips:
            await send_suspicious_login_email(user.email, ip_address, user_agent)

        await repository.reset_failed_login_attempts(user.id)
        access_token = await create_access_token(data={"sub": str(user.id)})
        refresh_token = await refresh_access_token(data={"sub": str(user.id)})

        # Salvar refresh token no banco
        refresh_repo = RefreshTokensRepository()
        expires_at = datetime.utcnow() + timedelta(days=1)
        await refresh_repo.save(user_id=user.id, token=refresh_token, expires_at=expires_at)

        return {
            "user_id": user.id,
            "email": user.email,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
