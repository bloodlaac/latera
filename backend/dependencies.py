from fastapi import Depends
from backend.database.db_connector import DBConnector
from typing import Annotated
from backend.database.session import SessionLocal
from sqlalchemy.orm import Session


def get_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]
StorageDep = Annotated[DBConnector, Depends(DBConnector)]
