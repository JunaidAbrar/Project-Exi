from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)

    # core fields for PHASE 1 + Google Sheet mapping
    external_id = Column(String(100), nullable=False)   # ID from agent sheet
    address = Column(String(255), nullable=False)
    suburb = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False, default="SA")
    postcode = Column(String(10), nullable=False)

    weekly_rent = Column(Numeric(10, 2), nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    car_spaces = Column(Integer, nullable=True)
    pet_allowed = Column(Boolean, nullable=True)

    description = Column(Text, nullable=True)
    image_urls = Column(Text, nullable=True)  # comma-separated URLs

    is_active = Column(Boolean, default=True, nullable=False)

    client = relationship("Client", back_populates="rentals")

    __table_args__ = ()
