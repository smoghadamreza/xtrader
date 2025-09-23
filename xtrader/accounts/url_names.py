from accounts.apps import AccountsConfig

class URLMeta(type):
    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if not name.startswith("__") and isinstance(value, str):
            return AccountsConfig.name + ":" + value
        return value

class AccountsURLS(metaclass=URLMeta):
    APP_NAME = AccountsConfig.name

    # 🔑 Authentication
    SIGN_UP = "userena-sign-up"
    SIGN_IN = "userena-sign-in"
    SIGN_OUT = "userena-sign-out"
    EMAIL_CONFIRM = "userena-email-confirm"
    ACTIVATE = "userena-activate"
    ACTIVATE_RETRY = "userena-retry-activation"
    ACTIVATE_PENDING = "userena-activation-pending"

    # 🔑 Password management
    PASSWORD_RESET = "userena-password-reset"
    PASSWORD_RESET_CONFIRM = "userena-password-reset-confirm"
    PASSWORD_RESET_DONE = "userena-password-reset-done"
    PASSWORD_RESET_COMPLETED = "userena-password-reset-completed"

    # 🔑 Email & signup completion
    EMAIL_CHANGE = "userena-email-change"
    SIGNUP_COMPLETED = "userena-sign-up-completed"
    EMAIL_CHANGE_COMPLETED = "userena-email-change-completed"
    EMAIL_CHANGE_VERIFICATION_NEEDED = "userena-email-change-verification-needed"

    # 🔑 Account state
    ACCOUNT_DISABLED = "userena-account-disabled"
    PROFILE_EDIT = "userena-profile-edit"
    PROFILE_DETAIL = "userena-profile-detail"
    PROFILE_LIST = "userena-profile-list"

    # 🔑 Wallet endpoints
    GET_DEPOSITS = "get-deposits"
    SYNC_DEPOSITS = "sync-deposits"
    NEW_DEPOSIT = "new-deposit"
    GET_WALLET = "get-wallet"

    # 🔑 Status endpoints
    TELEGRAM_STATUS = "telegram-status"
    ACCOUNT_STATUS = "account-status"
