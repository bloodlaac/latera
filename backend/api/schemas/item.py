from pydantic import BaseModel
from datetime import datetime


class ItemCreate(BaseModel):
    title: str | None = None
    content: str

class ItemResponse(ItemCreate):
    item_id: int
    created_at: datetime
    modified_at: datetime | None = None
