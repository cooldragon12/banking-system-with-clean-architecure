

from src.core.use_cases.account import AccountCreation
from src.core.use_cases.transaction import MakeTransactionUseCase

from src.infrastructure.repositories.account import AccountRepository
from src.infrastructure.repositories.transaction import TransactionRepository

from src.core.entities.transaction import TransactionType

def test_transactions():
    account_repo = AccountRepository()
    transaction_repo = TransactionRepository()

    account1 = AccountCreation(
        account_repo, 
        customer_id='231saa',
        name='John Doe', 
        email='johndoe@example.com',
        phone_number='08012345678',
        account_number='23122321111', 
        balance=500.0
    ) # 500

    account2 = AccountCreation(
        account_repo, 
        customer_id='231saa',
        name='Jane Doe',
        email='janedow@example.com',
        phone_number='08012345678',
        account_number='23122321112', balance = 1000.0
    )# 1000
    
    account3 = AccountCreation(
        account_repo, 
        customer_id='231saa',
        name='Jane Doe',
        email="john@example.com",
        phone_number='08012345678',
        account_number='23122321113', balance=0.0
    ) # 0


    get_account1 = account_repo.find_account_by_id(account1.entity.account_number)
    get_account2 = account_repo.find_account_by_id(account2.entity.account_number)
    get_account3 = account_repo.find_account_by_id(account3.entity.account_number)
    
    # Making a transaction

    result1 = MakeTransactionUseCase(
        account_repo,
        transaction_repo,
        get_account1.account_number,
        200,
        TransactionType.TRANSFER_SEND,
        get_account2.account_number
    ).execute()

    # Checks if the transaction was successful , for sending money
    assert result1 == "Transaction Successful" 
    assert get_account1.balance == 300
    assert get_account2.balance == 1200

    # Transaction 2
    result2 = MakeTransactionUseCase(
        account_repo,
        transaction_repo,
        get_account2.account_number,
        300.0,
        TransactionType.WITHDRAWAL
    ).execute()
    
    # Checks if the transaction was successful, for withdrawal
    assert result2 == "Transaction Successful" 
    assert get_account2.balance == 900

    # Transaction 3
    result3 = MakeTransactionUseCase(
        account_repo,
        transaction_repo,
        get_account3.account_number,
        100.0,
        TransactionType.DEPOSIT
    ).execute()
    
    # Checks if the transaction was successful, for deposit
    assert result3 == "Transaction Successful" 
    assert get_account3.balance == 100


    # Failed Transactions Test

    result4 = MakeTransactionUseCase(
        account_repo,
        transaction_repo,
        get_account1.account_number,
        1000,
        TransactionType.TRANSFER_SEND,
        get_account3.account_number
    ).execute()

    # Checks if the transaction was not successful, for sending money
    assert result4 == "Insufficient balance"
    assert get_account1.balance == 300 # Check if the transaction persisted

    result5 = MakeTransactionUseCase(
        account_repo,
        transaction_repo,
        get_account2.account_number,
        1000,
        TransactionType.WITHDRAWAL
    ).execute()

    # Checks if the transaction was not successful, for withdrawal
    assert result5 == "Insufficient balance"
    assert get_account2.balance == 900 # Check if the transaction persisted

    result6 = MakeTransactionUseCase(
        account_repo,
        transaction_repo,
        '23122321117',
        amount=1000,
        transaction_type=TransactionType.DEPOSIT
    ).execute()

    # Checks if the transaction was not successful, for deposit
    assert result6 == "Account does not exist"

    

