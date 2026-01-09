class ResponseMessages:
    FUND_NOT_FOUND = "شما مدیر هیچ صندوقی برای سرمایه‌گذاری نیستید."
    FUND_INVESTOR_INVALID_ID = "شناسه سرمایه‌گذار اشتباه است."
    INVALID_ACTION = "عملیات مشخص نشده یا نادرست است."
    INSUFFICIENT_DEPOSIT_IN_FUND = "موجودی واریزی صندوق کافی نیست."
    INSUFFICIENT_UNITS_FROM_INVESTOR = "سرمایه‌گذار واحد‌های کمتری دارد."

    NOT_AUTHORIZED = "شما مجاز به انجام این عملیات نیستید."
    CREATED = "ساخته شد."
    ALREADY_EXISTS = "این مورد قبلا ساخته شده است."
    
    NAME_IS_TOO_LONG = "اسم و یا فامیلی شما بیش از حد طولانی است. هر کدام می‌تواند حداکثر ۲۰ حرف داشته باشد."



class ResponseData:
    CREATED = "created"
    ALREADY_EXISTS = "already exists"
