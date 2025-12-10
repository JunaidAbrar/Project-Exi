from fastapi import FastAPI
from app.api.v1.router import api_router
from app.models import *  # noqa
from app.db.session import engine
from app.db.base import Base


def create_app() -> FastAPI:
    app = FastAPI(title="Project EXi API")

    # DB init (later use Alembic migrations in production)
    Base.metadata.create_all(bind=engine)

    app.include_router(api_router, prefix="/api/v1")

    return app


app = create_app()
