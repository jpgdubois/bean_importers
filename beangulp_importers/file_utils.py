from typing import Union, Tuple, Optional
import re
from os import path
from datetime import datetime


def match_file_extension(filepath: str, extension: Union[str, Tuple[str]]) -> bool:
    """
    Check if the given file path ends with the specified file extension(s).
    
    Parameters:
        filepath (str): The file path to check.
        extension (Union[str, Tuple[str]]): The file extension(s) to match.
                                             This can be a single extension as a string 
                                             (e.g., '.txt') or multiple extensions as a tuple 
                                             (e.g., ('.txt', '.csv')).
    
    Returns:
        bool: True if the file path ends with the specified extension(s), 
              False otherwise.
    """
    
    # Normalize the extension input to a tuple if it's a single string
    if isinstance(extension, str):
        extension = (extension,)
    
    # Check if the filepath ends with any of the specified extensions
    return filepath.endswith(extension)


def match_filename_pattern(filepath: str, regex: str) -> bool:
    """
    Check if the filename in the given file path matches the specified regex pattern.
    
    Parameters:
        filepath (str): The file path to check.
        regex (str): The regular expression pattern to match the filename against.
    
    Returns:
        bool: True if the filename matches the regex pattern, False otherwise.
    """
    # Extract the filename from the file path
    filename = path.basename(filepath)

    # Use the regular expression to check for a match
    return bool(re.match(regex, filename))


def match_file_date(
    filepath: str,
    regex: str,
    date_format: str = "%Y-%m-%d",
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None
) -> bool:
    """
    Check if the date extracted from the filename is within the specified date range.

    Parameters:
        filepath (str): The file path to check.
        regex (str): The regular expression pattern for the filename with the date to extract as a group.
        date_format (str): The format of the date compatible with datetime.strptime().
        start_date (Optional[datetime.date]): The start date of the range (inclusive).
        end_date (Optional[datetime.date]): The end date of the range (inclusive).

    Returns:
        bool: True if the extracted file date is within the specified range, False otherwise.
    
    Raises:
        ValueError: If no date is found in the filename or if the date cannot be parsed.
    """
    # Extract the date from the filename
    file_date = extract_date_from_filename(filepath, regex, date_format)

    # Check if the file_date is between start_date and end_date
    if start_date and file_date < start_date:
        return False
    if end_date and file_date > end_date:
        return False

    return True


def extract_date_from_filename(filepath: str, regex: str, date_format: str = "%Y-%m-%d") -> datetime.date:
    """
    Extract the latest date from the filename in the given file path.

    Parameters:
        filepath (str): The file path to check.
        regex (str): The regular expression pattern for the filename with the date to extract as a group.
        date_format (str): The format of the date compatible with datetime.strptime().

    Returns:
        datetime.date: The date found in the filename.

    Raises:
        ValueError: If no match is found or if the date cannot be parsed.
    """
    # Extract the filename from the file path
    filename = path.basename(filepath)
    
    # Match the filename against the regex
    match = re.match(regex, filename)

    # Raise an error if there is no match
    if not match:
        raise ValueError(f"No match found for the regex '{regex}' in filename '{filename}'.")

    # Extract the date string from the match group
    date_str = match.group(1)
    
    # Attempt to parse the date string
    try:
        return datetime.strptime(date_str, date_format).date()
    except ValueError:
        raise ValueError(f"Could not parse date '{date_str}' with format '{date_format}'.")
