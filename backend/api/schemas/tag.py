from pydantic import BaseModel, AfterValidator, ConfigDict
from typing import Annotated


def validate_name(name: str):
    name = name.strip().lower()

    if not name:
        raise ValueError("tag name must not be empty")
    
    return name


class TagCreate(BaseModel):
    name: Annotated[str, AfterValidator(validate_name)]


class TagResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
