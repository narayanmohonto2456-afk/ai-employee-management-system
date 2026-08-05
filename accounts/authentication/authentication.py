from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .jwt_handler import JWTHandler
from .constants import AUTH_HEADER_PREFIX

User = get_user_model()


class PyJWTAuthentication(BaseAuthentication):
    """
    Custom JWT Authentication for DRF.
    """

    def authenticate(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        parts = auth_header.split()

        if len(parts) != 2:
            raise AuthenticationFailed(
                "Invalid Authorization Header."
            )

        if parts[0] != AUTH_HEADER_PREFIX:
            raise AuthenticationFailed(
                "Invalid Authorization Prefix."
            )

        token = parts[1]

        try:

            payload = JWTHandler.decode_token(token)

            user = User.objects.get(
                id=payload["user_id"]
            )

            return (user, token)

        except User.DoesNotExist:

            raise AuthenticationFailed(
                "User not found."
            )

        except Exception as error:

            raise AuthenticationFailed(
                str(error)
            )