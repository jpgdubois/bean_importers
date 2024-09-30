from dataclasses import dataclass
from typing import Mapping, Optional
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
    empty_date: str = ""

    def __call__(self, text_entry: Mapping[str, str]) -> Optional[datetime.date]:
        """
        Extract the date from the text entry and return it.

        Args:
            text_entry (Mapping[str, str]): The dictionary-like object 
                                            containing text data.

        Returns:
            date | None: The extracted dates, None if the date string is equal to empty_date.

        Raises:
            KeyError: If the required date key is missing in the text entry.
            ValueError: If the date is not in the expected format.
        """
        _require_keys(text_entry, self.date)
        
        date = text_entry[self.date]

        # Check if date entry is empty
        if date == self.empty_date:
            return None
        
        # Format date
        try:
            date_value = datetime.strptime(date, self.date_format).date()
        except ValueError as e:
            raise ValueError(f"Invalid date format for '{self.date}': {e}")

        return date_value