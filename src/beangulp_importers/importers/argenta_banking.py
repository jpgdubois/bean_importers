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


class ArgentaImporter(BankingImporter):

    def __init__(
        self,
        root_account: str,
        root_account_id: str,
    ):
        file_description = file.FileDescriptionXLSX(
            file_extension = ".xlsx",
            file_pattern_regex = rf"^Argenta_({root_account_id})_(?P<date>\d{{4}}-\d{{2}}-\d{{2}})_\d{{6}}\.xlsx$",
            file_date_format = "%Y-%m-%d",
            file_header = ("Rekening", "Boekdatum", "Valutadatum", "Referentie", "Beschrijving", "Bedrag", "Munt", "Verrichtingsdatum", "Rekening tegenpartij", "Naam tegenpartij", "Mededeling"),
            entry_mapping=None,
            start_date = None,
            end_date = None,
        )
        get_date = date.FromPostingTransactionDate(
            posting_date="Boekdatum",
            transaction_date="Valutadatum",
            date_format="%d-%m-%Y",
        )
        get_transaction_type = transaction_type.FromTransactionType(
            transaction_type_key="Beschrijving",
            transaction_type_mapping={
                TransactionType.transfer: ["Diverse verrichting", "Inkomende overschrijving", "Betaling bancontact"],
                TransactionType.skip: [],
            },
        )
        get_payee_narration = payee_narration.FromPayeeNarration(
            payee_key="Naam tegenpartij",
            max_payee_length=20,
            narration_key="Mededeling",
            max_narration_length=40,
        )
        get_amount = amount.FromAmount(
            amount_key="Bedrag",
            currency_key="Munt",
        )

        BankingImporter.__init__(
            self,
            root_account=root_account,
            get_date=get_date,
            get_payee_narration=get_payee_narration,
            get_transaction_type=get_transaction_type,
            get_root_amount=get_amount,
            file_description=file_description,
        )    


if __name__ == "__main__":
    main = beangulp.Ingest([ArgentaImporter(
        root_account="Assets:BE:Argenta",
        root_account_id="BE00000000000000",
    ),
    ])
    main()