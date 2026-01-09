class TemplatesMeta(type):
    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if not name.startswith('__') and isinstance(value, str):
            return value + ".html"
        return value

class TemplateFiles(metaclass=TemplatesMeta):
    ERROR = "error"

    # Userena Templates
    USERENA_BASE = "userena/"
    USERENA_SIGNUP = USERENA_BASE + "signup"
    USERENA_SIGNUP_FORM = USERENA_BASE + "signup_form"
    USERENA_SIGNIN_FORM = USERENA_BASE + "signin_form"
    USERENA_ACTIVATION_PENDING = USERENA_BASE + "activation_pending"
    USERENA_ACTIVATION_FAILED = USERENA_BASE + "activation_failed"
    USERENA_ACTIVATION_RETRY_SUCCESS = USERENA_BASE + "activation_retry_success"
    USERENA_ACCOUNT_DISABLED = USERENA_BASE + "account_disabled"
    USERENA_ACTIVATION_LINK_EXPIRED = USERENA_BASE + "activation_link_expired"
    USERENA_SIGNUP_COMPLETED = USERENA_BASE + "signup_completed"
    USERENA_SIGNOUT = USERENA_BASE + "signout"
    USERENA_BASE_USERENA = USERENA_BASE + "base_userena"

    # Userena Email Templates
    USERENA_EMAIL_CHANGE_FORM = USERENA_BASE + "email_change_form"
    USERENA_EMAIL_CHANGE_VERIFICATION = USERENA_BASE + "email_change_verification"
    USERENA_EMAIL_CHANGE_FAILED = USERENA_BASE + "email_change_failed"
    USERENA_EMAIL_CHANGE_COMPLETED = USERENA_BASE + "email_change_completed"

    # Userena Password Templates
    USERENA_PASSWORD_CHANGE_COMPLETED = USERENA_BASE + "password_change_completed"
    USERENA_PASSWORD_CHANGE_CONFIRMATION_FORM = USERENA_BASE + "password_change_confirmation_form"
    USERENA_PASSWORD_CHANGE_FORM = USERENA_BASE + "password_change_form"
    USERENA_PASSWORD_CHANGE_VERIFICATION = USERENA_BASE + "password_change_verification"
    USERENA_FORGOT_PASSWORD_FORM = USERENA_BASE + "forgot_password_form"

    # Userena Profile Templates
    USERENA_PROFILE_DETAIL = USERENA_BASE + "profile_detail"
    USERENA_PROFILE_FORM = USERENA_BASE + "profile_form"
    USERENA_PROFILE_LIST = USERENA_BASE + "profile_list"

    # Admin Templates
    ADMIN_BASE = "admin/"
    ADMIN_INDEX = ADMIN_BASE + "index"

    # Admin Data Templates
    ADMIN_DATA_BASE = ADMIN_BASE + "data/"
    ADMIN_DATA_STOCKWATCH = ADMIN_DATA_BASE + "stockwatch"

    # Base Template
    BASE = "base"


class TextTemplates(TemplateFiles):
    """
    Manages plain text template file paths.
    
    This class inherits from TemplateFiles but overrides the
    __getattribute__ method to handle .txt file extensions.
    """
    # Userena Email Text Files
    EMAILS_BASE = TemplateFiles.USERENA_BASE + "emails/"
    USERENA_EMAIL_ACTIVATION_MESSAGE_TXT = "activation_email_message"
    USERENA_EMAIL_ACTIVATION_SUBJECT_TXT = "activation_email_subject"
    USERENA_EMAIL_CONFIRMATION_MESSAGE_NEW_TXT = "confirmation_email_message_new"
    USERENA_EMAIL_CONFIRMATION_MESSAGE_OLD_TXT = "confirmation_email_message_old"
    USERENA_EMAIL_CONFIRMATION_SUBJECT_NEW_TXT = "confirmation_email_subject_new"
    USERENA_EMAIL_CONFIRMATION_SUBJECT_OLD_TXT = "confirmation_email_subject_old"
    USERENA_EMAIL_PASSWORD_CHANGE_MESSAGE_TXT = "password_change_message"

    def __getattribute__(self, name):
        """
        Overrides the parent method to append '.txt' to string attributes.
        """
        value = super(TemplateFiles, self).__getattribute__(name)
        if not name.startswith('__') and isinstance(value, str):
            return value + ".txt"
        return value
