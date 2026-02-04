from datetime import datetime
from pydantic import BaseModel


class ItemRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_at: datetime | None = None

    # class Config:
    #     from_attributes = True
