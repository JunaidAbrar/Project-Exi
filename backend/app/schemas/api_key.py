from pydantic import BaseModel


class ApiKeyBase(BaseModel):
    description: str | None = None


class ApiKeyCreate(ApiKeyBase):
    pass  # key will be generated server-side


class ApiKeyRead(ApiKeyBase):
    id: int
    key: str
    is_active: bool

    class Config:
        from_attributes = True
