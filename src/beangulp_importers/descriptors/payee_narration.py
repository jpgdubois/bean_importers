from dataclasses import dataclass
from typing import Mapping, Tuple, Optional
from beangulp_importers.string_utils import shorten_text, clean_text, reduce_whitespace

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
class FromPayeeNarration:
    payee_key: str
    narration_key: str
    max_payee_length: int = -1
    max_narration_length: int = -1

    def __call__(self, text_entry: Mapping[str, str]) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts and cleans payee and narration from the provided text entry.

        Args:
            text_entry (Mapping[str, str]): The dictionary-like object containing the text entry.

        Returns:
            PayeeNarration: An instance containing the cleaned payee and narration.
        """
        _require_keys(text_entry, self.payee_key, self.narration_key)

        payee_text = text_entry[self.payee_key]
        if payee_text is None:
            payee_text = ""

        narration_text = text_entry[self.narration_key]
        if narration_text is None:
            narration_text = ""

        payee_value = shorten_text(reduce_whitespace(clean_text(payee_text)), self.max_payee_length)
        narration_value = shorten_text(reduce_whitespace(clean_text(narration_text)), self.max_narration_length)
        return payee_value, narration_value

@dataclass(kw_only=True, frozen=True)
class FromPayee:
    payee_key: str
    max_payee_length: int = -1

    def __call__(self, text_entry: Mapping[str, str]) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts and cleans payee from the provided text entry.

        Args:
            text_entry (Mapping[str, str]): The dictionary-like object containing the text entry.

        Returns:
            PayeeNarration: An instance containing the cleaned payee and None for narration.
        """
        _require_keys(text_entry, self.payee_key)

        payee_value = shorten_text(reduce_whitespace(clean_text(text_entry[self.payee_key]), self.max_payee_length))
        return payee_value, None

@dataclass(kw_only=True, frozen=True)
class FromNarration:
    narration_key: str
    max_narration_length: int = -1

    def __call__(self, text_entry: Mapping[str, str]) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts and cleans narration from the provided text entry.

        Args:
            text_entry (Mapping[str, str]): The dictionary-like object containing the text entry.

        Returns:
            PayeeNarration: An instance containing None for payee and the cleaned narration.
        """
        _require_keys(text_entry, self.narration_key)

        narration_value = shorten_text(reduce_whitespace(clean_text(text_entry[self.narration_key])), self.max_narration_length)
        return None, narration_value
