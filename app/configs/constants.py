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

# ********** User **********
USER: str = "User"
USER_PREFIX: str = "/users"
USER_PATH: dict = {"GET_LIST_USERS": "/", "CREATE_DEMO_USER": "/"}
# ===========================

# ********** Role **********
# ===========================

# ********** Product **********
PRODUCT: str = "Product"
PRODUCT_PREFIX: str = "/products"
PRODUCT_PATH: dict = {
    "GET_LIST_PRODUCTS": "/",
    "CREATE_PRODUCT": "/",
    "GET_PRODUCT": "/{product_id}",
    "UPDATE_PRODUCT": "/{product_id}",
    "DELETE_PRODUCT": "/{product_id}",
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

## Product:

You can use this API to manage products.
- **Get List Products**: Get list of products.
- **Create Product**: Create a new product.
- **Get Product**: Get a product by id.
- **Update Product**: Update a product by id.
- **Delete Product**: Delete a product by id.

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
        {"name": "User", "description": "User endpoints usefull for user management."},
        {
            "name": "Product",
            "description": "Product endpoints usefull for product management.",
        },
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

# ********** Create demo user **********
PHONE_NUMBER = "1234"
USERNAME = "ABC@@"

# ********** S3 **********

AWS_ACCESS_KEY_ID = config["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = config["AWS_SECRET_ACCESS_KEY"]
