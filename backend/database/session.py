from backend.database.engine import engine
from sqlalchemy.orm import sessionmaker


SessionLocal = sessionmaker(engine)
