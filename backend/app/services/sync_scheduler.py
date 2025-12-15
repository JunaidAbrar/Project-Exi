import time
import threading
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.client import Client
from app.services.sync_service import sync_client_rentals_from_sheet


def run_periodic_sheet_sync() -> None:
    """
    Simple background loop:
    - every N seconds
    - for each active client with sheet_url
    - run sync_client_rentals_from_sheet
    """
    interval = settings.SHEET_SYNC_INTERVAL_SECONDS

    while True:
        db: Session = SessionLocal()
        try:
            clients = (
                db.query(Client)
                .filter(
                    Client.is_active.is_(True),
                    Client.sheet_url.isnot(None),
                )
                .all()
            )
            for client in clients:
                try:
                    result = sync_client_rentals_from_sheet(db, client)
                    # For now: minimal log
                    print(f"[sync] client={client.slug} -> {result}")
                except Exception as e:
                    print(f"[sync] error for client {client.slug}: {e}")
        finally:
            db.close()

        time.sleep(interval)


def start_scheduler_thread() -> None:
    t = threading.Thread(target=run_periodic_sheet_sync, daemon=True)
    t.start()
