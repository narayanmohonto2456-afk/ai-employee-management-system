from datetime import timedelta

# JWT Configuration

ACCESS_TOKEN_LIFETIME = timedelta(minutes=30)

REFRESH_TOKEN_LIFETIME = timedelta(days=1)

JWT_ALGORITHM = "HS256"

JWT_ISSUER = "Enterprise AI HRMS"

JWT_AUDIENCE = "Enterprise AI HRMS Users"

AUTH_HEADER_PREFIX = "Bearer"