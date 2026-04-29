from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes_auth import router_auth
from app.api.routes_chat import router_chat
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.core.errors import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception:
        raise

    yield
    
    await engine.dispose()


def create_app():
    app = FastAPI(
        title=settings.APP_NAME,
        lifespan=lifespan
    )

    @app.get("/health", tags=["health"])
    async def health_check() -> dict:
        return {
            "status": "healthy",
            "environment": settings.ENV,
        }
    
    register_exception_handlers(app)
    
    app.include_router(router_chat)
    app.include_router(router_auth)

    return app

app = create_app()