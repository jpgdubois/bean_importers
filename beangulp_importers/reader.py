import petl as etl

def read_csv(file_path: str, header_rows: int=0, footer_rows: int=0) -> list:
    """
    Read a CSV file, skipping a specified number of header and footer rows.

    :param file_path: Path to the CSV file.
    :param header_rows: Number of rows to skip from the top (default is 1).
    :param footer_rows: Number of rows to skip from the bottom (default is 1).
    :return: petl table with header and footer rows skipped.
    """
    # Load the CSV file
    table = etl.fromcsv(file_path)
    
    # Skip header and footer
    table = etl.skip(table, header_rows)  # Skip header rows
    table = etl.head(table, len(table) - footer_rows)  # Skip footer rows
    
    return etl.dicts(table)


def read_xlsx(file_path, sheet_name=0, header_rows=0, footer_rows=0):
    """
    Read an Excel (.xlsx) file, skipping a specified number of header and footer rows,
    and return the data as a list of dictionaries.

    :param file_path: Path to the Excel file.
    :param sheet_name: Name or index of the sheet to read (default is the first sheet).
    :param header_rows: Number of rows to skip from the top (default is 1).
    :param footer_rows: Number of rows to skip from the bottom (default is 1).
    :return: List of dictionaries representing each row.
    """
    # Load the Excel file
    table = etl.fromxlsx(file_path, sheet=sheet_name)
    
    # Skip header and footer
    table = etl.skip(table, header_rows)  # Skip header rows
    table = etl.head(table, len(table) - footer_rows)  # Skip footer rows
    
    # Convert to list of dictionaries
    return etl.dicts(table)

if __name__ == "__main__":
    # table = read_csv(r"/home/jpg/Nextcloud/Documents/personal_finances/ledger/documents/Assets/Revolut/CHF/2024-08-01.checking.account-statement_2024-08-01_2024-09-02_en_770fbf.csv")
    table = read_xlsx(r"/home/jpg/Nextcloud/Documents/personal_finances/ledger/downloads/Argenta_BE31979787460755_2024-09-02_213235.xlsx")
    print(table)
