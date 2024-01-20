from sqlmodel import SQLModel
from sqlmodel import Field
from datetime import datetime
from db_engine import db_engine


class CraigslistVehicleRecord(SQLModel, table=True):
    id: int = Field(primary_key=True)
    url: str = Field(nullable=True)
    region: str = Field(nullable=True)
    region_url: str = Field(nullable=True)
    price: int = Field(nullable=True)
    year: int = Field(nullable=True)
    manufacturer: str = Field(nullable=True)
    model: str = Field(nullable=True)
    condition: str = Field(nullable=True)
    cylinders: str = Field(nullable=True)
    odometer: int = Field(nullable=True)
    title_status: str = Field(nullable=True)
    transmission: str = Field(nullable=True)
    VIN: str = Field(nullable=True)
    drive: str = Field(nullable=True)
    size: str = Field(nullable=True)
    type: str = Field(nullable=True)
    paint_color: str = Field(nullable=True)
    image_url: str = Field(nullable=True)
    county: str = Field(nullable=True)
    state: str = Field(nullable=True)
    lat: float = Field(nullable=True)
    long: float = Field(nullable=True)
    posting_date: datetime = Field(nullable=False, index=True)
    removal_date: datetime = Field(nullable=False, index=True)


if __name__ == "__main__":
    SQLModel.metadata.create_all(bind=db_engine)
