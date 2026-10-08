from backend.api.schemas.item import ItemResponse, ItemCreate, ItemUpdate
from fastapi import status, HTTPException, Response
from itertools import count
from datetime import datetime, timezone


class DBConnector:

    id_generator = count(start=0)
    storage = {}

    def select_items(self) -> list[ItemResponse]:
        return [ItemResponse(item_id=k, **v) for k, v in self.storage.items()]

    def select_item(self, item_id: int) -> ItemResponse:
        if item_id not in self.storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no item with such id"
            )

        return ItemResponse(item_id=item_id, **self.storage[item_id])

    def add_item(self, item: ItemCreate) -> ItemResponse:
        new_id = next(self.id_generator)

        self.storage[new_id] = {
            "title": item.title,
            "content": item.content,
            "created_at": datetime.now(timezone.utc),
            "modified_at": None
        }

        new_item = ItemResponse(item_id=new_id, **self.storage[new_id])

        return new_item

    def update_item(self, item_id: int, new_item: ItemUpdate) -> ItemResponse:
        if item_id not in self.storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no item with such id"
            )

        update_data = new_item.model_dump(exclude_unset=True)
        old_item = self.storage[item_id]
        modified = False

        if not update_data:
            return ItemResponse(item_id=item_id, **old_item)

        if "content" in update_data and old_item["content"] != new_item.content:
            old_item["content"] = new_item.content
            modified = True

        if "title" in update_data and old_item["title"] != new_item.title:
            old_item["title"] = new_item.title
            modified = True

        if modified:    
            old_item["modified_at"] = datetime.now(timezone.utc)
        
        return ItemResponse(item_id=item_id, **old_item)

    def delete_item(self, item_id: int) -> Response:
        if item_id not in self.storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no item with such id"
            )

        self.storage.pop(item_id)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
