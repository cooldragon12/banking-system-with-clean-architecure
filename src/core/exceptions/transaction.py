
class InsufficientFundsError(Exception):
    pass

class InvalidTransactionError(Exception):
    pass

class InvalidTransactionAmountError(Exception):
    pass

class ExceedsDailyLimitError(Exception):
    pass