from fastapi import APIRouter

from app.api.v1 import health, clients, rentals, leads, sync

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(rentals.router, prefix="/rentals", tags=["rentals"])
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(sync.router, prefix="/sync", tags=["sync"])