class Symbol:
    USDT = "USDT"

class XtraderRequestKeys:
    # used in aum.views.issue_redeem_unit
    INVESTOR_ID = "investor_id"
    ACTION = "action"
    AMOUNT = "amount" 

class XtraderRequestValues:
    # used in finance.copy_trade
    NEW = "NEW"
    CANCEL = "CANCELED"

    # used in aum.FundService.issue_redeem_unit
    ISSUE = "issue"
    REDEEM = "redeem"

class XtraderResponseKeys:
    C = "c"  # TODO: I think this supposed to be status code.
    MESSAGE = "msg"


