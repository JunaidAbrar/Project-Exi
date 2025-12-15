from typing import List, Dict

import gspread
from google.oauth2.service_account import Credentials

from app.core.config import settings


SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

EXPECTED_COLUMNS = [
    "external_id",
    "address",
    "suburb",
    "state",
    "postcode",
    "weekly_rent",
    "bedrooms",
    "bathrooms",
    "car_spaces",
    "description",
    "image_urls",
]


def _get_gspread_client() -> gspread.Client:
    if not settings.GOOGLE_SERVICE_ACCOUNT_FILE:
        raise RuntimeError("GOOGLE_SERVICE_ACCOUNT_FILE not configured")

    creds = Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_FILE,
        scopes=SCOPES,
    )
    return gspread.authorize(creds)


def fetch_rows_from_sheet(sheet_url: str) -> List[Dict[str, str]]:
    """
    Returns a list of dicts where keys are EXPECTED_COLUMNS and values are cell strings.
    Missing columns are set to "".
    """
    gc = _get_gspread_client()
    sh = gc.open_by_url(sheet_url)
    ws = sh.sheet1  # first worksheet

    data = ws.get_all_records()  # list of dicts keyed by header row

    rows: List[Dict[str, str]] = []
    for row in data:
        normalized: Dict[str, str] = {}
        # Normalize keys: lower + underscore
        normalized_row = {k.strip().lower().replace(" ", "_"): str(v).strip() for k, v in row.items()}

        for col in EXPECTED_COLUMNS:
            normalized[col] = normalized_row.get(col, "")
        rows.append(normalized)

    return rows
