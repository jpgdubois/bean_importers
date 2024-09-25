import re
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from beancount.core.amount import Amount

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


@dataclass
class AmountIdentifier:
    """
    A class to identify and process different types of monetary amounts 
    based on the provided input parameters. This class can handle amounts 
    based on direct amounts, deposits and withdrawals, or signed amounts.

    Attributes:
        sign (str): Key of the sign information of the amount (positive or negative).
        amount (str): Key of the string representation of the amount.
        deposit (str): Key of the string representation of the deposit amount.
        withdrawal (str): Key of the string representation of the withdrawal amount.
        currency (str): Key of the currency associated with the amount (e.g., 'USD').
        mode (str): The mode of operation which determines how the amount is calculated 
                    (e.g., 'from_amount', 'from_deposit_withdrawal', or 'from_sign_amount').
    """

    sign: str
    amount: str
    deposit: str
    withdrawal: str
    currency: str
    mode: str

    @staticmethod
    def from_amount(amount: str, currency: str) -> 'AmountIdentifier':
        """
        Creates an AmountIdentifier from the amount and currency.

        Args:
            amount (str): Key of the amount to be identified.
            currency (str): Key of fhe currency of the amount.

        Returns:
            AmountIdentifier: An instance with mode set to 'from_amount'.
        """
        return AmountIdentifier(sign="", amount=amount, deposit="", withdrawal="", mode="from_amount", currency=currency)

    @staticmethod
    def from_deposit_withdrawal(deposit: str, withdrawal: str, currency: str) -> 'AmountIdentifier':
        """
        Creates an AmountIdentifier from the deposit and withdrawal amounts.

        Args:
            deposit (str): Key of the deposit amount.
            withdrawal (str): Key of the withdrawal amount.
            currency (str): Key of the currency associated with the amounts.

        Returns:
            AmountIdentifier: An instance with mode set to 'from_deposit_withdrawal'.
        """
        return AmountIdentifier(sign="", amount="", deposit=deposit, withdrawal=withdrawal, mode="from_deposit_withdrawal", currency=currency)

    @staticmethod
    def from_sign_amount(sign: str, amount: str, currency: str) -> 'AmountIdentifier':
        """
        Creates an AmountIdentifier from a sign and amount.

        Args:
            sign (str): Key of the sign of the amount (e.g., '+' or '-').
            amount (str): Key of the amount value.
            currency (str): Key of the currency associated with the amount.

        Returns:
            AmountIdentifier: An instance with mode set to 'from_sign_amount'.
        """
        return AmountIdentifier(sign=sign, amount=amount, deposit="", withdrawal="", mode="from_sign_amount", currency=currency)

    def get_amount(self, entry: dict) -> Amount:
        """
        Retrieves the amount based on the mode of the `AmountIdentifier` object.
        The function processes the provided dictionary `entry` depending on the mode 
        (`from_amount`, `from_deposit_withdrawal`, or `from_sign_amount`). It checks 
        for the necessary keys in the dictionary and raises appropriate errors for 
        missing keys or invalid values.

        Args:
            entry (dict): The dictionary containing the required data for calculating the amount.

        Returns:
            Amount: The calculated amount as an Amount object.

        Raises:
            KeyError: If required keys are missing from the `entry` dictionary.
            ValueError: If invalid values or mode is encountered (e.g., both deposit 
                        and withdrawal are non-zero, or mode is unknown).
        """
        # Check if the currency key is present in the entry dictionary
        if self.currency not in entry:
            raise KeyError(f"Key '{self.currency}' not found in entry")

        # Match the mode to determine how to calculate the amount
        match self.mode:
            case "from_amount":
                # Ensure the 'amount' key is present in the dictionary
                if self.amount not in entry:
                    raise KeyError(f"Key '{self.amount}' not found in entry")
                # Convert the 'amount' text to a decimal and return as an Amount object
                amount = convert_text_to_decimal(entry[self.amount])
                currency = convert_text_to_currency(entry[self.currency])
                return Amount(amount, currency)

            case "from_deposit_withdrawal":
                # Ensure both 'deposit' and 'withdrawal' keys are present in the dictionary
                if self.deposit not in entry or self.withdrawal not in entry:
                    raise KeyError(f"Keys '{self.deposit}' or '{self.withdrawal}' not found in entry")
                # Convert deposit and withdrawal text to decimal values
                deposit = convert_text_to_decimal(entry[self.deposit])
                withdrawal = convert_text_to_decimal(entry[self.withdrawal])
                currency = convert_text_to_currency(entry[self.currency])

                # Check if either deposit or withdrawal is non-zero but not both
                if deposit != 0 and withdrawal == 0:
                    return Amount(deposit, currency)
                elif deposit == 0 and withdrawal != 0:
                    return Amount(withdrawal, currency)              
                else:
                    raise ValueError("Deposit and withdrawal cannot both be non-zero")

            case "from_sign_amount":
                # Ensure the 'amount' and 'sign' keys are present in the dictionary
                if self.amount not in entry or self.sign not in entry:
                    raise KeyError(f"Keys '{self.amount}' or '{self.sign}' not found in entry")
                # Convert the amount and sign text to decimal and numeric sign respectively
                amount = convert_text_to_decimal(entry[self.amount])
                sign = convert_text_to_sign(entry[self.sign])
                currency = convert_text_to_currency(entry[self.currency])

                # Return the amount with the applied sign
                return Amount(sign * amount, currency)

            case _:
                # Raise an error for unknown modes
                raise ValueError(f"Unknown mode: {self.mode}")


@dataclass
class DateIdentifier:
    """
    A class to identify and process transaction and posting dates from a given input. 
    This class can handle dates formatted as strings and convert them to datetime objects 
    based on the specified format.

    Attributes:
        transaction_date (str): Key for the transaction date in the entry dictionary.
        posting_date (str): Key for the posting date in the entry dictionary.
        format (str): The date format string used for parsing dates (default is "%Y-%m-%d").
    """
    
    transaction_date: str
    posting_date: str
    format: str = "%Y-%m-%d"

    @staticmethod
    def from_date(date: str, format: str = "%Y-%m-%d") -> 'DateIdentifier':
        """
        Creates a DateIdentifier instance from a posting date.

        Args:
            date (str): The posting date as a string.
            format (str): The format to use for the date (default is "%Y-%m-%d").

        Returns:
            DateIdentifier: An instance with transaction_date set to an empty string and posting_date set to the provided date.
        """
        return DateIdentifier(transaction_date="", posting_date=date, format=format)

    @staticmethod
    def from_transaction_posting_date(transaction_date: str, posting_date: str, format: str = "%Y-%m-%d") -> 'DateIdentifier':
        """
        Creates a DateIdentifier instance from transaction and posting dates.

        Args:
            transaction_date (str): The transaction date as a string.
            posting_date (str): The posting date as a string.
            format (str): The format to use for the dates (default is "%Y-%m-%d").

        Returns:
            DateIdentifier: An instance with specified transaction_date and posting_date.
        """
        return DateIdentifier(transaction_date=transaction_date, posting_date=posting_date, format=format)

    def get_date(self, entry: dict) -> datetime:
        """
        Retrieves the date from the provided entry dictionary, defaulting to the posting date.

        Args:
            entry (dict): The dictionary containing date data.

        Returns:
            datetime: The posting date as a datetime object.
        """
        return self.get_posting_date(entry)

    def get_posting_date(self, entry: dict) -> datetime:
        """
        Retrieves the posting date from the provided entry dictionary.

        Args:
            entry (dict): The dictionary containing posting date data.

        Returns:
            datetime: The posting date as a datetime object.

        Raises:
            KeyError: If the posting_date key is not found in the entry dictionary.
        """
        if self.posting_date not in entry:
            raise KeyError(f"Key '{self.posting_date}' not found in entry")
        return datetime.strptime(entry[self.posting_date], self.format)

    def get_transaction_date(self, entry: dict) -> datetime:
        """
        Retrieves the transaction date from the provided entry dictionary.

        Args:
            entry (dict): The dictionary containing transaction date data.

        Returns:
            datetime: The transaction date as a datetime object.

        Raises:
            KeyError: If the transaction_date key is not found in the entry dictionary.
        """
        if self.transaction_date and self.transaction_date not in entry:
            raise KeyError(f"Key '{self.transaction_date}' not found in entry")
        return datetime.strptime(entry[self.transaction_date], self.format)


@dataclass
class TransactionTypeIdentifier:
    """
    A class to identify the type of a transaction based on predefined keys. 
    This class allows for classification of transactions into categories such as 
    transfer, exchange, and skip, based on the provided input parameters.

    Attributes:
        key (str): Key of the transaction type to be identified in the entry.
        transfer (set[str]): A list of strings representing transfer transaction types.
        exchange (set[str]): A list of strings representing exchange transaction types.
        skip (set[str]): A list of strings representing transaction types to be skipped.
    """

    key: str
    transfer: set[str]
    exchange: set[str]
    skip: set[str]

    def get_type(self, entry: dict) -> str:
        """
        Retrieves the type of the transaction from the provided entry dictionary.

        Args:
            entry (dict): The dictionary containing transaction data.

        Returns:
            str: The type of transaction, which can be 'transfer', 'exchange', or 'skip'.

        Raises:
            KeyError: If the key for the transaction type is not found in the entry dictionary.
            ValueError: If the transaction type is not recognized.
        """
        # Check if the key exists in the entry dictionary
        if self.key not in entry:
            raise KeyError(f"Key '{self.key}' not found in entry")
        
        # Match the transaction type
        match entry[self.key]:
            case x if x in self.transfer:
                return "transfer"
            case x if x in self.exchange:
                return "exchange"
            case x if x in self.skip:
                return "skip"
            case _:
                raise ValueError(f"Unknown transaction type: {entry[self.key]}")

        
@dataclass
class PayeeNarrationIdentifier:
    """
    A class to identify and process payee and narration information from transactions. 
    This class allows for retrieval of the payee and narration based on the provided 
    input parameters.

    Attributes:
        payee (str): Key of the payee associated with the transaction.
        narration (str): Key of the narration or description of the transaction.
        payee_account (str): Key of the account associated with the payee (optional).
    """

    payee: str
    narration: str = ""
    payee_account: str = ""

    def get_payee(self, entry: dict) -> str:
        """
        Retrieves the payee from the provided entry dictionary.

        Args:
            entry (dict): The dictionary containing transaction data.

        Returns:
            str: The cleaned payee string.

        Raises:
            KeyError: If the payee key is not found in the entry dictionary.
        """
        if self.payee not in entry:
            raise KeyError(f"Key '{self.payee}' not found in entry")
        return clean_text(entry[self.payee])

    def get_narration(self, entry: dict) -> str:
        """
        Retrieves the narration from the provided entry dictionary.

        Args:
            entry (dict): The dictionary containing transaction data.

        Returns:
            str: The cleaned narration string.

        Raises:
            KeyError: If the narration key is not found in the entry dictionary.
        """
        if self.narration not in entry:
            raise KeyError(f"Key '{self.narration}' not found in entry")
        return shorten_text(clean_text(entry[self.narration]), 40)
