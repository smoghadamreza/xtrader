from django.contrib.auth.models import User
from social.models import Follow
from finance.models import Exchange
from accounts.models import Profile
from typing import Dict

class AccountStatusService:
    @staticmethod
    def get_profile_status(user: User) -> Dict[str, bool|str]:
        status = {
            'following': False,
            'exchange': False,
            'telegram': False,
        }
        
        following = Follow.objects.filter(follower=user).first()
        if following:
            status['following'] = True
            status['pro_trader'] = following.pro_trader.brand
            
        if Exchange.objects.filter(trader=user).exists():
            status['exchange'] = True
            
        profile = Profile.objects.filter(user=user).first()
        if profile and profile.telegram_id:
            status['telegram'] = True
            
        return status
