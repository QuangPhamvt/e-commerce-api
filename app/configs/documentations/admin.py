from app.configs.constants import (
    CATEGORY,
    PRODUCT,
    ROLE,
    SERIES,
    TAG,
    DEPOSIT,
    EXCHANGE,
    USER,
)


# ********** DOCUMENTATIONS **********
TITLE: str = "E-Commerce API For Admin"
DESCRIPTION: str = """
E-Commerce API For Admin helps you do awesome stuff.



## Role:

You can use this API to manage roles.

- **Create Role**: Create a new role.
- **Get Role**: Get list of role.
- **Delete Role**: Delete a role.
- **Update Role**: Update a role.

## Series:

You can use this API to manage Series.

- **Create Series**: Create a new Series.
- **Get Series**: Get list of Series.
- **Delete Series**: Delete a Series.
- **Update Series**: Update a Series.

## Tag:

You can use this API to manage Tag.

- **Create Tag**: Create a new Tag.
- **Get Tag**: Get list of Tag.
- **Delete Tag**: Delete a Tag.

## Category:

- **Create Category**: Create a new Category.
- **Create Sub-Category**: Create a new Sub-Category.
- **Get Category**: Get list of Category.
- **Delete Category**: Delete a Category.
- **Delete Sub-Category**: Delete a Sub-Category.
- **Update Category**: Update a Category.

## Product:

You can use this API to manage products.
- **Get List Products**: Get list of products.
- **Create Product**: Create a new product.
- **Get Product**: Get a product by id.
- **Update Product**: Update a product by id.
- **Delete Product**: Delete a product by id.
- **Get List Products By Tag**: Get list of products by tag.
- **Set Series To Product**: Set series to product.
- **Get Products By Series**: Get list of products by series.

## Deposit:

You can use this API to manage deposit.
- **Get List Deposit**: Get list of deposit.
- **Create Deposit**: Create a new deposit.
- **Get Deposit**: Get a deposit by id.
- **Update Deposit**: Update a deposit by id.
- **Delete Deposit**: Delete a deposit by id.


## Exchange:

You can use this API to manage exchange.
- **Get List Exchange**: Get list of exchange.
- **Create Exchange**: Create a new exchange.
- **Get Exchange**: Get a exchange by id.
- **Update Exchange**: Update a exchange by id.
- **Delete Exchange**: Delete a exchange by id.

## User:

You can use this API to manage users.
- **Get List Users**: Get list of users.
- **Create Demo User**: Create a demo user.

"""
SUMMARY: str = "This is a simple API for E-Commerce"
VERSION: str = "0.0.1"
# DOCS_URL: str = "/docs"
# ROOT_PATH: str = "/api/v1"

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
        {"name": ROLE, "description": "Role endpoints useful for role management."},
        {
            "name": SERIES,
            "description": "Series endpoints useful for series management.",
        },
        {"name": TAG, "description": "Tag endpoints useful for tag management."},
        {
            "name": PRODUCT,
            "description": "Product endpoints useful for product management.",
        },
        {
            "name": CATEGORY,
            "description": "Category endpoints useful for category management.",
        },
        {
            "name": DEPOSIT,
            "description": "Deposit endpoints useful for deposit management.",
        },
        {
            "name": EXCHANGE,
            "description": "Exchange endpoints useful for exchange management.",
        },
        {
            "name": USER,
            "description": "User endpoints useful for user management.",
        },
    ],
}
