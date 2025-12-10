import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.client import Client
from app.models.api_key import ApiKey
from app.schemas.client import ClientCreate, ClientRead
from app.schemas.api_key import ApiKeyRead

router = APIRouter()


@router.post("/", response_model=ClientRead)
def create_client(payload: ClientCreate, db: Session = Depends(get_db)):
    existing = db.query(Client).filter(Client.slug == payload.slug).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client slug already exists",
        )
    client = Client(name=payload.name, slug=payload.slug)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.post("/{client_slug}/keys", response_model=ApiKeyRead)
def create_api_key_for_client(client_slug: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.slug == client_slug, Client.is_active.is_(True)).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found",
        )

    raw_key = secrets.token_urlsafe(32)
    api_key = ApiKey(client_id=client.id, key=raw_key, description="default")

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return api_key
