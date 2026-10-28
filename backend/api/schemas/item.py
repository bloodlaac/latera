from typing import Annotated
from pydantic import BaseModel, AfterValidator, BeforeValidator, ConfigDict
from datetime import datetime
from backend.database.models.tag import Tag


def is_valid_string(text: str | None) -> str:
    if not text or text.isspace():
        raise ValueError("content must not be empty")
    return text.strip()


def check_tags(tags: list[int]) -> list[int]:
    return list(set(tags))


def obj_to_id(tags: list[Tag]) -> list[int]:
    ids = []
    
    for tag in tags:
        ids.append(tag.id)

    return ids


class ItemCreate(BaseModel):
    title: str | None = None
    content: Annotated[str, AfterValidator(is_valid_string)]
    tags: Annotated[list[int], AfterValidator(check_tags)] = []


class ItemUpdate(BaseModel):
    title: str | None = None
    content: Annotated[str | None, AfterValidator(is_valid_string)] = None
    tags: Annotated[list[int], AfterValidator(check_tags)] = []


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str | None = None
    content: str
    tags: Annotated[list[int], BeforeValidator(obj_to_id)]
    created_at: datetime
    modified_at: datetime | None = None
    deleted_at: datetime | None = None
