import petl as etl
from petl.util.base import DictsView
from typing import Tuple, Iterable, Optional, Mapping
import warnings


def read_csv_table(filepath: str, header_rows: int = 0, footer_rows: int = 0, row: Optional[int] = None, delimiter: str = ",") -> DictsView:
    """
    Reads a CSV file, skipping a specified number of header and footer rows.

    Args:
        filepath (str): Path to the CSV file.
        header_rows (int): Number of rows to skip from the top. Default is 0.
        footer_rows (int): Number of rows to skip from the bottom. Default is 0.
        row (Optional[int]): Optional row index to read (0-based). If None, returns the entire table after skipping.
        delimiter (str): Character that separates values in the CSV file. Default is ','.

    Returns:
        DictsView: A petl table with header and footer rows skipped, or a single row as a dictionary if `row` is specified.
    """
    # Load the CSV file
    table = etl.fromcsv(filepath, delimiter = delimiter)
    
    # Skip header and footer
    table = etl.skip(table, header_rows)  # Skip header rows
    table = etl.head(table, len(table) - footer_rows)  # Skip footer rows

    if row is not None:
        # Extract the specific row and return as a dictionary
        row_data = etl.rowslice(table, row, row + 1)  # Get the specified row
        return etl.dicts(row_data)  # Convert to dictionary view

    return etl.dicts(table)  # Return the entire table as a dictionary view


def read_csv_header(filepath: str, header_rows: int = 0, delimiter: str = ",") -> Tuple[str]:
    """
    Reads the header of a CSV file using petl, skipping the specified number of rows.

    Args:
        filepath (str): The path to the CSV file.
        header_rows (int): The number of rows to skip before reading the header. Default is 0.
        delimiter (str): Character that separates values in the CSV file. Default is ','.

    Returns:
        Tuple[str]: A tuple of strings representing the column headers.
    """
    # Use petl to skip rows and retrieve the header
    table = etl.skip(etl.fromcsv(filepath, delimiter=delimiter), header_rows)
    header = table.header()

    return header


def match_csv_header(filepath: str, header: Iterable[str], header_rows: int = 0, delimiter: str = ",") -> bool:
    """
    Compares the header of a CSV file with a given header.

    Args:
        filepath (str): The path to the CSV file.
        header (Iterable[str]): The header to compare against.
        header_rows (int): Number of rows to skip before reading the header. Default is 0.
        delimiter (str): Character that separates values in the CSV file. Default is ','.

    Returns:
        bool: True if the headers match, False otherwise.
    """
    target_header = read_csv_header(filepath, header_rows, delimiter=delimiter)
    return target_header == tuple(header)


def match_csv_entry(filepath: str, entry_dict: Mapping[str, str], header_rows: int = 0, footer_rows: int = 0) -> bool:
    """
    Checks if a given entry exists in the first row of a CSV file.

    Args:
        filepath (str): The path to the CSV file.
        entry_dict (Mapping[str, str]): A dictionary representing the entry to match.
        header_rows (int): Number of rows to skip from the top. Default is 0.
        footer_rows (int): Number of rows to skip from the bottom. Default is 0.

    Returns:
        bool: True if the entry exists, False otherwise.
    """
    target_dict = read_csv_table(filepath, header_rows, footer_rows, row=0)

    # Return false when there are no entries in the file.
    if len(target_dict) == 0:
        return False
    return all(item in target_dict[0].items() for item in entry_dict.items())


def read_xlsx_table(filepath: str, sheet_name: int = 0, header_rows: int = 0, footer_rows: int = 0, row: Optional[int] = None) -> DictsView:
    """
    Reads an Excel (.xlsx) file, skipping a specified number of header and footer rows.

    Args:
        filepath (str): Path to the Excel file.
        sheet_name (int): Name or index of the sheet to read. Default is the first sheet (0).
        header_rows (int): Number of rows to skip from the top. Default is 0.
        footer_rows (int): Number of rows to skip from the bottom. Default is 0.
        row (Optional[int]): Optional row index to read (0-based). If None, returns the entire table after skipping.

    Returns:
        DictsView: A petl table with header and footer rows skipped, or a single row as a dictionary if `row` is specified.
    """
    # Load the Excel file
    table = etl.fromxlsx(filepath, sheet=sheet_name)
    
    # Skip header and footer
    table = etl.skip(table, header_rows)  # Skip header rows
    table = etl.head(table, len(table) - footer_rows)  # Skip footer rows

    if row is not None:
        # Extract the specific row and return as a dictionary
        row_data = etl.rowslice(table, row, row + 1)  # Get the specified row
        return etl.dicts(row_data)  # Convert to dictionary view
    
    # Convert to list of dictionaries
    return etl.dicts(table)


def read_xlsx_header(filepath: str, sheet_name: int = 0, header_rows: int = 0) -> Tuple[str]:
    """
    Reads the header of an Excel (.xlsx) file using petl, skipping the specified number of rows.

    Args:
        filepath (str): The path to the Excel file.
        sheet_name (int): Name or index of the sheet to read. Default is the first sheet (0).
        header_rows (int): The number of rows to skip before reading the header. Default is 0.

    Returns:
        Tuple[str]: A tuple of strings representing the column headers.
    """
    # Use petl to skip rows and retrieve the header
    table = etl.skip(etl.fromxlsx(filepath, sheet=sheet_name), header_rows)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)  # Catch warning about default stylesheet not being defined
        header = table.header()

    return header


def match_xlsx_header(filepath: str, header: Iterable[str], sheet_name = 0, header_rows: int = 0) -> bool:
    """
    Compares the header of an Excel file with a given header.

    Args:
        filepath (str): The path to the Excel file.
        header (Iterable[str]): The header to compare against.
        sheet_name (int): Name or index of the sheet to read. Default is the first sheet (0).
        header_rows (int): Number of rows to skip before reading the header. Default is 0.

    Returns:
        bool: True if the headers match, False otherwise.
    """
    target_header = read_xlsx_header(filepath, sheet_name, header_rows)
    return target_header == tuple(header)


def match_xlsx_entry(filepath: str, entry_dict: Mapping[str, str], sheet_name: int = 0, header_rows: int = 0, footer_rows: int = 0) -> bool:
    """
    Checks if a given entry exists in the first row of an Excel file.

    Args:
        filepath (str): The path to the Excel file.
        entry_dict (Mapping[str, str]): A dictionary representing the entry to match.
        sheet_name (int): Name or index of the sheet to read. Default is the first sheet (0).
        header_rows (int): Number of rows to skip from the top. Default is 0.
        footer_rows (int): Number of rows to skip from the bottom. Default is 0.

    Returns:
        bool: True if the entry exists, False otherwise.
    """
    target_dict = read_xlsx_table(filepath, sheet_name, header_rows, footer_rows, row=0)
    
    # Return false when there are no entries in the file.
    if len(target_dict) == 0:
        return False
    return all(item in target_dict.items() for item in entry_dict.items())


if __name__ == "__main__":
    table = match_csv_entry(r"/home/jpg/Nextcloud/Documents/personal_finances/ledger/documents/Assets/Revolut/CHF/2024-08-01.checking.account-statement_2024-08-01_2024-09-02_en_770fbf.csv", {'Currency': 'CHF'})
    table = match_xlsx_entry(r"/home/jpg/Nextcloud/Documents/personal_finances/ledger/downloads/Argenta_BE31979787460755_2024-09-02_213235.xlsx", {'Munt': 'EUR'})
    print(table)
