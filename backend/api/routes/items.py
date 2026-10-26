from fastapi import APIRouter
from fastapi import status
from backend.api.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from fastapi import HTTPException
from backend.dependencies import SessionDep, StorageDep


router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.get("", status_code=status.HTTP_200_OK, response_model=list[ItemResponse])
def get_items(storage: StorageDep, session: SessionDep):
    return storage.get_items(session)


@router.get("/{item_id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
def get_item(item_id: int, storage: StorageDep, session: SessionDep):    
    item = storage.get_item(item_id, session)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no item with such id"
        )
    return item


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ItemResponse)
def create_item(item: ItemCreate, storage: StorageDep, session: SessionDep):
    return storage.post_item(item, session)


@router.patch("/{item_id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
def update_item(item_id: int, new_item: ItemUpdate, storage: StorageDep, session: SessionDep):
    item = storage.patch_item(item_id, new_item, session)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no item with such id"
        )

    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, storage: StorageDep, session: SessionDep):
    if not storage.delete_item(item_id, session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no item with such id"
        )

    return

@router.post("/{item_id}/restore", status_code=status.HTTP_204_NO_CONTENT)
def restore_item(item_id: int, storage: StorageDep, session: SessionDep):
    item = storage.restore_item(item_id, session)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no item with such id"
        )

    return
