from backend.api.schemas.item import ItemCreate, ItemUpdate
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.database.models.item import Item
from datetime import datetime, timezone


class DBConnector:

    def get_items(self, session: Session) -> list[Item]:
        stmt = select(Item).where(Item.deleted_at.is_(None)).order_by(Item.item_id)
        result = session.scalars(statement=stmt).all()

        return list(result)

    def get_item(self, item_id: int, session: Session) -> Item | None:
        item = session.get(Item, item_id)

        if item is None or item.deleted_at is not None:
            return None
        return item

    def post_item(self, item: ItemCreate, session: Session) -> Item:
        new_item = Item(**item.model_dump())

        session.add(new_item)
        session.commit()

        session.refresh(new_item)

        return new_item

    def patch_item(self, item_id: int, new_item: ItemUpdate, session: Session) -> Item | None:
        modified = False
        
        db_item = session.get(Item, item_id)

        if db_item is None or db_item.deleted_at is not None:
            return None
        
        update_data = new_item.model_dump(exclude_unset=True)
        
        if not update_data:
            return db_item

        if (
            "content" in update_data
            and new_item.content is not None
            and new_item.content != db_item.content
        ):
            db_item.content = new_item.content
            modified = True

        if "title" in update_data and new_item.title != db_item.title:
            db_item.title = new_item.title
            modified = True

        if modified:
            db_item.modified_at = datetime.now(timezone.utc)
            session.commit()
            session.refresh(db_item)

        return db_item

    def delete_item(self, item_id: int, session: Session) -> bool:
        item = session.get(Item, item_id)

        if item is None:
            return False

        if item.deleted_at is None:
            item.deleted_at = datetime.now(timezone.utc)
        # session.delete(item)
            session.commit()

        return True

    def get_trash(self, session: Session) -> list[Item]:
        stmt = select(Item).where(Item.deleted_at.is_not(None)).order_by(Item.deleted_at.desc())

        items = session.scalars(statement=stmt).all()

        return list(items)

    def restore_item(self, item_id: int, session: Session) -> Item | None:
        item = session.get(Item, item_id)

        if item is None:
            return None

        if item.deleted_at is not None:
            item.deleted_at = None
            session.commit()

        return item
