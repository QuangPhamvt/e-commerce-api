from app.configs.constants import CATEGORY, PRODUCT, SERIES, TAG

# ********** DOCUMENTATIONS **********
TITLE: str = "E-Commerce API for Definition"
DESCRIPTION: str = """
E-Commerce API for Authentication helps you do awesome stuff.

## Series:

You can use this API to get information about Series.

- **Get Series**: Get list of Series.

## Tag:

You can use this API to get information about Tag.

- **Get Tag**: Get list of Tag.

## Category:

You can use this API to get information about Category.

- **Get Category**: Get list of Category.

## Product:

You can use this API to get information about products.

- **Get List Products**: Get list of products.




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
            "name": SERIES,
            "description": "Series endpoints useful for Series information.",
        },
        {
            "name": TAG,
            "description": "Tag endpoints useful for Tag information.",
        },
        {
            "name": CATEGORY,
            "description": "Category endpoints useful for Category information.",
        },
        {
            "name": PRODUCT,
            "description": "Product endpoints useful for Product information.",
        },
    ],
}
