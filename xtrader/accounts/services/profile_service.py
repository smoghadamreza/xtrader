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
from accounts.services.exceptions import NoProfileFoundForUser

from utils.unix_millis import UnixMillis


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
    def _generate_code(cls, code_length: int = 6) -> str:
        char_set = (
            string.ascii_lowercase + string.ascii_uppercase + string.digits
        )
        return ''.join(random.choice(char_set) for _ in range(code_length))
    
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

    def get_telegram_activation_code(self) -> str:
        if self.has_telegram_id():
            return ""
        if self._is_profile_telegram_activation_code_invalid():
            self._generate_telegram_activation_code()
        return cast(str, self._profile.telegram_activation_code)
    
    def has_telegram_id(self) -> bool:
        return bool(self._profile.telegram_id)

    def _generate_telegram_activation_code(self) -> None:
        activation_code = self._generate_code()
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