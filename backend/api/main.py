from fastapi import FastAPI
from backend.api.routes import items


app = FastAPI(title="Latera")
app.include_router(items.router)


@app.get("/")
def root():
    return { "message": "hehe" }
