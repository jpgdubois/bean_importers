import re
from decimal import Decimal, ROUND_HALF_EVEN
from os import path
from datetime import datetime
from typing import Optional, Union
from beangulp_importers.datatypes import Currency

def convert_text_to_currency(text: str) -> Currency:
    """
    Extract the currency code from the given text.

    This function removes non-letter characters, converts the text to uppercase,
    and checks if it corresponds to a known currency code in the Currency Enum.

    Args:
        text (str): The input text containing a currency code.

    Returns:
        Currency: The extracted currency as an enum member if found.

    Raises:
        ValueError: If no known currency code is found in the text.
    """
    cleaned_text = "".join(char for char in text if char.isalpha()).upper()
    
    try:
        return Currency[cleaned_text]  # Return the matching Currency enum member
    except KeyError:
        raise ValueError(f"Unknown currency: {cleaned_text}")


def convert_text_to_decimal(text: str) -> Decimal:
    """
    Convert a string representation of a number into a Decimal.

    This function strips whitespace, handles signed numbers, and replaces
    the last non-digit character found (that is not a sign) with a decimal point.

    Args:
        text (str): The string representation of the number to convert.

    Returns:
        Decimal: The converted decimal number.

    Raises:
        ValueError: If the input string cannot be converted to a Decimal.
    """
    if isinstance(text, (float, int)):
        return Decimal(text).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)
    
    text = text.strip()  # Strip whitespace from the input

    if not text:
        return Decimal(0)  # Handle empty string

    sign = ''
    if text[0] in ('+', '-'):
        sign = text[0]
        text = text[1:].strip()

    separators = re.sub(r"\d", "", text)  # Exclude signs and digits
    if separators:
        for sep in separators[:-1]:
            text = text.replace(sep, "")
        number = text.replace(separators[-1], ".")

    number = sign + number

    try:
        return Decimal(number).quantize(Decimal('.01'), rounding=ROUND_HALF_EVEN)
    except ValueError:
        raise ValueError(f"Cannot convert '{number}' to Decimal.")


def convert_text_to_sign(text: str) -> int:
    """
    Convert a given word into a numeric sign (1 or -1) based on its meaning.

    Args:
        text (str): The word to be converted, representing either a positive 
                    or negative financial concept (e.g., "credit", "debit").

    Returns:
        int: 1 for positive concepts (e.g., "credit", "deposit"), 
             -1 for negative concepts (e.g., "debit", "withdrawal").

    Raises:
        ValueError: If the input word is not recognized as either positive or negative.
    """
    positive_words = {"positive", "credit", "deposit", "gain", "increase", "bij"}
    negative_words = {"negative", "debit", "withdrawal", "loss", "decrease", "af"}
    
    text = text.lower()  # Normalize to lowercase for case-insensitive matching
    
    if text in positive_words:
        return 1
    elif text in negative_words:
        return -1
    else:
        raise ValueError(f"Unrecognized word for sign conversion: {text}")


def extract_date_from_filename(filepath: str, regex: str, date_format: str = "%Y-%m-%d") -> datetime.date:
    """
    Extract a date from the filename in the specified file path.

    Args:
        filepath (str): The file path to check.
        regex (str): The regular expression pattern for extracting the date from the filename.
        date_format (str): The date format compatible with datetime.strptime().

    Returns:
        datetime.date: The date found in the filename.

    Raises:
        ValueError: If no match is found or if the date cannot be parsed.
    """
    filename = path.basename(filepath)
    match = re.match(regex, filename)

    if not match:
        raise ValueError(f"No match found for the regex '{regex}' in filename '{filename}'.")

    date_str = match.group("date")

    try:
        return datetime.strptime(date_str, date_format).date()
    except ValueError:
        raise ValueError(f"Could not parse date '{date_str}' with format '{date_format}'.")


def match_filepath_extension(filepath: str, *extensions: str) -> bool:
    """
    Check if the given file path ends with the specified file extension(s).

    Args:
        filepath (str): The file path to check.
        extensions (Union[str, Tuple[str]]): One or more file extensions to match.

    Returns:
        bool: True if the file path ends with any specified extension, False otherwise.

    Raises:
        ValueError: If the filepath is empty.
    """
    if not filepath:
        raise ValueError("The provided filepath is empty.")
    
    return filepath.endswith(extensions)


def match_filepath_pattern(filepath: str, regex: str) -> bool:
    """
    Check if the filename in the given file path matches the specified regex pattern.

    Args:
        filepath (str): The file path to check.
        regex (str): The regular expression pattern to match the filename against.

    Returns:
        bool: True if the filename matches the regex pattern, False otherwise.

    Raises:
        ValueError: If the filepath is empty or the regex pattern is invalid.
    """
    if not filepath:
        raise ValueError("The provided filepath is empty.")
    
    if not regex:
        raise ValueError("The regex pattern cannot be empty.")

    filename = path.basename(filepath)
    return bool(re.match(regex, filename))


def match_filepath_date(
    filepath: str,
    regex: str,
    date_format: str = "%Y-%m-%d",
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None
) -> bool:
    """
    Check if the date extracted from the filename is within the specified date range.

    Args:
        filepath (str): The file path to check.
        regex (str): The regex pattern for extracting the date from the filename.
        date_format (str): The date format compatible with datetime.strptime().
        start_date (Optional[datetime.date]): The start date of the range (inclusive).
        end_date (Optional[datetime.date]): The end date of the range (inclusive).

    Returns:
        bool: True if the extracted file date is within the specified range, False otherwise.

    Raises:
        ValueError: If no date is found in the filename or if the date cannot be parsed.
    """
    if not filepath:
        raise ValueError("The provided filepath is empty.")
    
    try:
        file_date = extract_date_from_filename(filepath, regex, date_format)
    except ValueError as e:
        raise ValueError(f"Error extracting date from filename: {e}")

    if start_date and file_date < start_date:
        return False
    if end_date and file_date > end_date:
        return False

    return True


def clean_text(text: str) -> str:
    """
    Clean the input text by removing special characters and converting to lowercase.

    Args:
        text (str): The input string to clean.

    Returns:
        str: The cleaned string with special characters removed and all characters in lowercase.
    """
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    return cleaned_text.lower()  # Convert to lowercase


def shorten_text(text: str, max_length: int = -1) -> str:
    """
    Shorten the given text to a specified maximum length without cutting off words.

    Args:
        text (str): The text to shorten.
        max_length (int): The maximum length of the shortened text; -1 indicates no limit.

    Returns:
        str: The shortened text with "..." added if it exceeds the max length.

    Raises:
        ValueError: If max_length is negative (other than -1).
    """
    if max_length < -1:
        raise ValueError("max_length cannot be negative except for -1.")

    if max_length == -1:
        return text

    if len(text) <= max_length:
        return text  

    shortened = text[:max_length].rsplit(' ', 1)[0] 
    return f"{shortened}..."


def reduce_whitespace(text: str) -> str:
    """
    Reduce consecutive whitespace characters in a string to a single space.

    Args:
        text (str): The string to process.

    Returns:
        str: The processed string with reduced whitespace.
    """
    return re.sub(r'\s+', ' ', text).strip()
