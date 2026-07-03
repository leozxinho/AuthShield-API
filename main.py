from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.controller.auth_router import router as auth_router
from infrastructure.database.create_tables import create_tables
from infrastructure.database.connection import create_pool, close_pool

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.rate_limiter import limiter




@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_pool()
    await create_tables()
    yield
    await close_pool()


app = FastAPI(
    lifespan=lifespan,
    title="Sistema de Login",
    version="1.0.0",
    description="API de autenticação com FastAPI",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(auth_router)



@app.get("/")
def home():
    return {"message": "API Online"}
