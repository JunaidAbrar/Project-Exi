from pydantic import BaseModel


class LeadBase(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    budget_min: int | None = None
    budget_max: int | None = None
    preferred_suburb: str | None = None
    source: str = "chat"
    status: str = "new"


class LeadCreate(LeadBase):
    pass


class LeadRead(LeadBase):
    id: int

    class Config:
        from_attributes = True
