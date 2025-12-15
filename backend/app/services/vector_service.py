from typing import List
import uuid

from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from app.core.config import settings
from app.models.rental import Rental


_client: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )
        _ensure_collection()
    return _client


def _ensure_collection() -> None:
    client = QdrantClient(
        host=settings.QDRANT_HOST,
        port=settings.QDRANT_PORT,
    )
    collection_name = settings.QDRANT_COLLECTION_RENTALS

    existing = client.get_collections()
    exists = any(c.name == collection_name for c in existing.collections)

    if not exists:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=qmodels.VectorParams(
                size=settings.QDRANT_EMBED_DIM,
                distance=qmodels.Distance.COSINE,
            ),
        )


def rental_point_id(client_id: int, rental_id: int) -> str:
    """Generate a deterministic UUID for a rental point based on client_id and rental_id."""
    # Use a fixed namespace UUID for consistency
    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')  # DNS namespace UUID
    combined = f"{client_id}:{rental_id}"
    return str(uuid.uuid5(namespace, combined))


def upsert_rental_embedding(
    client_id: int,
    rental: Rental,
    vector: List[float],
) -> None:
    client = get_qdrant_client()
    collection_name = settings.QDRANT_COLLECTION_RENTALS

    payload = {
        "client_id": client_id,
        "rental_id": rental.id,
        "external_id": rental.external_id,
        "suburb": rental.suburb,
        "state": rental.state,
        "postcode": rental.postcode,
        "pet_allowed": rental.pet_allowed,
        "is_active": rental.is_active,
    }

    client.upsert(
        collection_name=collection_name,
        points=[
            qmodels.PointStruct(
                id=rental_point_id(client_id, rental.id),
                vector=vector,
                payload=payload,
            )
        ],
    )


def delete_rental_embeddings(
    client_id: int,
    rental_ids: List[int],
) -> None:
    if not rental_ids:
        return

    client = get_qdrant_client()
    collection_name = settings.QDRANT_COLLECTION_RENTALS

    point_ids = [rental_point_id(client_id, rid) for rid in rental_ids]

    client.delete(
        collection_name=collection_name,
        points_selector=qmodels.PointIdsList(points=point_ids),
    )
