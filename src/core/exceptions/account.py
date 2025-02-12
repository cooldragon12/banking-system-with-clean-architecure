

class InvalidAccountError(Exception):
    """Raised when the account is invalid or does not exist"""
    pass


class AccountAlreadyExistsError(Exception):
    """Raised when the account already exists"""
    pass
    