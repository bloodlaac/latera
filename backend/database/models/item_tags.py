from sqlalchemy import Table, Column, ForeignKey
from backend.database.base import Base


item_tags = Table(
    "item_tags",
    Base.metadata,
    Column("item_id", ForeignKey("items.id", ondelete="cascade"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="cascade"), primary_key=True)
)
