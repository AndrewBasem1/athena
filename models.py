from sqlmodel import SQLModel
from sqlmodel import Field
from pydantic import field_validator
from datetime import datetime
from typing import Union
from re import match
from sqlalchemy import BigInteger
from sqlalchemy import Column
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
    region: strOrNone = nonIndexedNullableField
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
    county: strOrNone = indexedNullableField
    state: strOrNone = indexedNullableField
    lat: floatOrNone = nonIndexedNullableField
    long: floatOrNone = nonIndexedNullableField
    posting_date: datetimeOrNone = indexedNullableField
    removal_date: datetimeOrNone = indexedNullableField

    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, cell_value) -> None:
        """
        a field validator that converts empty strings to None
        so we minimize the number of empty strings in the database
        """
        if isinstance(cell_value, str):
            if cell_value.strip() == "":
                return None
        return cell_value

    @field_validator("cylinders", mode="before")
    @classmethod
    def get_number_of_cylinders(cls, cylinders_cell_value) -> Union[int, None]:
        """
        A field validator that extracts the number of cylinders from the cylinders cell value to be converted to an int.
        """
        if isinstance(cylinders_cell_value, int):
            return cylinders_cell_value
        else:
            pattern = r"\d"
            try:
                regex_match = match(pattern, cylinders_cell_value)
                regex_match_str = regex_match[0]
                regex_match_int = int(regex_match_str)
                return regex_match_int
            except:
                return None


class CraigslistVehicleRecord(CraigslistVehicleRecordRead, table=True):
    """
    A SQLModel class for creating a Craigslist vehicle record (i.e. line) in the database.
    id is added here as autoincrementing primary key so we can use int instead of bigint in MySQL
    (because the values in the dataset are all above the threshold for int)
    """

    id: Optional[int] = Field(default=None, primary_key=True)


def recreate_db_tables_from_scratch():
    SQLModel.metadata.drop_all(bind=db_engine)
    SQLModel.metadata.create_all(bind=db_engine)


if __name__ == "__main__":
    recreate_db_tables_from_scratch()
