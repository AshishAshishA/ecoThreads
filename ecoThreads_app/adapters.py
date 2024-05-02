from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        # Allow sign up without email verification for all social accounts
        return True

    def get_providers(self):
        providers = []
        for app in SocialApp.objects.all():
            providers.append({
                'id': app.id,
                'name': app.name,
                'provider': app.provider,
            })
        return providers
