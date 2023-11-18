# adapters.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.state.get('process') == 'login':
            # Set the process parameter to 'login' for pop-up
            sociallogin.state['process'] = 'login'
