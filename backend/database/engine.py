from sqlalchemy import create_engine, URL
from backend import config


url_object = URL.create(
    drivername="postgresql+psycopg",
    username=config.db_user,
    password=config.db_password,
    host=config.db_host,
    port=config.db_port,
    database=config.db_name,
)

engine = create_engine(url_object)
