from src.core.base import BaseRepository
from src.core.entities.transaction import Transaction

class TransactionRepository(BaseRepository[Transaction]):
    entity = Transaction
    
    def list_by_account(self, account_id:str):
        return [transaction for transaction in self._data if transaction.account_id == account_id]
    