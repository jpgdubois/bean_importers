from typing import Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from beancount.core.amount import Amount
from beangulp_importers.text_utils import (
    convert_text_to_currency,
    convert_text_to_decimal,
    convert_text_to_sign,
    clean_text,
    shorten_text,
)

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
            currency (str): Key of the currency or currency of the amount.

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
            currency (str): Key of the currency or currency of the amount.

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
            currency (str): Key of the currency or currency of the amount.

        Returns:
            AmountIdentifier: An instance with mode set to 'from_sign_amount'.
        """
        return AmountIdentifier(sign=sign, amount=amount, deposit="", withdrawal="", mode="from_sign_amount", currency=currency)

    def get_amount(self, text_entry: dict) -> Amount:
        """
        Retrieves the amount based on the mode of the `AmountIdentifier` object.
        The function processes the provided dictionary `text_text_entry` depending on the mode 
        (`from_amount`, `from_deposit_withdrawal`, or `from_sign_amount`). It checks 
        for the necessary keys in the dictionary and raises appropriate errors for 
        missing keys or invalid values.

        Args:
            text_text_entry (dict): The dictionary containing the required data for calculating the amount.

        Returns:
            Amount: The calculated amount as an Amount object.

        Raises:
            KeyError: If required keys are missing from the `text_text_entry` dictionary.
            ValueError: If invalid values or mode is encountered (e.g., both deposit 
                        and withdrawal are non-zero, or mode is unknown).
        """
        # Check if the currency key is present in the text_text_entry dictionary, if not assume the string is the currency itself
        currency = self.currency if self.currency not in text_entry else text_entry[self.currency]
        currency = convert_text_to_currency(currency)
            
        # Match the mode to determine how to calculate the amount
        match self.mode:
            case "from_amount":
                # Ensure the 'amount' key is present in the dictionary
                if self.amount not in text_entry:
                    raise KeyError(f"Key '{self.amount}' not found in text_text_entry")
                # Convert the 'amount' text to a decimal and return as an Amount object
                amount = convert_text_to_decimal(text_entry[self.amount])
                return Amount(amount, currency)

            case "from_deposit_withdrawal":
                # Ensure both 'deposit' and 'withdrawal' keys are present in the dictionary
                if self.deposit not in text_entry or self.withdrawal not in text_entry:
                    raise KeyError(f"Keys '{self.deposit}' or '{self.withdrawal}' not found in text_entry")
                # Convert deposit and withdrawal text to decimal values
                deposit = convert_text_to_decimal(text_entry[self.deposit])
                withdrawal = convert_text_to_decimal(text_entry[self.withdrawal])

                # Check if either deposit or withdrawal is non-zero but not both
                if deposit != 0 and withdrawal == 0:
                    return Amount(deposit, currency)
                elif deposit == 0 and withdrawal != 0:
                    return Amount(withdrawal, currency)              
                else:
                    raise ValueError("Deposit and withdrawal cannot both be non-zero")

            case "from_sign_amount":
                # Ensure the 'amount' and 'sign' keys are present in the dictionary
                if self.amount not in text_entry or self.sign not in text_entry:
                    raise KeyError(f"Keys '{self.amount}' or '{self.sign}' not found in text_entry")
                # Convert the amount and sign text to decimal and numeric sign respectively
                amount = convert_text_to_decimal(text_entry[self.amount])
                sign = convert_text_to_sign(text_entry[self.sign])

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
        transaction_date (str): Key for the transaction date in the text_entry dictionary.
        posting_date (str): Key for the posting date in the text_entry dictionary.
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

    def get_date(self, text_entry: dict) -> datetime.date:
        """
        Retrieves the date from the provided text_entry dictionary, defaulting to the posting date.

        Args:
            text_entry (dict): The dictionary containing date data.

        Returns:
            datetime: The posting date as a datetime object.
        """
        return self.get_posting_date(text_entry)

    def get_posting_date(self, text_entry: dict) -> datetime.date:
        """
        Retrieves the posting date from the provided text_entry dictionary.

        Args:
            text_entry (dict): The dictionary containing posting date data.

        Returns:
            datetime: The posting date as a datetime object.

        Raises:
            KeyError: If the posting_date key is not found in the text_entry dictionary.
        """
        if self.posting_date not in text_entry:
            raise KeyError(f"Key '{self.posting_date}' not found in text_entry")
        return datetime.strptime(text_entry[self.posting_date], self.format)

    def get_transaction_date(self, text_entry: dict) -> datetime.date:
        """
        Retrieves the transaction date from the provided text_entry dictionary.

        Args:
            text_entry (dict): The dictionary containing transaction date data.

        Returns:
            datetime: The transaction date as a datetime object.

        Raises:
            KeyError: If the transaction_date key is not found in the text_entry dictionary.
        """
        if self.transaction_date and self.transaction_date not in text_entry:
            raise KeyError(f"Key '{self.transaction_date}' not found in text_entry")
        return datetime.strptime(text_entry[self.transaction_date], self.format)


@dataclass
class TransactionTypeIdentifier:
    """
    A class to identify the type of a transaction based on predefined keys. 
    This class allows for classification of transactions into categories such as 
    transfer, exchange, and skip, based on the provided input parameters.

    Attributes:
        key (str): Key of the transaction type to be identified in the text_entry.
        transfer (set[str]): A list of strings representing transfer transaction types.
        exchange (set[str]): A list of strings representing exchange transaction types.
        skip (set[str]): A list of strings representing transaction types to be skipped.
    """

    key: str
    transfer: Tuple[str] = ()
    exchange: Tuple[str] = ()
    skip: Tuple[str] = ()

    def get_type(self, text_entry: dict) -> str:
        """
        Retrieves the type of the transaction from the provided text_entry dictionary.

        Args:
            text_entry (dict): The dictionary containing transaction data.

        Returns:
            str: The type of transaction, which can be 'transfer', 'exchange', or 'skip'.

        Raises:
            KeyError: If the key for the transaction type is not found in the text_entry dictionary.
            ValueError: If the transaction type is not recognized.
        """
        # Check if the key exists in the text_entry dictionary
        if self.key not in text_entry:
            raise KeyError(f"Key '{self.key}' not found in text_entry")
        
        # Match the transaction type
        match text_entry[self.key]:
            case x if x in self.transfer:
                return "transfer"
            case x if x in self.exchange:
                return "exchange"
            case x if x in self.skip:
                return "skip"
            case _:
                raise ValueError(f"Unknown transaction type: {text_entry[self.key]}")

        
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

    payee: Optional[str] = None
    narration: Optional[str] = None
    payee_account: Optional[str] = None

    def get_payee(self, text_entry: dict) -> Optional[str]:
        """
        Retrieves the payee from the provided text_entry dictionary.

        Args:
            text_entry (dict): The dictionary containing transaction data.

        Returns:
            str: The cleaned payee string.

        Raises:
            KeyError: If the payee key is not found in the text_entry dictionary.
        """
        if not self.payee:
            return None
        if self.payee not in text_entry:
            raise KeyError(f"Key '{self.payee}' not found in text_entry")
        return clean_text(text_entry[self.payee])

    def get_narration(self, text_entry: dict) -> Optional[str]:
        """
        Retrieves the narration from the provided text_entry dictionary.

        Args:
            text_entry (dict): The dictionary containing transaction data.

        Returns:
            str: The cleaned narration string.

        Raises:
            KeyError: If the narration key is not found in the text_entry dictionary.
        """
        if not self.narration:
            return None
        if self.narration not in text_entry:
            raise KeyError(f"Key '{self.narration}' not found in text_entry")
        return shorten_text(clean_text(text_entry[self.narration]), 40)

    def get_payee_account(self, text_entry: dict) -> Optional[str]:
        """
        Retrieves the payee account from the provided text_entry dictionary.

        Args:
            text_entry (dict): The dictionary containing transaction data.

        Returns:
            str: The cleaned payee account string.

        Raises:
            KeyError: If the narration key is not found in the text_entry dictionary.
        """
        if not self.payee_account:
            return None
        if self.payee_account not in text_entry:
            raise KeyError(f"Key '{self.payee_account}' not found in text_entry")
        return shorten_text(clean_text(text_entry[self.payee_account]), 40)
