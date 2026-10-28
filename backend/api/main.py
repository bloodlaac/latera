import backend.database.models
from fastapi import FastAPI
from backend.api.routes import items
from backend.api.routes import tags
from backend.api.schemas.item import ItemResponse
from backend.dependencies import SessionDep, StorageDep


app = FastAPI(title="Latera")
app.include_router(items.router)
app.include_router(tags.router)


@app.get("/")
def root():
    return { "message": "hehe" }


@app.get("/trash", response_model=list[ItemResponse])
def get_trashed_items(session: SessionDep, storage: StorageDep):
    return storage.get_trash(session)
