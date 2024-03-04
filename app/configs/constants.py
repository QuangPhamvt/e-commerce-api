from dotenv import dotenv_values


config = dotenv_values(".env")

TITLE: str = "E-Commerce API"
SUMMARY: str = "This is a simple API for E-Commerce"
VERSION: str = "0.0.1"
DOCS_URL: str = "/docs"
ROOT_PATH: str = "/api/v1"


AUTH: str = "Auth"
AUTH_PREFIX: str = "/auth"
AUTH_PATH: dict = {
    "SIGN_UP": "/signup",
    "VERIFY": "/verify",
    "SIGN_IN": "/sign-in",
    "LOG_OUT": "/logout",
    "REFRESH": "/refresh",
    "GET_ME": "/me",
}

USERS: str = "User"
ITEMS: str = "Item"
CUSTOM: str = "Custom"
ADMIN: str = "Admin"

DB_PORT: int = 3306

DOCUMENTATIONS: dict = {
    "title": TITLE,
    "summary": SUMMARY,
    "version": VERSION,
    "docs_url": DOCS_URL,
    "root_path": ROOT_PATH,
    "openapi_tags": [
        {
            "name": AUTH,
        },
        {
            "name": USERS,
        },
        {
            "name": ITEMS,
        },
        {
            "name": CUSTOM,
        },
        {"name": ADMIN},
    ],
}

DEFAULT_ROLE_NAME = "User"

# Token
ACCESS_TOKEN_SECRET = config["ACCESS_TOKEN_SECRET"]
ACCESS_TOKEN_EXPIRE = config["ACCESS_TOKEN_EXPIRE"]
REFRESH_TOKEN_SECRET = config["REFRESH_TOKEN_SECRET"]
REFRESH_TOKEN_EXPIRE = config["REFRESH_TOKEN_EXPIRE"]
