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


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
def get_item(id: int, storage: StorageDep, session: SessionDep):    
    item = storage.get_item(id, session)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no item with such id"
        )
    return item


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ItemResponse)
def create_item(item: ItemCreate, storage: StorageDep, session: SessionDep):
    try:
        new_item = storage.post_item(item, session)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"no tag with id {e}, choose another"
        )

    return new_item


@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
def update_item(id: int, new_item: ItemUpdate, storage: StorageDep, session: SessionDep):
    try:
        item = storage.patch_item(id, new_item, session)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"no tag with id {e}, choose another"
        )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no item with such id"
        )

    return item


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int, storage: StorageDep, session: SessionDep):
    if not storage.delete_item(id, session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no item with such id"
        )

    return

@router.post("/{id}/restore", status_code=status.HTTP_204_NO_CONTENT)
def restore_item(id: int, storage: StorageDep, session: SessionDep):
    item = storage.restore_item(id, session)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no item with such id"
        )

    return
