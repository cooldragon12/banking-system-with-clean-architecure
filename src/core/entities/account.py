# This file contains the Account class which is a dataclass that represents an account entity.
from dataclasses import dataclass
from src.core.entities.customer import Customer


@dataclass
class Account:
    customer_id: str | Customer
    account_number: str
    balance: float

    def deposit(self, amount: float):
        self.balance += amount
    
    def withdraw(self, amount: float):
        self.balance -= amount

    @classmethod
    def transfer(cls, amount:float, from_account:'Account', target_account:'Account'):
        from_account.balance -= amount
        target_account.balance += amount
        return from_account, target_account # Amount transferred


    def __str__(self):
        return self.account_number