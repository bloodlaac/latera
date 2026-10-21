from backend.api.schemas.item import ItemCreate, ItemUpdate
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.database.models.item import Item


class DBConnector:

    def get_items(self, session: Session) -> list[Item]:
        stmt = select(Item).order_by(Item.item_id)
        result = session.scalars(statement=stmt).all()

        return list(result)


    def get_item(self, item_id: int, session: Session) -> Item | None:
        return session.get(Item, item_id)

    def post_item(self, item: ItemCreate, session: Session) -> Item:
        new_item = Item(**item.model_dump())

        session.add(new_item)
        session.commit()

        session.refresh(new_item)

        return new_item

    def patch_item(self, item_id: int, new_item: ItemUpdate, session: Session) -> Item | None:
        db_item = session.get(Item, item_id)

        if db_item is None:
            return None
        
        update_data = new_item.model_dump(exclude_unset=True)
        
        if not update_data:
            return db_item

        if "content" in update_data and new_item.content is not None:
            db_item.content = new_item.content

        if "title" in update_data:
            db_item.title = new_item.title

        session.commit()
        session.refresh(db_item)

        return db_item

    def delete_item(self, item_id: int, session: Session) -> bool:
        item = session.get(Item, item_id)

        if item is None:
            return False

        session.delete(item)
        session.commit()

        return True
