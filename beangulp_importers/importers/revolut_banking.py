from dataclasses import dataclass
import datetime
from typing import List, NamedTuple

from beancount.core.data import Account, Entries
from ..reader import read_csv
from ..transaction_builder import transfer
from ..datatypes import (
    DateIdentifier,
    TransactionTypeIdentifier,
    PayeeNarrationIdentifier,
    AmountIdentifier,
    
)

import beangulp
from beangulp.testing import main


class Importer(beangulp.Importer):

    def __init__(
        self,
        account: str,
        fee_account: str,
        currency: str,
    ):
        self.account = account
        self.fee_account = fee_account
        self.currency = currency

        self.date = DateIdentifier.from_transaction_posting_date(
            transaction_date="Started Date",
            posting_date="Completed Date",
            format="%Y-%m-%d",
        )
        self.transaction_type = TransactionTypeIdentifier(
            key="Type",
            transfer={"TOPUP"},
            exchange={"EXCHANGE"},
        )
        self.payee_narration = PayeeNarrationIdentifier(
            narration="Description",
        )
        self.amount = AmountIdentifier.from_amount(
            amount="Amount",
            currency="Currency",
        )
        self.fee = AmountIdentifier.from_amount(
            amount="Fee",
            currency="Currency",
        )
        self.balance = AmountIdentifier.from_amount(
            amount="Balance",
            currency="Currency",
        )


    def identify(self, filepath: str) -> bool:
        return super().identify(filepath)
    
    def filename(self, filepath: str) -> str | None:
        return super().filename(filepath)
    
    def account(self, filepath: str) -> str:
        return self.account
    
    def date(self, filepath: str) -> datetime.date:
        raise NotImplementedError
    
    def extract(self, filepath: Account, existing: List[NamedTuple]) -> List[NamedTuple]:
        """
        Extract transactions from the provided CSV file and return Beancount entries.

        Args:
            filepath (str): The file path of the CSV file.
            existing (List[data.Entry]): A list of existing Beancount entries.

        Returns:
            List[data.Entry]: A list of extracted Beancount entries.
        """
        return super().extract(filepath, existing)