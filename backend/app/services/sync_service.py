from typing import Dict, Any

from sqlalchemy.orm import Session

from app.models.client import Client
from app.models.rental import Rental
from app.services.google_sheet_service import fetch_rows_from_sheet
from app.services.embedding_service import build_rental_text, embed_text
from app.services.vector_service import upsert_rental_embedding, delete_rental_embeddings


def _parse_int(value: str) -> int | None:
    value = value.strip()
    if not value:
        return None
    try:
        return int(float(value))
    except ValueError:
        return None


def _parse_decimal_str(value: str) -> str:
    value = value.strip()
    if not value:
        return "0"
    # keep as string; SQLAlchemy Numeric will handle conversion
    return value


def _parse_bool(value: str) -> bool | None:
    value = value.strip().lower()
    if not value:
        return None
    if value in ("true", "yes", "1", "y"):
        return True
    if value in ("false", "no", "0", "n"):
        return False
    return None


def sync_client_rentals_from_sheet(db: Session, client: Client) -> Dict[str, Any]:
    """
    Syncs rentals for a single client from its Google Sheet.
    - Inserts new rentals
    - Updates changed rentals
    - Marks missing rentals as inactive
    - Updates Qdrant vectors for new/updated
    - Deletes Qdrant vectors for deactivated
    """
    if not client.sheet_url:
        return {"status": "skipped", "reason": "no_sheet_url"}

    rows = fetch_rows_from_sheet(client.sheet_url)

    # map external_id -> sheet row
    sheet_by_external: Dict[str, dict] = {}
    for row in rows:
        ext_id = row.get("external_id", "").strip()
        if not ext_id:
            continue
        sheet_by_external[ext_id] = row

    # existing rentals for client
    existing_rentals: list[Rental] = (
        db.query(Rental)
        .filter(Rental.client_id == client.id)
        .all()
    )
    rentals_by_external = {r.external_id: r for r in existing_rentals}

    created = 0
    updated = 0
    deactivated = 0

    updated_rental_ids: list[int] = []
    created_rental_ids: list[int] = []
    deactivated_rental_ids: list[int] = []

    # upsert based on sheet
    for ext_id, row in sheet_by_external.items():
        weekly_rent = _parse_decimal_str(row["weekly_rent"])
        bedrooms = _parse_int(row["bedrooms"]) or 0
        bathrooms = _parse_int(row["bathrooms"]) or 0
        car_spaces = _parse_int(row["car_spaces"])
        pet_allowed = _parse_bool(row["pet_allowed"])

        if ext_id in rentals_by_external:
            rental = rentals_by_external[ext_id]

            has_changes = (
                rental.address != row["address"]
                or rental.suburb != row["suburb"]
                or rental.state != row["state"]
                or rental.postcode != row["postcode"]
                or str(rental.weekly_rent) != weekly_rent
                or rental.bedrooms != bedrooms
                or rental.bathrooms != bathrooms
                or rental.car_spaces != car_spaces
                or rental.pet_allowed != pet_allowed
                or (rental.description or "") != row["description"]
                or (rental.image_urls or "") != row["image_urls"]
                or rental.is_active is False
            )

            if has_changes:
                rental.address = row["address"]
                rental.suburb = row["suburb"]
                rental.state = row["state"]
                rental.postcode = row["postcode"]
                rental.weekly_rent = weekly_rent
                rental.bedrooms = bedrooms
                rental.bathrooms = bathrooms
                rental.car_spaces = car_spaces
                rental.pet_allowed = pet_allowed
                rental.description = row["description"] or None
                rental.image_urls = row["image_urls"] or None
                rental.is_active = True
                updated += 1
                updated_rental_ids.append(rental.id)
        else:
            rental = Rental(
                client_id=client.id,
                external_id=ext_id,
                address=row["address"],
                suburb=row["suburb"],
                state=row["state"],
                postcode=row["postcode"],
                weekly_rent=weekly_rent,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                car_spaces=car_spaces,
                pet_allowed=pet_allowed,
                description=row["description"] or None,
                image_urls=row["image_urls"] or None,
                is_active=True,
            )
            db.add(rental)
            db.flush()  # to get rental.id
            created += 1
            created_rental_ids.append(rental.id)

    # mark missing rentals as inactive
    sheet_external_ids = set(sheet_by_external.keys())
    db_external_ids = set(rentals_by_external.keys())

    missing_ext_ids = db_external_ids - sheet_external_ids
    for ext_id in missing_ext_ids:
        rental = rentals_by_external[ext_id]
        if rental.is_active:
            rental.is_active = False
            deactivated += 1
            deactivated_rental_ids.append(rental.id)

    db.commit()

    # embeddings for created + updated
    # we re-query to ensure we have latest data
    if created_rental_ids or updated_rental_ids:
        all_ids = created_rental_ids + updated_rental_ids
        rentals = (
            db.query(Rental)
            .filter(
                Rental.client_id == client.id,
                Rental.id.in_(all_ids),
            )
            .all()
        )
        for rental in rentals:
            text = build_rental_text(
                address=rental.address,
                suburb=rental.suburb,
                state=rental.state,
                postcode=rental.postcode,
                description=rental.description,
                pet_allowed=rental.pet_allowed,
            )
            vector = embed_text(text)
            upsert_rental_embedding(client.id, rental, vector)

    # delete embeddings for deactivated rentals
    if deactivated_rental_ids:
        delete_rental_embeddings(client.id, deactivated_rental_ids)

    return {
        "status": "ok",
        "client_id": client.id,
        "created": created,
        "updated": updated,
        "deactivated": deactivated,
    }
