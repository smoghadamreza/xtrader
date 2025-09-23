from datetime import timedelta
import random
import string
from typing import cast, List, Tuple

from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from userena.utils import get_user_profile
from accounts.models import Profile
from accounts.exceptions import NoProfileFoundForUser

from utils.consts import TelegramMessage, XtraderRequestValues
from utils.unix_millis import UnixMillis
from utils.misc import generate_secure_token


class ProfileService:

    def __init__(self, user: User) -> None:
        try:
            self._profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise NoProfileFoundForUser()

    @property
    def profile(self) -> Profile:
        return self._profile
    
    @classmethod
    def get_user_and_profile(cls, username: str) -> Tuple[User, Profile]:
        """Helper method to fetch user and their profile."""
        user = get_object_or_404(
            klass=get_user_model(), 
            username__iexact=username
        )
        user = cast(User, user)
        profile = cast(Profile, get_user_profile(user=user))
        return user, profile

    @staticmethod
    def connect_via_telegram(user_id: int, activation_code: str) -> str:
        """
        Handle Telegram activation logic for a user.
        Returns the reply message to be sent back.
        """
        # Default guide
        reply = TelegramMessage.ACCOUNT_CONNECTION_GUIDE

        # /start just returns guide
        if activation_code == XtraderRequestValues.START:
            return reply

        try:
            profile = Profile.objects.get(telegram_activation_code=activation_code)
            now_timestamp = UnixMillis.from_datetime_to_timestamp(timezone.now())
            activation_code_valid = (
                profile.telegram_activation_timestamp and
                now_timestamp < profile.telegram_activation_timestamp
            )
            if activation_code_valid:
                return TelegramMessage.ACCOUNT_CONNECTED
            return TelegramMessage.EXPIRED_ACTIVATION_CODE
        except Profile.DoesNotExist:
            pass

        try:
            profile = Profile.objects.get(telegram_id=str(user_id))
            return TelegramMessage.ACCOUNT_IS_ALREADY_CONNECTED
        except Profile.DoesNotExist:
            return TelegramMessage.INVALID_ACTIVATION_CODE


    def get_telegram_activation_code(self) -> str:
        if self.has_telegram_id():
            return ""
        if self._is_profile_telegram_activation_code_invalid():
            self._generate_telegram_activation_code()
        return cast(str, self._profile.telegram_activation_code)
    
    def has_telegram_id(self) -> bool:
        return bool(self._profile.telegram_id)

    def _generate_telegram_activation_code(self) -> None:
        activation_code = generate_secure_token()
        self._profile.telegram_activation_code = activation_code
        self._profile.telegram_activation_timestamp = UnixMillis.from_dt_to_ms(
            dt=timezone.now() + timedelta(minutes=5)
        )
        self._profile.save(
            update_fields=[
                "telegram_activation_code", "telegram_activation_timestamp"
            ]
        )

    def _is_profile_telegram_activation_code_invalid(self) -> bool:
        now_timestamp = cast(int, UnixMillis.from_dt_to_ms(dt=timezone.now()))
        valid_activation_code_condition = bool(
            self._profile.telegram_activation_code and 
            self._profile.telegram_activation_timestamp and 
            self._profile.telegram_activation_timestamp > now_timestamp
        )
        return not valid_activation_code_condition
    
    @classmethod
    def _get_all_valid_emails(cls) -> List[str]:
        return list(
        Profile.objects
        .filter(user__is_active=True)
        .exclude(user__email="")
        .values_list("user__email", flat=True)
    )