from src.core.use_cases.account import AccountCreation

from src.infrastructure.repositories.account import AccountRepository

def test_creation_account():
    account_repo = AccountRepository()
    account1 = AccountCreation(
        account_repo, 

        customer_id='231saa',
        name='John Doe', 
        email='johndoe@example.com',
        phone_number='08012345678',
        account_number='23122321110', 
        balance=0.0
    )
    account2 = AccountCreation(
        account_repo, 
        customer_id='231saa',
        name='Jane Doe',
        email='janedow@example.com',
        phone_number='08012345678',
        account_number='23122321122', balance=0.0
    )

    get_account1 = account_repo.find_account_by_id(account1.entity.account_number)
    get_account2 = account_repo.find_account_by_id(account2.entity.account_number)
    
    assert get_account1 == account1.entity
    assert get_account2 == account2.entity
    assert get_account1 != get_account2
    assert account1.entity != account2.entity