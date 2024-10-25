from enum import Enum

class Currency(Enum):
    """
    An enumeration representing various currencies, defined by their official ISO codes.

    Attributes:
        CHF (str): Swiss Franc.
        EUR (str): Euro.
        SEK (str): Swedish Krona.
        USD (str): US Dollar.
        GBP (str): British Pound.
        JPY (str): Japanese Yen (commented out).
        AUD (str): Australian Dollar (commented out).
        CAD (str): Canadian Dollar (commented out).
        NZD (str): New Zealand Dollar (commented out).
        BTC (str): Bitcoin (commented out).
        ETH (str): Ethereum (commented out).
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
    An enumeration representing different types of transactions.

    Attributes:
        transfer (str): A transfer transaction.
        exchange (str): An exchange transaction.
        skip (str): A transaction to skip.
    """
    transfer = "transfer"  # A transfer transaction
    exchange = "exchange"  # An exchange transaction
    skip = "skip"          # A transaction to skip
