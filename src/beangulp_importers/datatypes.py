from enum import Enum

class Currency(Enum):
    """
    An Enum representing various currencies, where each currency is defined
    by its official ISO code.
    """
    CHF = "CHF"  # Swiss Franc
    EUR = "EUR"  # Euro
    SEK = "SEK"  # Swedish Krona
    USD = "USD"  # US Dollar
    GBP = "GBP"  # British Pound
    # JPY = "JPY"  # Japanese Yen
    # AUD = "AUD"  # Australian Dollar
    # CAD = "CAD"  # Canadian Dollar
    # NZD = "NZD"  # New Zealand Dollar
    # BTC = "BTC"  # Bitcoin
    # ETH = "ETH"  # Ethereum


class TransactionType(Enum):
    """
    Enum representing different types of transactions.

    Attributes:
        transfer: A transfer transaction.
        exchange: An exchange transaction.
    """
    transfer = "transfer"
    exchange = "exchange"
    skip = "skip"