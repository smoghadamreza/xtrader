from accounts.apps import AccountsConfig

class AccountsURLS:
    APP_NAME = AccountsConfig.name

    SIGNUP_COMPLETED = "userena-sign-up-completed"
    EMAIL_CHANGE_COMPLETED = "userena-email-change-completed"
    ACCOUNT_DISABLED = "userena-account-disabled"
    ACCOUNT_ACTIVATION_PENDING = "userena-activation-pending"


    def __getattribute__(self, name):
        """
        Overrides the parent method to append '.txt' to string attributes.
        """
        value = super(AccountsURLS, self).__getattribute__(name)
        if not name.startswith('__') and isinstance(value, str):
            return self.APP_NAME + ":" + value
        return value 