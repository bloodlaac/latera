from fastapi import FastAPI, status, Depends
from backend.api.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from backend.database.db_connector import DBConnector
from typing import Annotated


app = FastAPI(title="Latera")
StorageDep = Annotated[DBConnector, Depends(DBConnector)]


@app.get("/")
def read_root():
    return { "API health": "gud" }


@app.get("/items", status_code=status.HTTP_200_OK, response_model=list[ItemResponse])
def get_items(storage: StorageDep):
    return storage.select_items()


@app.get("/items/{item_id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
def get_item(item_id: int, storage: StorageDep):
    return storage.select_item(item_id)


@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=ItemResponse)
def create_item(item: ItemCreate, storage: StorageDep):
    return storage.add_item(item)


@app.patch("/items/{item_id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
def update_item(item_id: int, new_item: ItemUpdate, storage: StorageDep):
    return storage.update_item(item_id, new_item)


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, storage: StorageDep):
    return storage.delete_item(item_id)
