from fastapi import FastAPI, status, HTTPException
from schemas.item import ItemCreate, ItemResponse
from datetime import datetime
from itertools import count

id_generator = count(start=0)

items = [
    {
        "id": 0,
        "content": "some pretty text"
    },
    {
        "id": 1,
        "title": "i'm a title",
        "content": "i'll be a jpg file someday!"
    }
]

app = FastAPI()

@app.get("/items", status_code=status.HTTP_200_OK, response_model=[ItemResponse])
def get_items():
    return items

@app.get("/items/{item_id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
def get_item(item_id: int):
    for json_item in items:
        if json_item["id"] == item_id:
            return ItemResponse(**items[item_id])
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="no item with such id"
    )

@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=ItemResponse)
def create_item(item: ItemCreate):
    if not item.content or len(item.content) == 0 or item.content.isspace():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="content field must not be empty"
        )

    new_id = next(id_generator)
    
    new_item = ItemResponse(
        item_id=new_id, 
        title=item.title,
        content=item.content,
        created_at=datetime.now()
    )
    item_json = new_item.model_dump()
    items.append(item_json)

    return new_item

@app.patch("/items/{item_id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
def update_item(item_id: int, new_item: ItemCreate):
    if new_item.content is None or len(new_item.content) == 0 or new_item.content.isspace():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="content field must not be empty"
        )
    
    for json_item in items:
        if json_item["id"] == item_id:
            json_item["title"] = new_item.title
            json_item["content"] = new_item.content
            json_item["modified_at"] = datetime.now()
            
            return ItemResponse(**json_item)

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    for i, json_item in enumerate(items):
        if json_item["id"] == item_id:
            items.pop(i)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="no item with such id"
    )