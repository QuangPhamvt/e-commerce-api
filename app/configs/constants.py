from dotenv import dotenv_values


config = dotenv_values(".env")


# ********** Auth **********
AUTH: str = "Auth"
AUTH_PREFIX: str = "/auth"
AUTH_PATH: dict = {
    "SIGN_UP": "/signup",
    "VERIFY": "/verify",
    "SIGN_IN": "/sign-in",
    "LOG_OUT": "/logout",
    "REFRESH": "/refresh",
    "GET_ME": "/me",
    "FORGOT": "/forgot",
    "RESET": "/reset",
}
# ===========================


DB_PORT: int = 3306


# ********** DOCUMENTATIONS **********
TITLE: str = "E-Commerce API"
DESCRIPTION: str = """
E-Commerce API helps you do awsome stuff.

## Auth:

You can use this API to authenticate users.

- **Sign Up**: Create a new user.
- **Verify**: Verify user's email address by token.
- **Sign In**: Sign in with email and password.
- **Log Out**: Log out and revoke token.
- **Refresh**: Refresh token when it's expired.
- **Get Me**: Get user's information by token.

## Role:

You can use this API to manage roles.

- **Create Role**: Create a new role.

"""
SUMMARY: str = "This is a simple API for E-Commerce"
VERSION: str = "0.0.1"
DOCS_URL: str = "/docs"
ROOT_PATH: str = "/api/v1"
USERS: str = "User"
ADMIN: str = "Admin"

DOCUMENTATIONS: dict = {
    "title": TITLE,
    "summary": SUMMARY,
    "version": VERSION,
    "description": DESCRIPTION,
    "docs_url": DOCS_URL,
    "root_path": ROOT_PATH,
    "contact": {
        "name": "CustomAFK",
        "url": "https://github.com/QuangPhamvt",
        "email": "quangpm220503vt@gmail.com",
    },
    "openapi_tags": [
        {
            "name": AUTH,
            "description": "Auth endpoints usefull for user authentication.",
        },
        {"name": "Role", "description": "Role endpoints usefull for role management."},
    ],
}

DEFAULT_ROLE_NAME = "User"

# Token
ACCESS_TOKEN_SECRET = config["ACCESS_TOKEN_SECRET"]
ACCESS_TOKEN_EXPIRE = config["ACCESS_TOKEN_EXPIRE"]
REFRESH_TOKEN_SECRET = config["REFRESH_TOKEN_SECRET"]
REFRESH_TOKEN_EXPIRE = config["REFRESH_TOKEN_EXPIRE"]

# Forgot Password
FORGOT_CODE_EXPIRE = config["FORGOT_CODE_EXPIRE"]
