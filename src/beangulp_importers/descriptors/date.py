from dataclasses import dataclass
from typing import Mapping, Tuple
from datetime import datetime

def _require_keys(text_entry: Mapping[str, str], *keys: str) -> None:
    """
    Ensures that all required keys are present in the text_entry.

    Args:
        text_entry (Mapping[str, str]): The dictionary-like object to check.
        *keys (str): The keys that are required to exist in text_entry.

    Raises:
        KeyError: If any of the specified keys are not found in text_entry.
    """
    for key in keys:
        if key not in text_entry:
            raise KeyError(f"Key '{key}' not found in text entry")


@dataclass(kw_only=True, frozen=True)
class FromDate:
    """
    Extracts a date from the provided key in the text entry.
    """
    date: str
    date_format: str = "%Y-%m-%d"  # Default date format

    def __call__(self, text_entry: Mapping[str, str]) -> Tuple[datetime.date, datetime.date]:
        """
        Extract the date from the text entry and return it.

        Args:
            text_entry (Mapping[str, str]): The dictionary-like object 
                                            containing text data.

        Returns:
            Tuple[date, date]: The extracted posting and transaction dates, which are assumed to be identical.

        Raises:
            KeyError: If the required date key is missing in the text entry.
            ValueError: If the date is not in the expected format.
        """
        _require_keys(text_entry, self.date)
        
        try:
            date_value = datetime.strptime(text_entry[self.date], self.date_format).date()
        except ValueError as e:
            raise ValueError(f"Invalid date format for '{self.date}': {e}")

        return date_value

@dataclass(kw_only=True, frozen=True)
class FromPostingTransactionDate:
    """
    Extracts posting and transaction dates from the provided keys in the text entry.
    """
    posting_date: str
    transaction_date: str
    date_format: str = "%Y-%m-%d"  # Default date format

    def __call__(self, text_entry: Mapping[str, str]) -> Tuple[datetime.date, datetime.date]:
        """
        Extract the posting and transaction dates from the text entry.

        Args:
            text_entry (Mapping[str, str]): The dictionary-like object 
                                            containing text data.

        Returns:
            Tuple[date, date]: The extracted posting and transaction dates.

        Raises:
            KeyError: If any required date keys are missing in the text entry.
            ValueError: If the posting date is not before the transaction date.
            ValueError: If any date is not in the expected format.
        """
        _require_keys(text_entry, self.posting_date, self.transaction_date)

        try:
            posting_date_value = datetime.strptime(text_entry[self.posting_date], self.date_format).date()
            transaction_date_value = datetime.strptime(text_entry[self.transaction_date], self.date_format).date()
        except ValueError as e:
            raise ValueError(f"Invalid date format for '{self.posting_date}' or '{self.transaction_date}': {e}")

        if posting_date_value > transaction_date_value:
            raise ValueError(f"Posting date must be before Transaction date: {posting_date_value} <= {transaction_date_value}")

        return posting_date_value, transaction_date_value
