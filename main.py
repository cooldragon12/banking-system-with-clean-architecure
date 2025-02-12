"""Test the main module."""

from tests.test_account_creation import test_creation_account
from tests.test_transaction_types import test_transactions
from tests.test_account_statement import test_account_statement

def test_main():
    test_creation_account()
    test_transactions()
    test_account_statement()
    print("Test passed")




if __name__ == "__main__":
    test_main()