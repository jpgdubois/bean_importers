from dataclasses import dataclass
from typing import Mapping, Iterable

from beangulp_importers.datatypes import TransactionType


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
class FromTransactionType:
    """
    Class that identifies the transaction type from a text entry.

    Attributes:
        transaction_type_key (str): The key in the text entry that contains 
                                     the transaction type value.
        transaction_type_mapping (Mapping[TransactionTypes, str]): A mapping 
                                                                 of transaction types to their corresponding string representations.

    Methods:
        __call__(text_entry: Mapping[str, str]) -> TransactionTypes:
            Extract and return the corresponding transaction type based on the 
            value found in the text entry.
    """
    transaction_type_key: str
    transaction_type_mapping: Mapping[TransactionType, Iterable[str]]

    def __call__(self, text_entry: Mapping[str, str]) -> TransactionType:
        """
        Extract the transaction type from the text entry based on the provided 
        transaction type mapping.

        Args:
            text_entry (Mapping[str, Iterable[str]]): The dictionary-like object containing 
                                             the transaction type mapping to the corresponding labels.

        Returns:
            TransactionTypes: The identified transaction type.

        Raises:
            KeyError: If any required keys are missing in the text entry.
            ValueError: If the transaction type found in the text entry is not 
                         recognized.
        """
        _require_keys(text_entry, self.transaction_type_key)
        for transaction_type, keys in self.transaction_type_mapping.items():

            # Find the transaction type corresponding to the key in text_entry
            if text_entry[self.transaction_type_key] in keys:
                return transaction_type
        
        raise ValueError(f"Transaction type '{text_entry[self.transaction_type_key]}' not recognized.")
