from dataclasses import dataclass
from typing import Type

from src.core.entities.account import Account

class TransactionType:
    DEPOSIT = 'DEPOSIT'
    WITHDRAWAL = 'WITHDRAWAL'
    TRANSFER_SEND = 'TRANSFER_SEND'
    TRANSFER_RECEIVE = 'TRANSFER_RECEIVE'

@dataclass
class Transaction:
    id: str
    account_id:  str | Account
    amount: float
    transaction_type: Type[TransactionType]
    date: str = None