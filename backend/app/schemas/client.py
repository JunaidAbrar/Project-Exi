from pydantic import BaseModel


class ClientBase(BaseModel):
    name: str
    slug: str


class ClientCreate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
