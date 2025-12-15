from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.models import *  # noqa
from app.db.session import engine
from app.db.base import Base
from app.services.sync_scheduler import start_scheduler_thread


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the background scheduler thread
    start_scheduler_thread()
    yield
    # Shutdown: (thread is daemon, so it will auto-terminate)


def create_app() -> FastAPI:
    app = FastAPI(title="Project EXi API", lifespan=lifespan)

    # DB init (later use Alembic migrations in production)
    Base.metadata.create_all(bind=engine)

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
