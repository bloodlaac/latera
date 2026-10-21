from backend.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, DateTime, Text
from datetime import datetime, timezone


class Item(Base):
    __tablename__ = "items"

    item_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str | None] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    modified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=lambda: datetime.now(timezone.utc)
    )
