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

# ********** Product **********
PRODUCT: str = "Product"
PRODUCT_PREFIX: str = "/products"
PRODUCT_PATH: dict = {
    "GET_LIST_PRODUCTS": "",
    "CREATE_PRODUCT": "",
    "GET_PRODUCT": "/{id}",
    "UPDATE_PRODUCT": "/{id}",
    "DELETE_PRODUCT": "/{id}",
    "GET_PRODUCTS_BY_TAG": "/tag/{tag_name}",
}
# ===========================

# ********** Category **********
CATEGORY: str = "Category"
CATEGORY_PREFIX: str = "/categories"
CATEGORY_PATH: dict = {
    "GET_LIST_CATEGORIES": "",
}
# ===========================

# ********** Series **********
SERIES: str = "Series"
SERIES_PREFIX: str = "/series"
SERIES_PATH: dict = {
    "GET_LIST_SERIES": "",
}
# ===========================

# ********** Tag **********
TAG: str = "Tag"
TAG_PREFIX: str = "/tags"
TAG_PATH: dict = {
    "GET_LIST_TAG": "",
    "CREATE_TAG": "",
    "DELETE_TAG": "/{id}",
    "ADD_PRODUCT_TAGS": "/products/{id}",
}
# ===========================

# ********** Role **********
ROLE: str = "Role"
ROLE_PREFIX: str = "/roles"
ROLE_PATH: dict = {
    "GET_LIST_ROLES": "",
    "CREATE_ROLE": "",
    "DELETE_ROLE": "/{id}",
    "UPDATE_ROLE": "/{id}",
}
# ===========================

# ********** Deposit **********
DEPOSIT: str = "Deposit"
DEPOSIT_PREFIX: str = "/deposits"
DEPOSIT_PATH: dict = {
    "GET_LIST_DEPOSIT": "",
    "CREATE_DEPOSIT": "",
    "GET_DEPOSIT_BY_ID": "/{id}",
    "DELETE_DEPOSIT": "/{id}",
    "UPDATE_DEPOSIT": "/{id}",
}
# ===========================

# ********** Exchange **********
EXCHANGE: str = "Exchange"
EXCHANGE_PREFIX: str = "/exchanges"
EXCHANGE_PATH: dict = {
    "GET_LIST_EXCHANGE": "",
    "CREATE_EXCHANGE": "",
    "GET_EXCHANGE_BY_ID": "/{id}",
    "DELETE_EXCHANGE": "/{id}",
    "UPDATE_EXCHANGE": "/{id}",
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
            "description": "Auth endpoints useful for user authentication.",
        },
        {"name": ROLE, "description": "Role endpoints useful for role management."},
        {"name": USER, "description": "User endpoints useful for user management."},
        {
            "name": "Product",
            "description": "Product endpoints useful for product management.",
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
