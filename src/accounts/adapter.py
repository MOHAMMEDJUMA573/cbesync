from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        REDIRECT_MAP = {
            "school": "schools:school_app_dashboard",
            "sysadmin": "admin:index",
        }
        user = request.user
        redirect_url = REDIRECT_MAP.get(user.user_type)
        if redirect_url:
            return reverse(redirect_url)

        return super().get_login_redirect_url(request)
