from utils.templates import TemplateFiles

class AccountsTemplates(TemplateFiles):
    """
    Manages template paths for the 'accounts' app.
    """
    BASE = "accounts/"
    LANDING = BASE + "landing"
    MAIL_TEMPLATE = BASE + "mail_template"
    SETTINGS = BASE + "settings"
    USER_INFO = BASE + "user_info"
