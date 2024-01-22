from sqlmodel import create_engine

database_connection_url = "sqlite:///./craigslist_vehicles.db"
db_engine = create_engine(database_connection_url, echo=False)
