from typing import List
import numpy as np
from app.core.config import settings

EMBED_DIM = settings.QDRANT_EMBED_DIM


def build_rental_text(
    address: str,
    suburb: str,
    state: str,
    postcode: str,
    description: str | None,
    pet_allowed: bool | None = None,
) -> str:
    parts = [
        address,
        suburb,
        state,
        postcode,
    ]
    if pet_allowed is not None:
        parts.append("Pets allowed" if pet_allowed else "No pets")
    if description:
        parts.append(description)
    return ", ".join([p for p in parts if p])


def embed_text(text: str) -> List[float]:
    """
    TODO: Replace with real Groq Llama 3.1 8B embedding call.
    For now: deterministic pseudo-embedding for development.
    """
    if not text:
        text = "empty"

    rng = np.random.default_rng(abs(hash(text)) % (2**32))
    vec = rng.normal(size=EMBED_DIM)
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec.tolist()
    return (vec / norm).tolist()
