from src.core.entities.transaction import TransactionType

from src.core.use_cases.account import AccountCreation
from src.core.use_cases.transaction import MakeTransactionUseCase
from src.core.use_cases.account import GenerateAccountStatementUseCase

from src.infrastructure.repositories.account import AccountRepository
from src.infrastructure.repositories.transaction import TransactionRepository


def test_account_statement():
    account_repo = AccountRepository()
    transaction_repo = TransactionRepository()
    account1 = AccountCreation(
        account_repo, 
        customer_id='231saa',
        name='John Doe', 
        email='johndoe@example.com',
        phone_number='08012345678',
        account_number='23122321111', 
        balance=1000
    )

    account2 = AccountCreation(
        account_repo, 
        customer_id='231saa',
        name='Jane Doe',
        email='janedow@example.com',
        phone_number='08012345678',
        account_number='23122321112', balance=1000
    )

    get_account1 = account_repo.find_account_by_id(account1.entity.account_number)
    get_account2 = account_repo.find_account_by_id(account2.entity.account_number)

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
    assert get_account1.balance == 800
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
        get_account2.account_number,
        100.0,
        TransactionType.DEPOSIT
    ).execute()


    # gENERATE ACCOUNT STATEMENT
    GenerateAccountStatementUseCase(get_account1.account_number, account_repo, transaction_repo).execute()
    GenerateAccountStatementUseCase(get_account2.account_number, account_repo, transaction_repo).execute()
