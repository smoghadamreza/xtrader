# accounts/services/user_activation_service.py
from userena.models import UserenaSignup
from userena import settings as userena_settings
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.translation import gettext as _
from typing import Tuple, Optional
from django.contrib.auth.models import User

class UserActivationService:
    @staticmethod
    def activate_user(activation_key: str, request) -> Tuple[Optional[User], Optional[str]]:
        """
        Activate a user with an activation key.
        
        Returns:
            Tuple of (user, error_message) where error_message is None if successful
        """
        try:
            if (not UserenaSignup.objects.check_expired_activation(activation_key) or
                not userena_settings.USERENA_ACTIVATION_RETRY):
                
                user = UserenaSignup.objects.activate_user(activation_key)
                if user:
                    # Sign the user in.
                    auth_user = authenticate(
                        identification=user.email, 
                        check_password=False
                    )
                    login(request, auth_user)

                    if userena_settings.USERENA_USE_MESSAGES:
                        messages.success(
                            request,
                            _("Your account has been activated and you have been signed in."),
                            fail_silently=True,
                        )
                    return user, None
                else:
                    return None, "invalid link"
            else:
                return None, "link expired, you should retry"
        except UserenaSignup.DoesNotExist:
            return None, "activation failed"
    
    @staticmethod
    def reissue_activation(activation_key: str) -> Optional[str]:
        """
        Reissue a new activation key for expired keys.
        
        Returns:
            New activation key if successful, None otherwise
        """
        if not userena_settings.USERENA_ACTIVATION_RETRY:
            return None
            
        try:
            if UserenaSignup.objects.check_expired_activation(activation_key):
                new_key = UserenaSignup.objects.reissue_activation(activation_key)
                return new_key
        except UserenaSignup.DoesNotExist:
            pass
            
        return None