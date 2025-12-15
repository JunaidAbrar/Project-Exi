from pydantic import BaseModel
from decimal import Decimal


class RentalBase(BaseModel):
    external_id: str
    address: str
    suburb: str
    state: str = "SA"
    postcode: str
    weekly_rent: Decimal
    bedrooms: int
    bathrooms: int
    car_spaces: int | None = None
    description: str | None = None
    image_urls: str | None = None
    is_active: bool = True


class RentalCreate(RentalBase):
    pass


class RentalRead(RentalBase):
    id: int

    class Config:
        from_attributes = True
