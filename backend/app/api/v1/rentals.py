from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_client_and_api_key
from app.db.session import get_db
from app.schemas.rental import RentalCreate, RentalRead
from app.models.rental import Rental
from app.models.client import Client

router = APIRouter()


@router.post("/", response_model=RentalRead)
def create_rental(
    payload: RentalCreate,
    client: Client = Depends(get_client_and_api_key),
    db: Session = Depends(get_db),
):
    rental = Rental(
        client_id=client.id,
        **payload.model_dump()
    )
    db.add(rental)
    db.commit()
    db.refresh(rental)
    return rental


@router.get("/", response_model=list[RentalRead])
def list_rentals(
    client: Client = Depends(get_client_and_api_key),
    db: Session = Depends(get_db),
):
    rentals = db.query(Rental).filter(
        Rental.client_id == client.id
    ).all()
    return rentals


@router.get("/{rental_id}", response_model=RentalRead)
def get_rental(
    rental_id: int,
    client: Client = Depends(get_client_and_api_key),
    db: Session = Depends(get_db),
):
    rental = db.query(Rental).filter(
        Rental.id == rental_id,
        Rental.client_id == client.id
    ).first()

    if not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental not found"
        )
    return rental


@router.delete("/{rental_id}")
def delete_rental(
    rental_id: int,
    client: Client = Depends(get_client_and_api_key),
    db: Session = Depends(get_db),
):
    rental = db.query(Rental).filter(
        Rental.id == rental_id,
        Rental.client_id == client.id
    ).first()

    if not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental not found"
        )

    db.delete(rental)
    db.commit()
    return {"status": "deleted"}
