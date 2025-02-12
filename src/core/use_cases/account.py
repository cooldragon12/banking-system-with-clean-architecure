from typing import Type
from src.core.base import BaseUseCase, BaseRepository
from src.core.entities.account import Account
from src.core.entities.customer import Customer
from src.core.entities.transaction import Transaction

from src.infrastructure.repositories.account import AccountRepository
from src.infrastructure.repositories.transaction import TransactionRepository

class AccountCreation(BaseUseCase[Account]):

    def __init__(
            self,
            repository1: BaseRepository[Account],
            **kwargs
            ):
        self.repository = repository1
        self.execute_validation(kwargs)
        customer = self.create_customer(kwargs.get('customer_id', ''), kwargs.get('name', ''), kwargs.get('email', ''), kwargs.get('phone_number', ''))
        account = self.create_account(customer, kwargs.get('account_number', ''),kwargs.get('balance', 0.0))
        self.entity = account

    def create_customer(self, customer_id:str, name:str, email:str, phone_number:str) -> Customer:
        customer = Customer(customer_id, name, email, phone_number)
        return customer
    

    def create_account(self, customer_id:str, account_number:str, balance:float) -> Account:
        account = Account(customer_id, account_number, balance)
        entity_account = self.repository.save(account)
        return entity_account
    
    def validate(self, value):
        customer = value.get('customer_id')
        account_number = value.get('account_number')
         
        if not customer:
            raise ValueError("Customer is required")
        
        if not account_number:
            raise ValueError("Account is required")
        return value

class GenerateAccountStatementUseCase(BaseUseCase[Account]):
    
    def __init__(self, account_id, account_repo:Type[AccountRepository],transaction_repo: Type[TransactionRepository]):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo
        self.entity = self.account_repo.find_account_by_id(account_id)

    def print_account_details(self):
        import datetime
        print("""
==============================================================================
  Account Number: {}                Date issued: {}
  Account Balance: {}
    
  Customer Name: {}    
------------------------------------------------------------------------------
    
              """.format(
                  self.entity.account_number, 
                  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                  self.entity.balance, 
                  self.entity.customer_id.name,
                  ))
    
    def generate_account_statement(self, account_id:str):
        transactions =self.transaction_repo.list_by_account(account_id)
        print("""
------------------------------------------------------------------------------
Transaction ID     | Transaction Type  | Amount      | Date
------------------------------------------------------------------------------""")
        for transaction in transactions:
            length = len(transaction.transaction_type)
            if length < 16:
                type = transaction.transaction_type + ' ' * (16 - length)
            else:
                type = transaction.transaction_type
            print("""{}                  | {}   | {}        | {}""".format(
    transaction.id,
    type,
    transaction.amount,
    transaction.date.strftime("%Y-%m-%d %H:%M:%S")
    ))
    
    def end_statement(self):
        print("""
=============================================================================
    End of Statement
=============================================================================
              
                """)
    def execute(self):
        self.print_account_details()
        self.generate_account_statement(self.entity.account_number)
        self.end_statement()
