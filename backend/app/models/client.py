from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    # e.g. 'acme-real-estate-sa'
    slug = Column(String(255), nullable=False, unique=True)

    # TODO: store WhatsApp number, branding later (phase 5+)
    is_active = Column(Boolean, default=True, nullable=False)

    api_keys = relationship("ApiKey", back_populates="client")
    rentals = relationship("Rental", back_populates="client")
    leads = relationship("Lead", back_populates="client")
