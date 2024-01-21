from sqlmodel import create_engine
from os import environ
from dotenv import load_dotenv

load_dotenv()
DATABASE_HOST = environ["DATABASE_HOST"]
DATABASE_PORT = environ["DATABASE_PORT"]
DATABASE_USERNAME = environ["DATABASE_USERNAME"]
DATABASE_PASSWORD = environ["DATABASE_PASSWORD"]
DATABASE_SCHEMA = environ["DATABASE_SCHEMA"]

database_connection_url = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_SCHEMA}"

db_engine = create_engine(database_connection_url, echo=True)
