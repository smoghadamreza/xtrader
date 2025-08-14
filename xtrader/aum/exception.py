class FundNotFound(Exception):
    pass

class FundInvestorNotFound(Exception):
    pass

class InvalidAction(Exception):
    pass

class InsufficientDepositInFund(Exception):
    pass

class InsufficientUnitsFromInvestor(Exception):
    pass

class NameIsTooLong(ValueError):
    pass

class InvestorAlreadyExists(Exception):
    pass

class NoSnapshotFound(Exception):
    pass
