from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_client_and_api_key
from app.db.session import get_db
from app.models.client import Client
from app.services.sync_service import sync_client_rentals_from_sheet

router = APIRouter()


@router.post("/google-sheet")
def trigger_google_sheet_sync(
    client: Client = Depends(get_client_and_api_key),
    db: Session = Depends(get_db),
):
    result = sync_client_rentals_from_sheet(db=db, client=client)
    return result
