from backend.api.schemas.item import ItemCreate, ItemUpdate
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from backend.database.models.item import Item
from backend.database.models.tag import Tag
from backend.api.schemas.tag import TagCreate
from datetime import datetime, timezone


class DBConnector:

    def get_items(self, session: Session, tags: list[int] | None) -> list[Item]:
        if tags is None:
            stmt = select(Item).where(Item.deleted_at.is_(None)).order_by(Item.id)
        else:
            stmt = (
                select(Item)
                .join(Item.tags)
                .where(Tag.id.in_(tags))
                .where(Item.deleted_at.is_(None))
                .distinct()
                .order_by(Item.id)
            )
                
        result = session.scalars(statement=stmt).all()

        return list(result)

    def get_item(self, id: int, session: Session) -> Item | None:
        item = session.get(Item, id)

        if item is None or item.deleted_at is not None:
            return None
        return item

    def post_item(self, item: ItemCreate, session: Session) -> Item:
        item_data = item.model_dump(exclude={"tags"})
        new_item = Item(**item_data)

        db_tags = []
                    
        for tag_id in item.tags:
            db_tag = session.get(Tag, tag_id)

            if db_tag is None:
                raise ValueError(tag_id)
            db_tags.append(db_tag)

        new_item.tags = db_tags

        session.add(new_item)
        session.commit()

        session.refresh(new_item)

        return new_item

    def patch_item(self, id: int, new_item: ItemUpdate, session: Session) -> Item | None:
        modified = False
        
        db_item = session.get(Item, id)

        if db_item is None or db_item.deleted_at is not None:
            return None
        
        update_data = new_item.model_dump(exclude_unset=True)
        
        if not update_data:
            return db_item

        if "tags" in update_data:
            db_tags_ids = []
            
            for tag in db_item.tags:
                db_tags_ids.append(tag.id)

            if set(db_tags_ids) != set(update_data["tags"]):
                new_tags = update_data["tags"]
                db_tags = []

                for tag_id in new_tags:
                    db_tag = session.get(Tag, tag_id)

                    if db_tag is None:
                        raise ValueError(tag_id)
                    db_tags.append(db_tag)

                db_item.tags = db_tags
                modified = True

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

    def delete_item(self, id: int, session: Session) -> bool:
        item = session.get(Item, id)

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

    def restore_item(self, id: int, session: Session) -> Item | None:
        item = session.get(Item, id)

        if item is None:
            return None

        if item.deleted_at is not None:
            item.deleted_at = None
            session.commit()

        return item


    def get_tags(self, session: Session) -> list[Tag]:
        stmt = select(Tag).order_by(Tag.id)

        tags = session.scalars(statement=stmt).all()

        return list(tags)


    def get_tag(self, session: Session, id: int) -> Tag | None:
        tag = session.get(Tag, id)

        return tag


    def post_tag(self, session: Session, tag: TagCreate) -> Tag:
        new_tag = Tag(**tag.model_dump())

        try:
            session.add(new_tag)
            session.commit()
        except IntegrityError:
            session.rollback()
            raise ValueError(tag.name)
        
        session.refresh(new_tag)

        return new_tag


    def delete_tag(self, session: Session, id: int) -> bool:
        tag = session.get(Tag, id)

        if tag is None:
            return False

        session.delete(tag)
        session.commit()

        return True
