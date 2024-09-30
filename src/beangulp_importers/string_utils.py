import re
from decimal import Decimal
from os import path
from datetime import datetime
from typing import Optional
from beangulp_importers.datatypes import Currency

def convert_text_to_currency(text: str) -> Currency:
    """
    Extracts the currency code from the given text by removing non-letter characters,
    converting it to uppercase, and checking against the Currency Enum.

    Args:
        text (str): The input text containing a currency code.

    Returns:
        Currency: The extracted currency as an enum member if found and known.

    Raises:
        ValueError: If no known currency code is found in the text.
    """
    # Remove spaces and non-letter characters, then convert to uppercase
    cleaned_text = "".join(char for char in text if char.isalpha()).upper()

    # Try to find the cleaned text in the Currency Enum
    try:
        return Currency[cleaned_text]  # Return the matching Currency enum member
    except KeyError:
        raise ValueError(f"Unknown currency: {cleaned_text}")


def convert_text_to_decimal(text: str) -> Decimal:
    """
    Convert a string representation of a number into a decimal.

    This function strips whitespace, handles signed numbers, and replaces
    the last non-digit character found (that is not a sign) with a decimal point.

    Args:
        number (str): The string representation of the number to convert.

    Returns:
        Decimal: The converted decimal number.

    Raises:
        ValueError: If the input string cannot be converted to a decimal.
    """
    # Strip whitespace from the input
    text = text.strip()

    # handle empty string
    if not text:
        return Decimal(0)

    # Handle optional sign at the beginning
    sign = ''
    if text and text[0] in ('+', '-'):
        sign = text[0]
        text = text[1:].strip()

    # Find all separators (non-digit characters)
    separators = re.sub(r"\d", "", text)  # Exclude signs and digits
    if separators:
        for sep in separators[:-1]:
            text = text.replace(sep, "")
        number = text.replace(separators[-1], ".")

    # Prepend the sign back to the number
    number = sign + number

    try:
        # Convert the cleaned string to float
        return Decimal(number)
    except ValueError:
        raise ValueError(f"Cannot convert '{number}' to Decimal.")


def convert_text_to_sign(text: str) -> int:
    """
    Converts a given word into a numeric sign (1 or -1) based on its meaning.
    
    Parameters:
    text (str): The word to be converted. It should represent either a positive 
                or a negative financial or directional concept (e.g., "credit", "debit").
    
    Returns:
    int: 1 if the word represents a positive concept (e.g., "credit", "deposit"), 
         -1 if it represents a negative concept (e.g., "debit", "withdrawal").
    
    Raises:
    ValueError: If the input word is not recognized as either positive or negative.
    
    Examples:
    >>> text_to_sign("credit")
    1
    >>> text_to_sign("withdrawal")
    -1
    """
    positive_words = {"positive", "credit", "deposit", "gain", "increase", "bij"}
    negative_words = {"negative", "debit", "withdrawal", "loss", "decrease", "af"}
    
    text = text.lower()  # Normalize the input to lowercase for case-insensitive matching
    
    if text in positive_words:
        return 1
    elif text in negative_words:
        return -1
    else:
        raise ValueError(f"Unrecognized word for sign conversion: {text}")
    

def extract_date_from_filename(filepath: str, regex: str, date_format: str = "%Y-%m-%d") -> datetime.date:
    """
    Extract a date from the filename in the given file path.

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
    date_str = match.group("date")

    # Attempt to parse the date string
    try:
        return datetime.strptime(date_str, date_format).date()
    except ValueError:
        raise ValueError(f"Could not parse date '{date_str}' with format '{date_format}'.")


def match_filepath_extension(filepath: str, *extensions: str) -> bool:
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

    Raises:
        ValueError: If the filepath is empty.
    """
    if not filepath:
        raise ValueError("The provided filepath is empty.")
    
    # Check if the filepath ends with any of the specified extensions
    return filepath.endswith(extensions)


def match_filepath_pattern(filepath: str, regex: str) -> bool:
    """
    Check if the filename in the given file path matches the specified regex pattern.

    Parameters:
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

    # Extract the filename from the file path
    filename = path.basename(filepath)

    # Use the regular expression to check for a match
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
    if not filepath:
        raise ValueError("The provided filepath is empty.")
    
    # Extract the date from the filename
    try:
        file_date = extract_date_from_filename(filepath, regex, date_format)
    except ValueError as e:
        raise ValueError(f"Error extracting date from filename: {e}")

    # Check if the file_date is between start_date and end_date
    if start_date and file_date < start_date:
        return False
    if end_date and file_date > end_date:
        return False

    return True


def clean_text(text: str) -> str:
    """
    Cleans the input text by removing special characters and converting it to lowercase.

    Args:
        text (str): The input string to clean.

    Returns:
        str: The cleaned string with special characters removed and all characters in lowercase.
    """
    # Remove special characters using regex and convert to lowercase
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    cleaned_text = cleaned_text.lower()  # Convert to lowercase
    return cleaned_text


def shorten_text(text: str, max_length: int = -1) -> str:
    """
    Shortens the given text to a specified maximum length,
    ensuring that words are not cut off in the middle.

    Args:
        text (str): The text to shorten.
        max_length (int): The maximum length of the shortened text.
                          It can be -1 to indicate no limit.

    Returns:
        str: The shortened text with "..." added if it exceeds the max length.

    Raises:
        ValueError: If max_length is negative (other than -1).
    """
    # Raise an error if max_length is negative and not -1
    if max_length < -1:
        raise ValueError("max_length cannot be negative except for -1.")

    # Return original text if max_length is set to -1
    if max_length == -1:
        return text

    # Return original text if it's within the limit
    if len(text) <= max_length:
        return text  

    # Shorten text without cutting off words
    shortened = text[:max_length].rsplit(' ', 1)[0] 
    return f"{shortened}..."

def reduce_whitespace(text: str) -> str:
    """
    Reduce consecutive whitespace characters in a string to a single space.

    :param input_string: The string to process.
    :return: The processed string with reduced whitespace.
    """
    return re.sub(r'\s+', ' ', text).strip()

