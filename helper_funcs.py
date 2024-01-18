import zipfile
import csv
import io
from pathlib import Path
from typing import Generator


def csv_lines_generator_from_zip_file(
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
