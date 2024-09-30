from dataclasses import dataclass
import datetime
from typing import List, NamedTuple, Optional

from beancount.core import data, flags
import beangulp
from beangulp.testing import main

from beangulp_importers.file_utils import read_csv_table
from beangulp_importers.datatypes import TransactionType, Currency
from collections import defaultdict

from beangulp_importers.descriptors.protocols import (
    AmountIdentifier,
    DateIdentifier,
    PayeeNarrationIdentifier,
    TransactionTypeIdentifier,
    FileDescription
)

@dataclass(kw_only=True, frozen=True)
class BankingImporter(beangulp.Importer):

    root_account: str
    fee_account: Optional[str] = None
    get_date: DateIdentifier
    get_payee_narration: PayeeNarrationIdentifier
    get_transaction_type: TransactionTypeIdentifier
    get_root_amount: AmountIdentifier
    get_fee_amount: Optional[AmountIdentifier] = None
    get_balance: Optional[AmountIdentifier] = None
    file_description: FileDescription

    def identify(self, filepath: str) -> bool:
        return self.file_description.identify(filepath)
    
    def filename(self, filepath: str) -> str | None:
        return self.file_description.name(filepath)
    
    def date(self, filepath: str) -> datetime.date:
        return self.file_description.date(filepath)
    
    def account(self, filepath: str) -> str:
        return self.root_account
    
    def extract(self, filepath: str, existing: List[NamedTuple]) -> List[NamedTuple]:
        """
        Extract transactions from the provided file and return Beancount entries.

        Args:
            filepath (str): The file path of the CSV file.
            existing (List[data.Entry]): A list of existing Beancount entries.

        Returns:
            List[data.Entry]: A list of extracted Beancount entries.
        """
        entries = []    # List with the newly generated transactions
        balances = defaultdict(list)  # Dictionary with latest balance for each currency
        default_account = self.account(filepath)

        for lineno, row in enumerate(self.file_description.read(filepath)):
            # TODO: Implement extracting tags from table
            # TODO: Implement extracting links from table
            # TODO: Implement extracting flags from table

            meta = data.new_metadata(filepath, lineno)
            date = self.get_date(row)
            payee, narration = self.get_payee_narration(row)
            amount = self.get_root_amount(row)
            transaction_type = self.get_transaction_type(row)

            if not date:
                continue

            # Create a transaction.
            postings = [
                data.Posting(default_account, amount, None, None, None, None),
            ]
            if self.get_fee_amount and self.fee_account:
                fee = self.get_fee_amount(row)
                data.Posting(self.fee_account, fee, None, None, None, None),

            txn = data.Transaction(
                meta,
                date,
                flags.FLAG_OKAY,
                payee,
                narration,
                data.EMPTY_SET,
                data.EMPTY_SET,
                postings
            )

            # Add the transaction to the output list.
            entries.append(txn)

            # Do not add a balance check if balance is not available
            if not self.get_balance:
                continue

            # Add balance to balances list.
            balance = self.get_balance(row)
            if balance:
                date = date + datetime.timedelta(days=1)
                amount = balance
                # meta = data.new_metadata(filepath, lineno)
                balances[Currency(balance.currency)].append(data.Balance(meta, date, default_account, amount, data.EMPTY_SET, data.EMPTY_SET))

        if not entries:
            return []

        # Append balances.
        for currency, balances in balances.items():
            # Assume last balance is the latest one
            entries.append(balances[-1])

        return entries