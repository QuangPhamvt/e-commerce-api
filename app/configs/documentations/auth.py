from app.configs.constants import AUTH

# ********** DOCUMENTATIONS **********

TITLE: str = "E-Commerce API for Authentication"
DESCRIPTION: str = """
E-Commerce API for Authentication helps you do awesome stuff.

## Auth:

You can use this API to authenticate users.

- **Sign Up**: Create a new user.
- **Verify**: Verify user's email address by token.
- **Sign In**: Sign in with email and password.
- **Log Out**: Log out and revoke token.
- **Refresh**: Refresh token when it's expired.
- **Get Me**: Get user's information by token.



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
    # "root_path": ROOT_PATH,
    "contact": {
        "name": "CustomAFK",
        "url": "https://github.com/QuangPhamvt",
        "email": "quangpm220503vt@gmail.com",
    },
    "openapi_tags": [
        {
            "name": AUTH,
            "description": "Auth endpoints useful for user authentication.",
        },
    ],
}
