from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)

    # renter contact
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)

    # basic qualification, will extend later
    budget_min = Column(Integer, nullable=True)
    budget_max = Column(Integer, nullable=True)
    preferred_suburb = Column(String(100), nullable=True)

    source = Column(String(50), nullable=False, default="chat")  # 'chat' | 'whatsapp' | 'widget'
    status = Column(String(50), nullable=False, default="new")   # 'new' | 'contacted' | ...

    client = relationship("Client", back_populates="leads")
