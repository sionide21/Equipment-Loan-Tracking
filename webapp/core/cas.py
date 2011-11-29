from django_cas.backends import CASBackend
from models import Whitelist


class WhitelistCASBackend(CASBackend):
    """CAS authentication backend that verifies users against whitelist"""
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, ticket, service):
        user = super(WhitelistCASBackend, self).authenticate(ticket, service)
        if not user:
            return None

        if Whitelist.objects.filter(username=user.username) or user.is_superuser:
            return user
        return None
