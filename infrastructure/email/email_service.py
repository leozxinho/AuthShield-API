import aiosmtplib
from email.mime.text import MIMEText
from infrastructure.config.settings import get_settings


async def send_validation_email(to_email: str, verification_token: str):
    """
    Envia um email de validação para o usuário com o token de verificação.
    """
    settings = get_settings()

    subject = "Validação de Conta"
    body = f"Por favor, clique no link abaixo para validar sua conta:\n\nhttp://localhost:8000/auth/verify?verification_token={verification_token}"

    message = MIMEText(body)
    message["From"] = settings.EMAIL_USER
    message["To"] = to_email
    message["Subject"] = subject

    try:
        async with aiosmtplib.SMTP(hostname=settings.EMAIL_HOST, port=settings.EMAIL_PORT) as smtp:
            await smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            await smtp.send_message(message)
    except Exception as e:
        print(f"[EMAIL] Falha ao enviar email de validação para {to_email}: {e}")


async def send_suspicious_login_email(to_email: str, ip_address: str, user_agent: str):
    """
    Envia um email de alerta para o usuário sobre uma tentativa de login suspeita.
    """
    settings = get_settings()

    subject = "Alerta de Tentativa de Login Suspeita"
    body = f"Detectamos uma tentativa de login suspeita em sua conta.\n\nEndereço IP: {ip_address}\nAgente do Usuário: {user_agent}\n\nSe não foi você, por favor, altere sua senha imediatamente."

    message = MIMEText(body)
    message["From"] = settings.EMAIL_USER
    message["To"] = to_email
    message["Subject"] = subject

    try:
        async with aiosmtplib.SMTP(hostname=settings.EMAIL_HOST, port=settings.EMAIL_PORT) as smtp:
            await smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            await smtp.send_message(message)
    except Exception as e:
        print(f"[EMAIL] Falha ao enviar alerta de login suspeito para {to_email}: {e}")


async def send_password_reset_email(to_email: str, token: str):
    """
    Envia um email com o link de redefinição de senha.
    """
    settings = get_settings()

    reset_link = f"http://localhost:8000/auth/reset-password?token={token}"
    subject = "Redefinição de Senha"
    body = f"Você solicitou a redefinição de senha.\n\nClique no link abaixo para redefinir sua senha:\n\n{reset_link}\n\nEste link expira em 1 hora."

    message = MIMEText(body)
    message["From"] = settings.EMAIL_USER
    message["To"] = to_email
    message["Subject"] = subject

    try:
        async with aiosmtplib.SMTP(hostname=settings.EMAIL_HOST, port=settings.EMAIL_PORT) as smtp:
            await smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
            await smtp.send_message(message)
    except Exception as e:
        print(f"[EMAIL] Falha ao enviar email de redefinição de senha para {to_email}: {e}")
