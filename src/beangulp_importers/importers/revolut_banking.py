import beangulp
from beangulp.testing import main
from beangulp_importers.descriptors import (
    date,
    file,
    payee_narration,
    amount,
    transaction_type,
)
from beangulp_importers.datatypes import TransactionType, Currency
from beangulp_importers.base_importer.banking_importer import BankingImporter


class RevolutImporter(BankingImporter):

    
    def __init__(
        self,
        root_account: str,
        fee_account: str,
        currency: Currency,
    ):

        file_description = file.FileDescriptionCSV(
            file_extension = ".csv",
            file_pattern_regex = r"^account-statement_\d{4}-\d{2}-\d{2}_(?P<date>\d{4}-\d{2}-\d{2})_(en(-gb)?)_.*\.csv$",
            file_date_format = "%Y-%m-%d",
            file_delimiter=",",
            file_header = ("Type", "Product", "Started Date", "Completed Date", "Description", "Amount", "Fee", "Currency", "State", "Balance"),
            entry_mapping={'Currency': currency.value},
            start_date = None,
            end_date = None,
        )
        get_date = date.FromDate(
            date="Completed Date",
            date_format="%Y-%m-%d %H:%M:%S",
            empty_date="",
        )
        get_transaction_type = transaction_type.FromTransactionType(
            transaction_type_key="Type",
            transaction_type_mapping={
                TransactionType.exchange: ["EXCHANGE"],
                TransactionType.transfer: ["TOPUP", "CARD_PAYMENT", "TRANSFER"],
                TransactionType.skip: [],
            },
        )
        get_payee_narration = payee_narration.FromNarration(
            narration_key="Description",
            max_narration_length=40,
        )
        get_amount = amount.FromAmount(
            amount_key="Amount",
            currency_key="Currency",
        )
        get_fee = amount.FromAmount(
            amount_key="Fee",
            currency_key="Currency",
        )
        get_balance = amount.FromAmount(
            amount_key="Balance",
            currency_key="Currency",
        )
        BankingImporter.__init__(
            self,
            root_account=root_account,
            fee_account=fee_account,
            get_date=get_date,
            get_payee_narration=get_payee_narration,
            get_transaction_type=get_transaction_type,
            get_root_amount=get_amount,
            get_fee_amount=get_fee,
            get_balance=get_balance,
            file_description=file_description,
        )

if __name__ == "__main__":
    main = beangulp.Ingest([
        RevolutImporter(
            root_account="Assets:Revolut:EUR",
            fee_account="Expenses:Revolut:Fee",
            currency=Currency.EUR,
        ),
        RevolutImporter(
            root_account="Assets:Revolut:CHF",
            fee_account="Expenses:Revolut:Fee",
            currency=Currency.CHF,
        ),
    ])
    main()