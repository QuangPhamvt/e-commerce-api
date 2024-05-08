from dotenv import dotenv_values
from enum import Enum

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
    "GOOGLE_LOGIN": "/google/login",
    "GOOGLE_CALLBACK": "/google/callback",
    "GOOGLE_LOGOUT": "/google/logout",
    "FACEBOOK_LOGIN": "/facebook/login",
    "FACEBOOK_CALLBACK": "/facebook/callback",
    "PROTECTED": "/protected",
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
    "GET_PRODUCTS_BY_TAG": "/tag/{id}",
    "SET_SERIES_TO_PRODUCT": "/{product_id}/series/{series_id}",
    "SET_CATEGORY_TO_PRODUCT": "/{product_id}/categories/{category_id}",
    "GET_PRODUCTS_BY_SERIES": "/series/{id}",
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
    "ADD_PRODUCT_TAGS": "/products",
    "BULK_TAGS": "/bulk",
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

# ********** Cart **********
CART: str = "Cart"
CART_PREFIX: str = "/carts"
CART_PATH: dict = {
    "GET_CART_BY_USER": "",
    "CREATE_CART": "",
    "DELETE_CART": "/{id}",
}
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
BUCKET_NAME = config.get("BUCKET_NAME") or "customafk-ecommerce-web-dev"
AWS_ACCESS_KEY_ID = config["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = config["AWS_SECRET_ACCESS_KEY"]
AWS_BUCKET_NAME = config.get("AWS_BUCKET_NAME") or "customafk-ecommerce-web"


# ********** Product Status **********
class ProductStatus(str, Enum):
    PRE_ORDER = "PRE-ORDER"
    IN_STOCK = "IN STOCK"
    OUT_OF_STOCK = "OUT OF STOCK"


# ********** Base URL **********
BASE_URL = "http://customafk.image/"
CLOUDFRONT_URL = config["CLOUDFRONT_URL"]
DOMAIN_API = config["DOMAIN_API"]

WEB_DOMAIN_URL = config.get("WEB_DOMAIN_URL") or ""

# ********** Oauth **********

#Google
GOOGLE_ID = config["GOOGLE_ID"]
GOOGLE_SECRET = config["GOOGLE_SECRET"]
#Facebook
FACEBOOK_ID = config["FACEBOOK_ID"]
FACEBOOK_SECRET = config["FACEBOOK_SECRET"]