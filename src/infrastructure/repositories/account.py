from src.core.base import BaseRepository
from src.core.entities.account import Account

class AccountRepository(BaseRepository[Account]):
    entity = Account
    
    def save_account(self, account: Account):
        self.save(account)
        return account
    
    def find_account_by_id(self, account_id: str):
        return self.find(account_id, by='account_number')

    def find_account_by_customer_id(self, customer_id: str):
        return self.find(customer_id, by='customer_id')
    
 
