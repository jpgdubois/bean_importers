from typing import Protocol, Optional, Mapping, Tuple, Iterable
from beancount.core.amount import Amount
from datetime import datetime
from beangulp_importers.datatypes import TransactionType


class AmountIdentifier(Protocol):
    """
    Protocol for any callable that can identify and return an Amount 
    based on a text entry.
    """
    def __call__(self, text_entry: Mapping[str, str]) -> Amount:
        """
        Extract and return an Amount from the text entry.
        
        Args:
            text_entry (Mapping[str, str]): The dictionary-like object 
                                            containing text data.
        
        Returns:
            Amount: The extracted amount object.
        """
        ...


class DateIdentifier(Protocol):
    """
    Protocol for any callable that can identify and return dates 
    from a text entry.
    """
    def __call__(self, text_entry: Mapping[str, str]) -> Tuple[datetime.date, datetime.date]:
        ...


class TransactionTypeIdentifier(Protocol):
    """
    Protocol for any callable that can identify and return a transaction type 
    based on a text entry.

    Methods:
        __call__(text_entry: Mapping[str, str]) -> TransactionTypes:
            Extract and return the transaction type from the text entry.
    """
    def __call__(self, text_entry: Mapping[str, str]) -> TransactionType:
        ...


class PayeeNarrationIdentifier(Protocol):
    def __call__(self, text_entry: Mapping[str, str]) -> Tuple[Optional[str], Optional[str]]:
        ...

class FileDescription(Protocol):

    def identify(self, filepath: str) -> bool:
        ...

    def date(self, filepath: str) -> datetime.date:
        ...

    def read(self, filepath: str) -> Iterable[Mapping]:
        ...

    def name(self, filepath: str) -> str:
        ...