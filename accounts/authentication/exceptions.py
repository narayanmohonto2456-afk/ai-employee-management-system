class AuthenticationError(Exception):
    """Base authentication exception."""
    pass


class InvalidToken(AuthenticationError):
    """Raised when a JWT token is invalid."""
    pass


class ExpiredToken(AuthenticationError):
    """Raised when a JWT token has expired."""
    pass


class BlacklistedToken(AuthenticationError):
    """Raised when a JWT token has been blacklisted."""
    pass


class EmailNotVerified(AuthenticationError):
    """Raised when a user's email is not verified."""
    pass