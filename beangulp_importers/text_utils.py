import re
from decimal import Decimal
from datetime import datetime

def convert_text_to_decimal(text: str) -> Decimal:
    """
    Convert a string representation of a number into a float.

    This function strips whitespace, handles signed numbers, and replaces
    the last non-digit character found (that is not a sign) with a decimal point.

    Args:
        number (str): The string representation of the number to convert.

    Returns:
        float: The converted floating-point number.

    Raises:
        ValueError: If the input string cannot be converted to a float.
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
        number = text[1:].strip()

    # Find all separators (non-digit characters)
    separators = re.sub(r"\d", "", number)  # Exclude signs and digits
    if separators:
        for sep in separators[:-1]:
            number = number.replace(sep, "")
        number = number.replace(separators[-1], ".")

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


def convert_text_to_currency(text: str) -> str:
    """
    Extracts the currency code from the given text by removing non-letter characters,
    converting it to uppercase, and checking against a list of known currencies.

    Args:
        text (str): The input text containing a currency code.

    Returns:
        str: The extracted currency code if found and known.

    Raises:
        ValueError: If no known currency code is found in the text.
    """
    # List of known currencies (can vary in length)
    known_currencies = {"CHF", "EUR", "SEK", "USD", "GBP", "JPY", "AUD", "CAD", "NZD", "BTC", "ETH"}

    # Remove spaces and non-letter characters, then convert to uppercase
    cleaned_text = ''.join(char for char in text if char.isalpha()).upper()

    # Check if the cleaned text is a known currency
    if cleaned_text in known_currencies:
        return cleaned_text  # Return the known currency code in uppercase
    else:
        raise ValueError(f"Unknown currency: {cleaned_text}")


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


def shorten_text(text: str, max_length: int = 40) -> str:
    """
    Shortens the given text to a specified maximum length,
    ensuring that words are not cut off in the middle.

    Args:
        text (str): The text to shorten.
        max_length (int): The maximum length of the shortened text.

    Returns:
        str: The shortened text with "..." added if it exceeds the max length.
    """
    if len(text) <= max_length:
        return text  # Return original text if it's within the limit

    # Shorten text without cutting off words
    shortened = text[:max_length].rsplit(' ', 1)[0]  # Cut off at the last space within the limit

    return f"{shortened}..."


