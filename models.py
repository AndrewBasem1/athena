from sqlmodel import SQLModel
from sqlmodel import Field
from datetime import datetime
from typing import Union
from db_engine import db_engine
from typing import Optional

strOrNone = Union[str, None]
intOrNone = Union[int, None]
floatOrNone = Union[float, None]
datetimeOrNone = Union[datetime, None]

nonIndexedNullableField = Field(nullable=True, index=False)
indexedNullableField = Field(nullable=True, index=True)


class CraigslistVehicleRecordRead(SQLModel):
    """
    SQLModel class for reading in a Craigslist vehicle record (i.e. line) from the CSV file.
    """

    url: strOrNone = nonIndexedNullableField
    region: strOrNone = indexedNullableField
    region_url: strOrNone = nonIndexedNullableField
    price: intOrNone = nonIndexedNullableField
    year: intOrNone = nonIndexedNullableField
    manufacturer: strOrNone = nonIndexedNullableField
    model: strOrNone = nonIndexedNullableField
    condition: strOrNone = nonIndexedNullableField
    cylinders: intOrNone = nonIndexedNullableField
    odometer: intOrNone = nonIndexedNullableField
    title_status: strOrNone = nonIndexedNullableField
    transmission: strOrNone = nonIndexedNullableField
    VIN: strOrNone = nonIndexedNullableField
    drive: strOrNone = nonIndexedNullableField
    size: strOrNone = nonIndexedNullableField
    type: strOrNone = nonIndexedNullableField
    paint_color: strOrNone = nonIndexedNullableField
    image_url: strOrNone = nonIndexedNullableField
    county: strOrNone = nonIndexedNullableField
    state: strOrNone = indexedNullableField
    lat: floatOrNone = nonIndexedNullableField
    long: floatOrNone = nonIndexedNullableField
    posting_date: datetimeOrNone = indexedNullableField
    removal_date: datetimeOrNone = indexedNullableField


class CraigslistVehicleRecord(CraigslistVehicleRecordRead, table=True):
    """
    A SQLModel class for creating a Craigslist vehicle record (i.e. line) in the database.
    id is added here as autoincrementing primary key so we can use int instead of bigint in MySQL
    (because the values in the dataset are all above the threshold for int)
    """

    id: Optional[int] = Field(default=None, primary_key=True)


def recreate_db_tables_from_scratch():
    """Drops all tables if they exist and recreates them from scratch according to our predefined sqlmodel Models."""
    SQLModel.metadata.drop_all(bind=db_engine)
    SQLModel.metadata.create_all(bind=db_engine)


if __name__ == "__main__":
    recreate_db_tables_from_scratch()
