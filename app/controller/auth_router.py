from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.schemas.login_schema import LoginSchema
from app.schemas.register_schema import RegisterSchema
from app.schemas.forgot_password_schema import ForgotPasswordSchema
from app.schemas.reset_password_schema import ResetPasswordSchema
from app.schemas.change_password_schema import ChangePasswordSchema
from app.schemas.update_profile_schema import UpdateProfileSchema
from app.dependencies import get_current_user
from domain.entities.users import User
from domain.usecase.login_users import LoginUserUseCase
from domain.usecase.register_users import RegisterUserUseCase
from domain.usecase.logout_users import LogoutUserUseCase
from domain.usecase.verify_token import VerifyEmailUseCase
from domain.usecase.reflesh_token import RefreshTokenUseCase
from domain.usecase.forgot_password import ForgotPasswordUseCase
from domain.usecase.reset_password import ResetPasswordUseCase
from domain.usecase.change_password import ChangePasswordUseCase
from domain.usecase.update_profile import UpdateProfileUseCase
from domain.usecase.delete_account_usecase import DeleteAccountUseCase
from app.rate_limiter import limiter


router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()


# ==================== ENDPOINTS PÚBLICOS ====================


@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, data: LoginSchema):
    ip = request.client.host
    ua = request.headers.get("user-agent", "desconhecido")
    try:
        result = await LoginUserUseCase.execute(email=data.email, password=data.password, ip_address=ip, user_agent=ua)
        return result
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/register")
@limiter.limit("5/minute")
async def register(request: Request, data: RegisterSchema):
    try:
        return await RegisterUserUseCase.execute(name=data.name, email=data.email, password=data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/verify")
@limiter.limit("5/minute")
async def verify_email(request: Request, verification_token: str):
    try:
        return await VerifyEmailUseCase.execute(verification_token=verification_token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/forgot-password")
@limiter.limit("5/minute")
async def forgot_password(request: Request, data: ForgotPasswordSchema):
    try:
        return await ForgotPasswordUseCase.execute(email=data.email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reset-password")
@limiter.limit("5/minute")
async def reset_password(request: Request, data: ResetPasswordSchema):
    try:
        return await ResetPasswordUseCase.execute(token=data.token, new_password=data.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==================== ENDPOINTS PROTEGIDOS ====================


@router.post("/refresh")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        return await RefreshTokenUseCase.execute(refresh_token=credentials.credentials)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = f"Bearer {credentials.credentials}"
        return await LogoutUserUseCase.execute(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.put("/change-password")
async def change_password(data: ChangePasswordSchema, current_user: User = Depends(get_current_user)):
    try:
        return await ChangePasswordUseCase.execute(
            user=current_user,
            current_password=data.current_password,
            new_password=data.new_password
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.put("/profile")
async def update_profile(data: UpdateProfileSchema, current_user: User = Depends(get_current_user)):
    try:
        return await UpdateProfileUseCase.execute(
            user=current_user,
            name=data.name,
            email=data.email
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/account")
async def delete_account(current_user: User = Depends(get_current_user)):
    try:
        return await DeleteAccountUseCase.execute(user=current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
