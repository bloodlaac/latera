from backend.database.base import Base
from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.database.models.item_tags import item_tags
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from backend.database.models.item import Item


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text, unique=True)
    items: Mapped[list["Item"]] = relationship(secondary=item_tags, back_populates="tags")
