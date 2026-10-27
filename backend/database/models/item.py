from backend.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, DateTime, Text
from datetime import datetime, timezone
from backend.database.models.item_tags import item_tags
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from backend.database.models.tag import Tag


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    tags: Mapped[list["Tag"]] = relationship(secondary=item_tags, back_populates="items")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    modified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None
    )
