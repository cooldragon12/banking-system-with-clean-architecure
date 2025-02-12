from typing import Type
from datetime import datetime
from src.core.entities.transaction import TransactionType
from src.core.entities.transaction import Transaction
from src.core.base import BaseUseCase
from src.infrastructure.repositories.transaction import (
    TransactionRepository
    )
from src.infrastructure.repositories.account import (
    AccountRepository
    )
class MakeTransactionUseCase(BaseUseCase[Transaction]):
    def __init__(
            self,
            account_repository: Type[AccountRepository], 
            transaction_repository: Type[TransactionRepository], 
            sender,
            amount,
            transaction_type: Type[TransactionType], 
            receiver=None 
        ):
        self.sender = sender
        self.receiver = receiver
        self.transaction_repository = transaction_repository
        self.account_repository = account_repository
        self.transaction_type = transaction_type
        self.amount = amount
    
    def make_transaction(self,  amount, transaction_id):
        """
        Make a transaction
        """
        if self.transaction_type == TransactionType.TRANSFER_SEND or self.transaction_type == TransactionType.TRANSFER_RECEIVE:
            return self.transfer_transaction(amount, transaction_id)
        
        elif self.transaction_type == TransactionType.WITHDRAWAL:
            return self.withdraw_transaction(amount, transaction_id)
        
        elif self.transaction_type == TransactionType.DEPOSIT:
            return self.deposit_transaction(amount, transaction_id)
        return None
    
    def transfer_transaction(self, amount, transaction_id):
        send_transaction = Transaction(transaction_id, self.sender, amount, TransactionType.TRANSFER_SEND, date=datetime.now())
        receive_transaction = Transaction(transaction_id, self.receiver, amount, TransactionType.TRANSFER_RECEIVE,date=datetime.now())
        # Persist the transaction
        entity_transaction = self.transaction_repository.save(send_transaction)
        self.transaction_repository.save(receive_transaction) # Receiver transaction


        # Update the account balance
        sender_account = self.account_repository.find_account_by_id(self.sender)
        receiver_account = self.account_repository.find_account_by_id(self.receiver)
        sender_account.transfer(amount,sender_account, receiver_account)


        return entity_transaction
    
    def withdraw_transaction(self, amount,transaction_id):
        send_transaction = Transaction(transaction_id, self.sender, amount, TransactionType.WITHDRAWAL, date=datetime.now())
        entity_transaction = self.transaction_repository.save(send_transaction)

        # Update the account balance
        account = self.account_repository.find_account_by_id(self.sender)
        account.withdraw(amount)
        return entity_transaction

    def deposit_transaction(self, amount,transaction_id):
        receive_transaction = Transaction(transaction_id,self.sender, amount, TransactionType.DEPOSIT, date=datetime.now())
        entity_transaction = self.transaction_repository.save(receive_transaction)

        # Update the account balance
        account = self.account_repository.find_account_by_id(self.sender)
        account.deposit(amount)

        return entity_transaction
    
    ## Validate the transaction
    def validate_amount(self, amount):
        if self.transaction_type == TransactionType.WITHDRAWAL or self.transaction_type == TransactionType.TRANSFER_SEND:
            if amount > self.account_repository.find_account_by_id(self.sender).balance:
                raise ValueError("Insufficient balance")

        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        return amount
    
    def validate(self, amount):
        sender_exist = self.account_repository.find_account_by_id(self.sender)
        if sender_exist is None:
            raise ValueError("Account does not exist")

        if self.transaction_type == TransactionType.TRANSFER_SEND:
            receiver_exist = self.account_repository.find_account_by_id(self.receiver)
            if receiver_exist is None:
                raise ValueError("Receiver account does not exist")

    # Generate transaction id
    def generate_id(self):
        return str(len(self.transaction_repository._data) + 1)

    # Execute the transaction
    def execute(self):
        try:
            self.execute_validation(self.amount)
            transaction = self.make_transaction(self.amount, self.generate_id())
            return "Transaction Successful" if transaction.id else "Transaction Failed" 
        except ValueError as e:
            return str(e)
