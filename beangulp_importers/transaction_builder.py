from beancount.core.amount import Amount
from beancount.core import data, flags

def transfer(
    date: str,
    payee: str,
    narration: str,
    account: str,
    amount: Amount,
    fee_amount: Amount,
    fee_account: str,

):
    postings = []
    postings.append(
        data.Posting(
            account=account,
            units=amount,
            cost=None,
            price=None,
            flag=None,
            meta=None,
        )
    )
    postings.append(
        data.Posting(
            account=fee_account,
            units=fee_amount,
            cost=None,
            price=None,
            flag=None,
            meta=None,
        )
    )

    txn = data.Transaction(
        meta=None,
        date=date,
        flag=flags.FLAG_OKAY,
        payee=payee,
        narration=narration,
        tags=None,
        links=None,
        postings=postings,
    )
    return txn

