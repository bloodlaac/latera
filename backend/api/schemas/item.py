from typing import Annotated
from pydantic import BaseModel, AfterValidator
from datetime import datetime


def is_valid_string(text: str | None) -> str:
    if not text or text.isspace():
        raise ValueError("content must not be empty")
    return text


class ItemCreate(BaseModel):
    title: str | None = None
    content: Annotated[str, AfterValidator(is_valid_string)]


class ItemUpdate(BaseModel):
    title: str | None = None
    content: Annotated[str | None, AfterValidator(is_valid_string)] = None


class ItemResponse(ItemCreate):
    item_id: int
    created_at: datetime
    modified_at: datetime | None = None
