from pydantic import BaseModel


class ClientBase(BaseModel):
    name: str
    slug: str
    sheet_url: str | None = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    sheet_url: str | None = None
    is_active: bool | None = None
    
class ClientRead(ClientBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
