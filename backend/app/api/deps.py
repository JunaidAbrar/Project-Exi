from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.client import Client
from app.models.api_key import ApiKey


async def get_client_and_api_key(
    x_client_id: str | None = Header(default=None, alias=settings.CLIENT_ID_HEADER),
    x_api_key: str | None = Header(default=None, alias=settings.API_KEY_HEADER),
    db: Session = Depends(get_db),
) -> Client:
    if not x_client_id or not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing client or API key",
        )

    client = (
        db.query(Client)
        .filter(Client.slug == x_client_id, Client.is_active.is_(True))
        .first()
    )
    if not client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client",
        )

    api_key = (
        db.query(ApiKey)
        .filter(
            ApiKey.client_id == client.id,
            ApiKey.key == x_api_key,
            ApiKey.is_active.is_(True),
        )
        .first()
    )
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return client
