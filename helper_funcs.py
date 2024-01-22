import zipfile
import csv
import io
from pathlib import Path
from typing import Generator
from sqlalchemy import Engine
from models import CraigslistVehicleRecordRead
from models import CraigslistVehicleRecord
from os import environ
from sqlmodel import Session
from db_engine import db_engine
from pydantic import ValidationError as PydanticValidationError


def _csv_lines_generator_from_zip_file(
    zip_file_path: Path, csv_file_name: str
) -> Generator[str, None, None]:
    """
    helper function for reading csv lines from a zip file without extracting it to save memory (disk and RAM)

    ## Parameters
    - zip_file_path: `pathlib.Path` object of the zip file
    - csv_file_name: `str` name of the csv file inside the zip file

    ## Returns
    - `Generator[str, None, None]` a generator of csv lines

    ## Usage
    calling `next()` on the generator object returned will return the next csv line as a `str`
    """
    with zipfile.ZipFile(zip_file_path) as zip_file:
        with zip_file.open(csv_file_name) as csv_file:
            decoded_csv_file = io.TextIOWrapper(csv_file, encoding="utf-8")
            csv_reader = csv.reader(decoded_csv_file)
            for line in csv_reader:
                yield line


def _insert_batch_of_craigslist_vehicle_records(
    batch_of_craigslist_vehicle_records: list[CraigslistVehicleRecord],
    db_engine: Engine = db_engine,
) -> None:
    """
    inserts a batch of Craigslist vehicle records into the database.
    """
    with Session(db_engine) as session:
        session.add_all(batch_of_craigslist_vehicle_records)
        session.commit()


def migrate_craigslist_records_csv_from_zip_to_db(
    zip_file_path: Path = environ.get("ZIP_FILE_NAME"),
    csv_file_name: str = environ.get("CSV_FILE_NAME"),
    batch_size: int = 10_000,
) -> None:
    """
    parses and inserts the Craigslist vehicle records from a zip file into the database.
    """
    csv_lines_generator = _csv_lines_generator_from_zip_file(
        zip_file_path=zip_file_path, csv_file_name=csv_file_name
    )
    # getting the first line for the col headers
    col_headers = next(csv_lines_generator)
    rows_count_in_current_batch = 0
    total_rows_parsed = 0
    total_rows_inserted = 0
    current_batch = []
    while True:
        try:
            print(f"total_rows_parsed: {total_rows_parsed}", end="\r")
            while rows_count_in_current_batch < batch_size:
                current_row_values = next(csv_lines_generator)
                current_record_dict = {
                    col_header: current_row_value
                    for col_header, current_row_value in zip(
                        col_headers, current_row_values
                    )
                }
                try:
                    craiglist_vehicle_record_without_id = (
                        CraigslistVehicleRecordRead.model_validate(current_record_dict)
                    )
                    craiglist_vehicle_record = CraigslistVehicleRecord.model_validate(
                        craiglist_vehicle_record_without_id
                    )
                    current_batch.append(craiglist_vehicle_record)
                    rows_count_in_current_batch += 1
                    total_rows_parsed += 1
                except PydanticValidationError as e:
                    print(e)
                    print(current_record_dict)
                    print("-" * 30)
                    continue
            else:
                print(f"starting batch insertion of {batch_size} records")
                _insert_batch_of_craigslist_vehicle_records(current_batch)
                print(f"finished batch insertion of {batch_size} records")
                total_rows_inserted += rows_count_in_current_batch
                rows_count_in_current_batch = 0
                current_batch = []
        except StopIteration:
            break
    print(f"total_rows_parsed: {total_rows_parsed}")
    print(f"total_rows_inserted: {total_rows_inserted}")
    return None


if __name__ == "__main__":
    migrate_craigslist_records_csv_from_zip_to_db()
