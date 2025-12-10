from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_client_and_api_key
from app.db.session import get_db
from app.schemas.lead import LeadCreate, LeadRead
from app.models.lead import Lead
from app.models.client import Client

router = APIRouter()


@router.post("/", response_model=LeadRead)
def create_lead(
    payload: LeadCreate,
    client: Client = Depends(get_client_and_api_key),
    db: Session = Depends(get_db),
):
    lead = Lead(
        client_id=client.id,
        **payload.model_dump()
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get("/", response_model=list[LeadRead])
def list_leads(
    client: Client = Depends(get_client_and_api_key),
    db: Session = Depends(get_db),
):
    leads = db.query(Lead).filter(
        Lead.client_id == client.id
    ).order_by(Lead.id.desc()).all()

    return leads
