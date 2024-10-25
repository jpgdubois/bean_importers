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


class INGCurrentImporter(BankingImporter):
    
    def __init__(
        self,
        root_account: str,
        root_account_id: str,
    ):

        file_description = file.FileDescriptionCSV(
            file_extension = ".csv",
            file_pattern_regex = rf"^{root_account_id}_\d{{2}}-\d{{2}}-\d{{4}}_(?P<date>\d{{2}}-\d{{2}}-\d{{4}})\.csv$",
            file_date_format = "%d-%m-%Y",
            file_delimiter = ";",
            file_header = ("Date", r"Name / Description", "Account", "Counterparty", "Code", r"Debit/credit", "Amount (EUR)", "Transaction type", "Notifications", "Resulting balance", "Tag"),
            entry_mapping=None,
            start_date = None,
            end_date = None,
        )
        get_date = date.FromDate(
            date="Date",
            date_format="%Y%m%d",
        )
        get_transaction_type = transaction_type.FromTransactionType(
            transaction_type_key="Code",
            transaction_type_mapping={
                TransactionType.exchange: [],
                TransactionType.transfer: ["OV", "GT", "VZ", "ID", "GT", "IC", "GT", "OV", "BA"],
                TransactionType.skip: [],
            },
        )
        get_payee_narration = payee_narration.FromNarration(
            narration_key=r"Name / Description",
            max_narration_length=40,
        )
        get_amount = amount.FromSignAmountWithCurrency(
            sign_key=r"Debit/credit",
            amount_key="Amount (EUR)",
            currency=Currency.EUR,
        )
        get_balance = amount.FromAmountWithCurrency(
            amount_key="Resulting balance",
            currency=Currency.EUR,
        )
        BankingImporter.__init__(
            self,
            root_account=root_account,
            fee_account=None,
            get_date=get_date,
            get_payee_narration=get_payee_narration,
            get_transaction_type=get_transaction_type,
            get_root_amount=get_amount,
            get_fee_amount=None,
            get_balance=get_balance,
            file_description=file_description,
        )


class INGSavingsImporter(BankingImporter):
    
    def __init__(
        self,
        root_account: str,
        root_account_id: str,
    ):

        file_description = file.FileDescriptionCSV(
            file_extension = ".csv",
            file_pattern_regex = rf"^{root_account_id}_(?P<date>\d{{2}}-\d{{2}}-\d{{4}})_\d{{2}}-\d{{2}}-\d{{4}}\.csv$",
            file_date_format = "%d-%m-%Y",
            file_delimiter = ";",
            file_header = ("Datum", "Omschrijving", "Rekening", "Rekening naam", "Tegenrekening", "Af Bij", "Bedrag", "Valuta", "Mutatiesoort", "Mededelingen", "Saldo na mutatie"),
            entry_mapping=None,
            start_date = None,
            end_date = None,
        )
        get_date = date.FromDate(
            date="Datum",
            date_format="%Y-%m-%d",
        )
        get_transaction_type = transaction_type.FromTransactionType(
            transaction_type_key="Mutatiesoort",
            transaction_type_mapping={
                TransactionType.exchange: [],
                TransactionType.transfer: ["Inleg"],
                TransactionType.skip: [],
            },
        )
        get_payee_narration = payee_narration.FromPayeeNarration(
            payee_key=r"Tegenrekening",
            max_payee_length=20,
            narration_key=r"Mededelingen",
            max_narration_length=40,
        )
        get_amount = amount.FromSignAmountWithCurrency(
            sign_key=r"Af Bij",
            amount_key="Bedrag",
            currency=Currency.EUR,
        )
        get_balance = amount.FromAmountWithCurrency(
            amount_key="Saldo na mutatie",
            currency=Currency.EUR,
        )
        BankingImporter.__init__(
            self,
            root_account=root_account,
            fee_account=None,
            get_date=get_date,
            get_payee_narration=get_payee_narration,
            get_transaction_type=get_transaction_type,
            get_root_amount=get_amount,
            get_fee_amount=None,
            get_balance=get_balance,
            file_description=file_description,
        )

if __name__ == "__main__":
    main = beangulp.Ingest([
        INGSavingsImporter(
            root_account="Assets:NL:ING:Current",
            root_account_id="",
        ),
    ])
    main()