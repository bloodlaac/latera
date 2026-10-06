from pydantic import BaseModel
from datetime import datetime


class ItemCreate(BaseModel):
    title: str | None = None
    content: str


class ItemUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class ItemResponse(ItemCreate):
    item_id: int
    created_at: datetime
    modified_at: datetime | None = None
