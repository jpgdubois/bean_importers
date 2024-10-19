from dataclasses import dataclass
from typing import Protocol, Mapping

from beancount.core.amount import Amount

from beangulp_importers.string_utils import Currency, convert_text_to_currency
from beangulp_importers.string_utils import convert_text_to_decimal, convert_text_to_sign


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
class FromAmount:
    """
    Extracts an Amount based on the provided keys for amount and currency.
    """
    amount_key: str
    currency_key: str

    def __call__(self, text_entry: Mapping[str, str]) -> Amount:
        """
        Extract the amount and currency from the text entry and return 
        an Amount object.
        
        Args:
            text_entry (Mapping[str, str]): The dictionary-like object 
                                            containing text data.
        
        Returns:
            Amount: The extracted amount with the currency.
        
        Raises:
            KeyError: If any required keys are missing in the text entry.
        """
        _require_keys(text_entry, self.amount_key, self.currency_key)

        amount_value = convert_text_to_decimal(text_entry[self.amount_key])
        currency_value = convert_text_to_currency(text_entry[self.currency_key]).value
        return Amount(amount_value, currency_value)


@dataclass(kw_only=True, frozen=True)
class FromDepositWithdraw:
    """
    Extracts an Amount based on separate deposit and withdrawal keys 
    and currency key.
    """
    deposit_key: str
    withdraw_key: str
    currency_key: str

    def __call__(self, text_entry: Mapping[str, str]) -> Amount:
        """
        Extract the deposit or withdrawal amount and return an Amount object.
        
        Args:
            text_entry (Mapping[str, str]): The dictionary-like object 
                                            containing text data.
        
        Returns:
            Amount: The extracted amount with the currency.
        
        Raises:
            KeyError: If any required keys are missing in the text entry.
            ValueError: If both deposit and withdrawal are non-zero.
        """
        _require_keys(text_entry, self.deposit_key, self.withdraw_key, self.currency_key)

        deposit_value = convert_text_to_decimal(text_entry[self.deposit_key])
        withdrawal_value = convert_text_to_decimal(text_entry[self.withdraw_key])
        currency_value = convert_text_to_currency(text_entry[self.currency_key]).value

        if deposit_value != 0 and withdrawal_value == 0:
            return Amount(deposit_value, currency_value)
        elif deposit_value == 0 and withdrawal_value != 0:
            return Amount(withdrawal_value, currency_value)
        else:
            raise ValueError("Deposit and withdrawal cannot both be non-zero")


@dataclass(kw_only=True, frozen=True)
class FromSignAmount:
    """
    Extracts an Amount based on provided keys for a sign, amount, and currency.
    """
    sign_key: str
    amount_key: str
    currency_key: str

    def __call__(self, text_entry: Mapping[str, str]) -> Amount:
        """
        Extract the signed amount and return an Amount object.
        
        Args:
            text_entry (Mapping[str, str]): The dictionary-like object 
                                            containing text data.
        
        Returns:
            Amount: The extracted signed amount with the currency.
        
        Raises:
            KeyError: If any required keys are missing in the text entry.
        """
        _require_keys(text_entry, self.sign_key, self.amount_key, self.currency_key)

        amount_value = convert_text_to_decimal(text_entry[self.amount_key])
        sign_value = convert_text_to_sign(text_entry[self.sign_key])
        currency_value = convert_text_to_currency(text_entry[self.currency_key]).value

        return Amount(sign_value * amount_value, currency_value)


@dataclass(kw_only=True, frozen=True)
class FromAmount:
    """
    Extracts an Amount based on the provided key for amount and the actual currency.
    """
    amount_key: str
    currency_key: str

    def __call__(self, text_entry: Mapping[str, str]) -> Amount:
        """
        Extract the amount and currency from the text entry and return 
        an Amount object.
        
        Args:
            text_entry (Mapping[str, str]): The dictionary-like object 
                                            containing text data.
        
        Returns:
            Amount: The extracted amount with the currency.
        
        Raises:
            KeyError: If any required keys are missing in the text entry.
        """
        _require_keys(text_entry, self.amount_key, self.currency_key)

        amount_value = convert_text_to_decimal(text_entry[self.amount_key])
        currency_value = convert_text_to_currency(text_entry[self.currency_key]).value
        return Amount(amount_value, currency_value)


@dataclass(kw_only=True, frozen=True)
class FromDepositWithdraw:
    """
    Extracts an Amount based on separate deposit and withdrawal keys 
    and currency.
    """
    deposit_key: str
    withdraw_key: str
    currency_key: str

    def __call__(self, text_entry: Mapping[str, str]) -> Amount:
        """
        Extract the deposit or withdrawal amount and return an Amount object.
        
        Args:
            text_entry (Mapping[str, str]): The dictionary-like object 
                                            containing text data.
        
        Returns:
            Amount: The extracted amount with the currency.
        
        Raises:
            KeyError: If any required keys are missing in the text entry.
            ValueError: If both deposit and withdrawal are non-zero.
        """
        _require_keys(text_entry, self.deposit_key, self.withdraw_key, self.currency_key)

        deposit_value = convert_text_to_decimal(text_entry[self.deposit_key])
        withdrawal_value = convert_text_to_decimal(text_entry[self.withdraw_key])
        currency_value = convert_text_to_currency(text_entry[self.currency_key]).value

        if deposit_value != 0 and withdrawal_value == 0:
            return Amount(deposit_value, currency_value)
        elif deposit_value == 0 and withdrawal_value != 0:
            return Amount(withdrawal_value, currency_value)
        else:
            raise ValueError("Deposit and withdrawal cannot both be non-zero")


@dataclass(kw_only=True, frozen=True)
class FromSignAmount:
    """
    Extracts an Amount based on a sign, amount, and currency.
    """
    sign_key: str
    amount_key: str
    currency_key: str

    def __call__(self, text_entry: Mapping[str, str]) -> Amount:
        """
        Extract the signed amount and return an Amount object.
        
        Args:
            text_entry (Mapping[str, str]): The dictionary-like object 
                                            containing text data.
        
        Returns:
            Amount: The extracted signed amount with the currency.
        
        Raises:
            KeyError: If any required keys are missing in the text entry.
        """
        _require_keys(text_entry, self.sign_key, self.amount_key, self.currency_key)

        amount_value = convert_text_to_decimal(text_entry[self.amount_key])
        sign_value = convert_text_to_sign(text_entry[self.sign_key])
        currency_value = convert_text_to_currency(text_entry[self.currency_key]).value

        return Amount(sign_value * amount_value, currency_value)


@dataclass(kw_only=True, frozen=True)
class FromAmountWithCurrency:
    """
    Extracts an Amount based on the provided keys for amount and an actual Currency.
    """
    amount_key: str
    currency: Currency  # type hint for actual Currency object

    def __call__(self, text_entry: Mapping[str, str]) -> Amount:
        """
        Extract the amount from the text entry and return an Amount object with the given Currency.
        Args:
            text_entry (Mapping[str, str]): The dictionary-like object containing text data.
        Returns:
            Amount: The extracted amount with the specified currency.
        Raises:
            KeyError: If any required keys are missing in the text entry.
        """
        _require_keys(text_entry, self.amount_key)

        amount_value = convert_text_to_decimal(text_entry[self.amount_key])
        return Amount(amount_value, self.currency.value)  # Using the Currency object directly

@dataclass(kw_only=True, frozen=True)
class FromDepositWithdrawWithCurrency:
    """
    Extracts an Amount based on separate deposit and withdrawal keys and an actual Currency.
    """
    deposit_key: str
    withdraw_key: str
    currency: Currency  # type hint for actual Currency object

    def __call__(self, text_entry: Mapping[str, str]) -> Amount:
        """
        Extract the deposit or withdrawal amount and return an Amount object with the given Currency.
        Args:
            text_entry (Mapping[str, str]): The dictionary-like object containing text data.
        Returns:
            Amount: The extracted amount with the specified currency.
        Raises:
            KeyError: If any required keys are missing in the text entry.
            ValueError: If both deposit and withdrawal are non-zero.
        """
        _require_keys(text_entry, self.deposit_key, self.withdraw_key)
        
        deposit_value = convert_text_to_decimal(text_entry[self.deposit_key])
        withdrawal_value = convert_text_to_decimal(text_entry[self.withdraw_key])

        if deposit_value != 0 and withdrawal_value == 0:
            return Amount(deposit_value, self.currency.value)  # Using the Currency object directly
        elif deposit_value == 0 and withdrawal_value != 0:
            return Amount(withdrawal_value, self.currency.value)  # Using the Currency object directly
        else:
            raise ValueError("Deposit and withdrawal cannot both be non-zero")

@dataclass(kw_only=True, frozen=True)
class FromSignAmountWithCurrency:
    """
    Extracts an Amount based on provided keys for a sign, amount, and an actual Currency.
    """
    sign_key: str
    amount_key: str
    currency: Currency  # type hint for actual Currency object

    def __call__(self, text_entry: Mapping[str, str]) -> Amount:
        """
        Extract the signed amount and return an Amount object with the given Currency.
        Args:
            text_entry (Mapping[str, str]): The dictionary-like object containing text data.
        Returns:
            Amount: The extracted signed amount with the specified currency.
        Raises:
            KeyError: If any required keys are missing in the text entry.
        """
        _require_keys(text_entry, self.sign_key, self.amount_key)
        
        amount_value = convert_text_to_decimal(text_entry[self.amount_key])
        sign_value = convert_text_to_sign(text_entry[self.sign_key])
        
        return Amount(sign_value * amount_value, self.currency.value)  # Using the Currency object directly
