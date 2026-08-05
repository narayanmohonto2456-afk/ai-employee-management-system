import jwt

from datetime import datetime, timezone

from django.conf import settings

from .constants import (
    ACCESS_TOKEN_LIFETIME,
    REFRESH_TOKEN_LIFETIME,
    JWT_ALGORITHM,
    JWT_ISSUER,
    JWT_AUDIENCE,
)

from .exceptions import (
    InvalidToken,
    ExpiredToken,
)


class JWTHandler:
    """
    Handles JWT generation and validation.
    """

    @staticmethod
    def create_access_token(user):

        now = datetime.now(timezone.utc)

        payload = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "type": "access",
            "iat": now,
            "exp": now + ACCESS_TOKEN_LIFETIME,
            "iss": JWT_ISSUER,
            "aud": JWT_AUDIENCE,
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=JWT_ALGORITHM,
        )

    @staticmethod
    def create_refresh_token(user):

        now = datetime.now(timezone.utc)

        payload = {
            "user_id": user.id,
            "type": "refresh",
            "iat": now,
            "exp": now + REFRESH_TOKEN_LIFETIME,
            "iss": JWT_ISSUER,
            "aud": JWT_AUDIENCE,
        }

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=JWT_ALGORITHM,
        )

    @staticmethod
    def decode_token(token):

        try:

            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
                audience=JWT_AUDIENCE,
                issuer=JWT_ISSUER,
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise ExpiredToken()

        except jwt.InvalidTokenError:
            raise InvalidToken()